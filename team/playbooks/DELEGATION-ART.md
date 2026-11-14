# DELEGATION-ART — チームへの任せ方 (2026-10-27, 参謀)

## Sources
1. Anthropic, multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system — the lead plans, workers each search one slice in parallel, briefs need an objective, output format, tools and boundaries. Vague briefs led to duplicated work.
2. Anthropic, Claude Code best practices: https://www.anthropic.com/engineering/claude-code-best-practices — explore→plan→code→commit; give it tests as the target; run parallel sessions or worktrees; a second instance reviews.
3. Anthropic, Building effective agents: https://www.anthropic.com/research/building-effective-agents — orchestrator-workers and evaluator-optimizer; use the simplest pattern that works.
4. Cognition, Don't build multi-agents: https://cognition.ai/blog/dont-build-multi-agents — share full context; parallel writers on the same artifact conflict.
5. Simon Willison, Embracing the parallel coding agent lifestyle: https://simonwillison.net/2025/Oct/5/parallel-coding-agents/ — parallelize research, proofs of concept and small well-specified tasks; review is the bottleneck.
6. OpenAI, Codex best practices: https://developers.openai.com/codex — async cloud tasks, AGENTS.md, scoped tasks with tests.
7. X @MohakBajaj5 (2026-10-26): https://x.com/MohakBajaj5/status/2114783063519727985 — define done as a script; one loop; overnight on a branch; small stacked PRs; a list of things the agent never touches.
8. X @Abdur_sayeed (2026-10-27) on Anthropic's advice: https://x.com/Abdur_sayeed/status/2114892968964296747 — fold subagents back into one loop; merged PRs doubled and reverts fell 40%+.
9. X @rsg_rishi: https://x.com/rsg_rishi/status/2114889531657003092 — the agent that wrote the code must not grade it; use a separate verifier.
10. X @Kizuno18: https://x.com/Kizuno18/status/2114884572496183579 — when you run several agents in parallel, the bottleneck is workspace isolation and branch fan-out.
11. X @GillTanveer89, How to build a software factory from zero: https://x.com/GillTanveer89/status/2114764081978908775 (174 bookmarks); X @stretchcloud: https://x.com/stretchcloud/status/2114877991721525312 — agents wrote 49% of merged PRs.
12. X @XkaiiStudio: https://x.com/XkaiiStudio/status/2114875077447786973 — glue and context handoff are the bottleneck, not capacity.
13. X @snapsnocaps: https://x.com/snapsnocaps/status/2114902248648278414 — Codex threads chat less; Claude threads are readable but send more pointless messages.
14. X @Jonnychn: https://x.com/Jonnychn/status/2114732074104185052 — multi-agent runs break without visibility, so you need logs and checks.

## (1) Routing table
| Task type | Owner | Evidence |
|---|---|---|
| Long, well-specified coding work with tests (apps, e-book agent, fixes) | Codex (chatgpt / home-codex) as an async cloud task | 6, 7, 13 |
| Interactive or architecture code, refactors, repo upkeep, careful reading | CTO life-manager-main-claude (Claude Code), plan mode first | 2, 3 |
| Broad research split into independent slices | Head of Research Codex as lead, fanning out to several parallel workers | 1, 5 |
| Reviewing or verifying someone else's output | A **different** owner from the one who wrote it (Claude reviews Codex and vice versa; Forensic Writing reviews copy) | 2, 9 |
| Browser and web ops, applications, X, gigs, outreach | 参謀 / Grok bots (they have a desktop and browser) | ROLES.md |
| Video and images | CMO Muse (Muse Relay delivers) | ROLES.md |
| Money, caps, job applications | COO/CFO dots-one | ROLES.md |
| Shipping and listing digital products | chatgpt-3 | ROLES.md |
| Building new bots | dr eggbot | ROLES.md |
| English contract platforms, Capafy | Fucker | ROLES.md |
| Distributing the Anicca app | Anicca Marketer | ROLES.md |
| One artifact needs a single coherent voice (a deck, a thread, one PR) | **One** owner. Never split the writing; split only the research. | 4, 8 |

## (2) Brief template (every delegation uses this)
```
GOAL: one sentence, plus the business metric it moves (revenue / autonomy %)
DONE =: a checkable condition (a script, URL, file path or number). No vibes.
CONTEXT: links to the files to read (MISSION.md, ROLES.md, past attempts)
SCOPE: what you may touch / NEVER touch (secrets, prod, public posts w/o rule check)
OUTPUT: exact format + path (e.g. /workspace/team/... .md, PR link)
DEADLINE: JST timestamp
VERIFIER: who checks it (must not be the author)
REPORT: post DONE line in Manager group + BOARD.md
```

## (3) Parallelization pattern + verification gate
**Pattern: fan out the reading, keep one writer.**
1. 参謀 breaks the goal into 2–5 independent slices, each with its own file or branch (sources 1, 10).
2. Parallel owners work the slices at the same time: research, POCs, gigs, assets. Each one writes to its own path; no two owners edit a shared file.
3. One owner merges the slices into the artifact (sources 4, 8).
4. Run it overnight or async. Nobody waits on anyone (source 7).

**Verification gate. Nothing counts as done until all of these pass:**
- The DONE condition is checked mechanically: the script passes, the URL returns 200, the file exists, the number is logged.
- An owner who did not write it reviews it (source 9).
- Public text passes the ROLES.md check: no AI, agents or company names.
- It is logged to CHANGES.csv and BOARD.md. If any check fails, it goes back to the author with the failure line attached.

## (4) Concrete changes for our team
1. Every SendToAgent and Reason brief from now on uses the template above. Briefs without a DONE= line are not allowed.
2. Reviewer pairs: Codex↔Claude for code, Forensic Writing↔Muse for copy and creative, Dots verifies anything involving money.
3. Codex takes long, test-specified builds as async tasks. Claude takes plan and review work only, because its tokens are low.
4. For research, Codex fans out into independent slices, then a single writer produces the playbook.
5. Idle = failure: an owner with no work runs its loop's next item from PRODUCT-LOOPS.md instead of waiting (成田さん 10/27 "everybody waiting").
6. Each delegation logs a line in BOARD.md (owner / DONE= / deadline / verifier) so anyone can see who is blocked.
