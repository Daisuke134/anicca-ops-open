# Anicca スクリーンショット解体と実験バックログ — 2026-11-11

Written: 2026-11-11 14:25 JST, Grok Bot 参謀.
Scope: 勝者 I am だけでなく、同カテゴリの上位アプリと公開 ASO / オンボ / ペイウォール資料を照合。en-US の PPO を優先。完了条件は `team/playbooks/AB-TEST-RULES.md` に従う。

公開ファネル（直近7日、Anicca id6755129214）: インプレッション 302、ページ閲覧 15、初回ダウンロード 1。ボトルネックは検索結果のタップ（表示されてもページを開かれない）。だから最初の実験面はスクリーンショット（とくに検索に出る先頭3枚の見出し）である。

## 1. いまの ASC 状態（14:23 JST に ascx で再確認）

ライブの PPO 実験がすでに1件ある。**複製は作っていない。審査中のため中身も差し替えていない。**

| 項目 | 値 |
|---|---|
| 実験名 | Lock Screen first screenshot Nov 2026 |
| ID | `d7ffa0d7-704c-42ef-abf8-588f3bada53e`（v2、紐付け先は公開中 1.9.10 `c66f729e-921d-48cf-bd01-ba4b359bc32e`） |
| 状態 | `WAITING_FOR_REVIEW`（編集不可） |
| トラフィック | 50% |
| トリートメント | `a5376aa3-4b0f-4af7-b1e0-479ace583533`「Lock Screen widget first」、locale は en-US のみ |
| サイズ | APP_IPHONE_67 のみ（1320×2868、8枚） |
| 中身 | 1枚目だけロック画面ウィジェット＋見出し「Affirmations on your Lock Screen, a new one every day。」。2–8枚目は公開中コントロールと同じファイル |

Anicca 1.9.11 は別件で `WAITING_FOR_REVIEW`（ビルドのペイウォール更新）。スクショの checksum は 1.9.10 と同一。公開中コントロール（en-US / ja とも IPHONE_67、8枚）を `/workspace/anicca-aso/control-live/` に保存済み。

次の PPO（見出しコピー v1）は、このロック画面実験が Winner / Loser / inconclusive で閉じた当日に提出する。資産は作成済み。ja 用も作ってあるが、最初のコピー実験は en-US だけ出す。

## 2. 公開中コントロール（Anicca）の先頭3枚

レイアウトはすでに「明るい背景 + 大きい見出し + 実機のアファメーション画面」で、カテゴリの勝ちパターンに近い。弱いのは**文言**である。全文が長く、1枚目は問題（negative thoughts loop）から入り、2–5枚目は操作説明に寄っている。

| # | en-US（公開中） | ja（公開中） |
|---|---|---|
| 1 | When negative thoughts loop, read one kinder line | 頭の中の否定的な声に、やさしい一行を |
| 2 | Swipe through daily cards | カードをスワイプして毎日読む |
| 3 | Save the words you want to reread | 心に残る言葉をお気に入りに保存 |
| 4 | Choose from 8 backgrounds | 8種類の背景から選べる |
| 5 | Copy or share a card as an image | 言葉をコピー、画像でシェア |
| 6 | Get gentle reminders | 通知でリマインダーを受け取る |
| 7 | At your own pace, one card at a time | 自分のペースで、まずは1枚から |
| 8 | Subscription required / Price shown before purchase | 継続利用は有料サブスク / 料金は購入前に表示 |

8枚目の課金表示は残す（虚偽にしないための開示）。US 評価は1件なので、社会的証明（星の数や「trusted by millions」）は使わない。

## 3. カテゴリ解体（2026-11-11、iTunes / 公開スクショ）

出典は各国 App Store の現行スクショ（iTunes lookup で取得、ファイルは `/workspace/anicca-aso/competitors/`）。Shine（旧 The Shine App）は本日の US 検索では見つからず、代替として同カテゴリの Mantra と Gratitude を見ている。

### 先頭3枚の型

| アプリ | ID / 評価（US） | 1枚目（hook） | 2枚目（educate） | 3枚目 | 色と型 |
|---|---|---|---|---|---|
| I am - Daily Affirmations | 874656917 / 4.8、約74万件 | Daily reminders to stay positive（ロック画面ウィジェット＋通知。実アファメーション「I am enough.」） | Personalized affirmations（画面いっぱいに一文） | Customizable widgets（ホーム＋Watch） | ベージュ、見出しは3–5語、実UI |
| Motivation - Daily quotes | 876080126 / 4.8、約108万件 | Get motivation throughout the day（ロック画面＋通知。I am と同じ型） | Change your thoughts, change your life（全文カード＋ストリーク） | 1000s of options to customize widgets | 黒・グレー。Monkey Taps 姉妹アプリ |
| ThinkUp | 906660772 / 4.7、約7.5千件 | Overcome Challenges with Positive Affirmations（カテゴリグリッド） | 引用（社会的証明） | Record Powerful Affirmations in your Voice | オレンジ勾配。1枚目はベネフィットだが文字が多い |
| Finch: Self-Care Pet | 1528595748 / 4.9、約77万件 | Self-care is better together | Build habits with friends by your side | 仲間との応援 | 明るい青空。巨大なベネフィット見出し、キャラが主役 |
| Calm | 571800810 / 4.8、約199万件 | The #1 App for Sleep & Meditation ＋ 3M 5-star / Award | Trusted by millions | Fall asleep to Sleep Stories | 青空。1枚目は社会的証明（評価数が本物のため） |
| Headspace | 493145008 / 4.8、約97万件 | Award Winning（賞のロゴ） | Stress less | Sleep soundly | 黄・オレンジ。2枚目以降は2語の成果 |
| Mantra | 1202851636 / 4.8、約3.4万件 | Feel better with Mantra | Get daily affirmations | Be the best version of you | 暖色。短い成果コピー |
| Gratitude | 1372575227 / 4.9、約4.5万件 | Capture Daily Gratitude Moments | Reflect And Record Your Gratitude | Guided Challenges For Everyday Growth | ピンク。タイトルケースのベネフィット |

I am / Motivation の共通型（検索で勝てる型）:

1. 先頭は「毎日、どこで目に入るか」（ロック画面・通知・ウィジェット）。短い成果コピー。
2. 2枚目は、実アファメーションが画面の主役。
3. 見出しは3–6語、コントラストが高く、サムネイルでも読める。
4. 背景は単純で明るい（または意図的に暗い）。1枚にベネフィットは1つ。
5. 4枚目以降でテーマ数・カテゴリ・ストリークなどの「量」を出す。

Anicca が今すぐ真似すべきなのは「短い成果コピー」である。1枚目をロック画面にする案は、**すでに審査中の実験**でテスト中。次はコピーだけを変える（変数を混ぜない）。

## 4. 公開ベストプラクティス（出典つき）

### スクリーンショット / ASO

- Apple: 検索結果には最大3枚（ポートレート）が出る。実在の体験を見せ、いちばん強いベネフィットを先に置く。[App Store Asset Best Practices](https://developer.apple.com/app-store/asset-best-practices/)
- AppTweak: 最初の3枚が影響のほとんど。短いベネフィットキャプション（機能名ではなく成果）。1枚1メッセージ。文字は小さい画面でも読めるサイズ。[How to optimize your app screenshots](https://www.apptweak.com/en/aso-blog/how-to-optimize-your-app-screenshots), [Design creatives… ASO best practices](https://www.apptweak.com/en/aso-blog/best-aso-practices-for-your-app-game-creatives)
- SplitMetrics: アイコンとスクショは競合分析と A/B の実データで決める。1要素ずつテストする。[Best ASO Practices](https://splitmetrics.com/blog/app-store-optimization-best-practices/)

### オンボーディング / ペイウォール

- Superwall: オンボーディングの複数ページ・ペイウォールは、単ページより転換が 37% 高い（12.41% vs 9.07%、取引ゼロを除いた集計）。価値を先に見せ、そのあと価格。[Multi-page onboarding paywalls](https://superwall.com/blog/new-postmulti-page-onboarding-paywalls-convert-37-better-than-single-page-heres-why), [Superwall Best Practices](https://superwall.com/blog/superwall-best-practices-winning-paywall-strategies-and-experiments-to)
- RevenueCat: ペイウォールはジャーニーの一部。表示のタイミングと回数を見る。ある事例では、ウェルカム直後のペイウォール（8%）より、3枚の説明のあとのペイウォール（15%）の方がトライアル開始が高い。[What the best subscription apps get right about paywalls](https://www.revenuecat.com/blog/growth/how-top-apps-approach-paywalls)
- Adapty State of Paywalls 2026: オンボーディング中のペイウォールの方が、後出しより有料化が高い（閲覧あたり 0.85% vs 0.23%）。先にオファー（地域・トライアル・期間）を試し、見た目やコピーはあと。年間プランにトライアルを付けるのが一般的。[State of Paywalls 2026](https://adapty.io/state-of-paywalls/)
- The Paywall Index: よく出る3画面は「トライアルの約束 → リマインダー → オファー」。リマインダーありの方が転換が高い、という集計。年額先行は、年額+月額の並記より強い傾向。[The Anatomy of the Best-Performing Onboarding Paywalls](https://thepaywallindex.substack.com/p/the-anatomy-of-the-best-performing)

これらは他社の集計であり、Anicca の少件数ファネルにそのまま当てはめない。仮説の順番を決める材料にする。

## 5. 次の PPO（キュー）: 見出しコピー v1（en-US）

- **仮説:** 検索のタップ率は、現行の長い問題提起コピーより、3–6語の成果コピーの方が高い。レイアウト・実画面・順番は変えず、見出しだけを変える。
- **コントロール:** 公開中の現行8枚（上記）。
- **トリートメント:** 同じ実画面・同じ青背景・同じ端末フレーム。見出しだけ差し替え。

| # | コントロール | トリートメント |
|---|---|---|
| 1 | When negative thoughts loop, read one kinder line | A kind line every morning |
| 2 | Swipe through daily cards | Swipe a new affirmation |
| 3 | Save the words you want to reread | Save the lines you love |
| 4 | Choose from 8 backgrounds | A background that calms you |
| 5 | Copy or share a card as an image | Share a line with someone |
| 6 | Get gentle reminders | Gentle reminders all day |
| 7 | At your own pace, one card at a time | One card, at your pace |
| 8 | Subscription required / Price shown before purchase | Subscription required. Price shown before purchase |

- **市場:** en-US（検索タップが細い市場）。ja セットも資産としては作成済みだが、この実験には載せない。
- **サイズ:** 1320×2868。現行どおり APP_IPHONE_67 で出す。同じファイルは APP_IPHONE_69 としてもバリデーション済み（`asc screenshots validate`、error 0）。
- **トラフィック:** 50%。指標は PPO のコンバージョン（ページ閲覧 → 初回ダウンロード）。
- **完了条件:** `team/playbooks/AB-TEST-RULES.md`（最低7日、90% で勝ち/負け、14日または上限で inconclusive、当日に次を出す）。
- **資産パス（box）:**
  - en-US IPHONE_67: `/workspace/anicca-aso/treatment-iam-copy-v1/en-US/APP_IPHONE_67/01_enUS.png` … `08_enUS.png`
  - en-US IPHONE_69: `/workspace/anicca-aso/treatment-iam-copy-v1/en-US/APP_IPHONE_69/`
  - ja（次々回用）: `/workspace/anicca-aso/treatment-iam-copy-v1/ja/APP_IPHONE_67/` と `APP_IPHONE_69/`
  - コントロール: `/workspace/anicca-aso/control-live/en-US/APP_IPHONE_67/`
  - 審査中トリートメント1枚目: `/workspace/anicca-aso/treatment-lockscreen/en-US/01_lockscreen.png`
- 画面は公開中スクショの実UIを切り出して使っている。未実装の機能は描いていない。

提出コマンド（ロック画面実験が閉じたあと、参謀が実行。今は実行しない）:

```
bash /workspace/team/scripts/ascx.sh product-pages experiments create --v2 --app 6755129214 --platform IOS --name "Headline copy v1 short benefit en-US" --traffic-proportion 50
# treatments create → localizations create --locale en-US → screenshot-sets upload --device-type IPHONE_67 --path /workspace/anicca-aso/treatment-iam-copy-v1/en-US/APP_IPHONE_67
# 提出前に experiments view で状態を確認し、レビューへ出す
```

## 6. 実験バックログ（優先順。常に次をキューする）

完了条件は、特記がない限り `AB-TEST-RULES.md` と同じ（7日 / 90% / 14日）。

### スクリーンショット（PPO、1件ずつ）

| 順 | 実験 | 仮説 | 指標 | 状態 |
|---|---|---|---|---|
| 0 | 1枚目をロック画面ウィジェットに | 検索では「毎日ロック画面で目に入る」が、アプリ内カードよりタップされる | PPO CVR | **ライブ:** `WAITING_FOR_REVIEW` `d7ffa0d7-…` |
| 1 | 見出しコピー v1（短い成果、en-US） | 長い問題提起より、3–6語の成果コピーの方がタップされる。レイアウトは固定 | PPO CVR | **キュー済み、資産あり。** #0 の翌日に提出 |
| 2 | 見出しコピー v2（キーワード先行） | 「Daily affirmations every morning」のように検索語を先頭に置く方が、v1 より CVR が上がる | PPO CVR | キュー（v1 の次） |
| 3 | 見出しコピー v3（短い問題解決） | 「Quiet the loop. One kind line.」のように問題→解消を短く置く | PPO CVR | キュー |
| 4 | ロック画面 × 勝ちコピー | #0 が勝ち、かつコピーの勝ち文言が決まったら、1枚目だけ結合する（変数は結合後の1セット） | PPO CVR | #0 とコピー系のあと |
| 5 | より大きなレイアウト変更 | コピーが inconclusive なら、I am 型（明るい単色、さらに大きい見出し、端末枠を寄せる）へ変える | PPO CVR | コピーが inconclusive のとき前倒し |
| 6 | ja に勝ちセットを適用して PPO | en-US の勝ちは、ja でも同じ方向に効く | PPO CVR（jp） | en-US の勝ち確定後 |

### オンボーディング（アプリ内。PPO とは別面、同時に1つ）

| 順 | 実験 | 仮説 | 指標 |
|---|---|---|---|
| A | ペイウォールの前に価値を2–3画面置く | Superwall / RevenueCat の型どおり、先に「何が届くか」を見せるとトライアル開始が上がる | インストール → トライアル開始（有料化も併記） |
| B | 最初のアファメーション（aha）の直後にペイウォール | 価値を1枚体験してからの方が、オンボ完了直後より転換する | 同上 |
| C | パーソナライズ質問の長さ | 質問を短くした方が完了率は上がるが、その後の有料化は下がらない | オンボ完了とトライアル開始 |

### ペイウォール（アプリ内。同時に1つ）

| 順 | 実験 | 仮説 | 指標 |
|---|---|---|---|
| P1 | 年額先行 + 7日トライアルを主ボタンに（「Start my 7-day free trial」） | 年額にトライアルを載せ、CTA に日数を書く方が、月額並記より有料化と LTV が良い | ペイウォール閲覧 → トライアル、およびトライアル → 有料 |
| P2 | オファーの前にリマインダー画面 | 「忘れてもキャンセルできる」を先に出すと、トライアル開始が上がる（Paywall Index） | 同上 |
| P3 | オファー自体（期間・価格・トライアル日数） | Adapty どおり、見た目より先にオファーを試す | 有料化と LTV。返金・解約も見る |

P1 は `team/playbooks/DAILY-SHIP-LOOP.md` と `PURCHASE-FIX-2026-11-11.md` の年額先行と重なる。コード側の変更は Codex、提出は参謀。ペイウォール実験はバイナリまたはリモート設定のどちらで出すかを、開始時に実験メモへ書く。

## 7. やらないこと

- 審査中の PPO を二件目として立てない。
- US 評価1件のまま「trusted by millions」や偽の星を置かない。
- 未実装のウィジェット数やテーマ数を盛らない（「8 backgrounds」を「1000+」に書き換えない）。
- 有料の ASO / デザインツールを使わない。
- ロック画面実験の結果が出る前に、デフォルトの公開スクショを差し替えない。
