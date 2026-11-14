# E2E 投稿→収益 (2026-10-12〜2026-11-11, 生成 2026-11-11 15:55 JST)

正直な前提: タップ→インストールを投稿単位で結ぶ ct/utm はまだ無い。下の投稿↔インストールは**相関（同時期）であって帰属ではない**。

## 鎖（アプリ別, ASC実数）
ASCは前日分が翌日JST午後に出るため、朝の実行では「昨日」が0/未公開になる。
| 製品 | 新規DL 昨日 | 新規DL 7日 | 課金件数 7日 | 収益(proceeds) 7日 |
|---|---|---|---|---|
| Anicca | 0 | 1.0 | 0.0 | 0.0 |
| Daily Dhamma | 0 | 4.0 | 0 | 0 |
| Honne | 0 | 0 | 0 | 0 |
| STUDIO CHERIE | 0 | 1.0 | 0 | 0 |
| Sleep Reset | 0 | 0 | 0 | 0 |
| Thankful | 0 | 0 | 0 | 0 |
| sub:app.rork.vcinrjbl3ke00f07gtlzf | 0 | 0 | 0 | 0 |

## 投稿・エンゲージメント（アカウント別 7日）
| アカウント | 投稿 | 指標合計 |
|---|---|---|
| @anicca-affirmation-video | 18 | average_view_duration=74, average_view_percentage=71, estimated_minutes_watched=25, subscribers_gained=0, subscribers_lost=0 |
| @anicca-ai | 6 | average_view_percentage=367, average_view_duration=103, estimated_minutes_watched=13, likes=1, subscribers_gained=0 |
| ani.cca1234 | 1 | reach=3 |
| anicca.cemetery | 0 | reach=0 |
| anicca.en | 1 | reach=39 |
| anicca.encards | 1 | reach=1 |
| anicca.he | 17 |  |
| anicca.ios | 1 | reach=1 |
| anicca.ios.jp | 1 | reach=1 |
| anicca.jp | 18 |  |
| anicca.jp.videos | 1 | reach=31 |
| anicca.jp4 | 17 |  |
| anicca.jpx | 17 |  |
| anicca_buddha | 19 |  |
| anicca_slideshow | 17 |  |
| aniccaaffirmation | 24 |  |
| aniccaen2 | 17 |  |
| bluesky/anicca-affirm | 0 |  |
| bluesky/bluesky_anicca | 3 | likes=0, reposts=0, replies=0 |
| bluesky/bluesky_anicca_en | 0 |  |
| bluesky/bluesky_anicca_en (aniccaapp) | 0 |  |
| bluesky/bluesky_lm | 0 |  |
| bluesky/bluesky_lm (lifemanager-jp) | 0 |  |
| bluesky/bluesky_lm_en | 1 | likes=0, reposts=0, replies=0 |
| bluesky/lifemanager-jp | 0 |  |
| bluesky/lm_en | 0 |  |
| daisuke-narita | 21 |  |
| dev.to/aniccaapp | 1 |  |
| devto/aniccaapp | 0 |  |
| diceai0 | 7 |  |
| directory/junkstartups | 3 |  |
| everfocus-labs | 1 | clicks=1, engagement=0, page_views=0, shares=0, comments=0 |
| honne_reveal | 17 |  |
| honnevideo | 17 |  |
| instagram/obou.anicca | 1 |  |
| linkedin/Daisuke Narita | 1 |  |
| mastodon/mastodon_anicca | 2 | likes=0, reposts=0, replies=0 |
| mastodon/mastodon_anicca_en | 0 |  |
| mastodon/mastodon_lm | 0 |  |
| monk.mujo | 2 | reach=663 |
| monk_anicca | 14 |  |
| nostr/anicca | 3 |  |
| nostr/anicca npub1jtay | 0 |  |
| nostr/anicca_npub | 0 |  |
| nostr/npub1jtay3qxp | 0 |  |
| note/saqwd | 1 |  |
| obou.anicca | 4 | reach=6 |
| obou_anicca | 16 |  |
| selawmqt | 1 |  |
| telegraph/Daisuke Narita | 0 |  |
| telegraph/anicca-telegraph | 0 |  |
| tiktok+ig/obou_anicca/obou.anicca | 1 |  |
| tiktok/@aniccaaffirmation (Postiz Affirmation Girl) | 0 |  |
| tiktok/obou_anicca | 2 | impr_24h=0 |
| tumblr/dailyanicca | 3 |  |
| x/@diceai0 | 0 |  |
| x/@selawmqt | 0 |  |
| x/diceai0 | 16 | impr_24h=150, likes=29, reposts=11, replies=3, follows=0 |
| x/selawmqt | 1 |  |

## タップ（PostHog utm/ct, connector-pulls）
- 2026-11-01 app_store_click/mastodon_aniccaapp_bio taps=41 server-side capture from US/Columbus (16 IPs, new person per tap): likely link-preview/self-check bots, not proven human (pulled 11/1 15:5x)
- 2026-11-01 app_store_click/mastodon_aniccaapp_bio taps=41 ct=mastodon_aniccaapp_bio; install events still lack ct/utm so post-level attribution correlation only; (pulled 11/6 15:30 JST)
- 2026-11-01 app_store_click/mastodon_aniccaapp_bio taps=41 ct=mastodon_aniccaapp_bio; install events still lack ct/utm so post-level attribution correlation only; (pulled 2026-11-10 15:41 JST)
- 2026-11-01 app_store_click/mastodon_aniccaapp_bio taps=41 ct=mastodon_aniccaapp_bio; install events still lack ct/utm so post-level attribution correlation only; (pulled 2026-11-11 15:35 JST)
- 2026-11-01 app_store_click/mastodon_anicca_affirm_bio taps=24 server-side capture from US/Columbus (16 IPs, new person per tap): likely link-preview/self-check bots, not proven human (pulled 11/1 15:5x)
- 2026-11-01 app_store_click/mastodon_anicca_affirm_bio taps=24 ct=mastodon_anicca_affirm_bio; install events still lack ct/utm so post-level attribution correlation only; (pulled 11/6 15:30 JST)
- 2026-11-01 app_store_click/mastodon_anicca_affirm_bio taps=24 ct=mastodon_anicca_affirm_bio; install events still lack ct/utm so post-level attribution correlation only; (pulled 2026-11-10 15:41 JST)
- 2026-11-01 app_store_click/mastodon_anicca_affirm_bio taps=24 ct=mastodon_anicca_affirm_bio; install events still lack ct/utm so post-level attribution correlation only; (pulled 2026-11-11 15:35 JST)
- 2026-11-01 app_store_click/instagram_ani.cca1234_bio taps=14 server-side capture from US/Columbus (16 IPs, new person per tap): likely link-preview/self-check bots, not proven human (pulled 11/1 15:5x)
- 2026-11-01 app_store_click/instagram_ani.cca1234_bio taps=14 ct=instagram_ani.cca1234_bio; install events still lack ct/utm so post-level attribution correlation only; (pulled 11/6 15:30 JST)
- 2026-11-01 app_store_click/instagram_ani.cca1234_bio taps=14 ct=instagram_ani.cca1234_bio; install events still lack ct/utm so post-level attribution correlation only; (pulled 2026-11-10 15:41 JST)
- 2026-11-01 app_store_click/instagram_ani.cca1234_bio taps=14 ct=instagram_ani.cca1234_bio; install events still lack ct/utm so post-level attribution correlation only; (pulled 2026-11-11 15:35 JST)
- 2026-11-01 app_store_click/instagram_anicca.en_bio taps=10 server-side capture from US/Columbus (16 IPs, new person per tap): likely link-preview/self-check bots, not proven human (pulled 11/1 15:5x)
- 2026-11-01 app_store_click/instagram_anicca.en_bio taps=10 ct=instagram_anicca.en_bio; install events still lack ct/utm so post-level attribution correlation only; (pulled 11/6 15:30 JST)
- 2026-11-01 app_store_click/instagram_anicca.en_bio taps=10 ct=instagram_anicca.en_bio; install events still lack ct/utm so post-level attribution correlation only; (pulled 2026-11-10 15:41 JST)

## 変更→前後比較（before/after 比較であり証明ではない; Anicca新規DL）
| 日時 | 製品 | 種別 | 内容 | 前7日DL | 後DL(〜7日) |
|---|---|---|---|---|---|
| 2026-11-02 18:56 | ? | listing | - 2026-11-02 18:56 JST｜dr eggbot｜WINNERS #16 反映済み（4302213のみ）｜https://c | 4.0 | 0 (7日) |
| 2026-11-02 19:00 | ? | listing | - 2026-11-02 19:00 JST｜dr eggbot｜WINNERS #16 反映済み（全AI出品9件）｜4302213に加え  | 4.0 | 0 (7日) |
| 2026-11-03 08:46 | ? | SEO | - 2026-11-03 08:46 JST｜Reporter｜追跡 Apify/RapidAPI/SEO/iOS｜done｜Apify u | 3.0 | 1.0 (7日) |
| 2026-11-07  | Honne | pricing | - 2026-11-07 09:0x JST｜参謀｜Honne product loop｜done｜RC 7d new4/trials0/M | 1.0 | 1.0 (4日) |
| 2026-11-07 02:12 | ? | ASO | - 2026-11-07 02:12 JST｜Muse Relay｜source 7699801497952898324 X変稿の公開照合｜ | 1.0 | 1.0 (4日) |
| 2026-11-07 02:52 | ? | SEO | - 2026-11-07 02:52 JST｜Muse Relay｜既存source 7699801497952898324の初回note横 | 1.0 | 1.0 (4日) |
| 2026-11-07 08:39 | Anicca | SEO | - 2026-11-07 08:39 JST｜Reporter｜08:30 finance daily｜done｜RC 21proj再取得  | 1.0 | 1.0 (4日) |
| 2026-11-07 10:45 | Anicca | SEO | - 2026-11-07 10:45 JST｜参謀｜Team revenue loop｜shipped｜Birdfury CLAIM htt | 1.0 | 1.0 (4日) |
| 2026-11-10  | ? | listing | - 2026-11-10 04:4x JST｜参謀｜Team revenue loop｜checked｜Gmail 24h: 入金・新規受注 | 1.0 | 0 (1日) |
| 2026-11-10  | PromptBase | listing | - 2026-11-10 06:4x JST｜参謀｜Team revenue loop｜checked｜Gmail 3h: 入金・新規受注・ | 1.0 | 0 (1日) |
| 2026-11-10  | Anicca | listing | - 2026-11-10 12:4x JST｜参謀｜Team revenue loop｜checked｜Gmail 3h: 入金なし。Pro | 1.0 | 0 (1日) |
| 2026-11-10 08:42 | Anicca | SEO | - 2026-11-10 08:42 JST｜Reporter｜08:30 finance daily｜done｜RC 21proj再取得  | 1.0 | 0 (1日) |
| 2026-11-10 21:25 | ? | channel | - 2026-11-10 21:25 JST｜Reporter｜連絡方針切替受領｜done｜bot間DM停止、Reporter結果はBOAR | 1.0 | 0 (1日) |
| 2026-11-10 22:17 | Anicca | ASO | - 2026-11-10 22:17 JST｜Grok Bot 参謀｜現実把握＋X勝者調査｜done｜research/REALITY-AN | 1.0 | 0 (1日) |
| 2026-11-10 22:57 | Anicca | ASO | - 2026-11-10 22:57 JST｜Anicca Marketer｜Anicca ASO promo text｜done｜en-U | 1.0 | 0 (1日) |
| 2026-11-10 23:00 | Anicca | ASO | - 2026-11-10 23:00 JST｜Grok Bot 参謀｜Grok Bot X winners → affirmation ap | 1.0 | 0 (1日) |
| 2026-11-11  | ? | release | - 2026-11-11 10:4x JST｜参謀｜Team revenue loop｜checked｜Gmail 2h: 入金なし。Cro | 1.0 | 0 (0日) |
| 2026-11-11 08:45 | Anicca | release | - 2026-11-11 08:45 JST｜Reporter｜08:30 finance daily｜done｜RC 21proj再取得  | 1.0 | 0 (0日) |
| 2026-11-11 12:49 | ? | pricing | - 2026-11-11 12:49 JST｜dr eggbot｜coconala-lancers-loop｜done｜box_mem_ga | 1.0 | 0 (0日) |
| 2026-11-06 17:41 | Capafy | draft | Fucker: corrected Storytime scope/listing draft source and local ZIP o | 1.0 | 1.0 (5日) |
| 2026-11-07 02:36 | Capafy | package | Fucker: prepared Shorts Hook Lab 9466718786 0be20 host-key + GAP#5 tag | 1.0 | 1.0 (4日) |
| 2026-11-07 09:05 | Capafy | after-read | Fucker: conversion after-read catch-up; store CVR unknown (no seller s | 1.0 | 1.0 (4日) |
| 2026-11-07 09:05 | Capafy | listing | Fucker: HANDED TO PARENT browser runbook for 7785270416 Data Analyst C | 1.0 | 1.0 (4日) |
| 2026-11-07 09:14 | Capafy | listing | Fucker: 7785270416 v1.0.3 submitted In Review (not approved): buyer-qu | 1.0 | 1.0 (4日) |

※前日比は範囲内データのみ。範囲外は空=0扱いになるので 30日で回すと正確（`e2e.py 開始 終了`）。

## GAP
