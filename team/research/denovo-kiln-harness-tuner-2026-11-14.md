# P0 + tool scan — 2026-11-14 20:2x JST (参謀 X reader)

## P0: Denovo (denovo.dev) — "turns any idea into a startup that runs autonomously"
- Seen on X: https://x.com/spuliz91/status/2121238461378105440 (user claim "$250 MRR with an autonomous company running on Denovo"; 0 imp, so a self-reported claim, not verified).
- What it is (site + Product Hunt + pricing page, read this run): idea → scorecard, business plan, pitch deck, brand, promo videos, full-stack web app wired to Stripe → Engineering / Sales / Research / Marketing agents in "Auto mode" (10 verified cold emails/day, ads on Google/Meta/LinkedIn, IG/LinkedIn posts). NYC, 6 people, Denovo Operating AI LLC (Delaware). Plans: Free $0, Build $25, Launch $49, Growth $199/mo, Scale +$950 agent work/mo.
- Design choice to note: two lanes. Lane 1 autonomous (brand, deck, outreach, content, follow-ups). Lane 2 human approval gate for payments, external comms and irreversible actions ("should I do this?").
- Sources: https://www.denovo.dev/ , https://www.producthunt.com/products/denovo , https://www.denovo.dev/subscription
- Not adopted as a tool: it would run a separate company in their sandbox; we already run our own stack.

## Tool: Kiln Harness Tuner (MIT) — tunes an agent's tools, prompts, skills and model against evals
- Seen on X: https://x.com/ai_algoit/status/2121410372683096413
- Repo: https://github.com/Kiln-AI/harness-tuner (MIT, created 2026-10-30, 11 stars at read time; PyPI harness-tuner 0.5.0). Install: `uv tool install harness-tuner`.
- What it does: plans experiments, measures on train, promotes on val, never reads test; rewrites tool wrappers (smaller responses, fewer repeated calls), cuts prompt contradictions, moves long instructions into skills, tunes model/settings; supports synthetic users for multi-turn evals. Runs on Claude Code / Codex / OpenCode subscriptions; needs the free Kiln app on the same machine and provider keys; LLM calls cost money (docs/costs.md).
- Fit: this is evaluation-driven development (成田さん's order) applied to our own agents, with held-out test enforced in code. First target candidates: the @diceai0 reply writer (eval = X-WRITING-STYLE rules + reply engagement), and the behavior model eval in /workspace/bb43/behaviorbench_eval.
- Decision: adopt as a trial. Owner @codex (Reason). Cheapest first: one task, one eval set, smallest budget, report cost + before/after on held-out test.
