# Cheap wake (high-frequency routines)
Source: https://x.com/BotDirectoryAI/status/2116668898112376838 (idea via @Kevin_Logan): "turn the top routine's repeatable steps into a script so each run costs less."
Applies to any routine that runs 4+ times a day (e.g. Dots Reason inbox relay ~672/wk, dr eggbot upwork-fresh-bids ~336/wk, inbox-sweep ~84/wk, Fucker revenue loop ~84/wk).
1. Step 0 is one cheap check (a box script, one search call, or one file mtime). Do not re-read RULES.md / long docs first.
2. If nothing new since the last run: end the turn with one line ("no new items HH:MM"). No subagents, no logs beyond that line.
3. Only when something new exists: load the runbook and do the full work. Send procedural parts to the low-effort executor or codex-run.sh.
4. Keep the "last seen" id/timestamp in a small state file so step 0 is a diff, not a re-scan.
