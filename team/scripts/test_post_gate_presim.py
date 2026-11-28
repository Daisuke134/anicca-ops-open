"""Tests for post_gate presim requirement (T1128-0950-PRESIM-GATE, owner @devin).

Covers presim_logged() and the main() gate: an X create with --text-file and no
--in-reply-to needs a team/metrics/presim-log.csv row (sha1[:10] of the text,
ts_jst within 180 min of --now) unless POST_GATE_PRESIM_SKIP is set.
"""
import datetime as dt
import hashlib
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_gate  # noqa: E402

JST = dt.timezone(dt.timedelta(hours=9))
NOW = dt.datetime(2026, 11, 28, 12, 0, tzinfo=JST)
TEXT = "hello presim world"


def sha(t):
    return hashlib.sha1(t.encode("utf-8")).hexdigest()[:10]


def write_log(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("text_sha,ts_jst,score\n")
        for s, ts in rows:
            f.write(f"{s},{ts},0.9\n")


def presim_args(tmp_path, text=TEXT, extra=()):
    tf = tmp_path / "post.txt"
    tf.write_text(text, encoding="utf-8")
    return ["--poster", "muse", "--platform", "x", "--account", "@anicca",
            "--action", "create", "--source-url", "https://example.com/winner",
            "--text-file", str(tf), "--now", "2026-11-28 12:00", *extra]


@pytest.fixture
def gate_ok(monkeypatch):
    """Stub out the rest of the gate so main() reaches rc 0 once presim passes."""
    monkeypatch.setattr(post_gate, "check", lambda *a, **k: {"allowed": True})


@pytest.fixture
def log_path(tmp_path, monkeypatch):
    p = tmp_path / "presim-log.csv"
    monkeypatch.setattr(post_gate, "PRESIM_LOG", str(p))
    return p


def test_presim_logged_within_window(tmp_path):
    p = tmp_path / "presim-log.csv"
    write_log(p, [(sha(TEXT), "2026-11-28 10:30"), ("deadbeef00", "2026-11-28 11:59")])
    assert post_gate.presim_logged(TEXT, str(p), NOW) is True
    # future row still inside the window also counts
    write_log(p, [(sha(TEXT), "2026-11-28 14:00")])
    assert post_gate.presim_logged(TEXT, str(p), NOW) is True


def test_presim_logged_outside_window(tmp_path):
    p = tmp_path / "presim-log.csv"
    write_log(p, [(sha(TEXT), "2026-11-28 08:59"), (sha(TEXT), "2026-11-28 15:01")])
    assert post_gate.presim_logged(TEXT, str(p), NOW) is False
    # missing log fails closed
    assert post_gate.presim_logged(TEXT, str(tmp_path / "nope.csv"), NOW) is False


def test_presim_logged_different_text(tmp_path):
    p = tmp_path / "presim-log.csv"
    write_log(p, [(sha("a different post"), "2026-11-28 11:59")])
    assert post_gate.presim_logged(TEXT, str(p), NOW) is False


def test_main_passes_when_presim_logged(gate_ok, log_path, tmp_path, capsys):
    write_log(log_path, [(sha(TEXT), "2026-11-28 11:30")])
    rc = post_gate.main(presim_args(tmp_path))
    assert rc == 0
    assert "POST-GATE OK" in capsys.readouterr().out


def test_main_refuses_when_presim_missing(gate_ok, log_path, tmp_path, capsys):
    write_log(log_path, [(sha(TEXT), "2026-11-28 06:00")])  # 6h old, outside 180 min
    rc = post_gate.main(presim_args(tmp_path))
    out = capsys.readouterr().out
    assert rc == 2
    assert "presim missing: run python3 team/scripts/x_presim.py score --file/--text first" in out


def test_main_reply_is_exempt(gate_ok, log_path, tmp_path, capsys):
    # no log file at all, but --in-reply-to makes it a reply -> presim not required
    rc = post_gate.main(presim_args(tmp_path, extra=["--in-reply-to", "1234567890"]))
    assert rc == 0
    assert "presim" not in capsys.readouterr().out


def test_main_skip_env_passes(gate_ok, log_path, tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("POST_GATE_PRESIM_SKIP", "ops override for launch")
    rc = post_gate.main(presim_args(tmp_path))  # no log file
    out = capsys.readouterr().out
    assert rc == 0
    assert "presim skipped: ops override for launch" in out
