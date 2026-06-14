---
name: beta-program
description: >
  Closed beta program playbook covering recruitment, success criteria,
  communication cadence, and beta-to-GA exit gates.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-execution
  updated: 2026-05-21
  tech-stack: beta-program, kano-model, cohort-design, beta-to-ga-gates
---
# Closed Beta Program Playbook

## Overview

A structured playbook for running a closed beta that produces clear learning, retained design partners, and an unambiguous decision on whether to proceed to general availability. Most betas fail not because the product is wrong, but because the program is run informally: recruitment is opportunistic, success criteria are implicit, communication is sporadic, and exit gates are never defined. This skill replaces all of that with concrete templates and decision rules.

A good closed beta runs 4-8 weeks, recruits 10-30 participants from three concentric cohorts ("friends, family, fanatics"), publishes a weekly cadence the team commits to, and exits on pre-agreed criteria rather than the calendar. The outputs are a beta program plan, a recruitment script, a weekly cadence template, and an exit memo that either greenlights GA, extends the beta, or kills the feature.

### When to Use

- **Pre-GA validation** -- A feature has cleared internal alpha but needs external validation under real workloads before a public launch.
- **High-risk feature** -- Significant blast radius, regulatory exposure, or pricing changes that warrant a controlled rollout to a small group first.
- **Design partner program** -- Recruiting a small set of customers whose feedback shapes v1 scope and pricing.
- **Enterprise rollout** -- New module that needs reference customers and case studies before broad sales enablement.

### When NOT to Use

- Continuous trunk-based delivery where every change ships to all users behind feature flags (use `launch-playbook/` and a progressive rollout instead).
- Pure usability testing with 5-7 participants (use a research protocol, not a beta program).
- Internal-only dogfooding (run a 2-week alpha with engineering and customer-facing staff).

## The Closed Beta Framework

### Cohort Design: Friends, Family, Fanatics

A widely-used pattern (popularized by early-stage operators including Y Combinator partners) for sequencing beta recruitment in three concentric rings of decreasing trust and increasing signal.

| Cohort | Who | Goal | Typical Size | Tolerance for Rough Edges |
|--------|-----|------|--------------|---------------------------|
| **Friends** | Internal employees, advisors, immediate network | Find the worst bugs without reputational risk | 5-10 | Very high |
| **Family** | Existing customers who explicitly opted in, design partners | Validate the workflow fits real jobs and produces value | 10-20 | High |
| **Fanatics** | Cold-recruited prospects matching the ICP who actively want to solve the problem | Validate that the feature drives acquisition, not just retention | 10-15 | Medium |

Run the cohorts sequentially (Friends -> Family -> Fanatics) or with deliberate overlap. Do not skip Friends to "save time" -- this is where every embarrassing crash should surface.

### Kano Model for Beta Scope

Use the Kano model (Noriaki Kano, 1984) to decide what is in scope for the beta build:

| Kano Category | Definition | Beta Decision |
|---------------|------------|---------------|
| **Must-be** | Basic expectations; absence causes immediate dissatisfaction | Must be present and stable on day 1 of beta |
| **Performance** | More-is-better attributes that scale with investment | Include enough to demonstrate the value curve |
| **Delight** | Unexpected features that produce strong positive reactions | Pick 1-2 delight features for the beta -- this is where you generate quotes for the launch |
| **Indifferent** | Features the user does not care about | Cut from beta scope; revisit post-GA |
| **Reverse** | Features that some users actively dislike | Make them opt-in; track who turns them off |

The most common mistake is shipping a beta with only Must-be features. Without at least one Delight feature, your beta produces neutral feedback and no quotable testimonials.

### Beta Success Criteria (Set Before Recruitment)

Define quantitative and qualitative gates before opening recruitment. If you set them after the beta starts, they will be rationalized to match what you already see.

| Gate Type | Example Metric | Example Target |
|-----------|----------------|----------------|
| **Activation** | % of beta users who reach the first key action within 7 days | >= 70% |
| **Engagement** | Median sessions per active beta user per week | >= 3 |
| **Retention** | % of beta users still active in week 4 | >= 60% |
| **Outcome** | % of beta users who achieve the headline outcome (saves X minutes, reduces Y, etc.) | >= 50% |
| **NPS / CSAT** | Net Promoter Score within the beta cohort | >= 30 |
| **Crash-free sessions** | Crash-free session rate across beta | >= 99.5% |
| **P0 bug count** | Open P0 bugs at exit-gate review | 0 |
| **Quotable testimonials** | Named customers willing to be quoted in launch materials | >= 3 |

### Weekly Communication Cadence

A beta dies of silence. Commit to a weekly rhythm and publish it to participants on day 1.

| Day | Action | Owner |
|-----|--------|-------|
| **Monday** | Weekly digest to participants: what shipped, known issues, what to try this week | PM |
| **Tuesday** | Office hours (30 min open Zoom or async thread) | PM + Eng Lead |
| **Wednesday** | Internal beta health review: metrics, bugs, themes | PM |
| **Thursday** | One-on-one with rotating subset (2-3 participants/week) | PM or PMM |
| **Friday** | Weekly metrics snapshot posted to participants Slack/Discord | PM |

### Beta-to-GA Exit Gates

At the end of the planned beta window (typically 4-8 weeks), run an exit-gate review against the pre-agreed criteria. There are exactly four outcomes:

1. **Greenlight GA** -- All gates met. Proceed to launch using `launch-playbook/`.
2. **Extend beta** -- Most gates met, 1-2 gaps with a clear plan to close in 2-4 more weeks.
3. **Pivot** -- Engagement/outcome gates failed; usage pattern reveals a different job-to-be-done. Rewrite the PRD.
4. **Kill** -- Both engagement and outcome gates failed with no compelling alternative pattern. Write the postmortem and free the team.

The decision should be made by the DACI driver (see `daci-framework/`) with documented input from engineering, design, marketing, and at least one beta participant.

## Workflow

1. **Frame the beta.** Define the hypothesis, the target cohort definition, and the headline outcome you expect beta users to achieve. Reference the PRD from `create-prd/`.
2. **Set exit gates.** Fill in `assets/beta-program-plan.md` with quantitative and qualitative gates. Get explicit sign-off from PM, Engineering, and the executive sponsor.
3. **Build the recruitment funnel.** Use `assets/recruitment-script.md` to draft outreach for each of the three cohorts. Aim to over-recruit by 2x (expect 50% activation).
4. **Stand up the participant comms channel.** Slack Connect, Discord, or shared email list. Publish the weekly cadence on day 1.
5. **Run the cadence.** Hold weekly Monday digests, Tuesday office hours, Wednesday internal reviews, Thursday 1:1s, Friday metric snapshots. Use `assets/weekly-cadence-template.md`.
6. **Run the exit-gate review.** At week N, populate `assets/exit-memo.md` with actual data vs. each gate. The DACI driver picks one of the four outcomes.
7. **Communicate the decision.** Tell participants what happens next: GA timeline, extension plan, pivot, or sunset. Honor any commitments (early access, pricing, credits).
8. **Hand off to launch.** If greenlit, hand the beta artifacts (testimonials, case studies, known issues, gate data) to `launch-playbook/`.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Recruitment misses target by >50% | Recruitment script led with features instead of the participant's pain; cohort definition too narrow | Rewrite outreach to lead with the problem and the participant's payoff; widen the cohort by one dimension (industry, role, or company size) |
| Engagement collapses after week 2 | No clear "what to try this week" prompt; users hit a rough edge and bounced | Re-establish the Monday digest with a specific weekly task; ship a hotfix for the top friction point within the same week |
| Beta participants stop responding to outreach | Cadence is too heavy or asks generic questions | Cut to one async ping per week with a specific question tied to that week's release; offer credits for completed feedback |
| Exit-gate metrics look good but team has no quotes | Beta lacked Delight features; outreach never asked for permission to quote | Add 1-2 Delight features in an extension week; explicitly ask for quotable testimonials in the week-3 1:1 |
| Exec sponsor pushes to skip exit gates and ship | Gates were set without sponsor buy-in; gates conflict with a hard launch date | Re-run the decision with the DACI driver; document the override and the risk in `assets/exit-memo.md` |
| Beta drags 12+ weeks with no decision | No pre-agreed exit window; team keeps adding scope | Enforce a 6-week default; any extension requires a written 2-week plan with measurable gates |
| Participants leak the beta publicly | NDA was implied, not explicit; participants felt the embargo was unfair | Send a one-page beta agreement at activation; offer an early-public-praise window in the final week to channel enthusiasm |

## Success Criteria

- Recruitment hits >= 100% of the planned cohort size across all three rings (Friends, Family, Fanatics).
- Exit-gate criteria are documented, quantitative, and signed off before recruitment opens.
- Weekly cadence runs every week of the beta with documented attendance and themes.
- At least 50% of activated participants achieve the headline outcome by the exit-gate review.
- The exit-gate review produces a single documented decision (Greenlight / Extend / Pivot / Kill) within 5 business days of beta end.
- At least 3 named participants agree to be quoted in launch materials.
- Beta artifacts (gate data, testimonials, known issues, customer requests) are handed off to the launch team in a single bundle.

## Scope & Limitations

**In Scope:**
- Closed beta planning, recruitment, cadence, and exit-gate decisions
- Three-cohort sequencing (Friends, Family, Fanatics)
- Kano scoping for beta feature set
- Weekly communication templates and exit memo
- Beta-to-GA handoff to `launch-playbook/`

**Out of Scope:**
- Public open beta or waitlist management (different mechanics; treat as a soft launch via `launch-playbook/`)
- A/B testing and statistical experiment design (see `discovery/brainstorm-experiments/`)
- Pricing experiments (run a dedicated pricing test, not piggybacked on beta)
- Marketing campaign execution for the beta (light recruitment only; full GTM lives in `launch-playbook/`)

**Important Caveats:**
- A 30-person closed beta is not statistically representative. Treat outcome metrics as directional, not conclusive.
- Friends-cohort feedback is biased toward "this is great" -- weight Fanatics-cohort feedback 2x in the exit decision.
- If your beta participants are also paying customers, any service disruption is a real incident. Run beta features behind a feature flag with a documented rollback path (see `delivery-manager/`).

## Integration Points

| Integration | Direction | What Flows |
|-------------|-----------|------------|
| `create-prd/` | Receives from | PRD defines the hypothesis and headline outcome that beta gates measure |
| `discovery/identify-assumptions/` | Receives from | Riskiest assumptions become the beta's primary learning goals |
| `discovery/brainstorm-experiments/` | Complementary | Beta is one experiment type; brainstorm-experiments covers smaller/faster alternatives |
| `daci-framework/` | Uses | DACI driver owns the exit-gate decision |
| `launch-playbook/` | Feeds into | Greenlit beta hands testimonials, case studies, and known issues to launch |
| `release-notes/` | Feeds into | Beta release notes preview the GA changelog |
| `summarize-meeting/` | Complementary | Office hours and 1:1 notes become structured weekly summaries |
| `senior-pm/` | Reports to | Exec sponsor receives the exit memo and signs the GA decision |

## References

- `references/beta-program-guide.md` -- Full playbook reference: cohort sequencing, Kano model deep dive, exit-gate worked examples, common failure modes.
- `assets/beta-program-plan.md` -- Beta program plan template with gates, cohort sizing, timeline.
- `assets/recruitment-script.md` -- Email/DM templates for the three cohorts plus screening questions.
- `assets/weekly-cadence-template.md` -- Monday digest, Tuesday office hours, Wednesday review, Friday snapshot templates.
- `assets/exit-memo.md` -- Exit-gate decision memo template (Greenlight / Extend / Pivot / Kill).
- Kano, Noriaki. "Attractive Quality and Must-Be Quality." Journal of the Japanese Society for Quality Control, 1984.
