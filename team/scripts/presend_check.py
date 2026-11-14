#!/usr/bin/env python3
"""RULE 0t pre-send check. Usage: presend_check.py FILE (or stdin). Exit 1 + hits if banned words found."""
import re, sys
BANNED = ["成果報酬","成功報酬","成果連動","別払い","別途お支払","直接お支払","直接取引","直接契約","サイト外","手数料なし","振込先","銀行振込","PayPal","LINE","Zoom","Google ?Docs","Googleドキュメント","Googleスプレッドシート","Chatwork","Slack","電話番号","メールアドレス"]
text = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
hits = [w for w in BANNED if re.search(w, text, re.I)]
if hits:
    print("NG:", ", ".join(hits)); sys.exit(1)
print("OK")
