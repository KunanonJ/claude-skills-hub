---
name: backlog-refinement
description: >
  Backlog refinement playbook covering INVEST quality, vertical story splitting,
  Definition of Ready, and Definition of Done -- with a Python scorer that grades
  each story against INVEST and emits a ready/not-ready verdict.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-execution
  updated: 2026-05-21
  python-tools: refinement_scorer.py
  tech-stack: invest, story-splitting, definition-of-ready, definition-of-done
---
# Backlog Refinement Expert

## Overview

Refinement is the most under-invested ritual in agile teams. Stories arrive at sprint planning oversized, ambiguous, or strategically disconnected, and the team spends planning meetings doing what should have happened the week before. This skill is the refinement playbook: how to grade stories against INVEST, how to split stories vertically (so each slice ships value end-to-end), and how to keep a working Definition of Ready and Definition of Done that prevent half-baked work from entering or leaving a sprint.

The skill includes a Python scorer (`refinement_scorer.py`) that grades each story in a JSON backlog file against the six INVEST criteria and outputs a readiness score (0-6) per story. Stories scoring 5-6 are sprint-ready; 3-4 need targeted refinement; below 3 need to be reworked or returned to discovery.

This is a complement to `wwas/` (the Why-What-Acceptance format) and `job-stories/` (the JTBD format). Either format produces stories; this skill grades them and gets them sprint-ready.

### When to Use

- **Weekly refinement session** -- Standard ritual: grade next-sprint candidates against INVEST and split anything too large.
- **Backlog hygiene sweep** -- Quarterly: re-grade the top 30 backlog items and retire what no longer connects to current strategy.
- **Sprint planning input** -- Before planning: confirm all candidates pass DoR.
- **New team onboarding** -- A new team needs a shared definition of "ready" and "done" to ship predictably.
- **Velocity diagnosis** -- If sprint completion is erratic, refinement quality is usually the cause; this skill is the diagnostic.

### When NOT to Use

- For pure technical task lists with no user-facing outcome -- INVEST applies loosely; use a simpler checklist.
- For ad-hoc bug triage -- bugs follow a different lifecycle (triage > prioritize > fix) than feature stories.
- When the work has not been scoped yet -- send it back to `discovery/` skills before refining.

## The INVEST Criteria

Bill Wake's INVEST acronym (2003) defines the six properties of a high-quality story:

| Letter | Property | What it means | Quick test |
|--------|----------|---------------|------------|
| **I** | **Independent** | Can be delivered without waiting for another story | "Can this ship alone? If no, what is the dependency?" |
| **N** | **Negotiable** | Implementation is open to discussion | "Does this prescribe HOW, or only WHAT and WHY?" |
| **V** | **Valuable** | Delivers value to a user or business | "If we built only this and nothing else, who benefits?" |
| **E** | **Estimable** | The team can size effort with reasonable confidence | "Can two engineers independently estimate within ~2x?" |
| **S** | **Small** | Fits within one sprint (typically 1-5 days of effort) | "Can a pair finish this in <5 days?" |
| **T** | **Testable** | Acceptance criteria are observable and verifiable | "How would QA prove this is done?" |

A story scoring 6/6 is sprint-ready. A story scoring 5/6 with a soft fail on one criterion is usually safe to admit if the team agrees on the gap. Anything 4 or below needs a refinement pass.

## Vertical Slicing and Story Splitting

The most common refinement failure is **horizontal slicing** -- splitting a story by layer (DB, API, UI, infra) rather than by user outcome. Horizontal slices fail INVEST-V (no slice delivers user value alone) and INVEST-I (every slice depends on the others).

**Vertical slices** cut through every layer to deliver an end-to-end thin sliver of user value. Each slice is independently shippable and independently valuable.

### The 9 splitting recipes (Richard Lawrence)

Richard Lawrence's Story Splitting Flowchart enumerates 9 reliable patterns. Use them in this priority order:

| # | Pattern | Use when | Example |
|---|---------|----------|---------|
| 1 | **Workflow steps** | The story spans a multi-step process | "Checkout" → "Add to cart" / "Pay" / "Confirm" |
| 2 | **Business rule variations** | The story covers many rules | "Discount" → "Loyalty discount" / "Volume discount" / "Promo code" |
| 3 | **Happy / unhappy paths** | Error handling adds complexity | "Submit form" → "Submit valid form" / "Handle validation errors" |
| 4 | **Input options / platforms** | Multiple inputs or platforms | "Search" → "Search via keyword" / "Search via filters" / "Search via voice" |
| 5 | **Data types or parameters** | Multiple data variations | "Export report" → "Export CSV" / "Export PDF" / "Export XLSX" |
| 6 | **Operations (CRUD)** | The story covers multiple ops | "Manage users" → "Create user" / "Edit user" / "Delete user" |
| 7 | **Test scenarios / cases** | Test plan reveals natural splits | "Login" → "Login with email" / "Login with SSO" / "Login with MFA" |
| 8 | **Defer performance** | The simple version works | "Search 1M records" → "Search basic" (v1) / "Optimize search" (v2) |
| 9 | **Spike (last resort)** | The team cannot estimate | A time-boxed investigation, then re-split |

### The SPIDR alternative (Mike Cohn)

Mike Cohn's SPIDR mnemonic covers a similar space with five buckets: **S**pikes, **P**aths, **I**nterfaces, **D**ata, **R**ules. Use whichever taxonomy your team finds memorable; the patterns overlap.

### Splitting anti-patterns to avoid

- **Splitting by layer.** "Backend API" / "Frontend UI" / "Database migration" are tasks, not stories. They violate INVEST-V.
- **Splitting by team.** If only "the backend team" can deliver a slice, the slice is not independently valuable.
- **Splitting by sprint.** Forcing a 10-day story into "Sprint 1 part" and "Sprint 2 part" is scheduling, not splitting.
- **Splitting too thin.** A 2-hour story is not a story; it is a task. Roll it back up.

## Definition of Ready (DoR)

The DoR is the team's agreement on what a story must satisfy before it can enter a sprint. It is the **input quality gate**.

### Recommended DoR template

A story is Ready when:

- [ ] Title is descriptive and specific (no "Implement X")
- [ ] Why statement references a specific objective, OKR, or customer outcome
- [ ] Description is 1-2 paragraphs and serves as a reminder of the refinement discussion
- [ ] Acceptance criteria: at least 4, each describing an observable user-facing outcome
- [ ] INVEST score >= 5/6 (verified by `refinement_scorer.py` or facilitated review)
- [ ] Dependencies on other stories or teams are identified and noted
- [ ] Design assets linked (or marked "TBD by [date]" with owner)
- [ ] Estimated by the team using their preferred unit (story points, t-shirt, days)
- [ ] No open blocker questions
- [ ] Tagged with sprint goal it contributes to

### DoR anti-patterns

- **Too strict** -- a 20-item DoR creates a backlog of "almost ready" stories. Cap at 10.
- **Unenforced** -- a DoR that planning ignores is theater. Enforce: stories that fail DoR are removed from the sprint candidate list, not "negotiated in."
- **One-size-fits-all** -- spikes, bugs, and feature stories have different DoRs. Keep three short checklists rather than one long one.

## Definition of Done (DoD)

The DoD is the team's agreement on what a story must satisfy before it can be called complete. It is the **output quality gate** and is typically uniform across all stories.

### Recommended DoD template

A story is Done when:

- [ ] All acceptance criteria pass in the deployed environment
- [ ] Code merged to main branch (or release branch per release process)
- [ ] Automated tests written and passing (unit + integration for changed paths)
- [ ] Code reviewed and approved by at least one other engineer
- [ ] Manual QA pass (or QA sign-off if separate QA exists)
- [ ] Documentation updated (help center, internal runbook, API docs, as applicable)
- [ ] Feature flag wired (if behind a flag) or release-notes entry drafted
- [ ] Analytics or telemetry events instrumented (so we can measure the outcome)
- [ ] Accessibility check pass (WCAG AA for user-facing UI)
- [ ] Product owner has accepted the story

### DoD anti-patterns

- **"Done" but not deployed** -- a story that is merged but not in front of a user is not done. Require deployment in the DoD.
- **No instrumentation** -- shipping without telemetry means you cannot measure the outcome. Require analytics for any value-claim story.
- **Skipping accessibility** -- a11y debt compounds. Require WCAG AA on every user-facing change.

## Workflow

1. **Pull candidates from the backlog.** Aim for 1.5x the team's velocity in candidates per refinement session.
2. **Score each candidate with `refinement_scorer.py`.** Use `--input backlog.json --format markdown` to get a per-story INVEST grade.
3. **Triage by score:**
   - **5-6:** Promote to "Refined" lane.
   - **3-4:** Discuss in session, address the failing criteria.
   - **0-2:** Send back to discovery (`discovery/brainstorm-ideas/` or `discovery/identify-assumptions/`) -- the work has not been scoped enough.
4. **Split oversized stories.** Apply the 9 Lawrence patterns in priority order. Each new slice must independently pass INVEST-V and INVEST-S.
5. **Enforce the DoR.** Anything failing DoR at planning is removed from the candidate list, not "negotiated in."
6. **Enforce the DoD at review.** Stories that miss any DoD bullet are not "almost done" -- they roll to the next sprint.
7. **Hand off refined stories to sprint planning.** A well-refined backlog reduces planning to: pick the top N stories that fit capacity.

## Tools

| Tool | Purpose | Command |
|------|---------|---------|
| `refinement_scorer.py` | Grade stories against INVEST and emit readiness verdicts | `python scripts/refinement_scorer.py --input backlog.json --format markdown` |
| `refinement_scorer.py --demo` | Inspect demo data and output format | `python scripts/refinement_scorer.py --demo --format markdown` |

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Refinement sessions run long and produce few refined stories | Too many candidates per session; team trying to refine everything at once | Cap at 1.5x velocity in candidates; spend max 2 minutes per story on initial INVEST grade; deep-refine only those scoring 3-4 |
| Same stories appear in 3+ refinement sessions without progress | Story is too vague; team lacks information; or story belongs in discovery | Apply the "3-strike rule" -- if a story fails to refine three sessions in a row, send to `discovery/identify-assumptions/` to reframe |
| Sprint planning becomes the refinement session | DoR is not enforced; pressure to "make the sprint full" overrides quality | Empower the team to leave the sprint under-full rather than admit DoR-failing stories; track planning duration as a velocity proxy |
| Splits produce horizontal slices (API / UI / DB) | Team defaults to architecture decomposition; PM does not push back | Use the 9 Lawrence patterns explicitly; require each slice to answer "who benefits if this is the only thing we ship?" |
| Stories pass DoD but value does not materialize | Acceptance criteria describe activity, not outcome; no telemetry | Rewrite acceptance criteria as observable user outcomes; require telemetry/analytics in the DoD |
| Estimates vary wildly across the team | INVEST-Estimable failure; story too vague or too large | Re-refine with a spike if needed; split into smaller slices that two engineers can size within 2x of each other |
| `refinement_scorer.py` gives 6/6 but story still feels risky | Score covers form, not substance; risk is in the assumptions, not the format | Use `discovery/identify-assumptions/` and `discovery/pre-mortem/` for substantive risk; INVEST is necessary but not sufficient |

## Success Criteria

- 80%+ of stories entering sprint planning score 5/6 or 6/6 on INVEST
- Refinement session length stays under 60 minutes per week, per team
- DoR and DoD are reviewed and updated at least once per quarter
- Story splits produce vertical slices in 90%+ of cases (each slice independently valuable)
- Sprint planning meetings take less than half the duration of refinement (because refinement did the work)
- Rolled-over story rate (stories that miss the sprint) below 15% sustained
- Stories scoring below 3 on INVEST are sent back to discovery rather than forced into a sprint

## Scope & Limitations

**In Scope:**
- INVEST quality grading of individual stories
- Vertical story splitting using the 9 Lawrence patterns and SPIDR taxonomy
- Definition of Ready and Definition of Done templates and enforcement protocol
- Refinement session structure and cadence guidance
- Python tool that grades backlog JSON against INVEST and emits per-story verdicts

**Out of Scope:**
- Authoring stories from scratch (use `wwas/` or `job-stories/`)
- Backlog prioritization or sequencing (use `prioritization-frameworks/`)
- Sprint planning, capacity calculation, or velocity forecasting (use `../scrum-master/`)
- Discovery, problem framing, or opportunity definition (use `discovery/` skills)
- Story estimation techniques (Planning Poker, Affinity Estimation -- covered in `agile-coach/`)

**Important Caveats:**
- INVEST is a heuristic, not a guarantee. A story can score 6/6 and still be the wrong story to build. Use this skill alongside `prioritization-frameworks/` and `discovery/identify-assumptions/` for full coverage.
- The 9 Lawrence patterns work for product stories. Pure technical infrastructure work may follow different splitting heuristics (component boundaries, deployment risk).
- DoR and DoD must be team-authored to be enforced. Imposing an external DoR/DoD without team buy-in produces theater, not quality.
- The Python scorer grades structural form (does the story have a Why, a What, and 4+ ACs?), not strategic substance. A 6/6 story can still be misaligned with strategy.

## Integration Points

| Integration | Direction | Description |
|-------------|-----------|-------------|
| `execution/wwas/` | Receives from | WWAS-format stories enter refinement to be graded and split |
| `execution/job-stories/` | Receives from | Job stories enter refinement to be graded and split |
| `execution/prioritization-frameworks/` | Pairs with | Prioritization sets the sequence; refinement makes the top N actually executable |
| `discovery/identify-assumptions/` | Sends to | Stories scoring 0-2 are sent back to discovery for assumption mapping |
| `discovery/brainstorm-experiments/` | Sends to | Stories with unvalidated assumptions become experiment candidates |
| `../scrum-master/` | Feeds into | Refined stories feed sprint planning; refinement quality drives velocity stability |
| `execution/status-update-generator/` | Indirect | DoD compliance feeds the "what's done this week" section of status updates |
| `../jira-expert/` | Pairs with | Refined stories become Jira tickets with structured fields and DoR/DoD checklists |

## Tool Reference

### refinement_scorer.py

Grades each story in a JSON backlog file against the six INVEST criteria and emits a readiness score (0-6) per story plus an aggregate readiness summary for the backlog.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--input` | string | (required unless `--demo`) | Path to JSON file containing backlog items |
| `--demo` | flag | false | Use built-in demo backlog data |
| `--format` | choice | markdown | Output format: json, markdown, mermaid, confluence, notion, linear |
| `--output` | string | stdout | Output file path |
| `--threshold` | int | 5 | Minimum score for a story to be flagged "READY" (default 5/6) |

### Input JSON shape

```json
{
  "stories": [
    {
      "id": "STORY-1",
      "title": "Add SSO login for enterprise users",
      "why": "Enterprise customers cite missing SSO as the #1 blocker; supports $2M ARR expansion target",
      "what": "Add SAML 2.0 SSO option to the login page. Users with company email domains see SSO as the primary login method; password login remains as fallback.",
      "acceptance_criteria": [
        "Users with configured domains see SSO as primary login option",
        "SAML 2.0 IdP-initiated flow works for Okta and Azure AD",
        "Failed SSO falls back to password with helpful error",
        "Audit log records every SSO login attempt"
      ],
      "estimate_days": 4,
      "has_design": true,
      "dependencies": []
    }
  ]
}
```

### Scoring rubric

| Criterion | Passes if... |
|-----------|--------------|
| Independent | `dependencies` field is empty or omitted |
| Negotiable | `what` field is present and under 800 characters (long whats prescribe implementation) |
| Valuable | `why` field is present and references a metric, OKR, customer, or business outcome (heuristic) |
| Estimable | `estimate_days` field is present and is a positive number |
| Small | `estimate_days` is between 1 and 5 |
| Testable | `acceptance_criteria` field contains at least 4 items |

## References

- `references/invest-and-splitting-guide.md` -- Deep dive on INVEST, the 9 Lawrence patterns, SPIDR, and worked split examples
- `assets/refinement_checklist.md` -- Ready-to-use DoR and DoD checklists plus a refinement session agenda
