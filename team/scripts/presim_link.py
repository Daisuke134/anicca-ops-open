#!/usr/bin/env python3
"""presim_link POSTS_JSON [--csv PATH] [--write]: link presim-log rows to real X post ids.

POSTS_JSON = X API v2 get_users_posts response ({"data": [{"id", "text", ...}]}).
A row is unlinked when post_id is empty or not all digits (queue-*/bip-* placeholders).
Match: the post text (whitespace-normalized) starts with the row's text_preview's first 40
normalized chars. Prints `sha -> id` per match; --write fills post_id in place.
"""
import argparse
import csv
import json
import re
import sys

DEFAULT = "team/metrics/presim-log.csv"


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def link(rows, posts):
    used = {r.get("post_id") for r in rows}
    matches = []
    for r in rows:
        if (r.get("post_id") or "").isdigit():
            continue
        key = norm(r.get("text_preview"))[:40]
        if not key:
            continue
        for p in posts:
            if p["id"] not in used and norm(p.get("text")).startswith(key):
                matches.append((r.get("text_sha", ""), p["id"]))
                r["post_id"] = p["id"]
                used.add(p["id"])
                break
    return matches


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("posts_json")
    ap.add_argument("--csv", default=DEFAULT)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    data = json.load(open(a.posts_json, encoding="utf-8"))
    posts = data.get("data", []) if isinstance(data, dict) else data
    with open(a.csv, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    matches = link(rows, posts)
    for sha, pid in matches:
        print(f"{sha} -> {pid}")
    if a.write and matches:
        with open(a.csv, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
