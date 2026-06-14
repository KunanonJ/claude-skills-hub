# Triage Worksheet

Manual triage worksheet for teams not running the Python tool, or for the team's weekly review of the tool's output.

## Meta

| Field | Value |
|---|---|
| Triage date | YYYY-MM-DD |
| Triage owner | (PM name) |
| Queue period | YYYY-MM-DD to YYYY-MM-DD |
| Total items in queue | |
| Channel mix | support: __, sales: __, nps: __, in_app: __, exec_ask: __, social: __, partner: __, customer_interview: __ |

## Step 1 — Intake review

Confirm every item in the queue has the required fields:

- [ ] `id`
- [ ] `channel`
- [ ] `customer_id`
- [ ] `segment`
- [ ] `raw_text` (verbatim, not paraphrased)
- [ ] `received_at`
- [ ] `submitter`

Flag any items missing fields and send back to the originating channel for cleanup.

## Step 2 — Dedup and cluster

Group items into clusters by underlying opportunity (not literal request). One cluster row per opportunity.

| Cluster | Opportunity (1-line summary) | Customer IDs in cluster | Distinct customers | Top segments |
|---|---|---|---|---|
| C-001 | | | | |
| C-002 | | | | |
| C-003 | | | | |

## Step 3 — Categorize

For each cluster, assign a category:

| Cluster | Category |
|---|---|
| C-001 | Bug / Feature request / Question / Strategy |
| C-002 | |
| C-003 | |

Reminder:

- **Bug**: existing functionality is broken → route to engineering bug queue
- **Feature request**: new functionality → score and prioritize
- **Question**: customer needs help, not a product change → route to docs/support; flag if recurring
- **Strategy**: implies a strategic direction change → route to leadership

## Step 4 — Kano category

For each feature-request cluster, pick a Kano category. See `assets/kano_quick_reference.md` if unfamiliar.

| Cluster | Kano category | Reason / signal |
|---|---|---|
| C-001 | basic / performance / delight / indifferent / reverse | |
| C-002 | | |
| C-003 | | |

## Step 5 — Score

For each feature-request cluster, compute the priority score.

```
priority = kano_weight × log10(distinct_customers + 1) × max_segment_weight × (1 + strategic_alignment)
```

| Cluster | Kano weight | Volume factor | Max segment weight | Strategic alignment | Priority |
|---|---|---|---|---|---|
| C-001 | | | | | |
| C-002 | | | | | |

Kano weights (default): basic = 4, performance = 2, delight = 3, indifferent = 0, reverse = -3.

Segment weights (default): enterprise = 4, mid_market = 2, smb = 1, prosumer = 1.

Strategic alignment: 0 (no alignment), 1 (somewhat aligned with current strategy), 2 (directly advances a strategic theme).

## Step 6 — Route

For each cluster, pick a destination:

| Cluster | Priority | Destination |
|---|---|---|
| C-001 | | Prioritization / Bug tracker / Docs / Strategy / Archive |
| C-002 | | |

Routing rules:
- Bug → bug tracker
- Question → docs/support
- Strategy → exec channel
- Feature request with priority ≥ 4.0 → prioritization-frameworks
- Feature request with priority < 4.0 → archive

## Step 7 — Draft responses

For each item in the queue, pick a response template (see `assets/response_templates.md`):

| Item ID | Customer | Cluster | Priority | Response template |
|---|---|---|---|---|
| FB-... | cust-... | C-001 | | Will-build / Exploring / Won't-build |

Responses are sent by the originating channel owner (support agent, AE, CSM) — not directly by the PM.

## Step 8 — Notes for monthly retro

Surface anything worth discussing at the monthly triage retro:

- Channel mix anomalies (spike or drop in a channel)?
- Recurring opportunity themes (same cluster reappearing across weeks)?
- Override patterns (Kano heuristic consistently wrong on a specific signal)?
- Roadmap signal (a cluster that has appeared 4+ weeks in a row should be on the roadmap or explicitly declined)?

```
Notes:
- ...
```

## Sign-off

- [ ] All items have an acknowledgment plan (template + owner + date)
- [ ] All clusters have a routing destination
- [ ] All overrides to Kano category are documented
- [ ] Worksheet archived in the team wiki / Notion / Confluence
