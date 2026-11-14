#!/usr/bin/env bash
# launch-iam-v2-ppo.sh — Anicca (6755129214) PPO "treatment-iam-v2" one-shot launcher.
# Test spec + done condition: team/research/ANICCA-PPO-IAM-V2-TEST-2026-11-11.md
# Modes:
#   status   (default) show all PPO experiments + whether v2 can be created
#   start-d7 start d7ffa0d7 once Apple has approved it (ACCEPTED/APPROVED, not yet started)
#   stop-d7  stop d7ffa0d7 (only when its done condition is met; log the result first)
#   launch   create v2 experiment + treatment + en-US loc, sync 8 shots, create review submission and submit
# Never touches d7ffa0d7 except in start-d7 / stop-d7. Exits non-zero if another experiment is in review/running.
set -euo pipefail
APP=6755129214
D7=d7ffa0d7-704c-42ef-abf8-588f3bada53e
NAME="I am layout v2 Nov 2026"
TNAME="I am layout v2 (8 shots)"
HERE=$(cd "$(dirname "$0")/../.." && pwd)
DIR67=${DIR67:-$HERE/marketing/anicca/aso/treatment-iam-v2/en-US/APP_IPHONE_67}
DIR65=${DIR65:-/workspace/anicca-aso/treatment-iam-v2/en-US/APP_IPHONE_65}
ASC="bash /workspace/team/scripts/ascx.sh"
mode=${1:-status}
j(){ python3 -c "import sys,json;d=json.load(sys.stdin);print($1)"; }

list(){ $ASC product-pages experiments list --v2 --app "$APP" --paginate; }
states(){ list | python3 -c "import sys,json;[print(e['id'],e['attributes']['state'],e['attributes'].get('startDate'),e['attributes'].get('endDate'),e['attributes']['name'],sep=' | ') for e in json.load(sys.stdin)['data']]"; }

case "$mode" in
status) states ;;
start-d7)
  st=$(list | python3 -c "import sys,json;print([e['attributes']['state'] for e in json.load(sys.stdin)['data'] if e['id']=='$D7'][0])")
  echo "d7 state: $st"
  case "$st" in ACCEPTED|APPROVED|READY_TO_START|COMPLETED_REVIEW) $ASC product-pages experiments update --v2 --experiment-id "$D7" --started true ;; *) echo "not startable yet"; exit 4;; esac ;;
stop-d7) $ASC product-pages experiments update --v2 --experiment-id "$D7" --started false ;;
launch)
  busy=$(list | python3 -c "import sys,json;print(','.join(e['id'][:8]+':'+e['attributes']['state'] for e in json.load(sys.stdin)['data'] if e['attributes']['state'] not in ('STOPPED','COMPLETED','REJECTED','PREPARE_FOR_SUBMISSION')))")
  if [ -n "$busy" ]; then echo "BLOCKED: other experiment not finished: $busy (Apple: one PPO at a time)"; exit 3; fi
  $ASC screenshots validate --path "$DIR67" --device-type IPHONE_67 >/dev/null
  EXP=$(list | python3 -c "import sys,json;print(next((e['id'] for e in json.load(sys.stdin)['data'] if e['attributes']['name']=='$NAME'),''))")
  [ -z "$EXP" ] && EXP=$($ASC product-pages experiments create --v2 --app "$APP" --platform IOS --name "$NAME" --traffic-proportion 50 | j "d['data']['id']")
  echo "experiment $EXP"
  TR=$($ASC product-pages experiments treatments list --v2 --experiment-id "$EXP" | j "next((t['id'] for t in d['data']),'')")
  [ -z "$TR" ] && TR=$($ASC product-pages experiments treatments create --v2 --experiment-id "$EXP" --name "$TNAME" | j "d['data']['id']")
  echo "treatment $TR"
  LOC=$($ASC product-pages experiments treatments localizations list --treatment-id "$TR" | j "next((l['id'] for l in d['data'] if l['attributes']['locale']=='en-US'),'')")
  [ -z "$LOC" ] && LOC=$($ASC product-pages experiments treatments localizations create --treatment-id "$TR" --locale en-US | j "d['data']['id']")
  echo "localization $LOC"
  $ASC product-pages experiments treatments localizations screenshot-sets sync --localization-id "$LOC" --path "$DIR67" --device-type IPHONE_67 --confirm >/dev/null
  if $ASC product-pages experiments treatments localizations screenshot-sets list --localization-id "$LOC" | grep -q APP_IPHONE_65 && [ -d "$DIR65" ]; then
    $ASC product-pages experiments treatments localizations screenshot-sets sync --localization-id "$LOC" --path "$DIR65" --device-type IPHONE_65 --confirm >/dev/null
  fi
  $ASC product-pages experiments treatments localizations screenshot-sets list --localization-id "$LOC"
  SUB=$($ASC review submissions-create --app "$APP" --platform IOS | j "d['data']['id']")
  $ASC review items add --submission "$SUB" --item-type appStoreVersionExperiments --item-id "$EXP" \
    || $ASC review items add --submission "$SUB" --item-type appStoreVersionExperimentsV2 --item-id "$EXP"
  $ASC review submissions-submit --id "$SUB" --confirm
  echo "SUBMITTED experiment=$EXP submission=$SUB — after approval run: $ASC product-pages experiments update --v2 --experiment-id $EXP --started true"
  ;;
*) echo "usage: $0 [status|start-d7|stop-d7|launch]"; exit 2;;
esac
