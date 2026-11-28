#!/usr/bin/env python3
"""Run due items of team/distribution/direct-queue.json on the FREE direct paths (no Postiz).

Box cron: */5 * * * * flock -n /tmp/direct-slot.lock python3 team/scripts/direct/slot_runner.py
One item per run (browser tab hygiene). Writes status/url back to the queue, appends
team/metrics/direct-posts.jsonl and an ACTIVITY POSTED line, then commits+pushes those files.
Platforms: youtube (yt_studio_upload.py). tiktok (tt_api_post.py) only once the TikTok app audit passes.
"""
import datetime as dt, json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
Q = os.path.join(ROOT, "team/distribution/direct-queue.json")
LEDGER = os.path.join(ROOT, "team/metrics/direct-posts.jsonl")
JST = dt.timezone(dt.timedelta(hours=9))
HERE = os.path.dirname(os.path.abspath(__file__))


def sh(cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kw)


def main():
    sh(["git", "pull", "-q", "--rebase", "--autostash", "origin", "main"])
    q = json.load(open(Q))
    now = dt.datetime.now(JST)
    due = [i for i in q["items"] if i.get("status") == "queued"
           and dt.datetime.strptime(i["due_jst"], "%Y-%m-%d %H:%M").replace(tzinfo=JST) <= now]
    if not due:
        return 0
    it = sorted(due, key=lambda i: i["due_jst"])[0]
    late = (now - dt.datetime.strptime(it["due_jst"], "%Y-%m-%d %H:%M").replace(tzinfo=JST)).total_seconds() / 60
    if late > 180:
        it["status"] = "skipped_stale"; it["note"] = f"{int(late)} min late"
    else:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
            fh.write(it.get("caption", "")); cap = fh.name
        if it["platform"] == "youtube":
            r = sh([sys.executable, os.path.join(HERE, "yt_studio_upload.py"), "--file", it["file"],
                    "--title", it["title"], "--desc-file", cap], timeout=900)
            out = (r.stdout + r.stderr).strip().splitlines()
            url = next((l.split()[-1] for l in out if l.startswith("UPLOADED PUBLIC")), None)
        elif it["platform"] == "tiktok":
            r = sh([sys.executable, os.path.join(HERE, "tt_api_post.py"), "--handle", it["account"].lstrip("@"),
                    "--file", it["file"], "--caption-file", cap], timeout=900)
            out = (r.stdout + r.stderr).strip().splitlines()
            try:
                url = json.loads(out[-1]).get("url")
            except Exception:
                url = None
        else:
            out, url = [f"unsupported platform {it['platform']}"], None
        it["status"] = "posted" if url else "failed"
        it["url"] = url; it["posted_at"] = now.strftime("%Y-%m-%d %H:%M JST")
        if not url:
            it["error"] = " | ".join(out[-3:])[:400]
    json.dump(q, open(Q, "w"), ensure_ascii=False, indent=1)
    with open(LEDGER, "a") as fh:
        fh.write(json.dumps({k: it.get(k) for k in ("id", "platform", "account", "status", "url", "posted_at",
                                                    "source_url", "error")}, ensure_ascii=False) + "\n")
    act = os.path.join(ROOT, "team/ACTIVITY.md")
    with open(act, "a") as fh:
        fh.write(f"- {now:%Y-%m-%d %H:%M} JST | 参謀 (direct slot_runner) | {'POSTED' if it.get('url') else it['status'].upper()} | "
                 f"{it['platform']}:{it['account']} FREE direct path (no Postiz) {it.get('url') or it.get('error') or ''} | "
                 f"winner {it.get('source_url')} | team/distribution/direct-queue.json\n")
    sh(["git", "add", Q, LEDGER, act])
    sh(["git", "commit", "-qm", f"direct slot_runner: {it['id']} {it['status']}"])
    for _ in range(3):
        if sh(["git", "push", "-q", "origin", "HEAD:main"]).returncode == 0:
            break
        sh(["git", "pull", "-q", "--rebase", "--autostash", "origin", "main"])
    print(it["id"], it["status"], it.get("url"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
