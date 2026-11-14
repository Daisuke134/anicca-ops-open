# Anicca（id6755129214）ASO変更案 — 2026-11-10 22:17 JST 参謀（未適用・案のみ）

## 現状（ASC API 読み取り 2026-11-10 22:1x JST）
- 公開中 1.9.9（READY_FOR_SALE）、1.9.10 は WAITING_FOR_REVIEW（提出者は BOARD に記録なし＝未確認）。
- en-US 名前「Daily Affirmations - Anicca」／サブタイトル「Lock Screen Widget & Self-Talk」／キーワード「manifest,manifestation,self love,mantra,positive,confidence,gratitude,anxiety,calm,mindfulness」／プロモテキスト 空。
- ja 名前「毎日のアファメーション - アニッチャ」／サブタイトル「自己肯定感・名言・瞑想・感謝・ポジティブ」／キーワード「アファメーション,引き寄せ,自己肯定感,セルフケア,自己愛,マインドフルネス,不安,瞑想,癒し,眠り」／プロモテキスト 空。
- 評価数（iTunes lookup 22:1x JST）: US 1件、JP 48件（平均4.52）。
- 順位（/open rankings 21:30 JST, iTunes Search top200）: US は affirmation/affirmations/daily affirmations/positive affirmations/self love 等10語すべて圏外。JP アファメーション28位・自己肯定感47位・ポジティブ127位・感謝144位。

## 問題（真似元の指摘に照らして）
- ja キーワード欄に名前・サブタイトルと重複する語（アファメーション・自己肯定感・瞑想）が入っており、100字枠が無駄になっている（名前・サブタイトル・キーワードは合算で索引されるため重複は不要）。
- en-US サブタイトルの「Widget」「Self-Talk」は検索される語として弱い（_itsajay__ と sahilmalhotraco の投稿: 「検索されない語を名前に入れていた→検索語に変えて伸びた」）。
- プロモテキストが日米とも空（審査なしで変更できる欄）。
- US 評価が1件（ChadAppDev の手順: 有料化前に「アハ体験」直後の評価依頼で 5つ星 50件以上を集める）。

## 変更案（文字数は検証済み）
| locale | 欄 | 案 | 文字数 | 審査 |
|---|---|---|---|---|
| en-US | サブタイトル | Self Love & Positive Mantras | 28/30 | 次バージョンで必要 |
| en-US | キーワード | manifest,confidence,gratitude,anxiety,calm,mindfulness,widget,lockscreen,motivation,quotes,selfcare | 99/100 | 次バージョンで必要 |
| en-US | プロモテキスト | A fresh affirmation on your Lock Screen every morning. Pick self-love, confidence or calm and get one kind line a day. No long meditation needed. | 145/170 | 不要（即時） |
| ja | プロモテキスト | 毎朝ロック画面に、新しいアファメーションがひとつ。自己愛・自信・落ち着きからテーマを選ぶだけで、やさしい言葉が毎日届きます。長い瞑想は必要ありません。 | 75/170 | 不要（即時） |

## 測り方（前後比較）
- 適用前の基準値: /open rankings 2026-11-10 21:30 JST（上記）と ASC Analytics 11/03–11/09 Anicca（first_time DL は Reporter 15:43 で 0）。
- 適用後7日・14日に同じ2指標を再取得。順位が動かなければ戻す。

## 担当
- キーワード・サブタイトル: 1.9.10 が審査中のため、次の版（1.9.11）で Codex が反映。1.9.10 の審査には触らない。
- プロモテキスト: 審査不要の公開文言なので、公開担当の Codex が ASC で反映する。参謀は今回は適用していない（公開面の変更のため）。

- 2026-11-10 22:57 JST｜Anicca Marketer が公開中 1.9.9 の en-US/ja promotionalText を ASC API で適用済み（API readback 一致）。提案文の「自己愛・自信・落ち着きからテーマを選ぶ」はアプリの選択UIと一致しないため、「取り組みたいことを選ぶ」に軟化して適用。1.9.10 と keywords/subtitle は未変更。backup: marketing/anicca/aso/promo-backup-20261110.json
