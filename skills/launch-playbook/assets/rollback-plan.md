# Rollback Plan: [Feature / Product Name]

**Launch date:** [YYYY-MM-DD]
**Plan Owner:** [Engineering Lead]
**Rollback Authority:** [Incident Commander -- name]
**Exec Consultation Required:** [Yes / No -- triggers when financial / contractual impact > $X]

---

## 1. Rollback Strategy

| Aspect | Approach |
|--------|----------|
| **Mechanism** | [Feature flag toggle / config change / blue-green swap / database revert] |
| **Time to execute** | [Target: < 5 minutes for flag; < 15 min for deploy revert] |
| **Reversibility** | [Idempotent / one-way after T+X / requires data migration to reverse] |
| **Blast radius of rollback** | [Who is affected: all users / specific ring / specific account tier] |
| **Customer-visible rollback notice** | [Yes / No -- if Yes, draft is in `/comms/rollback-notice.md`] |

---

## 2. Rollback Triggers (Pre-Authorized)

The Incident Commander is pre-authorized to execute rollback on any of these:

| Trigger | Threshold | Detection Source |
|---------|-----------|------------------|
| Error rate spike | > 5x baseline for > 5 min | APM dashboard |
| Crash-free session rate drop | < 99% for > 5 min | Crashlytics / Sentry |
| Payment failure | Any payment-flow failures attributable to the change | Payment monitoring |
| Data corruption | Any signal of bad data being written | Data quality alerts + manual report |
| Auth failure | Any cohort unable to authenticate | Auth service alerts |
| P0 support volume | 3+ matching P0 customer reports within 1 hour | Support escalation channel |

Triggers requiring exec consultation (revenue/contractual):

| Trigger | Required Consult |
|---------|------------------|
| Rollback affects a contractual SLA customer | Exec Sponsor + Legal |
| Rollback after public press coverage | Exec Sponsor + PMM |
| Rollback of pricing change | Exec Sponsor + CFO |

---

## 3. Rollback Execution Runbook

### Step 1: Declare Rollback

- IC announces rollback in war room.
- Status page updated to "Investigating" within 5 minutes.
- Exec sponsor notified within 15 minutes.

### Step 2: Execute

For feature flag rollback:
1. Engineer with deploy access toggles flag in [tool / dashboard / CLI].
2. Engineer confirms flag state in production.
3. Engineer monitors error rate and crash-free rate for 10 minutes.
4. IC announces "Rollback executed" in war room.

For deploy revert:
1. Engineer reverts last deploy via [CI/CD tool].
2. Engineer monitors deploy completion.
3. Engineer runs smoke tests against production.
4. IC announces "Rollback executed" in war room.

For database revert (high risk):
1. Confirm point-in-time recovery target with DBA.
2. Block writes during revert.
3. Execute revert.
4. Validate data integrity with checksum / row count.
5. Unblock writes.
6. IC announces "Rollback executed and validated" in war room.

### Step 3: Verify

- [ ] Error rate returns to baseline within 15 minutes
- [ ] Crash-free session rate returns to >= 99.5% within 15 minutes
- [ ] Support volume trending down
- [ ] No new P0 reports for 30 minutes

### Step 4: Communicate

- [ ] Status page updated to "Resolved"
- [ ] Internal #general announcement
- [ ] Customer email to anyone notified about launch
- [ ] Press / blog post amendment if public coverage occurred

### Step 5: Post-Rollback Review

Within 48 hours of rollback:
- [ ] Postmortem document started (blameless format)
- [ ] Root cause identified
- [ ] Detection-time analysis
- [ ] Re-launch criteria defined
- [ ] Re-launch date proposed

---

## 4. Rollback Drill (Pre-Launch)

Mandatory at T-7 (or earlier).

| Drill | Owner | Status |
|-------|-------|:------:|
| Feature flag toggle drill in staging | Eng Lead | [ ] |
| Deploy revert drill in staging | Eng Lead | [ ] |
| Production rollback drill with no-op feature | Eng Lead | [ ] |
| Communication chain dry-run (IC -> war room -> exec) | IC | [ ] |
| Status page update drill | Eng Lead | [ ] |

Document results below:

| Drill | Date | Outcome | Issues Found | Resolution |
|-------|------|---------|--------------|-----------|
| | | | | |
| | | | | |

---

## 5. Risks That Rollback Does Not Solve

Some failures cannot be rolled back. Identify them now.

| Risk | Why Rollback Does Not Help | Mitigation |
|------|----------------------------|-----------|
| Public press already issued | Reputational damage is done | PMM drafts amendment statement pre-launch |
| Customer data already written in new format | Data migration is forward-only | Backwards-compatible schema; dual-write during launch |
| Pricing change communicated to customers | Trust impact | Honor announced pricing; roll back only the back-end logic |
| Mobile app update shipped to app stores | App store delays | Server-side feature flag to disable client features |

---

## 6. Sign-Off

By signing below, the rollback plan is approved and the rollback authority is confirmed.

| Name | Role | Date | Signature |
|------|------|------|-----------|
| | Engineering Lead | | |
| | PM | | |
| | Incident Commander | | |
| | Exec Sponsor | | |
