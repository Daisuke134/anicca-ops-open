import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import go_redirect_probe as probe


def fake_fetch(result):
    calls = []

    def fetch(url):
        calls.append(url)
        return result

    fetch.calls = calls
    return fetch


def good_location(ct="abc123"):
    return (302, f"https://apps.apple.com/app/id123456?ct={ct}&mt=8")


def test_pass_redirect():
    f = fake_fetch(good_location("abc123"))
    ok, reason = probe.check("abc123", f)
    assert ok and reason == ""
    assert f.calls == ["https://aniccaai.com/go/anicca?ct=abc123"]


def test_missing_ct_fails():
    f = fake_fetch((301, "https://apps.apple.com/app/id123456?mt=8"))
    ok, reason = probe.check("abc123", f)
    assert not ok and "ct" in reason


def test_wrong_host_fails():
    f = fake_fetch((302, "https://evil.example.com/app?ct=abc123"))
    ok, reason = probe.check("abc123", f)
    assert not ok and "evil.example.com" in reason


def test_200_status_fails():
    f = fake_fetch((200, "https://apps.apple.com/app?ct=abc123"))
    ok, reason = probe.check("abc123", f)
    assert not ok and "200" in reason


def test_cli_exit_code(monkeypatch, capsys):
    monkeypatch.setattr(probe, "fetch", lambda url: good_location("ct-ok"))
    rc = probe.main(["ct-ok", "ct-ok"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "PASS ct-ok" in out
    assert "go pass=2/2" in out

    monkeypatch.setattr(probe, "fetch", lambda url: (200, ""))
    rc = probe.main(["ct-ok"])
    assert rc == 1
    out = capsys.readouterr().out
    assert "FAIL ct-ok" in out
    assert "go pass=0/1" in out
