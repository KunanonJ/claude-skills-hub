# Beta Exit Memo: [Feature / Product Name]

**Owner (DACI Driver):** [Name, role]
**Date of exit-gate review:** [YYYY-MM-DD]
**Beta start / end dates:** [YYYY-MM-DD] / [YYYY-MM-DD]
**Decision:** [Greenlight GA / Extend Beta / Pivot / Kill]
**Document status:** [Draft / Signed Off]

---

## 1. Executive Summary

Three sentences. Decision, headline rationale, next concrete action.

> Example: We are greenlighting GA for [Feature]. All 8 exit gates met, 4 named reference customers confirmed, no open P0 bugs. Launch is scheduled for [date] using `launch-playbook/`.

---

## 2. Gate Results

| Gate | Target | Actual | Status | Notes |
|------|--------|--------|:------:|-------|
| Activation (% to first action in 7 days) | >= 70% | [X]% | [Met/Miss/Partial] | |
| Median time-to-first-action | <= 24h | [X]h | [Met/Miss/Partial] | |
| Median sessions/week (weeks 2-4) | >= 3 | [X] | [Met/Miss/Partial] | |
| Retention (% active in week 4) | >= 60% | [X]% | [Met/Miss/Partial] | |
| Outcome (% achieving headline) | >= 50% | [X]% | [Met/Miss/Partial] | |
| NPS | >= 30 | [X] | [Met/Miss/Partial] | |
| Open P0 bugs | 0 | [X] | [Met/Miss/Partial] | |
| Crash-free sessions | >= 99.5% | [X]% | [Met/Miss/Partial] | |
| Quotable testimonials | >= 3 | [X] | [Met/Miss/Partial] | |
| Support runbook + training | Yes | [Yes/No] | [Met/Miss] | |
| Pricing decision finalized | Yes | [Yes/No] | [Met/Miss] | |

---

## 3. Cohort Performance

| Cohort | Recruited | Activated | Retained (week 4) | NPS | Notable Feedback Themes |
|--------|----------:|----------:|------------------:|----:|-------------------------|
| Friends | | | | | |
| Family | | | | | |
| Fanatics | | | | | |

**Weighted cohort signal** (Friends 0.5x, Family 1.0x, Fanatics 2.0x):

> [Summary in 2-3 sentences.]

---

## 4. Top Learnings

1. **What surprised us positively.** [One paragraph.]
2. **What surprised us negatively.** [One paragraph.]
3. **What the data confirms we should keep.** [Bullet list of features/flows the data supports.]
4. **What the data says we should cut or change.** [Bullet list with rationale.]

---

## 5. Testimonials and Reference Customers

| Participant | Company | Quote (draft) | Written Permission | Reference Tier |
|-------------|---------|---------------|:------------------:|:--------------:|
| [Name] | [Company] | "..." | [Yes/No] | [1/2/3] |
| [Name] | [Company] | "..." | [Yes/No] | [1/2/3] |
| [Name] | [Company] | "..." | [Yes/No] | [1/2/3] |

> Reference tiers: 1 = on-stage / case study; 2 = quotable in marketing; 3 = analyst reference only.

---

## 6. Open Bugs and Known Issues at Exit

| Severity | ID | Description | Plan |
|:--------:|----|-------------|------|
| P0 | | | Must fix before GA |
| P1 | | | Fix in first post-GA sprint |
| P2 | | | Track in backlog |

---

## 7. The Four-Outcome Decision

### Option A: Greenlight GA

- All gates met (or gaps explicitly accepted by exec sponsor).
- Launch date: [YYYY-MM-DD]
- Launch owner: [Name]
- Handoff to `launch-playbook/` confirmed.

### Option B: Extend Beta

- Gaps to close: [list]
- Extension length: [2-4 weeks]
- New exit-gate review date: [YYYY-MM-DD]
- Participant communication owner: [Name]
- Additional commitments to participants: [list]

### Option C: Pivot

- New hypothesis: [one sentence]
- Rewritten PRD owner: [Name]
- Beta participants we will carry forward: [count]
- Participant communication owner: [Name]
- Postmortem on original hypothesis: [link]

### Option D: Kill

- Reason: [one paragraph]
- Postmortem: [link]
- Code action: [Remove / Keep behind flag / Archive]
- Sunset communication to participants: [link, see `eol-communication/`]
- What we learned not to try again: [list]

---

## 8. Sign-Off

By signing below, the named stakeholders acknowledge the decision above and the next steps.

| Name | Role | Date | Decision Acknowledged |
|------|------|------|----------------------|
| | PM (DACI Driver) | | |
| | Engineering Lead | | |
| | Design Lead | | |
| | PMM | | |
| | Exec Sponsor (DACI Approver) | | |

---

## 9. Appendix: Raw Data Sources

- Gate metrics dashboard: [link]
- Participant 1:1 notes (consented summary): [link]
- Bug tracker view: [link]
- Pricing decision memo: [link]
- Beta program plan (signed): [link]
