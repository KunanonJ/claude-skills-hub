---
name: debug-detective
description: Investigate bugs systematically before fixing. Generate ranked hypotheses with confirming evidence, suggest targeted logging, surface bad assumptions, and propose the smallest test to isolate the root cause. Use when the user reports a bug, error, weird behavior, "why doesn't this work", or any "X is broken" / "X returns wrong result" situation.
---

# Debug Like Sherlock Holmes

**Do NOT fix the bug yet.** Investigation comes before action.

Walk through these steps:

1. **5 ranked hypotheses** — list 5 possible causes, ordered most-to-least likely. Be specific (not "a bug in the function" but "off-by-one in the loop bound at line N").

2. **Evidence test for each** — for every hypothesis, what observation would *confirm* it and what would *rule it out*? If a hypothesis can't be tested, it's not useful — discard it.

3. **Targeted instrumentation** — what specific log lines, print statements, breakpoints, or trace IDs would make the cause visible? Aim for minimum noise.

4. **Assumption check** — list assumptions in the code that could be wrong:
   - Input shape (sorted? unique? non-null?)
   - Timing (sync? always completes? bounded latency?)
   - Concurrency (single-threaded? atomic?)
   - External state (DB row exists? cache fresh? clock monotonic?)

5. **Smallest isolating test** — the minimal reproduction. Strip away everything not needed to trigger the bug. If you can reduce it to a unit test, do.

After the analysis, **stop and wait** for the user to gather evidence and report back. Then propose a fix.

Senior developers don't guess bug causes — they investigate. Stop guessing, start observing.
