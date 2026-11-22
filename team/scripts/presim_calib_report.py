"""Pre-simulation calibration report: median abs log error by format."""

import csv
import json
import math
import statistics
import sys
from datetime import datetime, timedelta


def _as_positive_float(value):
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number <= 0:
        return None
    return number


def _median_abs_ln_err(errors):
    if not errors:
        return None
    return float(statistics.median(errors))


def _loo_bias(rows):
    residuals = []
    for row in rows:
        pred = _as_positive_float(row.get("pred_impr"))
        actual = _as_positive_float(row.get("actual_impr"))
        if pred is None or actual is None:
            continue
        residuals.append(math.log(actual) - math.log(pred))

    n = len(residuals)
    result = {
        "n": n,
        "multiplier": None,
        "median_abs_ln_err_raw": None,
        "median_abs_ln_err_loo": None,
    }
    if n < 2:
        return result

    center = statistics.median(residuals)
    result["multiplier"] = float(math.exp(center))
    result["median_abs_ln_err_raw"] = float(statistics.median(abs(r) for r in residuals))
    loo_errors = []
    for i, r in enumerate(residuals):
        others = residuals[:i] + residuals[i + 1:]
        loo_errors.append(abs(r - statistics.median(others)))
    result["median_abs_ln_err_loo"] = float(statistics.median(loo_errors))
    return result


def report(rows, bias=False):
    overall_errors = []
    by_format_errors = {}

    for row in rows:
        pred = _as_positive_float(row.get("pred_impr"))
        actual = _as_positive_float(row.get("actual_impr"))
        if pred is None or actual is None:
            continue
        fmt = row.get("format")
        if fmt is None or str(fmt).strip() == "":
            fmt = "other"
        else:
            fmt = str(fmt).strip()
        error = abs(math.log(pred) - math.log(actual))
        overall_errors.append(error)
        by_format_errors.setdefault(fmt, []).append(error)

    out = {
        "overall": {
            "n": len(overall_errors),
            "median_abs_ln_err": _median_abs_ln_err(overall_errors),
        },
        "by_format": {
            fmt: {"n": len(errors), "median_abs_ln_err": _median_abs_ln_err(errors)}
            for fmt, errors in by_format_errors.items()
        },
    }
    if bias:
        out["loo_bias"] = _loo_bias(rows)
    return out


TS_FORMAT = "%Y-%m-%d %H:%M"


def _parse_ts(value):
    if value is None:
        return None
    try:
        return datetime.strptime(str(value).strip(), TS_FORMAT)
    except ValueError:
        return None


TS_FORMATS = (TS_FORMAT, "%Y-%m-%d %H:%M:%S")


def _parse_ts_loose(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    for fmt in TS_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


_ACTUAL_IMPR_KEYS = ("actual_impr", "actual_impressions", "impressions", "actual")


def _has_actual_impressions(row):
    for key in _ACTUAL_IMPR_KEYS:
        if _as_positive_float(row.get(key)) is not None:
            return True
    return False


def _parse_hours(value):
    try:
        hours = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(hours) or hours <= 0:
        return None
    return hours


def pending(rows, hours, now=None):
    out = []
    for row in rows:
        if _has_actual_impressions(row):
            continue
        ts_raw = row.get("ts")
        if ts_raw is None or str(ts_raw).strip() == "":
            ts_raw = row.get("ts_jst")
        ts = _parse_ts_loose(ts_raw)
        if ts is None:
            continue
        if now is not None:
            ref = now
            if ts.tzinfo is not None and ref.tzinfo is None:
                ref = ref.replace(tzinfo=ts.tzinfo)
        elif ts.tzinfo is not None:
            ref = datetime.now(ts.tzinfo)
        else:
            ref = datetime.now()
        if ts >= ref - timedelta(hours=hours):
            continue
        text = row.get("text")
        out.append({
            "ts": ts_raw,
            "id": row.get("id"),
            "text": "" if text is None else str(text)[:60],
        })
    return out


def _parse_args(argv):
    bias = False
    since = None
    pending_hours = None
    i = 2
    while i < len(argv):
        arg = argv[i]
        if arg == "--bias" and not bias:
            bias = True
            i += 1
        elif arg == "--since" and since is None and i + 1 < len(argv):
            since = argv[i + 1]
            i += 2
        elif arg == "--pending" and pending_hours is None and i + 1 < len(argv):
            pending_hours = _parse_hours(argv[i + 1])
            if pending_hours is None:
                return None
            i += 2
        else:
            return None
    if since is not None and _parse_ts(since) is None:
        return None
    return bias, since, pending_hours


def _usage(argv):
    print(
        f'usage: {argv[0]} <csv> [--bias] [--since "YYYY-MM-DD HH:MM"] [--pending HOURS]',
        file=sys.stderr,
    )


def main(argv):
    if len(argv) < 2:
        _usage(argv)
        return 2
    parsed = _parse_args(argv)
    if parsed is None:
        _usage(argv)
        return 2
    bias, since, pending_hours = parsed
    with open(argv[1], newline="") as fh:
        rows = list(csv.DictReader(fh))
    if since is not None:
        cutoff = _parse_ts(since)
        rows = [
            row for row in rows
            if (ts := _parse_ts(row.get("ts_jst"))) is not None and ts >= cutoff
        ]
    if pending_hours is not None:
        print(json.dumps(pending(rows, pending_hours)))
        return 0
    print(json.dumps(report(rows, bias=bias)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
