# DELEGATION.md — Grok Bot版 (2026-11-01)
JA: 少数の良いボットに、手順はskillとして渡す。参謀(CEOボット)は管理と新ボット作成だけ。新ボットは Dr Eggbot で2体(X Operator / Applications)のみ。引き継ぎは本人に書かせ、初回を確認して旧コピーを止める。ルーチンはイベント駆動・脚本化して Super で同じ成果。
EN: Few good bots; every instruction becomes a skill; CEO bot manages and creates bots, holds few loops; 2 new bots via Dr Eggbot; self-written handoffs, verify first run, stop old copy; event-driven + scripted routines to keep output on Super.
Sources: Grok Bot users only. Notes: team/research/GROKBOT-WINNERS-2026-11-01.md

1. 参謀 = CEO bot: manage, create bots, few hands-on loops. — @Abhinavstwt "CEO bot manages all the other bots and can even create new ones" https://x.com/Abhinavstwt/status/2115064469990572454 ; @chriskim_dev chief of staff, human asks only status/blockers https://x.com/chriskim_dev/status/2115495540129689952
2. Few good bots. Only 2 new (X Operator, Applications), designed by Dr Eggbot. — @poteto https://x.com/poteto/status/2116576229319233596 ; one focused bot per job like tibot https://x.com/poteto/status/2115205951649423585
3. Every handoff = skill + runbook path. Tell the owner bot to save the instructions as its own skill (store in anicca-ops). — @poteto guide (same) ; @Rasmic skills repo https://x.com/Rasmic/status/2115934131041296822
4. Handoff written by the outgoing owner (roles, memory, routines) → new owner's first run verified in logs → stop old copy. — @realmikeredler https://x.com/realmikeredler/status/2116659261954531514
5. Each bot gets its own email, accounts, vault entries, connectors. — @poteto guide
6. Cost on Super: weekly ask which bots/routines used most; script repeatable steps; event triggers instead of polling; cap concurrent awake routines; check what really needs the bigger plan. — @BotDirectoryAI https://x.com/BotDirectoryAI/status/2116668898112376838 ; @agentwirenews https://x.com/agentwirenews/status/2116656353238454288 ; @oziyavvo https://x.com/oziyavvo/status/2116672662420193413 ; @NashBriggsy https://x.com/NashBriggsy/status/2116663879820292584
7. Human gets one short sorted digest; posts/sends stay behind approval. — tibot https://x.com/poteto/status/2115205951649423585 ; @oziyavvo (same)
8. Every mistake → workflow/skill change so it never repeats (LEARNINGS.md). — @poteto https://x.com/poteto/status/2115133011352240581
9. Ask Dr Eggbot for routine cadence design. — @tetumemo https://x.com/tetumemo/status/2116673180781904377
Measure: 1 week company-wide output vs Ultra baseline; same or more → Super.

## 移管先の修正（成田さん 2026-11-01 08:38 JST）
参謀のループは Codex / Dots には渡さない（両者の仕事が重要なため）。すべて Grok Bot に渡す。
- X Operator (fc6bc285): X配信、いいね巡回、タイムライン読み、X稼ぎ口探し、勝ち投稿分析
- Applications (1d0470fa): 応募ループ、YC fast-track、Naïve get-in、受託ループの応募部分、Maritime M3
- Fucker: Honne（移管済み）、x402、Life Manager Cloud + Maritime 運用
- Anicca Marketer: Distribution、CMO weekly、Reddit
- dr eggbot: Lancers/CW/ココナラ
