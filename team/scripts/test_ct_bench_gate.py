import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ct_bench_gate

HEADER = "ts_jst,probe,pass,n,na,err\n"


def write_csv(tmp_path, rows):
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "ct-bench.csv"
    lines = [HEADER.rstrip("\n")]
    for i, (passed, n, na, err) in enumerate(rows):
        lines.append(f"2026-11-{i + 1:02d}T00:00:00+09:00,p{i},{passed},{n},{na},{err}")
    path.write_text("\n".join(lines) + "\n")
    return str(path)


def run_gate(tmp_path, rows):
    return ct_bench_gate.gate(ct_bench_gate.load_rows(write_csv(tmp_path, rows)))


def test_ok_when_metrics_stable(tmp_path):
    ok, reason = run_gate(tmp_path, [(3, 3, 1, 1), (4, 4, 1, 0)])
    assert (ok, reason) == (True, "ok")


def test_fail_err_up(tmp_path):
    ok, reason = run_gate(tmp_path, [(4, 4, 1, 0), (4, 5, 1, 1)])
    assert (ok, reason) == (False, "err up")


def test_fail_pass_ratio_down(tmp_path):
    ok, reason = run_gate(tmp_path, [(4, 4, 0, 0), (4, 5, 0, 0)])
    assert (ok, reason) == (False, "pass ratio down")


def test_insufficient_rows(tmp_path):
    ok, reason = run_gate(tmp_path, [(4, 4, 1, 0)])
    assert (ok, reason) == (True, "insufficient")


def test_cli_exit_codes(tmp_path, capsys):
    ok_path = write_csv(tmp_path, [(3, 3, 1, 1), (4, 4, 1, 0)])
    fail_path = write_csv(tmp_path / "sub", [(4, 4, 1, 0), (4, 5, 1, 1)])

    assert ct_bench_gate.main([ok_path]) == 0
    assert capsys.readouterr().out.strip() == "GATE OK ok"

    assert ct_bench_gate.main([fail_path]) == 1
    assert capsys.readouterr().out.strip() == "GATE FAIL err up"
