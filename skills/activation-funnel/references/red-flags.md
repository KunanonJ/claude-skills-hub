# Red Flags: Activation Funnel

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them. Pair with the SKILL.md and Troubleshooting table.

## How to use this document

When you have just produced a funnel analysis (via `funnel_analyzer.py` or by hand) or proposed an activation optimization, scan the red flags below before acting on the data. Each red flag shows the *bad* and *good* interpretation, anchored in McClure's AARRR and Sean Ellis's activation framing.

---

## Red Flag 1: Vanity-Metric Optimization (Top of Funnel Without Activation)

**Symptom.** Funnel analysis shows acquisition is up 200%, celebrated as a win. Activation rate is unchanged (or down). Retention drops.

**Why it's bad.** Acquisition without activation is buying users who do not become customers. McClure's Pirate Metrics put acquisition at the top precisely because it is *the easiest* metric to inflate — and the easiest to mistake for progress. The activation step is where retention is determined; optimizing only acquisition is vanity.

**Bad example:**
> "Q3 result: signups +200% (50K -> 150K). Big win."

**Good example:**
> "Q3 result: signups +200% (50K -> 150K). Activation rate dropped from 28% to 14% (cohort 30-day). Net activated users: 14K -> 21K (+50%) — real growth, but the funnel is leakier. Investigate: are new signups lower-intent?"

**How to catch it.** Always report acquisition alongside activation rate. If only acquisition appears, the report is vanity.

---

## Red Flag 2: Optimizing One Funnel Stage at the Cost of Another

**Symptom.** Team optimizes the signup form (drop fields, simplify) — signups up 40%. Two weeks later, activation drops 20% because new signups have no profile data and abandon at setup.

**Why it's bad.** Funnel stages are coupled. Optimizing for the local metric can damage the downstream. The funnel analyzer reports stage-by-stage drop-off precisely so the analyst can see whether a local win produced a global loss.

**Bad example:**
> Test: simplify signup form (remove 6 fields). Result: signup conversion +40%. Ship.

**Good example:**
> Test: simplify signup form. Result: signup +40%, activation -20%, net activated users +12% (still positive but smaller than headline). Counter-test: add 'optional profile' step *after* activation moment. Result: signup +35%, activation -2%, net +33%."

**How to catch it.** When optimizing a stage, did you measure the next 1-2 stages downstream? If not, you may have damaged the funnel net.

---

## Red Flag 3: Activation Defined as a Random Event (Not Predictive of Retention)

**Symptom.** Team picks "user clicked a button on day 1" as activation. Has not validated that this event predicts day-30 retention.

**Why it's bad.** Sean Ellis's activation definition is the event that *statistically predicts* long-term retention. Slack's 2000-messages, Facebook's 7-friends-in-10-days, Dropbox's 1-file-1-folder-1-device were all picked because cohort analysis showed they were retention-predictive. A button-click that does not predict retention is just an event.

**Bad example:**
> "Activation = user clicked 'Get Started' button on day 1."

**Good example:**
> "Activation candidate: 'completed 3 setup steps within first session.' Validation: cohort analysis on 30-day retention. Users who hit candidate event: 68% retain. Users who do not: 19%. Lift = 49pp — strong signal. Activation defined."

**How to catch it.** Is your activation event validated against retention via cohort analysis? If not, it is an event, not activation.

---

## Red Flag 4: Pirate Metrics Without Counter-Metrics

**Symptom.** Funnel report shows only the AARRR conversions going up. No counter-metrics (churn, refund rate, NPS, support load).

**Why it's bad.** Funnel metrics can be inflated by techniques that damage product quality (aggressive notifications, hidden cancel buttons, fake urgency). Counter-metrics catch this. McClure himself recommends balancing the funnel with retention and revenue context.

**Bad example:**
> "Funnel report: Acquisition +30%, Activation +15%, Retention +8%, Revenue +20%, Referral +5%. Everything's up."

**Good example:**
> "Funnel: Acquisition +30%, Activation +15%, Retention +8%, Revenue +20%, Referral +5%. Counter-metrics: support tickets per user +22% (sustained), NPS -4 points (concerning), 30-day refund rate +12% (action triggered). Net: investigate refund/support spikes before declaring win."

**How to catch it.** Does your funnel report include counter-metrics? If not, you cannot see damage.

---

## Red Flag 5: Treating One-Time Spike as Trend

**Symptom.** Activation rate spiked from 28% to 41% for one week. Team declares win and ships announcement.

**Why it's bad.** Spikes can be driven by composition changes (a marketing campaign brought in higher-intent users), seasonality, or noise. Treating a one-week spike as trend produces premature victory claims and embarrassing reversals when the spike normalizes.

**Bad example:**
> "Activation hit 41% last week, up from 28%. Onboarding redesign is working. Announcement going out tomorrow."

**Good example:**
> "Activation 41% last week (up from 28% baseline). Composition check: 80% of last week's signups came from a paid campaign targeting power users. Apples-to-apples comparison: organic activation 30% (up 2pp). Conclusion: small real lift, large composition effect. Wait 4 more weeks before announcing."

**How to catch it.** Before declaring a trend, do you have 4+ weeks of data and a composition check? If not, you are over-claiming.

---

## Red Flag 6: Funnel Without Telemetry (Building on Wishful Thinking)

**Symptom.** Funnel diagram exists. Stage counts come from spreadsheet estimates and "what we think happens", not instrumented events.

**Why it's bad.** A funnel without telemetry is a fiction. The funnel_analyzer tool requires real stage counts; estimates produce reports that look authoritative but encode the team's hopes instead of reality. The SKILL.md "When NOT to Use" specifically warns about this.

**Bad example:**
> Stage counts: Signup 1000, Profile setup ~600?, First action ~300?, Activation ~150?

**Good example:**
> Stage counts (from product analytics, last 30 days): Signup 1,247, Profile setup 723 (58%), First action 412 (33%), Activation 219 (18%). Events instrumented in Segment, verified against database counts."

**How to catch it.** Where did your stage counts come from? If estimates, instrument first.

---

## Red Flag 7: Bottleneck Mis-Identification (Biggest Drop vs Biggest Opportunity)

**Symptom.** Funnel shows a 40pp drop from Acquisition to Activation; team focuses there. But a 25pp drop from Activation to Retention has 10x the revenue impact because each Retention-stage user is worth $X.

**Why it's bad.** The biggest drop in percentage is not always the biggest opportunity in business value. Weighted by user value (LTV, revenue), a smaller drop at a high-value stage can outweigh a bigger drop early. The bottleneck call-out in funnel_analyzer is a starting point, not a final answer.

**Bad example:**
> "Biggest drop is signup-to-activation (40pp). Focus all optimization there."

**Good example:**
> "Biggest pp drop: signup-to-activation (40pp). Biggest $ opportunity: activation-to-revenue (25pp drop but each activated user is worth $200 LTV; $5M annual revenue lift potential vs $1.2M from signup-to-activation). Recommended focus: revenue stage, with light investment in earlier stages."

**How to catch it.** Did you weight bottlenecks by user value, or just by % drop? Unweighted drops mislead.

---

## Red Flag 8: Funnel Stages Designed Backwards (Output Defining Input)

**Symptom.** Funnel stages chosen to match an existing analytics dashboard, not to reflect the actual user journey.

**Why it's bad.** The funnel exists to reveal the user's path; stages must come from the journey, not from tool limitations. Tool-driven funnels miss critical drop-offs because they fit what is easy to measure, not what matters.

**Bad example:**
> "Funnel: Page view -> Click -> Form submit -> ?" (Stages reflect Google Analytics event types.)

**Good example:**
> "Funnel reflects user journey (interview-validated): Land on page -> Read value prop -> Start signup -> Complete signup -> Reach setup screen -> Begin setup -> Complete setup -> Take first action -> Reach activation event. Telemetry added for all 9 stages."

**How to catch it.** Did stages come from user journey interviews/observation, or from existing dashboards? Tool-shaped funnels miss insights.

---

## Red Flag 9: Cohort Effects Hidden (Aggregating Across Time)

**Symptom.** Funnel reports lifetime aggregate ("of all signups, X% activated"). Hides the fact that recent cohorts have much lower activation than older ones.

**Why it's bad.** Aggregation hides trends. Recent cohorts might be activating at 12% while older cohorts (when product was simpler) activated at 35%. The aggregate looks like 22% — close to neither truth. Cohort analysis is mandatory for trend understanding.

**Bad example:**
> "Lifetime activation rate: 22%."

**Good example:**
> "Activation by cohort (signup month): Jan 35%, Feb 31%, Mar 28%, Apr 22%, May 17%, Jun 14%. Trend: declining 4pp/month. Investigate: what changed in onboarding between Jan and Jun?"

**How to catch it.** Are your funnel numbers cohort-segmented or aggregated? Aggregated hides trends.

---

## Red Flag 10: Confusing Funnel with Journey

**Symptom.** Funnel diagram is linear: A -> B -> C -> D. Real user behavior has loops, branches, and re-entries.

**Why it's bad.** Many user journeys are not linear funnels. They include re-engagement (lapsed users return), branching (consumer vs creator flows), and multi-session activation. Forcing a linear funnel diagram on a non-linear journey misses signal. Funnels are useful but not universal.

**Bad example:**
> "Funnel: Signup -> Setup -> Activation -> Retention -> Revenue. Linear."

**Good example:**
> "Primary funnel (first-session activation): Signup -> Setup -> First action -> Activation. Re-engagement funnel (returning lapsed users): Lapsed -> Email open -> Return -> Reactivation event. Two funnels, separate analyses; combined view shows the loop."

**How to catch it.** Is the real journey linear? If users loop or branch, a single funnel hides that.

---

## Red Flag 11: Funnel Diagram Without Action Plan

**Symptom.** Beautiful funnel diagram with conversion rates. No experiments designed, no owners assigned, no investment decision made.

**Why it's bad.** The funnel is a diagnosis tool. The output of diagnosis is treatment. A funnel without a follow-up plan is decoration; the team marvels at the leak and does nothing.

**Bad example:**
> "Funnel diagram presented in QBR. Discussion ended after 'wow, big drop at setup.' No action."

**Good example:**
> "Funnel diagram presented. Bottleneck: setup stage (32pp drop). Action: 5 candidate experiments designed (drop fields, add progress bar, defer setup, prefill data, video walkthrough). Owner: PM. Top 2 experiments prioritized for next sprint. Quarterly target: lift setup completion from 41% to 55%."

**How to catch it.** Does the funnel analysis end with owned, dated next actions? If not, it was decoration.

---

## Red Flag 12: AARRR Treated as Mandatory When AAARRR Fits Better (Or Vice Versa)

**Symptom.** Team uses 5-stage AARRR for a product where the front-end Awareness stage is actually the bottleneck. Or team uses 6-stage AAARRR for a product where Awareness is irrelevant (e.g., internal tool).

**Why it's bad.** Framework match-to-context matters. McClure's AAARRR extension exists because some products need explicit Awareness measurement; others do not. Forcing the wrong shape produces either missing data (AARRR missing Awareness) or noise (AAARRR padding for internal tool).

**Bad example:**
> Internal tool funnel using 6 stages: "Awareness 100%, Acquisition 100%, Activation 60%, Retention 40%..." (Awareness is meaningless for an internal tool that everyone is required to use.)

**Good example:**
> Internal tool funnel: 4 stages (no Awareness, no Acquisition — usage is mandated): Onboarded -> Activated -> Retained -> Power user. Stages chosen to reflect this context."

**How to catch it.** Does your funnel shape match your product context? If Awareness is irrelevant, drop it; if it is the bottleneck, add it.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Vanity Optimization | Acquisition reported alongside activation rate? |
| 2 | Local Win, Global Loss | Optimization measured 1-2 stages downstream? |
| 3 | Activation Not Predictive | Activation event validated via retention cohort? |
| 4 | No Counter-Metrics | Counter-metrics (churn, NPS, support) tracked? |
| 5 | Spike Treated as Trend | 4+ weeks of data + composition check? |
| 6 | No Telemetry | Stage counts from instrumented events, not estimates? |
| 7 | Bottleneck Mis-Identified | Bottlenecks weighted by user value, not just %? |
| 8 | Stages Tool-Shaped | Stages reflect user journey, not dashboard limits? |
| 9 | Cohort Hidden in Aggregate | Numbers segmented by signup cohort? |
| 10 | Linear When Journey Isn't | Loops and branches mapped separately if real? |
| 11 | No Action Plan | Owned, dated next actions tied to bottleneck? |
| 12 | Wrong Funnel Shape | AARRR/AAARRR matched to product context? |

## Related Reading

- SKILL.md Troubleshooting section (for symptom -> root cause -> resolution)
- references/aarrr-stages.md (for stage definitions, if present)
- references/activation-validation.md (for retention-cohort method, if present)
- brainstorm-experiments/references/red-flags.md (for experiment design when optimizing stages)
- SHARED_OUTPUT_SCHEMA.md (for output format integration with Jira/Linear/Confluence)
