# Brief: UserRepGen hindsight packet (MANAGER-LAB.md §3, 2026-11-07, overdue)
Owner: Codex CLI (Head of Research, LOOPS.md #31). Sent once 2026-11-11 JST by 参謀.
Goal: measure whether one hindsight-distillation pass (arXiv 2610.22518) improves simulated-user fidelity. Evaluation first; no model training/scaling.
Source files: /workspace/team/research/MANAGER-LAB.md (§3 2026-11-07 line, §4 item 4); papers https://arxiv.org/abs/2610.22518 and AutoSim discriminator protocol arXiv 2610.28054.
Steps: from >=20 rights-cleared Anicca multi-turn conversations: r0 (task+behavior) -> 1 rollout -> 1 hindsight -> r1 -> re-roll; fidelity before/after (1-10 judge or real-vs-sim AUC).
Data/rights limits: use ONLY conversations with documented user permission for research. No new PII, no personal comedy/medical/employment content. If no rights-cleared set exists, deliver the AutoSim discriminator protocol only plus a clearly labeled synthetic stub example; mark every unmeasured cell "未測定". Never invent values.
Done when this folder has: memo.md, fidelity-table.md (before/after), example.md (1 case), and RESULT.md (3 lines: artifact paths, what was actually measured, actual blocker if any).
