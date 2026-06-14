# Productboard Driver Template

Drivers are Productboard's prioritization criteria. Each Feature is scored against each Driver on a 0-10 scale; Drivers have weights that sum to 100%; the composite Feature score is the weighted average.

Drivers are the single highest-leverage configuration in a Productboard workspace. They turn strategy into a sortable list. Poor Driver design (vague criteria, mismatched weights, scoring scales without definitions) produces noise; well-designed Drivers produce decisions.

## How to design Drivers

1. Pick **3-5 Drivers**. More than 5 becomes noise; fewer than 3 gives insufficient resolution.
2. **Each Driver maps to a strategic dimension** the team weighs against. A common set: Revenue Impact, Strategic Fit, Customer Demand, Effort, Risk.
3. **Weights sum to 100%**. Higher-weight Drivers move scores more. Re-weight quarterly as strategy shifts.
4. **Each Driver has a defined 0-10 scoring scale with concrete anchors**. "5" should mean something specific, not just "medium".
5. **Drivers should be roughly orthogonal**. Two Drivers measuring nearly the same thing double-counts.

## Driver definition template

Copy this template for each Driver in the workspace:

```
## Driver: [Name]

Definition: [One paragraph: what this Driver measures, and what it does NOT measure.]

Weight: __%

Scoring scale (0-10):
  0  — [Concrete anchor]
  2  — [Concrete anchor]
  5  — [Concrete anchor]
  8  — [Concrete anchor]
  10 — [Concrete anchor]

How to score:
  - [Practical guidance for the PM scoring a Feature against this Driver]

Common mistakes:
  - [Anti-patterns to avoid]

Evidence required:
  - [What kind of evidence supports a score above 7]
```

## Worked examples

### Driver: Revenue Impact

**Definition**: The Feature's contribution to net new MRR, expansion MRR, and churn reduction over the next 12 months. Does NOT measure cost savings, brand value, or strategic alignment (those have their own Drivers).

**Weight**: 30%

**Scoring scale**:
- 0 — No measurable revenue impact within 12 months
- 2 — Small impact: < $50k ARR
- 5 — Moderate: $50k - $250k ARR
- 8 — High: $250k - $1M ARR
- 10 — Transformational: > $1M ARR

**How to score**:
- Pull from the financial model in Finance
- Use a range with a midpoint, not a single number
- Distinguish net new (new customers) vs expansion (existing customers buying more) vs retention (churn avoided); add them

**Common mistakes**:
- Scoring "10" because a single enterprise customer might churn — that's renewal-risk, score it under that Driver
- Scoring on revenue that's > 18 months out — too speculative

**Evidence required for score >= 7**:
- Linked Finance model
- Sales pipeline data
- Or specific customer commitment

---

### Driver: Customer Demand

**Definition**: The aggregate strength of customer evidence behind the Feature. Captures volume (how many distinct customers), recency (last 90 days), and intensity (urgency language, NPS impact). Does NOT measure individual customer revenue weight (that's Revenue Impact) or strategic fit.

**Weight**: 25%

**Scoring scale**:
- 0 — No customer evidence
- 2 — 1-3 linked Insights, mostly older than 6 months
- 5 — 5-15 linked Insights, mixed recency
- 8 — 15-30 linked Insights, mostly recent, with named accounts
- 10 — 30+ recent linked Insights, recurring across segments

**How to score**:
- Use Productboard's linked-Insights count as the starting point
- Adjust for recency: weight Insights from the last 90 days 2x
- Adjust for diversity: 10 Insights from 10 customers is stronger than 10 Insights from 1 customer

**Common mistakes**:
- Inflating the score because Sales is loud — Sales escalations are evidence, but no more than other channels
- Forgetting to refresh the score as new Insights accumulate

**Evidence required for score >= 7**:
- Linked Insights visible in Productboard
- Mix of channels (not 100% support or 100% sales)
- At least 5 distinct customers / companies

---

### Driver: Strategic Fit

**Definition**: How well the Feature advances the company's currently-stated strategic themes (Objectives). Does NOT measure customer demand or revenue (those are separate Drivers).

**Weight**: 20%

**Scoring scale**:
- 0 — Off-strategy or actively counter to current themes
- 2 — Tangentially related
- 5 — Supports a non-priority theme
- 8 — Directly advances a top-3 priority theme
- 10 — Critical to a top-1 priority theme; without this, the theme fails

**How to score**:
- Map the Feature to the current quarter's Objectives in Productboard
- If the Feature can't be mapped to an Objective, the score is at most 5
- Discuss with leadership when in doubt

**Common mistakes**:
- Inflating the score because the PM personally likes the Feature
- Failing to re-score when strategic themes shift (quarterly review fixes this)

**Evidence required for score >= 7**:
- Linked Productboard Objective
- Leadership endorsement

---

### Driver: Effort

**Definition**: Engineering and design effort to ship to a beta-quality release. Measured in T-shirt sizes mapped to weeks. Lower effort scores higher (inverse Driver). Does NOT measure operational complexity post-launch (separate consideration).

**Weight**: 15%

**Scoring scale**:
- 0 — XXL: > 6 months for one team
- 2 — XL: 3-6 months for one team
- 5 — L: 6-12 weeks for one team
- 8 — M: 2-6 weeks for one team
- 10 — S: < 2 weeks for one team

**How to score**:
- Get engineering's T-shirt size estimate; do not rely on PM intuition
- For multi-team Features, sum the effort
- Re-estimate after design / discovery; Effort scores often shift down after the team learns the work

**Common mistakes**:
- PM-only effort estimate; always confirm with engineering
- Estimating only the build, ignoring testing / launch / operational overhead

**Evidence required for score >= 7**:
- Engineering lead has confirmed estimate
- Comparable past Features delivered in similar time

---

### Driver: Risk

**Definition**: Probability and severity of negative outcomes from shipping (technical risk, compliance risk, customer-trust risk, security risk). Lower risk scores higher (inverse Driver).

**Weight**: 10%

**Scoring scale**:
- 0 — High risk: regulatory exposure, security implications, irreversible
- 2 — Moderate-high: significant customer-trust risk if it fails
- 5 — Moderate: typical technical risk
- 8 — Low: well-understood, reversible, isolated
- 10 — Negligible: small reversible change

**How to score**:
- Consult Engineering on technical risk
- Consult Legal/Compliance on regulatory risk
- Consult CS/Support on customer-trust risk

**Common mistakes**:
- Ignoring risk because the Feature is "small" — small Features can have big risks (security regression, compliance gap)
- Inflating risk to deprioritize a Feature the PM doesn't want to build

**Evidence required for score >= 7**:
- Engineering risk review
- Legal review if regulatory

---

## Weight reasoning (worked example)

A growth-stage SaaS company with the following themes:

- Strategic focus: "Move upmarket to mid-market and enterprise" (50% of strategic energy)
- Secondary: "Improve retention" (30%)
- Tertiary: "Activate self-serve more efficiently" (20%)

Driver weight rationale:

| Driver | Weight | Rationale |
|---|---|---|
| Revenue Impact | 30% | Upmarket motion is revenue-driven |
| Customer Demand | 25% | Customer signal is the gatekeeper for upmarket fit |
| Strategic Fit | 20% | Themes are explicit and shouldn't be drowned out |
| Effort | 15% | Effort always matters but isn't the deciding factor at this stage |
| Risk | 10% | Risk-aware but not risk-averse |

Re-weighting examples:

- If strategy shifts to "Defend the base / cut burn", Effort weight goes up and Revenue Impact weight goes down (smaller surface area, faster ROI matters more)
- If strategy shifts to "AI-first transformation", Strategic Fit weight goes up dramatically
- If strategy shifts to "Enterprise compliance year", Risk weight goes up and inverts (high-compliance Features score higher, not lower)

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| 7+ Drivers | Consolidate; some Drivers measure nearly the same thing |
| Scoring scale without anchors | Add concrete examples at 0, 5, 10 |
| Drivers that never get re-weighted | Quarterly review on the calendar |
| Effort Driver weighted > 30% | Effort becomes the dominant factor and small-fast wins crowd out strategic Features |
| Risk Driver weighted < 10% | Risk gets ignored; surprise compliance / security incidents follow |
| Customer Demand based on count alone | Adjust for recency and segment diversity |
| Strategic Fit gameable by whoever scores | Require linked Objective for score >= 7 |

## Quarterly Driver review

A 60-minute meeting with PM lead + leadership:

1. (15 min) Review the last quarter: which Features won the prioritization, did they ship, did they hit their success criteria?
2. (15 min) Review the current strategic themes (Objectives). Have they shifted? Are new themes emerging?
3. (15 min) Discuss whether Driver weights still reflect the strategy.
4. (15 min) Update weights in Productboard. Communicate the change to the PM team and document the rationale.

The quarterly cadence is the right rhythm: more often is destabilizing; less often lets the system drift.

## See also

- `assets/productboard-feature-template.md` — Feature description template
- `assets/productboard-insight-triage-workflow.md` — daily Insight triage SOP
- `references/productboard-api-patterns.md` — programmatic Driver / Objective access
