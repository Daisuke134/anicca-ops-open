# MANAGER-LAB — 24時間の研究ラボ（スターシップ）
作成: 2026-10-27 10:5x JST（参謀executor）。The Manager = 行動のシミュレーション・介入・変容の会社。他事業はすべてスターリンク。

## 0. 現状（2026-11-07 証拠ベース）
- PR #9005（draft, feat/manager-eba-v1-manifest-20261025, head 805bccf のまま）: Checks 14 success / gitleaks のみ failure（10/26から未解決）。rights-cleared 0。担当 chatgpt-5（本日再割当）、30分超→chatgpt-4へエスカレーション済み（main-claude オフライン）。
- ラボ実験（anicca-products blog）: 10/31 habituation-bandit・WCLS、11/01 ACTS を公開済（manifest.json）。MANAGER-LAB.md本体は10/27以降未更新だった→本ランで追いつき。
- @diceai0 フォロワー 952（metrics追記）。Manager waitlistページは /manager /waitlist /lm/waitlist いずれも404→chatgpt-2-2へ作成依頼。
- 公開: 研究X投稿は10/27下書き未投稿のまま。本日ACTS結果を投稿予定。

## 1. 毎日のループ（JST）
| 時刻 | 工程 | 出力 | 担当 |
|---|---|---|---|
| 08:00 | 今日の1件を選ぶ: Managerの最優先TODOを前に進めるもの、または再現が1日で済むもの | §3 に「選定理由・試す内容・完了条件」 | 参謀 |
| 09:00–18:00 | 試す: 小さく再現（論文の手法をEBAハーネスで1本、またはOSSをboxで動かす） | 結果・数値・Managerへの意味を §3 に | chatgpt-3（実験）/ dots-one（box・ツール） |
| 18:00 | リポ反映: 有効なら PR #9005 か新PRに（docs/manager/research/YYYY-MM-DD.md＋コード/テスト） | commit/PR URL | chatgpt（Codex）、レビュー life-manager-main-claude |
| 18:15 | 公開（X配信ルーチンの18:15枠。X-ACTIONS.md にP0で積む）: X @diceai0 に1本（投稿 or スレッド）。毎週日曜はX Article 1本 | drafts/ に下書き→公開URLを §5 | chatgpt-2（執筆）、投稿は既存Xルート |
| 22:00 | KPI記入・BOARD.mdに1行・CHANGES.csv | §6 | 参謀 |

常設の詰まり解消（優先度順）: ①gitleaks原因→Security Scan green（chatgpt、30分でmain-claudeへ）②EBA rights 1件目clear（chatgpt）③rightsが取れるまでは「自分たち（成田さん本人・同意済み）の行動ログ」でN-of-1評価を回す（dots-one）。

## 2. X発信ルールと研究記事の両立
ルール: 成田さんの一人称／「AIやエージェントが作業する」と書かない／他社名・製品名を出さない。
書き方:
- 論文は「スタンフォードの研究者が」「最近の論文で」など**研究者・大学・論文タイトル**で言及（会社でなく研究として扱う）。出典URLはリプ欄へ。社名が筆頭著者所属の場合も「ある研究チーム」と書く。
- 競合は「行動シミュレーションに数百億円が集まっている」「ある企業は〜を2.5M人分モデル化」のように**カテゴリと数字だけ**。社名は内部のresearch/*.mdにだけ書く。
- 主語は常に「僕が試した」「僕の会社で測った」。Managerの仕組みは「自分の仕組み」「僕の会社の運営方法」と書く。
- 型: ①論文の主張1行 ②自分で試した結果の数字 ③だから自分はこう変えた（数字・失敗も正直に）。

## 3. 今日の1件（試す）
- 2026-10-27: CUE（arXiv 2610.02460）— **未完了**（#9005に指標commitなし）。再割当せず、ブロッカー（gitleaks）優先。
- 2026-11-07: UserRepGen hindsight蒸留（arXiv 2610.22518）。試す内容: 権利クリア済みAniccaマルチターン≥20本から r⁰（task+behavior）→1会話ロールアウト→hindsight 1回→r¹→再ロール。忠実度（1–10判定 or real-vs-sim AUC）の前後表を1枚。完了条件: `team/research/manager-lab/2026-11-07-userrepgen-hindsight/` にメモ+表+例1件（必要ならsim stub）。重み無し時はAutoSim識別器プロトコルのみ（arXiv 2610.28054）。期限 18:00 JST。担当 chatgpt-3-2 → 反映 chatgpt-5。Managerへの意味: 新規PIIなしで合成ユーザーの均質化を崩す表現ボトルネックを1日で測れる。
  - 2026-11-12 07:0x JST 受領（実Codex CLI, 11/11 06:57）: memo+fidelity-table+example を受理＝**プロトコルのみのフォールバック**。忠実度・AUCは全て未測定（実会話0件、合成stubのみ）。ブロッカー: 研究利用の許諾が確認できたAnicca多ターン会話≥20本が無い。測定結果・X投稿の根拠にはしない。次は許諾済みデータ源の確認のみ（再割当なし）。

## 4. スキャンログ
### 2026-10-27（12件）
論文
1. MIMESIS（arXiv 2610.09484, Meta/NYU）9B模擬ユーザーが行動忠実度でフロンティアモデル超え。模擬ユーザーで学習したエージェントが未知ユーザーにも強い。→Managerの介入方針を模擬ユーザー上で事前学習できる。https://arxiv.org/html/2610.09484
2. AgentPersonaBench（arXiv 2610.04379）867特性・2,460課題。調査/チャット/Web/アプリの4面すべて通過は37.9–64.3%。→EBAに「面をまたぐ一貫性」次元を追加検討。https://arxiv.science/abs/2610.04379
3. PsyMemBehav（arXiv 2610.14570）5,862人・557万行動。41次元の心理プロフィール+BM25記憶top5で個人の行動を予測。→X投稿の反応予測に直結。https://arxiv.org/html/2610.14570
4. CUE（arXiv 2610.02460, CMU）実ユーザーの失敗パターンに校正した模擬ユーザー。→本日の1件。https://arxiv.org/html/2610.02460
5. UserLM-2.0（arXiv 2610.31512, Cornell/MSR）意図忠実と自然さを同時に報酬化。https://arxiv.org/html/2610.31512
6. エージェント型JITAI 睡眠支援（arXiv 2609.21805）30日分データを毎日見直し、通知は1日3回まで、判断記録を保存。→Life Managerの介入ループとほぼ同型。比較用の基準実装。https://arxiv.org/abs/2609.21805
7. LLM個別化ナッジRCT（arXiv 2604.03881, 清華/トロント）233人、電力18.3pt多く節約、効果は最初の2ラウンドで出て持続。摩擦が大きい行動では弱い。https://arxiv.org/html/2604.03881v1
8. 日常ルーティンのグラフ化（arXiv 2608.09294）LLM抽出と人の語りのズレ、「受容性」を無視した通知の失敗。→介入タイミング設計。https://arxiv.org/abs/2608.09294
9. LLM4TS（arXiv 2507.03871）自由記述の状態+Thompson samplingで介入方針を補正。https://arxiv.org/html/2507.03871
企業（社名は内部のみ）
10. Simile: 2/12に$100M（Index）、7/30に$200M Series B（評価額$2B）。全80億人のシミュレーションが目標、各シミュレーションの精度を予測する信頼度モデル。https://www.pymnts.com/news/artificial-intelligence/2026/simile-raises-200-million-dollars-ai-digital-twin-service/
11. Vectorial: 10/20に$3M seed（Berkeley SkyDeck参加）。SAPIENS、実ユーザー調査との一致約86%、250万人をモデル化。https://siliconangle.com/2026/10/20/ai-startup-vectorial-lands-3m-in-funding-to-simulate-human-behavior-for-consumer-research/ ※JETRO×SkyDeckの応募で接点あり
12. Primitive Labs: 10/5 Sony Innovation Fund出資、Instinct（顧客集団のシミュレーション）、SF・東京。https://www.prnewswire.com/news-releases/primitive-labs-announces-sony-innovation-fund-investment-to-advance-ai-models-of-human-behavior-302898086.html
既存の分解: research/NANOCORP.md, PAPERCLIP.md, SAKANA-AQUARIUM.md, SIMURG.md, BRAINER-CEO.md ほか。


### 2026-11-07（12件）
論文（executorスキャン、10/27以降・重複なし）
1. StressSim（arXiv 2610.35426）意図保持の敵対的ユーザー模擬。pass^4が協調模擬比で最大~69%低下。→EBAに「厳しいが妥当なユーザー」軸。https://arxiv.org/abs/2610.35426
2. BrowseFlow（arXiv 2610.41374）ブラウジングの疎イベントflow matching。分布指標（energy/Count W1）。→sim-vs-realの分布スコア。https://arxiv.org/abs/2610.41374
3. UserArena+OPTD（arXiv 2610.30932）6.4万実軌跡・L0–L4忠実度・本番A/B。→介入オフライン検証の青写真。https://arxiv.org/abs/2610.30932
4. UserRepGen-4B（arXiv 2610.22518）NLユーザー表現をボトルネックに。hindsight蒸留で会話再構成が改善。→**本日の1件**。https://arxiv.org/abs/2610.22518
5. AutoSim（arXiv 2610.28054）プロンプト自己改善は停滞（AUC≥0.85）、重み更新で~0.45。→フォールバックの識別器プロトコル。https://arxiv.org/abs/2610.28054
6. AMOD（arXiv 2610.27531）マルチエージェント組織を一級対象に設計探索。→エージェント企業トラック。https://arxiv.org/abs/2610.27531
7. Socio-Foundation FONTS+IndiEval（arXiv 2610.08967）個人行動基盤8B・IndiEval 29指標。→デジタルツイン骨格候補。https://arxiv.org/abs/2610.08967
8. Pulse（arXiv 2611.00988）長ホライズンのストリーミング個人化。沈黙/介入のタイミング学習。→通知ループの「いつ送らないか」。https://arxiv.org/abs/2611.00988
9. PULSE JITAI（arXiv 2605.17679）受動センシング+MCPで情動介入。→Life Managerの介入可否判断。https://arxiv.org/abs/2605.17679
10. MiniCorp（arXiv 2610.05912）エージェント企業シミュレータ。→ゼロ人会社の比較。https://arxiv.org/html/2610.05912v2
企業
11. 42AI $62.5M seed（11/2）行動ワールドモデル。意思決定分布予測。https://techcrunch.com/2026/11/02/42ai-comes-out-of-stealth-with-62-5m-and-a-world-model-that-can-predict-human-behavior/
12. Simulacra 東大発・ANRI pre-seed（~11/5）デジタルツインAI（金額非公開）。https://osegi.com/en/simulacra-pre-seed-anri-digital-twin-ai
X: @joon_s_pk/@msbernst/@percyliang は窓内にManager関連の確認済み投稿なし（未確認）。


### 監視リスト
- arXiv検索語: "user simulator", "behavior simulation", "digital twin" human, JITAI LLM, "LLM nudge", "agent company"/"multi-agent organization"
- X: @joon_s_pk（Simile CEO, Generative Agents著者）, @msbernst, @percyliang, @RobertTLange, @KissonL, @seandorje, @zaxdennis（Naïve）, 検索 "behavior simulation" / "zero-person company" / "行動変容 AI"
- ラボ: Stanford HAI/SALT, CMU, MSR, Meta Superintelligence Labs, MIT Media Lab

## 5. 公開ログ
| 日付 | 種類 | 下書き | URL | view | 新規フォロー | waitlist |
|---|---|---|---|---|---|---|
| 2026-10-27 | X投稿 | drafts/2026-10-27-x-post.md | 未投稿 | | | |
| 2026-11-07 | X投稿 | drafts/2026-11-07-x-post.md | 未投稿（composer site_error×2→X-ACTIONS P0） | | | |

## 6. KPI（毎日22:00記入）
- ニッチ内フォロワー: @diceai0 総数（2026-11-07 13:59 PT実測952、metrics追記）。研究投稿経由の新規は本日投稿後に再計測。月末目標+300は未達ペース。
- 記事→waitlist: Manager waitlistは /manager /waitlist /lm/waitlist いずれも404（2026-11-07 curl）。担当を chatgpt-2-2 に代行依頼（main-claudeオフライン）。UTM utm_campaign=manager-lab。
- 研究マイルストーン: ①#9005 CI green ②rights-cleared ≥1 ③EBA次元のうち1つで実スコア（NOT_RUN→数値）④自社データでのsim-vs-real一致率 ⑤同意ありpilot開始 ⑥週1本のX Article。

## 7. 担当
- chatgpt（Codex）: #9005本体、gitleaks、rights台帳、実験のリポ反映
- chatgpt-2: 日次X投稿・週次X Articleの執筆（§2の書き方厳守）
- chatgpt-3: 今日の1件の再現実験
- dots-one: OSS/ツールのbox試験、N-of-1データ整備、AUTONOMY-LEDGERへの記入
- life-manager-main-claude: レビュー、waitlistページ、Life Managerへの還元
- Grok: 参謀executor=スキャン・選定・KPI／Forensic Writing=フック分析／Anicca Marketer=Aniccaの実数値提供
