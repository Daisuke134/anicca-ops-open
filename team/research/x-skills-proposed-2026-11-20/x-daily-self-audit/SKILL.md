---
name: x-daily-self-audit
description: >-
  Use when once or twice a day, to count what our X account actually did by type (replies, self-replies, originals, quotes, reposts) in the owner's local day, compare against the day's targets, and log the gap.
---
# X daily self-audit

Count our real public activity by type, compare it with the targets the posting routine was given, and write one log line. Do this before changing tactics. Report what the counts show, not what the plan said.

This is our own procedure. It extends the measure step of x-growth-playbook and complements x-metrics-reader, which reads per-post numbers and followers. This skill counts actions by type and checks reply targeting.

## Hard limits
- Read only. No posting, liking or following.
- Numbers come only from API reads made in this run. If a read fails, write "unread", never a guess.

## Inputs
- Our handle and author id.
- The owner's time zone. Days are local days. For JST, day D runs from D-1 15:00Z to D 15:00Z.
- Today's targets: the newest dated section of the tactics file the posting routine reads. If none exists, use the x-growth-playbook defaults.

## Step 1: counts by type
Use the public post counts endpoint with hourly granularity, starting at the local day's start in UTC. Sum the hourly buckets into local days.

| type | query |
|---|---|
| all replies (incl. self) | `from:<handle> is:reply` |
| originals + quotes | `from:<handle> -is:reply -is:retweet` |
| quotes | `from:<handle> is:quote` |
| reposts | `from:<handle> is:retweet` |

- Self-replies: replies whose `in_reply_to_user_id` is our own id. Split them out from a timeline read.
- Replies to others = all replies minus self-replies.
- Originals = (originals + quotes) minus quotes.
- The counts endpoint covers about 7 days, so run it daily to keep a longer history in the log.

## Step 2: quality checks
Read our timeline for the day with metrics, paging as needed:
- median views per type (originals, replies to others, quotes)
- for replies to others: each parent's views and author followers
  - **share of replies under parents with 1k+ views** (target 60%+)
  - share of replies to accounts under 1k followers that are not already talking to us (target 20% or less)
- reply-backs: share of replies on our own posts that we answered within 60 minutes
- duplicate check: any two of our replies with identical or near-identical text (must be 0)
- top 5 replies and top 3 originals by views, each with parent size, parent age at reply time, and format

## Step 3: followers and installs
- Followers now, plus the delta from yesterday's log line.
- Installs by campaign tag, if the store dashboard or file is readable this run. Otherwise "unread".

## Step 4: compare and log
For each type, compute actual / target and the gap. Flag anything under 70% by midday, or under 100% at day end.

Append one line to the audit log (newest on top):
`YYYY-MM-DD HH:MM <tz> | replies-to-others A/T | self-replies A | originals A/T | quotes A/T | reposts A/T | demo clips A/T | med views o/r/q | parents 1k+ X% | reply-backs X% | dupes N | followers F (+d) | installs I or unread | biggest gap: <type>`

## Step 5: hand off
- Give the biggest gap to the next posting slot as its first job.
- Report only verified numbers. Stay silent if nothing changed since the last audit.

## Step 1b: Articles and routine gaps (added 2026-11-20)
- **Articles:** `search_posts_all` with `from:<handle> url:"x.com/i/article"` and `start_time` 14 days back; cross-check one page of `get_users_posts` with `post.fields=article`. Log `articles 14d N on D days | last <date>`. Target 1 per JST day (x-daily-article). On 2026-11-20 the baseline was @diceai0 5 on 2 days (last 11/12), @selawmqt 0.
- **Routine gaps:** from marketing/X-ACTIONS.md, find the longest stretch with no routine-logged run. Flag any gap over 6h (example found: 11/16 15:17 → 11/20 14:24 JST).
- **Series misses:** Day-series posts missed (example: Day 7–9 missed before Day 10 on 11/20).
- Add `articles N/1 | longest gap Hh | series missed N` to the Step 4 log line.
