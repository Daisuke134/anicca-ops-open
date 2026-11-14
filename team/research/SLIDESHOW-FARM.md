# Slideshow Farm プレイブック（Ernesto Lopez型）— 2026-10-26
出典: https://x.com/ErnestoSOFTWARE/status/2112940887806296269 （X記事 "How we automated a slideshow farm 10M+ views/mo ran by AI agents", 2026-10-22 01:15 JST公開。Viktor/Postiz提供のスポンサー記事）
## 元データ
- レシピアプリのページ: 193本を手作業で1日1〜2本 → 8.6M再生、最高981K。投稿停止でページも停止
- 形式: 1枚目=料理写真+名前、次=材料、最後=アプリCTA。キャプションにアプリ名フル表記
- 目安: 5M再生 ≈ $2k–5k売上（オンボーディング次第）
## バズる3要素
1. フック: 誰向けかを名指し、次スライドを見ざるを得ない形。当たりフックは文言少し変えて何度も再利用（Part 2, 3…）
2. 一貫したテーマ/キャラ: 同じキャラ・同じ見た目でフィードを統一（Higgsfieldでキャラ固定）
3. サウンド: ニッチで当たった曲を使い続ける（当たり曲は平均の7〜8倍）
## 自動化手順（記事の構成）
1. ニッチ最大のページをViewTrack(自社ツール)で全スライド+再生/保存を抽出
2. AI社員(Viktor, Slack)が上位3フォーマットを抽出 → 2か月分のブリーフ
3. Claude+Higgsfield MCP(higgsfield.ai/mcp)で120本一括制作、最終スライドにアプリ
4. 人が承認 → Postizで11/1〜12/30を一括予約
5. 毎週月曜に再生数レビュー → 当たりはPt2、大当たりはKling(Higgsfield)で動画化
## 我々の版（無料・人間なし）
- 対象: モンク系TikTok/IG、Anicca TikTok。1日1本/アカウント（慣れたら2本）
- 分析: ViewTrack無し → X/TikTok公開ページを手動/Apifyで上位ページ抽出、保存数重視
- 制作: 画像はGenerateImage/既存素材、スライドはスクリプト生成（6〜8枚、9:16）。モンク=同じ僧侶キャラ+一言の教え、Anicca=「寝る前に読むアファメーション」等のフック固定
- 投稿: Postiz（接続済みMCPあり）で予約。最後のスライド=Anicca、キャプションにアプリ名+UTM(ct=tt_slideshow)
- 承認: 人の承認の代わりにMuse/参謀が品質ゲート（誇張・医療的主張なし）
- 週次: 月曜に再生/保存→当たりのPt2を作成。結果はLEARNINGS.md
- 担当: Anicca Marketer=Anicca TikTok試作、Muse=モンク系、参謀=週次レビュー
