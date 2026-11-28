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


def test_intent_lock_refuses_identical_create_within_30min(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    _write_tiktok_repo(repo)
    intents = tmp_path / "intents.jsonl"
    monkeypatch.setenv("POST_GATE_LOCAL_ROOT", str(repo))
    monkeypatch.setenv("POST_GATE_INTENTS", str(intents))

    now = dt.datetime(2026, 11, 22, 12, 0, tzinfo=post_gate.JST)
    src = "https://anicca.ai/winner/1"
    first = post_gate.check("tester", "tiktok", "@tt", "create", src, now=now,
                            text="same exact post text")
    assert first["allowed"] is True
    assert intents.exists()

    # second create with the same text sha256 inside 30 min -> refused
    with pytest.raises(post_gate.Refused, match="intent lock"):
        post_gate.check("tester", "tiktok", "@tt", "create", src, now=now,
                        text="same exact post text")
    # a schedule of the same text is refused too
    with pytest.raises(post_gate.Refused, match="intent lock"):
        post_gate.check("tester", "tiktok", "@tt", "schedule", src, now=now,
                        text="same exact post text")
    # different text is still allowed
    ok = post_gate.check("tester", "tiktok", "@tt", "create", src, now=now,
                         text="a completely different post text")
    assert ok["allowed"] is True
    # after 30 minutes the same text may be posted again
    later = now + dt.timedelta(minutes=31)
    again = post_gate.check("tester", "tiktok", "@tt", "create", src, now=later,
                            text="same exact post text")
    assert again["allowed"] is True


def test_en_connect_opener_refuses_number_first():
    with pytest.raises(post_gate.Refused, match="lead with the request"):
        post_gate.check_en_connect_opener("3 wins this week\nI'd love to connect with builders")
    with pytest.raises(post_gate.Refused, match="lead with the request"):
        post_gate.check_en_connect_opener("$2,400 MRR\nI'd love to connect")
    with pytest.raises(post_gate.Refused, match="lead with the request"):
        post_gate.check_en_connect_opener("Day 12 of building in public\nI'd love to connect")


def test_en_connect_opener_passes_request_first():
    assert post_gate.check_en_connect_opener(
        "\nI'd love to connect with indie hackers\n3 wins this week") is None


def test_en_connect_opener_ignored_for_ja(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    _write_repo(repo)
    recent = tmp_path / "recent.json"
    recent.write_text("[]", encoding="utf-8")
    monkeypatch.setenv("POST_GATE_LOCAL_ROOT", str(repo))
    monkeypatch.setenv("POST_GATE_IGNORE_MTIME", "1")
    monkeypatch.setenv("POST_GATE_INTENTS", str(tmp_path / "intents.jsonl"))
    monkeypatch.setattr(post_gate, "ct_link_check", lambda *args, **kwargs: None)

    now = dt.datetime(2026, 11, 22, 12, 0, tzinfo=post_gate.JST)
    res = post_gate.check(
        "tester", "x", "@test", "create", "https://anicca.ai/winner/1",
        now=now, text="3つの学び\nつながりたい方はぜひ", recent_json=str(recent),
        lang="ja", kind="connect",
    )
    assert res["allowed"] is True


def test_main_prints_connect_advice_without_blocking(tmp_path, monkeypatch, capsys):
    text_file = tmp_path / "post.txt"
    text_file.write_text("今日の学びを共有します\nつながりたい方はぜひ", encoding="utf-8")
    monkeypatch.setattr(post_gate, "check", lambda *args, **kwargs: {"allowed": True})
    monkeypatch.setattr(post_gate, "presim_logged", lambda *args, **kwargs: True)

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
