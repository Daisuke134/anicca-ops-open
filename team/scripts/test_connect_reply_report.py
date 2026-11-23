import csv
import io
import json

import connect_reply_report
import reply_back_rate


ROOT_ONE = "9000000000000000001"
ROOT_TWO = "9000000000000000002"
OUR_AUTHOR_ID = "1111111111111111111"


def _conversation(root_id, reply_id):
    return {
        "data": [
            {
                "id": root_id,
                "author_id": "2222222222222222222",
                "created_at": "2026-01-01T00:00:00Z",
                "referenced_tweets": [],
            },
            {
                "id": reply_id,
                "author_id": "3333333333333333333",
                "created_at": "2026-01-01T00:05:00Z",
                "referenced_tweets": [{"type": "replied_to", "id": root_id}],
            },
            {
                "id": "4444444444444444444",
                "author_id": OUR_AUTHOR_ID,
                "created_at": "2026-01-01T00:10:00Z",
                "referenced_tweets": [{"type": "replied_to", "id": reply_id}],
            },
        ]
    }


def test_main_prints_csv_rows_for_each_conversation_file(tmp_path, monkeypatch, capsys):
    (tmp_path / f"{ROOT_TWO}.json").write_text(
        json.dumps(_conversation(ROOT_TWO, "5555555555555555555")),
        encoding="utf-8",
    )
    (tmp_path / f"{ROOT_ONE}.json").write_text(
        json.dumps(_conversation(ROOT_ONE, "6666666666666666666")),
        encoding="utf-8",
    )

    calls = []
    posts_seen = {}

    def fake_reply_back_rate(posts, root_id, our_author_id, window_hours):
        calls.append((root_id, our_author_id, window_hours))
        posts_seen[root_id] = posts
        if root_id == ROOT_ONE:
            if window_hours == 2.0:
                return {
                    "replies": 2,
                    "answered_in_window": 1,
                    "rate": 0.5,
                    "median_minutes_to_answer": 12.5,
                }
            return {
                "replies": 2,
                "answered_in_window": 2,
                "rate": 1.0,
                "median_minutes_to_answer": 45.25,
            }
        if window_hours == 2.0:
            return {
                "replies": 3,
                "answered_in_window": 0,
                "rate": None,
                "median_minutes_to_answer": None,
            }
        return {
            "replies": 3,
            "answered_in_window": 1,
            "rate": 0.25,
            "median_minutes_to_answer": None,
        }

    monkeypatch.setattr(reply_back_rate, "reply_back_rate", fake_reply_back_rate)

    assert connect_reply_report.main([str(tmp_path), OUR_AUTHOR_ID]) == 0

    output = capsys.readouterr().out
    reader = csv.DictReader(io.StringIO(output))
    assert reader.fieldnames == ["root_id", "n", "rate_2h", "rate_24h", "median_min"]
    assert list(reader) == [
        {
            "root_id": ROOT_ONE,
            "n": "2",
            "rate_2h": "0.5",
            "rate_24h": "1.0",
            "median_min": "45.25",
        },
        {
            "root_id": ROOT_TWO,
            "n": "3",
            "rate_2h": "",
            "rate_24h": "0.25",
            "median_min": "",
        },
    ]
    assert calls == [
        (ROOT_ONE, OUR_AUTHOR_ID, 2.0),
        (ROOT_ONE, OUR_AUTHOR_ID, 24.0),
        (ROOT_TWO, OUR_AUTHOR_ID, 2.0),
        (ROOT_TWO, OUR_AUTHOR_ID, 24.0),
    ]
    assert posts_seen[ROOT_ONE]["data"][0]["id"] == ROOT_ONE
    assert posts_seen[ROOT_TWO]["data"][0]["id"] == ROOT_TWO
