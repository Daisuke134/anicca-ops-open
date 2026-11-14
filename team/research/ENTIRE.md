# Entire (entire.io) — "Git forge for agent-human collaboration" (found 2026-10-27 07:2x JST)

Source: launch post by Thomas Dohmke (ex-GitHub CEO) https://x.com/ashtom/status/2114763996691562540 (2026-10-27 02:00 JST; 52k views, 321 likes, 162 bookmarks at 07:2x). Missed by the 02:3x–06:3x passes because the searches didn't cover "forge"/"agent-human collaboration"; caught via an "agent native" quote.

## What it is (entire.io, fetched 2026-10-27)
- Hosted, distributed Git-compatible forge built for agents: claims up to 418 pushes/s (vs GitHub 4.7, Cursor 65).
- "Trails" replace PRs: goal stays attached from idea to merge, agents loop until evals are green, agent reviews/evals flag findings.
- Session storage: prompts, tool calls, decisions stored with every commit; secrets redacted locally.
- Continuous memory (entire-brain + entire-graph): repo as multi-agent memory, claims up to 71% fewer tokens; agentic search over code + commits + sessions.
- Entire CLI: github.com/entireio/cli, MIT, ~5.2k stars, active (pushed 2026-10-27). Hooks into git to capture agent sessions next to commits. Works with Claude Code/Codex.

## Relevance
- Not a company-ops automation product, but agent-native infrastructure for exactly how the Reason Network ships (many Claude/Codex sessions pushing to Daisuke134/life-manager). The "why behind each commit" record is also Manager R&D material (agent memory from session history).

## Adoption decision
1. Do NOT move the forge (GitHub canonical repo + hackathon PR #8745 stay where they are).
2. Trial the MIT Entire CLI (session capture only, local, no hosted push) on the life-manager repo in one Reason session: does it record Claude/Codex sessions next to commits without slowing pushes, and does the record help the next session pick up context? Owner: main-claude-2 after the swap/CI work (low priority). Result = one line in BOARD.
3. Copy into Life Manager Cloud: keep the "intent + session log next to each action" idea for the customer-facing action log (same trust theme as Simurg/Crevio/NanoCorp).
4. Public posts: don't name Entire.
