# Daily ship log — six iOS apps

Cadence: every app ships one App Store Connect improvement per day, Anicca first. Install truth = Apple first-time downloads. No paid ads. No secrets in this file.

Funnel window used for today's decisions: App Store Analytics 2026-11-03 to 2026-11-09 (latest complete snapshot; 2026-11-10 sales report was not yet published at 19:19 JST). RevenueCat for Anicca: 2026-10-14 to 2026-11-11.

| App | Impressions | Page views | First-time downloads | Page CVR | Weakest step today | RC / monetization |
|---|---:|---:|---:|---:|---|---|
| Anicca | 302 | 15 | 1 | 6.7% | Purchase: 0 new trials / $0 revenue in 28d (5 paid subs, MRR $20.34, last MRR still $20.34) | 3-day trial already on yearly.b in 175 territories |
| Honne | 177 | 2 | not reported | n/a (2 page views) | Impression→page (1.1%) | 0 trials / 2 old subs, MRR $4 |
| Dhamma Quotes | 203 | 8 | 5 | 62.5% in this 7d (28d page CVR 34%) | Purchase: 0 trials / $0 (page already converts) | 7-day trial already on yearly in 175 territories |
| Sleep Reset | 110 | not reported | not reported | n/a | Discovery + purchase (1 trial in 28d did not convert) | 7-day trial already on yearly in 175 territories |
| Thankful | 113 | 11 | 1 | 9.1% in this 7d (28d page CVR 5.9%) | Page conversion is the known leak; trial was USA+JPN only | Annual $39.99; monthly $4.99 |
| STUDIO CHERIE | 118 | 12 | 1 | 8.3% in this 7d (28d page CVR 4.2%) | Page conversion; live subtitle was missing | Promo rewritten earlier today, judged 11/18; not retouched |

28-day IAP proceeds remain $0 on all six apps.

---

## 2026-11-11 19:19 JST — Grok Bot 参謀

### Anicca (id 6755129214)
- **Change:** Live 1.9.10 promotional text (en-US, ja, fr-FR, de-DE, es-ES, pt-BR, pt-PT) now names the existing 3-day free trial on yearly.b, keeping the Lock Screen hook. Same text written onto in-review 1.9.11 so approval will not revert it. 1.9.11 build 824 stays WAITING_FOR_REVIEW. No 1.9.12 build existed. PPO `d7ffa0d7-704c-42ef-abf8-588f3bada53e` was not touched.
- **Hypothesis:** Shoppers who reach the product page do not start a trial because the listing never says one exists, even though yearly.b already has a 3-day intro in 175 territories. Naming the trial on the live promo should lift trial starts and help the weak 6.7% page→download step.
- **Metric to watch:** RevenueCat new trials and 28-day proceeds; Apple first-time downloads and page CVR vs 6.7%.
- **ID / state:** Live loc `856c7a60-9c4a-46a8-b5b0-3ff40fb0d7c9` (en-US) and `1ee7a15e-c315-4e05-b4bf-d9fbb1ee47a4` (ja), READY_FOR_SALE 1.9.10. Version 1.9.11 `26cbce6a-1451-4c09-9402-3dcd24f89636` still WAITING_FOR_REVIEW (submission `7935cb9a-6b23-4645-8e2e-169f8cd518d4`). Read back 19:16 JST: “Start a 3-day free trial.” / 「年額プランを3日間無料で試せます。」

### Honne (id 6759667221)
- **Change:** Live 1.0.6 promotional text (en-US + ja) now leads with the めろとーく privacy hook (“They are not notified” / 「相手にバレません」). Same promo copied onto unsubmitted 1.0.7. Live name/subtitle could not be edited (READY_FOR_SALE app-info is locked). PREPARE app-info en-US name set to `Honne: Text Message Decoder` (ja subtitle was already `既読スルーと脈あり分析`) so 1.0.7 can carry the search-listing fix. No 1.0.7 binary existed; 1.0.7 was not submitted.
- **Hypothesis:** The 177→2 impression→page leak is mostly name/subtitle/icon (live en-US name is still just “Honne”). The live lever today is the product-page promo: a privacy-first hook should help the few people who land convert, and it will also be on 1.0.7 when that build is attached.
- **Metric to watch:** Impression→page views (1.1%) and first-time downloads once Apple reports them; then 1.0.7 name/subtitle after that version ships.
- **ID / state:** Live 1.0.6 `161b4239-702b-49ce-a756-5bf4a8fb1035` promo read back 19:16 JST. 1.0.7 `244979cc-f61b-4a87-8829-ec11bf012a66` remains PREPARE_FOR_SUBMISSION. PREPARE app-info en-US `f7338eb1-fc54-4573-86cc-7365a7d4d796` name = Honne: Text Message Decoder.

### Dhamma Quotes (id 6757726663)
- **Change:** Created unsubmitted iOS version 1.2.0 (metadata copied from live 1.1.1, including the winning promo). Set PREPARE app-info to the already-agreed searchable title/subtitle: en-US `Dhamma Quotes: Buddha Quotes` / `Buddhist Wisdom & Daily Calm`; ja `ダンマ：ブッダの言葉` / `毎日の仏教の智慧と静けさ`. Live name/subtitle are locked on READY_FOR_SALE and were not changed. Live promo was left as the 34% winner. No new binary; 1.2.0 was not submitted.
- **Hypothesis:** Page conversion is already strong; the remaining store leak is 203→8 impression→page. A more searchable title (Buddha Quotes) should lift listing taps once 1.2.0 is approved with Codex’s paywall build (due 11/12 18:00 JST).
- **Metric to watch:** Impression→page and first-time downloads after 1.2.0 is live; do not judge on the live 1.1.1 listing.
- **ID / state:** Version `24d6e703-9789-4288-b29c-350da525670c` PREPARE_FOR_SUBMISSION. PREPARE app-info `17bf1645-17f2-40f5-bcbc-0847f961ee0b`. Live 1.1.1 `494a0f6a-de92-4d4f-bf48-402a36809cc1` READY_FOR_DISTRIBUTION. Read back 19:16 JST.

### Sleep Reset (id 6762143790)
- **Change:** Live 1.0.2 en-US promotional text now names the existing 7-day free trial on yearly (BetterSleep pattern), after the free sleep-reset score hook. Adding a ja localization on the live version was rejected (cannot create a locale after the version has been submitted).
- **Hypothesis:** 110 impressions with no reported page views/downloads, plus one 28-day trial that did not convert. Shoppers who do reach the page should see that a 7-day trial exists.
- **Metric to watch:** Product page views, first-time downloads, and RevenueCat new trials vs the prior 1 trial / 0 paid in 28 days.
- **ID / state:** Live loc `d0149ee0-c2c9-4886-9588-7ce1764c4125` on 1.0.2 `5206fb7b-0eb0-4053-a724-c9364841e3a4` READY_FOR_DISTRIBUTION. Read back 19:16 JST: “start a 7-day free trial to reset your rhythm.”

### Thankful (id 6759514159)
- **Change:** Extended `thankful_annual` (id 6759519847) from 2 territories (USA, JPN) to all 175: plan availability now 175 (USA+JPN kept, 173 added, none removed) and a 1-week free-trial intro now exists in all 175 (USA+JPN start 2026-02-22 unchanged; 173 new intros start 2026-11-11). `thankful_monthly` availability also expanded to 175 so the group can sell worldwide; no new monthly intros were added (still USA+JPN only). Prices were not equalized or changed (annual USA $39.99 / JPN ¥6000; monthly USA $4.99 / JPN ¥680). Live promo from earlier today (Gratitude winner copy, judge 11/18) was not retouched. No new version.
- **Hypothesis:** 0 trials were not only a paywall/CTA break; the annual trial was missing in 173 storefronts. Covering those territories unblocks trial starts outside USA/JPN. Page CVR (5.9% / 9.1%) remains the top listing leak and still needs the screenshot treatment.
- **Metric to watch:** RevenueCat new trials by territory (especially non-US/JP) and first-time downloads. Page CVR still judged 11/18 against the earlier promo test.
- **ID / state:** Annual intros 175/175 ONE_WEEK FREE_TRIAL, read back 19:19 JST. Annual and monthly plan availability 175, `availableInNewTerritories=true`. Live version 1.0.2 still READY_FOR_DISTRIBUTION.

### STUDIO CHERIE (id 6766485903)
- **Change:** Created unsubmitted iOS version 1.0.2 (metadata copied from live 1.0.1, including today’s XZ-style promo). Set the missing subtitle on the PREPARE app-info only: ja `クローゼット＆着回しコーデ`, en-US `Closet & Outfit Ideas` (XZ category words). Live app-info subtitle could not be edited (READY_FOR_SALE is locked) and remains empty. Live promo was not touched (already rewritten today, judged 11/18). No new binary; 1.0.2 was not submitted.
- **Hypothesis:** 4.2% (28d) / 8.3% (7d) page CVR is partly a listing problem: the live search row is just “STUDIO CHERIE” with no subtitle. The subtitle will reach the store when 1.0.2 is approved with Codex’s 30-item cap paywall (due 11/13 18:00 JST).
- **Metric to watch:** Page CVR vs 4.2% after 1.0.2 is live; today’s live promo still judged 11/18.
- **ID / state:** Version `34b305ad-6ded-48e4-95e4-58c5d950e30b` PREPARE_FOR_SUBMISSION. PREPARE app-info `2b316636-0221-4cd6-8ac5-bef9fd6d1291`. Live 1.0.1 `277266d6-bde4-4e3f-92ec-0659b78493a5` READY_FOR_DISTRIBUTION. Empty READY_FOR_REVIEW submissions on this app had 0 items and were left alone. Read back 19:16 JST.

---

## Anicca screenshot PPO status (untouched)

- **ID:** `d7ffa0d7-704c-42ef-abf8-588f3bada53e`
- **Name:** Lock Screen first screenshot Nov 2026
- **State:** WAITING_FOR_REVIEW (not live; `reviewRequired: true`)
- **Traffic:** 50%
- **Start / end:** none (not started)
- **Treatments:** 1 — `a5376aa3-4b0f-4af7-b1e0-479ace583533` “Lock Screen widget first”
- **Per-variant numbers:** none (experiment has not started)
- Control remains live 1.9.10 screenshots. This test was not modified today.

---

## 2026-11-12 (JST) — logged 18:2x by growth loop

| App | Change (live ASC) | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Anicca 6755129214 | es-ES/es-MX listing (subtitle/keywords/description), Issue #56, 17:38 | Spanish search impressions rise from ~0 | ES/MX impressions, PV | readback exact; 1.9.12 WAITING_FOR_REVIEW untouched |
| Anicca 6755129214 | Lifetime $89.99 USA / ¥13,980 JPN, Issue #55, 18:05 | Price ladder anchor lifts annual take-rate | paywall → purchase (RC) | readback USA 89.99 |
| CHERIE, Honne, Dhamma, Sleep, Thankful, Aura Looks | Billing Grace Period ON 16d ALL_RENEWALS prod+sandbox (#61, Muse decision) | Recovers involuntary churn at no cost | RC billing-issue recoveries | readback all 6 true/true/SIXTEEN_DAYS/ALL_RENEWALS |


## 2026-11-13 (JST) — logged 14:3x by growth loop (参謀)

| App | Change (live ASC) | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Anicca 6755129214 | (13:52, enforcer run) promo text pt-BR/de-DE/fr-FR/it → Lock Screen how-to hook, live 1.9.12 + in-review 1.9.14 (promo is editable in review) | I am pattern lifts PV→DL in those locales | ASC PV/DL BR/DE/FR/IT, judge 11/20 | PATCH 200 ×8, readback match (marketing/anicca/aso/promo-applied-20261113-1350.json) |
| Anicca 6755129214 | (14:10, grok-sanbo) Retention Messaging en-US+ja, text only, no offer, all 8 subs | Cancel-screen message saves some voluntary churn | RC cancellations / save rate 14d before vs after approval | msg 225f819c, review cb240aae WAITING_FOR_REVIEW |
| Thankful 6759514159 | (13:35, grok-sanbo) ja promoText | — | ja PV→DL | PATCH 200, readback match |
| **Honne 6759667221** | **(14:27) NEW PPO "Result screenshot first (ja) Nov 2026": treatment = live ja iPhone 6.7" screenshots reordered 3-2-1-4 (分析結果 → 相手の本音 → 悩み選択 → 履歴); control leads with the onboarding question. 50% traffic.** | First screenshot that shows the outcome (real meaning + reply suggestion) lifts imp→PV (3.8% 28d) and PV→DL (14.9%); treatment shots also show in search results. Source: https://developer.apple.com/app-store/product-page-optimization/ | PPO conversion vs control at ≥90% confidence (App Analytics); ASC imp→PV, PV→DL ja | exp `20ef37ba-a86e-4050-95df-98fa47a97bd8`, treatment `9141c661-b1c7-4105-b598-a2d5b04e875d`, review submission `e4cc5ea0-34c6-471c-9450-5a6d00b2a2bf` WAITING_FOR_REVIEW (14:27 JST). Start on approval (#86). No version touched. |


### KEEP / REVERT (changes ≥24h old, re-measured 14:2x JST)

| Change (date) | Re-measure | Verdict |
|---|---|---|
| Anicca promo names 3-day trial, 7 locales (11/11 19:19) | ASC PT 11/11: 109 imp, 8 PV, 0 DL; RC trials 0 (11/11–11/13) vs 0 before | KEEP for es-ES/pt-PT (no harm, n too small); en/ja/fr/de/pt-BR already superseded by Lock Screen hook (11/12 22:04, 11/13 13:52) |
| Honne promo「相手にバレません」en+ja (11/11) | RC Honne trials 0, revenue $0 (11/04–11/13); ASC per-app pull not in script this run | KEEP (no regression signal; inconclusive). Honne ASC imp→PV re-measure due 11/18 |
| Sleep Reset promo names 7-day trial (11/11) | RC: not re-measured (Sleep Reset not in the Anicca RC project) | INCONCLUSIVE — re-measure 11/18 with its own RC project |
| Thankful annual + 1w trial in 175 territories (11/11) | not re-measured this run | INCONCLUSIVE — 11/18 |
| CHERIE subtitle (11/12, live with 1.0.2 now READY_FOR_SALE) | <24h live | judge 11/18 vs 4.2% |
| Anicca es-ES/es-MX listing (11/12 17:38) | live only since 1.9.12 release (11/13); ASC PT 11/12+ unpublished | judge 11/20 |
| Lifetime $89.99 / ¥13,980 (11/12 18:05) | RC purchases 0 before and after | KEEP (no data) — judge with first purchases |
| Billing grace 16d, 6 apps (11/12) | RC billing-issue events: none observed | KEEP (zero-cost, no downside) |

### 2026-11-13 18:4x JST — growth loop 18:00 (参謀): ships for apps with none today

| App | Change (live ASC promo text, live version) | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Sleep Reset 6762143790 | en-US promo → named moment "Lying awake at 2am, or wide awake after a night shift or jet lag?" + free score + 7-day trial | Naming one painful moment beats a category promise (Muse playbook §C, files/no-installs-fix-playbook-2026-11-13.md) and lifts imp→PV / PV→DL | ASC en-US imp→PV, PV→DL; judge 11/20 | 1.0.4 loc 5d0d53eb, PATCH 200, readback match |
| Dhamma Quotes 6757726663 | en-US + ja promo → "Mind racing at work or before sleep?" /「考えごとで頭がいっぱいの時に。」 + daily verse + presence reminder | same | ASC en/ja imp→PV, PV→DL; judge 11/20 | 1.2.1 locs 73f26bf8, 2079e13d, readback match |
| STUDIO CHERIE 6766485903 | en-US promo → "Standing in front of a full closet with nothing to wear?" (ja unchanged) | same | ASC en-US PV→DL; judge 11/20 | 1.0.2 loc eb9054a2, readback match |

Backup/applied: marketing/anicca/aso/promo-backup-3apps-20261113-1840.json (Sleep Reset old text recorded by hand in the same file), promo-applied-3apps-20261113-1840.json. Anicca untouched this run: already 4 promo ships + retention messaging today; PPO d7ffa0d7 APPROVED/running since 11/12 12:31 PT (50%), 1.9.14 WAITING_FOR_REVIEW. All six apps now have a ship logged for 11/13.

### 2026-11-13 22:3x JST — growth loop 22:00 (参謀)

| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Anicca 6755129214 | TikTok + IG bio landing switched to the approved CPP "TikTok Lock Screen" via direct App Store link with ct (registry files/attribution-links.md §0); Codex issue #90 so /go keeps ppid | Visitors from Lock Screen how-to content convert better on a page showing the same widget than on the default page (Apple: custom product pages match the page to the ad/content intent — https://developer.apple.com/app-store/custom-product-pages/) → lifts PV→DL 4.8% | ASC Detailed PV/DL by ct with ppid f1554a3f; judge 11/20 | CPP f1554a3f ver 3a07f082 APPROVED; link verified 200; Muse places by 11/14 10:00 (#40 comment 6854181201) |

KEEP/REVERT at 22:00: Anicca promo Lock Screen hook (11/12 22:04) — ASC PT 11/12 still unpublished at 22:2x JST (latest processingDate 11/12 covers through PT 11/11), RC trials 0 / purchases 0 (21:1x watch). HOLD, re-read 11/14 22:00. No 24h data = no verdict, not a revert.

### 2026-11-14 10:2x JST — growth loop 10:00 (参謀)

Funnel (files/attribution-daily-2026-11-14.md, ASC Standard, PT 11/04–11/10, latest complete): 334 imp → 14 PV → 1 first-time DL → 0 Mixpanel external → 0 trial → 0 purchase. Search imp→PV 8/326 = 2.5% (benchmark 4.8%, https://benchhacks.com/benchmarks/appstore-benchmarks.htm); PV→DL 1/14 = 7% (benchmark ~25% iOS, AppTweak via https://www.webtonic.io/blog/app-store-optimization-statistics). Weakest step: PV→DL (0.28× benchmark).

| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Anicca 6755129214 | Submitted CPP review for Morning + Anxiety intents (2 items) the moment the 2-slot limit freed (1.9.14 submission 0f3d398b COMPLETE) | Intent-matched product pages convert higher than the default page (Apple CPP guidance https://developer.apple.com/app-store/custom-product-pages/) → lifts PV→DL 7% | ASC Detailed PV/DL per ppid once approved; Muse links Morning/Anxiety content to them | reviewSubmission c04b20de-7658-4f7b-ba55-606597bbeb47 WAITING_FOR_REVIEW 2026-11-14T01:25:07Z |

KEEP/REVERT: Lock Screen promo (11/12 22:04) — ASC PT 11/11+ still not complete in Standard at 10:2x JST → HOLD, re-read 11/14 22:00 (no data ≠ revert).
