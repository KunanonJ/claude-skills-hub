---
name: linear-expert
description: >
  Linear expert for team and workspace administration, Cycles, Projects,
  Initiatives, Roadmaps, GraphQL API queries, automations, triage workflows,
  GitHub integration, bulk operations, and Jira-to-Linear migration. Use for
  Linear configuration, workflow design, GraphQL authoring, and modern
  PM-friendly issue tracking at scale.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-integration
  updated: 2026-05-21
  tech-stack: [linear, graphql, github, slack]
  tags: [linear, graphql, cycles, initiatives, roadmaps, triage, migration]
---
# Linear Expert

Master-level expertise in Linear configuration, workflow design, GraphQL API mastery, Cycle and Project management, Initiative-level roadmaps, triage automation, GitHub integration, and migration from Jira. Covers everything from workspace setup to programmatic bulk operations against the Linear API.

## Overview

Linear is an opinionated, keyboard-driven issue tracker built around a strict data model (Team → Project → Issue → Sub-issue) and a GraphQL-only public API. Unlike Jira, Linear's strength is its lack of configurability: there is one workflow shape (Backlog → Unstarted → Started → Completed → Canceled), one priority scale (0-4), and a tight set of first-class concepts (Cycles, Projects, Initiatives, Labels, Milestones). The job of a Linear expert is to operate fluently inside those rails while extending the system through the API, automations, and integrations.

### When to Use

- Setting up a new Linear workspace, team, or project from scratch
- Designing Cycle cadence, triage rules, and SLA workflows
- Writing GraphQL queries and mutations against the Linear API
- Configuring GitHub PR auto-link/auto-close and Slack notifications
- Building Initiative / Project / Milestone hierarchies for executive roadmaps
- Running bulk operations (relabel, retarget, reassign) across hundreds of issues
- Migrating an existing Jira instance to Linear without losing history
- Diagnosing why automations, sub-issues, or triage rules are not firing as expected

## Concepts

### Data Model

| Entity | Purpose | Key Fields |
|---|---|---|
| **Workspace** (Organization) | Top-level account, billing scope | `urlKey`, `name`, `samlEnabled` |
| **Team** | Permissions boundary, workflow owner, issue identifier prefix (e.g. `ENG`, `DESIGN`) | `key`, `cyclesEnabled`, `triageEnabled`, `defaultIssueState` |
| **Cycle** | Time-boxed iteration owned by one team (Linear's "sprint") | `number`, `startsAt`, `endsAt`, `progress`, `scopeHistory` |
| **Project** | Cross-functional body of work with a target date; spans one or more teams | `state` (planned/started/paused/completed/canceled), `targetDate`, `lead`, `teamIds` |
| **Initiative** | Strategic theme that groups Projects under a top-line outcome | `status`, `targetDate`, `owner`, `projects` |
| **Roadmap** | Saved view of Projects/Initiatives ordered by time | (UI construct, queried as filtered Project list) |
| **Issue** | The atomic unit of work | `identifier` (e.g. `ENG-123`), `state`, `priority`, `estimate`, `cycle`, `project`, `parent` |
| **Sub-issue** | Issue with `parent` set, rolls progress up | inherits team from parent |
| **Label** | Free-form tag; can be grouped into mutually-exclusive label groups | `color`, `parent` (for groups) |
| **Milestone** | Project-scoped checkpoint with a target date | `name`, `targetDate`, `sortOrder` |
| **Workflow State** | Per-team status; lives in one of 5 types | `type` (backlog/unstarted/started/completed/canceled/triage) |
| **Triage** | Special inbox state for unassigned/unscored incoming issues | enabled per-team via `triageEnabled` |

### Issue Identifier & Linear-Flavored Markdown

- Issues are referenced as `TEAMKEY-NUMBER` (e.g. `ENG-123`, `DSGN-47`). The number is workspace-unique within the team. Pasting an identifier in any Linear text field auto-resolves to a link with the issue title.
- **Mentions**: `@username` resolves against workspace members. `@team-name` mentions an entire team.
- **Priorities** map to numeric values: `0` No priority, `1` Urgent, `2` High, `3` Medium, `4` Low. Most UIs and the API accept the numeric value.
- **Markdown extensions**: standard CommonMark plus issue refs, mentions, task lists (`- [ ]`), and inline emoji shortcodes (`:rocket:`).
- **Code blocks** support fenced language tags; Linear renders syntax highlighting for ~30 languages.

## Core Workflows

### 1. Workspace and Team Setup

1. Create workspace; set URL key (immutable, used in all issue URLs).
2. Configure SSO/SAML if available on the plan tier.
3. Create the first Team with a meaningful 2-4 letter key (it appears in every issue ID forever).
4. Decide per-team:
   - **Cycles enabled?** Yes for shipping teams, no for triage-only/support teams.
   - **Cycle cadence**: typically 1-2 weeks, set the day-of-week start.
   - **Triage enabled?** Yes if external sources (Slack, support, GitHub Issues) create issues that need human routing.
   - **Estimation scale**: Exponential (0, 1, 2, 4, 8), Fibonacci, Linear (1-5), or T-shirt.
5. Customize workflow states (within the 5 allowed types). Common pattern: `Backlog → Todo → In Progress → In Review → Done → Canceled`.
6. Define core labels and label groups (e.g. group `area/*` with values `area/api`, `area/web`, `area/infra`).
7. **HANDOFF TO**: team leads for issue templates, automations, and GitHub install.

### 2. Cycle and Project Planning

**Cycle planning checklist** (run 1-2 days before cycle start):
1. Review the Cycle view: any issues without estimates, owners, or projects?
2. Pull issues from Backlog into Todo for the upcoming cycle.
3. Confirm cycle scope against the team's recent velocity (Linear shows median cycle velocity in Insights).
4. Set the cycle's auto-archive cadence (default: 6 completed cycles).

**Project planning**:
1. Create Project; assign Lead, target date, and member teams.
2. Add Milestones inside the project; order them.
3. Pull or create issues, assigning each to a milestone where useful.
4. Set Project status updates cadence (weekly is the default expectation).

### 3. Initiative and Roadmap Management

Initiatives are the top of Linear's hierarchy (Initiative → Project → Milestone → Issue).
1. Create an Initiative per strategic theme (e.g. "Self-Serve Onboarding Q3").
2. Attach 3-7 Projects per Initiative; more than 10 signals the Initiative is too broad.
3. Use the Roadmap view to visualize Initiatives and Projects on a quarterly timeline.
4. Owner posts an Initiative update at minimum monthly; the update appears in the Initiative feed and in any subscribed Slack channel.

### 4. Triage Workflow

Triage is Linear's inbox for issues that arrive without a workflow state. It's the right destination for Slack-created issues, customer support escalations, and inbound GitHub Issues.
1. Enable Triage on the receiving team.
2. Configure intake sources: GitHub Issues mirroring, Slack-to-Linear, customer request form, or API.
3. Establish a daily triage cadence (one person, ~15 minutes). For each triage item:
   - Confirm or reassign team.
   - Assign priority (Urgent/High/Medium/Low).
   - Assign owner or leave in `Todo` for cycle planning.
   - Attach project/milestone if it belongs to existing work.
   - Apply labels (`area/*`, `type/bug|feature|chore`).
4. **HANDOFF TO**: cycle planning for any items not closed during triage.

### 5. GitHub Integration

Linear's GitHub integration is bidirectional and the highest-leverage automation in the product.
1. Install the Linear GitHub app on the org; grant access to the relevant repos.
2. **Magic words in PR titles or descriptions** auto-link and auto-close:
   - `Fixes ENG-123`, `Closes ENG-123`, `Resolves ENG-123` move the issue to Done on PR merge.
   - `Part of ENG-123` or just `ENG-123` link without auto-close.
3. **Branch name auto-linking**: branches matching `<username>/eng-123-short-description` are auto-detected.
4. PR status changes update the issue state (Linear → In Review when PR opens; → Done when merged).
5. Configure per-team "GitHub repos" so only the relevant repos appear in the issue sidebar.

### 6. Bulk Operations

Bulk edits go through the API for anything beyond ~50 issues. Strategy:
1. Build a GraphQL query to fetch the issue IDs matching the criteria.
2. Loop in batches of 50; call `issueUpdate` mutation for each.
3. Rate limit: stay under 1,500 requests / hour per API key on free tier, 5,000 on paid.
4. Always include an `--dry-run` mode in scripts; print the full list of issues that will change before mutating.
5. Use `issueBatchUpdate` mutation (where available) to update up to 100 issues per call.

### 7. Migration from Jira

Linear ships a first-party Jira importer that covers ~80% of cases. For the remaining 20%, plan a custom GraphQL-backed migration.
1. **Inventory Jira**: project count, custom fields, workflows, user count, issue count, attachment volume.
2. **Map concepts**:
   - Jira Project → Linear Team (often) or Linear Project (sometimes)
   - Jira Epic → Linear Project
   - Jira Initiative → Linear Initiative
   - Jira Sprint → Linear Cycle
   - Jira Subtask → Linear Sub-issue
   - Jira Components → Linear Labels (often in an `area/*` group)
3. **Decide on history**: Linear's importer preserves comments, attachments, status history, and assignees, but not custom field values verbatim (they map to labels or description text).
4. **Pilot with one Jira project** before mass migration. Validate identifiers, link integrity, and attachment downloads.
5. **Cut over**: freeze Jira writes, run final import, redirect all integrations (Slack, GitHub, CI) to Linear, archive Jira.
6. **HANDOFF TO**: `jira-expert/` for the Jira freeze and decommission plan.

## API / Query Patterns

Linear's API is GraphQL-only, served at `https://api.linear.app/graphql`. Auth is via personal API key (`Authorization: <key>`) or OAuth2. See `references/linear-graphql-patterns.md` for a complete query catalog.

**List issues for a team in the active cycle**:
```graphql
query ActiveCycleIssues($teamKey: String!) {
  team(id: $teamKey) {
    activeCycle {
      issues(first: 100) {
        nodes {
          identifier
          title
          state { name type }
          assignee { name }
          priority
          estimate
        }
      }
    }
  }
}
```

**Create an issue**:
```graphql
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { id identifier url }
  }
}
```
Variables:
```json
{
  "input": {
    "teamId": "team-uuid-here",
    "title": "Support TOTP for SSO logins",
    "description": "Customers on Enterprise plan want TOTP as a second factor.",
    "priority": 2,
    "labelIds": ["label-uuid-area-auth"],
    "projectId": "project-uuid-self-serve-q3"
  }
}
```

**Transition an issue to a new state**:
```graphql
mutation MoveIssue($id: String!, $stateId: String!) {
  issueUpdate(id: $id, input: { stateId: $stateId }) {
    success
    issue { identifier state { name } }
  }
}
```

**Find all open Urgent issues across the workspace**:
```graphql
query UrgentOpen {
  issues(
    filter: {
      priority: { eq: 1 }
      state: { type: { in: [backlog, unstarted, started] } }
    }
    first: 50
  ) {
    nodes { identifier title team { key } assignee { name } }
  }
}
```

**Paginate through a large result set**:
```graphql
query AllOpenIssues($after: String) {
  issues(first: 250, after: $after, filter: { state: { type: { neq: completed } } }) {
    pageInfo { hasNextPage endCursor }
    nodes { identifier title }
  }
}
```
Loop until `pageInfo.hasNextPage` is false, passing `endCursor` as the next `after`.

**Bulk update via batch mutation**:
```graphql
mutation BatchLabel($ids: [String!]!, $labelId: String!) {
  issueBatchUpdate(ids: $ids, input: { labelIds: [$labelId] }) {
    success
    issues { identifier }
  }
}
```

**Webhook payload shape** (for `Issue` events):
```json
{
  "action": "create",
  "type": "Issue",
  "data": { "id": "...", "identifier": "ENG-123", "title": "..." },
  "url": "https://linear.app/acme/issue/ENG-123",
  "createdAt": "2026-05-21T12:00:00.000Z",
  "webhookId": "...",
  "webhookTimestamp": 1716292800000
}
```
Always validate the `Linear-Signature` header against your webhook secret.

### CLI Patterns

Linear does not ship a first-party CLI, but several community CLIs exist; alternatively, a thin shell wrapper around `curl` plus GraphQL queries is the most portable pattern.

```bash
# Minimal curl-based query helper
linear_query() {
  curl -s -X POST https://api.linear.app/graphql \
    -H "Authorization: $LINEAR_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"$1\"}"
}
```

## Best Practices

**Data quality**
- Enforce labels via team conventions (e.g. every issue must carry one `area/*` and one `type/*` label).
- Estimate every issue before it enters a cycle. Cycle velocity is meaningless if half the issues have null estimates.
- Use sub-issues for genuine parent-child decomposition; do not use them as a substitute for projects.

**Workflow discipline**
- Resist the urge to add a 7th or 8th workflow state. Linear's strength is the constrained model. If a team feels squeezed, the right move is usually a label, not a new state.
- Use the `Triage` state aggressively for any source that creates issues automatically; do not let bots write directly into `Todo`.

**Cycles and projects**
- Cycle scope set at planning time should drift no more than ~20% during the cycle; bigger drift is a signal of unclear acceptance criteria upstream.
- Projects without a target date are red flags; every project should have one even if approximate.

**API hygiene**
- Cache the team and label UUIDs your scripts use; never look them up by name on every call.
- Use webhooks instead of polling. Linear's webhook system covers nearly every entity.
- Respect rate limits; back off on `429` responses with the `Retry-After` header.

**Governance**
- Restrict who can create teams (admins only on larger workspaces).
- Audit Initiatives quarterly; merge or close stale ones.
- Document the workspace's label taxonomy in a pinned issue or Notion page.

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---|---|---|
| Issue did not auto-close on PR merge | PR description used wrong magic word, repo not connected to the team, or PR was merged via squash without the magic word in the commit message | Verify the GitHub integration is enabled for the team; ensure the magic word (`Fixes`, `Closes`, `Resolves`) appears in PR title or description; if squash-merging, include the magic word in the commit message |
| GraphQL query returns null for a field that should exist | Field is gated behind a permission your API key lacks, or the field is on a different type (e.g. `Issue.project` vs `Issue.projectMilestone`) | Re-check the schema via Linear's GraphQL Playground; ensure the API key belongs to a workspace member with access to the relevant team |
| Triage rules not firing for inbound items | Team does not have triage enabled, or the source integration is configured to write directly to a workflow state | Enable triage in team settings; reconfigure the source (e.g. Slack-to-Linear) to create issues without a state so they land in triage |
| Bulk update script hits 429 errors | Exceeded the per-key rate limit (1,500/hr free, 5,000/hr paid) | Add exponential backoff; use `issueBatchUpdate` instead of per-issue calls; spread work over time or upgrade the plan |
| Cycle issues show the wrong velocity | Issues without estimates are excluded from velocity; canceled work is excluded; scope changes during cycle distort the chart | Require estimates at planning time; review the cycle's scope history in Insights to spot mid-cycle additions |
| Custom field values from Jira are missing after import | Linear has no custom fields; the Jira importer maps them to labels or appends to description, which can lose semantics | Pre-map critical Jira custom fields to label groups before import; for fields that cannot be expressed as labels, append structured key:value lines to the description |
| Webhook deliveries are missing or duplicated | Receiver is too slow (>10s response), or the webhook secret is rotated and signatures fail validation | Respond with 2xx within 5 seconds; queue work asynchronously; verify the signature on every payload using the current secret |

## Success Criteria

- All active teams have triage enabled (where applicable), a defined cycle cadence, and a standard label taxonomy
- 95%+ of issues entering a cycle carry an estimate, an owner, and a state-appropriate label
- Cycle velocity variance stays within 25% of the trailing 6-cycle median
- Every active Project has a Lead, a target date, and a status update within the last 14 days
- Initiatives have a clear owner and a monthly update; no Initiative carries more than 10 Projects
- GitHub PRs auto-close their linked Linear issues in 95%+ of merges
- API/automation scripts respect rate limits; no script triggers more than 5 `429` responses per day
- Jira-to-Linear migrations cut over with zero loss of comment history and 100% of identifiers redirected

## Scope & Limitations

**In Scope:** Linear workspace, team, and project configuration; cycle and project planning; Initiative and Roadmap hierarchy; triage workflow design; GitHub PR integration; GraphQL query and mutation authoring; bulk operations via API; webhook configuration; Jira → Linear migration planning and execution.

**Out of Scope:** Jira-side configuration and migration freeze (hand off to `jira-expert/`); Notion documentation pages for Linear roadmaps (hand off to `notion-pm/`); strategic prioritization and OKR setting (hand off to `senior-pm/`, `execution/brainstorm-okrs/`); sprint coaching and team health (hand off to `scrum-master/`); release notes generation from Linear issues (hand off to `execution/release-notes/`).

**Limitations:** Linear has no custom fields; all extension happens through labels, descriptions, or external systems. The free tier caps at 250 issues per workspace and excludes Initiatives and SAML. API rate limits are workspace-wide and shared across all keys; heavy automation may require coordination. Importers preserve most history but cannot recreate Jira's custom workflow states; mapping is many-to-five. GraphQL schema evolves continuously; pin client code to the deprecation calendar.

## Integration Points

| Integration | Direction | What Flows |
|---|---|---|
| `jira-expert/` | Jira → Linear | Migration mappings, custom-field translation, freeze coordination |
| `notion-pm/` | Linear → Notion | Roadmap embeds, Initiative pages, project status rollups |
| `execution/create-prd/` | PRD → Linear | PRD page becomes the Linear Project description; PRD sections become Milestones |
| `execution/brainstorm-okrs/` | OKR → Linear | Initiatives mapped to Objectives; Projects tagged with KR identifiers |
| `execution/outcome-roadmap/` | Roadmap → Linear | Outcome roadmap rows mapped to Linear Initiatives; outputs become Projects |
| `execution/release-notes/` | Linear → Release Notes | Closed issues in a cycle/project become release note line items |
| `execution/prioritization-frameworks/` | Scoring → Linear | RICE/WSJF scores written back to labels or description fields |
| `scrum-master/` | Linear → Analytics | Cycle data feeds velocity_analyzer.py and sprint_health_scorer.py |
| `senior-pm/` | Linear → Portfolio | Initiative-level rollups feed project_health_dashboard.py |
| `delivery-manager/` | Linear → Release | Project completion state and milestone dates feed release coordination |

## References

- `references/linear-graphql-patterns.md` — canonical query and mutation catalog with variables
- `references/linear-vs-jira.md` — concept-by-concept translation guide for teams migrating from Jira
- `assets/linear-team-template.md` — recommended new-team configuration
- `assets/linear-triage-workflow.md` — daily triage SOP and rotation template
- Linear API docs: https://developers.linear.app/docs
- Linear GraphQL schema explorer: https://studio.apollographql.com/public/Linear-API/
- Linear method (workspace conventions): https://linear.app/method
