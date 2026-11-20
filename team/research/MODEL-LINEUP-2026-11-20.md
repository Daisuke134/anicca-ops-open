# Model lineup — 2026-11-20 (from an unverified Japanese X post, then live-checked)

Source list: 成田さん 2026-11-20 22:13–22:25 JST asked us to learn from a Japanese X post of “best models per role,” plus OpenCode Go / Command Code $10 plans, Sakura Internet free API, and a Prime Intellect RL Residency post. **The X-post names are marked unverified until a live API listed them.**

Checked 2026-11-20 22:40–22:50 JST (Asia/Tokyo):

- Command Code `GET https://api.commandcode.ai/provider/v1/models` via curl, agent GOAT key (not printed): **HTTP 200, 105 models.** No prices on this endpoint.
- OpenRouter `GET https://openrouter.ai/api/v1/models` with the company key `credentials.json` `service: "openrouter-anicca-bounty-build"` (not a human Gmail key, not printed): **HTTP 200, 442 models.** Prices below are USD **per 1M tokens** (prompt / completion), converted from OpenRouter’s per-token fields × 1e6.
- OpenCode Go is **not subscribed**. Free OpenCode models already run on this box.
- Sakura Internet free API is a product signup (phone + card); no key yet. See `team/applications/compute/sakura-ai-engine.md`.

## Role map

The table was drafted by Command Code `z-ai/glm-5.3-flash` (task `team/cc-tasks/2026-11-20/lineup-role-map.task.md`, 19.7 s, finish=stop) and then checked against the live id/price lists. Do not treat the X-post names as official ids.

| Role | Requested (unverified X-post name) | Best available now | Approx cost (OpenRouter, $ / 1M in / out) | Notes |
| --- | --- | --- | --- | --- |
| General best / reasoning | Gemini 4 Neon | OpenRouter / Command Code `google/gemini-4-neon` (CC id `google/gemini-4-neon`) | 3 / 15 | Listed on both. Too expensive for routine workers. |
| Hard reasoning | Opus 5.5 | OpenRouter `anthropic/claude-opus-5.5`; Command Code `claude-opus-5-5` | 4 / 20 | Listed on both. Not a cheap-worker default. |
| Fast coding | GPT-Sol-6.2 Fast | **Exact “Fast” id not found.** Closest: OpenRouter `openai/gpt-6.2-sol`; Command Code `gpt-6.2-sol` | 2 / 10 | Use only if a coding task actually needs this class. Default coding worker stays DeepSeek / GLM Flash. |
| Writing / Fable | Fable 5.2 | OpenRouter `anthropic/claude-fable-5.2`; Command Code `claude-fable-5-2` | 8 / 40 | Listed on both. Expensive. |
| Computer use | GPT-Sol-6.1 Terra Fast | **Exact “Fast” id not found.** Closest: OpenRouter `openai/gpt-6.1-terra`; Command Code `gpt-6.1-terra` | 1 / 5 | Name “Terra Fast” unverified. |
| Long agent | GPT-6.2 Astra | OpenRouter `openai/gpt-6.2-astra`; Command Code `gpt-6.2-astra` | 8 / 40 | Listed on both. Expensive. |
| Bulk | Gemini 4 Hydrogen / DeepSeek V4.1 1017 | OpenRouter `deepseek/deepseek-v4.1-flash-1017` (best bulk price) and `google/gemini-4-hydrogen` | 1017: 0.036 / 0.50; Hydrogen: 1.5 / 7.5 | **Neither 1017 nor hydrogen is on Command Code `GET /models`.** On Command Code, bulk = GOAT-boosted `deepseek/deepseek-v4.1-flash` (OpenRouter list price 0.0507 / 0.2028, but billed against the $100 GOAT boost). |
| Classification | Liquid d1.2 / Gemini Decision 1 | **Those exact names were not found.** Closest verified: OpenRouter `liquid/lfm-3-1.7b` (0.08 / 0.20) and `liquid/lfm-3-1.7b:free` (0 / 0); also `liquid/lfm-2.5-24b-a2b` (0.05 / 0.70) | see left | No “Gemini Decision 1” on either catalog. Do not invent an id. |
| Cheap coding | GLM-5.3 | Command Code `z-ai/glm-5.3-flash` (GOAT boosted) or `zai-org/GLM-5.3`; OpenRouter `z-ai/glm-5.3-flash` / `z-ai/glm-5.3` | Flash 0.0399 / 0.0784; full 0.0699 / 1.40 | Preferred cheap alternative to DeepSeek when DeepSeek returns empty content on long tasks. |
| $10 plans | OpenCode Go & Command Code GOAT | Command Code **GOAT already paid** ($10.78/mo, credits reset 2026-12-20). OpenCode Go **not signed up** (packet `team/runbooks/OPENCODE-GO-SIGNUP.md`) | $10 / $10.78 per month | Free OpenCode models work today: `opencode/deepseek-v4.1-flash-free`, `opencode/glm-5.3-flash-free`. |
| JP free API | Sakura Internet | さくらのAI Engine 基盤モデル無償プラン, up to 3,000 Chat Completions req/month | ¥0 inside the cap | Signup needs phone + credit card. No key yet. |

Image / video / music / TTS lists from the same X post were **not checked in this pass** (no catalog names were provided beyond the mention). Do not invent a media stack from memory.

## Tiny real tests (this run)

All via `team/scripts/cc-worker.sh`, agent GOAT key, no secrets in the task files. Log: `team/state/cc-worker-log.md`.

| Time (JST) | Model | Task | Result | Proof |
| --- | --- | --- | --- | --- |
| 22:4x | `deepseek/deepseek-v4.1-flash` max_tokens=1024 | Draft the role-map table | FAIL `finish=length` (content empty after the worker’s fence strip) | Retried on GLM |
| 22:4x | `z-ai/glm-5.3-flash` max_tokens=2048 | Same role-map table | **OK**, 19.7 s, in=965 out=1407, finish=stop. Table checked against the live catalogs | `team/cc-tasks/2026-11-20/lineup-role-map.result.md` |
| 22:4x | `z-ai/glm-5.3-flash` max_tokens=2048 | Priority list for compute packets | **OK**. Used as a draft; the ledger in `team/applications/COMPUTE-PROGRAMS.md` is the verified copy | `team/cc-tasks/2026-11-20/compute-priority.result.md` |
| 22:4x | `deepseek/deepseek-v4.1-flash` max_tokens=512 | Two-sentence company blurb from given facts | **OK**, 2.4 s, in=155 out=242, finish=stop. Facts preserved ($2,188, $24 MRR, 7 subs, $0 raised, six apps, not incorporated, /open URL) | `team/cc-tasks/2026-11-20/one-line-blurb.result.md` |

Earlier the same day (19:59 JST, already in the cheap-workers runbook): both `deepseek/deepseek-v4.1-flash` and `z-ai/glm-5.3-flash` returned `OK` on a “reply with OK” smoke test. GLM needs max_tokens ≥ 256 because it spends reasoning tokens first.

Frontier models (Neon, Opus 5.5, Astra, Fable 5.2) were **listed** but **not** called in this pass, to avoid burning GOAT / OpenRouter credit at 50–400× the cheap-worker price.

## Routing (what every agent should actually call)

Updated in `team/runbooks/CHEAP-WORKERS-OPENCODE-COMMANDCODE.md` and `team/runbooks/CHEAP-WORKERS-FOR-EVERY-AGENT.md`:

1. **Default worker:** Command Code `deepseek/deepseek-v4.1-flash` via `cc-worker.sh`.
2. **If DeepSeek hits empty content / length on a real task:** `z-ai/glm-5.3-flash` with max_tokens ≥ 256 (8000–12000 for code).
3. **Overflow:** OpenCode free models, or Command Code free ids, or (company OpenRouter key only) `deepseek/deepseek-v4.1-flash-1017`.
4. **Do not** route routine drafting or bulk jobs to Neon / Opus 5.5 / Astra / Fable 5.2 / Hydrogen. Use those only for a named hard task after a cost check.
5. **OpenCode Go** paid ids (`opencode-go/deepseek-v4.1-flash`, `opencode-go/glm-5.3-flash`) become the OpenCode default only after the signup packet is completed and the key is in the store.
