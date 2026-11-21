import json, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import connect_loo_prescore as m

SCRIPT = os.path.join(os.path.dirname(__file__), "connect_loo_prescore.py")


def write(tmp_path, lines):
    p = tmp_path / "x.csv"
    p.write_text("post_id,impr\n" + "\n".join(lines) + "\n", encoding="utf-8")
    return str(p)


def run(path):
    return json.loads(subprocess.check_output([sys.executable, SCRIPT, path]))


def test_six_values(tmp_path):
    vals = [3731, 2482, 1078, 1677, 1460, 1568]
    out = run(write(tmp_path, [f"p{i},{v}" for i, v in enumerate(vals)]))
    assert out["n"] == 6
    assert out["prescore"] == 1622.5
    assert abs(out["median_loo_err"] - 0.2902) < 1e-3
    assert len(out["loo"]) == 6


def test_invalid_rows_skipped(tmp_path):
    out = run(write(tmp_path, ["a,100", "b,", "c,abc", "d,0", "e,-5", "f,nan", "g,inf", "h,300"]))
    assert out["n"] == 2
    assert out["prescore"] == 200
    assert [r["post_id"] for r in out["loo"]] == ["a", "h"]


def test_n1(tmp_path):
    out = run(write(tmp_path, ["a,100"]))
    assert (out["n"], out["prescore"], out["loo"], out["median_loo_err"]) == (1, 100.0, [], None)


def test_empty():
    o = m.score([]); assert (o["n"], o["prescore"], o["loo"], o["median_loo_err"]) == (0, None, [], None)


def test_repeated_post_id_no_leakage(tmp_path):
    out = run(write(tmp_path, ["post-a,100", "post-a,1000", "post-b,1000", "post-c,"]))
    assert out["n"] == 2
    assert out["duplicate_rows_collapsed"] == 1
    assert out["skipped_rows"] == 1
    assert sorted(r["post_id"] for r in out["loo"]) == ["post-a", "post-b"]


def test_extreme_finite_values_no_crash(tmp_path):
    out = run(write(tmp_path, ["a,1e308", "b,1e-308", "c,1"]))
    assert out["n"] == 3
    assert all(math.isfinite(r["abs_ln_err"]) for r in out["loo"])

