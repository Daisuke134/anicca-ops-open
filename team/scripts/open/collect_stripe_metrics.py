#!/usr/bin/env python3
"""Collect a public-safe, read-only Stripe metrics feed for /open."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable


API_VERSION = "2026-04-22.dahlia"
WINDOW_DAYS = 90
PAGE_SIZE = 100
RequestGet = Callable[[str, list[tuple[str, str]]], dict[str, Any]]


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("collection time must include a timezone")
    return value.astimezone(timezone.utc)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _blank_endpoint() -> dict[str, Any]:
    return {"status": "unavailable", "records": None, "complete": False}


def _blank_feed(observed_at: str, reason: str) -> dict[str, Any]:
    endpoints = ("balance", "subscriptions_active", "subscriptions_trialing", "balance_transactions", "refunds", "payouts")
    return {
        "source": "Stripe API",
        "status": "unavailable",
        "reason": reason,
        "observed_at": observed_at,
        "window": None,
        "balance": {"status": "unavailable", "currencies": []},
        "subscriptions": {"status": "unavailable", "currencies": [], "unclassified_count": None},
        "balance_transactions": {"status": "unavailable", "currencies": [], "daily": []},
        "refunds": {"status": "unavailable", "currencies": []},
        "payouts": {"status": "unavailable", "currencies": []},
        "coverage": {name: _blank_endpoint() for name in endpoints},
    }


def _request_get(key: str, path: str, params: list[tuple[str, str]]) -> dict[str, Any]:
    query = urllib.parse.urlencode(params)
    token = base64.b64encode(f"{key}:".encode("utf-8")).decode("ascii")
    request = urllib.request.Request(
        f"https://api.stripe.com{path}?{query}" if query else f"https://api.stripe.com{path}",
        headers={
            "Authorization": f"Basic {token}",
            "Stripe-Version": API_VERSION,
            "User-Agent": "Anicca-Open-Stripe-Metrics/1.0",
        },
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Stripe response is not an object")
    return value


def _paginate(
    request_get: RequestGet,
    path: str,
    params: list[tuple[str, str]],
) -> tuple[list[dict[str, Any]], bool, int, str | None]:
    records: list[dict[str, Any]] = []
    invalid_rows = 0
    cursor: str | None = None
    seen_cursors: set[str] = set()
    while True:
        page_params = [*params, ("limit", str(PAGE_SIZE))]
        if cursor:
            page_params.append(("starting_after", cursor))
        try:
            page = request_get(path, page_params)
        except Exception as error:  # provider text may contain private data; keep only the class name
            return records, False, invalid_rows, type(error).__name__
        if not isinstance(page, dict) or not isinstance(page.get("data"), list):
            return records, False, invalid_rows, "MalformedResponse"
        data = page["data"]
        clean = [row for row in data if isinstance(row, dict)]
        invalid_rows += len(data) - len(clean)
        records.extend(clean)
        if page.get("has_more") is not True:
            return records, True, invalid_rows, None
        if not clean:
            return records, False, invalid_rows, "PaginationCursorMissing"
        next_cursor = clean[-1].get("id")
        if not isinstance(next_cursor, str) or not next_cursor or next_cursor in seen_cursors:
            return records, False, invalid_rows, "PaginationCursorInvalid"
        seen_cursors.add(next_cursor)
        cursor = next_cursor


def _status(complete: bool, records: int, invalid_rows: int = 0) -> str:
    if not complete or invalid_rows:
        return "partial"
    return "observed" if records else "observed_empty"


def _page_status(complete: bool, records: int, invalid_rows: int, error_type: str | None) -> str:
    if error_type and records == 0 and invalid_rows == 0:
        return "unavailable"
    return _status(complete, records, invalid_rows)


def _currency(value: Any) -> str | None:
    if not isinstance(value, str) or re.fullmatch(r"[a-zA-Z]{3}", value) is None:
        return None
    return value.upper()


def _integer(value: Any, *, signed: bool = True) -> int | None:
    if not isinstance(value, int) or isinstance(value, bool):
        return None
    if not signed and value < 0:
        return None
    return value


def _safe_label(value: Any, fallback: str = "other") -> str:
    if not isinstance(value, str):
        return fallback
    candidate = value.lower()
    return candidate if re.fullmatch(r"[a-z0-9_]{1,40}", candidate) else fallback


def _subscription_currency(row: dict[str, Any]) -> str | None:
    direct = _currency(row.get("currency"))
    if direct:
        return direct
    items = row.get("items")
    data = items.get("data") if isinstance(items, dict) else None
    currencies = {
        _currency((item.get("price") or {}).get("currency"))
        for item in data or []
        if isinstance(item, dict) and isinstance(item.get("price"), dict)
    }
    currencies.discard(None)
    return next(iter(currencies)) if len(currencies) == 1 else None


def _aggregate_balance(value: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    if not isinstance(value, dict):
        return {"status": "unavailable", "currencies": []}, {"status": "unavailable", "records": None, "complete": False, "error_type": "MalformedResponse"}
    totals: dict[str, dict[str, int]] = defaultdict(lambda: {"available_minor": 0, "pending_minor": 0})
    invalid_rows = 0
    record_count = 0
    field_complete = {"available_minor": True, "pending_minor": True}
    for field, target in (("available", "available_minor"), ("pending", "pending_minor")):
        rows = value.get(field)
        if not isinstance(rows, list):
            invalid_rows += 1
            field_complete[target] = False
            continue
        for row in rows:
            if not isinstance(row, dict):
                invalid_rows += 1
                field_complete[target] = False
                continue
            currency, amount = _currency(row.get("currency")), _integer(row.get("amount"))
            if currency is None or amount is None:
                invalid_rows += 1
                field_complete[target] = False
                continue
            totals[currency][target] += amount
            record_count += 1
    status = _status(invalid_rows == 0, record_count, invalid_rows)
    endpoint = {"status": status, "records": record_count, "complete": invalid_rows == 0}
    currencies = []
    for currency in sorted(totals):
        row: dict[str, Any] = {"currency": currency, **totals[currency]}
        for field, complete in field_complete.items():
            if not complete:
                row[field] = None
        currencies.append(row)
    return {"status": status, "currencies": currencies}, endpoint


def _time_params(start: datetime, end: datetime) -> list[tuple[str, str]]:
    return [
        ("created[gte]", str(int(start.timestamp()))),
        ("created[lte]", str(int(end.timestamp()))),
    ]


def _aggregate_subscriptions(
    request_get: RequestGet,
    status_name: str,
    endpoint_name: str,
) -> tuple[dict[str, int], dict[str, Any], int]:
    records, complete, malformed, error_type = _paginate(
        request_get, "/v1/subscriptions", [("status", status_name)]
    )
    counts: dict[str, int] = defaultdict(int)
    unclassified = 0
    for row in records:
        currency = _subscription_currency(row)
        if row.get("status") != status_name or currency is None:
            unclassified += 1
            continue
        counts[currency] += 1
    invalid_rows = malformed + unclassified
    endpoint_status = _page_status(complete, len(records), invalid_rows, error_type)
    endpoint: dict[str, Any] = {
        "status": endpoint_status,
        "records": len(records) if complete else None,
        "complete": complete and invalid_rows == 0,
    }
    if error_type:
        endpoint["error_type"] = error_type
    return counts, endpoint, unclassified


def _aggregate_transactions(
    records: list[dict[str, Any]],
    *,
    complete: bool,
    invalid_rows: int,
    error_type: str | None,
    start: datetime,
    end: datetime,
) -> tuple[dict[str, Any], dict[str, Any]]:
    currencies: dict[str, dict[str, int]] = defaultdict(lambda: {"count": 0, "amount_minor": 0, "fee_minor": 0, "net_minor": 0})
    daily: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    malformed = invalid_rows
    for row in records:
        currency = _currency(row.get("currency"))
        amount = _integer(row.get("amount"))
        fee = _integer(row.get("fee"), signed=False)
        net = _integer(row.get("net"))
        created = _integer(row.get("created"), signed=False)
        if currency is None or amount is None or fee is None or net is None or created is None:
            malformed += 1
            continue
        try:
            occurred = datetime.fromtimestamp(created, timezone.utc)
        except (OSError, OverflowError, ValueError):
            malformed += 1
            continue
        if occurred < start or occurred > end:
            malformed += 1
            continue
        category = _safe_label(row.get("reporting_category"))
        kind = _safe_label(row.get("type"))
        total = currencies[currency]
        total["count"] += 1
        total["amount_minor"] += amount
        total["fee_minor"] += fee
        total["net_minor"] += net
        date = occurred.date().isoformat()
        key = (date, currency, category, kind)
        bucket = daily.setdefault(key, {"date": date, "currency": currency, "reporting_category": category, "type": kind, "count": 0, "amount_minor": 0, "fee_minor": 0, "net_minor": 0})
        bucket["count"] += 1
        bucket["amount_minor"] += amount
        bucket["fee_minor"] += fee
        bucket["net_minor"] += net
    status = _page_status(complete, len(records), malformed, error_type)
    endpoint: dict[str, Any] = {"status": status, "records": len(records) if complete else None, "complete": complete and malformed == 0}
    if error_type:
        endpoint["error_type"] = error_type
    return {
        "status": status,
        "currencies": [{"currency": code, **currencies[code]} for code in sorted(currencies)],
        "daily": [daily[key] for key in sorted(daily)],
    }, endpoint


def _aggregate_status_rows(
    endpoint_name: str,
    records: list[dict[str, Any]],
    *,
    complete: bool,
    invalid_rows: int,
    error_type: str | None,
    start: datetime,
    end: datetime,
) -> tuple[dict[str, Any], dict[str, Any]]:
    grouped: dict[str, dict[str, dict[str, int]]] = defaultdict(lambda: defaultdict(lambda: {"count": 0, "amount_minor": 0}))
    malformed = invalid_rows
    for row in records:
        currency = _currency(row.get("currency"))
        amount = _integer(row.get("amount"), signed=False)
        created = _integer(row.get("created"), signed=False)
        if currency is None or amount is None or created is None:
            malformed += 1
            continue
        try:
            occurred = datetime.fromtimestamp(created, timezone.utc)
        except (OSError, OverflowError, ValueError):
            malformed += 1
            continue
        if occurred < start or occurred > end:
            malformed += 1
            continue
        status = _safe_label(row.get("status"))
        bucket = grouped[currency][status]
        bucket["count"] += 1
        bucket["amount_minor"] += amount
    status = _page_status(complete, len(records), malformed, error_type)
    endpoint: dict[str, Any] = {"status": status, "records": len(records) if complete else None, "complete": complete and malformed == 0}
    if error_type:
        endpoint["error_type"] = error_type
    return {
        "status": status,
        "currencies": [
            {"currency": currency, "statuses": [{"status": label, **grouped[currency][label]} for label in sorted(grouped[currency])]}
            for currency in sorted(grouped)
        ],
    }, endpoint


def collect(key: str | None, request_get: RequestGet, now: datetime) -> dict[str, Any]:
    """Return provider-safe aggregates; never return a Stripe object or identifier."""
    end = _utc(now)
    observed_at = _iso(end)
    if not isinstance(key, str) or not key.startswith("rk_live_"):
        reason = "restricted_read_key_missing" if not key else "restricted_live_key_required"
        return _blank_feed(observed_at, reason)
    start = end - timedelta(days=WINDOW_DAYS)
    feed = _blank_feed(observed_at, "")
    feed["reason"] = None
    feed["status"] = "observed"
    feed["window"] = {"start": _iso(start), "end": _iso(end), "days": WINDOW_DAYS, "timezone": "UTC"}

    try:
        balance_raw = request_get("/v1/balance", [])
        feed["balance"], feed["coverage"]["balance"] = _aggregate_balance(balance_raw)
    except Exception as error:
        feed["balance"] = {"status": "unavailable", "currencies": []}
        feed["coverage"]["balance"] = {"status": "unavailable", "records": None, "complete": False, "error_type": type(error).__name__}

    subscription_counts: dict[str, dict[str, int]] = defaultdict(lambda: {"active": 0, "trialing": 0})
    unclassified_total = 0
    for status_name in ("active", "trialing"):
        endpoint_name = f"subscriptions_{status_name}"
        counts, endpoint, unclassified = _aggregate_subscriptions(request_get, status_name, endpoint_name)
        feed["coverage"][endpoint_name] = endpoint
        unclassified_total += unclassified
        for currency, count in counts.items():
            subscription_counts[currency][status_name] += count
    subscription_statuses = [feed["coverage"][f"subscriptions_{status_name}"]["status"] for status_name in ("active", "trialing")]
    active_complete = subscription_statuses[0] in {"observed", "observed_empty"}
    trialing_complete = subscription_statuses[1] in {"observed", "observed_empty"}
    feed["subscriptions"] = {
        "status": "partial" if any(status not in {"observed", "observed_empty"} for status in subscription_statuses) else ("observed" if any(status == "observed" for status in subscription_statuses) else "observed_empty"),
        "currencies": [
            {"currency": currency,
             "active": subscription_counts[currency]["active"] if active_complete else None,
             "trialing": subscription_counts[currency]["trialing"] if trialing_complete else None}
            for currency in sorted(subscription_counts)
        ],
        "unclassified_count": unclassified_total if active_complete and trialing_complete else None,
    }

    window_params = _time_params(start, end)
    tx_records, tx_complete, tx_invalid, tx_error = _paginate(request_get, "/v1/balance_transactions", window_params)
    feed["balance_transactions"], feed["coverage"]["balance_transactions"] = _aggregate_transactions(
        tx_records, complete=tx_complete, invalid_rows=tx_invalid, error_type=tx_error, start=start, end=end
    )
    for endpoint_name, path, target in (
        ("refunds", "/v1/refunds", "refunds"),
        ("payouts", "/v1/payouts", "payouts"),
    ):
        records, complete, invalid_rows, error_type = _paginate(request_get, path, window_params)
        feed[target], feed["coverage"][endpoint_name] = _aggregate_status_rows(
            endpoint_name, records, complete=complete, invalid_rows=invalid_rows, error_type=error_type, start=start, end=end
        )

    endpoint_statuses = [value["status"] for value in feed["coverage"].values()]
    if all(status == "unavailable" for status in endpoint_statuses):
        feed["status"] = "unavailable"
    elif any(status not in {"observed", "observed_empty"} for status in endpoint_statuses):
        feed["status"] = "partial"
    return feed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    key = os.environ.get("OPEN_STRIPE_READ_KEY")
    feed = collect(key, lambda path, params: _request_get(key or "", path, params), now)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(feed, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Stripe metrics feed: {feed['status']} at {feed['observed_at']}")


if __name__ == "__main__":
    main()
