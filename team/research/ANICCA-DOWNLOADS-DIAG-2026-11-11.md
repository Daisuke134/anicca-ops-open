
作成: Grok Bot executor。数値は捏造していない。取れない指標は「取得できず」と書いた。

対象期間（Appleの最新確定日は **2026-11-09**。Sales も Analytics も 11/10・11/11 は未公開）:
- 7日: 2026-11-03〜11-09
- 30日: 2026-10-11〜11-09

ソース: `bash /workspace/team/scripts/ascx.sh`（ASC Analytics Reports ONGOING `04c74879-547f-4e35-b231-1fafd485801d` と Sales Summary）。各日は、その Date の最新 processingDate（11/09 分は processing 2026-11-10）の行だけを合計した。RevenueCat プロジェクト `projbb7b9d1b`（anicca）。PostHog 接続先プロジェクト 327882。X 公開API。

既存計画との関係（重複作業を避ける）:
- `team/research/INSTALLS-FUNNEL-AND-1K-PLAN-2026-11-11.md`（11:00 JST）の7日ファネル（当時 11/04–11/09 または 11/03–11/09 で 283〜302 impressions）と一致。本ファイルは 30日・ソース・地域・Sales突合・RevenueCat・チャネル・ct= を足した更新。
- `team/research/ASO-PROPOSAL-ANICCA-2026-11-10.md` のキーワード案は **1.9.11 として既に審査提出済み**。再提出しない。
- `team/research/ANICCA-PPO-IAM-V2-TEST-2026-11-11.md`: PPO `d7ffa0d7` は審査中。v2 は作らない（他実験が審査中のため）。

## 1. 結論

**主因は「見つけられていない」（impressions が少ない）こと。** ついで、米国の検索では見られてもページを開かれない。ソーシャルとWebはインストールにほとんど乗っていない。

7日のファネル（Analytics Counts）:

| 段階 | 件数 | 前段からの転換 |
|---|---:|---:|
| Impressions | 302（約43/日） | — |
| Product page views | 15 | 5.0% |
| First-time downloads（Sales typ 1 と一致） | 1 | ページ→DL 6.7%、imp→DL 0.33% |
| 新規トライアル（RevenueCat） | 0 | — |
| 新規有料・期間売上（RevenueCat / Sales IAP） | 0 / proceeds $0 | — |

30日: **1,132 impressions → 95 page views（8.4%）→ 16 first-time DL**（ページ→DL 16.8%、imp→DL 1.41%）。Sales typ 1 も **16**。トライアル 0、売上 $0。

1,000 DL/日を今の 30日 imp→DL 1.41% で出すには、約 7.1 万 impressions/日が必要。今は約 38/日。ページ転換を上げても、今の規模では桁が足りない。

## 2. ファネル実数

### 2.1 ソース別（Analytics Standard）

7日（2026-11-03〜11-09）:

| Source Type | Impressions | Page views | First-time DL | Redownload |
|---|---:|---:|---:|---:|
| App Store search | 294 | 8 | 1 | 3 |
| App Store browse | 8 | 1 | 0 | 0 |
| App referrer | 0 | 5 | 0 | 0 |
| Web referrer | 0 | 1 | 0 | 0 |
| Unavailable | — | — | 0 | 1 |

30日（2026-10-11〜11-09）:

| Source Type | Impressions | Page views | First-time DL | Redownload |
|---|---:|---:|---:|---:|
| App Store search | 1,107 | 50 | 10 | 4 |
| App Store browse | 25 | 15 | 0 | 0 |
| App referrer | 0 | 21 | 6 | 0 |
| Web referrer | 0 | 9 | 0 | 0 |
| Unavailable | — | — | 0 | 1 |

- **インストールを出しているのは検索（30日 10件）と App referrer（6件）だけ。** Browse と Web referrer の first-time は 0。
- 検索のページ転換は低い（30日 1,107→50 = 4.5%）。Browse は imp が少ないがページ転換は高い（25→15）。
- App referrer の 6 first-time は、Detailed レポートの対象行に入っておらず、参照元アプリ名は **この30日分では取得できず**。過去（2026-01〜02、Detailed に残っている行）では `com.ss.iphone.ugc.Ame`（Douyin）と `com.ss.iphone.ugc.tiktok.lite` から日本向け first-time が出ていた。それを現在の6件の内訳とはみなさない。

### 2.2 地域別（Analytics）

7日 impressions 上位と first-time（Sales typ 1。7日の first-time は GB の1件のみ）:

| Territory | Imp | Page views | 7日 first-time | 30日 first-time（Sales） |
|---|---:|---:|---:|---:|
| US | 106 | 5 | 0 | 4 |
| JP | 37 | 6 | 0 | 7 |
| IN | 31 | 0 | 0 | 2 |
| KR | 26 | 0 | 0 | 1 |
| BR | 25 | 0 | 0 | 0 |
| GB | 18 | 1 | 1 | 1 |

30日の転換差:

- **JP: 186 imp → 64 page views（34.4%）→ first-time 7**
- **US: 293 imp → 13 page views（4.4%）→ first-time 4**
- **KR: 323 imp → 0 page views**（30日 impressions の 28.5% がページ未到達。検索に出ているが開かれていない）

米国は「見られても開かれない」。日本は開かれるが、絶対量が少ない。

### 2.3 日次 first-time（Sales typ 1 = アプリ新規。Analytics と合計は一致）

7日: 11/03 0、11/04 0、11/05 0、11/06 0、11/07 0、11/08 0、11/09 1（GB）。再DL typ 3 は 6、更新 typ 7 は 304（1.9.8/1.9.9 の自動更新で、新規獲得ではない）。

30日 typ 1 の内訳: JP 7、US 4、IN 2、KR 1、CO 1、GB 1。再DL typ 3 は 8。更新 typ 7 は 305。

10/12 の Sales ファイルは Apple が `available=false`（0件扱い）。Analytics の 10/12 も first-time 行なし。

### 2.4 キャンペーン（ct=）

Discovery Detailed と Downloads Detailed には `Campaign` 列がある。取得できた行では **すべて空**。ただし Detailed の網羅は Standard より狭い（30日の検索 impressions、Detailed は 305 / Standard 1,107）。よって「ct= 経由のインストールが1件も無い」と断定はできない。言えるのは、**取得できた Detailed 行にも、Standard の Web referrer first-time にも、ct= 付きの成果は1件も出ていない**こと。

## 3. 公開中のストア掲載と審査

公開中（iTunes lookup および App Info、2026-11-11 21:4x JST）: **1.9.10**。リリース `2026-11-11T01:03:08Z` = **2026-11-11 10:03 JST**。

| locale | 名前 | サブタイトル | キーワード | スクリーンショット |
|---|---|---|---|---|
| en-US | Daily Affirmations - Anicca | Lock Screen Widget & Self-Talk | manifest,manifestation,self love,mantra,positive,confidence,gratitude,anxiety,calm,mindfulness | iPhone 6.7" 8枚 COMPLETE（1.9.11 も同一ファイル） |
| ja | 毎日のアファメーション - アニッチャ | 自己肯定感・名言・瞑想・感謝・ポジティブ | アファメーション,引き寄せ,自己肯定感,セルフケア,自己愛,マインドフルネス,不安,瞑想,癒し,眠り | iPhone 6.7" 8枚 COMPLETE |

プロモテキストは日米とも入っている（審査不要欄。11/10 に適用済み）。評価: **US 1件（平均5）、JP 48件（平均4.52）**。

**1.9.11 は審査中（WAITING_FOR_REVIEW）。** version id `26cbce6a-1451-4c09-9402-3dcd24f89636`。提出 `2026-11-11T04:37:25.082Z` = **2026-11-11 13:37 JST**（submission `7935cb9a-6b23-4645-8e2e-169f8cd518d4`）。ビルド 1.9.11 (824) は VALID。**二重提出しない。**

1.9.11 の変更（審査中の App Info / localization）:
- en-US サブタイトルは提案文の "Self Love & Positive Mantras" ではなく、**"Positive widgets & motivation"**。
- en-US キーワード: `manifest,confidence,gratitude,anxiety,calm,mindfulness,lockscreen,mantra,quotes,selfcare,reminders`。
- ja キーワードは提案どおり重複を外したもの。ja サブタイトルは公開中と同じ。

**PPO `d7ffa0d7-704c-42ef-abf8-588f3bada53e`（Lock Screen first screenshot Nov 2026）は WAITING_FOR_REVIEW、traffic 50%、未開始。** 承認後に `start-d7` が必要（開始しなければ実験は走らない）。v2 は「他実験が審査中」で今は作れない。計画どおり d7 を閉じてから（遅くとも 11/27 JST）。

## 4. RevenueCat（projbb7b9d1b、通貨 USD）

概要（ダッシュボード「Last 28 days」および stock）:
- Active trials: **0**
- Active subscriptions: **5**
- MRR: **$20**（概要の表示は $20。以前の /open は $20.34）
- Revenue（28日）: **$0**
- New customers（28日）: 192 ← **インストールではない**（サーバ作成・審査・シミュレータを含む。RC チャート注記および既存の測定ルールどおり）
- Active users（28日）: 211

日次チャート（resolution=day、2026-10-12〜11-11）: **Revenue 合計 $0、Transactions 0、New Trials 合計 0**。有料新規（actives_new）も概要と整合して 0。Sales に Anicca の IAP/購読行は 10/01〜11/09 で 0、proceeds $0。

つまりダウンロード後の課金ファネルも、今は新規トライアルすらない。ただし 7日の first-time は1件なので、課金側の主因は「入っていない」こと。

## 5. チャネル別（インストール/売上に効いているか）

| チャネル | 到達・クリック | ASC への着地 | 30日 first-time | 売上 | 判断 |
|---|---|---|---:|---:|---|
| App Store 検索 | 1,107 imp / 50 pv | 測定済み | 10 | $0 | **唯一の定常獲得。** ただし US は開かれない。止める対象ではない |
| App referrer | 21 pv、ソース名は30日分取得できず | 測定済み | 6 | $0 | 残す。中身の特定は Detailed 不足 |
| App Store browse | 25 imp / 15 pv | 測定済み | 0 | $0 | 量は小さい。止めなくてよい |
| Web referrer（サイト等） | 9 page views | 測定済み | **0** | $0 | サイト経由は今インストールになっていない |
| @selawmqt（X、フォロワー13） | 直近25投稿の主題は Hook Lab / Capafy / ショート動画ツール。Anicca の App Store リンクなし。最高 impressions 258（11/02 の接続投稿）。他はおおむね 0〜88 | なし | 0（Anicca 言及なし） | $0 | **Anicca の獲得チャネルになっていない**（別プロダクトの発信） |
| Instagram / Mastodon / YouTube / Bluesky / Tumblr の bio リダイレクト | PostHog `app_store_click`（source=web_redirect）: 2026-10-11〜11-11 に **139**（うち 11/01 だけで 127）。内訳例: mastodon_aniccaapp_bio 41、mastodon_anicca_affirm_bio 24、instagram_ani.cca1234_bio 15、instagram_anicca.en_bio 13 など。tiktok_*_bio は 1+1。`app_store_click_nonhuman` は別途 194 | ASC Web referrer pv は30日で9、first-time 0。Detailed の Campaign は空 | **0** | $0 | クリックは記録されているがストアの新規DLになっていない。サイト/リダイレクトが ct= を落としている可能性が高い。11/01 の127は異常値の可能性あり |
| TikTok / IG / Threads の投稿本体 | この Postiz アカウント（アカウント3）の 2026-10-12〜11-12 投稿リストは **0件**。投稿インプの最新値は **取得できず** | 30日の Web/キャンペーン first-time 0 | 確認できる範囲で 0 | $0 | 投稿経由の成果は見えない。bio クリックもDLになっていない |
| aniccaai.com SEO | 接続中の PostHog プロジェクトに `$pageview` が無い。Web overview の「30日 visitors 36 / views 212、7日 0」はサイト計測として使えない | Web referrer 30日 pv 9、first-time 0 | 0 | $0 | **サイトのオーガニック訪問数は、この PostHog では取得できず。** ASC 上のWeb経由DLは0 |

Tumblr 今日の配信（`marketing/anicca/2026-11-11-distribution-pass.md`）は `aniccaai.com/affirmation-app?...&ct=tumblr_dailyanicca_20261111` で出している。これもサイトが ct= を落とす経路。

## 6. ソーシャルがDLにならない理由（データで言える範囲）

1. **App Store リンクが無い。** @diceai0 の直近投稿はアプリに触れていてもリンクがない。計測も流入も起きない。
2. **サイトを経由すると ct= が落ちる。** ランディングの App Store ボタンは固定の `ct=`（例: affirmation-app ページは素の `https://apps.apple.com/app/id6755129214`、SEO ページは `seo_en_*` / `seo_geo_*`）で、クエリの `ct=x-diceai0-*` や `ct=tumblr_*` を転送しない（`marketing/X-APPSTORE-CT-GAPS-2026-11-11.md` および `apps/landing` の実装）。
3. **リーチが小さい。** 今日の @diceai0 返信は impressions が一桁〜20台。@selawmqt は Anicca を売っていない。
4. 過去（2026年1–2月）の TikTok/Douyin アプリ経由は日本で first-time を出していたが、**今の30日 Detailed では同じ参照元の first-time 行が無い。**

## 7. ROI順の無料施策3つ（既存オーナーを崩さない）

1. **すべての Anicca 言及に、直の App Store リンク（ct=付き）を付ける。** 担当: **X Operator**（投稿・返信）。形式: `https://apps.apple.com/app/id6755129214?pt=93486075&ct=x-diceai0-<slug>&mt=8`。サイトリンクだけにしない。効果測定: 48時間後に ASC Campaign で `x-diceai0` の units > 0。  

2. **aniccaai.com の App Store ボタンが、流入クエリの `ct=` をそのまま付ける。** 担当: **参謀 / Codex**（コード変更。既存オーナー）。直リンクに変えても、Tumblr・IG bio・既存キューはまだサイトを踏む。ここを直さないと bio の 139 クリックが ASC で見えない状態が続く。1.9.11 や PPO には触らない。

3. **1.9.11 の審査を待ち、承認後に米国検索を7日測る。PPO d7 は承認当日に start する。** 担当: **Codex**（1.9.11 は提出済み、再提出しない）+ **Anicca Marketer**（測定と `start-d7`）。米国は 293 imp → 13 pv。キーワードとサブタイトルの変更はすでに 1.9.11 に入っている。スクリーンショット実験は検索結果の見た目用。短尺動画＋ストアCTA（担当 **Muse**、既存の 1k/day 計画の1番）は、過去に App referrer で日本DLが出た経路なので、リンク付きで続ける。新しい実験や二重提出はしない。

止めるべきなのは「チャネルそのもの」より、**リンク無しの Anicca 言及**と、**ct= を落とすサイト経由**。検索は止めてはいけない。@selawmqt を Anicca 獲得に使うなら、Anicca の直リンクを付けるか、役割を分ける。

## 8. 取得できなかったもの

- Analytics / Sales の 2026-11-10 と 11-11（未公開）。
- Unique impressions の合計（内訳行の Unique Counts は足せない）。
- 直近30日の App referrer 6 first-time の参照元アプリ名（Detailed 不足）。
- ASC Campaign の完全な網羅（Detailed が Standard より少ない）。
- aniccaai.com のオーガニック訪問（この PostHog に `$pageview` が無い）。
- TikTok / IG / Threads の投稿インプ（Postiz アカウント3の当該期間は投稿0件。他アカウントの数値は未取得）。
- 1.9.11 サブタイトルが提案と違う理由（事実のみ記載）。

