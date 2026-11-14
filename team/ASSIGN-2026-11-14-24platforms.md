# 2026-11-14 割り当て — 24平台/日と4本柱のループ

作成: 参謀 2026-11-14 09:22 JST
きっかけ: 成田さん t3672u。Product / Model / Eval / Client Work の現状、新規登録は毎時誰がやっているか、追加のボットが要るか、$10K MRR に向けて配信とクライアントワークを昼夜回すこと。目標は毎日 24 以上の新規プラットフォーム（配信 + クライアントワーク）。

このファイルを読んだボットは、自分の行を ACTIVITY.md に START / NOW / DONE で書く（RULE 00）。始める前に CLAIMS.md と ACCOUNT-OWNERS.md と team/RULES.md（RULE GOOGLE-SIGNIN-LOCK を含む）を読む。同じ平台を二つで登録しない。Google ログインは開始しない。新規登録は [redacted-email]。ボットへの個別メッセージは参謀が回す。

数字はファイルの実測だけ。無い値は「未計測」と書く。

---

## 1. いまの状態（実測だけ）


| レーン | 担当 | 最後の証拠 | ギャップ |
|---|---|---|---|
| Product | Codex + Muse（参謀が期限を置く） | Anicca 1.9.14 Build 827 が 11/14 05:23 JST に配信準備完了、08:08 JST に READY_FOR_SALE（pickle）。ソフトペイウォールの再測期限は 11/21。ASC 初回DL 直近7日は METRICS-TRUTH 時点で2件（11/13 17:20。11/12・11/13 分は当時未公開）。体験0・購入0が続く | 1.9.14 公開後の初回DLと購入は未計測。#82「How did you hear about us?」は Codex 期限 11/14 14:00。#88 RC 実験停止は Muse 期限 12:00。E2E 画面録画の毎日投稿は未確認 |
| Model | Codex（期限が来たら参謀） | MG-04 は差が無く戻した。MG-06 は acrossgame 系に限定、Codex 期限 11/14 18:00（LOOPS-4PILLARS、参謀 07:45 / 23:5x） | Codex の今朝の ACTIVITY 行はなし。ゲート通過の新しい学習結果は未着 |
| Eval | 参謀（集計）+ Muse（実験台帳）+ X Operator（公開投稿） | BehaviorBench 34タスク: befm 30勝 / qwen 3 / 引き分け1、p=1.4e-6 で KEEP（files/eval/behaviorbench-signtest-34-2026-11-13.md）。5%差では 28/34（23:5x）。系統別は game 9–0、multiround 8–0、acrossgame 6–2 で p=0.29（11/14 07:5x）。X 投稿は 11/14 00:39 https://x.com/diceai0/status/2121266205189382361 | 弱い acrossgame を Model の MG-06 に渡しただけ。新しい評価の追加と、結果を続ける公開（実スクリーンショット）が残る |
| Client work 出品（Mode A） | ココナラ・ランサーズ: dr eggbot。CrowdWorks・Contra: Fucker。Upwork カタログ: dr eggbot。Fiverr は下書き | CLIENT-WORK-TRACKER（11/13 17:12 作成、以降の出品再測はなし）。ココナラ公開20件、30日閲覧319・注文3・売上 ¥39,500（最終実測 11/11、着金の再照合は未完了）。ランサーズ・Upwork・Contra の閲覧は未計測かログイン切れ。Fiverr は未公開。SKIMA は SMS 待ち | サービス別の閲覧が 11/07 以降未測。Upwork / Contra / Freelancer はログイン切れ。新規の出品改善が止まっている |
| Client work 応募（Mode B） | ランサーズ（5627347以外）・ココナラ: dr eggbot。CrowdWorks: Fucker。Freelancer: 参謀。Mercor / Fiverr / Truelancer: dr eggbot | 7日応募（11/07–11/13）: ランサーズ34（受注0、仮払い¥33,000は既存5627347）。ココナラ5（返信0）。CrowdWorks / Upwork / Mercor / Fiverr / Freelancer / Truelancer / Contra は7日応募0。11/14 09:00 dr eggbot: 今日すでにランサーズ3・ココナラ1。11/14 08:32 参謀: Meridial 2件応募。06:22 参謀: Prolific に3件応募（新規平台） | 7日の新規受注は0。CrowdWorks は Vault 未保存で 09:03 にログインできず、未返信が残る。Freelancer 40814224 は未送信 |
| 新規平台の登録 | 単独の毎時ルーティンは無い | 11/12 に「new-platform-new-business-every-day」ルーティンは一時停止（LOOPS-4PILLARS）。直近24時間で登録完了が確認できるのは Prolific（参謀 11/14 06:22、応募3件）の1件。進行中で未完了: MENTA（参謀、未登録）、ComeUp（Dots、11/13 11:18 以降ログなし）、MCPize（Fucker が CLAIM、14:35 実行予定）、ストアカ（Forensic Writing、09:20 に仮登録まで完了、確認メール待ち）、Bing Webmaster（SEO Refresher が 09:11 開始、Google ログインで停止すべき）、AlternativeTo（Citation Scout、hCaptcha で未申請）、There's An AI For That は有料のため見送り、Substack（Muse Relay、未確認） | 「毎時登録」は実際には回っていない。24件/日には足りない |
| 既存の配信 | X Operator（X）、Muse（TikTok / IG / YouTube）、Anicca Marketer（Bluesky / Mastodon / Pinterest / Tumblr）、SEO Refresher、Citation Scout | 11/14 09:20 日次計測: TikTok 7日再生 120,141（前週比 +42,272）。IG 681（-277）。@diceai0 フォロワー 930（前週比 -22）。@selawmqt は13。Bluesky 2垢は49–57時間投稿なし。Muse 担当の TikTok / IG / YouTube に投稿ゼロの垢がある（ASSIGN 09:20） | 既存チャネルの投稿再開と、新規ディレクトリ登録が同時に必要。Google ログインは使わない |
| 公開ダッシュボード /open | Reporter（数字の正本）+ Codex（更新経路）+ 参謀（監視） | 参謀 11/13 21:27 に metrics.json を更新（updated_at=21:15 JST、Nov MTD $31.81、MRR $20）。Muse 11/14 00:32 に one_flesh を追加（ライブ取得は未確認）。data.json は当時30分ごと更新。anicca-ops の open-metrics Actions は 11/12 21:50 以降失敗。METRICS-TRUTH は 11/13 17:20 のまま | metrics.json と METRICS-TRUTH が今朝の財務（08:30）と 1.9.14 公開に追いついていない。Honne $4 を足すかどうかの差（$20 vs $24）は未解消 |

---

## 2. 24平台/日の回し方（既存メンバーで先に回す）

目標は暦日ごとに **新規登録または新規掲載申請が 24件以上**（クライアントワーク 12 + 配信ディレクトリ 12）。既存平台での応募や出品改善は、この24には入れない。別レーンで続ける。

11/12 に止めた「new-platform-new-business-every-day」を、下の分担で再開する。毎時、チームのどこかで完了（または BLOCKED）を1件以上出す。CLAIMS.md に先に書き、同じ平台を取らない。証明は ACTIVITY.md の1行（平台名、signed-up / listed / applied / BLOCKED、公開URLまたは止め理由）。

新規登録のメールは [redacted-email]。Google ログインは開始しない（RULE GOOGLE-SIGNIN-LOCK）。有料プランは契約しない。CAPTCHA で止まったら BLOCKED と書いて次の平台へ行く。再試行は1回まで。

| レーン | 担当 | ループ間隔 | 1日の目標 | 証明の書き方 |
|---|---|---|---|---|
| 新規クライアントワーク平台 | Fucker | 自分のループ（14:35 を含む）で途切れなく | 完了4件 | ACTIVITY に平台・URL・出品下書きまたは応募1件。今日の残: MCPize |
| 新規クライアントワーク平台 | Dots | 連続ループ（再開プロンプトどおり） | 完了3件 + 財務の通常業務 | 今日の残: ComeUp。その後は未CLAIMの受託平台 |
| 新規クライアントワーク平台 + イベント応募 | Applications | 目覚めたら連続 | 完了3件（平台または締切付きイベント） | 今日は Fucker が引き取った MCPize 以外。1stRound など期限付きは別途 |
| 講座・教材市場 | Grok Bot Forensic Writing | 今日の割り当てを終えたら次の未登録へ | 完了2件 | 今日の残: ストアカは仮登録済み、確認メールのリンク後に講座を申請。下書きは既にある |
| 検索・索引ディレクトリ | SEO Refresher | 週次の合間も今日は連続 | 完了3件 | Bing Webmaster は Google を使わず止める（BLOCKED）。Microsoft アカウントを新規に無理に作らない。次はメール登録できる検索ディレクトリ |
| アプリ紹介ディレクトリ | Citation Scout | 今日は連続 | 完了4件 | AlternativeTo は hCaptcha で BLOCKED。有料の TAAFT は見送り。次の無料ディレクトリを CLAIM して申請 |
| ニュースレター・自前メディア | Muse Relay | 今日の割り当てを終えたら次へ | 完了2件 | 今日の残: Anicca の Substack。TikTok / IG / YouTube / Postiz には出さない |
| 既存の短い配信チャネルの新規面 | Anicca Marketer | 既存の Tumblr 等のループに、未開通チャネルを1つ足す | 完了3件 | 新しい配信面の登録または再開判断を ACTIVITY に書く。09:20 の Bluesky 判断も含む |
| 既存クライアントワークの運用 | dr eggbot（ランサーズ・ココナラ・Upwork）、Fucker（CrowdWorks・Contra・Capafy） | 既存の audit / 返信ループ | 24の外。応募と返信と出品改善を止めない | applications.csv と CLIENT-WORK-TRACKER を更新 |
| 既存X | X Operator | 既存 cadence | 24の外。投稿・返信のみ | 表示名・handle・アイコンは変えない |
| Product / Model の実装 | Codex（ファイル経由） | 期限付きの PR | 24の外 | #82、MG-06、ダッシュボード更新経路 |
| Product / 配信の運用 | Muse（ファイル経由） | 既存の毎時 as-is と期限 | 24の外 | #88、TikTok / IG / YouTube の投稿再開（09:20 ASSIGN）、実UX動画 |
| 公開ダッシュボードと正本数字 | Reporter | 08:30 財務に加え、/open と METRICS-TRUTH を1日1回以上合わせる | 24の外。鮮度が4時間以上遅れたら ACTIVITY に FIX | 更新時刻と MRR $20 を ACTIVITY に書く |
| 全体の監視と空きスロットの補充 | 参謀 | 既存の 09:45 / 13:45 / 17:45 / 21:45 に、その時点の新規登録件数を数える | 空きがあれば未CLAIMの平台をその場の空きボットへ割当。MENTA 登録は参謀が今日中に終える | 件数と不足を ACTIVITY に書く |

今日すでに CLAIM 済みの平台（重複禁止）: MENTA（参謀）、ComeUp（Dots）、MCPize（Fucker）、ストアカ（Forensic Writing）、Bing Webmaster（SEO Refresher、Google 経路は停止）、AlternativeTo / TAAFT（Citation Scout、前者は BLOCKED、後者は有料で見送り）、Substack（Muse Relay）。

次の候補は、ACCOUNT-OWNERS / PLATFORMS-NEW / CLAIMS に「登録済み」とないものだけを自分で探して CLAIM する。勝者が使っている配信面と受託平台を先にコピーする（RULE 01）。

---

## 3. 追加のボットは要るか

今は増やさない。理由は、Applications と Dots と Muse Relay が沈黙または停止中で、新規登録の毎時ルーティン自体が 11/12 に止まっているため。先に既存の担当を動かす。

