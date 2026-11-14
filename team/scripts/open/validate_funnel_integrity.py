#!/usr/bin/env python3
"""
validate_funnel_integrity.py - Funnel definition integrity gate (Issue #51).

Companion to validate_funnel_monotonic.py (Pickle, Issue #52), which guards
stage monotonicity inside the store funnel file. This checker guards the
three mixing failure modes fixed by the canonical funnel definition
(Daisuke134/anicca-ops files/full-funnel-spec-and-data-2026-11-12.md v3):

  1. WINDOW_MIXING  - every funnel block in one artifact must use the same
     window, and the canonical window length is 7 days. A 28-day store
     block next to a 7-day in-app block (the 2026-11-12 incident shape:
     28d ASC downloads joined to a different-period in-app cohort) fails.
  2. INVERSION      - inside one block (one chain), stage counts must be
     non-increasing. A later stage larger than an earlier stage fails.
  3. SOURCE_MIXING  - one chain must come from one measurement system.
     Canonical sources per stage kind (v3): store stages (impressions /
     product page views / first-time downloads) = App Store Connect;
     in-app cohort stages = Mixpanel (production only); purchase /
     trial / churn stages = RevenueCat cross-checked with ASC.
     A single chain mixing ASC and Mixpanel stages fails, a store stage
     not sourced from ASC fails, and any installs/units/downloads figure
     sourced from RevenueCat fails anywhere in the artifact (RC "new
     customers" must never be presented as installs).

Accepted inputs:
  A) Funnel artifact JSON:
     {"apps": [{"app": "Anicca",
                "window": {"start": "2026-11-04", "end": "2026-11-10"},
                "blocks": [{"kind": "store", "source": "ASC",
                            "stages": [{"key": "impressions", "count": 334},
                                       ...]},
                           {"kind": "in_app", "source": "Mixpanel",
                            "stages": [...]}]}]}
     Per-stage "source" overrides the block source.
  B) /open data.json: product_analytics.<app>.funnel blocks are extracted
     (steps[].distinct_users, data_from/data_to, source) and checked as
     in-app blocks.

Exit code: 0 = pass, 1 = violations found, 2 = input unreadable.
Usage: validate_funnel_integrity.py <file.json> [--window-days 7]
"""

import argparse
import datetime as dt
import json
import pathlib
import sys

WINDOW_MIXING = "WINDOW_MIXING"
INVERSION = "INVERSION"
SOURCE_MIXING = "SOURCE_MIXING"

STORE_STAGE_KEYS = {"impressions", "page_views", "product_page_views",
                    "downloads", "first_time_downloads", "units", "installs"}
PURCHASE_STAGE_KEYS = {"paywall_views", "paywall_view", "purchase_start",
                       "purchase_complete", "trial_start", "trials",
                       "purchases", "churn", "cancellations"}
CANONICAL_SOURCE = {
    "store": {"asc", "app store connect", "appstoreconnect"},
    "in_app": {"mixpanel"},
    "purchase": {"revenuecat", "asc", "app store connect", "appstoreconnect"},
}


def _norm_source(s):
    return str(s or "").strip().lower()


def _stage_source(stage, block):
    return _norm_source(stage.get("source") or block.get("source") or "")


def _stage_kind(stage, block):
    if block.get("kind") in ("store", "in_app", "purchase"):
        return block["kind"]
    key = str(stage.get("key") or "")
    if key in STORE_STAGE_KEYS:
        return "store"
    if key in PURCHASE_STAGE_KEYS:
        return "purchase"
    return "in_app"


def _window_of(block_or_app, fallback=None):
    w = block_or_app.get("window") or fallback or {}
    start = w.get("start") or block_or_app.get("data_from")
    end = w.get("end") or block_or_app.get("data_to")
    days = w.get("days") or block_or_app.get("window_days")
    if start and end:
        try:
            d0 = dt.date.fromisoformat(str(start)[:10])
            d1 = dt.date.fromisoformat(str(end)[:10])
            return (str(d0), str(d1), (d1 - d0).days + 1)
        except ValueError:
            return (str(start), str(end), None)
    if days:
        return (None, None, int(days))
    return None


def check_artifact(art, window_days=7):
    """Return a list of violations: dicts with code/app/block/detail."""
    violations = []

    def add(code, app, block, detail):
        violations.append({"code": code, "app": app, "block": block,
                           "detail": detail})

    apps = art.get("apps")
    if apps is None:
        apps = _extract_open_datajson(art)
    windows_seen = {}

    for app_entry in apps or []:
        app = app_entry.get("app", "Unknown")
        app_window_raw = app_entry.get("window")
        for block in app_entry.get("blocks", []):
            bname = block.get("kind") or block.get("name") or "block"
            win = _window_of(block, app_window_raw)
            if win is None:
                add(WINDOW_MIXING, app, bname,
                    "funnel block declares no window; v3 requires an explicit "
                    "fixed window on every block")
            else:
                windows_seen.setdefault(win, []).append(f"{app}/{bname}")
                if win[2] is not None and win[2] != window_days:
                    add(WINDOW_MIXING, app, bname,
                        f"window length {win[2]}d != canonical {window_days}d "
                        f"({win[0]}..{win[1]})")
            stages = block.get("stages") or block.get("steps") or []
            prev = None
            prev_key = None
            chain_sources = set()
            for st in stages:
                count = st.get("count", st.get("distinct_users"))
                key = st.get("key") or st.get("label") or "?"
                src = _stage_source(st, block)
                if src:
                    chain_sources.add(src)
                kind = _stage_kind(st, block)
                canon = CANONICAL_SOURCE.get(kind, set())
                if src and canon and not any(c in src for c in canon):
                    add(SOURCE_MIXING, app, bname,
                        f"stage '{key}' (kind={kind}) sourced from "
                        f"'{st.get('source') or block.get('source')}', "
                        f"canonical source is {sorted(canon)}")
                if count is not None:
                    if prev is not None and count > prev:
                        add(INVERSION, app, bname,
                            f"stage '{key}' count {count} > earlier stage "
                            f"'{prev_key}' count {prev} in the same chain")
                    prev = count
                    prev_key = key
            if len(chain_sources) > 1:
                add(SOURCE_MIXING, app, bname,
                    f"single chain mixes measurement systems: "
                    f"{sorted(chain_sources)} (v3: store chain and in-app "
                    f"chain are separate blocks, never one chain)")

    distinct_windows = {w for w in windows_seen if w[2] is not None}
    if len(distinct_windows) > 1:
        add(WINDOW_MIXING, "*", "*",
            f"artifact mixes windows across blocks: "
            f"{sorted(str(w) for w in distinct_windows)}")

    for path, src in _scan_install_sources(art):
        if "revenuecat" in _norm_source(src):
            add(SOURCE_MIXING, "*", path,
                "installs/units/downloads figure sourced from RevenueCat; "
                "installs are App Store Connect first-time downloads only")
    return violations


INSTALL_KEYS = {"installs", "units", "downloads", "first_time_downloads"}


def _scan_install_sources(node, path="$"):
    hits = []
    if isinstance(node, dict):
        for k, v in node.items():
            if str(k).lower() in INSTALL_KEYS:
                if isinstance(v, dict) and v.get("source"):
                    hits.append((f"{path}.{k}", v.get("source")))
                elif node.get("source"):
                    hits.append((path, node.get("source")))
            hits.extend(_scan_install_sources(v, f"{path}.{k}"))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            hits.extend(_scan_install_sources(v, f"{path}[{i}]"))
    return hits


def _extract_open_datajson(d):
    apps = []
    pa = d.get("product_analytics") or {}
    for app_key, entry in pa.items():
        funnel = (entry or {}).get("funnel") or {}
        steps = funnel.get("steps") or []
        if not steps:
            continue
        stages = [{"key": s.get("label") or f"step{i}",
                   "count": s.get("distinct_users")}
                  for i, s in enumerate(steps)]
        apps.append({
            "app": app_key,
            "window": {"start": funnel.get("data_from"),
                       "end": funnel.get("data_to")},
            "blocks": [{"kind": "in_app",
                        "source": funnel.get("source") or entry.get("source"),
                        "stages": stages}],
        })
    return apps


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--window-days", type=int, default=7)
    args = ap.parse_args(argv)
    p = pathlib.Path(args.file)
    if not p.exists():
        print(f"FAIL: file not found: {p}")
        return 2
    try:
        art = json.loads(p.read_text())
    except Exception as e:
        print(f"FAIL: unreadable JSON: {e}")
        return 2
    violations = check_artifact(art, window_days=args.window_days)
    if violations:
        for v in violations:
            print(f"VIOLATION [{v['code']}] app={v['app']} "
                  f"block={v['block']}: {v['detail']}")
        print(f"FAIL: {len(violations)} funnel integrity violation(s); "
              f"do not publish")
        return 1
    print("OK: funnel integrity checks passed "
          f"(window={args.window_days}d fixed, no inversion, no source mixing)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
