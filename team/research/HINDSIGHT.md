# Hindsight (vectorize-io/hindsight) — 評価 2026-10-26 17:3x JST（参謀, Xタイムライン）
Repo: https://github.com/vectorize-io/hindsight — MIT（ルート LICENSE, © Vectorize AI）。hindsight-api パッケージのREADMEは Apache-2.0 表記（どちらも商用可）。約53.8k★。X上で「53,000 stars」投稿（@vatanmalik_45, 10/26）から発見。

## 判定: ADOPT（パイロット）
- Life Manager Cloud: 顧客ごとに bank を1つ（bank_id=customer）。「その人の生活の事実」と「Managerがやったことの結果」を分けて持てる＝Managerの判断記録・学習にそのまま合う。Hindsight Cloud には依存しない（顧客データは自前VMの self-host のみ）。
- Manager R&D（PR #9005）: 記憶層の比較対象として、既存のファイル記憶と同じ課題で長期記憶タスクの成績を比べる。合成データのみ（rights-cleared-only）。
- 担当: life-manager-main-claude-2（LM Cloud側の組み込み案、フラグの裏で）＋ Manager R&D セッション（評価）。コーディネーターが次回Reasonで配布。
- やらないこと: 本番顧客データ投入は評価が出てから。
