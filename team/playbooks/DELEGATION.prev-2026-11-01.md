# DELEGATION playbook (team-wide, copied from winners, 2026-11-01)
Full research + sources: research/ORCHESTRATOR-ROLE-2026-11-01.md

## Rules (each copied from a named source)
1. The bot 成田さん talks to (参謀) holds no hands-on loops: it splits work, assigns, integrates, decides and escalates. Sources: Anthropic multi-agent research system; Paperclip delegation guide; @ryangrowthh Chief of Staff article; @0xGhostyx (Lauren Tan's chief of staff "never does the work itself").
2. One bot = one job. Two roles in one bot lowers quality. Sources: @ryangrowthh; @0xCarnagee (Grok Bot docs: "narrow bots beat one do-everything bot").
3. One owner per stage; parallel handoffs on the same task create duplicates. Don't split a single task across agents in parallel. Sources: @0xGhostyx; Cognition "Don't Build Multi-Agents".
4. Handing off a loop = give the owner the runbook path in team/runbooks/. Owner runs first pass, logs it; only then the old owner stops its copy and updates LOOPS.md + ACCOUNT-OWNERS.md.
5. Cost: hourly routines can burn a week of usage in a day. Inside each loop, fixed steps (fetching, inbox checks, logging) go to a cheap worker; skip passes when nothing changed; report only on change. Sources: @0xGhostyx; @taylorhbuilds (orchestrators burn the most tokens).
6. Interrupt the human at most a few times a day; otherwise one summary. Source: @agent_isho.
7. Measure for 1 week after each handoff (applications, impressions, revenue vs usage); roll back if worse, change one thing at a time. Source: Anthropic 2026-10-22.

## Goal
Same or more total output on a cheaper plan (Ultra trial → Super if output holds).
