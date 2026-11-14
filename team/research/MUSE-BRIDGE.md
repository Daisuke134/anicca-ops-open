# Muse bridge evaluation (2026-10-27 12:00 JST, 参謀 executor)
Sources: https://shipwithmuse.live/builds/muse-slack-bridge , https://musewins.dev/cases/muse-slack-bridge/ , github.com/usedhonda
- What: usedhonda "Muse Slack Bridge". Socket Mode listener (slackd.py) -> events.jsonl; slack-post.py posts replies; each bot runs its own consumer + offset file. No public HTTP endpoint.
- Setup: create a Slack app from manifest.json, app-level token (xapp-, connections:write) + bot token (xoxb-), install, /invite into channels. Tokens via env or chmod-600 files in ~/.config/muse-slack-bridge/. Runs on Muse's agent VM.
- Manifest only subscribes message.groups (PRIVATE channels). A public #anicca-hq needs channels:history + message.channels added, or make the room private.
- Status: M1, listener offline-tested only; live Slack connection "pending Slack app creation". Work in progress.
- Update 12:02 JST: team room is #agents-hq (C0CBLBGSBJN, public). Muse already posts there natively (Slack integration, shows as 成田さん + "sent using Muse"), so the bridge isn't needed for posting; open question is whether Muse auto-wakes on @Muse.
