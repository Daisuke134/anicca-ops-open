---
name: x-reply-targeting
description: >-
  Use when picking which X posts to reply under and drafting each reply, for a small account (under ~5k followers) that grows mainly through replies.
---
# X reply targeting and drafting

Replies under the right posts are the main growth engine for small X accounts. This skill covers two things: picking targets, and writing each reply so it earns profile clicks.

Adapted from:
- hanamizuki/solopreneur, `skills/marketer/x-growth` and `references/engagement-engine.md` (MIT): https://github.com/hanamizuki/solopreneur
- sergebulaev/x-skills, `skills/x-reply-drafter` and `references/reply-templates.md` (MIT, Copyright the respective author): https://github.com/sergebulaev/x-skills

Changes from the sources: the DM outreach, the follow-based tactics and the Publora publishing steps are removed. Rows from the team source library (`marketing/X-GROWTH-SOURCES.md`, IDs like R1) are added.

## Hard limits
- No DMs. No follow or unfollow schemes. No pods, no paid tools, no reply services.
- Never say publicly that AI or automation writes the replies.
- No other company names and no owner real name in reply text unless the owner wrote it.
- Every number in a reply must be true and come from a file or page opened this run.
- This skill drafts. Publishing goes only through the owner's gate and posting routine.
- Never reuse reply text. The ranker repo has a duplicate-reply rule that labels repeated reply text as COPYPASTA_SPAM, including a CJK character variant: https://github.com/xai-org/x-algorithm/blob/main/botmaker-rules/scarecrow/bot/BBQDuplicateTextRepliesProd.bot

## 1. Keep a target list (three tiers)
hanamizuki's Dream 100 mix, sized relative to you:

| tier | share of list | size vs you | why |
|---|---|---|---|
| peer | 75% | 0.5x to 2x | they reply back, which starts real conversations |
| stretch | 15% | 2x to 10x | growing audiences that notice regulars |
| aspirational | 10% | 100k+ | big reach per reply, low reciprocity |

Track each account: handle, followers (read now), niche, last time we replied, and whether they ever answered us. Every week, drop accounts that never answer and add new ones.

## 2. Find fresh posts (every slot)
1. Search niche keywords with `-is:reply -is:retweet`, newest first, in each language you post in.
2. Keep posts under 60 minutes old. hanamizuki says 1 to 2 hours; winners in our library say the first hour [R1, R2].
3. Rank what is left:
   - views or likes already climbing
   - few replies yet, so ours sits near the top
   - author inside the target tiers
4. Skip off-niche posts, outrage bait, giveaways, and anything you cannot add a real fact to.
5. Work in blocks: about 15 minutes per block, several blocks a day. hanamizuki's range for accounts under 3k is 20 to 60 replies a day; winners in our library reach 78 to 100+ [R1, R2].

## 3. Decide: reply, quote, or skip
| reply when | quote when (see x-quote-formats) | skip when |
|---|---|---|
| adding to the thread in place | your point deserves its own reach | you have nothing concrete to add |
| answering the author's question | your followers need the original as context | the post is days old, so a fresh post is better |
| building a relationship with the author | the post is rising fast in your niche | the post is from a small account and your take is a dunk |

## 4. Draft the reply
Keep it to 1 to 3 short lines. The first line must work on its own. Include one of: a number, a step, a catch, or a counterpoint [R8].

Shapes, adapted from sergebulaev's reply templates:
- **Answer:** answer their question plainly, then add one real detail or number.
- **Concede then sharpen:** say what is right in their point, then the piece you would push on.
- **Extend:** restate their point briefly, then the next layer that compounds it.
- **Lived experience:** "we hit this" plus what broke, our number, and what we changed.
- **Sharp question:** an edge case that makes the author think. Not "can you explain more?".

Also from hanamizuki: the strongest replies combine a short personal hook, an insight that extends the post, and proof of domain knowledge. Not every reply needs all three.

## 5. Scrub before handing off
- One idea per reply. If you have two ideas, keep the stronger one.
- React to what they actually said, not a strawman.
- No "great point", "this", "so true", "100%".
- No hard sell on someone else's post, and no link in replies to others.
- No em or en dashes. At most one emoji, and none on a serious take.
- Must read differently from every reply we posted today, so check today's log.
- End on a landing or a specific question, not "what do you think?".

## 6. Log
For each reply posted, log: target URL, author followers, parent age and views at reply time, the shape used, and our reply's views and likes at 24h. Every week, list the 5 best replies and what they share (tier, parent age, shape). Shift targeting toward what wins.

## Fixed reply circle (added 2026-11-20, source: X Head of Creator Product via https://x.com/WaitWhatDept/status/2123625798351376576)
- Keep a fixed circle of 5–10 in-niche accounts (AI agents / zero-human company / build in public / Vipassana) and reply to each of them daily with 1–2 thoughtful lines, before picking any one-off targets. Who we reply to trains X on our niche, so never reply outside it.
- Pair the circle replies with our own original posts the same day; prefer short native video or clips when we have one (video is ~40% of impressions).

## What X Operator's log shows works (added 2026-11-20, marketing/X-ACTIONS.md 11/20)
- Reply-backs come before outbound replies, from a `Last mention handled` cursor.
- Skip list used in practice: connect-only replies, thanks-only replies, a person's 3rd looping question in a day, authors who blocked us, unavailable parents.
- Outbound tier actually used: authors with about 2k–9k followers (peer tier), occasionally up to 500k; log followers, parent views and parent age with each reply.
- Recent winner shapes logged as hypotheses: a one-line prompt asking for a one-word answer (@ben_sage, 18 replies at 62 min), one honest dilemma line with no answer (@fre2dm). Treat as experiments until 24h numbers back them.
