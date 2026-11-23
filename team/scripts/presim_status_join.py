#!/usr/bin/env python3
"""Join presim log rows to X API v2 post JSON by text prefix.

Usage: presim_status_join.py <presim.csv> <posts.json>
Prints a JSON list of rows with status_id/actual_impr filled when matched.
"""
import csv
import json
import sys

PREVIEW_LEN = 40


def _norm(s):
    return " ".join((s or "").split())


def join(presim_rows, posts):
    texts = [(_norm(p.get("text")), p) for p in posts.get("data", [])]
    out = []
    for row in presim_rows:
        row = dict(row)
        key = _norm(row.get("text_preview"))[:PREVIEW_LEN]
        matches = [p for text, p in texts if key and text.startswith(key)]
        if len(matches) == 1:
            post = matches[0]
            row["status_id"] = post.get("id")
            row["actual_impr"] = (post.get("public_metrics") or {}).get("impression_count")
        out.append(row)
    return out


def main(argv):
    csv_path, json_path = argv[1], argv[2]
    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))
    with open(json_path) as f:
        posts = json.load(f)
    json.dump(join(rows, posts), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main(sys.argv)
