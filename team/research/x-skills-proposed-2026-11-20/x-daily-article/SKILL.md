---
name: x-daily-article
description: >-
  Use once per JST day for @diceai0 (and when @selawmqt has Premium): pick one
  real team story, write or adapt one native X Article with a blog twin,
  pre-score it, hand it to X Operator to publish, and measure it at 24h.
---
# X daily Article

One native X Article per JST day on @diceai0. The owner asked for this on 2026-11-20 17:21 JST (t4192u: "posting a daily article to X daily ... posting to X articles as well"). The site copy on aniccaai.com/blog is canonical.

Baseline when this skill was written (public x reads, 2026-11-20): in the 14 days 11/06 17:00 to 11/20 17:00 JST, @diceai0 published 5 Articles on 2 days (11/10: 2, one deleted; 11/12: 3) and none since 11/12. @selawmqt published 0. The target is 14 of 14 days.

## Who does what
- Any teammate may write the draft and the blog twin. Only **X Operator** publishes on X (RULE X-ONE-WRITER). Only an agent with anicca-products push rights publishes the blog.
- 参謀 (or whoever runs this skill) owns the daily slot: if no draft exists by 15:00 JST, write one from the topic sources below.

## Hard limits
- Real facts only. Every number comes from a repo file, a dashboard page or a vendor page opened this run, with the path or URL kept in an internal evidence comment.
- No owner real name. The company line comes from team/COMPANY-ONE-LINER.md and closes the piece; it never leads.
- Runbook rules for @diceai0 apply (no other company names, no AI-does-the-work framing) unless the queue item cites an owner ask id that requests that topic. Write the ask id in the queue item.
- No paid-product links. One free link at most, plus aniccaai.com/open for numbers.
- Never republish a deleted Article (2120081017570546101) or re-release an old one.

## 1. Pick today's topic (5 minutes, files only)
In this order, take the first that has a real result with numbers:
1. An owner ask that names an article (team/OWNER-CONTEXT.md tail, last 24h).
2. A result shipped in the last 48h: team/ACTIVITY.md DONE lines, team/PROOF-NUMBERS.md, files/eval/*, team/metrics/*.json.
3. A failure with a fix (FIX/BLOCKED lines in ACTIVITY.md, team/LESSONS.md).
4. A comparison or how-to the team already researched (team/research/, team/playbooks/).
5. A topic from team/marketing/X-ARTICLES-PLAYBOOK.md §5 not yet published (check marketing/X-ACTIONS.md and the account).
Skip any topic already published as an Article in the last 30 days (search `from:diceai0 url:"x.com/i/article"`).

## 2. Write (copy the winner shape)
Template from team/marketing/X-ARTICLES-PLAYBOOK.md §2/§4 (winner: @kenn https://x.com/kenn/status/2110764296984781135):
- Title 3 to 10 words: a confession or a number.
- Open with 2 or 3 "Do you...?" lines, then "We do." and the twist.
- 5 to 7 H2 sections: what we tried, what happened (numbers), the mistake, what we changed, what's next.
- 800 to 1,800 words. One real image per ~300 words when we have them; a chart generated from real counts is fine if labeled with its source.
- End with one question to readers, the company line, then `Originally published at https://aniccaai.com/blog/<slug>`.
- Write EN and JA. Save to `team/articles/<topic>-YYYY-MM-DD.md` and `-ja.md` with front-matter (slug, title, date, lang, winner_format_copied) and an `<!-- evidence -->` block listing every source.
- Run unslop. No em dashes, no hashtags.

## 3. Pre-score
- `python3 team/scripts/x_presim.py score --surface article --account diceai0 --backend codex --text "<title + first 3 lines>"` (use `--dry` only for drafts you will not post). Record pred_impr.
- Run x-pre-post-score on the title + teaser. Under 60: rewrite the title and first 3 lines once, then go.

## 4. Queue and hand off
- Append to marketing/X-QUEUE-diceai0.md: `## X ARTICLE — <topic> (<date time> JST, <writer>; ask <id or none>; X Operator only)` with body path, headline image path, 3-line teaser (no hashtags), winner URL, pred_impr, rule notes.
- One line in team/inbox/x-operator.md with @x-operator and the queue section name.
- Blog: JSON for apps/landing/data/research/<slug>.json (slug, title, date, project, lang, description, word_count, markdown without the evidence block). Push or PR to Daisuke134/anicca-products if you can; if not, save a `git format-patch` under team/articles/blog-patch/ and ask the publishing owner in their inbox.

## 5. Publish (X Operator)
- Claim in team/CLAIMS.md, run team/scripts/post-gate.py with the winner URL.
- Desktop x.com → Articles → Write. Paste title, cover, body from the H1 to the canonical line. Publish once.
- Post the teaser with the Article card. Self-reply the other-language one-liner.
- Read back with `get_users_posts` / `get_posts_by_id` (post.fields article). Log the live /status/ URL in marketing/X-ACTIONS.md, POST-LOG.csv and team/ACTIVITY.md. Mark the queue item `[posted <URL>]`.
- If the blog URL is not live yet, drop the canonical line instead of linking a 404, and add it later only by editing the Article.

## 6. Measure at 24h
- `x_presim.py actual` and `get_posts_by_id` for impressions, likes, replies, bookmarks, quotes.
- One line in marketing/X-METRICS.md: Article id, age, numbers, pred vs actual, which section people quoted.
- Weekly (Sunday): rank the 7 Articles by impressions and bookmarks; keep the title shape of the top 2, drop the bottom shape.

## Log line (one per day)
`YYYY-MM-DD HH:MM JST | x-daily-article | <topic> | draft <path> | queued <section> | posted <URL or not yet> | pred <n> | 24h <impr/likes/bookmarks or pending>`
