# Paperclip (paperclipai/paperclip) — 評価 2026-10-26 19:3x JST（参謀, Xタイムライン, P0）
Repo: https://github.com/paperclipai/paperclip — MIT、約107k★、本日も更新（pushed 2026-10-26 10:18Z）。サイト https://paperclip.ing、Cloudはウェイトリスト。
発見: X @RaajKapadia /status/2114622147595538719（最新リリース: private agent tasks/projects、権限、BYOモデルゲートウェイ、MCP連携）。
中身: 「エージェントのチームで事業を回す」Node.jsサーバー＋React UI。ゴール→「採用」（CEO/CTO/エンジニア/マーケ、任意のエージェント）→予算を決めて実行→ダッシュボードで監視。
柱4つ: タスク管理（承認・レビューゲート・定期実行）、エージェントの組織図（役割・権限・秘密情報の範囲）、エージェント育成（スキル共有・評価・性能レビュー）、Agentic OS（モデル横断の実行基盤・サンドボックス・MCP・コスト管理）。
対応: Claude Code / Codex / Cursor+Cloud / Gemini CLI / OpenCode / Hermes / Grok Build / Kimi。「heartbeatを受けられれば雇える」。

## なぜP0か
Aniccaの「人がループにいないゼロ人の会社」そのもの。僕らの今の仕組み（参謀＋Reasonの各セッション＋BOARD.md＋ルーチン）と同じ問題を、組織図・予算・ゴール整合・heartbeatで解いている。Life Manager Cloudが「固定スクリプトでなく、ゴールから動き続けるエージェント」であるべき、という成田さんの方針（10/26 18:00）とも一致。

## 判定: ADOPT（評価パイロット）＋真似る
1. 真似る（すぐ）: heartbeat型の採用モデル、エージェントごとの予算上限、ゴール→タスクの紐づけ、性能レビュー。Life Manager Cloudの設計（止まったら自動再起動・ゴールと数値から判断）に取り込む。
2. パイロット: box（またはMac mini）でローカル起動し、Life Manager Cloudの事業ゴール1つ（例: Capafy販売）で、Claude/Codexセッションを「社員」として登録し、BOARD.md運用と比べる（止まらず回るか・コスト・報告の手間）。
3. 判断基準: 1週間で「止まった回数」「人手の介入回数」「コスト」が今より良ければ、Life Manager Cloudの実行層の候補にする。悪ければ設計だけ借りる。
- 担当: life-manager-main-claude-2（LM Cloud実装側、パイロット）＋ Manager R&D セッション（PR #9005、組織運営モデルとして比較メモ）。コーディネーターが次回Reasonで配布。報告は参謀へ。
- やらないこと: 成田さんの秘密情報・本番顧客データを入れない。Paperclip Cloud（有料ウェイトリスト）は使わない。
- 公開投稿では名前を出さない。
