# 海外面（英・西）フリースロット台帳 — 2026-11-18 実測（pickle）

「応募できるのに応募していない」を無くすための台帳。各面の**無料で応募できる上限**と**現在のゲート**を、
その日の実測（ログイン→送信画面→確認画面）で毎回上書きする。数字は JST。

## 1. 無料スロットのある面

| 面 | 無料枠 | 2026-11-18 の実測 | 次の1件を撃つタイミング |
|---|---|---|---|
| Twine | 1応募/日（日本時間 09:40 頃回復） | 復活を確認し **1件送信**（Anti-Cheat System $5,000 見積・awaiting review）。送信後は 0/1 | 翌日 09:40 以降に1件。Twineは「顔出し・声」案件が大半なので、**開発/制作系のネイティブ案件が出た日**に使う |
| Upwork | Connects 従量（残1） | ログイン可・メッセージ4room 全て返信なし・`q=Japanese` は音声収録案件が大半。**Connects 1 では提案不可** | Connects 回復（月次10）or 招待案件（招待は Connects 無料） |
| Microworkers | タスク従量（無料） | ログイン可。**Translation 0件 / Transcription 0件 / Annotation 0件**。残りは「他サイトのアカウント作成」型スパムと「請求書PDFをアップロード」型（個人書類の提出＝不可） | 週1でカテゴリだけ見る。安全タスクが出た日だけ実施 |
| Truelancer | 無料ユーザーの入札枠 | **新規登録＋メール認証完了**（[redacted-email]、無料ユーザー継続・$1 Pro trialは未課金）。`/freelance-translation-jobs` はヒンディー/ウルドゥー/ロシア/マラヤーラム語のみ・各100〜270提案で**日本語案件0** | プロフィール（/onboarding/profile）を作り、日本語/AI案件が出た日の入札に回す |
| DataAnnotation | 在庫従量 | ログイン可（Daisuke Narita）。**「We do not have any open projects to assign you at the moment」**＝割当0件（前日と同じ） | メール通知待ち・週1確認 |

## 2. 課金しないと撃てない面（支出判断＝本人へ）

| 面 | ゲート | 実測 |
|---|---|---|
| Contra | Pro $17/月（年払い） | Free は全110件中3件のみ表示・3件とも応募済。`/jobs` は「No matched or recommended jobs right now」。Messages 0件。Services 9本は PUBLISHED のまま |
| PeoplePerHour | 提案クレジット（15/25 per month） | サインアップ〜「Application complete」までは無料で到達。**提案送信だけが有料**。「Continue to payment」のみ |
| Freelancer.com | 入札 0/6（無料枠枯渇） | 変更なし |

## 3. 資格要件で閉じている面（待ち）

| 面 | 状態 |
|---|---|
| Welo Data | アセスメント3本 Complete。**ja-JP の Opportunity は 0件**（デンマーク語1件のみ） |
| TELUS Digital | Quality Assurance Rater - Japanese 応募済（applicationId 55611010）。研修/試験案内メール待ち |
| Translated / DataAnnotation / Alignerr | 登録済・在庫待ち（Alignerr はカメラ面接が残） |

## 4. 人間工程で不可（触らない）

- **Alignerr**: Google SSOのみ・カメラ面接が残 → この席からは着手しない（正本の指示どおり）。
- **Prolific / Babel Audio / Chorus / Go With Guide**: 顔・声・現地対面が本質。
- **Fiverr**: press-and-hold hCaptcha で停止（既存セッション必須）。

## 5. 提案の型（この面で通す型）

1. **4分割で書く**: ①データ/入力の設計 ②判定ロジック ③人が確認する運用（監査ログ・異議申し立て） ④テストと文書。
2. **最初の小さな有償マイルストーンを自分から提案**（例: 5日スパイク）→ 発注者の判断コストを下げる。
3. **見積額は先方レンジの上限を1つ選び、「レンジ上限・最終額はクライアントと合意」と明記**（Twine の fee はコミットではない）。
4. **日本語ネイティブ × ソフトウェア**を1行で言い切る（"Tokyo-based, native Japanese, MS in information science (NAIST)"）。
5. 送信後は**確認画面の文言をそのまま記録**（"Your application has been sent" 等）。「押した」ではなく「そう表示された」を証拠にする。
