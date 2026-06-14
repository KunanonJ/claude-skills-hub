# Linear Team Configuration Template

Copy this checklist when creating a new Linear team. Adjust the bracketed values; defaults reflect what works for a 5-15 person product engineering team shipping a SaaS product.

---

## 1. Team Identity

- **Team name:** `[Engineering]`
- **Team key:** `[ENG]` (2-4 uppercase letters; immutable; prefixes every issue ID)
- **Team icon and color:** pick something distinct from other teams
- **Description:** one sentence on the team's mission

## 2. Cycles

- **Cycles enabled:** Yes (set No only for support/triage-only teams)
- **Cycle duration:** `[2 weeks]`
- **Cycle starts on:** `[Monday]`
- **Auto-archive completed cycles after:** `[6 cycles]`
- **Upcoming cycles to show:** `[3]`

## 3. Triage

- **Triage enabled:** Yes (almost always; the inbox for inbound issues)
- **Triage responsibility:** rotation, one person per day or per cycle
- **Auto-assign new issues to triage when:** created via integration, API, or by a non-team-member

## 4. Estimation

- **Scale:** `[Fibonacci]` (0, 1, 2, 3, 5, 8) — closest analog to Jira story points
- **Allow zero estimate:** Yes (use for genuinely trivial work)
- **Enforce estimates before issues enter a cycle:** Yes (team norm; not auto-enforced)

## 5. Workflow States

Use the default 6-state workflow unless there is a specific need:

| Type | State Name | Notes |
|---|---|---|
| `triage` | Triage | Inbox for unrouted issues |
| `backlog` | Backlog | Future work, not yet committed |
| `unstarted` | Todo | Committed to a cycle but not started |
| `started` | In Progress | Active work |
| `started` | In Review | PR open / awaiting QA |
| `completed` | Done | Shipped / closed as done |
| `canceled` | Canceled | Won't do, duplicate, obsolete |

Resist adding more states; use labels for nuance (e.g. `status/blocked`, `status/awaiting-customer`).

## 6. Labels (recommended starter set)

### Type label group (mutually exclusive)
- `type/feature`
- `type/bug`
- `type/chore`
- `type/spike`
- `type/incident`

### Area label group (mutually exclusive)
- `area/api`
- `area/web`
- `area/mobile`
- `area/infra`
- `area/data`

### Free-form labels
- `tech-debt`
- `customer-request`
- `security`
- `breaking-change`
- `good-first-issue`

## 7. Members and Permissions

- **Team admins:** 2 (the team lead + one backup)
- **Members:** every IC and manager on the team
- **Guests:** designers, PMs, support engineers who file issues but do not own delivery

## 8. Integrations

- **GitHub:** install Linear GitHub app; connect the team's primary repos.
- **Slack:** route Initiative updates and Project status updates to `#team-[name]-updates`.
- **PagerDuty / on-call:** if applicable, auto-create incidents as Linear issues with `type/incident`.
- **Figma:** enable the Figma integration so attached frames render inline.

## 9. Templates

Create 3-5 issue templates the team will actually use:

- **Bug report** — sections for repro, expected, actual, environment.
- **Feature request** — problem, proposed solution, success criteria.
- **Spike** — question, time-box, acceptance criteria for the writeup.
- **Incident** — timeline, impact, root cause, follow-ups (link to postmortem).
- **Tech-debt** — debt description, cost of inaction, proposed fix.

## 10. Cadences

| Ceremony | Frequency | Owner |
|---|---|---|
| Cycle planning | Monday of cycle start | Team lead |
| Cycle review | Friday before cycle end | Team lead |
| Triage rotation | Daily, ~15 min | Rotating |
| Initiative update | Weekly | Initiative owner |
| Project status update | Weekly | Project lead |

## 11. Conventions Document

Pin a Linear issue titled "Team conventions" with:
- This template, filled in.
- Branch naming convention (`<user>/eng-<number>-<slug>`).
- PR magic words (`Fixes ENG-123`).
- Estimation rubric (what does a 3 mean vs a 5?).
- Definition of done.

## 12. Audit Schedule

- **Quarterly:** review labels (merge unused, retire stale).
- **Quarterly:** review templates (are they being used? still relevant?).
- **Quarterly:** review automations and integrations.
- **Annually:** review workflow states (is the team still happy with the shape?).
