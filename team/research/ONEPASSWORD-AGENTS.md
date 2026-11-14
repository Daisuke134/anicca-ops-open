- 対応: Muse(Meta)とGrok Botは「数日中」全プラットフォーム。Claude Duet/ChatGPT Work/dots/Townieは近日。.eu/.caアカウント不可
- 安全性 vs /workspace/.secrets(mode 600): 秘密がエージェントのコンテキストやログに出ない、承認と取消ができる点で明確に安全。ただし「ログインごとにユーザー承認」が前提＝無人ループと衝突
## 推奨
現時点は「全面移行しない／Grok Bot側で使えるようになったら成田さん本人アカウントのログインだけに限定採用を検討」。
- エージェント専用アカウント(agentmail系)は無人運用が必須なので.secrets(600)継続。代わりに: .secretsをログ・出力に絶対出さない、ファイルごとのローテーション、CREDENTIALS-INDEX.md で棚卸し
