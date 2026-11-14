#!/usr/bin/env python3
"""Tests for post_gate (e) X duplicate gate + X Operator sole-writer owner rows. Never calls X.
Replays the two real 2026-11-13 duplicates on @diceai0 (18:47/18:48 and 21:50:15/21:50:58 JST).
Run: python3 team/scripts/test_x_dedup.py"""
import json, os, subprocess, sys, tempfile, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import test_post_gate as T  # noqa: E402  (its CLI cases run on import too)
GATE = os.path.join(HERE, "post-gate.py")
SRC = "https://x.com/levelsio/status/2120150942674780181"
NOW = "2026-11-13 21:50"
LOCK = ("How to put an affirmation on your iPhone Lock Screen (it changes every day):\n\n1. Long-press the Lock Screen "
        "→ Customize\n2. Add the Anicca widget\n3. Pick a feeling: anxious, overthinking, self-worth\n\nA new line every "
        "morning, before you unlock.\n\nhttps://t.co/J6P8M43AE5 https://t.co/aXDl5RgZBV")
OPEN = ("We publish our company numbers live.\n\nNovember so far: $31.81 revenue, $1,640.08 costs.\nMRR: $20. Goal: "
        "$10,000.\n\nThe red number is the honest part.\n\nToday we moved the page's publishing off a Mac mini at home, so "
        "it keeps updating without it. https://t.co/kXbm9pKtek")
OPEN_RETRY = OPEN.replace("kXbm9pKtek", "bHq0HmlHds")  # what the browser retry actually posted 43 s later
NEW = "Day 4 of building my affirmation app.\n\nShipped: review prompt after the first widget add."

root = T.fixture("- POST-CLAIM | 2026-11-13 21:40 JST | x-operator | x:@diceai0 | create | " + SRC + "\n"
                 "- POST-CLAIM | 2026-11-13 21:40 JST | grok-sanbo | x:@アニッチャ | create | " + SRC)
intents = os.path.join(root, "intents.jsonl")


def recent(posts, age_s=0):
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, dir=root)
    # same shape as the raw x tool output saved with write_to_file
    f.write('<x tool output>\n' + json.dumps({"data": posts, "meta": {"result_count": len(posts)}}) + "\nX reads left ...")
    f.close()
    t = time.time() - age_s; os.utime(f.name, (t, t))
    return f.name


def txt(s):
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, dir=root); f.write(s); f.close(); return f.name


def run(*args, env_extra=None):
    env = {**os.environ, "POST_GATE_LOCAL_ROOT": root, "POST_GATE_INTENTS": intents, **(env_extra or {})}
    r = subprocess.run([sys.executable, GATE, "--now", NOW, *args], capture_output=True, text=True, env=env)
    return r.returncode, (r.stdout + r.stderr).strip()


CASES = []
def case(name, want, *args, env_extra=None):
    code, out = run(*args, env_extra=env_extra)
    ok = (code == 0) == (want == "allow"); CASES.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: exit={code} -> {out[:220]}")
    return out

X = ["--platform", "x", "--account", "@diceai0", "--action", "create", "--source-url", SRC]
live_lock = [{"id": "2121178088218501270", "created_at": "2026-11-13T09:47:20.000Z", "text": LOCK}]
live_open = [{"id": "2121224120276799878", "created_at": "2026-11-13T12:50:15.000Z", "text": OPEN}]

# owner: X Operator is the only @diceai0 writer now
case("参謀 (grok-sanbo) posts on @diceai0 -> refused, queue instead", "refuse", "--poster", "grok-sanbo", *X,
     "--text-file", txt(NEW), "--recent-json", recent([]))
case("X Operator, new text, fresh empty read-back -> allowed", "allow", "--poster", "X Operator", *X,
     "--text-file", txt(NEW), "--recent-json", recent(live_lock))
case("X Operator, no --recent-json -> refused (fail closed)", "refuse", "--poster", "x-operator", *X,
     "--text-file", txt(NEW), "--recent-json", "")
case("X Operator, stale read-back (15 min old) -> refused", "refuse", "--poster", "x-operator", *X,
     "--text-file", txt(NEW), "--recent-json", recent([], age_s=900))
# replay incident 1: lock-screen how-to, the retry 41 s later
case("Incident 18:48: same how-to already live -> refused", "refuse", "--poster", "x-operator", *X,
     "--text-file", txt(LOCK), "--recent-json", recent(live_lock))
# replay incident 2: same text, different t.co link
case("Incident 21:50:58: same 'company numbers' text, new t.co -> refused", "refuse", "--poster", "x-operator", *X,
     "--text-file", txt(OPEN_RETRY), "--recent-json", recent(live_open))
case("Near-same (one word edited) -> refused", "refuse", "--poster", "x-operator", *X,
     "--text-file", txt(OPEN.replace("honest part", "honest bit")), "--recent-json", recent(live_open))
# uncertain submit: first attempt recorded, post not visible yet in an immediate read-back
case("Uncertain submit: attempt 1 recorded", "allow", "--poster", "x-operator", *X, "--record-intent",
     "--text-file", txt(OPEN), "--recent-json", recent([]))
case("Uncertain submit: retry right away with an empty read-back -> refused (wait + read back)", "refuse",
     "--poster", "x-operator", *X, "--text-file", txt(OPEN), "--recent-json", recent([]))
# a read-back taken >= 3 min after the attempt that still lacks the post -> a real retry is allowed
rb = recent([])
later = time.time() + 400; os.utime(rb, (later, later))
case("Uncertain submit: read-back 6+ min later, still not live -> retry allowed", "allow", "--poster", "x-operator", *X,
     "--text-file", txt(OPEN), "--recent-json", rb, env_extra={"POST_GATE_IGNORE_MTIME": "1"})
# other accounts are untouched
case("@アニッチャ stays grok-sanbo; new text -> allowed", "allow", "--poster", "grok-sanbo", "--platform", "x",
     "--account", "@アニッチャ", "--action", "create", "--source-url", SRC, "--text-file", txt(NEW), "--recent-json", recent([]))

print(f"\nx-dedup {sum(CASES)}/{len(CASES)} passed")
sys.exit(0 if all(CASES) and all(T.CASES) else 1)
