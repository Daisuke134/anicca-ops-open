# NanoCorp — "Autonomous companies run by AI" (found 2026-10-27 00:3x JST, X reader)
- Source: https://x.com/plbiojout/status/2114741593454330031 (founder Pierre-Louis Biojout, 15:31 UTC 10/26, 83 views at find time). Site https://www.nanocorp.so, changelog https://www.nanocorp.so/whats-new/v4-0-0 (V4 shipped 2026-10-23). YC page lists it (W24 company page, founder ex-phospho CTO).
- What it is: closed SaaS. One prompt -> an agent builds and runs an online business (site, offer, checkout, marketing, routine ops) on a daily schedule, paid in credits, Founder plan subscription.
- V4 "Goals": the agent proposes a goal as a card (result, how it will check it, limits, credits it may use); owner approves/edits/declines; each approved goal runs in its own conversation; a Goals tab shows working/done/waiting. Tasks renamed Routines. One sidebar for multiple businesses. Paid-tool failures are explained to the agent so it doesn't repeat the call. Failed renewal = 7-day grace while agent keeps working.
- Benchmark launch post: "gave agents $500 cash to run a business; after 30 days avg $2,818 cash, $15.84 inference per shop" — simulated shops (inspired by Andon Labs Vending-Bench), simulated dollars, 4 scenarios, methodology in thread. Same shape as Naïve's "$300 + 3 accounts -> cash after 30 days".
- Open source / license: none.
- Why it matters: direct competitor to Life Manager Cloud (company side) and the clearest winner in "autonomous company" (YC-backed, public changelog weekly, public benchmark). Copy target.
- Adoption decision (copy, no product adoption):
  1. Life Manager Cloud: a "goal card" object = result + how the manager checks it + limits + budget; each goal runs as its own thread; a Goals view with working/done/waiting. Fits our agent-driven (not fixed-cron) design: goals replace brittle scripts. Default stays act-alone (no human in the loop), card is for visibility, not approval.
  2. Our own public number: run a "$X start -> cash after 30 days" scoreboard on our real businesses (real dollars, not simulated) and post it as build-in-public; real money beats their simulated dollars.
  3. Weekly public changelog page for Life Manager (their "one post a week, RSS").
- Owner: Life Manager Cloud loop (main-claude-2 / Codex on PR #8745) via BOARD.md; item 2 = X build-in-public routine.
