# iOS product-loop audit — 2026-10-31 (read-only)
Sources: ASC API (/v1/apps, subscriptionGroups, prices filtered USA/JPN, effective ≤ 2026-10-31) pulled 10:00 JST; RevenueCat get-overview-metrics (MRR = 28-day); Mac mini source grep (~/anicca-project). Nothing was changed.
pricing-2026-10-31.md: **does not exist yet**, so there's no comparison against it.

## Totals
RevenueCat: Anicca 5 active subscriptions / MRR $20; Honne 2 / $4; sleep, Thankful, dhamma 0. Active trials = 0 in every project checked. Total 7 subscriptions / ~$24 MRR. I did not query the other RC projects; the ASC state below suggests they're not on sale.

## Per-app table
| App | Store state of subs | Plans (USD / JPY) | Active subs / MRR (RC) | Onboarding | Paywall (code) | Top competitor (source) | Gap |
|---|---|---|---|---|---|---|---|
| Daily Affirmations – Anicca (ai.anicca.app.ios) | yearly.b, monthly.b, yearly.retention APPROVED; annual $59.99, monthly $12.99, weekly.b removed from sale; lifetime IAP exists | yr $29.99/¥5000, mo $9.99/¥1500, retention yr $22.49/¥3500 | 5 / $20; 0 trials; 78 new customers/28d | 10 steps (welcome→goal→pain→freq→nudge→processing→plan reveal→comparison→rating→notifications) | Primer + plan selection after onboarding. Default is **soft** (xmark/skip). Hard only when the PostHog flag `paywall-ab-test` payload says so (PlanSelectionStepView.swift:35) | I am (Monkey Taps): yr $59.99–69.99 with 3-day trial, mo $9.99–14.99, lifetime $149.99, no weekly; ~$400–700K/mo est. https://apps.apple.com/us/app/i-am-daily-affirmations/id874656917 , https://apppricer.com/app/874656917 , https://adapty.io/paywall-library/i-am-daily-affirmations/ | Annual at half the leader's price; no trial (0 active trials); paywall soft by default |
| Honne (app.rork.hon-ne-honyaku-ai) | APPROVED | yr $39.99/¥6000, mo $14.99/JPY unknown, wk $7.99/¥1300 | 2 / $4; 25 new/28d | source not found on Mac mini | unknown | unknown (not researched) | source location unknown |
| Aura Looks (app.rork.kqa4…) | READY_TO_SUBMIT (in resubmission) | yr $59.99/¥10000, retention yr $44.99/¥7000, wk $7.99/¥1300 | RC project "Looksmax": not queried | OnboardingFlow present | PaywallView with xmark → soft; Apple 2.1b asked for a way to reopen the paywall; nothing gated (see earlier report) | Umax: wk $3.99–9.99, mo $9.99–24.99; 6-step onboarding (selfies), results blurred until pay or invite 3 friends; ~$65–150K/mo. https://apps.apple.com/us/app/umax-become-hot/id6471026798 , https://screensdesign.com/showcase/umax-become-hot , https://toomanypaywalls.com/app/umax | No real gated value (Umax gates the result itself) |
| For Better Sleep – Sleep Reset | APPROVED | wk $7.99/¥1300, yr $39.99/¥6000 | 0 / $0; 3 new/28d | source not found | unknown | BetterSleep: yr $59.99 (std), wk $9.99, lifetime $249.99, 7-day trial on yearly. https://apps.apple.com/us/app/bettersleep-relax-and-sleep/id314498713 , https://www.bettersleep.com/blog/sleep-cycle-vs-bettersleep-2026-honest-sleep-app-comparison | Traffic (3 users/28d) is the binding issue, not price |
| Thankful – Gratitude Journal | APPROVED | yr $29.99/¥5000, mo $4.99/¥800 | 0 / $0; 8 new/28d | OnboardingView | PaywallView, skip + xmark → soft | unknown | no weekly; soft; low traffic |
| Dhamma Quotes (com.dailydhamma.app, Expo) | APPROVED | yr $19.99/¥3000, mo $4.99/¥800 | 0 / $0; 14 new/28d | has skip | unknown (RN, not inspected) | unknown | lowest annual of the portfolio |
| STUDIO CHERIE | APPROVED | mo $0.99/¥210 | not queried | not found | unknown | unknown | $0.99/mo price |
| FrostDip | **no subscription products in ASC** | none | 0 (RC proj exists) | Welcome→Experience→Notifications | soft ("Maybe Later", xmark) | unknown | can't earn: no products |
| Zone2Daily | READY_TO_SUBMIT | yr $29.99/¥5000, mo $4.99/¥800, wk $1.99/¥300 | not live | Explainer→Age→Notifications | soft ("Maybe Later") | unknown | weekly $1.99 vs $7.99 used elsewhere |
| Eye Break | READY_TO_SUBMIT | yr $29.99, mo $4.99, wk $1.99 | not live | OnboardingPage | no skip/xmark found → possibly hard (unverified) | unknown | weekly $1.99 |
| Chi Daily | READY_TO_SUBMIT (on hold, 4.2) | yr $34.99/¥6000, mo $4.99/¥800 | not live | 3 screens | soft ("Maybe Later"/Skip) | unknown | held |
| Desk Stretch | READY_TO_SUBMIT | yr $29.99, mo $4.99 | not live | ProblemEmpathy→PainArea | soft ("Maybe Later") | unknown | not submitted |
| Affirm Well | READY_TO_SUBMIT | yr $29.99, wk $2.99 | not live | Welcome→Focus→Widget | soft (Skip/xmark) | I am (above) | not submitted |
| Micro-Mood | READY_TO_SUBMIT | yr $29.99, mo $4.99 | not live | source not found | unknown | unknown | — |
| SleepRitual | MISSING_METADATA | mo $4.99, yr $29.99 | — | source missing | — | — | withdrawn |
| HookTele, VagusReset, BreathCalm Test, BreathStory, TestFactory001, AppName, TestDeleteMe1-3 | no products / test | — | — | — | — | — | not revenue apps |

## Proposed changes, ordered by expected MRR impact
1. **Anicca (71% of subs, the only app with real traffic: 78 new customers/28d).** Set the PostHog `paywall-ab-test` payload to hard for 100% of new users. Add a 3-day trial on the yearly plan, matching I am (it has one; Anicca shows 0 trials). Raise yearly for new users only, from $29.99 to $49.99–59.99 (I am: $59.99–69.99). Re-enable a weekly ($7.99 product exists, removed from sale) or keep monthly $9.99 as the leader does. Impact is unknown until conversion is measured; this is where the volume is.
2. **Honne (2 subs, 25 new/28d).** Second-largest traffic. Find the source first (not under ~/anicca-project), then put a hard paywall after onboarding. Its prices are already at market (wk $7.99, yr $39.99).
3. **Aura Looks resubmission.** Copy Umax: gate the score result itself behind the weekly ($7.99) plan. This also answers Apple 2.1b. The weekly price is already in Umax's range.
4. FrostDip: create subscription products before resubmitting. Without them it can't earn anything.
5. Factory apps (Zone2Daily, Eye Break, Affirm Well): bring weekly from $1.99/$2.99 up to the $7.99 tier used by the live apps. Products are READY_TO_SUBMIT, so there's no grandfathering issue.
6. Dhamma, Thankful, Sleep Reset, Studio Cherie: traffic is ≤14 new/28d. A pricing change there is low impact, so distribution comes first. Studio Cherie's $0.99/mo is far below the portfolio.

## Unknowns
Paywall conversion rates (not pulled); Honne, Sleep Reset and Micro-Mood source; competitors for gratitude, dhamma, translation and fitness timers; RC numbers for non-live projects; Honne monthly JPY price.
