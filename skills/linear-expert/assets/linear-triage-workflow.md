# Linear Triage Workflow Template

A standard operating procedure for daily triage on a Linear team. Copy this into a pinned Linear issue titled "Triage SOP" and adapt the bracketed values.

---

## Purpose

Triage is the gate between "something arrived" and "the team has agreed to do something about it." A healthy triage practice:

- Prevents inbound noise from polluting cycle planning.
- Ensures every customer-impacting issue gets attention within `[1 business day]`.
- Catches duplicates before they fragment the conversation.
- Surfaces patterns (e.g. five related bugs from the same area) early.

## Sources Feeding Triage

| Source | Integration | Lands in |
|---|---|---|
| Slack (`/linear` command) | Built-in | Triage with `slack` label |
| GitHub Issues mirror | Built-in | Triage with `github` label |
| Customer support (Zendesk/Front/Intercom) | Plugin or webhook | Triage with `customer-request` label |
| API (internal tools) | Custom | Triage with the calling tool's name as a label |
| Cron / monitoring (Datadog, Sentry) | Webhook | Triage with `monitoring` + `type/incident` labels |

## Rotation

- **Triage owner:** rotates `[daily]` among `[team members]`.
- **Backup:** the previous day's owner.
- **Calendar:** post the rotation in `#team-[name]` and pin.
- **Time commitment:** ~15 minutes/day, ~45 minutes if the queue is over 20 items.

## Daily Triage Procedure

For each item in the Triage view, work top to bottom:

### Step 1 — Comprehend
- Read the title and description.
- If it is unclear, leave a comment requesting more info; assign back to the reporter; keep in Triage.

### Step 2 — Deduplicate
- Search for similar issues (`/` then keyword). If a duplicate exists:
  - Add a comment linking to the canonical issue.
  - Mark this issue as Canceled with the canonical issue linked via the "duplicate of" relation.
  - Done.

### Step 3 — Categorize
Apply at minimum:
- One `type/*` label (`bug`, `feature`, `chore`, `spike`, `incident`).
- One `area/*` label (`api`, `web`, `mobile`, `infra`, `data`).
- Any source label that did not auto-apply (`customer-request`, `monitoring`).

### Step 4 — Prioritize
Set priority based on the rubric:

| Priority | When | SLA from triage |
|---|---|---|
| `1` Urgent | Production down, security exposure, top-10 customer blocked | Owner assigned same day; work starts within 24h |
| `2` High | Multiple customers affected, no workaround, or critical feature gap | Owner assigned in this cycle; work starts in this cycle |
| `3` Medium | Customer impact with workaround, or strategic feature | Considered in next cycle planning |
| `4` Low | Polish, nice-to-have, internal-only | Backlog; revisited quarterly |
| `0` No priority | Use sparingly; usually fix priority instead | n/a |

### Step 5 — Route
Based on type and area:
- **Bug, area in scope:** assign to an owner on this team; move to `Todo`.
- **Bug, area out of scope:** reassign the issue to the correct team; leave a comment.
- **Feature request:** attach to an existing Project if it fits; otherwise leave priority-tagged in Backlog for next cycle planning.
- **Incident:** assign to the on-call engineer immediately; create a follow-up "incident review" issue.

### Step 6 — Move Out of Triage
Once steps 1-5 are complete, change the state from `Triage` to:
- `Todo` if it has an owner and a cycle.
- `Backlog` if it is real but not committed.
- `Canceled` if it was a duplicate, won't-do, or invalid.

Triage is empty when no item has state type `triage`.

## Edge Cases

**Item I cannot triage in 5 minutes:**
- Add a comment with my best guess at categorization.
- Tag the area's tech lead with a question.
- Leave it in Triage; flag it in the next standup.

**Item that needs product input:**
- Reassign to the team's PM in triage; add `needs-pm-input` label.
- The PM has 2 business days to respond; otherwise it returns to triage.

**Item from a customer with a workaround:**
- Reply via the support channel (don't make the customer learn Linear).
- Categorize and prioritize as normal.

**Item that turns out to be a spike or research request:**
- Apply `type/spike` and a time-box estimate.
- Define the writeup as the acceptance criteria.

## Weekly Triage Review

Every `[Friday]`, the team lead spends 15 minutes:
- Counts items triaged vs items closed during the week.
- Notes any repeat patterns (5 bugs in the same area → tech-debt project?).
- Reviews any items that bounced between teams (sign of unclear ownership).
- Posts a brief summary in `#team-[name]-updates`.

## Metrics to Track

- **Triage queue size:** target < `[10]` items at end of each day.
- **Time-in-triage:** P50 < `[24h]`, P95 < `[3 days]`.
- **Triage → Done conversion:** what % of triaged items eventually ship vs get canceled?
- **Source distribution:** which inbound source produces the most actionable issues?

Pull these from Linear Insights or by querying the GraphQL API on a schedule.

## Anti-Patterns

- Letting items sit in Triage for more than 5 business days.
- Skipping labels because "I'll get to it later."
- Assigning every triaged item to the team lead by default.
- Treating Triage as a backlog (Backlog is for items the team has decided to do).
- Triaging in bulk once a week (loses freshness; lets urgent items rot).
