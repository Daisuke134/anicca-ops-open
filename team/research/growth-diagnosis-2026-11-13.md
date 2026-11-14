# @diceai0 duplicates, flat followers, ~1 install: root cause, fix, plan (2026-11-13 23:5x JST)

Trigger: 成田さん 23:38 JST: "you are posting the same post at the same time, twice … why 928 followers … our install is like one … we need 100 installs/day, then 1,000."
Author: 参謀 (executor). Every number has a source. Unknowns say "unknown". No post, delete or paid spend was made for this file.

## 1. The two duplicates: who, when, why

Live X data (x get_posts_by_ids, 23:4x JST 11/13):

| Pair | Post A | Post B | Gap | Written by | Evidence |
|---|---|---|---|---|---|
| Lock Screen how-to | [2121178088218501270](https://x.com/diceai0/status/2121178088218501270) 18:47:20 JST, 23 imp, 0 replies | [2121178259790377201](https://x.com/diceai0/status/2121178259790377201) 18:48:01 JST, 27 imp, 0 replies | 41 s, different media key (the image was uploaded twice = a full second compose) | 参謀 routine "Build in public" (18:40 run), box browser | team/ACTIVITY.md 18:52 line: "X's first Post click landed late, so the browser retry made a duplicate" |
| "We publish our company numbers live" | [2121224120276799878](https://x.com/diceai0/status/2121224120276799878) 21:50:15 JST, 34 imp, 2 likes, 1 outside reply (@Marin_Medici) | [2121224303190401120](https://x.com/diceai0/status/2121224303190401120) 21:50:58 JST, 17 imp, 0 likes, our link reply + 1 outside reply (@sudoaptaj) | 43 s, different media key and t.co | Same 参謀 "Build in public" routine (21:40 run), box browser | ACTIVITY 21:52 POSTED lists only ...303 and says "2 originals"; ...120 is not logged anywhere by that run. Same 40-second retry signature as pair 1. |

Not the cause: X Operator. Its own lines (ACTIVITY 18:37–23:38) show only reply-backs, Day 3 (22:15) and one original (23:16), each "verified via X data", and both duplicates are attributed to grok-sanbo in X Operator's logs (marketing/X-ACTIONS.md lines 2354, 2382). Muse / Mac mini: no POSTING lines for @diceai0 on 11/13.

Root cause, in three layers:
1. **Uncertain-submit retry.** The browser Post button did not visibly confirm within a few seconds, the run clicked/composed again, and the first submit had in fact landed. Nothing forced a timeline read-back before the retry.
2. **The gate was skipped.** RULE POST-GATE already says browser posts must run `post-gate.py` and paste `POST-GATE OK` into the log. Neither 18:47 nor 21:50 has a POST-CLAIM in team/CLAIMS.md or a POST-GATE OK line (the last one for @diceai0 is 16:12). And the gate had no duplicate check anyway: it only checked owner / source / claim / hold.
3. **Too many writers.** The 11/12 exception let any bot post directly on @diceai0. The gate also aliased `x-operator` to `grok-sanbo`, so it could not tell X Operator from 参謀 routines. 3+ writers (X Operator, BIP, No-human spotlight; earlier Muse/Mac) meant the routine that posts least often and verifies least was posting originals.

The 21:5x DONE line said each post went out once, which was wrong: nothing re-read the timeline after posting. Verification was missing, not only prevention.

## 2. What was fixed (this commit)

- `team/scripts/post_gate.py` new check **(e) X duplicate gate** for X create/schedule:
  - `--text-file` (exact text) + `--recent-json` (raw output of `x get_users_posts` for the account, ≤ 10 min old; fail closed if missing or stale).
  - Refuses if the same first line (≥ 20 chars) or ≥ 0.85 similarity (URLs and punctuation ignored) is already live in the last 24 h.
  - `--record-intent` writes the attempt to `team/state/x-post-intents.jsonl` right before clicking Post. A second attempt with the same text is refused until a read-back taken ≥ 3 min after the first attempt still shows it is not live. That is the rule that would have stopped both 11/13 pairs.
  - Postiz path: X integrations need `POST_GATE_X_RECENT`, otherwise refused.
- Owner rows: `x | @diceai0 | x-operator`, `x | @selawmqt | x-operator`. `x-operator` is no longer an alias of `grok-sanbo`, so 参謀 routines are now refused on @diceai0 with "write a draft … instead".
- `team/ACCOUNT-OWNERS.md`: new section "X は X Operator だけが投稿する"; the 11/12 "any bot may post directly" exception is struck through.
- `team/RULES.md`: RULE X-ONE-WRITER (one writer, gate (e), never click Post twice, read back after every post, log DUPLICATE if two ids share a first line).
- Test `team/scripts/test_x_dedup.py`: 11/11 pass. It replays both real duplicates (refused), the 41-s blind retry (refused), the legit retry after a clean read-back 6 min later (allowed), 参謀 posting on @diceai0 (refused), and a stale/missing read-back (refused). Existing `test_post_gate.py` 14/14 and `test_post_gate_wiring.py` 3/3 still pass.

Not deleted (needs 成田さん's OK). If he says yes, delete these:
- Pair 1: delete **2121178088218501270** (23 imp vs 27; neither has replies).
- Pair 2: delete **2121224303190401120** (17 imp, 0 likes vs 34 imp, 2 likes). Its link reply 2121224361239548162 and @sudoaptaj's reply go with it; X Operator then adds the /open link as a reply under 2121224120276799878.

## 3. Followers: the real trend

Source: follower counts logged in team/ACTIVITY.md, BOARD.md, X-ACTIONS.md, metrics snapshots; live value from x get_users_by_username 23:4x JST 11/13.

| When (JST) | Followers | Following |
|---|---:|---:|
| 10/30 17:42 | 493 | 4,498 |
| 10/31 22:00 | 690 | |
| 11/01 23:15 | 831 | |
| 11/02 22:4x | 915 | |
| 11/03 10:41 | 935 | |
| 11/06 14:18 | 924 | 4,502 |
| 11/10 11:06 | 955 (peak) | |
| 11/10 23:00 | 928 | 4,507 |
| 11/11 22:36 | 934 | |
| 11/12 20:35 | 929 | |
| **11/13 23:4x (live)** | **928** | **4,508** |

So: +442 in 4 days (10/30 → 11/03), then **flat for 10 days (935 → 928)**. Following barely moved (4,498 → 4,508), so the jump was not follow-for-follow.

What caused the jump: JP "つながり募集" (connect) posts. 10/31 08:28 self-intro [2116311371772289130](https://x.com/diceai0/status/2116311371772289130) got 3,870 imp / 180 likes, and followers went 494 → 674 that day (+180). [2116816037991825868](https://x.com/diceai0/status/2116816037991825868) 1,889 imp / 92 replies. By 11/06 the same template got 150 and 133 imp (X-ACTIONS line 1522): it wore out and was dropped, and nothing replaced it.

What is being posted now (x get_users_posts, originals only, 11/10–11/13):

| Day (JST) | Originals | Median imp | Max imp |
|---|---:|---:|---:|
| 11/10 | 7 | 50 | 149 |
| 11/11 | 6 | 48 | 121 |
| 11/12 | 25 | 39 | 498 (JP YC hackathon report) |
| 11/13 | 12 | 23 | 85 |

Posting volume went up 2–4x while median reach halved (50 → 23). Several product originals put the App Store link in the body (for example both Lock Screen posts), and X shows link posts to fewer people. Our own 11/13 Layer-5 decision already moves links to the first reply. Outbound replies on 11/13: 17, median 4 imp each. The best post of the 4 days was a first-hand JP event report (498), not a product post.

## 4. Installs: the real numbers

| Metric | Value | Source |
|---|---:|---|
| Anicca App Store impressions, PT 11/06–11/11 | 383 (search 373, browse 10) | files/attribution-daily-2026-11-13.md (ASC Analytics) |
| Product page views | 21 | same |
| First-time downloads | **1** (GB, App Store search, 11/09 PT) | same |
| Prior window 11/04–11/10 | 334 / 14 / 1 | same |
| PT 11/12 | unpublished at 14:17 JST 11/13 | same |
| External users reaching RevenueCat since 11/06 | 1 (the same GB user) | same |
| Trials / purchases since 11/06 | 0 / 0 | same (RC charts) |
| Human App Store link clicks, last 14 d, all channels | 20 | PostHog `app_store_click` traffic_class=human, queried 23:5x JST |
| … of which from X (@diceai0 ct) | 5 (3 on the 11/13 Lock Screen post, first one 6 s after posting, so possibly a preview/own hit) | same |
| … from Instagram bios | 9 | same |
| … from TikTok | **0** | same |
| ct on ASC downloads | blank on every row | attribution file |

Honest read: **X sends ~0 installs.** 5 clicks in 14 days, 0 attributable downloads. The single install in 6 days came from App Store search. App Store page → download is 1/21 = 4.8% (Muse's spec cites a Health & Fitness median of 22–28%).

The big leak is TikTok: 12 Anicca/monk TikTok accounts had **126,891 views in 7 days** (accounts-snapshot-2026-11-12, 205 posts), up from 77,869 the week before, yet **0** TikTok link clicks. Only 1 of 11 TikTok bios has a link (files/install-fix-loop-spec-2026-11-13.md). The audience exists; the path to the App Store doesn't.


2. **X is the wrong engine for installs, and it's being run for volume.** 12–25 originals a day at a median of 23–50 imp, mostly link posts in English to an audience built from JP connect posts. More posts with less reach per post don't add followers. The one thing that grew followers (JP connect posts, 3,870 imp) was dropped when it wore out, with no replacement test.
3. **The store page converts badly and gets almost no search traffic.** 383 impressions a week; 4.8% page → download; US ratings = 1 (JP 48). The winners' engine is ratings velocity + ASO, which we don't have yet.
4. **Measurement is blind.** ct is blank on every ASC row, per-TikTok-post views weren't collected until tonight, and Mixpanel gets 0 external users. Nobody can see which post made which install.

## 6. What the winners did (sources)

- **Oliver Henry / "Larry"** (TikTok slideshows for 2 iOS apps): 6-slide slideshows, hook on slide 1, copied formats from niche competitors, closed the loop on RevenueCat revenue instead of views. Results: 500k views and ~$588 MRR in the first week, 8M views in a peak week, $714 MRR. Key details: he posts the agent's output as a **draft** and publishes by phone with a trending sound, because TikTok deprioritizes API posts. Low views = fix the hook; views without installs = fix the CTA. Sources: https://agent-built.vercel.app/biz/larry-tiktok-agent , https://www.luminarylane.app/blog/from-larry-to-lane/ , https://www.signalcast.app/episode/the-startup-ideas-podcast/i-let-openclaw-run-my-organic-marketing-while-i-sleep (the same episode cites Ernesto Lopez at $70K MRR with this loop).
- **Monkeytaps "I am – Daily Affirmations"** (the category leader): 647.5K+ ratings at 4.8★. They ask for a rating only after the user gets value, rank #1 for "affirmations" plus 1,000+ long-tail keywords, have 1.4M Instagram followers on the Affirmations account, and cross-promote between their own apps. Paid ads exist too, but the article credits ASO + ratings as the main lever. Source: https://thegrowthhackinglab.com/case-studies/monkeytaps-app-studio-12-million/ ; App Store listing https://apps.apple.com/us/app/i-am-daily-affirmations/id874656917
- **Our own winner (@diceai0, 10/31):** the JP connect self-intro (3,870 imp, +180 followers in a day) shows X grows on community posts, not product links.

Takeaway: 100 installs a day for an affirmation app comes from **short-form video with a working link, plus ratings-driven ASO**. Not from X.

## 7. Plan to reach 100 installs/day: top 3 levers

Today: ~0.15 first-time downloads/day (1 in PT 11/06–11/11). Target path: 5/day by 11/20 → 25/day by 11/30 → 100/day by 12/15. Measured daily from ASC first-time downloads (PT, latest processingDate) in files/attribution-daily-*.md.

| # | Lever | Owner | What exactly | Measurable target | Date |
|---|---|---|---|---|---|
| 1 | **Fix the TikTok → App Store path, then scale the Larry format** | **Muse** (TikTok/IG; install-fix loop already running hourly) + **Anicca Marketer** (slideshow production) | (a) ct link `aniccaai.com/go/anicca?ct=<surface>_<handle>_bio` in **all 11** TikTok bios + IG app accounts (Issue #40). (b) Test the in-app-browser → store path on an iPhone without the app installed (#89). (c) Every slideshow: 6 slides, slide 1 = a winner's hook copied from the niche, last slide = "Anicca – lock-screen affirmations, link in bio". Kill a surface after 7 posts below its median; double the top surface. | 11/11 bios with a live ct link (re-read proof); TikTok human clicks ≥ 30/day in PostHog; TikTok-attributed downloads ≥ 5/day | bios 11/14 10:00; clicks 11/18; downloads 11/22 |
| 3 | **X: stop chasing volume; one writer, community growth, honest ct** | **X Operator** (sole @diceai0 writer) | (a) Gate (e) on every post (this commit). (b) Cap originals at 6/day; links go in the first reply, never in the body. (c) Bring back a JP connect/community post 1×/day with a fresh template (the only format that grew followers: 3,870 imp, +180). (d) Weekly first-hand event/number story (11/12 JP hackathon report = 498 imp, best of 4 days). X is for followers and credibility, not installs; it gets no install target. | 0 duplicates (DUPLICATE lines in ACTIVITY = 0); median original ≥ 60 imp; followers 928 → 1,000 | duplicates from now; imp 11/20; 1,000 followers 11/27 |

Measurement guardrail (all owners): ct must show up in ASC Detailed rows. Today they're blank everywhere, so attribution is unknown. Owner: Codex / Dots attribution audit (#80), by 11/20.

Already running, so not new: Muse's install-fix loop (files/install-fix-loop-spec-2026-11-13.md, hourly), PPO d7ffa0d7, 39-locale promo text, RC targeting rule 7488639479. This plan uses those as levers 1–2 rather than starting parallel work.

## 8. Unknowns
- ASC PT 11/12 numbers: unpublished at writing.
- Which downloads came from which channel: unknown, because ct is blank on every ASC row.
- Whether the 3 clicks on the 11/13 Lock Screen ct include a link-preview or own hit (the first came 6 s after posting).
- X follower data from 11/04–11/05 and 11/07–11/09: not logged.
