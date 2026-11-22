import json, math, os, statistics, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import connect_loo_prescore as m

SCRIPT = os.path.join(os.path.dirname(__file__), "connect_loo_prescore.py")


def write(tmp_path, lines, header="post_id,impr"):
    p = tmp_path / "x.csv"
    p.write_text(header + "\n" + "\n".join(lines) + "\n", encoding="utf-8")
    return str(p)


def run(path, *extra):
    return json.loads(subprocess.check_output([sys.executable, SCRIPT, path, *extra]))


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


def test_by_segment(tmp_path):
    lines = ["a,100,first", "b,200,first", "c,400,first",
             "d,1000,repeat", "e,2000,repeat",
             "f,5000,solo"]
    out = run(write(tmp_path, lines, "post_id,impr,segment"), "--by-segment")
    assert out["n"] == 6
    loo = {r["post_id"]: r for r in out["loo"]}
    # within-segment LOO predictions
    assert loo["a"]["pred"] == 300    # median(200, 400)
    assert loo["b"]["pred"] == 250    # median(100, 400)
    assert loo["c"]["pred"] == 150    # median(100, 200)
    assert loo["d"]["pred"] == 2000
    assert loo["e"]["pred"] == 1000
    # 1-post segment falls back to all rows: median(100,200,400,1000,2000) = 400
    assert loo["f"]["pred"] == 400
    assert loo["f"]["fallback"] is True
    assert all(loo[p]["fallback"] is False for p in "abcde")
    # per-segment medians and overall
    assert out["segments"]["first"]["n"] == 3
    assert out["segments"]["repeat"]["n"] == 2
    assert out["segments"]["solo"]["n"] == 1
    first_errs = [abs(math.log(v) - math.log(p)) for v, p in
                  zip([100, 200, 400], [300, 250, 150])]
    assert out["segments"]["first"]["median_loo_err"] == statistics.median(first_errs)
    repeat_errs = [abs(math.log(v) - math.log(p)) for v, p in zip([1000, 2000], [2000, 1000])]
    assert out["segments"]["repeat"]["median_loo_err"] == statistics.median(repeat_errs)
    assert out["median_loo_err"] == statistics.median([r["abs_ln_err"] for r in out["loo"]])


def test_last3(tmp_path):
    lines = ["a,100,first", "b,200,first", "c,400,first", "d,800,first", "e,1600,first",
             "f,1000,second", "g,3000,second"]
    path = write(tmp_path, lines, "post_id,impr,segment")

    # --last alone: previous 3 posts in CSV order, else fall back to all other rows
    plain = {r["post_id"]: r for r in run(path, "--last", "3")["loo"]}
    assert plain["d"]["pred"] == 200       # median(100, 200, 400)
    assert plain["e"]["pred"] == 400       # median(200, 400, 800)
    assert plain["f"]["pred"] == 800       # median(400, 800, 1600)
    assert plain["g"]["pred"] == 1000      # median(800, 1600, 1000)
    assert plain["a"]["pred"] == 900       # fallback: median(200,400,800,1000,1600,3000)
    assert plain["a"]["fallback"] is True
    assert plain["d"]["fallback"] is False

    # --last with --by-segment: previous 3 posts in the same segment
    seg = {r["post_id"]: r for r in run(path, "--by-segment", "--last", "3")["loo"]}
    assert seg["d"]["pred"] == 200         # median(100, 200, 400) in "first"
    assert seg["e"]["pred"] == 400         # median(200, 400, 800) in "first"
    assert seg["f"]["pred"] == 600         # 0 earlier in "second" -> all rows except f
    assert seg["g"]["pred"] == 600         # 1 earlier (< 3) -> all rows except g
    assert seg["f"]["fallback"] is True
    assert seg["g"]["fallback"] is True


def test_by_segment_without_flag_is_old(tmp_path):
    lines = ["a,100,first", "b,200,repeat"]
    path = write(tmp_path, lines, "post_id,impr,segment")
    plain = run(path)
    assert "segments" not in plain
    assert all("fallback" not in r for r in plain["loo"])
    assert run(path, "--by-segment")["segments"]  # flag does add segments when column exists


def test_missing_segment_column_old_output(tmp_path):
    path = write(tmp_path, ["a,100", "b,200", "c,400"])
    assert run(path, "--by-segment") == run(path)

