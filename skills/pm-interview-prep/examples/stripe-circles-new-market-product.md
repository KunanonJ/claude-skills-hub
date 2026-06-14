# Example: Full CIRCLES Answer — "Design a Stripe Product for a New Market"

> Real-world scenario showing how to apply this skill end-to-end.

## Context

The candidate, Wei Park, is preparing for a Senior PM loop at Stripe. The recruiter has flagged that the product-sense round will be open-ended and will likely ask Wei to design a product for a market segment Stripe does not currently dominate. Wei has 6 years of PM experience at a Series-B B2B SaaS and is targeting the Senior PM level.

The interviewer is a Group PM in the Stripe Payments org. The slot is 45 minutes including intro and Q&A — effectively 35 minutes of question time. The skill's CIRCLES framework is the canonical approach for exactly this kind of question, and Wei has rehearsed the timing (3-5 min Comprehend, 2-3 min Identify, etc.) until the pace is internalized.

## Inputs

- Candidate: Senior PM bar
- Company: Stripe
- Interviewer: Group PM, Payments org
- Question: "Design a Stripe product for a new market." (intentionally vague)
- Time budget: 35 minutes
- Preparation: 8-12 STAR stories ready as backup if the round pivots to behavioral; CIRCLES pacing drilled
- Tools allowed: whiteboard or virtual canvas

## Applying the skill

1. **Did not jump to a solution.** Spent the full Comprehend budget (4 minutes) clarifying the scope. This is the single biggest differentiator between Senior PM and PM candidates.
2. **Picked a specific segment, justified it.** Did not say "small businesses." Picked "freelance creative professionals in Southeast Asia accepting cross-border payments" and defended why that specific segment.
3. **Reported 4 prioritized customer needs, not a generic list.** Mapped needs to JTBD.
4. **Cut through with an explicit criterion.** Used "strategic fit with Stripe's platform + customer pain frequency" as the prioritization criterion.
5. **Listed 5 distinct solutions** including one creative non-obvious option.
6. **Evaluated trade-offs** with a 4-column comparison (impact, effort, risk, strategic fit).
7. **Summarized with a single recommendation, a why, and a next step.**
8. **Stayed on the time budget.** Came in at 32 minutes, leaving 3 minutes for the interviewer to push back.

## The artifact

```
================================================================
  PRODUCT SENSE ANSWER — STRIPE
  Question: "Design a Stripe product for a new market."
  Candidate: Wei Park
  Target level: Senior PM
  Time used: 32 minutes (of 35-min budget)
================================================================


--- COMPREHEND (4 min) ---

Wei: "Before I jump in, can I clarify three things?

  1. By 'new market' do you mean a new geography, a new
     customer segment, or a new use case? Or open to my choice?
  2. Are there constraints I should respect — e.g. must build
     on existing Stripe primitives, or greenfield?
  3. Is the success criterion 'biggest opportunity for Stripe'
     or 'most strategic for Stripe in 3-5 years'?"

Interviewer: "Open to your choice on #1. Build on existing
Stripe primitives if reasonable, but don't constrain yourself
artificially. Success criterion is 'most strategic for Stripe
in 3-5 years', not pure short-term TAM."

Wei: "Got it. I will pick a specific segment, ground it in
JTBD, and prioritize for 3-5 year strategic value, not
immediate revenue."


--- IDENTIFY THE CUSTOMER (3 min) ---

"I am going to pick a specific segment: freelance creative
professionals in Southeast Asia who accept cross-border
payments from clients in North America and Europe. Concretely
— freelance designers, video editors, illustrators, software
developers based in Vietnam, Indonesia, the Philippines, and
Thailand who get paid by US, UK, and EU clients.

Why this segment, three reasons:

  1. Stripe's current core customer is small-to-medium online
     businesses in mature payment markets (US, UK, EU, Canada,
     Australia). Cross-border individual freelancers in SEA
     are a market Stripe touches via Stripe Atlas and Express
     but does not own end-to-end.

  2. The SEA freelance population is in the millions and
     growing. They have an acute pain — getting paid
     internationally — that current tools (PayPal, Wise,
     bank wires) solve poorly with high fees and slow
     settlement.

  3. Strategic fit: a freelancer in SEA today is the SMB
     business owner of 2030. Owning the relationship early
     is a 3-5 year strategic bet, not a quarter-1 revenue bet.
     That maps to your success criterion."


--- REPORT CUSTOMER NEEDS (6 min) ---

"Let me list 4 prioritized needs for this segment, mapped to
JTBD:

  Need 1 — Get paid in my local currency without losing 6-8%
  to FX + intermediary fees.
  JTBD: 'When my US client wires me $2,000, hire me to make
  sure I net at least $1,900 in dong/rupiah/peso/baht.'

  Need 2 — Get paid quickly. Today it takes 3-7 business days.
  JTBD: 'When my client says they paid me, hire me to see the
  money in my account same-day so I can pay my rent on time.'

  Need 3 — Look professional to international clients without
  needing a US LLC.
  JTBD: 'When I invoice a client, hire me to make the payment
  experience feel as smooth as a US-based freelancer's, so I
  do not lose work to my US-based competitors.'

  Need 4 — Manage taxes and compliance without becoming an
  accountant.
  JTBD: 'When I get paid from 4 countries, hire me to make
  sure I am not breaking SEA tax laws or US 1099 rules, so
  I do not get a surprise audit.'

I would also call out an anti-need: a US LLC. Stripe Atlas
solves the US-LLC pathway, but in interviews with SEA
freelancers, only the top tier wants the US LLC overhead.
Most just want the payment to work."


--- CUT THROUGH PRIORITIZATION (4 min) ---

"Prioritization criterion: strategic fit with Stripe's
platform multiplied by customer pain frequency.

  Need              Pain freq  Strategic fit  Score
  ---------------   --------   -------------  -----
  1 FX / fee loss   Every pay  HIGH           5x5 = 25
  2 Speed of pay    Every pay  HIGH           5x5 = 25
  3 Look pro        Every pay  MEDIUM         5x3 = 15
  4 Tax/compliance  Quarterly  MEDIUM         3x3 =  9

I am going to focus on Needs 1 and 2 because they are tied
(both score 25) and they reinforce each other — fast cheap
payment is one product motion, not two. Need 3 follows
naturally from a well-designed payment flow. Need 4 is a
real pain but the strategic fit is lower; Stripe is not
becoming a tax accountant."


--- LIST SOLUTIONS (8 min) ---

"Five solutions, ranging from incremental to creative:

  S1  Stripe Connect for Freelancers (SEA edition)
      A streamlined Express-account onboarding optimized for
      individual freelancers in SEA, with default local-
      currency payout, FX fee disclosed up front, and same-day
      bank settlement in the 4 target countries.

  S2  Local payment rails partnership
      Partner with local rails (DuitNow in Malaysia, PromptPay
      in Thailand, GoPay in Indonesia, GCash in Philippines)
      so the freelancer can receive into a local wallet
      instantly, then withdraw to bank or spend directly.

  S3  Hosted invoicing experience targeted at SEA freelancers
      A simple invoice product (Stripe Invoicing already
      exists) with localized fields, multi-currency display,
      and a "looks like a US freelancer" payment page — but
      with the back-end optimized for SEA settlement.

  S4  Freelance Earnings Card (CREATIVE — non-obvious)
      A virtual + physical card tied to the freelancer's
      Stripe balance. The freelancer can spend their earnings
      directly in local currency without converting back to
      bank — eliminating one whole FX step. This makes Stripe
      the freelancer's primary financial relationship, not
      just the payment intermediary. This is the strategic
      bet that maps to your 3-5 year horizon.

  S5  Stripe Climate-style 'global freelancer fund' to deepen
      community brand affinity — non-product but supports
      acquisition.

I will set S5 aside as marketing, not product. The real
choice is among S1, S2, S3, S4."


--- EVALUATE TRADE-OFFS (5 min) ---

"
  Solution                     Impact  Effort  Risk    Strat fit
  --------------------------   ------  ------  ------  ---------
  S1 Connect SEA edition       MED     LOW     LOW     MED
  S2 Local rails partnership   HIGH    MED     MED     HIGH
  S3 SEA invoicing experience  MED     LOW     LOW     MED
  S4 Earnings Card             HIGH    HIGH    HIGH    VERY HIGH

S1 and S3 are table stakes — they should ship in any case
and they are low-risk extensions of existing Stripe primitives.

S2 is the highest near-term impact. Local rails partnerships
are not glamorous but they unlock the same-day settlement that
the customer cares about most. Effort is medium because Stripe
already partners with networks at the institutional level.

S4 is the strategic bet. It is high-risk (regulatory complexity
in 4 countries, KYC, anti-money-laundering, card-issuance
licensing). But if it lands, Stripe owns the freelancer's
whole financial relationship — exactly the 3-5 year strategic
moat the question called for."


--- SUMMARIZE (2 min) ---

"My recommendation: sequence the four solutions across 3 years.

  Year 1   Ship S1 (Connect SEA edition) + S3 (SEA invoicing)
           as table stakes. Acquire the user. Validate that
           SEA freelancers are willing to switch from PayPal
           to Stripe at our target conversion rate.

  Year 2   Ship S2 (local rails). This is the impact lift on
           speed-of-payment that drives Stripe to be the
           default tool, not PayPal.

  Year 3   Ship S4 (Earnings Card) in the 1-2 countries with
           the cleanest regulatory pathway (probably the
           Philippines and Singapore-adjacent flows). This
           is the strategic bet that defines whether Stripe
           owns the next generation of SMB owners or watches
           Wise/Revolut do it.

The bet that defines the strategic answer is S4. S1-S3 keep
us in the game; S4 wins the next decade.

Next step I would take if this were day one: 12 customer
interviews — 3 freelancers each in Vietnam, Indonesia,
Philippines, Thailand. Validate that the JTBD I listed are
real and prioritized in the order I have them. Specifically
pressure-test that 'speed of payment' is genuinely tied with
'FX / fee loss' rather than secondary."

================================================================
INTERVIEWER FOLLOW-UP (3 min)
================================================================

Interviewer: "Why not just expand Stripe Atlas to SEA?"

Wei: "Atlas solves the US-LLC pathway, which I called out as
an anti-need. The top tier of SEA freelancers wants Atlas;
the broad middle just wants the money to land cleanly.
Expanding Atlas to SEA is a different product for a different
segment — high-end freelancers building agencies. That is a
good adjacent product but it does not address the 4 needs I
prioritized. If I had to choose between the two for Year 1,
I would choose Connect SEA edition + invoicing because the
addressable market is 10x larger and the JTBD is sharper."

================================================================
SELF-CRITIQUE (post-interview, not shared with interviewer)
================================================================

What went well:
  - Held the full Comprehend budget. Clarifying scope produced
    the "strategic in 3-5 years" success criterion that drove
    the whole answer.
  - Specific segment with defended reasoning.
  - One creative solution (S4 Earnings Card) without going
    full sci-fi.
  - Time budget held; came in at 32 of 35 minutes.

What to do differently:
  - Spent slightly too long on solution evaluation (5 min vs
    target 3-5 min); could have been crisper.
  - Could have called out a counter-metric: if Stripe takes
    too much margin out of cross-border payments, freelancers
    route around it. A guardrail metric would have signaled
    Senior PM instinct more strongly.
  - Should have offered a hypothesis on competitive response
    (Wise, Payoneer, Revolut). I did not name competitors
    by name and only one interviewer follow-up touched it.

Score per dimension (self-graded against Senior PM rubric):
  Problem framing                 STRONG
  Customer empathy                STRONG
  Creativity                      STRONG (S4 was the move)
  Prioritization rigor            STRONG
  Trade-off articulation          ADEQUATE (slightly long)
  Strategic thinking              STRONG
  Communication / structure       STRONG
  Senior PM signal overall        STRONG
```

## Why this works

- **Full Comprehend budget.** Wei spent 4 minutes clarifying scope before any solutioning. The "strategic in 3-5 years" framing the interviewer offered defined the whole answer. A weaker candidate would have asked one question and dived into solutions.
- **Specific segment with defensible reasoning.** "Freelance creative professionals in SEA accepting cross-border payments" is a real segment. "Small businesses" is not. Specificity is the single strongest signal of customer empathy.
- **Explicit prioritization criterion.** Used "strategic fit x pain frequency" and showed the math. Interviewers grade prioritization not on the answer but on the rigor of the criterion.
- **One creative solution.** The Earnings Card (S4) is the move that signals Senior PM range — most candidates list 5 incremental ideas. S4 is the "strategic bet" the question explicitly invited.
- **Sequenced the answer.** Did not pick a single winner; sequenced four solutions across 3 years with rationale. This is what real Senior PM strategic recommendations look like.
- **Held time budget.** 32 of 35 minutes used. Left room for follow-up. Candidates who use 100% of the time signal poor pacing.
- **Self-critique afterward.** Wei graded their own answer against the rubric, identifying the missing guardrail metric and the missing competitive-response hypothesis. This kind of reflection is what closes the gap from Senior to Group PM over time.

## What's next

- For behavioral round preparation, use the STAR template from this same skill and prepare the 12 canonical stories.
- For the technical round, work through the estimation 5-step framework and at least 2 metric-tree warm-up problems.
- After the loop, use [`../pm-career-ladder/`](../pm-career-ladder/) to map any feedback received against the Senior PM rubric for the next loop.
- If the offer comes in, use [`../pm-onboarding/`](../pm-onboarding/) to design a 30-60-90 day plan.
- The product-sense skills exercised here transfer directly to [`../../execution/create-prd/`](../../execution/create-prd/) and [`../../discovery/brainstorm-ideas/`](../../discovery/brainstorm-ideas/) on the job.
