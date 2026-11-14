# X Article best practices (derived 2026-11-10 23:xx JST)

Built from X public reads (namespace `x`, `search_posts_all` + `get_posts_by_ids`, window 2026-09-11 to 2026-11-10) and open-source writing skills. Metrics are public_metrics at read time. Supersedes nothing; extends `team/gaps/x-article-format-en.md` (2026-11-02).

## Winners read in full

| Author | Title | Views | Likes | Bookmarks | Replies | Words |
|-|-|-|-|-|-|-|
| @0xwhrrari https://x.com/0xwhrrari/status/2102020016539324501 | Jev Engineering: Stop Using LLMs for Every Decision | 901,058 | 516 | 1,269 | 46 | long |
| @DanielSmidstrup https://x.com/DanielSmidstrup/status/2111860161870532857 | 200 Days on X: 0 to 12.9k Followers, a $1k MRR SaaS and $7K/Month | 103,371 | 142 | 61 | 73 | 1,251 |
| @Joshua_WD https://x.com/Joshua_WD/status/2116582206361465050 | What actually worked in AI coding agent posts this week | 2,597 | 29 | 5 | 34 | 1,396 |
| @livesanches https://x.com/livesanches/status/2118470328246489391 | I RUN A STARTUP WITH 11 BOTS AND ZERO EMPLOYEES | 542 | 12 | 1 | 9 | 581 |
| Earlier set (2026-11-02): @gregisenberg, @jackfriks, @tibo_maker, see `team/gaps/x-article-format-en.md` | | 36k-63k | | 435-526 | | 922-2,867 |

## Checklist

1. Title is one concrete claim with a real number or time box, first person (W1 "200 Days on X: 0 to 12.9k...", @0xwhrrari "Stop Using LLMs for Every Decision"). 8 to 16 words.
2. First line states the hard fact before any context, then a one-line twist, then a one-line map of the article ("Here's exactly how it happened, what worked, what didn't, and what's next." W1).
3. State limits up front. "Every number below came from the post itself. No made-up stats." (@Joshua_WD). Unmeasured numbers are written as unmeasured, never estimated.
4. Use only real numbers. Never borrow someone else's result as yours; name whose number it is (house rule + x-longform-post "Never fabricate metrics").
5. Short paragraphs, 1 to 3 sentences. Sentence-case headings every 3 to 5 paragraphs. Lists only for numbers, routines, or steps (kluless13 x-articles, from the X Creators guide).
6. Order: what happened with dates, the numbers, what worked, what didn't, lesson, what's next, thanks or question (W1, W5, @livesanches).
7. Name and link the people you copied. Credit converts readers (@livesanches cites his own failure; @Joshua_WD names every account).
8. One visual block that reads in 3 seconds: a table or a small code-block diagram under 40 chars wide (ericosiu x-longform-post).
9. Include the failure. The "my first mistake" section is the most quotable part of @livesanches and W2.
10. Close with concrete next steps and one specific question for replies, then the follow CTA (W1, @Joshua_WD, @livesanches "What would you hand to a bot first?").
11. Teaser post: hard numbers on line 1, what I did on line 2, "I wrote down what worked and what didn't" on line 3. Under 270 chars, no hashtags (W1, W5, @livesanches).
12. Humanizer pass before publishing: no "not X, it's Y", no stacked triads, no em dashes, no AI vocabulary, straight quotes, no generic conclusion (ericosiu x-longform-post 24 patterns, sergebulaev x-humanizer V3, local `unslop`).
13. English only for public articles. Japanese drafts are internal sources, never published as-is (owner, 2026-11-10).
14. Length 900 to 1,300 words for a personal story; 1,300 to 2,900 for a breakdown.
15. Cover image: one big real number on a plain background; no stock robots.

## Sources (skills)

- ericosiu/ai-marketing-skills x-longform-post (MIT): https://github.com/ericosiu/ai-marketing-skills/blob/main/x-longform-post/SKILL.md
- kluless13/claude-skills x-articles (based on X Creators guide): https://github.com/kluless13/claude-skills/blob/main/skills/x-articles/SKILL.md
- sergebulaev/x-skills x-humanizer V3 (MIT): https://github.com/sergebulaev/x-skills
- Local skills applied: `unslop`, `technical-writing` (pstack).
- Cloned copies: /workspace/skills-external/{ai-marketing-skills,claude-skills,x-skills}

## Applied in

- /workspace/marketing/articles/x-article-2026-11-10-en.md (rewrite of the deleted Japanese article 2120081017570546101)
- Reusable skill: /workspace/oss/article-writing-skill/SKILL.md
