---
name: launch-playbook
description: >
  Internal and external launch coordination playbook covering pre-launch,
  launch day, and post-launch with run-of-show, comms, rollback, and retro.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-execution
  updated: 2026-05-21
  tech-stack: launch, three-launches, dark-launch, raci, progressive-rollout
---
# Launch Playbook (Internal + External Coordination)

## Overview

A complete launch coordination playbook for software products and features. It covers the three windows that matter -- pre-launch (T-30 to T-1), launch day (T-0), and post-launch (T+1 to T+30) -- and produces five concrete artifacts: a run-of-show, an internal comms plan, an external comms checklist, a rollback plan, and a post-launch retro template.

Most failed launches are not failed builds; they are failed coordination. Engineering ships on time, but support has not been trained, sales does not have collateral, the changelog is wrong, the rollback path was never tested, and the executive sponsor hears about a customer complaint before hearing about the launch. This playbook prevents those failures by assigning every owner and every artifact before T-30.

The framework supports both "big bang" launches (single date, broad reach) and progressive rollouts (dark launch, ring deployment, feature-flag exposure curve). Use Marty Cagan's "three launches" model (alpha, beta, GA) to sequence and de-risk; use a RACI matrix to assign ownership across PM, Engineering, PMM, Sales, Support, and Legal.

### When to Use

- **GA after closed beta** -- A feature is exiting beta (see `beta-program/`) and needs coordinated launch.
- **Major version release** -- Significant new functionality with cross-functional dependencies (sales enablement, support training, legal review).
- **Re-launch / repositioning** -- An existing feature is being relaunched with new positioning, pricing, or audience.
- **High-blast-radius change** -- Infrastructure migration, pricing change, or breaking API change requiring tightly coordinated comms.

### When NOT to Use

- Continuous-delivery bug fixes and minor improvements (use `release-notes/` only).
- Internal-only changes with no external comms (skip launch playbook; use a release runbook).
- Product sunsets and deprecations (use `eol-communication/`).

## The Three Launches Framework

Marty Cagan's "three launches" model (popularized in *Inspired*, 2008/2018) sequences a launch into three windows that test different risks.

| Launch | Audience | Primary Risk Tested | Typical Duration |
|--------|----------|--------------------|-----------------|
| **Alpha** | Internal employees, dogfooding | Does it work at all? | 1-2 weeks |
| **Beta** | 10-30 closed external participants | Does it produce the outcome? Is it stable? | 4-8 weeks (see `beta-program/`) |
| **GA (Launch)** | All target users | Does the market care? Can we scale? | The launch event + 30-day stabilization |

This skill focuses on the GA launch. Alpha lives with engineering; Beta lives in `beta-program/`. By the time you open this playbook, both should be complete or in their final week.

## The Launch Timeline (T-30 to T+30)

### Pre-Launch (T-30 to T-1)

| Day | Workstream | Action |
|----:|-----------|--------|
| T-30 | All | Kickoff: confirm date, owner per workstream, exec sponsor |
| T-30 | PM + PMM | Positioning brief signed off |
| T-21 | Eng | Code freeze decision; rollout strategy (big bang vs progressive) confirmed |
| T-21 | Support | Runbook drafted; FAQ in progress |
| T-21 | Sales | Enablement deck drafted; pricing finalized |
| T-14 | Legal | Final review of public-facing copy, ToS changes, pricing pages |
| T-14 | Marketing | Press release, blog post, social copy, email campaign drafted |
| T-10 | Eng | Dark launch / feature flag toggled for internal verification |
| T-7 | All | Dry-run of the launch-day run-of-show; rollback drill |
| T-7 | Support | Team training completed; runbook published |
| T-7 | Sales | Reps trained; battle cards distributed |
| T-3 | All | Final go/no-go check against launch readiness checklist |
| T-2 | Marketing | Embargoed press outreach |
| T-1 | All | Final confirmation; on-call rota for launch day published |

### Launch Day (T-0)

Run from a single shared document (the run-of-show). Hourly cadence. Single incident commander. See `assets/launch-run-of-show.md`.

### Post-Launch (T+1 to T+30)

| Day | Workstream | Action |
|----:|-----------|--------|
| T+1 | PM + Eng | War-room standup: metrics, incidents, customer sentiment |
| T+1 | PMM | Launch-day metrics report to exec sponsor |
| T+3 | Support | First-3-days ticket triage; identify themes |
| T+7 | PM | Week-1 retrospective using `assets/post-launch-retro.md` |
| T+14 | PMM | Press coverage roundup; first-2-weeks adoption report |
| T+30 | All | 30-day retrospective; long-term metrics vs forecast |
| T+30 | PM | Decision: invest more / sustain / sunset / iterate |

## Launch Type Selection

### Big Bang

Single date, all users, full announcement. Use when:

- The product is stable, tested, and beta gates were met cleanly.
- Marketing leverage of a single date is critical (e.g., conference keynote).
- No technical risk that benefits from gradual exposure.

### Progressive Rollout

Stage exposure by feature flag, geography, account tier, or random percentage. Use when:

- Performance or scale risk that cannot be tested in beta volume.
- New billing flow, payment system, or anything that could lose customer money on failure.
- Migration that needs a clear rollback path per cohort.

### Dark Launch

Code is in production behind a flag, exercising real traffic and infrastructure, but not visible to users. Use when:

- You need to validate infrastructure under real load before any user-visible change.
- The feature has expensive backend dependencies (database migrations, indexing, queue capacity).

The three are not mutually exclusive: dark-launch the backend, then progressive-rollout the UI, then big-bang the announcement.

## RACI Matrix for Launches

| Workstream | PM | Eng | PMM | Sales | Support | Legal | Exec |
|-----------|:--:|:---:|:---:|:-----:|:-------:|:-----:|:----:|
| Positioning & messaging | A | C | R | C | I | C | I |
| Code freeze & deployment | I | R/A | I | I | I | I | I |
| Sales enablement | C | I | R | A | I | I | I |
| Support runbook & training | C | C | I | I | R/A | I | I |
| Legal & compliance review | C | I | C | I | I | R/A | I |
| External comms (PR, blog, social) | I | I | R/A | I | I | C | I |
| Internal comms (all-hands, FAQ) | R/A | I | C | I | C | I | I |
| Launch day run-of-show | R/A | C | C | I | C | I | I |
| Rollback decision | C | C | I | I | I | I | A |
| 30-day retrospective | R/A | C | C | C | C | I | I |

R = Responsible, A = Accountable, C = Consulted, I = Informed.

## Workflow

1. **Kickoff at T-30.** Confirm launch date, type (big bang / progressive / dark), and exec sponsor. Open `assets/launch-run-of-show.md` and `assets/internal-comms-plan.md`.
2. **Assign the RACI.** Every cell above is named within 48 hours of kickoff.
3. **Lock the positioning.** PMM owns; PM + Eng + Legal review. Signed off by T-21.
4. **Build the comms artifacts.** Internal comms plan (T-14), external comms checklist (T-10), customer email and press release (T-7).
5. **Test the rollback.** Engineering runs a rollback drill in staging by T-7. The result is documented in `assets/rollback-plan.md`.
6. **Run the dry-run.** At T-7, walk through the launch-day run-of-show with all owners present. Identify any unowned action.
7. **Go/no-go at T-3.** Use the launch-readiness checklist in `assets/external-comms-checklist.md`. Any "No" requires a documented mitigation or a launch postponement.
8. **Run launch day.** Single incident commander; hourly cadence; war room (physical or virtual) open from T-0 to end-of-day.
9. **Stabilize T+1 to T+7.** Daily war-room standup; rapid hotfix lane open; sales and support triage themes.
10. **Run the 30-day retro.** Use `assets/post-launch-retro.md`. Decide: invest more, sustain, iterate, or sunset.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Launch date slips repeatedly | Beta gates were not actually met; team launching on the calendar instead of the criteria | Reopen the beta exit memo from `beta-program/`; re-baseline date based on actual gate status |
| Sales has no idea the feature exists on launch day | Enablement workstream not assigned an owner; PMM assumed Sales would self-serve from the blog post | Add a named Sales Enablement Lead in the RACI by T-21; mandatory training session in week T-1 |
| Support overwhelmed in first 48 hours | Runbook published too late, no T-7 training, no on-call rota | Make Support runbook + training a T-7 launch gate; require named on-call schedule in the run-of-show |
| Press coverage misrepresents the feature | Embargoed materials skipped or PMM and PM had different messaging | Single shared positioning brief signed off by T-21; PMM-led press briefings only; one PR contact for all journalists |
| Rollback "tested" but fails in production | Drill was performed in staging with synthetic data; production differences not exercised | Run a production rollback drill (with a no-op feature) at T-14; document the result in `assets/rollback-plan.md` |
| Exec sponsor hears about a customer issue before hearing about the launch | No internal comms plan; #launches Slack channel never existed | Internal comms plan with exec briefing at T-1 and T+1; dedicated launch channel from T-30 |
| Post-launch metrics never reviewed | Team disbanded at T+1; nobody owns 30-day decision | Calendar-block the 30-day retro at kickoff; assign accountable PM in the RACI |

## Success Criteria

- All five launch artifacts (run-of-show, internal comms plan, external comms checklist, rollback plan, retro) are populated and signed off before T-7.
- Launch RACI has every cell assigned to a named individual by T-21.
- Rollback drill was successfully performed and documented by T-7.
- Go/no-go at T-3 has explicit approval from PM, Engineering, PMM, Support, Legal, and Exec Sponsor.
- Launch day runs from a single shared run-of-show with hourly cadence and single incident commander.
- Post-launch retrospective produces a 30-day decision (invest more / sustain / iterate / sunset) documented and shared with the exec sponsor.
- Zero unplanned customer-visible incidents in the first 24 hours, or any incidents have a documented timeline from detection to resolution.

## Scope & Limitations

**In Scope:**
- GA launch coordination across Engineering, Product, PMM, Sales, Support, Legal
- Run-of-show, rollback plan, comms plans, post-launch retrospective
- Big bang, progressive rollout, and dark launch patterns
- T-30 to T+30 timeline
- RACI assignment for cross-functional launches

**Out of Scope:**
- Beta program execution (use `beta-program/`)
- Release notes content generation (use `release-notes/`)
- End-of-life / sunset communication (use `eol-communication/`)
- Incident response runbooks (link to `delivery-manager/` and engineering on-call procedures)
- Marketing campaign performance analysis beyond the 30-day window (handoff to demand gen)

**Important Caveats:**
- A launch is not a moment; it is a 60-day window (T-30 to T+30). Plan staffing accordingly.
- The single most common cause of failed launches is a missing RACI assignment, not a missing artifact. If you can name the artifact but not the owner, the artifact will not exist.
- Big-bang launches concentrate risk on one date. They are appropriate when the marketing leverage justifies the risk; default to progressive rollout otherwise.

## Integration Points

| Integration | Direction | What Flows |
|-------------|-----------|------------|
| `beta-program/` | Receives from | Greenlit beta hands off testimonials, known issues, and pricing decision |
| `create-prd/` | Receives from | PRD provides positioning, segments, and v1 scope |
| `release-notes/` | Feeds into | Launch produces the GA release notes |
| `daci-framework/` | Uses | Major launch decisions (go/no-go, rollback) use DACI |
| `eol-communication/` | Complementary | Launches that replace older features trigger sunset comms |
| `delivery-manager/` | Uses | Deployment, on-call rota, and rollback execution |
| `senior-pm/` | Reports to | Exec sponsor receives T-1, T+1, T+7, T+30 updates |
| `summarize-meeting/` | Feeds into | War-room standups and retro produce structured summaries |
| `status-update-generator/` | Feeds into | Post-launch metrics roll up into weekly status |

## References

- `references/launch-coordination-guide.md` -- Full launch playbook: three-launches sequencing, RACI worked examples, big-bang vs progressive decision rules, anti-patterns.
- `assets/launch-run-of-show.md` -- Hourly run-of-show template for launch day.
- `assets/internal-comms-plan.md` -- Pre-launch, launch-day, and post-launch internal comms templates.
- `assets/external-comms-checklist.md` -- T-30 to T-0 checklist for press, blog, social, email, sales enablement, support training, and legal review.
- `assets/rollback-plan.md` -- Rollback decision matrix, drill checklist, and execution runbook template.
- `assets/post-launch-retro.md` -- 7-day and 30-day retrospective template.
- Cagan, Marty. *Inspired: How to Create Tech Products Customers Love*. Wiley, 2018.
