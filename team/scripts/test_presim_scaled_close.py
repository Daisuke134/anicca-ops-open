"""Tests for presim_scaled_close: leave-one-out scaled close errors."""

import math
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import presim_scaled_close as psc

CSV_TEXT = (
    "text_preview,pred_impr,actual_impr\n"
    "hello there,10,20\n"
    "hi friend,10,20\n"
    "good morning,10,20\n"
    "see you soon,10,40\n"
    "connect with you,10,100\n"
)

LN2 = math.log(2)
LN4 = math.log(4)
LN10 = math.log(10)


def write_csv(tmp_path):
    p = tmp_path / "presim-log.csv"
    p.write_text(CSV_TEXT)
    return p


def test_load_rows_filters_closed(tmp_path):
    p = write_csv(tmp_path)
    rows = psc.load_rows(p)
    assert len(rows) == 5
    assert all(r["pred"] == 10 for r in rows)


def test_fmt_classification(tmp_path):
    p = write_csv(tmp_path)
    rows = psc.load_rows(p)
    fmts = sorted(r["fmt"] for r in rows)
    assert fmts.count("connect") == 1
    assert len(set(fmts)) == 2


def test_compute_hand_computed(tmp_path):
    stats = psc.compute(psc.load_rows(write_csv(tmp_path)))

    # 'other' rows: actual/pred ratios are 2,2,2,4.
    # LOO medians: rows with ratio 2 see others {2,2,4} -> 2;
    # the ratio-4 row sees {2,2,2} -> 2.
    other = stats["other"]
    assert other["n"] == 4
    assert other["raw"] == pytest.approx(LN2)
    assert other["scaled"] == pytest.approx(0.0)

    # 'connect' row: only one row in its format -> ratio stays 1.
    connect = stats["connect"]
    assert connect["n"] == 1
    assert connect["raw"] == pytest.approx(LN10)
    assert connect["scaled"] == pytest.approx(LN10)

    # ALL: raw values LN2,LN2,LN2,LN4,LN10 -> median LN2.
    # scaled values 0,0,0,LN2,LN10 -> median 0.
    all_ = stats["ALL"]
    assert all_["n"] == 5
    assert all_["raw"] == pytest.approx(LN2)
    assert all_["scaled"] == pytest.approx(0.0)


def test_loo_excludes_self_and_needs_three_others(tmp_path):
    # Only 3 rows in a format: each has exactly 2 others -> ratio 1.
    p = tmp_path / "c.csv"
    p.write_text(
        "text_preview,pred_impr,actual_impr\n"
        "a,10,20\n"
        "b,10,40\n"
        "c,10,80\n"
    )
    stats = psc.compute(psc.load_rows(p))
    # raw ratios 2,4,8 -> ln values ln2, ln4, ln8; median ln4.
    assert stats["other"]["raw"] == pytest.approx(LN4)
    # no scaling applied (fewer than 3 others) -> scaled == raw
    assert stats["other"]["scaled"] == pytest.approx(LN4)


def test_cli_output(tmp_path, capsys):
    p = write_csv(tmp_path)
    rc = psc.main([str(p)])
    assert rc == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert out[0] == "connect n=1 raw=2.30 scaled=2.30"
    assert out[1] == "other n=4 raw=0.69 scaled=0.00"
    assert out[2] == "ALL n=5 raw=0.69 scaled=0.00"


def test_cli_subprocess(tmp_path):
    p = write_csv(tmp_path)
    script = Path(psc.__file__)
    res = subprocess.run(
        [sys.executable, str(script), str(p)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "ALL n=5 raw=0.69 scaled=0.00" in res.stdout
