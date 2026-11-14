# APPKITTIE-WINNERS — ループログ

Source of truth for the playbook itself is `team/research/APP-WINNERS.md` (アファメーションを最先・最深に書き、そのあとに稼ぐ型、そのあとに自社への適用ログ)。このファイルは AppKittie の回次記録である。同じアプリの重複は書かず、前回から変わったことだけ足す。

ルール: 有料プランは買わない。無料トライアルでもカードは登録しない。ボットのメールだけで完結する無料枠があれば、そのときにだけアカウントを作る。数字はページに出たとおり。無ければ unknown。

古いメモ `team/opportunities/APPKITTIE-WINNERS.md`（2026-10-26）は、当時すでにログインが有料だったため apphitlist など別ソースの推計を使っている。その金額を、AppKittie の数値として再掲しない。

---

## ループの回し方

1. 公開ページ `https://www.appkittie.com/` を取る。通常の WebFetch は空になる（JS）。`curl` で HTML を取り、`RSC: 1` + `Accept: text/x-component` で RSC を取る。必要なら box の Playwright / Chromium で描画する。
2. 公開ドキュメントは Markdown で読める: `https://www.appkittie.com/docs/llms.txt` と各 `.md`。
3. `/api/v1/*` は API キー必須で、キーは Pro のダッシュボードから発行する。無料プランのクレジットは 0。ここにキーを足さない。
4. 公開ページに出た勝者を、六つのニッチ（アファメーション、関係・メッセージ、仏教・名言、睡眠、感謝日記、美容・サロン）と横断パターンに振り分ける。
5. 各アプリはストアリンクを iTunes lookup で足す。AppKittie に売上／DL が無ければ unknown。
6. 新しい事実だけを `APP-WINNERS.md` にマージする（アプリ名で重複排除）。このログに回次を1節足す。
7. コピーする変更が1–2個決まったら `team/playbooks/AB-TEST-RULES.md` のバックログへ、オーナーと完了条件つきで入れる。走っている PPO は止めない。
8. `/workspace/anicca-ops-gh` で編集し、`share.sh` する（`.team-share-repo` を直接編集しない）。

目安は毎日1回。公開デモの金額が前回と同じなら「変化なし」と書いて終わる。

---

## Run 1 — 2026-11-11 15:10 JST（Grok Bot 参謀）

成田さんの依頼は 14:56 JST。初回。

### アクセス

| 経路 | 結果 |
|---|---|
| WebFetch | 空（想定どおり、JS サイト） |
| `curl` HTML / RSC | 成功。公開マーケティングページ、FAQ、フィルターデモ、プロフィールデモ、オンボーディング／広告／オーガニックの説明を取得 |
| `/health` | `{"ok":true}`（サイトのヘルスチェック。アプリ一覧ではない） |
| `/api/v1/apps` など | `401 {"error":"Invalid or missing API key"}` |
| `/dashboard/explore` など | ページは 200 だが、中身はログイン後。RSC にアプリ一覧は入っていない |
| 無料プラン | JS 上の `PLAN_TIERS.free`: ads / creators / videos / screenshots がすべて false、`apiCreditsMonthly: 0`、キーワード・ASO・レビュー枠も 0。ライブの勝者一覧は取れない |
| Pro | 公開料金ページとスキーマ: **$79/月**、年払い **$588/年**（ページメタは Offer Pro price 79 USD）。5,000 API credits/月。自己サービスで買えるのは Pro |
| トライアル | クライアントフラグ `TRIALS_ENABLED` は **false**。`TRIAL_PERIOD_DAYS` は 7。オンでもチェックアウトはカード確認（「different card to start your free trial」）。カードは使わない |
| サインアップ | しなかった。メールだけの無料枠では中身が取れず、トライアルはカードが要るため |

結論: 公開ページとドキュメントには届く。ライブのフィルター済み勝者一覧、オンボーディング全画面、広告ライブラリ、キーワードは、有料壁の向こうにある。この回の AppKittie 数値は、公開マーケティングページに出ていた文字列に限る。

### この回、AppKittie 公開ページに出ていたもの

詳細とストア側の解体は `APP-WINNERS.md` に書いた。ここはスナップショットだけ。

アファメーションに直接出ていた名前:
- **Stella** — オーガニック枠のラベル「Stella — Manifest method」。売上・DL は **unknown**。ストアは https://apps.apple.com/us/app/stella-manifest-anything/id6757347283

フィルターデモの売上数字（ページ表記のまま）はプレイブックの表を見ること。ニッチに近い候補は **Glam AI $820K（+40%）**（美容寄りの名前、ストアリンクはページになし、ID 未引き）。睡眠・感謝・関係・仏教の名前は、公開デモには出ていなかった。

オンボーディングの公開デモ: Brainrot 33画面、PushScroll、Lightly。コメント「an app making $600K/mo」のオンボーディングを複製、とある（アプリ名なし）。

### この回キューに入れた変更

ライブの PPO `d7ffa0d7` には触っていない。`AB-TEST-RULES.md` に次の2つを追加した（詳細はそちら）:

1. Anicca オンボーディング: I am / Stella の「長い個別クイズ → プラン生成 → ソフトな年額トライアル」の構造（文言は自作）。
2. Anicca プロダクト: Stella / Aya / Innertune の「聞く（個別音声＋朝アラーム）」戦術。未実装をスクショに描かない。

次の回: 公開ページのデモ金額に差分があるか見る。無料のメールオンリー経路が本当に開いたときだけ、アカウントを検討する。
