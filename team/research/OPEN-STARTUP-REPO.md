# Open Startup Repo 調査（2026-10-26）
- Repo: https://github.com/ultrametricai/ultrametric （clone済: /workspace/research/open-startup-repo）
- 告知ポスト: https://x.com/judegomila/status/2113638585274695800 （2026-10-23 JST）／続報「他にどの国を見たい？」https://x.com/judegomila/status/2113708084560548113
- ライセンス: コード=Apache-2.0。open-rankings/のデータは独自Data License（短い引用は帰属表示つきで可、まとめて再利用するには許可が必要）
- 規模: 2,689 commits、PR 307件マージ、TypeScript、CLI `npm i -g ultrametric`、MCP/プラグインあり

## これは何か（やさしい日本語）
会社の立ち上げと運営を「AIエージェントが動かせるように」分解した公開データベース。
1. open-rankings: 142市場（決済・銀行・会計・給与・法務・税・行政など）の各ツールを、API/MCP/CLI/ブラウザ操作でAIがどこまで動かせるかで採点
2. open-processes: 設立・税申告・資金調達・SOC2などを手順に分け、各手順を agent / form / human に振り分け、所要時間と「取り消しやすさ」を付与
3. open-law: 国・州ごとの法ルール（US各州、UK、EU、SG、KR、AU、NZ、HK）
4. open-modules: キャップテーブル、ランウェイ、期限カレンダー、給与税などの決定的な計算ライブラリ
5. 目標は「AIに頼むだけで会社をつくり、月$1Mまで動かす」。私たちのNo Human In The Loopと同じ方向

## 日本のカバー状況

## AIによる操作のしやすさ ランキング（verdicts集計: full=2, partial=1。自前集計なので目安）
| 分野 | 上位 |
|---|---|
| 決済 | Stripe 77 > Paddle 58 > PayPal/Polar 55 |
| 銀行 | Ramp 76 ≈ Mercury 75 > Brex 52 |
| 会計 | Digits 58 > Zoho Books 53 > QuickBooks 49 |
| 給与 | Gusto 56 > Check 45 > Rippling 44 |
| 法務/設立 | DocuSign 37 > Ironclad 30 > Clerky 25 |
| サブスク課金 | Chargebee 52 > Lago 50 > Stripe Billing 47 |
| 税 | Avalara 44 > Anrok/Kintsugi/Numeral 42 > Stripe Tax 37 |

## 今すぐ採り入れること
1. **決済はStripeに一本化（上の表で1位）**: Stripe認証の宿題を最優先で片付ける。RevenueCat＋Stripeを、AIが動かせる収益の土台にする
2. **手順の型をそのまま真似る**: 私たちのroutineの各手順に `route: agent|form|human`、`reversibility`、`所要時間` を付ける。humanになっている手順を毎週数えて減らすことをKPIにする（"human step count"）。参考: open-processes/agent-run-back-office.json, bookkeeping-close.json, connect-a-payment-processor.json, create-a-subscription-product.json
3. **US法人を作るとき**: 設立はClerky、銀行はMercuryかRamp、給与はGusto、税はStripe Tax（いずれもエージェント操作性の上位）。open-processes/incorporate-*.jsonの手順に従う

## 足りないもの（私たちのニーズとの差）
- 個人の生活運営（Life Managerの領域）は対象外。会社運営だけ
- 「売上を作る」側（集客・販売のループ）は薄い。手順とベンダー選びが中心
- ランキングはUS中心で、日本で使えるかどうかの情報がない

## 次のアクション（担当）
| # | アクション | 担当 | 期限 |
|---|---|---|---|
| 1 | Stripe認証を片付け、決済→RevenueCat→指標の経路をagentだけで回す | 参謀 → Reasonセッション | 10/31 |
| 2 | routine全体に route/reversibility を付け、human手順数を X-METRICS と同じ日次指標にする | 参謀 routines | 11/2 |
| 5 | X scoutが「会社/スタートアップをエージェントで自動化」系の発表をP0として拾う | 参謀 X routine | 今日 |
| 6 | 日本モジュールのPRを Daisuke134 から出すかどうか決める（まだ出さない） | 参謀 | 11/7 |

## 貢献すべきか → はい（日本モジュール）
理由: 作者が国を募集中で日本はゼロ。PRはbuild in publicの材料になり、「No Human In The Loopの日本の会社」として最初の貢献者になれる。CONTRIBUTING.md §6「Add a jurisdiction」の形に合わせる:
1. `jurisdictions/vendor-geo.json` に JP の行を追加（Stripe JP, freee, マネーフォワード, GMOあおぞらネット銀行 など `{productId,country:"JP",status}`）
3. `open-law/JP/` を追加（所得税法の申告期限、会社法の設立手続き など。出典は e-Gov 法令検索）
下書きは /workspace/team/research/open-startup-japan-pr-draft/ に置く。**PRはまだ出さない。**
