import csv
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import presim_status_join as psj

SCRIPT = Path(__file__).resolve().parent / "presim_status_join.py"


def _post(pid, text, impr):
    return {
        "id": pid,
        "text": text,
        "public_metrics": {"impression_count": impr},
    }


def test_join_single_match():
    rows = [{"post_id": "p1", "text_preview": "Hello world this is a preview", "actual_impr": ""}]
    posts = {"data": [_post("999", "Hello world this is a preview with more text", 42)]}
    out = psj.join(rows, posts)
    assert out[0]["status_id"] == "999"
    assert out[0]["actual_impr"] == 42


def test_join_no_match():
    rows = [{"post_id": "p1", "text_preview": "Completely different text", "actual_impr": ""}]
    posts = {"data": [_post("999", "Hello world this is a preview with more text", 42)]}
    out = psj.join(rows, posts)
    assert "status_id" not in out[0]
    assert out[0]["actual_impr"] == ""


def test_join_ambiguous_two_matches():
    rows = [{"post_id": "p1", "text_preview": "Same opening text here", "actual_impr": ""}]
    posts = {
        "data": [
            _post("1", "Same opening text here first post", 10),
            _post("2", "Same opening text here second post", 20),
        ]
    }
    out = psj.join(rows, posts)
    assert "status_id" not in out[0]


def test_join_whitespace_normalization():
    rows = [
        {"post_id": "p1", "text_preview": "  Lots   of\n\t whitespace  in this preview", "actual_impr": ""}
    ]
    posts = {
        "data": [
            _post("777", "Lots of whitespace in this preview and extra", 55)
        ]
    }
    out = psj.join(rows, posts)
    assert out[0]["status_id"] == "777"
    assert out[0]["actual_impr"] == 55


def test_join_does_not_mutate_input():
    row = {"post_id": "p1", "text_preview": "Some preview text", "actual_impr": ""}
    posts = {"data": [_post("1", "Some preview text longer", 3)]}
    psj.join([row], posts)
    assert row == {"post_id": "p1", "text_preview": "Some preview text", "actual_impr": ""}


def test_cli(tmp_path):
    csv_path = tmp_path / "presim.csv"
    json_path = tmp_path / "posts.json"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["post_id", "text_preview", "actual_impr"])
        w.writeheader()
        w.writerow({"post_id": "x1", "text_preview": "Fictional preview text", "actual_impr": ""})
        w.writerow({"post_id": "x2", "text_preview": "No such post anywhere", "actual_impr": ""})
    json_path.write_text(
        json.dumps({"data": [_post("12345", "Fictional preview text continued", 88)]})
    )
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(csv_path), str(json_path)],
        capture_output=True, text=True, check=True,
    )
    out = json.loads(result.stdout)
    assert out[0]["status_id"] == "12345"
    assert out[0]["actual_impr"] == 88
    assert "status_id" not in out[1]
