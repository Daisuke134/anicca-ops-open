# ASC rejections audit — 2026-10-31 (read-only, Codex)

| App | App ID | Version | State | releaseType | Last submission (JST) | Source (Mac mini) |
|---|---|---|---|---|---|---|
| Aura Looks | 6763930574 | 1.0.0 | REJECTED (sub cc812367 UNRESOLVED_ISSUES) | AFTER_APPROVAL | 2026-05-01 18:30 | ~/anicca-project/mobile-apps/rork-lookmax-pro/ios (AuraLooksScore) |
| Chi Daily | 6759994539 | 1.0 | REJECTED (sub 0b529110 UNRESOLVED_ISSUES) | AFTER_APPROVAL | 2026-04-16 11:42 | ~/anicca-project/mobile-apps/20260304-105016-app/ChiDailyios |
| FrostDip | 6760225278 | 1.0 | REJECTED (sub 7b96c39a UNRESOLVED_ISSUES) | AFTER_APPROVAL | 2026-04-16 11:31 | ~/anicca-project/mobile-apps/20260307-223953-app/FrostDipios |
| Zone2Daily | 6760271560 | 1.0 | REJECTED (sub 2b277328 UNRESOLVED_ISSUES) | AFTER_APPROVAL | 2026-04-16 11:26 | ~/anicca-project/mobile-apps/20260309-070017-app/zone2dailyios |
| Eye Break | 6760196743 | 1.0 | REJECTED (sub 1c891c85 UNRESOLVED_ISSUES) | AFTER_APPROVAL | 2026-04-16 11:37 | ~/anicca-project/mobile-apps/20260307-002214-app/EyeBreakIslandios |
| SleepRitual | 6759916261 | 1.0 | DEVELOPER_REJECTED (no review submission on record) | AFTER_APPROVAL | none | NOT FOUND (no com.anicca.sleepritual pbxproj under mobile-apps) |
| Daily Affirmations | 6755129214 | 1.9.6 | WAITING_FOR_REVIEW (sub 39f7baec, submitted 10-30 10:36) | AFTER_APPROVAL ✅ | — | ~/anicca-project (aniccaios) |

## Rejection reasons
The public ASC API does NOT expose Resolution Center message text or guideline numbers (reviewSubmissionItems only return state=REJECTED). No saved rejection notes were found in the Mac mini project folders. Reason text is only visible in the ASC web UI (App Review > Resolution Center) — requires a human-session login.

## Proposed fix plan (pending reasons)
1. Read each Resolution Center message in ASC web UI (blocker: login).
2. Per guideline: 2.1 → reviewer notes/demo path + IAP attached; 4.3 spam/template → differentiate or drop; 3.1.2 subscriptions → paywall terms/EULA/privacy links; 5.1.1 → account deletion/permissions copy; 2.3 metadata → screenshots/description.
3. SleepRitual: developer-rejected, never reviewed; locate source first (possibly a different repo/prefix) before any resubmit.
4. Note: 4 Factory apps were rejected together on 04-16 — likely the same template-wide reason (4.3 design spam is a strong suspect); confirm before rewriting.

## Rejection reasons (from Apple emails, read 2026-10-31 JST)

**Standard IAP-bug Next Steps (Apple's text, the same in every "2.1(b) IAP bugs" item below):** "Apple reviews In-App Purchase products in the sandbox and the In-App Purchase products do not need prior approval to function in review. Review the product configurations, complete any missing information, and test them in the sandbox. To offer In-App Purchases in the app, the Account Holder must also accept the Paid Apps Agreement in the Business section of App Store Connect. Confirm you have a Paid Apps Agreement in effect."
**Standard "IAP not submitted" Next Steps:** "Submit your In-App Purchases and upload a new binary in App Store Connect so we can proceed with our review. Note you must provide an App Review screenshot in App Store Connect in order to submit In-App Purchases for review."

### Aura Looks (latest: msg 19e178d59ab551cd)
- Submission ID cc812367-ca71-4d7b-ae3b-a82171eb0265. Submitted May 1, 2026 02:30 PDT. Reviewed May 11, 2026 (resubmission). Device: iPad Air 11-inch (M3), iPadOS 26.4.2. Version 1.0.0 (8).
- **Guideline 2.1(b) - Performance - App Completeness**
  - Issue: "The In-App Purchase products in the app exhibited one or more bugs which create a poor user experience. Specifically, after closing subscription page (without purchase), we could not find the subscription page again. The in-app purchases/subscriptions do not need to have been previously approved to confirm they function correctly in review."
  - Next Steps: standard IAP-bug text.
- Older rejection (msg 19dd40c7003a3b12, app then named "Aura Looks Score"): submission 29c98011-569a-450a-9087-81eee260fc6b, reviewed Apr 28, 2026, iPad Air 11-inch (M3), 1.0.0 (1).
  - 2.1(b): the IAP products had not been submitted for review.
  - **5.6 Developer Code of Conduct:** "The app attempts to manipulate customers into making unwanted In-App Purchases." Next Steps: revise the app to comply, then resubmit.
  - 2.1(b) IAP bug: tapping purchase returned the reviewer to the purchase screen. No purchase went through and nothing was unlocked.
- **Likely fix:** add an always-visible way to reopen the paywall after it is dismissed (for example an Upgrade/Premium button in the main UI or Settings), and test this in the sandbox. Keep the 5.6 fixes in place (no manipulative paywall) and confirm purchases unlock content.

### Chi Daily: TCM Wellness Coach (msg 19d95ef928c0e027)
- Submission ID 0b529110-d749-48a6-903d-73f9b9062393. Submitted Apr 15, 2026 19:42 PDT. Reviewed Apr 16, 2026 (new app). Device: iPad Air 11-inch (M3), iPadOS 26.4.1. Version 1.0.
- **Guideline 3.1.2(c) - Business - Payments - Subscriptions**
  - Issue: required auto-renewable subscription information is missing.
    - In the app: the length of the subscription, the price (and price per unit if appropriate), a functional link to the Terms of Use (EULA), and a functional link to the privacy policy. Apple suggests SubscriptionStoreView.
    - In the metadata: a EULA link in the App Description (standard Apple EULA) or a custom EULA in ASC, and a privacy policy in the Privacy Policy field.
  - Next Steps: "Update the app and App Store metadata to include the information specified above. Once the app and metadata includes all of the required information, or if they already do, reply to this message with a screen recording to confirm. Include this information in the Notes field of the App Review Information section in App Store Connect for future submissions."
- **Guideline 1.5 - Safety**
  - Issue: the Support URL https://aniccafactory.github.io/chidaily/support is not functional or shows an error.
  - Next Steps: point the Support URL to a working page with support information.
- **Guideline 2.3.3 - Performance - Accurate Metadata**
  - Issue: most of the 6.7-inch iPhone screenshots do not show the actual app in use.
  - Next Steps: upload new screenshots that show the app in use on each supported device (use "View All Sizes in Media Manager"). Apple notes that marketing material and splash or login screens do not count.
- **Guideline 4.2 - Design - Minimum Functionality**
  - Issue: "The usefulness of the app is limited by the minimal functionality it currently provides. Specifically, the app does not provide sufficient content and features to be useful, unique, and 'app-like.'"
  - Next Steps: "review the app concept and incorporate different content and features that are in compliance with the App Review Guidelines."
- **Guideline 2.1(b) - Performance - App Completeness**
  - Issue: IAP bug. "The app closed the paywall when 'Start 7-Day Free Trial' was tapped and did not trigger payment."
  - Next Steps: standard IAP-bug text.
- **Likely fix:** this is the heaviest of the five.
  - Fix the trial button so it actually starts the StoreKit purchase.
  - Add the subscription terms, price and EULA/privacy links in the paywall, and the EULA link in the description.
  - Fix the support page.
  - Replace the screenshots with real in-app screens.
  - Add substantial features or content to answer 4.2.

### Cold Plunge Timer - FrostDip (latest: msg 19d94943e9592d85)
- Submission ID 7b96c39a-6de3-425b-bc10-7acb2e91d7bb. Submitted Apr 15, 2026 19:31 PDT. Reviewed Apr 16, 2026 (resubmission). Device: iPad Air 11-inch (M3). Version 1.0.
- **Guideline 3.1.2(c) - Business - Payments - Subscriptions**
  - Issue: the App Store metadata needs a functional Terms of Use (EULA) link: in the App Description if the standard Apple EULA is used, or as a custom EULA in ASC.
  - Next Steps: update the metadata. Reply with a screen recording if it is already included, and put this in the App Review Notes for future submissions.
- **Guideline 2.5.1 - Performance - Software Requirements**
  - Issue: "The app uses the HealthKit or CareKit APIs but does not clearly identify the HealthKit and CareKit functionality in the app's user interface."
  - Next Steps: clearly identify the HealthKit/CareKit functionality in the UI.
- Older rejection (msg 19ce1a30406d1c57): submission 938ac2bc-c4a4-40b9-82c2-3192fcaf3c3f, reviewed Mar 12, 2026, iPad Air M3, iPadOS 26.3.1, 1.0.
  - 2.1(b): IAP products had not been submitted.
  - 3.1.2(c): EULA link missing in the metadata.
  - 2.1(b) IAP bug: an error screen appeared on purchase.
- **Likely fix:** add the Apple standard EULA link to the App Description, and label the HealthKit features clearly in the UI (for example "Saves to Apple Health" with the Health icon on the relevant screen or in Settings).

### Zone2Daily (latest: msg 19d9493aeeeb1e1b)
- Submission ID 2b277328-8f21-4dfe-8aaa-29cea128ce31. Submitted Apr 15, 2026 19:26 PDT. Reviewed Apr 16, 2026 (resubmission). Device: iPad Air 11-inch (M3). Version 1.0.
- **Guideline 3.1.2(c) - Business - Payments - Subscriptions**
  - Issue: the metadata needs a functional EULA link (App Description or custom EULA) and a functional privacy policy in the Privacy Policy field. Apple suggests SubscriptionStoreView.
  - Next Steps: update the metadata. Reply with a screen recording if it is already included, and put this in the App Review Notes.
- **Guideline 1.4.1 - Safety - Physical Harm**
  - Issue: "The app includes medical information but does not include citations for the medical information. Specifically, the app provides health or medical calculations and references in the app without citations, such as links to sources for this information."
  - Next Steps: "Include citations in the app of the sources of the recommendations or information, such as links to those sources. The citations to the sources should be easy for the user to find."
- Older rejection (msg 19ce195a505e4307): submission a584a39d-bc60-4849-a23b-3d7fbb74fcc3, reviewed Mar 12, 2026, iPad Air M3, 1.0.
  - 2.1(b): IAP products had not been submitted.
  - 3.1.2(c): EULA link missing in the metadata.
- **Likely fix:** add the EULA link to the description and the privacy policy URL in ASC, and add an easy-to-find "Sources" section in the app that links the citations for the heart-rate zone and health calculations.

### Eye Break - EyeBreakIsland (latest: msg 19d9474e679ed598)
- Submission ID 1c891c85-1df7-45aa-951c-1d447a302864. Submitted Apr 15, 2026 19:37 PDT. Reviewed Apr 16, 2026 (resubmission). Devices: iPad Air 11-inch (M3) and iPhone 17 Pro Max, iPadOS/iOS 26.4.1. Version 1.0.
- **Guideline 5.2.5 - Legal - Intellectual Property**
  - Issue: "The app's metadata still includes content that is similar to designs or terms used for Apple products and services... Terms for 'Dynamic Island' in the app subtitle in an inappropriate manner."
  - Next Steps: remove terms confusingly similar to Apple products or services from the metadata.
- **Guideline 1.5 - Safety**
  - Issue: the Support URL https://daisuke134.github.io/anicca-products/eyebreakisland/support.html is not functional or shows an error.
  - Next Steps: point it to a working support page.
- **Guideline 2.1(b) - Performance - App Completeness**
  - Issue: "The In-App Purchase products in the app still exhibited one or more bugs... we could not access the paid features after purchasing the subscription."
  - Next Steps: standard IAP-bug text.
- Older rejection (msg 19cde2e869cadd1a): submission 3f28c788-4b36-477b-aa42-8bf1245f2efb, reviewed Mar 11, 2026, iPad Air M3 and iPhone 17 Pro Max, 1.0. The same three issues, plus one more:
  - 2.1(b): IAPs had not been submitted.
  - 5.2.5: "Dynamic Island" in the subtitle.
  - 2.1(b): features stayed locked after purchase.
  - 1.5: Support URL broken.
- **Likely fix:** remove "Dynamic Island" from the subtitle and metadata, publish a working support page, and fix entitlement unlocking after a sandbox purchase (check the entitlement and active-subscription status and refresh it right after purchase). Test on both iPad and iPhone.
