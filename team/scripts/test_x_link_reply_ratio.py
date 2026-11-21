"""Tests for x_link_reply_ratio."""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from x_link_reply_ratio import ratios


def test_median_for_connect_format():
    pairs = [
        {"parent_impr": 646, "reply_impr": 42, "format": "connect"},
        {"parent_impr": 1078, "reply_impr": 99, "format": "connect"},
    ]
    result = ratios(pairs)
    assert result["connect"] == pytest.approx(0.0784, abs=1e-4)


def test_individual_ratios():
    pairs = [
        {"parent_impr": 646, "reply_impr": 42, "format": "connect"},
        {"parent_impr": 1078, "reply_impr": 99, "format": "connect"},
        {"parent_impr": 185, "reply_impr": 42, "format": "other"},
    ]
    result = ratios(pairs)
    assert result["connect"] == pytest.approx((42 / 646 + 99 / 1078) / 2)
    assert result["other"] == pytest.approx(42 / 185)


def test_skips_nonpositive_parent():
    pairs = [
        {"parent_impr": 0, "reply_impr": 10, "format": "connect"},
        {"parent_impr": -5, "reply_impr": 10, "format": "connect"},
        {"parent_impr": 100, "reply_impr": 10, "format": "connect"},
    ]
    result = ratios(pairs)
    assert result["connect"] == pytest.approx(0.1)


def test_blank_format_maps_to_other():
    pairs = [
        {"parent_impr": 100, "reply_impr": 5, "format": ""},
        {"parent_impr": 100, "reply_impr": 10, "format": None},
        {"parent_impr": 200, "reply_impr": 20, "format": "video"},
    ]
    result = ratios(pairs)
    assert result["other"] == pytest.approx(0.075)
    assert result["video"] == pytest.approx(0.1)


def test_empty_returns_empty_dict():
    assert ratios([]) == {}


def test_cli(tmp_path, capsys):
    csv_path = tmp_path / "pairs.csv"
    csv_path.write_text(
        "parent_impr,reply_impr,format\n"
        "646,42,connect\n"
        "1078,99,connect\n"
        "185,42,other\n"
    )
    script = Path(__file__).parent / "x_link_reply_ratio.py"
    proc = subprocess.run(
        [sys.executable, str(script), str(csv_path)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    out = proc.stdout.strip().splitlines()
    assert out == [
        f"connect\t2\t{(42/646 + 99/1078)/2:.4f}",
        f"other\t1\t{42/185:.4f}",
    ]
