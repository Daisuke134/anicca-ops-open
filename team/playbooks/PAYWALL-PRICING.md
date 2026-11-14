> **SUPERSEDED IN PART (2026-10-31 10:34 JST, 参謀):** PART 1's hard-paywall advice is replaced by PART 2 decision D1. Every app gets a soft, closable paywall at the end of onboarding, copied from the winners.

# PAYWALL & PRICING PLAYBOOK — Anicca (id6755129214) + Life Manager Cloud
Written 2026-10-27 JST. Rule: copy proven practice, never invent. Each claim has a source. [UNVERIFIED] = not confirmed from a primary page this turn.

## Sources
- RC = RevenueCat State of Subscription Apps 2026: https://www.revenuecat.com/state-of-subscription-apps/
- RC-HF = RevenueCat SOSA 2026, Health & Fitness: https://www.revenuecat.com/state-of-subscription-apps-2026-health-and-fitness/
- AD-PW = Adapty, "High-performing paywall 2026": https://adapty.io/blog/high-performing-paywall-2026/
- AD-PLAN = Adapty, weekly vs monthly vs annual: https://adapty.io/blog/weekly-monthly-annual-subscription-plan/
- AD-REP = Adapty State of In-App Subscriptions 2026: https://adapty.io/state-of-in-app-subscriptions-report/
- SW = Superwall, how to A/B test a paywall: https://superwall.com/blog/how-to-ab-test-a-paywall
- APPLE = App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- ASC-IAP = ASC Help, submit an IAP: https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-in-app-purchase/
- ASC-NOTES = ASC Help, IAP review notes and screenshot: https://developer.apple.com/help/app-store-connect/manage-in-app-purchases/view-and-edit-in-app-purchase-information/
- RC-COMM = RevenueCat Community, 2.1 rejection thread: https://community.revenuecat.com/general-questions-7/apple-store-rejection-guideline-2-1-performance-app-completeness-6493
- SBI = SBI Growth, Headspace & Calm teardown (2025-01-06): https://sbigrowth.com/insights/headspace-calm-pricing
- PT = PriceTimeline, Calm: https://pricetimeline.com/data/price/calm
- BR = Breethe lifetime comparison: https://breethe.com/sleep-and-meditation-app-guide/compare-evaluate/lifetime-subscription-comparison-breethe-vs-calm-vs-headspace
- MANAI = Manai annual-price comparison (checked 2026-10-09): https://www.manaiapp.com/compare/calm-vs-finch-vs-headspace-vs-i-am-vs-insight-timer/annual-price

## 1. Paywall layout and copy
- Structure beats looks. Changes to plans, trials or duration raise LTV more than changes to visuals or copy (AD-REP; AD-PW: "design is the last thing to optimize").
- Show the annual saving as an explicit number. The median annual plan costs about 3x monthly, roughly 75% off per month (AD-PLAN).
- Test one variable at a time. Run at least 14 days and decide on D30 retained revenue per install, not trial starts (SW).
- Copy: Headspace's customer-centric "Meditation made simple" works better than Calm's superiority angle (SBI; this is a qualitative opinion).
- Teardown of the Calm/Headspace/I Am/Finch/Fabulous in-app paywall layout from screenshots: [UNVERIFIED, not yet captured. TODO: screenshot the US and JP paywalls on a device.]

## 2. Plan lineup and default selection
- Health & Fitness: lead with Annual, with a trial (AD-PLAN decision table). H&F is the only category where annual's share is still growing (AD-PW).
- Three-plan paywalls tend to beat single-plan ones through anchoring. Monthly works as an anchor, rarely as the lead plan (AD-PLAN).
- Annual pre-selected vs monthly pre-selected is a standard A/B test, decided on D30 ARPU (SW reference plan).

## 3. Free trials
- H&F median trial-to-paid is 37.7%, top quartile >51.4% (RC-HF). H&F median download-to-trial is 6.9% (RC-HF).
- Putting the trial on Annual only, not Monthly, is a consistent pattern in top apps. Monthly trials subsidize the least valuable subscribers (AD-PW).
- Calm and Headspace use a 7-day trial (SBI; this was in a search summary, so [UNVERIFIED] against the current paywall).
- 3.1.2: subscription terms must be clear before purchase (APPLE 3.1.2).

## 4. Price points (benchmarks)
- All categories, yearly: most common $30, median $34.80. Monthly: most common $10, median $8. Weekly: most common $5 (RC).
- H&F medians: $9.99 monthly, $39.94 yearly (RC-HF, as quoted by sahha.ai: https://sahha.ai/blog/health-app-monetization-first-month/).
- Adapty, North America medians: weekly $8.49, monthly $13.99, annual $40.99 (AD-PLAN).
- In H&F, expensive annual plans earn 4.5x the LTV per user of cheap ones (AD-PLAN).
- Competitors, US annual: Calm $79.99 (MANAI 2026-10) and $69.99 (PT 2025-06), so prices change; Headspace $69.99; Finch Plus $69.99; I Am Premium $59.99 (MANAI).
- JP storefront prices for these apps: [UNVERIFIED. TODO: read the App Store JP listings' "In-App Purchases" section.]

## 5. Lifetime
- Calm offers Lifetime at $399.99 (BR, PT). Headspace has no lifetime tier now (BR). SBI (2025-01) said Calm $299.99 and Headspace $399.99, which conflicts with BR, so treat SBI as dated.
- Lifetime is a secondary, high-priced anchor, not the lead plan (inferred from Calm's lineup: Annual + Lifetime). Our $59.99 Lifetime is below Calm's $69.99–79.99 *annual* [observation; test raising it].
- Whatever we configure must be visible on every storefront the reviewer uses (see 7).

## 6. Storefronts and localization
- Paywalls must show the localized StoreKit price string, never a hard-coded price (standard StoreKit practice; [UNVERIFIED source this turn]).
- Country-based tests come after pricing and visual tests (AD-PLAN).
- No per-country plan hiding unless the review notes explain it (APPLE 2.1(b)).

## 7. App Review: making IAPs findable
- 2.1(b): "make sure they are complete, up-to-date, visible to the reviewer and functional. If any configured in-app purchase items cannot be found or reviewed in your app, explain the reason in your review notes." (APPLE)
- A new IAP must be in the same submission as the app version (ASC-IAP). Add a review screenshot and notes for each IAP (ASC-NOTES).
- An empty paywall is often caused by the Paid Apps agreement or tax/banking not being done (RC-COMM).
- 3.1.1: restore must exist for restorable IAPs (APPLE).
- Our case: Lifetime showed only on JPN, the reviewer was on US, and we were rejected under 2.1(b). Fix: show every configured product on every storefront.

## 8. Anicca checklist
1. [ ] Show Lifetime (ai.anicca.app.ios.lifetime) on ALL storefronts. Remove the JPN-only gate. (2.1(b))
2. [ ] Review notes: list Monthly, Annual and Lifetime with tap-by-tap paths, and attach an IAP review screenshot. (ASC-NOTES)
3. [ ] Attach every new or unapproved IAP to the same submission as the build. (ASC-IAP)
4. [ ] Confirm Restore Purchases works, and that the paywall terms, privacy, price and period are clear. (APPLE 3.1.1/3.1.2)
5. [ ] Show 3 plans with Annual pre-selected and leading, an explicit "save X%" vs monthly, and Monthly as the anchor. (AD-PLAN)
6. [ ] Put the free trial on Annual only (7 days to match Calm/Headspace). (AD-PW, SBI)
7. [ ] Prices: use localized StoreKit strings only. Benchmark US annual $39.99–69.99 (RC-HF median $39.94; peers $59.99–79.99). Consider testing Lifetime above $59.99, for example near 3–5x annual. [the multiple is a hypothesis, unverified]
8. [ ] A/B test one variable at a time, 14+ days, on D30 ARPU (SW): (a) annual vs monthly default, (b) trial on/off on monthly, (c) price levels.
9. [ ] Later: capture paywall screenshots from Calm, Headspace, I Am, Finch and Fabulous on the US and JP stores to close the [UNVERIFIED] gaps.
10. [ ] Life Manager Cloud: same rules. Lead with annual, show the saving, keep the trial annual-only, and keep products visible on all storefronts. Productivity benchmarks differ, since direct purchase beats trials there (AD-PLAN), so test.

---
# PART 2: COPY-THE-WINNER SPECS PER APP (written 2026-10-31 JST)
Rule (参謀): pricing, paywall and onboarding are copied from the category winner. We don't invent. Every fact below has a link. **UNKNOWN** means not verified on 10/31. Our prices come from /workspace/team/research/pricing-2026-10-31.md (PR = that file).
## Decision log (参謀, 2026-10-31 10:34 JST; every decision copies a winner)
- **D1. Soft paywall everywhere.**
  - Every app shows a closable paywall as the last onboarding step, with a yearly free trial and a trial timeline.
  - Winners: I am (SD-IAM), Motivation (SD-MOT), BetterSleep (SD-BS), Calm (SD-CALM) and Daylio (SD-DAY). ScreensDesign labels all of them "Soft Paywall".
  - The PostHog flag `paywall-ab-test` stays, with default = soft.
  - This supersedes the "hard paywall after onboarding" line in research/pricing-2026-10-31.md and in PART 1.
- **D2a. Zone2Daily: one-time unlock.**
  - Ship a **$7.99 non-consumable `PRO`**, no subscription. Winner: Zones for Training, whose only IAP is "PRO $7.99" (AS-ZONES).
- **D2b. ChiDaily: two one-time unlocks.**
  - Ship **2 non-consumables, "Unlock session video", $2.99 each**.
  - Winner: 7 Minute Chi lists exactly two IAPs, both "Unlock session video $2.99" (AS-CHI).
  - Its v5.2 release note says "the 2 in-app purchases" carry a "2 for 1 offer" (AS-CHI version history).
  - Our mirror:
    - `chidaily.unlock.pack1`: the first premium session-video pack.
    - `chidaily.unlock.pack2`: the second pack.
  - Each is a non-consumable at $2.99 and must be restorable.
  - The winner's 2-for-1 promo is not copied; its mechanics are UNKNOWN.
- **D3. FrostDip ships free (verified 10/31 10:3x JST).**
  - Plunge's US listing reads "Free · Designed for iPhone" with **no** "In-App Purchases" section (AS-PLUNGE).
  - Plunge is a companion app for Plunge hardware, so it has no paid tier to copy.
  - FrostDip therefore ships **free, with no paywall and no IAP**. It is logged as a **distribution / top-of-funnel app**: cross-promote the other Anicca apps from it.
- **D4. Anicca close-paywall offer: YES, copy it.**
  - PaywallPro's I am teardown lists a "Special Offer / Downsell Paywall": "Triggered when users tap close or dismiss", "Offers additional 20% - 50% discount incentive", "Features countdown timer", CTA "Claim Discount" (https://www.paywallpro.app/apps/406-i-am-daily-affirmations).
  - The App Store also lists a discounted "I Am Premium $47.99" next to the $59.99/yr product (AS-IAM), and AppPricer shows the $47.99 product as annual with a 3-day trial (https://apppricer.com/app/874656917). That fits a discount variant, but it is circumstantial.
  - Caveat: PaywallPro is third-party; we have no device capture of our own.
  - Our $29.99 offer against $49.99 is 40% off, inside the observed 20–50% range. Create `yearly.retention` at $29.99/yr. It is queued in PRODUCT-LOOPS.md.

Source key:
- SD-IAM https://screensdesign.com/showcase/i-am-daily-affirmations
- AS-IAM https://apps.apple.com/us/app/i-am-daily-affirmations/id874656917
- SD-BS https://screensdesign.com/showcase/bettersleep-relax-and-sleep
- AS-BS https://apps.apple.com/us/app/bettersleep-relax-and-sleep/id314498713
- SD-CALM https://screensdesign.com/showcase/calm
- AS-FMJ https://apps.apple.com/us/app/5-minute-journal-daily-diary/id1062945251
- SD-MOT https://screensdesign.com/showcase/motivation-daily-quotes
- AS-MOT https://apps.apple.com/us/app/motivation-daily-quotes/id876080126
- AS-MERO https://apps.apple.com/jp/app/id6757545135
- GAP-MERO /workspace/team/gaps (copy at /tmp/mm/x/team/gaps/GAP-honne-merotalk.md)
- SD-UMAX https://screensdesign.com/showcase/umax-become-hot
- AS-UMAX https://apps.apple.com/us/app/umax-become-hot/id6471026798
- SD-DAY https://screensdesign.com/showcase/daylio-journal-daily-diary
- AS-DAY https://apps.apple.com/us/app/daylio-journal-mood-tracker/id1194023242
- AS-BEND https://apps.apple.com/us/app/bend-stretching-flexibility/id1513988468
- AS-EYE https://apps.apple.com/us/app/eye-care-20-20-20/id967901219
- AS-ZONES https://apps.apple.com/us/app/zones-for-training/id1139688415
- AS-PLUNGE https://apps.apple.com/us/app/plunge-official-app/id6450953005
- AS-CHI https://apps.apple.com/us/app/7-minute-chi-calm-move/id1048130885

Shared pattern across every winner we checked (SD-IAM, SD-MOT, SD-BS, SD-CALM, SD-DAY): a personalization quiz, then the paywall as the **last onboarding step**, with a free trial on the yearly plan. Calm, Daylio and Motivation all show a trial **timeline** (today / reminder / billing day) on that paywall. ScreensDesign labels all of these "Soft Paywall" (closable). We copy this as-is (decision D1 below).

Shared SwiftUI building blocks (use these in every app):
- `OnboardingFlow`: a `NavigationStack` driven by `[Step]`, with a progress bar on top and one question per screen. Multi-select uses chip buttons. Answers are stored in `@AppStorage`.
- `TrialTimelinePaywall`, from top to bottom:
  1. Hero headline.
  2. Three-row timeline: "Today: full access", "Day N-2: we remind you", "Day N: billed {price}".
  3. A plan list built from RevenueCat `offering.availablePackages`, with the annual package first and preselected. Price strings come from `storeProduct.localizedPriceString` and are never hard-coded.
  4. CTA.
  5. Restore, Terms and Privacy.
- `RetentionOfferSheet`: shown once when the paywall is dismissed. It offers the `retention` package.

## 1. Anicca (Daily Affirmations): winner **I am – Daily Affirmations** (Monkey Taps)
Facts:
- Onboarding: **25 steps** (SD-IAM).
  - Quiz covers goals, moods and beliefs; asks the user's **name** and **zodiac sign**; lets the user pick an **app icon** and a **feed theme** (SD-IAM).
  - Mid-onboarding it cross-promotes the "Self-Growth Essentials" bundle (SD-IAM).
  - Exact question list and order: UNKNOWN (the full video is paywalled on ScreensDesign).
- Social proof: the store shows 4.8 from 737K ratings (AS-IAM). Whether a rating screen appears inside onboarding is UNKNOWN.
- Paywall:
  - Shown at the **end of onboarding** (SD-IAM).
  - **3-day free trial converting to yearly**, with the yearly price shown as a **monthly equivalent** (SD-IAM).
  - ScreensDesign classifies it as a soft paywall (SD-IAM).
  - Plan order, trial toggle, headline and CTA copy: UNKNOWN.
- Prices (AS-IAM): yearly $59.99, monthly $14.99, lifetime $149.99. Other SKUs at $47.99, $11.99, $9.99 and $69.99 (likely test or offer variants; their purpose is UNKNOWN).
- Close / downsell offer: **verified by teardown**. It appears when the user taps close: a 20–50% discount, a countdown timer, CTA "Claim Discount" (https://www.paywallpro.app/apps/406-i-am-daily-affirmations). See D4.

**What we copy (Anicca build):**
Onboarding, 12 screens. We cut the winner's 25 steps to the categories it is verified to use.
1. Welcome: "Affirmations that change how you think." CTA "Get started".
2. Name: TextField, "What should we call you?". Used in affirmations.
3. Age range (chips).
4. Goals (multi-select): self-esteem, anxiety, love, gratitude, motivation, sleep.
5. Current mood (single-select emoji).
6. Beliefs / spirituality (chips, optional skip).
7. Zodiac sign (grid, optional skip). Copied from I am.
8. Reminders: how many per day (stepper 1–10) and a time window (two `DatePicker`s), then the notification permission prompt.
9. Widget intro: lock-screen widget preview image.
10. Theme picker: grid of 6 backgrounds with a live preview of an affirmation.
11. App icon picker: `UIApplication.setAlternateIconName`.
12. "Building your plan…" loader for 2 seconds, then the paywall.

Paywall: `TrialTimelinePaywall`.
- Annual **$49.99/yr with a 7-day trial** (`ai.anicca.app.ios.yearly.c`), preselected.
- Subline: "$4.17/mo, billed yearly" (monthly-equivalent display copied from SD-IAM).
- Second row: Weekly **$6.99, no trial** (`ai.anicca.app.ios.weekly.c`).
- No monthly plan (PR).
- CTA: "Start my 7-day free trial", or "Continue" when weekly is selected.
- Our trial is 7 days; the winner's is 3 (PR chose 7).

Retention:
- On close, show `RetentionOfferSheet` once, copying I am's downsell:
  - Headline "Limited-Time Discount".
  - Yearly at **$29.99** (`yearly.retention`, 40% off $49.99), with a countdown timer.
  - CTA "Claim Discount".
  - A close X that leads into the app (soft).
- Evidence: D4.

## 2. Honne 本音翻訳: winner **めろとーく | LINE相性分析** (appful Inc.)
Facts:
- JP rating 4.6 from 7,230 ratings; #148 in Utilities (AS-MERO).
- Reads the LINE chat history directly, with no pasting. Shows 16 type categories, graphs, an AI summary and an AI character chat (GAP-MERO).
- Prices (AS-MERO):
  - Pro 1 week ¥500
  - Pro 1 month ¥980
  - Premium 1 week ¥980
  - Ticket packs: 5 for ¥160, 20 for ¥480
- Onboarding screens, paywall layout, trial and retention offer: all UNKNOWN. There is no ScreensDesign or teardown page for it.

**What we copy:** the result-first and type-label hooks the winner verifiably uses. The paywall placement follows PR, which puts it after the first translation preview.

Onboarding, 6 screens:
1. Welcome: "相手の本音、AIが読み解きます".
2. Who it is for (chips): 恋人 / 好きな人 / 友達 / 職場.
3. Privacy promise: "相手にバレません". This mirrors the winner's privacy claim (GAP-MERO). State only what is true.
4. Paste or import chat (TextEditor + a "LINEのトーク履歴を読み込む" file importer for .txt).
5. Analyzing loader.
6. **Preview result**:
   - Show the type label and the first insight.
   - Blur the rest with a blur overlay.
   - Then show the paywall.

Paywall:
- Yearly **$49.99 / ¥7,000 with a 3-day trial**, preselected (`com.daisuke.honne.premium.yearly`).
- Weekly **$7.99 / ¥1,300**.
- No ¥660 monthly.
- CTA: "3日間無料で全部見る".
- Show the trial timeline.

Retention:
- UNKNOWN for the winner. The winner has cheap ticket packs (¥160 for 5), so consider a ticket fallback later.
- For now: no retention offer, and close returns to the blurred result (free tier stays 3 per day per GAP-MERO).

## 3. Sleep Reset: winner **BetterSleep**
Facts:
- **18 onboarding steps** (SD-BS).
- Early social proof: press mentions, testimonials and a star rating (SD-BS).
- Personalization quiz, then a projected-improvement graph and a "You today vs You in a week" screen (SD-BS).
- The paywall follows the quiz with **3 plan options: Individual / Duo / Family**, an "App of the Day" badge and user stats. A feature-list screen comes after it (SD-BS).
- Prices: $59.99, $39.99, $69.99, $99.99, $11.99 and others (AS-BS). The mapping of price to plan is UNKNOWN.
- 7-day trial on yearly (audit doc, citing AS-BS).

Copy, 8 screens:
1. Social-proof splash (rating + "App of the Day"-style badge, using only real badges we have).
2. Sleep problem (multi-select).
3. Bedtime (picker).
4. Wake time (picker).
5. Hours slept (picker).
6. Goal.
7. "You today → You in a week" graph (SwiftUI `Charts`).
8. Notification permission, then the paywall.

Paywall:
- Yearly **$59.99 with a 7-day trial**, preselected.
- Weekly $7.99.
- The Duo/Family tiers are not copied (no Family Sharing SKUs yet).

Retention: UNKNOWN for the winner; none.

## 4. Thankful: winner **5 Minute Journal** (Intelligent Change)
Facts:
- Prices (AS-FMJ):
  - "Annual Journaling Premium" $39.99
  - "**Annual 3d trial $39.99**"
  - 1 month $9.99
  - $24.99 "Annual Subscr (existing users)"
  - $19.99 annual
  - $4.99 monthly
- Onboarding and paywall layout: UNKNOWN (no teardown found).

Copy, 6 screens. The structure is borrowed from the shared pattern, not from the winner:
1. Welcome.
2. Why you journal (multi-select).
3. Morning reminder time.
4. Evening reminder time.
5. First "3 things I'm grateful for" entry (the product demo).
6. Notification permission, then the paywall.

Paywall:
- Annual **$39.99 with a 7-day trial** (PR keeps the 1-week trial; the winner uses 3 days), preselected.
- Monthly $4.99 as the anchor.

Retention: UNKNOWN for the winner; none.

## 5. Dhamma Quotes: winner **Motivation – Daily quotes** (Monkey Taps; 1.1M ratings, #29 H&F)
Facts:
- **41 onboarding steps**, with multi-select questions such as "What's your biggest source of motivation?" (SD-MOT).
- Notification count and time window (SD-MOT).
- Theme picker with a live preview (SD-MOT).
- Soft paywall at the end with a **3-day trial and a trial timeline** (SD-MOT).
- Prices: $47.99, $35.99, $39.99, $19.99, $23.99, $14.99, $11.99, $9.99, $4.99 and $3.99 (AS-MOT). The plan mapping is UNKNOWN.

Copy, 8 screens:
1. Welcome.
2. What draws you to the Dhamma (multi-select).
3. Experience level.
4. Topics (multi).
5. Reminder count and time window.
6. Notification permission.
7. Theme picker with live quote preview.
8. Loader, then the paywall.

Paywall:
- Yearly **$39.99 with a 7-day trial**, preselected.
- Weekly $4.99.
- Trial timeline.

Retention: UNKNOWN; none.

## 6. Aura Looks: winner **Umax**
Facts:
- **6 onboarding steps** (SD-UMAX).
- "Trusted by 1,000,000+ people" right after gender selection; rating prompt very early (SD-UMAX).
- Front selfie and side selfie on separate screens (SD-UMAX).
- **Results blurred: pay for Pro or invite 3 friends** (SD-UMAX).
- No free trial (SD-UMAX).
- Prices: weekly $3.99–9.99, monthly $9.99–24.99 (AS-UMAX).

Copy, 6 screens:
1. Gender.
2. Social proof (our real numbers only).
3. Front selfie.
4. Side selfie.
5. Analyzing.
6. Blurred score.

Paywall: weekly $7.99, yearly $59.99, as already in ASC per the audit. Restore and a re-open path are required (Apple 2.1b).

Retention: retention yearly $44.99 (from the audit). The "invite 3 friends" unlock is optional later.

## 7. AffirmWell: winner **I am** (same as §1)
Copy the Anicca spec in a shorter form: Welcome, Focus, Reminders, Widget, Theme, then the paywall.

Prices (PR factory row): yearly $39.99 with a 3-day trial, weekly $4.99.

## 8. MicroMood: winner **Daylio**
Facts:
- **8 onboarding steps**, including choosing a color palette and an emoji style (SD-DAY).
- Soft paywall at the end of onboarding with a **visual 7-day trial timeline** (today / reminder / trial end) (SD-DAY).
- Prices: $35.99, $23.99, $17.99, $4.99 and a $59.99 "PREMIUM" (AS-DAY). The mapping is UNKNOWN.

Copy, 6 screens:
1. Welcome.
2. Mood emoji style.
3. Color palette.
4. Reminder time.
5. Log your first mood.
6. Notification permission, then the paywall.

Paywall: yearly $39.99 with a 3-day trial (PR factory row), weekly $4.99, trial timeline.

## 9. DeskStretch: winner **Bend: Stretching & Flexibility** (174.7K ratings)
Facts:
- Prices (AS-BEND):
  - "Annual Membership (50% Off)" $29.99 / $39.99
  - "Annual (70% Off)" $19.99 / $23.99
  - Monthly $4.99 / $9.99 / $13.99
- The discount-labelled annual SKUs point to a "% off" badge on annual.
- Onboarding and paywall layout: UNKNOWN.

Copy:
- Our onboarding as built: ProblemEmpathy, PainArea, then the paywall.
- Annual $39.99 with a 3-day trial, shown with a "% off vs weekly" badge.
- Weekly $4.99.

## 10. Eye Break: winner **Eye Care 20 20 20**
Facts:
- Prices (AS-EYE): Weekly $2.99, Monthly $6.99, Yearly $49.99, Pro $1.99.
- Onboarding and paywall: UNKNOWN.

Copy:
- Onboarding as built.
- Yearly $39.99 with a 3-day trial (PR), weekly $4.99.

## 11. Zone2Daily: winner **Zones for Training** (19.2K ratings)
- Facts: its only IAP is "PRO" at $7.99 (AS-ZONES). Onboarding: UNKNOWN.
- **Copy (D2a):**
  - Product: one non-consumable `zone2daily.pro` at $7.99.
  - Paywall: a "Go PRO" sheet at the end of onboarding, closable, with a single "Unlock PRO – $7.99" button and Restore.
  - No trial and no timeline, because a one-time purchase has no trial. This is an exception to D1 that mirrors the winner.
  - The weekly and yearly subscriptions are removed from sale.

## 12. FrostDip: winner **Plunge – Official App** (1.8K ratings)
- Facts: "Free", with no In-App Purchases section on the US listing, checked 10/31 (AS-PLUNGE).
- **Copy (D3):** ship free, with no paywall and no IAP. Treat it as a distribution / top-of-funnel app, with a cross-promo card for Anicca apps in Settings.

## 13. ChiDaily: winner **7 Minute Chi** (2.6K ratings)
- Facts: two IAPs, each "Unlock session video" at $2.99 (AS-CHI).
- **Copy (D2b):**
  - Products: two non-consumables, `chidaily.unlock.pack1` and `chidaily.unlock.pack2`, at $2.99 each. Locked session videos show a lock badge and an "Unlock – $2.99" button.
  - Restore lives in Settings.
  - Paywall: a closable sheet at the end of onboarding offering pack 1.
  - The subscriptions are removed from sale.

## Open items
- The plan-to-price mapping for multi-SKU winners still needs a device capture (US Apple ID).
- D4 rests on one third-party teardown (PaywallPro). Re-check it with a device capture when possible.
