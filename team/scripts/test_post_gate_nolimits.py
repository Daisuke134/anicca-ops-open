"""2026-11-28 owner order t167u: plain reposts allowed, no caps, hard safety kept."""
import os, sys, tempfile, json, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_gate as pg
import pytest

def _root(tmp):
    root = tmp / "repo"
    (root / "team/distribution/shortform").mkdir(parents=True)
    (root / "team/lm-compat/lm/config").mkdir(parents=True)
    src = "/workspace/team/"
    import shutil
    shutil.copy(src + "ACCOUNT-OWNERS.md", root / "team/ACCOUNT-OWNERS.md")
    for p in ("distribution/shortform", "lm-compat/lm/config"):
        f = src + p + "/marketing-destinations.json"
        if os.path.exists(f):
            shutil.copy(f, root / "team" / p / "marketing-destinations.json")
    now = dt.datetime.now(pg.JST)
    (root / "team/CLAIMS.md").write_text(f"- POST-CLAIM | {now:%Y-%m-%d %H:%M} JST | x-operator | x:@diceai0 | create | https://x.com/a/status/1\n")
    return root

@pytest.fixture
def env(tmp_path, monkeypatch):
    root = _root(tmp_path)
    monkeypatch.setenv("POST_GATE_LOCAL_ROOT", str(root))
    monkeypatch.setenv("POST_GATE_INTENTS", str(tmp_path / "i.jsonl"))
    rj = tmp_path / "recent.json"
    rj.write_text(json.dumps({"data": []}))
    return rj

def go(rj, text=None, action="create", src="https://x.com/a/status/1", **kw):
    return pg.check("x-operator", "x", "@diceai0", action, src, text=text, recent_json=str(rj), **kw)

def test_repost_needs_no_text_and_twice_refused(env):
    r = go(env, action="repost", src="https://x.com/z/status/99")
    assert r["action"] == "repost"
    with pytest.raises(pg.Refused):
        go(env, action="repost", src="https://x.com/z/status/99")

def test_repost_needs_status_url(env):
    with pytest.raises(pg.Refused):
        go(env, action="repost", src="https://example.org/foo")

def test_many_connects_and_quotes_no_cap(env):
    for i in range(8):
        go(env, f"つながりたいです{i} 個人開発でアプリを作っています。ストアの数字を毎日出します {i*7}", lang="ja", kind="connect")

@pytest.mark.parametrize("t", ["成田です", "Daisuke here", "Our AI agents run the whole company", "I love Pickle", "token " + "sk" + "-" + "abcdefghijklmnopqrstuvwxyz1234"])
def test_safety_refuses(env, t):
    with pytest.raises(pg.Refused):
        go(env, t)

def test_duplicate_refused(env, tmp_path):
    env.write_text(json.dumps({"data": [{"id": "5", "text": "same text here for the dup check please", "created_at": dt.datetime.now(dt.timezone.utc).isoformat()}]}))
    with pytest.raises(pg.Refused):
        go(env, "same text here for the dup check please")
