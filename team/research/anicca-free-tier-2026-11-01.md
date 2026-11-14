# Anicca 未購読・×後の無料範囲（2026-11-01）
引用は `/workspace/repos/m1-ci-20261030/aniccaios/aniccaios/` 相対。iOS実装のみ調査；サーバー・RevenueCat外部設定は未検証。
- ×はprimer/planSelection両方に表示。購入せずオンボーディング完了→FeedRootViewへ進む（Onboarding/OnboardingBibleViews.swift:723–743、Onboarding/OnboardingFlowView.swift:116–120、ContentView.swift:19–29）。
- アファメーション：全ローカルプールを無料閲覧。日次回数チェックなし；ページングはプール末尾で止まる（Views/Feed/FeedRootView.swift:35–41,70–73、Views/Feed/VerticalPager.swift:70–80）。
- プールは英・日・西それぞれq001〜q200。独仏葡は英語にフォールバック。「200件/日」の割当ではない（Services/QuoteProvider.swift:16–21,41–280,283–522,525–764）。
- いいね・コピー・共有、テーマ変更、いいね一覧に購読ゲートなし（Views/Feed/QuoteCardView.swift:59–80、Views/Feed/SettingsSheet.swift:19–49,88–95）。
- reminders/nudges：設定は固定State「4回/日」の表示のみ。変更・保存・予約処理がなく、実際の無料配信数は不明（Views/Feed/SettingsSheet.swift:168–190）。
- ローカルproblem/free通知の新規予約は0件：APNs移行済みで旧free_nudge_0〜2を削除するだけ。旧3件を現行無料枠と解釈できない（Notifications/ProblemNotificationScheduler.swift:12–14,33–40）。APNsの無料回数・曜日・配信期間はこのiOSコードでは不明。
- AI：LLM生成Nudge取得は未購読なら空配列を返すため不可（Services/LLMNudgeService.swift:21–28、Models/SubscriptionInfo.swift:18）。独立したAI coach/chat画面・無料会話枠は見つからず不明；現行入口はフィード＋設定（ContentView.swift:19–29、Views/Feed/FeedRootView.swift:35–50,82–99）。
- 日数：×後にN日で失効する実装・曜日制限は見つからず。完了状態を永続保存・起動時復元し、ルーターは購読で再遮断しない（AppState.swift:86,165–169、ContentView.swift:19–29）。サーバー側期間制限は不明。
- その他上限：freeのmonthlyUsageLimit/Remaining/Countはnilで数値枠なし。サーバーも無制限という保証ではない（Models/SubscriptionInfo.swift:79–90）。canReceiveNudgeは常にtrueで配信数の保証ではない（AppState.swift:765–770）。
- Paywall再表示：×後の通常起動・フィード閲覧・回数/日数経過による自動再表示トリガーは見つからず。完了状態ならOnboardingFlowViewを通らない（AppState.swift:86,165–169、ContentView.swift:19–29、Views/Feed/FeedRootView.swift:70–99）。
- 未完了オンボーディングに戻れば、質問完了＋未購読でonAppear時にpaywall表示。resetStateは完了状態をfalseにする（Onboarding/OnboardingFlowView.swift:31–34、AppState.swift:224–229）。設定→SubscriptionはCustomerCenterView；その中の再paywall/購入導線はSDK・外部設定依存で不明（Views/Feed/SettingsSheet.swift:52–59）。
