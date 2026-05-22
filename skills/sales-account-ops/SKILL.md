---
name: sales-account-ops
description: Use when designing or running AI-assisted sales operations workflows such as customer call prep, weekly forecast reports, account-book management, territory scoring, prospect prioritization, Salesforce or CRM summaries, BigQuery revenue/spend analysis, scheduled sales tasks, account research dashboards, or human-approved CRM updates.
---

# Sales Account Ops

Use this skill to build sales-account workflows where Codex assembles data, drafts structured outputs, and leaves judgment or writes to a human approval step. It adapts Anthropic's 4,000-account Claude Cowork workflow for Codex-style local automation and connector use.

Source basis: https://claude.com/blog/how-an-anthropic-sales-leader-uses-claude-cowork-to-run-a-4-000-account-book

## Core Principles

- Automate data assembly, reformatting, reconciliation, and first-pass scoring so humans spend time on customer judgment and commentary.
- Put recurring prep on a schedule when possible. A workflow that runs automatically beats a slash command people forget.
- Encode the exact output format the team already uses: briefs, one-page forecast reports, dashboards, CRM notes, or shared links.
- Pilot on a small slice before running across the whole account book.
- Use human-in-the-loop approval before CRM writes, customer-facing messages, account scores, or forecast changes become official.
- Preserve provenance: every number, score, account rationale, and recommendation should point back to source data.

## Workflow

### 1. Identify the Cadence

Classify the request:

- Daily: customer call prep, meeting-room prep, account snapshots, recent activity summaries.
- Weekly: forecast rollup, pipeline movers and decliners, leadership report, manager-level snapshot.
- Quarterly or annual: territory scoring, TAM sizing, prospect-list refresh, account propensity modeling, comp benchmarking.
- Ad hoc: board prep, renewal risk review, pricing/account history, executive briefing.

### 2. Define the Data Contract

List sources and fields before generating output:

- CRM: account, opportunity, stage, owner, next step, close date, forecast commit, activity history.
- Warehouse: token spend, product usage, revenue, seats, activation, retention, expansion.
- Calendar/email/docs: meeting participants, agenda, notes, prior decisions, internal commentary.
- Web research: company news, hiring, AI commitments, industry signals, comparable case studies.

For each source, mark:

- Verified available.
- Assumed available.
- Needs user-provided export or connector.
- Sensitive or write-protected.

### 3. Specify the Output

Use an explicit format before the run:

```text
OUTPUT NAME:
AUDIENCE:
CADENCE:
SOURCES:
SECTIONS:
APPROVAL NEEDED BEFORE:
PUBLISH LOCATION:
```

Common outputs:

- Customer call brief: account summary, current spend/usage, open pipeline, recent notes, likely use cases, suggested questions.
- Weekly forecast: top-line metrics, top deals, movers, decliners, risk notes, first-line-manager rollup, commentary placeholders.
- Territory scoring dashboard: score, dimensions, weights, rationale, use cases, comparable customers, owner view.
- Account research pack: business context, AI maturity, pain hypotheses, buying committee, trigger events, next action.

### 4. Run a Small Test Slice

Before scaling:

- Run one meeting, one manager rollup, or one territory.
- Compare totals against source systems.
- Check if rationales are specific enough for a seller to act on.
- Adjust weights, dimensions, filters, and report layout.
- Confirm that no protected fields or secrets appear in outputs.

### 5. Scale and Schedule

Once the pilot is credible:

- Batch the workflow by territory, owner, segment, or manager.
- Add checkpoints for long-running jobs.
- Save transcripts, prompts, query logs, and output versions for auditability.
- Deliver to the target surface: document, dashboard, spreadsheet, CRM draft, Slack-ready summary, or web report.
- Keep approval explicit before edits to Salesforce, HubSpot, shared forecasts, customer emails, or externally visible documents.

## Account Scoring Pattern

Use dimensions that fit the segment, then test on a sample before running the book:

```text
SEGMENT:
DIMENSIONS:
WEIGHTS:
SCORING SCALE:
REQUIRED EVIDENCE:
RATIONALE FORMAT:
DISQUALIFIERS:
REVIEW OWNER:
```

Example dimensions:

- Agent opportunity.
- Internal transformation potential.
- AI commitment.
- White space against existing spend.
- Industry fit.
- Knowledge-worker density.
- Public hiring or product signals.
- Existing relationship strength.

## Verification

Report:

- Sample size and coverage.
- Source systems used.
- Reconciliation checks against CRM or warehouse totals.
- Any missing, stale, or conflicting data.
- Human approvals completed.
- Items intentionally left as drafts.

## Anti-Patterns

- Writing directly to CRM without a human approval step.
- Scoring thousands of accounts before checking ten examples.
- Producing a beautiful report with unreconciled numbers.
- Hiding source gaps behind confident prose.
- Optimizing for automation while removing seller context and judgment.
