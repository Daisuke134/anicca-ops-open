# 自律会社の回し方（参謀用ルール）2026-10-27
出典つき。[未検証]は今回ページを開いて確認していないもの。

1. **夜間ループ＝状態を見る→1タスク決める→実行→朝に報告。** Polsiaは各エージェントがこれを毎晩回し、創業者には毎日メール1通だけ。 https://render.com/blog/a-sandbox-doesn-t-constrain-an-api-key-what-polsia-learned-running-autonomous-companies-on / https://www.antoinebuteau.com/lessons-from-ben-cera/
2. **CEOエージェントは優先順位だけ決め、実作業は専門エージェントへ。** 依頼をそのまま実行しない。（同上 Part 5）
3. **判断はモデル、commit・deploy・ログ確認・再試行は決まった手順に。** 開いたままのループは「最後の地味な一歩」を飛ばす。（Render/Polsia）
4. **権限・予算・ツールは1つの設定ファイルで宣言し、縛られる側は編集できない。** 役割に必要なツールだけ渡す。 https://usenaive.ai/
5. **1回の実行は1スライス。終わったら進捗ファイルとgitに残し、次回は最初にそれを読む。** https://www.anthropic.com/research/effective-harnesses-for-long-running-agents
6. **作った本人に採点させない。** 書き込み権限のない新しい文脈の評価役がPASS/NEEDS_WORK。証拠ファイルを読まないと「完了」と書けない（デフォルトFAIL）。 https://github.com/anthropics/cwc-long-running-agents
7. **成果の単位あたりコストを測る。** 実行回数ではなく「検証済みの前進/回」「不要なツール呼び出し」「1成果あたりコスト」。 https://ai-magister.com/en/articles/ai-agent-harness-guide
8. **モデルが上がるたびに仕組みを削る。** ハーネスは複雑なほど高い（$9 vs $200の比較）。 https://www.beri.net/learning/anthropic-harness-design-long-running-apps
9. **権限の重いもの（支払い・オンボーディング・本番の重大変更）は範囲を決めて二重チェック。** Polsiaも決済とオンボーディングは自動変更の対象外。（Buteau Part 5 #22）
10. **自律度はスライダー。** 小さく任せて検証が速いところから広げる。Karpathy「autonomy slider」[未検証] https://www.youtube.com/watch?v=LCEmiRjPEtQ
11. **1人で全部出す人は「作ったものを毎回公開して出す」。** levelsio流のbuild in public [未検証] https://x.com/levelsio
12. **「1人で10億ドル企業」はAltmanの予想であって実績ではない。** 目標にはしても主張には使わない。[未検証] https://fortune.com/2024/02/04/sam-altman-one-person-unicorn-silicon-valley-founder-myth/

注：「Grok Botの使い手がどう回しているか」のX検索は今回できていない（公開事例が見つからず未実施）。次回のセルフ改善ループで1回だけ探す。

## Grok Bot winners（2026-10-27 X調査。各ルールに出典。動画本編・t.co先のガイドは未視聴＝章立て/投稿本文のみ）
1. **チーフは作業しない。振り分け→監視→回収→上申だけ。** 最初にチーフを作る。 https://x.com/irongiantXBT/status/2113420143959195748
2. **文脈はチャットで渡さず/workspaceに置く（社内バス）。** 調査・下書き・証拠・決定・引き継ぎは全部ファイル。どのBotも途中から拾える。（同上 step3）
3. **全ワークフローに3つの関門：出典→証拠→実行。** 人の承認が要る所まで止まらず進む。（同上 step5）
4. **人が承認するのはお金・公開・削除・署名・取り消せない外部行為だけ。** 調査・下書き・照合・検証・キュー入れはBotが勝手に。（同上 step6）
5. **高くつく失敗：頻繁なポーリング、全部の同期、二重実行する再試行、Botの増やしすぎ。** （同上 step7）
6. **各Botに役割契約：ROLE / INPUTS / OUTPUT / WHEN TO ASK。** 修正は一時的に直さず役割の説明に恒久化。 https://x.com/irongiantXBT/status/2109293672495784029
7. **手順：一度手で完了→安定させる→スキル保存→最後にルーチン化。** スキル＝やり方、ルーチン＝いつ回すか。 同上 / https://x.com/tsukiema_/status/2112947495059743047
8. **Chief of Staff（1日の計画と配布）→PM（分割と出来の検査）→25+ワーカー。** 検査役を作業者と分ける。 https://x.com/tsukiema_/status/2113988709150261313
9. **入口は1つのBotだけ。「委任した作業をやったふりをしない」「証拠なしで完了にしない」「速いからと専門の仕事を奪わない」。** 存在するからといってBotを足さない。 https://x.com/unicodef1wn/status/2102375891875581966
10. **構成：memory→tools→skills→delegation→routines、24/7オンコールBot、スマホから全体運用。** https://x.com/neilchor/status/2106462016063877233 / https://x.com/Mahaximus_/status/2113994869513277546
11. **1Bot1仕事、全員が同じ1つのDB（Notion）に保存。** 8つのチャットを掘らない。 https://x.com/emanueledpt/status/2108497977111445907
13. **実例：本を出版（表紙・中身チェック・出品・ISBN）＋サイト公開＋寝ている間に36件応募。** https://x.com/ianbower/status/2114897692513960394
14. **35体を超えたら、チーム→部門→会社の入れ子にして、各単位にリードを置く。** https://x.com/greyfedora0/status/2114581269644513288
15. 職種別ガイド17本（営業・SDR・サポート・マーケ等）。自分の仕事に一番近い1本から1体作る。 https://x.com/1920web1080/status/2111091527896191080 [リンク先未読]
注：「grok bot」×MRR/売上のX検索で見つかった具体的な金額の実例は12だけ。大きな売上の公開例は見つからず。
