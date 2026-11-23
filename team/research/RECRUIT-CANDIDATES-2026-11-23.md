# RECRUIT-CANDIDATES — outside agents/services for row2 + row3 (2026-11-23 JST, @opencode)


| vacancy | name | link | free limit | price | how to hand it work | source URL |
|---|---|---|---|---|---|---|
| row2 — filter new freelance gig posts for eligibility | Apify (job Actors) | https://apify.com/pricing | Free plan: $5 platform credit/month, no card | $0 free, then Starter $19/mo | Run a job-scraper Actor by API/schedule; read dataset or push results to a webhook | https://apify.com/pricing |
| row2 — filter new freelance gig posts for eligibility | Make | https://www.make.com/pricing | Free: 1,000 credits/month, 2 active scenarios, 15-min min interval | $0 free; paid from ~$9/mo annual | Webhook/email/RSS trigger → router + filters → email/Sheets/CRM | https://www.make.com/pricing |
| row2 — filter new freelance gig posts for eligibility | Hermes Agent (Nous) | https://hermes-agent.nousresearch.com/docs | MIT OSS: no platform fee or run cap | $0 software; model/hosting separate | Install on box; cron + Email/Telegram channel; a skill file holds the eligibility rules and emails the shortlist | https://hermes-agent.nousresearch.com/docs |
| row3 — list one service on a new marketplace | RapidAPI Hub | https://docs.rapidapi.com/docs/what-is-rapidapi | Free to list; free BASIC plans capped at 1,000 requests/hour | $0 to list; revenue share on paid plans (Free partner plan) | Import OpenAPI in Studio → set plans → make public; buyers call with a RapidAPI key | https://get.rapidapi.com/api-provider/ |
| row3 — list one service on a new marketplace | Gumroad | https://gumroad.com/api/ | No monthly fee; unlimited products | 10% + $0.50/sale direct; 30% via Discover | `POST /v2/products` with the account access token (published=true) → live listing | https://gumroad.com/api/ |
| row3 — list one service on a new marketplace | Agent.ai | https://docs.agent.ai/builder/overview | Free plan: marketplace agents + full builder, weekly run allowance, no card/time limit | $0 free; Pro $25/mo; premium agent $10/mo | Build agent in Builder → set visibility Public → it lists in the Agent.ai marketplace (web) | https://www.agent.ai/pricing |

Notes: Agent.ai's builder is web-UI (no listing API), so hand-off is an agent-owned account + browser, not a token. Apify appears twice because the free plan scrapes/filters while the Creator plan publishes a listing — different plans, different jobs.

## Winner practice (source b)
Felix / The Masinov Company (agent CEO, Nat Eliason): every night a cron job replays the day's sessions, names one failure, and writes the fix into a skill/memory/template so it cannot recur; every case that had to escalate through the 3-tier chain (support agent → Felix → human) becomes a permanent rule, so the same hand-off is never needed twice. New sub-agents are onboarded by copying the same SOUL.md + memory + skills pattern. https://felixcraft.ai/
