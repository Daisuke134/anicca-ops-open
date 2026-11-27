"""Wiring tests: dup_pairs is enforced inside post_gate.check for X create/schedule."""
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


def _setup(tmp_path, monkeypatch, posts):
    repo = tmp_path / "repo"
    _write_repo(repo)
    recent = tmp_path / "recent.json"
    recent.write_text(json.dumps(posts), encoding="utf-8")
    monkeypatch.setenv("POST_GATE_LOCAL_ROOT", str(repo))
    monkeypatch.setenv("POST_GATE_IGNORE_MTIME", "1")
    monkeypatch.setenv("POST_GATE_INTENTS", str(tmp_path / "intents.jsonl"))
    monkeypatch.setattr(post_gate, "ct_link_check", lambda *args, **kwargs: None)
    return recent


def _check(recent):
    now = dt.datetime(2026, 11, 22, 12, 0, tzinfo=post_gate.JST)
    return post_gate.check(
        "tester", "x", "@test", "create", "https://anicca.ai/winner/1",
        now=now, text="a brand new candidate post text", recent_json=str(recent),
    )


def test_check_refuses_when_readback_shows_same_text_twice_within_10min(tmp_path, monkeypatch):
    base = dt.datetime(2026, 11, 22, 11, 0, tzinfo=post_gate.JST)
    posts = [
        {"id": "111", "text": "oops posted twice ok", "created_at": base.isoformat()},
        {"id": "222", "text": "oops posted twice ok", "created_at": (base + dt.timedelta(minutes=3)).isoformat()},
    ]
    recent = _setup(tmp_path, monkeypatch, posts)
    with pytest.raises(post_gate.Refused, match="duplicate scan"):
        _check(recent)


def test_check_allows_when_same_text_posts_are_spaced_out(tmp_path, monkeypatch):
    base = dt.datetime(2026, 11, 22, 10, 0, tzinfo=post_gate.JST)
    posts = [
        {"id": "111", "text": "repeated but spaced out ok", "created_at": base.isoformat()},
        {"id": "222", "text": "repeated but spaced out ok", "created_at": (base + dt.timedelta(minutes=45)).isoformat()},
    ]
    recent = _setup(tmp_path, monkeypatch, posts)
    assert _check(recent)["allowed"] is True


def test_check_allows_clean_readback(tmp_path, monkeypatch):
    base = dt.datetime(2026, 11, 22, 11, 0, tzinfo=post_gate.JST)
    posts = [
        {"id": "111", "text": "first distinct live post ok", "created_at": base.isoformat()},
        {"id": "222", "text": "second distinct live post ok", "created_at": (base + dt.timedelta(minutes=1)).isoformat()},
    ]
    recent = _setup(tmp_path, monkeypatch, posts)
    assert _check(recent)["allowed"] is True
