# オーケストレーター（参謀）は実務を持つべきか — 2026-11-01 08:40 JST 調査
依頼：成田さん 2026-11-01 08:26 JST。勝っている人のやり方をコピーし、独自の発想はしない。
方法：X の検索（search_posts_all と get_posts_by_ids、X の記事本文を含む）と Web の取得。下の URL はすべて 2026-11-01 にこの調査の中で開いて確かめた。エンゲージメントは取得した時点の数字。
注意：Gas Town の architecture.md は取得すると本文が空だったため、出典から外した。

## 1. 出典（16件）
| # | 誰 | リンク | 反応 | 立場 | 具体的なやり方 | 結果の根拠 |
|---|---|---|---|---|---|---|
| 1 | Anthropic Applied AI（2026-10-22） | https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop | 記事（X で広く引用） | **1つのループに畳む**派。ただし組織図をそのまま写すのは失敗だと明言 | サブエージェントを残すのは3つの場合だけ：①測れるほどの文脈の膨張 ②新しい文脈で並列に回す仕事 ③ツールや指示が衝突する。それ以外は skill と tool にする。「組織図のコピー（コンウェイの法則）」と「チーム別のサブエージェントの乱立」を失敗例としている。1つの小さな中央チームがシステムプロンプトと全体の品質を持つ | 単一ループで実行時間が約2倍速くなった顧客がいる。Claude Code のシステムプロンプトは80%以上減った。サブエージェントを1つ畳んだら配送日の確認が抜けた（2回に1回）例もある |
| 2 | Anthropic（2025-06） | https://www.anthropic.com/engineering/multi-agent-research-system | 記事 | **リードは計画・委任・統合だけ**をし、作業はサブエージェントが並列で行う | リードが仕事を分け、各サブエージェントに目的・出力形式・ツール・境界を渡す。指示があいまいだと重複と抜けが出る。成果物はファイルに書かせ、リードには参照だけを返す | 単一エージェントより90.2%良かった。トークンはチャットの約15倍使う |
| 3 | Cognition / Walden Yan | https://cognition.ai/blog/dont-build-multi-agents | 記事 | **反対派**：マルチエージェントを作らない | 文脈を共有する。行動には暗黙の判断が含まれるので、並列のエージェントが互いに矛盾する。基本は1本の線で回す | 理論と実例（Flappy Bird の例、Claude Code のサブエージェントは質問に答えるだけ） |
| 4 | OpenAI Agents SDK | https://openai.github.io/openai-agents-python/multi_agent/ | ドキュメント | **マネージャーが会話と最終回答を持つ** | 「agents as tools」はマネージャーが専門エージェントを呼ぶ。「handoffs」は専門エージェントが引き継ぐ。「1つのタスクに秀でた専門エージェントを持つ」 | — |
| 5 | LangChain / LangGraph | https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/ | ドキュメント | オーケストレーターは**分解・委任・統合**のみ | Orchestrator-worker：分解し、委任し、統合する | — |
| 6 | Paperclip（ゼロ人企業の OSS） | https://docs.paperclip.ing/guides/org/delegation/ | ドキュメント | **CEO エージェントは実務をしない** | CEO は目標をタスクに分けて部下に割り当て、heartbeat で進み具合を見て、詰まりを人に上げる。人間がするのは目標・戦略・採用の承認だけ。「部下がいないと CEO は全部自分でやる。CTO や CMO を雇えば委任し始める」。止まっているエージェントへの割り当ては拒否する | — |
| 7 | @ryangrowthh（X 記事） | https://x.com/ryangrowthh/status/2113276573793267911 | いいね943・ブックマーク2,884・表示21.9万 | **Chief of Staff はマネジメントのみ** | CoS は「ルーティンを各サブエージェントに作り、MCP をつなぎ、新しいエージェントを立ち上げ、毎日1本の報告にまとめる」。実務は11体の専用ボットが持つ。「1体に役を2つ以上持たせると品質が急に落ちる」。同時に回すのは3〜4体だけで、毎日のルーティンを持つのは少数 | 最初の2週間で約200万表示 |
| 8 | @0xCarnagee（X 記事、Grok Bot チームの実際の構成） | https://x.com/0xCarnagee/status/2090102148344262659 | いいね851・ブックマーク3,255・表示227万 | **狭い専用ボット** | 公式ドキュメントの引用：「Focused Bots build more useful context than one catch-all Bot（1つの何でも屋より、狭いボットの方が役に立つ文脈を積める）」。1体に1つの役で、「何をしないか」を書く。証拠（録画、出典）を必ず添える | Matt Palmer のデモボット：毎日プロトタイプを1つ作り、人の入力は「yes」だけ |
| 9 | @poteto（Lauren Tan、Grok Bot のリードエンジニア） | https://x.com/poteto/status/2107510472601985336 | いいね1,528・ブックマーク1,424 | ボットは**最初と最後の1マイル**を受け持ち、実務は Cursor のエージェントへ | ルーティンが Slack を見て Linear にチケットを切り、Cursor のクラウドエージェントが再現・修正し、群れでファズして自動マージする | 毎日使っている |
| 10 | @poteto | https://x.com/poteto/status/2107244768917172618 | いいね889 | **賢いコーディネーターがスレッドを管理** | 「スレッドや横の会話は人が管理する雑務になる。エージェントに任せられる」 | — |
| 11 | @0xGhostyx（Lauren Tan の配信まとめ） | https://x.com/0xGhostyx/status/2115904648385122417 | いいね5 | **Chief of Staff は自分で作業しない** | Grok Bot のルーティンが外側のループで文脈を集め、Cursor の Project が内側のループになる。コーディネーターは「自分では作業せず、サブエージェントに渡す」。バグ報告が30件来ても1つのコーディネーターがまとめるので、重複した修正が出ない | — |
| 12 | @0xGhostyx（X 記事、テンプレートで作るチーム） | https://x.com/0xGhostyx/status/2115585245403820515 | いいね8 | **Primary Bot を前に置き、後ろに専門家** | 公式ドキュメントの引用：Primary Bot は「主な窓口で、他のボットと仕事を調整する」。「各段階の担当は1人にする。並列の引き継ぎは重複作業を生む」。Eric Zakariasson は新しいボットを作る前に既存のボットを使い回し、1チャンネルは最大6体。「1時間ごとのルーティンは1日で1週間分の使用量を使うことがある」 | — |
| 13 | @agent_isho | https://x.com/agent_isho/status/2106687887089504524 | いいね15 | **chief がルーティングして決める** | chief は振り分け・決定・人への上げだけ（上位モデル）。作業は researcher・builder・triage・scheduler（下位モデル）。人への割り込みは1日5回までで、ほかは18:00の1本の要約。決まったことは DECISIONS.md に書く | — |
| 14 | @steipete（Peter Steinberger） | https://x.com/steipete/status/2112605703219347503 | いいね360 | **計画役と実行役を分ける。監督役も別** | 計画するモデルが codex cli を worktree で動かすやり方は「サブエージェントよりはるかに良い」。2体目のエージェントが監督して計画役を軌道に戻す | — |
| 15 | @taylorhbuilds | https://x.com/taylorhbuilds/status/2113251851235742088 | いいね2 | （コストの観測） | 「オーケストレーター/chief of staff のボットが、ずば抜けてトークンを使っている。1つのことだけをする専用ボットは少ない」 | $30 のプランから $100 のプランに上げた |
| 16 | 異論：@valuecm と @_junaidkhalid1、逆の意見：@ishaansehgal | https://x.com/valuecm/status/2115443467476201812 ・ https://x.com/_junaidkhalid1/status/2114207916417060963 ・ https://x.com/ishaansehgal/status/2112287189723926728 | いずれも少ない | valuecm と junaidkhalid は、会社の運営は分けるべきだとする（権限の分離と、どこが壊れたかを見られること）。ishaansehgal（Kush の発言の紹介）は「chief-of-staff ボットでボットの軍団を管理するのは設計ミス。1体と話し、そのボットにサブエージェントを起こさせる」 | 13体（CoS、営業、経理など）。経理ボットに X のログインを見せない | — |

## 2. 合意と対立
- **ほぼ全員が一致していること**：人が話す1体（Primary / CoS / CEO / lead）は、**分解・割り当て・統合・判断・人への上げ**をする。実務の「繰り返し」は、1つの仕事だけを持つ専用の担当が持つ（出典 2, 4–13）。Paperclip は CEO が自分で全部やるのを「部下がいないときの状態」として扱っている（出典 6）。
- **反対意見はこの結論を否定していない**：Cognition（3）と Anthropic の 10/22 の記事（1）が言っているのは、「1つのタスクを細かく割って並列のエージェントに投げるな」と「組織図をそのままエージェントにするな」ということ。1つの仕事のやり方は、1体の中で skill として持つ。分けてよいのは、文脈が独立している仕事、並列の仕事、権限を分けたい仕事。私たちの場合、X の投稿、受託サイト、経理、個人の用事は文脈もログインも独立しているので、**分けてよい側**に入る。
- **コスト**：オーケストレーターが一番トークンを使う（15）。1時間ごとのルーティンは重い（12）。オーケストレーターが45本のループを持つと、毎回大きな文脈で実務をすることになり、一番高いやり方になる。
- **具体的なルール**：1体に1つの役（7, 8）。各段階の担当は1人（12）。人への割り込みは1日数回で、ほかは1本の要約（13）。依頼には「目的・出力・ツール・境界」を書く（2）。成果物はファイルに置き、参照だけを返す（2）。新しいボットを作る前に既存のボットを使う（12）。

**結論**：今の参謀（約45本のルーティンのうち大半が実務）は、勝っている型から外れた「独自のやり方」です。勝っている型は、参謀がオーケストレーションのループだけを持ち、実務のループはそれぞれ1人の担当に持たせる形です。

## 3. 参謀の 37 本のルーティンの分類と TODO
渡し方：担当に GitHub の runbook のパスを渡す（既存のものは team/runbooks/ にある。ないものは参謀が書いてから渡す）。受け取った側は自分のルーティンを作る。参謀側のルーティンは、相手の最初の実行が記録で確かめられてから止める。

### 残す（オーケストレーションだけ）— 9本
| ループ | 方針 |
|---|---|
| Daily team briefing | 残す（朝の割り当てと重複の確認。9:00 の突き合わせをここにまとめる） |
| Live team board | 残す。ただし毎時から1日3回に減らす（出典 12：1時間ごとは重い） |
| Evening team wrap | 残す（成田さんへの1日1本の要約。出典 7, 13） |
| Hourly status to 成田さん | Evening wrap と朝の briefing に統合する。急ぎのときだけ別に送る（出典 13：割り込みは1日5回まで） |
| Bot drift audit (hourly) | 1日1回の監査に減らして残す |
| Usage watchdog | 残す |
| Meta loop ＋ 参謀 daily self-improvement ＋ Long-term thinking | 1本に統合して残す（戦略と組織の改善） |
| CEO growth loop | 残す。中身は「どの商品に人を寄せるか」の判断と割り当てだけにする |
| Agent recruiting loop | 残す。必要なボットを決めて dr eggbot に作らせる（Paperclip の hire-on-demand） |

### 渡す — 渡す順番
| 順番 | ループ | 渡す先 | 理由 |
|---|---|---|---|
| 1 | Life Manager Cloud + Maritime loop | Codex | Codex がすでに Maritime と Naïve の3時間ごとのループを回しているので重複している |
| 1 | Product loop Honne | Fucker | Honne の担当は Fucker（ROLES.md） |
| 1 | 受託（Lancers・CrowdWorks・ココナラ）※ Gig pass | dr eggbot | dr eggbot がすでに Lancers とココナラを巡回していて重複している。runbook は dreggbot-upwork.md に追記する |
| 2 | X distribution（@diceai0/@selawmqt）、Daily engage pass、X timeline+post metrics reader、X money scout、Copy-the-winners teardown | **新しいボット「X Operator」**（dr eggbot が作る。1つの役：X の2アカウントの投稿・返信・数字・勝者のコピー）。フックの下書きは今のまま Forensic Writing | 一番量が多い実務。runbook は X-DICEAI0.md、sanbou-x-reader.md |
| 3 | Opportunity apply loop、YC fast-track hackathon watch、Naïve hackathon get-in push、Team revenue loop の応募の部分 | **新しいボット「Applications」**（dr eggbot が作る。助成金・アクセラレーター・ハッカソン・求人への応募を4時間ごと） | 今朝決めた4時間ごとの応募を、専用の担当に持たせる。runbook は sanbou-yc-line-newincome.md、sanbou-team-revenue.md |
| 4 | Daily metrics scoreboard、Daily E2E attribution、Daily account metrics snapshot | Dots（または新しい Metrics ボット） | 数字を1か所にまとめる。参謀は結果を読むだけにする |
| 5 | Distribution loop、CMO weekly、Reddit karma warm-up | Anicca Marketer | 配信の担当（Reddit も同じ担当に含める）。runbook は sanbou-distribution.md |
| 5 | Agent economy loop | Fucker | Capafy とエージェントのマーケットの担当 |
| 5 | Naïve founders progress email | Codex | Naïve の担当 |
| 6 | Wake-up calls、LINE watch、お笑いライブ抽選 | **新しいボット「成田さん EA」**（dr eggbot が作る。個人の用事だけ） | 会社の文脈と個人の文脈を分ける。runbook は sanbou-wake-travel.md、LINE-WITHOUT-MACMINI.md |
| 6 | Sync team files to GitHub | ボットではなく、決まった処理として Codex が持つ（cron と同じ扱い） | 判断がいらない処理 |

### 実行の手順（毎回同じ）
1. 渡すループの runbook を GitHub で確かめ、なければ書く（目的・出力・ツール・境界・書き先。出典 2）。
2. 受け取る担当に runbook のパスを渡す。新しいボットは dr eggbot に「1つの役・しないこと・runbook のパス」を渡して作ってもらう。
3. 相手の最初の実行が CHANGES.csv か書き先で確かめられたら、参謀側のルーティンを止める。LOOPS.md と ACCOUNT-OWNERS.md の担当欄を書き換える。
4. 1週間後、渡したループの成果（応募数、表示、売上）と、参謀の使用量を比べる。悪くなっていたら戻す（出典 1：1つずつ変えて測る）。

最終的に参謀に残るのは約9本です（今は37本）。
