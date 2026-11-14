# Grok Bot best practices log (参謀 best-practice loop)

Each entry: date, source, practice, what I changed, proof, effect (measured or UNKNOWN). Author self-reports are marked as such.

## 2026-11-11 15:4x JST
- Source: https://x.com/ScottyBeamIO/status/2120161342229192867 (103 likes, 84 bookmarks; author self-report: bot found $600/yr forgotten subs). Other X results for "Grok Bot use case" since 11/09 were low-signal (≤8 likes).
- Practice: "the bot must pay for itself" — audit recurring charges from receipts and cut what no live loop uses.
- Changed: wrote team/research/SUBSCRIPTION-AUDIT-2026-11-11.md from Gmail charge notices 11/01–11/11 (OpenRouter ¥8,621, Maritime AI ¥3,268, LinkedIn Premium ¥1,990/mo, HeyGen ¥1,634, one unclassified Apple receipt), with keep/cut rule and one owner (Reporter).
- Proof: the audit file + gmail ids inside it.
- Effect: UNKNOWN (no cancellation confirmed yet; potential up to ~¥15,500/mo if all cut, not a saving until a provider confirms).
- Repeated-failure note: Daily team briefing (09:00) and Evening wrap (21:30) both failed because their WakeParent relay was Aborted. Fix owner: 参謀 main chat (a routine run can only read its own routine) — change those two to post directly via the Slack connector from their saved instruction instead of relaying through the parent.

## 2026-11-11 23:4x JST
- Practice: measure with the native per-bot / per-routine usage breakdown before cutting anything, and fix routines whose own cadence guarantees no-op runs.
- Changed: skill grok-bot-overhead-reduction gained step 4b (top-3 routines by share, cadence-vs-gate mismatch check, hand exact patch to the routine's own chat).
- Proof (this week, 参謀 bot only, shares of all Grok Bot usage; weekly limit 61.7% used, resets Fri 11/13 13:30 JST): X distribution & prediction eval 2% (~672 runs/wk, every 15 min), Life Manager remote-work loop 2% (~336), Travel/wake flush 1% (~476), Muse/Dots/Codex reply loop 1% (~2,016 runs/wk), not-from-routine 36%. X distribution's 23:29 run was nothing_to_do because its own 30-min posting gap blocked it, so a 15-min cadence produces guaranteed skips.
- Owner + patch (one owner: 参謀 main chat, since a routine run can only read itself): change X distribution routine (folder x-build-in-public-private-account) from */15 to */30 with gap rule 25 min, so posting volume is unchanged and the guaranteed-skip runs disappear.
- Effect: UNKNOWN until the patch is live and a matched next-week window is compared.
- Repeated-failure note: still open from 15:4x — briefing/wrap WakeParent Aborted; same owner (main chat).

## 2026-11-12 07:4x JST
- Source: https://x.com/ocadubarral/status/2120529739764961699 (2 likes; author self-report: cut >80% of Grok Bot usage without turning off any bot, Ultra lasted 48h before and now a week; step 1 is triage before each demand, deciding whether it is worth effort and where it goes; the rest of the thread was not readable via API). Higher-like posts since 23:4x were repo/template lists (https://x.com/spectnfa/status/2120542315005559169 41 likes, https://x.com/de1lymoon/status/2120624000971800949 25 likes), low fit right now.
- Why now (measured): weekly limit 69.8% used at 07:36 JST vs 61.7% at 23:4x (about +1 point/hour), resets Fri 11/13 13:30 JST in ~29h, and extra credits are $0, so the current pace runs out before reset. Within 参謀: Muse/Dots/Codex reply loop rose from 1% to 3% of all Grok Bot usage this week in 8h (~2,016 runs/wk); X distribution 3% (~336/wk, cadence now */30); Life Manager remote-work loop 2%; not-from-routine 34%.
- Practice: triage gate as step 0 of every routine run: one cheap check, end with one line when nothing qualifies.
- Changed: this loop (folder daily-self-improvement) got step 0: one X search, and only when a new post has ≥20 likes or ≥15 bookmarks or a routine's usage share jumps ≥1 point does the full run happen; otherwise one log line and end.
- Owner handoff (one owner: 参謀 main chat, because a routine run can only read its own routine; get was refused this run): give the Muse/Dots/Codex reply loop (folder fac-bots-inbox-grok-sanbo-every-2h) the same step 0 from CHEAP-WAKE.md, a last-seen ts state file diffed against Slack #agents-hq and the GitHub files, ending in one line with no subagents when nothing is new. Its 5-minute cadence stays as 成田さん set it.
- Effect: UNKNOWN until the next matched usage reading.
