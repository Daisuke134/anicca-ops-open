"""Self-contained tests for post_gate's gate result and non-blocking advice output."""
import datetime as dt
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_gate


def _write_repo(root):
    (root / "team" / "distribution" / "shortform").mkdir(parents=True)
    (root / "team").mkdir(parents=True, exist_ok=True)
    (root / "team" / "ACCOUNT-OWNERS.md").write_text(
        "```post-gate-owners\n"
        "x | @test | tester |\n"
        "```\n",
        encoding="utf-8",
    )
    (root / "team" / "CLAIMS.md").write_text(
        "- POST-CLAIM | 2026-11-22 12:00 JST | tester | x:@test | create | https://anicca.ai/winner/1\n",
        encoding="utf-8",
    )
    (root / "team" / "distribution" / "shortform" / "marketing-destinations.json").write_text(
        json.dumps({"targets": [{"platform": "x", "native_handle": "@test"}], "holds": []}),
        encoding="utf-8",
    )


def test_check_allows_owned_claimed_x_create(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    _write_repo(repo)
    recent = tmp_path / "recent.json"
    recent.write_text("[]", encoding="utf-8")
    monkeypatch.setenv("POST_GATE_LOCAL_ROOT", str(repo))
    monkeypatch.setenv("POST_GATE_IGNORE_MTIME", "1")
    monkeypatch.setenv("POST_GATE_INTENTS", str(tmp_path / "intents.jsonl"))
    monkeypatch.setattr(post_gate, "ct_link_check", lambda *args, **kwargs: None)

    now = dt.datetime(2026, 11, 22, 12, 0, tzinfo=post_gate.JST)
    result = post_gate.check(
        "tester",
        "x",
        "@test",
        "create",
        "https://anicca.ai/winner/1",
        now=now,
        text="A fresh post",
        recent_json=str(recent),
    )

    assert result["allowed"] is True
    assert result["poster"] == "tester"
    assert result["account"] == "x:@test"


def test_check_still_refuses_without_claim(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    _write_repo(repo)
    (repo / "team" / "CLAIMS.md").write_text("", encoding="utf-8")
    recent = tmp_path / "recent.json"
    recent.write_text("[]", encoding="utf-8")
    monkeypatch.setenv("POST_GATE_LOCAL_ROOT", str(repo))
    monkeypatch.setenv("POST_GATE_IGNORE_MTIME", "1")
    monkeypatch.setenv("POST_GATE_INTENTS", str(tmp_path / "intents.jsonl"))
    monkeypatch.setattr(post_gate, "ct_link_check", lambda *args, **kwargs: None)

    now = dt.datetime(2026, 11, 22, 12, 0, tzinfo=post_gate.JST)
    with pytest.raises(post_gate.Refused, match="no POST-CLAIM"):
        post_gate.check(
            "tester",
            "x",
            "@test",
            "create",
            "https://anicca.ai/winner/1",
            now=now,
            text="A fresh post",
            recent_json=str(recent),
        )


def test_main_prints_connect_advice_without_blocking(tmp_path, monkeypatch, capsys):
    text_file = tmp_path / "post.txt"
    text_file.write_text("今日の学びを共有します\nつながりたい方はぜひ", encoding="utf-8")
    monkeypatch.setattr(post_gate, "check", lambda *args, **kwargs: {"allowed": True})

    rc = post_gate.main([
        "--poster", "tester",
        "--platform", "x",
        "--account", "@test",
        "--action", "create",
        "--source-url", "https://anicca.ai/winner/1",
        "--text-file", str(text_file),
    ])

    out = capsys.readouterr().out
    assert rc == 0
    assert "POST-GATE OK" in out
    assert "POST-GATE ADVICE-WARN: connect request must be line 1 (X-STYLE 11/22)" in out
