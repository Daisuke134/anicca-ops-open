import csv
import json
import math

import presim_close

HEADER = [
    "post_id",
    "pred_impr",
    "pred_likes",
    "actual_impr",
    "actual_likes",
    "actual_replies",
    "abs_log_err_impr",
    "abs_log_err_likes",
]

POSTS = {
    "data": [
        {
            "id": "1001",
            "created_at": "2026-11-10T00:00:00.000Z",
            "public_metrics": {
                "impression_count": 500,
                "like_count": 12,
                "reply_count": 3,
            },
        },
        {
            "id": "1002",
            "created_at": "2026-11-14T12:00:00.000Z",
            "public_metrics": {
                "impression_count": 999,
                "like_count": 99,
                "reply_count": 9,
            },
        },
        {
            "id": "1003",
            "created_at": "2026-11-01T00:00:00.000Z",
            "public_metrics": {
                "impression_count": 700,
                "like_count": 70,
                "reply_count": 7,
            },
        },
        {
            "id": "1004",
            "created_at": "2026-11-01T00:00:00.000Z",
            "public_metrics": {
                "impression_count": 800,
                "like_count": 80,
                "reply_count": 8,
            },
        },
    ]
}

NOW = "2026-11-15T00:00:00+00:00"


def make_csv(tmp_path):
    path = tmp_path / "presim-log.csv"
    rows = [
        # closable: digits, empty actual, post 120h old
        ["1001", "400", "10", "", "", "", "", ""],
        # <24h old at NOW
        ["1002", "100", "5", "", "", "", "", ""],
        # already closed
        ["1003", "300", "6", "500", "8", "2", "0.511", "0.154"],
        # non-numeric post_id
        ["queue-abc", "200", "4", "", "", "", "", ""],
    ]
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(HEADER)
        w.writerows(rows)
    return path


def read_rows(csv_path):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def test_closes_only_eligible_row(tmp_path, capsys):
    csv_path = tmp_path / "presim-log.csv"
    posts_path = tmp_path / "posts.json"
    posts_path.write_text(json.dumps(POSTS))
    csv_path = make_csv(tmp_path)
    assert presim_close.main([str(posts_path), "--now", NOW, "--csv", str(csv_path), "--write"]) == 0
    out = capsys.readouterr().out
    assert "1001 400 500" in out

    rows = read_rows(csv_path)
    closed = rows[0]
    assert closed["actual_impr"] == "500"
    assert closed["actual_likes"] == "12"
    assert closed["actual_replies"] == "3"
    assert closed["abs_log_err_impr"] == str(round(abs(math.log(500 / 400)), 3))
    assert closed["abs_log_err_likes"] == str(round(abs(math.log(13 / 11)), 3))

    # <24h row untouched
    assert rows[1]["actual_impr"] == ""
    assert rows[1]["abs_log_err_impr"] == ""
    # already-closed row untouched
    assert rows[2]["actual_impr"] == "500"
    assert rows[2]["abs_log_err_impr"] == "0.511"
    # non-numeric post_id untouched
    assert rows[3]["actual_impr"] == ""


def test_untouched_rows_byte_identical(tmp_path):
    csv_path = tmp_path / "presim-log.csv"
    original = make_csv(tmp_path).read_text()
    posts_path = tmp_path / "posts.json"
    posts_path.write_text(json.dumps(POSTS))
    presim_close.main([str(posts_path), "--now", NOW, "--csv", str(csv_path), "--write"])
    lines = original.splitlines(keepends=True)
    assert lines[1] == original.splitlines(keepends=True)[1]  # sanity
    # untouched rows remain byte-identical
    new_lines = csv_path.read_text().splitlines(keepends=True)
    assert new_lines[0] == lines[0]
    assert new_lines[2] == lines[2]
    assert new_lines[3] == lines[3]
    assert new_lines[4] == lines[4]


def test_zero_metrics_leave_err_empty(tmp_path, capsys):
    posts = {"data": [{"id": "2001", "created_at": "2026-11-01T00:00:00Z",
                       "public_metrics": {"impression_count": 0, "like_count": 0, "reply_count": 0}}]}
    csv_path = tmp_path / "presim-log.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(HEADER)
        w.writerow(["2001", "100", "10", "", "", "", "", ""])
    posts_path = tmp_path / "posts.json"
    posts_path.write_text(json.dumps(posts))
    assert presim_close.main([str(posts_path), "--now", NOW, "--csv", str(csv_path), "--write"]) == 0
    rows = read_rows(csv_path)
    assert rows[0]["actual_impr"] == "0"
    assert rows[0]["abs_log_err_impr"] == ""
    assert rows[0]["abs_log_err_likes"] == str(round(abs(math.log(1 / 11)), 3))


def test_no_write_leaves_csv(tmp_path):
    csv_path = tmp_path / "presim-log.csv"
    original = make_csv(tmp_path).read_text()
    posts_path = tmp_path / "posts.json"
    posts_path.write_text(json.dumps(POSTS))
    assert presim_close.main([str(posts_path), "--now", NOW, "--csv", str(csv_path)]) == 0
    assert csv_path.read_text() == original
