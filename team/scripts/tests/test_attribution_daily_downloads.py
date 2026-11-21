#!/usr/bin/env python3
"""Tests for the ASC download resilience added for Issue #442.

Covers:
  * a segment download that raises SSLError twice is retried and then succeeds,
  * a segment download that keeps failing in Python falls back to curl,
  * a missing downloads cache renders First-time DL as `unknown`, never 0,
  * one failing report does not stop the other three pulls.

Run: python3 -m pytest team/scripts/tests/test_attribution_daily_downloads.py -q

No network, no ASC credentials: `requests` is a local stub and `_curl_bytes` is replaced.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import types
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "attribution-daily.py"


def load_module():
    spec = importlib.util.spec_from_file_location("attribution_daily_dl", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ad = load_module()


class _Resp:
    def __init__(self, payload=None, content=b"", status=200):
        self._payload = payload
        self.content = content
        self.status_code = status

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class _SSLStub(types.SimpleNamespace):
    """requests-like module whose segment GET fails with SSLError N times, then serves gzip TSV."""

    def __init__(self, failures: int, body: bytes):
        super().__init__(failures=failures, body=body, calls=0)
        self.get = self._get

    def _get(self, url, **kw):
        if url.startswith("https://seg.invalid"):
            self.calls += 1
            if self.calls <= self.failures:
                raise ConnectionError("SSLError: HTTPSConnectionPool(host='asp-us-west-2.s3.us-west-2.amazonaws.com')")
            return _Resp(None, self.body)
        raise AssertionError(f"unexpected URL {url}")


def _tsv() -> bytes:
    import gzip
    header = ["Date", "Event", "Source Type", "Counts", "Download Type", "Page Type", "Territory",
              "App Apple Identifier"]
    line = ["2026-11-18", "Download", "App Store search", "3", "First-time download", "No page", "US", ad.APP_ID]
    return gzip.compress(("\t".join(header) + "\n" + "\t".join(line) + "\n").encode())


def _install_requests(monkeypatch, stub):
    monkeypatch.setitem(__import__("sys").modules, "requests", stub)


def test_ssl_error_on_segment_is_retried(tmp_path, monkeypatch):
    stub = _SSLStub(failures=2, body=_tsv())
    _install_requests(monkeypatch, stub)
    monkeypatch.setattr(ad, "_backoff", lambda attempt: None)
    assert ad._get_bytes("https://seg.invalid/1", timeout=5) == _tsv()
    assert stub.calls == 3


def test_persistent_python_failure_falls_back_to_curl(tmp_path, monkeypatch):
    stub = _SSLStub(failures=99, body=_tsv())
    _install_requests(monkeypatch, stub)
    monkeypatch.setattr(ad, "_backoff", lambda attempt: None)
    called = {}

    def fake_curl(url, timeout=120):
        called["url"] = url
        return _tsv()

    monkeypatch.setattr(ad, "_curl_bytes", fake_curl)
    assert ad._get_bytes("https://seg.invalid/1", timeout=5) == _tsv()
    assert called["url"] == "https://seg.invalid/1"


def test_missing_downloads_cache_renders_unknown_not_zero(tmp_path):
    cache = tmp_path / "cache"
    cache.mkdir()
    (cache / "discovery.json").write_text(json.dumps([
        {"_proc": "2026-11-19", "Date": "2026-11-18", "Event": "Impression",
         "Source Type": "App Store search", "Counts": 7, "App Apple Identifier": ad.APP_ID},
        {"_proc": "2026-11-19", "Date": "2026-11-18", "Event": "Page view",
         "Source Type": "App Store search", "Counts": 2, "App Apple Identifier": ad.APP_ID},
    ]))
    args = argparse.Namespace(cache=str(cache), pull=False, start="2026-11-13", end="2026-11-19",
                              report_date="2026-11-21", allow_stale_write=False)
    text = ad.render_table(args)
    table = [ln for ln in text.splitlines() if ln.startswith("| 2026-11-18")][0]
    assert "| unknown |" in table, table
    total = [ln for ln in text.splitlines() if ln.startswith("| **total**")][0]
    assert "**unknown**" in total, total
    assert "no — first-time DL shown as unknown (not 0)" in text


def test_downloads_rows_still_render_counts(tmp_path):
    cache = tmp_path / "cache"
    cache.mkdir()
    proc = "_proc"
    (cache / "discovery.json").write_text(json.dumps([
        {proc: "2026-11-19", "Date": "2026-11-18", "Event": "Impression",
         "Source Type": "App Store search", "Counts": 7, "App Apple Identifier": ad.APP_ID},
    ]))
    (cache / "downloads.json").write_text(json.dumps([
        {proc: "2026-11-19", "Date": "2026-11-18", "Event": "Download", "Source Type": "App Store search",
         "Counts": 3, "Download Type": "First-time download", "Page Type": "No page", "Territory": "US",
         "App Apple Identifier": ad.APP_ID},
    ]))
    args = argparse.Namespace(cache=str(cache), pull=False, start="2026-11-13", end="2026-11-19",
                              report_date="2026-11-21", allow_stale_write=False)
    text = ad.render_table(args)
    table = [ln for ln in text.splitlines() if ln.startswith("| 2026-11-18")][0]
    assert "| 3 |" in table, table
    assert "unknown |" not in table.split("|")[5], table


def test_one_failed_report_does_not_stop_the_others(tmp_path, monkeypatch):
    cache = tmp_path / "cache"
    cache.mkdir()
    calls = []

    def fake_pull(report_id, since, dest, allow_stale=False):
        calls.append(report_id)
        if report_id == ad.STANDARD_DOWNLOADS:
            raise ConnectionError("SSLError: HTTPSConnectionPool")
        return [{"Date": "2026-11-18", "Event": "Impression", "Source Type": "App Store search", "Counts": 1,
                 "_proc": "2026-11-19", "App Apple Identifier": ad.APP_ID}]

    monkeypatch.setattr(ad, "pull_asc_report", fake_pull)
    args = argparse.Namespace(cache=str(cache), pull=True, start="2026-11-13", end="2026-11-19",
                              report_date="2026-11-21", allow_stale_write=False)
    text = ad.render_table(args)
    assert len(calls) == 4
    assert "Standard downloads cache: no" in text
    assert "| 2026-11-18 | aso_search | 1 |" in text
