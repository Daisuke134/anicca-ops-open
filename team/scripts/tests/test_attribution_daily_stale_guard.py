#!/usr/bin/env python3
"""Regression tests for the stale-overwrite guard in team/scripts/attribution-daily.py.

Incident replayed (参謀, 2026-11-15 22:2x JST): `--pull` wrote PT 11/04-11/10 cache
rows over files that already held PT 11/08-11/14, shrinking the measured window.

Run:  python3 -m unittest discover -s team/scripts/tests -p 'test_attribution_daily*.py'
  or: python3 team/scripts/tests/test_attribution_daily_stale_guard.py

No network and no ASC credentials: `asc` and `requests` are stubbed through PYTHONPATH
for the end-to-end reruns, so the real `--pull` write path executes unchanged.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "attribution-daily.py"


def load_module():
    spec = importlib.util.spec_from_file_location("attribution_daily", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ad = load_module()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(*dates):
    return [{"Date": d, "Event": "Impression", "Counts": 1, "App Apple Identifier": ad.APP_ID} for d in dates]


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
    header = [
        "Date", "Event", "Source Type", "Source Info", "Campaign", "Counts",
        "Unique Counts", "Download Type", "Page Type", "Territory",
        "App Version", "App Apple Identifier",
    ]
    lines = ["\\t".join(header)]
    for d in dates:
        lines.append("\\t".join([
            d, "Impression", "App Store search", "", "", "7", "5", "",
            "No page", "US", "1.9.14", os.environ.get("STUB_APP", "6755129214"),
        ]))
        lines.append("\\t".join([
            d, "Download", "App Store search", "", "", "1", "1", "First-time download",
            "No page", "US", "1.9.14", os.environ.get("STUB_APP", "6755129214"),
        ]))
    return "\\n".join(lines) + "\\n"


def get(url, headers=None, params=None, timeout=None):
    path = urlparse(url).path
    if path.endswith("/instances"):
        return _Resp({"data": [{"id": "inst-1", "attributes": {
            "processingDate": os.environ.get("STUB_PROC_DATE", "2026-11-15")}}], "links": {}})
    if path.endswith("/segments"):
        return _Resp({"data": [{"attributes": {"url": "https://seg.invalid/1"}}]})
    if url.startswith("https://seg.invalid"):
        return _Resp(None, gzip.compress(_tsv().encode()))
    raise AssertionError("unexpected stub URL " + url)
'''


class UnitGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_norm_pt_date(self):
        self.assertEqual(ad.norm_pt_date("2026-11-14"), "2026-11-14")
        self.assertEqual(ad.norm_pt_date(" 2026-11-09 "), "2026-11-09")
        self.assertIsNone(ad.norm_pt_date("2026-02-30"))
        self.assertIsNone(ad.norm_pt_date("11/14/2026"))
        self.assertIsNone(ad.norm_pt_date(None))
        self.assertIsNone(ad.norm_pt_date(""))

    def test_newest_pt_date_in_rows(self):
        self.assertEqual(ad.newest_pt_date_in_rows(rows("2026-11-09", "2026-11-14", "2026-11-10")), "2026-11-14")
        self.assertIsNone(ad.newest_pt_date_in_rows([]))
        self.assertIsNone(ad.newest_pt_date_in_rows([{"Counts": 3}, "junk"]))

    def test_stale_reason_only_when_incoming_is_older(self):
        self.assertIsNotNone(ad.stale_overwrite_reason("2026-11-14", "2026-11-10"))
        self.assertIsNone(ad.stale_overwrite_reason("2026-11-14", "2026-11-14"))
        self.assertIsNone(ad.stale_overwrite_reason("2026-11-10", "2026-11-14"))
        self.assertIsNone(ad.stale_overwrite_reason(None, "2026-11-10"))
        self.assertIsNone(ad.stale_overwrite_reason("2026-11-14", None))

    def test_write_guarded_rows_blocks_and_preserves_bytes(self):
        dest = self.tmp / "downloads.json"
        dest.write_text(json.dumps(rows("2026-11-08", "2026-11-14")))
        before = sha(dest)
        self.assertFalse(ad.write_guarded_rows(dest, rows("2026-11-04", "2026-11-10")))
        self.assertEqual(sha(dest), before)
        self.assertEqual(ad.newest_pt_date_in_json_file(dest), "2026-11-14")

    def test_write_guarded_rows_allows_newer_equal_and_missing(self):
        dest = self.tmp / "downloads.json"
        self.assertTrue(ad.write_guarded_rows(dest, rows("2026-11-04", "2026-11-10")))
        self.assertTrue(ad.write_guarded_rows(dest, rows("2026-11-08", "2026-11-14")))
        self.assertEqual(ad.newest_pt_date_in_json_file(dest), "2026-11-14")
        self.assertTrue(ad.write_guarded_rows(dest, rows("2026-11-08", "2026-11-14")))
        self.assertFalse(list(self.tmp.glob("*.tmp")), "atomic temp file left behind")

    def test_write_guarded_rows_override(self):
        dest = self.tmp / "downloads.json"
        dest.write_text(json.dumps(rows("2026-11-14")))
        self.assertTrue(ad.write_guarded_rows(dest, rows("2026-11-10"), allow_stale=True))
        self.assertEqual(ad.newest_pt_date_in_json_file(dest), "2026-11-10")

    def test_empty_incoming_pull_cannot_erase_dated_cache(self):
        dest = self.tmp / "downloads.json"
        dest.write_text(json.dumps(rows("2026-11-14")))
        before = sha(dest)
        self.assertFalse(ad.write_guarded_rows(dest, []))
        self.assertEqual(sha(dest), before)
        self.assertTrue(ad.write_guarded_rows(dest, [], allow_stale=True))

    def test_unreadable_existing_cache_does_not_block(self):
        dest = self.tmp / "downloads.json"
        dest.write_text("{not json")
        self.assertTrue(ad.write_guarded_rows(dest, rows("2026-11-10")))

    def test_report_window_parse_and_block(self):
        out = self.tmp / "attribution-daily-2026-11-16.md"
        text14 = "# r\n\n- Complete ASC days in this file: 2026-11-08 .. 2026-11-14 PT\n"
        self.assertIsNone(ad.newest_pt_date_in_report_file(out))
        out.write_text(text14)
        self.assertEqual(ad.newest_pt_date_in_report_file(out), "2026-11-14")
        before = sha(out)
        self.assertFalse(ad.write_guarded_report(out, "# older\n", "2026-11-10"))
        self.assertEqual(sha(out), before)
        self.assertTrue(ad.write_guarded_report(out, "# newer\n", "2026-11-16"))

    # --- peer review 2026-11-16 03:3x JST, finding 1: report missing end ---

    def test_report_missing_window_end_cannot_overwrite_known_window(self):
        """`window_end=None` over a dated report must not be accepted."""
        out = self.tmp / "attribution-daily-2026-11-16.md"
        out.write_text("# r\n\n- Complete ASC days in this file: 2026-11-08 .. 2026-11-14 PT\n")
        before = sha(out)
        self.assertFalse(
            ad.write_guarded_report(out, "# INCOMPLETE (missing window)\n", None),
            "a report with no verifiable window replaced a report that had one",
        )
        self.assertEqual(sha(out), before, "old report bytes were lost")
        self.assertEqual(ad.newest_pt_date_in_report_file(out), "2026-11-14")
        self.assertTrue(list(self.tmp.glob("*.tmp")) == [])
        # explicit override still allowed for a deliberate, documented write
        self.assertTrue(ad.write_guarded_report(out, "# INCOMPLETE\n", None, allow_stale=True))

    def test_report_missing_end_is_blocked_even_with_no_prior_end_known(self):
        out = self.tmp / "fresh.md"
        self.assertTrue(ad.write_guarded_report(out, "# INCOMPLETE\n", None))
        self.assertEqual(out.read_text(), "# INCOMPLETE\n")

    def test_report_window_end_from_rendered_text_when_argument_missing(self):
        """Preserve the known window: the text itself may carry the measured window."""
        out = self.tmp / "r.md"
        out.write_text("- Complete ASC days in this file: 2026-11-08 .. 2026-11-14 PT\n")
        newer = "- Complete ASC days in this file: 2026-11-08 .. 2026-11-15 PT\n"
        self.assertTrue(ad.write_guarded_report(out, newer, None))
        self.assertEqual(ad.newest_pt_date_in_report_file(out), "2026-11-15")
        before = sha(out)
        older = "- Complete ASC days in this file: 2026-11-04 .. 2026-11-10 PT\n"
        self.assertFalse(ad.write_guarded_report(out, older, None))
        self.assertEqual(sha(out), before)
        self.assertTrue(ad.write_guarded_report(out, "- Complete ASC days in this file: 2026-11-04 .. 2026-11-10 PT\n", None, allow_stale=True))

    # --- peer review 2026-11-16 03:3x JST, finding 2: same-max-date coverage ---

    def test_same_newest_date_coverage_loss_is_blocked(self):
        """[11/08, 11/14] replaced by [11/14] keeps the newest date and loses a day."""
        dest = self.tmp / "downloads.json"
        dest.write_text(json.dumps(rows("2026-11-08", "2026-11-14")))
        before = sha(dest)
        self.assertFalse(
            ad.write_guarded_rows(dest, rows("2026-11-14")),
            "coverage loss at an equal newest PT date was accepted",
        )
        self.assertEqual(sha(dest), before, "cache bytes changed on a blocked write")
        self.assertEqual(ad.newest_pt_date_in_json_file(dest), "2026-11-14")
        self.assertEqual(ad.pt_dates_in_rows(json.loads(dest.read_text())), {"2026-11-08", "2026-11-14"})
        # the same shrink is allowed only as an explicit backfill/repair
        self.assertTrue(ad.write_guarded_rows(dest, rows("2026-11-14"), allow_stale=True))

    def test_same_newest_date_equal_or_wider_coverage_still_writes(self):
        dest = self.tmp / "downloads.json"
        dest.write_text(json.dumps(rows("2026-11-08", "2026-11-14")))
        self.assertTrue(ad.write_guarded_rows(dest, rows("2026-11-08", "2026-11-14")), "identical re-pull refused")
        self.assertTrue(ad.write_guarded_rows(dest, rows("2026-11-07", "2026-11-08", "2026-11-14")), "wider coverage refused")
        self.assertEqual(ad.newest_pt_date_in_json_file(dest), "2026-11-14")

    def test_same_newest_date_fewer_rows_for_same_days_is_blocked(self):
        """A pull that returns fewer dated rows for the same days is an incomplete pull."""
        dest = self.tmp / "downloads.json"
        two_per_day = [
            {"Date": d, "Event": ev, "Counts": 1, "App Apple Identifier": ad.APP_ID}
            for d in ("2026-11-08", "2026-11-14")
            for ev in ("Impression", "Download")
        ]
        dest.write_text(json.dumps(two_per_day))
        before = sha(dest)
        self.assertFalse(ad.write_guarded_rows(dest, rows("2026-11-08", "2026-11-14")))
        self.assertEqual(sha(dest), before)
        self.assertEqual(ad.dated_row_count(json.loads(dest.read_text())), 4)
        self.assertTrue(ad.write_guarded_rows(dest, rows("2026-11-08", "2026-11-14"), allow_stale=True))

    def test_newer_pull_with_fewer_days_still_writes_but_warns(self):
        """Forward movement is allowed; the PT days it drops are announced, not silent."""
        dest = self.tmp / "downloads.json"
        dest.write_text(json.dumps(rows("2026-11-08", "2026-11-14")))
        self.assertTrue(ad.write_guarded_rows(dest, rows("2026-11-15")))
        self.assertEqual(ad.newest_pt_date_in_json_file(dest), "2026-11-15")
        self.assertEqual(ad.pt_dates_in_rows(json.loads(dest.read_text())), {"2026-11-15"})


class EndToEndRerunTests(unittest.TestCase):
    """Runs the real CLI twice per scenario against a stubbed ASC endpoint."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.stub = self.tmp / "stubpy"
        self.stub.mkdir()
        (self.stub / "asc.py").write_text(STUB_ASC)
        (self.stub / "requests.py").write_text(STUB_REQUESTS)
        self.cache = self.tmp / "cache"
        self.cache.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cli(self, dates, start, end, out, extra=None):
        env = dict(os.environ)
        env["PYTHONPATH"] = str(self.stub)
        env["STUB_DATES"] = ",".join(dates)
        cmd = [
            sys.executable, str(SCRIPT), "--pull",
            "--cache", str(self.cache),
            "--start", start, "--end", end,
            "--out", str(out),
            "--report-date", "2026-11-16",
        ] + list(extra or [])
        return subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=180)

    def cache_shas(self):
        return {p.name: sha(p) for p in sorted(self.cache.glob("*.json"))}

    def test_incident_replay_older_pull_cannot_shrink_newer_cache(self):
        week_new = [f"2026-11-{d:02d}" for d in (8, 9, 10, 11, 12, 13, 14)]
        week_old = [f"2026-11-{d:02d}" for d in (4, 5, 6, 7, 8, 9, 10)]

        first = self.run_cli(week_new, "2026-11-08", "2026-11-14", self.tmp / "report.md")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(len(self.cache_shas()), 4, "expected 4 cache files from the pull")
        newest_before = {
            name: ad.newest_pt_date_in_json_file(self.cache / name) for name in self.cache_shas()
        }
        self.assertTrue(all(v == "2026-11-14" for v in newest_before.values()), newest_before)
        shas_before = self.cache_shas()
        report_before = sha(self.tmp / "report.md")

        # one rerun: same cache, older PT window, same report path
        second = self.run_cli(week_old, "2026-11-04", "2026-11-10", self.tmp / "report.md")
        self.assertEqual(second.returncode, ad.STALE_EXIT_CODE, second.stderr)
        self.assertEqual(self.cache_shas(), shas_before, "cache was modified by the stale pull")
        self.assertEqual(sha(self.tmp / "report.md"), report_before, "report was overwritten")
        blocked = [ln for ln in second.stderr.splitlines() if "BLOCKED stale overwrite" in ln]
        self.assertEqual(len(blocked), 5, second.stderr)  # 4 cache files + the report
        self.assertIn("existing newest PT date 2026-11-14 is newer than incoming 2026-11-10", second.stderr)
        self.assertNotIn("cache wrote", second.stderr)

    def test_stale_pull_still_renders_older_window_into_a_new_report(self):
        week_new = [f"2026-11-{d:02d}" for d in (8, 9, 10, 11, 12, 13, 14)]
        week_old = [f"2026-11-{d:02d}" for d in (4, 5, 6, 7, 8, 9, 10)]
        self.assertEqual(self.run_cli(week_new, "2026-11-08", "2026-11-14", self.tmp / "a.md").returncode, 0)
        shas_before = self.cache_shas()
        # A different output path: the cache is still protected, the report is written
        # from the newer cache rows filtered to the requested (older) window.
        r = self.run_cli(week_old, "2026-11-04", "2026-11-10", self.tmp / "b.md")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.cache_shas(), shas_before)
        self.assertIn("BLOCKED stale overwrite", r.stderr)
        self.assertTrue((self.tmp / "b.md").exists())

    def test_forward_pull_still_writes(self):
        self.assertEqual(
            self.run_cli([f"2026-11-{d:02d}" for d in (4, 5, 6)], "2026-11-04", "2026-11-06", self.tmp / "r1.md").returncode,
            0,
        )
        r = self.run_cli([f"2026-11-{d:02d}" for d in (8, 9, 10, 11, 12, 13, 14)], "2026-11-08", "2026-11-14", self.tmp / "r2.md")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("cache wrote", r.stderr)
        for name in self.cache_shas():
            self.assertEqual(ad.newest_pt_date_in_json_file(self.cache / name), "2026-11-14")

    def test_allow_stale_write_override(self):
        self.assertEqual(
            self.run_cli([f"2026-11-{d:02d}" for d in (8, 9, 10, 11, 12, 13, 14)], "2026-11-08", "2026-11-14", self.tmp / "x.md").returncode,
            0,
        )
        r = self.run_cli(
            [f"2026-11-{d:02d}" for d in (4, 5, 6, 7, 8, 9, 10)],
            "2026-11-04", "2026-11-10", self.tmp / "x.md", extra=["--allow-stale-write"],
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("cache wrote", r.stderr)

    # --- peer review 2026-11-16 03:3x JST: the two extra loss paths, end to end ---

    def test_incident_replay_same_newest_date_fewer_days_is_blocked(self):
        """Review case 2: cache [11/08..11/14] must survive a pull of [11/14] only."""
        week_new = [f"2026-11-{d:02d}" for d in (8, 9, 10, 11, 12, 13, 14)]
        first = self.run_cli(week_new, "2026-11-08", "2026-11-14", self.tmp / "a.md")
        self.assertEqual(first.returncode, 0, first.stderr)
        shas_before = self.cache_shas()
        self.assertEqual(len(shas_before), 4)

        second = self.run_cli(["2026-11-14"], "2026-11-08", "2026-11-14", self.tmp / "b.md")
        # The report path is new, so the run itself succeeds; the cache must not move.
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(self.cache_shas(), shas_before, "coverage loss was accepted")
        blocked = [ln for ln in second.stderr.splitlines() if "BLOCKED stale overwrite" in ln]
        self.assertEqual(len(blocked), 4, second.stderr)  # 4 cache files, report is fresh
        self.assertIn("same newest PT date but coverage would shrink", second.stderr)
        self.assertIn("2026-11-08", second.stderr)
        # the protected cache still carries the whole measured week into the report
        body = (self.tmp / "b.md").read_text()
        for d in week_new:
            self.assertIn(d, body)

    def test_report_without_window_end_cannot_replace_dated_report(self):
        """Review case 1: a run with no verifiable window end exits 3, report kept."""
        week = [f"2026-11-{d:02d}" for d in (8, 9, 10, 11, 12, 13, 14)]
        r1 = self.run_cli(week, "2026-11-08", "2026-11-14", self.tmp / "r.md")
        self.assertEqual(r1.returncode, 0, r1.stderr)
        report = self.tmp / "r.md"
        self.assertIn("2026-11-14 PT", report.read_text())
        before = sha(report)

        # --end "" => the rendered window has no verifiable end
        r2 = self.run_cli(week, "2026-11-08", "", report)
        self.assertEqual(r2.returncode, ad.STALE_EXIT_CODE, r2.stderr)
        self.assertEqual(sha(report), before, "dated report was replaced by an undated one")
        self.assertIn("no verifiable window end", r2.stderr)
        self.assertIn("refused to write", r2.stderr)

    def test_same_window_repull_still_writes(self):
        week = [f"2026-11-{d:02d}" for d in (8, 9, 10, 11, 12, 13, 14)]
        self.assertEqual(self.run_cli(week, "2026-11-08", "2026-11-14", self.tmp / "c.md").returncode, 0)
        shas_before = self.cache_shas()
        r = self.run_cli(week, "2026-11-08", "2026-11-14", self.tmp / "c.md")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("BLOCKED stale overwrite", r.stderr)
        self.assertEqual(len([ln for ln in r.stderr.splitlines() if "cache wrote" in ln]), 4, r.stderr)
        self.assertEqual(sorted(self.cache_shas()), sorted(shas_before))


if __name__ == "__main__":
    unittest.main(verbosity=2)
