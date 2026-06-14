# Launch Coordination Reference Guide

A practical reference for coordinating cross-functional product launches. Expands the patterns in `SKILL.md` with worked examples, common failure modes, and the decision rules behind big-bang vs progressive vs dark launches.

---

## 1. The Three-Launches Model (Cagan)

Marty Cagan's framing splits a single GA launch into three sequenced events. Each tests a different risk; skipping one transfers that risk forward in time and amplifies it.

| Launch | Tests | Failure Mode if Skipped |
|--------|-------|-------------------------|
| **Alpha** | Does it run? Does it crash? | Embarrassing demos; production crashes |
| **Beta** | Does it produce the outcome? Will customers pay? | Launch with no testimonials; high churn at GA |
| **GA** | Can we scale? Does the market care? | Successful technical launch, commercial flop |

The output of each launch feeds the next:

- Alpha -> known-issues list and crash signatures
- Beta -> testimonials, pricing validation, refined positioning
- GA -> adoption curve, press, sales pipeline

This skill (`launch-playbook/`) is the GA event. Alpha is engineering's responsibility. Beta is `beta-program/`.

---

## 2. Launch Type Decision Tree

```
Is the change customer-money-affecting (billing, pricing, payments)?
  YES -> Progressive Rollout (mandatory)
  NO  -> continue

Is there marketing leverage in a single date (keynote, conference, partner co-marketing)?
  YES -> Big Bang (with dark-launch backend prep at T-14)
  NO  -> continue

Is the feature performance-sensitive at scale (search, ML inference, real-time)?
  YES -> Dark Launch + Progressive Rollout
  NO  -> continue

Are external dependencies tightly coupled (mobile app store releases, partner APIs)?
  YES -> Big Bang (forced by external timing)
  NO  -> Progressive Rollout (default)
```

### Big Bang

- One date, all users, full announcement.
- Concentrates risk; rewards rehearsal.
- Use when marketing leverage of the single date is material.

### Progressive Rollout (Ring Deployment)

- Ring 0: internal employees (alpha)
- Ring 1: beta cohort (see `beta-program/`)
- Ring 2: 5% of GA-eligible users
- Ring 3: 25% of GA-eligible users
- Ring 4: 100% of GA-eligible users

Each ring is held for a minimum dwell time (typically 24-72 hours) and gated on:

- Crash-free session rate >= 99.5%
- No new P0 bugs in the ring
- Customer support ticket volume within +20% of baseline

### Dark Launch

- Code is in production, real traffic exercises it, but no UI visible.
- Used for infrastructure validation: database migrations, cache warming, queue capacity, ML model latency.
- Most useful at T-14 through T-7 of a big-bang launch.

---

## 3. RACI Worked Examples

### Example A: Major Feature Launch (SaaS)

| Workstream | PM | Eng | PMM | Sales | Support | Legal | Exec |
|-----------|:--:|:---:|:---:|:-----:|:-------:|:-----:|:----:|
| Positioning brief | A | C | R | C | I | C | I |
| Pricing decision | R | I | C | C | I | C | A |
| Code deployment | I | A | I | I | I | I | I |
| Sales deck + battle cards | C | I | C | A | I | I | I |
| Support runbook | C | C | I | I | A | I | I |
| Press release | I | I | A | I | I | C | I |
| Customer email | C | I | A | I | I | C | I |
| Launch-day war room | A | C | C | I | C | I | I |
| Rollback authority | C | C | I | I | I | I | A |
| 30-day retro | A | C | C | C | C | I | I |

### Example B: Pricing Change

For pricing changes, Legal moves from C to A on customer-facing comms (regulatory exposure), Exec moves to A on the pricing decision itself, and CS becomes R on customer notification.

| Workstream | PM | Eng | PMM | Sales | CS | Support | Legal | Exec |
|-----------|:--:|:---:|:---:|:-----:|:--:|:-------:|:-----:|:----:|
| Pricing decision | C | I | C | C | C | I | C | A |
| Pricing page copy | C | I | R | C | I | I | A | I |
| Customer notification | C | I | C | C | R | I | A/C | I |
| Renewal communications | I | I | C | A | R | I | C | I |

### Anti-Pattern: "Everyone is Responsible"

If two or more people are listed as A (Accountable) for the same cell, nobody is. There is exactly one Accountable per cell.

---

## 4. The Launch-Readiness Checklist (T-3 Go/No-Go)

Every item must be Yes. Any No requires a documented mitigation or postponement.

### Engineering

- [ ] Code frozen for at least 72 hours
- [ ] Deployment runbook reviewed and signed
- [ ] Rollback drill completed in production with no-op feature
- [ ] On-call rota published for T-0 through T+3
- [ ] Monitoring dashboards updated; alerts validated
- [ ] Database migrations completed and verified (if applicable)
- [ ] Feature flag default state confirmed

### Product

- [ ] PRD final state archived
- [ ] Beta exit memo signed (if applicable)
- [ ] Known-issues list published internally
- [ ] Success metrics dashboard live and accessible

### PMM / Marketing

- [ ] Positioning brief signed off
- [ ] Press release approved by Legal
- [ ] Blog post staged and scheduled
- [ ] Social copy drafted across all channels
- [ ] Customer email campaign tested
- [ ] Press embargo policy documented
- [ ] Analyst pre-briefings completed (if applicable)

### Sales

- [ ] Sales deck delivered to reps at least T-7
- [ ] Battle cards distributed
- [ ] Pricing approved and loaded into CRM/CPQ
- [ ] Demo environment updated
- [ ] Field training session completed
- [ ] Top-account list reviewed for personalized outreach

### Support

- [ ] Runbook published internally
- [ ] FAQ live on help center
- [ ] Tier-1 team training completed
- [ ] Tier-2 escalation path defined
- [ ] Ticket macros updated
- [ ] Status page draft entry ready

### Legal & Compliance

- [ ] Public-facing copy reviewed
- [ ] ToS or DPA changes signed off (if applicable)
- [ ] Pricing page complies with relevant regulations
- [ ] Data residency / privacy claims verified

### Executive Comms

- [ ] Exec sponsor briefed at T-3
- [ ] Board/exec digest scheduled for T+1 and T+7
- [ ] Internal all-hands or company-wide email scheduled

---

## 5. Launch Day Operating Model

### Single Incident Commander

The Incident Commander is the named person empowered to make any operational call on launch day, including a rollback. Default: the PM owns the launch run-of-show; the Engineering Lead is IC for operational/technical decisions. Both are named explicitly in the run-of-show.

### Hourly Cadence

| Hour | Action |
|------|--------|
| T-1h | Final pre-launch standup; all teams confirm ready |
| T-0 | Flag flip / deploy / send launch comms |
| T+1h | First metrics check: traffic, errors, conversion |
| T+2h | Adoption snapshot; first customer reactions |
| T+4h | Second metrics check; press monitoring |
| T+6h | Support volume check; incident review (if any) |
| T+8h | End-of-day summary to exec sponsor |

### War Room

Single shared channel + video bridge. Open T-1h to end of day. Everyone with an A or R role attends.

### Communication Rules During Incident

1. The Incident Commander declares incident scope and severity.
2. PM owns external customer comms; PMM owns press response.
3. Engineering owns technical updates; goes through PM to customer-facing channels.
4. No public update is issued without IC approval.
5. Status page updated within 10 minutes of any user-visible degradation.

---

## 6. Rollback Decision Matrix

| Symptom | Severity | Action |
|---------|----------|--------|
| Error rate > 5x baseline for > 5 min | P0 | Immediate rollback |
| Crash-free session rate < 99% | P0 | Immediate rollback |
| Payment / billing failure | P0 | Immediate rollback |
| Data corruption observed | P0 | Immediate rollback + DB integrity check |
| Support volume > 3x baseline | P1 | Investigate; rollback if no clear root cause in 1 hour |
| One specific cohort failing | P1 | Disable for that cohort; continue rollout for others |
| Negative press coverage only | P2 | Continue; respond per PMM playbook |

Authority to rollback rests with the Incident Commander, with executive sponsor consultation if material business impact (revenue, contracts, public commitments).

---

## 7. Post-Launch Window: What to Measure

### Days 1-3: Stabilization

- Crash-free session rate
- Error rate vs baseline
- Support ticket volume vs baseline
- Top 5 support ticket themes

### Days 4-14: Adoption

- % of eligible users who used the feature at least once
- % who used it more than once (repeat use)
- Median time-to-first-use
- Top user paths through the feature

### Days 15-30: Outcome

- Headline outcome metric vs forecast
- Revenue impact (new MRR, expansion, retention)
- Sales pipeline created
- Press coverage tone and reach

The 30-day window produces one decision: invest more, sustain, iterate, or sunset.

---

## 8. Common Launch Failure Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **"It worked in beta"** | Performance collapses at GA volume | Add dark-launch and progressive rollout to absorb scale risk |
| **Sales surprise** | Sales reps see the announcement on the same day as customers | Mandatory enablement at T-7 with attendance tracking |
| **Support drowning** | Tier-1 buried in tickets; escalations stack | Pre-launch volume forecast; surge staffing for first 72h |
| **Press misalignment** | Coverage contradicts internal messaging | Single positioning brief; PMM-only press contact |
| **Rollback paralysis** | Symptoms unclear; team debates instead of rolling back | Rollback decision matrix pre-signed by IC and Exec Sponsor |
| **Exec surprise** | Sponsor learns about a customer complaint from a customer | Internal comms plan with named touchpoints at T-1, T-0, T+1 |
| **No-one owns the retro** | Team disbands at T+1; 30-day decision never made | Calendar-block the retro at kickoff; named owner in RACI |
| **Comms-only launch** | Marketing fires on schedule, product never ships the feature flag | Single integrated checklist with engineering deploy as a gating item |

---

## 9. Internal Comms Touchpoints

| Time | Audience | Channel | Owner |
|------|----------|---------|-------|
| T-30 | Executive sponsor | 1:1 brief | PM |
| T-21 | Cross-functional leads | Kickoff doc + meeting | PM |
| T-14 | Sales leadership | Pre-enablement preview | PMM |
| T-7 | All sales reps | Enablement session | PMM + Sales Lead |
| T-7 | All support agents | Training session | Support Lead |
| T-3 | Exec sponsor | Go/no-go memo | PM |
| T-2 | Whole company | Pre-launch teaser email | PMM |
| T-0 | Whole company | Launch announcement | PMM + Exec Sponsor |
| T+1 | Exec sponsor | First-24h metrics | PM |
| T+7 | Exec sponsor | Week-1 retro summary | PM |
| T+30 | Exec sponsor + leadership | 30-day decision memo | PM |

---

## 10. References

- Cagan, Marty. *Inspired: How to Create Tech Products Customers Love*. Wiley, 2018.
- Cagan, Marty. *Empowered: Ordinary People, Extraordinary Products*. Wiley, 2020.
- Humble, Jez and Farley, David. *Continuous Delivery*. Addison-Wesley, 2010. (Dark launches, ring deployments.)
- Beyer, Betsy et al. *Site Reliability Engineering*. O'Reilly, 2016. (Incident command, rollback patterns.)
