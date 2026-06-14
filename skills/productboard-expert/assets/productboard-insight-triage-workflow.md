# Insight Inbox Triage Workflow (SOP)

Productboard's Insight inbox (sometimes called "Notes" in the API) is where customer feedback arrives from Slack, Intercom, Salesforce, email, and the Productboard Portal. This document is the daily standard operating procedure for keeping the inbox at zero (or near-zero) and converting Insights into prioritization signal.

The single biggest predictor of Productboard ROI is whether the team runs a daily Insight triage. Teams that don't end up with stale inboxes and Features that score on opinion rather than evidence.

## When and how often

- **Daily**: 15 minutes, one PM owns the triage. Run at a fixed time (e.g. 9:30am after standups).
- **Weekly**: 30-minute review of items parked in "Needs discussion" with PM + CS + Sales.
- **Monthly**: 60-minute trend review — top customer themes, channel mix, segment skew.

## Pre-triage

Before triage, the inbox must have:

- Insights flowing from all configured channels (run a weekly check that no channel has gone silent)
- Each Insight with a `customer` association — if a channel is producing Insights without customer attribution, fix the channel config

## The daily ritual (15 minutes)

### Step 1: Filter the inbox

In Productboard's Insights inbox view, filter to:

- **Status**: Not yet processed
- **Sort**: Newest first
- **Date range**: Last 24 hours (or since last triage)

### Step 2: For each Insight, decide

For each Insight in order, spend ~60 seconds deciding:

1. **Is it actually a feature request?**
   - **Bug**: route to engineering bug tracker; mark Insight processed; do not link to a Feature
   - **Question**: route to support / docs team; mark Insight processed; flag if recurring (it's a doc gap)
   - **Strategy ask**: park in "Needs discussion"; surface in weekly review
   - **Feature signal**: continue to step 3

2. **Does it map to an existing Feature?**
   - Search Productboard for the Feature
   - If found: link the Insight to the Feature
   - If not found: create a new Feature with a draft name and link the Insight to it

3. **Tag the Insight appropriately**:
   - Customer segment (`enterprise`, `mid-market`, `smb`)
   - Source (`support`, `sales`, `nps`, `in-app`)
   - Theme if relevant (`ai`, `reporting`, `onboarding`)

4. **Mark "processed"**.

### Step 3: Weekly batch for "Needs discussion"

Anything ambiguous goes into the "Needs discussion" pile (a Productboard view or a saved filter). The weekly meeting with PM + CS + Sales decides:

- Convert to a Feature (someone takes the action)
- Park indefinitely (with rationale)
- Reject (low signal, archive)

### Step 4: Done

If the daily ritual takes more than 20 minutes, the inbox is moving faster than the team can triage. Options:

- Filter the intake (reduce noise from a channel)
- Pre-tag at intake (automate "source=support" tagging so the PM doesn't manually classify)
- Add a second triager (typically a senior PM or PMO)

## Quality bar

A well-triaged Insight has:

- [ ] Verbatim customer content preserved (not paraphrased into a one-liner)
- [ ] At least one Feature link (or marked as bug/question/strategy)
- [ ] Customer / Company association
- [ ] Source tag (which channel)
- [ ] Segment tag (which customer segment)

## Anti-patterns

| Anti-pattern | Why it hurts | Fix |
|---|---|---|
| One Feature per Insight | Explodes Feature count; dilutes scoring; obscures actual demand | Multiple Insights link to one Feature; create new Features rarely |
| Paraphrasing the Insight at intake | Loses the customer's actual words; over time the Insight inbox becomes a stream of PM interpretations rather than customer voice | Preserve verbatim; PM interpretation goes in the Feature description, not the Insight |
| Skipping triage on a busy day | One day's miss becomes a weekly backlog | Run triage every business day, no exceptions; if the PM is out, name a backup |
| Linking an Insight to 5+ Features | Says "this Insight is about everything"; informationally worthless | Link to the 1-3 Features the Insight most directly supports |
| Customer field missing | The Insight can't be filtered by segment or company; lost analytical value | Reject Insights at intake that arrive without a customer; fix the source channel config |
| Tagging is inconsistent across triagers | Two PMs use different tag names for the same thing; reporting fragments | Maintain a single tag taxonomy in a pinned doc; enforce it |
| Insights from Salesforce come without verbatim | Sales pasted the "summary" not the customer's words | Train sales to include the customer quote in the Salesforce note before pushing |

## Roles and rotation

For a team with multiple PMs, rotate triage on a weekly cadence. Benefits:

- Every PM sees the full customer voice, not just their own area
- Cross-pollination of context between product areas
- Burden of triage spread, not concentrated

Discourage permanent triage assignment to junior PMs — it sounds delegable but actually requires senior judgment about Feature creation/merge/split decisions.

## Metrics to monitor

The PM lead should track weekly:

| Metric | Target | What it tells you |
|---|---|---|
| Inbox depth (unprocessed Insights) | < 50 | Triage is keeping up |
| Daily triage time | 10-20 min | Sustainable rhythm |
| Insights per Feature (top 20 Features) | 5-30 | Healthy linking discipline; under 3 means under-linked, over 50 means over-broad Features |
| % Insights with customer association | > 95% | Channel hygiene |
| Channel mix variance week-over-week | < 30% swing | Intake stability |
| "Needs discussion" pile depth | < 20 | Weekly review is keeping up |

## What good looks like

A Productboard workspace with healthy triage shows:

- Top Features have 10-50 linked Insights each
- Insights are tagged consistently across PMs
- The "Top customers behind this Feature" sidebar shows a recognizable mix, not the same one enterprise account
- Sales asks "did you build that thing customer X asked for?" and the PM can answer with a Feature ID and 8 other customers behind it
- New PMs onboarding can read 5 random Insights in a Component and form a clear picture of the customer pain

## Sample dialogue (for training a new triager)

> *Insight*: "I cannot believe you still don't have a way to share dashboards with people who don't have an account. Every other tool does this. This is a deal-breaker." — from Salesforce, AE Priya, on Acme Corp account.
>
> *New triager*: "I think this is a new Feature?"
>
> *Senior PM*: "Let's search first. Search 'share dashboard'."
>
> *Search returns*: Feature "Shareable read-only dashboard view" (existing, with 6 linked Insights).
>
> *Senior PM*: "Existing Feature. Link this Insight to it. Tag the Insight with `enterprise`, `salesforce`, and `urgency-high`. Note the customer ID. Mark processed. Done."
>
> *New triager*: "Should I create a new Feature called 'PDF export'?"
>
> *Senior PM*: "Don't. The customer mentioned a workaround they'd accept; they didn't ask for a specific solution. The Feature stays at the opportunity level ('Shareable read-only view'), not the solution level ('PDF export'). The PM team will decide on the solution later."

Time elapsed: ~45 seconds. That's the target.
