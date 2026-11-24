#!/usr/bin/env python3
"""Proves a wired posting script calls the gate BEFORE any network call. urlopen is replaced; nothing is posted."""
import datetime as dt
import importlib.util
import json
import os
import sys
import urllib.request

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import post_gate  # noqa: E402

SRC = "https://anicca.ai/winner/shortform-1"
INTEGRATION = "cmp93bkpu01uvoh0yd3aj560g"
PAYLOAD = {"type": "now", "posts": [{"integration": {"id": INTEGRATION},
                                    "value": [{"content": "x"}],
                                    "settings": {"__type": "tiktok"}}]}

spec = importlib.util.spec_from_file_location(
    "shortform_post", os.path.join(ROOT, "team", "distribution", "shortform", "post.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def _fixture(tmp_path, claims=""):
    repo = tmp_path / "repo"
    (repo / "team" / "distribution" / "shortform").mkdir(parents=True)
    (repo / "team").mkdir(parents=True, exist_ok=True)
    (repo / "team" / "ACCOUNT-OWNERS.md").write_text(
        "```post-gate-owners\n"
        f"tiktok | @aniccaaffirmation | muse | {INTEGRATION}\n"
        "```\n",
        encoding="utf-8",
    )
    (repo / "team" / "CLAIMS.md").write_text(claims, encoding="utf-8")
    (repo / "team" / "distribution" / "shortform" / "marketing-destinations.json").write_text(
        json.dumps({"targets": [{"platform": "tiktok", "native_handle": "@aniccaaffirmation",
                                 "integration_id": INTEGRATION}],
                    "holds": []}),
        encoding="utf-8",
    )
    return repo


@pytest.fixture
def gated(tmp_path, monkeypatch):
    """Block all network, point the gate at a tmp intents ledger, return the call log."""
    calls = []

    def fake_urlopen(request, *a, **k):
        calls.append(request.full_url)
        raise RuntimeError("NETWORK BLOCKED IN TEST")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("POST_GATE_INTENTS", str(tmp_path / "intents.jsonl"))
    monkeypatch.setenv("ANICCA_SOURCE_URL", SRC)
    return calls


def _attempt(monkeypatch, poster, repo):
    monkeypatch.setenv("ANICCA_POSTER", poster)
    monkeypatch.setenv("POST_GATE_LOCAL_ROOT", str(repo))
    try:
        mod.req("POST", "/posts", PAYLOAD)
        return 0
    except SystemExit as e:
        return e.code
    except RuntimeError:
        return "reached-network(blocked by test)"


def test_gate_refuses_wrong_owner_before_network(tmp_path, monkeypatch, gated):
    repo = _fixture(tmp_path)
    code = _attempt(monkeypatch, "参謀", repo)
    assert code == 2 and gated == []


def test_gate_refuses_missing_claim_before_network(tmp_path, monkeypatch, gated):
    repo = _fixture(tmp_path)  # no POST-CLAIM for muse
    code = _attempt(monkeypatch, "muse", repo)
    assert code == 2 and gated == []


def test_gate_passes_claimed_post_reaches_network(tmp_path, monkeypatch, gated):
    claim_at = dt.datetime.now(post_gate.JST) - dt.timedelta(minutes=10)
    claims = (f"- POST-CLAIM | {claim_at:%Y-%m-%d %H:%M} JST | muse | "
              f"tiktok:@aniccaaffirmation | create | {SRC}\n")
    repo = _fixture(tmp_path, claims)
    code = _attempt(monkeypatch, "muse", repo)
    assert code == "reached-network(blocked by test)"
    assert len(gated) == 1 and gated[0].endswith("/posts")
