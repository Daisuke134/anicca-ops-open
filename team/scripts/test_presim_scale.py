import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import presim_scale


@pytest.fixture
def csv_path(tmp_path):
    p = tmp_path / "presim-log.csv"
    p.write_text(
        "pred_impr,actual_impr,text_preview\n"
        "10,20,other: hello there\n"
        "10,15,other: checking in\n"
        "10,30,other: following up\n"
        "26,730,connect with builders today\n"
        "5,,other: still pending\n"
    )
    return p


def test_ratios(csv_path):
    r = presim_scale.ratios(csv_path)
    assert set(r) == {"other", "connect"}
    assert r["other"][1] == 3
    assert r["other"][0] == pytest.approx(2.0)
    assert r["connect"][1] == 1
    assert r["connect"][0] == pytest.approx(730 / 26)


def test_scaled_pred(csv_path):
    r = presim_scale.ratios(csv_path)
    assert presim_scale.scaled_pred("other", 50, r) == pytest.approx(100.0)
    assert presim_scale.scaled_pred("connect", 26, r) == 26
    assert presim_scale.scaled_pred("unknown", 10, r) == 10


def test_cli(csv_path, capsys):
    presim_scale.main([str(csv_path)])
    out = capsys.readouterr().out.strip().splitlines()
    assert out == [
        "connect ratio=28.08 n=1",
        "other ratio=2.00 n=3",
    ]
