#!/usr/bin/env python3
"""Post one TikTok via the hosted Postiz API, behind the hard post-gate.

Owner: opencode (team/ACCOUNT-OWNERS.md, 2026-11-27 t4384u). Muse is no longer the TikTok poster.
Every call must carry a cited winner source URL (成田さん 2026-11-11).

Flow (fails closed):
  1. resolve the integration id from the ```post-gate-owners``` block in team/ACCOUNT-OWNERS.md
     (tiktok | @handle | owner | integration_id) and refuse if the owner is not --poster
  2. run team/scripts/post-gate.py  (owner + winner source + open POST-CLAIM in team/CLAIMS.md + holds)
  3. upload the media to /public/v1/upload
  4. create the post at /public/v1/posts through post_gate.guard_postiz (second gate, same rules)
  5. append a receipt to team/metrics/tiktok-posts.jsonl

Examples:
  python3 team/scripts/tiktok_post.py --account @aniccaaffirmation \
      --media assets/demo-videos/anicca-demo-living-home-2026-11-19.mp4 \
      --caption-file work-tmp/caption.txt \
      --source-url https://www.instagram.com/reel/DKAZBgAIw24/ \
      --title "Affirmations that change on their own, all day"
  # schedule instead of publish now:
  ... --schedule 2026-11-28T03:30:00.000Z
  # verify everything without publishing:
  ... --dry-run

Never prints secrets. Key: credentials.json service=postiz (api_key).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import uuid
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
API = "https://api.postiz.com/public/v1"
OWNERS = os.path.join(ROOT, "team", "ACCOUNT-OWNERS.md")
GATE = os.path.join(HERE, "post-gate.py")
LEDGER = os.path.join(ROOT, "team", "metrics", "tiktok-posts.jsonl")
JST = dt.timezone(dt.timedelta(hours=9))


def postiz_key() -> str:
    with open(os.path.join(ROOT, "credentials.json"), encoding="utf-8") as fh:
        creds = json.load(fh)
    for c in creds.get("credentials", []):
        if c.get("service") == "postiz" and c.get("api_key"):
            return c["api_key"]
    raise SystemExit("BLOCKED: no postiz api_key in credentials.json (service=postiz)")


def owners_block() -> list[list[str]]:
    text = open(OWNERS, encoding="utf-8").read()
    m = re.search(r"```post-gate-owners\n(.*?)```", text, re.S)
    if not m:
        raise SystemExit("BLOCKED: post-gate-owners block not found in team/ACCOUNT-OWNERS.md")
    rows = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        rows.append([c.strip() for c in line.split("|")])
    return rows


def resolve(platform: str, account: str) -> tuple[str, str]:
    """Return (owner, integration_id) for platform:@handle, most specific row wins."""
    best = None
    for row in owners_block():
        if len(row) < 3 or row[0] != platform:
            continue
        if row[1] in ("*", account):
            best = row
    if not best:
        raise SystemExit(f"BLOCKED: {platform}:{account} is not in the post-gate-owners block")
    owner = best[2]
    iid = best[3] if len(best) > 3 else ""
    if not iid:
        raise SystemExit(f"BLOCKED: no integration id for {platform}:{account}")
    return owner, iid


def req(method: str, path: str, key: str, data: bytes | None = None, headers: dict | None = None):
    r = urllib.request.Request(API + path, data=data, method=method,
                               headers={"Authorization": key, **(headers or {})})
    with urllib.request.urlopen(r, timeout=300) as resp:
        return json.loads(resp.read().decode() or "{}")


def upload(key: str, path: str) -> dict:
    ext = os.path.splitext(path)[1] or ".mp4"
    ctype = "video/mp4" if ext == ".mp4" else "image/jpeg"
    bnd = uuid.uuid4().hex
    with open(path, "rb") as fh:
        blob = fh.read()
    body = (f"--{bnd}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"upload{ext}\"\r\n"
            f"Content-Type: {ctype}\r\n\r\n").encode() + blob + f"\r\n--{bnd}--\r\n".encode()
    return req("POST", "/upload", key, body, {"Content-Type": f"multipart/form-data; boundary={bnd}"})


def main() -> int:
    a = argparse.ArgumentParser()
    a.add_argument("--account", required=True, help="@handle of the TikTok account")
    a.add_argument("--media", required=True, nargs="+", help="video (.mp4) or 1+ image paths")
    a.add_argument("--caption-file", required=True)
    a.add_argument("--source-url", required=True, help="cited winner original (https://...)")
    a.add_argument("--title", default="", help="TikTok title field (optional)")
    a.add_argument("--poster", default="opencode")
    a.add_argument("--schedule", default="", help="ISO datetime; omit to publish now")
    a.add_argument("--cover-ms", type=int, default=0, help="cover frame at N ms into the video")
    a.add_argument("--photo", action="store_true", help="photo/carousel post (sets autoAddMusic=yes)")
    a.add_argument("--dry-run", action="store_true")
    args = a.parse_args()

    platform = "tiktok"
    account = args.account if args.account.startswith("@") else "@" + args.account
    caption = open(args.caption_file, encoding="utf-8").read().strip()
    if not caption:
        raise SystemExit("BLOCKED: empty caption")
    if not re.match(r"^https?://", args.source_url or ""):
        raise SystemExit("BLOCKED: --source-url must be the cited winner original URL")

    owner, iid = resolve(platform, account)
    if owner != args.poster:
        raise SystemExit(f"BLOCKED: {platform}:{account} is owned by {owner}, not {args.poster}")

    # gate #1: CLI (reads claims/holds from GitHub main)
    gate_cmd = [sys.executable, GATE, "--poster", args.poster, "--platform", platform,
                "--account", account, "--action", "schedule" if args.schedule else "create",
                "--source-url", args.source_url, "--text-file", args.caption_file]
    print("gate:", " ".join(gate_cmd[-6:]))
    env = dict(os.environ)
    # The CLI gate is a pre-check: it must not burn the (f) 30-minute intent lock, or the real
    # guard_postiz call right after refuses the same text (2026-11-28 参謀: every post refused).
    # The lock is recorded once, by guard_postiz, immediately before the provider call.
    env["POST_GATE_INTENTS"] = os.path.join(ROOT, "work-tmp", f"post-gate-intents-precheck-{os.getpid()}.jsonl")
    if subprocess.run(gate_cmd, cwd=ROOT, env=env).returncode != 0:
        return 2

    settings = {"__type": "tiktok", "privacy_level": "PUBLIC_TO_EVERYONE", "duet": False,
                "stitch": False, "comment": True, "autoAddMusic": "yes" if args.photo else "no",
                "brand_content_toggle": False, "brand_organic_toggle": False,
                "content_posting_method": "DIRECT_POST"}
    if args.title:
        settings["title"] = args.title

    receipt = {"at": dt.datetime.now(JST).isoformat(), "poster": args.poster,
               "account": account, "integration": iid, "media": args.media,
               "source_url": args.source_url, "caption": caption}
    if args.dry_run:
        print(json.dumps({**receipt, "dry_run": True}, ensure_ascii=False, indent=1))
        return 0

    key = postiz_key()
    medias = []
    for path in args.media:
        up = upload(key, path)
        media = {"id": up.get("id"), "path": up.get("path")}
        if path.lower().endswith((".mp4", ".mov")) and args.cover_ms:
            media["thumbnailTimestamp"] = args.cover_ms
        medias.append(media)
    value = {"content": caption, "image": medias}
    # `date` is required by the Postiz schema even for type=now (400 without it)
    date = args.schedule or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    payload = {"type": "schedule" if args.schedule else "now", "date": date,
               "shortLink": False, "tags": [],
               "posts": [{"integration": {"id": iid}, "value": [value], "settings": settings}]}

    # gate #2: library guard, right before the provider call
    os.environ["ANICCA_POSTER"] = args.poster
    os.environ["ANICCA_SOURCE_URL"] = args.source_url
    sys.path.insert(0, HERE)
    import post_gate  # noqa: E402

    body = json.dumps(payload).encode()
    post_gate.guard_postiz("POST", API + "/posts", body)
    created = req("POST", "/posts", key, body, {"Content-Type": "application/json"})

    receipt.update({"uploads": [m["id"] for m in medias], "postiz": created})
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(receipt, ensure_ascii=False) + "\n")
    print("POSTED_OR_SCHEDULED " + json.dumps({"id": (created or [{}])[0].get("postId") if isinstance(created, list) else created,
                                              "integration": iid, "ledger": LEDGER}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
