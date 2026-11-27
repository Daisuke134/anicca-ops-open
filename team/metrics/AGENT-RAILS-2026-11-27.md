# AGENT-RAILS — 2026-11-27（日次計測・配布面の拡張）

計測: 2026-11-27 10:09 JST / @pickle
計測器: `python3 team/scripts/agent_rails_probe.py` → `team/metrics/agent-rails.json`（read-only、支出・署名・投稿なし）

## 1. 前日差（2026-11-26 09:49 → 2026-11-27 10:09 JST）

| 面 | 11-26 | 11-27 | 差 |
|---|---|---|---|
| make.fun 受取（Solana USDC, 自前 keypair） | 0.25（paid, tx `kNVuYw…LTh8C`） | 0.25 | **±0** |
| make.fun 参加可能 competition | 171 open | 47 open | −124（波が終了） |
| x402 payTo `0x6592…EDc7`（Base USDC） | 0.976 | 0.976 | **±0（24h 新規入金なし）** |
| x402 台帳 `x402_inflows.jsonl` | $0.01（2 call） | $0.01 | ±0（差額 0.966 は未回収のまま） |
| エージェント基軸ウォレット `0x6664…F18A` | 0.000 | 0.000 | ±0 |
| Agoragentic | `temporarily_unavailable`（platform_custody_frozen） | 同左 | **変化なし＝市場停止継続** |


## 2. 3判定

2. **Agoragentic ゲート**: `market.json` の `payment.wallet.status = temporarily_unavailable`（reason `platform_custody_frozen`）、`x402_edge.status = temporarily_unavailable`。出品は 1件 approved / sandbox reachable / free slots 0 のまま → 指示どおり何もしない（復帰した日だけ sandbox 再確認）。
3. **新規供給（make.fun）**: 全 open を API で取得（`/api/competitions?status=open`、500件上限）→ **期限が未来かつ応募 < 500 は 5件、すべて $5（AgentQuest Moment of the Day）**。**賞金 ≥ $50 かつ応募 < 500 は 0件**（$50 以上はすべて応募 ≥ 500、最大は token-radar-01 $1,325 / 35,281 応募）→ **打つ対象なし**。

## 3. 今日やった改善: 配布面（discovery）を x402scan から4面へ拡張

x402 は「呼ばれないと0円」。24h で入金 ±0 の原因は需要ではなく**発見されていないこと**なので、人間アカウント・支出・ブラウザを使わない無料APIディレクトリへ登録した（全て冪等、`team/scripts/x402_extra_directories.py`）。

| ディレクトリ | 結果（実測） |
|---|---|
| **x402dash** `api.x402dash.com/v1/register` | **5/9 登録・`verified:true`**（context-compressor, focus-coach, prompt-sanitizer, emotion-detector, intent-router）。残り4本は **5件/時/IP の制限で 429** → 11:1x JST 以降に同スクリプト再実行で完了 |
| **hive402** `api/public/list` | **9/9 登録・`verified:true`**（probeReason: *live 402 challenge matches a listed payment route (network, asset, amount, payTo)*）。カタログ 67,168 endpoints / 43,890 probe-verified に対し我々は元々1本（funding-rates, guest 経由）だけだった |
| **SarnAI Agent Discovery Board** | 2件作成（サービス面 `4e55229a-…` / context-compressor `67a74870-…`）。62,000+ services、health check 通過で検索上位5件に出る。10:26 JST に両件 `state:"searchable"` を実測（`GET /listings/{id}/status`） |
| **x402-list.com** | **未実行（$1.00 のフリーホスト審査料）** — 支出は本人判断。応答: `free_host_fee_required`, amount 1,000,000 µUSDC, payTo `0x5da411…6c70` |
| **minia2a.uk** | 保留。EIP-191 署名は無料だが `wallet` 欄に `0x6664…F18A` を書くと実 settlement（`0x6592…`）と食い違うため、payTo 切替後に回す |
| x402scan（週次） | **9/9 再登録 OK、failed 0**（`registered:9, failed:0, deprecated:3`）。deprecated の3件は**実測では全9本が 402 を返しており**（10:12 JST）、死んだ endpoint は確認できず＝フラグの意味は未検証 |

**注意（順序）**: payTo が鍵なしアドレスのままなので、増えた配布面からの売上は当面すべて `0x6592…EDc7` に落ちる。**#690（切り替え）が先、配布拡張はその次**の順を固定する。

## 4. Issue #690 の現状（本日 10:2x JST）

- 状態: **OPEN / assignee なし / PR なし**（`PAY_TO` を含む PR は 0件）。
- 実測: 9 endpoints すべて 402、`payTo=0x6592…EDc7` で不変。`/funding-rates` は **GET**（POST は 404）。
- 切り替えの実体: `Daisuke134/anicca-products` `apps/x402-agents/src/server.js:131` `const PAY_TO = process.env.X402_WALLET_ADDRESS;` → **Railway の環境変数1つ**。コード変更は不要。
- ブロッカー（実測）: チームの Railway 認証は**全部無効** = `railway-existing-cli-session` は 2026-11-10 18:22 JST 期限切れ、旧セッションは 2026-10-22 に `rejected_by_official_cli`、`anicca-railway-api` は backboard GraphQL で "Project Token not found" / "Not Authorized"。→ **新しい Railway ログインなしには誰もデプロイ不能**。Codex は 11/27 08:23 JST に使用上限で停止。
- 対応: #690 に担当（@devin）へ 12:00 JST 期限で実測＋選択肢(a)完了/(b)BLOCKED の1行を要求（https://github.com/Daisuke134/anicca-ops/issues/690#issuecomment-7207195693）、#539 に持ち場確定のポインタ（https://github.com/Daisuke134/anicca-ops/issues/539#issuecomment-7207196811）。Pickle は引き取らない。

## 5. 次にやること（明日の計測で自動的に判定できる形）

1. #690: devin の ACK、または「Railway の project/service/environment とオーナー1操作」の特定 → 本人向け1操作として整理。
2. x402dash 残り4本: `python3 team/scripts/x402_extra_directories.py --only x402dash`（11:1x JST 以降、429 が消えていれば4本登録）。
4. Agoragentic: `market.json` が `operational` に変わった日だけ sandbox 再確認。
