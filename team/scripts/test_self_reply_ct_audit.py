"""Tests for self_reply_ct_audit."""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import self_reply_ct_audit as m


def test_app_store_url_is_bad():
    result = m.audit([
        {"id": "p1", "text": "check this", "urls": ["https://apps.apple.com/app/id6755129214?ct=x-diceai0-day11-en"]},
    ])
    assert result["n_with_link"] == 1
    assert result["n_ok"] == 0
    assert result["bad"] == [{"id": "p1", "problems": ["direct-app-store"]}]


def test_go_link_with_ct_is_ok():
    result = m.audit([
        {"id": "p2", "text": "link", "urls": ["https://aniccaai.com/go/anicca?ct=x-diceai0-day11-en"]},
    ])
    assert result == {"n_with_link": 1, "n_ok": 1, "bad": []}


def test_go_link_without_ct_is_missing_ct():
    result = m.audit([
        {"id": "p3", "text": "link", "urls": ["https://aniccaai.com/go/anicca"]},
    ])
    assert result["n_with_link"] == 1
    assert result["n_ok"] == 0
    assert result["bad"] == [{"id": "p3", "problems": ["missing-ct"]}]


def test_post_without_url_not_counted():
    result = m.audit([
        {"id": "p4", "text": "no links here", "urls": []},
        {"id": "p5", "text": "also none", "urls": ["notaurl", "ftp://x"]},
    ])
    assert result == {"n_with_link": 0, "n_ok": 0, "bad": []}


def test_mixed_posts():
    posts = [
        {"id": "ok", "text": "", "urls": ["https://aniccaai.com/go/anicca?ct=abc123-def"]},
        {"id": "bad", "text": "", "urls": ["https://apps.apple.com/app/id1?ct=x"]},
        {"id": "none", "text": "", "urls": []},
    ]
    result = m.audit(posts)
    assert result["n_with_link"] == 2
    assert result["n_ok"] == 1
    assert result["bad"][0]["id"] == "bad"


def test_cli_prints_json_and_exit_code(tmp_path):
    posts = [{"id": "p1", "text": "", "urls": ["https://aniccaai.com/go/anicca"]}]
    path = tmp_path / "posts.json"
    path.write_text(json.dumps(posts))
    proc = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "self_reply_ct_audit.py"), str(path)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 1
    out = json.loads(proc.stdout)
    assert out["n_with_link"] == 1
    assert out["bad"][0]["problems"] == ["missing-ct"]


def test_cli_exit_zero_when_all_ok(tmp_path):
    posts = [{"id": "p1", "text": "", "urls": ["https://aniccaai.com/go/anicca?ct=abc123-def"]}]
    path = tmp_path / "posts.json"
    path.write_text(json.dumps(posts))
    proc = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "self_reply_ct_audit.py"), str(path)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0
    out = json.loads(proc.stdout)
    assert out["n_ok"] == 1
    assert out["bad"] == []
