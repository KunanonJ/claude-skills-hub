# Cross-Team Dependency Weekly Sync

**Program:** [Program name]
**Cadence:** Every [day] at [time], 45 minutes
**Facilitator:** [PM / Program Manager name]
**Required attendees:** One named representative per team with current dependencies
**Optional attendees:** Exec sponsor (monthly check-in only)
**Source of truth:** [Link to dependencies.json]

---

## Standing Agenda (45 min)

### 1. Critical Path Walk (15 min)

Generated from `dependency_graph.py --format markdown`.

For each item on the critical path:
- **Status update** from owner (30 sec max)
- **Blockers** (specific, not "it's hard")
- **Ask** (what does this dep need from the room right now?)

| ID | From | To | Description | Owner | Status | Slack | Ask |
|----|------|----|----|--------|--------|------:|-----|
| | | | | | | | |

### 2. At-Risk Items (10 min)

Items not on critical path but with negative or low slack, status `blocked` or `at_risk`.

For each: one-sentence status, plan to recover, escalation if needed.

| ID | From | To | Description | Status | Slack | Recovery Plan |
|----|------|----|----|--------|------:|--------------|
| | | | | | | |

### 3. New Dependencies (5 min)

Anything added since last sync.

| ID | Description | Reason for addition | Added by |
|----|-------------|--------------------|----------|
| | | | |

### 4. Closed and Unblocked (2 min)

Mark `done` in the JSON. Acknowledge the contributor.

| ID | Description | Closed by | Date |
|----|-------------|-----------|------|
| | | | |

### 5. Conway's Signals (3 min)

Anything that looks like a recurring pattern between the same teams. Tag for the quarterly Conway's review.

> Example: "Mobile <-> Platform is now 4 open deps; this is the 3rd quarter in a row. Recommend quarterly review for permanent interface."

### 6. Action Items and Owners (10 min)

| Action | Owner | Due |
|--------|-------|-----|
| | | |
| | | |

---

## Pre-Sync Preparation (PM checklist)

- [ ] Update `dependencies.json` with status changes from the past week
- [ ] Run `python dependency_graph.py --input dependencies.json --format markdown` and paste into the meeting doc
- [ ] Run `--format mermaid` and update the published graph (README / Notion / Confluence)
- [ ] Confirm critical-path items have named owners; chase if missing

## Post-Sync Followup (PM checklist)

- [ ] Update `dependencies.json` with sync decisions
- [ ] Push commit to dependency repo with summary of changes
- [ ] Post sync summary in program channel
- [ ] Calendar-block next sync if missing

---

## Escalation Path

| Severity | Trigger | Escalate To | Within |
|----------|---------|-------------|-------|
| Sync risk | Critical-path item slipped > 3 days | Program manager + producer team lead | 24h |
| Program risk | Critical path delayed > 1 week | Exec sponsor | 48h |
| Conway signal | Same team pair > 4 open deps for 2+ quarters | Org leadership | Next quarterly review |

---

## Quarterly Conway's Review (separate meeting)

Held once per quarter, 60 minutes.

1. Top team-pair dependency counts for the quarter (data from `--by_team_pair`).
2. Any pair >25% of total deps -> discuss merge / interface / dedicated PM response.
3. Update org-design proposals (if any).
4. Confirm next quarter's program manager assignments.
