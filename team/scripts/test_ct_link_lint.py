"""Tests for ct_link_lint."""

import subprocess
import sys
from pathlib import Path

import pytest

from ct_link_lint import lint

SCRIPT = Path(__file__).with_name("ct_link_lint.py")


def test_direct_app_store_link_flagged():
    assert lint("Get it at https://apps.apple.com/us/app/anicca/id123") == ["direct-app-store"]


def test_itunes_link_flagged():
    assert lint("See https://itunes.apple.com/app/id123") == ["direct-app-store"]


def test_go_link_without_ct_flagged():
    assert lint("Install https://aniccaai.com/go/anicca") == ["missing-ct"]


def test_go_link_with_bad_ct_flagged():
    assert lint("Install https://aniccaai.com/go/anicca?ct=BAD_CT") == ["bad-ct"]
    assert lint("Install https://aniccaai.com/go/anicca?ct=abc") == ["bad-ct"]


def test_valid_go_link_passes():
    assert lint("Install https://aniccaai.com/go/anicca?ct=x-diceai0-20261121-en-connect") == []


def test_multiple_links_all_checked():
    text = (
        "Apps: https://apps.apple.com/us/app/id1 and "
        "https://aniccaai.com/go/anicca?ct=oklink-2026-en-us"
    )
    assert lint(text) == ["direct-app-store"]


def test_unrelated_url_ignored():
    assert lint("See https://example.com/go/anicca") == []


def test_no_urls():
    assert lint("plain text") == []


def test_cli_exit_codes(tmp_path, monkeypatch):
    good = "https://aniccaai.com/go/anicca?ct=x-diceai0-20261121-en-connect"
    bad = "https://apps.apple.com/us/app/id123"
    monkeypatch.setattr(sys, "argv", ["ct_link_lint.py", good])
    assert subprocess.run([sys.executable, str(SCRIPT), good]).returncode == 0
    assert subprocess.run([sys.executable, str(SCRIPT), bad]).returncode == 1
