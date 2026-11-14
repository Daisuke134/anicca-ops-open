# AGENT-RECRUITING — ChatGPT ログインで使えるエージェントと無料アシスタント（2026-10-30 JST 参謀/executor）
出典: OpenAI Help「Using your ChatGPT plan in other apps」(help.openai.com/en/articles/20001542)、learn.chatgpt.com/docs/sign-in-with-chatgpt（パートナー一覧）、devin.ai/blog/sign-in-with-chatgpt (2026-09-29)、blog.kilo.ai/p/sign-in-with-chatgpt (2026-09-29)、kilo.ai/docs、aidedex.com 2026 ガイド、hermes-agent.nousresearch.com/docs (Photon)、openclaw.ai、inkbox.ai。

## 前提（大事）
- 「ChatGPT プランを使う」許可は Go/Plus/Pro のみ。成田さんは Pro（cfo/EXPENSES.md）。
- 外部アプリの利用は **成田さんの同じ Codex/ChatGPT Work 枠から減る**（枠は増えない）。ChatGPT 設定でアプリごとの週上限を必ず設定。
- 「サインインだけ」と「プラン使用」は別許可。アプリ自体の有料プラン料金は別（例: Devin は Devin Pro 以上が必要）。

## ランキング
| # | 名前 | 何をする | 費用 | サインイン経路 | 引き取れるループ |
|-|-|-|-|-|-|
| 1 | Codex CLI（既存 bin/codex-run.sh） | box 上でコーディング実行 | ¥0 追加（Pro 枠） | `codex login --device-auth`（ChatGPT） | Capafy修正・スクリプト・Postiz self-host 移行 |
| 2 | OpenCode（OSS） | ターミナル型コーディングエージェント、並列可 | 無料＋Pro 枠 | ChatGPT プラン連携（公式 OSS 連携） | Codex の予備・並列ジョブ |
| 3 | Kilo Code（CLI/Cloud Agents/Code Review） | コーディング、クラウドエージェント、PR レビュー | サインイン無料・推論は Pro 枠（Cloud 計算は別料金） | 「Continue with ChatGPT」→ BYOK で ChatGPT 接続 | GitHub PR レビュー、Fucker の Capafy 作業の分担 |
| 6 | Devin（Cloud/Desktop/CLI） | 自律コーディング | Devin Pro 以上が必要（料金は要確認）＋Pro 枠 | Sign in with ChatGPT | 大きめの開発タスク（有料なので後回し） |
| 7 | Warp / Amp Code / Conductor | ターミナル/コーディング | アプリ側料金は要確認＋Pro 枠 | ChatGPT プラン パートナー | Codex と重複 |
| 8 | OpenClaw（OSS） | 29チャネル対応の個人エージェント | 無料（モデル代別、ChatGPT OSS 連携あり） | 自前インストール | Hermes と重複。ClawHub に危険スキル多数(ClawHavoc)→非推奨 |
| 9 | Meta Muse / Lindy / Instinct | 秘書系 | Muse 無料枠／Lindy 試用7日後 $49.99〜／Instinct 招待制 | 各サイト | 優先度低 |
- Cursor: ChatGPT プラン パートナー一覧に無し（既に Super に含まれる）。Cline/Zed も対象外。

## 上位5の導入手順
1. **Codex CLI**: bash -n 済み（構文OK）。成田さんの ChatGPT で `CODEX_HOME=/home/box/.codex-chatgpt codex login --device-auth`（1:1チャットで本人がコード入力）。ChatGPT 設定で週上限を設定。
2. **OpenCode**: `npm i -g opencode-ai` → `opencode auth login` で ChatGPT 選択。`team/bin/opencode-run.sh` を codex-run.sh と同形で作成。
3. **Kilo Code CLI**: Continue with ChatGPT でアカウント作成→BYOK で「OpenAI (ChatGPT subscription)」接続（APIキー欄は使わない＝従量課金になる）。Cloud Agents の計算費は使わない設定。
- 共通: 各アプリに ChatGPT 側で週上限（例 Pro 枠の10%ずつ）。BOARD.md に記録。

## 追記 2026-10-30 14:45 JST（executor）: Town 追加・上位8と登録に使う身元
- **Poke**: Free $0 / Pro $19 / Ultra $199。登録は電話番号必須。Gmail/Outlook のみ連携（AgentMail は連携不可→メール機能は使えない、チャット＋Web検索＋リマインド用）。
- Inkbox の身元確認（MCP, 14:40 JST）: 現在の身元 managerjghh は **メール [redacted-email] のみ、電話番号は未割当**。他に anicca-agent / aiclips-agent-11a830 の身元あり（電話番号は未確認・切替は未実施）。

### 上位8（登録はまだしていない）
| # | 名前 | 経路 | 身元 | 費用 | 引き取るループ |
|-|-|-|-|-|-|
| 2 | OpenCode | ChatGPT プラン連携 | 同上 | ¥0 追加 | Codex の並列・予備 |
| 3 | Kilo Code | Continue with ChatGPT | 同上 | 無料（Cloud 計算は使わない） | PR レビュー |
| 4 | Hermes Agent | box に入れて ChatGPT プラン接続 | メール: [redacted-email]、Telegram bot | 無料 | 受信箱トリアージ・日次レポート（参謀の使用量を減らす） |
| 5 | Town | メール登録→ Telegram/メールで使う | [redacted-email]（LM 秘書用途） | Free（月30チャット） | 成田さんの予定・リマインドの下書き |
| 6 | Poke | 電話番号で登録 | Inkbox 番号（未割当→先に用意）＋ [redacted-email] | Free | 軽いリサーチ・リマインド |
| 7 | instinct / cue（既存） | 既存の登録のまま | 既存 | 既存 | 現状維持、担当を LOOPS.md で明記 |
| 8 | Devin | Sign in with ChatGPT | 成田さんの ChatGPT | Devin Pro 以上が必要（有料・料金未確認）→ 保留 | 大きな開発 |
- ChatGPT ログイン系（1〜3, 8）は成田さん本人のアカウントなので、ログインは成田さんの 1:1 チャットで本人がコードを入れる。ChatGPT 側でアプリごとの週上限を設定。
