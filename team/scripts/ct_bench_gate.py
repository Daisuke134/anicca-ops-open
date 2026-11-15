#!/usr/bin/env python3
"""Gate check for ct-bench.csv: fails if errors went up or pass ratio went down."""

import csv
import os
import sys

DEFAULT_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "metrics", "ct-bench.csv")


def load_rows(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return [r for r in reader]


def _metrics(row):
    return (int(row["pass"]), int(row["n"]), int(row["err"]))


def gate(rows):
    """Take the last two data rows; return (ok, reason)."""
    if len(rows) < 2:
        return True, "insufficient"
    prev = _metrics(rows[-2])
    last = _metrics(rows[-1])
    if last[2] > prev[2]:
        return False, "err up"
    prev_ratio = prev[0] / prev[1] if prev[1] else 0.0
    last_ratio = last[0] / last[1] if last[1] else 0.0
    if last_ratio < prev_ratio:
        return False, "pass ratio down"
    return True, "ok"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0] if argv else DEFAULT_CSV
    ok, reason = gate(load_rows(path))
    print(f"GATE {'OK' if ok else 'FAIL'} {reason}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
