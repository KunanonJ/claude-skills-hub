# Notion Roadmap Template

Drop-in schema and view definitions for the Roadmap database. Copy the property list into a new Notion database, then create the views described below.

---

## Database properties

| Property | Type | Configuration |
|---|---|---|
| Title | title | (required) |
| ID | unique_id | Prefix: `ROAD` |
| Horizon | select | Options: `Now`, `Next`, `Later` (or `Q1 2026`, `Q2 2026`, ...) |
| Status | status | To-do: `Discovery` · In progress: `Defining`, `Building` · Complete: `Shipped`, `Killed` |
| Owner | people | One PM |
| Customer Outcome | rich_text | One sentence outcome |
| OKR | relation | → OKRs database |
| PRDs | relation | → PRDs database |
| Start | date | Range start |
| End | date | Range end |
| Confidence | select | `High` (green) / `Medium` (yellow) / `Low` (red) |
| Audience | multi_select | `Internal`, `Customer`, `Exec`, `Board` |
| Teams Involved | multi_select | `Eng`, `Design`, `Data`, `Marketing`, `Sales`, `Support` |
| Dependencies | relation (self) | Cross-row dependencies |
| Last Updated | date | Auto-set on status change (manual or automation) |
| Latest Update | rich_text | One-paragraph update |
| Risk Level | select | `Low` / `Medium` / `High` |
| Customer Quotes | rich_text | Pull quotes for exec views |
| PRD Count | rollup | Source: PRDs, property: Title, calc: Count |
| PRDs Shipped | rollup | Source: PRDs, property: Status, calc: Count where = Shipped |

---

## Recommended views

### View 1: Timeline (Default)

- **Type:** Timeline
- **Date source:** Start / End
- **Group by:** Horizon
- **Filter:** Status not in (Killed)
- **Sort:** Start ascending
- **Visible properties:** Title, Owner, Status, Confidence, OKR, PRD Count
- **Use:** Quarterly planning, sequencing, dependency conflicts

### View 2: Now / Next / Later Board

- **Type:** Board
- **Group by:** Horizon
- **Filter:** Status not in (Killed, Shipped)
- **Sort:** Confidence descending, then Start ascending
- **Visible properties:** Owner, Customer Outcome, OKR, Confidence, Risk Level
- **Use:** Strategic conversations, team standups

### View 3: Exec Read-Out

- **Type:** Table
- **Filter:** Audience contains Exec; Status not in (Killed)
- **Sort:** Horizon ascending, then Start ascending
- **Visible properties (in order):** Title, Customer Outcome, Owner, Status, Confidence, End, Latest Update, Risk Level
- **Hidden:** PRDs, Dependencies, Teams Involved
- **Use:** Monthly exec roadmap review; export as PDF

### View 4: Customer-Facing

- **Type:** Gallery
- **Filter:** Audience contains Customer; Status not in (Killed)
- **Card preview:** page content or cover image
- **Visible properties:** Customer Outcome, Horizon, End, Confidence
- **Use:** Source for customer-facing roadmap pages, sales decks

### View 5: At Risk

- **Type:** Table
- **Filter:** (Risk Level = High) OR (Confidence = Low) OR (Status = Defining AND End < today + 30d)
- **Sort:** End ascending
- **Visible properties:** Title, Owner, Status, Risk Level, Confidence, End, Latest Update
- **Use:** Weekly portfolio risk review

### View 6: Dependencies Graph

- **Type:** Table grouped by Owner
- **Filter:** Dependencies is not empty
- **Sort:** Start ascending
- **Visible properties:** Title, Dependencies, Owner, End
- **Use:** Identify critical-path coordination needs (also see `execution/dependency-map/`)

### View 7: Shipped (Archive)

- **Type:** Table
- **Filter:** Status = Shipped
- **Sort:** End descending
- **Visible properties:** Title, Owner, Customer Outcome, OKR, End, PRD Count
- **Use:** Retrospective, "what shipped this quarter" updates

---

## Page body template (for each roadmap row)

```
# <Initiative Name>

> [!NOTE]
> **Customer outcome:** <one sentence>
> **OKR:** @OKR-014 (Increase activation to 45%)
> **Horizon:** Now · **Confidence:** Medium · **Owner:** @PM

## Problem
What customer/business problem this initiative solves.

## Strategy
The approach and why it is the right one now.

## Phases / Milestones
| Phase | Description | Target |
|---|---|---|
| Discovery | Customer interviews + prototype | YYYY-MM-DD |
| Build MVP | Core flow shipped to alpha | YYYY-MM-DD |
| Iterate | Validate metrics, expand scope | YYYY-MM-DD |
| GA | General availability | YYYY-MM-DD |

## Underlying PRDs
- @PRD-018: <PRD title>
- @PRD-024: <PRD title>

## Dependencies
- @ROAD-005 (depends on auth-svc rewrite)

## Risks
- <Risk 1>: mitigation
- <Risk 2>: mitigation

## Latest update (YYYY-MM-DD)
- <bullet>
- <bullet>

## Customer voice
> "<quote>" — @Customer Research entry
```

---

## Automation suggestions

- **On Status → Shipped:** auto-set `End` to today.
- **On Status change:** prompt Owner to update `Latest Update` (Slack reminder).
- **Weekly Friday:** post a summary of At Risk view items to `#leadership-roadmap`.
- **On PRD Status → Shipped:** rollup `PRDs Shipped` increments; auto-recompute progress.

---

## Audit cadence

- **Weekly:** Owner reviews their rows; updates `Latest Update` and `Risk Level`.
- **Monthly:** Head of Product reviews At Risk view; rebalances confidence.
- **Quarterly:** Full roadmap review; merge/split rows; promote `Next` → `Now`.
- **Annually:** Archive Shipped rows older than 18 months to a "Roadmap Archive" database.
