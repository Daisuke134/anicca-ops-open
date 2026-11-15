import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import presim_calib as pc  # noqa: E402

CSV = """backend,pred_impr,actual_impr,text_preview
heuristic,10,40,個人開発者とつながりたい
heuristic,20,80,Let's connect with builders
heuristic,10,20,What would you build?
heuristic,10,10,plain post
heuristic,,50,missing pred
heuristic,10,0,zero actual
"""


def test_fmt():
    assert pc.fmt("繋がりたい #x") == "connect"
    assert pc.fmt("Want to CONNECT WITH you") == "connect"
    assert pc.fmt("why？") == "question"
    assert pc.fmt("hello") == "other"


def test_loo(tmp_path, capsys):
    f = tmp_path / "p.csv"
    f.write_text(CSV, encoding="utf-8")
    res = pc.evaluate(pc.load(str(f)))
    n, raw, cal = res["connect"]
    assert n == 2 and math.isclose(raw, math.log(4)) and math.isclose(cal, 0.0, abs_tol=1e-12)
    assert res["question"] == (1, math.log(2), math.log(2))  # no other rows -> factor 1
    assert res["all"][0] == 4
    assert pc.main([str(f)]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0].startswith("format n") and out[-1].startswith("all 4 ")


def test_by_backend(tmp_path):
    f = tmp_path / "p.csv"
    f.write_text(CSV, encoding="utf-8")
    assert "connect/heuristic" in pc.evaluate(pc.load(str(f), by_backend=True))
