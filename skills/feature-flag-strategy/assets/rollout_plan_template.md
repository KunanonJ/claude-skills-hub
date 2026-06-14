# Rollout Plan: [Feature Name]

A single-page operational plan for shipping a feature behind a flag. Owned by the PM; reviewed by Engineering, on-call, and the sponsor before the first ramp step.

**Version:** 0.1 (draft)
**PM owner:** ____________________
**Engineering lead:** ____________________
**On-call rota:** ____________________
**Sponsor:** ____________________
**Created:** 2026-05-22
**Status:** Draft / Approved / Ramping / GA / Retired

---

## 1. Feature summary

| Field | Value |
|---|---|
| Feature name | |
| Surface | web / mobile (iOS) / mobile (Android) / API / infra |
| Linked PRD | [link] |
| Linked PR/FAQ | [link if external launch] |
| Blast radius if it goes wrong | (1-3 sentences -- who is affected, how badly) |
| Customer-visible? | Yes / No |
| Regulated surface? | None / GDPR / EU AI Act tier / HIPAA / PCI / SOC 2 in scope |

## 2. Flag classification

| Field | Value |
|---|---|
| Flag type | Release / Experiment / Ops / Permission |
| Flag name | `<scope>__<feature>__<purpose>__<version>` |
| Flag service | LaunchDarkly / Statsig / Optimizely / Unleash / OpenFeature / in-house |
| Retirement date (release/experiment only) | YYYY-MM-DD |
| Owner | PM + Engineering lead |
| Dependencies | (other flags that must be on / off) |

## 3. Rollout shape

Primary shape (one of A-G): __________

Combined with: __________ (if applicable)

## 4. Ramp stages

| # | Audience | % / segment | Hold time | Gate criteria to advance | Owner | Target date |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |
| 6 | GA | 100% | -- | Stable for 1-2 weeks | | |

**Gate criteria guidance:** each row should name a specific, measurable metric. Examples:
- "Error rate < 0.5% sustained for 24h"
- "p95 latency within 10% of baseline"
- "Adoption above 60% of exposed users within 48h"
- "Customer NPS not regressed vs control"

## 5. Metrics to watch at each stage

| Metric | Source | Owner | Alert threshold |
|---|---|---|---|
| Error rate | (dashboard link) | On-call | |
| p95 latency | | On-call | |
| Adoption | | PM | |
| Conversion / activation | | PM | |
| Business KPI (e.g., revenue) | | PM + finance | |
| Customer tickets / NPS | | Support | |
| Cost (especially for AI features) | | PM + eng | |

## 6. Kill-switch

| Field | Value |
|---|---|
| Who can flip without escalation | (named individuals + on-call rota) |
| Two-person rule? | Yes / No |
| Kill-switch flip steps | (1) navigate to flag X; (2) set rollout to 0%; (3) confirm in dashboard Y; (4) post in #channel |
| Post-flip notification | (Slack channel + email list) |

### Kill-switch thresholds (pre-agreed)

| Trigger | Threshold | Action |
|---|---|---|
| Error rate | > X% for Y minutes | Flip to 0%, then triage |
| p95 latency | > Z ms for Y minutes | Throttle or flip |
| Top-customer impact | >= 1 paid customer blocked | Flip to 0%; escalate to account team |
| Cost overrun (AI features) | > 120% of stage budget | Throttle; downgrade model |

## 7. Communication plan

| When | Audience | Channel | Content |
|---|---|---|---|
| T-7 days | Internal (eng, support, sales) | Email | Heads-up; FAQ; what to escalate |
| T-1 day | Internal | Slack | "Tomorrow we start ramping" |
| Each stage advance | Internal | Slack | "Moving to N%" with metric summary |
| GA | External customers | Email / changelog / in-product | Standard launch comms (use `launch-playbook/`) |
| If kill-switch flipped | Internal + affected customers | Slack + ticket | Incident-style comms |

## 8. Holdout (if applicable)

| Field | Value |
|---|---|
| Holdout % | (typically 1-10%) |
| Composition | Random / stratified by segment |
| Duration | (at least one retention horizon; often quarter) |
| Re-exposure plan | When holdout ends, how users are merged |
| Owner | PM + analytics |

## 9. Dependencies

| Depends on | Status | Resolution date |
|---|---|---|
| Other flag(s) | | |
| Backend service version | | |
| Mobile client version | | |
| Regulatory approval | | |
| Customer comms ready | | |
| Support docs ready | | |
| Runbook ready | | |

## 10. Retirement plan (release / experiment toggles)

- [ ] Retirement date set: ____________________
- [ ] Retirement PR opened at flag creation: ____________________
- [ ] Test matrix updated when feature reaches GA
- [ ] Documentation updated
- [ ] Config entry removed from flag service
- [ ] Final archive note (what flag controlled, when it retired, who owned it)

## 11. Sign-offs (required before stage 1)

| Role | Name | Date |
|---|---|---|
| PM | | |
| Engineering lead | | |
| On-call lead | | |
| Sponsor | | |
| Legal / Compliance (if regulated) | | |
| Support lead | | |

---

## Stage transition log

A running log of each ramp transition. Filled in by the owner as the rollout progresses.

| Date | Stage | From % | To % | Metrics snapshot | Approver | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |

## Incident log (if applicable)

| Date | Stage | Trigger | Action taken | Post-incident note |
|---|---|---|---|---|
| | | | | |

---

**This plan is a living document.** Update after each stage transition. Archive at retirement.
