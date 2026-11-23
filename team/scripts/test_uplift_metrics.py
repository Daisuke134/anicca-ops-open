"""Tests for uplift_metrics.py CLI and metric functions."""

import json
import random
import subprocess
import sys
from pathlib import Path

import pytest

import uplift_metrics

SCRIPT = Path(__file__).with_name("uplift_metrics.py")


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


def write_csv(tmp_path, lines):
    path = tmp_path / "data.csv"
    path.write_text("\n".join(lines) + "\n")
    return path


GOOD_ROWS = [
    "1,1,0.9",
    "1,0,0.8",
    "0,1,0.7",
    "0,0,0.6",
    "1,1,0.5",
    "0,0,0.4",
    "1,0,0.3",
    "0,1,0.2",
]


def test_cli_basic(tmp_path):
    path = write_csv(tmp_path, ["treatment,outcome,score", *GOOD_ROWS])
    proc = run_cli(str(path))
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert out["n"] == 8
    assert out["skipped"] == 0
    assert out["qini"] is not None
    assert out["auuc"] is not None


def test_cli_matches_functions(tmp_path):
    path = write_csv(tmp_path, ["treatment,outcome,score", *GOOD_ROWS])
    proc = run_cli(str(path))
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    treatment, outcome, score = [], [], []
    for line in GOOD_ROWS:
        t, o, s = line.split(",")
        treatment.append(float(t))
        outcome.append(float(o))
        score.append(float(s))
    assert out["qini"] == pytest.approx(uplift_metrics.qini(treatment, outcome, score))
    assert out["auuc"] == pytest.approx(uplift_metrics.auuc(treatment, outcome, score))


def test_cli_skips_bad_rows(tmp_path):
    rows = GOOD_ROWS[:4] + ["1,abc,0.5", "0,1,", "x,1,0.3", "1,0,0.1"]
    path = write_csv(tmp_path, ["treatment,outcome,score", *rows])
    proc = run_cli(str(path))
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert out["n"] == 5
    assert out["skipped"] == 3


def test_cli_empty_file(tmp_path):
    path = write_csv(tmp_path, [])
    proc = run_cli(str(path))
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert out == {"n": 0, "qini": None, "auuc": None, "skipped": 0}


def test_cli_header_only(tmp_path):
    path = write_csv(tmp_path, ["treatment,outcome,score"])
    proc = run_cli(str(path))
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert out["n"] == 0
    assert out["qini"] is None
    assert out["auuc"] is None


def test_cli_usage_bad_args(tmp_path):
    proc = run_cli()
    assert proc.returncode == 2
    assert "usage" in proc.stderr.lower()
    proc = run_cli("a.csv", "b.csv")
    assert proc.returncode == 2
    assert "usage" in proc.stderr.lower()


def test_cli_missing_file(tmp_path):
    proc = run_cli(str(tmp_path / "nope.csv"))
    assert proc.returncode != 0


def test_qini_positive_for_good_score():
    # Perfect ranking: highest scores have the largest uplift.
    treatment = [1, 1, 0, 0]
    outcome = [1, 0, 1, 0]
    score = [0.9, 0.8, 0.2, 0.1]
    assert uplift_metrics.qini(treatment, outcome, score) > 0
    assert uplift_metrics.auuc(treatment, outcome, score) is not None


def test_metrics_degenerate_inputs():
    assert uplift_metrics.qini([], [], []) is None
    assert uplift_metrics.auuc([], [], []) is None
    # Single arm only.
    assert uplift_metrics.qini([1, 1], [1, 0], [0.5, 0.4]) is None
    assert uplift_metrics.auuc([0, 0], [1, 0], [0.5, 0.4]) is None


def test_cli_main_returns_0(tmp_path, monkeypatch, capsys):
    path = write_csv(tmp_path, ["treatment,outcome,score", *GOOD_ROWS])
    monkeypatch.setattr(sys, "argv", ["uplift_metrics.py", str(path)])
    assert uplift_metrics.main() == 0
    out = json.loads(capsys.readouterr().out)
    assert out["n"] == 8


def test_qini_fixture_random_vs_oracle():
    rng = random.Random(0)
    n = 200
    treatment = [1] * 100 + [0] * 100
    rng.shuffle(treatment)

    tau = [0.0] * n
    treated_idx = [i for i, t in enumerate(treatment) if t]
    for i in treated_idx[:80]:
        tau[i] = 1.0

    lift = 0.006
    outcome = [lift if tau[i] else 0.0 for i in range(n)]
    oracle_score = list(tau)
    random_score = [rng.random() for _ in range(n)]

    assert uplift_metrics.qini(treatment, outcome, oracle_score) > 0.1
    assert abs(uplift_metrics.qini(treatment, outcome, random_score)) < 0.05
