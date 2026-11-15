"""Tests for presim_format_report.py (self-contained: fake presim_calib)."""

import csv
import sys
import types
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

# presim_calib is not shipped in this checkout; inject a deterministic fake
# so the report's `from presim_calib import fmt` resolves predictably.
_fake_calib = types.ModuleType("presim_calib")


def _fake_fmt(text):
    t = (text or "").lower()
    if "connect" in t:
        return "connect"
    if "?" in t:
        return "question"
    return "other"


_fake_calib.fmt = _fake_fmt
sys.modules["presim_calib"] = _fake_calib

sys.path.insert(0, str(SCRIPTS_DIR))

import presim_format_report as report  # noqa: E402

HEADER = ["text_preview", "predicted_impr", "post_id", "actual_impr"]
ROWS = [
    # 2 connect: one closed (pred 26, actual 730), one posted but not closed
    ["connect tip: lead with the ask", "26", "1001", "730"],
    ["connect follow-up", "10", "1002", "0"],
    # 1 question, unposted
    ["quick question for the thread?", "5", "", "0"],
    # 2 other: one closed (pred 59, actual 11), one posted but not closed
    ["plain observation post", "59", "1003", "11"],
    ["another plain post", "7", "1004", "0"],
]


def _write_csv(tmp_path):
    path = tmp_path / "presim-log.csv"
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADER)
        writer.writerows(ROWS)
    return path


def _lines(capsys):
    return capsys.readouterr().out.strip().splitlines()


def test_connect_and_other_lines_exact(tmp_path, capsys):
    csv_path = _write_csv(tmp_path)
    assert report.main([str(csv_path)]) == 0
    lines = _lines(capsys)
    assert (
        "connect scored=2 posted=2 closed=1 "
        "median_pred=26 median_actual=730 ratio=28.08"
    ) in lines
    assert (
        "other scored=2 posted=2 closed=1 "
        "median_pred=59 median_actual=11 ratio=0.19"
    ) in lines


def test_sorted_formats_and_all_line(tmp_path, capsys):
    csv_path = _write_csv(tmp_path)
    report.main([str(csv_path)])
    lines = _lines(capsys)
    assert lines == [
        "connect scored=2 posted=2 closed=1 "
        "median_pred=26 median_actual=730 ratio=28.08",
        "other scored=2 posted=2 closed=1 "
        "median_pred=59 median_actual=11 ratio=0.19",
        "question scored=1 posted=0 closed=0 "
        "median_pred=- median_actual=- ratio=-",
        "all scored=5 posted=4 closed=2 "
        "median_pred=42.5 median_actual=370.5 ratio=8.72",
    ]
