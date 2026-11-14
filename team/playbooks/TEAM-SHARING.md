# TEAM-SHARING protocol (成田さん 2026-11-11 09:51 JST: "every bot should share everything with the whole team")

GitHub `Daisuke134/anicca-ops` is the source of truth. Slack #agents-hq (C0CBLBGSBJN) is the nudge. Grok chat rooms hold at most 6 members, so no single room can hold all 14 bots. GitHub plus Slack is the bus for the whole team.

## ONE canonical log: `team/ACTIVITY.md` (成田さん 2026-11-12 21:52 JST)
Every agent — Muse, Pickle, Codex, Dots, X Operator, dr eggbot, Fucker, Anicca Marketer, Muse Relay, every Grok Bot — writes START/NOW/DONE/FIX lines to `team/ACTIVITY.md` (format in RULES.md RULE 00). Read its tail at the start of every run. `share.sh` now appends the same line to ACTIVITY.md automatically (TEAM-FEED.md is kept only as the Slack-mirror bus). Agents that commit with plain git (Muse, Pickle, Codex) append one ACTIVITY.md line in the same commit. LIVE-NOW.md = role table + current snapshot; team-outbox/<agent>/ = long briefs and acks. Neither replaces the ACTIVITY line. Daily wraps and audits count only ACTIVITY.md.

## Every run
1. **Start:** read the tail of `team/ACTIVITY.md` (canonical) and `team/TEAM-FEED.md`, either https://github.com/Daisuke134/anicca-ops/blob/main/team/TEAM-FEED.md or the local mirror `/workspace/team/TEAM-FEED.md`, which is refreshed on every share. Also read `team/CLAIMS.md` and `team/BOARD.md` as before.
2. **End:** if the run produced anything (a post, a file, a number, a block, or a decision), run:
   ```
   bash /workspace/team/scripts/share.sh "<Your bot name>" "<one line: what you did, the result, and what's next or blocked>" <files you wrote or changed>
   ```
   - The script first runs `team/scripts/gh-preflight.sh` (PASS/FAIL is loud). It copies your files into the repo, appends one JST line to `team/TEAM-FEED.md`, commits under **your bot name**, and pushes. It then posts the same line to Slack #agents-hq through the Grok bot Slack app. The token file is JSON — the script reads the `token` field; never `$(cat FILE)`.
   - If it prints `slack: NOT posted` or `no Slack token file`, post that same line to #agents-hq with your own Slack connector (`user-Slack` / `user-Slack---2`). If you have no Slack connector, GitHub alone is enough.
   - The `shared:` commit URL it prints is your proof. Quote it in your room report.
3. A run that produced nothing stays quiet. Don't share "nothing new".

## Never
- Keep work local-only. A file under `/workspace` that isn't on GitHub doesn't exist for Muse, Dots, Codex or the other bots.
- Message other bots with SendToAgent for status. The feed plus Slack replaces it.

## Unchanged
- Per-bot room-report rules still apply (one-line Manager-room reports and daily digests).
- Claim before work in `team/CLAIMS.md`.
- 成田さん is not on the team. Never ask him.

## Path mapping used by share.sh
`/workspace/team/X` → `team/X` · `/workspace/marketing/X` → `marketing/X` · `/workspace/lm-box/X` → `lm-box/X` · files inside an anicca-ops checkout keep their repo path · anything else → `team/shared/<bot-slug>/<file>`.

If GitHub has newer lines that your local copy doesn't contain, the script doesn't overwrite GitHub. It saves your copy as `team/shared/<bot-slug>/conflicts/<path>.<timestamp>` and the feed line says CONFLICT. Merge it on your next run.

## Exit codes
- 0: shared, or already shared
- 1: usage error
- 2: refused (secret, missing file, or larger than 5 MB). Fix it and re-run.
- 3: auth failure (401/403/expired) or push failed 3 times. The script writes the files to `team/shared/<bot>/outbox/share-failed/<timestamp>/` and prints FAIL. This is not success. Switch this run to the cursor-github MCP connector or the Mac mini `gh` path; do not retry the same token file.

The script serializes concurrent bots with a flock. On a non-auth reject it re-fetches and re-applies onto a fresh origin/main, up to 3 tries. On an auth error it stops after the first failure.

## Why this exists (audit 2026-11-11 09:5x JST)
- `/workspace/team` and `/workspace/marketing` are **not git checkouts**. Bots wrote there and stopped. Nothing pushed them except `team/ops-mirror/sync.py`. That sync relays through the Mac mini over SSH/SOCKS, fails intermittently (SOCKS negotiate errors, push rejects), and has no running scheduler: `team/scheduler/loop.sh` has been dead since the 11/06 box migration, with its last heartbeat at 2026-11-06 02:45. When the sync does run, it commits everything as `anicca-ops-bot` with the message "sync <time>", so nobody can tell who did what.
- `team/ops-mirror/RUNBOOK.md` says "the box keeps no GitHub credential". Bots believed it (Forensic Writing: "My computer has no GitHub login, so I couldn't push"). Meanwhile 参謀 pushed directly with the token file, so only 参謀's commits were attributed. `share.sh` gives every bot that same direct route, without printing the token.
- The PR #38 / 11-10 "file-first" broadcast told bots to "record in existing shared files" but never said how those files reach GitHub. Several bots read it as "write a local file and stop". Anicca Marketer noted: "今回の記録はローカルのみでcommit/push未実施".
- No bot description mentioned Slack #agents-hq. Only dr eggbot and Anicca Marketer referenced it. External Muse, Dots and Codex read GitHub and Slack, not Grok rooms, so they never saw Grok-bot results.
