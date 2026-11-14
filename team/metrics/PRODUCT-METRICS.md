# PRODUCT-METRICS — 2026-10-27 08:10 JST
Sources: PostHog project 327882 (only project; only Anicca iOS sends events), RevenueCat overview (28d). Mixpanel: not used. Benchmarks: none cited (no source fetched; not invented).

## Anicca iOS (PostHog app_name=aniccaios, RC projbb7b9d1b)
| metric | 7d | 28d |
|---|---|---|
| active users (Application Opened) | 13 | 37 |
| installs (Application Installed) | 6 | 21 |
| D1 / D7 retention (60d install cohort) | 5/54 = 9% | ~8% (4/48) |
| paywall_view → purchase | not tracked since 2026-04-14 | Apr 1–14: 147→18 (~12%) |
| RC new customers / active users | - | 44 / 67 |
| trials / active subs / MRR | 0 / 5 / $20 | revenue 28d $0 |
Top events 28d: $screen 436, Application Opened 143, Backgrounded 128, $identify 23, Installed 21.
Bottleneck: D1 retention 9% + 0 trials; funnel events missing. Fix: life-manager-main-claude (msg 01M5X6YD51NTAPTTHHS2K0H698), due 10/27 18:00.

## Honne (RC projcfa60dd8) — no analytics
| new customers 28d | active users 28d | trials | subs | MRR |
|---|---|---|---|---|
| 28 | 29 | 0 | 2 | $4 |
## Thankful (RC proj7aaf9429) — no analytics
| 9 | 9 | 0 | 0 | $0 |
## デイリー・ダンマ (RC proj86624956) — no analytics
| 14 | 20 | 0 | 0 | $0 |
## For Better Sleep (RC proj77301666 "sleep") — no analytics
| 2 | 2 | 0 | 0 | $0 |
## PDF Insight — no analytics, no RevenueCat project found
Instrumentation + paywall-at-end-of-onboarding trial fix for all five: chatgpt-3 (msg 01M5X6YH686R8RX3QXSDX84T7H), due 10/27 20:00.
Other RC projects (not in streams list, unreviewed): Chi Daily, Looksmax, EyeBreakIsland, DeskStretch, Wee, loopmind, SleepRitual, Micro Mood, affirmdaily, hooktele, FrostDip.
