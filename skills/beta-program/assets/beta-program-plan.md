# Beta Program Plan: [Feature / Product Name]

**Owner (PM):** [Name]
**Engineering Lead:** [Name]
**Exec Sponsor:** [Name]
**Start Date:** [YYYY-MM-DD]
**Planned Exit-Gate Review:** [YYYY-MM-DD]
**Document Status:** [Draft / Signed Off / In-Flight / Closed]

---

## 1. Hypothesis

We believe that [target user] will [adopt behavior / achieve outcome] because [reason rooted in evidence]. We will know this is true when [observable signal].

**Linked PRD:** [link]
**Linked Riskiest Assumptions:** [link to `identify-assumptions/` output]

---

## 2. Headline Outcome

The single user-facing outcome this beta proves or disproves:

> [Example: "A new project manager can publish a portfolio status report in under 5 minutes that their VP rates 4+ out of 5 for clarity."]

---

## 3. Cohorts

| Cohort | Target Size | Source | Recruiter | Recruitment Window |
|--------|------------:|--------|-----------|-------------------|
| Friends | [5-10] | [Internal Slack, advisor network] | [Name] | [Week -2 to -1] |
| Family | [10-20] | [CS warm intros, existing customers] | [Name] | [Week -1 to +1] |
| Fanatics | [10-15] | [Cold outreach, community] | [Name] | [Week +1 to +3] |
| **Total** | **[25-45]** | | | |

---

## 4. Scope (Kano Categorization)

| Feature | Kano Category | In Beta? | Notes |
|---------|---------------|:--------:|-------|
| [Feature A] | Must-be | Yes | Stable on day 1 |
| [Feature B] | Performance | Yes | Demonstrates value curve |
| [Feature C] | Delight | Yes | Quotable testimonial target |
| [Feature D] | Indifferent | No | Defer to post-GA |
| [Feature E] | Reverse | Opt-in | Track opt-out rate |

---

## 5. Exit Gates

All gates must be measurable, with a baseline, target, and owner. If any gate is "TBD" at sign-off, the beta does not start.

### Activation Gates

| Gate | Baseline | Target | Owner |
|------|----------|--------|-------|
| % of activated users reaching first key action within 7 days | n/a | >= 70% | PM |
| Median time-to-first-action | n/a | <= 24 hours | PM |

### Engagement Gates

| Gate | Baseline | Target | Owner |
|------|----------|--------|-------|
| Median sessions/week (active users, weeks 2-4) | n/a | >= 3 | PM |
| % of activated users still active in week 4 | n/a | >= 60% | PM |

### Outcome Gates

| Gate | Baseline | Target | Owner |
|------|----------|--------|-------|
| % of activated users who achieve the headline outcome | n/a | >= 50% | PM |
| Median NPS within active cohort | n/a | >= 30 | PM |

### Quality Gates

| Gate | Baseline | Target | Owner |
|------|----------|--------|-------|
| Open P0 bugs at exit-gate review | 0 | 0 | Eng Lead |
| Crash-free session rate | n/a | >= 99.5% | Eng Lead |

### Launch-Readiness Gates

| Gate | Baseline | Target | Owner |
|------|----------|--------|-------|
| Quotable testimonials (named, written permission) | 0 | >= 3 | PMM |
| Support runbook published and team trained | No | Yes | Support Lead |
| Pricing decision finalized and communicated | No | Yes | PM + Exec |

---

## 6. Timeline

| Week | Milestone |
|-----:|-----------|
| -2 | Friends cohort recruited, NDA sent, environment provisioned |
| -1 | Friends cohort activated; sanity-test the cadence and tooling |
| 1 | Family cohort recruitment closes; weekly cadence begins |
| 2 | Fanatics cohort recruitment opens |
| 3 | Mid-beta health check against gates; adjust if needed |
| 4 | Fanatics activation complete; 1:1s with reference candidates |
| 5-6 | Optimization week(s); close gate gaps |
| 7 | Exit-gate data freeze; populate exit memo |
| 8 | Exit-gate decision: Greenlight / Extend / Pivot / Kill |

---

## 7. Communication Plan

- **Channel:** [Slack Connect / Discord / dedicated email list]
- **Monday digest:** PM, by 10:00 local
- **Tuesday office hours:** PM + Eng Lead, 30 min
- **Wednesday internal review:** PM, gate metrics + bugs + themes
- **Thursday 1:1s:** PM, 2-3 participants/week, rotating
- **Friday snapshot:** PM, gate dashboard + one learning

---

## 8. NDA, Pricing, and Commitments

- **NDA:** [One-page mutual; sent at activation]
- **Pricing during beta:** [Free / Discounted / Paid trial]
- **Pricing at GA:** [State the exact price now]
- **Renewal commitment:** [If applicable: locked rate for X months]
- **Reference rights:** [Opt-in only; written permission per use]

---

## 9. Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|:----------:|:------:|------------|-------|
| Fanatics conversion <5% | Medium | High | Rerun positioning before scaling outreach | PM |
| P0 bug surfaces in week 1 | Medium | High | Hotfix within 48h; extend Friends phase if needed | Eng Lead |
| Exec sponsor pushes to skip exit gates | Low | High | Documented sign-off on gates before recruitment | PM |
| Participant drop-off after week 2 | Medium | Medium | Personal outreach in week 1; ship a delight feature in week 3 | PM |

---

## 10. Sign-Off

By signing below, the named stakeholders agree to the gates above and accept the four-outcome exit-gate framework (Greenlight / Extend / Pivot / Kill).

| Name | Role | Date | Signature |
|------|------|------|-----------|
| | PM | | |
| | Engineering Lead | | |
| | Exec Sponsor | | |
