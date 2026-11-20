# X growth audit — daily Article + skills coverage (2026-11-20 17:4x JST, Grok Bot 参謀 executor)
Owner ask t4192u (17:21 JST): post an X Article daily; make sure X Operator's winning practice is written as skills.

## X Articles, last 14 days (11/06 17:00 → 11/20 17:00 JST)
Method: public x `search_posts_all` `(from:diceai0 OR from:selawmqt) url:"x.com/i/article"` from 2026-11-06T08:00Z (one page, no more results), cross-checked with `get_users_posts`/`search_posts_all -is:reply -is:retweet` pages for @diceai0 11/14–11/20 (post.fields=article: none) and marketing/X-ACTIONS.md (deleted 11/10 Article).
| account | Articles | days with one | ids (JST) |
|---|---|---|---|
| @diceai0 | 5 (4 live) | 2 of 14 | 11/10 18:07 2120081017570546101 (deleted, X-ACTIONS + X-QUEUE l.116); 11/10 22:55 2120153363891241298 (162 imp); 11/12 16:38 2120783226503405633 (171); 11/12 16:59 2120788569316851828 (84); 11/12 17:57 2120803080086110233 (735) |
| @selawmqt | 0 | 0 of 14 | 7 originals in window, none an Article |
Daily Article is NOT happening: none since 11/12. The 11/14 "X ARTICLE — PUBLISH NOW" item was put on HOLD 11/15 (X-QUEUE-diceai0.md l.862-868).

## Other gaps found
- X-ACTIONS 11/20 14:24 entry: no routine-logged X Operator run between 11/16 15:17 and 11/20 14:24 JST; Day 7–9 posts missed.
- Plain reposts refused by post-gate (logged 11/20 16:12, 17:20).

## Skills vs what X Operator does (skills dir /home/box/agent-data/workflows, read-only here)
No skill covers X Articles at all. Proposed full SKILL.md files: team/research/x-skills-proposed-2026-11-20/<slug>/SKILL.md (same as /workspace/proposed-skills/).
- NEW x-daily-article: one Article per JST day, topic sourcing from team files, pre-score, queue to X Operator, blog twin, 24h measure.
- x-diceai0-posting-run: + the 11-step slot loop from X-ACTIONS (gates, reply-backs from a mention cursor with skip rules, tiered outbound, own-number quote, JA/EN windows + Day series, facts opened, Follows line, repost gap, per-slot log + day tally, daily Article check, owner-ask exception).
- x-daily-self-audit: + Article count 14d, longest routine gap, series misses.
- x-metrics-reader: + Article list/metrics, 24h presim actual, 21:00 no-Article flag.
- x-pre-post-score: + Article surface checks + x_presim --surface article.
- x-growth-playbook: + daily Article section with benchmarks/baseline.
- x-first-hour-engagement: + teaser/self-reply/pin routine after an Article.
- x-reply-targeting: + reply-back cursor, skip list, tiers and hypotheses from the 11/20 log.
