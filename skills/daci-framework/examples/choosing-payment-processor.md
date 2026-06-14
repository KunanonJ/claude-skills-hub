# Example: DACI for "Choose a Payment Processor" at Northwind SaaS

> Real-world scenario showing how to apply DACI to a high-stakes vendor decision.

## Context

Northwind SaaS is a Series-B B2B subscription product (~$15M ARR). It currently uses Stripe but has hit two friction points: Stripe Billing's invoice customization is constraining for enterprise deals, and the team has been quoted lower rates by two competitors. The CFO wants a decision on whether to migrate to a different payment processor (or stay) in the next 30 days.

The CFO opened a Slack thread; 7 stakeholders chimed in with opinions in 2 days. The thread is now a swamp. The Head of Product (Asha Ravi) volunteers to facilitate a DACI to unstick the decision.

The three options on the table: stay on Stripe, migrate to Adyen, migrate to Braintree.

## Inputs

- 5 named stakeholders + 1 exec sponsor (CFO)
- 3 vendor options with one-pager pros/cons each
- Constraint: decision required within 30 days (board meeting deadline)
- Estimated migration cost: 4-6 engineer-weeks
- Annual processing cost: $1.4M (Stripe), $1.1M (Adyen quoted), $1.05M (Braintree quoted)

## Applying the skill

1. **Identified the working group** (5 stakeholders + exec sponsor).
2. **Defined the decision** as a single one: "Which payment processor will Northwind use for the next 24 months?" -- not "should we migrate" (which is a yes/no embedded in the same question).
3. **Built current-state DACI** in 10 minutes. Discovered the failure pattern -- no Driver, the CFO had implicitly assumed they were the Driver but had been treating everyone like a Contributor.
4. **Designed target-state DACI**: Asha (Head of Product) drives because the cross-functional weight lives in product workflows; CFO is the Approver; CTO is the technical Approver; everyone else is Contributor or Informed.
5. **Wrote a 30-day decision timeline** with checkpoints.
6. **Documented the framework** in Confluence so the next vendor decision has a precedent to copy.

Key decision quoted: *"Two Approvers is the maximum we tolerate. Adding Sales as a third Approver would lock the decision indefinitely -- they get Contributor status."*

## The artifact

````markdown
# DACI: Choose a Payment Processor (24-month decision)

**Working group:** Northwind SaaS finance + product + engineering
**Driver:** Asha Ravi (Head of Product)
**Decision date:** 2026-06-19 (30 days from kickoff)
**Status:** In flight (RFP responses due 2026-06-05)

## The decision (single sentence)

"Which payment processor will Northwind use as its primary billing infrastructure for the next 24 months: Stripe (incumbent), Adyen, or Braintree?"

## Stakeholders

| Person | Role | Why involved |
|---|---|---|
| Asha Ravi | Head of Product | Owns billing UX and customer impact |
| Jordan Tran | CFO | Owns cost-of-payments line; budget authority |
| Mei Lin | CTO | Owns engineering effort + technical risk |
| Pat O'Brien | Head of Sales | Voices enterprise-deal friction |
| Sara Hughes | Head of Customer Support | Voices ticket impact and migration UX |

## Current-state DACI (how this decision was unfolding)

| | Asha | Jordan (CFO) | Mei (CTO) | Pat (Sales) | Sara (Support) |
|---|:-:|:-:|:-:|:-:|:-:|
| Choose payment processor | C | D (assumed) | C | C | C |

**Pain pattern observed:**
- No real Driver: CFO assumed they were driving, but every Slack message went to all 5 people, which produced 5 opinions and 0 movement.
- Implicit Approver list of "everyone": the loudest blocker (Pat with the enterprise deal) was de facto vetoing without veto rights.
- No Informed: the broader team had no visibility into the timeline.

## Target-state DACI

| Decision sub-question | Asha | Jordan (CFO) | Mei (CTO) | Pat (Sales) | Sara (Support) | Notes |
|---|:-:|:-:|:-:|:-:|:-:|---|
| Choose payment processor | D | A | A | C | C | Two Approvers (financial + technical) |
| Define decision criteria | D | C | C | C | C | Driver owns the scorecard |
| Define migration timeline (if migrating) | C | I | D | I | C | CTO drives engineering plan |
| Approve customer comms plan | C | I | I | I | D | Support drives customer-facing change comms |
| Approve internal go/no-go | D | A | A | C | C | Same Approvers; documented in Confluence |

**Rules respected:**
- Each row has exactly one D.
- 1-2 Approvers per row (CFO for financial; CTO for technical).
- Pat moved from C-with-veto-power-implied to true C: voice but not block.

## Decision criteria scorecard

Asha (Driver) published this within 48 hours of kickoff. Approvers signed off on the criteria before vendor evaluation began.

| Criterion | Weight | Notes |
|---|---|---|
| Total cost of processing (12-mo projected) | 25% | Includes interchange + fees + transfer costs |
| One-time migration cost (eng-weeks) | 10% | CTO estimates |
| Invoice customization for enterprise deals | 20% | Sales-named blocker |
| API stability + SDK quality | 15% | CTO assessment |
| Compliance scope (PCI, SOC 2 alignment) | 10% | Existing RA/QM owner sign-off |
| Customer-impact during migration | 10% | Support assessment |
| Strategic optionality (chargeback handling, future markets) | 10% | Future-facing |

Each vendor scored 1-5 per criterion, weighted, summed.

## 30-day timeline

| Day | Milestone | Owner |
|---|---|---|
| Day 0 (2026-05-20) | DACI agreed | Asha |
| Day 2 | Criteria scorecard published | Asha |
| Day 3 | Approvers sign off on criteria | Jordan + Mei |
| Day 5 | RFP sent to Adyen + Braintree; existing Stripe quoted for renewal | Asha + Jordan |
| Day 12 | RFP responses due | Vendors |
| Day 15 | Technical evaluation complete (CTO team) | Mei |
| Day 17 | Support migration UX assessment | Sara |
| Day 20 | Sales enterprise-deal compatibility assessment | Pat |
| Day 22 | All Contributor input collected; scorecard filled | Asha |
| Day 25 | Driver presents recommendation to Approvers | Asha |
| Day 27 | Approvers sign off or push back | Jordan + Mei |
| Day 28 | Communicate to Informed list | Asha |
| Day 30 (2026-06-19) | Decision locked; if migration, Mei opens engineering project | -- |

## Veto rules

- Either Approver (CFO or CTO) can veto, but the veto must be documented with the failing criterion and a numeric threshold (per blameless governance).
- A veto re-opens the decision to one further round only; if the second round fails, the decision escalates to CEO.
- Contributors cannot veto. Their input is captured in the scorecard but does not block.

## Informed list

- All-hands at the next Friday all-hands once decision is final.
- Engineering team after Day 25 recommendation is presented (because timeline impacts roadmap).
- Board notified by CFO ahead of the next board meeting.

## Health metrics (track over the 30 days)

| Metric | Target | Actual |
|---|---|---|
| Days from kickoff to decision | <= 30 | TBD |
| Stakeholders surveyed: "do you know who is the Driver?" | 5/5 | TBD |
| Approver vetos issued | <= 1 (one revision round) | TBD |
| Slack thread message count on this topic | <= 30 (down from current swamp) | TBD |
| Documented criteria override | 0 (no "we changed our minds without documenting") | TBD |

## What happens after the decision

- If "stay on Stripe": Jordan negotiates renewal; Asha closes out the DACI; Pat documents the enterprise-deal workaround.
- If "migrate to Adyen" or "migrate to Braintree": CTO opens a migration project; new DACI created for the migration plan (different decision, different framework).

## Lessons learned (logged 2026-05-22 by Asha)

Why this decision got stuck in the original Slack thread (logged for the next decision):

1. **No named Driver.** Nobody had been told they owned moving the decision forward.
2. **Approver count ambiguous.** The CFO and CTO both assumed they had veto, but neither was named; meanwhile, Sales acted as if they did.
3. **No decision criteria.** Every conversation became "I prefer Adyen" vs "I prefer Stripe" rather than "Adyen scores 4.2 vs Stripe 3.8 on the published criteria."
4. **No timeline.** Without a date, the decision drifted.

The DACI template (Driver / Approver / Contributor / Informed + criteria + timeline) addresses all four.

## Confluence page link

`product / governance / DACI templates / Choose Payment Processor v1`

Pinned to `#product-governance` Slack channel for next vendor decision.
````

## Why this works

- One Driver (Asha), forcing single-throat-to-choke movement.
- Two Approvers maximum, split by domain (financial + technical), so no decision gridlock.
- The Sales head -- the loudest voice in the original thread -- moves to Contributor. Voice is preserved; veto is not granted.
- Criteria published before vendor evaluation prevents "I changed my mind because of vibes" overrides.
- A 30-day timeline with named checkpoints converts the swamp into a sequence.

## What's next

- Use [../create-prd/](../create-prd/) to capture the decision in PRD Section 2 (Contacts) if any feature depends on the chosen processor.
- Pair with [../../discovery/identify-assumptions/](../../discovery/identify-assumptions/) -- the "we'll save $300k/year" assumption needs explicit validation.
- Use [../summarize-meeting/](../summarize-meeting/) for the Day 25 recommendation meeting.
- Build a Confluence template DACI for future vendor decisions; pin to the product governance space.
- If "migrate" is the answer, hand off to [../launch-playbook/](../launch-playbook/) for the migration coordination.
