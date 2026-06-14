# Example: Pricing Page Redesign Rollout at Northwind SaaS

> Real-world scenario showing how to plan a staged geo rollout with a holdout group.

## Context

Northwind SaaS is a Series-B B2B subscription product. The Growth team has redesigned the pricing page after Van Westendorp research suggested customers found the current page confusing. The redesign moves from a 4-tier matrix to a 3-tier "good-better-best" with a usage estimator. Expected lift: 8-15% on free-trial start rate.

This is a high-stakes change -- pricing pages convert revenue. The PM (Hugo Aalto) needs a rollout plan that protects revenue if the redesign is worse than expected. He decides to use a staged geo rollout with a long-lived holdout to measure long-term effects.

## Inputs

- LaunchDarkly flag system in place
- 65% of revenue from US, 15% EU, 10% UK, 10% rest-of-world
- Free-trial start rate baseline: 4.2% of pricing-page visitors
- Minimum detectable effect (MDE) for the A/B: 0.5 percentage points (2-week run, ~80k visitors)
- Pricing experiments must comply with consumer-law principles in EU and UK (no "personalized price discrimination")
- Reversal plan: instant rollback to old page on flag-off

## Applying the skill

1. **Classified the flag** -- this is a release toggle (Fowler) with an embedded A/B experiment. Lifespan: 8 weeks max, retirement date 2026-07-22.
2. **Picked rollout shape**: geographic (low-risk region first) with a holdout, hybrid of shapes B + D.
3. **Defined gate criteria** between stages: free-trial start rate within MDE of control, no spike in support tickets on pricing confusion, paid-conversion rate not regressing.
4. **Wrote kill-switch criteria** in advance: any 24-hour drop > 1pp in free-trial start, or paid-conversion drop > 0.5pp.
5. **Named the flag clearly** using the team's convention: `pricing_page_redesign_v3_2026q2`.
6. **Set a 5% long-term holdout** that never gets exposed -- measures lift 90 days post-rollout.

Key decision quoted: *"The holdout group is sacred. 5% of US visitors never see the new page, even after rollout, so we can measure long-term effect in November."*

## The artifact

````markdown
# Pricing Page Redesign v3 -- Rollout Plan

**PM:** Hugo Aalto
**Eng owner:** R. Kim (Growth Eng)
**Flag:** `pricing_page_redesign_v3_2026q2`
**Flag type:** Release toggle (with embedded A/B experiment)
**Created:** 2026-05-22
**Retirement date:** 2026-07-22 (8 weeks; firm)
**Rollback owner:** R. Kim (eng on-call) -- single-click kill via LaunchDarkly

## Rationale

Pricing page redesign expected to lift free-trial start rate by 8-15% based on
Van Westendorp + usability testing (n=12). High revenue exposure: pricing
page receives ~40k US visitors / week. Staged geo rollout with a holdout
protects revenue if the redesign underperforms.

## Flag taxonomy

| Field | Value |
|---|---|
| Flag type | Release toggle |
| Lifespan | 8 weeks (firm retirement) |
| Owner | Hugo (PM) + R. Kim (Eng) |
| Kill-switch | Yes (one-click in LaunchDarkly) |
| Tested? | Yes -- killswitch drill 2026-05-19 |
| Experiment? | Yes -- 50/45/5 split with permanent holdout |

## Rollout shape

Hybrid of shape B (audience-first, geographic) + shape D (A/B with holdout).

### Stage timeline

| Stage | Audience | Split | Start | Hold for | Gate to next |
|---|---|---|---|---|---|
| 0. Dark launch | Production traffic shadowed; no UI change | 0% | 2026-05-26 | 3 days | No template render errors |
| 1. Internal | Acme employees + 50 invited beta testers | 100% see new | 2026-05-29 | 3 days | No P0 + visual QA pass |
| 2. AU + NZ (low-risk region) | New 50%, Old 45%, Holdout 5% | 50/45/5 | 2026-06-02 | 7 days | Free-trial start rate within MDE; no support-ticket spike |
| 3. UK + IE | Same split | 50/45/5 | 2026-06-09 | 7 days | Same |
| 4. EU (GDPR-compliant labeling) | Same split | 50/45/5 | 2026-06-16 | 7 days | Same |
| 5. US (final, largest cohort) | Same split | 50/45/5 | 2026-06-23 | 14 days | Same |
| 6. Decision day | -- | -- | 2026-07-07 | -- | Roll 100% (minus 5% holdout) or rollback |
| 7. Long-term holdout measurement | -- | 5% never exposed | 2026-07-08 onward | 90 days | Measure long-term lift in October |

### The holdout group

5% of every region's visitors are assigned to a permanent holdout cohort and continue to see the old pricing page **even after the new page rolls to 100%**. The holdout is sticky by browser fingerprint + cookie + IP-class. It lets the team measure long-term lift in Q4 (90 days post-rollout) by comparing the holdout to the rolled-out population.

Holdout group is documented in the experimentation registry and cannot be cleared without explicit team-lead approval.

## Gate criteria (per stage)

| Metric | Threshold | Source |
|---|---|---|
| Free-trial start rate (test vs control) | Test >= Control - 0.5pp | Amplitude |
| Paid conversion rate (trial -> paid, 14d window) | Test >= Control - 0.3pp | Internal billing dashboard |
| Support tickets tagged "pricing-confused" | < 1.2x baseline | Zendesk |
| Page load p95 (new vs old) | New <= Old + 100ms | Datadog RUM |
| Bounce rate on pricing page | Test <= Control + 2pp | Amplitude |
| Net Promoter survey on pricing clarity | Test >= Control - 5 | In-app survey |

Gates evaluated at end of each hold period. Stage advances only if all gates pass; otherwise hold or rollback.

## Kill-switch criteria

Any one of these triggers immediate rollback (no committee needed; R. Kim flips the flag and notifies):

- 24h drop > 1pp in free-trial start rate (test cohort vs prior 7-day baseline)
- 24h drop > 0.5pp in paid-conversion rate
- 24h spike > 3x in "pricing-confused" support tickets
- Sev1/Sev2 incident attributed to the new page

Rollback action: set flag to 0% in all environments; old page restored. Estimated time: < 30 seconds from decision to fully rolled back.

## Statistical design

| Parameter | Value |
|---|---|
| Primary metric | Free-trial start rate |
| Hypothesis (XYZ) | "We believe the redesign will lift free-trial start rate by 0.5pp (4.2% -> 4.7%) within 4 weeks at the 95% confidence level." |
| MDE | 0.5pp |
| Power | 80% |
| Significance | 95% (two-sided) |
| Sample needed | ~80,000 visitors per arm |
| Expected duration to power | 9-14 days at US volume |
| Holdout cohort | 5% permanent |

If the test fails to reach significance by end of US stage (day 14), the decision is "no detectable effect" and the rollout proceeds only if the test arm is not worse than control. Inconclusive is not "ship anyway".

## Decision tree

```
Stage 2-5 daily check:
  IF any kill-switch triggered:
    -> Flag to 0% in that region; root cause; post-mortem (use ../post-mortem/)
  IF gates pass AND hold period complete:
    -> Advance to next stage
  IF gates fail (not kill-switch level) AND hold period complete:
    -> Pause; investigate; either fix and retry stage, or rollback

Stage 6 (decision day, 2026-07-07):
  IF test arm beat control significantly:
    -> Roll to 100% minus holdout; declare experiment success
  IF test arm matched control (within MDE):
    -> Roll to 100% minus holdout (still a wash, but the new page is the
       stronger long-term bet); declare inconclusive primary
  IF test arm underperformed control:
    -> Rollback; new design back to drawing board
```

## Communications

| Audience | What | When | Channel |
|---|---|---|---|
| Support team | New page is live in {region}; common questions | Day before each stage | Slack briefing |
| Sales team | Pricing page change; how to reference in deals | Day before stage 5 (US) | Sales enablement |
| Account managers | Heads-up for existing customers | Day before stage 5 | Email |
| Exec team | Daily metrics dashboard | Stages 2-5 | Notion page |
| Public | No public announcement during experiment | -- | -- |
| Public | Public announcement after stage 6 if successful | T+1 of decision day | Blog post |

## Flag retirement plan (firm)

| Date | Action | Owner |
|---|---|---|
| 2026-07-07 | Decision day | Hugo + R. Kim |
| 2026-07-08 | Begin holdout-only logic (5% on old page, 95% on new) | R. Kim |
| 2026-07-22 | Flag code cleaned up; old-page code path removed except behind holdout flag | R. Kim |
| 2026-10-07 | 90-day holdout measurement complete | Hugo |
| 2026-10-14 | Holdout retired; everyone on new page; flag code fully removed | R. Kim |

If the flag is not retired by 2026-10-14, it becomes flag debt; ticket auto-created in the flag-debt board.

## Regional / regulatory notes

- **AU + NZ:** no regulatory adjustments; standard A/B.
- **UK:** consumer-law principles -- no personalized pricing per-individual; the A/B varies design, not price. Cleared by Legal.
- **EU (GDPR):** experiment assignment uses anonymous cookie; no personal data leaves the EU. Cleared.
- **US:** standard A/B.

## Pre-launch checklist

- [x] Flag created in LaunchDarkly with retirement date
- [x] Kill-switch drilled (2026-05-19)
- [x] Experiment registered in experimentation registry
- [x] Legal sign-off (EU + UK)
- [x] Support team briefed
- [x] Datadog RUM dashboard configured
- [x] Amplitude dashboard configured
- [x] Holdout cohort logic verified (5% sticky)
- [ ] Stage 0 (dark launch) start: 2026-05-26
- [ ] Daily metrics review by Hugo at 11:00 each day during stages 2-5

## What we are NOT doing

- We are NOT personalizing prices per visitor (would violate UK/EU consumer-law principles).
- We are NOT running this experiment in regions where pricing display is regulated differently (we have one global price; the experiment is design, not price level).
- We are NOT skipping a region to save time; the staged geo rollout is the protection.
- We are NOT treating the holdout as "we'll see if anyone notices"; it has a documented owner, a documented removal date, and a measurement plan.
````

## Why this works

- The flag has a firm retirement date set at creation -- treats "release toggle" as a Fowler-class flag that must die.
- The kill-switch criteria are numeric and pre-agreed, so an on-call engineer can roll back without paging the PM at 2am.
- The 5% holdout is documented as sacred, with an owner, a sticky-assignment mechanism, and a 90-day measurement plan. This is the move that surfaces long-term lift, not just short-term test-vs-control.
- Geographic staging (AU first, US last) limits revenue exposure to ~3% of traffic per low-risk stage.
- Legal sign-off in EU + UK before launch -- not after a complaint -- avoids the "rolled out, then had to roll back" failure mode.

## What's next

- Pair with [../pricing-prd/](../pricing-prd/) if the redesign changes pricing model, not just page design.
- Use [../post-mortem/](../post-mortem/) if the kill-switch fires.
- Use [../launch-playbook/](../launch-playbook/) for the post-rollout public announcement on T+1 of decision day.
- Feed long-term holdout results into [../north-star-metric/](../north-star-metric/) as the canonical NSM lift measurement.
- Use [../status-update-generator/](../status-update-generator/) to surface daily metrics to exec during stages 2-5.
