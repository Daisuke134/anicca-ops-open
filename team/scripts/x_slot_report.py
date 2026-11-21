"""Report on X slot rows: median impressions per format."""

import argparse
import csv
import statistics
import sys
from collections import defaultdict

VALID_FORMATS = ("connect", "question", "other")


def format_medians(rows):
    """Return {format: median impressions} for rows.

    Each row may be a dict with 'format' and 'impressions' keys, or a
    sequence/CSV-row where the first field is the format and the second
    is impressions. Formats not in {connect, question, other}, or blank,
    are grouped as 'other'. Empty input returns {}.
    """
    grouped = defaultdict(list)
    for row in rows:
        if isinstance(row, dict):
            fmt = row.get("format")
            imp = row.get("impressions")
        else:
            fmt = row[0] if len(row) > 0 else None
            imp = row[1] if len(row) > 1 else None
        fmt = str(fmt).strip().lower() if fmt is not None else ""
        if fmt not in VALID_FORMATS:
            fmt = "other"
        if imp is None or imp == "":
            continue
        grouped[fmt].append(float(imp))
    return {
        fmt: statistics.median(vals)
        for fmt, vals in grouped.items()
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", help="CSV of slot rows")
    parser.add_argument(
        "--by-format",
        action="store_true",
        help="print 'format TAB n TAB median' per format, sorted by median desc",
    )
    args = parser.parse_args(argv)

    with open(args.csv_file, newline="") as f:
        rows = list(csv.reader(f))

    medians = format_medians(rows)
    counts = defaultdict(int)
    for row in rows:
        fmt = row[0] if row else ""
        fmt = str(fmt).strip().lower()
        if fmt not in VALID_FORMATS:
            fmt = "other"
        counts[fmt] += 1

    for fmt in sorted(medians, key=lambda f: (-medians[f], f)):
        print(f"{fmt}\t{counts[fmt]}\t{medians[fmt]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
