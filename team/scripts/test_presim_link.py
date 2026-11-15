import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import presim_link  # noqa: E402

CSV = "post_id,text_sha,text_preview\n,s1,Hello   world this is a long enough preview text ok\nqueue-x,s2,No match here\n111,s3,Hello world this is a long enough preview text ok\n"
POSTS = {"data": [{"id": "999", "text": "Hello world this is a long enough preview text ok and more"}]}


def test_link_write(tmp_path, capsys):
    c, j = tmp_path / "p.csv", tmp_path / "p.json"
    c.write_text(CSV)
    j.write_text(json.dumps(POSTS))
    assert presim_link.main([str(j), "--csv", str(c), "--write"]) == 0
    assert capsys.readouterr().out.strip() == "s1 -> 999"
    rows = list(csv.DictReader(open(c)))
    assert [r["post_id"] for r in rows] == ["999", "queue-x", "111"]


def test_dry_run_unchanged(tmp_path):
    c, j = tmp_path / "p.csv", tmp_path / "p.json"
    c.write_text(CSV)
    j.write_text(json.dumps(POSTS))
    presim_link.main([str(j), "--csv", str(c)])
    assert c.read_text() == CSV
