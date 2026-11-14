# Purchase fix — six live iOS apps
Written: 2026-11-11 12:18 JST, Grok Bot 参謀. ASC reads and the Sleep Reset ja localizations were done with `/workspace/asc.py` earlier this run; further App Store Connect work uses `bash /workspace/team/scripts/ascx.sh`. RevenueCat was read and patched via the RevenueCat MCP. Public App Store pages were read 2026-11-11 to name each niche #1. No prices were changed. No secrets in this file.

Goal (成田さん 11:56–11:57 JST): every one of the six apps must be able to take a real purchase, and each paywall must be copied from the #1 app in that niche. Fact: ~92% of users who open an app reach a paywall, yet there were 0 completed new purchases and $0 new revenue in 28 days (Anicca still has 5 old subs, MRR $20; Honne has 2 old subs, MRR $4).

Install truth stays Apple first-time downloads, never RevenueCat new customers. Soft, closable paywall (decision D1 in `team/playbooks/PAYWALL-PRICING.md`) is unchanged.


The Paid Apps agreement, tax, and banking are not the shared break. Evidence: Anicca has 5 live paid subscribers and Honne has 2. Those charges already cleared Apple.

The live subscription products that the current offerings point at are APPROVED, have review screenshots, and have en-US + ja localizations (Sleep Reset ja was missing; fixed this run, still PREPARE_FOR_SUBMISSION). Store-side metadata is not why new purchases are $0.

RevenueCat Paywall charts show 0 paywall viewers on Anicca. Those charts only count RevenueCat Paywalls, not custom in-app paywalls. The live apps use custom paywalls (`paywall_id` is null on every current offering). The leak is therefore at trial / purchase start on a custom paywall: users see the wall, then do not start a StoreKit purchase. RC active trials = 0 on every project, including apps whose yearly plan already has a free trial in ASC for all 175 territories (Anicca yearly.b, Honne yearly, Dhamma yearly, Sleep yearly).

The connected PostHog project (Default project, id 327882) has no `paywall_viewed` / `purchase_started` / `purchase_failed` events in 28 days — only landing-page and `Application Opened` events. The 92% paywall-reach figure is from the earlier Muse / product-loop instrumentation, not from this PostHog project. Codex must emit those events from the custom paywalls so the next loop can see button vs skip vs StoreKit error.

Prices were last raised for new subscribers on 2026-11-01 (existing subs preserved). This brief does not change prices.

---

## 1. Anicca (id6755129214, `ai.anicca.app.ios`)

### Break
Config is good enough to charge; the live paywall is not the I am copy, and nobody is starting the trial. Current RC offering `anicca_live_20261030` (is_current) is yearly.b + monthly.b only. The already-built I am-copy offering `anicca_iam_copy_20261101` (annual + monthly + lifetime) is not current. 0 new trials in 28 days even though yearly.b has a 3-day free trial in all 175 territories.

### Evidence
- Live version 1.9.10 READY_FOR_DISTRIBUTION; 1.9.11 is PREPARE_FOR_SUBMISSION (no binary yet — do not submit).
- ASC (read 11/11): `yearly.b` APPROVED, 3-day trial × 175, screenshot present; `yearly.c` APPROVED, 7-day trial × 175; `monthly.b` APPROVED, no trial; `weekly.c` APPROVED, no trial; `yearly.retention` APPROVED, no trial; `ai.anicca.app.ios.lifetime` APPROVED non-consumable, review screenshot MISSING, no localizations listed. Legacy `annual` / `monthly` / `weekly.b` are DEVELOPER_REMOVED_FROM_SALE. Orphan `Anicca` subscription and consumable `ai.anicca.app.ios` are MISSING_METADATA (not in the current offering).
- RC project `projbb7b9d1b` (this project is shared with leftover Honne / SleepRitual products — do not treat its “190 new customers” as Anicca installs). Overview 11/11: 5 active subs, $20 MRR, $0 revenue 28d, 0 active trials. Entitlement `anicca`.
- Prices already live for new subs (from the 11/01 schedule, not changed today): yearly.b $49.99 / ¥7,000, monthly.b $12.99 / ¥1,900, weekly.c $6.99 / ¥1,100, yearly.c $49.99 / ¥7,000 with a 7-day trial. `yearly.retention` was also moved to $49.99 / ¥7,000 on 11/01, so it is no longer a downsell (it is the same price as annual). Lifetime JP price read back as ¥10,000; US was not in the first price page.
- RC “new customers” in this project are not Apple first-time downloads (14 downloads in 28 days).

### Winner
**I am – Daily Affirmations** (Monkey Taps), id874656917. Public App Store 11/11: US 738,598 ratings, JP 1,778, v7.8.0. https://apps.apple.com/us/app/i-am-daily-affirmations/id874656917

**Winner paywall structure** (store listing + ScreensDesign + PaywallPro teardown, already in PAYWALL-PRICING.md):
- Placement: soft (closable) paywall as the last onboarding step, after a long personalization quiz and a “building your plan” loader.
- Plans: yearly $59.99, monthly $14.99, lifetime $149.99. Other listed SKUs ($47.99, $11.99, $9.99, $69.99) look like tests or offer variants.
- Trial: 3-day free trial on yearly only. Yearly is shown as a monthly equivalent.
- Close / downsell: when the user taps close, a “Special Offer / Downsell” with 20–50% off, a countdown timer, CTA “Claim Discount”.
- Copy / layout details (headline, CTA, exact plan order) were not re-captured on a device today.

### Exact copy-spec for our paywall
Use already-approved products. Do not change prices in this loop.
- Placement: last onboarding step, after a short “Building your plan…” loader. Soft close (delayed X). Decision D1.
- Plans, annual first and preselected: `ai.anicca.app.ios.yearly.b` ($49.99 / ¥7,000, 3-day trial — same trial length as I am). Subline: monthly equivalent from the StoreKit string, never a hard-coded price (“$4.17/mo, billed yearly” in US).
- Second row: `ai.anicca.app.ios.monthly.b` (no trial), as the I am monthly anchor.
- Third row: `ai.anicca.app.ios.lifetime`. Restore, Terms, Privacy on the same screen.
- CTA when yearly is selected: “Start my 3-day free trial”. CTA when monthly or lifetime is selected: “Continue”.
- Trial timeline on yearly: Today = full access; Day 2 = we remind you; Day 3 = billed {localized price}.
- On first close: `RetentionOfferSheet`, headline “Limited-Time Discount”, countdown, CTA “Claim Discount”. Do **not** show `yearly.retention` until its price is actually below annual (it is currently $49.99, same as yearly.b). 参謀 will restore a real discount in a later coordinated price change; Codex should hide the sheet until then rather than offer 0% off.
- 参謀 will not flip the current offering to `anicca_iam_copy_20261101` until the 1.9.11 (or follow-on) binary can render three plans including lifetime. Flipping it under live 1.9.10 risks a broken custom paywall.
- Also in that binary: move the rating prompt after value (already in GROWTH-PLAN item 11); record plan name on purchase start; emit `paywall_viewed` / `purchase_started` / `purchase_failed` / `purchase_cancelled`.

### Fix / owner / due
- Codex (build + paywall), due **2026-11-13 18:00 JST**: ship the copy-spec above in the 1.9.11 binary (or a follow-on). Do not submit 1.9.11 until the intended binary is attached. Existing GROWTH-PLAN items 10–11 stay in force.
- 参謀, due **2026-11-13 18:00 JST**: after that binary can render lifetime, set `anicca_iam_copy_20261101` as the current offering and read it back. Upload a review screenshot + localizations for lifetime if we keep selling it (screenshot is currently MISSING).

---

## 2. Honne 本音翻訳 (id6759667221, `app.rork.hon-ne-honyaku-ai`)

### Break
Store and offering can charge (2 old paid subs exist). The yearly plan already has a 3-day trial in ASC for all 175 territories, but RevenueCat’s product catalog still shows `trial_duration: null`, and RC trials_new / active trials are 0. The live paywall is not the めろとーく result-first copy (blurred preview, then paywall, trial CTA). Monthly is correctly kept out of the current offering.

### Evidence
- Live version 1.0.6 READY_FOR_DISTRIBUTION; 1.0.7 PREPARE_FOR_SUBMISSION (no submit until a real binary).
- ASC: `com.daisuke.honne.premium.yearly` APPROVED, 3-day trial × 175, screenshot present, en-US + ja APPROVED. Monthly and weekly APPROVED, no trial. Group “Premium” localizations APPROVED.
- RC project `projcfa60dd8`, current offering `default`: `$rc_weekly` + `$rc_annual` (yearly has no trial_duration in RC). Overview: 2 active subs, $4 MRR, $0 revenue 28d, 0 trials, 21 RC new customers (not installs; Apple first-time downloads = 15 / 28d). Leftover store identifiers `premium_yearly` / `premium_monthly` still sit on the iOS app — a wrong-id smell, not used in the current offering.
- Prices for new subs (unchanged today): yearly $49.99 / ¥7,000, weekly $7.99 / ¥1,300.

### Winner
**めろとーく | LINE相性分析** (appful Inc.), id6757545135. Public App Store 11/11: JP 7,362 ratings, US 6, v2.14.1. https://apps.apple.com/jp/app/id6757545135

**Winner paywall structure** (JP listing, 11/11, plus GAP-honne-merotalk):
- Plans listed on the store: Pro 1 week ¥500, Pro 1 month ¥980, Premium 1 week ¥980, ticket packs 5 for ¥160 and 20 for ¥480. No yearly SKU on the public IAP list.
- Placement / trial / copy: no ScreensDesign teardown. The product hook is result-first (type label + preview, then pay). Privacy claim: the other person is not notified. Paywall after the first preview is the copy we already adopted in PAYWALL-PRICING.md.
- We do not copy the ticket packs in this loop, and we do not add a ¥500 weekly (our weekly is already $7.99 / ¥1,300). We keep the yearly + 3-day trial that was added to match how subscription winners convert, because めろとーく’s listed IAPs have no trial and no yearly on the store page.

### Exact copy-spec for our paywall
- Placement: after the first translation / type-label preview. Show the type and the first insight in the clear, blur the rest, then the soft paywall. Close returns to the blurred result (free tier stays 3/day).
- Plans, yearly first and preselected: `com.daisuke.honne.premium.yearly` ($49.99 / ¥7,000, 3-day trial — already in ASC). Second row: `com.daisuke.honne.premium.weekly` (no trial). Do not show monthly.
- CTA: 「3日間無料で全部見る」 when yearly is selected; weekly CTA is “Continue”. Trial timeline on yearly.
- Price strings from StoreKit only. Restore / Terms / Privacy on the screen.
- Do not trust RC `trial_duration` for the CTA; use StoreKit intro-eligibility / the known ASC 3-day trial. Codex should still start the yearly product so Apple presents the trial sheet.
- No retention offer in this loop (winner tickets are a later test).
- Events: `paywall_viewed`, `purchase_started`, `purchase_failed`, `purchase_cancelled`.

### Fix / owner / due
- 参謀, done 11/11: confirmed yearly 3-day trial is live in ASC; current offering already has weekly + yearly; no price change.
- Codex, due **2026-11-13 18:00 JST**: ship the preview-blur + trial-timeline paywall in the 1.0.7 binary (or follow-on). Do not submit 1.0.7 until that binary is attached.

---

## 3. Dhamma Quotes (id6757726663, `com.dailydhamma.app`)

### Break
Products are APPROVED and the yearly plan has a 7-day trial in all 175 territories, but RC shows `trial_duration: null`, 0 subs, 0 trials, $0. The current offering’s package keys were only `monthly` / `annual` (not `$rc_*`). If the app looks up `$rc_annual`, the paywall can be empty or the CTA can no-op. That is a plausible code-side break and is now patched in RC (see Fix).

### Evidence
- Live version 1.1.1 READY_FOR_DISTRIBUTION.
- ASC: `com.dailydhamma.app.premium.yearly` APPROVED, 7-day trial × 175, screenshot present, en-US + ja APPROVED. Monthly APPROVED, no trial. Group “dhamma pro” localizations APPROVED. Older `com.dailydhamma.app.yearly` / `.monthly` still exist in the RC catalog; they are not in the current offering.
- RC project `proj86624956`, current offering `default`. Overview: 0 subs, $0 MRR, $0 revenue, 0 trials, 17 RC new customers (Apple first-time downloads = 17 / 28d). Entitlement `premium`.
- Prices for new subs: yearly $39.99 / ¥6,000, monthly $12.99 / ¥1,900.

### Winner
**Motivation – Daily quotes** (Monkey Taps), id876080126. Public App Store 11/11: US 1,079,284 ratings, JP 3,578, v7.8.0. https://apps.apple.com/us/app/motivation-daily-quotes/id876080126

**Winner paywall structure** (ScreensDesign + store IAP list):
- Placement: soft paywall at the end of a long onboarding quiz (41 steps), after notification timing and a theme picker with live preview.
- Trial: 3-day trial with a visible trial timeline (today / reminder / billing day).
- Prices on the US listing (plan mapping not on the store page): $47.99 / $39.99 / $35.99 yearly-range, $11.99 / $9.99 monthly-range, $4.99 / $3.99 weekly-range. JP listing includes 1年 ¥3,990 / ¥3,000 / ¥1,500 and cheaper weekly/monthly SKUs.

### Exact copy-spec for our paywall
- Placement: last onboarding step, after theme picker + short loader. Soft close.
- Plans, yearly first and preselected: `com.dailydhamma.app.premium.yearly` ($39.99 / ¥6,000, 7-day trial already in ASC). Second row: monthly as the anchor (`com.dailydhamma.app.premium.monthly`). Look up `$rc_annual` / `$rc_monthly` (now present) and keep a fallback to `annual` / `monthly`.
- CTA: “Start my 7-day free trial” on yearly. Trial timeline: Today / Day 5 reminder / Day 7 billed {localized price}.
- No retention offer in this loop (unknown for the winner).
- Events as above.

### Fix / owner / due
- 参謀, done 11/11 and read back: added packages `$rc_annual` (pkgec13f05b1b6) and `$rc_monthly` (pkge66d0e8bfc3) on offering `ofrng18fe5c8f69`, attached `com.dailydhamma.app.premium.yearly` and `.premium.monthly` only (not the legacy ids).
- Codex, due **2026-11-12 18:00 JST**: ship the trial-timeline paywall, look up `$rc_annual` first, and start the yearly purchase so Apple presents the 7-day trial. Needs a new version after 1.1.1.

---

## 4. Sleep Reset (id6762143790, `app.rork.vcinrjbl3ke00f07gtlzf`)

### Break
Both products are APPROVED. ASC already has a 7-day trial on yearly (175 territories) and a 3-day trial on weekly. RC’s iOS yearly product still shows `trial_duration: null`, and the current offering’s only package keys were `weekly` / `annual`. The paywall is not leading with yearly + 7-day trial the way BetterSleep does. Japanese localizations were missing on the group and on both subscriptions.

### Evidence
- Live version 1.0.2 READY_FOR_DISTRIBUTION.
- ASC: `sleepreset_yearly` APPROVED, 7-day trial × 175, screenshot present, en-US only (until today). `sleepreset_weekly` APPROVED, 3-day trial × 175, en-US only. Group “Sleep Reset Premium Plan” was en-US only.
- RC project `proj77301666`, current offering `default`. Overview: 0 subs, $0, 0 trials, 6 RC new customers (Apple first-time downloads = 4 / 28d). Entitlement `premium`.
- Prices for new subs: yearly $59.99 / ¥9,000, weekly $7.99.

### Winner
**BetterSleep: Relax and Sleep**, id314498713. Public App Store 11/11: US 390,898 ratings, JP 20,404, v26.20. https://apps.apple.com/us/app/bettersleep-relax-and-sleep/id314498713

**Winner paywall structure** (ScreensDesign + store IAP list):
- Placement: soft paywall after an 18-step onboarding quiz, early social proof, a projected-improvement graph, and “You today vs You in a week”.
- Plans: Individual / Duo / Family. US listing prices include $59.99, $39.99, $69.99, $99.99, $11.99 and others; plan-to-price mapping is not on the store page.
- Trial: 7-day trial on yearly (prior audit + AS-BS).

### Exact copy-spec for our paywall
- Placement: last onboarding step, after the “You today → You in a week” graph and the notification prompt. Soft close.
- Plans, yearly first and preselected: `sleepreset_yearly` ($59.99 / ¥9,000, 7-day trial). Second row: `sleepreset_weekly`. Do not add Duo/Family (no Family Sharing SKUs). Look up `$rc_annual` / `$rc_weekly` (now present) with a fallback to `annual` / `weekly`.
- CTA: “Start my 7-day free trial” on yearly. Trial timeline. Weekly is the anchor, not the lead, even though weekly also has a 3-day trial in ASC — do not advertise a trial on weekly (BetterSleep puts the trial on yearly).
- No retention offer in this loop.
- Events as above.

### Fix / owner / due
- 参謀, done 11/11 and read back:
  - Added ja localizations, all PREPARE_FOR_SUBMISSION (submit with the next Sleep version): group `a5d68e09-16f6-4cb1-af16-6de4b25bf89d` “Sleep Reset プレミアム”; weekly `d60d11cf-8460-408a-ac0a-cdd677c75081` “週間プラン”; yearly `3b53ed59-892a-42f3-9eec-1981497f3524` “年額プラン”. Further ASC work on these uses `ascx.sh`.
  - Added RC packages `$rc_annual` (pkgedd63d90f10) and `$rc_weekly` (pkge08ed03f395) and attached the iOS + test-store products.
- Codex, due **2026-11-12 18:00 JST**: ship the BetterSleep-style yearly-lead paywall and include the new ja IAP strings in the next version.

---

## 5. Thankful (id6759514159, `app.rork.thankful-gratitude-app`)

### Break
Products are APPROVED and the current offering already uses `$rc_annual` / `$rc_monthly`. The 1-week trial exists only in USA and JPN (2 intro offers), not in the other 173 territories. RC shows the iOS annual trial as P1W. 0 trials and 0 subs still mean US/JP users are not starting a purchase either, so the main leak is the custom paywall / CTA, with incomplete trial coverage as a second bug. Entitlement lookup key is `pro` (not `premium`) — the app must request `pro`.

### Evidence
- Live version 1.0.2 READY_FOR_DISTRIBUTION.
- ASC: `thankful_annual` APPROVED, 1-week trial in USA + JPN only (start 2026-02-22), screenshot present, en-US + ja APPROVED. `thankful_monthly` also has a 1-week trial in USA + JPN only. Group “Thankful Pro” localizations APPROVED.
- RC project `proj7aaf9429`, current offering `default` with `$rc_monthly` + `$rc_annual`. Overview: 0 subs, $0, 0 trials, 12 RC new customers (Apple first-time downloads = 2 / 28d). Entitlement `pro`.
- Prices for new subs: annual $39.99 / ¥6,000, monthly $12.99 / ¥1,900 (monthly was raised on 11/01; not changed today).

### Winner
**Gratitude: Self-Care Journal** (Hapjoy), id1372575227, is #1 in this niche by public App Store ratings on 11/11: US 44,994 vs **5 Minute Journal** (id1062945251) at 17,626. https://apps.apple.com/us/app/gratitude-self-care-journal/id1372575227  
5 Minute Journal remains the namesake gratitude-journal analog (US annual “Annual Journaling Premium” $39.99, a listed “Annual 3d trial $39.99”, monthly $9.99 / $4.99) and was the prior playbook target.

**Winner (Gratitude) paywall structure** (US/CA store IAP lists + vendor site, 11/11; no device teardown of the in-app wall):
- Plans: Annual Pro listed at $29.99 and $39.99, monthly Pro at $4.99 / $6.99, quarterly $9.99, plus other “Gratitude Pro” SKUs ($34.99, $47.99, $49.99 on some storefronts). The website quotes $39.99 / year and $6.99 / month and says the yearly plan includes a free trial for eligible users. AppsLupa lists a 1-month trial on some annual and monthly SKUs and a 7-day trial on a $34.99 yearly SKU. Exact onboarding placement is UNKNOWN; we keep the shared winner pattern (paywall as the last onboarding step).

### Exact copy-spec for our paywall
- Placement: last onboarding step, after the first “3 things I’m grateful for” entry and the notification prompt. Soft close.
- Plans, annual first and preselected: `thankful_annual` ($39.99 / ¥6,000, 1-week trial — already in US/JP, to be extended). Subline: monthly equivalent from StoreKit. Second row: `thankful_monthly` as the anchor. Do not change the $12.99 monthly price in this loop.
- CTA: “Start my 7-day free trial” on annual. Trial timeline. Do not advertise a trial on monthly (even though monthly currently has a US/JP intro — winners put the trial on annual). Entitlement to unlock: `pro`.
- No retention offer in this loop.
- Events as above.

### Fix / owner / due
- 参謀, done 11/11: confirmed offering mapping and the 2-territory trial gap.
- 参謀, due **2026-11-12 18:00 JST**: extend the 1-week free trial on `thankful_annual` to the remaining territories with `ascx.sh` (copy the existing USA/JPN intro; do not add new trials on monthly; do not change prices). Read back the intro count.
- Codex, due **2026-11-12 18:00 JST**: ship the copy-spec (annual preselected, trial timeline, entitlement `pro`, events).

---

## 6. STUDIO CHERIE (id6766485903, `app.rork.xhozd938ie79zdqd5plem`)

### Break
This was the only app with no purchase path at all. A monthly subscription already existed and is APPROVED, but there was no RevenueCat project, so the app could not present a working offering. There is no yearly SKU. There is no in-app paywall wired to StoreKit / RC.

### Evidence
- Live version 1.0.1 READY_FOR_DISTRIBUTION.
- ASC: one subscription group “STUDIO CHERIE Closet”. Product `app.rork.xhozd938ie79zdqd5plem.closet.monthly` APPROVED, ONE_MONTH, no intro offer, screenshot present, en-US + ja APPROVED. Display names already describe the 30-item cap (“Add beyond 30 items…” / 「31点目から服を追加登録できます」). US $0.99, JP ¥210 (read back 11/11). No other IAP.
- RC: no project existed this morning. Apple first-time downloads = 2 / 28d; page→install 4.2%.

### Winner
**XZ(クローゼット) ファッション・洋服 コーディネート** (standing ovation inc.), id909369654, is #1 in this niche on the Japan App Store, which is the storefront CHERIE actually ships in. Public ratings 11/11: JP 4,094 vs Acloset 170, Alta Daily 108, Whering 79, Stylebook 150. US ratings for XZ are only 37; the US AI-closet leader by ratings is Alta Daily (18,995), then Whering (12,099). https://apps.apple.com/jp/app/id909369654

Acloset (id1542311809) stays the team’s prior AI-closet model (Basic $3.99 / mo or $27.99 / yr, Premium $9.99 / $59.99, free up to 100 items). It is not the JP niche #1 by public ratings, and we are not inventing a $27.99 yearly SKU in this loop.

**Winner (XZ) paywall structure** (JP App Store IAP list 11/11 + official “有料プランについて” / release notes):
- Plans on the JP listing: 有料プラン ¥200, 広告非表示プラン ¥150 (listed twice). No yearly SKU on the store page.
- Trial / placement: a 90-day in-app お試し期間 (account trial, not a StoreKit intro on the listing). After it ends, new item registration and new outfit creation are gated; already-registered items and outfits stay viewable for free. Since 5.1.7, a user can watch a video ad to register 1 item/day. Paywall is a “有料プラン” screen (release 5.1.22 fixed it failing to load).
- We do not copy the 90-day StoreKit trial (it is an account trial, and a 90-day intro would defer revenue for a quarter). We already have a 30-item free cap, which is the same *kind* of gate (free closet, pay to add / generate more).

Our $0.99 / ¥210 monthly is Apple’s closest standard tier to XZ’s ¥200. That is the price we copy. No yearly is created, because the winner has none on the public page.

### Exact copy-spec for our paywall
- Placement: soft, closable sheet (1) at the end of first-run onboarding, and (2) when the user hits the 30-item cap or taps AI コーデ提案 / 着回しシミュレーション (XZ gates new registration and new outfits, not viewing). Closing the wall leaves viewing and the first 30 items free.
- Plan: a single row, `app.rork.xhozd938ie79zdqd5plem.closet.monthly` at the localized StoreKit price ($0.99 / ¥210). No yearly in this loop. No ad-removal SKU (we are not shipping ads).
- CTA: 「クローゼットを無制限にする」 / “Unlock unlimited closet”. Restore / Terms / Privacy on the screen.
- Entitlement: `premium`. Offering: current `default`, package `$rc_monthly`.
- No StoreKit free trial in this loop (winner’s 90-day try is in-app; our free cap is the 30-item allowance already described on the IAP).
- Events as above.

### Fix / owner / due
- 参謀, done 11/11 and read back:
  - Confirmed the monthly IAP is APPROVED at $0.99 / ¥210. Did not invent a yearly price.
  - Created RevenueCat project `projc98adb88` (https://app.revenuecat.com/projects/c98adb88), App Store app `app269a228732` (bundle `app.rork.xhozd938ie79zdqd5plem`), product `proddd8cc55bfa` = `app.rork.xhozd938ie79zdqd5plem.closet.monthly`, entitlement `premium` (`entl7cffd75f27`), current offering `default` (`ofrng8fb4d650f5`) with package `$rc_monthly` (`pkge64bd6e74e1`) attached to that product.
  - ASC API key and subscription key are **not** yet configured on this new RC app (a new project cannot copy keys from a sibling in another project; do not paste keys into chat). 参謀 will attach them in the RevenueCat dashboard, due **2026-11-11 18:00 JST**, then read `app_store_connect_api_key_configured` back as true.
- Codex, due **2026-11-13 18:00 JST**: implement the paywall + RevenueCat SDK in a new CHERIE version (current live is 1.0.1), using the public RC API key for `projc98adb88`, entitlement `premium`, offering `default`, package `$rc_monthly`. Hand the API key only through the existing secrets path, never in a chat message or this brief. Submit that version with the paywall so review can exercise the already-approved IAP.

---

## What was not changed
- No subscription prices.
- Anicca current offering left on `anicca_live_20261030` until the binary can render lifetime.
- 1.9.11 and Honne 1.0.7 left PREPARE_FOR_SUBMISSION with no submit.
- Thankful intro offers not yet expanded beyond USA/JPN (queued 11/12, `ascx.sh`).

## Event contract for Codex (every app)
Emit, at least: `paywall_viewed`, `purchase_started` (with plan / product id), `purchase_failed` (with error), `purchase_cancelled`. Without these, the next loop cannot tell a skipped wall from a dead CTA from a StoreKit error.
