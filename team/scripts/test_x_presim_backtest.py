import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import x_presim as xp
import x_presim_backtest as xpb

FETCHED = "2026-11-10T00:00:00Z"


def write_originals(tmp_path):
    posts = [
        {"id": "p1", "created_at": "2026-11-01T00:00:00Z", "text": "We shipped 3 paid apps in 30 days. Revenue is up.",
         "public_metrics": {"impression_count": 100}},
        {"id": "p2", "created_at": "2026-11-02T00:00:00Z", "text": "Our agent evals failed twice before this worked.",
         "public_metrics": {"impression_count": 250}},
        {"id": "p3", "created_at": "2026-11-03T00:00:00Z", "text": "New open-source plugin on GitHub for Claude.",
         "public_metrics": {"impression_count": 400}},
        {"id": "p4", "created_at": "2026-11-04T00:00:00Z", "text": "Why does sleep affect app retention?",
         "public_metrics": {"impression_count": 80}},
        # younger than 24h before fetched_at -> excluded
        {"id": "p5", "created_at": "2026-11-09T12:00:00Z", "text": "Fresh post not old enough yet.",
         "public_metrics": {"impression_count": 999}},
        # starts with '@' -> excluded
        {"id": "p6", "created_at": "2026-11-05T00:00:00Z", "text": "@someone thanks for the feedback",
         "public_metrics": {"impression_count": 999}},
    ]
    path = tmp_path / "originals.json"
    path.write_text(json.dumps(posts), encoding="utf-8")
    return path


@pytest.fixture(autouse=True)
def fixed_baseline(monkeypatch):
    monkeypatch.setattr(xp, "baseline", lambda account: 50.0)


def test_exclusions_and_n(tmp_path, capsys):
    path = write_originals(tmp_path)
    out = tmp_path / "out.json"
    xpb.main(str(path), FETCHED, str(out))
    res = json.loads(capsys.readouterr().out)
    assert res["n"] == 4


def test_output_json_schema(tmp_path):
    path = write_originals(tmp_path)
    out = tmp_path / "out.json"
    xpb.main(str(path), FETCHED, str(out))
    res = json.loads(out.read_text(encoding="utf-8"))
    for k in ("sim", "shrink", "naive"):
        assert "median_abs_log_err" in res[k]
        assert "spearman" in res[k]
    assert res["naive"]["spearman"] is None
    assert res["skill_vs_naive"] == round(1 - res["sim"]["median_abs_log_err"] / res["naive"]["median_abs_log_err"], 3)


def test_spearman_identical_and_reversed():
    assert xpb.spearman([1, 2, 3, 4], [1, 2, 3, 4]) == pytest.approx(1.0)
    assert xpb.spearman([1, 2, 3, 4], [4, 3, 2, 1]) == pytest.approx(-1.0)
