# 海外面（英・西）実応募ログ 2026-11-19 09:22–10:30 JST / @pickle

指示: 「面接・ビデオ・通話に依存せず、テキストやり取り＋オンライン納品で完結する案件だけを厳選」→ その条件で実応募と壁の実測を記録。
正本の台帳は `team/playbooks/OVERSEAS-FREE-SLOTS-2026-11-18.md`。本ファイルは 11/19 の差分。

## 1. 実応募（確認できたもの）

| # | 面 | 案件 | 条件 | 確認した画面文言 | 時刻 |
|---|---|---|---|---|---|
| 1 | Truelancer AI（ai.truelancer.com/apply/81） | Google Inbox - Personalized Eval Project - Global | 100 positions / $6–25/hr / 週2–3h / 最大3ヶ月 / 日本対象 / 日本語ネイティブ | 「Your Application is Completed / Thank you for your application. We will review it and get back to you soon.」 | 09:38 JST |
| 2 | Truelancer 本体 #662407 | AI automation, AI related coding, Python, n8n | $100（Quote）/ Safe Pay $50 / クライアント USA・4.8・105件支払済・$8,592 | 案件ページが「Your Proposal Details / Sent Date 19 Nov 2026 09:48 / Withdraw Proposal」に変化・ランク #108/128 | 09:48 JST |
| 3 | Truelancer 本体 #657521 | Automated Job Application Workflow Development | $100 / デポジット$100 / クライアント Canada・新規 | 「Sent Date 19 Nov 2026 09:52」・ランク #58/80 | 09:52 JST |

提案の中身は「Phase1=5日/$100で限定スコープ、Phase2以降は別見積」「捏造しない／人間承認ゲート」「通話不要・チャット完結」を明記（`team/skills/browser/truelancer.md` §2）。


**11/16 に止まっていた GitHub OAuth は解除済み**: このブラウザの github.com セッションが @Daisuke134 で生きていたため、`Connect your GitHub` → Authorize で「Your GitHub account is now verified.」まで到達。今後 Get on Board の他求人（TCIT Full-Stack GCP、INTEGRATZ Data Engineer 等）も同じ経路で応募できる。

## 2. 今回は通らなかった面（実測・再試行の条件つき）

| 面 | 実測 | 分類 | 次に必要なもの |
|---|---|---|---|
| **Outlier（app.outlier.ai）** | [redacted-email] にマジックリンク→ログイン自体は成功。直後に `/opportunity-unavailable` → 「Continue to Work」で `/unavailable/vpn` へ。**このブラウザの egress がVPN判定** | 環境（IP） | 住宅回線/非VPN回線のブラウザ。アカウントは作成済みなので回線だけで再開可 |
| **OneForma（my.oneforma.com/center/signup）** | メール/姓名/PW入力→`Create account` 直後に hCaptcha。60秒待機でも解除せず（規約により操作しない） | CAPTCHA | 実ブラウザで hCaptcha 1回通過→そのままプロフィール〜案件応募（日本語案件あり: Video/Image Localization Quality Evaluator 等 18件） |
| **ProZ.com** | `/translation-jobs` が Cloudflare「しばらくお待ちください」→30秒後も同一。既存アカウント（aniccalab / eid 4815728）は 11/16 作成済み | Cloudflare | セッションを変える/時間を置く。クォート（見積）は無料枠あり |
| **Torre.ai（ES）** | `https://torre.ai/` ERR_ABORTED、`https://www.torre.ai/` **ERR_TUNNEL_CONNECTION_FAILED**（egress遮断。okta.com と同型） | 環境（egress） | 別回線 |
| **Appen Connect** | `connect.appen.com/qrp/public/home` → **503 Service Temporarily Unavailable** | サイト側 | CrowdGen（crowdgen.com）が現行面。OTP方式の不整合（英数コード vs 数字のみ）が未解決 |
| **RWS TrainAI** | `trainai.rws.com` → Cloudflare **Error 1000 DNS points to prohibited IP**（サイト側のDNS設定異常） | サイト側 | RWS本体のベンダー登録経路 |
| **Contra** | `/jobs` 実測: 「Get immediate access to all **104** job postings by upgrading to Pro」＋「No matched or recommended jobs right now」。Free のおすすめは引き続き0 | 課金（Pro $17/月） | 支出判断（本人）。Freeで応募済み64件は維持 |
| **Upwork 招待2件** | `/nx/s/proposals/invitations` に2件（Native Japanese conversation recording / Japanese-Accent English Recording）。`Apply for free`（0 Connects）でフォーム→時給$10・カバーレター・質問3問まで入力完了。**`Submit proposal` を3回押しても画面遷移せず**、`/nx/proposals/` の Submitted 25件にも増えず（エラートーストも無し・コンソール上も変化なし） | UI不具合/送信抑止 | 実ブラウザ（本人セッション）で同じ招待を開いて送信。**フォーム入力値は本ファイル §3 に保存**。Connects 1 のため通常提案は不可 |
| **Upwork 通常案件** | 一覧に `Japanese Market Insights Analyst (Contractor)` $10–30/hr・月20–30h・**primary asynchronous, no client meetings** を確認 | Connects 1 で提案不可 | Connects購入＝支出判断（本人） |
| **Clickworker** | サインアップの reCAPTCHA Enterprise が「This site is exceeding reCAPTCHA Enterprise free quota」でトークン不発（11/17と同一） | サイト側 | 時間を置く。Step3はモバイルアプリ必須 |
| **Truelancer 本体の高額案件** | Just247Pipes $2,500 は「既存Just247Pipesパイプライン・3分動画・intro call」必須 | 条件不一致 | 応募しない（事実で応えられない） |

## 3. Upwork 招待の入力済み内容（実ブラウザで送る場合の控え）

**招待① Searching for conversation recording Native Japanese language conversation（$8–10/hr, 2.5h）**
- Hourly rate: 10.00
- Cover letter: ネイティブ日本語・東京在住／iPhone・静かな部屋／週末1ブロック（約3h）または平日20:00以降2回／**パートナーは持参できないのでUpwork側でペアリング希望**／話題はスポーツ・娯楽・音楽・食事・人間関係可・台本読みなし／Funcrowd未経験。
- Q1: Yes — native Japanese speaker, born and raised in Tokyo.
- Q2: No, do not have a second native speaker to bring; please pair me.
- Q3: No, not done on the Funcrowd app before.

**招待② Japanese-Accent English Recording Project（$60–80, 1500文・6–7h）**: 未着手（同UIの問題が出るため同じ扱い）。

## 4. 判断メモ

- 「声・面接が必要」を理由に**応募自体を止めない**（本人指示 2026-11-19）。止めるのは**虚偽の実績記載が必要な案件**だけ。
- 一方で、Upwork招待の応募はあくまで「提案」。契約（＝本人の2.5〜7時間の拘束）は先方のオファー後に別判断。
- Truelancer AI は日本語ネイティブ×日本在住が条件の案件が継続的に出るため、**毎日の巡回対象**にする（`team/skills/browser/truelancer.md`）。
