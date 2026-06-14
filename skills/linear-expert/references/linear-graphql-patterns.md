# Linear GraphQL Patterns

Canonical GraphQL queries and mutations for the Linear API. Endpoint: `https://api.linear.app/graphql`. Auth: `Authorization: <personal-api-key>` or OAuth2 bearer token.

All queries below assume an HTTP POST with a JSON body of the shape:
```json
{ "query": "<graphql-string>", "variables": { ... } }
```

---

## 1. Discovery — IDs You Need First

Most mutations require UUIDs (teamId, stateId, labelId, projectId). Cache these locally; do not look them up by name on every call.

**Get team IDs and state IDs**:
```graphql
query Teams {
  teams(first: 50) {
    nodes {
      id
      key
      name
      states { nodes { id name type } }
      labels { nodes { id name parent { name } } }
    }
  }
}
```

**Get current user (whoami)**:
```graphql
query Me {
  viewer { id name email }
}
```

**Get workspace projects and initiatives**:
```graphql
query Portfolio {
  projects(first: 100, filter: { state: { in: ["started", "planned"] } }) {
    nodes { id name state targetDate lead { name } }
  }
  initiatives(first: 50) {
    nodes { id name status targetDate owner { name } projects { nodes { id name } } }
  }
}
```

---

## 2. Reading Issues

**Single issue by identifier**:
```graphql
query IssueByIdentifier($id: String!) {
  issue(id: $id) {
    identifier title description priority estimate
    state { name type }
    assignee { name }
    creator { name }
    project { name }
    cycle { number }
    labels { nodes { name } }
    children { nodes { identifier title state { name } } }
    comments { nodes { user { name } body createdAt } }
  }
}
```
Variables: `{ "id": "ENG-123" }` (Linear's `issue(id:)` accepts both UUID and the public identifier).

**List issues with a complex filter**:
```graphql
query OpenBugsInArea {
  issues(
    first: 100
    filter: {
      labels: { name: { in: ["type/bug", "area/auth"] } }
      state: { type: { in: [backlog, unstarted, started] } }
      priority: { lte: 2 }
    }
    orderBy: updatedAt
  ) {
    nodes { identifier title priority state { name } assignee { name } updatedAt }
  }
}
```

**Active cycle issues for a team**:
```graphql
query ActiveCycle($teamId: String!) {
  team(id: $teamId) {
    activeCycle {
      number startsAt endsAt
      issues(first: 250) {
        nodes { identifier title state { type } estimate assignee { name } }
      }
    }
  }
}
```

**Pagination loop**:
```graphql
query AllOpenIssues($after: String) {
  issues(
    first: 250
    after: $after
    filter: { state: { type: { neq: completed } } }
  ) {
    pageInfo { hasNextPage endCursor }
    nodes { id identifier title }
  }
}
```
Client loop: call repeatedly, passing `endCursor` as the next `after`, until `hasNextPage` is false.

---

## 3. Creating Issues

**Minimal issue create**:
```graphql
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { id identifier url title }
  }
}
```
Variables:
```json
{
  "input": {
    "teamId": "<team-uuid>",
    "title": "Add SAML support",
    "description": "Customers on Enterprise need SAML 2.0.",
    "priority": 2,
    "estimate": 3,
    "labelIds": ["<label-uuid-area-auth>", "<label-uuid-type-feature>"],
    "projectId": "<project-uuid>",
    "assigneeId": "<user-uuid>"
  }
}
```

**Create a sub-issue**:
```graphql
mutation CreateSubIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { identifier parent { identifier } }
  }
}
```
Variables: add `"parentId": "<parent-issue-uuid>"` (the sub-issue inherits the parent's team).

**Create from triage** (issue lands in the Triage inbox; do not set `stateId`):
```graphql
mutation CreateTriageIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { identifier state { type } }
  }
}
```
Variables:
```json
{
  "input": {
    "teamId": "<team-with-triage-enabled>",
    "title": "Customer report: login loop on Safari",
    "description": "Repro: ... Customer: acme.com"
  }
}
```

---

## 4. Updating Issues

**Transition state**:
```graphql
mutation Transition($id: String!, $stateId: String!) {
  issueUpdate(id: $id, input: { stateId: $stateId }) {
    success
    issue { identifier state { name type } }
  }
}
```

**Reassign**:
```graphql
mutation Reassign($id: String!, $assigneeId: String!) {
  issueUpdate(id: $id, input: { assigneeId: $assigneeId }) {
    success
    issue { identifier assignee { name } }
  }
}
```

**Add a label** (Linear replaces the full label set; merge in client first):
```graphql
mutation Relabel($id: String!, $labelIds: [String!]!) {
  issueUpdate(id: $id, input: { labelIds: $labelIds }) {
    success
    issue { identifier labels { nodes { name } } }
  }
}
```

**Move to cycle**:
```graphql
mutation MoveToCycle($id: String!, $cycleId: String!) {
  issueUpdate(id: $id, input: { cycleId: $cycleId }) {
    success
    issue { identifier cycle { number } }
  }
}
```

**Attach to project + milestone**:
```graphql
mutation AttachProject($id: String!, $projectId: String!, $milestoneId: String!) {
  issueUpdate(id: $id, input: { projectId: $projectId, projectMilestoneId: $milestoneId }) {
    success
    issue { identifier project { name } projectMilestone { name } }
  }
}
```

---

## 5. Bulk Operations

**Batch update up to 100 issues per call**:
```graphql
mutation BatchPriority($ids: [String!]!, $priority: Int!) {
  issueBatchUpdate(ids: $ids, input: { priority: $priority }) {
    success
    issues { identifier priority }
  }
}
```

**Pattern for bulk relabel**:
1. Query the target issues, collect their `id` (UUID, not identifier) values.
2. Chunk into batches of 100.
3. Call `issueBatchUpdate` per batch.
4. Sleep 200ms between batches to stay well under rate limits.

---

## 6. Comments and Attachments

**Post a comment**:
```graphql
mutation Comment($input: CommentCreateInput!) {
  commentCreate(input: $input) {
    success
    comment { id body user { name } }
  }
}
```
Variables: `{ "input": { "issueId": "<uuid>", "body": "Repro confirmed on Safari 17." } }`.

**Attach a URL (e.g. GitHub PR, Figma frame, Notion page)**:
```graphql
mutation Attach($input: AttachmentCreateInput!) {
  attachmentCreate(input: $input) {
    success
    attachment { id title url }
  }
}
```
Variables:
```json
{
  "input": {
    "issueId": "<uuid>",
    "title": "PR #482",
    "url": "https://github.com/acme/web/pull/482",
    "iconUrl": "https://github.com/favicon.ico"
  }
}
```

---

## 7. Projects and Initiatives

**Create a project**:
```graphql
mutation CreateProject($input: ProjectCreateInput!) {
  projectCreate(input: $input) {
    success
    project { id name url }
  }
}
```
Variables:
```json
{
  "input": {
    "name": "Self-Serve Onboarding",
    "teamIds": ["<team-uuid>"],
    "leadId": "<user-uuid>",
    "targetDate": "2026-09-30",
    "state": "planned"
  }
}
```

**Post a project status update**:
```graphql
mutation ProjectUpdate($input: ProjectUpdateCreateInput!) {
  projectUpdateCreate(input: $input) {
    success
    projectUpdate { id body health }
  }
}
```
Variables:
```json
{
  "input": {
    "projectId": "<uuid>",
    "body": "Week 3: API spec signed off; web build starting.",
    "health": "onTrack"
  }
}
```

**Create an initiative and link projects**:
```graphql
mutation CreateInitiative($input: InitiativeCreateInput!) {
  initiativeCreate(input: $input) {
    success
    initiative { id name }
  }
}
```
Then attach projects via `initiativeToProjectCreate` for each project.

---

## 8. Webhooks

Webhook bodies arrive as JSON; validate `Linear-Signature` (HMAC-SHA256 of the raw body with your webhook secret).

Common event types:
- `Issue` — `create`, `update`, `remove`
- `Comment` — `create`, `update`, `remove`
- `Project`, `ProjectUpdate`, `Cycle`, `Reaction`, `IssueLabel`

Payload skeleton:
```json
{
  "action": "update",
  "type": "Issue",
  "data": { "id": "...", "identifier": "ENG-123", "title": "...", "state": { "name": "In Progress" } },
  "updatedFrom": { "stateId": "<previous-state-uuid>" },
  "url": "https://linear.app/acme/issue/ENG-123",
  "createdAt": "2026-05-21T12:00:00.000Z",
  "webhookId": "...",
  "webhookTimestamp": 1716292800000
}
```

Best practice: respond 2xx within 5 seconds; queue the work asynchronously.

---

## 9. Rate Limits

- Free plan: ~1,500 requests / hour per API key.
- Paid plans: 5,000 requests / hour per API key.
- Burst limit: ~50 requests / second.
- On `429`, the response includes `Retry-After` (seconds). Honor it with exponential backoff.

For long-running scripts, prefer:
- Batched mutations (`issueBatchUpdate`) over per-issue loops.
- Webhooks over polling.
- Caching of IDs, label names, and state names.

---

## 10. Reference Mutations Cheatsheet

| Operation | Mutation |
|---|---|
| Create issue | `issueCreate(input: IssueCreateInput!)` |
| Update issue | `issueUpdate(id: String!, input: IssueUpdateInput!)` |
| Batch update | `issueBatchUpdate(ids: [String!]!, input: IssueUpdateInput!)` |
| Archive issue | `issueArchive(id: String!)` |
| Delete issue | `issueDelete(id: String!)` |
| Create comment | `commentCreate(input: CommentCreateInput!)` |
| Attach URL | `attachmentCreate(input: AttachmentCreateInput!)` |
| Create project | `projectCreate(input: ProjectCreateInput!)` |
| Project update | `projectUpdateCreate(input: ProjectUpdateCreateInput!)` |
| Create label | `issueLabelCreate(input: IssueLabelCreateInput!)` |
| Create cycle | `cycleCreate(input: CycleCreateInput!)` |
| Create initiative | `initiativeCreate(input: InitiativeCreateInput!)` |

Full schema: https://studio.apollographql.com/public/Linear-API/
