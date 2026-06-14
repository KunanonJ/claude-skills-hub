# Example: David Okafor — 30-60-90 Day Plan as New PM at Northwind Fintech

> Real-world scenario showing how to apply this skill end-to-end.

## Context

David Okafor is starting in two weeks as the new PM for the "Disputes & Chargebacks" product area at Northwind Fintech, a Series-B B2B payments platform (~140 employees). He is replacing a PM who left for a competitor after 14 months. The area has been without a PM for 5 weeks; engineering has been shipping operational fixes but no roadmap progress. The disputes operations team (internal users + customer-facing) has been escalating noise to engineering directly.

David has 5 years PM experience, all at consumer fintech. This is his first move into B2B. He needs to land credibly with three audiences: his EM partner, the disputes operations team, and the VP Product who hired him. He is using the pm-onboarding skill to design a structured 30-60-90 day plan before day 1.

## Inputs

- David's background: 5 years PM at consumer fintech (top-10 banking app)
- New scope: B2B disputes & chargebacks platform serving 800 merchant customers
- Team: 7 engineers, 1 designer, 1 data analyst (shared with adjacent team)
- Manager: VP Product (Anna)
- EM partner: Reza
- Time gap: 5 weeks without a PM
- VP Product expectation (verbal): "Land softly, but I want a roadmap by end of Q3"
- Constraint: David is also relocating internationally; first 2 weeks of work are remote

## Applying the skill

1. **Diagnosed STARS before day 1.** Used the recruiter and Anna for an early scoping call. The signals (departing PM, operational backlog, internal team escalating, but underlying product is working) pointed to Realignment, not Turnaround.
2. **Resisted the urge to bring a roadmap.** A weaker new PM would have pitched a 90-day roadmap in week 1 to look smart. The skill is clear: in Realignment, listen for 60 days before publishing direction.
3. **Built the stakeholder map week 1.** Identified 14 named stakeholders across product, eng, design, ops, customer success, finance, and 3 customer voices.
4. **Used the 30-day questions verbatim.** Asked the five Watkins questions in every 1:1, captured patterns.
5. **Identified two early wins by day 45.** Small, observable, irreversible, low-risk. Not "the roadmap" — just credibility builders.
6. **Anchored the day-60 review.** Brought a written PoV to Anna at exactly day 60, not earlier.
7. **Shipped one PRD by day 90.** Scoped to be the right size for the credibility budget he had earned.

## The artifact

```
================================================================
  DAVID OKAFOR — 30-60-90 DAY PLAN
  Role: PM, Disputes & Chargebacks
  Company: Northwind Fintech (Series-B B2B payments)
  Start: 2026-05-25
  Day-30: 2026-06-23 | Day-60: 2026-07-22 | Day-90: 2026-08-22
  Manager: Anna (VP Product)
  EM partner: Reza
================================================================

PRE-DAY-1 (2 weeks before start)

  [x] Read Northwind public materials, S-1 if any, press releases
  [x] Read internal docs Anna shared: last 2 quarterly roadmaps,
      last 3 monthly business reviews, customer NPS report
  [x] 30-min call with Anna to align on:
      - First-90-day expectations
      - The departing PM's "what worked / what was hard" memo
      - Who I must meet by week 2
      - What no one else is going to tell me
  [x] 20-min call with Reza (EM partner) to:
      - Understand his read on team health
      - Schedule first weekly 1:1
      - Get his shortlist of engineers I should meet first
  [x] Set up workstation, slack, email, Jira, Confluence access


================================================================
DAYS 1-30 — LEARN  (Goal: build context, no decisions)
================================================================

WEEK 1 — LOGISTICS, MANAGER, IMMEDIATE TEAM

  Day 1   Onboarding admin. Manager 1:1 — kickoff template
          (from pm-1on1s skill).
  Day 2   1:1 with Reza. Agree on partnership operating model.
          Sit in on team standup as silent observer.
  Day 3   Coffee/intro 1:1s with each of 7 engineers (15 min).
  Day 4   1:1 with the designer and the data analyst.
  Day 5   First end-of-week sync with Anna. Draft stakeholder
          shortlist (14 names) and 90-day plan.

  Stakeholder shortlist (initial):
    Product:   Anna (VP), 3 sibling PMs
    Eng:       Reza (EM), 7 engineers
    Design:    Liang (lead designer), shared
    Data:      Sofia (data analyst), shared
    Ops:       Disputes Ops manager (Renata), 4 ops specialists
    CS:        Disputes-focused CSMs (3)
    Finance:   Chargebacks-impact finance contact (1)
    Customers: 3 named merchant contacts willing to take a call

WEEK 2 — CUSTOMER IMMERSION

  - Listen to 12 recorded customer calls (Gong)
  - Read top-20 support tickets in the disputes queue
  - 30-min call with 3 named customer contacts
  - Read the last 6 months of customer-feedback Jira tickets
  - Map customer segments: enterprise (>$1M GMV), mid-market
    ($100K-$1M), self-serve (<$100K)
  - Output: top-5 customer pain hypotheses (1 page)

WEEK 3 — PRODUCT IMMERSION

  - Use the product daily as an internal merchant
  - Walk through the dispute lifecycle end-to-end with an ops
    specialist
  - Read all PRDs from last 12 months (8 docs)
  - Walk the metrics tree:
      Top-level   Chargebacks dispute win rate %
      Inputs      Time-to-evidence-submission, evidence quality
                  score, automated-routing accuracy %, manual-
                  intervention rate, customer satisfaction with
                  dispute outcome
  - Output: product-area map + baseline metrics dashboard

WEEK 4 — TEAM IMMERSION

  - 30-min 1:1 with each of the 7 engineers (NOT a re-do of week
    1 coffee chats — these are deeper)
  - 5 Watkins questions in every 1:1:
      1. What is going well you most want to preserve?
      2. What is broken or breaking?
      3. What changes would you most want from this role?
      4. What would derail me in the first six months?
      5. Who else should I be talking to about this?
  - 1:1 with Renata (disputes ops manager) — twice. She is the
    single most informed voice on the area.
  - Output: team strength/gap map; STARS diagnosis draft

DAY-30 DELIVERABLE — "What I'm Learning" memo (1 page)

  Format: shared to Anna, then Reza for fact-check, then
  optional share to the team.

  Contents:
    - STARS diagnosis: Realignment.
      Evidence: the product is working (dispute win rate 71%,
      industry median 65%); the team is competent (engineers
      report low burnout); but customer expectations are
      ahead of the team's roadmap, and Ops is doing manual
      work that should be product.
    - Top 3 things going well:
      1. Dispute win rate above industry median
      2. Engineering quality high — escaped defects below team
         average
      3. Strong Ops partnership; Renata is the institutional
         memory of the area
    - Top 3 risks:
      1. Ops is escalating to engineering directly; PM
         workflow has been bypassed for 5 weeks
      2. 2 of 800 merchant customers are 38% of dispute volume
         (concentration risk); product not designed for them
      3. The dispute evidence flow is 9 manual steps in the
         worst case; this is the operational debt
    - Top 5 questions still open:
      1. Is the long-tail of small merchants worth optimizing
         for or accept the concentration?
      2. Why did the previous PM leave? (asked carefully)
      3. What is Anna's secret roadmap intent that she has
         not told me?
      4. Is the data infrastructure ready to support an
         outcome-based roadmap?
      5. Where does the disputes product fit in the company-
         level NSM?


================================================================
DAYS 31-60 — PLAN  (Goal: build a point of view)
================================================================

WEEK 5 — DEEPER CUSTOMER WORK

  - 30-min recorded calls with 6 more merchant customers,
    weighted toward the 2 concentration accounts
  - Cross-functional joint sessions: 1 with finance (chargebacks
    P&L impact), 1 with CS leadership (renewal correlation
    with dispute experience)
  - Output: customer-segment-specific JTBD map

WEEK 6 — COMPETITIVE + MARKET

  - Read public competitor materials (Stripe Dispute, Adyen
    RevenueProtect, Chargebacks911)
  - Internal interview with 2 sales engineers on what
    competitors say in deals
  - Output: 1-page competitive PoV

WEEK 7 — EARLY WIN IDENTIFICATION

  Two early-win candidates identified, both small enough to
  ship inside 90 days, both visible and credibility-building:

  EW1  Auto-route disputes from concentration customers to
       a dedicated queue with the senior ops team. 1 sprint
       of work. Visible to Renata's team day-1. Cuts manual
       triage time by an estimated 30%.

  EW2  Add a "previous dispute outcome" indicator to the
       dispute screen so ops sees pattern (this customer has
       won 14 of 15 prior disputes -> high-confidence flow).
       2 sprints of work. Reduces evidence-gathering time.

  Both early wins are:
    - Small (sprint-scale, not roadmap-scale)
    - Reversible (feature flag protected)
    - Observable (clear metric movement in 4 weeks)
    - Aligned to Ops who has been doing manual workarounds

WEEK 8 — POINT OF VIEW DRAFT

  Wrote a 2-page PoV memo:
    - Where the product is winning, where it is losing
    - The 3 bets that matter most for the next 4 quarters
    - The 2 things we will explicitly NOT do
  Reviewed with Reza first, then revised, then Anna.

DAY-60 DELIVERABLE — PoV memo + early wins announcement

  Walked Anna through the PoV in a 60-minute session. Agreed:
    - PoV is right
    - Early wins ship in Q3
    - Real roadmap published at day 90, not day 60

  Announced early wins to the team and to Renata. Renata's
  reaction: "Finally."


================================================================
DAYS 61-90 — DELIVER  (Goal: credibility + roadmap)
================================================================

WEEK 9 — EARLY WINS SHIP

  EW1 ships in week 9, behind feature flag. Rolled to
  concentration customers first. Renata's team measures
  triage time daily.

WEEK 10 — FIRST PRD WRITTEN

  First real PRD authored by David: "Dispute Evidence
  Workflow v2" — the systemic fix to the 9-step manual flow.
  Used the org's PRD template (8 sections + team extension).
  Reviewed by Reza, Anna, Renata, Sofia. Passed the 10-second
  exec scan.

  Scope is intentionally modest — not a moonshot. David is
  spending credibility carefully.

WEEK 11 — Q3 ROADMAP DRAFT

  Drafted Q3 roadmap with 3 bets aligned to the PoV. Reviewed
  with sibling PMs to surface dependencies. Pressure-tested
  with Renata and finance.

  Roadmap structure (3 bets, in priority order):
    Bet 1  Dispute evidence workflow v2 (the PRD above)
    Bet 2  Concentration customer dedicated experience
    Bet 3  Outcome-based metrics dashboard for ops

WEEK 12 — Q3 ROADMAP REVIEW + RETRO

  Roadmap presented at the cross-team product review. Anna
  signed off. Roadmap published.

  Personal retro with Anna:
    - STARS diagnosis (Realignment) — confirmed correct
    - Early wins — landed both
    - Roadmap — ambitious but credible
    - 1 thing to do differently: David held the customer
      calls list to himself for too long; sibling PMs found
      out about the concentration insight from Renata, not
      from David. Should have shared earlier.

DAY-90 DELIVERABLE — Roadmap + retro

  Published Q3 roadmap (3 bets, owner = David, EM = Reza)
  Retro memo to Anna (private)
  Public team retro with the 7 engineers (group format)


================================================================
WHAT DAVID DID NOT DO IN 90 DAYS
================================================================

  - Did not rewrite the team's working processes
  - Did not change the team's tools or rituals
  - Did not commit to any single customer's wishlist
  - Did not pick a fight with the departing PM's decisions
  - Did not bring a 5-quarter roadmap to month 1
  - Did not promise leadership a turnaround story

  Each of these was a temptation. The skill is clear: in
  Realignment, do no harm, listen long, act small early.
```

## Why this works

- **STARS diagnosis came first.** David did not treat the situation as a Turnaround (because the product is working) or a Sustaining-success (because customer expectations are diverging). Realignment is the right diagnosis and it dictated the whole pace.
- **Listened before publishing direction.** A roadmap at day 30 would have been built on guesses; a roadmap at day 90 was built on 6 weeks of customer + team data. The trust earned is the difference.
- **Early wins are small.** EW1 is one sprint. EW2 is two sprints. Both are reversible. Both are aligned to Renata's pain. New PMs who pick a big visible bet as the early win miss it and burn credibility.
- **5 Watkins questions in every 1:1.** Used the same five questions across 14 stakeholders so patterns surfaced. Different questions across people = no comparable data.
- **Named what he did not do.** The "what David did NOT do" section is the discipline. Every item there is a temptation a less-experienced PM would have indulged.
- **PRD at day 70, not day 14.** The first PRD David authored was a real one with real evidence behind it. Most new PMs ship a placeholder PRD in week 2 to look productive; this destroys the credibility-bank that the listening phase built.
- **Shared the retro publicly.** A group retro at day 90 with the engineering team signals confidence and invites continued feedback. Most PMs do a private retro with their manager only.

## What's next

- For week 1's manager 1:1 kickoff and the weekly Reza 1:1, use [`../pm-1on1s/`](../pm-1on1s/) — Type A for Anna, Type B for Reza.
- The first PRD in week 10 should follow [`../../execution/create-prd/`](../../execution/create-prd/).
- The Q3 roadmap presentation maps to [`../../execution/outcome-roadmap/`](../../execution/outcome-roadmap/) and [`../../execution/roadmap-communication/`](../../execution/roadmap-communication/).
- Concentration-customer risk identified in week 5 deserves an explicit assumption-map; see [`../../discovery/identify-assumptions/`](../../discovery/identify-assumptions/).
- 6 months in, David revisits [`../pm-career-ladder/`](../pm-career-ladder/) to assess where he is on the Sr-PM trajectory.
- When David hands off to a future PM successor someday, this onboarding plan becomes the template.
