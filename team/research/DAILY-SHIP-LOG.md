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
