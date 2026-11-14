# ADVISOR-DMS — drafts only, not sent (2026-11-14 13:21 JST)

成田さん 13:18 JST: successful people already giving us advice on X should be DMed from @diceai0 and asked for product feedback.

**Do not send from this pass.** Parent / 参謀 sends from @diceai0. X Operator does not post these. These are Chat DMs, not public replies (public thank-yous are in `marketing/X-QUEUE-diceai0.md`).

Selection: from the 14-day replies/mentions in [USER-FEEDBACK.md](USER-FEEDBACK.md). Kept founders and operators who gave specific, usable advice. Dropped “let’s connect”, follow-backs, invite-code quotes, tool pitches, and inflated bios with no real advice (e.g. @builtnewai). All ten wrote in English, so the DMs are in English. App Store link is the one requested: https://apps.apple.com/app/id6755129214

Follower counts are public metrics as of 2026-11-14 13:1x JST.

---

## 1. @boardyai — Boardy

- X user id: `1766194375044804608`
- Followers: 53,279 (verified)
- Why: verified connector; endorsed free-first and offered a concrete distribution path
- Advice: “free first is the right call. a longevity media operator with wellness pages could put anicca in front of them.” — https://x.com/boardyai/status/2121044113785307501 (reply to @selawmqt, 2026-11-13 09:50 JST)

DM from @diceai0 (do not send yet):

```
Boardy — thank you for backing free-first, and for the thought about a longevity media operator with wellness pages. We killed the hard paywall: 1.9.14 (in review) makes the first personalized affirmation, the daily feed, and favorites free. When it goes live I'll tell you. If you still think that intro is a fit, I'd like to take you up on it. And if you have two minutes with the app itself: what's the first thing a wellness reader would not understand? https://apps.apple.com/app/id6755129214
```

## 2. @TTrimoreau — Thomas Trimoreau

- X user id: `1480815621076049920`
- Followers: 16,859
- Why: founder, large audience; gave a concrete distribution number, not just encouragement
- Advice: “Try to do 100 replies minimum” — https://x.com/TTrimoreau/status/2121161169557668185 (2026-11-13 17:40 JST)

DM from @diceai0 (do not send yet):

```
Thomas — thank you for the “100 replies minimum.” We were at about 50 a day; I'm raising the floor toward 100. The other leak is still the store: 334 search impressions, 14 page opens, 1 install last week, so replies only help if the app makes sense on first open. If you try Anicca, where would a first-time user bounce? https://apps.apple.com/app/id6755129214
```

## 3. @vovalukashov — Luka Shaw

- X user id: `986522701580984320`
- Followers: 2,940
- Why: Sr SWE at ManyChat, ships tiny products in public (~$204/m); specific ASO practice
- Advice: “Before I name an app I use ASO Mobile to see how often people search for the phrase” — https://x.com/vovalukashov/status/2121282123193876560 (2026-11-14 01:40 JST). Also: “Almost all from App Store search, people type the exact phrase that's in the app name.”

DM from @diceai0 (do not send yet):

```
Luka — thank you for the ASO Mobile tip, and for pointing out that people type the phrase in the app name. 326 of our 334 impressions came from search, but only 14 opened the page, so I think our name is not the phrase they type. I'll check volume before I touch the name. We also made the app free-first (1.9.14 is in review). If you open the listing, does the name plus the first screenshot make it obvious what it does? https://apps.apple.com/app/id6755129214
```

## 4. @abolbuild — Abol

- X user id: `1287429903466614784`
- Followers: 2,261
- Why: operator; asked for the exact guardrail we were missing
- Advice: “can you make the build fail when the plan list belongs to another app?” — https://x.com/abolbuild/status/2120867730689810555 (2026-11-12 22:14 JST)

DM from @diceai0 (do not send yet):

```
Abol — yes. Thank you for asking if the build can fail when the plan list belongs to another app. That's now a team ticket: a release check that fails if the paywall product IDs are not this app's. Apple caught it before we did; that shouldn't happen again. When the check is in, I'll tell you. If you have a minute with Anicca, does anything on the first screen feel like it would fail a similar “is this actually for this user?” test? https://apps.apple.com/app/id6755129214
```

## 5. @faqdev — Facu

- X user id: `2012591602066239489`
- Followers: 1,899
- Why: ships multiple macOS/iOS apps (Orbit, Infall, Tracer); clear monetization advice we are already acting on
- Advice: “Free to try with a paid upgrade works for me too. My apps let people try before paying, either a limited free tier or a trial. Not having a paywall on a first impression matters a lot.” — https://x.com/faqdev/status/2118799512638500903 (2026-11-07 05:15 JST)

DM from @diceai0 (do not send yet):

```
Facu — thank you for saying a paywall shouldn't be the first impression. We agreed, and we killed the hard paywall. 1.9.14 (in review) makes the first personalized affirmation, the daily feed, and favorites free; premium is optional. When it's live I'll come back with the trial number. After you open it, is the free part obvious in the first minute, or does it still feel gated? https://apps.apple.com/app/id6755129214
```

## 6. @DurakTheRobot

- X user id: `1698957023067480064`
- Followers: 1,296
- Why: indie app founder (OweScape, CoupleQuest) plus client work; useful dissent (icon/title vs screenshot)
- Advice: “With 14 of 334 opening the page, I'd start with the icon and title, since that's all people see in search. Screenshots only get a chance once someone taps. That one person downloading straight from search is a nice sign the title already matches what they wanted.” — https://x.com/DurakTheRobot/status/2121256991062667499 (2026-11-14 00:00 JST)

DM from @diceai0 (do not send yet):

```
Thank you — especially for protecting the title. Several people said “change screenshot 1 first,” and that's the one change we'll run for a week against the 14/334 baseline, so the title stays put. Your point that the one search-install means the title already matches is why. When that week is in, I'll share the number. If you glance at the listing, would you have tapped it from search as it is now? https://apps.apple.com/app/id6755129214
```

## 7. @SSShken — Artem Horobchenko

- X user id: `1909713300868280320`
- Followers: 789
- Why: operator shipping with agents; described the exact failure mode (code fine, setting wrong)
- Advice: “all 3 misses in my last agent run were like this: the code was fine, a setting outside it was wrong. I’d add a release check that the paywall product IDs actually belong to this app.” — https://x.com/SSShken/status/2120872515111194632 (2026-11-12 22:33 JST)

DM from @diceai0 (do not send yet):

```
Artem — thank you. “The code was fine, a setting outside it was wrong” is exactly what happened, and your release-check idea is now a ticket: fail the release if the paywall product IDs are not this app's. I'll tell you when that check exists. Separately, Anicca is free-first in 1.9.14 (in review). If you try it, what's the first setting or copy mistake a user would hit? https://apps.apple.com/app/id6755129214
```

## 8. @hermanbjorheim — Herman

- X user id: `991746497694830592`
- Followers: 734
- Why: ships apps; disciplined test design (one screenshot, not the whole set)
- Advice: “0 of 14 is actually cleaner data. i'd swap the first screenshot on its own before redoing the set, it's doing most of the work. change everything at once and you won't know what fixed it” — https://x.com/hermanbjorheim/status/2121137007678152709 (2026-11-13 16:04 JST). Also: “1 out of 14 from the page is the number that jumps out to me. people who tap through are already curious, so it's the screenshots losing them.”

DM from @diceai0 (do not send yet):

```
Herman — thank you for pushing “one screenshot, not the whole set.” That's the test: screenshot 1 becomes a tight crop of the home-screen widget, everything else stays, and we compare a full week to 14 opens from 334 impressions. I'll post the before and after. If you look at the current first screenshot, what should that crop actually show? https://apps.apple.com/app/id6755129214
```

## 9. @MichaelABarroso — Michael Barroso

- X user id: `709866091892367361`
- Followers: 301
- Advice: “334 to 14 says the icon and title aren't stopping the scroll. i'd test the first screenshot before touching anything else” — https://x.com/MichaelABarroso/status/2121399944833577389 (2026-11-14 09:28 JST)

DM from @diceai0 (do not send yet):

```
Michael — thank you. We're taking that literally: the only change is screenshot 1 (a close crop of the home-screen widget). Icon and title stay until we have a week against the 14/334 baseline. I'll share that number with you. If you open the listing, does the current first screenshot stop you, or would you have kept scrolling? https://apps.apple.com/app/id6755129214
```

## 10. @djl997 — Dirk Jan

- X user id: `846786340784148484`
- Followers: 262
- Why: design-minded developer; the clearest product advice on first-run (strong onboarding, no account)
- Advice: “Create a very strong onboarding they could not resist. No account use eg.” — https://x.com/djl997/status/2121335207643275642 (2026-11-14 05:11 JST)

DM from @diceai0 (do not send yet):

```
Dirk Jan — thank you. “A very strong onboarding they could not resist, no account” is now the bar for the first session. Anicca already doesn't require an account; 1.9.14 (in review) also removes the hard paywall, so the first personalized affirmation and the daily feed are free. When you open it, is the first minute irresistible, or does it still feel like setup? What's the one step you would cut? https://apps.apple.com/app/id6755129214
```

---

Status: drafted 2026-11-14 13:21 JST. **0 of 10 sent.**
