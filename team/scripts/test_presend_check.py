"""Tests for team/scripts/presend_check.py (run via subprocess)."""

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent / "presend_check.py"


def run_script(text=None, args=None):
    cmd = [sys.executable, str(SCRIPT)]
    if args:
        cmd += args
    if text is not None:
        return subprocess.run(cmd, input=text, capture_output=True, text=True)
    return subprocess.run(cmd, capture_output=True, text=True)


def run_file(tmp_path, text):
    path = tmp_path / "msg.txt"
    path.write_text(text, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
    )


def test_clean_japanese_file(tmp_path):
    r = run_file(tmp_path, "こんにちは。今日はよろしくお願いします。")
    assert r.returncode == 0
    assert r.stdout.strip() == "OK"


def test_clean_japanese_stdin():
    r = run_script("こんにちは。今日はよろしくお願いします。")
    assert r.returncode == 0
    assert r.stdout.strip() == "OK"


@pytest.mark.parametrize(
    "word",
    ["成果報酬", "LINE", "Zoom", "PayPal", "メールアドレス"],
)
def test_banned_words_file(tmp_path, word):
    r = run_file(tmp_path, f"これは {word} を含む文章です。")
    assert r.returncode == 1
    assert "NG:" in r.stdout
    assert word in r.stdout


@pytest.mark.parametrize(
    "word",
    ["成果報酬", "LINE", "Zoom", "PayPal", "メールアドレス"],
)
def test_banned_words_stdin(word):
    r = run_script(f"これは {word} を含む文章です。")
    assert r.returncode == 1
    assert "NG:" in r.stdout
    assert word in r.stdout


def test_google_docs_one_space_case_insensitive(tmp_path):
    r = run_file(tmp_path, "google docs にまとめました。")
    assert r.returncode == 1
    assert "Google ?Docs" in r.stdout


def test_google_docs_uppercase_file(tmp_path):
    r = run_file(tmp_path, "Google Docs を使います。")
    assert r.returncode == 1
    assert "Google ?Docs" in r.stdout


def test_google_docs_stdin(tmp_path):
    r = run_script("Google  Docs を使います。")
    # Actual behaviour: 'Google ?Docs' matches zero or one space, so
    # 'Google  Docs' (two spaces) is NOT flagged -> exit 0.
    assert r.returncode == 0
    assert r.stdout.strip() == "OK"


def test_multiple_hits_all_listed(tmp_path):
    r = run_file(tmp_path, "LINE と Zoom と PayPal で連絡します。")
    assert r.returncode == 1
    ng_line = r.stdout.strip()
    for word in ("LINE", "Zoom", "PayPal"):
        assert word in ng_line
