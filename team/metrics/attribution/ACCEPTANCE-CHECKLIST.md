# E2E attribution acceptance checklist (dots-one, 2026-10-27 10:3x JST, from official docs)
1. UTM presence alone is not revenue attribution. Apple campaign links (ct/pt/mt) give per-campaign downloads/sales/subscriptions; joining to RevenueCat customer IDs is separate evidence.
2. Apple shows campaign data only after >=24h and when each metric >=5 in the period; first download must be within 24h of link use (last link wins). Hidden != 0.
3. RevenueCat is not an attribution authority. Campaign value / acquisition path / customer ID must match; set attributes before purchase; never pre-fill write-once reserved attributes with "Unknown".
4. Separate trial, first paid, renewal, cancel, expire, refund events; dedupe by event id. Purchases != people; estimated proceeds != payout != profit.
5. Pass evidence = post ID -> campaign -> customer ID -> event join, with records on both sides. Sandbox pass != production pass; observation alone doesn't prove incremental revenue.
Sources: developer.apple.com/help/app-store-connect-analytics/acquisition/campaign-links/ ; revenuecat.com/docs/integrations/attribution (+ getting-started, setup-checklist, webhooks/event-types-and-fields)
Used by: 参謀 Daily E2E attribution routine (15:30 JST).
