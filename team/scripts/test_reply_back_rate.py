import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reply_back_rate import reply_back_rate

ROOT = "root1"
US = "us"


def post(pid, author, parent, ts):
    return {
        "id": pid,
        "author_id": author,
        "in_reply_to_id": parent,
        "created_at": ts,
    }


def test_synthetic_thread_rate():
    # spec says 4 replies: build exactly 4
    posts = [
        post("r1", "a1", ROOT, "2024-01-01T10:00:00Z"),
        post("a1", US, "r1", "2024-01-01T10:30:00Z"),   # 30m -> in window
        post("r2", "a2", ROOT, "2024-01-01T11:00:00Z"),
        post("a2", US, "r2", "2024-01-01T14:00:00Z"),   # 3h -> out of window
        post("r3", "a3", ROOT, "2024-01-01T12:00:00Z"), # unanswered
        post("r4", "a4", ROOT, "2024-01-01T14:00:00+00:00"),
        post("a4", US, "r4", "2024-01-01T15:30:00Z"),   # 90m -> in window
    ]
    res = reply_back_rate(posts, ROOT, US, window_hours=2.0)
    assert res["replies"] == 4
    assert res["answered_in_window"] == 2
    assert res["rate"] == 0.5
    assert res["median_minutes_to_answer"] == pytest.approx(60.0)


def test_self_replies_not_counted():
    posts = [
        post("r1", US, ROOT, "2024-01-01T10:00:00Z"),
        post("a1", US, "r1", "2024-01-01T10:10:00Z"),
    ]
    res = reply_back_rate(posts, ROOT, US)
    assert res["replies"] == 0
    assert res["rate"] is None
    assert res["median_minutes_to_answer"] is None


def test_bad_rows_skipped():
    posts = [
        {"id": "bad1"},  # missing fields
        {"id": "bad2", "author_id": "a", "in_reply_to_id": ROOT,
         "created_at": "not-a-date"},
        None,
        "garbage",
        post("r1", "a1", ROOT, "2024-01-01T10:00:00Z"),
        post("a1", US, "r1", "2024-01-01T10:15:00Z"),
    ]
    res = reply_back_rate(posts, ROOT, US)
    assert res["replies"] == 1
    assert res["answered_in_window"] == 1
    assert res["rate"] == 1.0
    assert res["median_minutes_to_answer"] == pytest.approx(15.0)


def test_no_replies_null_rate():
    res = reply_back_rate([], ROOT, US)
    assert res == {
        "replies": 0,
        "answered_in_window": 0,
        "rate": None,
        "median_minutes_to_answer": None,
    }


def test_answer_before_reply_not_counted():
    posts = [
        post("a1", US, "r1", "2024-01-01T09:00:00Z"),  # before reply
        post("r1", "a1", ROOT, "2024-01-01T10:00:00Z"),
    ]
    res = reply_back_rate(posts, ROOT, US)
    assert res["answered_in_window"] == 0
    assert res["rate"] == 0.0


def xapi_tweet(tid, author, parent, ts):
    refs = []
    if parent is not None:
        refs.append({"type": "replied_to", "id": parent})
    return {
        "id": tid,
        "author_id": author,
        "created_at": ts,
        "referenced_tweets": refs,
    }


def test_xapi_search_json_shape():
    payload = {
        "data": [
            xapi_tweet("r1", "a1", ROOT, "2024-01-01T10:00:00Z"),
            xapi_tweet("a1", US, "r1", "2024-01-01T10:30:00Z"),
            xapi_tweet("r2", "a2", ROOT, "2024-01-01T11:00:00Z"),
            xapi_tweet("a2", US, "r2", "2024-01-01T14:00:00Z"),
            xapi_tweet("r3", "a3", ROOT, "2024-01-01T12:00:00Z"),
            xapi_tweet("r4", "a4", ROOT, "2024-01-01T14:00:00+00:00"),
            xapi_tweet("a4", US, "r4", "2024-01-01T15:30:00Z"),
        ],
        "meta": {"result_count": 7},
    }
    res = reply_back_rate(payload, ROOT, US, window_hours=2.0)
    assert res["replies"] == 4
    assert res["answered_in_window"] == 2
    assert res["rate"] == 0.5
    assert res["median_minutes_to_answer"] == pytest.approx(60.0)


def test_xapi_shape_matches_list_shape():
    xapi = {
        "data": [
            xapi_tweet("r1", "a1", ROOT, "2024-01-01T10:00:00Z"),
            xapi_tweet("a1", US, "r1", "2024-01-01T10:10:00Z"),
            xapi_tweet("top", "a9", None, "2024-01-01T09:00:00Z"),
        ]
    }
    plist = [
        post("r1", "a1", ROOT, "2024-01-01T10:00:00Z"),
        post("a1", US, "r1", "2024-01-01T10:10:00Z"),
        post("top", "a9", None, "2024-01-01T09:00:00Z"),
    ]
    assert reply_back_rate(xapi, ROOT, US) == reply_back_rate(plist, ROOT, US)


def test_xapi_empty_and_missing_data():
    assert reply_back_rate({"data": []}, ROOT, US)["replies"] == 0
    assert reply_back_rate({"meta": {}}, ROOT, US)["replies"] == 0


def test_cli_xapi_json(tmp_path):
    payload = {
        "data": [
            xapi_tweet("r1", "a1", ROOT, "2024-01-01T10:00:00Z"),
            xapi_tweet("a1", US, "r1", "2024-01-01T10:10:00Z"),
        ]
    }
    f = tmp_path / "search.json"
    f.write_text(json.dumps(payload))
    script = Path(__file__).resolve().parent / "reply_back_rate.py"
    out = subprocess.run(
        [sys.executable, str(script), str(f), ROOT, US, "2"],
        capture_output=True, text=True, check=True,
    )
    res = json.loads(out.stdout)
    assert res["replies"] == 1
    assert res["answered_in_window"] == 1


def test_cli(tmp_path):
    data = [
        post("r1", "a1", ROOT, "2024-01-01T10:00:00Z"),
        post("a1", US, "r1", "2024-01-01T10:10:00Z"),
    ]
    f = tmp_path / "posts.json"
    f.write_text(json.dumps(data))
    script = Path(__file__).resolve().parent / "reply_back_rate.py"
    out = subprocess.run(
        [sys.executable, str(script), str(f), ROOT, US, "2"],
        capture_output=True, text=True, check=True,
    )
    res = json.loads(out.stdout)
    assert res["replies"] == 1
    assert res["answered_in_window"] == 1
