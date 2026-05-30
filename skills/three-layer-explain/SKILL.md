---
name: three-layer-explain
description: Explain a concept, library, framework, or design pattern at 3 levels — 30-second PM summary, 5-minute working example, and deep trade-offs/gotchas/anti-patterns. Use when the user asks "explain X", "what is X", "how does X work", "should I use X", or is learning a new library/pattern/technology and needs to use it quickly.
---

# 3-Layer Explanation

Explain the concept, library, or pattern at three distinct levels. Skip textbook framing; the user needs to use this *tomorrow*.

## Layer 1 — 30-second PM summary

- 1-2 sentences max
- Language a non-engineer would follow
- Answer: what problem does this solve, and what does using it feel like at the highest level?

## Layer 2 — 5-minute engineer explanation

- The mental model an engineer needs to use this correctly
- A minimal, runnable code example showing the most common use case
- Annotate the code with what each line is doing and why
- Show what the input/output looks like

## Layer 3 — Trade-offs, gotchas, when not to use

- **Trade-offs**: what does this give up compared to alternatives?
- **Gotchas**: things that bite in real code (perf cliffs, footguns, version mismatches, common misuse)
- **When NOT to use**: the cases where reaching for this is wrong, even though it looks like a fit
- **Alternatives**: 1-2 sibling tools/patterns and when each is preferable

## Rules

- **Don't pad with history or philosophy.** If the user wanted a Wikipedia article, they'd read one.
- **Code must run** as written. No `...` placeholders, no pseudo-code.
- **Be honest about weaknesses.** A "this is great for everything" explanation is wrong.

The goal: user can use it confidently in production within an hour of reading.
