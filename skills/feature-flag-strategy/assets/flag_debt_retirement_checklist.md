# Flag Debt Retirement Checklist

A working checklist for retiring an individual feature flag, plus a quarterly audit procedure to keep flag count from growing unbounded. Use this with a flag inventory dashboard (LaunchDarkly / Statsig / Optimizely / Unleash all surface stale-flag reports natively).

---

## Part A: Per-flag retirement checklist

Use for any flag eligible for retirement (release toggle at 100% for 30+ days, experiment toggle whose experiment has concluded, dead-feature 0% toggle).

**Flag name:** ____________________
**Owner:** ____________________
**Retirement date target:** ____________________

### Pre-conditions

- [ ] Flag has been at 100% (or 0% for dead features) for >= 30 days.
- [ ] No regression has been triaged in the last 30 days that the flag would mitigate.
- [ ] All customers have migrated (for sunset / dead-feature flags).
- [ ] Owner has reviewed and approved retirement.

### Code removal

- [ ] Identify every code path that checks the flag.
- [ ] Determine the surviving branch (typically the "on" branch for release toggles; the "off" branch for retiring features).
- [ ] Remove the flag check; promote the surviving branch.
- [ ] Remove the dead branch entirely.
- [ ] Remove any helper functions or constants that exist only for the flag.
- [ ] Update unit tests: remove tests that assert both branches; keep tests that assert the surviving behavior.

### Configuration cleanup

- [ ] Remove the flag entry from the flag service.
- [ ] Remove any environment-specific overrides.
- [ ] Remove the flag from any per-tenant override tables.
- [ ] Update flag-inventory documentation.

### Documentation

- [ ] Update the team's runbook (if the flag was referenced).
- [ ] Update SRE runbooks (if the flag was operational).
- [ ] Update customer-facing docs (if the flag was a permission flag now being made universal).
- [ ] File a final archive note: `<flag-name>: type, owner, lived from <date> to <date>, retired because <reason>`.

### Test matrix

- [ ] Remove the flag from any explicit test-matrix configurations.
- [ ] Verify CI passes with the flag removed.
- [ ] Verify the feature works in staging without the flag.

### Communication

- [ ] Notify the team in standup or async update.
- [ ] If the flag was visible to customers (rare), confirm no customer-facing change.

### Verification (post-merge)

- [ ] Production check: confirm no residual flag references in logs.
- [ ] Production check: confirm metrics are stable post-removal.
- [ ] Close the retirement ticket.

---

## Part B: Quarterly flag-debt audit

Run every 12-14 weeks. Time budget: 1-2 hours for the audit, plus retirement PRs that follow.

### Step 1: Pull the inventory

From the flag service, export the live-flag list. Include:
- Flag name
- Type (if classified)
- Owner / team
- Created date
- Last flip date
- Current rollout %
- Environment(s)

### Step 2: Classify

For every flag, confirm its type. Common mis-classifications:

- A flag labeled "release toggle" that has been at 100% for >180 days is probably an unretired flag, not an active release toggle.
- A flag labeled "permission toggle" that gates by user-id rather than by plan/role is probably tenant-specific config, not a permission flag.
- A flag with no labels is a defect; assign one.

### Step 3: Identify retirement candidates

Filter for:

| Filter | Action |
|---|---|
| Release toggle at 100% > 30 days | Retire |
| Release toggle at 0% > 30 days (feature dead) | Retire |
| Experiment toggle past decision date by > 14 days | Retire |
| Flag with no owner | Assign owner first, then re-evaluate |
| Flag with no last-flip > 90 days, not Ops or Permission | Retire candidate |
| Flag referenced in fewer than 3 places in code | Trivial retire |

### Step 4: Identify mis-classified flags

| Filter | Action |
|---|---|
| Release toggle still live > 180 days | Re-classify as permission / ops, OR retire |
| Permission flag using a dynamic per-request evaluation | Re-architect as static evaluation |
| Ops flag without a documented runbook entry | Document |
| Experiment toggle with no decision date | Set decision date or retire |

### Step 5: Score the team

| Metric | Target | This quarter |
|---|---|---|
| Total live flags | < 15 per team | |
| Release toggles older than 30 days | 0 | |
| Experiment toggles past decision date | 0 | |
| Flags without an owner | 0 | |
| Flags retired this quarter | >= 5 | |
| Flag count delta (vs last quarter) | <= 0 | |

If "total live flags" exceeds 30 per team, the team has flag debt as a system problem, not a per-flag problem. Schedule a dedicated retirement sprint.

### Step 6: Action items

| # | Flag | Action | Owner | Due |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

### Step 7: Process improvements

If the audit surfaces repeat patterns:

- "We keep forgetting to retire release toggles" -> add retirement PR as a launch-checklist requirement; tooling to auto-open the PR at flag creation.
- "Owners leave; flags orphan" -> ownership is team-level, not individual; re-assign at team reorg.
- "We don't know what a flag controls" -> require a description field; reject flag creation without one.
- "Our test matrix exploded" -> retire more flags; do not test impossible combinations.

---

## Part C: Anti-patterns to surface in the audit

| Anti-pattern | How to detect | Fix |
|---|---|---|
| Permanent release toggle | Release toggle at 100% > 90 days | Retire or re-classify |
| Zombie experiment | Experiment toggle past decision date with no decision | Retire; document the experiment outcome |
| Orphan flag | Owner left, no successor | Assign team owner; review with team lead |
| Test-only flag in prod | Flag exists only for testing but is configured in production | Move to env-specific config |
| Flag used as feature flag and as A/B test | Single flag does double duty | Split into two flags |
| Mystery flag | No description, no recent activity, unclear purpose | Investigate; retire if no purpose found |

---

## Part D: Onboarding new-team-member checklist

When a new engineer / PM joins the team:

- [ ] Walk through the team's flag inventory in their first week.
- [ ] Show the flag-naming convention.
- [ ] Show the kill-switch decision tree.
- [ ] Show the retirement checklist.
- [ ] Add the new joiner to the flag-service permissions appropriate to their role.
- [ ] Ensure the new joiner is on the rota for the quarterly audit.

---

**Last updated:** 2026-05-22
