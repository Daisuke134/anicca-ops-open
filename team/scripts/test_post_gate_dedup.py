import datetime as dt
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_gate

JST = post_gate.JST


def now():
    return dt.datetime.now(JST)


def post(text, when=None, pid="1", in_reply_to=""):
    when = when or now()
    p = {"id": pid, "text": text, "created_at": when.isoformat()}
    if in_reply_to:
        p["in_reply_to_user_id"] = in_reply_to
    return p


# ------------------------------------------------------------- norm_text / first_line / text_key
def test_norm_text_drops_urls_punctuation_case():
    assert post_gate.norm_text("  Check This OUT!!! https://x.com/a/status/1.  ") == "check this out"
    assert post_gate.norm_text("Hello, World?!") == "hello world"
    assert post_gate.norm_text("") == ""


def test_first_line_skips_blank_lines():
    assert post_gate.first_line("\n\n   \nThe Real First Line!\nsecond line") == "the real first line"
    assert post_gate.first_line("   \n\t\n") == ""


def test_text_key_differs_with_in_reply_to():
    t = "hello world this is a test post"
    assert post_gate.text_key(t) != post_gate.text_key(t, in_reply_to="12345")
    assert post_gate.text_key(t) == post_gate.text_key(t)


# ------------------------------------------------------------- x_dedup_check recent-post rules
def test_dedup_refuses_identical_text_live_within_24h():
    t = "Identical text that was already posted live one hour ago ok"
    recent = [post(t, now() - dt.timedelta(hours=1), pid="42")]
    with pytest.raises(post_gate.Refused):
        post_gate.x_dedup_check("@acct", t, recent, now(), now=now(), intents=[])


def test_dedup_refuses_same_first_line_different_body():
    fl = "This is a shared opening line that is definitely long enough"
    body_a = ("First body talks entirely about quarterly revenue numbers, hiring plans "
              "and office logistics for the winter season ahead of us all right now.")
    body_b = ("Second body discusses weekend hiking trails, homemade pasta recipes, "
              "garden pruning tips and a completely unrelated assortment of topics.")
    recent = [post(fl + "\n" + body_a, now() - dt.timedelta(hours=2), pid="7")]
    cand = fl + "\n" + body_b
    with pytest.raises(post_gate.Refused):
        post_gate.x_dedup_check("@acct", cand, recent, now(), now=now(), intents=[])


def test_dedup_refuses_near_same_text_only_url_changed():
    base = "We shipped the new pipeline today and results look amazing across the board"
    recent = [post(base + " https://example.com/v1", now() - dt.timedelta(hours=1), pid="9")]
    cand = base + " https://example.com/v2-different"
    with pytest.raises(post_gate.Refused):
        post_gate.x_dedup_check("@acct", cand, recent, now(), now=now(), intents=[])


def test_dedup_allows_same_text_older_than_24h():
    t = "This exact same text was posted more than twenty four hours ago"
    recent = [post(t, now() - dt.timedelta(hours=25), pid="3")]
    assert post_gate.x_dedup_check("@acct", t, recent, now(), now=now(), intents=[])["dedup"] == "ok"


def test_dedup_allows_clearly_different_text():
    recent = [post("Completely unrelated post about lunch recipes and weekend plans",
                  now() - dt.timedelta(hours=1), pid="5")]
    cand = "Announcing our brand new product launch next Tuesday morning everyone"
    assert post_gate.x_dedup_check("@acct", cand, recent, now(), now=now(), intents=[])["dedup"] == "ok"


def test_dedup_allows_empty_recent_list():
    assert post_gate.x_dedup_check("@acct", "Any fresh text to post today ok",
                                   [], now(), now=now(), intents=[])["dedup"] == "ok"


def test_dedup_refuses_empty_text():
    with pytest.raises(post_gate.Refused):
        post_gate.x_dedup_check("@acct", "   \n  ", [], now(), now=now(), intents=[])


# ------------------------------------------------------------- intent ledger
def intent_for(text, account="@acct", ts=None, poster="tester"):
    return {"at": "2026-11-14 12:00:00 JST", "ts": (ts or now()).timestamp(),
            "account": account, "poster": poster, "key": post_gate.text_key(text),
            "first_line": post_gate.first_line(text)[:80], "in_reply_to": ""}


def test_dedup_refuses_recent_intent_before_readback_catches_up():
    t = "A post text that was attempted a minute ago and may have gone through"
    it = intent_for(t, ts=now())
    with pytest.raises(post_gate.Refused):
        post_gate.x_dedup_check("@acct", t, [], now() + dt.timedelta(minutes=1),
                                now=now(), intents=[it])


def test_dedup_allows_intent_when_readback_at_least_3min_after_attempt():
    t = "A post text that was attempted a while ago and readback is fresh"
    it = intent_for(t, ts=now())
    res = post_gate.x_dedup_check("@acct", t, [], now() + dt.timedelta(minutes=4),
                                  now=now(), intents=[it])
    assert res["dedup"] == "ok"


def test_dedup_ignores_intent_for_another_account():
    t = "Same text but recorded against a different account entirely ok"
    it = intent_for(t, account="@other", ts=now())
    res = post_gate.x_dedup_check("@acct", t, [], now() + dt.timedelta(minutes=1),
                                  now=now(), intents=[it])
    assert res["dedup"] == "ok"


# ------------------------------------------------------------- dup_pairs (Buffer same-text-per-profile guard)
def test_dup_pairs_flags_same_text_same_profile_within_window():
    t0 = now()
    posts = [
        post("double submit text here ok", t0, pid="1", in_reply_to=""),
        post("double submit text here ok", t0 + dt.timedelta(minutes=2), pid="2"),
    ]
    pairs = post_gate.dup_pairs(posts, window_min=10)
    assert len(pairs) == 1
    assert {p["id"] for p in pairs[0]} == {"1", "2"}


def test_dup_pairs_allows_same_text_different_profiles():
    t0 = now()
    posts = [
        {**post("same text on two channels", t0, pid="1"), "profile": "chan-a"},
        {**post("same text on two channels", t0 + dt.timedelta(minutes=1), pid="2"), "profile": "chan-b"},
    ]
    assert post_gate.dup_pairs(posts, window_min=10) == []


def test_dup_pairs_allows_same_text_outside_window():
    t0 = now()
    posts = [
        post("same text spaced well apart ok", t0, pid="1"),
        post("same text spaced well apart ok", t0 + dt.timedelta(minutes=30), pid="2"),
    ]
    assert post_gate.dup_pairs(posts, window_min=10) == []


def test_dup_pairs_window_min_parameter_is_respected():
    t0 = now()
    posts = [
        post("same text fifteen minutes apart", t0, pid="1"),
        post("same text fifteen minutes apart", t0 + dt.timedelta(minutes=15), pid="2"),
    ]
    assert post_gate.dup_pairs(posts, window_min=10) == []
    assert len(post_gate.dup_pairs(posts, window_min=20)) == 1


def test_dup_pairs_ignores_different_text_and_bad_rows():
    t0 = now()
    posts = [
        post("first distinct text ok", t0, pid="1"),
        post("second distinct text ok", t0 + dt.timedelta(minutes=1), pid="2"),
        {"text": "no timestamp at all"},
        "not-a-dict",
        {"created_at": t0.isoformat()},
    ]
    assert post_gate.dup_pairs(posts, window_min=10) == []


def test_dup_pairs_normalizes_urls_and_punctuation():
    t0 = now()
    posts = [
        post("Check this out!!! https://example.com/a", t0, pid="1"),
        post("check this out https://example.com/b", t0 + dt.timedelta(seconds=30), pid="2"),
    ]
    assert len(post_gate.dup_pairs(posts, window_min=10)) == 1


def test_dup_pairs_empty_input():
    assert post_gate.dup_pairs([], window_min=10) == []
    assert post_gate.dup_pairs(None, window_min=10) == []


# ------------------------------------------------------------- record_intent / load_intents round-trip
def test_record_and_load_intents_round_trip(tmp_path, monkeypatch):
    intents_file = tmp_path / "intents.jsonl"
    monkeypatch.setenv("POST_GATE_INTENTS", str(intents_file))

    assert post_gate.load_intents() == []

    t = "Round trip intent text that should persist in the ledger file"
    rec1 = post_gate.record_intent("@acct", "tester", t)
    rec2 = post_gate.record_intent("@acct", "tester", t, in_reply_to="999")

    loaded = post_gate.load_intents()
    assert len(loaded) == 2
    assert loaded[0]["key"] == rec1["key"] == post_gate.text_key(t)
    assert loaded[0]["account"] == "@acct"
    assert loaded[0]["poster"] == "tester"
    assert loaded[1]["key"] == rec2["key"] == post_gate.text_key(t, in_reply_to="999")
    assert loaded[1]["key"] != loaded[0]["key"]
    assert intents_file.exists()
    assert len(intents_file.read_text().strip().splitlines()) == 2
