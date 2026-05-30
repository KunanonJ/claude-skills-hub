---
name: adr-writer
description: Write a real-format Architecture Decision Record comparing two or more options. Covers context, trade-offs, scaling behavior at 10× load, hidden costs, recommendation with reasoning, and likely 2-year regrets. Use when the user is choosing between architectures, frameworks, databases, queue technologies, deployment platforms, or any "should I use X or Y" decision.
---

# Architecture Decision Record (ADR)

The user is choosing between options to solve a problem. Format the output as an ADR a real engineering organization would file.

Use this structure:

```markdown
# ADR-NNN: [Decision Title]

**Status:** Proposed
**Date:** YYYY-MM-DD
**Deciders:** [user]

## Context
[The problem, constraints, what's in scope, what's out of scope]

## Considered Options
1. [Option A]
2. [Option B]
3. [Option C if relevant]

## Decision Drivers
- [Hard constraints: SLA, budget, team skill, compliance]
- [Soft preferences: ergonomics, hiring, ecosystem]

## Option Analysis

### Option A: [Name]
- **Pros:** ...
- **Cons:** ...
- **At 10× load:** what scales, what breaks, what costs jump
- **Hidden costs:** operational overhead, migration risk, vendor lock-in, training, on-call
- **2-year regret risk:** what would future-you wish past-you had picked instead?

### Option B: [Name]
[Same structure]

## Decision
**Chosen: [Option X]**

Reasoning: [Why this beats the alternatives *given the constraints*]

## Consequences
- **Positive:** ...
- **Negative:** ...
- **Reversibility:** how hard is this to undo in 6 months / 2 years?

## Open Questions
[Things that should be answered before committing]
```

If the user gave you only options without context, **ask before writing** — an ADR without constraints is fiction. Ask for: traffic profile, team size/skill, budget ceiling, compliance/SLA, existing stack, time horizon.

Staff engineers don't pick by preference — they pick by constraint, long-term impact, and reversibility.
