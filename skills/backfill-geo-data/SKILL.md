---
name: backfill-geo-data
description: "Enrich missing geographic data (country, state, city) on contacts and companies using HubSpot workflows, external data providers, or IP-based geolocation."
license: MIT
metadata:
  author: tomgranot
  version: "1.0"
  category: ongoing-maintenance
---

# Backfill Geographic Data

Fill in missing country, state, and city values on contacts and companies. Geographic data enables territory assignment, regional reporting, and compliance (GDPR, state privacy laws).

## Prerequisites

- HubSpot API token in `.env`
- Python with `hubspot-api-client` installed via `uv`
- Standardized geo values already in place (run `/standardize-geo-values` first)

## Enrichment Methods

### Method 1: HubSpot Workflow Enrichment (Simplest)

Use HubSpot's built-in Operations Hub data quality tools or Breeze Intelligence (if available on your plan) to auto-fill geographic fields.

1. Create a workflow triggered by: country is unknown AND email is known
2. Use the "Enrich contact" action (Operations Hub Professional+) or Breeze Intelligence enrichment
3. If enrichment fills country/state, the workflow completes
4. If enrichment fails, branch to flag for manual review

### Method 2: Company Domain Lookup (API-based)

For contacts with a company domain but no geo data, look up the company's geographic information:

```python
from hubspot import HubSpot
from hubspot.crm.contacts import PublicObjectSearchRequest

api_client = HubSpot(access_token=os.getenv("HUBSPOT_API_TOKEN"))

# Find contacts missing country but with company association
search = PublicObjectSearchRequest(
    filter_groups=[{
        "filters": [
            {"propertyName": "country", "operator": "NOT_HAS_PROPERTY"},
            {"propertyName": "associatedcompanyid", "operator": "HAS_PROPERTY"}
        ]
    }],
    properties=["email", "associatedcompanyid"]
)
```

Copy country/state/city from the associated company to the contact (same pattern as `/enrich-company-name`).

### Method 3: External Data Provider

Integrate with a third-party enrichment service (Clearbit, ZoomInfo, Apollo, etc.):
1. Export contacts missing geo data
2. Run through enrichment provider
3. Import enriched data back via CSV or API

## Step-by-Step Instructions

### Stage 1: Before — Assess the Gap

1. Count contacts missing country, state, and city.
2. Segment by source — which lead sources tend to have missing geo data?
3. Choose the enrichment method based on volume and budget.

### Stage 2: Execute — Run Enrichment

1. Apply the chosen method (or combine methods for maximum coverage).
2. Process in batches of 100 to respect rate limits.
3. Validate enriched values against the standardized geo format from `/standardize-geo-values`.

### Stage 3: After — Verify

1. Re-count contacts missing geographic fields. Calculate improvement percentage.
2. Spot-check 20-30 enriched contacts for accuracy.
3. Set up the new-contact hygiene workflow to prevent future gaps.

### Stage 4: Rollback

- If enrichment data is inaccurate, filter contacts updated by the enrichment process (use `hs_lastmodifieddate` range) and clear the geo fields.
- Keep a backup export of the original data before running enrichment.

## Tips

- IP-based geolocation (from form submissions) is already captured by HubSpot in `ip_city`, `ip_state`, `ip_country`. Copy these to the standard fields if the standard fields are empty.
- Do not overwrite manually-entered geo data with enrichment data — always check "if empty" before writing.
