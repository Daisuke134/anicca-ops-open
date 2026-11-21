import csv
import json
import math
import statistics
import subprocess
import sys
from pathlib import Path

import pytest

from presim_calib_report import report


def test_exact_match_zero_error():
    result = report([{"pred_impr": 100, "actual_impr": 100, "format": "video"}])
    assert result["overall"] == {"n": 1, "median_abs_ln_err": 0.0}
    assert result["by_format"]["video"] == {"n": 1, "median_abs_ln_err": 0.0}


def test_mismatch_abs_ln_err():
    result = report([{"pred_impr": 2482, "actual_impr": 2102, "format": "video"}])
    expected = abs(math.log(2482) - math.log(2102))
    assert result["overall"]["median_abs_ln_err"] == pytest.approx(expected, abs=1e-4)
    assert result["overall"]["median_abs_ln_err"] == pytest.approx(0.1662, abs=1e-4)


def test_median_with_multiple_rows():
    rows = [
        {"pred_impr": 100, "actual_impr": 100, "format": "a"},
        {"pred_impr": 200, "actual_impr": 100, "format": "a"},
        {"pred_impr": 300, "actual_impr": 100, "format": "b"},
    ]
    result = report(rows)
    assert result["overall"]["n"] == 3
    expected_overall = statistics.median([
        abs(math.log(100) - math.log(100)),
        abs(math.log(200) - math.log(100)),
        abs(math.log(300) - math.log(100)),
    ])
    assert result["overall"]["median_abs_ln_err"] == pytest.approx(expected_overall)
    assert result["by_format"]["a"]["n"] == 2
    assert result["by_format"]["b"]["n"] == 1


def test_blank_format_goes_to_other():
    result = report([
        {"pred_impr": 100, "actual_impr": 50, "format": ""},
        {"pred_impr": 100, "actual_impr": 50},
        {"pred_impr": 100, "actual_impr": 50, "format": "   "},
    ])
    assert result["overall"]["n"] == 3
    assert list(result["by_format"]) == ["other"]
    assert result["by_format"]["other"]["n"] == 3
    assert result["by_format"]["other"]["median_abs_ln_err"] == pytest.approx(math.log(2))


def test_bad_rows_skipped():
    rows = [
        {"pred_impr": "", "actual_impr": 100, "format": "a"},
        {"pred_impr": 100, "actual_impr": "abc", "format": "a"},
        {"pred_impr": 0, "actual_impr": 100, "format": "a"},
        {"pred_impr": 100, "actual_impr": -5, "format": "a"},
        {"pred_impr": None, "actual_impr": 100, "format": "a"},
        {"pred_impr": 100, "actual_impr": 100, "format": "a"},
    ]
    result = report(rows)
    assert result["overall"]["n"] == 1
    assert result["overall"]["median_abs_ln_err"] == 0.0


def test_empty_input():
    assert report([]) == {
        "overall": {"n": 0, "median_abs_ln_err": None},
        "by_format": {},
    }


def test_all_rows_invalid():
    rows = [{"pred_impr": "x", "actual_impr": "y", "format": "a"}]
    assert report(rows) == {
        "overall": {"n": 0, "median_abs_ln_err": None},
        "by_format": {},
    }


def test_cli_prints_json(tmp_path):
    csv_path = tmp_path / "rows.csv"
    with open(csv_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["pred_impr", "actual_impr", "format"])
        writer.writeheader()
        writer.writerow({"pred_impr": 100, "actual_impr": 100, "format": "video"})
        writer.writerow({"pred_impr": "bad", "actual_impr": 5, "format": "video"})
    script = Path(__file__).with_name("presim_calib_report.py")
    proc = subprocess.run(
        [sys.executable, script, str(csv_path)],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(proc.stdout)
    assert data["overall"]["n"] == 1
    assert data["overall"]["median_abs_ln_err"] == 0.0
    assert data["by_format"]["video"]["n"] == 1
