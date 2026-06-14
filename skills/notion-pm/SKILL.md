---
name: notion-pm
description: >
  Notion expert for product management workflows. Covers database design for
  PRDs, OKRs, Roadmaps, and Decisions; property types (relation, rollup,
  formula); view design (Board, Timeline, Calendar, Gallery, Table); page
  architecture; Notion-flavored Markdown blocks; Notion REST API patterns;
  and sync patterns with Jira, Linear, and GitHub.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-integration
  updated: 2026-05-21
  tech-stack: [notion, rest-api, jira, linear, github]
  tags: [notion, databases, prd, okr, roadmap, decisions]
---
# Notion for Product Management

Master-level expertise in using Notion as the documentation and operational backbone for a product team: PRDs, OKRs, roadmaps, decision logs, sprint reviews, 1:1 notes, customer research, and sync patterns with Jira, Linear, and GitHub. Covers Notion's database model, view design, formula and rollup patterns, page architecture, and REST API.

## Overview

Notion's PM value comes from its database model: every meaningful PM artifact (a PRD, an OKR, a roadmap row, a decision) becomes a row in a typed database, with relations to other databases. This unlocks linked views (one source of truth, many surface presentations), rollups (aggregate child progress into a parent), and a queryable API. The job of a Notion PM expert is to design these databases up front, restrain ad-hoc page creation, and tie the workspace into Jira/Linear/GitHub so the artifacts stay current without manual maintenance.

### When to Use

- Standing up a new product team's documentation workspace
- Designing a PRD, OKR, Roadmap, or Decisions database from scratch
- Refactoring an existing Notion workspace that has grown into a sprawl of unrelated pages
- Building roadmap or status views aggregated from underlying issue trackers
- Authoring Notion REST API calls (page creation, database queries, block updates)
- Setting up two-way sync between Notion and Jira/Linear/GitHub
- Establishing governance: ownership, review cadence, archive strategy

## Concepts

### Workspace Hierarchy

| Level | Purpose | Example |
|---|---|---|
| **Workspace** | Top-level account, billing scope, SCIM/SAML | "Acme Inc" |
| **Teamspace** | Permission boundary for a team or function | "Product", "Engineering" |
| **Page** | A document or container | "Onboarding wiki" |
| **Database** | Typed collection of pages (rows = pages with properties) | "PRDs DB", "OKRs DB" |
| **Database row** | A page whose parent is a database | "PRD: Self-Serve Signup" |
| **Linked Database** | A view of another database, embedded in a page | A "This Quarter" view of the PRDs DB |
| **Block** | A unit of content inside a page (paragraph, heading, callout, toggle, image, embed) | "Heading 2", "Callout", "Synced Block" |

### Property Types (the heart of database design)

| Type | Use | Notes |
|---|---|---|
| `title` | The row's name; every database has exactly one | Renders as the page title |
| `rich_text` | Long-form text | Supports markdown formatting |
| `select` | Single-value tag from a closed list | E.g. PRD status: Draft / Review / Approved / Shipped |
| `multi_select` | Multi-value tags | E.g. PRD area: API, Web, Mobile |
| `status` | Special select with three groups: To-do, In progress, Complete | First-class in views |
| `date` | Date or date range | Supports reminders |
| `people` | Reference to workspace member(s) | Owner, reviewer |
| `files` | Attached files or URLs | Specs, mocks |
| `checkbox` | Boolean | Approved? |
| `url`, `email`, `phone` | Typed contact data | Customer DB |
| `number` | Numeric with optional format (percent, currency) | Confidence, RICE score |
| `formula` | Computed from other properties | E.g. RICE = (R*I*C)/E |
| `relation` | Link to row(s) in another database | PRD → OKR, PRD → Roadmap Item |
| `rollup` | Aggregate property of related rows | "Sum of estimates from linked Linear issues" |
| `created_time`, `last_edited_time` | System | Always present |
| `created_by`, `last_edited_by` | System | Always present |
| `unique_id` | Auto-incremented short ID with prefix | E.g. PRD-001, DEC-042 |

### Views

Every database can present multiple views, each with its own filter, sort, group, and property visibility:

- **Table** — spreadsheet-like; default editing view
- **Board** — Kanban grouped by a select/status property; great for PRD status, OKR confidence
- **Timeline** — Gantt-like; great for Roadmaps when there is a date-range property
- **Calendar** — month view; great for launches, reviews, sprint ceremonies
- **Gallery** — card view with the cover image; great for customer research notes or design reviews
- **List** — minimal, dense; great for backlog-style browsing

### Notion-Compatible Markdown / Block Types

Notion is not strictly Markdown, but Markdown extensions are recognized in many contexts. Key blocks used in PM artifacts:

- Headings: `#`, `##`, `###`
- Callouts: `> [!NOTE]`, `> [!WARNING]`, `> [!TIP]` (in Markdown imports; native block in UI)
- Toggle blocks: collapse-expand sections (great for "Open questions", "Out of scope")
- Synced blocks: a single block reused across pages (Definition of Done, glossary)
- Code blocks: fenced with language for syntax highlighting
- Linked databases: a view of another DB embedded inline
- Mentions: `@person`, `@page`, `@date`
- Bookmarks: a URL becomes a rich preview card
- Embeds: Figma, Loom, GitHub Gist, YouTube
- Math: `$equation$` inline; `$$equation$$` block

## Core Workflows

### 1. Workspace Setup for a Product Team

1. Create a Teamspace named `Product`.
2. Create the foundational databases as direct children of the Teamspace:
   - PRDs
   - OKRs (with quarter as a property)
   - Roadmap
   - Decisions
   - Customer Research
   - Sprint Reviews (or Cycle Reviews if on Linear)
   - 1:1s
3. Define the relations between them (see `references/notion-database-design-for-pm.md`).
4. Create a Teamspace home page with a curated set of linked database views.
5. Establish naming conventions; pin them in a "Team conventions" page.
6. Set permissions: full access for product team, edit for engineering, view for everyone else.
7. **HANDOFF TO**: PMs to start populating PRDs and OKRs.

### 2. PRD Database Design

A PRD is a row in the PRDs database. Properties:

| Property | Type | Purpose |
|---|---|---|
| `Title` | title | PRD name |
| `Status` | status | Draft / In Review / Approved / In Build / Shipped / Killed |
| `Owner` | people | Driving PM |
| `Author` | people | Original drafter |
| `Reviewers` | people | DRI, Eng lead, Design lead |
| `Target Date` | date | Aspirational launch |
| `Priority` | select | P0 / P1 / P2 / P3 |
| `OKR` | relation → OKRs | Which OKR(s) this serves |
| `Roadmap Item` | relation → Roadmap | Which roadmap item this delivers |
| `Linear Project` | url | Link to the Linear Project tracking the work |
| `Jira Epic` | url | If using Jira |
| `Tech Lead` | people | Engineering DRI |
| `Design Lead` | people | Design DRI |
| `Approved On` | date | Set when status → Approved |
| `Shipped On` | date | Set when status → Shipped |
| `Document` | (page body) | The PRD itself, with the template from `assets/notion-prd-template.md` |

Build views:
- **My PRDs** (filter: Owner is me)
- **In Review** (filter: Status = In Review; sort by Target Date)
- **This Quarter** (filter: Target Date in this quarter, group by Status)
- **All by Owner** (group by Owner, hide killed)

### 3. OKR Database Design

| Property | Type | Purpose |
|---|---|---|
| `Title` | title | KR or Objective name |
| `Type` | select | Objective / Key Result |
| `Parent Objective` | relation (self) | For KRs, link to parent Objective |
| `Quarter` | select | Q1 2026, Q2 2026, ... |
| `Owner` | people | Single accountable owner |
| `Status` | status | Not started / On track / At risk / Off track / Hit / Missed |
| `Confidence` | select | 10 / 7 / 5 / 3 (Wodtke scale) |
| `Target` | rich_text | The measurable target |
| `Current` | rich_text | Current value (updated weekly) |
| `Progress` | number (percent) | Manual or formula |
| `PRDs` | relation → PRDs | PRDs that contribute to this KR |
| `Notes` | rich_text | Context, blockers |

Views:
- **This Quarter by Objective** (group by Parent Objective)
- **My OKRs** (filter: Owner is me)
- **At Risk / Off Track** (filter on Status)

### 4. Roadmap Database Design

| Property | Type | Purpose |
|---|---|---|
| `Title` | title | Initiative name |
| `Horizon` | select | Now / Next / Later (or Q1 / Q2 / Q3 / Q4) |
| `Status` | status | Discovery / Defining / Building / Shipped / Killed |
| `Owner` | people | Driving PM |
| `Customer Outcome` | rich_text | Outcome statement |
| `OKR` | relation → OKRs | What this rolls up to |
| `PRDs` | relation → PRDs | Underlying PRDs |
| `Start` | date | Range start |
| `End` | date | Range end |
| `Confidence` | select | High / Medium / Low |
| `Audience` | multi_select | Internal / Customer / Exec |

Views:
- **Timeline** (grouped by Horizon, dates from Start/End)
- **Now/Next/Later Board** (grouped by Horizon)
- **Customer-Facing** (filter: Audience contains Customer)

### 5. Decisions (ADR-style) Database

| Property | Type | Purpose |
|---|---|---|
| `Title` | title | Decision name |
| `ID` | unique_id (prefix DEC) | Auto-numbered |
| `Status` | select | Proposed / Approved / Superseded / Reversed |
| `Date` | date | Decision date |
| `DACI Driver` | people | The Driver |
| `Approver` | people | The Approver |
| `Contributors` | people | Contributors |
| `Informed` | people | Informed parties |
| `Context` | rich_text | What forced the decision |
| `Options` | (page body) | Options considered with pros/cons |
| `Decision` | rich_text | Chosen path |
| `Supersedes` | relation (self) | If this overrides a prior decision |

### 6. Sprint / Cycle Review Database

| Property | Type | Purpose |
|---|---|---|
| `Title` | title | "Sprint 23 Review" or "Cycle 47 Review" |
| `Cycle Number` | number | For sorting |
| `Date` | date | Review date |
| `Team` | select | Engineering, Design, Data, ... |
| `Velocity` | number | Story points or issue count |
| `Health` | select | Green / Yellow / Red |
| `Demos` | rich_text | What was shown |
| `Outcomes` | rich_text | What changed for users |
| `Retro` | (page body) | Liked / Learned / Lacked / Longed-for |

### 7. Linking Strategy

Three layers of linking:

1. **Relations** for many-to-many DB joins (PRD ↔ OKR, PRD ↔ Roadmap).
2. **Mentions** for one-off references inside page bodies (`@PRD: Self-Serve Signup`).
3. **Sub-pages** only for hierarchical content that does not warrant a database (e.g. PRD has a child page "Open Questions").

Avoid: linking with raw markdown links to other Notion pages (loses bidirectionality and search relevance).

### 8. Sync Patterns

**Notion ↔ Jira**
- One-way: build a Zapier/Make/n8n job that, on PRD status change, creates the linked Jira Epic.
- Two-way (advanced): periodically diff PRD status and Jira Epic status; reconcile.
- Embed: paste a Jira issue URL; Notion renders a rich preview (read-only).

**Notion ↔ Linear**
- One-way: on PRD approval, create a Linear Project; store its URL in `Linear Project` property.
- Roll-up: a scheduled job queries Linear's GraphQL API for project progress and writes back to a Notion number property.
- Embed: paste a Linear issue/project URL for a rich preview.

**Notion ↔ GitHub**
- Embed: PR and Issue URLs render as rich previews.
- Custom: a webhook handler creates Decisions DB rows when an ADR is added to a repo.

See `references/notion-api-patterns.md` for the API calls these patterns use.

## API / Query Patterns

The Notion API is REST, served at `https://api.notion.com/v1/`. Auth is via integration tokens (`Authorization: Bearer secret_...`). Every request must include `Notion-Version: 2022-06-28` (or the current version). See `references/notion-api-patterns.md` for the full library.

**Query a database** (find all PRDs in review):
```bash
curl -X POST https://api.notion.com/v1/databases/<db_id>/query \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "filter": {
      "property": "Status",
      "status": { "equals": "In Review" }
    },
    "sorts": [{ "property": "Target Date", "direction": "ascending" }]
  }'
```

**Create a page in a database** (new PRD):
```bash
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent": { "database_id": "<prd_db_id>" },
    "properties": {
      "Title":   { "title":  [{ "text": { "content": "PRD: Self-Serve Signup" } }] },
      "Status":  { "status": { "name": "Draft" } },
      "Owner":   { "people": [{ "id": "<user_id>" }] },
      "Target Date": { "date": { "start": "2026-09-30" } }
    },
    "children": [
      { "object": "block", "type": "heading_2",
        "heading_2": { "rich_text": [{ "text": { "content": "Problem" } }] } },
      { "object": "block", "type": "paragraph",
        "paragraph": { "rich_text": [{ "text": { "content": "..." } }] } }
    ]
  }'
```

**Update a page property** (mark PRD approved):
```bash
curl -X PATCH https://api.notion.com/v1/pages/<page_id> \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "properties": {
      "Status":      { "status": { "name": "Approved" } },
      "Approved On": { "date":   { "start": "2026-05-21" } }
    }
  }'
```

**Append blocks to a page** (add a section):
```bash
curl -X PATCH https://api.notion.com/v1/blocks/<page_id>/children \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "children": [
      { "object": "block", "type": "callout",
        "callout": {
          "icon":     { "type": "emoji", "emoji": "ℹ" },
          "rich_text": [{ "text": { "content": "Approved by Product Council on 2026-05-21." } }]
        }
      }
    ]
  }'
```

**Paginate through a large database** (handle `has_more`):
```bash
# Pass `start_cursor` from the previous response on each subsequent call
curl -X POST https://api.notion.com/v1/databases/<db_id>/query \
  -d '{ "page_size": 100, "start_cursor": "<cursor>" }'
```

**Compound filter** (PRDs owned by me and in review):
```json
{
  "filter": {
    "and": [
      { "property": "Owner",  "people": { "contains": "<user_id>" } },
      { "property": "Status", "status": { "equals": "In Review" } }
    ]
  }
}
```

### Rate Limits

Notion rate-limits at ~3 requests/second per integration with bursts permitted. On `429`, honor the `Retry-After` header. For bulk operations, batch and add 300-500ms sleep between writes.

## Best Practices

**Database design**
- Decide property types up front; changing a property type later can be lossy.
- Prefer `select` and `status` over free-text where values are constrained; this enables filters and Boards.
- Use `relation` for any many-to-many link between artifact types; do not paste page URLs into rich_text.
- Use `unique_id` for any artifact you want to reference externally (PRD-042, DEC-017).

**Views over duplication**
- Never copy a database row to display it elsewhere; embed a Linked Database View instead.
- Each page should have at most one source-of-truth database; everything else is a view.

**Page architecture**
- Teamspace home page = a curated dashboard of linked views; not a content dumping ground.
- Use synced blocks for content reused across many pages (e.g. Definition of Done).
- Cap page nesting at 3 levels for navigability.

**Governance**
- Every active page in a database must have an Owner and a `Last Reviewed` date.
- Quarterly review: archive Shipped/Killed PRDs older than 12 months.
- Permissions at the Teamspace level whenever possible; avoid per-page overrides.

**API hygiene**
- Cache database IDs, property IDs, and user IDs.
- Always set `Notion-Version` header explicitly to avoid silent breaks.
- Use webhooks (via Notion's official webhooks where available, or Zapier/Make as fallback) instead of polling.

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---|---|---|
| API returns 404 for a database the integration "should" see | Integration has not been explicitly shared on the database (or its parent page) | Open the database in Notion, click "..." → "Add connections" → select the integration |
| Rollup property shows nothing | The relation property is empty, or the rolled-up property is filtered out | Confirm the relation has linked rows; check the rollup's source property; rebuild the rollup if added recently |
| Status property cannot be set via API | The status name does not exactly match an existing option (case-sensitive) | Read the database schema first; use the exact option name; status options cannot be created via the API in some plan tiers |
| Linked database view loses its filter after edit | The view was edited in a destination page rather than at the source | Edit views at the database's source location; saved views from the source propagate everywhere |
| Page becomes very slow to load | Too many embedded videos, too many rollup calculations, or a deeply nested toggle structure | Move heavy content to a child page; replace rollups with formula caches where possible; flatten toggles |
| Workspace search returns irrelevant results | Pages share generic titles ("Notes"), or are missing tags | Use descriptive titles with a prefix (PRD:, DEC:, OKR:); add multi_select tags |
| Bulk import of Markdown loses callouts and toggles | Notion's Markdown import does not preserve all custom block types | Use the API to create blocks programmatically (block-by-block) for high-fidelity migration |

## Success Criteria

- Every PM artifact (PRD, OKR, Decision, Roadmap item) lives in a database, not as an ad-hoc page
- 90%+ of database rows have an Owner and a Last Reviewed date within the past 6 months
- The Teamspace home page is the single launching point for the team's daily work
- New team members can find an active PRD in under 3 clicks from the home page
- API integrations (Linear sync, Jira sync, GitHub webhooks) run nightly with zero manual reconciliation
- No more than 5% of database rows reference deleted or archived counterparts (relation hygiene)
- Quarterly OKR check-ins are recorded in the OKR database with updated Confidence and Progress
- Decision log captures 100% of architecture-level decisions across the team

## Scope & Limitations

**In Scope:** Notion workspace and Teamspace setup, database design for PRDs/OKRs/Roadmap/Decisions/Reviews/1:1s, view design, property and relation modeling, page architecture, Notion REST API authoring, sync pattern design with Jira/Linear/GitHub, governance and review cadences.

**Out of Scope:** Notion administration (SCIM, SAML, billing) at the workspace level beyond Teamspace setup. Jira space and project configuration (hand off to `jira-expert/` and `confluence-expert/`). Linear configuration (hand off to `linear-expert/`). Strategic OKR setting (hand off to `execution/brainstorm-okrs/`). Story splitting and backlog refinement (hand off to `execution/backlog-refinement/`, `execution/story-splitting/`).

**Limitations:** Notion's API rate limits (~3 req/s) make it unsuitable for very high-throughput sync; batch and queue. Status properties cannot have options created via the API in lower plan tiers; pre-create options manually. Rollups cannot reference rollups in older API versions; chain via formulas where needed. Page-level permissions can be overridden in unexpected ways by Teamspace-level changes. Notion is not a real-time collaboration substitute for chat; do not try to replace Slack with comments.

## Integration Points

| Integration | Direction | What Flows |
|---|---|---|
| `jira-expert/` | Notion ↔ Jira | PRD-to-Epic creation; Jira issue embeds in PRD pages |
| `confluence-expert/` | Migration | When moving from Confluence to Notion, structure and content mapping |
| `linear-expert/` | Notion ↔ Linear | PRD-to-Project creation; Linear progress rollups into Notion |
| `execution/create-prd/` | PRD → Notion | PRD scaffolder output rendered as Notion blocks via `--format notion` |
| `execution/brainstorm-okrs/` | OKR → Notion | OKR validator output written to the OKR DB |
| `execution/outcome-roadmap/` | Roadmap → Notion | Roadmap rows materialized in the Roadmap DB |
| `execution/daci-framework/` | Decision → Notion | DACI decisions logged in the Decisions DB |
| `execution/status-update-generator/` | Notion → Status | Weekly status pulls aggregates from PRDs/OKRs DBs |
| `execution/release-notes/` | Notion → Release | Shipped PRDs feed release notes input |
| `senior-pm/` | Notion → Portfolio | OKR and Roadmap DBs feed portfolio reports |
| `discovery/interview-synthesis/` | Research → Notion | Customer research database populated from interview synth output |

## References

- `references/notion-api-patterns.md` — full REST API call catalog with request/response examples
- `references/notion-database-design-for-pm.md` — canonical schemas for PRDs, OKRs, Roadmap, Decisions, Reviews
- `assets/notion-prd-template.md` — PRD page template using Notion-native blocks
- `assets/notion-roadmap-template.md` — Roadmap database schema and view definitions
- `assets/notion-okr-template.md` — OKR database schema with Wodtke confidence model
- Notion API docs: https://developers.notion.com/
- Notion API reference: https://developers.notion.com/reference/intro
- Notion changelog: https://developers.notion.com/page/changelog
