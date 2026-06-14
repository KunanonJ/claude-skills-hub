# Example: Northwind SaaS — Product Trio Ideation for B2B Onboarding Redesign

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Northwind SaaS (Series-B B2B payments platform, ~140 employees) has a leaky onboarding funnel. Of merchants who sign up, only 38% reach "first successful transaction" within 7 days. Customer success says the manual hand-holding it takes to get a merchant live is unsustainable — they cannot scale it past the next 200 merchants. The Activation team has 1 quarter to move the metric.

The PM, Maria Chen, has 4 weeks before quarterly planning. Rather than walking in with her own list of ideas, she is running a Product Trio ideation session with the lead designer (Liang) and the lead engineer (Reza). The brainstorm-ideas skill is being applied to generate 15 ideas across the trio, then converge on a small set tied to specific opportunities in the existing-product Opportunity Solution Tree.

## Inputs

- Metric: 7-day activation rate (first successful transaction within 7 days of signup)
- Baseline: 38%; target: 55% within one quarter
- Customer success data: 6 named friction patterns from recent CS calls
- 14 customer interview transcripts from the last 90 days
- Team: Maria (PM), Liang (Designer), Reza (Engineer)
- Constraint: 1 quarter to ship; can use feature flags; cannot rebuild the auth system
- Constraint: cannot increase CS headcount

## Applying the skill

1. **Framed the problem before brainstorming.** Defined outcome (55% 7-day activation), segment (new merchants in tiers 1-2 self-serve), and constraints (no auth rebuild, no CS headcount add). The team did NOT start generating ideas until the frame was locked.
2. **Ran the Product Trio session in 3 silent rounds.** Each role generated 5 ideas independently (no group-think) before sharing. This is the discipline the skill names — Brainstorming-then-Sharing produces wider idea spread than open discussion.
3. **Scored each of 15 ideas against the existing-product lens.** Did not pick winners by feel.
4. **Built the Opportunity Solution Tree.** The 15 ideas were rolled up into 3 opportunities (interview-grounded), then ideas became candidate solutions within those branches.
5. **Compared within branches, not across them.** Per skill: choose between Solution A vs B for the same opportunity. Never compare Solution A (Opportunity 1) against Solution F (Opportunity 3) because they answer different customer needs.
6. **Picked 2 bets to validate, not to ship.** The session output is what to test next quarter, not what to build.

## The artifact

```
================================================================
  ONBOARDING REDESIGN — PRODUCT TRIO IDEATION OUTPUT
  Date: 2026-05-22
  PM:        Maria Chen
  Designer:  Liang Zhou
  Engineer:  Reza Karimi
  Outcome:   7-day activation from 38% -> 55% by 2026-08-31
================================================================


PART 1 — PROBLEM FRAME

Outcome: 7-day activation rate (% of new merchants who complete
        first successful transaction within 7 days of signup)
        Baseline: 38%
        Target: 55%

Target segment: Tier 1-2 self-serve merchants (US-based,
        <$100K projected annual GMV, no dedicated CS rep)
        ~600 new signups/month

Constraints:
  - Cannot rebuild auth system (compliance review pending)
  - No CS headcount addition
  - 1 quarter (12 weeks) to ship
  - Feature flags available
  - Must be reversible (kill switch within 1 sprint)


PART 2 — 15 IDEAS FROM THE TRIO

==========================================
PM PERSPECTIVE (Maria) — 5 ideas
==========================================

PM-1  Tiered onboarding by GMV projection
      Ask one question on signup: projected monthly GMV.
      Route enterprise candidates to a 60-min onboarding
      call with sales engineering. Route self-serve to a
      streamlined 5-min flow. Today everyone gets the same
      30-min wizard.

PM-2  Industry-specific templates
      Top-10 merchant industries each get a one-click
      "preset" of products, tax categories, and webhook
      defaults. Today everyone starts from a blank slate
      regardless of vertical.

PM-3  "Sandbox first" — let merchants test before going live
      Default new accounts to test mode. First transaction
      in test mode counts as activation milestone 1.
      Production switch is intentional, gated on success.

PM-4  Activation-bound pricing incentive
      "Process your first $100 in week 1 -> first month
      transaction fees waived." Aligns merchant time with
      our outcome.

PM-5  Account manager assignment for hovering merchants
      Identify merchants who hit the "stuck" pattern (signed
      up, no test transaction by day 3) and proactively
      assign a CS rep for one 15-min call. Costly per
      account; reserved for top-decile by GMV projection.

==========================================
DESIGNER PERSPECTIVE (Liang) — 5 ideas
==========================================

D-1   Progress bar that doesn't lie
      Today the progress bar shows 5 steps even though the
      hard step (compliance verification) takes 24-72 hours
      and is invisible. Show all dependencies with realistic
      timing so merchants don't bounce thinking it's broken.

D-2   "Send to my developer" handoff
      80% of merchants have someone else integrate the API.
      A first-class flow to send a pre-filled developer-
      handoff email with credentials, sample code, and a
      direct calendar link to integrations support.

D-3   Live receipts feed during integration
      As the merchant's developer tests, the merchant sees
      a real-time activity feed: "Test charge of $1.00 just
      came in from your sandbox." Today they refresh blindly.

D-4   Friction-killing 1-page checklist
      One page. 7 boxes. Tickable. Replaces the 11-tab
      wizard. Empty boxes are the most powerful prompt in UX.

D-5   "Why we need this" inline explainer
      Every form field that asks for sensitive data (SSN,
      bank routing) gets an inline microcopy explaining
      why and citing the regulator. Reduces abandonment at
      the compliance step.

==========================================
ENGINEER PERSPECTIVE (Reza) — 5 ideas
==========================================

E-1   Pre-fill from a single tax-ID lookup
      With one tax ID, we can pre-fill business name,
      address, structure type via a public lookup API.
      Cuts 8 fields to 1. Already used internally for
      enterprise; just plumb it into self-serve.

E-2   Async compliance with optimistic activation
      Today compliance must clear before any transaction.
      Change to: allow test-mode transactions immediately,
      production transactions once compliance clears.
      Merchant's perceived activation time drops from
      24-72 hours to minutes.

E-3   Webhook auto-discovery from popular platforms
      If the merchant has a Shopify/WooCommerce/Magento
      store, OAuth into it and auto-configure the webhook.
      Today this is 14 manual steps.

E-4   Daily activation-cohort report to CS
      Engineering effort to build a daily report of
      day-3 stuck merchants for CS. Powers PM-5 above.

E-5   API key auto-rotation kill-switch
      Side effect: removes one merchant fear of "what if
      something goes wrong with the test key, do I lose
      everything?" Reduces psychological friction.


PART 3 — OPPORTUNITY SOLUTION TREE

Outcome: 7-day activation rate 38% -> 55%

  Opportunity 1: Compliance step blocks activation
    perception time even when work is done
    (Evidence: 8 of 14 interviews; CS data shows 60% of
     day-3 stuck merchants are waiting on compliance)

    Solutions:
      E-2  Async compliance with optimistic activation
      D-1  Honest progress bar with real timing
      D-5  Inline "why we need this" microcopy

  Opportunity 2: Self-serve merchants get lost in a
    wizard built for enterprise integration teams
    (Evidence: 5 of 14 interviews; activation rate by tier
     shows self-serve is 22 pts below enterprise)

    Solutions:
      PM-1  Tiered onboarding by GMV
      PM-2  Industry-specific templates
      PM-3  Sandbox-first default
      D-4   One-page tickable checklist
      D-2   Send-to-developer handoff
      E-1   Tax-ID single-field pre-fill
      E-3   Webhook auto-discovery

  Opportunity 3: Merchant -> developer handoff loses
    momentum
    (Evidence: 6 of 14 interviews mentioned "I had to wait
     for my dev"; activation rate where merchant != integrator
     is 12 pts lower)

    Solutions:
      D-2   Send-to-developer handoff (also above)
      D-3   Live receipts feed during integration
      E-3   Webhook auto-discovery (also above)

  Opportunity 4: Top-decile merchants would benefit from
    proactive CS touch
    (Evidence: 3 of 14 interviews; ROI questionable for
     mid-tier; reserved for high-projection merchants)

    Solutions:
      PM-5  Account manager assignment for hovering merchants
      E-4   Daily activation-cohort report to CS

  Opportunity (declined): Activation-bound pricing incentive
    PM-4 sits outside the tree because the interview signal
    does not support price-as-a-blocker. Merchants did NOT
    cite cost in interviews. PM-4 is a marketing experiment,
    not an activation product change. Documented and parked.


PART 4 — SCORING WITHIN BRANCHES

Score each candidate solution on a 1-5 scale:

  Core Value      Does this single solution clearly remove a
                  named friction?
  Speed           Can we validate in <2 weeks?
  Differentiation Does this beat Stripe / Adyen for the same
                  segment?
  Timing          Is the team ready to ship this in 12 weeks?
  Scalability     Does this scale beyond the test cohort?

OPPORTUNITY 1 — Compliance friction

  Solution                              CV  Sp  Df  Ti  Sc  Total
  E-2  Async compliance                  5   3   4   4   5    21
  D-1  Honest progress bar               4   5   2   5   5    21
  D-5  Inline microcopy                  3   5   3   5   5    21

  Tied at 21. Tie-breaker: E-2 is structurally the only
  one that changes activation TIME, not just perception.
  Choose E-2.

OPPORTUNITY 2 — Self-serve gets lost

  Solution                              CV  Sp  Df  Ti  Sc  Total
  E-1  Tax-ID pre-fill                   4   5   3   5   5    22
  D-4  One-page checklist                4   4   3   4   5    20
  PM-1 Tiered onboarding by GMV          5   3   3   3   5    19
  PM-3 Sandbox-first default             5   3   4   4   5    21
  PM-2 Industry templates                4   3   4   2   4    17
  D-2  Send-to-developer handoff         4   3   3   4   4    18
  E-3  Webhook auto-discovery            4   2   4   3   5    18

  Top: E-1 (22), PM-3 (21), D-4 (20). Choose PM-3
  (sandbox-first) because it pairs with E-2 above — same
  underlying philosophy of "let them experience success
  before the slow compliance step gates them."

OPPORTUNITY 3 — Merchant-developer handoff
  D-2 already chosen via opp 2. Defer the rest.

OPPORTUNITY 4 — Proactive CS for top decile
  PM-5 + E-4 combo. Reza estimates E-4 is a one-sprint
  build. But this is bottlenecked on CS capacity, not on
  product. Park for next quarter unless 7-day activation
  doesn't move with bets 1 + 2.


PART 5 — BETS THIS QUARTER

The team commits to validating two bets:

BET A: Async compliance + optimistic activation (E-2)
       Solves Opportunity 1.
       Hypothesis: shifting to async compliance moves 7-day
       activation +8 pts for merchants who would otherwise
       wait 24+ hours for compliance.

BET B: Sandbox-first default flow (PM-3)
       Solves Opportunity 2.
       Hypothesis: making test-mode the default cuts
       merchant time-to-first-test-transaction from
       median 6 hours to median 30 minutes, lifting 7-day
       activation +6 pts.

Combined target: 38% + 14 pts = 52% (close to the 55%
goal). The Quarter 4 work will be Opportunity 3 (handoff)
unless one of these underperforms.

Both bets ship behind feature flags. Both have kill criteria
defined in their own experiment briefs.


PART 6 — WHAT WE DID NOT PICK AND WHY

  PM-4 (pricing incentive)
    Not supported by interview evidence. Parked.

  D-3 (live receipts feed)
    High delight value but doesn't move the metric.
    Candidate for Q4.

  PM-2 (industry templates)
    High effort for 10 verticals; phased follow-up.

  PM-5 + E-4 (proactive CS)
    Bottlenecked on CS capacity; revisit Q4.

  E-5 (auto-rotation)
    Quality improvement, not activation lever. Goes to
    backlog.

Documenting the no-pick set is as important as the picks.
These are not bad ideas — they are not the ideas for THIS
outcome in THIS quarter.
```

## Why this works

- **Silent independent generation before group discussion.** Each of the three roles generated 5 ideas alone before sharing. This is the single move that produces 15 distinct ideas instead of 5 with three people nodding.
- **The Opportunity Solution Tree is interview-grounded.** Each opportunity cites how many of the 14 interviews supported it. The skill warns against opportunities invented by the team without customer evidence — and this output cites the evidence row by row.
- **Compared solutions WITHIN branches, not across.** PM-3 (sandbox-first) competed against E-1 and D-4 because all three address Opportunity 2. PM-3 did NOT compete against E-2 (async compliance) — they address different opportunities and both can be bets.
- **Declined PM-4 explicitly and named why.** The pricing incentive sounds clever but had zero interview support. A weaker session would have kept it in the bucket "because it might work." Naming it as parked and naming the reason is the discipline.
- **Picked bets, not the whole list.** Two bets, with clear hypotheses. Not "we're going to ship 7 of these." The combined hypothesis (52% vs target 55%) is honest about the remaining gap.
- **Anti-pattern avoided: scoring before opportunity mapping.** A weaker team scores 15 ideas on a generic RICE matrix and picks the top 3. That ignores the structural fact that 3 ideas solving the same friction are redundant; you want 1 idea per friction.

## What's next

- Both bets become lean experiments designed in [`../brainstorm-experiments/`](../brainstorm-experiments/), each with its own XYZ hypothesis and kill criteria.
- The 14 customer interviews underpinning the opportunity tree should also be synthesized via [`../interview-synthesis/`](../interview-synthesis/) into a shareable opportunity-tree Mermaid diagram.
- Each bet that ships gets a full PRD via [`../../execution/create-prd/`](../../execution/create-prd/).
- The activation funnel is monitored via [`../../execution/activation-funnel/`](../../execution/activation-funnel/) — these bets target the activation step specifically.
- Pre-mortem the bigger of the two bets (E-2 async compliance) using [`../pre-mortem/`](../pre-mortem/) before commit.
- Assumption-map both bets using [`../identify-assumptions/`](../identify-assumptions/) so we know what could falsify each.
