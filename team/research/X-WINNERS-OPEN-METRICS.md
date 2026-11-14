# X winners: public live metrics (researched 2026-10-31 22:15 JST, x connector + web)

## Top 5 to copy
| # | Winner | Link | What it shows | How it stays current |
|-|-|-|-|-|
| 1 | FelixCraft / The Masinov Company (Felix, OpenClaw agent CEO; Nat Eliason chairman) | https://felixcraft.ai/dashboard | Revenue 7d / 30d / lifetime, revenue by stream (Claw Mart, Felix Craft, Polylogue, CM earnings), each stream says "Verify on TrustMRR", crypto treasury separate, "Updated <timestamp>" | Pulled live from Stripe; scope stated in one line ("Stripe transactions only, excludes crypto"). **Closest model for Anicca.** |
| 2 | TrustMRR (Marc Lou, @marclou) | https://trustmrr.com · @trust_mrr | MRR, revenue 30d, total revenue, growth 30d, profit margin, active subs; leaderboard | Read-only API key to Stripe/RevenueCat/Whop/etc.; users cannot edit numbers; hourly refresh. Bot posts each new listing on X. |
| 3 | Pieter Levels (@levelsio) open pages / open-startup movement | https://x.com/levelsio/status/2077811187157176751 | Revenue per product, published publicly, decisions posted on X | Live counters from Stripe + frequent X posts |
| 4 | Baremetrics Open Startups (via MoltSets etc.) | https://www.runsby.ai/ (MoltSets $73,543 MRR, Baremetrics) | Full SaaS dashboard: MRR, churn, LTV | Direct Stripe sync |
| 5 | The Autonomous Company (@autocompanylog) | https://x.com/autocompanylog/status/2102117554114510858 | Net worth, commercial evidence, active experiments, operating activity, **human interventions count**, public log | Updated as experiment runs |
Also: RunsBy.ai (https://www.runsby.ai/) — directory separating "Verified · own dashboard" from "Founder-reported"; only verified are summed. Anicca should get listed there + TrustMRR.

## Lessons to copy
1. Never label a number "unverified": either it comes from a provider API (verified) or it is not shown in totals. State the scope in one line instead (Felix).
2. Revenue by stream, each with its source link.
3. 7d / 30d / lifetime + "updated at" timestamp, hourly/daily auto-pull.
4. Publish costs and profit margin too (TrustMRR shows margin; almost no agent company shows costs → Anicca's differentiator).
5. Count human interventions (autocompanylog) — fits "zero-human".
6. Critique to respect (@Shpigford): MRR alone is a bad success metric → show profit, not just MRR.

## X post / article drafts (do not post; for Muse)
1. "Felix shows revenue. TrustMRR shows margin. Almost nobody running a company on AI agents shows the costs. Anicca's /open now shows all three: revenue by agent, every cost line, and profit. Ours is negative today. That's the point. aniccaai.com/open"
2. "We deleted the word 'unverified' from our open dashboard. If we can't trace a number to a receipt, Stripe, RevenueCat or the chain, that's a tracking bug, not a label. Every row now links its source."
3. Article: "What I copied from Felix, TrustMRR and levelsio to build a zero-human company's open P&L" — sections: why costs matter more than MRR; revenue stages (ordered → earned → paid out); the cost list we cut for November; daily auto-pull job.
