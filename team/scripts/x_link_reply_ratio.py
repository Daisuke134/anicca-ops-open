"""Median reply-impression ratio per format for X link posts."""

import argparse
import csv
import sys
from collections import defaultdict
from statistics import median


def ratios(pairs):
    """Return {format: median(reply_impr / parent_impr)} for pairs.

    Skips pairs with parent_impr <= 0. Blank/missing formats are grouped
    under "other". Returns {} for empty input.
    """
    by_format = defaultdict(list)
    for pair in pairs:
        parent = pair.get("parent_impr", 0)
        if parent <= 0:
            continue
        fmt = pair.get("format") or ""
        fmt = fmt.strip() if isinstance(fmt, str) else fmt
        if not fmt:
            fmt = "other"
        by_format[fmt].append(pair.get("reply_impr", 0) / parent)
    return {fmt: median(vals) for fmt, vals in by_format.items()}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", help="CSV with parent_impr, reply_impr, format columns")
    args = parser.parse_args(argv)

    pairs = []
    with open(args.csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                pairs.append(
                    {
                        "parent_impr": float(row["parent_impr"]),
                        "reply_impr": float(row["reply_impr"]),
                        "format": row.get("format", ""),
                    }
                )
            except (KeyError, ValueError):
                continue

    # group to also report counts
    counts = defaultdict(int)
    vals = defaultdict(list)
    for pair in pairs:
        parent = pair["parent_impr"]
        if parent <= 0:
            continue
        fmt = pair["format"].strip() or "other"
        counts[fmt] += 1
        vals[fmt].append(pair["reply_impr"] / parent)

    for fmt in sorted(vals):
        print(f"{fmt}\t{counts[fmt]}\t{median(vals[fmt]):.4f}")


if __name__ == "__main__":
    sys.exit(main())
