#!/usr/bin/env bash
# Box memory gate (RULE 0w). Run before any browser/desktop work on the shared box.
# Exit 0 = go, exit 3 = stop (log BLOCKED once, don't open the browser).
# Never kills anything: other agents' tabs are not yours to close.
MIN_MB="${MIN_MB:-1500}"
avail=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
chrome=$(pgrep -c chrome || true)
load=$(cut -d' ' -f1 /proc/loadavg)
echo "box_mem_gate avail=${avail}MB chrome_procs=${chrome} load=${load} min=${MIN_MB}MB"
if [ "$avail" -lt "$MIN_MB" ]; then
  echo "STOP: under ${MIN_MB}MB. Skip browser work this run; close only tabs you opened; log one BLOCKED line with these numbers."
  exit 3
fi
