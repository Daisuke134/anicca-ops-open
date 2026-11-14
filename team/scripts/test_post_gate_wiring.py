#!/usr/bin/env python3
"""Proves a wired posting script calls the gate BEFORE any network call. urlopen is replaced; nothing is posted."""
import importlib.util, json, os, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import test_post_gate as T  # noqa: E402  (reuses fixture(); its CLI cases also run on import)

calls = []
def fake_urlopen(*a, **k):
    calls.append(a[0].full_url if hasattr(a[0], "full_url") else a[0]); raise RuntimeError("NETWORK BLOCKED IN TEST")
urllib.request.urlopen = fake_urlopen

spec = importlib.util.spec_from_file_location("shortform_post", os.path.join(ROOT, "team/distribution/shortform/post.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
payload = {"type": "now", "posts": [{"integration": {"id": "cmp93bkpu01uvoh0yd3aj560g"}, "value": [{"content": "x"}],
                                      "settings": {"__type": "tiktok"}}]}
results = []
def attempt(name, poster, root, want_network):
    calls.clear(); os.environ.update(ANICCA_POSTER=poster, ANICCA_SOURCE_URL=T.SRC, POST_GATE_LOCAL_ROOT=root)
    try:
        mod.req("POST", "/posts", payload); code = 0
    except SystemExit as e: code = e.code
    except RuntimeError: code = "reached-network(blocked by test)"
    ok = bool(calls) == want_network
    results.append(ok); print(f"[{'PASS' if ok else 'FAIL'}] wiring: {name}: result={code} network_calls={len(calls)}")

attempt("shortform/post.py req() as 参謀 -> @aniccaaffirmation", "参謀", T.fixture(), False)
attempt("shortform/post.py req() as muse, no claim", "muse", T.fixture(), False)
claimed = T.fixture(f"- POST-CLAIM | 2026-11-12 00:10 JST | muse | tiktok:@aniccaaffirmation | create | {T.SRC}")
import post_gate, datetime as dt
real_now = post_gate.dt.datetime
class FrozenDT(dt.datetime):
    @classmethod
    def now(cls, tz=None): return real_now(2026, 11, 12, 0, 30, tzinfo=post_gate.JST)
post_gate.dt.datetime = FrozenDT
attempt("shortform/post.py req() as muse, claimed (gate passes, request reaches fake network)", "muse", claimed, True)
print(f"\nwiring {sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) and all(T.CASES) else 1)
