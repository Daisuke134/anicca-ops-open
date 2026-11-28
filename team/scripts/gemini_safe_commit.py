#!/usr/bin/env python3
"""Helpers for team/scripts/gemini-worker.sh: pick inbox task, write a
constrained prompt, and refuse/restore any Gemini edit outside the
task deliverable path."""

from __future__ import annotations

import argparse
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

TASK_ID_RE = re.compile(r"\b(T[0-9]{4}U(?:-[A-Z0-9]+)+|[A-Z]{2,}-[A-Z0-9][A-Z0-9_-]{2,})\b")
CHECKBOX_RE = re.compile(r"^(\s*[-*]\s+)\[\s*\]\s+(.*)$")
ALLOWED_SUFFIXES_AFTER_GUARD = {
    "team/ACTIVITY.md",
    "team/inbox/gemini.md",
    "team/state/gemini-worker-log.md",
}


def jst_now() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M JST")


def run(repo: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def changed_paths(repo: Path) -> list[str]:
    proc = run(repo, ["git", "status", "--porcelain", "-u"])
    paths = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        # porcelain: XY PATH or XY ORIG -> PATH
        rest = line[3:] if len(line) > 3 else line
        if " -> " in rest:
            rest = rest.split(" -> ", 1)[1]
        rest = rest.strip().strip('"')
        paths.append(rest)
    return paths


def restore_except(repo: Path, keep: Iterable[str]) -> list[str]:
    keep_set = set(keep)
    restored = []
    for path in changed_paths(repo):
        if path in keep_set:
            continue
        # Restore tracked files; remove untracked ones (except keep).
        tracked = run(repo, ["git", "ls-files", "--", path], check=False)
        if tracked.stdout.strip():
            run(repo, ["git", "checkout", "-q", "HEAD", "--", path], check=False)
        else:
            full = repo / path
            if full.is_file():
                full.unlink()
            elif full.is_dir():
                # do not recursively delete unexpected dirs blindly if they
                # contain the keep path; only drop empty leftover files.
                pass
        restored.append(path)
    return restored


def extract_task_id(text: str, fallback: str = "GEMINI-TASK") -> str:
    m = TASK_ID_RE.search(text)
    if m:
        return m.group(1)
    # filename fallback
    stem = Path(text).stem if "\n" not in text and len(text) < 400 else ""
    if stem:
        m = TASK_ID_RE.search(stem)
        if m:
            return m.group(1)
        safe = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-")
        return safe or fallback
    return fallback


def iter_open_tasks(inbox: Path) -> list[tuple[str, str]]:
    """Return [(task_id, full_item_text), ...] for unchecked boxes."""
    lines = inbox.read_text(encoding="utf-8", errors="replace").splitlines()
    items: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        m = CHECKBOX_RE.match(lines[i])
        if not m:
            i += 1
            continue
        body = m.group(2)
        block = [lines[i]]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if CHECKBOX_RE.match(nxt) or nxt.startswith("## "):
                break
            if nxt.startswith("- [") or nxt.startswith("- 20"):
                break
            # keep following indented / continuation lines of this item
            if nxt.startswith("  ") or (nxt.strip() and not nxt.startswith("#") and not nxt.startswith("- ")):
                block.append(nxt)
                i += 1
                continue
            break
        tid = extract_task_id("\n".join(block) + "\n" + body)
        items.append((tid, "\n".join(block)))
    return items


FAIL_LOG = Path(os.environ.get("GEMINI_WORKER_LOG", "/workspace/logs/gemini-worker.log"))
FAIL_RE = re.compile(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) JST\] FAIL (\S+)")


def recently_failed_ids(
    log_path: Path | None = None, hours: float = 3.0, min_fails: int = 2
) -> set[str]:
    """Skip tasks that already failed repeatedly in the current window.

    Stops the cron worker from re-picking a quota-exhausted task every 5
    minutes (guard rc=11) and burning the rest of the free-tier budget.
    """
    path = log_path or FAIL_LOG
    if not path.is_file():
        return set()
    cutoff = datetime.datetime.now() - datetime.timedelta(hours=hours)
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = FAIL_RE.search(line)
        if not m:
            continue
        try:
            ts = datetime.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M")
        except ValueError:
            continue
        if ts >= cutoff:
            tid = m.group(2)
            counts[tid] = counts.get(tid, 0) + 1
    return {tid for tid, n in counts.items() if n >= min_fails}


def pick_next(items: list[tuple[str, str]]) -> tuple[str, str] | None:
    """Prefer today's writing queue (T1128-*, then T4329U-*), skip stale
    code-edit tasks that tell Gemini to patch other repos, and skip tasks
    that have already failed repeatedly in the last few hours."""
    if not items:
        return None
    skip = recently_failed_ids()
    if skip:
        items = [(i, t) for i, t in items if i not in skip]
        if not items:
            return None

    def is_stale_code_edit(text: str) -> bool:
        lowered = text.lower()
        return (
            "daisuke134/anicca" in lowered
            and ("fix the ballot" in lowered or "open a pr" in lowered or "comedy/" in lowered)
        )

    writing = [(i, t) for i, t in items if not is_stale_code_edit(t)]
    pool = writing or items

    def pref(prefix: str):
        for i, t in pool:
            if i.startswith(prefix):
                return (i, t)
        return None

    # Revenue / distribution first (t4336u), then the rest of today's queue.
    for prefix in (
        "T1128U-",
        "T1127U-",
        "T4329U-GM-ASO-COPY",
        "T4329U-GM-JA6",
        "T4329U-GM-EN6",
        "T4329U-GM-SELA",
        "T4329U-GM-COMMUNITY",
        "T4326U-XO-POST-DRAFTS",
        "T4325U-ARTICLE-DRAFT",
        "HOOKSCORE-REV-2",
        "GM-SEO1",
        "T4330U-GM-OGIRI",
        "T4329U-",
        "T4326U-",
        "T4325U-",
        "T4284U-",
        "GM-",
        "RESEARCH-",
    ):
        hit = pref(prefix)
        if hit:
            return hit
    return pool[0]


def cmd_pick(args: argparse.Namespace) -> int:
    inbox = Path(args.inbox)
    if not inbox.is_file():
        return 0
    items = iter_open_tasks(inbox)
    hit = pick_next(items)
    if not hit:
        return 0
    print(hit[0])
    return 0


def cmd_task_id_from_file(args: argparse.Namespace) -> int:
    path = Path(args.task)
    text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else path.name
    print(extract_task_id(text + "\n" + path.name))
    return 0


def build_prompt(repo: Path, task_id: str, item_text: str) -> str:
    return f"""You are the Anicca Gemini worker. Complete ONE writing/research task.

STRICT FILE RULES (non-negotiable):
- Create or overwrite ONLY this file: team/gemini/out/{task_id}.md
- Do not read or write credentials, .secrets, keys, or tokens.
- Do not modify team/ACTIVITY.md, team/inbox/gemini.md, marketing/X-QUEUE*.md,
  marketing/X-DRAFTS*.md, or any other file. The wrapper will log ACTIVITY
  and mark the inbox checkbox after you finish.
- If you need facts, read only existing non-secret repo files
  (team/PROOF-NUMBERS.md, team/opportunities/PROFILE.md, team/CAPACITY.md).
- Never invent installs, revenue, reviews, testimonials, or acceptances.
  If a number is not in those files, write "unverified" instead.
- RULE NO-FAKE-OFFER. Do not claim YC acceptance or travel.

TASK ID: {task_id}

TASK:
{item_text}

Write a complete, useful deliverable in Markdown to team/gemini/out/{task_id}.md
and then stop. Do not run git commit or git push.
"""


def cmd_prompt(args: argparse.Namespace) -> int:
    repo = Path(args.repo)
    inbox = repo / "team/inbox/gemini.md"
    items = iter_open_tasks(inbox)
    item_text = ""
    for tid, text in items:
        if tid == args.task_id:
            item_text = text
            break
    if not item_text:
        item_text = f"(checkbox text not found; still write team/gemini/out/{args.task_id}.md for {args.task_id})"
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(repo, args.task_id, item_text)
    # refuse if the generated prompt looks like it contains a secret
    if re.search(
        r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{30,}|AGE-SECRET-KEY-|password\s*[:=])",
        prompt,
    ):
        print("gemini_safe_commit: generated prompt looks like it contains a secret", file=sys.stderr)
        return 4
    out.write_text(prompt, encoding="utf-8")
    print(str(out))
    return 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    repo = Path(args.repo)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    proc = run(repo, ["git", "status", "--porcelain", "-u"])
    out.write_text(proc.stdout, encoding="utf-8")
    return 0


def is_append_only_diff(repo: Path, path: str) -> bool:
    proc = run(repo, ["git", "diff", "-U0", "--", path], check=False)
    text = proc.stdout
    if not text.strip():
        # maybe untracked? treat new file as ok if path is allowed
        return True
    # Any removed line (other than diff headers) is a rewrite.
    for line in text.splitlines():
        if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
            continue
        if line.startswith("-") and not line.startswith("---"):
            return False
    return True


def mark_inbox_done(inbox: Path, task_id: str, deliverable: str) -> bool:
    text = inbox.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines(keepends=True)
    changed = False
    out = []
    for line in lines:
        if (not changed) and CHECKBOX_RE.match(line.rstrip("\n")) and task_id in line:
            line = line.replace("[ ]", "[x]", 1)
            if deliverable not in line:
                # append proof on the same line if it is not huge
                stripped = line.rstrip("\n")
                nl = "\n" if line.endswith("\n") else ""
                line = f"{stripped} | DONE {deliverable}{nl}"
            changed = True
        out.append(line)
    if not changed:
        return False
    inbox.write_text("".join(out), encoding="utf-8")
    return True


def cmd_guard(args: argparse.Namespace) -> int:
    repo = Path(args.repo)
    task_id = args.task_id
    deliverable = f"team/gemini/out/{task_id}.md"
    keep = {deliverable}

    restored = restore_except(repo, keep)
    dest = repo / deliverable
    if not dest.is_file() or dest.stat().st_size < 80:
        print(
            f"gemini_safe_commit: no usable deliverable at {deliverable} "
            f"(restored {len(restored)} unexpected paths)",
            file=sys.stderr,
        )
        # Restore deliverable too if we are aborting and it is junk? keep it
        # for debugging under the out/ path only if it exists; if empty, drop.
        if dest.is_file() and dest.stat().st_size < 80:
            # leave tiny file uncommitted; do not write ACTIVITY
            pass
        return 11

    body = dest.read_text(encoding="utf-8", errors="replace")
    if not body.strip():
        print("gemini_safe_commit: deliverable is empty", file=sys.stderr)
        return 11

    # Script (not Gemini) appends exactly one ACTIVITY line.
    activity = repo / "team/ACTIVITY.md"
    line = (
        f"- {jst_now()} | @gemini | DONE | {task_id} "
        f"deliverable {deliverable} (auto-run, no shared-file edits)\n"
    )
    existing = activity.read_text(encoding="utf-8", errors="replace")
    if not existing.endswith("\n"):
        existing += "\n"
    activity.write_text(existing + line, encoding="utf-8")
    if not is_append_only_diff(repo, "team/ACTIVITY.md"):
        run(repo, ["git", "checkout", "-q", "HEAD", "--", "team/ACTIVITY.md"], check=False)
        print("gemini_safe_commit: ACTIVITY.md was not append-only; restored", file=sys.stderr)
        return 12

    inbox = repo / "team/inbox/gemini.md"
    if inbox.is_file():
        if not mark_inbox_done(inbox, task_id, deliverable):
            print(
                f"gemini_safe_commit: could not mark {task_id} done in inbox (left deliverable)",
                file=sys.stderr,
            )
            # still ok to commit deliverable + ACTIVITY
        else:
            # Inbox should be a small edit: no huge deletions.
            proc = run(repo, ["git", "diff", "--numstat", "--", "team/inbox/gemini.md"], check=False)
            # numstat: added deleted path
            for row in proc.stdout.splitlines():
                parts = row.split()
                if len(parts) >= 2 and parts[1].isdigit() and int(parts[1]) > 20:
                    run(repo, ["git", "checkout", "-q", "HEAD", "--", "team/inbox/gemini.md"], check=False)
                    print("gemini_safe_commit: inbox diff too large; restored inbox", file=sys.stderr)
                    return 13

    # Final path allow-list.
    unexpected = [p for p in changed_paths(repo) if p not in keep | ALLOWED_SUFFIXES_AFTER_GUARD]
    if unexpected:
        restore_except(repo, keep | ALLOWED_SUFFIXES_AFTER_GUARD)
        # re-check
        unexpected = [p for p in changed_paths(repo) if p not in keep | ALLOWED_SUFFIXES_AFTER_GUARD]
        if unexpected:
            print(
                "gemini_safe_commit: abort, unexpected paths still dirty: "
                + ", ".join(unexpected),
                file=sys.stderr,
            )
            return 14

    print(f"gemini_safe_commit: ok {deliverable} restored_unexpected={len(restored)}")
    return 0


def cmd_rebase_fix(args: argparse.Namespace) -> int:
    """If rebase stopped on ACTIVITY/inbox/log only, keep upstream and re-apply our appends."""
    repo = Path(args.repo)
    proc = run(repo, ["git", "diff", "--name-only", "--diff-filter=U"], check=False)
    conflicts = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    allowed = {
        "team/ACTIVITY.md",
        "team/inbox/gemini.md",
        "team/state/gemini-worker-log.md",
        args.deliverable,
    }
    if not conflicts:
        cont = run(repo, ["git", "-c", "core.editor=true", "rebase", "--continue"], check=False)
        return 0 if cont.returncode == 0 else 21
    if any(c not in allowed for c in conflicts):
        run(repo, ["git", "rebase", "--abort"], check=False)
        print(
            "gemini_safe_commit: rebase conflicts beyond allowed files: " + ", ".join(conflicts),
            file=sys.stderr,
        )
        return 22
    for path in conflicts:
        run(repo, ["git", "checkout", "-q", "--ours", "--", path], check=False)
        run(repo, ["git", "add", "--", path], check=False)
    activity = repo / "team/ACTIVITY.md"
    marker = f"DONE | {args.task_id} "
    text = activity.read_text(encoding="utf-8", errors="replace") if activity.exists() else ""
    if marker not in text:
        if text and not text.endswith("\n"):
            text += "\n"
        text += (
            f"- {jst_now()} | @gemini | DONE | {args.task_id} "
            f"deliverable {args.deliverable} (auto-run, no shared-file edits)\n"
        )
        activity.write_text(text, encoding="utf-8")
        run(repo, ["git", "add", "--", "team/ACTIVITY.md"], check=False)
    inbox = repo / "team/inbox/gemini.md"
    if inbox.exists():
        mark_inbox_done(inbox, args.task_id, args.deliverable)
        run(repo, ["git", "add", "--", "team/inbox/gemini.md"], check=False)
    cont = run(repo, ["git", "-c", "core.editor=true", "rebase", "--continue"], check=False)
    if cont.returncode != 0:
        run(repo, ["git", "rebase", "--abort"], check=False)
        print("gemini_safe_commit: rebase --continue failed; aborted", file=sys.stderr)
        return 23
    print("gemini_safe_commit: rebase conflicts resolved for allowed files")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="gemini_safe_commit")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("pick")
    p.add_argument("--inbox", required=True)

    p = sub.add_parser("task-id-from-file")
    p.add_argument("--task", required=True)

    p = sub.add_parser("prompt")
    p.add_argument("--repo", required=True)
    p.add_argument("--task-id", required=True)
    p.add_argument("--out", required=True)

    p = sub.add_parser("snapshot")
    p.add_argument("--repo", required=True)
    p.add_argument("--out", required=True)

    p = sub.add_parser("guard")
    p.add_argument("--repo", required=True)
    p.add_argument("--task-id", required=True)
    p.add_argument("--head-before", required=True)
    p.add_argument("--log", required=True)
    p.add_argument("--rc", required=True)
    p.add_argument("--elapsed", required=True)
    p.add_argument("--model", required=True)

    p = sub.add_parser("rebase-fix")
    p.add_argument("--repo", required=True)
    p.add_argument("--task-id", required=True)
    p.add_argument("--deliverable", required=True)

    args = parser.parse_args()
    if args.cmd == "rebase-fix":
        return cmd_rebase_fix(args)
    if args.cmd == "pick":
        return cmd_pick(args)
    if args.cmd == "task-id-from-file":
        return cmd_task_id_from_file(args)
    if args.cmd == "prompt":
        return cmd_prompt(args)
    if args.cmd == "snapshot":
        return cmd_snapshot(args)
    if args.cmd == "guard":
        return cmd_guard(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
