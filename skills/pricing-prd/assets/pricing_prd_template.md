# Pricing PRD: [Change Name]

| Field | Value |
|---|---|
| **Version** | 1.0 |
| **Author** | (PM) |
| **Reviewers** | PM, Finance, Legal, Marketing, Sales, Eng |
| **Status** | Draft / In Review / Approved / Shipped |
| **Target launch date** | YYYY-MM-DD |
| **Linked strategy doc** | (link to `business-growth/pricing-strategy/` output) |

---

## 1. Summary

> 3-5 sentences. What is the pricing change? Why now? What are the headline metrics we expect to move?

---

## 2. Background

### Current state

- Current pricing model: (tier / usage / hybrid)
- Current tiers and prices: ...
- Current ARPU, conversion rate, gross margin, churn — baseline numbers

### Why now

- Market context: (competitor pricing moves, willingness-to-pay shifts, customer feedback)
- Internal context: (financial targets, product changes, segment evolution)
- What changed: (new capability, new segment, new constraint)

### Willingness-to-pay research

| Method | Date | Sample | Findings |
|---|---|---|---|
| Van Westendorp PSM | YYYY-MM | n=___ | OPP=$__, IPP=$__, RAP=$__-$__ |
| Conjoint | (or N/A) | | |
| Competitor benchmark | YYYY-MM | n=___ competitors | Range $__-$__ |
| Customer interviews | YYYY-MM | n=___ | Qualitative WTP signals |

---

## 3. Objective

### Business benefit

- Primary metric: (ARPU / conversion / gross margin / LTV)
- Predicted change: ± __% in __ days

### Customer benefit

- (How does the change improve the customer's outcome? Be honest — sometimes the customer benefit is fairness, predictability, or value clarity rather than a lower price.)

### Key Results

| KR | Baseline | Target | Date |
|---|---|---|---|
| ARPU (new sign-ups) | $__ | $__ | YYYY-MM-DD |
| Conversion rate | __% | __% | YYYY-MM-DD |
| Gross margin | __% | __% | YYYY-MM-DD |
| 90-day cohort retention | __% | __% | YYYY-MM-DD |

---

## 4. Market Segments

| Segment | Size (customers / revenue) | Current ARPU | Target ARPU | WTP band |
|---|---|---|---|---|
| SMB | | | | |
| Mid-market | | | | |
| Enterprise | | | | |

---

## 5. Pricing Model

- **Chosen model**: Tier / Usage / Hybrid / Per-seat / Outcome
- **Rationale**: ...
- **Models considered and rejected**:
  - ...
  - ...

---

## 6. Packaging

### Tier structure

| Tier | Target archetype | Value carrier(s) | Boundary metric |
|---|---|---|---|
| Good | | | |
| Better | | | |
| Best | | | |

### Pricing table

| Tier | Price (monthly) | Price (annual) | Annual discount |
|---|---|---|---|
| Good | $__ | $__ | __% |
| Better | $__ | $__ | __% |
| Best | $__ | $__ | __% |

### Trial mechanism

- Type: free tier / time-bounded trial / reverse trial / sales-led
- Duration / limits: ...
- Conversion trigger: ...

---

## 7. Grandfathering

- **Policy**: Permanent / Time-bounded (__ months) / No grandfathering
- **Affected customers**: __ customers, __% of MRR
- **Migration mechanism**: auto / opt-in / opt-out
- **Rate-limit**: no customer pays more than __% more YoY without explicit re-signature
- **Legal review status**: completed / pending (region-specific notes below)

---

## 8. Communication Plan

| Channel | Audience | Lead time | Owner | Status |
|---|---|---|---|---|
| Sales enablement (battle card + FAQ) | AEs, SDRs, CSMs | 4 weeks pre-launch | | |
| Support enablement (macros + escalation) | Support agents | 2 weeks pre-launch | | |
| Customer email (existing customers) | All paying customers | 8 weeks pre-launch | | |
| Customer email (grandfathered cohort) | Affected customers | 8 weeks pre-launch | | |
| In-app banner / modal | Logged-in users | Launch day | | |
| Pricing page | Public | Launch day | | |
| Status page note | Public | Launch day | | |
| Blog post | External | Launch day or 24h pre | | |
| Press / analyst brief (if strategic) | Analysts, press | 1-2 weeks pre-launch | | |

Drafts of customer communication attached as appendices.

---

## 9. A/B Test Design

(Skip if rolling out without an A/B; document the rationale below.)

| Element | Detail |
|---|---|
| **Hypothesis** | (one paragraph, with primary metric and threshold) |
| **Primary metric** | (ARPU per visitor / conversion rate / etc.) |
| **Secondary metrics** | (activation, downgrade, churn, support volume) |
| **MDE** | (e.g. 10% relative on ARPU) |
| **Power / significance** | 80% / 5% |
| **Sample size per arm** | n = __ |
| **Test duration** | __ weeks |
| **Holdout** | __% on old pricing, persistent for 90 days post-rollout |
| **Stop conditions** | (e.g. variant churn > control churn + 3pp; conversion drop > 10pp relative) |
| **Eligibility** | (new sign-ups only / anonymous visitors only / etc.) |
| **Legal review** | (jurisdictions checked) |

---

## 10. Rollback Criteria

Rollback thresholds written in advance, not improvised during the rollout:

| Condition | Threshold | Action | Decision authority |
|---|---|---|---|
| Conversion drops | > __pp relative for > __ days | Pause new traffic; investigate | |
| Existing-customer churn | > __x baseline 30-day churn | Pause comm; offer cohort price freeze | |
| Support volume | > __x baseline for > __ days | Add capacity; reassess comm | |
| Public sentiment | Sustained negative, > __ mentions / 24h | PR response; consider price freeze | |
| Revenue net impact | Below P10 financial projection | Reassess with Finance | |

---

## 11. Regional Pricing

| Region | Currency | Tax treatment | PPP adjustment | Payment methods | Notes |
|---|---|---|---|---|---|
| US/Canada | USD | Exclusive | None | Card, ACH | |
| EU | EUR | Inclusive | None | Card, SEPA, iDEAL | EU consumer law disclosures |
| UK | GBP | Inclusive | None | Card, BACS | |
| LATAM | (USD or local) | | (decision) | | |
| APAC | | | | | |
| MEA | | | | | |

---

## 12. Pricing Page UX

- Page mockup link: ...
- Reviewed against `assets/pricing_page_checklist.md`: yes / no
- Open UX issues: ...

---

## 13. Release & Success Criteria

### Phased rollout

| Phase | Cohort | Date | Exit criteria to next phase |
|---|---|---|---|
| Phase 0 — Internal | Employees | T-2 weeks | No critical bugs |
| Phase 1 — A/B on new sign-ups | __% traffic | T-0 | A/B test reaches significance or duration |
| Phase 2 — Full rollout new sign-ups | 100% traffic | T+__ | No rollback triggers hit |
| Phase 3 — Existing customer migration | Grandfathering cohort | T+__ months | Migration completion |

### Success criteria

- All 13 sections complete and reviewed by PM, Finance, Legal, Marketing, Sales, Eng
- A/B test (if applicable) reaches significance on primary metric
- 90-day post-launch retro shows metrics within ± 20% of projection
- Customer support volume returns to baseline within 30 days
- Sales-quoted price matches listed price 95%+ of the time

### Explicit deferrals

- (What is in scope for this PRD vs deferred to a future change)

---

## Sign-off

| Role | Name | Signed | Date |
|---|---|---|---|
| PM | | | |
| Finance | | | |
| Legal | | | |
| Marketing | | | |
| Sales | | | |
| Eng | | | |

---

## Appendices

- A. Customer email drafts (existing customers, grandfathered cohort)
- B. Sales battle card and FAQ
- C. Support enablement macros
- D. Pricing-page mockups
- E. A/B test analysis plan
- F. Financial model (link)
- G. Legal review notes (regions)
- H. Competitor pricing comparison (date of capture)
