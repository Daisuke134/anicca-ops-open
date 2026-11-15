#!/usr/bin/env python3
"""CLI-level proof for the two evidence-loss paths found in the @chatgpt review.

Review: https://github.com/Daisuke134/anicca-ops/issues/79#issuecomment-6899241744
(reviewed source: commit 9d5b3ba6, frozen here as
`fixtures/attribution-daily-at-9d5b3ba6.py`).

Case 1 - report with no verifiable window end
    seed  files/attribution-daily-2026-11-16.md holding
          `- Complete ASC days in this file: 2026-11-08 .. 2026-11-14 PT`
    rerun `--end ""` (no verifiable window end) onto the same path.
    Reviewed source: accepted, exit 0, the dated report is gone.
    Patched source : refused, exit 3, report byte-identical.

Case 2 - cache, same newest PT date, fewer measured days
    seed the cache from PT 2026-11-08..2026-11-14
    rerun a pull whose feed returns PT 2026-11-14 only.
    Reviewed source: all four cache files replaced, 7 measured days -> 1.
    Patched source : `BLOCKED ... coverage would shrink`, files byte-identical.

ASC is stubbed (`asc` + `requests` on PYTHONPATH) because this box has no
/workspace/asc.py credentials; the stubbed feed uses the real DAILY segment columns,
so the actual write path is what runs. No live ASC pull, no product data, no secrets.

Run:  python3 team/scripts/tests/attribution_daily_review2_cases_proof.py
Exit: 0 when the reviewed source loses evidence in both cases and the patched source
      loses none; 1 otherwise.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
REVIEWED = HERE / "fixtures" / "attribution-daily-at-9d5b3ba6.py"
PATCHED = SCRIPTS / "attribution-daily.py"

STUB_ASC = """\
B = "https://asc.invalid"
def tok():
    return "stub-token-never-printed"
"""

STUB_REQUESTS = '''\
"""Minimal requests stub: serves synthetic ASC DAILY segments from STUB_DATES."""
import gzip, os
from urllib.parse import urlparse


class _Resp:
    def __init__(self, payload=None, content=b""):
        self._payload = payload
        self.content = content
        self.status_code = 200

    def json(self):
        return self._payload

    def raise_for_status(self):
        return None


def _tsv():
    dates = [d for d in os.environ.get("STUB_DATES", "").split(",") if d]
    header = ["Date", "Event", "Source Type", "Source Info", "Campaign", "Counts",
              "Unique Counts", "Download Type", "Page Type", "Territory",
              "App Version", "App Apple Identifier"]
    lines = ["\\t".join(header)]
    for d in dates:
        lines.append("\\t".join([d, "Impression", "App Store search", "", "", "7", "5",
                                 "", "No page", "US", "1.9.14", "6755129214"]))
        lines.append("\\t".join([d, "Download", "App Store search", "", "", "1", "1",
                                 "First-time download", "No page", "US", "1.9.14",
                                 "6755129214"]))
    return "\\n".join(lines) + "\\n"


def get(url, headers=None, params=None, timeout=None):
    path = urlparse(url).path
    if path.endswith("/instances"):
        return _Resp({"data": [{"id": "inst-1",
                                "attributes": {"processingDate": "2026-11-15"}}], "links": {}})
    if path.endswith("/segments"):
        return _Resp({"data": [{"attributes": {"url": "https://seg.invalid/1"}}]})
    if url.startswith("https://seg.invalid"):
        return _Resp(None, gzip.compress(_tsv().encode()))
    raise AssertionError("unexpected stub URL " + url)
'''

NEW_WEEK = [f"2026-11-{d:02d}" for d in (8, 9, 10, 11, 12, 13, 14)]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def measured_days(p: Path) -> list[str]:
    try:
        data = json.loads(p.read_text())
    except Exception:
        return []
    if not isinstance(data, list):
        return []
    return sorted({r.get("Date") for r in data if isinstance(r, dict) and r.get("Date")})


def run(script: Path, cache: Path, stub: Path, dates, start, end, out: Path):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(stub)
    env["STUB_DATES"] = ",".join(dates)
    cmd = [sys.executable, str(script), "--pull", "--cache", str(cache),
           "--start", start, "--end", end, "--out", str(out),
           "--report-date", "2026-11-16"]
    return subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=180)


def report_lines(stderr: str) -> list[str]:
    return [ln for ln in (stderr or "").strip().splitlines() if ln.strip()]


def case1(script: Path, stub: Path, root: Path) -> dict:
    """Report with no verifiable window end over a report that has one."""
    cache, report = root / "cache", root / "attribution-daily-2026-11-16.md"
    cache.mkdir(parents=True, exist_ok=True)
    seed = run(script, cache, stub, NEW_WEEK, "2026-11-08", "2026-11-14", report)
    before_sha = sha(report) if report.exists() else None
    before_has_end = report.exists() and "2026-11-14 PT" in report.read_text()

    second = run(script, cache, stub, NEW_WEEK, "2026-11-08", "", report)
    after_text = report.read_text() if report.exists() else ""
    print("  seed run (PT 2026-11-08..2026-11-14):")
    print(f"    exit={seed.returncode}  report window end present={before_has_end}")
    print("  rerun with --end \"\" (no verifiable window end):")
    print(f"    exit={second.returncode} (patched expectation: 3)")
    for line in report_lines(second.stderr):
        print(f"    stderr| {line}")
    unchanged = report.exists() and sha(report) == before_sha
    print(f"    report byte-identical after rerun: {unchanged}")
    print(f"    report still declares a PT window end: {'2026-11-14 PT' in after_text}")
    lost = second.returncode == 0 and not unchanged and "2026-11-14 PT" not in after_text
    return {"lost": lost, "unchanged": unchanged, "exit": second.returncode,
            "blocked": "no verifiable window end" in second.stderr}


def case2(script: Path, stub: Path, root: Path) -> dict:
    """Cache holding seven measured PT days replaced by a pull of a single day."""
    cache, report_a, report_b = root / "cache", root / "a.md", root / "b.md"
    cache.mkdir(parents=True, exist_ok=True)
    seed = run(script, cache, stub, NEW_WEEK, "2026-11-08", "2026-11-14", report_a)
    before = {p.name: sha(p) for p in sorted(cache.glob("*.json"))}
    days_before = {p.name: measured_days(p) for p in sorted(cache.glob("*.json"))}

    second = run(script, cache, stub, ["2026-11-14"], "2026-11-08", "2026-11-14", report_b)
    after = {p.name: sha(p) for p in sorted(cache.glob("*.json"))}
    days_after = {p.name: measured_days(p) for p in sorted(cache.glob("*.json"))}
    changed = sorted(n for n in before if before[n] != after.get(n))
    print("  seed run (PT 2026-11-08..2026-11-14):")
    print(f"    exit={seed.returncode}")
    for name, days in days_before.items():
        print(f"    {name:26s} measured PT days={len(days)} ({days[0]}..{days[-1]})")
    print("  rerun where the feed returns PT 2026-11-14 only:")
    print(f"    exit={second.returncode}")
    for line in report_lines(second.stderr):
        print(f"    stderr| {line}")
    print(f"    cache files changed by rerun: {changed or 'none'}")
    for name, days in days_after.items():
        print(f"    {name:26s} measured PT days={len(days)} {days}")
    return {"lost": bool(changed), "changed": changed, "exit": second.returncode,
            "blocked": "coverage would shrink" in second.stderr}


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="attr-review2-"))
    stub = tmp / "stubpy"
    stub.mkdir()
    (stub / "asc.py").write_text(STUB_ASC)
    (stub / "requests.py").write_text(STUB_REQUESTS)
    try:
        print("attribution-daily.py — review cases 1 and 2, CLI proof")
        print(f"host python: {sys.version.split()[0]}")
        print(f"reviewed source: team/scripts/tests/fixtures/{REVIEWED.name} "
              f"sha256={sha(REVIEWED)[:16]}")
        print(f"patched source : team/scripts/attribution-daily.py "
              f"sha256={sha(PATCHED)[:16]}")

        print("\n=== REVIEWED SOURCE (commit 9d5b3ba6) — case 1")
        r1 = case1(REVIEWED, stub, tmp / "rev-case1")
        print("\n=== REVIEWED SOURCE (commit 9d5b3ba6) — case 2")
        r2 = case2(REVIEWED, stub, tmp / "rev-case2")

        print("\n=== PATCHED SOURCE — case 1")
        p1 = case1(PATCHED, stub, tmp / "fix-case1")
        print("\n=== PATCHED SOURCE — case 2")
        p2 = case2(PATCHED, stub, tmp / "fix-case2")

        ok = (
            r1["lost"] and r2["lost"]
            and not p1["lost"] and p1["exit"] == 3 and p1["blocked"]
            and not p2["lost"] and p2["blocked"]
        )
        print("\n=== VERDICT")
        print(f"  reviewed: case1 lost={r1['lost']} exit={r1['exit']}, "
              f"case2 lost={r2['lost']} changed={len(r2['changed'])} file(s)")
        print(f"  patched : case1 lost={p1['lost']} exit={p1['exit']} "
              f"blocked_reason_logged={p1['blocked']}, case2 lost={p2['lost']} "
              f"blocked_reason_logged={p2['blocked']}")
        print(f"  {'PASS' if ok else 'FAIL'} — both paths fail closed on the patched source "
              f"and stay open on the reviewed source")
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
