# Six-app store funnel on the open dashboard

Updated: 2026-11-11 13:45 JST. Grok Bot 参謀.

Public URL: https://aniccaai.com/open/

The live page already had App Store impressions / page views / first-time downloads for five apps, plus RevenueCat chart shells and the Anicca in-app screen funnel. It did not show one end-to-end store funnel for all six apps, and STUDIO CHERIE was missing from the App Store snapshot.

This pass adds a "Store funnel, six iOS apps" table at the top of the Apps group. Columns: impressions → page views → first-time downloads (App Store) → trial starts (28d) → active trials → paid subscriptions (stock) → MRR → 28-day proceeds → churn (last complete period).

## Coverage now

| App | Impressions | Page views | First-time downloads | Trial starts 28d | Paid subs / MRR | Churn |
|---|---|---|---|---|---|---|
| Anicca | 302 | 15 | 1 | 0 | 5 / $20.34 | 0% (0 of 5) |
| Honne | 177 | 2 | not reported in this 7-day download snapshot | 0 | 2 / $4 | Oct 50% (1 of 2); Nov so far 0% |
| Dhamma Quotes | 203 | 8 | 5 | 0 | 0 / $0 | n/a (no paid stock) |
| Sleep Reset | 110 | not reported | not reported | 1 | 0 / $0 | n/a; one trial did not convert |
| Thankful | 113 | 11 | 1 | 0 | 0 / $0 | n/a (no paid stock) |
| STUDIO CHERIE | 118 | 12 | 1 | 0 | 0 / $0 | n/a. RC project created 12:16 JST today. Collector now includes this app. |

App Store window is the current dashboard snapshot (about 2026-11-04 to 2026-11-10). RevenueCat window is 2026-10-14 to 2026-11-11, with MRR and paid subs as current stock. 28-day proceeds are $0 on all six apps. RevenueCat new customers are not installs and are not used as the install step.

## Still missing, and why

- STUDIO CHERIE App Store numbers were missing from the 13:42 table, then filled by the same deploy after the collector app list was updated: 118 impressions, 12 page views, 1 first-time download (2026-11-03 to 2026-11-09).
- Honne first-time downloads and Sleep Reset page views / first-time downloads: Apple did not return those rows in the current 7-day download/discovery days (not zero; not reported).
- Paid conversions as a period count: RevenueCat overview does not give a single "new paid conversions" number. We show 28-day proceeds ($0) and paid-subscription stock instead.
- Renewals as a period count: not a single published RevenueCat number. Churned actives and active subscriptions are the retention read.
- PostHog is not wired for these six iOS apps on this page.
- Honne is still `credential_missing` in the scheduled `metrics.json` RevenueCat snapshot. Today's table used the RevenueCat connector for Honne overview and churn. The scheduled collector still needs a project-scoped reader key for Honne so the regular metrics refresh keeps those charts filled.

## Keep updating

- `store_funnel` lives in `apps/landing/public/open/data.json` and is rendered by `index.html` (`renderStoreFunnel`).
- The existing 15-minute / hourly open refresh must keep the `store_funnel` key, or re-run `team/scripts/open/merge_store_funnel.py` after each data.json rebuild. If a refresh writes data.json without that key, the table falls back to a "not yet in this snapshot" message; App Store and RevenueCat sections below remain.
- Do not publish through `team/scripts/open/update_open.sh` / the local v2 builder; that path overwrites the richer live schema (this already happened once today and was restored).

Deployed in https://github.com/Daisuke134/anicca-products/commit/c10da48f09ba8fe2085007988218243f17783a0d (live at 13:50 JST). A follow-up data refresh writes the STUDIO CHERIE App Store counts into the funnel table.

Follow-up https://github.com/Daisuke134/anicca-products/commit/19dee43e2 writes STUDIO CHERIE 118 impressions / 12 page views / 1 first-time download into the funnel table.
