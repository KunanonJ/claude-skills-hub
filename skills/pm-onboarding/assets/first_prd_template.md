# First PRD Template (for new PMs)

This is a tighter PRD template calibrated for a new-PM's first authored doc. The full 8-section PRD template (`execution/create-prd/`) is appropriate from your second PRD onward.

**Aim:** 2-4 pages. Customer-evidenced. Scoped to ship within the 90-day onboarding window.

---

# [Feature / Project Name]

**Author:** [Your name]
**Manager:** [Their name]
**Date:** [YYYY-MM-DD]
**Status:** Draft / Review / Approved
**Target ship:** [Week N of 90-day onboarding]

---

## 1. Summary (3 sentences max)

What is this? Who is it for? Why are we doing it now?

> _________________________________________________________________
> _________________________________________________________________
> _________________________________________________________________

---

## 2. Customer evidence

Cite 2-3 customer interviews you ran yourself, or 2-3 specific customer signals (ticket clusters, sales feedback). New-PM PRDs are weakest when they cite "we believe" instead of "P3 said...".

| Source | What they said / showed | Date |
|--------|--------------------------|------|
| Interview with [name/role] | "..." | |
| Interview with [name/role] | "..." | |
| Support ticket cluster | [n tickets in 30 days about X] | |

---

## 3. Problem statement (1 paragraph)

Frame the problem from the customer's perspective.

> _________________________________________________________________
> _________________________________________________________________
> _________________________________________________________________

---

## 4. Why now? (1 paragraph)

What changed or what makes this the right thing to do this quarter?

> _________________________________________________________________
> _________________________________________________________________

---

## 5. Proposed solution

### 5.1 What we're building

1-2 paragraphs. Reminder of the discussion, not a full spec.

> _________________________________________________________________
> _________________________________________________________________

### 5.2 Key features (P0 / P1 / P2)

- **P0:** ____________________________________________________
- **P0:** ____________________________________________________
- **P1:** ____________________________________________________
- **P2:** ____________________________________________________

### 5.3 Design link

[Figma / mock link, or "TBD" with target date]

### 5.4 Explicitly out of scope

What you considered but deliberately deferred.

- _________________________________________________________________
- _________________________________________________________________

---

## 6. Success criteria

How will we know v1 worked?

- **Primary metric:** [metric] from [baseline] to [target] within [time]
- **Secondary metric:** [metric] from [baseline] to [target]
- **Guardrail:** [metric] must not drop below [threshold]

---

## 7. Timeline

- **Discovery / spike:** Week N-N
- **Design:** Week N-N
- **Build:** Week N-N
- **Launch:** Week N
- **Post-launch review:** Week N

---

## 8. Open questions

Questions I'm still working through. Surfacing them invites collaboration.

- _________________________________________________________________
- _________________________________________________________________
- _________________________________________________________________

---

## 9. Reviewers

Who should see this before approval?

| Name | Role | Reviewed? | Comments |
|------|------|-----------|----------|
| | Manager | | |
| | Eng Lead | | |
| | Design Lead | | |
| | Skip-level (optional) | | |
| | Cross-functional partner | | |

---

## New-PM PRD checklist

Before you share with reviewers:

- [ ] Length is 2-4 pages (longer = compress)
- [ ] Section 2 cites 2-3 customer signals you personally validated
- [ ] Section 5 explicitly lists what's out of scope
- [ ] Section 6 has measurable success criteria with baselines
- [ ] Section 7 lands inside your 90-day window
- [ ] Eng Lead has seen the draft before formal review
- [ ] Design Lead has seen the draft before formal review
- [ ] You can articulate the why in 2 sentences without reading the doc
