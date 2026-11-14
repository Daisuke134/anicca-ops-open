# AI Design Skills 導入とリデザイン方針（2026-10-26）

## 導入
- 取得元: /workspace/research/ai-design-skills, /workspace/research/redesign-skill（MIT確認済み）
- チーム共有: /workspace/team/skills/ai-design-skills/（README参照）
- 採用: redesign-existing-projects（既存ページ全般）, landing-page-design（構成・コピー・ビジュアル規則）, design-to-motion（X/LP用動画・GIF）
- ページ割当: /lm→redesign＋landing(A2/A4/A5)。/en /ja→redesign監査のみ（創業ストーリー本文は維持）。affirmation-app→redesign＋design-to-motion（ウィジェット動作ループ）。Honne/PDF Insight→redesign。AI Monk→landing（新規）。Capafy/PromptBase→design-to-motionでサムネ/プレビュー。

## 最優先ページ: aniccaai.com/lm（Life Manager）
理由: 有料Cloudの入口で、現状は機能説明が長く、CTAが2つ並び（Run it locally / Explore cloud）、"being built" が多く成果が見えない。A8の落とし穴（曖昧な価値、競合CTA、成果なき機能列挙）に当たる。
※ affirmation-appは今回curlで本文がほぼ取れなかった（クライアント描画の可能性）。SEO観点で次点として監査すること。

### 構成（landing-page-design A2, レイアウトA: クラシックヒーロー＋セクション）
1. ヒーロー: 見出し（成果＋対象）、サブ見出し、主CTA1つ、証拠1つ、実画面
2. タグライン表示セクション（B11、単語ごとに濃くなる）
3. 問題→解決（毎日指示し直す負担 → 自分から動いて結果を確かめる管理役）
4. 効果3つ: お金と仕事／毎日のこと／体と心（各1行の成果＋具体例）
5. 使い方3ステップ: つなぐ → 任せる範囲を決める → 確認済みの結果を受け取る
6. 証拠: 実際のログ画面・オープンソースのリポジトリ（実在のもののみ）
7. FAQ 6〜12問（料金、データの置き場所、ローカルとCloudの違い、解約、収入は保証されない、など）
8. リスク低減: **7-day free trial**、いつでも解約
9. 最終CTA（ヒーローと同一）

### ヒーローコピー方針（誠実に）
- 見出し案: "A manager that moves your life forward without being asked." / JA「頼まなくても、あなたの毎日を前に進めるマネージャー。」
- サブ: 仕事・収入・生活・体と心を一つのマネージャーが優先順位を決めて進め、結果を確認する。オープンソースのコアをローカルで、またはCloudで常時稼働。
- 主CTA: "Start 7-day free trial"（Cloud）。ローカル版はヒーロー下のテキストリンクに格下げ。
- 証拠1行: オープンソース（GitHub）＋実際の稼働ログのスクショ。ユーザー数・収益などの数字は実データが出るまで書かない。「収入は保証されません」は残す。

### ビジュアル（B1〜B7）
単一書体、斜体・極太なし、文中ハイフンなし、Tailwind刻みのサイズ/余白、背景グラデーションなし、ヒーロー幅680px上限、動きはIntersectionObserver。ヒーロー画像はdesign-to-motionで「朝のブリーフィング→タスク完了確認」のループ動画化。

### 上位3変更
1. CTAを1本化: "Start 7-day free trial"（スモークテストが要求する文言）を主CTAに、ローカル版は副リンクへ。
2. ヒーローを成果主語に書き直し、"being built"・機能説明の長文を削って実画面/動画で見せる。
3. 3ステップ＋FAQ＋リスク低減（7日無料・解約自由・収入非保証）を追加して不安を下で潰す。

### 担当・手順
- 担当: Reason main-claude（life-manager-main-claude-2）。life-manager でPR → anicca-products のワークフローピン（landing-pr-build.yml, netlify-deploy.yml）更新 → Netlify。
- /lm スモークテストは '7-day free trial' の文言が必要。EN/JA両方。
- 計測: 主CTAクリック率と trial 開始数を変更前後で比較（PostHog）。
- 本ドキュメント作成時点でデプロイは一切していない。
