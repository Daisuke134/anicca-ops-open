# Subscriptions audit — 2026-11-14 23:20 JST (Asia/Tokyo)

Discovery only. Nothing was cancelled, downgraded, or purchased in this pass. Parent will drive cancellations in the browser.

Owner rule (成田さん 2026-11-14 23:03 JST, t3967u): keep only **ChatGPT**, **Muse**, and **Grok / Grok Bot**. Everything else is waste unless flagged NEEDS-JUDGMENT. Grok Bot runs on Cursor, so Cursor is flagged KEEP rather than cancel.

Amounts, dates, and statuses below come from sources opened tonight, not from memory. A prior team file is cited only when a fresh search did not re-open that body, and that is marked.

## Sources opened tonight

| Source | Result |
|---|---|
| Agentmail `[redacted-email]` (also listed: `anicca.affirm@`, `pdfinsight.app@`) | Search for receipt/invoice/subscription/payment after 2026-08-14: **0 messages**. Same finding as earlier team notes: team inboxes do not receive billing mail. |
| Postiz connectors `user-Postiz---3` / `---2` | No plan or billing tool is exposed. Postiz is still sending live “post published” mail through 2026-11-14 21:48 JST, so the paid cloud plan is still active. |
| Repo | `credentials.json` (service names only), `team/cfo/expenses.json` (as_of snapshot + Oct/Nov charges), `team/finance/SUBSCRIPTIONS.md`, `team/finance/COST-CUTS.md`, `team/research/SUBSCRIPTION-AUDIT-2026-11-11.md`, `team/research/GROK-COST-SAVING.md`, `team/COSTS.md`, `team/BUSINESS-STREAMS.md`, `team/cfo/history.csv`. |


## Decision table

Times below are Asia/Tokyo. “Next renewal” is taken from a receipt or provider email when it says so; otherwise it is the last charge plus one cycle, marked *expected*.

### KEEP

| Service | Plan | Amount | Cycle | Latest charge | Next renewal | Pays with | Source | Cancel / billing URL | Login (credentials.json key only) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|

### CANCEL

| Service | Plan | Amount | Cycle | Latest charge | Next renewal | Pays with | Source | Cancel / billing URL | Login (credentials.json key only) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| Sunflower Plus (Apple, 断薬日数カウンター) | annual | ¥6,000 | yearly | — | expiry notice: ended 2026-11-11 | Apple | 1a1806f4ae60d8f4 | https://apps.apple.com/account/subscriptions | `apple-app-store` | **Let it stay expired.** Today is past 11/11; no renewal receipt found. |
| Grok Bot Pro (Apple) | monthly ¥4,000 | refunded | cancelled 2026-10-16, replaced by X Super | 2026-10-09; refund −¥3,221 | none | Apple / ••7873 | 1a12124cf9c37d89, refund 1a143ef1d6c24c00 | already cancelled | `apple-app-store` | **Already ended.** Replaced by the KEEP Grok bundle. |

### NEEDS-JUDGMENT

| Service | Plan | Amount | Cycle | Latest charge | Next renewal | Pays with | Source | Cancel / billing URL | Login (credentials.json key only) | Reason |
|---|---|---|---|---|---|---|---|---|---|---|
| Apple Developer Program | membership | ¥12,980 paid 2026-06-01 (net ¥11,800 + tax ¥1,180), valid 2026-06-02 through 2027-06-02 | yearly | 2026-06-01 (outside the 3-month mail window; prior Gmail receipt MC75953903 / order W1442003095, cited in SUBSCRIPTIONS.md) | membership valid through 2027-06-02; next charge not seen | payment method not re-opened tonight | team/finance/SUBSCRIPTIONS.md (June receipt). No new Apple Developer invoice in the last 3 months | https://developer.apple.com/account/membership | `apple-app-store`, `apple-app-store-connect-api`, `asc` | **NEEDS-JUDGMENT.** Required to keep iOS apps on the App Store and take that revenue. Do not cancel casually. |
| Zoho Workplace Mail 10GB | Mail 10GB, 1 user ([redacted-email]) | ¥1,980/year (¥1,800 + ¥180 tax), invoice 11141950 | yearly | 2026-01-09 | *expected* 2027-01-09 | card on file (earlier team note: expires 11/2026, same ••2838 family) | Zoho Store 19ba2c189d2980f2; invoice mail 19ba2cc9265a333d. A `from:zoho.com` search missed these because the senders are `@zoho.jp` / `@zohostore.jp` | Zoho Store / https://store.zoho.jp | (Zoho login; no exact key spotted) | **NEEDS-JUDGMENT.** This is the company mailbox, not a token plan. Closing it drops [redacted-email]. |

## One-off / not a subscription (listed so they are not mistaken for monthly plans)

| Item | Amount | Date | Source | Note |
|---|---|---|---|---|
| FANY tickets | one-off comedy tickets, prior team note | Oct | COST-CUTS.md | Not recurring. |
| LAUNCH $10 | 2026-09-24 | expenses.json 1a0d3c9a518ae091 | One-off. |

## Unbilled in the last 3 months (free tier, another inbox, or already zero)


These are **not** proven active paid subscriptions. Open each billing page on the cancel pass if a card is still on file. Credentials exist for many of them (`netlify-anicca-existing-deployment`, `supabase-life-manager-production`, `apify`, `agentmail`, `revenuecat-dashboard`, `aws-root-life-manager-cloud`, etc.).

## What /open and expenses.json already showed for 2026-10

Every provider in `team/cfo/expenses.json` was included above. The October observed-payment subset there is ¥149,729 and is explicitly not a complete company total. November charges found tonight that post-date that file’s Nov subset (which only had the 11/01 Upwork ¥2,000) include: Google Cloud ¥44,298, U-NEXT ¥2,189, OpenRouter ¥8,621, Relixir ¥3,257 + ¥3,271, Maritime ¥3,268, HeyGen API ¥1,634, LinkedIn Career ¥1,990, Power Plan ¥3,499, and トリファ ¥3,640.

## Gaps (do not invent)

- ChatGPT billing page was not opened, so the three October OpenAI debits are not mapped to named plans, and the missing 11/02 Pro debit is unexplained.
- Railway, Hetzner, and DigitalOcean consoles were not opened tonight.
- 三井住友 Vpass sent payment-amount notices (2026-08-26, 09-26, 10-28) but the envelope does not itemize merchants; Apple Pay charges on ••7873 were taken from Apple receipts instead.
- Link spend history is empty, so Link cannot confirm or deny any recurring merchant.

## Suggested cancel order for the browser pass (not done)

1. U-NEXT trial (before ~2026-12-02).  
2. Postiz (before 2026-11-25).  
3. Apple: LinkedIn Premium Career, Power Plan (before ~2026-12-07). Confirm HeyGen Creator and Sunflower are already ending.  
4. Turn off auto top-up: OpenRouter, HeyGen API, Relixir, Maritime, Telnyx.  
5. Hetzner / DigitalOcean if consoles are empty.  
6. Then the NEEDS-JUDGMENT rows, one at a time, starting with X Premium (Article access) and Railway (live services).

No subscription was changed in this pass.
