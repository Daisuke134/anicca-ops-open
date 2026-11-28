#!/bin/bash
exec ssh -i ~/.ssh/id_ed25519_macmini -o UserKnownHostsFile=~/.ssh/known_hosts_macmini -o StrictHostKeyChecking=accept-new -o ConnectTimeout=25 -o ServerAliveInterval=15 -o ProxyCommand='python3 /workspace/anicca-ops-main/team/scripts/socks5-proxy.py %h %p' anicca@100.99.82.95 "$@"
