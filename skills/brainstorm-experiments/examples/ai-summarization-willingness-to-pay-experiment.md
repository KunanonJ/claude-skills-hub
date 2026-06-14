# Example: Acme Analytics — Lean Experiment: "Will Users Pay for AI Summarization?"

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Acme Analytics (Series-B B2B data platform, ~220 employees, ~3,200 paying accounts) is considering an AI summarization feature: each dashboard would get a one-paragraph plain-English narrative auto-generated daily ("Revenue is up 8% week-over-week, driven by enterprise renewals. Three accounts are flagged at risk."). Engineering effort to ship a full version: ~5 engineer-months. Inference costs at scale: ~$80K/year.

The PM, Priya, hears strong stated interest from sales and customer success — "every customer wants this." But the PM has been burned before by stated preference. Before committing engineering, Priya wants to test the harder question: **will customers actually pay for it?** The brainstorm-experiments skill is being applied to design a lean validation in 3 weeks.

## Inputs

- Stated interest: high (sales calls, CS escalations)
- Cost to build full version: ~5 engineer-months + $80K/year inference
- Time budget for experiment: 3 weeks max
- Product surface: existing dashboard product, 3,200 accounts, ~9,000 weekly active users
- Pricing context: current tiers are $99 / $499 / $2,499 per month; AI summarization is being considered as a paid add-on or a tier-3-only feature
- Internal politics: CTO is skeptical of the cost; CRO is pushing hard; this experiment must produce a defensible signal one way or the other

## Applying the skill

1. **Wrote the XYZ hypothesis.** The instinct of a weaker PM would be "users will love AI summaries." Priya restated it as: "At least 8% of trialing tier-2 customers who see an AI summary option in their dashboard will click 'enable for $20/month' within 14 days."
2. **Demanded skin-in-the-game.** Not a survey. Not a "would you pay?" question. The signal is a paid upgrade click. SITG = money.
3. **Picked a fake door + concierge hybrid.** Fake door measures intent (click-to-pay). Concierge MVP validates that the manually-generated summary actually creates value for users who do convert.
4. **Used YODA, not industry benchmarks.** Did not look at OpenAI press claims or competitor case studies. Acme's data, Acme's customers.
5. **Pre-set kill criteria.** If conversion is below 4%, kill the feature. Between 4% and 12%, run a follow-up experiment. Above 12%, ship.
6. **Excluded the "every customer wants this" signal.** The experiment specifically does not measure stated interest. Conversations after the experiment will not change the kill/keep decision.

## The artifact

```
================================================================
  EXPERIMENT BRIEF — AI SUMMARIZATION PAID ADD-ON
  Owner:   Priya Rao (PM, Activation)
  Drafted: 2026-05-22
  Status:  Approved, starts 2026-05-26
================================================================


PART 1 — HYPOTHESIS

XYZ Format:

  "At least 8% of tier-2 trial customers (Y) who see the AI
   Summary upsell in their dashboard (Y context) will click
   'enable for $20/month' within 14 days (Z), at a willingness-
   to-pay threshold of $20/month (X% threshold)."

  X (threshold) :  8%
  Y (population):  Tier-2 trial customers (currently 380 active
                   trials, ~270 visit dashboard in any given
                   14-day window)
  Z (action)    :  Click "Enable for $20/month" CTA

The hypothesis is FALSIFIABLE — if fewer than 8% click,
we have a clear signal the feature does not earn its cost.

Counter-hypothesis (the null we are trying to reject):
  "Stated interest will not convert to paid upgrade clicks
   above 4%."

Pre-experiment Bayesian prior:
  Priya's prior: 6% conversion (between sales optimism and
                 historical add-on pricing data).
  CTO's prior:   2% conversion.
  CRO's prior:   25% conversion.

Both priors are 3-4x apart from each other. That spread is
itself evidence the team should run the experiment.


PART 2 — METHOD

This experiment is a FAKE DOOR + CONCIERGE MVP hybrid.

Why two methods together:
  - Fake door measures intent (click-to-pay)
  - Concierge MVP validates that manually-generated summaries
    actually create value for users who DO convert

If we only did fake door, we'd test demand but not whether
the value lands. If we only did concierge, we'd test value
but not whether anyone would pay. Together they answer both.


PART 3 — DESIGN

[A] FAKE DOOR

  Where:    Tier-2 trial customer dashboard, top-right of the
            main dashboard view
  What:     A clearly visible card:
            "NEW: AI-generated summary of your dashboard,
             delivered daily.
             Enable for $20/month"
            [Enable] button
  Tracking: enable_click event in analytics; cohort tagged
            "ai_summary_v1"

  On click:
    Show a modal:
      "Thanks for your interest! AI Summary is in invitation-
       only beta. We will reach out within 2 business days to
       set up your trial."
    Capture the click as the primary metric.
    Trigger a Slack alert to Priya.

[B] CONCIERGE MVP FOR CLICKERS

  When someone clicks "Enable":
    Within 24 hours, Priya (or a contractor analyst) manually
    writes a plain-English summary of that customer's
    dashboard. Delivers via email by 9am customer-local-time.
    Continues daily for up to 14 days.

  Quality bar: a 60-90 word paragraph that names the top
    metric, week-over-week movement, and one notable account
    or segment change. NOT a copy-paste of dashboard numbers.

  Goal:    Validate whether customers who convert get value.
  Capacity: Up to 30 customers (Priya + 1 contractor analyst
           at 4 hours/day each)


PART 4 — METRICS

Primary metric:
  Click-to-enable conversion rate = clicks / dashboard views
  Pre-set thresholds:
    < 4%   KILL
    4-12%  RUN FOLLOW-UP (pricing test, value-prop variant)
    > 12%  SHIP (commit engineering investment)

Secondary metrics (for the concierge phase only):
  - Email open rate (target: >60%)
  - "Continue using after week 1" survey question (target: >70%)
  - Manual unsubscribe before day 14 (target: <15%)
  - Direct "I would pay for this" qualitative quotes (sample
    of 5 customers will get a 15-min follow-up call)

GUARDRAIL metrics (catch unintended damage):
  - Tier-2 trial conversion to paid (do not drop)
  - Support ticket volume from the experiment cohort (must
    stay within 2 std dev of control)


PART 5 — POPULATION & DURATION

Population:
  - Tier-2 trial customers active in the last 30 days
  - Estimated ~270 will see the card during the experiment
    window
  - NOT shown to: existing paid customers, tier-3 customers,
    or customers in active CS escalation

Duration:
  14 days for the fake door
  14 days of concierge delivery for clickers

Control:
  No A/B split needed for the fake-door test — we are
  measuring an absolute click rate against a fixed threshold,
  not comparing variants. (If conversion lands in the 4-12%
  band, the follow-up experiment will be properly A/B tested.)


PART 6 — RISKS & MITIGATIONS

R1  Customers feel deceived when "Enable" leads to a beta
    waitlist modal.
    Mitigation: The modal language is honest ("invitation-only
    beta"). Customers who reach out get the concierge service
    within 24 hours — they DO get the feature. The "door" is
    not fake from the customer's perspective.

R2  Concierge capacity overwhelmed if clicks exceed 30.
    Mitigation: If clicks pass 30 in days 1-3, we cap fresh
    enrollments and add a "next available slot" message for
    the rest of the experiment.

R3  Internal pressure to call the result early.
    Mitigation: Pre-committed to 14-day duration. No internal
    party may change the kill/keep thresholds mid-experiment.

R4  Sales team accidentally promotes the feature to customers
    not in the experiment cohort.
    Mitigation: Sales briefed pre-launch. The button does not
    render outside the cohort.

R5  Concierge summaries leak data (e.g., wrong customer's data
    in another customer's email).
    Mitigation: Per-customer separate Google Doc; 2-person
    review (Priya + contractor) before send for the first 5
    customers, then 1-person review after the process is
    proven.


PART 7 — TIMELINE

  Week -1 (May 19-25)
    [x] Design review with CTO, CRO
    [x] Engineering scoping: 1 day to ship the fake door
        (just a feature flag + tracking event)
    [x] Concierge process documented; sample summaries
        written for 3 internal accounts to calibrate quality
    [x] Slack alert wired

  Week 0 (May 26-Jun 1)  -- EXPERIMENT STARTS
    Day 1: Soft launch to 30 customers
    Day 2: Validate alerting works; review first summaries
           with the contractor
    Days 3-7: Full cohort

  Week 1 (Jun 2-8)
    Days 8-14: Continue, hold capacity if past 30 clicks

  Week 2 (Jun 9-15)
    Day 15: Wrap-up. Run the 5 qualitative follow-up calls.

  Week 3 (Jun 16-22)
    Readout. Decision meeting with CTO, CRO, VP Product.


PART 8 — DECISION CRITERIA (PRE-COMMITTED)

After 14 days, take the path indicated by the click rate.
We commit to following the rule we wrote BEFORE the data
came in.

  CLICK RATE                ACTION
  ------------------------  -------------------------------
  <4%                       KILL. Document in failed-
                            experiments register. Send a
                            short note to CRO with the data.
                            Re-visit in 12 months only with
                            new evidence.
  4% - 8%                   RUN FOLLOW-UP. Test variants
                            (price $10/$20/$40, value prop
                            language, free with tier-3).
  8% - 12%                  CONDITIONAL SHIP. Validate that
                            secondary metrics (email open
                            rate, week-1 retention) are
                            healthy. If yes, ship as $20/mo
                            add-on. If no, treat as 4-8%.
  >12%                      SHIP. Move to engineering scoping
                            of the production version.

The decision committee is:
  Priya (PM, owns the rec)
  CTO (must approve build cost)
  VP Product (final tie-breaker)

Notably absent from the committee:
  Sales leadership (their input is in the priors, not the
  decision). This is intentional — the experiment exists
  precisely because stated interest is not a buying signal.


PART 9 — READOUT TEMPLATE (TO BE FILLED AFTER EXPERIMENT)

  Click rate observed:     ___% (vs 8% threshold)
  Total clicks:            ___ of ~270 dashboard views
  Concierge enrolled:      ___ customers
  Email open rate:         ___%
  Week-1 retention:        ___%
  Direct paid-conversion:  ___ (any customer who said "stop
                            beta, just charge me"?)
  Qualitative themes:      Top 3 quotes from the 5 follow-up
                            calls

  Recommendation:          [KILL | FOLLOW-UP | SHIP]
  Rationale:               ___
  Next step:               ___


PART 10 — WHAT THIS EXPERIMENT IS NOT

  - Not a usability test (we have one already for the
    summary format)
  - Not a pricing test (it tests one price; pricing optimization
    is the follow-up if we land in the 4-8% band)
  - Not a competitive analysis (YODA principle — we are not
    comparing to vendors)
  - Not a measure of stated interest (we already know that
    is high)

The experiment is exactly one thing: does stated interest
convert into a paid-upgrade click at our test threshold?
```

## Why this works

- **Killed the "every customer wants this" signal up front.** Sales leadership is excluded from the decision committee because their input is in the prior, not the data. This is the discipline that separates real validation from theater.
- **XYZ hypothesis is falsifiable with a clear threshold.** "8% of tier-2 trials will click 'enable' in 14 days." Not "users will love this." A weaker PM writes a hypothesis they cannot lose.
- **SITG = paid click, not survey response.** The whole point of the experiment is to test the difference between stated interest and behavioral commitment.
- **Fake door + concierge hybrid covers both demand and value delivery.** If only one method, only half the question is answered.
- **Kill criteria pre-committed.** If conversion is <4%, the feature dies. The decision rule was written before the data exists. This is the single biggest defense against post-hoc rationalization.
- **CTO and CRO priors captured.** The 2% vs 25% prior spread is itself the strongest evidence for why this experiment must be run. When the data lands, both leaders have publicly committed to a number.
- **Capacity-bounded concierge.** Up to 30 concierge customers. Not infinite. Real lean validation experiments name the limit and respect it.
- **Honest "fake door."** The modal does not lie — it says "invitation-only beta" and customers who click DO get the feature manually within 24 hours. The skill warns against deceptive fake doors; this avoids the anti-pattern.

## What's next

- If the experiment lands in the 4-12% band, the follow-up pricing experiment uses [`../../execution/pricing-prd/`](../../execution/pricing-prd/) for the pricing variants.
- If shipped, the production version requires an AI-specific PRD; see [`../../execution/ai-feature-prd/`](../../execution/ai-feature-prd/) for eval, guardrails, model selection, and cost framing.
- Pre-build assumption mapping for the broader feature should use [`../identify-assumptions/`](../identify-assumptions/).
- A pre-mortem for the production version uses [`../pre-mortem/`](../pre-mortem/) to surface Tiger/Paper Tiger/Elephant risks.
- The 5 qualitative follow-up calls feed [`../interview-synthesis/`](../interview-synthesis/) for an opportunity solution tree.
- If killed, document in the experiments register linked from [`../../confluence-expert/`](../../confluence-expert/) and revisit only with new evidence.
