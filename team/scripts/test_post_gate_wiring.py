"""Wiring tests: --lang en --kind connect routes post text through check_en_connect_opener."""
import datetime as dt
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_gate


def _write_tiktok_repo(root):
    (root / "team" / "distribution" / "shortform").mkdir(parents=True)
    (root / "team").mkdir(parents=True, exist_ok=True)
    (root / "team" / "ACCOUNT-OWNERS.md").write_text(
        "```post-gate-owners\n"
        "tiktok | @tt | tester |\n"
        "```\n",
        encoding="utf-8",
    )
    (root / "team" / "CLAIMS.md").write_text(
        "- POST-CLAIM | 2026-11-22 12:00 JST | tester | tiktok:@tt | create | https://anicca.ai/winner/1\n",
        encoding="utf-8",
    )
    (root / "team" / "distribution" / "shortform" / "marketing-destinations.json").write_text(
        json.dumps({"targets": [{"platform": "tiktok", "native_handle": "@tt"}], "holds": []}),
        encoding="utf-8",
    )


def _env(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    _write_tiktok_repo(repo)
    monkeypatch.setenv("POST_GATE_LOCAL_ROOT", str(repo))
    monkeypatch.setenv("POST_GATE_INTENTS", str(tmp_path / "intents.jsonl"))


def test_check_en_connect_refuses_number_first(tmp_path, monkeypatch):
    _env(tmp_path, monkeypatch)
    now = dt.datetime(2026, 11, 22, 12, 0, tzinfo=post_gate.JST)
    for text in ("3 wins this week\nI'd love to connect with builders",
                 "$2,400 MRR\nI'd love to connect",
                 "Day 12 of building in public\nI'd love to connect"):
        with pytest.raises(post_gate.Refused, match="lead with the request"):
            post_gate.check("tester", "tiktok", "@tt", "create", "https://anicca.ai/winner/1",
                            now=now, text=text, lang="en", kind="connect")


def test_check_en_connect_passes_request_first(tmp_path, monkeypatch):
    _env(tmp_path, monkeypatch)
    now = dt.datetime(2026, 11, 22, 12, 0, tzinfo=post_gate.JST)
    res = post_gate.check(
        "tester", "tiktok", "@tt", "create", "https://anicca.ai/winner/1",
        now=now, text="\nI'd love to connect with indie hackers\n3 wins this week",
        lang="en", kind="connect")
    assert res["allowed"] is True


def test_check_en_connect_ignored_for_ja(tmp_path, monkeypatch):
    _env(tmp_path, monkeypatch)
    now = dt.datetime(2026, 11, 22, 12, 0, tzinfo=post_gate.JST)
    res = post_gate.check(
        "tester", "tiktok", "@tt", "create", "https://anicca.ai/winner/1",
        now=now, text="3つの学び\nつながりたい方はぜひ", lang="ja", kind="connect")
    assert res["allowed"] is True


def test_main_en_connect_refuses_with_advice(tmp_path, monkeypatch, capsys):
    _env(tmp_path, monkeypatch)
    text_file = tmp_path / "post.txt"
    text_file.write_text("3 wins this week\nI'd love to connect", encoding="utf-8")
    rc = post_gate.main([
        "--poster", "tester",
        "--platform", "tiktok",
        "--account", "@tt",
        "--action", "create",
        "--source-url", "https://anicca.ai/winner/1",
        "--text-file", str(text_file),
        "--lang", "en",
        "--kind", "connect",
    ])
    out = capsys.readouterr().out
    assert rc == 2
    assert "POST-GATE REFUSED" in out
    assert "lead with the request" in out


def test_main_en_connect_allows_request_first(tmp_path, monkeypatch, capsys):
    _env(tmp_path, monkeypatch)
    text_file = tmp_path / "post.txt"
    text_file.write_text("I'd love to connect with indie hackers\n3 wins this week",
                         encoding="utf-8")
    rc = post_gate.main([
        "--poster", "tester",
        "--platform", "tiktok",
        "--account", "@tt",
        "--action", "create",
        "--source-url", "https://anicca.ai/winner/1",
        "--text-file", str(text_file),
        "--lang", "en",
        "--kind", "connect",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "POST-GATE OK" in out
