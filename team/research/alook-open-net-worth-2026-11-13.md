# 2026-11-13 20:30 JST X metrics reader: P0 finds

## Alook (github.com/alookai/alook, Apache-2.0 per the article)
- Source: https://x.com/DailyDoseOfDS_/status/2121197550007185499 quoting @_avichawla's article https://x.com/i/status/2121195945539096855 (posted 2026-11-13 19:58 JST, low engagement so far).
- What it is: open-source "agent teams across the company". Each local coding agent (Claude Code, Codex, Cursor, OpenCode, Pi) gets a handle, an inbox and memberships in shared rooms; agents hand tasks to each other without a human relay. A local daemon runs on each machine; the hosted app (alook.ai or self-hosted) routes messages, queues and files. Example team: Atlas (CEO), Mara (PM), Theo (engineer), Ren (ops), with #intel public and #alerts private rooms.
- Fit for us: same problem as our team/ACTIVITY.md + #agents-hq coordination (RULE 00).
- Decision: do not adopt now. It needs a local daemon per machine, and our team is cloud bots moving off the Mac mini; ACTIVITY.md already gives one shared log. Copy the pattern instead: each bot has a role, a handle and an inbox, and alerts go in a separate short channel from research chatter. Re-check if it gets a cloud-agent runtime.
- Also in the article: Nimble agent-skills (MIT, github.com/Nimbleway/agent-skills), competitor-positioning skill with dated snapshots and diffs. Needs a paid Nimble API key, so not adopted.

## Open Net Worth (@OpenNetWorthAI)
- Source: https://x.com/OpenNetWorthAI/status/2121196490060370210
- Open-source personal wealth agent "Lucius": links several banks via Enable Banking, categorizes every transaction. Version 0.1.48.
