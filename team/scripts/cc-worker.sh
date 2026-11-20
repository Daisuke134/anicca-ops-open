#!/usr/bin/env bash
# cc-worker.sh — send one bounded, NON-SECRET task to Command Code (cheap worker) and save the result.
# Usage: team/scripts/cc-worker.sh <task-file> <result-file> [model] [max_tokens]
#   model: deepseek/deepseek-v4.1-flash (default) | z-ai/glm-5.3-flash (needs max_tokens>=256)
# Key: loaded via team/scripts/load-worker-env.sh (decrypts from Daisuke134/anicca-secrets if no local cache).
# Log: one line per run appended to team/state/cc-worker-log.md (no task content, no key).
# Rule: never put secrets, cookies, PII or owner-private data in a task file. Verify the output before using it.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; repo="$(cd "$here/../.." && pwd)"
task="${1:?task file}"; out="${2:?result file}"
model="${3:-${CC_MODEL:-deepseek/deepseek-v4.1-flash}}"
maxtok="${4:-${CC_MAX_TOKENS:-4096}}"
case "$model" in z-ai/*) [ "$maxtok" -lt 256 ] && maxtok=256;; esac
[ -r "$task" ] || { echo "cc-worker: task file not readable: $task" >&2; exit 2; }
# refuse obvious secrets in the task
if grep -Eq '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY|AGE-SECRET-KEY-|password[[:space:]]*[:=])' "$task"; then
  echo "cc-worker: task looks like it contains a secret; refusing" >&2; exit 4; fi
# shellcheck disable=SC1091
source "$here/load-worker-env.sh"
[ -n "${COMMAND_CODE_API_KEY:-}" ] || { echo "cc-worker: no COMMAND_CODE_API_KEY" >&2; exit 3; }
sys="${CC_SYSTEM:-You are a careful junior engineer/writer for Anicca. Do exactly the task. Output only the deliverable (code or markdown), no preamble. Do not invent facts, numbers, or links; write TODO where data is missing.}"
body="$(python3 - "$task" "$model" "$maxtok" "$sys" <<'PY'
import json,sys
t=open(sys.argv[1]).read()
print(json.dumps({"model":sys.argv[2],"max_tokens":int(sys.argv[3]),"temperature":0.2,
 "messages":[{"role":"system","content":sys.argv[4]},{"role":"user","content":t}]}))
PY
)"
t0=$(date +%s.%N); raw="$(mktemp)"
code=$(curl -sS --max-time "${CC_TIMEOUT:-180}" -o "$raw" -w '%{http_code}' \
  -H "Authorization: Bearer $COMMAND_CODE_API_KEY" -H "Content-Type: application/json" \
  https://api.commandcode.ai/provider/v1/chat/completions --data-binary @- <<<"$body") || code=000
secs=$(python3 -c "import time;print(round(time.time()-$t0,1))")
status=FAIL; usage=""
if [ "$code" = 200 ]; then
  if python3 - "$raw" "$out" <<'PY'
import json,sys,re
d=json.load(open(sys.argv[1])); m=d["choices"][0]
c=(m["message"].get("content") or "").strip()
if c.startswith("```"):
    mm=re.match(r"^```[^\n]*\n(.*?)\n```", c, flags=re.S)
    if mm: c=mm.group(1).strip()
u=d.get("usage",{}); open(sys.argv[1]+".u","w").write(f"in={u.get('prompt_tokens')} out={u.get('completion_tokens')} finish={m.get('finish_reason')}")
if not c: sys.exit(1)
open(sys.argv[2],"w").write(c+"\n")
PY
  then status=OK; fi
  [ -f "$raw.u" ] && usage="$(cat "$raw.u")"
fi
mkdir -p "$repo/team/state"; log="$repo/team/state/cc-worker-log.md"
[ -f "$log" ] || printf '# Command Code worker log\n\n| time (JST) | agent | model | task | result | status | http | secs | usage |\n|---|---|---|---|---|---|---|---|---|\n' > "$log"
rel() { python3 -c "import os,sys;print(os.path.relpath(os.path.abspath(sys.argv[1]),sys.argv[2]))" "$1" "$repo"; }
echo "| $(TZ=Asia/Tokyo date '+%F %H:%M') | ${CC_AGENT:-${AGENT_NAME:-unknown}} | $model | $(rel "$task") | $(rel "$out") | $status | $code | $secs | $usage |" >> "$log"
rm -f "$raw" "$raw.u"
[ "$status" = OK ] || { echo "cc-worker: FAIL http=$code $usage (empty content? raise max_tokens)" >&2; exit 1; }
echo "cc-worker: OK -> $out ($secs s, $usage)"
