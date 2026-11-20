---
name: x-pre-post-score
description: >-
  Use when checking any X post, reply or quote draft before it goes to the posting gate; scores it against the current open ranker weights and a style checklist, then suggests one rewrite.
---
# X pre-post score

Score a draft against what the open X ranker actually rewards, then fix the weakest part. This is an editorial estimate, not a reach prediction.

Adapted from:
- tonkotsuboy/x-impact-checker (Apache-2.0): https://github.com/tonkotsuboy/x-impact-checker. Modified: the weights were updated to the current `param.rs`, emoji output was removed, and the factor list was compressed.
- attainmentlabs/x-open-source-algorithm-skill (MIT): https://github.com/attainmentlabs/x-open-source-algorithm-skill
- sergebulaev/x-skills, `skills/x-post-writer/references/single-tweet-checklist.md` (MIT): https://github.com/sergebulaev/x-skills
- Weights: xai-org/x-algorithm, `home-mixer/params/param.rs`, read 2026-11-15 at HEAD 30647a8: https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs

## The weights the ranker uses now
Each weight multiplies the predicted chance that a viewer takes that action. The file itself warns against reading weights as "N likes = 1 reply" counts.

| action | weight |
|---|---|
| reply | 5.0 (plus a 15.0 boost when the two accounts follow each other) |
| quote | 5.0 |
| share via DM | 5.0 |
| follow author | 4.0 |
| share | 2.118 |
| repost | 1.0 |
| like | 0.708 |
| continuous click dwell | 0.385 |
| click | 0.274 |
| open link | 0.2 |
| profile click, copy link, video view | 0.0 |
| not interested | -53.07 |
| block author | -31.2 |
| mute author | -58.8 |
| report | -234.0 |

Cold start, also in param.rs: posts under 7200 s old with under 200 impressions, from authors under 50,000 followers, can get reserved feed slots (15 to 16). The first two hours matter.

Outdated numbers to ignore: the 2023 values (reply 13.5, "author reply +75", like +30). attainmentlabs still quotes them; the current file does not contain them.

## Score (100 points)
Score each factor, then subtract penalties.

| factor | max | full marks when |
|---|---|---|
| reply pull | 25 | a real question, a debatable claim backed by our data, or an open gap readers can fill |
| quote pull | 20 | a clear stance or a number others will want to react to |
| follow pull | 15 | shows ongoing value: a series, a build log, a repeatable result |
| share pull | 10 | something a reader would send to a friend: a checklist, a hard number, a how-to |
| repost and like pull | 10 | useful or relatable in one read |
| dwell | 10 | worth stopping on: a screenshot, a clip, or detail that rewards reading |
| first line | 10 | stops the scroll alone, with no need for line two |

Penalties:

| risk | range | trigger |
|---|---|---|
| not interested | -5 to -15 | off-niche, vague value, clickbait |
| mute | -5 to -15 | repetitive, same structure as a recent post, too many posts in a row |
| block | -10 to -25 | aggressive, dunking on small accounts |
| report | -15 to -30 | misleading claims, spam patterns, duplicated reply text |

Grades: 75+ ready. 60 to 74 fix the weakest factor. Under 60 rewrite or drop.

## Style checklist (pass or fail)
Adapted from sergebulaev:
- One idea. Two ideas means two posts.
- At least one specific number with a named referent, if the claim allows it. It must be true and read this run.
- No reveal bridges ("The result?", "Here's what") and no "it's not X, it's Y".
- No stacks of AI vocabulary: leverage, robust, landscape, streamline, elevate, fundamentally.
- No em or en dashes.
- 0 or 1 emoji.
- No external link in the main post body; put it in the first self-reply. This comes from creator data [D1 in the source library]. Note that the ranker file itself only gives open link a low weight (0.2), so treat this as empirical, not code-proven.
- Ends on a landing or a specific question.

## Hard rule check (any fail blocks the draft)
- No owner real name. No other company names in our text.
- No claim that AI or automation does the work.
- No DM asks. No "follow for follow". No engagement bait ("RT if", "reply YES").
- Every number matches a file or page opened this run.

## Output
Report:
- the score and grade
- the 3 weakest factors, each with a one-line reason
- one rewritten version in the original language
- which weighted action the rewrite targets

Hand off to the posting gate only if the score is 60+ and the hard rule check passes.

## Articles (added 2026-11-20)
Score the title, the first 3 body lines and the teaser post together, then also run the simulator:
`python3 team/scripts/x_presim.py score --surface article --account diceai0 --backend codex --text "<title + first 3 lines>"`.
Article-specific checks (pass or fail), from team/marketing/X-ARTICLES-PLAYBOOK.md §2:
- Title 3 to 10 words, a confession or a number.
- Opens with 2 or 3 "Do you...?" lines a builder recognizes.
- 5 to 7 H2 sections; 800 to 1,800 words; one image per ~300 words when real images exist.
- Ends with one question, then the canonical line (only if the blog URL is live).
- Teaser is 1 to 3 lines, no hashtags, Article card attached.
The hard-rule line "No other company names / no AI-does-the-work claim" may be waived only for a queue item that cites an owner ask id for that topic.
