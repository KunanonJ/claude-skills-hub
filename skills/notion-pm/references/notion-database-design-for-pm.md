# Notion Database Design for PM

Canonical database schemas for a product team's Notion workspace. Each section gives:

- Properties (with types and purpose)
- Recommended views
- Key relations to other databases
- Optional formulas/rollups

Conventions:

- `title` is the page's name; every database has exactly one.
- Property names are Title Case.
- `unique_id` properties use a 3-letter prefix (PRD, OKR, DEC, etc.).
- All databases include system properties `Created time`, `Last edited time`, `Created by`, `Last edited by` (implicit).

---

## 1. PRDs Database

| Property | Type | Notes |
|---|---|---|
| Title | title | "PRD: Self-Serve Signup" |
| ID | unique_id (prefix `PRD`) | PRD-001 |
| Status | status | Draft / In Review / Approved / In Build / Shipped / Killed |
| Owner | people | Driving PM (one) |
| Author | people | Original drafter |
| Reviewers | people | Engineering lead, Design lead, others |
| Priority | select | P0 / P1 / P2 / P3 |
| Target Date | date | Aspirational launch |
| Approved On | date | Set when status → Approved |
| Shipped On | date | Set when status → Shipped |
| Areas | multi_select | API / Web / Mobile / Infra / Data |
| Customer Segments | multi_select | SMB / Mid-Market / Enterprise |
| OKR | relation → OKRs | Which OKR(s) this serves |
| Roadmap Item | relation → Roadmap | Roadmap row this delivers |
| Decisions | relation → Decisions | Decision log entries spawned by this PRD |
| Linear Project | url | Live link |
| Jira Epic | url | If using Jira |
| Confidence | select | High / Medium / Low |
| Tech Lead | people | |
| Design Lead | people | |
| Last Reviewed | date | Updated on any quarterly review |
| Days Since Review | formula | `dateBetween(now(), prop("Last Reviewed"), "days")` |

**Recommended views**:
- **My PRDs** — filter: Owner is me; group by Status.
- **In Review** — filter: Status = In Review; sort by Target Date asc.
- **Approved / In Build** — filter: Status in (Approved, In Build); group by Owner.
- **Shipping This Quarter** — filter: Target Date in next 90 days, Status != Killed.
- **Stale (>90 days since review)** — filter: Days Since Review > 90.

---

## 2. OKRs Database

| Property | Type | Notes |
|---|---|---|
| Title | title | "Increase activation rate" |
| ID | unique_id (prefix `OKR`) | OKR-014 |
| Type | select | Objective / Key Result |
| Parent Objective | relation (self) | KRs link to their Objective |
| Quarter | select | Q1 2026, Q2 2026, ... |
| Owner | people | Single accountable |
| Status | status | Not started / On track / At risk / Off track / Hit / Missed |
| Confidence | select | 10 / 7 / 5 / 3 (Wodtke) |
| Target | rich_text | "30% → 45%" |
| Current | rich_text | Updated weekly |
| Progress | number (percent) | Manual or formula from Current/Target if numeric |
| PRDs | relation → PRDs | Contributing PRDs |
| Initiatives | relation → Roadmap | Aggregated initiatives |
| Update Cadence | select | Weekly / Biweekly |
| Last Updated | date | Reflects the latest check-in |

**Rollup ideas**:
- PRDs Count: rollup PRDs relation, count.
- PRDs Shipped: rollup PRDs Status, count where = Shipped.

**Views**:
- **This Quarter by Objective** — group by Parent Objective, filter Quarter = current.
- **My OKRs** — filter: Owner is me.
- **At Risk / Off Track** — filter: Status in (At Risk, Off Track).
- **Confidence Distribution** — Board grouped by Confidence.

---

## 3. Roadmap Database

| Property | Type | Notes |
|---|---|---|
| Title | title | Initiative name |
| ID | unique_id (prefix `ROAD`) | ROAD-007 |
| Horizon | select | Now / Next / Later (or quarters) |
| Status | status | Discovery / Defining / Building / Shipped / Killed |
| Owner | people | Driving PM |
| Customer Outcome | rich_text | Outcome statement |
| OKR | relation → OKRs | What it rolls up to |
| PRDs | relation → PRDs | Underlying PRDs |
| Start | date | Range start |
| End | date | Range end |
| Confidence | select | High / Medium / Low |
| Audience | multi_select | Internal / Customer / Exec |
| Teams Involved | multi_select | Eng / Design / Data / Marketing / Sales |
| Dependencies | relation (self) | Other roadmap items this depends on |

**Rollups**:
- PRDs Count: rollup PRDs relation, count.
- All PRDs Shipped?: rollup PRDs Status, "show original" or "percent per group" to compute health.

**Views**:
- **Timeline (This Year)** — Timeline view; group by Horizon; date source Start/End.
- **Now/Next/Later Board** — Board grouped by Horizon.
- **Customer-Facing** — filter: Audience contains Customer.
- **Exec Read-Out** — filter: Status != Killed, sort by Horizon; show only Title, Customer Outcome, Status, Confidence, End.

---

## 4. Decisions (ADR) Database

| Property | Type | Notes |
|---|---|---|
| Title | title | "Adopt Postgres over MySQL for analytics" |
| ID | unique_id (prefix `DEC`) | DEC-042 |
| Status | select | Proposed / Approved / Superseded / Reversed |
| Date | date | Decision date |
| DACI Driver | people | The Driver (per `daci-framework/`) |
| Approver | people | The Approver |
| Contributors | people | |
| Informed | people | |
| Context | rich_text | What forced the decision |
| Decision | rich_text | Chosen path (the headline) |
| Trade-offs | rich_text | What we accepted/rejected |
| Supersedes | relation (self) | If this overrides a prior decision |
| Superseded By | relation (self, reverse) | Auto via relation |
| Related PRDs | relation → PRDs | |
| Tags | multi_select | architecture / process / hiring / vendor / pricing |

**Page body template** (each row's content):
- Context
- Options Considered (toggle per option, with pros and cons)
- Decision
- Consequences
- Action Items (to-do blocks)
- Review Date (`@date`)

**Views**:
- **Recent** — sort by Date desc.
- **By Tag** — group by Tags.
- **Open Action Items** — filter: pages with unchecked to-do blocks (use Notion's filter on "Has content").

---

## 5. Sprint / Cycle Reviews Database

| Property | Type | Notes |
|---|---|---|
| Title | title | "Sprint 23 Review" or "Cycle 47 Review" |
| Cycle Number | number | For sorting |
| Team | select | Engineering, Design, Data |
| Date | date | Review date |
| Velocity | number | Story points or issue count |
| Throughput | number | Issues completed |
| Cycle Time P50 | number | Days |
| Cycle Time P95 | number | Days |
| Health | select | Green / Yellow / Red |
| Demos | rich_text | What was shown |
| Outcomes | rich_text | What changed for users |
| Carryover | rich_text | What slipped |
| Retro Summary | rich_text | Liked / Learned / Lacked / Longed-for |
| Linked PRDs | relation → PRDs | PRDs touched this cycle |

**Views**:
- **Latest** — sort by Cycle Number desc; limit 1 per Team.
- **Health Over Time** — filter: Team = X; sort by Cycle Number; show Health.

---

## 6. Customer Research Database

| Property | Type | Notes |
|---|---|---|
| Title | title | "Interview: Acme Inc CTO 2026-05-15" |
| ID | unique_id (prefix `RSCH`) | RSCH-128 |
| Type | select | Interview / Survey / Usability / Diary Study |
| Date | date | When |
| Segment | select | SMB / Mid-Market / Enterprise |
| Industry | multi_select | Fintech / Healthtech / E-commerce / SaaS / Other |
| Company | rich_text | |
| Role | rich_text | |
| Interviewer | people | |
| Recording | url | Loom / Zoom |
| Transcript | files | |
| Key Quotes | rich_text | |
| Pains | multi_select | Pre-categorized (cost / time / quality / learning curve) |
| Gains Sought | multi_select | Pre-categorized |
| Linked Opportunities | relation → Opportunities (if using `discovery/interview-synthesis/`) | |
| Linked PRDs | relation → PRDs | If informed a PRD |

**Views**:
- **By Segment** — group by Segment.
- **Recent** — sort by Date desc, limit 25.
- **By Pain** — group by Pains.

---

## 7. 1:1s Database

| Property | Type | Notes |
|---|---|---|
| Title | title | "Alice ↔ Bob — 2026-05-21" |
| Date | date | |
| Partners | people | Both attendees |
| Cadence | select | Weekly / Biweekly / Monthly |
| Agenda Items | rich_text | |
| Action Items | rich_text | |
| Health Check | select | Green / Yellow / Red |
| Topics | multi_select | Career / Project / Feedback / Personal |

**Views**:
- **My 1:1s This Week** — filter: Partners contains me, Date in this week.
- **By Partner** — group by Partners.

---

## 8. Relations Diagram (Conceptual)

```
OKRs ──┬── PRDs ── Decisions
       └── Roadmap ── PRDs
                     ├── Customer Research (informs)
                     └── Sprint Reviews (closes)
```

- OKRs ← PRDs (many-to-many): a PRD can serve multiple KRs; a KR can have multiple PRDs.
- Roadmap ← PRDs (many-to-many): one roadmap item often spans multiple PRDs.
- Decisions ↔ PRDs (many-to-many): decisions emerge from PRDs and shape future ones.
- Customer Research → PRDs (one-to-many): research entries inform specific PRDs.
- Sprint Reviews ← PRDs (many-to-many): a sprint touches multiple PRDs.

---

## 9. Permissions Model

| Database | Read | Comment | Edit |
|---|---|---|---|
| PRDs | All workspace | Product, Eng, Design | Owners and Reviewers |
| OKRs | All workspace | Product, Leadership | Owners |
| Roadmap | All workspace | Product, Leadership | Product team |
| Decisions | All workspace | All workspace | DACI Drivers |
| Sprint Reviews | All workspace | Team members | Team members |
| Customer Research | Product, Eng, Design | Product, Eng, Design | Research team + PMs |
| 1:1s | Participants only | Participants only | Participants only |

Set permissions at the database level; avoid per-row overrides.

---

## 10. Database Hygiene

- **Property audit**: quarterly, remove unused properties (zero non-empty rows in 90 days).
- **Option audit**: quarterly, merge underused select options.
- **Relation audit**: monthly, search for relations pointing to archived rows.
- **Ownership audit**: monthly, flag any row whose Owner has left the team.
- **Stale row audit**: quarterly, archive rows untouched in 180+ days unless explicitly kept.
