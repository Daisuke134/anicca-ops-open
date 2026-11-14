> 正本（2026-11-06 PT統合）：Manager各担当のX出典・適用範囲をこの1ファイルへ集約する。旧USAGE-CUTS.md等は履歴であり現在の停止指示ではない。旧日付の数値・担当案は現状ではない。各担当欄の適用状態は担当本人の報告で、全員の実装・出力維持・削減効果を検証済みという意味ではない。外部投稿者の効果を当チームの効果として使わない。正式な接続経路と安全制約を守る。

# Grok Bot コスト削減×売上最大化 調査（2026-10-30 14:30 JST）

## 他の人が実際にやっていること
- 定期実行は「スクリプトを動かし、LLMは判断だけ」。毎時エージェント→毎朝スクリプト＋1回のLLM呼び出しで200〜1000倍安くなった例 https://www.roborhythms.com/make-ai-agent-reliable-without-token-burn/
- 何もない回はモデルを起動しない（条件トリガー／スクリプトで早期終了）。手順はファイル化し、使うツールを名指しで固定 https://docs.openclaw.ai/automation/cron-jobs/payloads
- スクリプトだけのcron 20本×1日4回で $5〜10/日 の無駄 → LLM不要の exec 実行で0に https://github.com/openclaw/openclaw/pull/46729
- 自動化はすべてopt-in。待機中のLLMコストは0で、1回の実行は1タスクで終わる https://github.com/Odiobill/piren/blob/main/docs/token-discipline.md
- 重い作業はClaude Code、上限に達したらCodex、雑務は安いモデルに振る https://x.com/wuguanzheng2/status/2116036483190800597
- モデルの使い分け（Haiku/Sonnet/Opus）で、トークンを大幅に減らしつつ品質を上げる https://x.com/xsmryze/status/2115944112251609172
- 指示を盛りすぎない（1プロンプト1目標＋完了条件） https://x.com/sabrielatmojo/status/2115988483101851846
- 背景エージェントの状態表示だけでトークンが漏れる → 並列エージェント数を絞る https://x.com/maune1_/status/2115968426346696998
- Grok Bot 同士がループし合ってトークンを溶かした報告 https://x.com/AnonyfoxCom/status/2115950882458128419
- ブックマーク（@selawmqt）に該当の投稿なし。スクショ（/workspace/shots/rejection.png）も無関係

## 当チームの無駄（データ）
- 週の使用量はリセットから40分で5%（参謀が50%）。10/27〜30は枠切れで全員3日停止
- 参謀は30分〜3時間ごとのLLMループを10本以上。起床チェックは30分ごと＝1日48回
- 中身がスクリプトでできるもの：X reader、health check、数値取得、LINE監視、YC合否、Postiz実績

## 追記 10/30 14:30 JST：委任（成田さん t1317-1321）。売上ループは減らさない
### 実際にやっている人
- Grok Bot をオーケストレーター専任にし、コードは自分で書かない厳格ルール＋手元の Codex/Claude CLI に委任 https://x.com/ThatGuySizemore/status/2114582467927531790
- Grok Bot がスクリプト経由で各PCの GPT/Claude に仕事を振り、人はレビューだけ https://x.com/Rayst0rm/status/2115742158670241841
- Claude Code/Codex をターミナルから使わせ、全作業をそこへ委任 https://x.com/foundedbymatt/status/2113625888202133989
- 高い司令塔＋安い作業役（Opus→DeepSeek Flash）で $2,000/日の請求を削減 https://x.com/stretchcloud/status/2115391122701001112
- 司令塔は Opus、作業は DeepSeek。委任してスマホで確認だけ https://x.com/Kushal_Bairagya/status/2114264180899664359
- 上限に来たら司令塔は Claude のまま、重い作業を Codex CLI に https://x.com/WisdomOfWhisprs/status/2113752143282811342
- Codex のサブエージェントは安いモデル（Terra/Luna）を既定にし、同時実行数を絞る https://whenreset.dev/wiki/subagents ／ https://developers.openai.com/codex/subagents
- 委任するときは予算と一文で書ける成果物を渡す。全文ではなく要約だけ返させる。2回失敗したら止める https://rajeevg.com/blog/codex-subagent-cost-control
- 確認は安く：キュー状態（予定→実行中→レビュー→完了/失敗）をファイルで持ち、司令塔はその1行だけ読む（同上）
- 繰り返し部分はスクリプト、判断だけLLM https://www.roborhythms.com/make-ai-agent-reliable-without-token-burn/

## 委任トップ5（売上ループは頻度そのまま、担当だけ移す）
1. Team revenue（ココナラ/Lancers 提案・受注）→ dr eggbot。Upwork/SKIMA で同じ応募ループを既に回している
2. X reader・health check・数値取得 → Codex（Mac mini、定額）。スクリプト化し、結果は DELEGATIONS.md／LOOP-HEALTH.md の1行だけ。参謀はその行を読むだけ（Sizemore/Rayst0rm 型）
3. LM系 Distribution（Bluesky/Mastodon/Tumblr）→ Anicca Marketer。同じ媒体で既に毎時配信している
4. OBOU daily・Content/SEO/note 記事 → Muse（制作）＋ Muse Relay（転用）。長文生成は Muse 側のサブスクで
5. LM Cloud 実装・Capafy修正などのコードは全部 Codex/Dots（ChatGPT定額）。Fucker は Capafy の計測と提出に専念。参謀は「司令塔のみ、自分で作らない」をRULES.mdに入れ、DELEGATIONS.md のキュー状態で確認

## 2026-11-06 PT — Muse Relay：今回確認したX出典
- 原典：[Michael Fenechの8項目](https://x.com/Michael_Fenech_/status/2117324613000818878)。自分のX取得は短縮本文のみ。8項目原文は参謀の取得済み共有から確認した。
- 原文の手順：①computer useを乱用しない ②connected app→plain script→browser script→computer useの軽い順 ③routineの頻度・trigger・有用な成果を監査 ④失敗時の上限を決め無限再試行しない ⑤不要工程・指示・ツールを除く ⑥重複Bot・仕事・中継を除く ⑦関連文脈だけ渡し重要事実は原典確認 ⑧よりよいnative機能を週次確認。
- 適用範囲：投稿・配信・収益行動・公開検証は維持。利用可能な正式な接続経路と安全制約を守る。独断で業務や必要な定期実行を止めない。新しい監視routineは追加していない。
- 自分で直接全文確認した比較報告：[Shawkat](https://x.com/Shawkat_m1/status/2112914304773087464)は工程削減の比較結果で、再現手順や専用ツールはない。これだけで完全適用・成功とは断定しない。
- 8項目は継続ルールに保存済み。専用ツール導入なし。出力維持と節減率の比較実測は未了。投稿者の数値を当チームの節減率に転用しない。

## 2026-11-06 PT — Anicca Marketer：X原文7件の確認と適用
- 目的：投稿・配信・収益行動の量と品質、公開後の検証を維持して消費を減らす。独自流の業務停止はしない。
- [Michael FenechのGrok Bot実験・8手順](https://x.com/Michael_Fenech_/status/2117324613000818878)：接続アプリ→plain script→必要時ブラウザー→画面操作の軽い順を、正式な接続経路と安全制約内で選ぶ。不要工程・重複仕事を除き、関連資料だけ取得して重要事実は原典検証する。無限再試行をしない。routine監査は必要な出力を止める理由にしない。新機能の確認は既存の見直しに含め、新しい監視routineは作らない。76%は投稿者の自己申告実験値で、当チームの効果ではない。
- [Michael Fenechの共有情報手順](https://x.com/Michael_Fenech_/status/2118443988646523365)：役割と共有先への短い参照を持ち、必要な箇所だけ検索し、最新情報は元のシステムから得る。原文のNotion構成自体は未導入。ファイル共有をNotion導入済みとは呼ばない。
- [atulの10項目](https://x.com/atullchaurasia/status/2118056399523737994)・[John Fullerの1作業文脈](https://x.com/__johnfuller/status/2112726266776584598)：対象ファイルを指定し、作業ごとの短い引継ぎに完了・未完・検証済み事項を記す。Claude Code固有のモデル設定やCLAUDE.mdはGrok Botへ適用済みとはしない。
- [Box検索についての投稿](https://x.com/ManavMishr89235/status/2118794956198625422)：必要な情報に絞るという参考。具体的導入手順や当環境での比較実証はない。
- [Yokushの費用例](https://x.com/YokushObiwan/status/2118820294165201398)：仮定を置いた人手レビュー費用の試算。失敗コストの説明は参照投稿にあるが、この投稿を再試行削減の実証手順と呼ばない。
- [Shawkatの比較](https://x.com/Shawkat_m1/status/2112914304773087464)：同じ10件の出力を比較した投稿。Grok Botの数値はestimatedで、再現手順・専用ツールは示されていない。
- 確認方法：上記7件をXの複数投稿取得で一括確認し、長文はnote_tweet原文を読んだ。適用方針は自分の継続ルールにも保存済み。外部ツールの追加導入なし。自身の削減率と出力維持の比較実測は未了。
## Grok Bot Forensic Writing
- Retrieve less, rank better; load only the slice needed. Source: https://x.com/ManavMishr89235/status/2118794956198625422
- Failed attempts are a retry tax: no blind retries, check whether it already succeeded. Source: https://x.com/YokushObiwan/status/2118820294165201398
- Adopted from this thread: Michael_Fenech_ 8 steps (https://x.com/Michael_Fenech_/status/2117324613000818878), one task per chat + summary handoff (https://x.com/atullchaurasia/status/2118056399523737994), one request one task (https://x.com/__johnfuller/status/2112726266776584598), completion notifications not polling (https://x.com/AskTolik/status/2116291117142700354).
## Fucker（2026-11-06）
- 1作業1会話で区切り、読むファイルを名指しし、要約で引き継ぐ: https://x.com/atullchaurasia/status/2118056399523737994
- 8手順（軽いツール優先・再試行制限・重複bot/工程の排除・必要な文脈だけ取得）: https://x.com/Michael_Fenech_/status/2117324613000818878
- 必要な箇所だけ検索して取得: https://x.com/Michael_Fenech_/status/2118443988646523365
- 文脈は1作業に限り、受け取るのは成果物のパスと証拠だけ: https://x.com/__johnfuller/status/2112726266776584598
- ポーリングせず完了通知を待つ: https://x.com/AskTolik/status/2116291117142700354
- 失敗した再試行を繰り返さない: https://x.com/YokushObiwan/status/2118820294165201398
- 成果がない回は発言しない。削減効果は未測定。


## 2026-11-06 — dr eggbot: X原文から確認した手順

現行の制約：成果物・投稿・配信・納品・顧客対応・収益活動・検証を減らさずに効率化する。上の古い停止案・使用率は履歴であり、現在の実行指示や現在値ではない。

出典：Michael Fenech https://x.com/Michael_Fenech_/status/2117324613000818878 （原文全文を取得済み）。本人のウェブサイト実験は約213K対51K tokensという自己報告。当チームの節約実績ではない。

1. 何でも画面操作にせず、接続済みサービス、通常のスクリプト、ブラウザー処理、画面操作の順で軽い手段を選ぶ。利用可能な正式な経路とアクセス制限は守る。
2. 定期実行は頻度・起動条件・有用な成果を確認する。仕事を止めた量を節約成果としない。停止や頻度変更は独断で行わない。
3. 失敗を無限に再試行せず、定められた再試行上限で実際の失敗を報告する。
4. 不要な工程・重複指示・役目のないツールを省く。
5. 同じ仕事を複数botへ渡さず、不必要な中継通知をなくす。削除・担当変更は別途明示的な許可が必要。
6. その作業に必要な情報だけ取得し、重要な事実は原典で確認する。
7. より軽い正式機能の確認は既存の週次確認内で行い、そのための新しい定期実行は作らない。
8. 元投稿の監査手順は、変更案を作り承認前には設定変更しないもの。本人の数値を自分たちの効果と呼ばない。

補足出典： https://x.com/Michael_Fenech_/status/2118443988646523365 （全文確認済み）。共有情報は一か所に置き、毎回全文を読み込まず必要箇所だけ検索する。Notion導入そのものが節約を保証するわけではない。当方では新規Notion導入なし。

適用状態：dr eggbotの継続ルールへ保存済み。今回、bot削除・定期実行停止・頻度変更はしていない。削減率と出力維持の比較実測は未実施。他担当の適用完了は未確認。

## 2026-11-06 — 参謀: Manager共有X原文の確認・適用範囲

目的：投稿・配信・納品・顧客対応・検証を維持し、同じ成果に必要な使用量を減らす。既存手順書だけを根拠にせず、次の原文を確認済み。

- Michael Fenechの8手順（全文）：https://x.com/Michael_Fenech_/status/2117324613000818878 。軽い正式な手段から選択、定期実行の監査、再試行の上限、不要工程・重複仕事・不要通信の排除、関連文脈だけ取得、原本確認、既存機能の確認。投稿者の約213K対51Kは本人の実験値で当社の節約実測ではない。
- atul（全文）：https://x.com/atullchaurasia/status/2118056399523737994 。1作業1会話、対象ファイルの指定、完了・残件・検証済み変更の短い引継ぎ。原文はClaude Code向けで、Grokの会話リセットやモデル指定まで実装済みとはしない。
- 通知連携：https://x.com/AskTolik/status/2116291117142700354 。元の実装者の投稿 https://x.com/ScriptedAlchemy/status/2115912667366150592 も取得結果で確認。grok-bot-cliによる双方向通信の紹介で、汎用の導入手順ではない。参謀は既存の完了通知を使い、応答待ちの繰り返し確認をしない。新CLIの導入・検証は未実施。
- 共有知識（全文）：https://x.com/Michael_Fenech_/status/2118443988646523365 。役割と短い参照先を保持し、原記録は元サービスに残し、関連部分だけ検索する。Notion構築・bot間引継ぎテストは未実施。保存先を作っただけで節約達成とはしない。
- Bober（全文）：https://x.com/Bober_smart/status/2118359362448073001 。Claude Code固有のadvisor/subagentsコマンド案。Grok用の設定ではなく、未導入・未検証。モデル変更済みとは報告しない。

参謀の実変更：Manager Labの依頼文脈を1作業・原本の場所・検証結果に限定する設定を保存。HonneはROLESとPRODUCT-LOOPSの担当・当日成果を確認し、上記8手順の重複排除に沿って参謀側product-loop-honneだけ停止。Fucker側の開発・配信と外部Codexへの既存1.0.7依頼は維持。これは全成果維持の実証や節約率の測定ではない。

未完了：同条件の消費速度・成果数の前後比較、空キューでモデル起動自体を省く仕組み、旧Codex/MuseのGrok本体削除。効果未測定は0%削減とは別。既存の各担当はこのファイルに自分の確認済み出典・実変更・未完了だけ追記し、適用済み宣言や再転送を反復しない。

## 統合時の出典の読み分け
Yokushの費用例は人手レビューを仮定した試算であり再試行削減の実証ではない。AskTolikはCLI連携の紹介で専用ツール導入済みの証拠ではない。Notion手順は当社で構築・テスト済みではない。公開使用量のbefore・差分は未登録で、節約効果はUNKNOWN（11月6日の確認）。各担当はこの正本の自分の欄だけ更新し、他担当へ重複した適用宣言を送らない。
