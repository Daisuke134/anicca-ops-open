import os
import re
import sys
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ct_probe  # noqa: E402
import ct_probe_bench  # noqa: E402

AS = "https://apps.apple.com/app/id1?ct="
PAGES = {
    "https://a.test/ok": f'<a href="{AS}PROBE">x</a>',
    "https://a.test/bad": f'<a href="{AS}home">x</a>',
    "https://a.test/none": "<p>no links</p>",
}


def fake_fetch(url, accept=None):
    base = url.split("?")[0]
    if base == "https://a.test/down":
        raise urllib.error.URLError("down")
    return PAGES[base], base


def run(tmp_path, monkeypatch, capsys, urls):
    monkeypatch.setattr(ct_probe, "_fetch", fake_fetch)
    monkeypatch.setattr(ct_probe, "_chunk_urls", lambda u, h: [])
    f = tmp_path / "urls.txt"
    f.write_text("# c\n\n" + "\n".join(urls) + "\n")
    rc = ct_probe_bench.main([str(f), "PROBE"])
    return rc, capsys.readouterr().out.strip().splitlines()


def test_mixed(tmp_path, monkeypatch, capsys):
    rc, out = run(tmp_path, monkeypatch, capsys, list(PAGES) + ["https://a.test/down"])
    assert out[:4] == ["https://a.test/ok pass", "https://a.test/bad fail",
                       "https://a.test/none na", "https://a.test/down err"]
    assert out[-1] == "bench pass=1/2 na=1 err=1"
    assert rc == 1


def test_all_pass(tmp_path, monkeypatch, capsys):
    rc, out = run(tmp_path, monkeypatch, capsys, ["https://a.test/ok", "https://a.test/none"])
    assert out[-1] == "bench pass=1/1 na=1 err=0" and rc == 0


def test_nothing_probed_is_not_pass(tmp_path, monkeypatch, capsys):
    rc, out = run(tmp_path, monkeypatch, capsys, ["https://a.test/none"])
    assert out[-1] == "bench pass=0/0 na=1 err=0" and rc == 1


def test_usage():
    assert ct_probe_bench.main(["only-one"]) == 2


def test_csv_header_and_rows(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(ct_probe, "_fetch", fake_fetch)
    monkeypatch.setattr(ct_probe, "_chunk_urls", lambda u, h: [])
    f = tmp_path / "urls.txt"
    f.write_text("\n".join(list(PAGES) + ["https://a.test/down"]) + "\n")
    csv = tmp_path / "bench.csv"
    for _ in range(2):
        rc = ct_probe_bench.main([str(f), "PROBE", "--csv", str(csv)])
        assert rc == 1
        capsys.readouterr()
    lines = csv.read_text().splitlines()
    assert lines[0] == "ts_jst,probe,pass,n,na,err"
    assert len(lines) == 3
    for row in lines[1:]:
        ts, probe, p, n, na, err = row.split(",")
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", ts)
        assert (probe, p, n, na, err) == ("PROBE", "1", "2", "1", "1")


def test_csv_values_match_summary(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(ct_probe, "_fetch", fake_fetch)
    monkeypatch.setattr(ct_probe, "_chunk_urls", lambda u, h: [])
    f = tmp_path / "urls.txt"
    f.write_text("https://a.test/ok\nhttps://a.test/none\n")
    csv = tmp_path / "bench.csv"
    rc = ct_probe_bench.main([str(f), "PROBE", "--csv", str(csv)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "bench pass=1/1 na=1 err=0" in out
    row = csv.read_text().splitlines()[-1].split(",")
    assert row[1:] == ["PROBE", "1", "1", "1", "0"]
