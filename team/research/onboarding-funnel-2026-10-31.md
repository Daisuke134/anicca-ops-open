# Anicca iOS onboarding funnel — 2026-10-31 (written 20:40 JST)
App: Anicca / Daily Affirmations (App Store 6755129214, bundle ai.anicca.app.ios). Windows: last 14 days (2026-10-17 → 10-31) and last 24h.
Sources: PostHog (execute-sql on `events`), RevenueCat project `anicca` (projbb7b9d1b), source ~/Projects/anicca-products/aniccaios (Mac mini).

## Key finding: the onboarding steps are not in PostHog
`AnalyticsManager.track()` sends to **Mixpanel only** (AnalyticsManager.swift:58-60). Only `trackPostHog()` reaches PostHog, and it is called for just 2 events (`paywall_viewed`, `paywall_purchased` in PlanSelectionStepView). Live build is 1.9.4; PostHog has 0 of either in 14 days.
PostHog 14d contains only: `$screen` 142 (27 users), Application Opened 50 (25), Application Backgrounded 36 (14), `$identify` 11, Application Installed 11 (11 users), app_store_click 2, Application Updated 2. 24h: $screen 7 (3 users), Opened 6 (3), Backgrounded 6 (3), Installed 0.

## Per-step table (10 steps + paywall)
| # | Step (analyticsName) | Views 14d | Completed 14d | Drop-off | Time/step | 24h |
|---|---|---|---|---|---|---|
| 0 | install (`Application Installed`, PostHog) | 11 users | — | — | — | 0 |
| 0 | new customers (RevenueCat) | 54 | — | — | — | Oct 30: 11, Oct 31 (UTC, partial): 8 |
| 1 | welcome | not tracked | not tracked | n/a | not tracked | n/a |
| 2 | goal | not tracked | not tracked | n/a | not tracked | n/a |
| 3 | pain_points | not tracked | not tracked | n/a | not tracked | n/a |
| 4 | struggle_freq | not tracked | not tracked | n/a | not tracked | n/a |
| 5 | nudge_times | not tracked | not tracked | n/a | not tracked | n/a |
| 6 | processing | not tracked | not tracked | n/a | not tracked | n/a |
| 7 | plan_reveal | not tracked | not tracked | n/a | not tracked | n/a |
| 8 | comparison | not tracked | not tracked | n/a | not tracked | n/a |
| 9 | rating_prompt (proxy: `$screen`=SKStoreReview) | 6 users (23 views) | — | proxy: 5 of 11 installs (45%) never reach it | not tracked | 0 |
| 10 | notifications | not tracked | not tracked | n/a | not tracked | n/a |
| P | paywall view (PostHog `paywall_viewed`; RC paywall chart) | 0 / 0 (custom paywall, RC can't see it) | — | n/a | not tracked | 0 |
| T | trial start (RC trials_new) | 0 | — | 100% of ≥6 users reaching step 9 | — | 0 |
| $ | purchase (RC revenue transactions) | 0 ($0) | — | — | — | 0 |

Caveat: PostHog sees 11 installs vs 54 RevenueCat new customers, so PostHog coverage is partial (SDK/identify gap). Proxy rows use autocaptured screens only.

## Missing events (in PostHog) — exact list
onboarding_started, onboarding_step_advanced{step} (welcome, goal, pain_points, struggle_freq, nudge_times, processing, plan_reveal, comparison, rating_prompt, notifications), onboarding_step_back, onboarding_completed, onboarding_welcome/struggles/struggle_depth/goals/insight/valueprop/notifications_completed, tinder_pain_card_agreed/dismissed, paywall_primer_viewed, paywall_plan_selection_viewed, paywall_viewed (PostHog call exists, 0 events), trial_started, purchase_completed, onboarding_paywall_purchased, onboarding_paywall_dismissed_free, paywall_purchased.
Not instrumented anywhere: a per-step **viewed** event and **time on step** (only "advanced" exists, no duration).

## Biggest drop-off (measurable)
Paywall → trial/purchase: ≥6 users reached step 9 of 10 in 14d and 54 RC customers were new, yet 0 trials and 0 purchases. Earlier steps cannot be ranked until events reach PostHog.

## Winner reference — I am (Monkey Taps)
Paywall is a soft paywall at the end of onboarding: annual plan with **3-day free trial**, price shown as monthly equivalent, "cancel anytime in iOS Settings", plus a downsell/special offer on close. https://www.paywallpro.app/apps/406-i-am-daily-affirmations , flow: https://screensdesign.com/apps/i-am-daily-affirmations/

## Update 2026-10-31 20:30 JST — Mixpanel attempt + ASC trial status
Mixpanel per-step funnel: **not built — no Mixpanel query credential exists.** `scripts/daily-metrics/mixpanel_client.py` needs env `MIXPANEL_SERVICE_ACCOUNT` (user:secret) for the Export API; it is not set in Mac mini env, ~/.secrets, ~/.config, ~/.zshrc/.zprofile, anicca-products .env/.github, keychain (service "mixpanel"), nor /workspace/.secrets. Only hits were the iOS project token in xcconfig/Info.plist (ingest-only, cannot query) and unrelated files (a coconala browser state, old logs). Mixpanel connector is erroring. Last local Mixpanel archive: metrics_archive/2026-01-28.json (stale). Per-step views/advanced/drop-off/median time therefore remain unknown.

ASC introductory offers (app 6755129214):
| Product | State | Intro offer |
|---|---|---|
| yearly.b | APPROVED | FREE_TRIAL 3 days, all 175 territories, **start date 2026-10-30** |
| monthly.b | APPROVED | none |
| yearly.c | WAITING_FOR_REVIEW | FREE_TRIAL 1 week, start 2026-10-30 |
| weekly.c | WAITING_FOR_REVIEW | none |
| yearly.retention | APPROVED | none |
→ Before 2026-10-30 no live plan had a trial, so 0 trials in RevenueCat for most of the 14-day window is expected; only ~1.5 days carried the yearly.b trial (still 0 trials, 0 purchases).
