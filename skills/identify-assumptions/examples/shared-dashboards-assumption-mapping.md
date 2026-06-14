# Example: Acme Analytics — Assumption Mapping for the Shared Dashboards Feature

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Acme Analytics (Series-B B2B data platform, ~220 employees, ~3,200 paying accounts) is considering "Shared Dashboards v1" — a feature that lets a customer build a dashboard and share it with people outside their org via a public link with optional embedded login. Sales is pushing for it as a competitive table-stakes parity feature. The PM (Priya Rao) has 6 weeks before the team commits engineering.

Priya is using the identify-assumptions skill to surface and rank the assumptions underneath the feature. She is intentionally NOT scoping the PRD yet; she wants to know which assumptions are most likely to falsify the whole bet so she tests those first.

## Inputs

- Feature concept: Shared Dashboards v1 — public/auth-gated dashboard sharing
- Sales claim: ~40% of mid-market deals lose to a competitor at the dashboard-sharing question
- Engineering: 4-5 engineer-months estimated; touches the embed framework
- Existing product: dashboards work great internally; no sharing at all today
- Customer interview data: 14 interviews in the last quarter mentioned sharing in some form
- Team: Priya (PM), Liang (Designer), Reza (Engineer)
- Timing: 2 weeks for assumption mapping + risk validation, then commit/no-commit decision

## Applying the skill

1. **Ran devil's advocate from all three roles separately.** Each role wrote their own challenges before the group session. Group-mode devil's advocate produces 4-5 assumptions; silent independent mode produces 8-12.
2. **Categorized into the 4-category model.** Shared Dashboards is an existing-product feature, not a new product, so Priya used Torres' core 4 (Value, Usability, Viability, Feasibility). Did NOT use the 8-category extended set.
3. **Surfaced 8 distinct assumptions.** Some are obvious, some are non-obvious. The non-obvious ones (Viability A2, Usability A4) are exactly what assumption mapping is for.
4. **Ranked on Impact x Risk (likelihood of being wrong).** Pre-set scoring rubric before scoring; team scored independently then reconciled.
5. **Picked the top 3 to test first.** The remaining 5 are documented but parked.
6. **Tied each top-3 assumption to a specific lean experiment.** Assumption mapping that does not lead to experiments is theatre.

## The artifact

```
================================================================
  ASSUMPTION MAP — SHARED DASHBOARDS v1
  Owner: Priya Rao (PM, Activation)
  Drafted: 2026-05-22
  Decision date: 2026-06-12 (commit / kill / re-scope)
================================================================


PART 1 — FEATURE STATEMENT (used as the anchor for assumptions)

"Acme customers will be able to share a dashboard with people
 outside their account via either (a) a public link with no
 login, or (b) a magic-link login that creates a guest viewer.
 Shared dashboards will refresh on the same cadence as the
 source dashboard. Pricing: included in tier-2 and tier-3;
 limited to 1 shared dashboard on tier-1."


PART 2 — DEVIL'S ADVOCATE ROUND (silent, 25 min)

Each role challenged the concept independently, then shared.

PM Devil's Advocate (Priya):
  - Is there real demand or are we chasing competitor parity?
  - Will paying customers actually share more often than
    they downgrade?
  - Does sharing cannibalize tier-3 seat licenses?
  - Will this distract us from Activation, our actual
    quarterly goal?

Designer Devil's Advocate (Liang):
  - Will external viewers understand a dashboard built for
    internal context?
  - Is the sender confident the data they're sharing is
    correct AT the moment of share, not just when they built
    the dashboard?
  - Will "guest viewers" feel like real users or feel like
    a degraded experience that hurts our brand?

Engineer Devil's Advocate (Reza):
  - Do we have the row-level security primitives to make
    this safe at all?
  - What happens if a shared dashboard contains a viz that
    accidentally exposes PII from another customer (cross-
    tenant data risk)?
  - Can our embed framework scale to 10x the current load
    from external traffic?
  - Who maintains the guest-auth flow once we're past v1?


PART 3 — ASSUMPTIONS, CATEGORIZED

8 assumptions surfaced. Mapped to the 4 categories:

VALUE — Will customers want this?

  V1  "At least 25% of mid-market customers will share at
       least one dashboard within 60 days of the feature
       launching."
       Evidence today: 5 of 14 interviews mentioned wanting
       to share with stakeholders. Sales claim of 40% deal
       loss reason is unverified.

  V2  "Customers who share will value the feature enough
       that it materially affects their renewal."
       Evidence today: none. We are inferring from
       competitor presence in deals.

USABILITY — Can customers figure out how to use it?

  U1  "Sharers will be able to set the right permission
       level (public vs. magic-link) on the first try
       without help."
       Evidence today: none.

  U2  "External viewers will understand the dashboard
       context (filters, date ranges, definitions) without
       the sender having to explain."
       Evidence today: contradicting signal — internal
       Acme staff frequently misread other teams'
       dashboards.

VIABILITY — Can the business sustain this?

  V3  "Sharing will not cannibalize tier-3 seat licenses
       in a way that reduces ARR."
       Evidence today: unknown. CS leadership and finance
       have different intuitions.

  V4  "Engineering and ongoing maintenance cost (estimated
       at 0.5 engineer-quarters/year ongoing after launch)
       is justified by the upgrade and retention impact."

FEASIBILITY — Can we build this?

  F1  "Our embed framework can support 10x external traffic
       on the same shared dashboard without performance
       degradation."

  F2  "Row-level security primitives are sufficient to
       prevent any cross-tenant data leak via a shared
       dashboard."


PART 4 — SCORING (Impact x Risk)

Rubric (pre-defined before scoring):

  Impact: how much does this assumption being wrong damage
          the bet?
    5  Falsification = kill the whole feature
    4  Falsification = major re-scope
    3  Falsification = launch delay
    2  Falsification = mitigation in v2
    1  Cosmetic — does not change the path

  Risk: likelihood the assumption is wrong
    5  Strong contradicting signal or no evidence at all
    4  Weak supporting signal
    3  Mixed signal
    2  Strong supporting signal, minor gaps
    1  Validated

Each team member scored independently. Reconciled values:

                                    Impact  Risk  Score
  V1  25% of mid-market will share    4      3     12
  V2  Sharing affects renewal         5      4     20
  U1  Permission UI is intuitive      3      3      9
  U2  External viewers understand     4      4     16
  V3  No tier-3 seat cannibalization  4      3     12
  V4  Maintenance cost is justified   3      2      6
  F1  Embed framework scales 10x      4      2      8
  F2  No cross-tenant data leak       5      2     10

  (Note F2: Impact is 5 because a leak is brand-ending;
   Risk is 2 because Reza has strong evidence the existing
   primitives are sufficient. Score is 10 — important to
   verify but not a top-3 spend.)


PART 5 — RANKED LIST

  Rank  Assumption  Score  Category
  ----  ----------  -----  -----------
  1     V2          20     Value
  2     U2          16     Usability
  3     V1          12     Value
  4     V3          12     Viability
  5     F2          10     Feasibility
  6     U1           9     Usability
  7     F1           8     Feasibility
  8     V4           6     Viability


PART 6 — TOP 3 PICKED FOR VALIDATION

The team will validate the top 3 BEFORE engineering commit.
The other 5 are documented; we will only revisit them if
the top 3 pass.

Top 3:

  V2 (score 20) — Sharing will materially affect renewal
  U2 (score 16) — External viewers understand dashboard
                  context
  V1 (score 12) — 25% will share within 60 days


PART 7 — EXPERIMENT BRIEFS FOR THE TOP 3

[V2] "Sharing affects renewal"

  Experiment: 30-customer concierge MVP. PM manually
  produces shared dashboard links for 30 mid-market
  customers known to have external stakeholder needs.
  Track for 60 days:
    - Do they use it?
    - In renewal conversations, do they cite it?
    - In win/loss interviews on these accounts vs control,
      does sharing change the renewal narrative?
  Pass: in qualitative interviews, >=15 of 30 spontaneously
  reference the shared dashboard as part of their value
  perception. Document in dovetail.
  Fail: <5 of 30 mention it.

  Cost: ~12 hours of PM time over 60 days.
  Decision rule: PASS = green light. FAIL = kill the
  feature outright; the renewal signal isn't there.
  AMBIGUOUS (5-15) = run a structured renewal-conversation
  follow-up.

[U2] "External viewers understand the dashboard"

  Experiment: 8 unmoderated usability sessions on Loom or
  Maze. Show the same shared dashboard to 8 external
  viewers (recruited via UserInterviews; given the dashboard
  context only — no setup explanation).
  Ask: "what is this dashboard telling you?" Score whether
  the takeaway matches the dashboard creator's intent.
  Pass: >=6 of 8 produce the correct takeaway.
  Fail: <=3 of 8 produce the correct takeaway.
  Ambiguous: 4-5 of 8 = redesign of the external view.

  Cost: ~$800 + 4 hours.
  Decision rule: PASS = ship as scoped. FAIL = redesign
  external-viewer experience first (different UI, different
  context affordances). AMBIGUOUS = redesign smaller.

[V1] "25% will share within 60 days"

  Experiment: Fake door. Add a "Share dashboard" button to
  the dashboard view, route the click to a modal saying
  "Coming soon — early access waitlist." Track click rate
  by customer tier.
  Pass: >=25% click rate among mid-market.
  Fail: <10% click rate.

  Cost: 1 engineer-day. Already feature-flagged in adjacent
  code.
  Decision rule: PASS = strong demand signal. FAIL = no
  demand, kill feature. AMBIGUOUS = run sales-call follow-up
  to deal-loss claim.


PART 8 — WHAT WE ARE NOT TESTING (and why)

  V3 (cannibalization) — Cannot be tested before launch.
       Mitigation: launch with monitoring; CS + finance
       align on a roll-back threshold.

  F2 (no cross-tenant data leak) — Cannot be "tested" the
       way a value assumption can. Treated as an
       engineering security requirement. Reza commits to
       a threat model + penetration test BEFORE GA, but
       this is a build-time guarantee, not a validation
       step.

  U1 (permission UI intuitive) — Will be tested during
       implementation usability testing. Not blocking the
       commit decision.

  F1 (10x scale) — Engineering will build load test before
       GA. Not blocking the commit decision.

  V4 (maintenance cost) — Internal estimate, validated by
       Reza's engineering plan, not by experiment.


PART 9 — DECISION FRAMEWORK

  After 2 weeks of running the 3 experiments:

  ALL 3 PASS         Commit to engineering. Begin PRD.
  V2 fails           Kill the feature. The renewal signal
                     was the load-bearing assumption.
  U2 fails           Re-scope: external-viewer redesign
                     before any commit.
  V1 fails           Likely kill, unless sales can produce
                     specific deal evidence we missed.
  Any AMBIGUOUS      Run the documented follow-up.


PART 10 — WHAT THIS PROCESS PROTECTED US AGAINST

  - Building Shared Dashboards because sales said so,
    without testing whether customers actually share.
  - Skipping the external-viewer experience design until
    after engineering had locked the architecture.
  - Treating cross-tenant data risk as a product question
    rather than a build-time engineering requirement.
  - Confusing "feature in competitor product" with
    "feature that drives our renewals."
```

## Why this works

- **Three roles, independent surfacing.** PM, Designer, and Engineer each wrote challenges silently before sharing. This produced 8 distinct assumptions vs. the 3-4 a group-discussion session typically yields.
- **Used the right category model.** Shared Dashboards is an existing-product feature, so Priya used the core 4 categories (Value, Usability, Viability, Feasibility). The 8-category extended set is for new-product decisions — using it here would have produced noise.
- **Impact and Risk scored separately.** A common mistake is to score "importance" as a single number. Splitting impact (consequence of being wrong) from risk (probability of being wrong) is what surfaces the asymmetric cases — like F2 (cross-tenant leak), which is high impact but low risk because Reza has evidence the primitives work.
- **Top 3 testable in 2 weeks.** Each top-3 assumption has a concrete experiment, a cost, and a decision rule. Less-experienced teams produce a beautiful assumption map and then never test anything.
- **Decision rule before experiment, not after.** The PASS/FAIL/AMBIGUOUS thresholds for each experiment are written before the data arrives. This is the single biggest defense against post-hoc rationalization.
- **F2 (cross-tenant leak) handled as engineering requirement, not experiment.** Some assumptions are not validated via PM experiment — they are guaranteed by build-time controls. The map names which is which.
- **V3 (cannibalization) explicitly parked.** Cannot be tested pre-launch. The mitigation is monitoring + rollback threshold, not pre-launch validation. Naming this honestly is the discipline.

## What's next

- Each of the 3 experiments is designed in detail using [`../brainstorm-experiments/`](../brainstorm-experiments/).
- If all 3 pass, the PRD itself uses [`../../execution/create-prd/`](../../execution/create-prd/).
- A pre-mortem on Shared Dashboards using [`../pre-mortem/`](../pre-mortem/) will classify the parked feasibility assumptions (F1, F2) as Tigers / Paper Tigers / Elephants.
- For V3 (cannibalization), the post-launch monitoring metric is wired into [`../../execution/north-star-metric/`](../../execution/north-star-metric/) and [`../../execution/activation-funnel/`](../../execution/activation-funnel/).
- Cross-tenant data leak (F2) — treat as a compliance question, hand to security and audit teams; out of scope for product discovery.
- After 60 days post-launch (if shipped), use [`../interview-synthesis/`](../interview-synthesis/) on the concierge customers from V2's experiment.
