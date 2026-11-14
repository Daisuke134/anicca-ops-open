# TEAM-CHAT-DECISION v2 (2026-10-27 12:35 JST) — supersedes v1 (kept in TEAM-CHAT-DECISION.v1.md)
Page: https://cursor.com/canvas/store-965ea9ad-f5ce-4294-abc1-5ed7c16986c1/63a89529-fc53-4ae7-b16e-ce4e79f45327
Criteria (成田さん t1131-t1134): #1 closeness to the Grok Bot Manager room (one chat, own name+avatar, addressed agent wakes itself, agents reply to each other, phone app). #2 easiest/fastest/cheapest setup. Score = close*3 + setup*3 + wake*2 + phone*2 + fit + reliability + cost + adoption (max 75). 38 options, 20+ X posts, GitHub stars fetched 10/27.

## Winner: new Grok Bot group room "HQ" + one proxy Grok agent per external agent
- Non-Grok agents cannot join a Grok room directly (rooms hold Grok Bot agents only, max 6; channels connectors only bridge Slack-style inbound to ONE agent). So: proxy agents "Codex", "Claude", "Muse", "Dots"; each, on its turn, relays to the real agent and pastes the real reply under its own name.
  - Muse/Dots: Reason send_message, wait up to 3 min on check_inbox; else post "waiting" and paste next turn.
- Manager room is full (6) -> HQ is a separate room: 参謀 + Codex + Muse first, then Claude + Dots (6 max).
- Latency (estimated, not measured yet): Grok<->Grok tens of seconds; Codex proxy 30-120 s; Muse/Dots via Reason 1-several min.
## Shortest path to live 3-agent back-and-forth today
1. dr eggbot creates proxy agents Codex + Muse (one job: relay, never answer themselves) ~10 min.
2. Create group room HQ with 参謀 + Codex + Muse; add 成田さん. ~2 min.
3. Test: 参謀 @Codex -> reply -> 参謀 @Muse "Codexの案どう？" -> Muse -> Codex again. Record timings in BOARD.md. Hop cap 3 bot-to-bot per thread.
## Top 3
1. Grok room + proxies (score 63) 2. Slack #agents-hq, one bot per agent + allowBotIds (57) 3. Telegram group bot-to-bot mode (54)
## Impact on Slack #agents-hq build
Demoted to fallback, not deleted; no new Slack channels. #anicca-hq abandoned. Muse keeps posting in #agents-hq until HQ room works.
## Key evidence
Grok Bot squads talking to each other: https://x.com/itsjcmerlo/status/2105284444881883330 , https://x.com/kaizenbuild/status/2111064076117766319
Slack: https://x.com/sarahwooders/status/2113799139402330425 , https://x.com/kyle_e_walker/status/2113958851624263716 ; Slack Code https://x.com/stretchcloud/status/2090415552317538370
Telegram bot-to-bot: https://x.com/thehypedotnews/status/2056404947755811215 (4.2k views); cost warning https://x.com/wengyip/status/2107175575643377916
Agent Relay OSS (AgentWorkforce/relay 1,035★): https://x.com/DevRyan17_/status/2114170076010357119 ; MCP Agent Mail (2,226★) https://x.com/doodlestein/status/2113384831216161165
Jinxo https://x.com/Y_orruu/status/2112476547483332901 ; Buzz https://x.com/thomasheimann/status/2083290916358348906 ; ClawBud https://x.com/clawbud/status/2096539529351963049 ; Pie https://x.com/s1dashu/status/2054392098489798856
Stars: openclaw 393k, hermes-agent 257k, MetaGPT 71k, autogen 61.6k, crewAI 60k, RocketChat 46k, langgraph 44k, mattermost 39k, chatwoot 38k, ChatDev 34.6k, agentscope 34.3k, AionUi 33.8k, openai-agents 30k, vibe-kanban 28k, A2A 26k, zulip 26k, letta 25k, camel 18k, claude-squad 8.7k, campfire 4.8k, synapse 4.7k, uAgents 1.6k, IBM acp 1.0k (stale 2025-08), coral-server 253, ccswarm 154, ccsc 42, cogent 0.
