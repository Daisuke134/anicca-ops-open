"""Audit posts' links with ct_link_lint."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ct_link_lint import lint


def audit(posts):
    n_with_link = 0
    n_ok = 0
    bad = []
    for post in posts:
        urls = post.get("urls") or []
        text = " ".join(urls) + " " + (post.get("text") or "")
        if "http://" not in text and "https://" not in text:
            continue
        n_with_link += 1
        problems = lint(text)
        if problems:
            bad.append({"id": post.get("id"), "problems": problems})
        else:
            n_ok += 1
    return {"n_with_link": n_with_link, "n_ok": n_ok, "bad": bad}


def main(argv):
    path = argv[1]
    with open(path) as f:
        posts = json.load(f)
    result = audit(posts)
    print(json.dumps(result, indent=2))
    return 1 if result["bad"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
