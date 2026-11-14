# Visual skills used for Anicca assets — 2026-11-10 23:00 JST

Record of which published agent design skills were searched, chosen, and actually followed for the 2026-11-10 visual set (X Article cover, App Store screenshot concepts, X/IG post visuals).

## Search

Looked at GitHub and skills.sh for widely used, actively maintained agent design skills.

| Skill | Author / repo | Evidence of use | URL | Chosen? |
|---|---|---|---|---|
| frontend-design | Anthropic, [anthropics/skills](https://github.com/anthropics/skills) | Repo **191,848 stars**, 22,540 forks, last push 2026-11-06. Skill has **1.1M installs** on [skills.sh](https://www.skills.sh/anthropics/skills) (highest in the repo). | https://github.com/anthropics/skills/tree/main/skills/frontend-design | Yes — App Store phone UI, token system, anti-generic review |
| canvas-design | Anthropic, same repo | **130.1K installs** on skills.sh. Made for static PNG/PDF art (posters, covers). Ships a `canvas-fonts/` set. | https://github.com/anthropics/skills/tree/main/skills/canvas-design | Yes — cover, post visuals, and the art-philosophy step for the whole set |
| brand-guidelines | Anthropic, same repo | **118.0K installs** on skills.sh | https://github.com/anthropics/skills/tree/main/skills/brand-guidelines | No — it applies Anthropic’s own colors (Poppins/Lora, terracotta `#d97757`). That would overwrite Anicca’s ensō / dawn-teal identity. |

Repo metadata pulled from the public GitHub API on 2026-11-10 22:58 JST: `stargazers_count` 191848, `forks_count` 22540, `pushed_at` 2026-11-06T22:32:32Z, `updated_at` 2026-11-10T13:56:45Z, description “Public repository for Agent Skills”. Install counts from skills.sh the same evening.

Local clone (sparse, skills only): `/workspace/skills-external/anthropics-skills/`.

## What was actually followed

### canvas-design (`SKILL.md` read in full before any canvas was drawn)

Required sequence, followed as written:

1. Write a visual philosophy as a `.md` file (a movement, not a layout template).
2. Deduce the quiet conceptual thread from the brief.
3. Express it on a canvas as PNG, with skill fonts from `canvas-fonts/`, sparse text, no clipped elements.
4. Second pass: refine what is already there rather than adding decoration.

Philosophies written:

- `/workspace/marketing/visuals/PHILOSOPHY-LEDGER-CUT.md` — for the X Article cover.
- `/workspace/marketing/visuals/PHILOSOPHY-ENSO-WEATHER.md` — for App Store screenshots and post visuals.

### frontend-design (`SKILL.md` read in full)

Used for the App Store screenshot concepts (they are product UI, not posters):

- Ground the look in the subject (morning lock screen, short cards, Pali “anicca” / impermanence, the existing ensō mark’s dawn indigo–teal).
- Two-pass process: token plan first, review against generic AI-design tells, then build.
- Avoid the skill’s listed defaults unless the brief demands them: cream + terracotta serif, black + acid green, broadsheet hairlines, identical SaaS cards, tracked all-caps eyebrows, middle-dot meta, tinted `#0B0B0B`, decorative `→`.
- The X Article cover brief *does* ask for a big number on a dark field and a plain sans caption. frontend-design says the brief wins on a pinned axis; the number treatment stays, but the black is ink (not the default tinted near-black + acid accent) and the number is set as a ledger entry, not a dashboard hero stat.

Plan file: `/workspace/marketing/visuals/DESIGN-PLAN-FRONTEND.md`.

## What was not used

- Anthropic `brand-guidelines` (wrong brand).
- Older internal notes in `team/research/AI-DESIGN-SKILLS.md` (2026-10-26 landing-page redesign). Those are a different skill set and were not the instructions for this visual pass.
- Paid design tools. Rendering is HTML/CSS + headless Chromium (Playwright) only.

## Source copy and claims (screenshots and posts)

English only. Only live or LP-backed copy:

- Live promo text (en-US, 1.9.9, applied 2026-11-10): “A fresh affirmation on your Lock Screen every morning. Choose what you want to work on and get one kind line a day. No long meditation needed.”
- LP https://aniccaai.com/affirmation-app: short cards, choose what is on your mind, enable notifications, example affirmations, “Anicca means impermanence.”
- App name as live: Daily Affirmations - Anicca (id6755129214).
- No invented feature names, ratings, user counts, or “13 themes” (that caption already conflicts with the listing).
