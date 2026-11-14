# SHARED-HUB — where every Anicca agent shares files, data, memory (2026-11-01 01:30 JST, 参謀 research)

## 1. Winners on X (copy source first)
| # | Who / post | Claimed result | Shared state they use | Security they describe |
|---|---|---|---|---|
| 1 | @petergyang on @nateliason's Felix — https://x.com/petergyang/status/2025956342763274654 | $4,000/week (Feb) | 3-layer markdown memory: knowledge graph + daily notes + tacit knowledge (files) | Bot gets its OWN X/Stripe/GitHub/email accounts, never the owner's ("blast radius stays contained") |
| 2 | @Atenov_D — https://x.com/Atenov_D/status/2060659782390804780 | Felix $80k/month on $400/mo | Same 3-layer memory; knowledge base rebuilt nightly 2am; 30-min heartbeat; sub-agents Iris/Remy reprogrammed nightly | Own accounts on GitHub, Stripe, Vercel, Twitter |
| 3 | @stacy_muur (Bankless recap) — https://x.com/stacy_muur/status/2033092093346984203 | $80k/mo verified-ish ($41k PDF) | Nightly 2am retro rewrites memory files for self + sub-agents | — |
| 4 | @marfinxx — https://x.com/marfinxx/status/2065134600167542815 | Felix $80k/30d | Main node Mac Mini with GitHub access | Warns: no container isolation, CVE-2026-25253 key theft → isolate |
| 6 | @exyonX — https://x.com/exyonX/status/2115643763230175443 | (Grok multi-agent) | Shared memory + shared `/workspace` filesystem | — |
| 7 | @moltbot_builds — https://x.com/moltbot_builds/status/2043500048579768734 | OpenClaw stack guide | — | Per-agent container, secrets manager, least privilege, audit logs, encrypt at rest |
| 8 | @linus5x — https://x.com/linus5x/status/2094365805353869771 | — | Shared memory only after verification (claim+evidence+expiry) | Prevents bad inference becoming "infrastructure" |
| 9 | @MorganSMFWorks — https://x.com/MorganSMFWorks/status/2093096965924122734 | — | "shared memory, coordination files, escalation paths" | — |
| 10 | @zainakrams — https://x.com/zainakrams/status/2105907141039325345 | — | Shared memory contract / blackboard beats agent chatter | — |
| 11 | @trytermsquad — https://x.com/trytermsquad/status/2098193079530348836 | product | Always-on cloud machine w/ shared memory for Codex/Claude | — |
| 12 | @AiCamila_ — https://x.com/AiCamila_/status/2069108680986153204 | — | — | Scoped short-lived creds fetched from a vault at runtime, never hard-coded |
| 13 | @shabnamporjalil — https://x.com/shabnamporjalil/status/2085770871092711726 | — | Warning: shared infra becomes a coordination layer | Scope who can see what |


## 2. Candidates compared
| Option | All agents reach it w/o human? | Notes |
|---|---|---|
| **GitHub repo (anicca-ops, current)** | Yes: Grok box, Mac mini, Muse VM, Codex cloud, cloud agents, Pally/OpenCode via git or GitHub MCP | Felix pattern. Versioned, audit log built in, fine-grained per-agent tokens / deploy keys. Large media → Git LFS or bucket |
| Reason (user-reason) | Only agents with Reason MCP/API key | Team memory: `listMemoryFiles`/`readMemoryFile`/`writeMemoryFile`/`searchMemory`/`deleteMemoryFile` (32 KiB/note, 12 KiB MEMORY.md, team writes owner/admin only, refuses secrets). Files: `createAttachment` (1 MiB via MCP, 25 MiB via REST), `listAttachments`, `downloadAttachment`, `deleteAttachment` — flat, no folders, signed short-lived URLs. Already present: team MEMORY.md + now.md (points to GitHub sanbou-ops ONBOARDING.md), 6 Anicca slide PNGs. No DB/KV. Good as index/inbox, not a file system |
| Cloudflare R2 / S3 | Yes with per-agent keys | Best for big media; no history/diff for docs |
| Google Drive (connector) | Grok yes; Codex/VMs need OAuth/service account | Human-oriented, weak for scripts |

## 3. Recommendation (copied as-is)
- **Primary shared place: GitHub repo Daisuke134/anicca-ops**, owned/operated by the team's own bot accounts — copied from Felix (https://x.com/petergyang/status/2025956342763274654, https://x.com/Atenov_D/status/2060659782390804780): markdown memory in 3 layers (knowledge/ , daily/ , tacit/) + nightly 2am retro that rewrites them.
- Big media (reels, PNGs): R2 bucket, path referenced from the repo. Reason team memory = one-line pointer index only (it already does this).

### How each agent reaches it
- Dots/Codex (Mac mini): its own `gh` login (no shared token file).
- Pally/Poke/OpenCode: read-only fine-grained PAT; writes via PR.


## 4. Migration — first 3 steps
1. Restore sync of anicca-ops from the Mac mini's own gh login; revoke the leaked token (in progress, user-approved).
