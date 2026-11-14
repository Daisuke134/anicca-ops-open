# SYNTHETIC STUB — hand-authored illustration, not a measured case

All text below was invented for this packet. It is not an Anicca conversation, a real person's profile, an actual model rollout, or evidence of fidelity improvement. It contributes zero observations to fidelity-table.md.

## Invented reference C

User: Help me sort a box of colored cards.
Assistant: Sort them by color, then by size.
User: Just colors. One step at a time.
Assistant: Put the blue cards in one pile.
User: Blue done. Next?
Assistant: Put the red cards in a second pile.
User: Done. That's enough for now.

## r0 — task + behavior

Task: Sort colored cards into color piles.
Behavior: Uses short replies and wants practical instructions.

## S0 — illustrative first rollout

User: Help me sort colored cards.
Assistant: Sort them by color, then by size.
User: Great, I'll sort by both color and size. What else?
Assistant: You could label every pile.
User: Yes, let's label everything too.

## One illustrative hindsight note

Compared with C, S0 accepts an extra sorting dimension and expands the task. The behavior description misses scope correction, requests for a single next step, brief progress reports, and stopping before expanding the activity. Add those observable patterns without inventing a biography or copying the reference turns.

## r1 — one illustrative revision

Task: Sort colored cards into color piles.
Behavior: Uses brief replies. Corrects suggestions that add sorting dimensions. Requests one actionable step at a time and reports completion before requesting another. May stop after partial progress rather than expand the task.

## S1 — illustrative re-roll

User: Cards to sort. Colors only.
Assistant: Sort them by color, then by size.
User: Skip size. First step?
Assistant: Make a pile of green cards.
User: Done. Next color?
Assistant: Make a yellow pile.
User: Done. Stopping here.

Before fidelity: 未測定. After fidelity: 未測定. AUC: 未測定. Change: 未測定.
The apparent behavioral alignment is scripted into this example; only a consented evaluation could test whether model-generated revision helps.
