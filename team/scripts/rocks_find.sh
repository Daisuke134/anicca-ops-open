#!/usr/bin/env bash
# Search GrokBot.Rocks (12k+ public Grok Bots) via its free public MCP endpoint. No key.
# Usage: rocks_find.sh "what the bot should do" [limit]   |  rocks_find.sh --latest [limit]
# Source: https://readmultiplex.com/2026/11/27/your-grok-bot-just-got-a-library-card-to-grokbot-rocks/
# Rule (TEMPLATE-FIRST): search here before building a new bot/routine/skill; credit the creator.
set -euo pipefail
LIMIT="${2:-5}"
if [ "${1:-}" = "--latest" ]; then
  BODY=$(python3 -c 'import json,sys;print(json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"latest","arguments":{"limit":int(sys.argv[1])}}}))' "$LIMIT")
else
  BODY=$(python3 -c 'import json,sys;print(json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"find_bots","arguments":{"query":sys.argv[1],"limit":int(sys.argv[2])}}}))' "$1" "$LIMIT")
fi
curl -s -m 30 -H 'Content-Type: application/json' -H 'Accept: application/json,text/event-stream' https://mcp.grokbot.rocks/mcp -d "$BODY" \
 | sed -n 's/^data: //p' | python3 -c 'import json,sys
for l in sys.stdin:
  r=json.loads(l).get("result",{})
  for c in r.get("content",[]):
    print(c.get("text",""))'

