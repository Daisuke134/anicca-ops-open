"""Recovering Difference Softmax (RDS) arm chooser.

Implements the bandit from Yancey & Settles, "Solving the User-Arm Allocation
Problem..." style RDS (KDD 2020), used here to pick a notification send slot
per user.

Score for an arm = mean reward of that arm minus the mean reward over all
arms (the "difference" term). A recency penalty is subtracted for arms used in
the last ``k`` sends; the penalty decays by ``gamma`` per send ("recovering").
A softmax with temperature ``tau`` turns scores into a sampling distribution.

Pure Python, no numpy required.
"""

import argparse
import json
import math
import random


def _arm_stats(history, arms):
    """Return (sum_rewards, counts) dicts for each arm seen in history."""
    sums = {}
    counts = {}
    for arm, reward in history:
        sums[arm] = sums.get(arm, 0.0) + reward
        counts[arm] = counts.get(arm, 0) + 1
    return sums, counts


class RDSArmChooser:
    """Recovering Difference Softmax chooser.

    Parameters
    ----------
    tau : float
        Softmax temperature (default 0.05).
    k : int
        Number of most recent sends over which the recency penalty applies
        (default 3). ``k=0`` disables the penalty.
    gamma : float
        Decay factor applied per send to the recency penalty (default 0.5).
    recency_penalty : float
        Magnitude of the penalty applied to the most recent send of an arm
        (default 0.5).
    """

    def __init__(self, tau=0.05, k=3, gamma=0.5, recency_penalty=0.5):
        if tau <= 0:
            raise ValueError("tau must be positive")
        if k < 0:
            raise ValueError("k must be non-negative")
        if not 0.0 <= gamma <= 1.0:
            raise ValueError("gamma must be in [0, 1]")
        if recency_penalty < 0:
            raise ValueError("recency_penalty must be non-negative")
        self.tau = tau
        self.k = k
        self.gamma = gamma
        self.recency_penalty = recency_penalty

    def scores(self, history, arms):
        """Compute the RDS score for each arm.

        ``history`` is an iterable of ``(arm, reward)`` pairs, oldest first.
        Returns a dict mapping each arm in ``arms`` to its score.
        """
        arms = list(arms)
        sums, counts = _arm_stats(history, arms)

        means = {}
        for arm in arms:
            if counts.get(arm, 0) > 0:
                means[arm] = sums[arm] / counts[arm]
            else:
                means[arm] = 0.0

        sampled_means = [means[a] for a in arms if counts.get(a, 0) > 0]
        overall = sum(sampled_means) / len(sampled_means) if sampled_means else 0.0

        scores = {a: means[a] - overall for a in arms}

        # Recency penalty: walk the last k sends, most recent first. The most
        # recent use gets the full penalty, decaying by gamma per send.
        if self.k > 0 and self.recency_penalty > 0:
            recent = list(history)[-self.k:]
            for pos, (arm, _reward) in enumerate(reversed(recent)):
                if arm in scores:
                    scores[arm] -= self.recency_penalty * (self.gamma ** pos)

        return scores

    def probabilities(self, history, arms):
        """Softmax probabilities over arms for the given history."""
        scores = self.scores(history, arms)
        arms = list(arms)
        logits = [scores[a] / self.tau for a in arms]
        m = max(logits)
        exps = [math.exp(x - m) for x in logits]
        total = sum(exps)
        return {a: e / total for a, e in zip(arms, exps)}

    def choose(self, history, arms, rng):
        """Pick an arm according to the RDS softmax distribution.

        ``rng`` is a ``random.Random`` instance (or anything with ``random()``).
        """
        arms = list(arms)
        if not arms:
            raise ValueError("arms must be non-empty")
        probs = self.probabilities(history, arms)
        r = rng.random()
        cum = 0.0
        for arm in arms:
            cum += probs[arm]
            if r < cum:
                return arm
        return arms[-1]


def simulate(n_users, n_days, true_rates, seed):
    """Simulate RDS vs a fixed single-slot baseline on fictional rates.

    Parameters
    ----------
    n_users : int
        Number of users to simulate.
    n_days : int
        Number of days (one send decision per day per user).
    true_rates : dict
        Fictional per-arm reward probabilities, e.g. ``{"a": 0.05, ...}``.
    seed : int
        RNG seed for reproducibility.

    Returns
    -------
    dict
        ``{"rds": mean reward per send, "fixed": mean reward per send,
        "fixed_arm": the baseline arm}``.
    """
    arms = list(true_rates.keys())
    if not arms:
        raise ValueError("true_rates must be non-empty")
    fixed_arm = arms[0]
    chooser = RDSArmChooser()
    master = random.Random(seed)

    rds_total = 0.0
    fixed_total = 0.0
    sends = 0

    for _ in range(n_users):
        user_rng = random.Random(master.random())
        history = []
        for _day in range(n_days):
            arm = chooser.choose(history, arms, user_rng)
            reward = 1.0 if user_rng.random() < true_rates[arm] else 0.0
            history.append((arm, reward))
            rds_total += reward

            fixed_total += 1.0 if user_rng.random() < true_rates[fixed_arm] else 0.0
            sends += 1

    return {
        "rds": rds_total / sends,
        "fixed": fixed_total / sends,
        "fixed_arm": fixed_arm,
    }


def replay_value(logs, policy):
    """Offline replay evaluation (Li et al. 2010, arXiv:1003.0146).

    ``logs`` are dicts ``{"context": ..., "action": ..., "reward": ...}``
    collected with a uniform random action policy. ``policy`` is a callable
    mapping a context to an action.

    Only events where ``policy(context) == action`` are kept (the logged
    action must match what the policy would have chosen). Returns
    ``(mean_reward, kept_count)``; ``(None, 0)`` when nothing matches.
    """
    total = 0.0
    kept = 0
    for event in logs:
        if policy(event["context"]) == event["action"]:
            total += event["reward"]
            kept += 1
    if kept == 0:
        return None, 0
    return total / kept, kept


def _fixed_arm_mean(n_users, n_days, rate, seed):
    """Mean reward of always sending a single arm with the given rate."""
    rng = random.Random(seed)
    sends = n_users * n_days
    total = sum(1.0 if rng.random() < rate else 0.0 for _ in range(sends))
    return total / sends


def parse_rates(text):
    """Parse a comma-separated ``arm=rate`` string into an ordered dict."""
    rates = {}
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        name, sep, value = part.partition("=")
        name = name.strip()
        if not sep or not name:
            raise ValueError(f"invalid rate entry {part!r}; expected arm=rate")
        rate = float(value)
        if not 0.0 <= rate <= 1.0:
            raise ValueError(f"rate for arm {name!r} must be in [0, 1]")
        rates[name] = rate
    if not rates:
        raise ValueError("rates must contain at least one arm")
    return rates


def _run_simulation(args):
    rates = parse_rates(args.rates)
    result = simulate(args.users, args.days, rates, args.seed)
    best_arm = max(rates, key=rates.get)
    best_fixed = _fixed_arm_mean(args.users, args.days, rates[best_arm], args.seed)
    return {
        "rds": result["rds"],
        "fixed": result["fixed"],
        "best_fixed": best_fixed,
        "regret_vs_best": best_fixed - result["rds"],
    }


def main(argv=None):
    """CLI entry point.

    ``--sim`` runs a seeded simulation over fictional arm rates and prints a
    JSON object with the RDS mean reward, the fixed-baseline mean reward, the
    oracle fixed-arm mean reward, and the regret versus that oracle.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sim", action="store_true",
                        help="run a seeded simulation and print JSON")
    parser.add_argument("--users", type=int, default=100,
                        help="number of simulated users (default 100)")
    parser.add_argument("--days", type=int, default=10,
                        help="number of simulated days per user (default 10)")
    parser.add_argument("--rates", default=None,
                        help="comma-separated arm=rate pairs, e.g. a=0.05,b=0.20")
    parser.add_argument("--seed", type=int, default=0,
                        help="RNG seed for reproducibility (default 0)")
    args = parser.parse_args(argv)

    if not args.sim:
        parser.error("the --sim flag is required")
    if args.users <= 0 or args.days <= 0:
        parser.error("--users and --days must be positive")
    if args.rates is None:
        parser.error("--rates is required with --sim")

    out = _run_simulation(args)
    print(json.dumps({k: round(v, 6) for k, v in out.items()}))


if __name__ == "__main__":
    main()
