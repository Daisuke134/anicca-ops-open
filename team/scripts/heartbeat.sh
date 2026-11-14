#!/bin/bash
# Copied from OpenClaw heartbeat (https://github.com/openclaw/openclaw/blob/fbdf5937/docs/gateway/heartbeat.md):
# cheap check every 30 min, no model; record changes for the nightly/afternoon runs to act on.
LOG=/workspace/team/health/heartbeat.log
while true; do
  TS=$(date '+%F %H:%M')
  python3 /workspace/team/scripts/browser_reaper.py --apply >/dev/null 2>&1
  FREE=$(free -m | awk '/Mem:/{print $7}')
  CHROME=$(pgrep -c chrome)
  echo "$TS free_mb=$FREE chrome=$CHROME" >> $LOG
  if [ "$FREE" -lt 1500 ]; then echo "$TS ALERT low_mem $FREE" >> /workspace/team/health/HEARTBEAT-ALERTS.md; fi
  sleep 1800
done
