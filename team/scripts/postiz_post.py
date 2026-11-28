#!/usr/bin/env python3
"""Post or schedule one Postiz post on youtube / linkedin / tiktok / instagram, behind the post-gate.

Bridge until each channel's free direct path is verified (成田さん t4403u/t4404u 2026-11-28).
Same flow as tiktok_post.py (owner + winner URL + POST-CLAIM + holds, CLI gate and guard_postiz),
but platform-generic. Never prints secrets.

  python3 team/scripts/postiz_post.py --platform youtube --account @anicca-ai \
     --media marketing/anicca/shorts/holiday-2026-11/01-en.mp4 --caption-file c.txt \
     --title "..." --source-url https://... --schedule 2026-11-28T02:15:00.000Z
"""
from __future__ import annotations
import argparse, datetime as dt, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tiktok_post as tp  # reuse key/owners/upload helpers

LEDGER = os.path.join(tp.ROOT, "team", "metrics", "postiz-posts.jsonl")


def settings_for(platform, title, photo):
    if platform == "youtube":
        return {"__type": "youtube", "title": title[:100], "type": "public",
                "selfDeclaredMadeForKids": "no", "tags": []}
    if platform == "linkedin":
        return {"__type": "linkedin", "post_as_images_carousel": False}
    if platform == "instagram":
        return {"__type": "instagram-standalone", "post_type": "post", "collaborators": []}
    return {"__type": "tiktok", "privacy_level": "PUBLIC_TO_EVERYONE", "duet": False, "stitch": False,
            "comment": True, "autoAddMusic": "yes" if photo else "no", "brand_content_toggle": False,
            "brand_organic_toggle": False, "content_posting_method": "DIRECT_POST",
            **({"title": title} if title else {})}


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--platform", required=True, choices=["youtube", "linkedin", "tiktok", "instagram"])
    a.add_argument("--account", required=True)
    a.add_argument("--media", nargs="*", default=[])
    a.add_argument("--caption-file", required=True)
    a.add_argument("--source-url", required=True)
    a.add_argument("--title", default="")
    a.add_argument("--poster", default="grok-sanbo")
    a.add_argument("--schedule", default="")
    a.add_argument("--photo", action="store_true")
    a.add_argument("--dry-run", action="store_true")
    x = a.parse_args()
    acct = x.account if x.account.startswith("@") else "@" + x.account
    caption = open(x.caption_file, encoding="utf-8").read().strip()
    if not caption:
        raise SystemExit("BLOCKED: empty caption")
    owner, iid = tp.resolve(x.platform, acct)
    if owner != x.poster:
        raise SystemExit(f"BLOCKED: {x.platform}:{acct} owned by {owner}")
    action = "schedule" if x.schedule else "create"
    cmd = [sys.executable, tp.GATE, "--poster", x.poster, "--platform", x.platform, "--account", acct,
           "--action", action, "--source-url", x.source_url, "--text-file", x.caption_file]
    env = dict(os.environ, POST_GATE_INTENTS=os.path.join(tp.ROOT, "work-tmp", f"post-gate-intents-precheck-{os.getpid()}.jsonl"))
    if subprocess.run(cmd, cwd=tp.ROOT, env=env).returncode != 0:
        return 2
    if x.dry_run:
        print("DRY-RUN OK", x.platform, acct, iid); return 0
    key = tp.postiz_key()
    medias = []
    for p in x.media:
        up = tp.upload(key, p)
        medias.append({"id": up.get("id"), "path": up.get("path")})
    date = x.schedule or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    payload = {"type": action if x.schedule else "now", "date": date, "shortLink": False, "tags": [],
               "posts": [{"integration": {"id": iid}, "value": [{"content": caption, "image": medias}],
                          "settings": settings_for(x.platform, x.title, x.photo)}]}
    os.environ["ANICCA_POSTER"] = x.poster
    os.environ["ANICCA_SOURCE_URL"] = x.source_url
    import post_gate
    body = json.dumps(payload).encode()
    post_gate.guard_postiz("POST", tp.API + "/posts", body)
    created = tp.req("POST", "/posts", key, body, {"Content-Type": "application/json"})
    rec = {"at": dt.datetime.now(tp.JST).isoformat(), "poster": x.poster, "platform": x.platform,
           "account": acct, "integration": iid, "media": x.media, "schedule": date,
           "source_url": x.source_url, "caption": caption, "postiz": created}
    with open(LEDGER, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print("OK", json.dumps(created, ensure_ascii=False)[:300])
    return 0


if __name__ == "__main__":
    sys.exit(main())
