# Funnel Design Canvas

A 90-minute workshop canvas for defining (or re-defining) a product's activation funnel. Run with PM + Eng + Design + a data/analytics partner. Output is a JSON file that feeds `funnel_analyzer.py`.

**Date:** 2026-05-22
**Facilitator:** [PM name]
**Attendees:** [Names + roles]

---

## Pre-work (do before the workshop)

- [ ] Pull D30 retention by cohort for the last 8-12 weeks.
- [ ] Pull the 20 most common first-session events.
- [ ] Bring screenshots of the current onboarding flow.
- [ ] Identify which segments (or personas) you are focused on for this funnel.

## Step 1: Pick the framework (5 min)

- [ ] AARRR (Acquisition / Activation / Retention / Revenue / Referral)
- [ ] AAARRR (adds Awareness at the top -- choose if category or brand is new)

Decision: ____________________

## Step 2: Define the cohort (10 min)

The funnel is for **one cohort, one journey**. Mixing cohorts produces lies.

| Field | Value |
|---|---|
| Cohort (who) | e.g., "All free-trial signups in the week of 2026-05-04" |
| Persona / segment | e.g., "Small-team admins" |
| Observation window | e.g., "Day 0 through Day 30" |
| Excluded users | e.g., "Internal employees, bot traffic, test accounts" |

## Step 3: List candidate stages (20 min)

Brainstorm stages in the journey. Aim for 4-7 final stages. Each stage is a **specific event** that can be measured.

| Order | Stage event | Bucket (acq/act/ret/rev/ref) | Why it matters |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |

**Rules:**
- Each stage is a verb + object (not a state).
- Each stage is between the previous and the next (no backflows).
- Stages do not have to be sequential in time -- but in this funnel they will be measured that way.

## Step 4: Pick the activation event (15 min)

Use Sean Ellis's framework. From the candidate stages above, which event is the activation event?

The activation event satisfies:
- [ ] Specific (count + action + window)
- [ ] Observable in telemetry
- [ ] Predictive of D30 retention (in your data)
- [ ] Achievable in a short window (single session, first week)
- [ ] Self-discovered (not gated by a prompt or a coupon)

**Activation event:** ________________________

**Evidence it predicts retention:** ____________________________

## Step 5: Counter-metrics per stage (15 min)

For every stage, what is the metric that must NOT degrade if you optimize this stage's conversion?

| Stage | Primary metric (conv. into this stage) | Counter-metric |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |

If a stage has no counter-metric, ask harder: what could you do to game this conversion? That suggests the counter-metric.

## Step 6: Instrumentation check (10 min)

For each stage:

| Stage | Event already instrumented? | Source | Owner | Gap to fix |
|---|---|---|---|---|
| 1 | Y / N | | | |
| 2 | Y / N | | | |
| 3 | Y / N | | | |
| 4 | Y / N | | | |
| 5 | Y / N | | | |

A funnel cannot be measured if the events are not instrumented. List instrumentation gaps as immediate action items.

## Step 7: Pull baseline numbers (10 min, or async)

For your cohort, fill in actual counts at each stage:

| Stage | Count | Notes |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |

If counts are not yet available, document the instrumentation work needed and re-run this canvas after data lands.

## Step 8: Generate the analysis (async, 5 min)

Convert the table above to JSON and run:

```bash
python scripts/funnel_analyzer.py --input my_funnel.json --format markdown > funnel_analysis.md
python scripts/funnel_analyzer.py --input my_funnel.json --format mermaid >> funnel_analysis.md
```

Share with the team.

## Step 9: Identify owners (5 min)

For each stage transition, who owns it?

| Transition | Owner | Next action |
|---|---|---|
| 1 -> 2 | | |
| 2 -> 3 | | |
| 3 -> 4 | | |
| 4 -> 5 | | |
| 5 -> 6 | | |
| 6 -> 7 | | |

Stage ownership is shared at the team level but specific at the project level. Without an owner, a stage's conversion is everyone's problem and no one's.

## Step 10: Action items

| # | Owner | Action | Due |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

---

## Output

After the workshop, you should have:

- A JSON funnel definition committed to source control.
- A baseline analysis (markdown + Mermaid).
- Counter-metrics paired with each stage.
- A list of instrumentation gaps with owners.
- A list of fix-the-funnel candidate projects (will go into `prioritization-frameworks/`).

Re-run this canvas every 2 quarters or after a major UX change.
