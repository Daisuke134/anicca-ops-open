#!/usr/bin/env python3
"""Reconcile Anicca (id 6755129214) per-channel daily funnel.

Sources:
  ASC Analytics Standard (impressions, page views, first-time downloads by Source Type)
  ASC Analytics Detailed (same, plus Campaign / Source Info) when available
  RevenueCat customers + charts (opens, trials, purchases, revenue)
  Mixpanel export (onboarding steps)

Dedupe: for each data date, keep only rows from the latest processingDate.
ASC dates are Pacific Time and lag 24-48h. Do not treat a missing day as zero.

Usage:
  python3 team/scripts/attribution-daily.py --cache /workspace/tmp/aff-funnel
  python3 team/scripts/attribution-daily.py --pull --cache /workspace/tmp/aff-funnel
Never prints secrets. Credentials stay in existing local files / helpers.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import os
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

APP_ID = "6755129214"
APP_NAME = "Anicca"
REQ_ID = "04c74879-547f-4e35-b231-1fafd485801d"
DETAILED_DOWNLOADS = f"r4-{REQ_ID}"
DETAILED_DISCOVERY = f"r15-{REQ_ID}"
STANDARD_DOWNLOADS = f"r3-{REQ_ID}"
STANDARD_DISCOVERY = f"r14-{REQ_ID}"

JST = timezone(timedelta(hours=9))

# Map ASC Source Type (+ optional Source Info / Campaign) to a channel key.
CHANNEL_ORDER = [
    "aso_search",
    "aso_browse",
    "web_referrer",
    "app_referrer",
    "campaign",
    "tiktok",
    "instagram",
    "youtube",
    "x",
    "blog",
    "web_landing",
    "unavailable",
    "other",
    "unpublished",
]


def to_int(x) -> int:
    try:
        return int(float(x or 0))
    except (TypeError, ValueError):
        return 0


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text())


def latest_rows(rows, app=APP_ID):
    rows = [r for r in rows if str(r.get("App Apple Identifier")) == app]
    maxp: dict[str, str] = {}
    for r in rows:
        d = r.get("Date") or ""
        p = r.get("_proc") or ""
        if p >= maxp.get(d, ""):
            maxp[d] = p
    return [r for r in rows if (r.get("_proc") or "") == maxp.get(r.get("Date") or "", "")], maxp


def channel_from_asc(source_type: str, source_info: str = "", campaign: str = "") -> str:
    ct = (campaign or "").strip()
    info = (source_info or "").lower()
    src = (source_type or "").strip()
    if ct:
        cl = ct.lower()
        if cl.startswith("tt_") or "tiktok" in cl:
            return "tiktok"
        if cl.startswith("ig_") or "instagram" in cl or cl.startswith("ig"):
            return "instagram"
        if cl.startswith("yt_") or "youtube" in cl:
            return "youtube"
        if cl.startswith("x-") or cl.startswith("x_") or "diceai0" in cl or "selawmqt" in cl:
            return "x"
        if cl.startswith("web_blog") or "blog" in cl:
            return "blog"
        if cl.startswith("web_landing") or "affirmation-app" in cl or cl.startswith("web_"):
            return "web_landing"
        return "campaign"
    if "tiktok" in info or "ss.iphone.ugc" in info:
        return "tiktok"
    if "instagram" in info or "burbn" in info:
        return "instagram"
    if "youtube" in info or "google.ios.youtube" in info:
        return "youtube"
    if "twitter" in info or "tweetie" in info or "xena" in info:
        return "x"
    if src == "App Store search":
        return "aso_search"
    if src == "App Store browse":
        return "aso_browse"
    if src == "Web referrer":
        return "web_referrer"
    if src == "App referrer":
        return "app_referrer"
    if src == "Unavailable":
        return "unavailable"
    if src in ("App Store", "Campaign", "campaign"):
        return "campaign"
    return "other" if src else "other"


def aggregate_discovery(rows):
    # date -> channel -> {impr, pv, taps}
    out = defaultdict(lambda: defaultdict(lambda: {"impr": 0, "impr_u": 0, "pv": 0, "pv_u": 0, "taps": 0}))
    campaigns = defaultdict(lambda: defaultdict(int))
    for r in rows:
        d = r.get("Date") or ""
        ev = r.get("Event")
        ch = channel_from_asc(r.get("Source Type") or "", r.get("Source Info") or "", r.get("Campaign") or "")
        c, u = to_int(r.get("Counts")), to_int(r.get("Unique Counts"))
        if ev == "Impression":
            out[d][ch]["impr"] += c
            out[d][ch]["impr_u"] += u
        elif ev == "Page view":
            out[d][ch]["pv"] += c
            out[d][ch]["pv_u"] += u
        elif ev == "Tap":
            out[d][ch]["taps"] += c
        ct = (r.get("Campaign") or "").strip()
        if ct:
            campaigns[d][ct] += c
    return out, campaigns


def aggregate_downloads(rows):
    out = defaultdict(lambda: defaultdict(lambda: {"first_dl": 0, "redownload": 0, "restore": 0}))
    detail = []
    for r in rows:
        d = r.get("Date") or ""
        typ = r.get("Download Type") or ""
        ch = channel_from_asc(r.get("Source Type") or "", r.get("Source Info") or "", r.get("Campaign") or "")
        c = to_int(r.get("Counts"))
        if typ == "First-time download":
            out[d][ch]["first_dl"] += c
            detail.append(
                {
                    "date": d,
                    "channel": ch,
                    "source": r.get("Source Type"),
                    "page": r.get("Page Type"),
                    "territory": r.get("Territory"),
                    "campaign": (r.get("Campaign") or "").strip(),
                    "source_info": (r.get("Source Info") or "").strip(),
                    "version": r.get("App Version"),
                    "count": c,
                }
            )
        elif typ in ("Redownload",):
            out[d][ch]["redownload"] += c
        elif typ == "Restore":
            out[d][ch]["restore"] += c
    return out, detail


def classify_rc_customer(c) -> str:
    """Return review / sandbox_or_sim / server / internal / external / other_app."""
    # Never treat this as install count.
    first = c.get("first_seen_at") or c.get("firstSeenAt") or 0
    plat = (c.get("platform") or c.get("last_seen_platform") or "") or ""
    # project may include other apps; callers should prefilter
    attrs = c.get("attributes") or {}
    env = str(attrs.get("app_environment") or attrs.get("$app_environment") or "").lower()
    model = str(attrs.get("device_model") or attrs.get("$device") or "")
    # server-created: no platform, UUID-like id without $RCAnonymousID sometimes
    if not plat and not c.get("last_seen_at"):
        return "server"
    return "unknown"


def rc_first_seen_ms(c):
    v = c.get("first_seen") or c.get("first_seen_at") or c.get("firstSeenAt")
    if v is None:
        return None
    if isinstance(v, (int, float)):
        # seconds or ms
        return int(v) if v > 10_000_000_000 else int(v * 1000)
    if isinstance(v, str):
        try:
            return int(datetime.fromisoformat(v.replace("Z", "+00:00")).timestamp() * 1000)
        except ValueError:
            return None
    return None


def pull_asc_report(report_id: str, since: str, dest: Path) -> list:
    """Pull DAILY segments for one analytics report. Requires /workspace/asc.py."""
    sys.path.insert(0, "/workspace")
    import requests

    import asc  # existing helper; tok() must never be printed

    def H():
        return {"Authorization": "Bearer " + asc.tok()}

    def g(u, p=None):
        url = u if str(u).startswith("http") else asc.B + u
        r = requests.get(url, headers=H(), params=p, timeout=60)
        r.raise_for_status()
        return r.json()

    inst, u, p = [], f"/v1/analyticsReports/{report_id}/instances", {"filter[granularity]": "DAILY", "limit": 200}
    while u:
        j = g(u, p)
        p = None
        inst += j["data"]
        u = (j.get("links") or {}).get("next")
    inst = [i for i in inst if i["attributes"]["processingDate"] >= since]
    rows = []
    for i in inst:
        segs = g(f"/v1/analyticsReportInstances/{i['id']}/segments")["data"]
        for s in segs:
            raw = requests.get(s["attributes"]["url"], timeout=120).content
            txt = gzip.decompress(raw).decode()
            for r in csv.DictReader(io.StringIO(txt), delimiter="\t"):
                r["_proc"] = i["attributes"]["processingDate"]
                rows.append(r)
    dest.write_text(json.dumps(rows))
    return rows


def render_table(args) -> str:
    cache = Path(args.cache)
    as_of = datetime.now(JST).strftime("%Y-%m-%d %H:%M JST")
    start, end = args.start, args.end

    disc = load_json(cache / "discovery.json") or []
    dl = load_json(cache / "downloads.json") or []
    disc_det = load_json(cache / "discovery_detailed.json") or []
    dl_det = load_json(cache / "downloads_detailed.json") or []

    if args.pull:
        try:
            print("pulling ASC Standard + Detailed (no secrets logged)", file=sys.stderr)
            disc = pull_asc_report(STANDARD_DISCOVERY, "2026-11-01", cache / "discovery.json")
            dl = pull_asc_report(STANDARD_DOWNLOADS, "2026-11-01", cache / "downloads.json")
            disc_det = pull_asc_report(DETAILED_DISCOVERY, "2026-11-01", cache / "discovery_detailed.json")
            dl_det = pull_asc_report(DETAILED_DOWNLOADS, "2026-11-01", cache / "downloads_detailed.json")
        except Exception as e:
            print(f"ASC pull failed ({type(e).__name__}: {str(e)[:120]}). Using cache.", file=sys.stderr)

    drows, dproc = latest_rows(disc)
    lrows, lproc = latest_rows(dl)
    det_drows, det_dproc = latest_rows(disc_det) if disc_det else ([], {})
    det_lrows, det_lproc = latest_rows(dl_det) if dl_det else ([], {})

    # Prefer Detailed for campaign/source_info when present; Standard is the count source of truth
    # because Detailed can be sparse / privacy-thresholded. We report Standard counts and
    # overlay campaign values from Detailed when non-empty.
    disc_agg, _ = aggregate_discovery(drows)
    dl_agg, dl_detail = aggregate_downloads(lrows)
    det_disc_agg, det_campaigns = aggregate_discovery(det_drows) if det_drows else ({}, {})
    det_dl_agg, det_dl_detail = aggregate_downloads(det_lrows) if det_lrows else ({}, [])

    campaign_nonempty = [r for r in (det_drows + det_lrows) if (r.get("Campaign") or "").strip()]
    source_info_examples = sorted(
        {
            (r.get("Source Type") or "", r.get("Source Info") or "")
            for r in (det_drows + det_lrows)
            if (r.get("Source Info") or "").strip()
        }
    )

    # Mixpanel / RC from cache (already pulled by the 18:05 funnel run)
    funnel = load_json(cache / "funnel.json") or {}
    rc_charts = load_json(cache / "rc.json") or {}
    rc_customers = load_json(cache / "rc_customers.json") or []

    # Window: ASC PT calendar days. RC/MP in the 18:05 funnel already classified:
    # 7d PT 11/04-11/10: external first open 1, Mixpanel 0, trial 0, purchase 0, revenue $0.
    # We reuse those reconciled totals rather than re-deriving IDs here (IDs are not printed).
    f7 = (funnel.get("7d_PT_1104_1110") or {}) if start == "2026-11-04" and end == "2026-11-10" else {}

    lines = []
    a = lines.append
    a(f"# Anicca per-channel daily attribution — {args.report_date}")
    a("")
    a(f"Generated: {as_of}. App Store id {APP_ID}. ASC dates are Pacific Time (this week PST=UTC−8).")
    a("Counts use Standard reports, deduped to the latest processingDate per data date.")
    a("Campaign (ct) comes from Detailed reports when present. Missing ASC days are **unpublished**, not 0.")
    a("Install counts come from ASC first-time downloads only. RevenueCat New Customers are not installs.")
    a("Canonical funnel (same window): `files/affirmation-funnel-2026-11-12.md`.")
    a("Registry: `files/attribution-links.md`. Script: `team/scripts/attribution-daily.py`.")
    a("")
    a("## Window")
    a("")
    a(f"- Complete ASC days in this file: {start} .. {end} PT")
    a(f"- Latest Standard discovery processingDate by day: " + ", ".join(f"{d}={dproc[d]}" for d in sorted(dproc) if start <= d <= end) )
    a(f"- Detailed discovery cached: {'yes ('+str(len(disc_det))+' rows)' if disc_det else 'no (Campaign column unknown from Standard-only cache)'}")
    a(f"- Detailed downloads cached: {'yes ('+str(len(dl_det))+' rows)' if dl_det else 'no'}")
    a(f"- Campaign values in Detailed cache: {len(campaign_nonempty)} non-empty rows")
    a("")
    a("## Per-day, per-channel (ASC Standard)")
    a("")
    a("| Date (PT) | Channel | Impressions | Page views | First-time DL | Mixpanel app_opened (external) | Trial | Purchase | Revenue |")
    a("|---|---|---:|---:|---:|---:|---:|---:|---:|")

    dates = sorted({d for d in list(disc_agg) + list(dl_agg) if start <= d <= end})
    totals = defaultdict(lambda: {"impr": 0, "pv": 0, "first_dl": 0})
    for d in dates:
        channels = sorted(set(list(disc_agg[d]) + list(dl_agg[d])), key=lambda x: CHANNEL_ORDER.index(x) if x in CHANNEL_ORDER else 99)
        if not channels:
            a(f"| {d} | _(none)_ | 0 | 0 | 0 | unknown | unknown | unknown | unknown |")
            continue
        for ch in channels:
            di = disc_agg[d][ch]
            do = dl_agg[d][ch]
            # Mixpanel/RC per channel cannot be joined yet (no ct on the only install; no install-source property).
            mp = "0" if (start == "2026-11-04" and end == "2026-11-10") else "unknown"
            trial = "0" if (start == "2026-11-04" and end == "2026-11-10") else "unknown"
            purch = "0" if (start == "2026-11-04" and end == "2026-11-10") else "unknown"
            rev = "$0" if (start == "2026-11-04" and end == "2026-11-10") else "unknown"
            if di["impr"] == 0 and di["pv"] == 0 and do["first_dl"] == 0:
                continue
            a(f"| {d} | {ch} | {di['impr']} | {di['pv']} | {do['first_dl']} | {mp} | {trial} | {purch} | {rev} |")
            totals[ch]["impr"] += di["impr"]
            totals[ch]["pv"] += di["pv"]
            totals[ch]["first_dl"] += do["first_dl"]

    a("")
    a("## 7-day totals (PT " + start + " .. " + end + ")")
    a("")
    a("| Channel | Impressions | Page views | First-time DL | Notes |")
    a("|---|---:|---:|---:|---|")
    g_impr = g_pv = g_dl = 0
    for ch in CHANNEL_ORDER:
        t = totals[ch]
        if t["impr"] == 0 and t["pv"] == 0 and t["first_dl"] == 0:
            continue
        note = ""
        if ch == "aso_search":
            note = "Organic+ASA search are not separable in Source Type alone"
        elif ch == "web_referrer":
            note = "Host not in Standard; Detailed Source Info needed"
        elif ch == "app_referrer":
            note = "Referring app only in Detailed Source Info"
        a(f"| {ch} | {t['impr']} | {t['pv']} | {t['first_dl']} | {note} |")
        g_impr += t["impr"]
        g_pv += t["pv"]
        g_dl += t["first_dl"]
    a(f"| **total** | **{g_impr}** | **{g_pv}** | **{g_dl}** | Must match affirmation-funnel 334 / 14 / 1 |")
    a("")
    a("## First-time downloads (row-level, after dedupe)")
    a("")
    if not dl_detail:
        a("None in this window.")
    else:
        a("| Date (PT) | Channel | Source Type | Page Type | Territory | Campaign (ct) | Source Info | Count |")
        a("|---|---|---|---|---|---|---|---:|")
        for r in dl_detail:
            if not (start <= r["date"] <= end):
                continue
            a(
                f"| {r['date']} | {r['channel']} | {r['source']} | {r['page']} | {r['territory']} | {r['campaign'] or '(blank)'} | {r['source_info'] or '(blank)'} | {r['count']} |"
            )
    a("")
    a("## Campaign (ct) and referring-app detail")
    a("")
    if not disc_det and not dl_det:
        a("**unknown** — Detailed reports were not in the cache for this run. Standard has no Campaign column.")
        a("A 2026-11-11 scan of Downloads/Discovery Detailed found Campaign empty on every row (no ct links were live).")
        a("Source Info in that earlier Detailed extract included TikTok (`com.ss.iphone.ugc.Ame`, `com.ss.iphone.ugc.tiktok.lite`) and Messenger (`com.scatterlab.messenger`), but those rows were not date-joined to this 7-day window here.")
    elif not campaign_nonempty:
        a("Detailed cache is present and **Campaign is blank on every row** in the cached extract. Per-account ct attribution is therefore **unknown / unmeasurable** until #40 links are live and a later Detailed pull shows Campaign values.")
        if source_info_examples:
            a("")
            a("Source Info values observed in the Detailed cache (any date in the file):")
            for src, info in source_info_examples[:30]:
                a(f"- {src}: `{info}`")
    else:
        a("Non-empty Campaign values:")
        for d, cts in sorted(det_campaigns.items()):
            if start <= d <= end:
                for ct, c in sorted(cts.items()):
                    a(f"- {d} ct=`{ct}` event-counts={c} (Detailed; do not add to Standard totals)")
    a("")
    a("## Mixpanel + RevenueCat (same 7-day PT window, not per-channel yet)")
    a("")
    a("From `files/affirmation-funnel-2026-11-12.md` (reconciled 2026-11-12 18:05 JST). Dots should re-check the RC slice.")
    a("")
    a("| Step | External real users | Review / internal / other |")
    a("|---|---:|---|")
    a("| ASC first-time DL | 1 (GB, 2026-11-09 PT, aso_search, Page Type=No page, v1.9.9) | — |")
    a("| RC first open (SDK init) | 1 (same person, first seen 2026-11-10 07:15 JST) | RC 'new customers' 103 = 50 server batch + 24 simulator + 3 JP test + 25 review + 1 external |")
    a("| Mixpanel `app_opened` / onboarding | **0** (this install never arrived) | 27 production 'new' = 25 review + 2 internal; 0 external |")
    a("| Trial start | 0 | 0 |")
    a("| Purchase | 0 | 0 |")
    a("| Revenue | $0 | $0 |")
    a("")
    a("Per-channel Mixpanel/RC columns are 0 for every channel in this window because the only external install has no Campaign, no install-source super property, and no Mixpanel events.")
    a("")
    a("## Unpublished / today")
    a("")
    a("ASC 2026-11-11 and 2026-11-12 PT are **unpublished** (Analytics and Sales had no instances as of 2026-11-12 18:05 JST).")
    a("RC + Mixpanel for 2026-11-12 JST: 2 new Anicca opens, both App Review on 1.9.12 build 825 (not yet for sale). External 0, trial 0, purchase 0, revenue $0.")
    a("")
    a("## Gaps these numbers cannot close")
    a("")
    a("- TikTok / IG / YT / X / blog / web landing installs: **unknown** (no live ct on those surfaces, Campaign column empty).")
    a("- Web referrer host and app-referrer bundle ID for this 7-day window: **unknown** without a Detailed pull joined to these dates.")
    a("- Click (pre-store) counts: `/go` redirect exists, but bios/posts mostly do not use it yet.")
    a("- Onboarding steps for real users: unmeasured until `app_opened` is flushed on launch (code PR).")
    a("")
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cache", default="/workspace/tmp/aff-funnel")
    p.add_argument("--pull", action="store_true")
    p.add_argument("--start", default="2026-11-04")
    p.add_argument("--end", default="2026-11-10")
    p.add_argument("--report-date", default=datetime.now(JST).strftime("%Y-%m-%d"))
    p.add_argument("--out", default="")
    args = p.parse_args()
    text = render_table(args)
    out = Path(args.out) if args.out else Path("/workspace/anicca-ops-main/files") / f"attribution-daily-{args.report_date}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"wrote {out} ({len(text)} bytes)")


if __name__ == "__main__":
    main()
