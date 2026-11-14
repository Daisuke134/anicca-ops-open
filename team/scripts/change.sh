#!/bin/bash
# usage: change.sh "agent" "change" "who is affected"
echo "$(TZ=Asia/Tokyo date '+%F %H:%M') JST | $1 | $2 | $3" >> /workspace/team/CHANGES.md
