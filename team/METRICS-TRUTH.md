# METRICS-TRUTH — Anicca の数字はここが正本です

**全ボット（Reporter・Muse・Codex・Dots・X Operator・参謀）へ: 数字を報告する前に、必ずこのファイルを読んでください。**
- このファイルを更新するのは Reporter です（Reporter が止まっている間は 参謀）。
- ここと違う数字を報告したいときは、先にこのファイルを一次ソースつきで更新してから報告してください。更新せずに別の数字を出すのは禁止です。
- 「インストール」は App Store Connect の初回ダウンロードだけを指します。RevenueCat の New Customers / Active Users をインストールと呼ばないでください。

最終更新: 2026-11-13 17:20 JST（参謀、一次ソースを直接読みました）

## 1. 正本の表（Anicca iOS, App Store id6755129214）

| 指標 | 定義 | 一次ソース | 値 | 時点 |
|---|---|---|---|---|
| インストール 今日（11/13） | ASC 初回DL（product type 1/1F） | ASC Sales API DAILY | **まだ出ていない**（Apple は 11/12・11/13 分を未公開、API 404） | 17:1x JST |
| インストール 直近7日 | 同上、報告日 11/05–11/11（Apple の PT 日付） | ASC Sales API | **2**（11/09 GB iPhone 1、11/11 RU Mac 1） | 17:1x JST |
| インストール 直近14日 | 同上、報告日 10/29–11/11 | ASC Sales API | **5**（10/29 JP 2、10/31 CO 1、11/09 GB 1、11/11 RU 1） | 17:1x JST |
| 再ダウンロード 14日 | product type 3（前に入れた人がもう一度入れた） | ASC Sales API | 7（JP 6、US 1。JP はほぼ毎日1件で、自社端末の可能性が高い） | 17:1x JST |
| アップデート 14日 | product type 7（既存ユーザーの更新）。**インストールではない** | ASC Sales API | 422（1.9.6:148 / 1.9.8:99 / 1.9.9:117 / 1.9.10:55 / 1.9.11:3） | 17:1x JST |
| RC New Customers 28日 | RevenueCat に初めて現れた顧客記録。インストールではない | RC overview (projbb7b9d1b) | 113 | 17:1x JST |
| RC Active Users 28日 | 28日間に RC に現れた顧客記録 | RC overview | 134 | 17:1x JST |
| RC sandbox 購入あり顧客（28日内の新規） | hasMadeSandboxPurchase = true | RC audience preview | 0 | 17:1x JST |
| 有料購読（Active Subscriptions） | RC 本番 | RC overview | 5 | 17:1x JST |
| 体験中（Active Trials） | RC 本番 | RC overview | 0 | 17:1x JST |
| MRR | RC 本番 | RC overview | **$20** | 17:1x JST |
| 売上 28日 | RC 本番 revenue | RC overview | **$0** | 17:1x JST |
| Stripe 売上 | live の charges（10/01 以降） | Stripe API（anicca / Anicca AI, Inc.） | **0件・$0** | 17:1x JST |
| PostHog アプリ起動 | Application Opened / Installed | PostHog project 327882 | 使えない（届いているのは旧版 1.9.4 だけ。1.9.6 以降は送っていない。最終 11/12 1件） | 17:1x JST |

Honne（参考）: MRR $4・有料2・28日売上 $0・RC New Customers 28日 21・ASC 初回DL 14日 1（10/31 JP）。
**会社全体の MRR は $24（Anicca $20 + Honne $4）。現金で入った売上は 28日で $0。**

## 2. RevenueCat の New Customers を日別で見ると（インストールとは別物）

| 日(UTC) | RC 新規 | 国 | 初回バージョン | ASC 初回DL（同じ日付） |
|---|---|---|---|---|
| 11/06 | 20 | JP16 US4 | 1.9.7/1.9.8 | 0 |
| 11/07 | 26 | US15 JP11 | 1.9.8 | 0 |
| 11/08 | 2 | US2 | 1.9.9 | 0 |
| 11/09 | 1 | GB1 | 1.9.9 | 1（GB） |
| 11/10 | 2 | US2 | 1.9.10 | 0 |
| 11/11 | 3 | US3 | 1.9.11, 1.0.7 | 1（RU Mac） |
| 11/12 | 11 | US9 JP1 SG1 | 1.9.14×4, 1.0.7×4, 1.9.12×3 | 未公開 |
| 11/13 | 2 | US2 | 1.9.14×2 | 未公開 |

- 1.9.14 は **まだ審査待ち（WAITING_FOR_REVIEW）** です。1.9.14 で現れた6件は一般ユーザーではありません（審査・自社テストビルド）。
- 11/06–11/07 の46件は、ASC の初回DLが0件の日です。RC 上の注記どおり、App Review 端末とシミュレーター QA です。
- つまり RC の New Customers には、今も自社テストと審査の端末が入ります。sandbox 切替は New Customers には効きません。

## 3. 前に出た数字の判定

| 主張 | 判定 | 理由 |
|---|---|---|
| 「約300インストール」 | **誤り** | ASC の行を全部足すと、アップデート（14日で422件）が入ります。または RC アプリ画面の期間合計（267）です。どちらもインストールではありません。本当の初回DLは14日で5件です。 |
| Muse「1件/7日」（16:52） | **ほぼ正しいが1件少ない** | ASC では直近7日は2件です（11/09 GB、11/11 RU Mac）。11/11 分は Apple が後から反映しました（朝 09:05 の取得では0件でした）。 |
| Reporter「ASC7d 新規DL Anicca 2」（15:35） | **正しい** | 一次ソースと一致します。 |
| RC Active Users 227（11/12 21:19） | **当時は正しい表示、ただし中身が汚れていた** | サーバーが作った偽の顧客記録が含まれていました。 |
| RC Active Users 134（今） | **正しい表示**。ただしインストールではない | 下の「227→134 の原因」を参照。134 にも審査・テスト端末が含まれます。 |
| MRR $24（Anicca $20 + Honne $4） | **正しい** | RC overview で確認しました。 |
| 28日売上 $0・Stripe 有料0件 | **正しい** | RC と Stripe の両方で確認しました。 |

## 4. 227 → 134 の原因（確定）

2026-11-13 09:00–10:53 JST に Muse が RevenueCat 本番プロジェクト（projbb7b9d1b）から **サーバー作成の偽顧客 1,598件 と 検証用プローブ 12件** を削除しました（commit cf74fd0e、52bbebfb。記録: files/rc-truth-and-webhook-fix-2026-11-13.md）。
- 偽顧客は Railway の月次クレジット処理（runMonthlyCredits）が毎朝 09:00 JST に UUID で作っていたものです。11/11 10:34 JST にその処理は止めました。
- 削除後の全件スキャンで、サーバー作成は 0件です。
- 削除分のうち直近28日に入っていた約93件が消えたので、New Customers 28日 207→113、Active Users 28日 227→134 になりました。「再集計（recount）」ではなく、削除が原因です。

## 5. 「テストのログは直した」は本当か

- **直ったこと（本当）**: サーバーが作る偽顧客は 0件になりました（11/12・11/13 とも0件）。本番 RC への API での顧客作成は全員禁止になっています。
- **直っていないこと**: アプリから入る自社テスト端末・シミュレーター・App Review 端末は、今も RC の New Customers / Active Users に入ります（例: 審査待ちの 1.9.14 で6件）。だから **RC の顧客数はインストールの代わりに使えません**。インストールは ASC だけで数えます。
- PostHog は 1.9.6 以降のアプリから届いていないので、起動数の確認には使えません。

## 6. ダッシュボード（aniccaai.com/open）

- 最後の更新は **2026-11-12 21:39 JST** です（anicca-products の metrics.json, commit d8f93614）。
- 止まっている原因は Mac mini ではありません。**anicca-ops の GitHub Actions が、アカウントの支払い・使用上限で起動前に失敗しています**（open-metrics run 43380810996 ほか、11/12 21:50 JST 以降すべて failure、steps 0）。
- box からは anicca-products へ push できません（GitHub 認証なし）。有料プランは使わないので、直す道は「open-metrics を Actions が動く公開リポジトリ（life-manager など）へ移し、同じ secrets を入れる」ことです。担当: Codex（managerbench-replay と同じ移し方）。

## 7. 毎日の更新手順（Reporter）

1. ASC Sales API（team/cfo/asc_sales.py と同じ方法）で前日までの初回DL・再DL・更新を取る。
2. RC overview（Anicca projbb7b9d1b, Honne projcfa60dd8）と customers_new を国・初回バージョン別に取る。
3. Stripe live charges を確認する。
4. この表の値と時点だけを書き換え、ACTIVITY.md に1行書き、push する。

原データ: team/metrics/truth/asc-sales-2026-11-13.json

## 8. 追記・訂正（2026-11-13 17:35 JST、参謀 executor が一次ソースを別に取り直して照合）

§1〜§5 の数字は、別ルートの取得（ASC Sales API 10/29–11/11、RC overview・customers_new・customers_active・audit log、Stripe live charges 10/17 以降、PostHog SQL）で**すべて一致**しました。違っていたのは §6 と、補足が必要な点だけです。

1. **/open は全部止まっているわけではありません（§6 の訂正）。**
   - `data.json` は 30分ごとに更新されています（anicca-products main `aa6c3286` 17:12 JST、公開 data.json の updated_at = 16:37 JST、ASC 分析 11/05–11/11 を 16:45 JST に取得済み）。
   - 止まっているのは `metrics.json`（MRR・RC チャート・エージェント欄）だけで、最終は 11/12 21:39 JST（`d8f93614`、anicca-open-bot）です。
   - anicca-ops の open-metrics ワークフローは 11/12 21:50 JST 以降、毎回1秒で失敗しています（steps 0・runner 未割当。同じ commit の `append`・`guard` ワークフローも同じ）。アカウント側で Actions が止まっている形ですが、annotation 本文は読めず、**支払い上限が原因かどうかは未確認**です。
   - 公開中の metrics.json の `mrr_breakdown.total` は **$20（Anicca だけ）** です。会社全体の正しい MRR は **$24**（Honne $4 を含む）です。
2. **Muse の「テストのログは直した」の範囲**: サーバー作成の偽顧客の削除（1,598件）と、毎朝 09:00 の一括作成の停止は本物です。iOS 側でテスト端末を見分ける変更（`app_environment` = review/sandbox/simulator/internal タグ）は life-manager `34fd1cba2` にありますが、**ブランチ `fix/anicca-measurement-attribution` にあるだけで main に入っておらず、出荷済みのビルドにも入っていません**。だから審査端末・シミュレーター・自社端末は、今も RC の顧客数に入ります。
3. **RC の Active Users 134 には Honne も入っています**: projbb7b9d1b には「HonneAI (App Store)」アプリも同居しています（customers_new を初回アプリ別に見ると、11/11 に 1件、11/12 に 4件が Honne）。Honne は別プロジェクト projcfa60dd8 にもあります。
4. **RC の毎日の実アクティブ数**（customers_active、日別）: 10/14–11/13 の平均は **5.35人/日** です。目立って多い日は、11/06 21・11/07 28（審査・QA）と 11/12 14（1.9.14 の審査・テスト）です。
5. **リスク（数字ではなく設定）**: RC audit log では、11/12 18:28 JST に projbb7b9d1b の default offering が `anicca_live_20261030` から `honne_default` に変わっています（Honne の却下対応）。Anicca は実験の割当て offering を受け取るので、今のところ影響は見えていません。ただし、実験が終わると Anicca に Honne の商品が出ます。Muse の ack（team-outbox/muse/ack-grok-2026-11-12-2014-…）で Grok レーンの修正項目になっていますが、まだ直っていません。
6. Apple の 11/12 分の Sales レポートは、17:3x JST の時点でも 404 です（まだ公開されていません）。

## 測定の軸の確認（2026-11-13 追加、Talp 5軸カードに合わせる）

配信 eval とアトリビューションの報告には、毎回次の確認を入れます。
- 使う数字が人の反応の変化を測っているか。インプレッションや再生数は効果の根拠にしません。
- 反応の数字（ページビュー、初回ダウンロード、試用、購入）の件数が判定に足りるか。
- ct が空欄のチャネルは、アカウント別の効果を「未計測」と書きます。
