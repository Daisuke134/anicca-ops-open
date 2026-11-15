#!/usr/bin/env python3
"""One-rerun proof for the attribution-daily.py stale-overwrite guard.

Reproduces the 2026-11-15 incident: a `--pull` run that brings back PT 11/04-11/10
while the cache already holds PT 11/08-11/14.

Steps
  1. seed the cache from an ASC pull of PT 2026-11-08..2026-11-14 (run A)
  2. rerun the same command with PT 2026-11-04..2026-11-10 against the SAME cache
     (run B) using the pre-fix script  -> shows the overwrite that happened
  3. repeat 1-2 with the patched script -> shows the guard blocking every write

ASC is stubbed (`asc` + `requests` on PYTHONPATH) because this box has no
/workspace/asc.py credentials; the stubbed feed uses the real DAILY segment columns.
Does not print secrets.
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
                                 "First-time download", "No page", "US", "1.9.14", "6755129214"]))
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
OLD_WEEK = [f"2026-11-{d:02d}" for d in (4, 5, 6, 7, 8, 9, 10)]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def newest(p: Path):
    try:
        data = json.loads(p.read_text())
    except Exception:
        return None
    dates = [r.get("Date") for r in data if isinstance(r, dict) and r.get("Date")]
    return max(dates) if dates else None


def describe(cache: Path):
    out = []
    for p in sorted(cache.glob("*.json")):
        out.append(f"    {p.name:26s} newest PT Date={newest(p)}  sha256={sha(p)[:16]}")
    return out or ["    (no cache files)"]


def run(script: Path, cache: Path, stub: Path, dates, start, end, out: Path, extra=()):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(stub)
    env["STUB_DATES"] = ",".join(dates)
    cmd = [sys.executable, str(script), "--pull", "--cache", str(cache),
           "--start", start, "--end", end, "--out", str(out),
           "--report-date", "2026-11-16"] + list(extra)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=180)
    return r


def scenario(label, script, stub, tmp: Path):
    cache = tmp / "aff-funnel"
    cache.mkdir(parents=True, exist_ok=True)
    report = tmp / "attribution-daily-2026-11-16.md"
    print(f"\n=== {label}")
    print(f"  script: {script.name}")

    a = run(script, cache, stub, NEW_WEEK, "2026-11-08", "2026-11-14", report)
    print("  RUN A (seed) --pull PT 2026-11-08..2026-11-14")
    print(f"    exit={a.returncode}")
    for line in a.stderr.strip().splitlines():
        print(f"    stderr| {line}")
    print("    after run A:")
    print("\n".join(describe(cache)))
    before = {p.name: sha(p) for p in cache.glob("*.json")}
    report_before = sha(report) if report.exists() else None

    b = run(script, cache, stub, OLD_WEEK, "2026-11-04", "2026-11-10", report)
    print("  RUN B (rerun, older PT window) --pull PT 2026-11-04..2026-11-10")
    print(f"    exit={b.returncode}")
    for line in b.stderr.strip().splitlines():
        print(f"    stderr| {line}")
    print("    after run B:")
    print("\n".join(describe(cache)))
    after = {p.name: sha(p) for p in cache.glob("*.json")}
    report_after = sha(report) if report.exists() else None
    changed = sorted(n for n in before if before[n] != after.get(n))
    print(f"    cache files changed by RUN B: {changed or 'none'}")
    print(f"    report changed by RUN B: {report_before != report_after}")
    print(f"    newest PT date after RUN B: "
          f"{ {p.name: newest(p) for p in cache.glob('*.json')} }")
    return b.returncode, changed, report_before != report_after


def main():
    tmp = Path(tempfile.mkdtemp(prefix="attr-proof-"))
    stub = tmp / "stubpy"
    stub.mkdir()
    (stub / "asc.py").write_text(STUB_ASC)
    (stub / "requests.py").write_text(STUB_REQUESTS)
    try:
        orig = SCRIPTS / "attribution-daily.orig.py"
        patched = SCRIPTS / "attribution-daily.py"
        print("attribution-daily.py stale-overwrite guard - one-rerun proof")
        print(f"host python: {sys.version.split()[0]}")

        code_orig, changed_orig, report_orig = scenario(
            "BEFORE (pre-fix script, incident reproduced)", orig, stub, tmp / "before")
        code_new, changed_new, report_new = scenario(
            "AFTER (patched script, guard active)", patched, stub, tmp / "after")

        print("\n=== VERDICT")
        ok = (
            changed_orig and report_orig
            and not changed_new and not report_new
            and code_new == 3
        )
        print(f"  pre-fix: {len(changed_orig)} cache file(s) shrank to an older PT window, "
              f"report overwritten={report_orig}, exit={code_orig}")
        print(f"  patched: cache changed={changed_new or 'none'}, report overwritten={report_new}, "
              f"exit={code_new} (expected 3)")
        print(f"  {'PASS' if ok else 'FAIL'} - the newer PT window survives the rerun")
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
