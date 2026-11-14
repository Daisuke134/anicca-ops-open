#!/usr/bin/env python3
"""Tests for changes_since.py: subprocess runs against tmp_path files."""
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "changes_since.py"


def run(agent, changes_file, cursor_dir, *args, extra_env=None):
    env = dict(os.environ)
    env["CHANGES_FILE"] = str(changes_file)
    env["CHANGES_CURSOR_DIR"] = str(cursor_dir)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, str(SCRIPT), agent, *args],
        env=env, capture_output=True, text=True, check=False,
    )


def setup(tmp_path):
    changes_file = tmp_path / "CHANGES.md"
    cursor_dir = tmp_path / "cursor"
    changes_file.write_text(
        "2026-11-14 10:00 JST | devin | did a thing\n"
        "some noise line not matching\n"
        "2026-11-14 11:30 JST | alice | did another thing\n"
        "\n"
        "garbage trailing text\n",
        encoding="utf-8",
    )
    return changes_file, cursor_dir


def test_first_run_prints_matching_lines_only(tmp_path):
    changes_file, cursor_dir = setup(tmp_path)
    r = run("devin", changes_file, cursor_dir)
    assert r.returncode == 0
    assert r.stdout.splitlines() == [
        "2026-11-14 10:00 JST | devin | did a thing",
        "2026-11-14 11:30 JST | alice | did another thing",
    ]


def test_second_run_prints_nothing(tmp_path):
    changes_file, cursor_dir = setup(tmp_path)
    run("devin", changes_file, cursor_dir)
    r = run("devin", changes_file, cursor_dir)
    assert r.returncode == 0
    assert r.stdout == ""


def test_new_appended_line_printed_alone(tmp_path):
    changes_file, cursor_dir = setup(tmp_path)
    run("devin", changes_file, cursor_dir)
    with open(changes_file, "a", encoding="utf-8") as f:
        f.write("2026-11-14 12:00 JST | bob | new line\n")
    r = run("devin", changes_file, cursor_dir)
    assert r.returncode == 0
    assert r.stdout.splitlines() == ["2026-11-14 12:00 JST | bob | new line"]


def test_peek_does_not_advance_cursor(tmp_path):
    changes_file, cursor_dir = setup(tmp_path)
    r = run("devin", changes_file, cursor_dir, "--peek")
    assert r.returncode == 0
    assert len(r.stdout.splitlines()) == 2
    # cursor file must not have been written
    assert not any(cursor_dir.iterdir()) if cursor_dir.exists() else True
    # next non-peek run still sees the same lines
    r2 = run("devin", changes_file, cursor_dir)
    assert r2.stdout.splitlines() == r.stdout.splitlines()


def test_non_word_agent_chars_map_to_safe_filename(tmp_path):
    changes_file, cursor_dir = setup(tmp_path)
    agent = "team/devin+bot.v2@example"
    r = run(agent, changes_file, cursor_dir)
    assert r.returncode == 0
    expected = "team_devin_bot_v2_example"
    assert (cursor_dir / expected).is_file()
    # all names in the cursor dir must be flat filenames (no path traversal)
    for p in cursor_dir.iterdir():
        assert p.is_file() and "/" not in p.name and "\\" not in p.name
    # second run for same agent prints nothing
    r2 = run(agent, changes_file, cursor_dir)
    assert r2.stdout == ""
