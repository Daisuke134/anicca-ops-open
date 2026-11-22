"""Uplift metrics: Qini-style coefficient and AUUC from treatment/outcome/score data.

CLI: python3 uplift_metrics.py <csv>
CSV columns: treatment (0/1), outcome (0/1 or float), score.
Prints JSON {"n":..,"qini":..,"auuc":..,"skipped":..}.
"""

import csv
import json
import sys


def _curve(treatment, outcome, score):
    """Return (xs, gains, n) for the cumulative uplift curve, or None if degenerate."""
    n = len(treatment)
    if n == 0:
        return None
    t_total = sum(1 for t in treatment if t)
    c_total = n - t_total
    if t_total == 0 or c_total == 0:
        return None

    order = sorted(range(n), key=lambda i: score[i], reverse=True)
    scale = t_total / c_total
    xs = [0.0]
    gains = [0.0]
    cum_t = 0.0
    cum_c = 0.0
    for k, i in enumerate(order, 1):
        if treatment[i]:
            cum_t += outcome[i]
        else:
            cum_c += outcome[i]
        xs.append(k / n)
        gains.append(cum_t - cum_c * scale)
    return xs, gains, n


def auuc(treatment, outcome, score):
    """Area under the cumulative uplift curve (trapezoidal), or None if degenerate."""
    curve = _curve(treatment, outcome, score)
    if curve is None:
        return None
    xs, gains, _ = curve
    area = 0.0
    for i in range(1, len(xs)):
        area += (xs[i] - xs[i - 1]) * (gains[i] + gains[i - 1]) / 2.0
    return area


def qini(treatment, outcome, score):
    """Qini coefficient: AUUC minus the expected AUUC under random ordering.

    Under random ordering the expected cumulative gain at fraction i/n is
    (i/n) * (Y_t - (T/C) * Y_c), a straight line, so its area is G_N / 2.
    """
    curve = _curve(treatment, outcome, score)
    if curve is None:
        return None
    xs, gains, n = curve
    area = 0.0
    for i in range(1, len(xs)):
        area += (xs[i] - xs[i - 1]) * (gains[i] + gains[i - 1]) / 2.0
    y_t = sum(o for t, o in zip(treatment, outcome) if t)
    y_c = sum(o for t, o in zip(treatment, outcome) if not t)
    t_total = sum(1 for t in treatment if t)
    c_total = n - t_total
    g_n = y_t - (t_total / c_total) * y_c
    return area - g_n / 2.0


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: uplift_metrics.py <csv>", file=sys.stderr)
        return 2

    treatment, outcome, score = [], [], []
    skipped = 0
    try:
        with open(args[0], newline="") as f:
            for row in csv.DictReader(f):
                try:
                    t = float(row["treatment"])
                    o = float(row["outcome"])
                    s = float(row["score"])
                except (KeyError, TypeError, ValueError):
                    skipped += 1
                    continue
                treatment.append(t)
                outcome.append(o)
                score.append(s)
    except OSError as e:
        print(f"uplift_metrics.py: {e}", file=sys.stderr)
        return 1

    result = {
        "n": len(treatment),
        "qini": qini(treatment, outcome, score),
        "auuc": auuc(treatment, outcome, score),
        "skipped": skipped,
    }
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
