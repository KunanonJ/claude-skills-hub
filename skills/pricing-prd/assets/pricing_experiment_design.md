# Pricing Experiment Design Worksheet

Complete this worksheet before launching any pricing A/B test. The discipline of writing it in advance prevents motivated stopping, p-hacking, and metric-shopping mid-experiment.

## 1. Hypothesis

> Write the hypothesis in a single paragraph that states: the change, the primary metric, the predicted direction and magnitude, the guardrail metric and threshold, and the duration.

**Example**: "Raising the Pro tier price from $29 to $39 will increase ARPU among new sign-ups by ≥ 15% relative to the control arm, without dropping conversion-to-paid more than 8 percentage points relative, measured over a 6-week test period. We will read out at 6 weeks for the primary metric and at 12 weeks plus 90-day cohort retention for the durability metric."

**Hypothesis:**

(write here)

## 2. Test arms

| Arm | Description | Traffic % |
|---|---|---|
| Control | Existing pricing | __% |
| Variant A | New pricing | __% |
| (optional) Variant B | Alternative new pricing | __% |

## 3. Eligibility

- Who is eligible: (new sign-ups / anonymous visitors / all visitors / specific segment)
- Who is excluded: (logged-in existing customers, internal traffic, specific geos)
- Allocation method: random assignment / hash-based / cookie-based
- Persistence: arm assignment persists for __ days

## 4. Metrics

### Primary

| Metric | Definition | Direction | Significance threshold |
|---|---|---|---|
| | | + / − | p < 0.05 |

### Secondary (guardrail)

| Metric | Definition | Direction | Threshold for concern |
|---|---|---|---|
| | | | |
| | | | |

### Tertiary (observational)

| Metric | Definition |
|---|---|
| | |
| | |

## 5. Sample size and power

| Parameter | Value |
|---|---|
| Baseline conversion / ARPU | |
| MDE (relative) | |
| Power | 80% |
| Significance | 5% (two-sided) |
| Computed sample size per arm | n = |
| Expected weekly traffic | |
| Required test duration | __ weeks |

## 6. Mix-shift detection

| Dimension | Capture method |
|---|---|
| Acquisition channel | UTM tags |
| Segment | self-reported / firmographic |
| Geography | Geo-IP |
| Plan tier distribution | post-conversion |
| Device | UA parsing |

Re-compute primary metric within each segment to detect mix-shift confounds.

## 7. Holdout

- Post-rollout holdout: __% on control pricing
- Duration: 90-180 days
- Reason: causal attribution after rollout; durable-effect monitoring

## 8. Stop conditions

Stop the experiment early IF:

- Variant churn at 30 days > control churn at 30 days + __ percentage points
- Variant conversion drop > __ percentage points absolute
- Support ticket rate in variant > __x baseline for __ consecutive days
- Legal or PR escalation requires pause
- Critical bug in the experiment infrastructure

Do NOT stop early because the primary metric reaches significance ("peeking"). The pre-registered readout date is fixed.

## 9. Readout plan

| Window | What we read out | Decision |
|---|---|---|
| Day __ (planned end) | Primary metric significance | Roll out / extend / rollback / iterate |
| Day 30 | Conversion + 30-day retention | Re-evaluate if delayed effect |
| Day 90 | Cohort LTV approximation | Final go / no-go on permanent rollout |
| Day 180 | Holdout comparison | Confirm long-term causal effect |

## 10. Pre-registration

- This document committed to version control on: YYYY-MM-DD
- Pre-registration link / commit hash: ...
- Approved by: PM, Finance, Data Science / Analytics

## 11. Decision authority

| Decision | Authority | Approvers |
|---|---|---|
| Launch test | PM | PM, Eng, Legal |
| Pause / rollback | PM (immediate) | PM with VP P&E sign-off post-hoc |
| Permanent rollout | VPE or equivalent | PM, Finance, VPE |
| Pricing change rollback after permanent rollout | VPE + CFO | |

## 12. Post-test analysis

After the test concludes:

- [ ] Compute primary metric with 95% confidence interval
- [ ] Compute secondary metrics with 95% confidence interval
- [ ] Decompose effect by segment (mix-shift check)
- [ ] Audit for sample-ratio mismatch (SRM)
- [ ] Audit for novelty / primacy effects (compare first vs last week)
- [ ] Write the readout document
- [ ] Make the decision in a documented forum

## Appendix: Common pitfalls (quick check)

- [ ] Test is not optimizing conversion at the expense of ARPU
- [ ] Test does not include existing customers
- [ ] Pricing page change is not bundled with the price change
- [ ] No sequential peeking; readout is pre-registered
- [ ] Sample size is sufficient for the MDE
- [ ] All required jurisdictions reviewed for legal exposure
