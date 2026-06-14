# Backlog Refinement Checklist

Ready-to-use Definition of Ready (DoR), Definition of Done (DoD), and a 60-minute refinement session agenda. Copy into your team's wiki and adapt.

---

## Definition of Ready (DoR)

A story is **Ready** when ALL of these are true:

- [ ] **Title** is descriptive and specific (no generic "Implement X")
- [ ] **Why** statement references a specific OKR, metric, customer outcome, or strategic objective
- [ ] **What** description is 1-2 paragraphs and serves as a reminder of the refinement discussion (not a spec)
- [ ] **Acceptance criteria**: at least 4, each describing an observable user-facing outcome
- [ ] **INVEST score**: >= 5/6 (verified by `refinement_scorer.py` or facilitated review)
- [ ] **Dependencies** on other stories or teams identified and noted (or "None")
- [ ] **Design assets** linked (or marked "TBD by [date]" with owner)
- [ ] **Estimate** captured in the team's preferred unit (story points, t-shirt, days)
- [ ] **No open blocker questions** (questions that block estimation or execution)
- [ ] **Tagged** with the sprint goal or theme it contributes to

> If any item fails, the story is NOT ready. Do not negotiate it into the sprint. Either fix in this refinement or defer to next week.

---

## Definition of Done (DoD)

A story is **Done** when ALL of these are true:

- [ ] All acceptance criteria pass in the deployed environment (not just dev)
- [ ] Code merged to main (or release branch per release process)
- [ ] Automated tests written and passing for changed paths (unit + at least one integration)
- [ ] Code reviewed and approved by at least one other engineer
- [ ] Manual QA pass complete (or QA sign-off if separate QA function exists)
- [ ] Documentation updated where applicable: help center, internal runbook, API docs
- [ ] Feature flag wired (if behind flag) or release-notes entry drafted
- [ ] Analytics / telemetry events instrumented for outcome measurement
- [ ] Accessibility check pass (WCAG 2.1 AA for user-facing UI)
- [ ] Product owner has accepted the story

> "Done" is binary. If any item is missed, the story rolls to the next sprint -- it is not "90% done."

---

## DoR / DoD by story type

Different work types deserve different gates. Keep three short lists rather than one long one.

### Feature story (full DoR + full DoD above)

The default. All bullets apply.

### Bug fix (lighter DoR)

- [ ] Reproducible: steps to reproduce documented
- [ ] Severity assessed (S1/S2/S3/S4)
- [ ] Root cause hypothesis noted (or "TBD via investigation")
- [ ] Acceptance: "bug no longer reproduces" + regression test added
- [ ] DoD applies in full (especially the regression test bullet)

### Spike (different DoR, modified DoD)

- [ ] Question to be answered stated in one sentence
- [ ] Time-box agreed (typically 1-3 days)
- [ ] Decision criteria noted (what answer ends the spike)
- [ ] DoD = written summary of findings + next-step recommendation (no code-merge requirement)

### Tech debt (modified DoR)

- [ ] Value chain articulated (what user-facing metric improves?)
- [ ] If no user-facing metric improves, classify as engineering hygiene and track outside the user-story backlog
- [ ] DoD applies in full

---

## 60-minute weekly refinement session agenda

| Time | Segment | Owner | Output |
|------|---------|-------|--------|
| 0:00-0:05 | Review last week's refined stories | PM | Continuity, catch rework |
| 0:05-0:10 | Pull next 8-12 candidates from prioritized backlog | PM | Candidate list |
| 0:10-0:20 | Quick INVEST triage (60s per story) | Whole team | 3 buckets: PROMOTE / REFINE / SEND BACK |
| 0:20-0:50 | Deep-refine 2-4 stories from REFINE bucket | Whole team | Split, clarify, write acceptance criteria |
| 0:50-0:57 | Estimate refined stories | Engineers | Sized stories |
| 0:57-1:00 | Confirm DoR pass, move to sprint queue | PM | Ready stories tagged |

> Use a visible timer. Refinement is the most under-invested ritual; protect the time-box.

---

## INVEST quick-grade card (print and laminate)

```
I -- Independent:  Can this ship alone?
N -- Negotiable:   Does this prescribe HOW, or only WHAT and WHY?
V -- Valuable:     Who benefits if this is the only thing we ship?
E -- Estimable:    Can two engineers estimate independently within 2x?
S -- Small:        Can a pair finish this in 1-5 days?
T -- Testable:     How would QA prove this is done?

Score: ___/6
  6   = Ready (promote)
  5   = Ready with one named gap
  3-4 = Refine
  0-2 = Send to discovery
```

---

## Story splitting cheat sheet

When a story scores low on INVEST-S (Small), apply patterns in this order:

1. **Workflow steps** -- Split a multi-step process by step
2. **Business rules** -- Split by rule (loyalty vs promo vs volume)
3. **Happy/unhappy paths** -- Ship happy path first
4. **Input options** -- Split by channel (keyword/filter/voice)
5. **Data types** -- Split by data variant (CSV/PDF/XLSX)
6. **CRUD operations** -- Split by operation
7. **Test scenarios** -- Split by tested scenario (Okta/AzureAD/etc)
8. **Defer performance** -- Ship correct first, optimize later
9. **Spike** -- Time-box investigation, then re-split

> Vertical only. Never split DB/API/UI/Infra -- that violates INVEST-V and INVEST-I.

---

## Anti-pattern audit (run quarterly)

Sample the last 30 completed stories. For each, check:

- [ ] Did it have an INVEST score >= 5 at sprint entry? (Target: 80%+)
- [ ] Did it roll over to a subsequent sprint? (Target: <15%)
- [ ] Did all acceptance criteria pass before "done"? (Target: 100%)
- [ ] Did telemetry confirm the predicted outcome? (Target: 70%+)
- [ ] Did any DoD bullet get waived? (Target: 0%)

Surface the data in retrospective (`../sprint-retrospective/`) and adjust DoR/DoD where pattern failures appear.

---

**Last updated:** 2026-05-21
