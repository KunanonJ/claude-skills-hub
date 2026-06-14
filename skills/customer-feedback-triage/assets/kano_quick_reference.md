# Kano Quick Reference

One-page reference card for triage. Pin this in the team's Notion / Confluence / wiki.

## The five categories

| Category | If present | If absent | Build it? | Verbatim signals |
|---|---|---|---|---|
| **Basic / Must-be** | Customer doesn't notice; satisfaction flat | Severe dissatisfaction; possible churn | Always — basic gaps are existential | broken, doesn't work, can't, missing, blocker, 404, error, crashed |
| **Performance** | More is linearly better | Linearly worse | Yes, with diminishing returns | faster, slower, more, increase, bulk, batch, scale, limit, throughput |
| **Delight / Attractive** | Disproportionate satisfaction; customer tells others | No effect; customer doesn't miss it | A few per quarter for differentiation | would love, wish, dream, magic, ai, smart, automatic, predict, suggest |
| **Indifferent** | No effect | No effect | Only if near-zero cost or precondition for something else | color, theme, icon, rename, label (aesthetic-only) |
| **Reverse** | Causes dissatisfaction | Improves satisfaction | Build the opposite (remove or reduce) | too chatty, annoying, intrusive, popup, spam, remove, disable |

## Priority weights in the triage formula

```
priority = kano_weight × log10(customers + 1) × max_segment_weight × (1 + strategic_alignment)
```

| Category | Kano weight |
|---|---|
| Basic | 4 |
| Performance | 2 |
| Delight | 3 |
| Indifferent | 0 |
| Reverse | -3 |

## Decision flowchart

```
Is the request about something the customer expected and didn't get?
  Yes → Basic
  No  → Is the customer asking for "more" or "faster" or "more of X"?
        Yes → Performance
        No  → Would the customer be delighted to discover this exists?
              Yes → Delight
              No  → Is the customer asking to REMOVE or DISABLE something?
                    Yes → Reverse
                    No  → Indifferent
```

## Common traps

| Trap | Fix |
|---|---|
| Categorizing every request as "performance" | Read the verbatim; "faster reports" can be basic if reports time out |
| Forgetting to re-categorize over time | Today's delighter becomes tomorrow's basic. Re-audit quarterly. |
| Treating all "AI" requests as delight | AI is migrating to performance and basic depending on category; re-check |
| Building indifferent features because they're easy | Easy ≠ valuable. Indifferent stays off the roadmap unless a precondition |
| Ignoring reverse signals | When customers ask you to remove something, listen — the opposite cluster (more of X) may be wrong |

## Segment overrides

A feature can shift categories by segment:

| Feature | SMB | Mid-market | Enterprise |
|---|---|---|---|
| SSO | Indifferent | Performance | Basic |
| Audit log | Indifferent | Performance | Basic |
| Custom branding | Delight | Performance | Basic |
| Public API | Performance | Performance | Performance |
| AI assistant | Delight | Delight → Performance | Performance |
| Mobile app | Performance | Performance | Indifferent (desktop-first) |

When a cluster is segment-skewed, re-categorize for the dominant segment in the cluster.

## When to run a proper Kano survey

The keyword heuristic is good enough for everyday triage. Run a proper Kano survey (functional + dysfunctional questions) when:

- The feature is strategically important and the team is split on category
- The decision involves significant engineering investment (> 1 quarter)
- The feature affects pricing or packaging (see `pricing-prd/`)
- A regulator or auditor will ask "how did you decide this was a must-have?"

A proper Kano survey with 50-100 customers takes 1-2 weeks and definitively resolves the category question.

## See also

- `references/kano-model-deep-dive.md` — full theory and edge cases
- `assets/triage_template.md` — manual triage worksheet
- `assets/response_templates.md` — response templates by category and channel
- Kano, N. et al. (1984). "Attractive Quality and Must-Be Quality"
