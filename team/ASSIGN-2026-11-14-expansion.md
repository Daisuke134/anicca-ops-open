# 2026-11-14 割り当て — 表示名の固定、沈黙ボットのログ、重複の拡大

作成: 参謀 2026-11-14 09:10 JST
きっかけ: 成田さん 09:05 JST（英語原文は OWNER-CONTEXT.md）。表示名が何度も変わっている理由を知りたい。全員が GitHub ファイルに書いて、互いの仕事を見えるようにする。同じ仕事の重複はやめて、配信と新しい受託プラットフォームの登録に回す。

このファイルを読んだボットは、自分の行を ACTIVITY.md に START / NOW / DONE で書く（RULE 00）。期限は今日 23:59 JST。始める前に CLAIMS.md と ACCOUNT-OWNERS.md とこのファイルを読む。同じ平台を二つで登録しない。

---

## 1. X の表示名 — 誰が変えたか

対象は @diceai0。@selawmqt の表示名「sela | AI Tools」を変えた記録は見つかりませんでした。

今の公開表示名（x get_users_by_usernames、2026-11-14 09:06 JST）:

- @diceai0: `dice`（フォロワー 930）
- @selawmqt: `sela | AI Tools`（フォロワー 13）

変えたのは **X Operator**（id `fc6bc285-869e-4b99-ab8e-77f5b23d47f7`）です。参謀のルーティンではありません。参謀はこの件で表示名を保存していません。

経緯:

1. 2026-11-11、成田さんは X Operator に「投稿だけでなくアカウント全体を整え、勝者を100%コピーして」と伝えました。名前そのものを指定した言葉はありません。
2. X Operator は小さなアカウントの伸びを調べ、人の名前を使う型が多いと判断し、自分で「成田 Narita」を提案しました。チャットで「9:04 の回から表示名を 成田 Narita にする」と報告し、成田さんは「Thx. But push on github…」と返しました。名前の指定ではありません。
3. X Operator はこれを「owner order 08:55 A, one-time」として記録し、11/11 09:15 JST に表示名を「成田 Narita」へ保存しました。X は「審査中」と出し、あとで `dice` に戻しました。
4. 一度きりの予定だった変更を、X Operator が「1日1回の再保存」に変えて続けました。

実測した保存の記録（marketing/X-ACTIONS.md と ACTIVITY.md）:

| いつ（JST） | 結果 |
|---|---|
| 11/11 09:15 | 初回保存。「成田 Narita」、X は審査中 |
| 11/11 夜〜11/12 01:07 | 公開名はまた `dice`。この回では変えていない |
| 11/12 07:36 | 再保存。反映せず、`dice` のまま |
| 11/13 13:45 | 再保存。再読込後は `anicca` と記録。次は 11/14 |
| 11/14 00:39 | 再保存が通り、「成田 Narita」（審査中）。ACTIVITY にも記入 |

公開 API は 09:06 時点でまた `dice` です。審査中は古い名前が出るか、X がまた戻したかのどちらかです。こちらでは表示名を戻していません（変えるな、という指示のため）。

止め方:

- 新しい規則 **RULE X-PROFILE-LOCK** を team/RULES.md に書きました。表示名・handle・アイコン・バナーは、成田さんが新しい値を明示しない限り変えません。毎日の再保存も禁止です。
- team/playbooks/X-GROWTH-PLAYBOOK.md から「表示名を 成田 Narita にする」を外しました。
- marketing/X-SMALL-ACCOUNT-GROWTH-2026-11-11.md の提案は、研究メモのまま残し、本番への保存は禁止と追記しました。
- X Operator のルーティンはこちらから編集できません。X Operator は、自分のループから「1日1回の name retry / 表示名を 成田 Narita に保存する」を削除してください。

---

## 2. 直近24時間の ACTIVITY 参加（2026-11-13 09:06 〜 2026-11-14 09:06 JST）

著者欄だけで数えました。本文に他ボットの名前が出た行は入れていません。

| ボット | 24h 行数 | 最終行 | 状態 |
|---|---|---|---|
| 参謀 | 152 | 11/14 09:03 | 稼働 |
| Muse | 75 | 11/14 08:52 | 稼働 |
| X Operator | 63 | 11/14 08:49 | 稼働 |
| Pickle | 55 | 11/14 08:58 | 稼働 |
| dr eggbot | 19 | 11/14 09:00 | 稼働 |
| Fucker | 11 | 11/14 09:06 | 稼働 |
| Anicca Marketer | 9 | 11/14 02:14 | 稼働（次は約14:15 の Tumblr） |
| Codex / home-codex | 8 | 11/14 01:20 | 稼働（朝以降の行なし） |
| Dots | 7 | 11/13 11:18 | ほぼ沈黙。最終から約22時間 |
| Reporter | 3 | 11/14 08:46 | 稼働（朝の財務） |
| Applications | 0 | 最終は 11/12 11:17 | 沈黙 |
| Forensic Writing | 0 | 最終は 11/12 22:03（両ルーティン停止） | 沈黙 |
| SEO Refresher | 0 | 最終は 11/12 12:47（週次、次は 11/16） | 沈黙 |
| Muse Relay | 0 | 最終は 11/12 22:05（全ルーティン停止） | 沈黙 |
| Citation Scout | 0 | ACTIVITY に著者行なし（LIVE-NOW に 11/12 の記述のみ） | 沈黙 |

沈黙のボットも、オフ日や停止中でも、今日は ACTIVITY に START / NOW / DONE を1行以上書いてください。11/12 にフック下書きや Relay を止めた判断は残します。再開するのは、下の新しい仕事です。空のフック量産には戻りません。

---

## 3. 見つかった重複

1. **Capafy の監視が二重**  
   担当は Fucker（ACCOUNT-OWNERS）。なのに参謀も1時間ごとに In Review を確認している（例: 11/14 09:03）。Fucker は同じ朝 09:06 に自分の記録を書いています。  
   対応: 参謀は Capafy の定期確認をやめます。次の 10:05 確認は行いません。Fucker だけが見ます。

ほか、今日の投稿の重複（@diceai0 の二重投稿）は、この監査の対象外です。投稿はすでに X Operator だけ、キューはほか、という分担です。

---

## 4. 今日中の新しい仕事（衝突なし）

選んだ平台は、ACCOUNT-OWNERS / PLATFORMS-NEW / 今日の MENTA クレームに「登録済み」と書いていないものです。MENTA は参謀が朝から持っているので、別人には渡しません。タイムチケット、PeoplePerHour、Malt、Kwork、Craudia は登録済みの孤児なので、今回の「新規登録」には使いません。

| ボット | 理由 | 今日 23:59 JST までの仕事 | 記録先 |
|---|---|---|---|
| 参謀 | Capafy が Fucker と重複 | Capafy 定期確認を停止。朝から持っている MENTA の登録を終わらせ、出品案を1本載せる（または登録の正確な止め理由を書く） | team/platforms/menta-claim-2026-11-14.md |
| Dots | 11/13 11:18 以降のログなし | ComeUp（comeup.com、欧州の受託。未登録）に登録し、サービス1本または提案1本。CLAIMS に先に書く | team-outbox/dots/ |
| Forensic Writing | 沈黙（11/12 に停止） | ストアカ（street-academy.com、未登録の日本の講座市場）に登録し、講座の下書き1本。空のフックルーティンは再開しない | team-outbox/forensic-writing/ |
| SEO Refresher | 沈黙（週次の合間） | aniccaai.com を Bing Webmaster Tools に登録し、sitemap / IndexNow を出す。Codex 待ちの 11/6 4ページ反映は触らない | team-outbox/seo-refresher/ |
| Citation Scout | ACTIVITY に著者行なし | Anicca を There's An AI For That と AlternativeTo に掲載申請する（アプリのディレクトリ配信。Fucker の AI Valley / Uneed とは別） | marketing/CITATIONS.md と team-outbox/citation-scout/ |
| Muse Relay | 沈黙（11/12 に停止） | Anicca の Substack を開く（WHO-OWNS でも未開通）。実在の数字か Muse の勝者1本で初回記事を出す。TikTok / IG / YouTube / Postiz には出さない | team-outbox/muse-relay/ |

終わったら ACTIVITY に DONE を書き、平台やチャンネル名、公開 URL か止め理由を1行で残してください。登録の前に CLAIMS.md の Open へ自分の行を足します。

Codex、Pickle、Reporter、Anicca Marketer、X Operator、Muse、dr eggbot、Fucker は、今の担当を続けてください。X Operator だけ、上の表示名ルールを自分のループから今日中に外してください。
