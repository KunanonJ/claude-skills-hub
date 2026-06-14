---
name: customer-feedback-triage
description: >
  Inbound customer-feedback triage system. Categorize, deduplicate, score, and
  respond to feature requests from support, sales, NPS, in-app feedback, and
  exec asks. Feeds a clean signal into prioritization-frameworks.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-execution
  updated: 2026-05-22
  python-tools: feedback_triage.py
  tech-stack: [kano-model, jtbd, rice, request-management, marty-cagan]
  tags: [feedback, triage, kano, requests, voice-of-customer, intake]
---
# Customer Feedback Triage

## Overview

Most PMs sit on a chaotic inbound stream — Slack DMs, support tickets, sales call notes, CSAT comments, NPS verbatims, in-app feedback widgets, partner emails, exec one-liners — and have no system for converting that stream into prioritization signal. The default mode is reactive: whoever shouts loudest wins, the loudest channels (sales, executives) dominate, and the actual user job stays invisible.

This skill provides a workflow and a Python tool for handling that stream. Inputs are raw feedback items from many channels. Outputs are deduplicated, categorized, scored, and routed items, plus acknowledgment responses for the customers who sent them.

The frameworks behind it are Marty Cagan's discovery-techniques separation of *request* from *opportunity* from *solution*, Noriaki Kano's model of feature-quality categories, Reforge's customer-development model, and ProductPlan's request-management playbook.

### When to Use

- You have a backlog of customer feedback that is not being processed.
- Sales or Customer Success is constantly forwarding feature requests and expecting a per-request answer.
- An executive is acting as a request channel and the roadmap is drifting accordingly.
- You are setting up a new feedback intake process (post-launch, post-funding, scaling beyond founder-led product).
- You need to respond to a customer who sent a feature request and you have to say "yes", "no", or "exploring" in a defensible way.
- You want a defensible audit trail for "we heard you but said no" decisions.

### When not to use

- For genuine product discovery (do not let feedback triage replace discovery — see `discovery/interview-synthesis/`).
- For prioritizing already-triaged items against each other (that is `prioritization-frameworks/`).
- For bug triage (use the bug triage process in your tracker — though the workflow here applies to feature-request items).

## Frameworks

### Marty Cagan: Request → Opportunity → Solution

Cagan separates three things customers and the inbound stream conflate:

| Layer | What it is | Example |
|---|---|---|
| **Request** | What the customer literally asked for | "Add an export to PDF button" |
| **Opportunity** | The underlying job or problem | "I need to share results with my CFO who doesn't have a login" |
| **Solution** | The chosen response | "Shareable read-only link" or "PDF export" or "CSV + email digest" |

The triage workflow's job is to convert each Request into an Opportunity and route the Opportunity to the appropriate discovery / prioritization process. The literal Request is rarely the right thing to build.

### Kano Model (Noriaki Kano, 1984)

Kano classifies features by how their presence or absence affects customer satisfaction. The five categories:

| Category | Effect of having it | Effect of missing it | Example (SaaS analytics tool) |
|---|---|---|---|
| **Basic / Must-be** | Expected; satisfaction does not increase | Severe dissatisfaction | Login works; data export exists |
| **Performance / One-dimensional** | More is linearly better | Less is linearly worse | Query speed; dashboard load time |
| **Delight / Attractive** | Disproportionate satisfaction | Customer does not miss it | Natural-language query; collaborative cursors |
| **Indifferent** | No effect | No effect | Theme color picker (for most users) |
| **Reverse** | Causes dissatisfaction | Improves satisfaction | An overly chatty AI assistant |

Kano categories shift over time: today's delighter becomes tomorrow's basic. The categorization in this triage workflow is the team's current snapshot.

### Reforge: Layered customer development

Reforge frames customer development as concentric rings: stated needs → revealed jobs → underlying motivations. The triage workflow operates at the first ring (stated needs, captured in the request text). It explicitly routes high-signal items into deeper discovery work to surface the second and third rings.

### ProductPlan: Request management

Three principles, drawn from ProductPlan's request-management practice and adopted here:

1. **Always acknowledge.** Every request, even ones that get a "no", gets a response. Customer silence is the fastest path to lost trust.
2. **Sometimes commit.** Commit only when the item is scored, prioritized, and on the roadmap with a date the team will actually hit.
3. **Rarely promise.** Avoid "we'll definitely build that" in any external channel until the item is funded, scoped, and started.

## Workflow

### Phase 1: Intake & normalization

For every inbound feedback item, capture a normalized record with these fields:

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Internal ID |
| `channel` | yes | One of: support, sales, social, nps, in_app, exec_ask, partner, customer_interview |
| `customer_id` | yes | Anonymous OK; needed for dedup and segment analysis |
| `segment` | recommended | e.g. SMB, mid-market, enterprise, prosumer |
| `raw_text` | yes | The verbatim ask — do not paraphrase at intake |
| `received_at` | yes | ISO-8601 |
| `submitter` | yes | The internal person who logged it (Support agent, AE, PM) |
| `opportunity_area` | optional | Coarse area, populated at triage (e.g. onboarding, reporting, integrations) |

Normalization rules:

- Capture the verbatim. Paraphrasing at intake loses signal. The PM can paraphrase at triage.
- One request per record. If a customer email contains 3 asks, create 3 records.
- Do not pre-judge at intake. Even off-topic items get logged and triaged later (they are signal about channel hygiene).

### Phase 2: Triage (run `feedback_triage.py`)

The Python tool ingests the normalized intake JSON and produces:

1. **Deduplicated clusters** — items grouped by similar opportunity, even if the literal requests differ.
2. **Kano category guess** — heuristic based on keyword signals (transparent and documented; the PM should override).
3. **Categorization** — Bug / Feature / Question / Strategy.
4. **Priority score** — combined Kano weight × volume × segment × strategic-alignment.
5. **Suggested response template** — Will-build / Won't-build / Exploring, parameterized by request and customer name.

### Phase 3: Categorization

For each clustered item, categorize:

| Category | Definition | Action |
|---|---|---|
| **Bug** | Existing functionality is broken | Route to engineering bug queue, not PM backlog |
| **Feature request** | New functionality | Continue to scoring |
| **Question** | Customer needs help, not a product change | Route to support / docs; flag if recurring (it's a doc gap) |
| **Strategy** | Item implies a strategic direction (new market, new pricing model) | Route to leadership, not the backlog |

### Phase 4: Scoring

Each Feature request gets three scores:

| Dimension | Range | Source |
|---|---|---|
| **Kano category** | basic / performance / delight / indifferent / reverse | Heuristic + PM override |
| **Volume** | count of customer requests | Tool aggregates after dedup |
| **Segment weight** | enterprise=4, mid-market=2, SMB=1 (configurable) | From customer record |
| **Strategic alignment** | 0-2 | Manual; does it advance current strategic theme? |

The composite priority is:

```
priority = (kano_weight × log10(volume + 1) × max_segment_weight × (1 + strategic_alignment))
```

Where Kano weights default to:
- Basic = 4 (gaps here are existential)
- Performance = 2
- Delight = 3
- Indifferent = 0
- Reverse = -3 (negative — actively avoid building)

This is a coarse score for triage routing, not a final RICE/ICE. Items above a threshold get routed to `prioritization-frameworks/` for proper scoring.

### Phase 5: Response

Every customer who submitted a request gets a response, even for "won't build". Three response templates (in `assets/response_templates.md`):

| Template | When | Tone |
|---|---|---|
| **Will-build** | Item is scored, prioritized, on roadmap with date | Specific, dated, conservative |
| **Exploring** | Item is interesting, not yet scoped | Acknowledge, do not commit, invite follow-up |
| **Won't-build** | Item is out of scope or low-signal | Respectful, explanation, sometimes offer workaround |

The response is sent by the channel originator (support agent, AE, CSM) — not the PM directly — so the customer relationship stays with the existing owner.

### Phase 6: Feed forward

| Output | Destination |
|---|---|
| High-priority Feature requests | `prioritization-frameworks/` for RICE/ICE scoring |
| Recurring opportunity themes | `discovery/identify-assumptions/` to surface implicit assumptions |
| Top customer voices for an opportunity | `discovery/interview-synthesis/` (target list for follow-up interviews) |
| Backlog-ready items | `wwas/` or `job-stories/` for backlog format |
| Bugs | engineering bug tracker |
| Strategic items | exec channel or `c-level-advisor/` |

## Common Traps

### Squeaky-wheel bias

The loudest customer is rarely the average customer. One enterprise account screaming for a feature does not equal demand. The volume score (count of distinct customers requesting) is the antidote; segment weight prevents under-counting enterprise asks, but does not let one enterprise ask dominate alone.

### Sales-driven roadmap

A common pattern: every closed-won deal comes with a list of "promised" features. The roadmap fills with one-off enterprise asks that benefit single customers. Mitigations:

- Sales-channel requests count toward volume only if the customer is willing to be quoted as wanting it (filters tire-kickers).
- A request with a single customer behind it scores low even with high segment weight.
- Track sales-promised features separately from PM-prioritized features; report monthly on the gap.

### HiPPO override

Highest-Paid Person's Opinion. An exec sends a one-liner request and it jumps the queue. The `exec_ask` channel is a real channel — execs do have customer context — but the request should run through the same triage as everything else. Use the response policy: acknowledge, sometimes commit, rarely promise.

### Confusing requests with discovery

A high-volume request for "X" does not mean X is the right solution. It is signal that an opportunity exists in the area of X. Discovery (interviews, prototypes, experiments) determines the actual solution. The triage routes signal into discovery — it does not replace discovery.

### Acknowledgment debt

Failing to respond to inbound requests teaches customers that submitting feedback is futile. The compounding cost is loss of signal volume — fewer customers bother submitting next quarter. Acknowledgment is non-negotiable, even for items the team will not build.

## Tools

| Tool | Purpose | Command |
|---|---|---|
| `feedback_triage.py` | Triage a JSON queue of inbound feedback | `python scripts/feedback_triage.py --input queue.json --format markdown` |
| `feedback_triage.py --demo` | Produce a sample triage queue across all 6 output formats | `python scripts/feedback_triage.py --demo --format markdown` |

The tool ships with `--format json|markdown|mermaid|confluence|notion|linear` per `SHARED_OUTPUT_SCHEMA.md`.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| Same customer appears in multiple clusters with different requests | Customer submitted multiple distinct opportunities; correct behavior | Confirm one record per ask is the intake rule; review whether the asks are genuinely distinct or whether the customer is fishing |
| Kano heuristic mis-categorizes a delighter as performance | The keyword heuristic is intentionally coarse | The Kano column is a starting guess; PM should override during review. Document overrides for future heuristic tuning |
| Volume score dominates over enterprise signal | Single enterprise asks have volume = 1 and lose to consumer-volume asks | Raise the segment weight for enterprise (default 4); if a single enterprise ask is strategically critical, route it via the `strategic_alignment` boost rather than overriding volume |
| Exec asks bypass triage | Cultural pattern; not a tool problem | Route every exec ask through the same intake form; report monthly on exec-channel volume and conversion to roadmap; surface the cost of HiPPO override quantitatively |
| Won't-build responses get hostile customer pushback | Tone too dismissive, or the response failed to explain the rationale | Use the Won't-build template's explanation pattern: acknowledge the underlying job, explain the tradeoff, offer the closest workaround |
| Triage queue grows faster than throughput | Intake is wider than triage capacity; PM is the bottleneck | Cap triage to a weekly batch; auto-acknowledge at intake with a 2-week response SLA; train Support/CSM to pre-categorize obvious bugs |
| Tool exits with input validation error | Required fields (`id`, `channel`, `customer_id`, `raw_text`, `received_at`) missing in JSON input | Confirm input matches the schema in Tool Reference below; run `--demo` to see a valid example |

## Success Criteria

- 100% of inbound feedback items receive an acknowledgment within 14 days
- Feature-request response distribution roughly: 10-20% will-build, 20-30% exploring, 50-70% won't-build (a roadmap is mostly "no")
- Deduplication reduces raw request volume by 30-60% (varies by channel mix and product maturity)
- Sales-promised feature delta from PM-prioritized list is reported monthly to leadership
- HiPPO exec-channel items are processed through triage at the same rate as other channels; exec-channel conversion rate to roadmap is tracked
- At least one customer interview per quarter is sourced from triage clusters (closing the loop from triage to discovery)
- Triage cadence is regular: at minimum monthly, ideally weekly for active products

## Scope & Limitations

**In Scope:** Inbound feedback intake schema, deduplication and clustering, Kano-based categorization, segment-aware volume scoring, response templating, routing to downstream skills (discovery, prioritization, backlog).

**Out of Scope:** Bug triage (use the team's bug tracker process). User research and interview-driven discovery (see `discovery/interview-synthesis/`). Detailed prioritization scoring with RICE/ICE/WSJF (see `prioritization-frameworks/`). Customer-relationship management (CRM is the system of record for the customer, this skill is the system of record for the request). NPS analysis methodology (this skill ingests NPS verbatims as one channel among many).

**Important Caveats:**
- The Kano category guess is a keyword heuristic, transparently documented. It is not ML and does not learn over time. The PM should treat it as a hint, not a verdict, and override liberally.
- The clustering algorithm is a simple word-overlap heuristic, intentional to keep the tool stdlib-only and inspectable. For production volumes (> ~500 items / month), consider augmenting with semantic clustering through a separate offline process.
- The scoring formula is coarse. Its purpose is to route items into downstream prioritization, not to substitute for it. Items above the threshold should still be RICE/ICE scored before going on the roadmap.
- "Acknowledge, sometimes commit, rarely promise" is a discipline, not a tool feature. The templates support the discipline; they do not enforce it. Sales and CS partners need explicit training to avoid promising in customer conversations.

## Integration Points

| Integration | Direction | What flows |
|---|---|---|
| `prioritization-frameworks/` | Feeds into | High-priority triaged Feature requests flow in with volume and Kano context as inputs to RICE/ICE/WSJF |
| `discovery/identify-assumptions/` | Feeds into | Recurring opportunity themes surface implicit product assumptions |
| `discovery/interview-synthesis/` | Feeds into | Top customers per cluster become the target list for follow-up interviews |
| `discovery/brainstorm-experiments/` | Feeds into | High-signal opportunities motivate experiment design |
| `wwas/` | Feeds into | Backlog-ready items move into Why-What-Acceptance format |
| `job-stories/` | Feeds into | Final backlog items use Job Stories format if team prefers JTBD framing |
| `senior-pm/` | Bidirectional | Stakeholder map informs segment weights; triage output informs stakeholder updates |
| `business-growth/customer-success/` | Bidirectional | CS team is the primary intake source via support tickets and CSAT |
| `sales-success/` | Bidirectional | Sales is the intake source for sales-channel asks; receives won't-build rationale |

## Tool Reference

### feedback_triage.py

Ingest a JSON queue of inbound feedback. Produce deduplicated clusters, Kano categorization, priority scores, and suggested response templates.

| Flag | Type | Default | Description |
|---|---|---|---|
| `--input` | string | (required unless `--demo`) | Path to JSON file with feedback items |
| `--demo` | flag | off | Run with built-in 12-item sample queue |
| `--format` | choice | `markdown` | One of `json`, `markdown`, `mermaid`, `confluence`, `notion`, `linear` |
| `--output` | string | stdout | File path to write output |
| `--segment-weights` | string | `enterprise=4,mid_market=2,smb=1,prosumer=1` | Override default segment weights |
| `--threshold` | float | `4.0` | Minimum priority score to route into prioritization-frameworks |

### Input schema

```json
{
  "items": [
    {
      "id": "FB-2026-0001",
      "channel": "support",
      "customer_id": "cust-1234",
      "segment": "enterprise",
      "raw_text": "We really need a way to export results to PDF for our weekly board pack",
      "received_at": "2026-05-12T14:23:00Z",
      "submitter": "support-agent-jane",
      "opportunity_area": "reporting"
    }
  ]
}
```

### Output schemas

**JSON** (`pm/customer-feedback-triage/v1`):

```json
{
  "schema": "pm/customer-feedback-triage/v1",
  "generated_at": "2026-05-22T00:00:00Z",
  "data": {
    "clusters": [
      {
        "cluster_id": "C-001",
        "opportunity_label": "Share results with non-licensed stakeholders",
        "kano_category": "performance",
        "category": "feature_request",
        "request_count": 5,
        "distinct_customers": 4,
        "segment_breakdown": {"enterprise": 2, "mid_market": 2},
        "priority_score": 12.4,
        "above_threshold": true,
        "items": ["FB-2026-0001", "FB-2026-0007", "..."]
      }
    ],
    "routing": {
      "to_prioritization": ["C-001"],
      "to_bug_tracker": ["C-008"],
      "to_strategy": ["C-012"],
      "to_docs": ["C-005"]
    },
    "responses": [
      {
        "item_id": "FB-2026-0001",
        "template": "exploring",
        "body_markdown": "..."
      }
    ]
  }
}
```

**Markdown** (default): a triage-board document with sections per cluster, routing summary, and response drafts.

**Mermaid**: a `flowchart TD` of clusters → routing destinations.

**Confluence / Notion / Linear**: storage-format-appropriate variants of the markdown output.

## References

- `references/customer-feedback-triage-guide.md` — full workflow with examples per channel
- `references/kano-model-deep-dive.md` — categorization heuristics, edge cases, time-dynamics
- `assets/triage_template.md` — manual triage worksheet for teams not running the Python tool
- `assets/response_templates.md` — Will-build / Exploring / Won't-build response templates with three variants each
- `assets/kano_quick_reference.md` — one-page reference card for the five Kano categories
- Marty Cagan, *Inspired: How to Create Tech Products Customers Love* (2nd ed., 2017) — request vs opportunity vs solution
- Marty Cagan, *Empowered* (2020) — discovery vs delivery separation
- Noriaki Kano et al., "Attractive Quality and Must-Be Quality" (1984)
- Patrick Campbell (ProfitWell) on Voice-of-Customer prioritization — https://www.profitwell.com/
- Reforge, "Customer Development" curriculum — https://www.reforge.com/
- ProductPlan, "How to Manage Product Feedback" — https://www.productplan.com/learn/product-feedback/
