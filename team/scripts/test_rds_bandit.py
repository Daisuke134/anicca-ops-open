"""Tests for the RDS notification-slot bandit. All rates are fictional."""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rds_bandit import RDSArmChooser, simulate

ARMS = ["a", "b", "c"]


def test_deterministic_with_seed():
    rates = {"a": 0.05, "b": 0.20, "c": 0.05}
    r1 = simulate(n_users=50, n_days=20, true_rates=rates, seed=7)
    r2 = simulate(n_users=50, n_days=20, true_rates=rates, seed=7)
    assert r1 == r2

    c = RDSArmChooser()
    hist = [("a", 1.0), ("b", 0.0), ("a", 1.0)]
    picks1 = [c.choose(hist, ARMS, random.Random(i)) for i in range(20)]
    picks2 = [c.choose(hist, ARMS, random.Random(i)) for i in range(20)]
    assert picks1 == picks2


def test_rds_beats_fixed_baseline():
    rates = {"a": 0.05, "b": 0.20, "c": 0.05}
    result = simulate(n_users=200, n_days=30, true_rates=rates, seed=42)
    assert result["rds"] > result["fixed"]
    assert result["fixed_arm"] == "a"
    # Sanity: baseline should be near arm a's fictional rate.
    assert abs(result["fixed"] - 0.05) < 0.03
    assert result["rds"] > 0.10


def test_recency_penalty_lowers_repeat_chance():
    # Equal rewards everywhere; only the recency penalty can make the most
    # recently used arm less likely.
    history = []
    for _ in range(6):
        history += [("a", 0.0), ("b", 0.0), ("c", 0.0)]
    history.append(("a", 0.0))  # most recent send was arm "a"

    n = 4000
    no_penalty = RDSArmChooser(tau=0.05, k=0, recency_penalty=0.0)
    with_penalty = RDSArmChooser(tau=0.05, k=3, gamma=0.5, recency_penalty=0.5)

    rng = random.Random(123)
    repeats_plain = sum(1 for _ in range(n) if no_penalty.choose(history, ARMS, rng) == "a")
    repeats_penalized = sum(1 for _ in range(n) if with_penalty.choose(history, ARMS, rng) == "a")

    assert repeats_penalized < repeats_plain
    # Roughly uniform without penalty (~1/3); clearly reduced with penalty.
    assert repeats_penalized < 0.30 * n
    assert repeats_plain > 0.28 * n


def test_small_tau_picks_argmax():
    # Rewards chosen so arm "b" has the highest mean.
    history = [("a", 0.0)] * 4 + [("b", 1.0)] * 4 + [("c", 0.0)] * 4
    chooser = RDSArmChooser(tau=1e-6, k=0, recency_penalty=0.0)
    rng = random.Random(99)
    picks = [chooser.choose(history, ARMS, rng) for _ in range(200)]
    assert all(p == "b" for p in picks)

    # Sanity check on scores: b's difference score is positive, others negative.
    scores = chooser.scores(history, ARMS)
    assert scores["b"] > scores["a"]
    assert scores["b"] > scores["c"]
