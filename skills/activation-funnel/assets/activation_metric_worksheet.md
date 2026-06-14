# Activation Metric Worksheet

A structured exercise for deriving (or auditing) the activation event for your product. Based on Sean Ellis's activation-rate framework.

**Product:** ____________________
**PM owner:** ____________________
**Date:** 2026-05-22
**Cohort window:** ____________________

---

## Step 1: Pull the retention cohorts

From your event store, pull:

- **Cohort A (retained):** users who were still active at D30 (or your chosen retention horizon).
- **Cohort B (churned):** users who signed up in the same window and were NOT active at D30.

Make sure both cohorts are filtered the same way (same product version, same plan tier, same segment).

| Metric | Cohort A (retained) | Cohort B (churned) |
|---|---|---|
| N | | |
| Average sessions in week 1 | | |
| Average events in week 1 | | |
| % paid users | | |
| % invited a teammate | | |

## Step 2: List candidate events

List the 10-20 most common events users perform in their first session / first week. Examples:

- Signed up
- Verified email
- Created a workspace / project / file
- Invited a teammate
- Added a contact / record
- Sent a message
- Made a payment
- Connected an integration

| # | Event name | Common? (Y/N) |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| ... | | |

## Step 3: Compute lift per candidate event

For each candidate event, compute:

- **% of Cohort A who did it** in their first week
- **% of Cohort B who did it** in their first week
- **Lift** = A_share - B_share (in percentage points)
- **Lift ratio** = A_share / B_share

| Event | % of A | % of B | Lift (pp) | Lift ratio |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

The event with the **highest lift** is the leading candidate.

## Step 4: Find the threshold

For the leading event, the question is no longer "did they do it" but "how much / how often / how many."

Pull the distribution of that event count in week 1 for both cohorts.

| Event count | % of A | % of B |
|---|---|---|
| 0 | | |
| 1 | | |
| 2 | | |
| 3 | | |
| 5 | | |
| 10 | | |
| 20 | | |

Look for the threshold where the retained cohort's curve diverges from the churned cohort's curve. That threshold is your candidate activation event count.

**Threshold chosen:** ____________________

## Step 5: Validate the activation event

The activation event candidate now reads:

`<event> at least <threshold> times within <window>`

For example: "Sent a message at least 3 times within the first 7 days."

Validate:
- [ ] It is **specific** (count + action + window).
- [ ] It is **observable** (existing event instrumentation).
- [ ] It is **predictive** (lift > 30 percentage points between cohorts).
- [ ] It is **achievable in a short window** (most users reach it without effort if onboarding is good).
- [ ] It is **self-discovered** (users do it because the product is useful, not because we forced them).

If any check fails, iterate.

## Step 6: Project current activation rate

Among the latest signup cohort:

- N total signups: ____________________
- N who hit the activation event: ____________________
- Activation rate: ____________________

## Step 7: Identify the path to activation

For users who **did** activate, what is the most common sequence of events leading up to the activation event?

| Order | Event | % of activated users who did this step |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

This becomes the **activation path**. Optimizing the funnel between these steps is the path of highest leverage.

## Step 8: Identify failure paths

For users who **did NOT** activate, where did they drop off?

| Step in the activation path | % of un-activated users who got here | % who proceeded to next step |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |

The step with the biggest drop is the bottleneck. Run the full `funnel_analyzer.py` analysis on this path to surface it formally.

## Step 9: Counter-metrics

For the activation event, define the counter-metric that must not degrade:

- [ ] **D7 retention of activated users** must stay above X%. (If you lower the activation bar to inflate the rate, this drops.)
- [ ] **D30 retention of activated users** must stay above Y%. (Longer-term version.)
- [ ] **Engagement depth per activated user** must stay above Z events/day. (Activated users should be engaged users.)

## Step 10: Lock and document

The activation event is **locked** when:
- [ ] PM, ML/Analytics, and Eng have signed off.
- [ ] The event is instrumented and queryable.
- [ ] The threshold is documented.
- [ ] Counter-metrics are documented and reviewed weekly.
- [ ] The event is referenced in the NSM tree (`north-star-metric/`) and in OKRs.

**Final activation event:** ____________________

**Sign-offs:**

| Role | Name | Date |
|---|---|---|
| PM | | |
| Analytics | | |
| Eng lead | | |

## Re-validation

The activation event should be re-validated every 6 months:
- [ ] Does the lift still hold on the latest cohort?
- [ ] Has the threshold drifted (event-count distribution changed)?
- [ ] Has the path to activation changed because of UX updates?

If the activation event no longer predicts retention, it is no longer the right event. Re-derive.
