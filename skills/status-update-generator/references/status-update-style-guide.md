# Status Update Style Guide

A reference on writing voice, structural rules, traffic-light discipline, and 5 worked examples covering Green / Yellow / Red updates across different team types.

---

## Voice and structure

### The cardinal rule: outcome over activity

A weekly update is a contract with the reader: in exchange for 60 seconds of attention, they get the state of the world. Activity-led updates ("we shipped X PRs") break the contract because they require translation. Outcome-led updates ("search latency dropped from 480ms to 210ms after the index rebuild shipped") deliver state directly.

| Activity-led (avoid) | Outcome-led (use) |
|----------------------|-------------------|
| Shipped PR-1234 | Search latency p95 dropped from 480ms to 210ms (PR-1234) |
| Held 3 customer interviews | 3 customer interviews confirm that the top onboarding friction is account verification |
| Completed sprint 23 | Sprint 23 delivered the SSO MVP; first pilot tenant configured this week |
| Wrote PRD for Feature X | Feature X PRD signed off by all 5 reviewers; build kicks off Monday |

### Length and cadence

- **One screen / one page max.** If the reader needs to scroll twice, the update is too long.
- **Same day, same time, every week.** Predictability beats polish.
- **5 bullets per section max.** Force prioritization. If you have 8 highlights, the top 3 do not stand out.

### Tone

- **Direct, not breezy.** Avoid "we're absolutely thrilled to share..." -- start with the news.
- **Confident, not hyperbolic.** "Latency is down to 210ms" beats "Latency is dramatically better!"
- **Honest, not defensive.** When something missed, name it plainly. Defensive updates train readers to assume things are worse than reported.

---

## The traffic-light rules

### Green = on track

Use Green when:

- No active blockers
- All risks have credible mitigations in flight
- Commitments will be met (or have been met)
- The team would tell the truth if asked "how is it going?" with no qualifier

Use Green sparingly. If 6 of the last 8 updates were Green, the team is probably not stretching enough -- or the watermelon effect is active.

### Yellow = at risk

Use Yellow when:

- There is an issue, but the team has a credible mitigation in flight
- A specific risk is now likely enough to require attention
- A delivery date is at risk by 1-2 weeks and the team is working the recovery

A Yellow update must specify the mitigation. "Yellow because of unknowns" is not a Yellow -- it is a Red waiting to be admitted.

### Red = off track

Use Red when:

- Intervention from leadership is required
- A delivery date is at risk by 3+ weeks
- An active incident is consuming team capacity
- The team cannot mitigate without external action

A Red update must include an explicit Ask. Red without an Ask means the PM has not done their job of escalating.

### The watermelon trap

The most common failure: **Green status with Red details inside.** It usually happens because:

1. The PM is conflict-averse
2. The team is over-promising to a sponsor who punishes Yellow
3. The status was decided before the body was written

The fix: write the body first, then choose the color from the contents. Have a peer read the body and predict the color. If they predict differently than you chose, you have watermelon.

---

## Worked examples

### Example 1: Green update (engineering platform team)

```markdown
# Acme Search Platform -- Week of 2026-05-18

**Author:** Jane Doe (PM) | **Status:** GREEN
**Rationale:** Index rebuild complete; latency targets exceeded; Phase 2 on schedule.

## Highlights
- Search latency p95 dropped from 480ms to 210ms after index rebuild (PROJ-1234)
- Customer support tickets for slow search resolved -- 12 open tickets closed
- Pilot tenant Acme Inc. migrated to v2 index with zero downtime
- Documentation refresh complete; new SDK docs live for partners

## Blockers
None this week.

## Risks
- Cost spike during traffic ramp -- L x M -- Mitigation: auto-scale ceiling at 80% budget -- Owner: SRE -- Due: 2026-05-30

## Asks
None this week.

## What's Next
- Onboard 3 pilot enterprise tenants (pending Sales sign-off; routine ask)
- Begin Phase 3 design (multi-tenant index sharding)
- Q2 OKR review: KR1 (latency) is met; KR2 (rollout) tracking on plan
```

### Example 2: Yellow update (consumer product team)

```markdown
# Onboarding Wizard -- Week of 2026-05-18

**Author:** Sam Lee (PM) | **Status:** YELLOW
**Rationale:** Activation lift below target; A/B variant B underperforming, switching to variant C this week.

## Highlights
- Variant A live in 50% experiment; activation rate at 38% (target was 42%)
- 22 user interviews complete; top friction confirmed as account verification step
- Help center articles for the new flow published; CSAT for setup at 7.4/10

## Blockers
- Variant C requires copy review from Legal (regulatory disclaimer)
  - Blocked by: Legal team
  - Need: 15-minute copy review by Wed 2026-05-21

## Risks
- Q2 activation target (42%) at risk if variant C does not lift performance -- M x H -- Mitigation: variant C launches Thu; readout by 2026-05-31. Backup: revert to legacy flow with copy tweaks -- Owner: Sam Lee -- Due: 2026-05-31
- Verification API rate limit could throttle launch -- L x M -- Mitigation: vendor confirmed cap raise for $1.5K/mo -- Owner: Eng lead -- Due: 2026-05-25

## Asks
- 15-minute legal copy review for variant C by Wed -- From: Legal Lead -- Consequence: variant C slip by 1 week pushes Q2 target out of reach

## What's Next
- Ship variant C
- Run readout on variant A vs variant C
- Reach decision on flow direction by end of sprint
```

### Example 3: Red update (cross-team migration)

```markdown
# Database Migration -- Week of 2026-05-18

**Author:** Priya Singh (Program Manager) | **Status:** RED
**Rationale:** Migration cutover blocked by data inconsistency discovered in pre-flight check; cutover slips by 2 weeks; leadership decision needed on customer comms.

## Highlights
- Pre-flight data validation flagged 2.3% of records with schema inconsistency
- Backfill script written and tested in staging; resolves 100% of flagged records
- Customer comms draft prepared with two options (silent fix vs. proactive notice)

## Blockers
- Cutover blocked until data is reconciled (now 2 weeks behind plan)
  - Blocked by: Backfill execution + customer comms decision
  - Need: Approval to run the backfill script in production + decision on customer notification

## Risks
- Customer trust impact if backfill is silent and surfaces in audit logs -- M x H -- Mitigation: send proactive notice (requires VP Marketing approval) -- Owner: Priya Singh -- Due: 2026-05-23
- SRE on-call coverage during extended cutover window -- M x M -- Mitigation: 2 additional SREs on rotation -- Owner: SRE manager -- Due: 2026-05-25

## Asks
1. Decision: silent backfill OR proactive customer notice -- From: VP Eng + VP Marketing -- By: 2026-05-22 -- Consequence: cutover slips beyond 2 weeks if not decided by Friday
2. Approval to extend cutover maintenance window by 90 minutes -- From: VP Customer Success -- By: 2026-05-23 -- Consequence: cannot start cutover

## What's Next
- Execute decision from above asks
- Run final backfill in production (Mon 2026-05-25, T-3 days before cutover)
- Cutover rescheduled for 2026-05-28 23:00 UTC
- Daily status updates resume for the cutover week
```

### Example 4: Green update (small startup, no formal sponsor)

```markdown
# Acme MVP -- Week of 2026-05-18

**Author:** Founder PM | **Status:** GREEN
**Rationale:** Beta cohort onboarded; first paying customer signed.

## Highlights
- 12 of 15 beta users onboarded; 9 completed setup within 24 hours
- First paying customer signed ($240/mo); contract sent and countersigned
- Stripe billing live in production with refund handling
- Top user feedback: dashboard load is slow; fix scoped for next week

## Blockers
None.

## Risks
- Dashboard performance complaints could hurt referrals -- M x M -- Mitigation: caching fix in progress; aim for 50% load-time reduction -- Owner: Eng (1 engineer team) -- Due: 2026-05-25

## Asks
- 1 hour from the design partner this week to walk through the slow dashboard -- From: Acme Co contact -- By: 2026-05-22 -- Consequence: shipping the fix blind

## What's Next
- Onboard remaining 3 beta users
- Ship dashboard caching fix
- Begin outbound to 10 prospects from the waitlist
```

### Example 5: Yellow update (regulated product, compliance team)

```markdown
# SOC 2 Type II Audit Prep -- Week of 2026-05-18

**Author:** Compliance PM | **Status:** YELLOW
**Rationale:** Evidence collection 70% complete; 3 controls still need owner sign-off; on track for audit window if sign-offs land by 2026-05-25.

## Highlights
- Evidence collected for 38 of 54 controls; auditor's portal updated
- New access-review automation passes the auditor's spot check
- Vendor risk reviews complete for all 12 in-scope vendors

## Blockers
None active; sign-off delays are tracked as Risks.

## Risks
- 3 control owners have not signed evidence (CTRL-12, CTRL-22, CTRL-31) -- M x H -- Mitigation: 1:1s scheduled this week; escalation path identified -- Owner: Compliance PM -- Due: 2026-05-25
- Auditor requested 2 additional artifacts (access reviews + change tickets sample) -- L x M -- Mitigation: artifacts pulled from Jira; awaiting redaction -- Owner: Compliance PM -- Due: 2026-05-22

## Asks
- VP Eng to nudge CTRL-22 owner if 1:1 outcome on Mon is non-committal -- From: VP Eng -- By: 2026-05-24 -- Consequence: control owner change for the audit window (paperwork churn)

## What's Next
- Land remaining 3 sign-offs
- Submit revised artifacts to auditor
- Begin Type II observation window (90 days)
```

---

## Format-specific tips

### Markdown (default)

- Use H1 for the team/project name, H2 for sections
- Keep bullets short; one line each where possible
- Bold the verdict ("Status: YELLOW")

### Confluence

- Use the `info`/`warning` macro for the status header (color-codable)
- Tables for risks render well
- Avoid heavy macros for the asks section -- they hide content in collapsed views

### Notion

- Use callouts (`> [!NOTE]`) for the status header
- Toggle blocks for "Risks" and "Asks" if your team prefers progressive disclosure
- Tag the page with the period so the database view is sortable

### Linear

- Use issue references where applicable (the tool emits `[PROJ-1234]` format)
- Use Linear priority labels (~~Urgent~~ / ~~High~~ etc.) on blockers and asks
- Post to the team channel and pin until the next update

---

## Reading the update like an exec

When you receive a status update, scan in this order:

1. **Color and rationale** -- 5 seconds
2. **Asks** -- this is what the sender needs from you
3. **Blockers** -- this tells you whether the team is healthy
4. **Highlights** -- only if you have time

If the sender hides the asks at the bottom or buries the color rationale, push back on the format. Predictable structure is the contract.

---

**Last Updated:** 2026-05-21
