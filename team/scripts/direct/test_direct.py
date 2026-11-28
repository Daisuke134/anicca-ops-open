"""Smoke tests for the free direct posting scripts (no network)."""
import importlib.util, json, os, py_compile
HERE = os.path.dirname(os.path.abspath(__file__))

def test_compile_all():
    for f in os.listdir(HERE):
        if f.endswith(".py"):
            py_compile.compile(os.path.join(HERE, f), doraise=True)

def test_queue_valid():
    q = json.load(open(os.path.join(HERE, "..", "..", "distribution", "direct-queue.json")))
    for i in q["items"]:
        assert i["source_url"].startswith("https://")
        assert i["status"] in ("queued", "posted", "failed", "skipped_stale")
