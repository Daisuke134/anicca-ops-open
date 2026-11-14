# ASC submit proof — 2026-11-11 11:45 JST (Grok Bot 参謀)

All states below were read back after submit. No app version was submitted.

## Review submission
- id: `6770a9b5-5dc1-407b-be9f-15bc63b819b9`
- submittedDate: 2026-11-11T02:45:45.168Z (11:45:45 JST)
- state: WAITING_FOR_REVIEW
- items: in-app event + 2 custom product page versions + 1 product page optimization experiment
- Anicca 1.9.11 (`26cbce6a-1451-4c09-9402-3dcd24f89636`) = PREPARE_FOR_SUBMISSION
- Honne 1.0.7 (`244979cc-f61b-4a87-8829-ec11bf012a66`) = PREPARE_FOR_SUBMISSION

A prior draft submission `799b8033-9756-4564-8bbb-0ed256fdd053` was canceled (COMPLETE) after the PPO treatment had auto-copied the live first screenshot. The lock-screen treatment was uploaded and moved to position 1, then everything was resubmitted on the id above.

## In-app event
- id: `6833274397`
- reference name: Overthinking Week Nov 2026
- state: WAITING_FOR_REVIEW
- badge: CHALLENGE
- deepLink: `anicca://quote/q003` (required by ASC; q003 = “Every breath moves me closer to my truest self.” in the shipping QuoteProvider)
- schedule: 2026-11-13T15:00:00Z – 2026-11-21T14:59:59Z, 41 territories including USA and JPN
- en-US details: `event-overthinking-week-details-1080x1920-en.png` 1080×1920 COMPLETE (id `c9c00019-2a31-877e-8f2c-a1fadbc9c944`)
- en-US card: existing 1920×1080 COMPLETE (id `a4800019-2a31-877e-8f1e-e04234ea1292`)
- ja details: `event-overthinking-week-details-1080x1920-ja.png` 1080×1920 COMPLETE (id `26000019-2a31-877e-8f1b-f1d0139fb0d9`)
- ja card: `event-overthinking-week-card-1920x1080-ja.png` 1920×1080 COMPLETE (id `09800019-2a31-877e-8f3e-26cf992e2729`)

The previous details asset was 1920×1080, which is the Event Card spec, not the Details Page spec (9:16, min 1080×1920). That was the ASSET_SPEC_MISMATCH.

## Custom Product Pages
- TikTok Lock Screen `f1554a3f-9a77-4945-9ba8-bb8b51a03b0e` / version `3a07f082-db21-407a-9c18-bab728ed949b` / WAITING_FOR_REVIEW
  https://apps.apple.com/us/app/daily-affirmations-anicca/id6755129214?ppid=f1554a3f-9a77-4945-9ba8-bb8b51a03b0e
  https://apps.apple.com/us/app/daily-affirmations-anicca/id6755129214?ppid=62120fb7-874f-439a-ada5-d666d279a752

## Product Page Optimization
- id: `d7ffa0d7-704c-42ef-abf8-588f3bada53e`
- name: Lock Screen first screenshot Nov 2026
- attached to live 1.9.10 `c66f729e-921d-48cf-bd01-ba4b359bc32e`
- trafficProportion: 50
- treatment: `a5376aa3-4b0f-4af7-b1e0-479ace583533` “Lock Screen widget first”, en-US set `8a9884f5-c7a6-4ae0-8c33-27360fbac67a`
- first screenshot: `anicca_en_01_lockscreen.png` 1320×2868, 892,679 bytes, COMPLETE, position 1 (id `52800019-2a31-877e-8030-a5c10d32e157`)
- shots 2–8 reused from the live 6.7" set
- state: WAITING_FOR_REVIEW (reviewRequired true; will not run until Apple approves)

## Honne 1.0.7 en-US
- localization `b3a36fbc-ed91-44b4-ad9e-cacbdc233576`
- first line is now: “Paste any text, DM, or chat and see what they might really mean.”
- remainder of the description was left in place
- version not submitted
