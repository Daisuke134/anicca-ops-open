#!/usr/bin/env python3
"""presim_close POSTS_JSON --now ISO8601 [--csv PATH] [--write]: close presim-log rows.

POSTS_JSON = X API v2 get_users_posts response
({"data": [{"id", "created_at", "public_metrics": {...}}]}).
A row is closable when post_id is all digits, actual_impr is empty, and the
matching post's created_at is >= 24h before --now. Fills actual_impr/actual_likes/
actual_replies and the abs_log_err_* columns. Prints `post_id pred actual err`
per closed row; --write rewrites the CSV in place (lineterminator "\n").
"""
import argparse
import csv
import json
import math
import sys
from datetime import datetime, timedelta, timezone

DEFAULT = "team/metrics/presim-log.csv"
AGE = timedelta(hours=24)


def parse_ts(s):
    dt = datetime.fromisoformat((s or "").replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def log_err(pred, actual):
    try:
        p, a = float(pred), float(actual)
    except (TypeError, ValueError):
        return ""
    if p == 0 or a == 0:
        return ""
    return str(round(abs(math.log(a / p)), 3))


def log_err_smoothed(pred, actual):
    try:
        p, a = float(pred), float(actual)
    except (TypeError, ValueError):
        return ""
    return str(round(abs(math.log((a + 1) / (p + 1))), 3))


def close(rows, posts, now):
    by_id = {}
    for p in posts:
        try:
            by_id[str(p["id"])] = p
        except (KeyError, TypeError):
            continue
    closed = []
    for r in rows:
        pid = r.get("post_id") or ""
        if not pid.isdigit() or (r.get("actual_impr") or "") != "":
            continue
        p = by_id.get(pid)
        if p is None:
            continue
        try:
            created = parse_ts(p.get("created_at"))
        except ValueError:
            continue
        if now - created < AGE:
            continue
        m = p.get("public_metrics") or {}
        impr = m.get("impression_count", 0)
        likes = m.get("like_count", 0)
        replies = m.get("reply_count", 0)
        r["actual_impr"] = str(impr)
        r["actual_likes"] = str(likes)
        r["actual_replies"] = str(replies)
        err_impr = log_err(r.get("pred_impr"), r["actual_impr"])
        err_likes = log_err_smoothed(r.get("pred_likes"), r["actual_likes"])
        r["abs_log_err_impr"] = err_impr
        r["abs_log_err_likes"] = err_likes
        closed.append((pid, r.get("pred_impr") or "", r["actual_impr"], err_impr))
    return closed


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("posts_json")
    ap.add_argument("--now", required=True)
    ap.add_argument("--csv", default=DEFAULT)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    data = json.load(open(a.posts_json, encoding="utf-8"))
    posts = data.get("data", []) if isinstance(data, dict) else data
    now = parse_ts(a.now)
    with open(a.csv, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    closed = close(rows, posts, now)
    for pid, pred, actual, err in closed:
        print(f"{pid} {pred} {actual} {err}")
    if a.write and closed:
        with open(a.csv, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
