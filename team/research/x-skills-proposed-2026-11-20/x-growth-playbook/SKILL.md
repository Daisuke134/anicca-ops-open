---
name: x-growth-playbook
description: >-
  Use when growing a small X account or turning X attention into installs: the
  twice-daily research, record, compare, retarget, act and measure loop, with
  sourced rules for replies, quotes, reposts, originals, connect posts and demo
  clips.
---
# X growth playbook

A daily loop that grows a small X account (under ~5k followers) and turns its attention into product installs. Every rule here cites a row in the source library (default path `marketing/X-GROWTH-SOURCES.md`; IDs like R1, Q1, D1). Read that file before acting. Copy measured winners. Never invent numbers.

## When to use
- Someone asks to grow an X account, "do what the winners do", or plan replies, quotes, reposts or originals.
- Someone asks how to get installs, users or sales from X.
- At the start of every scheduled research run and every posting run for an X account.
- When followers have been flat for 3+ days.

## Hard limits (always)
- Never send DMs. Never mass-follow or follow back by scheme (フォロバ100, ブルバ100). No pods, no paid growth tools, no AI or delegate reply services, no bots that auto-engage.
- Never claim in public that AI or automation does the work.
- Never put other companies' names, or the owner's real name, in post text unless the owner wrote that text.
- Honest numbers only: every number comes from a page, API read or file opened in this run.
- Publishing goes through whatever approval and gate the owner set up. This skill plans and measures; it does not grant permission to post.

## The daily loop
Run it twice a day (morning and evening in the audience's time zone).

1. **Measure ourselves.** Count yesterday's and today's originals, replies to others, self-replies, quotes and reposts. Exact public counts come from the counts endpoint by hour, summed into the owner's local day:
   - `from:<handle> is:reply`
   - `from:<handle> -is:reply`
   - `from:<handle> is:quote`
   - `from:<handle> is:retweet`
   Read median views per type, our 5 best replies, and the views of each reply's parent. Read followers.
2. **Research.** Find at least 2 new winners who state their own numbers:
   - X search: "followers in N days", "replies a day", "first 100 downloads", 「フォロワー」「個人開発」「DL」.
   - Web search for long write-ups: note.com, Substack, dev.to, Indie Hackers, X Articles.
   - Search GitHub for published X skills.
3. **Read.** Open the whole article or post, not the search snippet. Mark it extract or mirror when the full page couldn't be opened.
4. **Record.** Append rows to the source library. Each row: who (handle, followers read now), where (exact URL), when (date), what they did, their numbers, a short exact quote, and our rule. Mark UNVERIFIED claims. Never edit old rows; add corrections.
5. **Compare.** Put our counts next to the benchmarks below and the newest winners.
6. **Update targets.** Change a target only when 2+ independent winners agree, or our own 24h data proves it. Single-source tactics run as labeled experiments.
7. **Act.** Hand the day's targets and rules to the posting routine: write a dated section in the tactics file it reads. If a target is under 70% by midday, the next run spends its whole slot on that action.
8. **Measure again at 24h.** Judge each post on its 24h numbers only [Q3]. Retire formats that lose three times in a row.

## Distilled rules (with sources)
1. **Replies are the engine under ~2k followers: 50 to 100+ a day, every day** [R1 78/day, R2 100+, R3 50 to 100, R5, R6, R7]. Lower volume works too, just slower [J1 10+, J2 5 to 15].
2. **Targeting beats count.** Reply under niche posts that are already rising, inside their first hour [R1, R2, R8, C8]. Volume without targeting stalls [R16, O1].
3. **Reply format:** 1 to 3 lines, first line works alone, and add a number, a step, a catch or a counterpoint. Never a bare compliment [R8, J2, J4].
4. **Answer every reply on your own posts within the first hour, before new outbound work** [R1, R2, R3, R9, C1].
5. **Quote posts that are rising or viral in your niche, adding proof or your own number** [Q1, Q2, Q3, Q4]. In the ranker a quote weighs the same as a reply (5.0) and five times a repost (1.0) [A1].
6. **4 to 6 originals a day, spaced out, beats 10+** [R1, R2, J1]. Numbers get the views [J1, R9].
8. **Profile and pinned post do the converting** [R8, P1, P2, J4].
9. **Installs:** a 15 to 30 s screen recording plus one line, with the link in the first reply [D1, D2, D5, J5].
10. **Followers, installs and money are separate funnels; measure each** [D4, J5, Q1].

## Daily benchmarks (copy, then adjust from our own data)
| action | winners | default target |
|---|---|---|
| replies to others | 78 to 100+ (R1, R2, R6); up to 300 to 700 at the top (R7) | 100 |
| replies back on our own posts | all of them (R1, R2, R3) | 100% within 60 min |
| quotes | ~1/day as a format (Q3), "quote what is climbing" (Q1, Q2) | 4 (derived; no winner stated an exact count) |
| plain reposts of niche winners | no stated number; weight 1.0 (A1) | 3 |
| self-repost of our best post | single source (Q5) | 1, as an experiment |
| originals | 4 to 6 (R1, R2, J1) | 6 to 8 inside any owner cap |
| demo clip posts | D1, D2, D5 | 1 |

An owner-set target that is higher overrides these defaults.

## Picking reply targets
1. Search niche keywords with `-is:reply -is:retweet`, sorted by recency. Keep posts under 60 minutes old.
2. Prefer posts that already have 1k+ views, or authors with 2k to 500k followers in the niche [R2, R8].
3. Prefer posts with few replies so ours sits near the top [O1].
4. Keep 3 tiers in a list [R8; hanamizuki Dream 100]:
   - tier 1: about 5 accounts at 100k+, reply within 15 minutes
   - tier 2: about 10 accounts at 10k to 100k that reply back
   - tier 3: about 10 rising accounts under 10k
5. No more than 20% of daily replies to accounts under 1k that are not already talking to us.

## Quote formats that fit the evidence
- **Receipts:** "We tried this. Here is our number: …" [Q1].
- **Counter with data:** "Our data says the opposite: …"
- **Extend:** "The step that made it work for us: …"
- Line 1 must work without the quoted post. End with one question.
- Only quote posts under ~4h old that are still gaining.

## Distribution (installs, users, sales)
- Show, don't explain. A short screen recording plus one line beat an explained post with the link inside, 19.7K views to 258 [D1]. Recorded demos drove one maker's first 50 downloads [D2].
- Put the link in the first self-reply [D1, Q4] and tag it with a campaign parameter, so installs can be counted.
- Reply in "what are you building / share your app" threads with one screenshot and one line [D3]. Never DM.
- Revenue and download stories from big accounts are quote material [D7].
- Read install sources daily. Store search may beat social links [D4]. Profile clicks may beat link clicks [J5].

## Self-audit metrics (log every run)
- Counts vs targets: replies, reply-backs, quotes, reposts, self-repost, originals, demo clips.
- Median views per type; the share of replies under parents with 1k+ views (target 60%+).
- Followers (daily delta), profile visits if visible, installs by campaign parameter.
- Top 5 replies and top 3 originals with the reason they won (parent size, age, format).

## Anti-patterns (from sources)
- Lazy replies ("great post", "this") [R8].
- Replying to random or off-niche accounts [R14].
- Links in post bodies [D1, J5].
- Chasing viral views that don't convert [Q1].
- Follow-back schemes [J1, J6].
- Stacking several originals minutes apart; space them 60+ min [R1, R2, O3].
- Treating 2023 ranker weights (reply 13.5, "author reply 75") as current [A2 vs A1].

## Skills to load for each step
- Measure: x-daily-self-audit (step 1), x-metrics-reader (24h numbers).
- Research and record: x-research (steps 2 to 4).
- Act: x-reply-targeting (replies), x-quote-formats (quotes), x-pre-post-score (score every draft before the posting gate), x-first-hour-engagement (first 2 hours after each original).
- Never reuse reply text: the ranker repo flags duplicate replies as spam, including Japanese text (botmaker-rules BBQDuplicateTextRepliesProd.bot).

## Daily X Article (added 2026-11-20, owner ask t4192u)
- One native X Article per JST day on @diceai0, written from that week's real team work, with a blog twin on aniccaai.com/blog. Procedure: x-daily-article.
- Benchmarks: @dickiebush about 2 to 3 Articles a week (25 found July–Oct 2026, team/marketing/X-ARTICLES-PLAYBOOK.md §2); the owner's target for us is daily.
- Our baseline: 5 Articles on 2 of the last 14 days (11/06–11/20), best 735 impressions (2120803080086110233, JA YC hackathon), worst 84 (2120788569316851828). Judge Article shapes only at 24h.
- Add `articles` to the self-audit counts.
