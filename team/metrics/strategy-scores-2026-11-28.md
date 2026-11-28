# 配信戦略スコア 2026-11-28 09:45 JST（参謀・日次スナップショット）
出典: accounts-snapshot-2026-11-28.json（Postiz public API /integrations /posts /analytics、YouTube は /analytics/post/{id}）、x-users.json と x/diceai0-originals-7d-2026-11-28.json（X API v2、09:33–09:35 JST）、seo-daily.csv（GSC、09:40 JST 読み取り）、capafy-conversion-log.csv（09:00 after-read）、ACTIVITY.md の 11/21 以降の DONE/SHARE 行。
前日比の基準は accounts-snapshot-2026-11-24.json（11/25–27 のスナップショットはない）、前週比の基準は accounts-snapshot-2026-11-21.json。

| 戦略 | 担当 | 7日の出力 | 7日の結果 | 前週比 | 判定 |
|---|---|---|---|---|---|
| X @diceai0 | X Operator | 116本（11/25 以降は 9/1/9/4 本/日） | 表示 27,260、フォロワー 1,582 | 表示 -2,653（29,913→）、フォロワー +257 | 修正。本数が 11/25 から激減し日次表示 7,626→153–1,112。勝者 https://x.com/i/status/2126311625401721081 （毎日投稿で 5,000→9,600）。同文の二重投稿4組（11/21–24） |
| X @selawmqt | X Operator | 0本（最終 11/17） | 表示 0、フォロワー 12 | 表示 -10 | 停止（X Operator が ACCOUNT-OWNERS に判断を書く） |
| TikTok 短尺（12垢合計） | OpenCode（11/27 Muse から移管、backup 参謀） | 202本（予約 0、失敗 32） | 再生 75,694 | -6,143（81,837→） | 修正。予約が全垢0で 11/27 以降ほぼ停止。勝者 https://x.com/starter_story/status/2116623432377086285 （Flame、15–20垢で毎日投稿） |
| TikTok @obou_anicca / @anicca_buddha / @aniccaaffirmation | OpenCode | 21 / 27 / 26本 | 9,191 / 8,294 / 8,407 | +4,614 / +3,123 / +2,547 | 倍増。@obou_anicca は Postiz で無効化中 → 再有効化（止めない） |
| TikTok @anicca.jp4 / @honnevideo | OpenCode | 26 / 25本 | 8,166 / 4,271 | -6,647 / -6,585 | 修正（キャプション使い回し・失敗投稿） |
| Instagram リール（9垢） | Muse | 0本（全 integration 無効） | 再生 205 | -133 | 修正。勝者 https://x.com/ky_markets/status/2115449713587593646 （同じキャラ・同じ動画を4媒体へ） |
| YouTube Shorts（@anicca-ai ほか） | 参謀 | 4本（予約 0、11/21 にアップロード上限エラー1） | 再生 3（投稿別 Views 合計） | 計測開始のため比較なし | 修正。勝者 https://x.com/iRetinaPro/status/2121302322751959099 （Shorts 1k再生→インストール、動画内で App Store 検索語を言う） |
| LinkedIn 個人 | Muse | 24本（失敗2、同文の失敗→再投稿1） | 反応は Postiz で取れない | — | 計測を直すまで継続 |
| SEO（aniccaai.com） | 参謀 | — | GSC 11/17–23 クリック 31・表示 3,389（11/24–26 は GSC 未反映で0） | クリック +12（19→）、表示 +1,518（1,871→） | 倍増 |
| AEO（AI回答への引用） | 参謀 | 出荷行0 | 計測ファイルなし | — | 計測を作るまで判定しない |
| ディレクトリ掲載（x402 系ほか） | 参謀 | 5件（x402dash 8/8 など） | 流入計測なし | — | 継続（ct を付けて計測） |
| Reddit | 担当未定 | 0件 | — | — | 停止 |
| ニュースレター（Substack 2誌 + ¥980/月 Stripe） | 参謀 / @pickle | Substack 0本（最終 10/24）、Stripe 価格作成 11/28 | 購読者数は未計測 | — | Substack は停止。有料版は @diceai0 経由で計測開始 |
| アフィリエイト・UGC | 参謀（executor） | Grade / Collabstr 登録（11/27） | 成果0（開始直後） | — | 継続（成果報酬のみ） |
| クロスポスト（Bluesky・Mastodon・Nostr・Telegraph の Anicca 垢） | Anicca Marketer / 参謀 | 0本（Telegraph は Fucker の Honne ページ別計測） | いいね0 | 0 | 停止 |
| Tumblr @dailyanicca | Anicca Marketer | 6本 | 表示は公開APIなし（ct で計測） | — | 継続（ct タップで判定） |
| Life Manager 垢（Bluesky・Mastodon）・note・dev.to・@Manageraqo | 参謀 | 0本 | いいね0 | 0 | 停止。計測だけ続ける |
| Capafy（ストア） | 参謀 | — | salesVolume 3,179（7日 +107） | 前週の5日で +131 → 伸びが鈍化 | 継続 |

## 読めなかった数字
- Threads: box に読取経路なし（Postiz に threads integration なし、muse.json は 11/12 内容で古い）。
- PromptBase: gig-metrics.csv の最終検証が 10/26（views n/a）。
- note @anicca123: API は follower と記事数だけで閲覧数なし。
