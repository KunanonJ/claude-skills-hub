# Notion REST API Patterns

Canonical Notion API calls for PM workflows. Endpoint base: `https://api.notion.com/v1/`. Auth: `Authorization: Bearer secret_...` (internal integration token) or OAuth2. Every request must include `Notion-Version: 2022-06-28` (or the current pinned version your client uses).

All examples use `curl` for clarity; the same JSON bodies apply to any HTTP client.

---

## 1. Authentication & Connection

```bash
export NOTION_TOKEN="secret_..."
export NOTION_VERSION="2022-06-28"

NOTION_HEADERS=(
  -H "Authorization: Bearer $NOTION_TOKEN"
  -H "Notion-Version: $NOTION_VERSION"
  -H "Content-Type: application/json"
)
```

An integration only sees pages and databases that have been **explicitly shared** with it (open the database → "..." → Add connections). 404s are almost always a missing share.

---

## 2. Discovery — IDs You Need First

Notion IDs are 32-char hex (sometimes hyphenated). The API accepts both forms.

**Retrieve a database schema**:
```bash
curl -X GET "https://api.notion.com/v1/databases/<db_id>" "${NOTION_HEADERS[@]}"
```
Use the response to inspect property names, types, and the exact option strings for `select` / `status` / `multi_select` properties. Selectable options are **case-sensitive** when set via the API.

**Search for a database by title**:
```bash
curl -X POST "https://api.notion.com/v1/search" "${NOTION_HEADERS[@]}" \
  -d '{
    "query": "PRDs",
    "filter": { "value": "database", "property": "object" }
  }'
```

**Get a user (for the People property)**:
```bash
curl -X GET "https://api.notion.com/v1/users" "${NOTION_HEADERS[@]}"
```
Cache user IDs; they are stable.

---

## 3. Querying Databases

**Basic query**:
```bash
curl -X POST "https://api.notion.com/v1/databases/<db_id>/query" "${NOTION_HEADERS[@]}" \
  -d '{
    "filter": { "property": "Status", "status": { "equals": "In Review" } },
    "sorts":  [{ "property": "Target Date", "direction": "ascending" }],
    "page_size": 100
  }'
```

**Compound filter (AND)**:
```json
{
  "filter": {
    "and": [
      { "property": "Owner",  "people": { "contains": "<user_id>" } },
      { "property": "Status", "status": { "does_not_equal": "Killed" } },
      { "property": "Target Date", "date": { "next_quarter": {} } }
    ]
  }
}
```

**Compound filter (OR)**:
```json
{
  "filter": {
    "or": [
      { "property": "Status", "status": { "equals": "At Risk" } },
      { "property": "Status", "status": { "equals": "Off Track" } }
    ]
  }
}
```

**Filter by relation**:
```json
{ "filter": { "property": "OKR", "relation": { "contains": "<okr_page_id>" } } }
```

**Pagination**:
```json
{ "page_size": 100, "start_cursor": "<cursor_from_previous_response>" }
```
Loop while `has_more` is true, passing `next_cursor` as the next `start_cursor`.

---

## 4. Creating a Page in a Database

**Minimal PRD page**:
```bash
curl -X POST "https://api.notion.com/v1/pages" "${NOTION_HEADERS[@]}" \
  -d '{
    "parent": { "database_id": "<prd_db_id>" },
    "properties": {
      "Title":   { "title":  [{ "text": { "content": "PRD: Self-Serve Signup" } }] },
      "Status":  { "status": { "name": "Draft" } },
      "Owner":   { "people": [{ "id": "<user_id>" }] },
      "Target Date": { "date": { "start": "2026-09-30" } },
      "Priority":    { "select": { "name": "P1" } }
    },
    "children": [
      { "object": "block", "type": "heading_2",
        "heading_2": { "rich_text": [{ "text": { "content": "Problem" } }] } },
      { "object": "block", "type": "paragraph",
        "paragraph": { "rich_text": [{ "text": { "content": "Today, new users must..." } }] } },
      { "object": "block", "type": "callout",
        "callout": {
          "icon":     { "type": "emoji", "emoji": "ℹ" },
          "rich_text": [{ "text": { "content": "Reviewed by Eng + Design on 2026-05-19." } }]
        }
      }
    ]
  }'
```

**Setting a relation**:
```json
{
  "properties": {
    "OKR": { "relation": [{ "id": "<okr_page_id_1>" }, { "id": "<okr_page_id_2>" }] }
  }
}
```

**Setting multi_select**:
```json
{ "properties": { "Areas": { "multi_select": [{ "name": "API" }, { "name": "Web" }] } } }
```

---

## 5. Updating a Page

**Update properties only** (does not touch the page body):
```bash
curl -X PATCH "https://api.notion.com/v1/pages/<page_id>" "${NOTION_HEADERS[@]}" \
  -d '{
    "properties": {
      "Status":      { "status": { "name": "Approved" } },
      "Approved On": { "date":   { "start": "2026-05-21" } }
    }
  }'
```

**Archive a page** (Notion's "delete"):
```bash
curl -X PATCH "https://api.notion.com/v1/pages/<page_id>" "${NOTION_HEADERS[@]}" \
  -d '{ "archived": true }'
```

**Unarchive**:
```json
{ "archived": false }
```

---

## 6. Working with Blocks (Page Body)

**Append children to a page**:
```bash
curl -X PATCH "https://api.notion.com/v1/blocks/<page_id>/children" "${NOTION_HEADERS[@]}" \
  -d '{
    "children": [
      { "object": "block", "type": "heading_3",
        "heading_3": { "rich_text": [{ "text": { "content": "Open questions" } }] } },
      { "object": "block", "type": "toggle",
        "toggle": {
          "rich_text": [{ "text": { "content": "Should we A/B test the new flow?" } }],
          "children": [
            { "object": "block", "type": "paragraph",
              "paragraph": { "rich_text": [{ "text": { "content": "Pro: data. Con: 2 weeks." } }] } }
          ]
        }
      }
    ]
  }'
```

**Common block types for PM artifacts**:

| Block | JSON `type` value | Use |
|---|---|---|
| Heading | `heading_1`, `heading_2`, `heading_3` | Sections |
| Paragraph | `paragraph` | Body text |
| Bulleted list | `bulleted_list_item` | Lists |
| Numbered list | `numbered_list_item` | Ordered lists |
| To-do | `to_do` (`checked: true/false`) | Action items |
| Callout | `callout` (with `icon`) | Notes, warnings, decisions |
| Toggle | `toggle` (with `children`) | Collapsible details |
| Code | `code` (`language: "javascript"`) | Code snippets |
| Quote | `quote` | Customer voice, pull-quotes |
| Divider | `divider` | Section separator |
| Bookmark | `bookmark` (`url: "..."`) | Rich link preview |
| Embed | `embed` (`url: "..."`) | Figma, Loom, etc. |
| Table | `table` + child `table_row` blocks | Tables |
| Synced block | `synced_block` | Reusable content |

**Read a block** (for fetching the page body):
```bash
curl -X GET "https://api.notion.com/v1/blocks/<block_id>" "${NOTION_HEADERS[@]}"
```

**List a page's children**:
```bash
curl -X GET "https://api.notion.com/v1/blocks/<page_id>/children?page_size=100" "${NOTION_HEADERS[@]}"
```

**Update a block**:
```bash
curl -X PATCH "https://api.notion.com/v1/blocks/<block_id>" "${NOTION_HEADERS[@]}" \
  -d '{ "to_do": { "checked": true } }'
```

**Delete (archive) a block**:
```bash
curl -X DELETE "https://api.notion.com/v1/blocks/<block_id>" "${NOTION_HEADERS[@]}"
```

---

## 7. Creating a Database

Databases can be created as children of an existing page. Use this sparingly; most workspaces should design DBs in the UI and then drive them programmatically.

```bash
curl -X POST "https://api.notion.com/v1/databases" "${NOTION_HEADERS[@]}" \
  -d '{
    "parent": { "type": "page_id", "page_id": "<parent_page_id>" },
    "title":  [{ "type": "text", "text": { "content": "Decisions" } }],
    "properties": {
      "Title":   { "title": {} },
      "Status":  { "select": { "options": [
        { "name": "Proposed",   "color": "yellow" },
        { "name": "Approved",   "color": "green"  },
        { "name": "Superseded", "color": "gray"   }
      ]}},
      "Date":    { "date": {} },
      "Owner":   { "people": {} },
      "ID":      { "unique_id": { "prefix": "DEC" } }
    }
  }'
```

---

## 8. Rich Text Structure

Every text-bearing block uses a `rich_text` array. The minimal form:

```json
{ "text": { "content": "Hello" } }
```

With link:
```json
{ "text": { "content": "Linear", "link": { "url": "https://linear.app/..." } } }
```

With formatting:
```json
{
  "text": { "content": "important" },
  "annotations": {
    "bold": true, "italic": false, "code": false, "strikethrough": false, "underline": false,
    "color": "red"
  }
}
```

Mentions (a person):
```json
{ "mention": { "type": "user", "user": { "id": "<user_id>" } } }
```

Mentions (a page):
```json
{ "mention": { "type": "page", "page": { "id": "<page_id>" } } }
```

Mentions (a date):
```json
{ "mention": { "type": "date", "date": { "start": "2026-05-21" } } }
```

---

## 9. Sync Pattern Recipes

### Notion → Linear (create Project on PRD approval)

1. Webhook source: PRD status changes to Approved (handled by Zapier/Make/custom poller).
2. Read PRD properties via Notion API.
3. Look up Linear team ID and label IDs from cache.
4. Call Linear's `projectCreate` mutation (see `linear-expert/references/linear-graphql-patterns.md`).
5. Store the returned Linear Project URL in the PRD's `Linear Project` property via Notion PATCH.

### Linear → Notion (roll up project progress)

1. Scheduled job (nightly).
2. For each PRD with a non-null `Linear Project` URL: extract project ID; query Linear for project progress.
3. PATCH the PRD's `Linear Progress` number property and `Linear State` select property.

### GitHub → Notion (log ADR as a Decision)

1. GitHub Action on push to `main` matching `docs/adr/*.md`.
2. Parse the ADR front matter (title, status, date, drivers).
3. POST to Notion's pages endpoint with `parent.database_id = <decisions_db_id>`.

---

## 10. Rate Limits and Resilience

- ~3 requests/second per integration, with short bursts permitted.
- On `429`, response includes `Retry-After` header (seconds). Honor it.
- For bulk writes, batch and sleep 300-500ms between calls.
- Wrap mutating calls in idempotency checks where possible (search by title before create).
- Cache database schemas; refresh only when a 400 indicates a property mismatch.

## 11. Quick Reference

| Operation | Method | Endpoint |
|---|---|---|
| Query DB | POST | `/v1/databases/{id}/query` |
| Get DB schema | GET | `/v1/databases/{id}` |
| Create DB | POST | `/v1/databases` |
| Update DB schema | PATCH | `/v1/databases/{id}` |
| Get page | GET | `/v1/pages/{id}` |
| Create page | POST | `/v1/pages` |
| Update page props | PATCH | `/v1/pages/{id}` |
| Get block | GET | `/v1/blocks/{id}` |
| List children | GET | `/v1/blocks/{id}/children` |
| Append children | PATCH | `/v1/blocks/{id}/children` |
| Update block | PATCH | `/v1/blocks/{id}` |
| Delete (archive) block | DELETE | `/v1/blocks/{id}` |
| List users | GET | `/v1/users` |
| Search | POST | `/v1/search` |

Full reference: https://developers.notion.com/reference/intro
