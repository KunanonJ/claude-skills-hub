# Productboard REST API Patterns

A practical catalog of API calls for common Productboard operations. The Productboard API is REST, JSON, and Bearer-token authenticated. All examples use `curl` and assume:

```bash
export PB_TOKEN="<personal-access-token>"
```

Authoritative reference: https://developer.productboard.com/

## Conventions

- Base URL: `https://api.productboard.com`
- Required headers: `Authorization: Bearer $PB_TOKEN`, `X-Version: 1`, `Content-Type: application/json` for writes
- Pagination: cursor-based, via `pageCursor` query parameter
- Response envelope: most reads return `{ "data": [...], "pageCursor": "..." }`; writes return `{ "data": { ... } }`
- IDs are stable UUIDs

## Authentication

### Personal access token

For scripts and one-off integrations, generate a Personal Access Token from Productboard Settings → Access tokens. Treat as a secret; rotate periodically.

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  https://api.productboard.com/features?pageLimit=1
```

### OAuth2

For multi-user integrations, use the OAuth2 flow. Productboard supports the standard authorization-code grant. See developer docs for the consent URL and token-exchange details.

## Features

### List Features

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  "https://api.productboard.com/features?pageLimit=100"
```

Response:

```json
{
  "data": [
    {
      "id": "feat-1234-5678",
      "type": "feature",
      "name": "Shareable read-only dashboard view",
      "description": {
        "plainText": "Customers want to share dashboards with stakeholders who don't have an account.",
        "html": "<p>Customers want...</p>"
      },
      "status": {
        "id": "status-planned",
        "name": "Planned"
      },
      "parent": {
        "id": "feat-parent-9999",
        "type": "feature"
      },
      "component": {
        "id": "comp-reporting"
      },
      "owner": {
        "email": "pm@company.com"
      },
      "archived": false,
      "createdAt": "2026-04-01T12:00:00Z",
      "updatedAt": "2026-05-20T15:30:00Z",
      "links": {
        "self": "/features/feat-1234-5678",
        "html": "https://app.productboard.com/features/feat-1234-5678"
      }
    }
  ],
  "pageCursor": "eyJpZCI6ImZlYXQtMTIzNCJ9"
}
```

### Get a single Feature

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  https://api.productboard.com/features/feat-1234-5678
```

### Create a Feature

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Shareable read-only dashboard view",
      "description": {
        "plainText": "Customers want to share dashboards with stakeholders who do not have an account. PDF export is a common workaround request; the underlying need is shareable links."
      },
      "type": "feature",
      "parent": { "component": { "id": "comp-reporting" } },
      "status": { "id": "status-idea" },
      "owner": { "email": "pm@company.com" }
    }
  }' \
  https://api.productboard.com/features
```

### Update a Feature

```bash
curl -s -X PATCH -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "status": { "id": "status-planned" }
    }
  }' \
  https://api.productboard.com/features/feat-1234-5678
```

### Archive a Feature

```bash
curl -s -X PATCH -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{ "data": { "archived": true } }' \
  https://api.productboard.com/features/feat-1234-5678
```

## Components

### List Components

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  https://api.productboard.com/components
```

### Create a Component

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Reporting",
      "description": { "plainText": "Dashboards, reports, exports" }
    }
  }' \
  https://api.productboard.com/components
```

## Insights (Notes)

The "Insights" UI surface corresponds to "Notes" in some API versions. Confirm the current endpoint in the developer docs.

### List recent Notes

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  "https://api.productboard.com/notes?pageLimit=100"
```

### Create a Note (Insight)

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Acme Corp wants PDF export for board pack",
    "content": "On QBR call, CFO at Acme Corp asked for a way to share dashboards with their board. PDF export was mentioned as a workaround they would accept.",
    "source": {
      "origin": "Salesforce",
      "record_id": "opp-12345"
    },
    "customer_email": "cfo@acme.com",
    "tags": ["enterprise", "reporting", "qbr"]
  }' \
  https://api.productboard.com/notes
```

### Link a Note to a Feature

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "feature": { "id": "feat-1234-5678" },
      "note": { "id": "note-abcd-efgh" }
    }
  }' \
  https://api.productboard.com/notes/feature-links
```

### Get all Insights linked to a Feature

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  "https://api.productboard.com/notes?features.id=feat-1234-5678&pageLimit=100"
```

## Customers and Companies

### List Companies

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  https://api.productboard.com/companies
```

### Create a Company

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Acme Corp",
      "domain": "acme.com",
      "externalId": "sf-acct-001234",
      "customFields": [
        { "name": "MRR", "value": 40000 },
        { "name": "Segment", "value": "Enterprise" }
      ]
    }
  }' \
  https://api.productboard.com/companies
```

### Create a Customer

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "email": "cfo@acme.com",
      "company": { "id": "comp-acme-001" },
      "externalId": "sf-contact-9876"
    }
  }' \
  https://api.productboard.com/customers
```

## Releases

### List Releases

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  https://api.productboard.com/releases
```

### Create a Release

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Q3 2026 Launch",
      "startDate": "2026-07-01",
      "releaseDate": "2026-09-30",
      "state": "planned"
    }
  }' \
  https://api.productboard.com/releases
```

### Assign a Feature to a Release

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "release": { "id": "rel-q3-2026" },
      "feature": { "id": "feat-1234-5678" },
      "state": "planned"
    }
  }' \
  https://api.productboard.com/release-assignments
```

### List Feature assignments for a Release

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  "https://api.productboard.com/release-assignments?release.id=rel-q3-2026"
```

## Drivers (Objectives and Key Results)

The exact API endpoints for Drivers / Objectives evolve; consult the developer docs for the current version. The high-level pattern:

### List Objectives

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  https://api.productboard.com/objectives
```

### Link a Feature to an Objective

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "feature": { "id": "feat-1234-5678" },
      "objective": { "id": "obj-customer-success-q3" }
    }
  }' \
  https://api.productboard.com/objectives/feature-links
```

## Custom Fields

### List custom-field definitions

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  https://api.productboard.com/hierarchy-entities/custom-fields
```

### Get a custom-field value

```bash
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  "https://api.productboard.com/hierarchy-entities/custom-fields-values?customField.id=cf-tshirt&hierarchyEntity.id=feat-1234-5678"
```

### Set a custom-field value

```bash
curl -s -X PUT -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "customField": { "id": "cf-tshirt" },
      "hierarchyEntity": { "id": "feat-1234-5678" },
      "value": "L"
    }
  }' \
  https://api.productboard.com/hierarchy-entities/custom-fields-values
```

## Webhooks

### Subscribe to events

```bash
curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "events": [
        { "eventType": "feature.created" },
        { "eventType": "feature.updated" },
        { "eventType": "note.created" },
        { "eventType": "release-assignment.created" }
      ],
      "notification": {
        "url": "https://your-app.example.com/webhooks/productboard",
        "version": 1
      }
    }
  }' \
  https://api.productboard.com/webhooks
```

### Sample webhook payload

```json
{
  "data": {
    "eventType": "feature.updated",
    "id": "evt-1234",
    "links": {
      "target": "/features/feat-1234-5678"
    }
  },
  "timestamp": "2026-05-20T15:30:00Z"
}
```

The payload typically references the affected entity by ID and link; fetch the full entity via a follow-up GET. Verify the webhook signature using the workspace's webhook secret.

## Common bulk-operation patterns

### Backfill Insights from a CSV

Bulk-create Notes from an exported CSV (e.g. 2 years of support tickets at onboarding):

```bash
while IFS=, read -r title content source customer; do
  curl -s -X POST -H "Authorization: Bearer $PB_TOKEN" \
    -H "X-Version: 1" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg t "$title" --arg c "$content" --arg s "$source" --arg ce "$customer" '{
      title: $t,
      content: $c,
      source: { origin: $s },
      customer_email: $ce
    }')" \
    https://api.productboard.com/notes
  sleep 1.5    # rate-limit hygiene
done < insights.csv
```

### Snapshot Feature scores weekly

Snapshot the prioritized Feature list every Monday for trend analysis:

```bash
DATE=$(date +%Y-%m-%d)
curl -s -H "Authorization: Bearer $PB_TOKEN" \
  -H "X-Version: 1" \
  "https://api.productboard.com/features?pageLimit=500" \
  | jq '.data[] | {id, name, status: .status.name, updatedAt}' \
  > "snapshots/features-$DATE.jsonl"
```

### Reconcile with Jira

Find Features marked "Done" in Productboard but missing from Jira's released-version list:

```bash
# Pseudocode:
# 1. List Productboard Features with status=Done in the last 30 days
# 2. For each Feature, read the external Jira link from its custom field
# 3. Check the Jira issue status via Jira API
# 4. Flag mismatches
```

The detail is environment-specific; the pattern is to use Productboard as the source of truth for "what should have shipped" and Jira/Linear for "what did ship".

## Rate-limit handling

Productboard returns `429 Too Many Requests` with a `Retry-After` header (in seconds) when the workspace rate limit is exceeded. A robust client:

```bash
api_call() {
  local response
  while true; do
    response=$(curl -s -w "\n%{http_code}" "$@")
    local code=$(tail -n1 <<<"$response")
    local body=$(head -n-1 <<<"$response")
    if [ "$code" = "429" ]; then
      sleep 30
      continue
    fi
    echo "$body"
    return
  done
}
```

For Python clients, use the `tenacity` library or an exponential backoff pattern around the `requests` call.

## Pagination

Always paginate. Skipping pagination yields silently-truncated data.

```bash
cursor=""
while :; do
  response=$(curl -s -H "Authorization: Bearer $PB_TOKEN" \
    -H "X-Version: 1" \
    "https://api.productboard.com/features?pageLimit=100&pageCursor=$cursor")
  echo "$response" | jq -c '.data[]'
  cursor=$(echo "$response" | jq -r '.pageCursor // empty')
  [ -z "$cursor" ] && break
done
```

## Idempotency

Productboard does not provide an idempotency-key header on all endpoints. For bulk-create operations that may retry, deduplicate on your side using an external ID (e.g. Salesforce opportunity ID in the Note's `source.record_id` field) and check existence before creating.

## API versioning

The `X-Version` header is required. Productboard rolls out backward-incompatible changes via version bumps; pin your scripts to the version you tested against and review the changelog before bumping.

## Caveats

- Some endpoints documented in the developer portal are gated behind plan tiers. Confirm your workspace's plan before scripting against them.
- Permission semantics: a Personal Access Token inherits the user's permissions. A token from an Admin can do everything; a token from a Contributor cannot create Features in restricted Components.
- The API does not currently provide a built-in way to compute Driver weighted scores via the API; scores are managed in the UI. To compute composite scores externally, pull per-Driver scores and the Driver weights separately and combine.

## Further reading

- Productboard Developer Docs — https://developer.productboard.com/
- Productboard API changelog — published on developer docs
- Productboard Help Center on integrations — https://help.productboard.com/
