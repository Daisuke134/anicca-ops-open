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

### 2026-11-14 14:2x JST — growth loop 14:00 (参謀): ships for apps with none today

| App | Change (live ASC promo text) | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| STUDIO CHERIE 6766485903 | ja promo → named moment「クローゼットは服でいっぱいなのに、着る服がない朝に。」+ existing 着回し/試算/CHIE lines (mirrors the en-US named-moment change of 11/13) | Naming one painful moment lifts JP imp→PV / PV→DL (Muse playbook §C) | ASC ja-storefront PV→DL vs 4.2% 28d; judge 11/21 | live 1.0.2 loc 044a03c5, PATCH 200, readback match |
| Honne 6759667221 | en-GB / en-AU / en-CA promo → same privacy hook as en-US ("They are not notified. …"); old text was the generic read-receipt line | One consistent hook across English storefronts; privacy is the top worry in the competitor (めろとーく) pattern | ASC GB/AU/CA PV→DL; judge 11/21. Honne ja PPO (11/13) untouched | live 1.0.7 locs 2e614a75, 2739ab7b, 2db506c8, readback match |

### 2026-11-14 18:2x JST — growth loop 18:00 (参謀)
| Thankful 6759514159 | en-US promo → named moment "Lying in bed replaying everything that went wrong today? Write 3 good things in 2 minutes and end the day kinder. Private gratitude journal + daily affirmations." (old = category line "Gratitude journal + daily affirmations in one private app…") | Naming one painful moment beats a category promise (same pattern as Sleep/Dhamma/CHERIE 11/13–14; Muse playbook §C) | ASC en-US imp→PV, PV→DL; judge 11/21 | live 1.0.3 loc dffa4925, update OK, readback match |
| Anicca 6755129214 (product, via Codex) | Issue #92: paywall Lifetime row cut off + trial lines truncated (Muse audit D-01/D-02/D-13) + remove Purchases.logOut() on 3 paths (inflates RC New Customers) | Purchase step can't convert if the plans aren't visible; logOut fix makes RC customer counts trustworthy | trial/purchase per paywall view (RC + Mixpanel) after build | #92 open, Codex owner, due NOW |
| Dhamma / Sleep Reset (blocked) | No safe live surface: promo under test since 11/13 18:40 (judge 11/20), only READY_FOR_SALE versions (keywords/subtitle need a new version; Sleep Reset has en-US only, ja locale needs a new version) | — | — | Next: new PREPARE version for keywords + ja locale (Sleep) — Codex/Rork build needed |
### 2026-11-14 22:2x JST — growth loop 22:00 (参謀): day close
Funnel (ASC Standard PT 11/06–11/12, fresh pull 22:1x): 450 imp → 25 PV → 1 first-time DL → 0 external Mixpanel → 0 trial → 0 purchase (RC MRR $20, trials 0). vs 10:2x window: imp +35%, PV +79%, DL flat. Weakest: PV→DL 4% (benchmark ~25%).
| App | Today's ship / blocker (all 6 covered) |
|---|---|
| Anicca | CPP Morning+Anxiety review c04b20de (10:25) — still WAITING_FOR_REVIEW 22:2x; RC exp529116692b confirmed stopped 12:39 JST (#88 closed with proof) |
| STUDIO CHERIE | ja promo named moment (14:2x) |
| Honne | en-GB/AU/CA promo privacy hook (14:2x) |
| Thankful | en-US promo named moment (18:2x) |
| Dhamma Quotes | BLOCKER: promo under test (judge 11/20); keywords/subtitle need a new version → build via Codex |
| Sleep Reset | BLOCKER: same; ja locale needs a new version |
KEEP/REVERT: Anicca Lock Screen promo (all locales, 11/12 22:04 JST = PT 11/12 05:04) → **KEEP**. PT 11/12 imp→PV 4.5% vs prior 7d 4.2%, no drop; PV→DL n=3 PV (0 DL) too small to show harm; promo is zero-cost and matches PPO d7ffa0d7 + Lock Screen CPP. Re-judge with PT 11/13–11/19 on 11/21.
### 2026-11-15 10:4x JST — growth loop 10:00 (参謀)
Funnel (files/attribution-daily-2026-11-15.md, ASC Standard fresh pull, PT 11/07–11/13): 536 imp → 25 PV → 1 first-time DL → 0 external Mixpanel → 0 trial → 0 purchase. vs 22:2x window (PT 11/06–11/12: 450/25/1): imp +19%, PV flat, DL flat. imp→PV 4.7% (benchmark 4.8%), PV→DL 4% (benchmark ~25%) → weakest = PV→DL. Ratings: JP 48 (4.52★), US 1, GB 0 (iTunes lookup 10:3x).
| Anicca 6755129214 | Assigned search keywords to approved CPPs (unique per page): Anxiety en-US anxiety,calm; Morning en-US morning; Self-Love&Calm en-US self love + ja 自己愛,癒し; Lock Screen ja ロック画面,ウィジェット. Default page keeps affirmation/free/confidence/mindset/gratitude/manifest | Searchers for those terms land on an intent-matched page; Apple: CPP referrals +2.5pt vs 1.6% default (https://developer.apple.com/app-store/custom-product-pages/) → lifts search PV→DL | ASC Acquisition › Product Pages per ppid, source=App Store search (≥5 DL to show); judge 11/22 | live, search-keywords readback match (5 localizations) |
| Anicca (prep) | 1.10.0 PREPARE en-US keywords + "lock screen" (97 chars) | lets Lock Screen CPP take en searches after 1.10.0 approval | — | loc 1352c16b readback match |
Also: CPP review c04b20de COMPLETE → Morning + Anxiety CPPs live (shipped 11/14). Other 5 apps: no ship yet today → 14:00 run (candidate: first CPP + keywords for Honne/Thankful; none of the 5 has a CPP).

### 2026-11-15 14:2x JST — growth loop 14:00 (参謀): 3 more apps shipped (live ASC promo text, readback 8/8 match)
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Thankful 6759514159 | ja promo → named moment「寝る前に、今日うまくいかなかったことを思い返していませんか？よかったこと3つを2分で…」(mirrors en-US 11/14) | Named-moment hook beats feature list on PV→DL (Anicca weakest step today = PV→DL 4% vs ~25%) | ASC ja PV→DL, judge 11/17 (PT lag) | loc ada5e7a2 readback match |
| STUDIO CHERIE 6766485903 | en-US promo + audience/producer line "Grown-up style for your 40s-60s, produced by CHIE." (from ja copy) | Clear audience self-selects the right visitors → higher PV→DL | ASC en-US PV→DL, judge 11/17 | loc eb9054a2 match |
| Honne 6759667221 | privacy hook ("they are not notified") to es-ES, es-MX, pt-BR, fr-FR, de-DE; el promo was cut off → completed | Same hook as en/ja across top non-English storefronts | ASC per-territory PV→DL, judge 11/17 | 6 locs match |
| Dhamma / Sleep Reset | BLOCKER unchanged: promo under test (judge 11/20); keywords/ja need new version → Codex | — | — | — |
Backup/applied: marketing/anicca/aso/promo-backup-thankful-cherie-honne-20261115-1420.json, promo-applied-thankful-cherie-honne-20261115-1420.json.
KEEP/REVERT due: CHERIE ja + Honne en-GB/AU/CA (11/14 14:2x) → 24h reached, but ASC Standard data is PT-day lagged (latest PT 11/13) → no post-change day yet; HOLD, judge in 22:00 run / 11/16 pull. Muse 13:24/13:52 messages already answered by reply-loop 14:1x (commit "参謀 reply-loop 14:1x").

### 2026-11-15 18:3x JST — growth loop 18:00 (参謀): measure + unblock, no new ASC surface
Fresh ASC pull 18:2x (files/attribution-daily-2026-11-15-1830.md): PT 11/14 still unpublished (no rows) → window PT 11/08–11/14 = 509 imp → 20 PV → 1 DL (the only DL is GB search 11/09) → 0 trial → 0 purchase. Weakest step unchanged: PV→DL (~5%, benchmark ~25%).
No extra Anicca ship: 10:4x CPP-keyword ship already counts for today; promo (Lock Screen hook) is live in all 39 locales and under KEEP judgement to 11/21, so retouching it would break the read. 1.10.0 build 829 is VALID + PREPARE but intentionally held (home rebuild after 成田さん's 07:41 rejection) → not submitted.
Today's ships: Anicca, Thankful, STUDIO CHERIE, Honne = done. Dhamma / Sleep Reset = BLOCKER → Issue #177 [owner: codex] new builds, due 11/16 12:00 JST.
KEEP/REVERT: CHERIE ja + Honne en-GB/AU/CA (11/14) and today's 14:2x promos → HOLD (no post-change PT day published yet); judge on the 11/16 pull.

### 2026-11-15 22:2x JST — growth loop 22:00 (参謀): day close
Funnel (ASC Standard, latest valid pull files/attribution-daily-2026-11-15-1830.md; PT 11/14 still unpublished at 22:2x): PT 11/08–11/14 = 509 imp → 20 PV → 1 first-time DL → 0 external Mixpanel → 0 trial → 0 purchase. RC overview 22:2x (projbb7b9d1b): MRR $20, active subs 5, active trials 0, 28d revenue $0. vs 11/14 22:2x (450/25/1): imp +13%, PV −20%, DL flat. Weakest = PV→DL (~5% vs ~25%).
| App | Today's ship / blocker (all 6 covered) |
|---|---|
| Anicca | CPP search keywords on 4 approved CPPs (10:4x, live) + 1.10.0 PREPARE en keyword "lock screen" (held with build 829) |
| Thankful | ja promo named moment (14:2x) |
| STUDIO CHERIE | en-US promo audience line (14:2x) |
| Honne | privacy hook to es-ES/es-MX/pt-BR/fr-FR/de-DE + el fix (14:2x) |
| Dhamma Quotes / Sleep Reset | BLOCKER: promo under test to 11/20; keywords/ja need new version → Issue #177 [owner: codex] due 11/16 12:00 JST |
KEEP/REVERT: CHERIE ja + Honne en-GB/AU/CA (11/14) and 11/15 promos → HOLD (no post-change PT day published); Lock Screen promo KEEP (judged 11/14). Judge on 11/16 pull.
Measurement bug: `attribution-daily.py --pull --cache /workspace/tmp/aff-funnel` at 22:24 wrote an older window (PT 11/04–11/10) over today's file; restored from git. → @pickle: fix pull/cache so a new run never regresses the window (guard: refuse to write if latest PT date < existing file's).

### 2026-11-16 10:2x JST — growth loop 10:00 (参謀)
Funnel (files/attribution-daily-2026-11-16.md, fresh ASC Standard pull 10:2x; PT 11/15 unpublished): PT 11/09–11/14 = 564 imp → 26 PV → 1 first-time DL → 0 external Mixpanel → 0 trial → 0 purchase. vs 11/15 22:2x (PT 11/08–11/14: 509/20/1): imp +11%, PV +30%, DL flat. Weakest = PV→DL (3.8% vs ~25%). New: app_referrer 7 PV (TikTok com.ss.iphone.ugc.Ame) → 0 DL → #89 (Pickle handoff test) + Muse CPP links (#40).
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Anicca 6755129214 | Submitted in-app event 6833871115 "New Year Affirmation Start" (publish 12/12 JST, event 12/26–1/9, 41 territories) | Events add a second card in search and on the product page and can be featured (https://developer.apple.com/app-store/in-app-events/) → keeps an event on the page after Overthinking Week ends 11/21 → lifts imp→PV and PV→DL | ASC event impressions / opens + PV→DL in Dec | submission 6d709f4e, readback WAITING_FOR_REVIEW |
Gap 11/22–12/11 has no live event → bridge event, owner 参謀, due 11/17 22:00 JST (#64). Other 5 apps: no ship yet today → 14:00 run. Dhamma/Sleep Reset blocker #177 (codex, due 11/16 12:00 JST).
KEEP/REVERT: CHERIE ja + Honne en-GB/AU/CA promos (11/14 14:2x JST = PT 11/13 21:2x) → first post-change PT day 11/14 now published, but per-app pull not run for those apps this run → judge in the 14:00 run with their per-app pulls (no data invented). Lock Screen promo: KEEP holds (re-judge 11/21).

### 2026-11-16 14:2x JST — growth loop 14:00 (参謀)
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Honne 6759667221 | Privacy hook promo ("they are not notified" lead) to it, ko, nl-NL, pt-PT, fr-CA (were still on the old "read with no reply?" line) | Same hook as en/ja/es/pt-BR/fr/de across 5 more storefronts → higher PV→DL | ASC per-territory PV→DL IT/KR/NL/PT/CA, judge 11/18 once #236 lands | readback 5/5 match on version 244979cc |
| Thankful 6759514159 | BLOCKER: both promo locales under measurement; no-version surface left = in-app event → #237 [codex] US Thanksgiving event, due 11/17 12:00 JST | — | — | #237 |
| STUDIO CHERIE 6766485903 | BLOCKER: en-US/ja promos under measurement (judge after #236); new version needs a build | — | — | #236 |
| Dhamma Quotes / Sleep Reset | BLOCKER unchanged: #177 [codex] still open, overdue since 11/16 12:00 JST | — | — | #177 |
KEEP/REVERT: CHERIE ja/en-US + Honne en-GB/AU/CA promos still can't be judged — no per-app ASC pull exists. Filed #236 [codex] due 11/17 10:00 JST; no data invented. Anicca: ship already logged 10:2x (event 6833871115).

### 2026-11-20 14:4x JST — growth loop 14:00 (参謀)
Funnel (files/attribution-daily-2026-11-20.md, ASC Standard discovery pull 14:28 JST, PT 11/13–11/18 published): 467 imp → 145 PV → first-time DL **unknown** (Downloads report pull failed: S3 SSLError → #442 [pickle] due 11/21 10:00 JST; file's "0" is not a measured 0) → external Mixpanel 0 / trial 0 / purchase 0 (no new RC/Mixpanel pull this run). Search impressions fell from 105–127/day (PT 11/13–14) to 31–39/day (PT 11/16–18); search imp→PV 11/418 = 2.6% = weakest measurable step. Browse PV 36 + app_referrer PV 89 spike on PT 11/15–16 (Overthinking Week event card + social links).
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Anicca 6755129214 | New in-app event "21 Days of Calmer Holidays / 21日間のおだやかな年末" (CHALLENGE, en-US+ja, 41 territories, 11/22 00:00–12/12 23:59 JST) closes the gap after Overthinking Week (ends 11/21) until the New Year event (publish 12/12) | Events add a card in search results and on the product page; Overthinking Week weeks showed browse PV 36 + referrer PV 89 vs ~0 before → keep a live event so search imp→PV and browse don't drop back | ASC search/browse imp→PV and first-time DL, PT 11/22–11/28 vs PT 11/16–11/21 | event 6837154919, reviewSubmission e3a572ca, WAITING_FOR_REVIEW (proof marketing/anicca/aso/event-holiday-calm-2026-11/proof.json) |
| Honne / Thankful / CHERIE / Dhamma / Sleep Reset | BLOCKER: Codex CLI on box returns "Quota exceeded" and Devin CLI refuses the workspace (untrusted, config flag ignored) → #177/#236/#237 builds can't move this run | — | — | #177 #236 #237 |
KEEP/REVERT: Lock Screen promo (11/14) — HOLD: DL unknown until #442. 1.10.1 waiting for review (not touched).


### 2026-11-20 18:2x JST — growth loop 18:00 (参謀)
Funnel: no new pull since 14:28 (ASC Standard discovery PT 11/13–11/18: 467 imp → 145 PV → DL unknown #442 [pickle] due 11/21 10:00 JST → external Mixpanel 0 / trial 0 / purchase 0). Weakest measurable step unchanged: Anicca search imp→PV 2.6%. Anicca already shipped today (event 6837154919, 14:4x).
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Thankful 6759514159 | en-US promo text → seasonal Thanksgiving line: "Thanksgiving week: write 3 good things in 60 seconds, morning and night. A private gratitude journal with gentle reminders and daily affirmations. 7-day free trial." (was "Lying in bed replaying everything that went wrong today? …"; ja untouched as control) | Gratitude intent peaks Thanksgiving week (US 11/26); timely promo text raises PV→DL. Source: https://developer.apple.com/app-store/product-page/ (promo text editable anytime w/o review, for timely messaging) | US PV→DL PT 11/21–11/27 vs PT 11/13–11/19; revert to old line 11/28 | loc dffa4925 live (verified by re-read) |
KEEP/REVERT: Lock Screen promo HOLD (DL unknown until #442). Thankful prior en-US promo (11/15) closed as unjudgeable (no per-app pull, #236) — replaced by seasonal test. Honne/CHERIE/Dhamma/Sleep Reset: builds still blocked (Codex quota / Devin trust) #177/#236/#237.

### 2026-11-20 22:2x JST — growth loop 22:00 (参謀)
Funnel (fresh ASC pull 22:2x JST, Standard discovery newest PT 11/18, downloads newest PT 11/19; window PT 11/13–11/19): 467 imp → 145 PV → **3 first-time DL (measured; Downloads pull works again, #442 gap closed for this window)** → external Mixpanel unknown / trial 0 / purchase 0. DL rows: PT 11/15 aso_search JP ×2 (No page), PT 11/16 app_referrer JP ×1 (product page); ct blank. vs prior 7d baseline PT 11/04–11/10: 334/14/1. RevenueCat overview 22:2x JST (two projects projcfa60dd8 + projbb7b9d1b): MRR $4 + $20 = $24, active trials 0, active subs 2 + 5, 28d revenue $0. Weakest step: search imp→PV 11/418 = 2.6% (PV→DL 3/145 = 2.1% next).
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Honne 6759667221 | en-US promo → "Holiday group chats and "we should catch up" texts? …" (ja = control) | Seasonal timely promo text lifts PV→DL (Apple: promo text editable anytime for timely messaging, https://developer.apple.com/app-store/product-page/) | US PV→DL PT 11/21–11/27 vs 11/13–11/19; revert 11/28 | loc b3a36fbc live, verified by re-read |
| Dhamma Quotes 6757726663 | en-US promo → "Holiday rush filling your mind? …" | same | same | loc 73f26bf8 live, verified |
| Sleep Reset 6762143790 | en-US promo → "Holiday travel, late parties or jet lag? …" | same | same | loc 5d0d53eb live, verified |
| STUDIO CHERIE 6766485903 | en-US promo → "Holiday dinners and parties ahead, and nothing to wear? …" (ja control) | same | same | loc eb9054a2 live, verified |
All six apps have a ship today: Anicca (event 6837154919, 14:4x), Thankful (18:2x), Honne/Dhamma/Sleep Reset/CHERIE (22:2x). Builds #177/#236/#237 still blocked (Codex quota / Devin trust) — Muse 22:12 doctrine says Codex now has token headroom → re-push to Codex.
KEEP/REVERT: Lock Screen promo (Anicca, 11/14) — now judgeable: PT 11/13–19 3 DL vs PT 11/04–10 1 DL, PV 14→145 → KEEP (small n, re-check 11/27).
### 2026-11-21 10:5x JST — growth loop 10:00 (参謀)
Funnel (files/attribution-daily-2026-11-21.md; fresh ASC pull 10:3x JST, newest PT 11/19 for all four reports, so PT 11/20 isn't published yet): Anicca PT 11/13–11/19 = 500 imp → 146 PV → 3 first-time DL → Mixpanel unknown (no credential) → trial 0 → purchase 0. RevenueCat 10:3x JST: MRR $4 + $20 = $24, trials 0, 28d revenue $0. Yesterday's 467/145 was the same window with discovery only through PT 11/18; PT 11/19 added 33 imp and 1 PV. **No real metric change vs yesterday.** Weakest step: search imp→PV 12/450 = 2.7% (438 people saw the app and didn't tap). Overall PV→DL is 2.1%, but most of those PV come from the event card and social links.
| Anicca 6755129214 | Assigned search keyword "lock screen" to the approved CPP "TikTok Lock Screen" en-US (it had none). "lock screen" is in the live 1.10.1 en-US keyword field and isn't used by another CPP | Apple: keywords assigned to a CPP make that page show in search results for those terms instead of the default page (https://developer.apple.com/app-store/custom-product-pages/). Results for "lock screen" will show Lock Screen widget screenshots that match the intent → higher search imp→PV | ASC search imp→PV (US) PT 11/21–11/27 vs PT 11/13–11/19 (2.7%), plus Product Pages ppid f1554a3f search PV/DL; judge 11/28 | loc 08d709b0 searchKeywords readback ["lock screen"]; proof marketing/anicca/aso/cpp-keyword-lockscreen-en-20261121.json |
| Thankful 6759514159 | In-app event "Thanksgiving Gratitude Week" (CHALLENGE, en-US, USA, 11/22 00:00 PT – 11/29 23:59 PT, deep link aniccaai.com/thankful). This was #237, open since 11/16 | Event cards show in search and on the product page and can be featured (https://developer.apple.com/app-store/in-app-events/). Gratitude intent peaks Thanksgiving week, and the same seasonal message is in the en-US promo (11/20) | US imp / PV / DL PT 11/22–11/29 vs PT 11/13–11/19 (needs #236) + ASC event impressions | event 6837538280, reviewSubmission 6682e67b WAITING_FOR_REVIEW (readback); proof marketing/thankful/aso/event-thanksgiving-2026-11/proof.json |
| Sleep Reset 6762143790 | In-app event "Holiday Sleep Check" (CHALLENGE, en-US, USA/GBR/CAN/AUS, 11/22–12/20 PT, free score; the plan is disclosed as a subscription; deep link aniccaai.com/sleepreset) | The en-US promo was already retouched 11/20, so an event is the only no-build surface left. Same source as above | imp / PV / DL in 4 storefronts PT 11/22–12/20 vs prior 7d (needs #236) | event 6837539468, reviewSubmission 964c95fd WAITING_FOR_REVIEW; proof marketing/sleep-reset/aso/event-holiday-sleep-2026-11/proof.json |
| Honne 6759667221 | Privacy-hook promo ("they are not notified" lead) rolled out to zh-Hant, zh-Hans, id, th, vi (these still had the old "read with no reply?" opener) | Same hook as 18 other storefronts; 已讀不回 is a strong Asian intent. Apple: promo text is editable anytime with no review (https://developer.apple.com/app-store/product-page/) | ASC TW/CN/ID/TH/VN PV→DL PT 11/21–11/27 (needs #236) | 5/5 PATCH 200, readback match; backup/applied marketing/anicca/aso/promo-*-3apps-20261121-1100.json |
| Dhamma Quotes 6757726663 | ja promo → year-end hook "年末の忙しさで頭がいっぱいの時に。…" (was "考えごとで…"), the same seasonal idea as the 11/20 en-US line | Timely promo text lifts PV→DL (same Apple source) | JP PV→DL PT 11/21–11/27 vs 11/13–11/19 (needs #236); revert 12/31 | loc 2079e13d readback match |
| STUDIO CHERIE 6766485903 | ja promo → "忘年会やクリスマス、着ていく服がない？…" (was "クローゼットは服でいっぱいなのに…"), mirroring the 11/20 en-US holiday line | same | JP PV→DL PT 11/21–11/27 vs 11/13–11/19 (needs #236); revert 12/26 | loc 044a03c5 readback match |
All six apps have a ship today. Builds: #236 (per-app ASC pull) was re-pushed to the box Codex at 10:5x JST (worktree /workspace/codex-236, branch codex/236-per-app-asc; it started without a quota error). #177 (Dhamma/Sleep Reset build) re-pushed via team/inbox/codex.md; it needs a macOS build path because the box is Linux.
KEEP/REVERT: Lock Screen promo (Anicca 11/14): KEEP stands, re-check 11/27 (no new PT day). Honne en-GB/AU/CA promos (11/14, due today): **HOLD**, still no per-app data until #236 lands, nothing invented. CHERIE ja promo (11/14): closed as unjudgeable, replaced by today's ja seasonal line. Anicca CPP keywords (11/15): judge 11/22. Seasonal en-US promos for Thankful/Honne/Dhamma/Sleep/CHERIE (11/20): judge 11/28. RISK: Anicca "21 Days of Calmer Holidays" event 6837154919 is still WAITING_FOR_REVIEW and is set to start 11/22 00:00 JST. If it isn't approved in time it starts late, and Muse's ct=evt_holiday_20261122 shorts would point at a page with no event card.
**11:1x JST addendum: #236 landed** (Codex wrote the code; network was blocked in its sandbox, so 参謀 ran the pull and kept the Anicca default unchanged: 500/146/3 re-verified, 26+ tests pass; commit c05b941d6). Per-app baselines, PT 11/13–11/19 published days (files/attribution-daily-<app>-2026-11-21.md):
| App | Imp | PV | First-time DL | Note |
|---|---:|---:|---:|---|
| Dhamma Quotes 6757726663 | 499 | 17 | 6 | best DL; MM 75 / ID 36 imp |
| Honne 6759667221 | 295 | 16 | 1 | JP 82 imp / 4 PV |
| Thankful 6759514159 | 95 | 2 | 1 | US 52 imp, 1 DL (11/18) |
| Sleep Reset 6762143790 | 90 | 4 | 0 (some days have no rows) | GB 30 / US 36 imp |
| STUDIO CHERIE 6766485903 | 115 | 5 | unknown (downloads report newest PT 11/12) | JP 47 imp / 5 PV |
Caveat: a day with no download rows prints "unknown". It may really be 0, but the report doesn't tell us, so it isn't written as 0.
KEEP/REVERT, now judgeable: **Honne en-GB/AU/CA privacy promo (11/14) → KEEP (inconclusive)**. PT 11/13–19: GB 1 imp / 0 PV, AU 2 / 0, CA 5 / 1 PV / 0 DL. That's far below a readable sample. It costs nothing, matches the 18-locale hook, and shows no harm. Re-read 11/28 with the seasonal tests.
### 2026-11-21 14:3x JST — growth loop 14:00 (参謀)
Funnel: ASC re-pulled 14:2x JST (team/scripts/attribution-daily.py --pull, PT 11/14–11/20 requested). Newest published PT day is still **11/19** for all four reports, so PT 11/20 isn't out yet. Anicca PT 11/13–11/19 stays 500 imp → 146 PV → 3 first-time DL → Mixpanel unknown (#495) → trial 0 → purchase 0. No new RevenueCat pull this run, so MRR is the 10:3x value of $24. **No real metric change vs 10:5x.** Weakest step is still search imp→PV 2.7%. The two search DL in the window are both JP (PT 11/15).
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Anicca 6755129214 | Added search keywords 「不安」「ストレス」 to the approved CPP "Self-Love and Calm" ja (now 自己愛, 癒し, 不安, ストレス). Both are in the live 1.10.1 ja keyword field and not used by the other ja CPP (Lock Screen ja: ロック画面, ウィジェット) | Apple: keywords assigned to a CPP make that page show in search results for those terms instead of the default page (https://developer.apple.com/app-store/custom-product-pages/). JP searchers for 不安/ストレス see calm/self-love screenshots that match the intent → higher JP search imp→PV. JP is the only storefront with search DL this window | ASC JP search imp→PV + ppid 62120fb7 search PV/DL, PT 11/22–11/28 vs PT 11/13–11/19 (2.7% all-territory); judge 11/30 | loc 32ee83d8 searchKeywords readback [自己愛, 癒し, 不安, ストレス]; live, no review needed; proof marketing/anicca/aso/cpp-keyword-selflove-ja-20261121-1430.json |
Not touched: 1.10.1 is READY_FOR_DISTRIBUTION (live). No version is in review and no PPO experiment was changed. Event 6837154919 is still WAITING_FOR_REVIEW (submission e3a572ca, starts 11/22 00:00 JST).
KEEP/REVERT (changes from 11/20 that are now ≥24h old; newest PT day is 11/19, so none of them has a single post-change day yet):
- Anicca event "21 Days of Calmer Holidays" 6837154919 (11/20 14:4x): **HOLD, data not published.** It hasn't started (starts 11/22) and is still in review. Decidable 11/30 with PT 11/22–11/28.
- Thankful seasonal en-US promo (11/20 18:2x) and Honne/Dhamma/Sleep Reset/CHERIE holiday en-US promos (11/20 22:2x): **HOLD, data not published.** First post-change PT day is 11/21, published around 11/23. Decidable 11/28 (window PT 11/21–11/27, as planned).
- Anicca CPP keywords (11/15): **HOLD.** The planned judge date is 11/22, but PT 11/20+ isn't published. Decidable 11/22–11/23 when PT 11/21 lands.
- Muse holiday shorts ct=evt_holiday_20261122 (due 12:00 JST): **not posted** at 14:2x. Issue #498, new due 18:00 JST today.

### 2026-11-21 18:2x JST — growth loop 18:00 (参謀)
Funnel: ASC re-pulled 18:2x JST (attribution-daily.py --pull). Newest published PT day is still **11/19**, so Anicca PT 11/13–11/19 stays 500 imp → 146 PV → 3 first-time DL → Mixpanel unknown (#495) → trial 0 → purchase 0; MRR $24 (RevenueCat 10:3x). **No real metric change.** Weakest step: search imp→PV 2.7%; both search DL in the window are JP.
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Anicca 6755129214 | Added search keywords 「セルフケア」「マインドフルネス」 to the approved CPP "Self-Love and Calm" ja (now 自己愛, 癒し, 不安, ストレス, セルフケア, マインドフルネス). Both are in the live 1.10.1 ja keyword field and unused by the other ja CPP (Lock Screen ja: ロック画面, ウィジェット) | Same Apple CPP-keyword mechanism (https://developer.apple.com/app-store/custom-product-pages/): JP self-care/mindfulness searchers see calm/self-love screenshots instead of the default page → higher JP search imp→PV | JP search imp→PV and CPP 62120fb7 PV/DL, PT 11/22–11/28 | loc 32ee83d8 readback = 6 keywords, live (CPP version APPROVED) |
Not touched: 1.10.1 live, no version in review changed, no PPO changed, event 6837154919 untouched.
KEEP/REVERT: all 11/20+ changes HOLD (no post-change PT day published); Anicca CPP KW 11/15 judge when PT 11/21 lands (~11/23).
Muse holiday shorts ct=evt_holiday_20261122 (#498, due 18:00 JST): **not landed** in ACTIVITY at 18:2x → re-pushed, due 20:00 JST (event starts 11/22 00:00 JST).

### 2026-11-21 22:2x JST — growth loop 22:00 (参謀)
Funnel: ASC re-pulled 22:2x JST. Downloads report now has PT **11/20** (no Anicca first-time DL rows on 11/17–11/20); discovery still newest PT 11/19. Anicca PT 11/13–11/19 = 500 imp → 146 PV → 3 first-time DL (JP search 2 on 11/15, JP app referrer 1 on 11/16) → Mixpanel unknown (#495) → trial 0 → purchase 0. RevenueCat 22:2x JST: MRR $4 (projcfa60dd8) + $20 (projbb7b9d1b) = **$24**, active trials 0, 28d revenue $0. No real metric change vs 18:00. Weakest step unchanged: search imp→PV.
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
Not touched: 1.10.1 live, no version in review, no PPO change, event 6837154919 untouched (starts 11/22 00:00 JST).
KEEP/REVERT: all 11/20+ changes HOLD (no post-change PT discovery day published). Anicca CPP KW (11/15) judge when PT 11/21 lands (~11/23).
#498 Muse holiday shorts ×3 (ct=evt_holiday_20261122) and outliers #1/#3: **not landed** at 22:00 (due 12:00→18:00→20:00→22:00 all missed). Muse confirmed at 20:13 that 参謀 takes over if no URL; video posting is Muse's channel, so 参謀 checks Muse drafts first to avoid a double post, re-pushed with due 11/22 10:00 JST.

### 2026-11-22 10:4x JST — growth loop 10:00 (参謀)
Funnel (files/attribution-daily-2026-11-22.md; fresh ASC pull 10:20 JST, newest PT 11/20 for all four reports): Anicca PT 11/14–11/20 = 439 imp → 155 PV → 3 first-time DL (JP search 2 on 11/15, JP app referrer 1 on 11/16) → Mixpanel unknown (#495) → trial 0 → purchase 0. Channels: search 384/10/2, browse 55/38/0, web referrer 0/9/0, app referrer 0/98/1. Prior window PT 11/13–11/19 was 500/146/3; the drop of 61 imp is the window sliding (PT 11/13 out, 11/20 in), not a change we caused. RevenueCat not re-pulled this run (last read 11/21 22:2x JST: MRR $24, trials 0). **No real metric change.** Weakest step unchanged: search imp→PV 10/384 = 2.6%.
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Anicca 6755129214 | FIX + ship: approved CPP "Self-Love and Calm" en-US keywords [self love, calm, anxiety] → [self love, confidence]. Readback found "calm" and "anxiety" were already assigned to the approved CPP-Anxiety-EN (deaaf900, since 11/15), so the 11/21 22:2x ship overlapped it and its log line ("only Lock Screen uses keywords") was wrong. "confidence" is in the live 1.10.1 en-US keyword field and used by no CPP | One keyword → one CPP keeps the 11/15 Anxiety-CPP test readable and sends en-US "confidence" searchers to the self-love page (https://developer.apple.com/app-store/custom-product-pages/) | en-US search imp→PV; CPP 62120fb7 and deaaf900 PV/DL, PT 11/22–11/28 | loc 7354b614 readback [self love, confidence]; deaaf900 readback [anxiety, calm]; proof marketing/anicca/aso/cpp-keyword-selflove-en-fix-20261122-1040.json |
Not touched: 1.10.1 live, no version in review, no PPO change, event 6837154919 untouched. Lesson: before adding a CPP keyword, list keywords on **every** CPP (5 CPPs: Anxiety-EN, LockScreen-EN (draft), Morning-EN, Self-Love and Calm, TikTok Lock Screen).
Other 5 apps (Honne, Dhamma Quotes, Sleep Reset, Thankful, STUDIO CHERIE): handed to @codex via team/inbox/codex.md (TEAM-FIRST), one live ASC surface each with readback, due 18:00 JST; 参謀 verifies at the 18:00 run, and any app still without a ship gets a logged blocker by 22:00.
KEEP/REVERT: all 11/20+ changes HOLD (PT 11/21 discovery not published yet). Anicca CPP KW (11/15): judge when PT 11/21 lands (~11/23).
#498 Muse holiday shorts ×3 (ct=evt_holiday_20261122) and outliers #1/#3: **not landed** at 10:00 (due 11/22 10:00 JST missed; 5th miss). No new outlier briefs this run, because the two earlier briefs are still unposted.


### 2026-11-22 14:2x JST — growth loop 14:00 (参謀)
Funnel: no new ASC data since 10:20 pull (newest PT 11/20); numbers unchanged (Anicca PT 11/14–20 = 439 imp → 155 PV → 3 DL → trial 0 → purchase 0). Weakest step still search imp→PV 2.6%.
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Anicca 6755129214 | SHIP #2 today: submitted in-app event "2027 January - 7-Day Kinder Words (EN)" (en-US loc + card + details assets complete, 41 territories, publish 2027-01-02 JST) | In-app event cards show in search/Today for new-season intent; a 2nd queued event after New Year (6833871115 APPROVED) keeps an event card live through Jan (https://developer.apple.com/app-store/in-app-events/) | event impressions/PV/DL Jan; search imp→PV | event 6833871152, submission 3e5c470f-fb68-4d04-9ae0-e75fb4941950, WAITING_FOR_REVIEW |
Live now: Holiday Calm event 6837154919 PUBLISHED since 11/22 00:00 JST (first measurable PT 11/22 data ~11/24). #498 → @devin production (due 18:00), Muse posts by 21:00. Other 5 apps: still with @codex, verify at 18:00.

### 2026-11-22 18:5x JST — 5-app daily ship (Command Code for 参謀)
Surface audit first (all 5 apps' current versions are READY_FOR_DISTRIBUTION, so nothing in review was touched):
- On a LIVE version only `promotionalText` is PATCH-able. Verified by direct API probes: `keywords` → "Attribute 'keywords' cannot be edited at this time"; `description`/`whatsNew`/`supportUrl`/`marketingUrl` → same state error; app-info `subtitle`/`privacyPolicyUrl` → "can not be modified in the current state".
- Creating a new locale on a live version is impossible: `localizations create` → "Cannot create localization after the app version has been submitted for review." So the "add en-GB/en-AU/ja promo" route only works where the locale already exists (Honne has 39; Thankful/Dhamma/Sleep/CHERIE have only en-US + ja).
- Honne PPO experiment 20ef37ba (ja "Result screenshot first", APPROVED, running to 2027-02-12) NOT touched. No PPO on the other four.
- Cleanup: three throwaway probes (a retention message, a promoted purchase, a test CPP) were created and deleted in the same run; verified gone by re-list. Anicca 6755129214 not touched.

| App | Change (locale, field, old→new) | Hypothesis | Metric to watch | readback |
|---|---|---|---|---|
| Honne 6759667221 | promotionalText, 3 locales not touched in 7d (11/21 run used zh/zh-Hant/id/th/vi; these were last on the 11/15 batch): **pl** "Przeczytane bez odpowiedzi? Oschłe wiadomości? …" → "Nikt nie dostaje powiadomienia. Wklej oschłą wiadomość lub czat bez odpowiedzi, sprawdź, co mogła znaczyć, i dostań odpowiedź, która nie pogorszy relacji." · **tr** "Okundu ama yanıt yok mu? …" → "Karşı tarafa bildirim gitmez. Soğuk mesajı ya da okundu ama yanıtsız sohbeti yapıştırın, olası anlamı görün ve ilişkiyi bozmayan yanıt alın." · **ru** "Прочитано без ответа? …" → "Собеседник не получит уведомления. Вставьте сухое сообщение или чат, прочитанный без ответа, увидьте возможный смысл и получите ответ, который не испортит отношения." | Leads with the privacy reassurance ("they are not notified"), the hook that now carries 26 other storefronts. Privacy is the top worry in this niche, so the first line should name it before the problem | PL/TR/RU PV→DL PT 11/23–11/29 vs PT 11/14–11/20 (per-app pull #236); judge 11/30 | 3/3 PATCH 200 + `localizations view` returns exactly the new strings (pl ac35fc6f, tr 4b110763, ru f6499154) |
| Thankful 6759514159 | promotionalText **ja** (last touched 11/15, outside the 7-day window; en-US seasonal stays live as control): "寝る前に、今日うまくいかなかったことを思い返していませんか？…" → "今年もあと少し。寝る前に、今日よかったことを3つ書いてみませんか？2分で終わる、完全プライベートの感謝日記。毎日のアファメーションつき。7日間の無料トライアル。" | Year-end reflection framing mirrors the en-US Thanksgiving line without repeating it. Subscription disclosed as a free trial, not "free" | JP PV→DL PT 11/23–11/29 vs PT 11/14–11/20; revert 1/4 | loc ada5e7a2 readback = exact new string |
| Dhamma Quotes 6757726663 | NEW in-app event "A Verse Before the Rush (Dec 2026)" — CHALLENGE, en-US + ja, 18 territories, publish/start 2026-11-30 15:00Z → end 2026-12-31 14:59:59Z, deep link aniccaai.com/dailydharma, cards+details COMPLETE. Both promo locales were touched 11/20–11/21, so an event is the only untouched no-build surface | Event cards get a second slot in search and on the product page (https://developer.apple.com/app-store/in-app-events/). Dhamma has the best DL of the five (6 in PT 11/13–19) and no event at all; a Dec card keeps a seasonal entry point through the year-end intent peak | ASC event impressions/PV/DL + JP/TH/TW search imp→PV, PT 11/30–12/31 vs PT 11/14–11/20 | event 6837934616, submission 9cae257e-5379-4065-8caf-a15f85d8621c, **WAITING_FOR_REVIEW**; `app-events list --app 6757726663` shows the id (ownership checked) |
| STUDIO CHERIE 6766485903 | NEW in-app event "Party Season, Own Closet (Dec 2026)" — CHALLENGE, en-US + ja, 10 territories, 2026-11-28 15:00Z → 2026-12-26 14:59:59Z, deep link aniccaai.com/studio-cherie, cards+details COMPLETE. Copy states 30 items free + monthly plan (no false "free") | Party-season outfit intent peaks late Nov–Dec. Event copy pushes the owned-closet angle instead of shopping, which is the app's actual promise | ASC event impressions/PV/DL + JP/US PV→DL, PT 11/28–12/26 vs PT 11/14–11/20 | event 6837934913, submission 3e13f701-4551-4177-a463-cdc9e33cf12b, **WAITING_FOR_REVIEW**; ownership checked against app 6766485903 |
| Sleep Reset 6762143790 | NEW in-app event "Bedtime Reset for Party Season (Dec 2026)" — CHALLENGE, en-US + ja, 11 territories, 2026-11-28 15:00Z → 2026-12-26 14:59:59Z, deep link aniccaai.com/sleepreset, cards+details COMPLETE. Long description discloses the plan is a paid subscription with a 7-day trial | The live "Holiday Sleep Check 2026" event runs to 12/20 but targets the score only; a second card heads at the party-season bedtime shift and names the subscription honestly | ASC event impressions/PV/DL in US/GB/CA/AU/DE/JP, PT 11/28–12/26 vs PT 11/14–11/20 | event 6837935517, submission f35f189b-db29-4314-a469-16d465dacc0a, **WAITING_FOR_REVIEW**; both events listed under app 6762143790 |
Note for the 11/28 judge: the promo tests shipped 11/20–11/21 (Thankful en-US, Honne/Dhamma/Sleep/CHERIE en-US) finally have post-change days by then; these new surfaces are separate tests, so don't merge the reads.

### 2026-11-22 22:2x JST — growth loop 22:00 (参謀) day close
Ships today: 6/6 apps (Anicca x2: CPP Self-Love&Calm KW fix 10:4x, Jan event 6833871152 WAITING_FOR_REVIEW 14:2x; Honne/Thankful promo, Dhamma/CHERIE/Sleep Dec events 18:5x by Command Code). No new ASC PT day since 10:20 pull (newest PT 11/20): Anicca PT 11/14–20 = 439 imp → 155 PV → 3 DL → Mixpanel unknown (#495) → trial 0 → purchase 0. RC anicca MRR $20 (Reporter 21:41). KEEP/REVERT: none due (all 11/20+ changes HOLD until PT 11/21+ lands; Anicca CPP KW 11/15 judged ~11/23). #498 shorts rendered 18:23, not posted by 21:00 → Muse due 11/23 09:00.

### 2026-11-23 10:5x JST — growth loop 10:00 (参謀)
Funnel (files/attribution-daily-2026-11-23.md; fresh ASC pull 10:18–10:20 JST, newest PT 11/21 for all four reports, processingDate 11/22): Anicca PT 11/15–11/21 = 430 imp → 169 PV → 3 first-time DL (JP search 2 on 11/15, JP app referrer 1 on 11/16) → Mixpanel unknown (#495) → trial 0 → purchase 0. Channels: search 371/7/2, browse 59/49/0, web referrer 0/8/0, app referrer 0/105/1; ct Campaign blank on every row (TikTok/IG/YT/X/blog = unmeasured). RevenueCat 10:3x JST: MRR $20 (projbb7b9d1b, 5 subs) + $4 (projcfa60dd8, 2 subs) = $24, active trials 0, 28d revenue $0. vs 11/22 (PT 11/14–20: 439/155/3): one new PT day (11/21: search 114 imp/0 PV, browse 7/12, app ref 11 PV, 0 DL); the change is the window sliding. **No real metric change** (DL 3, trial 0, purchase 0, MRR $24). Weakest step: search imp→PV 7/371 = 1.9%; PV→DL is just as weak at 3/169 = 1.8%.
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Anicca 6755129214 | promotionalText en-US + ja on live 1.11.0 (version 2bc709e2): Lock Screen how-to line → en-US "Live now: 21 Days of Calmer Holidays. Add the Anicca Lock Screen widget once and get one gentle affirmation a day through Dec 12. 3-day free trial, then a subscription." / ja "開催中：21日間のおだやかな年末（12/12まで）。ロック画面にウィジェットを一度置くだけで、毎日ひとつやさしいアファメーションが届きます。3日間無料、その後はサブスクリプション。" Promo surface last touched 11/14 (9 days). Other 37 locales keep the Lock Screen line as control. PPO d7ffa0d7 untouched (promo is identical in both arms) | Promo text sits at the top of the product page, and the 2026 playbook says to echo a live in-app event there (https://asoagency.io/blogs/app-store-promotional-text; Apple https://developer.apple.com/app-store/product-page/). Visitors from the event card and #498 shorts see the same message → PV→DL above 1.8% | en-US + JP PV→DL, PT 11/23–11/29 vs PT 11/15–11/21; judge 11/30 | loc 0e8c84c3 (en-US) + d75f56dd (ja) readback match 10:4x JST; en-GB unchanged (control); proof marketing/anicca/aso/promo-holiday-event-20261123-1040.json |
KEEP/REVERT: **Anicca CPP keywords (11/15) → KEEP, hypothesis FAILED (no lift).** Search imp→PV PT 11/08–14 = 18/630 (2.9%) → PT 11/15–21 = 7/371 (1.9%); search DL 1 → 2. Detailed shows CPP search traffic of only 5 imp (Self-Love and Calm, PT 11/21); Anxiety/Morning show none. Keyword routing to a CPP gets almost no traffic at our rank and can't explain the impression drop, since impressions are counted per app. Reverting would break the 11/21–22 CPP reads due 11/28–30. No more CPP-keyword ships; the impression drop goes to keyword rank audit #632 (@devin, due 11/24 18:00). Every other change is HOLD: the 11/21–22 CPP keywords and seasonal promos have at most 1 post-change PT day (their pre-set windows end 11/28–30). Holiday event 6837154919 PUBLISHED (PT 11/22 data ~11/24). Jan event 6833871152 still WAITING_FOR_REVIEW.
Other 5 apps → @devin asc-5app-ship-1123 (team/inbox/devin.md), due 18:00 JST, readback rows required. #498 holiday shorts were NOT posted by the 09:00 due → Muse due 12:00 JST (comment on #498). Outlier briefs A/B → Muse, due 18:00.

**11:0x JST addendum (other 5 apps):** Devin's asc-5app-ship-1123 "PASS" (branch devin/asc-5app-ship-1123, 58d79c5f) shipped 0. All 5 proofs say status=blocked ("shell/network prohibited"), and the branch deletes 320 lines of this log, so it is NOT merged. ASC writes no longer go to Devin.
| App | Change | Hypothesis | Metric to watch | ID / state |
|---|---|---|---|---|
| Honne 6759667221 | promotionalText **de-DE + fr-FR** (live 1.0.7; last touched 11/15, outside 7d) → seasonal group-chat line mirroring en-US 11/20, privacy hook kept: de "Feiertags-Gruppenchats und „Lass uns mal treffen“? Nachricht einfügen, sehen, was gemeint sein könnte, und herzlich antworten. Die Person wird nicht benachrichtigt." / fr "Groupes des fêtes et « il faut qu'on se voie » ? Collez un message, voyez ce qu'il peut vouloir dire et répondez avec chaleur. La personne n'est pas notifiée." (was the plain privacy line). es-ES/es-MX/pt-BR keep the old line as control. PPO 20ef37ba (ja) untouched | Timely seasonal promo lifts PV→DL (https://asoagency.io/blogs/app-store-promotional-text; Apple product page guide) | DE/FR PV→DL PT 11/23–12/06 vs es/pt-BR control | loc a20dd9ca + bab1a191 readback match; proof marketing/honne/aso/promo-holiday-de-fr-20261123-1100.json |
| Thankful 6759514159 | BLOCKER (7-day rule): only en-US (11/20) + ja (11/22) promo locales, US Thanksgiving event live (11/22–11/29 PT); next free surface en-US promo 11/27 or a CPP (needs screenshots + review) | — | — | — |
| Dhamma Quotes 6757726663 | BLOCKER (7-day rule): en-US promo 11/20, ja 11/21, Dec event created 11/22; next free en-US 11/27 | — | — | — |
| Sleep Reset 6762143790 | BLOCKER (7-day rule): live 1.0.4 has en-US only (promo 11/20); events 11/20 + 11/22; next free en-US 11/27 | — | — | — |
| STUDIO CHERIE 6766485903 | BLOCKER (7-day rule): en-US promo 11/20, ja 11/21, Dec event 11/22; next free en-US 11/27 | — | — | — |
Ships today: Anicca 1, Honne 1, others 0/4 (blocked by the 7-day rule, not by a person). #632 input: 1.11.0 and 1.10.1 have identical keyword fields (files/anicca-keywords-1.11.0-vs-1.10.1-2026-11-23.json), so the release didn't cause the impression drop.
### 2026-11-23 — 5-app daily ship (@opencode, 11:2x JST)
Reassigned from Devin (branch `devin/asc-5app-ship-1123` NOT reused: it shipped 0 and truncated this log). All 5 latest versions re-read this run via `bash /workspace/team/scripts/ascx.sh versions list`: every one is `READY_FOR_DISTRIBUTION` (none in review). Honne PPO `20ef37ba` untouched. No new locales, no prices, no fake offers. ASC API was reachable; readbacks below are live API reads, not assumptions.
| App | Change (locale, field, old→new) | readback | status |
|---|---|---|---|
| Honne 6759667221 | promotionalText **de-DE + fr-FR** (shipped 11:0x JST by 参謀, independently re-verified here). de old: "Die Person wird nicht benachrichtigt. Füge eine knappe Nachricht oder einen ungelesenen Chat ein, sieh, was gemeint sein könnte, und erhalte eine passende Antwort." → new: "Feiertags-Gruppenchats und „Lass uns mal treffen“? Nachricht einfügen, sehen, was gemeint sein könnte, und herzlich antworten. Die Person wird nicht benachrichtigt." · fr old: "La personne n'est pas notifiée. Collez un message sec ou un chat vu sans réponse, voyez ce qu'elle veut peut-être dire et recevez une réponse qui n'aggrave rien." → new: "Groupes des fêtes et « il faut qu'on se voie » ? Collez un message, voyez ce qu'il peut vouloir dire et répondez avec chaleur. La personne n'est pas notifiée." | de loc `a20dd9ca` and fr loc `bab1a191` readback = exact new strings; es-ES + pt-BR unchanged as control | shipped |
| Dhamma Quotes 6757726663 | BLOCKER (7-day rule): only en-US (promo 11/20) + ja (promo 11/21) version locales; Dec event 6837934616 created 11/22. No CPP, no untouched surface. Next free en-US 11/27 | API readback: 2 locales, both inside the 7-day window | blocked |
| Sleep Reset 6762143790 | BLOCKER (7-day rule): live 1.0.4 has only en-US (promo 11/20); events 11/20 + 11/22. No second locale, new locales forbidden. Next free en-US 11/27 | API readback: 1 locale, inside window | blocked |
| Thankful 6759514159 | BLOCKER (7-day rule): en-US (promo 11/20) + ja (promo 11/22); Thanksgiving event live 11/22. Next free en-US 11/27 | API readback: 2 locales, both inside window | blocked |
| STUDIO CHERIE 6766485903 | BLOCKER (7-day rule): en-US (promo 11/20) + ja (promo 11/21); Dec event 6837934913 created 11/22. Next free en-US 11/27 | API readback: 2 locales, both inside window | blocked |
Proof JSON (status + old→new + API readback) for all five: `marketing/<app>/aso/2026-11-23-ship-proof.json` (honne, dhamma-quotes, sleep-reset, thankful, studio-cherie).
Ships this run: Honne 1 (already live, verified), others 0/4 blocked by the 7-day rule (not by a person, not by lack of network). No version in review touched, no PPO touched, no spend.

**14:2x JST checkpoint (参謀):** no further ship. Today's ships stand at Anicca 1 and Honne 1, and the other 4 are blocked by the 7-day rule. Weakest step is still search imp→PV (1.9%, PT 11/15–21); #632 rank audit is with @opencode. #498 escalation: if there's no post URL by 16:00 JST, the X fallback goes to @x-operator.

### 2026-11-23 22:3x JST — growth loop 22:00 (参謀) day close
Funnel: ASC re-pulled 22:2x JST. Downloads report now has PT 11/22 (proc 11/23); discovery (imp/PV) still newest PT 11/21, so the daily file attribution-daily-2026-11-23.md was kept (stale-write guard). Anicca first-time DL PT 11/22 = **2** (App Store search SA 1, app referrer JP 1) vs PT 11/21 = 0. Window PT 11/16–11/22 DL = 3 (11/15 JP search 2 slid out, 11/22 +2 in). Imp/PV for PT 11/22 not yet published. Mixpanel unknown (#495). RevenueCat 22:3x JST: MRR $20 (projbb7b9d1b, 5 subs) + $4 (projcfa60dd8, 2 subs) = **$24**, active trials 0, revenue 0. **No trial/purchase change.** The 11/22 DL predate today's promo ship (10:5x JST 11/23), so not attributable to it.
Ships today final: Anicca 1 (promo en-US+ja holiday event), Honne 1 (promo de-DE+fr-FR); Thankful/Dhamma/Sleep Reset/CHERIE = logged 7-day-rule blockers (next free surface en-US promo 11/27). KEEP/REVERT for Anicca promo + Honne de/fr: 11/24 10:00 run (first post-change PT day 11/23, published ~11/25 → decidable 11/30).
Muse outlier briefs A/B: no post URL by 21:30 JST (latest Muse file 19:05, admits not posted) → REASSIGNED to @opencode per agreed rule (team/inbox/opencode.md), Muse keeps #498-style review only.

### 2026-11-24 10:3x JST — growth loop 10:00 (参謀)
Funnel (files/attribution-daily-2026-11-24.md; ASC pulled 10:2x JST, discovery+downloads newest PT 11/22): Anicca PT 11/16–11/22 = 428 imp → 131 PV → 3 first-time DL (aso_search 382/4/1, aso_browse 46/38/0, web_referrer 0/10/0, app_referrer 0/79/2). Mixpanel per channel still unknown (#495). Trial/purchase: no change reported at 22:3x 11/23 (MRR $24, trials 0).
Weakest step: search impression→page view 1.0% (382→4); 11/21–22 search imp jumped to 114/90 with 0 PV. Source: https://developer.apple.com/app-store/search/ (result card = icon, name, subtitle, first 3 screenshots), https://developer.apple.com/app-store/product-page-optimization/.
Ship today: Anicca T4331 assigned @opencode (new PPO on screenshot order, else subtitle; deadline 15:00 JST; proof marketing/anicca/aso/2026-11-24-ship-proof.json). Others: Thankful/Dhamma/Sleep Reset/CHERIE 7-day rule until 11/27; Honne promo 11/23.
KEEP/REVERT: Anicca promo + Honne de/fr (11/23) — first post-change PT day 11/23 not yet published (newest PT 11/22); decision moved to 11/30 as planned. Nothing to revert today.
- 2026-11-24 14:2x JST growth loop 14:00 (参謀): Anicca T4331 未着地（@opencode プロセスなし）→ @devin へ付け替え（proof marketing/anicca/aso/2026-11-24-ship-proof.json）。Muse pt確認→@devin T1124-ASC-PT-CONFIRM。
### 2026-11-24 18:2x JST — growth loop 18:00 (参謀, router-only)
Anicca: PPO d7ffa0d7（lock-screen先頭）稼働継続・STOPせず（@pickle 17:5x実測）。subtitle「ロック画面のアファメーション」を 1.11.2 appInfoLocalizations ja へ PATCH → @pickle PK-ASO1（18:0x判断、提出で live）。KEEP/REVERT: PPO は結果待ち（判定は ASC PPO 有意差まで）。Muse own-winner #1 未着地→NOW 再督促。
