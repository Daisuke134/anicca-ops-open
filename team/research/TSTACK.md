# tstack (t3dotgg/tstack) — 2026-10-26 18:3x JST
- What: 9 agent skills for Claude Code / Codex (MIT, created 2026-10-24): full-send, full-stop, council (3 providers review until agree), sol-loop, file-pr, takeover, babysit-pr (watch CI + review bots, fix real findings), modernize, leaving-pr-comments.
- Needs: authenticated gh, python3; council/sol-loop need a harness that can run other providers' models.
- Why us: our PRs (#8745 LM Cloud, #9029) stall for hours waiting on CI/review; babysit-pr + file-pr are exactly that gap. council fits our team (Claude + Codex + chatgpt sessions = cross-provider review instead of 0 reviews).
- Decision: ADOPT babysit-pr, file-pr, leaving-pr-comments, council. Skip full-send (no unattended merge to main without our own gate) and takeover/modernize for now.
- Owner: Codex session (#8745 owner) installs into ~/.codex/skills and ~/.claude/skills on the Mac mini, uses babysit-pr on #8745 Step3; council = Claude session reviews Codex PRs. Report via Reason to 参謀.
