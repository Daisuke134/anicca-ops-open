"""Print reply-back-rate CSV rows for X API v2 conversation dumps."""

import argparse
import csv
import json
import sys
from pathlib import Path

import reply_back_rate


FIELDNAMES = ["root_id", "n", "rate_2h", "rate_24h", "median_min"]


def iter_report_rows(directory, our_author_id):
    directory = Path(directory)
    for path in sorted(directory.glob("*.json"), key=lambda item: item.name):
        if not path.is_file():
            continue
        with path.open("r", encoding="utf-8") as fh:
            posts = json.load(fh)
        root_id = path.stem
        res_2h = reply_back_rate.reply_back_rate(posts, root_id, our_author_id, 2.0)
        res_24h = reply_back_rate.reply_back_rate(posts, root_id, our_author_id, 24.0)
        yield {
            "root_id": root_id,
            "n": res_2h.get("replies"),
            "rate_2h": res_2h.get("rate"),
            "rate_24h": res_24h.get("rate"),
            "median_min": res_24h.get("median_minutes_to_answer"),
        }


def _csv_value(value):
    return "" if value is None else value


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Report reply-back rates for a directory of X API v2 conversation JSON files."
    )
    parser.add_argument("directory", help="Directory containing <root_id>.json files")
    parser.add_argument("our_author_id", help="Author ID for our account")
    args = parser.parse_args(argv)

    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(FIELDNAMES)
    for row in iter_report_rows(args.directory, args.our_author_id):
        writer.writerow([_csv_value(row[field]) for field in FIELDNAMES])
    return 0


if __name__ == "__main__":
    sys.exit(main())
