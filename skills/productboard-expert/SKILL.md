---
name: productboard-expert
description: >
  Productboard expert for workspace administration, Insight-to-Feature triage,
  Driver scoring, Releases, Roadmap views, REST API patterns, and two-way
  integration with Jira/Linear/Azure DevOps. Use for Productboard setup,
  prioritization workflows, and programmatic operations against the API.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-integration
  updated: 2026-05-22
  tech-stack: [productboard, rest-api, insights, drivers, features, releases]
  tags: [productboard, prioritization, insights, drivers, roadmap, salesforce, intercom, slack]
---
# Productboard Expert

Master-level expertise in Productboard workspace configuration, Insight inbox triage, Driver-based prioritization, Feature hierarchy management, Releases and Roadmap views, REST API operations, and two-way integration with Jira, Linear, Azure DevOps, Salesforce, Intercom, and Slack. Productboard is one of the top dedicated PM tools (alongside Aha! and ProductPlan); PMs adopting it benefit from a structured guide because the data model and prioritization mechanics differ meaningfully from generic issue trackers.

## Overview

Productboard sits between customer-feedback intake (Slack/Intercom/Salesforce/email) and the engineering tracker (Jira/Linear). Its strength is the explicit separation of three layers:

1. **Insights** — the inbound customer evidence (a sales note, a support ticket comment, an interview quote).
2. **Features** — the candidate product changes, organized in a hierarchy of Components and parent/child Features.
3. **Drivers and Releases** — the prioritization framework (Drivers = weighted criteria, Releases = time-boxed delivery groupings).

Insights link to Features (many-to-many); Features score against Drivers; high-scoring Features get added to Releases; Releases push down to Jira/Linear epics and stories. The flow is **inbox → triage → prioritize → ship**, and Productboard is opinionated about each step.

The job of a Productboard expert is to operate fluently inside this model, configure the workspace cleanly, run the Insight inbox without backlog, design Driver weightings that match the company's strategy, and write API automations for the workflows the UI does not cover.

### When to Use

- Setting up a new Productboard workspace or onboarding a new team
- Designing the Component hierarchy and Feature taxonomy
- Configuring Drivers and weighting them against strategic objectives
- Running the Insight inbox triage workflow (the highest-leverage daily ritual)
- Configuring two-way Jira/Linear/Azure DevOps integration
- Building Roadmap views for executives, customers, and internal teams
- Writing API calls to bulk-create Insights, update Features, or read prioritization data
- Integrating with Slack/Intercom/Salesforce/Zendesk for Insight capture
- Migrating from spreadsheet-based prioritization to Productboard
- Troubleshooting "Insights aren't flowing to Features", "scores aren't updating", and similar workflow failures

## Concepts

### Data Model

| Entity | Purpose | Key fields |
|---|---|---|
| **Workspace** | Top-level account; one company has one workspace | `name`, `plan_tier`, `members[]` |
| **Product** (legacy) / **Workspace** | Top-level container in some plans | varies |
| **Component** | Hierarchical grouping for Features (e.g. `Reporting > Dashboards > Filters`) | `id`, `name`, `parent_id` |
| **Feature** | The atomic prioritization unit; can have parent and child Features | `id`, `name`, `description`, `status`, `component_id`, `parent_id`, `tags[]`, `custom_fields` |
| **Insight** (also called "Note") | An inbound customer evidence item; lives in the Insights inbox until linked to Features | `id`, `title`, `content`, `source`, `customer{}`, `tags[]`, `feature_links[]` |
| **Customer** | A profile that can be associated with Insights and Companies | `id`, `email`, `external_id`, `company` |
| **Company** | An account-level grouping of Customers (typically pulled from CRM) | `id`, `name`, `mrr`, `segment` |
| **Driver** | A weighted prioritization criterion (e.g. "Revenue Impact", "Strategic Fit", "Customer Demand") | `id`, `name`, `weight`, `scoring_scale` |
| **Objective** | A strategic theme; Features can be linked to Objectives | `id`, `name`, `time_horizon` |
| **Release** | A time-boxed grouping of Features for delivery planning | `id`, `name`, `start_date`, `end_date`, `feature_ids[]` |
| **Release Group** | A category of Releases (e.g. "Q3 2026") | `id`, `name`, `release_ids[]` |
| **Roadmap view** | A saved configuration of Features filtered and grouped for presentation | UI construct |
| **Custom field** | User-defined Feature attribute (single select, multi-select, number, text, date) | `id`, `name`, `type`, `options[]` |

### Insights vs Features vs Drivers — the three layers

The mental model that makes Productboard click:

```
INSIGHTS (evidence)          FEATURES (candidates)         DRIVERS (criteria)
─────────────────            ──────────────────            ──────────────────
Slack message    ──┐
Salesforce note  ──┼──link──> Feature: "Shareable read-only link"  ──score──>  Revenue impact: 8/10
Intercom thread  ──┤                                                            Strategic fit:   7/10
NPS verbatim     ──┘                                                            Cust demand:     9/10
                                                                                ─────────
                                                                                composite: 8.1
```

Insights are evidence; Features are decisions; Drivers are the scoring system. The Insight-to-Feature link is the system's most important relationship: it lets the team answer "how many real customers asked for this and who are they?" with a click.

### Importance × Evidence

Productboard's Driver scoring is a 2D model: each Feature gets a score (Importance) per Driver, and each Driver has a weight. The composite Feature score is the weighted average.

Evidence (linked Insights) is the supporting data; it does not directly compute the score but is visible alongside the score for context. A high score without supporting Insights is a flag — the team is prioritizing based on opinion rather than evidence.

## Core Workflows

### 1. Workspace and Hierarchy Setup

1. Create the workspace. Set timezone, locale, currency.
2. Invite members; assign roles (Admin, Maker, Contributor, Viewer). Roles in Productboard are global; team-level restrictions come via Features access controls (paid tiers).
3. Define the **Component hierarchy** before adding Features. Common patterns:
   - By product area: `Reporting`, `Onboarding`, `Integrations`, `Billing`, `Platform`
   - By customer journey: `Acquisition`, `Activation`, `Retention`, `Expansion`
   - By team ownership: maps Component to engineering team — useful if engineering teams are stable, fragile if reorgs are frequent.
4. Decide on **Feature naming convention**. Avoid embedding solutions in names. Prefer "Shareable read-only dashboard view" to "PDF export button".
5. Create **Tags** for orthogonal attributes (e.g. `customer-segment/enterprise`, `effort/L`, `theme/AI`).
6. Create **Custom fields** for anything that doesn't fit Tags. Common custom fields: T-shirt size, Engineering owner, Design owner, External ticket ID.
7. **HANDOFF TO**: team leads to start populating Features and linking Insights.

### 2. Insight Inbox Triage (daily ritual)

Productboard's Insight inbox is the central inbound surface. Untriaged Insights pile up quickly if there's no daily ritual.

**Daily inbox triage** (one PM, ~15 minutes):

1. Filter the inbox to "Not yet processed" Insights.
2. For each Insight:
   - **Read the verbatim**. Resist paraphrasing.
   - **Link to one or more Features**. If a matching Feature doesn't exist, create one.
   - **Tag with relevant attributes** (customer segment, theme, source).
   - **Mark "processed"**.
3. If an Insight doesn't map to a Feature within 60 seconds, park it in the "Needs discussion" view and come back to it in the weekly review.

Anti-pattern: creating one Feature per Insight. This explodes Feature count and dilutes scoring. Multiple Insights should commonly map to the same Feature.

See `assets/productboard-insight-triage-workflow.md` for a full SOP.

### 3. Driver Configuration

Drivers are how the team's strategy becomes scoring weight. Configuration steps:

1. Decide on 3-5 Drivers. More than 5 Drivers becomes noise; fewer than 3 gives insufficient resolution.
2. Common Driver sets:
   - **General SaaS**: Revenue Impact, Strategic Fit, Customer Demand, Effort, Risk
   - **Enterprise-led**: Top Account Demand, Renewal Risk, New Logo Acquisition, Strategic Fit, Effort
   - **Growth-led**: Activation Lift, Retention Lift, ARPU Lift, Effort, Risk
3. Assign weights. Weights should sum to 100% (Productboard normalizes if they don't). Higher-weight Drivers move scores more.
4. Define the scoring scale per Driver (typically 0-10). Document what each level means — a "9" on Customer Demand should have a concrete definition (e.g. "≥ 20 customer requests in the last 90 days").
5. Review Driver weights quarterly. If strategy shifts (growth-focused → enterprise-focused), the weights need to shift correspondingly.

See `assets/productboard-driver-template.md` for a Driver definition template.

### 4. Feature Scoring

For each Feature in the candidate pool:

1. Score against each Driver on the defined scale (0-10).
2. Productboard computes the composite weighted score.
3. The Features table can be sorted by score; the top N candidates feed Roadmap planning.

**Discipline**: do not score every Feature in the workspace. Score only Features that are realistic candidates for the next 1-2 release horizons. Scoring 500 Features is a productivity trap.

### 5. Release and Roadmap Planning

1. Define **Releases** as time-boxed delivery containers (e.g. "Q3 2026", "September 2026 Launch").
2. Drag high-scoring Features into the appropriate Release. Productboard's "Plan" view supports this.
3. Set Feature status as Features move through their lifecycle: Idea → Discovery → Planned → In Progress → Done.
4. Create **Roadmap views** filtered for audiences:
   - Executive Roadmap: Releases grouped by Quarter, top Features per Release, status badges
   - Customer-Facing Roadmap (uses Productboard Portal): Features in "Planned" or later, with descriptions sanitized for external sharing
   - Internal Engineering Roadmap: full detail, integration with Jira/Linear status
5. **HANDOFF TO**: Eng for execution via Jira/Linear integration.

### 6. Two-Way Integration with Jira / Linear / Azure DevOps

Productboard's Jira/Linear/ADO integration is bidirectional:

- **Productboard → Jira/Linear**: When a Feature reaches "Planned", push it as an Epic to Jira/Linear. Sync description, owner, target Release date.
- **Jira/Linear → Productboard**: Status updates on the Epic flow back to Productboard. A merged PR closing the Epic marks the Feature as Done.
- **Child issues** (Stories, Tasks, Subtasks) live in Jira/Linear, not Productboard. Productboard tracks the Feature; the engineering tracker tracks the implementation breakdown.

Setup steps:

1. Install the integration in Productboard settings.
2. Map Productboard statuses to engineering-tracker statuses.
3. Map Productboard Releases to Jira Versions or Linear Cycles/Projects.
4. Decide on the push trigger (auto on status change, or manual).
5. Decide on field-mapping (custom fields, owners, dates).

### 7. Customer & Company Sync (Salesforce / HubSpot)

Productboard's value scales with customer-data fidelity. Sync from your CRM:

1. Install the Salesforce / HubSpot integration.
2. Sync Companies (with MRR/ARR, segment, renewal date) and Customers (with email, role, account).
3. Use Company segment and MRR to enrich Insight context. When a feature is requested by "Acme Corp (Enterprise, $480k ARR)", the Insight inherits that context.
4. Use Company MRR as a Driver input for "Customer Demand" or as a separate "Revenue at Risk" Driver.

### 8. Inbound Insight Capture

Productboard captures Insights from multiple channels:

| Channel | Method |
|---|---|
| Email | Forward to `pbinbox-{workspace}@productboard.com` |
| Slack | Productboard Slack app — react with a Productboard emoji to convert a message to an Insight |
| Intercom | Native integration — convert Intercom conversations to Insights |
| Salesforce | Native integration — push Salesforce opportunity notes as Insights |
| Zendesk | Native integration |
| Productboard Portal | Customers submit ideas directly (if enabled) |
| Browser extension | Capture from any web page |
| REST API | Programmatic creation — see API patterns below |

Configure intake from at least 2-3 channels at launch. Single-channel capture undercounts demand.

### 9. Bulk Operations via API

Productboard offers a REST API for operations the UI doesn't cover well. Common bulk operations:

- Bulk-create Insights from a CSV / data dump (e.g. importing 2 years of support tickets at onboarding)
- Bulk-update Feature custom fields based on engineering-tracker data
- Reconcile Features with Jira / Linear if integration drift occurs
- Snapshot Feature scores weekly for trend analysis
- Export the prioritization-ranked Feature list for use in another system

API patterns are detailed in `references/productboard-api-patterns.md`.

## API Patterns

Productboard's REST API is at `https://api.productboard.com` (versioned via the `X-Version` header; latest at time of writing is version 1). Authentication is via Bearer token (`Authorization: Bearer <token>`). All API access requires a paid plan tier.

Full reference: https://developer.productboard.com/

### Authentication

```bash
export PB_TOKEN="<personal-access-token>"
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  https://api.productboard.com/features
```

### List Features

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  "https://api.productboard.com/features?pageLimit=100"
```

Response shape:

```json
{
  "data": [
    {
      "id": "feat-abc-123",
      "name": "Shareable read-only dashboard view",
      "description": { "plainText": "...", "html": "..." },
      "status": { "id": "status-1", "name": "Planned" },
      "component": { "id": "comp-1", "name": "Reporting" },
      "parent": { "id": "feat-parent-1", "type": "feature" },
      "owner": { "email": "pm@company.com" },
      "createdAt": "2026-04-01T12:00:00Z",
      "updatedAt": "2026-05-20T15:30:00Z"
    }
  ],
  "pageCursor": "eyJ..."
}
```

Paginate using `pageCursor`.

### Create a Feature

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Shareable read-only dashboard view",
      "description": {
        "plainText": "Customers want to share dashboards with stakeholders who do not have an account, especially CFO/board readers."
      },
      "type": "feature",
      "parent": { "component": { "id": "comp-reporting" } },
      "status": { "id": "status-idea" }
    }
  }' \
  https://api.productboard.com/features
```

### Create an Insight (note)

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Acme Corp wants PDF export for board pack",
    "content": "On QBR call, CFO at Acme Corp asked for a way to share dashboards with their board. PDF export was mentioned as a workaround they would accept.",
    "source": { "origin": "Salesforce", "record_id": "opp-12345" },
    "customer_email": "cfo@acme.com",
    "tags": ["enterprise", "reporting", "quarterly-business-review"]
  }' \
  https://api.productboard.com/notes
```

(The exact endpoint may be `/notes` depending on plan tier — confirm via Productboard's developer documentation.)

### Link an Insight to a Feature

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "feature": { "id": "feat-abc-123" },
      "note": { "id": "note-xyz-789" }
    }
  }' \
  https://api.productboard.com/notes/feature-links
```

### List Releases

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  https://api.productboard.com/releases
```

### Add a Feature to a Release

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "release": { "id": "rel-q3-2026" },
      "feature": { "id": "feat-abc-123" },
      "state": "planned"
    }
  }' \
  https://api.productboard.com/release-assignments
```

### Update a Custom Field on a Feature

```bash
curl -s -X PUT -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "value": "Large"
    }
  }' \
  https://api.productboard.com/hierarchy-entities/custom-fields-values/cfv-tshirt-feat-abc-123
```

### Webhook subscription

Subscribe to events for outbound automation:

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "events": [
        { "eventType": "feature.created" },
        { "eventType": "feature.updated" },
        { "eventType": "note.created" }
      ],
      "notification": {
        "url": "https://your-app.example.com/webhooks/productboard",
        "version": 1
      }
    }
  }' \
  https://api.productboard.com/webhooks
```

Verify webhook signatures with the workspace secret.

### Rate limits

Productboard rate-limits at the workspace level. The published guidance (subject to change) is ~50 requests per minute on lower tiers and higher on Enterprise. The `Retry-After` header is returned on 429; back off accordingly.

### Pagination

Most list endpoints use cursor-based pagination via `pageCursor`. Always paginate; do not assume a single page returns everything.

## Best Practices

### Hierarchy and naming

- Define the Component hierarchy before bulk-creating Features. Reshuffling Components after the fact is painful.
- Feature names describe the customer outcome, not the implementation. Good: "Share a dashboard with non-account users". Bad: "PDF export button".
- Use parent/child Features sparingly. Two levels of Feature hierarchy is the practical maximum.

### Insight discipline

- Every Insight must have a `customer` field populated. Insights without customer attribution lose their value (you can't filter by segment or by company).
- The verbatim of the Insight is the most important field. Resist summarizing at intake.
- Re-link Insights when a Feature is split or merged. Orphan Insights degrade prioritization signal.

### Driver and scoring discipline

- Drivers should map to the company's current strategic themes. Re-weight at least quarterly.
- Score discipline: only score Features that are realistic candidates for the next 1-2 release horizons. Don't score the long tail.
- The composite score is a sorting aid, not a decision. Drivers + Insights together inform the call.

### Releases

- One Release = one time-boxed delivery window (a quarter, a sprint, a launch month). Avoid open-ended Releases ("Future").
- A Release with > 15 Features is probably too large. Split.
- Tie Releases to engineering Cycles/Versions via integration so status flows automatically.

### Roadmap views

- Build dedicated views for each audience (Exec, Customer, Engineering, Sales). Do not show engineering details to customers, or customer-facing names to engineering.
- Public-facing Roadmap (Portal): only Features in "Planned" or later; sanitized descriptions; no internal commitments.
- Refresh exec views before every monthly business review.

### API hygiene

- Cache Workspace-level IDs (Component IDs, Driver IDs, Custom Field IDs, Status IDs). Looking them up by name on every call wastes rate-limit budget.
- Use webhooks for event-driven workflows. Polling is expensive and slow.
- Always include `X-Version: 1` (or current version); APIs evolve and unversioned calls may break.
- Implement idempotency for bulk-create operations (use external IDs to prevent duplicates on retry).

### Governance

- Restrict workspace admin to 2-3 people. Component restructuring and Driver re-weighting are high-stakes operations.
- Audit Features quarterly: archive everything with status "Idea" that hasn't been touched in 6 months and has zero linked Insights.
- Audit Customers/Companies quarterly: sync drift with CRM is the most common Productboard data-quality issue.

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---|---|---|
| Insights from Slack/Intercom not appearing | Source integration not configured for the workspace, or the user submitting lacks permission | Check Productboard Settings → Integrations; confirm the connected accounts; check user permissions in the source app |
| Feature score not updating after linking new Insights | Score is driven by Drivers (manual scoring), not by Insight count; linking does not auto-recompute | Open the Feature, manually update the relevant Driver score (e.g. Customer Demand) to reflect the new evidence |
| Jira/Linear integration shows stale status | Webhook delivery failure, or the integration's user lost access to the project | Check Productboard integration logs; reconnect; verify the integration user is a member of the Jira/Linear project |
| Customer / Company data out of sync with CRM | Salesforce/HubSpot integration is one-way (CRM → Productboard) and runs on a schedule; recent CRM changes won't appear immediately | Trigger manual sync from Settings → Integrations; for real-time needs, use the Productboard API to push customer data on demand |
| API returns 429 (rate limit) | Workspace rate limit exceeded; common during bulk imports | Respect `Retry-After` header; spread bulk operations over time; consider Enterprise plan for higher limits |
| Insights inbox grows faster than triage capacity | Intake is wider than the daily ritual; multiple channels feeding without filtering | Reduce intake channels OR raise the triage cadence (twice daily); add automated rules to pre-tag Insights by source |
| Productboard Portal shows internal feature names externally | Roadmap view filter not applied; or Features marked public without renaming | Audit Portal-visible Features; ensure customer-facing Feature name is sanitized; use a separate Custom Field for internal-only naming |
| Drivers don't match how the team prioritizes | Weights stale from a previous strategy phase | Run the quarterly Driver review; collect input from PM/Eng/Sales/CS; recalibrate weights to current strategy |
| Cannot find a Feature in search | Feature is archived, or in a Component the user lacks access to | Toggle "Include archived" in search; check Component-level permissions; confirm workspace role |
| Insights are linked to too many Features (signal dilution) | PM links generously without judgment | Restrict linking to the 1-3 Features the Insight most directly supports; train the team that an Insight linked to 10 Features is informationally worthless |

## Success Criteria

- Component hierarchy is stable for 2+ quarters without restructuring
- Insight inbox is triaged daily; "Not yet processed" queue depth stays under 50 items
- 90%+ of Insights have a customer/company association
- All Features in the next 2 Release horizons are scored against current Drivers
- Drivers are re-weighted at least quarterly to match current strategy
- Jira/Linear integration delivers status updates within 5 minutes of the source event 95%+ of the time
- Customer-facing Roadmap (Portal) is refreshed monthly; no leaked internal commitments
- API rate-limit 429 responses stay under 1% of total API calls
- Exec Roadmap is reviewed monthly at the business review; presentation requires no Productboard-specific explanation
- New PM onboarding includes a Productboard walkthrough and a triage shadow within first 30 days

## Scope & Limitations

**In Scope:** Productboard workspace and Component hierarchy setup, Insight inbox triage workflow, Driver configuration and Feature scoring, Releases and Roadmap views (internal and customer-facing), Productboard REST API operations (Features, Insights, Releases, custom fields, webhooks), two-way integration setup with Jira/Linear/Azure DevOps, customer-data sync from Salesforce/HubSpot, bulk operations via API, Productboard Portal configuration.

**Out of Scope:** Engineering-side Jira/Linear configuration (see `jira-expert/` and `linear-expert/`). Strategic prioritization framework selection (see `execution/prioritization-frameworks/`). PRD authoring (see `execution/create-prd/`). Customer interview synthesis (see `discovery/interview-synthesis/`). Pricing-tier decisions for Productboard itself (administrative; not in scope for this skill).

**Limitations:** Productboard's API rate limits are workspace-wide; aggressive scripts can starve the UI for human users. The Salesforce/HubSpot integration is one-way (CRM → Productboard) and runs on a schedule, not in real time. Drivers max out at 10 per workspace on most plans; teams with more dimensions need to consolidate. Productboard's Roadmap views are good for time-bound delivery (Releases) but weaker for outcome-based roadmaps (Now/Next/Later); for the latter, augment with `execution/outcome-roadmap/`. Productboard's permission model is workspace-level on most plans; per-Component access controls are an Enterprise feature.

## Integration Points

| Integration | Direction | What flows |
|---|---|---|
| `jira-expert/` | Productboard ↔ Jira | Features push as Epics; status flows back; Sprint plan derived from prioritization |
| `linear-expert/` | Productboard ↔ Linear | Features push as Projects/Issues; Cycle assignment from Release dates |
| `execution/prioritization-frameworks/` | Bidirectional | Productboard Drivers operationalize the RICE/ICE/WSJF score; external scores can be imported as custom fields |
| `execution/create-prd/` | Productboard → PRD | High-priority Features become PRDs; PRD link goes back as Feature custom field |
| `execution/outcome-roadmap/` | Bidirectional | Outcome roadmap themes map to Productboard Objectives; Releases give the delivery side |
| `execution/roadmap-communication/` | Productboard → Comms | Customer-facing Roadmap variants pull from Productboard Portal |
| `execution/customer-feedback-triage/` | Bidirectional | Triaged feedback clusters become Insights pushed into Productboard; Insight inbox is the entry point for the triage workflow if Productboard is the primary intake |
| `execution/release-notes/` | Productboard → Release Notes | Completed Features in a Release become release-note line items |
| `senior-pm/` | Productboard → Portfolio | Productboard Driver scores and Feature distribution feed portfolio health |
| `notion-pm/` | Productboard ↔ Notion | Productboard Roadmap embeds into Notion pages; deep PRDs live in Notion linked from Features |
| `discovery/interview-synthesis/` | Bidirectional | Interview-derived insights become Productboard Notes; high-evidence Features motivate further interviews |
| `business-growth/customer-success/` | CS → Productboard | CS team is a primary Insight source via Salesforce / Intercom integration |

## References

- `references/productboard-api-patterns.md` — REST API call catalog with curl examples and JSON shapes
- `references/productboard-vs-jira-vs-linear.md` — when to use Productboard alongside (or instead of) Jira/Linear; concept translation
- `assets/productboard-feature-template.md` — recommended Feature structure (description, hypothesis, success criteria, dependencies)
- `assets/productboard-insight-triage-workflow.md` — daily Insight triage SOP
- `assets/productboard-driver-template.md` — Driver definition template with worked examples
- Productboard Developer Docs — https://developer.productboard.com/
- Productboard Help Center — https://help.productboard.com/
- Productboard "Excellence in Product Management" — https://www.productboard.com/excellence/
