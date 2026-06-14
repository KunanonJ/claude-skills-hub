# Launch Day Run-of-Show: [Feature / Product Name]

**Launch date (T-0):** [YYYY-MM-DD]
**Launch type:** [Big Bang / Progressive Rollout / Dark Launch]
**Incident Commander (operational):** [Name, role, contact]
**Launch Owner (run-of-show):** [Name, role, contact]
**Exec Sponsor:** [Name, role, contact]
**War room link:** [Slack channel / Zoom / Meet]

---

## Pre-Launch (T-1h to T-0)

| Time | Action | Owner | Status |
|------|--------|-------|:------:|
| T-1h00 | Pre-launch standup; confirm all teams ready | Launch Owner | [ ] |
| T-0h45 | Final monitoring dashboard check | Eng Lead | [ ] |
| T-0h30 | Status page set to "Maintenance" if applicable | Eng Lead | [ ] |
| T-0h15 | Sales and Support standby; on-call confirmed | Sales Lead + Support Lead | [ ] |
| T-0h05 | Final go/no-go from IC | Incident Commander | [ ] |

---

## Launch Window (T-0 to T+8h)

| Time | Action | Owner | Status | Notes |
|------|--------|-------|:------:|-------|
| T+0:00 | Deploy / flag flip | Eng Lead | [ ] | |
| T+0:05 | Verify health checks green | Eng Lead | [ ] | |
| T+0:10 | Internal company announcement | PMM | [ ] | |
| T+0:15 | First metrics snapshot (traffic, error rate, latency) | Eng Lead | [ ] | |
| T+0:30 | Press release goes live | PMM | [ ] | |
| T+0:30 | Blog post published | PMM | [ ] | |
| T+0:30 | Social media posts published | PMM | [ ] | |
| T+0:45 | Customer email campaign sent | PMM | [ ] | |
| T+1:00 | Hourly metrics check (traffic, errors, conversion) | Eng Lead | [ ] | |
| T+1:00 | First customer reactions reviewed | PM | [ ] | |
| T+1:30 | Sales reps notified to begin outbound | Sales Lead | [ ] | |
| T+2:00 | Hourly metrics check + support ticket volume | Eng + Support | [ ] | |
| T+2:00 | First press coverage roundup | PMM | [ ] | |
| T+3:00 | Hourly metrics check | Eng Lead | [ ] | |
| T+4:00 | Hourly metrics check + adoption snapshot | Eng + PM | [ ] | |
| T+4:00 | Mid-day comms update to exec sponsor | PM | [ ] | |
| T+5:00 | Hourly metrics check | Eng Lead | [ ] | |
| T+6:00 | Hourly metrics check + support volume review | Eng + Support | [ ] | |
| T+7:00 | Hourly metrics check | Eng Lead | [ ] | |
| T+8:00 | End-of-day summary to exec sponsor | PM | [ ] | |
| T+8:00 | War room closes; on-call handoff documented | IC | [ ] | |

---

## Progressive Rollout (if applicable)

| Ring | % of Users | Earliest Promote | Gate Criteria | Owner |
|------|-----------:|------------------|---------------|-------|
| Ring 1 | 1% | T+0 | Error rate < 2x baseline | Eng Lead |
| Ring 2 | 5% | T+24h | Crash-free >= 99.5%, no new P0 | Eng Lead |
| Ring 3 | 25% | T+72h | Same + support volume < 1.2x baseline | Eng Lead |
| Ring 4 | 100% | T+7d | Same + retro green | Eng Lead |

---

## Rollback Criteria (Pre-Authorized)

The Incident Commander is pre-authorized to roll back on any of:

- [ ] Error rate > 5x baseline for > 5 minutes
- [ ] Crash-free session rate falls below 99% for > 5 minutes
- [ ] Payment or billing flow failures observed
- [ ] Data corruption signal
- [ ] Three or more matching P0 support reports within 1 hour

Rollback execution: see `rollback-plan.md`.

---

## Communication Protocol During Incident

1. **Incident detected.** IC declares severity (P0 / P1 / P2) in war room.
2. **Status page updated within 10 minutes** for any user-visible degradation. Owner: Eng Lead.
3. **External customer comms.** PM drafts; IC approves; PMM sends.
4. **Press inquiries.** PMM only; no other team member responds.
5. **Internal updates.** Every 30 min during P0; every hour during P1; until resolved.
6. **Exec sponsor notified within 15 min of P0 declaration.**

---

## Roles and On-Call

| Role | Primary | Secondary | Hours On Call |
|------|---------|-----------|--------------|
| Incident Commander | [Name] | [Name] | T-1h to T+8h |
| Engineering on-call | [Name] | [Name] | T-1h to T+24h |
| PMM on-call | [Name] | [Name] | T-1h to T+8h |
| Support lead | [Name] | [Name] | T-1h to T+8h |
| Sales lead | [Name] | [Name] | T+0 to T+8h |

---

## Post-Day-0 Activities

- T+1 day: War-room standup at [time], 30 min
- T+3 days: First triage of support themes
- T+7 days: Week-1 retro (use `post-launch-retro.md`)
- T+30 days: 30-day retro and decision memo
