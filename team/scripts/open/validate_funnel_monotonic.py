#!/usr/bin/env python3
"""
validate_funnel_monotonic.py - Enforce monotonic non-increasing property on full funnel data.
Prevents publishing logical contradictions (e.g. later step > earlier step, DL 14 -> in-app 23).
Spec: Daisuke134/anicca-ops files/full-funnel-spec-and-data-2026-11-12.md & Issue #51/#52.
"""

import json
import sys
import pathlib

class FunnelInconsistencyError(Exception):
    pass

def validate_app_funnel(app_data):
    name = app_data.get("app", "Unknown")
    asc = app_data.get("asc", {})
    rc = app_data.get("revenuecat", {})

    impressions = asc.get("impressions")
    page_views = asc.get("page_views")
    downloads = asc.get("first_time_downloads")

    # Step 1: Impressions >= Page Views
    if impressions is not None and page_views is not None:
        if page_views > impressions:
            raise FunnelInconsistencyError(
                f"[{name}] Contradiction: page_views ({page_views}) > impressions ({impressions})"
            )

    # Step 2: Page Views >= First-Time Downloads
    if page_views is not None and downloads is not None:
        if downloads > page_views:
            raise FunnelInconsistencyError(
                f"[{name}] Contradiction: first_time_downloads ({downloads}) > page_views ({page_views})"
            )

    # Step 3: In-app cohort check (if present)
    # If in-app onboarding or active new cohort is reported, it must not exceed downloads for the same cohort window
    in_app_starts = app_data.get("in_app_starts")
    if in_app_starts is not None and downloads is not None:
        if in_app_starts > downloads:
            raise FunnelInconsistencyError(
                f"[{name}] Contradiction: in_app_starts ({in_app_starts}) > first_time_downloads ({downloads}) for same cohort"
            )

    # Step 4: Paywall views / trial starts
    paywall_views = app_data.get("paywall_views")
    if paywall_views is not None and in_app_starts is not None:
        if paywall_views > in_app_starts:
            raise FunnelInconsistencyError(
                f"[{name}] Contradiction: paywall_views ({paywall_views}) > in_app_starts ({in_app_starts})"
            )

    return True

def validate_store_funnel_file(path):
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Funnel file not found: {path}")

    data = json.loads(p.read_text())
    apps = data.get("apps", [])
    if not apps:
        raise FunnelInconsistencyError(f"No apps found in funnel file: {path}")

    for app in apps:
        validate_app_funnel(app)

    print(f"SUCCESS: Funnel monotonic validation passed for {len(apps)} apps in {path}")
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "/workspace/team/scripts/open/site/store_funnel.json"
    try:
        validate_store_funnel_file(target)
        sys.exit(0)
    except Exception as e:
        print(f"FAIL CLOSED: {e}", file=sys.stderr)
        sys.exit(1)
