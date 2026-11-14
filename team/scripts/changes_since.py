#!/usr/bin/env python3
"""Print CHANGES.md lines added since this agent's last check (no LLM needed). Usage: changes_since.py <agent> [--peek]
Exit 0 always; prints nothing if no new lines. Cursor stored in team/state/changes-cursor/<agent>."""
import sys,os,re
F="/workspace/team/CHANGES.md"; D="/workspace/team/state/changes-cursor"
a=re.sub(r"\W","_",sys.argv[1] if len(sys.argv)>1 else "anon"); os.makedirs(D,exist_ok=True); c=f"{D}/{a}"
L=[l.rstrip("\n") for l in open(F,encoding="utf-8") if re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d JST \|",l)]
seen=set(open(c,encoding="utf-8").read().splitlines()) if os.path.exists(c) else set()
for l in L:
    if l not in seen: print(l)
if "--peek" not in sys.argv: open(c,"w",encoding="utf-8").write("\n".join(L)+"\n")
