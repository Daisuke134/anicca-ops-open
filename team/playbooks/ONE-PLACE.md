# 情報は1か所 — GitHub ファイルで話す

成田さん 2026-11-14 09:36 JST: 全員が GitHub のファイルで話す。情報は散らさない。全員が読める1か所に置く。

入口はリポジトリ直下の [AGENTS.md](../../AGENTS.md)。規則の要約は [RULES.md の RULE 00](../RULES.md)。

## なぜファイルか（トークン）

直接メッセージ（SendToAgent / 部屋チャット）は、相手をその場で起動する。起動のたびにシステム指示と経緯を読み込むので、依頼本文よりずっと多くのトークンを使う。内容もその会話にしか残らず、他のメンバーには見えない。

Anthropic の公開測定では、エージェント単体は通常チャットの約4倍、複数エージェントの同期連携は約15倍のトークンを使う。計画や大きな成果は会話に詰めず、外部メモリ（ファイル）へ書き、返すのは参照だけでよい、とも書いてある。

- https://www.anthropic.com/engineering/built-multi-agent-research-system
- https://www.anthropic.com/research/multi-agent-research-system

ファイルに書けば1回で全員が読める。相手は次の定期起動で差分だけ読めばよく、今すぐ起こさなくてよい。直接メッセージは、今動かないと壊れるとき（停止・セキュリティ）だけ使う。

## 手順

1. 迷ったら [AGENTS.md](../../AGENTS.md) を開く。ここが地図。
2. 依頼と返信は `team/inbox/<相手>.md` に追記する。毎回の最初に自分の inbox を読む。返信も同じファイルの「返信」欄へ。
3. 着手前に `team/CLAIMS.md` で CLAIM し、`team/ACCOUNT-OWNERS.md` を読む。担当分けは `team/ASSIGN-*.md`。作業の記録は `team/ACTIVITY.md` に1行（START / NOW / DONE / FIX）。
4. Slack #agents-hq は「ファイルを見て」＋コミット URL の1行だけ。部屋や DM に決定を置かない。

## 置く場所

| 役割 | ファイル |
|---|---|
| 入口（地図） | `AGENTS.md` |
| この手順 | `team/playbooks/ONE-PLACE.md` |
| 規則 | `team/RULES.md` |
| 依頼と返信 | `team/inbox/<agent>.md` |
| 所有・着手 | `team/ACCOUNT-OWNERS.md`、`team/CLAIMS.md`、`team/ASSIGN-*.md` |
| 作業ログ（唯一） | `team/ACTIVITY.md` |
| 成田さんの言葉 | `team/OWNER-CONTEXT.md` |
| 応募台帳 | `team/applications/APPLICATIONS.md` |

inbox のファイル名: `applications.md` / `x-operator.md` / `dr-eggbot.md` / `muse.md` / `dots.md` / `codex.md` / `pickle.md` / `seo-refresher.md` / `forensic-writing.md` / `sanbo.md`（参謀）。足りなければ同じ置き方で足す。

## いま散らばっている場所（2026-11-14 の数え）

- `team/` 直下の md が 110。そのうち「ここから読め」と書いてある入口が9つ（`ONBOARDING.md` / `OPERATING.md` / `RULES.md` / `AGENT-PROTOCOL.md` / `TEAM.md` / `playbooks/TEAM-SHARING.md` / `STATUS-SHARING-PLAYBOOK.md` / `COMMS.md` / ルート `README.md`）。ルートに `AGENTS.md` は無かった。
- 会話・ログの置き場が重なっている: `ACTIVITY.md`、`TEAM-FEED.md`、`DAILY-LOG.md`、`LIVE-NOW.md`、`LIVE-STATE.md`、`NOW.md`、`BOARD.md`、`team/inbox/`（当時4ファイル）、`team-outbox/`（約910ファイル）、Slack、部屋 / SendToAgent。
- 担当表も重なっている: `ACCOUNT-OWNERS.md`、`WHO-DOES-WHAT.md`、`WHO-OWNS-WHAT.md`、`OWNERSHIP.md`、`ROLES.md`、`ORG-CHART.md`、`ORG-STRUCTURE.md`。

これからは上の表以外に新しい入口や新しい連絡用ファイルを作らない。

## 移行（古いファイルの扱い）

消さない。証拠と過去の本文は残す。新しい依頼と決定は、上の表にだけ書く。

- **依頼の正本は inbox。** `team-outbox/<from>/to-<to>-*.md` への新規依頼は止める。既存の outbox はアーカイブ。返信の ack も inbox の「返信」欄へ（RULE POST-GATE の投稿ゲート自体は変えない。変わるのは連絡の置き場だけ）。
- **ログの正本は ACTIVITY.md。** `TEAM-FEED.md` は `share.sh` のミラーで、ログの代わりにしない。`DAILY-LOG` / `LIVE-NOW` / `LIVE-STATE` / `NOW` / `BOARD` はスナップショットや過去ログであり、会話の場にしない。
- **入口は AGENTS.md。** `ONBOARDING.md` / `OPERATING.md` / `AGENT-PROTOCOL.md` / `TEAM.md` / `COMMS.md` / `STATUS-SHARING-PLAYBOOK.md` は入口の役目を譲る。担当の正本は `ACCOUNT-OWNERS.md`（ほかの担当表は参照用）。
- 秘密・個人情報はファイルに書かない。パスだけ書く。

## 参考にした実例

- AGENTS.md（コーディングエージェント共通の入口）: https://agents.md/
- Claude Code のプロジェクト記憶（CLAUDE.md / AGENTS.md）: https://code.claude.com/docs/en/memory
- GitLab handbook-first（先に handbook を直し、告知は差分リンクだけ。同じ文を複製しない）: https://handbook.gitlab.com/handbook/company/culture/all-remote/handbook-first/ と https://handbook.gitlab.com/handbook/about/handbook-usage/
- 37signals「Writing solidifies, chat dissolves」（大事なことは長い文で書き、チャットに落とさない）: https://basecamp.com/guides/how-we-communicate
- Beads（git 上のタスクを CLAIM して二重作業を防ぐ）: https://yegge.ai/essays/introducing-beads-a-coding-agent-memory-system/
- foreman（GitHub Issues をエージェントの作業キューにし、CLAIM してから着手）: https://github.com/agent-sh/foreman
