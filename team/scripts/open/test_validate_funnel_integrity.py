#!/usr/bin/env python3
"""Tests for validate_funnel_integrity.py (Issue #51).

Fixtures: the canonical v3 funnel (anicca-ops
files/full-funnel-spec-and-data-2026-11-12.md, window 2026-11-04..11-10)
must PASS; intentionally mixed data must FAIL with the expected code.
Run: python3 -m pytest test_validate_funnel_integrity.py
     (or plain python3 test_validate_funnel_integrity.py)
"""
import copy
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from validate_funnel_integrity import check_artifact, WINDOW_MIXING, INVERSION, SOURCE_MIXING

# Canonical v3 (2026-11-12): single 7-day window, store chain from ASC,
# in-app chain from Mixpanel production, kept as separate blocks.
V3_GOOD = {
    "apps": [{
        "app": "Anicca",
        "window": {"start": "2026-11-04", "end": "2026-11-10"},
        "blocks": [
            {"kind": "store", "source": "ASC",
             "stages": [{"key": "impressions", "count": 334},
                        {"key": "page_views", "count": 14},
                        {"key": "first_time_downloads", "count": 1}]},
            {"kind": "in_app", "source": "Mixpanel",
             "stages": [{"key": "first_open", "count": 25},
                        {"key": "onboarding_complete", "count": 25},
                        {"key": "paywall_views", "count": 23},
                        {"key": "purchase_start", "count": 2},
                        {"key": "purchase_complete", "count": 0}]},
        ],
    }]
}


def codes(violations):
    return {v["code"] for v in violations}


def test_v3_canonical_passes():
    assert check_artifact(copy.deepcopy(V3_GOOD)) == []


def test_window_mixing_28d_store_block_fails():
    bad = copy.deepcopy(V3_GOOD)
    bad["apps"][0]["blocks"][0]["window"] = {"start": "2026-10-14",
                                             "end": "2026-11-10"}  # 28 days
    v = check_artifact(bad)
    assert WINDOW_MIXING in codes(v), v


def test_combined_chain_source_mixing_and_inversion_fails():
    # The original incident shape: ASC store stages and a Mixpanel cohort
    # joined into ONE chain (DL 1 -> first_open 25).
    bad = {"apps": [{
        "app": "Anicca",
        "window": {"start": "2026-11-04", "end": "2026-11-10"},
        "blocks": [{"kind": "combined", "source": "ASC",
                    "stages": [
                        {"key": "impressions", "count": 334, "source": "ASC"},
                        {"key": "page_views", "count": 14, "source": "ASC"},
                        {"key": "first_time_downloads", "count": 1,
                         "source": "ASC"},
                        {"key": "first_open", "count": 25,
                         "source": "Mixpanel"},
                    ]}],
    }]}
    v = check_artifact(bad)
    assert SOURCE_MIXING in codes(v), v
    assert INVERSION in codes(v), v


def test_revenuecat_installs_source_fails():
    bad = copy.deepcopy(V3_GOOD)
    bad["apps"][0]["installs"] = {"count": 196, "source": "RevenueCat new customers"}
    v = check_artifact(bad)
    assert SOURCE_MIXING in codes(v), v


def test_in_app_stage_inversion_fails():
    bad = copy.deepcopy(V3_GOOD)
    bad["apps"][0]["blocks"][1]["stages"][3]["count"] = 99  # purchase_start > paywall
    v = check_artifact(bad)
    assert INVERSION in codes(v), v


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"{len(fns)} tests passed")
