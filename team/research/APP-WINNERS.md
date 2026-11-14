# APP-WINNERS — 勝ちアプリの蓄積プレイブック

Written: 2026-11-11 15:10 JST, Grok Bot 参謀.
Order: 成田さん 14:56 JST（AppKittie の勝者をループで集め続ける）+ 追加方針（世界一のアファメーションアプリ、そして最も稼ぐモバイルアプリについて、チームが一番詳しい状態になる）。

このファイルが正本である。アプリ名で重複を除き、新しい事実だけを追記する。数字は出典に書いたとおりに記録し、無いものは `unknown` と書く。推測で埋めない。

コピーしてよいのはレイアウトと戦術だけである。ロゴ、イラスト、音声、文言の全文はコピーしない。

関連ファイル:
- ループの回次ログ: `team/research/APPKITTIE-WINNERS.md`
- A/B の完了条件とバックログ: `team/playbooks/AB-TEST-RULES.md`

---

## Affirmation apps

ニッチのゴールは、Anicca を世界一のアファメーションアプリにすること。ここを最も深く書く。売上・DL の AppKittie 数値は、公開ページに出ていたものだけを「AppKittie 公開ページ」と明記する。ダッシュボードのライブ一覧は有料壁の向こうにあり、この回では取れていない。Store の評価・IAP・スクショは 2026-11-11 の US App Store / iTunes lookup による。

カテゴリでいま見えている二つの型:

1. **ウィジェット型（規模の勝ち、I am / Motivation）** — 検索の先頭はロック画面・通知・ウィジェット。短い成果コピー。カードの実画面。ソフトペイウォール。年額＋短いトライアル。
2. **音声・物語型（2026年の新規勝ち、Stella / Aya / Innertune）** — 先頭は「聞く」。個別の音声や未来の自分の声、朝のアラーム。スクショは社会的証明やイラストが多い。カード型の Anicca が次に取りうる戦術はこちら（音声と朝のフック）だが、未実装の機能をスクショに描かない。

Anicca のいまの PPO は型1のレイアウト合わせが進行中。型2はプロダクト実験としてキューに入れ、ライブの PPO `d7ffa0d7` には触らない。

### I am - Daily Affirmations（ニッチの規模1位、Anicca が真似る基準）

| 項目 | 記録 | 出典 |
|---|---|---|
| 名前 | I am - Daily Affirmations | US ストア |
| 開発者 | Monkey Taps | iTunes lookup 2026-11-11 |
| ストア | https://apps.apple.com/us/app/i-am-daily-affirmations/id874656917 | |
| AppKittie の売上 / DL | unknown（公開ページに数値なし） | AppKittie 公開ページ 2026-11-11 |
| US 評価 | 4.83（738,598件）、無料、v7.8.0 | iTunes lookup 2026-11-11 |
| 公開 | 2014-05-13、最終更新 2026-11-06 09:16 JST（ストアの UTC を変換） | iTunes lookup |
| スクショ枚数 | 9（1242×2688） | iTunes lookup / IAM-LAYOUT-SPEC-v2 |

- **ウィジェット:** ロック画面・ホーム・Watch がストアの主メッセージ。字幕候補（ページ内の最初の非ジャンル字幕）: "Inspirational positive widgets"。
- **オンボーディング:** ScreensDesign では 25ステップ。目標・気分・信念、名前、星座、アプリアイコン、フィードテーマ。途中でバンドル横断宣伝。最後がペイウォール。設問の全文は ScreensDesign が有料のため unknown。
- **ペイウォール:** オンボーディングの最後。ソフト（閉じられる）。3日無料トライアル → 年額。年額を月額換算で表示（SD-IAM）。閉じたあとに 20–50% のダウンセル（PaywallPro の解体、自前の実機撮影は未了）。
- **価格（US ストア IAP 一覧、2026-11-11）:** I am Premium (1 year) $59.99、I am Premium (1 month) $14.99、I am Premium (Lifetime) $89.99。ほかに同一名の $47.99 / $11.99 / $69.99 / $9.99 があり、期間はストア一覧では不明（オファーや試験SKUの可能性）。以前の社内メモの Lifetime $149.99 は、本日の一覧では $89.99 に変わっている。
- **ASO:** 名前に Daily Affirmations。ウィジェット語が字幕・スクショの主軸。14+ 言語展開は既存メモ（GROWTH-PLAN）にあるが、本日は言語リストを再確認していない。
- **広告:** AppKittie 公開ページには I am の広告クリエイティブは出ていない。unknown。

### Motivation - Daily quotes（I am の姉妹、同じ型）

| 項目 | 記録 | 出典 |
|---|---|---|
| 名前 | Motivation - Daily quotes | US ストア |
| 開発者 | Monkey Taps | iTunes lookup 2026-11-11 |
| ストア | https://apps.apple.com/us/app/motivation-daily-quotes/id876080126 | |
| AppKittie の売上 / DL | unknown | 公開ページに数値なし |
| US 評価 | 4.82（1,079,284件）、無料、v7.8.0 | iTunes lookup 2026-11-11 |
| 公開 | 2014-05-13、最終更新 2026-11-05 22:41 JST | iTunes lookup |

- **スクショ:** I am と同じ型。1枚目「Get motivation throughout the day」（ロック画面＋通知）。2枚目「Change your thoughts, change your life」（全文カード＋ストリーク）。3枚目はウィジェットの選択肢の多さ。字幕候補: "Positive widgets & motivation"。
- **オンボーディング / ペイウォール:** ScreensDesign ではソフトペイウォール、オンボーディングの最後、トライアルのタイムラインあり（SD-MOT）。ステップ数の再確認はしていない。
- **価格（US IAP 一覧）:** Motivation Premium / Premium Motivation として $47.99, $35.99, $11.99, $9.99, $39.99, $4.99, $23.99, $19.99, $3.99, $14.99。期間のラベルは一覧にない。ページ内の別箇所に monthly $8.99/mo、yearly $53.99/y with a 3-day trial という文言があるが、関連アプリの説明が混ざっている可能性があり、確定にはしない。
- **広告:** unknown（AppKittie 公開ページになし）。

### ThinkUp-Daily Affirmations app

| 項目 | 記録 | 出典 |
|---|---|---|
| 名前 | ThinkUp-Daily Affirmations app | US ストア |
| 開発者 | Precise Wellness LLC | iTunes lookup 2026-11-11 |
| ストア | https://apps.apple.com/us/app/thinkup-daily-affirmations-app/id906660772 | |
| AppKittie の売上 / DL | unknown | 公開ページに数値なし |
| US 評価 | 4.75（7,519件）、無料、v1.18.11 | iTunes lookup 2026-11-11 |
| 公開 | 2014-12-09、最終更新 2025-08-03（1年以上ストア更新が空いている） | iTunes lookup |

- **スクショ:** オレンジ系。1枚目「Overcome Challenges with Positive Affirmations」（カテゴリグリッド、文字多め）。2枚目は引用・社会的証明。3枚目「Record Powerful Affirmations in your Voice」。自分の声で録音するのが差別化。字幕候補: "Positivity & Success Mindset"。
- **オンボーディング / ペイウォール:** 本日の公開解体はなし。unknown。
- **価格（ストア説明文の表記）:** MONTHLY $7.99 / ANNUAL $39.99（60% OFF、$3.33/month と併記）/ FOR-LIFE $99.99。IAP 一覧には ThinkUpTrial $39.99、Unlimited access for one year $39.99、Monthly $7.99、For Life $79.99 と $99.99、3 months $14.99 など複数SKU。トライアルの日数は説明文では unknown。
- **ウィジェット / 広告:** unknown。
- **示唆:** 「自分の声」はカード型との差別化になるが、Anicca が未実装ならスクショに描かない。

### Shine

有名だった The Shine App（日次のセルフケアメッセージ）は、2026-11-11 の US / GB 検索では見つからなかった。見つかったのは別物の「Shine - Daily Affirmations」（id6449884309、Mert Sen FINDICAK、US 評価 0件、2025-06-02 公開）だけである。旧 Shine の価格・オンボ・スクショは、現行ストアでは確認できない。過去の二次情報を現在の数字として使わない。

### Innertune: Daily Affirmations

| 項目 | 記録 | 出典 |
|---|---|---|
| 名前 | Innertune: Daily Affirmations | US ストア |
| 開発者 | Innertune Media Inc. | iTunes lookup 2026-11-11 |
| ストア | https://apps.apple.com/us/app/innertune-daily-affirmations/id6443625379 | |
| AppKittie の売上 / DL | unknown | 公開ページに数値なし |
| US 評価 | 4.85（12,047件）、無料、v6.14.3 | iTunes lookup 2026-11-11 |
| 公開 | 2022-11-15、最終更新 2026-11-05 23:30 JST | iTunes lookup |
| 字幕候補 | Affirmations for Focus & Calm | ストア HTML の先頭字幕（関連アプリが混ざる可能性あり） |

- **スクショ（本日、公式 screenshotUrls を直接確認）:**
  1. 暗い星空、ヘッドフォンの人物。「THIS IS HOW YOU TAKE BACK CONTROL OF YOUR MIND」。星5と「Trusted by 1.1 Million People.」。これはクリエイティブ上の主張であり、US 評価件数（12,047）とは一致しない。数字の検証はできていない。
  2. 「REALITY BENDS TO WHAT YOU BELIEVE」。実機ホームで名前付きの質問（What mindset do you want to cultivate?）とセッション一覧（Fall asleep、Love yourself など）。
  3. 「WAKE UP WITH POSITIVE AFFIRMATIONS」。起床アラームの実画面。プレイリスト／Voice／Beat。サイレントでも鳴る、という注記。
- **プロダクト:** 説明文は、再生して睡眠・仕事中・休息中に繰り返す音声アファメーション。朝アラームがスクショの3枚目。
- **価格（US IAP 一覧）:** Innertune Premium (Yearly) $29.99、Innertune Premium Monthly $9.99（ほか $9.95、$19.99）、Innertune Premium $39.99 / $49.99 / $69.99（期間ラベルなし）、3 Months $29.99。ストア側のオファー文言: 「Free for 3 days, then $29.99/year after trial.」
- **オンボーディング / 広告:** unknown。
- **示唆（戦術のみ）:** 朝に「聞く」フック。I am のロック画面に対する、もう一つの朝の接点。

### Stella - Manifest Anything（AppKittie 公開ページに名前が出る新規）

| 項目 | 記録 | 出典 |
|---|---|---|
| 名前 | Stella - Manifest Anything | US ストア |
| 開発者 | Perl Productions LLC | iTunes lookup 2026-11-11 |
| ストア | https://apps.apple.com/us/app/stella-manifest-anything/id6757347283 | |
| AppKittie の売上 / DL | unknown。公開マーケティングページのオーガニック枠に「Stella — Manifest method」とだけ出る。売上数字は付いていない | AppKittie 公開ページ 2026-11-11 |
| US 評価 | 4.72（5,588件）、無料、v2.3.20 | iTunes lookup 2026-11-11 |
| 公開 | 2026-01-28、最終更新 2026-11-08 05:08 JST | iTunes lookup |

- **スクショ（本日確認）:**
  1. 桃色グラデ、月桂冠、「#1 Manifestation App」。実機。名前で聞く入力欄（What do you want to manifest?）、トレンドのチップ、物語カードのグリッド。
  2. 「Join 300,000+ others.」とレビュー引用3件（社会的証明だけの画面。US 評価 5,588件に対し 300,000+ はクリエイティブ上の主張で、検証していない）。
  3. 「Personalized visualizations.」写真の上に一文が載るプレーヤー。
- **プロダクト（ストア説明）:** 夢の人生を個別の音声ナラティブとして聞く。
- **オンボーディング:** 以前の社内メモは 28ステップのクイズのあとハードペイウォール＋トライアル、と第三者資料に依っていた。本日 AppKittie のオンボーディング画面は未取得（有料）。ステップ数は unknown として扱う。
- **価格（US IAP 一覧）:** すべて「Stella - Unlimited」または「Stella Unlimited」で $6.99, $19.99, $7.99, $29.99, $8.99, $9.99, $12.99, $14.99。期間は一覧にない。レビュー本文に「$6.99 a week」とあるが、レビューは公式IAPではないので参考に留める。
- **広告 / オーガニック:** AppKittie 公開ページが「Manifest method」をオーガニック動画の例として使っている。クリエイティブ本体は公開ページの静止画のみで、本稿では中身を再掲しない。

### Aya: Manifest Your Dream Self

| 項目 | 記録 | 出典 |
|---|---|---|
| 名前 | Aya: Manifest Your Dream Self | US ストア |
| 開発者 | Lit Apps LLC (Mobile) | iTunes lookup 2026-11-11 |
| ストア | https://apps.apple.com/us/app/aya-manifest-your-dream-self/id6760195623 | |
| AppKittie の売上 / DL | unknown | 公開ページに数値なし |
| US 評価 | 4.80（3,218件）、無料、v1.7.8 | iTunes lookup 2026-11-11 |
| 公開 | 2026-04-15、最終更新 2026-11-03 23:28 JST | iTunes lookup |

- **スクショ（本日確認）:**
  1. イラスト主導。「Manifest Your Dream Self」。月桂冠に「4M manifestations」「500K listeners」（クリエイティブ上の主張。US 評価 3,218件とは一致しない。未検証）。
  2. 「Custom audio visualizations from your future self」。プレイリスト型の音声UI。
  3. 「Tailor-made Subliminals / focus, noise, sleep & more」。周波数とボイスのプレーヤー。
- **プロダクト（ストア説明）:** なりたい自分の声が毎日話しかける、という立て付け。
- **価格（US IAP 一覧）:** Aya Premium – Weekly $9.99、Weekly 25% Off $7.49、Aya Weekly – 3 Day Trial $5.99、Aya Premium – Monthly $29.95、Aya Monthly – 25% First Month $29.95、Aya Premium – Yearly $149.99。単品: Unlock This Playlist $4.99、Unlock This Audio $1.99、3 Instant Episodes $4.99、15 Instant Episodes $19.99。説明文の別箇所に「annual subscription priced at US$29.99 per year」ともあり、IAP 一覧の $149.99 と食い違う。両方を記録し、どちらが現行の主SKUかは unknown。
- **ASO:** 以前の社内メモは国別のタイトル／字幕ローカライズを挙げていた。本日のストアページでは未再確認。
- **広告:** unknown。

### 同じ棚の参考（深さは一段下げる）

| アプリ | ストア | US 評価（2026-11-11） | メモ |
|---|---|---|---|
| Mantra - Daily Affirmations (id1202851636) | https://apps.apple.com/us/app/mantra-daily-affirmations/id1202851636 | 4.84（34,449） | 短い成果コピー、暖色。AppKittie 数値 unknown |
| Finch: Self-Care Pet (id1528595748) | https://apps.apple.com/us/app/finch-self-care-pet/id1528595748 | 4.95（774,228） | ペット型の習慣。アファメーションではないがセルフケアの規模勝ち。AppKittie 数値 unknown |
| Manifest Affirmations (id1551665207) | https://apps.apple.com/us/app/manifest-affirmations/id1551665207 | 4.53（6,696） | 検索に出てくる隣接。未解体 |

### Anicca（自社、比較用）

| 項目 | 記録 | 出典 |
|---|---|---|
| 名前 | Daily Affirmations - Anicca | US ストア |
| ストア | https://apps.apple.com/us/app/daily-affirmations-anicca/id6755129214 | id6755129214 |
| AppKittie の売上 / DL | unknown（掲載を確認していない） | |
| US 評価 | 5.0（1件）、無料、公開中は v1.9.10 | iTunes lookup 2026-11-11 15:00 頃 JST |
| 直近7日ファネル | インプレッション 302、ページ閲覧 15、初回DL 1 | ANICCA-SCREENSHOT-TEARDOWN、2026-11-11 |

ボトルネックは検索のタップ。だからスクショ（とくに先頭3枚）が先。カード型の実画面はすでに揃っている。弱いのは見出しの長さと、音声・朝アラームといった型2のプロダクトがまだないこと。

---

## Profitable mobile app patterns

AppKittie が公開で見せているものと、六つのニッチでストアから拾った勝ちパターン。AppKittie の金額は、公開マーケティングページのフィルターデモに表示されていた文字列そのもの。認証済みダッシュボードのライブクエリではない。デモ用に選ばれた可能性があり、日付付きの「ページにこう出ていた」以上には扱わない。

### AppKittie 公開ページが示すもの（2026-11-11）

サイトが公開で約束している中身: 売上・DL の推計、広告、バイラル動画、ASO キーワード、オンボーディング画面。毎日更新、iOS と Android。使い方の公式コピーは「すでに稼いでいるアプリを見つけ、広告・クリエイター・ASO を学び、同じ需要で自分の版を作る」。

公開ページのフィルターデモに出ていた推計月次売上と、併記の「last 12 months」増減:

| アプリ名（ページ表記） | 表示された Est. Monthly Revenue | 表示された増減 |
|---|---|---|
| MyFitnessPal | $8.2M | +12% |
| AllTrails | $6.4M | +31% |
| Strava | $5.3M | 増減は隣接行にあり、この行では確定できず → unknown |
| Flo Period Tracker | $4.1M | +22% |
| Cal AI | $3M | +75% |
| Ladder Strength | $1.9M | +64% |
| DecAI | $1.2M | -18% |
| Bevel | $1M | +43% |
| BitePal | $860K | +91% |
| Glam AI | $820K | +40% |
| MenuFit | $800K | +58% |
| MeAgain | $730K | +112% |
| Lyfta | $315K | +20% |
| Nomadtable | $130K | +190% |
| Potto | $105K | +37% |
| Pep AI | $90K | +24% |
| QUITTR | $60K | -68% |

同じページのアプリ・プロフィールデモ: Cal AI - Calorie Tracker（Viral Development LLC）に Est. Monthly Revenue $3M、+75% last 12 months、IAP 帯 $0.99–$29.99。Nomadtable に $130K、+190%。DecAI に $1.2M、-18%。ストアリンクはデモには付いていなかった。

ほかに公開ページが出していたパターン（金額はページの文言どおり）:

- フィルター例:「Launch date · After Jan 1, 2024」「Revenue · > $200K / mo」「Sort · Revenue high → low」
- オンボーディング: 「Steal the onboarding that converts」。デモは Brainrot（33画面）、PushScroll、Lightly。利用者コメント「an app making $600K/mo」のオンボーディングを複製して転換が上がった、とある。対象アプリ名はコメントにない。
- オーガニック枠: Cal AI — Protein tracking、Stella — Manifest method、ほか Alarm pushups / Grocery haul / Solo travel
- 広告枠の例: Duolingo、Lyfta、Cal AI
- 証言: Prayer Lock の創業者を「$1M ARR」と紹介

アクセスの限界は `APPKITTIE-WINNERS.md` に書いた。Pro は $79/月 または $588/年、無料プランは API クレジット 0 で ads / creators / videos / screenshots がすべて閉じている。トライアルはクライアントフラグがオフで、オンの場合もカードが要る。買わない。カード登録もしない。

### カテゴリを横断する戦術（検証されたものだけ）

1. **長い投資クイズのあと、閉じられる年額トライアルのペイウォール。** I am / Motivation / BetterSleep / Calm / Daylio がこの型（PAYWALL-PRICING D1、ScreensDesign）。AppKittie もオンボーディングライブラリを売りにしている。
2. **検索に出る先頭3枚は、短い成果コピーと実体験。** Apple / AppTweak の公開指針。I am / Motivation が実行している。Anicca の7日ファネルでは、表示されてもページが開かれない。
3. **朝の接点を一つ、強くする。** I am はロック画面。Innertune と Wayk は起きがけのアラーム。Stella / Aya は「聞く」。
4. **年額を主、トライアルは年額、月額や週額はアンカーかダウンセル。** Health & Fitness の公開集計（Adapty / RevenueCat）。I am は年 $59.99、Innertune は年 $29.99＋3日トライアル。
5. **閉じたあとのダウンセル。** I am で確認されている（20–50%、タイマー）。Aya は週次・月次の割引SKUをストアに出している。
6. **新しい勝ち（2026年公開の Stella 2026-01-28、Aya 2026-04-15、Wayk 2026-02-03）は、既存の規模勝ちをそのまま縮小したコピーではない。** 個別音声、課題つきアラーム、国別ASOなど、一つの強いフックを足している。

### 残る五つのニッチ（AppKittie のライブ一覧は未取得）

数字が AppKittie に無いものは unknown。勝ちの型はストアと既存解体から。

**Honne（関係・メッセージ助言）**
- 自社: id6759667221、https://apps.apple.com/us/app/honne/id6759667221 （JP は 本音翻訳）
- 真似る相手: めろとーく（id6757545135）。JP 4.6、7,230件（PAYWALL-PRICING、日付は 2026-10-31）。オンボとペイウォールの画面は unknown。価格は Pro 1週 ¥500 / 1ヶ月 ¥980、Premium 1週 ¥980、チケット 5枚 ¥160・20枚 ¥480（同メモ）。
- AppKittie 数値: unknown。
- 戦術: 結果を先に見せ、そのあとペイウォール。スクショは伏せたチャット＋言ったこと／意味。

**Dhamma Quotes（仏教・名言）**
- 自社: id6757726663、https://apps.apple.com/us/app/dhamma-quotes/id6757726663
- ページ→DL は自社六つのなかで良い（GROWTH-PLAN で 34%）。カテゴリの売上1位は AppKittie では unknown。Motivation 型の年額＋トライアルタイムラインをペイウォールに載せる計画がある。
- スクショは具体的な約束を先に出す（自社で効いている型）。

**Sleep Reset（睡眠）**
- 自社: id6762143790、https://apps.apple.com/us/app/for-better-sleep-sleep-reset/id6762143790
- 真似る相手: BetterSleep (id314498713)、US 4.74（390,898）、https://apps.apple.com/us/app/bettersleep-relax-and-sleep/id314498713 。ソフトペイウォール、年額先行＋7日トライアル（PAYWALL-PRICING）。Calm / Headspace も同じ棚。
- AppKittie 公開ページに SleepSense の数値は出ていない。SleepSense: Sleep Tracker (id6791916451) は US 4.34（765）、2026-07-22 公開。売上は unknown。
- 戦術: 週額リードをやめ、年額＋トライアルを主にする。

**Thankful（感謝日記）**
- 自社: id6759514159、https://apps.apple.com/us/app/id6759514159
- 真似る相手: Gratitude: Self-Care Journal (id1372575227)、US 4.88（44,994）。5 Minute Journal (id1062945251)、US 4.76（17,626）、年額の目安 $39.99＋トライアル（既存メモ）。Daylio (id1194023242) はソフトペイウォール＋タイムライン。
- AppKittie 数値: unknown。
- 自社のページ→DL は 5.9% と細い。先頭スクショが先。

**STUDIO CHERIE（美容・サロン）**
- 自社: id6766485903、https://apps.apple.com/us/app/studio-cherie/id6766485903
- 真似る相手: 既存メモのニッチ1位は XZ（JP 4,094件、2026-11-11 時点の再計測はしていない）。
- AppKittie 公開デモに **Glam AI $820K、+40%** と出ている。美容寄りの名前だが、公開ページにストアリンクは無い。本日は ID を引いていない。
- 戦術: ページ転換が 4.2% と細いので先頭スクショ。課金は月額 $0.99 が承認済みで、ペイウォール実装が残件。

---

## 自社六アプリに適用したことと、その結果

新しい適用を、日付・アプリ・面・結果（または未計測）で追記する。結果が出るまでは「未計測」と書く。

| 日付 (JST) | アプリ / 面 | 何を、誰の型から | 結果 |
|---|---|---|---|
| 2026-10-31 | 六アプリ / オンボ・ペイウォール方針 | ソフトペイウォール、年額トライアル、最後のステップ（I am / Motivation / BetterSleep / Calm / Daylio） | 方針決定（D1）。各アプリの実装と試験開始はまちまち。Anicca 1.9.11 が審査中（ペイウォール更新）。試験の勝敗は未計測 |
| 2026-11-11 | Anicca / PPO スクショ en-US | I am 型の「1枚目をロック画面に」（題材だけ変える） | 実験 `d7ffa0d7` は WAITING_FOR_REVIEW。**触らない。** 結果はまだない |
| 2026-11-11 | Thankful / ストア宣伝文 en-US | Gratitude: Self-Care Journal の立て付け（日記＋アファメーション＋プライベート） | 1.0.2 に反映済み。ページ→DL は 11/18 に判定予定。現時点は未計測 |
| 2026-11-11 | Honne / 説明文 en-US | 結果先出し（ペーストして意味が分かること） | 説明の先頭は更新済み。1.0.7 は未提出。転換の変化は未計測 |
| 進行中 | Honne / ペイウォール | めろとーく（初回プレビューのあと、年額先行、3日トライアル） | 1.0.7 待ち。未計測 |
| 進行中 | Dhamma / ペイウォール | Motivation 型の年額＋トライアルタイムライン | 未計測。ページ→DL 34% はスクショ側の既存結果 |
| 進行中 | Sleep Reset / ペイウォール | BetterSleep（年額 $59.99＋7日トライアルを主、週額は従） | 未計測 |
| 進行中 | STUDIO CHERIE / ペイウォール | ニッチ価格 $0.99/月。RC 接続と壁の実装が残件 | 未計測。ページ→DL 4.2% が先の漏れでもある |

この回でバックログに足した次の実験は `AB-TEST-RULES.md` を見ること。ライブの PPO `d7ffa0d7` は止めない、差し替えない。

| 2026-11-11 15:45 | 六アプリ / オンボ「どこで知った？」 | [0xbono](https://x.com/0xbono/status/2120331430098080255)：流入元の回答で継続率を分けて読む（TikTok 組と IG 組は残り方が違う） | Anicca は `onboarding_source_title` 画面が既にある。次の計測から継続率・課金率を流入元別に分けて読む（PostHog breakdown）。他5アプリに同画面が無ければ追加候補。未計測 |

---

## 2026-11-12 11:45 JST 回（Grok Bot 参謀、無料ソースのみ）

出典: Apple 公開 RSS（US、top grossing / top free、Health & Fitness 6013・Lifestyle 6012・Social Networking 6005、2026-11-12 11:40 JST 取得）、iTunes lookup（評価・版・スクショ枚数）、US App Store ページの IAP 一覧。売上額はどの無料ソースにも出ていないので unknown。順位は RSS の表示どおり。既存の I am（H&F 売上 #34、無料 #60）、Motivation（売上 #28、無料 #33）、BetterSleep（売上 #30）、Stella（売上 #69）、SleepSense（売上 #80）は既に記録済みで、この回の順位だけ追記する。

| アプリ | ニッチ（自社） | ストア | 順位（US、本日 RSS） | 評価 | IAP（ストア一覧の表示どおり） | 売上 |
|---|---|---|---|---|---|---|
| Finch: Self-Care Pet | 自己ケア（Anicca） | https://apps.apple.com/us/app/finch-self-care-pet/id1528595748 | H&F 売上 #14、無料 #20 | 4.95（774,615） | Finch Plus $39.99 / $9.99 / $34.99 / $69.99 / $5.99 / $41.99 / $59.99 / $49.99、Guardian Program $7.99 | unknown |
| Paired: Couples & Relationship | 関係（Honne） | https://apps.apple.com/us/app/paired-couples-relationship/id1469609343 | Lifestyle 売上 #69 | 4.72（210,772） | Premium Annual $74.99 / $39.99、Monthly $14.99、ほか $59.99 / $44.99 / $36.99 / $29.99 | unknown |
| Cozy Couples: Relationship App | 関係（Honne） | https://apps.apple.com/us/app/cozy-couples-relationship-app/id6463766369 | Lifestyle 売上 #83 | 4.84（47,079） | Plus $39.99 / $29.99 / $7.99 / $4.99、Streak Repair $1.99、Stars 200 $2.99・400 $4.99・1000 $9.99 | unknown |
| RISE: Sleep Tracker | 睡眠（Sleep Reset） | https://apps.apple.com/us/app/rise-sleep-tracker/id1453884781 | H&F 無料 #15、売上 #67 | 4.73（73,942） | Sleep Improvement Membership $69.99 / $59.99 / $35.99 / $9.99、Sleep & Energy Premium $69.99、AI Expert Access $29.99 | unknown |
| Hatch Sleep | 睡眠（Sleep Reset、ハード連動なので参考止まり） | https://apps.apple.com/us/app/hatch-sleep/id1158048301 | H&F 売上 #5、無料 #49 | 4.53（62,130） | Yearly $49.99 / $59.99、Monthly $4.99–$9.99 | unknown |
| Day One: Daily Journal & Diary | 感謝日記（Thankful） | https://apps.apple.com/us/app/day-one-daily-journal-diary/id1044867788 | H&F 売上 #81 | 4.83（118,939） | Silver Yearly $49.99、Silver 1 Month $8.99、Gold $74.99 | unknown |
| Waking Up: Meditation & Wisdom | 仏教・知恵（Dhamma Quotes） | https://apps.apple.com/us/app/waking-up-meditation-wisdom/id1307736395 | H&F 売上 #55 | 4.92（42,749） | Monthly $19.99、Yearly $149.99 / $199.99、Family Yearly $229.99 | unknown |
| Hairify - AI Hairstyle Try On | 美容（STUDIO CHERIE） | https://apps.apple.com/us/app/hairify-ai-hairstyle-try-on/id6758685096 | Lifestyle 売上 #73（2026-02-12 公開の新規） | 4.59（1,757） | Pro Weekly $12.99、Pro Yearly $39.99、Credits Pack $9.99 / $19.99 / $29.99 | unknown |

- **スクショ（1枚目を目で確認したもの）:** Paired は「#1 Couples App」の大見出し＋月桂樹で評価 4.7・313,029件・17 Million Downloads、その下に実画面2台（記念日カウンターとクイズ）。RISE は小見出し「BETTER SLEEP, BETTER LIFE」＋大見出し「Become a morning person」（なりたい自分の一言）＋月桂樹「Trusted by 5 million early risers」＋媒体ロゴ。Finch は「Self-care is better together」とキャラクターのイラストだけ（実画面なし）。Cozy Couples / Hatch / Day One / Waking Up / Hairify の1枚目は未確認（unknown）。
- **型:** 売れている睡眠・関係アプリは、1枚目を「なりたい状態の一言」＋手持ちの社会的証明で始める。社会的証明は実数があるときだけ使える。
- **価格の型:** 関係アプリ2本とも年額が主で、Cozy Couples は年額に加えて小額の消耗課金（ストリーク修復・スター）を持つ。Hairify はウィークリー＋クレジットパック（AI 生成アプリの型）。
- **オンボーディング / ペイウォール / 広告:** この回は取っていない。unknown。Meta Ad Library は今回未確認。
- **説明文の型:** Paired と Day One は、説明文の先頭行に DL 数・Apple の受賞・メディア掲載を箇条書きで並べる。

---

## 2026-11-14 11:4x JST 回（Grok Bot 参謀、無料ソースのみ）

出典: Apple 公開 RSS（US、top grossing / top free 各100、Health & Fitness 6013・Lifestyle 6012・Social Networking 6005、2026-11-14 11:3x JST 取得）、iTunes lookup（評価・公開日・スクショ枚数）、US App Store ページの IAP 一覧（表示どおり、順不同）。売上額はどの無料ソースにも出ていないので unknown。Meta Ad Library・オンボーディング・ペイウォール画面はこの回も未確認（unknown）。

既存の順位更新（US、本日 RSS）: Calm H&F 売上 #5、Hatch #6・無料 #49、Headspace 売上 #13、Finch 売上 #14・無料 #19、Motivation 売上 #25・無料 #37、BetterSleep 売上 #30、I am 売上 #32・無料 #50、Waking Up 売上 #51、RISE 無料 #9・売上 #59、Stella 売上 #69、Day One 売上 #79、SleepSense 売上 #92、Wayk 無料 #62、Paired Lifestyle 売上 #66、Hairify 売上 #72、Cozy Couples 売上 #77。

| アプリ | ニッチ（自社） | ストア | 順位（US、本日 RSS） | 評価 / 公開日 | IAP（ストア一覧の表示どおり） | 売上 |
|---|---|---|---|---|---|---|
| RIZZ | メッセージ助言（Honne の直接の型） | https://apps.apple.com/us/app/id1663430725 | Lifestyle 売上 #82 | 4.83（40,192）/ 2023-01-12 | INFINITE RIZZ $3.99 / $6.99 / $9.99 / $19.99 / $69.99 / $99.99、ONE YEAR $69.99、Unlimited RIZZ $4.99 | unknown |
| That Girl: Become a Clean Girl | 自己ケア・習慣（Anicca / 美容寄り） | https://apps.apple.com/us/app/id6756178380 | Lifestyle 売上 #94（2025-12-15 公開の新規） | 4.78（6,783） | Unlimited access $8.99 / $14.99 / $19.99 / $39.99 / $44.99 / $49.99 / $59.99 | unknown |
| Tolan: Your Friendly Guide | 自己ケア・AI 相棒（Anicca） | https://apps.apple.com/us/app/id6477549878 | H&F 無料 #15、売上 #45 | 4.78（190,859）/ 2024-06-19 | Tolan Lite $11.99、Tolan Plus $24.99（ほか (Old) 表記の旧 SKU） | unknown |
| Sleep Cycle | 睡眠（Sleep Reset） | https://apps.apple.com/us/app/id320606217 | H&F 売上 #47 | 4.68（32,037） | Premium $2.99–$57.99 の複数 SKU（$29.99 / $34.99 / $39.99 / $57.99 ほか） | unknown |
| ShutEye | 睡眠（Sleep Reset） | https://apps.apple.com/us/app/id1490078804 | H&F 売上 #67 | 4.76（350,436） | 1-Year $59.99、1-Month $9.99、Limited Time Offer $29.99・6-Month $19.99、Family 1-Year $59.99 | unknown |
| Perfect365 | 美容（STUDIO CHERIE） | https://apps.apple.com/us/app/id475976577 | Lifestyle 売上 #63 | 4.84（183,154） | PLUS Month $9.99 / Year $39.99、単品パック $1.99–$4.99 | unknown |

- **スクショ（目で確認したもの）:** RIZZ は3枚だけ。1枚目は社会的証明（ナンバーワン表記、月桂樹で実績数、掲載媒体名の列挙）、2枚目は「手順1: チャットのスクショを入れる」の実画面、3枚目は「手順2: すぐ返信案が出る」の実画面。That Girl の1枚目は「なりたい自分＋now」の大見出しと人物写真、小さな月桂樹バッジ。Tolan の1枚目はキャラクターのイラストと一文の約束（実画面なし、Finch と同じ型）。他の1枚目は未確認。
- **型（新）:** 関係・メッセージ助言の売れ筋は、スクショを「入力 → 結果」の2コマの手順で見せる。文言は短い命令形2行ずつ。
- **型（再確認）:** 「なりたい自分」見出し（RISE 11/12）が That Girl でも1枚目に使われている。自己ケアの新規勝ち（Tolan、Finch）はキャラクター・相棒型。
- **価格の型:** RIZZ は週額相当の小額 SKU が多数＋年額 $69.99。ShutEye と Sleep Cycle は年額主＋期間限定の割引 SKU（閉じたあとのダウンセル型）。
