# aniccaai.com/go/anicca — human clicks (from 2026-11-01 16:25 JST)

Code: Daisuke134/anicca-products 8d2b790ed (apps/landing/netlify/functions/_lib/marketing-go.js). Deployed by GitHub Action "Netlify Deploy (Landing)" run 41284347892 (success).

What changed
- Every hit now records the visitor's real IP (x-nf-client-connection-ip → cf-connecting-ip → x-real-ip → first x-forwarded-for), the user agent, the method and the referrer. PostHog `$ip` is set to the visitor IP (before: Netlify server 52.14.194.6, Columbus).
- Human clicks → PostHog event `app_store_click` (traffic_class=human).
- Everything else → `app_store_click_nonhuman` with traffic_class bot | internal | test and bot_reason (bot_ua, empty_ua, head_request, prefetch, internal_marker, internal_ip, test_ct_or_flag).
- Redirect is unchanged for everyone (302 → apps.apple.com/app/id6755129214?ct=…&pt=93486075&mt=8).
- Own checks: put `AniccaCheck` in the UA, or send header `x-anicca-check: 1`, or use ct starting `test_`, or `&check=1`. Mac mini IP 220.26.108.31 is excluded too (env GO_INTERNAL_IPS overrides). The box IP rotates (104.28.x), so use the marker.
- Netlify turns HEAD into GET before the function runs, so `curl -I` arrives as GET. Use the marker.

Rows from before 16:25 JST 11/01 carry no IP or UA and cannot be classified (prefix_unclassified).

Query (PostHog MCP execute-sql):
select properties.ct ct, countIf(event='app_store_click' and properties.traffic_class='human') human, countIf(properties.traffic_class='bot') bot, countIf(properties.traffic_class in ('internal','test')) own, countIf(properties.traffic_class is null) prefix_unclassified, count() raw from events where event like 'app_store_click%' and properties.source='web_redirect' and timestamp >= '2026-10-30 15:00:00' group by ct order by raw desc

Snapshot 2026-11-01 16:28 JST (since 10/31 00:00 JST): human 0, bot 2 (own test hits), own/test 6, before the fix (unclassified) 120 real-ct + 4 test-ct.
| ct | human | bot | unclassified before the fix |
|-|-|-|-|
| mastodon_aniccaapp_bio | 0 | 0 | 41 |
| mastodon_anicca_affirm_bio | 0 | 0 | 24 |
| instagram_ani.cca1234_bio | 0 | 0 | 14 |
| instagram_anicca.en_bio | 0 | 0 | 10 |
| instagram_anicca.ios.jp_bio | 0 | 0 | 9 |
| instagram_anicca.jp.videos_bio | 0 | 0 | 8 |
| youtube_anicca-ai_bio | 0 | 0 | 5 |
| bluesky_aniccaapp_bio / bluesky_anicca-affirm_bio / tumblr_dailyanicca_bio | 0 | 0 | 3 each |
| tiktok_anicca.jp_bio / tiktok_aniccaen2_bio | 0 | 0 | 1 each |
- 2026-11-01 22:05 JST /lm/guide per-ct views: in PostHog count event lm_guide_view grouped by properties.ct (human visits only; ct=none means no ?ct=). Internal/test/bot loads are lm_guide_view_nonhuman — exclude them. Live since commit 77445ae3.
