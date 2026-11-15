#!/usr/bin/env python3
"""X scout dedupe: print only URLs/post-ids not already in X-SCOUT-LOG.md.
Usage: echo "<url or id per line>" | python3 team/scripts/xscout_new.py
Script-first practice (https://x.com/Texas_Twins_Dad/status/2121773869694333328):
repeat steps run as a script instead of re-reasoning each run."""
import re, sys, pathlib
log = pathlib.Path(__file__).resolve().parent.parent / "playbooks" / "X-SCOUT-LOG.md"
seen = set(re.findall(r"status/(\d+)", log.read_text())) if log.exists() else set()
for line in sys.stdin:
    m = re.search(r"(\d{15,})", line)
    if m and m.group(1) not in seen:
        print(line.strip()); seen.add(m.group(1))
