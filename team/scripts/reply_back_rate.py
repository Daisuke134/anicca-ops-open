"""Compute reply-back rate for a thread."""

import json
import sys
from datetime import datetime, timezone
from statistics import median


def _parse_ts(value):
    if not isinstance(value, str) or not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _post_fields(post):
    """Return (id, author_id, in_reply_to_id, dt) or None if any field unusable."""
    if not isinstance(post, dict):
        return None
    pid = post.get("id")
    author = post.get("author_id")
    parent = post.get("in_reply_to_id")
    dt = _parse_ts(post.get("created_at"))
    if pid is None or author is None or parent is None or dt is None:
        return None
    return pid, author, parent, dt


def _normalize_posts(posts):
    """Accept a raw X API v2 search response ({"data": [...]}) and convert each
    tweet to the existing post format (in_reply_to_id from referenced_tweets)."""
    if isinstance(posts, dict):
        posts = posts.get("data")
    if not isinstance(posts, list):
        return []
    normalized = []
    for post in posts:
        if isinstance(post, dict) and "referenced_tweets" in post:
            post = dict(post)
            parent = None
            for ref in post.get("referenced_tweets") or []:
                if isinstance(ref, dict) and ref.get("type") == "replied_to":
                    parent = ref.get("id")
                    break
            post["in_reply_to_id"] = parent
        normalized.append(post)
    return normalized


def reply_back_rate(posts, root_id, our_author_id, window_hours=2.0):
    replies = []
    our_posts = []
    for post in _normalize_posts(posts):
        fields = _post_fields(post)
        if fields is None:
            continue
        pid, author, parent, dt = fields
        if parent == root_id and author != our_author_id:
            replies.append((pid, dt))
        if author == our_author_id:
            our_posts.append((parent, dt))

    window = float(window_hours) * 3600.0
    answered = []
    for reply_id, reply_dt in replies:
        best = None
        for parent, ans_dt in our_posts:
            if parent != reply_id:
                continue
            delta = (ans_dt - reply_dt).total_seconds()
            if 0 <= delta <= window and (best is None or delta < best):
                best = delta
        if best is not None:
            answered.append(best / 60.0)

    n = len(replies)
    k = len(answered)
    return {
        "replies": n,
        "answered_in_window": k,
        "rate": (k / n) if n else None,
        "median_minutes_to_answer": median(answered) if answered else None,
    }


def summary_json(posts, root_id, our_author_id):
    res_2h = reply_back_rate(posts, root_id, our_author_id, 2.0)
    res_24h = reply_back_rate(posts, root_id, our_author_id, 24.0)
    return {
        "rate_2h": res_2h["rate"],
        "rate_24h": res_24h["rate"],
        "median_min": res_24h["median_minutes_to_answer"],
        "n": res_2h["replies"],
    }


def main(argv):
    json_out = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    if len(argv) < 4:
        print(
            "usage: reply_back_rate.py <json> <root_id> <our_author_id> [hours] [--json]",
            file=sys.stderr,
        )
        return 2
    path = argv[1]
    root_id = argv[2]
    our_author_id = argv[3]
    hours = float(argv[4]) if len(argv) > 4 else 2.0
    with open(path, "r", encoding="utf-8") as fh:
        posts = json.load(fh)
    if json_out:
        print(json.dumps(summary_json(posts, root_id, our_author_id)))
    else:
        print(json.dumps(reply_back_rate(posts, root_id, our_author_id, hours)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
