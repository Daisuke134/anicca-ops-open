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
