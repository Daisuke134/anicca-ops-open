# DAILY-SHIP-LOOP — one winner-copied update per app, every day

Written: 2026-11-11 13:05 JST, Grok Bot 参謀.
Order: 成田さん 13:02 JST (told Muse, asked 参謀 to align with Muse directly). Goal: keep shipping a new App Store update on all six iOS apps every day, each copying one feature, screen, or ASO element from that app's niche winner.

Do not route this through legacy Grok Muse/Dots/Codex stand-ins. Talk in this file, `team/TEAM-FEED.md`, and Slack #agents-hq.

Sources already agreed: `team/research/PURCHASE-FIX-2026-11-11.md` (paywall copy-specs, 11/11), `team/research/GROWTH-PLAN-MERGED.md` (funnel + ASO/screenshot work), `team/playbooks/PAYWALL-PRICING.md` (onboarding teardowns). If Muse has a better winner, say so in the #agents-hq thread and we patch this file the same day.

## Owners (1 task, 1 owner)

| Lane | Owner | What |
|---|---|---|
| Code + build | Codex | Implement today's item in `Daisuke134/life-manager`. Cut a version bump. Start an Xcode Cloud build. Do not submit. Hand 参謀 a processed build number and the version string. |
| Submit + metadata / ASO | 参謀 | Attach the build, write What's New + any metadata/ASO for that item, submit with `bash /workspace/team/scripts/ascx.sh`. Verify the result on the real ASC version, not from a chat report. |
| Winner teardown + build-in-public | Muse | Keep the 5-item backlog honest (correct the winner or the next copy target if a teardown shows we are wrong). When a version is submitted, post the update as build-in-public content (Maestro video or screen recording of the copied thing + the store version). 参謀 does not post those accounts. |

Paywall prices and IAP catalog changes stay out of a silent daily ship. If an item needs a new SKU or a price change, 参謀 does that in a named ASC change first, then Codex ships the binary.

## Cadence

- One submission per app per day. The unit of "shipped" is an App Store version that leaves `PREPARE_FOR_SUBMISSION`.
- One version in review at a time, per app. If that app already has a version in `WAITING_FOR_REVIEW` or `IN_REVIEW`, Codex may still land the next item in a new `PREPARE_FOR_SUBMISSION` version, but 参謀 does not submit it until the earlier version is `PENDING_DEVELOPER_RELEASE`, `READY_FOR_SALE` / `READY_FOR_DISTRIBUTION`, or `REJECTED` / `METADATA_REJECTED`.
- Stagger the six submits so they do not hit Apple as one burst (JST, after the build is processed):

  | App | Submit window |
  |---|---|
  | Anicca | 16:00 |
  | Honne | 16:30 |
  | Dhamma Quotes | 17:00 |
  | Sleep Reset | 17:30 |
  | Thankful | 18:00 |
  | STUDIO CHERIE | 18:30 |

  If the build is late, slide that app to the next free 30-minute slot the same day. Do not skip the ship because the window passed. If the build is not processed by 22:00 JST, record the block in `team/TEAM-FEED.md` and submit as soon as it is ready the next morning (still one in review at a time).

- Rotation: stay on an item until its version is live or rejected-and-resubmitted. Then take the next item. After item 5 ships, Muse adds the next 5 from a fresh winner teardown; we do not invent a sixth item.

## Proof = ASC version state

Do not trust a Muse or Codex "we shipped" report. 参謀 reads App Store Connect:

```
bash /workspace/team/scripts/ascx.sh versions list --app <id>
bash /workspace/team/scripts/ascx.sh builds list --app <id>
```

A day counts as shipped for an app only when the new version's state is `WAITING_FOR_REVIEW` or later, the attached build number matches the intended binary, and that fact is appended to `team/TEAM-FEED.md` with the version, build, and state. `PREPARE_FOR_SUBMISSION` with no binary, or a failed Xcode Cloud build, is not a ship.

App IDs: Anicca `6755129214` · Honne `6759667221` · Dhamma Quotes `6757726663` · Sleep Reset `6762143790` · Thankful `6759514159` · STUDIO CHERIE `6766485903`.

## Daily procedure

1. 09:00 JST — 参謀 reads all six version + build lists. If yesterday's version is still in review, today's submit for that app is blocked; Codex still codes the next item.
2. Muse confirms or corrects today's item (default = the next unshipped row below). Corrections land in the #agents-hq thread, then in this file.
3. Codex implements one item per app, bumps the version, starts Xcode Cloud, and posts the build number in the same thread / feed.
4. 参謀 attaches, writes What's New as the one copied thing (no generic "bug fixes"), applies any ASO/metadata for that item, and submits in the stagger window.
5. Muse posts the build-in-public artifact the same day.
6. 参謀 records ASC state in the feed. Unshipped items stay at the top of the next day.

## Rotating backlog (5 concrete items each)

Today, 2026-11-11, is Day 1. Every app starts on item 1 (the already-agreed paywall copy). Existing due times in PURCHASE-FIX stay in force: Dhamma / Sleep / Thankful paywalls by 2026-11-12 18:00 JST; Anicca / Honne / CHERIE by 2026-11-13 18:00 JST. If a binary is not ready today, the item does not rotate; we still treat it as today's first item.

### 1. Anicca — winner **I am – Daily Affirmations** (Monkey Taps), id874656917
https://apps.apple.com/us/app/i-am-daily-affirmations/id874656917

| # | Copy this | Owner split |
|---|---|---|
| 1 | I am paywall in 1.9.11: last onboarding step after a short "Building your plan…" loader; yearly.b ($49.99, 3-day trial) preselected with a trial timeline and monthly-equivalent subline from StoreKit; monthly.b + lifetime as the other two rows; CTA "Start my 3-day free trial" on yearly, "Continue" otherwise; delayed close. Do not show the retention sheet until `yearly.retention` is actually cheaper than annual. Do not submit until the intended build is attached. After the binary can render lifetime, 参謀 flips offering `anicca_iam_copy_20261101` and adds the missing lifetime review screenshot + localizations. | Codex build; 参謀 offering + submit |
| 2 | Onboarding order copied from I am / Mantra: goal → feature preview (lock-screen widget + theme) → loader → paywall. Keep it short (we already cut I am's 25 steps). | Codex; 参謀 submit |
| 3 | ASO from I am + the 11/10 proposal, on the next editable version: en-US subtitle `Self Love & Positive Mantras`; keywords add `widget,lockscreen` and drop title-duplicate terms; ja keywords drop アファメーション / 自己肯定感 / 瞑想 (already in name/subtitle) and add ロック画面, ウィジェット. Description opens with I am's question-style hook, not "AI companion". | 参謀 metadata; ships with Codex's version |
| 4 | First App Store screenshot = a real lock-screen widget with one affirmation line (I am leads with widgets). What's New lists the visible change, never "Bug fixes and performance improvements." | Muse supplies the shot; 参謀 uploads; Codex if the widget UI itself is missing |
| 5 | Rating prompt after value, not in onboarding (I am has no onboarding rating prompt): native request after the 3rd save or the 3rd notification open, once, not on the paywall. Put "Anicca" on the shared image and prompt share after the 3rd favorite. | Codex; 参謀 submit |

### 2. Honne 本音翻訳 — winner **めろとーく \| LINE相性分析** (appful Inc.), id6757545135
https://apps.apple.com/jp/app/id6757545135

| # | Copy this | Owner split |
|---|---|---|
| 1 | めろとーく result-first paywall in 1.0.7: after the first translation / type-label preview, show the type and first insight in the clear, blur the rest, then the soft wall. Yearly ($49.99, 3-day trial already in ASC × 175) preselected; weekly as the anchor; do not show monthly. CTA 「3日間無料で全部見る」 + trial timeline. Close returns to the blurred result (free tier stays 3/day). Do not submit until that binary is attached. | Codex build; 参謀 submit |
| 2 | Privacy claim on the first onboarding screen, only if it is true: 「相手にバレません」 / "The other person is not notified." Winner's hook. | Codex; 参謀 submit |
| 3 | ASO: ja subtitle / keywords lead with 既読スルー, 脈あり, LINE (winner description opens on LINE相性). Keep the 11/11 en-US description opener ("Paste any text, DM, or chat and see what they might really mean."). | 参謀 metadata with the next version |
| 4 | First screenshot = a redacted chat + said-vs-meant (GROWTH-PLAN item 12). After 1.0.7 is live, Muse also puts a Honne TikTok CPP in TikTok/IG bios. | Muse shot + CPP; 参謀 upload |
| 5 | In-app review prompt after the 2nd clear result (not during onboarding), native API, once per version. | Codex; 参謀 submit |

### 3. Dhamma Quotes — winner **Motivation – Daily quotes** (Monkey Taps), id876080126
https://apps.apple.com/us/app/motivation-daily-quotes/id876080126

| # | Copy this | Owner split |
|---|---|---|
| 1 | Motivation-style paywall in a new version after live 1.1.1: last onboarding step after the theme picker + short loader; look up `$rc_annual` / `$rc_monthly` first (added 11/11) with fallback to `annual` / `monthly`; yearly ($39.99, 7-day trial × 175) preselected; monthly as the anchor; CTA "Start my 7-day free trial"; trial timeline Today / Day 5 reminder / Day 7 billed {StoreKit price}. Start the yearly product so Apple presents the trial. Due 11/12 18:00 JST. | Codex build; 参謀 submit |
| 2 | Theme picker with a live quote preview before the paywall (Motivation's last pre-paywall step). | Codex; 参謀 submit |
| 3 | Reminder count + time window, then the notification permission, copied from Motivation's onboarding. | Codex; 参謀 submit |
| 4 | ASO: first screenshot and What's New show a themed daily quote on the Lock Screen / home widget if we have one; otherwise a live theme preview. Keep the concrete-promise description that already converts at 34% page CVR. | 参謀 metadata; Muse shot |
| 5 | Rating prompt after value (Motivation, same studio as I am, does not ask during onboarding): native request after the 3rd favorite or 3rd notification open. | Codex; 参謀 submit |

### 4. Sleep Reset — winner **BetterSleep: Relax and Sleep**, id314498713
https://apps.apple.com/us/app/bettersleep-relax-and-sleep/id314498713

| # | Copy this | Owner split |
|---|---|---|
| 1 | BetterSleep-style yearly-lead paywall in a new version after live 1.0.2: last onboarding step after the "You today → You in a week" graph and the notification prompt; `$rc_annual` / `$rc_weekly` (added 11/11) with fallback; yearly ($59.99, 7-day trial) preselected; weekly as the anchor only (do not advertise the weekly 3-day trial). CTA "Start my 7-day free trial" + trial timeline. Include the ja IAP localizations already in `PREPARE_FOR_SUBMISSION`. No Duo/Family SKUs. Due 11/12 18:00 JST. | Codex build; 参謀 submit (ja IAPs ride along) |
| 2 | "You today → You in a week" projected-improvement graph as a real pre-paywall screen, not a static marketing image. | Codex; 参謀 submit |
| 3 | Early social proof on the first onboarding screen, using only numbers we actually have (ratings, not invented "App of the Day" badges). | Codex; 参謀 submit |
| 4 | ASO: first screenshot = the improvement graph + "7-day free trial" (BetterSleep leads with the outcome, not a feature grid). Submit the already-prepared ja IAP strings with this or item 1, whichever ships first. | 参謀 metadata; Muse shot |
| 5 | Bedtime / wake-time personalization (BetterSleep quiz) before the graph, then the notification prompt. | Codex; 参謀 submit |

### 5. Thankful — winner **Gratitude: Self-Care Journal** (Hapjoy), id1372575227
https://apps.apple.com/us/app/gratitude-self-care-journal/id1372575227
(5 Minute Journal, id1062945251, stays the namesake analog for reminders + "3 things" structure.)

| # | Copy this | Owner split |
|---|---|---|
| 1 | Gratitude-style paywall in a new version after live 1.0.2: last onboarding step after the first "3 things I'm grateful for" entry and the notification prompt; `thankful_annual` ($39.99) preselected with trial timeline; monthly as the anchor (do not advertise a trial on monthly); entitlement `pro`; CTA "Start my 7-day free trial". 参謀 extends the annual 1-week intro from USA+JPN to all remaining territories with `ascx.sh` by 11/12 18:00 JST (no new monthly intros, no price change). Codex paywall due the same time. | 参謀 intro-offer first; Codex build; 参謀 submit |
| 2 | First "3 things I'm grateful for" entry is a required pre-paywall demo, not a skipped optional screen. | Codex; 参謀 submit |
| 3 | Store page CVR is 5.9% (the top leak). Transplant Dhamma's concrete-promise first-screenshot / description layout (GROWTH-PLAN item 12). | Muse shot + copy; 参謀 upload on the next version |
| 4 | Morning and evening reminder times in onboarding, then the notification prompt (5 Minute Journal / gratitude-journal pattern). | Codex; 参謀 submit |
| 5 | ASO subtitle / keywords lead with gratitude journal / 感謝日記, not generic "self-care". What's New names the daily prompt, not "bug fixes." | 参謀 metadata |

### 6. STUDIO CHERIE — winner **XZ(クローゼット) ファッション・洋服 コーディネート** (standing ovation inc.), id909369654
https://apps.apple.com/jp/app/id909369654
(Japan storefront is the one CHERIE ships in. Acloset stays a prior model, not the JP #1.)

| # | Copy this | Owner split |
|---|---|---|
| 1 | XZ-style cap / coordinate paywall in a new version after live 1.0.1: soft sheet at the end of first-run onboarding, and again when the user hits the 30-item cap or taps AI コーデ提案 / 着回しシミュレーション. Closing the wall leaves viewing and the first 30 items free. Single plan: already-approved monthly at the StoreKit price ($0.99 / ¥210). CTA 「クローゼットを無制限にする」 / "Unlock unlimited closet". Entitlement `premium`, offering `default`, package `$rc_monthly` (RC project created 11/11). No yearly and no StoreKit trial in this loop. 参謀 attaches the ASC keys in the RevenueCat dashboard by 11/11 18:00 JST (do not paste keys into chat). Codex ships the wall by 11/13 18:00 JST. Hand the public RC API key only through the existing secrets path. | 参謀 RC keys today; Codex build; 参謀 submit |
| 2 | Gate new registration and new outfit creation only (XZ pattern). Already-registered items and outfits stay viewable for free after the cap. | Codex; 参謀 submit |
| 3 | Store page CVR is 4.2% (also a leak). First screenshot = a real コーディネート result, not a logo. ja What's New names the 30-item free cap and the unlock CTA. | Muse shot; 参謀 upload |
| 4 | Onboarding shows the 30-item free allowance before the paywall, in the same words as the already-approved IAP display name (「31点目から服を追加登録できます」). | Codex; 参謀 submit |
| 5 | ASO: ja keywords / subtitle lead with クローゼット, コーディネート, 着回し (XZ's name and category words). | 参謀 metadata |

## Today's first item (2026-11-11)

These are the Day 1 items. They do not rotate until the matching version is in review or live.

| App | First item |
|---|---|
| Anicca | I am paywall in 1.9.11 (yearly.b 3-day trial preselected, monthly + lifetime, trial timeline, delayed close). Build was being rebuilt at 12:32 JST after 823 failed ITMS-90186. 参謀 submits when the intended build is attached. |
| Honne | めろとーく blur-after-preview paywall in 1.0.7, CTA「3日間無料で全部見る」. Codex has not started this binary yet; start today. |
| Dhamma Quotes | Motivation yearly-lead paywall with `$rc_annual` + 7-day trial timeline. Due 11/12 18:00 JST. |
| Sleep Reset | BetterSleep yearly-lead paywall + ja IAP localizations. Due 11/12 18:00 JST. |
| Thankful | Gratitude annual-preselected paywall + trial timeline (entitlement `pro`); 参謀 extends the annual intro to all territories by 11/12 18:00 JST. |
| STUDIO CHERIE | XZ 30-item cap / coordinate paywall + RC wiring. 参謀 attaches RC↔ASC keys by 11/11 18:00 JST; Codex ships by 11/13 18:00. |

Muse: reply in the #agents-hq thread if any of the six winners above is the wrong #1, or if today's first item should be a different copied thing. 参謀 will patch this file the same day.
