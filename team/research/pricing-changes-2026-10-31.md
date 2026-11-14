# Pricing changes applied — 2026-10-31 (JST)
Done via the ASC API (team/pricing/lib.py) and the RevenueCat connector. Every change uses preserveCurrentPrice=true, so existing subscribers keep their price and Apple sends no price-increase consent. The old entries below show preserved=true in the readback.
Approved products: the new price starts 2026-11-01. Unreleased products: the new price is in effect now. All 175 territories are equalized from the US price point, with JP set to the nearest JP tier.
Readback raw data: team/pricing/verify.json. Logs: team/pricing/*.log.

| Product | Old (preserved for existing subs) US / JP | New for new subs US / JP | Effective | Readback |
|---|---|---|---|---|
| ai.anicca.app.ios.yearly.c | $—(new) / ¥—(new) | $49.99 / ¥7000 | now (initial price) | OK: 175 territories read back; newest entry dates {'': 175} |
| ai.anicca.app.ios.weekly.c | $—(new) / ¥—(new) | $6.99 / ¥1100 | now (initial price) | OK: 175 territories read back; newest entry dates {'': 175} |
| ai.anicca.app.ios.monthly.b | $9.99 / ¥500/1500 | $12.99 / ¥1900 | 2026-11-01 | OK: 175 territories read back; newest entry dates {'2026-11-01': 175} |
| ai.anicca.app.ios.yearly.b | $29.99 / ¥2000/5000 | $49.99 / ¥7000 | 2026-11-01 | OK: 175 territories read back; newest entry dates {'2026-11-01': 175} |
| ai.anicca.app.ios.yearly.retention | $7.99/29.99 / ¥1300/5000 | $49.99 / ¥7000 | 2026-11-01 | OK: 175 territories read back; newest entry dates {'2026-11-01': 175} |
| com.daisuke.honne.premium.yearly | $39.99 / ¥1810/6000 | $49.99 / ¥7000 | 2026-11-01 | OK: 175 territories read back; newest entry dates {'2026-11-01': 174, '2026-04-25': 1} |
| com.daisuke.honne.premium.monthly | $4.99 / ¥660 (preserved, existing subs only) | unchanged $14.99 / ¥2500 (since 2026-04-25) | — | REVERTED: the scheduled $12.99 was deleted (157× HTTP 204). Readback: USA [4.99 preserved, 14.99], JPN [660 preserved, 2500] |
| com.dailydhamma.app.premium.yearly | $19.99 / ¥3000 | $39.99 / ¥6000 | 2026-11-01 | OK: 175 territories read back; newest entry dates {'2026-11-01': 175} |
| com.dailydhamma.app.premium.monthly | $4.99 / ¥800 | $12.99 / ¥1900 | 2026-11-01 | OK: 175 territories read back; newest entry dates {'2026-11-01': 175} |
| thankful_annual | $29.99 / ¥5000 | $39.99 / ¥6000 | 2026-11-01 | OK: 175 territories read back; newest entry dates {'2026-11-01': 175} |
| thankful_monthly | $4.99 / ¥800 | $12.99 / ¥1900 | 2026-11-01 | OK: 175 territories read back; newest entry dates {'2026-11-01': 175} |
| sleepreset_yearly | $39.99 / ¥6000 | $59.99 / ¥9000 | 2026-11-01 | OK: 175 territories read back; newest entry dates {'2026-11-01': 175} |
| aura_pro_annual | $—(new) / ¥—(new) | $39.99 / ¥6000 | now (initial price) | OK: 175 territories read back; newest entry dates {'': 175} |
| aura_pro_annual_retention | $—(new) / ¥—(new) | $39.99 / ¥6000 | now (initial price) | OK: 175 territories read back; newest entry dates {'': 173, '2026-10-30': 2} |
| aura_pro_weekly | $—(new) / ¥—(new) | $4.99 / ¥800 | now (initial price) | OK: 175 territories read back; newest entry dates {'': 175} |
| deskstretch.annual | $29.99 / ¥5000 | $39.99 / ¥6000 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| deskstretch.monthly | $4.99 / ¥800 | $12.99 / ¥1900 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| chidaily.annual | $34.99 / ¥—(new) | $39.99 / ¥6000 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'': 20, '2026-10-30': 155} |
| chidaily.monthly | $4.99 / ¥800 | $12.99 / ¥1900 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| frostdip.annual | $29.99 / ¥5000 | $39.99 / ¥6000 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| frostdip.monthly | $6.99 / ¥1100 | $12.99 / ¥1900 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| frostdip.weekly | $1.99 / ¥300 | $4.99 / ¥800 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| zone2daily.annual | $29.99 / ¥5000 | $39.99 / ¥6000 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| zone2daily.monthly | $4.99 / ¥800 | $12.99 / ¥1900 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| zone2daily.weekly | $1.99 / ¥300 | $4.99 / ¥800 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| eyebreakisland.annual | $29.99 / ¥5000 | $39.99 / ¥6000 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| eyebreakisland.monthly | $4.99 / ¥800 | $12.99 / ¥1900 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| eyebreakisland.weekly | $1.99 / ¥300 | $4.99 / ¥800 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| affirmflow.annual | $29.99 / ¥5000 | $39.99 / ¥6000 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| affirmflow.weekly | $2.99 / ¥500 | $4.99 / ¥800 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| micromood.annual | $29.99 / ¥5000 | $39.99 / ¥6000 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |
| micromood.monthly | $4.99 / ¥800 | $12.99 / ¥1900 | 2026-10-30 | OK: 175 territories read back; newest entry dates {'2026-10-30': 175} |

## Intro offers (readback, 175 territories each)
- ai.anicca.app.ios.yearly.c: 7-day free trial (ONE_WEEK, from 2026-10-30)
- com.daisuke.honne.premium.yearly: 3-day free trial (new)
- com.dailydhamma.app.premium.yearly: 3-day trial ends 2026-11-01, then 7-day from 2026-11-02
- sleepreset_yearly: 3-day trial ends 2026-11-01, then 7-day from 2026-11-02
- com.aniccafactory.frostdip.annual: 7-day trial
- thankful_annual: the existing 1-week trial is kept (US and JP only)

## New products
- ai.anicca.app.ios.yearly.c (ASC 6829088945) and ai.anicca.app.ios.weekly.c (ASC 6829088753), in group "Anicca Premium B" (22027036).
  - Each has en-US and ja localization, a review screenshot (copied from yearly.b), availability in all territories, and prices.
  - State is MISSING_METADATA until they are attached to the next app version.
- RevenueCat project anicca:
  - prodb23225e5e5 (yearly.c) and prodf8f41e5911 (weekly.c) are attached to entitlement "anicca".
  - Offering default_v2 (ofrng1eeda3c7bc), not current, has $rc_annual → yearly.c and $rc_weekly → weekly.c.

## Not changed / reverted
- com.daisuke.honne.premium.monthly: I scheduled $12.99/¥1,900 and then deleted it, because that would have lowered the current new-user price of $14.99/¥2,500. The ¥660 only exists as a preserved price for existing subscribers, so new users never see it. The product is not removed from sale.
- Honne weekly ($7.99/¥1,300) and Sleep weekly ($7.99) are already above the floor.
- STUDIO CHERIE monthly, SleepRitual and test apps are not touched.
- FrostDip already had a group (21966024) with weekly 6760225308, monthly 6760225483 and annual 6760225430, so no duplicate was created. Prices were raised and a 7-day trial was added.

## Winner mirror redo — 2026-10-31 12:30 JST (replaces the floor prices above for these products)
Rule: copy the category winner's US and JP price exactly. Winner pages fetched this run (apps.apple.com, 12:08 JST). Script: team/pricing/redo.py with j_redo.json; preserveCurrentPrice=true. Approved products: the future 11-01 price was deleted and re-set, starting 2026-11-01. Unreleased: effective now. Readback: verify.json key `winner_mirror_2026-10-31`.
Note: redo.py also equalized the other 173 territories from the US price point (as in the first pass). Only US and JP come from the winner's page.

| Product | Old US / JP (new subs) | New US / JP | Start | Winner | Link |
|---|---|---|---|---|---|
| ai.anicca.app.ios.yearly.b | $49.99 / ¥7,000 (sched.) | $59.99 / ¥2,100 | 11-01 | I am | https://apps.apple.com/us/app/id874656917 , https://apps.apple.com/jp/app/id874656917 |
| ai.anicca.app.ios.monthly.b | $12.99 / ¥1,900 (sched.) | $14.99 / ¥1,500 | 11-01 (JP ¥1,500 already current) | I am | same |
| ai.anicca.app.ios.yearly.retention | $49.99 / ¥7,000 (sched.) | $59.99 / ¥2,100 | 11-01 | I am | same |
| affirmflow.annual | $39.99 / ¥6,000 | $59.99 / ¥2,100 | now | I am | same |
| com.dailydhamma.app.premium.yearly | $39.99 / ¥6,000 (sched.) | $47.99 / ¥3,990 | 11-01 | Motivation (Monkey Taps) | https://apps.apple.com/us/app/id876080126 , /jp/ |
| com.dailydhamma.app.premium.monthly | $12.99 / ¥1,900 (sched.) | $11.99 / ¥1,500 | 11-01 | Motivation | same |
| thankful_monthly | $12.99 / ¥1,900 (sched.) | $4.99 / ¥680 | 11-01 | Gratitude | https://apps.apple.com/us/app/id1372575227 |
| sleepreset_yearly | $59.99 / ¥9,000 (sched.) | $59.99 / ¥4,500 | 11-01 | BetterSleep | https://apps.apple.com/us/app/id314498713 |
| eyebreakisland.annual / monthly / weekly | $39.99/$12.99/$4.99 · ¥6,000/¥1,900/¥800 | $49.99/$6.99/$2.99 · ¥8,000/¥1,100/¥500 | now | Eye Care 20 20 20 | https://apps.apple.com/us/app/id967901219 |
| micromood.annual / monthly | $39.99/$12.99 · ¥6,000/¥1,900 | $35.99/$4.99 · ¥4,800/¥700 | now | Daylio | https://apps.apple.com/us/app/id1194023242 |
| aura_pro_weekly | $4.99 / ¥800 | $3.99 / ¥600 | now | LooksMax AI | https://apps.apple.com/us/app/id6474518292 |
Unchanged: thankful_annual ($39.99/¥6,000 = Gratitude already). Honne (３秒敬語 has only ¥550/mo, no match for our tiers), Zone2/ChiDaily/FrostDip/DeskStretch (winner has no subscription list), Anicca yearly.c/weekly.c, aura_pro_annual(+retention): not changed, no comparable winner sub price.
Retention: yearly.retention now equals yearly.b ($59.99/¥2,100), so it is no longer a discount. Retention screen should use ai.anicca.app.ios.monthly.b ($14.99/¥1,500, I am's monthly) until a win-back/promotional offer on yearly.b exists.
