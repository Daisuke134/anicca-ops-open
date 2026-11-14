import os
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).with_name("timers_fire.py")


def run_timer(tmp_path: Path, contents: str):
    timers = tmp_path / "TIMERS.md"
    inbox = tmp_path / "inbox"
    timers.write_text(contents, encoding="utf-8")
    env = {**os.environ, "TIMERS_FILE": str(timers), "INBOX_DIR": str(inbox)}
    result = subprocess.run(
        [sys.executable, str(SCRIPT)], env=env, capture_output=True, text=True
    )
    return result, timers, inbox


def table(*rows: str) -> str:
    return "| due JST | owner | what | source | status |\n|---|---|---|---|---|\n" + "".join(rows)


def test_fires_due_row_and_preserves_future_and_fired_rows(tmp_path):
    result, timers, inbox = run_timer(
        tmp_path,
        table(
            "| 2000-01-01 00:00 | codex | do due work | test source | pending |\n",
            "| 2999-01-01 00:00 | codex | do later work | future | pending |\n",
            "| 2000-01-01 00:00 | muse | already sent | old | fired |\n",
        ),
    )
    assert result.returncode == 0
    assert result.stdout == "fired=1\n"
    assert "do due work" in (inbox / "codex.md").read_text(encoding="utf-8")
    text = timers.read_text(encoding="utf-8")
    assert "do due work | test source | fired" in text
    assert "do later work | future | pending" in text
    assert "already sent | old | fired" in text


def test_no_due_rows_does_not_create_inbox(tmp_path):
    result, timers, inbox = run_timer(
        tmp_path,
        table("| 2999-01-01 00:00 | codex | later | source | pending |\n"),
    )
    assert result.returncode == 0
    assert result.stdout == "fired=0\n"
    assert not inbox.exists()
    assert "pending" in timers.read_text(encoding="utf-8")


def test_sanbou_alias_routes_to_existing_canonical_name(tmp_path):
    result, _, inbox = run_timer(
        tmp_path,
        table("| 2000-01-01 00:00 | 参謀 | check ct | four pillars | pending |\n"),
    )
    assert result.returncode == 0
    assert "check ct" in (inbox / "sanbou.md").read_text(encoding="utf-8")


def test_unsafe_owner_fails_closed(tmp_path):
    result, timers, inbox = run_timer(
        tmp_path,
        table("| 2000-01-01 00:00 | ../escape | nope | source | pending |\n"),
    )
    assert result.returncode != 0
    assert "unsafe timer owner" in result.stderr
    assert "pending" in timers.read_text(encoding="utf-8")
    assert not inbox.exists()
