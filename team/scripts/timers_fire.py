#!/usr/bin/env python3
"""Move due agent follow-ups from TIMERS.md to their owner's inbox."""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


TIMERS_FILE = Path(os.environ.get("TIMERS_FILE", "team/state/TIMERS.md"))
INBOX_DIR = Path(os.environ.get("INBOX_DIR", "team/inbox"))
ROW = re.compile(
    r"^(?P<prefix>\|\s*)(?P<due>\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*\|"
    r"\s*(?P<owner>[^|]+?)\s*\|\s*(?P<what>[^|]+?)\s*\|"
    r"\s*(?P<source>[^|]+?)\s*\|\s*(?P<status>pending|fired)\s*\|\s*$"
)
OWNER_ALIASES = {"参謀": "sanbou"}


def owner_inbox(owner: str) -> Path:
    clean = owner.strip().lstrip("@").strip()
    slug = OWNER_ALIASES.get(clean, clean)
    if not re.fullmatch(r"[\w.-]+", slug, re.UNICODE) or ".." in slug:
        raise ValueError(f"unsafe timer owner: {owner!r}")
    return INBOX_DIR / f"{slug}.md"


def fire(now: datetime | None = None) -> int:
    now = now or datetime.now(ZoneInfo("Asia/Tokyo"))
    lines = TIMERS_FILE.read_text(encoding="utf-8").splitlines(keepends=True)
    fired: list[tuple[Path, str]] = []
    output: list[str] = []

    for line in lines:
        match = ROW.match(line.rstrip("\n"))
        if not match or match["status"] != "pending":
            output.append(line)
            continue
        due = datetime.strptime(match["due"], "%Y-%m-%d %H:%M").replace(
            tzinfo=ZoneInfo("Asia/Tokyo")
        )
        if due > now:
            output.append(line)
            continue

        inbox = owner_inbox(match["owner"])
        message = (
            f"\n- {now:%Y-%m-%d %H:%M} JST TIMER FIRED (due {match['due']} JST)"
            f" from `{match['source']}`: {match['what']}\n"
        )
        fired.append((inbox, message))
        output.append(line.replace("| pending |", "| fired |"))

    if not fired:
        return 0

    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    for inbox, message in fired:
        with inbox.open("a", encoding="utf-8") as handle:
            handle.write(message)
    TIMERS_FILE.write_text("".join(output), encoding="utf-8")
    return len(fired)


if __name__ == "__main__":
    count = fire()
    print(f"fired={count}")
