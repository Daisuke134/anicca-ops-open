#!/usr/bin/env python3
"""Print the trend of the last two rows of the ct-bench metrics CSV.

Usage: ct_bench_trend.py [CSV]

CSV columns: ts_jst,probe,pass,n,na,err
Exit codes: 0 ok / no regression, 1 pass decreased or err increased,
            2 missing or empty CSV.
"""

import csv
import sys
from pathlib import Path

DEFAULT_CSV = Path(__file__).resolve().parent.parent / "metrics" / "ct-bench.csv"


def load_rows(path):
    try:
        text = Path(path).read_text()
    except OSError:
        return None
    return list(csv.DictReader(text.splitlines()))


def fmt(row):
    return (
        f"{row['pass']}/{row['n']} err={row['err']} ({row['ts_jst']})"
    )


def main(argv):
    path = argv[1] if len(argv) > 1 else DEFAULT_CSV
    rows = load_rows(path)
    if not rows:
        print(f"error: missing or empty CSV: {path}", file=sys.stderr)
        return 2

    last = rows[-1]
    last_pass = int(last["pass"])
    last_err = int(last["err"])

    if len(rows) == 1:
        print(f"last {fmt(last)} (no prev)")
        return 0

    prev = rows[-2]
    prev_pass = int(prev["pass"])
    prev_err = int(prev["err"])

    print(f"last {fmt(last)} vs prev {fmt(prev)}")
    print(f"delta pass={last_pass - prev_pass:+d} err={last_err - prev_err:+d}")

    return 1 if (last_pass < prev_pass or last_err > prev_err) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
