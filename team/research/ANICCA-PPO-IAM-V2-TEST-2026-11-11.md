# Anicca PPO — treatment-iam-v2 (I am layout, pixel-matched) · test file

Written 2026-11-11 20:40 JST, Grok Bot executor. Rules: `team/playbooks/AB-TEST-RULES.md` (this file only adds hypothesis, IDs, dates).

## Why
Last 7 days (ASC, 11/03–11/09): 302 impressions → 15 product page views → 1 first-time download. Owner rule (成田さん): copy the niche winner I am's screenshots exactly (canvas, font weight/size, positions, margins, uniform across slides, measured in px); only our own brand, screens and wording.

## Assets (already built and verified earlier today — not rebuilt)
- 8 slides en-US, APP_IPHONE_67 1320×2868 (6.9", committed): `marketing/anicca/aso/treatment-iam-v2/en-US/APP_IPHONE_67/01–08_en-US.png`
- Also APP_IPHONE_65 1242×2688 on the box: `/workspace/anicca-aso/treatment-iam-v2/en-US/APP_IPHONE_65/`
- Spec measured from I am live listing: `team/research/IAM-LAYOUT-SPEC-v2.md`, `iam-layout-spec.json`. Generator `team/shared/grok-bot/render_v2.py` (ParthJadhav/app-store-screenshots was evaluated; it is an interactive Next.js editor with no headless px-exact render, so one PIL template reads one spec for all slides).
- Verification PASS: frame/bezel 0–1 px, baselines/x-height/stem ≤2 px vs I am, spread across 8 slides ≤2 px; `asc screenshots validate --device-type IPHONE_67` 8/8 ok (re-run 20:35 JST). Side-by-side: `team/research/ANICCA-VS-IAM-FIRST3-v2.jpg`.
- Not copied: I am logo, illustrations, affirmation text, headline wording.

## Live state (read 2026-11-11 20:30 JST via ascx.sh)
| Item | ID | State |
|---|---|---|
| Current PPO "Lock Screen first screenshot Nov 2026" | `d7ffa0d7-704c-42ef-abf8-588f3bada53e` (treatment `a5376aa3…`) | WAITING_FOR_REVIEW, not started, 50% traffic |
| Its review submission (also carries In-App Event 6833274397 + 2 CPPs) | `6770a9b5-5dc1-407b-be9f-15bc63b819b9` | WAITING_FOR_REVIEW since 11:45 JST |
| v2 experiment | — | **Not creatable now.** `experiments create` → Apple: "Cannot create new experiment because another experiment is in review" (20:3x JST) |

Not done on purpose: cancelling submission 6770a9b5 to add v2 as a 2nd arm of d7ffa0d7. That would push the In-App Event (starts 2026-11-14 00:00 JST) and both CPPs to the back of the review queue, and a 3-arm split of ~300 impressions/week is even less able to reach 90%.

## Launch (one command)
`bash team/scripts/launch-iam-v2-ppo.sh status|start-d7|stop-d7|launch`
- `launch` refuses (exit 3) while any other experiment is not STOPPED/COMPLETED/REJECTED; then creates the experiment (50%), treatment, en-US localization, syncs the 8 shots (replacing Apple's auto-copied control shots), creates a review submission with only the experiment and submits it.
- Guard tested 20:3x JST (exit 3 BLOCKED on d7ffa0d7). Steps after the guard are not yet executed against ASC — first real run must read back the screenshot set (8 × 1320×2868, COMPLETE) before trusting it.
- After Apple approves any PPO it must be **started** (`start-d7`, or `experiments update --v2 --started true` for v2). Nobody starting it = the test never runs.

## Hypothesis (1 variable = layout/type system of all 8 slides)
Pixel-matching I am's layout lifts conversion (first-time downloads ÷ unique impressions, as shown in ASC PPO) vs the current control.

## Done condition (closes on exactly one)
Timeline:
1. d7ffa0d7: run `start-d7` the day Apple approves (expected 11/12–11/13 JST). Close it per AB-TEST-RULES at start+14 days, **no later than 2026-11-27 JST**. Log result (impressions, CVR, ASC confidence, verdict) here and in TEAM-FEED.
2. Same day d7ffa0d7 closes: run `launch` for v2. Expected start after review ≈ 2026-11-29 JST.
3. v2 verdict:
   - **Winner**: ASC shows treatment better at ≥90% confidence after ≥7 days → apply v2 as default screenshots in the next version (en-US 6.9" and 6.5"), then start the next backlog test.
   - **Loser**: control better at ≥90% → stop, keep control.
   - **Inconclusive**: <90% at start+14 days (**deadline 2026-12-13 JST**, if started 11/29) → stop, log `inconclusive`. Because the owner rule is to adopt the winner's layout, inconclusive = ship v2 as default anyway (cost is equal, v2 matches the winner); log it as "adopted on rule, not on data".
- Measurement dates: first read 7 days after v2 start (≈ 2026-12-06 JST), verdict 2026-12-13 JST. ASC data lags ~1–2 days.

## Honest power note
At ~300 impressions/week and ~1 download/week, neither test is likely to reach 90% in 14 days. The real install lever is impressions (ASO keywords in 1.9.11, In-App Event, short video, links with ct=). Screenshots matter mainly because they also show in search results.

## Content gap seen (not fixed here, owner rule = layout only)
Slides 1–3 of v2 use three near-identical card screens on the same green hills background; I am's first 3 show three different features (lock screen, card, widgets). Next iteration: use real, different Anicca screens (lock-screen widget, theme sheet, share image) in slots 1–3.
