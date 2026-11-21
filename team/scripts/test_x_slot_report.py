"""Tests for x_slot_report."""

import csv
import io
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

import x_slot_report


def test_format_medians_empty():
    assert x_slot_report.format_medians([]) == {}


def test_format_medians_groups_and_medians():
    rows = [
        ["connect", "10"],
        ["connect", "20"],
        ["connect", "30"],
        ["question", "100"],
        ["question", "200"],
        ["", "5"],
        ["nonsense", "7"],
    ]
    result = x_slot_report.format_medians(rows)
    assert result == {"connect": 20.0, "question": 150.0, "other": 6.0}


def test_format_medians_accepts_dicts():
    rows = [
        {"format": "connect", "impressions": "10"},
        {"format": "connect", "impressions": "30"},
        {"format": "Connect", "impressions": "20"},
        {"format": "", "impressions": "1"},
    ]
    result = x_slot_report.format_medians(rows)
    assert result == {"connect": 20.0, "other": 1.0}


def test_format_medians_skips_missing_impressions():
    rows = [["connect"], ["question", ""], ["question", None]]
    assert x_slot_report.format_medians(rows) == {}


def _write_csv(tmp_path, rows):
    path = tmp_path / "slots.csv"
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    return path


def test_by_format_cli_sorted_by_median_desc(tmp_path, capsys):
    rows = [
        ["connect", "10"],
        ["connect", "20"],
        ["connect", "30"],
        ["question", "100"],
        ["question", "200"],
        ["other", "5"],
        ["", "7"],
    ]
    path = _write_csv(tmp_path, rows)
    rc = x_slot_report.main([str(path), "--by-format"])
    assert rc == 0
    out = capsys.readouterr().out
    lines = out.strip().split("\n")
    assert lines[0].split("\t")[0] == "question"
    assert lines[-1].split("\t")[0] == "other"
    for line in lines:
        fmt, n, median = line.split("\t")
        assert n.isdigit()
        float(median)


def test_by_format_cli_empty_file(tmp_path, capsys):
    path = _write_csv(tmp_path, [["connect", "1"]])
    rc = x_slot_report.main([str(path), "--by-format"])
    assert rc == 0
    assert "connect\t1\t1.0" in capsys.readouterr().out
