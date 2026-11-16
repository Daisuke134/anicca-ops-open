"""Tests for presim_unlinked.py."""

import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import presim_unlinked  # noqa: E402

NOW = datetime(2026, 11, 15, 12, 0)

HEADER = ["ts_jst", "post_id", "text_sha", "note"]


def write_csv(tmp_path, rows):
    path = tmp_path / "presim-log.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(rows)
    return path


def row(ts, post_id, sha):
    return [ts, post_id, sha, "x"]


def test_digit_post_id_not_listed():
    rows = [{"ts_jst": "2026-11-15 08:00", "post_id": "12345",
             "text_sha": "aaa"}]
    assert presim_unlinked.unlinked(rows, NOW) == []


def test_empty_post_id_2h_old_listed():
    rows = [{"ts_jst": "2026-11-15 09:30", "post_id": "",
             "text_sha": "bbb"}]
    out = presim_unlinked.unlinked(rows, NOW)
    assert out == rows


def test_non_digit_post_id_2h_old_listed():
    rows = [{"ts_jst": "2026-11-15 09:30", "post_id": "bip-x",
             "text_sha": "ccc"}]
    out = presim_unlinked.unlinked(rows, NOW)
    assert out == rows


def test_empty_post_id_10min_old_not_listed():
    rows = [{"ts_jst": "2026-11-15 11:50", "post_id": "",
             "text_sha": "ddd"}]
    assert presim_unlinked.unlinked(rows, NOW) == []


def test_cli_lists_unlinked_and_exits_1(tmp_path):
    csv_path = write_csv(tmp_path, [
        row("2026-11-15 09:30", "", "sha-empty"),
        row("2026-11-15 09:30", "bip-x", "sha-bip"),
        row("2026-11-15 09:30", "999", "sha-linked"),
        row("2026-11-15 11:55", "", "sha-fresh"),
    ])
    script = Path(presim_unlinked.__file__)
    proc = subprocess.run(
        [sys.executable, str(script), str(csv_path),
         "--now", "2026-11-15 12:00"],
        capture_output=True, text=True)
    assert proc.returncode == 1
    lines = proc.stdout.strip().splitlines()
    assert lines[0] == "UNLINKED 2"
    assert set(lines[1:]) == {"sha-empty 2026-11-15 09:30",
                              "sha-bip 2026-11-15 09:30"}


def test_cli_clean_csv_exits_0(tmp_path):
    csv_path = write_csv(tmp_path, [
        row("2026-11-15 09:30", "12345", "sha-linked"),
        row("2026-11-15 11:55", "", "sha-fresh"),
    ])
    script = Path(presim_unlinked.__file__)
    proc = subprocess.run(
        [sys.executable, str(script), str(csv_path),
         "--now", "2026-11-15 12:00"],
        capture_output=True, text=True)
    assert proc.returncode == 0
    assert proc.stdout.strip() == "UNLINKED 0"


def test_main_returns_exit_code(tmp_path, capsys, monkeypatch):
    csv_path = write_csv(tmp_path, [row("2026-11-15 09:30", "", "s1")])
    monkeypatch.setattr(sys, "argv", [
        "presim_unlinked.py", str(csv_path), "--now", "2026-11-15 12:00"])
    assert presim_unlinked.main() == 1
    out = capsys.readouterr().out
    assert out.splitlines()[0] == "UNLINKED 1"


def test_failclosed_missing_csv(tmp_path):
    import subprocess, sys as _s, pathlib
    exe = pathlib.Path(__file__).resolve().parent / "presim_unlinked.py"
    p = subprocess.run([_s.executable, str(exe), str(tmp_path / "nope.csv"), "--now", "2026-11-15 21:30"], capture_output=True, text=True)
    assert p.returncode == 2 and "BLOCKED" in p.stdout


def run_cli(csv_path):
    script = Path(presim_unlinked.__file__)
    return subprocess.run(
        [sys.executable, str(script), str(csv_path),
         "--now", "2026-11-15 12:00"],
        capture_output=True, text=True)


def test_failclosed_empty_csv(tmp_path):
    csv_path = tmp_path / "presim-log.csv"
    csv_path.write_text("", encoding="utf-8")
    proc = run_cli(csv_path)
    assert proc.returncode == 2
    assert proc.stdout.startswith("BLOCKED")


def test_failclosed_header_only_csv(tmp_path):
    csv_path = tmp_path / "presim-log.csv"
    csv_path.write_text(",".join(HEADER) + "\n", encoding="utf-8")
    proc = run_cli(csv_path)
    assert proc.returncode == 2
    assert proc.stdout.startswith("BLOCKED")


def test_failclosed_missing_ts_jst_header(tmp_path):
    csv_path = tmp_path / "presim-log.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["post_id", "text_sha", "note"])
        w.writerow(["12345", "sha", "x"])
    proc = run_cli(csv_path)
    assert proc.returncode == 2
    assert proc.stdout.startswith("BLOCKED")


def test_failclosed_missing_post_id_header(tmp_path):
    csv_path = tmp_path / "presim-log.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ts_jst", "text_sha", "note"])
        w.writerow(["2026-11-15 09:30", "sha", "x"])
    proc = run_cli(csv_path)
    assert proc.returncode == 2
    assert proc.stdout.startswith("BLOCKED")


def test_failclosed_bad_ts_jst_on_digit_post_id(tmp_path):
    csv_path = write_csv(tmp_path, [
        row("not-a-timestamp", "12345", "sha-linked"),
    ])
    proc = run_cli(csv_path)
    assert proc.returncode == 2
    assert proc.stdout.startswith("BLOCKED")
