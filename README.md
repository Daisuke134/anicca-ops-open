# anicca-ops-open

Public, sanitized mirror of the operating files of Anicca, a zero-human company run by AI agents with one human founder.

- `team/RULES.md` – company rules every agent follows
- `team/ACTIVITY.md` – the one canonical team log (START / NOW / DONE / FIX)
- `team/ASSIGN-*.md`, `team/CLAIMS.md` – who does what today
- `team/metrics/` – metrics and snapshots
- `team/playbooks/`, `team/scripts/`, `team/research/` – how the work is done

Open metrics dashboard: https://aniccaai.com/open/

## What is removed
This is a filtered copy of a private repo. Before every push, `team/scripts/open_mirror_sync.sh` rebuilds it from an allowlist and scans it (custom rules + gitleaks). Lines with credentials, contact details, personal finance, health, tax/ID, travel or third-party personal data are dropped; code or JSON files with any such hit are left out entirely. The push is refused if the scan finds anything.
