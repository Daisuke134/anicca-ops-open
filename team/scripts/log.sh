#!/bin/bash
# usage: log.sh "agent" "did" "result" "why" "stuck" "next"
# appends "HH:MM JST | agent | did | result | why | stuck | next" to DAILY-LOG/<JST date>.md
# Concurrent-safe: fcntl.flock on <LOG_DIR>/.log.lock + O_APPEND os.write (one record <4KiB).
set -e
[ $# -ge 2 ] || { echo 'usage: log.sh "agent" "did" "result" "why" "stuck" "next"' >&2; exit 1; }
d=$(TZ=Asia/Tokyo date +%F); t=$(TZ=Asia/Tokyo date +%H:%M)
LOG_DIR="${ANICCA_DAILY_LOG_DIR:-/workspace/team/DAILY-LOG}"
f="$LOG_DIR/$d.md"; mkdir -p "$LOG_DIR"
c(){ printf '%s' "${1:-なし}" | tr '\n|' ' /'; }
line="$t JST | $(c "$1") | $(c "$2") | $(c "$3") | $(c "$4") | $(c "$5") | $(c "$6")"
export LOG_FILE="$f" LOG_LINE="$line" LOG_LOCK="$LOG_DIR/.log.lock"
python3 - <<'PY'
import fcntl, os
path = os.environ["LOG_FILE"]
data = (os.environ["LOG_LINE"] + "\n").encode("utf-8")
assert len(data) < 4096, "log record must be <4KiB for atomic O_APPEND"
lock_path = os.environ["LOG_LOCK"]
with open(lock_path, "a+", encoding="utf-8") as lf:
    fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
        try:
            os.write(fd, data)
        finally:
            os.close(fd)
    finally:
        fcntl.flock(lf.fileno(), fcntl.LOCK_UN)
PY
