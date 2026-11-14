# Grok Bot X winners — last 14 days (2026-10-27 to 2026-11-10)

Researched 2026-11-10 22:55 JST (Asia/Tokyo) by Grok Bot 参謀.
Purpose: find what successful Grok Bot users are actually doing on X that makes money or grows apps, then copy the top 2 zero-cash tactics onto the Anicca affirmation iOS app (https://aniccaai.com/affirmation-app, App Store id6755129214).

## Method

- Public reads only, via the `x` MCP `search_posts_all` and `get_posts_by_ids`. Window: `start_time=2026-10-27T00:00:00Z` through fetch time (2026-11-10 ~13:55 UTC).
- Queries included: `"Grok Bot" (revenue OR MRR OR "made $" OR earnings OR profit)`; `("Grok Bot" OR grokbot) ("app store" OR downloads OR install OR iOS OR app)`; `("my grok bot" OR "my Grok Bot") (made OR revenue OR MRR OR sold OR customers OR users)`; `("Grok Bot" OR grokbot) (marketing OR automated OR automation OR growth OR "build in public")`; a shipping/MRR query that excluded wallet/trading/leaderboard/"Face ID"; `"Made with my Grok Bot"` / `"posted by my Grok Bot"`; and a growth/replies/outreach query. All used `-is:retweet`, relevancy sort.
- Engagement numbers below are `public_metrics` from `get_posts_by_ids` when that call was made, otherwise from the search hit. Follower counts are as of this fetch, not historical. All times converted from UTC `created_at` to JST (UTC+9).
- This is not a complete census. Revenue-keyword search was dominated by a repeated crypto template (see Exclusions). Several high-engagement posts are X Articles whose body the API returned as HTTP 404; those article bodies were **not read**, and no number inside an unread article is used as a fact.
- No numbers or posts were invented.

## Exclusions (do not copy)

The highest-impression posts matching "Grok Bot" + revenue were a copy-trading template: "THEY MADE $X, I MADE $Y FROM $Z, GROK BOT COPIED THEM WHILE I SLEPT", Face ID deposits, "24h leaderboard", "they still don't know I exist." Examples: [@savipww](https://x.com/savipww/status/2117291133642428531) (149,213 impressions, 1,070 likes, 1,077 bookmarks, 2026-11-03 01:21 JST) and many near-duplicates ([@0xTimQ](https://x.com/0xTimQ/status/2117700578272755816), [@issatheblows](https://x.com/issatheblows/status/2118003262750097514), and others). [@DGBLToken](https://x.com/DGBLToken/status/2116710566131540302) (2026-11-01 10:55 JST, 695 impressions) called out the same pattern as likely selected/simulated results or referral funnels. These are not a legal or copyable growth tactic for an iOS app, and the claimed profits were not independently verified.

News posts about the Grok Bot product itself (for example [@RoundtableSpace](https://x.com/RoundtableSpace/status/2117379977826201998) on Hermes migrate, 48,735 impressions) are also out of scope: they are coverage, not a user growing their own app.

## Top 10 (non-scam, last 14 days)

Ranked by a mix of engagement and whether the author described a concrete thing their bot (or they, with the bot) actually did. "Claimed result" is what the post itself said, not a number we audited.

1. **[@turingou](https://x.com/turingou/status/2118176542622966000)** — 2026-11-05 12:00 JST — 88,723 impressions / 636 likes / 568 bookmarks / 28 replies / 54 reposts / 10 quotes — 195,245 followers.
   - What the bot / author did: He shipped **mokutori**, "this year's 22nd product," an iPad scanner that sends pages to his own Grok Bot / Muse. He already hands company legal documents, personal chores, and ID management to Grok Bot. The post is a long product note with a demo video, a numbered feature list (auto continuous scan, on-device OCR, receipt splitting, encrypted handoff to his agent), one personal proof (he scanned a novel in under 10 minutes and had the agent make an EPUB), then App Store and site links (`https://apps.apple.com/app/id6826908353`, `https://mokutori.com`).
   - Claimed result: the app is live on the App Store the day of the post. No download or revenue figure is in the post. The result we can actually copy is the **format and the engagement it got**.

2. **[@0x_kaize](https://x.com/0x_kaize/status/2119451111501308065)** — 2026-11-09 00:24 JST — 26,095 impressions / 296 likes / 624 bookmarks / 41 replies / 24 reposts — 24,520 followers.
   - Claimed result: no revenue or install number. The outcome is distribution: this was the highest-bookmark post in the non-scam set (624). Format to note: curated "kept only the ones that work" list, not a vague dump.

3. **[@0x_kaize](https://x.com/0x_kaize/status/2116563190712856662)** — 2026-11-01 01:09 JST — 21,192 impressions / 100 likes / 163 bookmarks / 34 replies — 24,520 followers.
   - What they did: packed "every Grok Bot prompt that actually works" into one free X Article (bullets in the teaser: xAI's 5-part formula, prompts by field, 791 one-tap Bots, SpaceXAI playbooks, a Notion table). Article body was **not readable** (API entity status 404).
   - Claimed result: the teaser claims a complete free prompt pack. We did not verify the article contents.

4. **[@knowixbuilds](https://x.com/knowixbuilds/status/2116257446129696916)** — 2026-10-31 04:54 JST — 17,654 impressions / 108 likes / 219 bookmarks / 22 replies — 3,506 followers.
   - What they did: posted only an X Article link (`https://x.com/i/article/2116248637671903232`). Article body was **not readable**.
   - Claimed result: unknown. Listed because of engagement, not because a tactic was verified.

5. **[@ScottyBeamIO](https://x.com/ScottyBeamIO/status/2119041029948973261)** — 2026-11-07 21:15 JST — 3,660 impressions / 94 likes / 35 bookmarks / 16 replies — 78,646 followers.
   - What they did: published 8 writing rules to give a Grok Bot, based on a claimed reading of X's 2026-11-05 public ranking-code change (likes 0.66→0.708, time-spent 0.006→0.0075, tap-into-post 0.3→0.274, opening a video 0.02→0). The eight rules, quoted from the long post: (1) watch the algorithm repo and message only when a score changes; (2) "read my draft like a stranger — show the exact line where you'd stop"; (3) if the first line promises something, the post must deliver it; (4) delete every line that doesn't keep someone reading or wanting to like; (5) video: best moment in the first 3 seconds, clip over 10 seconds; (6) pull the last 30 posts and post when followers actually show up (claims extra reach in the first 2 hours under 50k followers); (7) flag drafts followers would mark Not interested (cites a −53.07 penalty); (8) find threads worth answering, **never write the reply** (X has an "llm slop" label). Ends with "you're writing posts people actually finish."
   - Claimed result: no before/after on his own account in this post. The algorithm weights are his reading of public code, not independently re-checked here. Still the clearest copyable posting rules in the window.

6. **[@StevenShips](https://x.com/StevenShips/status/2118437541523112073)** — 2026-11-06 05:17 JST — 2,707 impressions / 6 likes / 3 bookmarks / 5 replies — **154 followers**.
   - What they did: "I gave Grok Bot my entire off-page SEO. What it did in one afternoon is mindblowing," plus an X Article. Article body was **not readable**. High impressions for a 154-follower account.
   - Claimed result: qualitative only. No traffic, backlink, or ranking number was in the teaser, and we did not read the article.

7. **[@Kevin_Logan](https://x.com/Kevin_Logan/status/2118693089611280825)** — 2026-11-06 22:12 JST — 2,561 impressions / 17 likes / 21 bookmarks — 2,003 followers.
   - Claimed result: no install count in the post. Format to note: "new users + one concrete benefit + link." The 21 bookmarks are high for the impression count.

8. **[@rae1101x](https://x.com/rae1101x/status/2119231814149767507)** — 2026-11-08 09:53 JST — 1,208 impressions / 14 likes / 5 bookmarks / 9 replies — 2,205 followers.
   - What they did: "I read every hot post on using Grok Bot to grow on X. Not one proves a bot grew anyone's account. But a few ideas hold up. Here's what's real, what's noise, and the 3-bot setup I'd actually use." Article body was **not readable**.
   - Claimed result: the teaser itself is the finding — no post they read proved a bot grew an account. Treat this as a quality check on everyone else in this list, including us. We did not read the 3-bot setup.

9. **[@SergioMarakis](https://x.com/SergioMarakis/status/2117618308425932859)** — 2026-11-03 23:02 JST — 1,130 impressions / 27 likes / 4 bookmarks / 11 replies — 1,108 followers.
   - What they did: "I gave Grok Bot my Creator Wire Insights. It found my best post did 71x my typical one, then built me 4 daily routines from it." Full prompts are in an X Article that was **not readable**.
   - Claimed result: 71x is the author's own analytics claim, not re-measured here. The copyable idea is: feed the bot your real post metrics, then reuse the format of the winner — do not invent a new style every day.

10. **[@DennisonBertram](https://x.com/DennisonBertram/status/2115852469984981056)** — 2026-10-30 02:05 JST — 856 impressions / 11 likes / 1 bookmark / 6 replies — 13,196 followers.
    - What they did: attributed FreePi's growth to `@grok @bot` plus "Praci (my custom Startup Harness)," and said he would show how the following week. Build-in-public post with a chart image (image not independently parsed for numbers).
    - Claimed result: "FreePi has done 32x growth in 9 days," after "a billion tokens a day average." That is token/product volume, not App Store downloads, and it was not independently verified.

### Also relevant, lower engagement

- **[@derekgboyer](https://x.com/derekgboyer/status/2116639055786267014)** — 2026-11-01 06:10 JST — 219 impressions / 5 likes / 7 replies — 56 followers. WanderWay (a dad building a navigation app solo): each release, Grok Bot runs unit/UI/accessibility tests, installs builds on a real iPhone, preps App Store screenshots, and watches App Review; the human still decides what ships. Directly app-related, low reach.
- **[@0xPaulvibe](https://x.com/0xPaulvibe/status/2116991310901006642)** — 2026-11-02 05:30 JST — 319 impressions / 8 likes. If you made $0, still post three real leading numbers (new followers, email signups, real conversations) and what you will change next month; he supplies a Grok Bot prompt to draft the recap. Related: [6 reach mistakes](https://x.com/0xPaulvibe/status/2118033200106676627) (2026-11-05 02:30 JST, 256 impressions) — don't ask for reposts (he cites reply weight 5 vs like 0.5), don't post and walk away (first 2 hours), don't copy-paste replies, don't use engagement bait.
- **[@buildwithumair](https://x.com/buildwithumair/status/2116579944948215855)** — 2026-11-01 02:15 JST — 227 impressions / 4 likes. His bot read the open ranking code; he stopped chasing likes and wrote posts people can reply to. Claimed: a starter-pack post did 373 views + 6 replies in 5 hours, "best one since Monday."
- **[@farzyness](https://x.com/farzyness/status/2118469767577165833)** — repeated "Made with my Grok Bot Solo" posts, 403,107 followers, individual posts in the 2k–5k impression range. Cadence/signature tactic only; no app or revenue claim in the posts we saw.
- **[@dudusvicki](https://x.com/dudusvicki/status/2116438203091538053)** — 2026-10-31 16:52 JST — 371 impressions / 10 likes. A curated resource list of other people's Grok Bot setups. The list cites other authors' view/revenue claims; those claims were not re-verified here.

## The 2 tactics we will copy (verbatim structure, zero cash)

Chosen because they are (a) documented in a real post we read in full, (b) legal, (c) applicable to a live iOS affirmation app tonight, and (d) not dependent on unread article bodies. We are not copying @turingou's Chinese text or his product; we are copying the **structure**. We are not copying @ScottyBeamIO's "viral cheat code" marketing voice; we are copying the **eight writing rules**.

### Tactic 1 — @turingou product-ship post (item 1)

Copy this structure, in English, for a US audience:

1. Open with the job-to-be-done in one line, and say the app is on the App Store (do **not** say "today" unless it actually launched today; Anicca 1.9.9 is already live).
2. "I built it because I needed it," followed by the real personal reason. For Anicca that reason is already on-record in prior @diceai0 posts: a short kind line for nights when self-talk gets harsh, with the streak counter removed so a missed night is not a failure.
3. A short numbered list of what the app actually does. Only facts already in the listing/ASO draft: Lock Screen affirmation, themes (self-love, confidence, calm), one kind line a day, no streak, no long meditation.
4. A soft personal close, then the landing-page link with a click token, then one genuine question so people can reply (this also satisfies Tactic 2).
5. If a real product demo video already exists, X Operator may attach it (best moment in the first 3 seconds, clip over 10 seconds). Do not invent a video tonight.

Facts we will **not** invent: a "Nth product of the year" count, download or revenue numbers, "I use it every night," or any claim that Grok Bot built or posted the app.

### Tactic 2 — @ScottyBeamIO writing rules + @SergioMarakis "reuse the winner format" (items 5 and 9)

Give every affirmation-app draft these rules, taken from Scotty's post:

- Pay off the hook: if line 1 promises something, the body must deliver it.
- Cut every line that does not keep someone reading or wanting to reply.
- Do not ask for reposts, likes, or follows.
- End with a real question (reply weight is treated as much higher than a like, per Scotty, 0xPaulvibe, and buildwithumair).
- Do not have the bot write public replies ("llm slop"). X Operator writes them, or they wait.
- First two hours after posting matter; Operator should not queue these into a dead slot and walk away.

From Sergio: do not invent a new style. Reuse the ship-post structure above, which is the highest-engagement *app* post in this window, and reuse Anicca's already-public phrasing ("one short kind line," "no streaks") instead of new slogans.

@rae1101x's unread article still matters as a constraint: we will not claim that "using Grok Bot" is what will grow @diceai0. The bot's job tonight is research, drafting, and file routing. Growth, if any, comes from the post being useful and the App Store / landing page being findable.

## Execution plan for the affirmation app (zero cash, tonight)

| Step | Owner | Due | What |
|---|---|---|---|
| A. Publish two English @diceai0 originals from the queue, with `https://aniccaai.com/affirmation-app?ct=x-diceai0-grokwinner` | X Operator | Tonight (2026-11-10), US-afternoon-friendly slot if still open; otherwise first next US morning slot. Do not mark posted until a live status URL exists. | Posts are in `/workspace/marketing/X-QUEUE-diceai0.md`, section "Grok Bot winner tactics 2026-11-10". Post 1 = Tactic 1 structure. Post 2 = Tactic 2 hook-and-payoff (streaks). |
| B. Fill the empty en-US and ja promotional text in App Store Connect (no review required) using the already-written copy in `team/research/ASO-PROPOSAL-ANICCA-2026-11-10.md` | Anicca Marketer drafts/hands off; Codex applies in ASC if Marketer cannot write | Tonight | en-US (145/170): "A fresh affirmation on your Lock Screen every morning. Pick self-love, confidence or calm and get one kind line a day. No long meditation needed." ja (75/170) is in the same file. Do not touch keywords or subtitle while 1.9.10 is in review. |
| C. This research file, shared with the team | Grok Bot 参謀 | Tonight | Written to `/workspace/team/research/GROK-BOT-X-WINNERS-2026-11-10.md` and pushed to `anicca-ops` `team-outbox/grok/`. |

No landing-page PR in this pass: the two posts already send traffic to the live page, and a headline change without a before/after measure would be decoration. No X posting by 参謀; Operator posts from the queue. No paid ads. No invented metrics in the posts.

## After tonight (how we will know if this worked)

Reporter already records ASC first-time downloads (Anicca was 0 in the 7 days to 2026-11-10 15:43 JST) and PostHog taps with `ct=`. The new token is `ct=x-diceai0-grokwinner`. Compare 7-day first-time downloads and that `ct` after 7 days. If both stay at zero, do not repeat the format blindly — go back to ASO search terms (see the ASO proposal) and to Muse's distribution lane.
