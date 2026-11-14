#!/usr/bin/env python3
"""Dry-run tests for post_gate.py. Never calls Postiz. Run: python3 team/scripts/test_post_gate.py"""
import json, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
GATE = os.path.join(HERE, "post-gate.py")
NOW = "2026-11-12 00:30"
SRC = "https://www.tiktok.com/@winner_example_real/video/7300000000000000000"


def fixture(extra_claims=""):
    d = tempfile.mkdtemp(prefix="postgate-")
    for p in ["team/ACCOUNT-OWNERS.md", "team/CLAIMS.md", "team/distribution/shortform/marketing-destinations.json",
              "team/lm-compat/lm/config/marketing-destinations.json"]:
        os.makedirs(os.path.dirname(os.path.join(d, p)), exist_ok=True)
        shutil.copy(os.path.join(ROOT, p), os.path.join(d, p))
    with open(os.path.join(d, "team/CLAIMS.md"), "a") as f:
        f.write("\n" + extra_claims + "\n")
    return d


def run(root, *args):
    env = {**os.environ, "POST_GATE_LOCAL_ROOT": root}
    r = subprocess.run([sys.executable, GATE, "--now", NOW, *args], capture_output=True, text=True, env=env)
    return r.returncode, (r.stdout + r.stderr).strip()


CASES = []
def case(name, want, root, *args):
    code, out = run(root, *args)
    ok = (code == 0) == (want == "allow")
    CASES.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: exit={code} -> {out}")

base = fixture()
case("参謀 -> tiktok @aniccaaffirmation (the 11/11 incident)", "refuse", base,
     "--poster", "参謀", "--platform", "tiktok", "--account", "@aniccaaffirmation", "--action", "create", "--source-url", SRC)
case("参謀 cancels Muse's scheduled post on @aniccaen2", "refuse", base,
     "--poster", "grok-sanbo", "--platform", "tiktok", "--account", "@aniccaen2", "--action", "delete", "--source-url", SRC)
case("Muse, no claim -> @honne_reveal", "refuse", base,
     "--poster", "muse", "--platform", "tiktok", "--account", "@honne_reveal", "--action", "create", "--source-url", SRC)

claimed = fixture(f"- POST-CLAIM | 2026-11-12 00:10 JST | muse | tiktok:@honne_reveal | create | {SRC}\n"
                  f"- POST-CLAIM | 2026-11-12 00:12 JST | muse | tiktok:@aniccaaffirmation | create | {SRC}")
case("Muse, claimed 20 min ago, owner, winner URL, no hold -> @honne_reveal", "allow", claimed,
     "--poster", "muse", "--platform", "tiktok", "--account", "@honne_reveal", "--action", "create", "--source-url", SRC)
case("Muse, claimed, but no winner URL", "refuse", claimed,
     "--poster", "muse", "--platform", "tiktok", "--account", "@honne_reveal", "--action", "create", "--source-url", "")
case("Muse, claimed, owner post on @aniccaaffirmation (muse_only hold exempts Muse)", "allow", claimed,
     "--poster", "muse", "--platform", "tiktok", "--account", "@aniccaaffirmation", "--action", "create", "--source-url", SRC)
held = fixture(f"- POST-CLAIM | 2026-11-12 00:10 JST | muse | tiktok:@anicca.daily | create | {SRC}")
case("Muse, claimed, but @anicca.daily has a hard hold (not_retained_for_recovery)", "refuse", held,
     "--poster", "muse", "--platform", "tiktok", "--account", "@anicca.daily", "--action", "create", "--source-url", SRC)
case("参謀 claims Muse's account in CLAIMS.md anyway -> still refused (owner check)", "refuse",
     fixture(f"- POST-CLAIM | 2026-11-12 00:10 JST | grok-sanbo | tiktok:@aniccaaffirmation | create | {SRC}"),
     "--poster", "grok-sanbo", "--platform", "tiktok", "--account", "@aniccaaffirmation", "--action", "create", "--source-url", SRC)

stale = fixture(f"- POST-CLAIM | 2026-11-11 23:00 JST | muse | tiktok:@honne_reveal | create | {SRC}")
case("Muse, claim 90 min old", "refuse", stale,
     "--poster", "muse", "--platform", "tiktok", "--account", "@honne_reveal", "--action", "create", "--source-url", SRC)

conflict = fixture(f"- POST-CLAIM | 2026-11-12 00:10 JST | muse | tiktok:@honne_reveal | create | {SRC}\n"
                   f"- POST-CLAIM | 2026-11-12 00:15 JST | codex | tiktok:@honne_reveal | create | {SRC}")
case("Muse claimed, but Codex holds an open claim on same account", "refuse", conflict,
     "--poster", "muse", "--platform", "tiktok", "--account", "@honne_reveal", "--action", "create", "--source-url", SRC)
released = fixture(f"- POST-CLAIM | 2026-11-12 00:10 JST | muse | tiktok:@honne_reveal | create | {SRC}\n"
                   f"- POST-CLAIM | 2026-11-12 00:15 JST | codex | tiktok:@honne_reveal | create | {SRC}\n"
                   f"- POST-RELEASE | 2026-11-12 00:20 JST | codex | tiktok:@honne_reveal")
case("Codex released its claim -> Muse allowed", "allow", released,
     "--poster", "muse", "--platform", "tiktok", "--account", "@honne_reveal", "--action", "create", "--source-url", SRC)

# Postiz payload path (what the wired scripts use): integration id -> account
pl = os.path.join(base, "payload.json")
json.dump({"type": "schedule", "posts": [{"integration": {"id": "cmp93bkpu01uvoh0yd3aj560g"},
                                          "value": [{"content": "x"}], "settings": {"__type": "tiktok"}}]}, open(pl, "w"))
case("Postiz payload: 参謀 schedules to @aniccaaffirmation integration", "refuse", base,
     "--poster", "参謀", "--postiz-payload", pl, "--action", "schedule", "--source-url", SRC)
pl2 = os.path.join(claimed, "payload.json")
json.dump({"type": "schedule", "posts": [{"integration": {"id": "cmoig11ew001zlv0yk6vqo1us"},
                                          "value": [{"content": "x"}], "settings": {"__type": "tiktok"}}]}, open(pl2, "w"))
case("Postiz payload: Muse, claimed, @honne_reveal integration", "allow", claimed,
     "--poster", "muse", "--postiz-payload", pl2, "--action", "schedule", "--source-url", SRC)
pl3 = os.path.join(claimed, "payload3.json")
json.dump({"type": "now", "posts": [{"integration": {"id": "cmUNKNOWN000"}, "value": [{"content": "x"}],
                                     "settings": {"__type": "tiktok"}}]}, open(pl3, "w"))
case("Postiz payload: unmapped integration id", "refuse", claimed,
     "--poster", "muse", "--postiz-payload", pl3, "--action", "create", "--source-url", SRC)

print(f"\n{sum(CASES)}/{len(CASES)} passed")
if __name__ == "__main__":
    sys.exit(0 if all(CASES) else 1)
