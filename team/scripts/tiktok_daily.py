#!/usr/bin/env python3
"""TikTok daily loop (owner: opencode). Runs with no Muse, no human.

For each focus account in team/distribution/shortform/tiktok-queue.json:
  - skip if an item for that account is already used today (JST)
  - take the first unused item, render its media if the item is a card carousel
  - post it through team/scripts/tiktok_post.py (which runs the hard post-gate twice)
  - mark the item used_on=<today>, append a POSTED line to team/ACTIVITY.md
  - optionally commit + push (--push) so the claim/ACTIVITY is visible to the team

Before each publish a POST-CLAIM must exist in team/CLAIMS.md on main for that account
(team/scripts/post-gate.py refuses otherwise). The loop writes the claim itself when --claim
is given and pushes it first; run it that way in a scheduled job.

Examples:
  python3 team/scripts/tiktok_daily.py --dry-run
  python3 team/scripts/tiktok_daily.py --claim --push
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUEUE = os.path.join(ROOT, "team", "distribution", "shortform", "tiktok-queue.json")
CLAIMS = os.path.join(ROOT, "team", "CLAIMS.md")
ACTIVITY = os.path.join(ROOT, "team", "ACTIVITY.md")
POST = os.path.join(ROOT, "team", "scripts", "tiktok_post.py")
CARDS = os.path.join(ROOT, "team", "scripts", "tiktok_buddha_cards.py")
JST = dt.timezone(dt.timedelta(hours=9))


def now() -> dt.datetime:
    return dt.datetime.now(JST)


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kw)


def push(msg: str) -> bool:
    if sh(["git", "add", "-A"]).returncode != 0:
        return False
    sh(["git", "commit", "-q", "-m", msg + "\n\nAgent: opencode"])
    sh(["git", "fetch", "-q", "origin", "main"])
    if sh(["git", "rebase", "-q", "--autostash", "origin/main"]).returncode != 0:
        sh(["git", "rebase", "--abort"])
        return False
    return sh(["git", "push", "-q", "origin", "HEAD:main"]).returncode == 0


def main() -> int:
    a = argparse.ArgumentParser()
    a.add_argument("--dry-run", action="store_true")
    a.add_argument("--claim", action="store_true", help="write POST-CLAIM rows and push before posting")
    a.add_argument("--push", action="store_true", help="commit + push queue/ACTIVITY after posting")
    a.add_argument("--account", default="", help="only this account")
    args = a.parse_args()

    today = now().strftime("%Y-%m-%d")
    stamp = now().strftime("%Y-%m-%d %H:%M JST")
    q = json.load(open(QUEUE, encoding="utf-8"))
    accounts = [args.account] if args.account else q["focus_accounts"]

    todo = []
    for acct in accounts:
        items = [i for i in q["items"] if i["account"] == acct]
        if any(i.get("used_on") == today for i in items):
            print(f"SKIP {acct}: already posted today")
            continue
        fresh = [i for i in items if not i.get("used_on")]
        if not fresh:
            print(f"SKIP {acct}: queue empty — add an item to {QUEUE}")
            continue
        todo.append(fresh[0])

    if not todo:
        print("NOTHING_TO_DO")
        return 0
    for item in todo:
        print(f"QUEUED {item['id']} -> {item['account']}")

    if args.claim:  # also allowed with --dry-run, so the claim path can be tested without publishing
        with open(CLAIMS, "a", encoding="utf-8") as fh:
            for item in todo:
                fh.write(f"- POST-CLAIM | {stamp} | opencode | tiktok:{item['account']} | create | {item['source_url']}\n")
        if not push(f"opencode: POST-CLAIM tiktok daily loop {today}"):
            print("BLOCKED: could not push POST-CLAIM")
            return 2

    rc = 0
    for item in todo:
        media = item.get("media", [])
        if item.get("cards_from"):
            out_dir = os.path.join(ROOT, "assets", "tiktok", "buddha-cards", item["id"])
            built = sh([sys.executable, CARDS, "--lines-file", os.path.join(ROOT, item["cards_from"]),
                        "--out-dir", out_dir])
            if built.returncode != 0:
                print(f"BLOCKED {item['id']}: card render failed: {built.stderr[:300]}")
                rc = 2
                continue
            media = json.loads(built.stdout)["cards"]
        cap = os.path.join(ROOT, "work-tmp", f"tt-cap-{item['id']}.txt")
        os.makedirs(os.path.dirname(cap), exist_ok=True)
        open(cap, "w", encoding="utf-8").write(item["caption"].strip() + "\n")
        cmd = [sys.executable, POST, "--account", item["account"], "--caption-file", cap,
               "--source-url", item["source_url"], "--title", item.get("title", ""),
               "--media", *media]
        if item.get("photo"):
            cmd.append("--photo")
        if item.get("cover_ms"):
            cmd += ["--cover-ms", str(item["cover_ms"])]
        if args.dry_run:
            cmd.append("--dry-run")
        print("RUN", item["id"])
        res = sh(cmd)
        sys.stdout.write(res.stdout)
        sys.stderr.write(res.stderr)
        if res.returncode != 0:
            print(f"FAILED {item['id']} rc={res.returncode}")
            rc = 2
            continue
        postiz_id = ""
        for line in res.stdout.splitlines():
            if line.startswith("POSTED_OR_SCHEDULED "):
                try:
                    postiz_id = json.loads(line.split(" ", 1)[1]).get("id") or ""
                except Exception:
                    pass
        if args.dry_run:
            continue
        item["used_on"] = today
        with open(ACTIVITY, "a", encoding="utf-8") as fh:
            fh.write(f"- {stamp} | @opencode | POSTED | tiktok:{item['account']} — {item['title'] or item['id']}"
                     f"（Postiz `{postiz_id}`）。勝者原典 {item['source_url']} 。loop: team/scripts/tiktok_daily.py"
                     f" | {item['source_url']}\n")
        with open(QUEUE, "w", encoding="utf-8") as fh:
            json.dump(q, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print(f"POSTED {item['account']} postiz={postiz_id}")

    if args.push and not args.dry_run and rc == 0:
        push(f"opencode: TikTok daily loop {today} (queue + ACTIVITY)")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
