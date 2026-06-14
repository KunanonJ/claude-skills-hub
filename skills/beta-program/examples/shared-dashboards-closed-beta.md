# Example: Closed Beta for Acme Analytics "Shared Dashboards"

> Real-world scenario showing how to apply the closed-beta playbook end-to-end.

## Context

Acme Analytics is a Series-C B2B analytics SaaS (~3,400 paying customers). Customer Success has repeatedly heard that customers want to share read-only dashboards with their own clients during QBRs -- today they screenshot or PDF-export, losing interactivity and freshness. Discovery validated the opportunity (interviews with 18 CSMs, 11 customers). A v1 "Shared Dashboards" feature has cleared alpha (internal dogfooding for 2 weeks, zero P0 bugs).

The PM (Devi, PM Growth) has 6 weeks to run a closed beta with up to 25 customers before a GA launch tied to the Acme user conference. She needs a plan, recruitment script, weekly cadence, success criteria, and an exit memo template.

## Inputs

- Validated alpha (internal, 60 users, 200 share links generated)
- ICP: mid-market companies running monthly or quarterly business reviews with external stakeholders
- Engineering capacity for hotfixes during beta: 1 engineer 50%
- 18 customers already opted in via a Productboard signal
- Conference launch date locked: 2026-07-14
- Beta budget: $4k (gift cards + zoom calls + admin)

## Applying the skill

1. **Sized the cohorts** with friends-family-fanatics: 6 friends (internal champions and advisors), 12 family (opted-in customers), 7 fanatics (cold-recruited from ICP segments not yet customers).
2. **Locked Kano scope.** Beta build includes 1 Delight feature (live cursor presence for shared sessions). Must-be + 2 Performance features stable.
3. **Set quantitative success gates before recruitment**: activation 70%, week-4 retention 60%, outcome 50% reaching the "shared a dashboard with >=2 stakeholders" milestone, NPS >= 30, crash-free >= 99.5%, P0 = 0, quotable testimonials >= 5.
4. **Designed a weekly cadence**: Monday survey send, Wednesday office hours (optional), Friday async update with what shipped + what's coming.
5. **Pre-committed exit criteria** so the GA / extend / kill decision was not improvised at week 5.
6. **Drafted the exit memo template** before opening recruitment, so the team knew what evidence to gather.

Key decision quoted: *"We will not extend the beta past 8 weeks. If gates miss at week 6, we delay the conference announcement, not the gates."*

## The artifact

````markdown
# Closed Beta Plan -- Shared Dashboards

**Product:** Acme Analytics -- Shared Dashboards v1
**PM:** Devi Rao
**Window:** 2026-05-26 to 2026-07-07 (6 weeks)
**GA target:** 2026-07-14 (Acme conference keynote)
**Decision date:** 2026-07-04 (T-10 before GA)

## 1. Objectives

- Validate that mid-market customers will use Shared Dashboards in real QBR workflows.
- Surface bugs at sufficient volume to harden v1 for public launch.
- Produce 5+ quotable testimonials and 3 case-study candidates.
- Inform v1.1 scope (in / out / deferred).

## 2. Cohort design (Friends / Family / Fanatics)

| Cohort | Size | Recruitment source | Start | Tolerance |
|---|---|---|---|---|
| Friends | 6 | 4 internal champions + 2 advisors | Wk 1 | Very high |
| Family | 12 | Productboard opt-ins + CSM nominations | Wk 2 | High |
| Fanatics | 7 | LinkedIn outreach to ICP non-customers | Wk 3 | Medium |
| **Total** | **25** | | | |

Family cohort over-recruits to 14 to expect 10-12 active.

## 3. Scope (Kano-aligned)

| Category | Included in beta |
|---|---|
| Must-be | Create share link, password-protect, expiry date, read-only enforcement, audit log, revoke link |
| Performance | Refresh latency < 3s on shared view, link generation < 2s |
| Delight | Live cursor presence (see who is viewing now, beta-flag) |
| Deferred to v1.1 | PDF export, white-label branding, custom domain |
| Indifferent (cut) | Theme picker, share-link emoji |

## 4. Success gates

| Gate | Metric | Target | Source |
|---|---|---|---|
| Activation | % beta users who generate first share link within 7 days | >= 70% | Amplitude |
| Engagement | Median sessions / active user / week | >= 3 | Amplitude |
| Outcome | % beta users who share with >=2 distinct stakeholders | >= 50% | Audit log |
| Retention | % active in week 4 | >= 60% | Amplitude |
| NPS | Beta-cohort NPS | >= 30 | In-app + survey |
| CSAT | Post-task CSAT on share creation | >= 4.2/5 | Pendo |
| Crash-free sessions | All beta traffic | >= 99.5% | Sentry |
| P0 bugs | Open at week 5 | 0 | Linear |
| Testimonials | Named, quotable, willing to be cited | >= 5 | CSM logs |
| Case studies | Candidates with measurable outcome | >= 3 | CSM logs |

Gates set before recruitment opens. Renegotiation requires VP Product sign-off.

## 5. Recruitment script

```
Subject: Early access to Shared Dashboards -- 6-week design partner program

Hi {first_name},

You mentioned during your QBR with {csm_name} that sharing dashboards with
your stakeholders is harder than it should be. We're closing the gap.

We're inviting 12 customers into a closed beta of Shared Dashboards over
the next 6 weeks. As a design partner you'd get:

- Early access starting {start_date}
- Direct line to me (the PM) via a shared Slack channel
- A 30-min weekly office hour (optional)
- A small thank-you ($150 Amazon gift card at week 6)
- First seat in the v1.1 design conversations

What we ask in return:
- Use Shared Dashboards in at least 2 real customer-facing sessions
- A 15-min interview at week 3 and week 6
- Permission to quote anonymized feedback in launch materials

You can opt out at any time with no impact on your account. The feature is
behind a flag and won't change your existing workflow.

Want in? Reply yes and I'll send a calendar link for kickoff.

Devi
PM, Acme Analytics
```

## 6. Weekly cadence

| Day | Activity | Owner | Channel |
|---|---|---|---|
| Mon AM | Weekly survey (3 questions) | PM | Email + in-app |
| Mon PM | Triage incoming bugs from prior week | Eng on-call | Linear |
| Wed 11am ET | Optional office hours (Zoom, 30 min) | PM + EM | Calendar |
| Thu | 1:1 with 2-3 design-partner accounts | PM + CSM | Zoom |
| Fri PM | Async update to all beta participants | PM | Slack channel + email |
| Fri PM | Internal status to exec sponsor | PM | Notion page |

Survey questions (3 only, every week):
1. How many times did you use Shared Dashboards this week?
2. What is one thing that almost stopped you from finishing a share?
3. NPS (0-10): how likely are you to recommend Shared Dashboards to a peer?

## 7. Communication artifacts

- Shared Slack channel `#beta-shared-dashboards` (Acme + customers; one channel total)
- Kickoff doc in Notion (this plan, with customer-safe redactions)
- Public changelog updated weekly
- Bug-report shortcut in-app (one click from any shared dashboard)
- Exit-survey form (NPS + open text + testimonial-permission checkbox)

## 8. Exit memo template (filled at week 6)

```markdown
# Shared Dashboards Closed Beta -- Exit Memo (T-10 to GA)

## Decision: [ ] GA  [ ] Extend  [ ] Reduce scope  [ ] Kill

## Gates summary

| Gate | Target | Actual | Pass? |
|---|---|---|---|
| Activation | >= 70% | __ % | __ |
| Engagement | >= 3 sessions/wk | __ | __ |
| Outcome | >= 50% | __ % | __ |
| Retention wk 4 | >= 60% | __ % | __ |
| NPS | >= 30 | __ | __ |
| CSAT | >= 4.2 | __ | __ |
| Crash-free | >= 99.5% | __ % | __ |
| P0 bugs open | 0 | __ | __ |
| Testimonials | >= 5 | __ | __ |
| Case studies | >= 3 | __ | __ |

## Top 3 risks for GA

1.
2.
3.

## Top 3 quotes

1. "<quote>" -- <name, title, company>
2.
3.

## v1.1 candidate items (sourced from beta feedback)

| Item | Frequency | Severity | Recommend |
|---|---|---|---|
|  |  |  |  |

## Decision rationale (2-3 paragraphs)

## Action items if GA-go

| Owner | Action | Due |
|---|---|---|
|  |  |  |

## Action items if extend / reduce / kill

| Owner | Action | Due |
|---|---|---|
|  |  |  |
```

## 9. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Friends cohort under-uses (internal users not in real QBR flows) | Med | Med | Pair each friend with 1 real customer engagement before week 2 |
| Family cohort participation drops by week 4 | Med | High | Wednesday office hours + Thursday 1:1s; $150 gift card at exit |
| Fanatics produce noisy bug reports (less context than family) | High | Low | CSM-tag fanatic reports separately; weight family reports for v1.1 scope |
| Live-cursor delight feature crashes (Sentry shows correlation) | Low | High | Flag isolates the feature; kill-switch tested week 0 |
| Conference timing pulls the GA forward | High | High | Plan declares 2026-07-14 GA non-negotiable; gates compress if needed; better to ship feature-light than miss gates |

## 10. Operational details

- Beta-feature flag: `shared_dashboards_v1` in LaunchDarkly, scoped per workspace
- Sentry project + Datadog dashboard piped to a shared Notion page
- Linear project `BETA-SHARE` for bugs; auto-triage SLA: P0 same day, P1 24h, P2 5d
- Comms freeze: no other Customer Workflows product announcements 2026-06-23 to 2026-07-14

## 11. Stakeholders

| Role | Name | RACI on beta decisions |
|---|---|---|
| PM (Driver) | Devi Rao | D |
| EM | N. Okafor | A (engineering go/no-go) |
| VP Product (Sponsor) | C. Bell | A (overall GA) |
| Head of CS | T. Park | C |
| PMM | J. Liu | C |
| Legal (data-sharing) | M. Hughes | C |
| Support lead | F. Ahmed | I |
````

## Why this works

- Friends-family-fanatics is sequenced and over-recruited, so the family cohort hits its active-12 target even after expected drop-off.
- Success gates are quantitative and pre-committed, eliminating the "let's just look at the data" rationalization at exit.
- Kano scope includes exactly one Delight feature (live cursor), avoiding the "beta with only must-haves produces no quotes" failure.
- The weekly survey is three questions only; participation does not erode by week 4.
- The exit memo template is published at kickoff, so the team gathers the right evidence weekly rather than scrambling at week 6.

## What's next

- After exit memo says "GA", hand off to [../launch-playbook/](../launch-playbook/) for the T-30 to T+30 launch coordination.
- Use [../prfaq/](../prfaq/) drafted earlier in discovery to anchor the GA narrative.
- Feed v1.1 candidates from the exit memo into [../prioritization-frameworks/](../prioritization-frameworks/) (RICE) at next quarterly planning.
- Use [../release-notes/](../release-notes/) for the GA release notes.
- Pair with [../../discovery/pre-mortem/](../../discovery/pre-mortem/) before the conference launch to stress-test failure modes.
