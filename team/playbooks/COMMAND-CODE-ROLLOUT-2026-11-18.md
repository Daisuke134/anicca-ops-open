# Command Code + OpenCode 全環境ロールアウト（Mac mini / 各VM / 各エージェント）

作成: 2026-11-18 / @pickle（大祐さん指示「Mac mini や各VMのすべてに Command Code と OpenCode を導入して、全エージェントがお互いに委任・利用できるように。$10プランで最新GLM/DeepSeekがほぼ無料」に対応）
状態: **導入・設定の手順は確定。APIキーだけが本決済の完了待ち**（キーが入ればそのまま実走可能）。

---

## 1. 実測済みの事実（2026-11-18）

| 項目 | 値 |
|---|---|
| npm パッケージ | **`command-code`**（v1.90.0 / `engines.node >=22`） |
| 入る実行ファイル | `cmd` / `cmdc` / `command-code` / `commandcode`（すべて `dist/index.mjs`） |
| 設定ディレクトリ | **`~/.commandcode/`** |
| 認証ファイル | **`~/.commandcode/auth.json`**（本番。`auth.local.json` / `auth.staging.json` は環境別） |
| 設定ファイル | **`~/.commandcode/config.json`**（`config.local.json` / `config.staging.json`）、ほかに `settings.json` / `settings.local.json` / `providers.json` / `mcp.json` |
| APIキー環境変数 | **`COMMAND_CODE_API_KEY`**（CLIとAPIで同じキーが使える） |
| BYOKローカルのみ | `CMD_LOCAL_ONLY=1`（= `--local-only`） |
| 認証確認コマンド | `cmd status` / `cmd whoami` / `cmd auth login` |
| APIキー発行 | **https://commandcode.ai/settings/keys**（GOAT以上。GoプランはAPI不可） |
| API エンドポイント | `https://api.commandcode.ai/provider/v1`（OpenAI Chat Completions `/chat/completions`・Responses `/responses`・Anthropic Messages `/messages`・`/models`） |
| OpenCode | `opencode-ai` v1.19.5。設定は **`~/.config/opencode/opencode.jsonc`**。Command Code を OpenAI互換プロバイダとして登録でき、`opencode models` で **commandcode/ 95モデル**が見えることを実測確認済み |

---

## 2. インストール（Mac mini / Linux VM 共通）

```bash
# Node 22 以上が必須
node -v            # v22.x 以上
npm i -g command-code
cmd --version      # 1.90.0 系

# 認証（2通り）
#  (a) APIキー方式＝無人・推奨
mkdir -p ~/.commandcode
export COMMAND_CODE_API_KEY='<credentials.json の commandcode.api_key>'
echo 'export COMMAND_CODE_API_KEY=...' >> ~/.zshrc   # Mac mini は ~/.zshrc、Linux は ~/.bashrc
cmd status         # → authenticated になればOK
#  (b) ブラウザ方式（127.0.0.1 コールバックが必要なので、そのホスト上で人が操作する場合のみ）
cmd auth login
```

- `~/.commandcode/` を**各ホストへコピーすれば認証を引き継げる**（`auth.json` にトークンが入る）。キー配布より安全なので、Mac mini と各VMは **`credentials.json` の `commandcode.api_key` を1箇所から読む**か、`auth.json` を scp する。
- 無人実行は `cmd -p "…" --output-format json`（非対話）。CI等では `--permission-mode dont-ask` と `--skip-onboarding` を併用。

## 3. OpenCode に Command Code を差す（このVMで実証済み）

`~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "commandcode": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Command Code (GOAT)",
      "options": {
        "baseURL": "https://api.commandcode.ai/provider/v1",
        "apiKey": "{env:COMMAND_CODE_API_KEY}"
      },
      "models": {
        "deepseek-v4.1-flash": { "name": "DeepSeek V4.1 Flash" },
        "glm-5.3-flash": { "name": "GLM-5.3 Flash" },
        "ling-3.1-flash": { "name": "Ling 3.1 Flash" }
      }
    }
  }
}
```

確認:
```bash
opencode models | grep '^commandcode/' | wc -l   # 95（実測）
opencode models | grep 'commandcode/deepseek-v4.1-flash'
```
- 起動後に `/models` で `commandcode/deepseek-v4.1-flash` 等を選ぶ。APIキーが未設定だと 401 になる（`opencode.jsonc` 自体の読み込みは通る）。
- 他のエージェント（Muse/Codex/Grok）に委任するときは、**同じ `COMMAND_CODE_API_KEY` を渡すだけ**。共有方法は `credentials.json` の1行（`commandcode.api_key`）を参照させるのが正本。

## 4. 各エージェントの使い分け（相互委任の形）

| 用途 | コマンド | 備考 |
|---|---|---|
| 単発の実装・修正を投げる | `cmd -p "<依頼>" --output-format json` | ヘッドレス。結果をそのままファイルへ |
| 既存セッション継続 | `cmd -c "<追記>"` / `cmd -r <name>` | `--name` で名前付けすると委任が追いやすい |
| モデル指定 | `cmd -m deepseek-v4.1-flash -p "…"` | `cmd --list-models` で一覧 |
| 他エージェントから HTTP で | `POST https://api.commandcode.ai/provider/v1/chat/completions`（`Authorization: Bearer $COMMAND_CODE_API_KEY`） | OpenAI互換。Anthropic SDK なら `/messages` |
| OpenCode 経由 | `opencode run -m commandcode/deepseek-v4.1-flash "…"` | 設定は §3 |

## 5. コスト（GOAT $10/mo）

- GOAT = **$10/月＋processing fee**で**最大$100クレジット**（+deals）。DeepSeek V4.1 Flash / GLM-5.3 Flash / Ling 3.1 Flash に各 $100 の枠（`/pricing` 2026-11-18 実測）。
- **実請求は JPY 建て**: `GOAT ￥1,657 ＋ processing fee ￥129 ＝ ￥1,786/月`（税￥0、1USD=165.7042JPY 時点）。
- API利用は**キー1本を全ホストで共有**すればクレジットも1つに集約される（残量は Studio > Billing / Usage で確認）。

## 6. 残ブロッカー

1. **決済が未完了**（Stripe hCaptcha / Link の `問題が発生しました`）。→ `team/playbooks/NO-HITL-LINK-CHECKOUT-2026-11-18.md` §4-5
2. APIキーは**GOAT有効化後**に https://commandcode.ai/settings/keys で発行 → `credentials.json` の `commandcode.api_key` に記録（未発行のため現状は空）。
