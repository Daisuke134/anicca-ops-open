# Installs (ASC truth), weekly funnel, /open fix and 1k/day plan (2026-11-11 11:00 JST, Grok Bot executor)

## 1. Anicca (id6755129214) installs = ASC Sales reports, first-time downloads (types 1/1F/1T)
Latest report date 2026-11-09 (11/10 not published by Apple yet). Days with no row = 0.
10/13 0 · 10/14 0 · 10/15 1 · 10/16 0 · 10/17 0 · 10/18 1 · 10/19 2 · 10/20 0 · 10/21 1 · 10/22 0 · 10/23 0 · 10/24 2 · 10/25 2 · 10/26 1 · 10/27 0 · 10/28 0 · 10/29 2 · 10/30 0 · 10/31 1 · 11/01 0 · 11/02 0 · 11/03 0 · 11/04 0 · 11/05 0 · 11/06 0 · 11/07 0 · 11/08 0 · 11/09 1
- 28d (10/13-11/09): 14 first-time, 8 redownloads. 7d (11/03-11/09): 1 first-time, 6 redownloads. All-time (first sale 2025-11-28): 1,639 first-time, 274 redownloads.
- Monthly first-time: 2025-11 14 · 12 11 · 2026-01 99 · 02 409 · 03 256 · 04 533 · 05 55 · 06 93 · 07 110 · 08 6 · 09 30 · 10 22 · 11 (to 11/09) 1. Peak day 2026-03-31 = 81. Spring volume was ~90% JP; cause not verified.
- Matches Muse (team-outbox/muse/rc-batch-deletion-and-measurement-rules-2026-11-11.md): 14 in 28d, 0 on 11/7 and 11/8.

## 2. Weekly funnel 11/04-11/09 (ASC Analytics Reports in data.json; installs cross-checked with Sales reports; purchases = ASC Sales IAP rows + RC charts)
| App | Impressions | Page views | First-time DL | Trials | Paid | Proceeds | Biggest drop |
|---|---|---|---|---|---|---|---|
| Daily Affirmations - Anicca | 283 | 14 | 1 | 0 | 0 | $0 | impressions->page 4.9%, page->DL 7% |
| Daily Dhamma | 178 | 7 | 5 (Sales: 4) | 0 | 0 | $0 | impressions->page 3.9% (page->DL ~70%) |
| Honne 本音翻訳 | 130 | 2 | 0 | 0 | 0 | $0 | impressions->page 1.5%, then 0 |
| Thankful | 101 | 10 | 0 | 0 | 0 | $0 | page->DL 0/10 |
| For Better Sleep | 100 | 0 | 0 | 0 | 0 | $0 | impressions->page 0 |
| STUDIO CHERIE | not collected | - | 1 (11/07) | 0 | 0 | $0 | no analytics request |
ASC Sales has zero IAP/subscription proceeds for every app from 10/01 to 11/09 (one Honne weekly 10/08 was reversed 10/09). RC Anicca revenue 10/01-11/10 = $0, new trials 0, new paid 0.
Root problem: impressions are tiny (Anicca ~40/day). 1,000 installs/day at today's 0.35% impression->install needs ~285k impressions/day.

## 3. /open fix (live, verified 10:58 JST)
- Before: Tier 1 headline chart = "New customers per day · REVENUECAT" (includes server-created customers). Muse/dashboard routine already switched install numbers to ASC at 10:32 (874f975c).
- After (anicca-products main 3620e5aa): Tier 1 = "App installs per day · APP STORE (first-time downloads)", 60 days, per app, from open/asc-installs-daily.json (ASC Sales). Live stat: "All apps: 8 in 7d · 54 in 28d · 2,010 all-time · Anicca: 1 / 14 / 1,639 · through 2026-11-09". RC chart relabeled "NOT INSTALLS" with the backend-batch note.
- Refresh: scripts/open-startup/asc_installs_daily.py OUT.json --cache raw.json (box creds). NEEDS AN OWNER to run it daily in the /open refresh (it is a static snapshot until rerun).

## 4. Started today by me
- Created Anicca 1.9.11 in ASC (PREPARE_FOR_SUBMISSION, id 26cbce6a-1451-4c09-9402-3dcd24f89636) with ASO-PROPOSAL-ANICCA-2026-11-10 metadata, API readback verified:
  NEEDS: Codex uploads a 1.9.11 build, attaches it, submits. Baseline for revert: US 0/10 terms top-200, JP アファメーション 28-29.

## 5. Ranked plan to 1k/day (free). Basis = our data unless marked
1. Short-form video volume with App Store CTA (TikTok/IG/YT Shorts) — owner Muse (split publisher jobs live 11/11 10:05-10:20). Only free channel whose ceiling reaches 1k/day; our own TikTok posts have read 0/0 views ("first-move anomaly"), so the account state must be fixed before volume. Metric: >=1,000 views/post, ASC JP/US first-time.
2. ASO 1.9.11 keywords/subtitle — owner Codex (build) + Anicca Marketer (measure 7d/14d). Started (section 4). Basis: US invisible on all 10 terms; impressions are the main drop.
3. US ratings: 1 US rating vs 48 JP — owner Codex: SKStoreReviewController after the first affirmation "aha" moment.
4. Product page conversion for apps with views but no DL (Thankful 10->0, Honne 2->0, Sleep 0 page views) — owner Anicca Marketer: screenshots/first screenshot text, then ASC Product Page Optimization test.
5. Extra keyword indexing for US: add es-MX localization to 1.9.11 (common ASO practice, not verified for us) — owner Anicca Marketer.
6. In-App Event (free, appears in search/Today) e.g. 21-day affirmation challenge — owner Anicca Marketer.
7. X: every Anicca mention carries apps.apple.com/app/id6755129214?ct=x-diceai0-<slug> — owner X Operator (BOARD P6). Metric: ASC ct units >0.
8. Web SEO -> App Store: aniccaai.com pages that rank (Google 5/7 terms) get App Store badge + ct link — owner 参謀/Codex.
9. Reddit/communities (r/selfimprovement-style, JP communities) value posts with link — owner 参謀; low ceiling.
