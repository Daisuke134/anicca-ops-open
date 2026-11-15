import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "ct_bench_trend.py"
HEADER = "ts_jst,probe,pass,n,na,err\n"


def run(csv_path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(csv_path)],
        capture_output=True,
        text=True,
    )


def write_csv(tmp_path, rows):
    p = tmp_path / "ct-bench.csv"
    p.write_text(HEADER + "".join(rows))
    return p


def test_improve(tmp_path):
    p = write_csv(
        tmp_path,
        [
            "2026-11-14T09:00+09:00,probeA,8,10,0,1\n",
            "2026-11-15T09:00+09:00,probeA,9,10,0,0\n",
        ],
    )
    r = run(p)
    assert r.returncode == 0
    assert "last 9/10 err=0 (2026-11-15T09:00+09:00) vs prev 8/10 err=1 (2026-11-14T09:00+09:00)" in r.stdout
    assert "delta pass=+1 err=-1" in r.stdout


def test_drop(tmp_path):
    p = write_csv(
        tmp_path,
        [
            "2026-11-14T09:00+09:00,probeA,9,10,0,0\n",
            "2026-11-15T09:00+09:00,probeA,7,10,0,3\n",
        ],
    )
    r = run(p)
    assert r.returncode == 1
    assert "delta pass=-2 err=+3" in r.stdout


def test_single_row(tmp_path):
    p = write_csv(tmp_path, ["2026-11-15T09:00+09:00,probeA,5,10,0,2\n"])
    r = run(p)
    assert r.returncode == 0
    assert "last 5/10 err=2 (2026-11-15T09:00+09:00) (no prev)" in r.stdout


def test_missing_file(tmp_path):
    r = run(tmp_path / "does-not-exist.csv")
    assert r.returncode == 2


def test_empty_file(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("")
    r = run(p)
    assert r.returncode == 2
