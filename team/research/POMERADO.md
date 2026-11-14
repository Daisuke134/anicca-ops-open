# Pomerado — 評価 / Evaluation (2026-10-26 14:4x JST, 参謀)

## 判定 / Verdict: ADOPT (pilot, behind flag)
- JA: ブラウザ操作で毎回やっている定型作業を「決定的なMCPツール」に変える。速く安く再現性が高い。認証情報は保存しないので、LM Cloudでは顧客ごとにシークレット保管庫から都度渡す設計が必要。
- EN: Turns repeat browser chores into deterministic MCP tools. Faster/cheaper/reproducible vs computer-use. Self-host OSS core; do NOT depend on Pomerado Cloud (saved logins) for customer data.

## Sites first / 最初の対象
Anicca ops (internal, low risk): 1) Capafy agent submit/version upload (top revenue, browser-only today) 2) Coconala DM read/reply-draft 3) Lancers board read 4) PROSRV-type form portals. ASC: has an official API — use API first; Pomerado only for Resolution Center gaps.

## Integration plan
1. Box/Mac mini: install, `--root ~/pomerado-integrations`, mint "Capafy: upload new agent version" + "Coconala: list unread DMs". Measure time vs browser.
2. LM Cloud PR #8745 action layer: adapter `actions/pomerado` behind flag `LM_ACTION_POMERADO=0` default; per-tenant integration dir; creds injected per call from tenant vault; read-only actions first; audit log each call.
3. Keep computer-use as fallback when an integration fails self-heal.
Owners: main-claude-2 (LM Cloud adapter), claude-2 (ASC/Capafy ops minting).
