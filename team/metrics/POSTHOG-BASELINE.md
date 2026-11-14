# PostHog Baseline — 2026-10-26 12:15 JST (read-only)

Org: `anicca` (1 org). Projects: **1** — `Default project` (id 327882, tz UTC). This is the Anicca iOS app (only $os=iOS, $app_version 1.9.4). **No Life Manager or STUDIO CHERIE project exists in PostHog.**
Windows are rolling from query time (now − 7d / now − 30d). Nothing in PostHog was created or changed.

## Active users
| metric | value |
|---|---|
| Active users last 24h | 5 |
| WAU (7d unique) | 13 |
| MAU (30d unique) | 46 |
| Avg DAU 7d / 30d | 2.3 / 3.2 |

## Top events (all events that exist in the 30d window)
| event | 7d count | 7d users | 30d count | 30d users |
|---|---|---|---|---|
| $screen | 67 | 13 | 449 | 46 |
| Application Opened | 22 | 13 | 160 | 44 |
| Application Backgrounded | 13 | 4 | 140 | 27 |
| $identify | 5 | 5 | 29 | 29 |
| Application Installed (installs/first opens) | 5 | 5 | 27 | 27 |
| Application Updated | 1 | 1 | 5 | 5 |

Only 6 event types in 30d. All-time events also include `paywall_viewed` (196 / 147 users), `paywall_dismissed` (33), `paywall_purchased` (33 / 18 users), `$feature_flag_called` (169) — **but all stopped on 2026-04-14 (UTC)**. Nothing since.

## Funnel status (last 30d)
- onboarding completed: **missing** (no event)
- paywall viewed: **0** (event last seen 2026-04-14)
- trial started: **missing** (no event ever)
- purchase/subscription: **0** in PostHog (paywall_purchased last seen 2026-04-12); revenue truth is RevenueCat.
- Screen names are SwiftUI generic (`UIHostingController<…>`), so onboarding can't be inferred. `SKStoreReview` shown to 15 users/30d.

Funnel Installed → paywall → trial → purchase **cannot be built for current data**. Historical (Apr 1–14): paywall_viewed 147 users → paywall_purchased 18 users (~12%, likely includes test buys).

## Weakest step
**Instrumentation itself**: since v1.9.x the app sends no paywall/onboarding/trial events. Fix: re-add `onboarding_completed`, `paywall_viewed`, `trial_started`, `subscription_purchased` captures (or RevenueCat→PostHog integration) and name screens via `.postHogScreenView("Name")`.
