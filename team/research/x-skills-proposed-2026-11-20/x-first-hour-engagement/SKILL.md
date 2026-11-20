---
name: x-first-hour-engagement
description: >-
  Use when the first 60 to 120 minutes after one of our X posts goes live; answering replies, placing the link reply, and the outbound burst that pulls readers back.
---
# X first hour after posting

The ranker gives small accounts a cold-start window. In `param.rs` (xai-org/x-algorithm), posts under 7200 s old with under 200 impressions, from authors under 50,000 followers, can get reserved feed slots. Replies weigh 5.0 against a like's 0.708, and a reply between mutual followers gets a 15.0 boost. So the first two hours decide most of a post's reach.

Adapted from:
- sergebulaev/x-skills, `references/algorithm-heuristics.md`, the "first 30-60 minutes" section (MIT): https://github.com/sergebulaev/x-skills
- hanamizuki/solopreneur, `references/engagement-engine.md`, the reply strategy and the 3:1 post-publish tactic (MIT): https://github.com/hanamizuki/solopreneur
- attainmentlabs/x-open-source-algorithm-skill, the 30-minute rule (MIT): https://github.com/attainmentlabs/x-open-source-algorithm-skill
- Weights: https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs, read 2026-11-15

Note: "3+ substantive replies in 30 minutes earns a second test" (sergebulaev) and "reply engaged by author" multipliers (hanamizuki) are creator claims. The second one is based on the 2023 ranker and does not appear in the current param.rs. Treat both as UNVERIFIED.

## Hard limits
- Every action goes through the owner's posting gate and the one writer. This skill only sequences the work.
- No DMs. No like or follow sprees. No pods and no asking friends to engage.
- Never post the same reply text twice.

## Before posting
1. Run x-pre-post-score on the draft.
2. Write the link reply now, if the post needs a link. Use a tagged campaign link so installs can be counted.
3. Pick 3 reply targets ahead of time: fresh, rising posts in our niche from accounts larger than us (x-reply-targeting).

## Minute 0 to 5
1. Post. Then confirm the public status URL, author and text (public-x-publication-result-verification).
2. Post the link as our first self-reply, if there is one. The main post stays link-free [D1].
3. Post the 3 planned outbound replies. This is hanamizuki's 3:1 tactic. Each must be a real reply that stands alone.

## Minute 5 to 60
1. Check our post's replies every 10 to 15 minutes, or at least twice in the hour.
2. Answer every real reply, newest first, before starting new outbound work [R1, R2, R3, R9].
   - Answer the question with one concrete detail.
   - When someone adds value, thank them by naming what they added, not just "thanks!".
   - Skip spam and bait. Do not argue with bad-faith replies.
3. If a reply adds something genuinely strong, quote it with credit (x-quote-formats), at most once per post.
4. Keep doing normal reply-targeting blocks between checks.

## Minute 60 to 120
1. Read views, replies, quotes, reposts and likes. Log them next to the post URL with the minute mark.
2. Answer any late replies.
3. If the post is clearly beating our median at 2h, plan a self-repost when it settles, roughly 6 to 12 hours later. This is a single-source experiment [Q5]; log it as one.

## What not to do
- Do not delete and repost to "reset" a weak post.
- Do not edit the post to add a link.
- Do not stack a second original within the hour; space originals out [R1].
- Do not chase likes. Likes weigh 0.708; replies and quotes weigh 5.0.

## Log line (per post)
`<status URL> | posted HH:MM | replies answered N/N | 3 outbound done y/n | 60m views V, replies R | 120m views V, replies R | self-repost planned y/n`

## After an X Article (added 2026-11-20)
- Minute 0: post the teaser (1 to 3 lines) with the Article card; self-reply the other-language one-liner; pin it if it is a launch or a series opener.
- Minute 5 to 60: answer every reply on the teaser and on the Article itself; quote the Article once from a relevant thread only if we add a new real number.
- Do not post a second Article the same day to rescue a slow one. Measure at 24h (x-metrics-reader §Articles).
