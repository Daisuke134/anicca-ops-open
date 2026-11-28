"""Tests for gemini_safe_commit.recently_failed_ids / pick_next skip."""
from __future__ import annotations

import datetime
import os
import tempfile
import unittest
from pathlib import Path

import gemini_safe_commit as g


class RecentlyFailedIdsTest(unittest.TestCase):
    def test_skips_repeated_recent_failures_and_prefers_fresh_task(self) -> None:
        now = datetime.datetime.now()
        older = (now - datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M")
        recent = now.strftime("%Y-%m-%d %H:%M")
        with tempfile.NamedTemporaryFile("w", suffix=".log", delete=False) as fh:
            fh.write(
                f"[{older} JST] FAIL OLD-TASK gemini_rc=1 guard_rc=11 100s\n"
                + (
                    f"[{recent} JST] FAIL T4329U-GM-JAKUB gemini_rc=1 guard_rc=11 361s\n"
                    * 3
                )
            )
            path = Path(fh.name)
        try:
            ids = g.recently_failed_ids(log_path=path, hours=3.0, min_fails=2)
            self.assertIn("T4329U-GM-JAKUB", ids)
            self.assertNotIn("OLD-TASK", ids)
            prev = g.FAIL_LOG
            g.FAIL_LOG = path
            try:
                items = [
                    ("T4329U-GM-JAKUB", "- [ ] T4329U-GM-JAKUB do research"),
                    ("T1128U-1015-GM-POSTING-TIMES", "- [ ] T1128U-1015-GM-POSTING-TIMES write schedule"),
                ]
                hit = g.pick_next(items)
                self.assertIsNotNone(hit)
                self.assertEqual(hit[0], "T1128U-1015-GM-POSTING-TIMES")
                self.assertIsNone(g.pick_next([items[0]]))
            finally:
                g.FAIL_LOG = prev
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
