# TEAM-CHAT-DECISION (executor, 2026-10-27 12:05 JST)
Question: one room where 成田さん + Grok bots + Codex + Claude Code + Muse + Dots all see everything and reply to each other automatically.

## Winner: Slack #agents-hq (C0CBLBGSBJN) (one Slack app identity per agent) + Reason as the wake/transport for Muse & Dots
Keep the Slack build that is underway. Add per-agent bridges (below) instead of one generic mirror.

## Ranked table (1-5, 5 best)
| # | Option | Wake on mention, no human | Phone view | Setup for OUR agents | Reliability | Cost | Builders using it | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | Slack channel, one bot per agent (CCSC bridge for Claude/Codex; Grok routines Slack trigger; Reason relay for Muse/Dots) | 4 (needs allowBotIds opt-in per bridge) | 5 | 4 (Grok bots have Slack connectors+triggers natively; logins exist for Dots/Muse) | 4 | 5 free | 5 | WIN |
| 2 | Cogent (cogent.tools) on top of Slack | 4 | 5 | 3 (Claude/Codex only; Grok/Muse/Dots unsupported) | 3 (new, 21 agents live) | free core | 2 | Optional adapter for Codex/Claude |
| 3 | Agent Relay (agentrelay.com, YC) channels | 5 agent-agent | 2 (desktop app, no phone chat noted) | 3 | 3 | free tier | 3 | Good backend, bad for 成田さん viewing |
| 4 | Telegram group (Bot API 10.0 bot-to-bot, May 2026) | 4 (BotFather bot-to-bot mode + admin + privacy off) | 5 | 2 (no Grok Telegram trigger/connector) | 4 | free | 3 (Hermes users) | Runner-up if Slack fails |
| 5 | Reason network alone | 4 (push tier) | 1 (no room/channel tools; only 1:1 send_message/check_inbox/list_team) | 5 | 3 | free | 1 | Transport, not the room |
| 6 | Discord / Matrix / Zulip | 3 | 4 | 2 | 3 | free | 2 | No advantage over Slack for us |

## Evidence
- Telegram FAQ (classic): "bots will not be able to see messages from other bots regardless of mode" — https://core.telegram.org/bots/faq/ . Changed May 7 2026: Bot-to-Bot Communication Mode; group bot msgs delivered only on /cmd@Bot or reply, or if receiver is admin + privacy off — https://core.telegram.org/api/bots/bot-to-bot , https://telegram.org/blog/ai-bot-revolution-11-new-features
- Slack multi-agent recipe (Claude+Codex in one channel, each its own Slack app, Socket Mode; peer bot msgs dropped unless listed in allowBotIds) — https://github.com/jeremylongshore/claude-code-slack-channel/blob/main/000-docs/multi-agent-channels.md , ACCESS.md
- Cogent: Slack<->Claude Code/Codex, agents talk to each other in one channel — https://cogent.tools/ , https://github.com/eaisdevelopment/cogent
- Agent Relay channels (#channel routing, Claude/Codex/Grok) — https://agentrelay.com/docs/channels
- X: @ericosiu "Grok Bot… manage teams of agents, let them talk to each other, and bring that work into Slack" (1.8k imp) https://x.com/ericosiu/status/2105719395783962802
- X: @sarahwooders "moved all our agents to Slack, and now they just talk to each other" https://x.com/sarahwooders/status/2113799139402330425
- X: @kyle_e_walker OpenClaw agents "@-mention each other on Slack and talk to each other" https://x.com/kyle_e_walker/status/2113958851624263716
- X: @MeryemArik9 #clankers Slack channel where agents talk to each other https://x.com/MeryemArik9/status/2111923227790385541
- X: @michellelsun asks for "slack for agents" for Muse+Claude Code+Codex (3.3k imp, 18 replies) https://x.com/michellelsun/status/2108334016109920406
- X: @wengyip Hermes+Telegram bot-to-bot group works but "dramatically increases model calls" (cost warning) https://x.com/wengyip/status/2107175575643377916
- X: @dragon_khoi "Bots in Slack require kickoff per task when multiple agents deliberate" (risk: need explicit mention routing) https://x.com/dragon_khoi/status/2107319454543811029

## Build plan: wake-on-mention per agent
Rules for all: reply only when @-mentioned by name or replied-to in thread; max 3 bot-to-bot hops per thread, then stop; ignore own messages; one reply per mention (dedupe by ts).
1. Grok bots (参謀, Anicca Marketer, Fucker, dr eggbot, Forensic Writing, Muse Relay): routine with Slack trigger on #agents-hq (C0CBLBGSBJN), filter "@<name>"; reply in-thread via user-Slack. VERIFY FIRST: that the trigger fires on messages posted by other bots/apps (unverified).
2. Claude Code (Mac mini): CCSC bridge (jeremylongshore/claude-code-slack-channel), own Slack app "Claude", Socket Mode, access.json requireMention=true, allowBotIds=[all team bot ids]. Disabled until tokens return.
4. Muse (terminal@htch-runtime) & Dots (dots-one): Muse/Dots already have Slack logins -> preferably their own Slack integration; else relay: watcher on Mac mini forwards @Muse/@Dots mentions via Reason send_message and posts check_inbox replies back as their bot identity.
5. 成田さん: Slack mobile app, member of #agents-hq (C0CBLBGSBJN).
6. Manager room: 参謀 mirrors key lines both ways.
Done = one thread where 参謀 -> Codex -> Muse reply back-and-forth with no human relay, logged in BOARD.md.

## Impact on #agents-hq (C0CBLBGSBJN) build
No change of platform. Change in method: give each agent its own Slack bot identity and explicitly allow peer bot IDs (otherwise bot messages are dropped), add hop limit for loop/cost control. Fallback if Grok Slack trigger ignores bot messages: Telegram supergroup with bot-to-bot mode.
