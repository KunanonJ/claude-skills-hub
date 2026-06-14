# Example: GA Launch Playbook for Acme Analytics Shared Dashboards

> Real-world scenario showing how to apply the launch playbook end-to-end.

## Context

Acme Analytics is launching "Shared Dashboards" at its annual user conference on 2026-07-14. The closed beta (see `beta-program/`) hit its gates: 78% activation, NPS 38, 5 quotable testimonials, zero P0s. The PRD (see `create-prd/`) and PR/FAQ (see `prfaq/`) are signed off. The launch is coordinated across Product, Engineering, PMM, Sales, Support, and Legal.

The PM (Devi Rao) needs a full launch playbook with run-of-show, internal + external comms, rollback plan, and post-launch retro template. The launch is "big bang" -- the conference keynote is the marketing leverage. There is no second chance.

## Inputs

- Beta exit memo: GA-go signed off 2026-07-04
- Conference keynote slot: 2026-07-14 at 10:15 ET (Devi presenting)
- Engineering on-call rota for launch week confirmed
- PMM has draft press release; needs Legal final pass
- Sales has 220 reps to enable; CS has 30 CSMs to train
- LaunchDarkly flag `shared_dashboards_v1` ready
- Support runbook in draft

## Applying the skill

1. **Set T-30 kickoff** for 2026-06-14: confirm date, owners per workstream, exec sponsor.
2. **Built the run-of-show** as a single shared Notion page; named incident commander (EM N. Okafor) and on-call rota.
3. **Three Launches frame**: Alpha done, Beta exited, GA is here -- the playbook only covers GA.
4. **Drilled the rollback plan** at T-7 (a Monday morning kill-switch drill in production). Verified flag-off and 24h share-link grace period.
5. **Pre-staged comms artifacts**: press release embargoed to 2026-07-13, blog post scheduled to publish 2026-07-14 at 10:30 ET (15 min after keynote start), customer email queued, status page entry drafted.
6. **Wrote the T+30 retro template** before launch so success criteria were not redefined after the fact.

Key decision quoted: *"If anything triggers the kill-switch criteria during keynote, we flip the flag, finish the keynote, and apologize live. We do not surprise customers with a rolled-back demo."*

## The artifact

````markdown
# Launch Playbook -- Acme Shared Dashboards GA

**Launch type:** Big bang, tied to Acme Conference keynote
**Launch date:** 2026-07-14 (T-0)
**Launch time:** 10:15 ET (keynote demo); 10:30 ET (flag flip + public)
**PM:** Devi Rao
**Incident commander (T-0):** N. Okafor (EM)
**Exec sponsor:** C. Bell (VP Product)

## Three Launches status

| Launch | Status | Notes |
|---|---|---|
| Alpha (internal) | DONE | Apr 15 - May 13; zero P0 |
| Beta (closed external) | DONE | May 26 - Jul 7; exit memo: GA-go |
| GA (this) | In flight | Today's playbook |

## Owners / RACI

| Workstream | Owner | RACI |
|---|---|---|
| Product spec + scope | Devi (PM) | R/A |
| Engineering delivery + on-call | N. Okafor (EM) | R/A |
| Press release + blog | J. Liu (PMM) | R |
| Sales enablement | M. Reyes (Sales Enablement) | R |
| Support runbook + training | F. Ahmed (Support Lead) | R |
| Legal review (ToS, public-facing copy) | M. Hughes (Legal) | A |
| Status page + on-call | DevOps on-call | R |
| Conference keynote | Devi + C. Bell | R/A |
| Executive comms (board, investors) | C. Bell (VP Product) | R |

## Pre-launch timeline (T-30 to T-1)

| Day | Workstream | Action | Owner | Status |
|----:|---|---|---|:-:|
| T-30 (Jun 14) | All | Launch kickoff meeting | Devi | DONE |
| T-30 | PM + PMM | Positioning brief signed off | Devi + J. Liu | DONE |
| T-21 (Jun 23) | Eng | Code freeze decision -- big bang chosen | N. Okafor | DONE |
| T-21 | Support | Runbook v1 drafted | F. Ahmed | DONE |
| T-21 | Sales | Enablement deck v1 drafted | M. Reyes | DONE |
| T-14 (Jun 30) | Legal | Final review of public-facing copy + ToS clause | M. Hughes | DONE |
| T-14 | Marketing | Press release + blog + social + email drafted | J. Liu | DONE |
| T-10 (Jul 4) | Eng | Dark-launch verified; 12 internal users smoke-tested in prod | N. Okafor | DONE |
| T-7 (Jul 7) | All | Run-of-show dry run + rollback drill | Devi | DONE |
| T-7 | Support | Team training completed | F. Ahmed | DONE |
| T-7 | Sales | 220 reps trained; battle cards distributed | M. Reyes | DONE |
| T-3 (Jul 11) | All | Final go/no-go check against launch readiness checklist | Devi | DONE |
| T-2 (Jul 12) | Marketing | Embargoed press outreach (Forbes, TechCrunch, ProductHunt) | J. Liu | DONE |
| T-1 (Jul 13) | All | Final confirmation; on-call rota for launch day published | Devi | DONE |

## Launch readiness checklist (T-3 gate)

- [x] PRD approved + frozen
- [x] PR/FAQ aligned with press release
- [x] Beta exit memo: GA-go
- [x] Feature flag tested + kill-switch drilled
- [x] Customer email queued (segmented)
- [x] In-app announcement scheduled
- [x] Press release embargoed
- [x] Blog post scheduled
- [x] Social posts scheduled (Twitter/X, LinkedIn)
- [x] Sales enablement complete (220/220 reps)
- [x] Support trained (30/30 CSMs)
- [x] Support runbook published
- [x] Documentation live (docs.acme.com/shared-dashboards)
- [x] Changelog entry drafted
- [x] Status page entry drafted (not yet published)
- [x] Pricing page updated (no pricing change, but feature row added)
- [x] Help center articles published
- [x] Legal sign-off on ToS update
- [x] Exec sponsor confirmed
- [x] On-call rota for launch day published
- [x] Monitoring dashboards configured (Datadog, Amplitude, Sentry)
- [x] Rollback plan documented + drilled
- [x] T+1, T+7, T+30 retro slots booked

## Launch day run-of-show (T-0, 2026-07-14)

Run from a single shared Notion page. Incident commander is N. Okafor. Single Slack channel `#launch-shared-dashboards` for the day.

| Time (ET) | Action | Owner |
|---|---|---|
| 06:00 | Pre-flight check: dashboards, on-call, support staffing | N. Okafor |
| 07:00 | Final monitoring sweep | DevOps |
| 08:00 | All-hands brief (15 min) -- Devi walks the day | Devi |
| 09:30 | Press embargo lifts | J. Liu |
| 10:00 | Conference keynote begins | C. Bell (CEO) |
| 10:15 | Demo of Shared Dashboards (live on stage) | Devi |
| 10:30 | Flag flip: 100% of Pro + Enterprise workspaces | N. Okafor |
| 10:30 | Blog post publishes | J. Liu |
| 10:30 | Social posts publish | PMM |
| 10:35 | Customer email starts sending (segmented, 5min ramp) | PMM |
| 10:35 | Status page entry: "Feature launch -- Shared Dashboards" | DevOps |
| 10:35 | In-app announcement enabled | Eng |
| 11:00 | First metrics read | Devi |
| 11:00 | Support war-room opens | F. Ahmed |
| 12:00 | Mid-day metrics check + Slack thread to exec | Devi |
| 14:00 | Press coverage roundup (afternoon) | PMM |
| 16:00 | End-of-day metrics read | Devi |
| 17:00 | Exec recap email | Devi |

### Kill-switch criteria (T-0)

If any of these triggers, flag goes to 0% immediately:

- Sev0/Sev1 incident in any dependent system (auth, billing, share-link service)
- Share-link generation error rate > 5% for 5 consecutive minutes
- Recipient-view error rate > 3% for 5 consecutive minutes
- Data leak / security incident (any)
- p95 latency on recipient view > 5s for 10 consecutive minutes

Kill-switch action: N. Okafor flips flag to 0%. Existing share links continue working for 24h grace period. Status page updated. Devi finishes keynote (does not surprise audience). Post-mortem opens immediately after keynote.

## Internal comms

| Audience | Channel | When | Owner |
|---|---|---|---|
| All Acme employees | All-hands T-1 | 2026-07-13 | Devi |
| Engineering | `#eng-announce` Slack | T-0 morning | N. Okafor |
| Sales | Mid-day briefing | T-0 lunch | M. Reyes |
| Support | War-room standup | T-0 11:00 | F. Ahmed |
| CSMs | War-room standup | T-0 11:00 | T. Park (Head of CS) |
| Board | Email recap | T+1 | C. Bell |

## External comms

| Audience | Channel | When |
|---|---|---|
| Customers (Pro + Enterprise) | Email | T-0, 10:35 ET (post-flag-flip) |
| Free-tier customers | Email | T-0 (informational; feature is paid-tier) |
| Press | Embargoed release | T-0, 09:30 ET embargo lift |
| Social (Twitter/X, LinkedIn) | Posts | T-0, 10:30 ET |
| ProductHunt | Launch post | T+1, 09:00 ET |
| In-app users | Banner | T-0, 10:35 ET |
| Existing share-link generators (beta cohort) | Personal thank-you | T-0 |

## Rollback plan

| Step | Action | Owner | Time |
|---|---|---|---|
| 1 | Flag to 0% in LaunchDarkly | N. Okafor | < 30s |
| 2 | Existing links continue (24h grace) | Auto | 0s |
| 3 | In-app banner updates: "Shared Dashboards temporarily unavailable" | Eng | < 5 min |
| 4 | Status page entry updated | DevOps | < 5 min |
| 5 | Support runbook switched to "rollback mode" responses | F. Ahmed | < 10 min |
| 6 | Customer email pause/redirect | PMM | < 10 min |
| 7 | Post-mortem opened | Devi | Within 2 hours |

Rollback was drilled 2026-07-07. Drill time: 4 min 18s from "go" to fully rolled back.

## Post-launch (T+1 to T+30)

| Day | Workstream | Action | Owner |
|---|---|---|---|
| T+1 (Jul 15) | PM + Eng | War-room standup; metrics + incidents | Devi + N. Okafor |
| T+1 | PMM | Launch-day metrics report to exec | J. Liu |
| T+1 | Support | First-day ticket triage | F. Ahmed |
| T+3 (Jul 17) | Support | Theme analysis of first 72h tickets | F. Ahmed |
| T+7 (Jul 21) | PM | Week-1 retrospective | Devi |
| T+14 (Jul 28) | PMM | Press coverage + adoption report | J. Liu |
| T+30 (Aug 13) | All | 30-day retrospective + decision | Devi |

## Success metrics (T+30 review)

| Metric | Target | Tracked |
|---|---|---|
| Pro-tier workspaces with >= 1 share link | >= 60% | Amplitude |
| Pro-tier expansions attributed to feature | >= 35% | HubSpot |
| Recipient NPS | >= 30 | In-link survey |
| Sev1/Sev2 incidents | 0 | Sentry + status page |
| P0 bugs open at T+30 | 0 | Linear |
| Press coverage (named tier-1 outlets) | >= 3 | PMM |
| Sales-cited deal wins citing feature | >= 5 | HubSpot |

## T+30 retrospective template

```markdown
# Shared Dashboards Launch -- T+30 Retrospective

**Date:** 2026-08-13

## Results vs targets

| Metric | Target | Actual | Variance |
|---|---|---|---|
|  |  |  |  |

## What went well
1.
2.
3.

## What went poorly
1.
2.
3.

## What surprised us
1.
2.

## Decisions

| Decision | Rationale | Owner | Due |
|---|---|---|---|
|  |  |  |  |

## Actions for v1.1
1.
2.

## Lessons for next launch
1.
2.
```

## Launch-day "do not do" list

- DO NOT change the demo flow during the keynote.
- DO NOT promise features that are in v1.1 (defer to "we're working on it").
- DO NOT roll back without consulting the incident commander.
- DO NOT engage with hostile social media commentary during the launch hour; channel through PMM.
- DO NOT skip the status page entry, even on a successful launch -- it's part of the customer trust signal.
````

## Why this works

- Single incident commander (N. Okafor) means there's never confusion about who decides on a rollback.
- The kill-switch criteria are pre-locked and numeric, not "if it feels bad".
- The rollback drill produced a real timing measurement (4 min 18 s) -- the plan is operationally tested, not theoretical.
- The keynote behavior is named: even in a rollback, Devi finishes the keynote. This anticipates the worst-case PR moment and pre-decides the response.
- The T+30 retro template is published before launch, so the team knows what evidence to collect during the launch window.

## What's next

- Pair with [../post-mortem/](../post-mortem/) if the kill-switch fires or any Sev1/2 occurs.
- Feed launch metrics into [../north-star-metric/](../north-star-metric/) and [../brainstorm-okrs/](../brainstorm-okrs/) (the Q3 OKR window opens at GA + 7d).
- Use [../release-notes/](../release-notes/) for the v1.1 release notes after T+30.
- Pair with [../status-update-generator/](../status-update-generator/) for the weekly exec updates from T+1 through T+30.
- Use [../eol-communication/](../eol-communication/) only if the launch fails and the feature is sunset (escape hatch).
