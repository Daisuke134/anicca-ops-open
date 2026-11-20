---
name: X metrics reader
description: >-
  Use every ~3 hours to read back @diceai0 and @selawmqt post numbers and
  followers from X and update the metrics logs.
---
# X metrics reader
Source of truth: /workspace/team/runbooks/sanbou-x-reader.md.

## Steps
1. Reads only through the X connectors (`x` for public reads, `user-X---4` for @diceai0's own data (verified 2026-11-02: `user-X---4` is @diceai0, `user-X` is @selawmqt read-only, `user-X--diceai0` is actually @Manageraqo, do not use)). Load the x-api-mcp-guide skill first. Never the browser for reads.
2. For @diceai0 and @selawmqt: get profile public_metrics (followers) and each recent post's views, likes, replies, reposts, quotes.
3. Append followers to /workspace/team/metrics/x-followers.csv (date, time JST, account, followers).
4. Update /workspace/marketing/X-METRICS.md with per-post numbers and the top post of the last 24h.
5. Study winners: note which hook, format, topic and target (reply vs own post) won, and write one line on what the next posts should copy into marketing/DISTRIBUTION-ANALYSIS.md when there's a clear pattern.
6. Honest numbers only, as returned this run. Credentials live in /workspace/.secrets (paths only, never print values).
7. Nothing new: end quietly. Blocked: one line in team/LIVE-STATE.md `- YYYY-MM-DD HH:MM JST｜X Operator｜x-reader｜blocked｜result｜blocker｜next`.

## Articles (added 2026-11-20)
8. Each run, list Articles from the last 14 days per account (`search_posts_all` `from:<handle> url:"x.com/i/article"`, then `get_posts_by_ids` with `post.fields=article,public_metrics`). Append to marketing/X-METRICS.md: id, title, age, impressions, likes, replies, bookmarks, quotes.
9. When an Article reaches 24h (±2h), run `python3 team/scripts/x_presim.py actual` so the pre-score gets its actual, and write pred vs actual in the same line.
10. If no Article was published in the current JST day by 21:00 JST, one line in team/ACTIVITY.md: `x-reader | no X Article today on @diceai0`.
