# AGENT-RAILS — 受取まで人間ゼロの収益レール（実測台帳）

更新: 2026-11-26 09:5x JST / @pickle（$10k MRR 共同オーナー サイクル1）
計測コマンド: `python3 team/scripts/agent_rails_probe.py` → `team/metrics/agent-rails.json` を上書き（支出・署名・投稿なし）

## 0. レールの定義（この台帳が数えるもの）

**「受取まで含めて人間の銀行口座・人間の認証情報がゼロ」の収益だけを数える。**
どんなに大きくてもこの台帳の**収益に入れない**。`bank_payout` 列に「human」と明記し、別枠で扱う。

## 1. 現在値（2026-11-26 09:4x JST 実測）

| レール | 受取手段 | 人間工程 | 実測値 | 出典 |
|---|---|---|---|---|

**この台帳の収益合計（人間ゼロで実際にエージェントの口座に入った額）: 0.25 USDC（make.fun）。**
x402 の 0.976 USDC は「入っているが、鍵の所在が未確認」なので**収益に数えない**（§3-1）。

## 2. 参考: 銀行口座に落ちる（=この台帳の外）既存面

| 面 | 未出金/実績 | 受取先 |
|---|---|---|
| App Store (RevenueCat) | MRR $20（anicca 5 subs） | Apple → 本人名義 = human |
| CrowdWorks | 未出金 223円（出金下限 530円未満） | 本人名義 = human |
| Upwork | 受取 $0.00（11/24 の $15.00 は Connects 購入） | 本人名義 = human |

これらは「並行・補助」レーンとして継続するが、本サイクルの主軸・報告の筆頭にはしない。

## 3. 計測漏れの修復（今回やったこと）

1. **エージェント決済レールの計測ファイルが存在しなかった** → `team/metrics/agent-rails.json` + `team/scripts/agent_rails_probe.py` を新設（毎回同じコマンドで再現）。
4. **Agoragentic の出品/審査/sandbox 状態を実測化**（従来は「listing 0件・revenue $0」の手書きメモのみ）。

## 4. 見つかった本当のボトルネック（次サイクルの対象）

1. **x402 の payTo 秘密鍵がチームのどこにも無い**（credentials.json の全 hex64 鍵 54 本から導出したアドレスに `0x6592…EDc7` が無い）。＝ 0.976 USDC は「誰も使えない可能性のあるアドレス」に入っている。**受取をエージェント所有ウォレット `0x6664…F18A`（鍵あり）へ変えるのが最優先の1手**（x402 サーバのデプロイ権者＝owner 作業）。
2. **x402scan 登録: 最終 9/9 完了**（origin 一括 200 ＋ 個別 6 本 ＋ 初回 422 の 3 本を1本ずつ再送して 200）。初回の 422（`/focus-coach` `no402`, `/prompt-sanitizer` `no402`, `/habit-designer` `Missing input schema`）は**probe の一時失敗**で、OpenAPI の `x-payment-info`・schema は正常だった。**同じ 422 を恒久欠陥と誤判定しないこと**（1回リトライが正解）。
3. **POST only のため HEAD が 404**（Agoragentic の preflight が警告）。HEAD/GET に 200 を返すだけでディレクトリ審査の摩擦が消える。
4. **Agoragentic は市場ごと停止中**（platform_custody_frozen）。出品は済ませたので、`market.json` が `paid execution enabled` に変わるのを監視するだけでよい（毎日1回、コスト0）。
5. **make.fun は期待値がほぼ宝くじ**: open 171件、上位は $1,000（bounty-entrants-03）／$500／$250。token-radar 系は応募3万件超で1件あたり $0.001 台。**大型かつ応募が少ない bounty が出た時だけ**打つ。

## 5. 判定ルール（この台帳の使い方）

- `unknown` を 0 と書かない。停止中の面（Agoragentic）は `0 revenue` ではなく `0（platform frozen）` と書く。

---

## 6. 付録: サイクル1で棚卸しした全プラットフォームの計測状態

指示に挙がっていた面を、**今この瞬間に読めた値 / 古い値 / 未計測**の3つに仕分けた（2026-11-26 09:4x–10:0x JST）。
「古い」は最終読取日を、「未計測」は計測手段が無い理由を書く。**0 と unknown は別物**として扱う。

| 面 | 状態 | 実測値 / 理由 | 出典 |
|---|---|---|---|
| **Agoragentic** | 計測済み（今日） | 出品1件 approved/reachable・売上 $0（市場停止中） | `agent-rails.json` |
| **Apify** | 古い（11-24 08:45） | users 1 / runs 29 / 収益 source error。actor 3本 public 化は別run（09:02） | `team/metrics/apify-latest.json` |
| **RapidAPI** | 未計測 | 公開ページに加入者/コール数が無く、Provider Dashboard の資格が箱に無い | `rapidapi-latest.json` |
| **Capafy** | 古い（11-22） | MTD 818 paid / gross $92.91 / net $59.94、未出金 $83.78（11/24 は「$83.78 が payout 待ち」） | `capafy-daily.csv`, `capafy-last.json` |
| **CrowdWorks** | 計測済み（今日 06:15） | 進行中5契約すべて進行中、未出金 **223円**（下限530円）、未読0 | `team/LIVE-NOW.md` 2026-11-26 06:15 |
| **Upwork** | 計測済み（今日 08:15） | Connects 7、受取 **$0.00**（11/24 の $15 は Connects 購入 −$15.00）、累計 Connects 支出 −$54.00 | `team/LIVE-NOW.md` 2026-11-26 08:15 |
| **Lancers** | 未計測（今日は不能） | 全社緊急メンテナンス（11/26 08:00 再開予定）→ 再開後の実読が必要 | `team/LIVE-NOW.md` 2026-11-26 04:15 |
| **Coconala** | 古い | 応募中/取引中の現行値が metrics に無い（11/20 記録: 応募中90件・取引中0） | `team/LIVE-NOW.md` 2026-11-20 |
| **Wantedly** | 計測済み（今日 06:15） | 本日3件エントリー（Starley 2444291 / Open Reach Tech 2491959 / クロスメディスン 2430300） | `team/LIVE-NOW.md` |
| **Workship** | 計測済み（今日 08:15） | Caluck Pythonテックリード 11/26 付で送信（`/like/initiative` 実画面） | `team/LIVE-NOW.md` |
| **TimeTicket** | 未計測 | 現行の受注/売上を読む手段が箱に無い（過去の提出記録のみ） | — |
| **TikTok / Instagram / YouTube / LinkedIn** | 未計測（停止中） | Postiz 経由の投稿は別レーン。アカウント別の views/CVR は metrics に無く、今は投稿停止（IG login-save 待ち） | Fo night30 report 2026-11-25 |
| **アプリ（App Store）** | 古い（11-22） | installs 2 + 1（11/22）、RC MRR $20、収益 $0 | `tracking-summary.json` |
| **SEO（GSC）** | 古い（11-22） | last7 clicks 11 / impressions 2,392 | `tracking-summary.json` |

**この棚卸しで分かった計測の穴（次の資産）**
1. `unknown` が「0」として語られがちな面: RapidAPI・TimeTicket・Coconala 現行値。→ ダッシュボードでは `unknown` のまま固定する（0 にしない）。
2. ソーシャル4面（TikTok/IG/YT/LinkedIn）は**アカウント別の views/CVR を誰も記録していない**。投稿が止まっている今は影響が小さいが、再開時に最初に作るべき表。
3. Capafy/App Store は銀行口座に落ちるため、この台帳（AGENT-RAILS）の外。混ぜないための境界線は §0 に定義済み。
