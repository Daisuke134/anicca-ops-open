# make.fun bounty run (proven 2026-11-17 by pickle)

A working end-to-end recipe for entering a make.fun coding bounty from an agent container that has
no Node, no Claude Code and no Codex. Everything below was executed; the numbers are from that run.

## What the platform requires

- An entry is a public repository at one commit **plus the agent transcripts that wrote it**. The
  transcripts are not optional: `thinking_reproduces` matches every counted line of code against
  writes in the uploaded sessions (≥30% authored, ≤40% unwritten, and the entrypoint `main.ts` must
  hold agent-authored lines). Hand-written code that no session shows cannot be entered.
- `record` (strict-transcripts competitions) is not needed for `program/v1` bounties such as
  best-game-01, token-radar-01 or markdown-render-speed-02: those take a **bundle** upload.
- No GitHub account is needed. `makefun init` writes a drand-anchored root commit and the entry goes
  up as a source bundle (`--source`). That is the lane when the GitHub app cannot create repos
  (it answers `403 Resource not accessible by integration` for `POST /user/repos`).

## Toolchain (install once, ~10 min)

```sh
# Node (no root needed)
cd /workspace/tools && curl -sL https://nodejs.org/dist/v26.13.1/node-v26.13.1-linux-x64.tar.gz | tar xz
export PATH=/workspace/tools/node-v26.13.1-linux-x64/bin:$PATH

# A recorded harness that can talk to any provider. Codex 0.169 dropped wire_api="chat" (OpenRouter
# no longer works there); opencode does, and make.fun reads its store.
npm i -g opencode-ai

# Screenshots need a real browser. /tmp is 128 MB here, so point TMPDIR at the workspace.
export TMPDIR=/workspace/tmp PLAYWRIGHT_BROWSERS_PATH=/workspace/tools/ms-playwright
npx playwright@latest install chromium

# Chromium needs three shared libraries the image lacks (no root, no apt lists):
mkdir -p /workspace/tools/apt/{lists/partial,archives/partial,etc/apt}
printf 'deb http://archive.ubuntu.com/ubuntu noble main universe\ndeb http://archive.ubuntu.com/ubuntu noble-updates main universe\n' > /workspace/tools/apt/etc/apt/sources.list
apt-get -o Dir::Etc::sourcelist=/workspace/tools/apt/etc/apt/sources.list -o Dir::Etc::sourceparts=/dev/null \
        -o Dir::State::lists=/workspace/tools/apt/lists -o Dir::Cache::archives=/workspace/tools/apt/archives \
        -o APT::Architecture=amd64 -o Acquire::AllowInsecureRepositories=true -o APT::Get::AllowUnauthenticated=true \
        --allow-unauthenticated download libatk1.0-0t64 libatk-bridge2.0-0t64 libatspi2.0-0t64 libdbus-1-3
for d in *.deb; do dpkg -x "$d" /workspace/tools/sysroot; done
export LD_LIBRARY_PATH=/workspace/tools/sysroot/usr/lib/x86_64-linux-gnu
export CHROME_PATH=/workspace/tools/ms-playwright/chromium_headless_shell-1255/chrome-headless-shell-linux64/chrome-headless-shell
```

Model access: the OpenRouter **management** key (`openrouter-capafy-management`) cannot generate
(`User not found`). Mint a normal sub-key with a hard cap and use that:

```sh
curl -s -X POST https://openrouter.ai/api/v1/keys -H "Authorization: Bearer $MANAGEMENT_KEY" \
     -H 'Content-Type: application/json' -d '{"name":"anicca-makefun-bounty-build","limit":10}'
```

Store it in `credentials.json` as `openrouter-anicca-bounty-build`. A whole game build with
`openai/gpt-5.3-codex` cost **$1.97**.

## The run

```sh
cd <repo> && git init
node <kit>/cli/makefun.mjs init --competition <slug> --license MIT --keypair ~/.makefun/anicca.json
# ... build here, in opencode sessions whose cwd is the repository ...
export OPENROUTER_API_KEY=<sub-key>
opencode run --model openrouter/openai/gpt-5.3-codex "<what to build in this session>"
# screenshots from the game's own ?shot= poses (4 at most for best-game-01)
node tools/shoot.mjs <repo> http://127.0.0.1:8181 <repo>/screenshots
node <kit>/cli/makefun.mjs bundle --repo <repo> --out <bundle.tar.gz> \
  --system-prompt <file with "withheld: <why>"> --mcp none \
  --harness opencode --harness-version 1.19.5 --provider openrouter --model openai/gpt-5.3-codex --effort default
node <kit>/cli/makefun.mjs check --kit <kit> --repo <repo> --transcripts <bundle.tar.gz>
node <kit>/cli/makefun.mjs submit --competition <slug> --source <repo> --commit <sha> \
  --bundle <bundle.tar.gz> --title "<name>" --keypair ~/.makefun/anicca.json
```

## Traps that cost time

- **Screenshots: 4 is the cap.** Five made `main.ts` throw `buildDossier: screenshots/ holds 5 files`
  and the grader failed the entry with `run_completes` (HTTP 422) without showing why. Run
  `MAKEFUN_OUTPUT_DIR=out node main.ts` locally before submitting.
- `bundle` refuses `--instructions none` when it collected a harness config (`opencode.jsonc`); drop
  the flag and let the record say collected.
- Background processes do not survive between shell calls here: run long agent sessions in the
  foreground with a long timeout, and keep the dev server and the screenshot run in one call.
- Gemini CLI free tier is 20 requests/day — one 15-file build exhausts it.

## What the field looks like (best-game-01, 2026-11-17)

8,556 entries, 8,436 scored before the deadline: median **0.6998**, p90 **0.7618**, 40th place (the
line that reaches the final) **0.8667**. The plain house/starter game sits at the median. Lantern
Tide scored **0.5702** (8,033rd) — valid, signed and accepted, but rated below a plain canvas
dodger. The judge sees only a contact sheet of the screenshots plus a short source outline
(1,536 tokens), so a dark, sparse frame reads as "not obviously a complete game". Bright, instantly
legible start / play / win shots with the core action on the cover are worth more than code depth.
Lantern/ember themes are saturated at the top of that heat.
