# Red Flags: Brainstorm Experiments

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them. Pair with the SKILL.md and Troubleshooting table.

## How to use this document

When you have just designed an experiment, scan the red flags below before running it. Each red flag shows a *bad* and *good* version of an experiment specification.

---

## Red Flag 1: Confirmation-Biased Experiment Design

**Symptom.** The experiment is structured so that any plausible outcome will be interpreted as success. The hypothesis is unfalsifiable.

**Why it's bad.** Savoia's pretotyping insists on falsifiable XYZ hypotheses ("At least X% of Y will do Z") because the only useful experiment is one that *can fail*. Confirmation-biased designs produce false confidence: the team believes they validated the idea, but actually validated nothing.

**Bad example:**
> Hypothesis: "Customers will be interested in our new AI assistant." Measurement: "Survey users; if any positive sentiment, we proceed."

**Good example:**
> Hypothesis: "At least 25% of trial users who see the AI-assistant prompt will click 'Try It' within their first session." Threshold: 25%. Below 15% = kill. 15-25% = iterate on prompt. Above 25% = proceed to build."

**How to catch it.** State your kill criterion *before* running. If you cannot describe a result that would make you stop, the experiment is confirmation theater.

---

## Red Flag 2: Asking Opinions Instead of Observing Behavior

**Symptom.** Experiment is a survey: "Would you use a feature that does X?" Results show 78% say yes; team builds; nobody uses it.

**Why it's bad.** Stated preference is a notoriously bad predictor of actual behavior (Fitzpatrick's Mom Test). People say they would exercise, would pay for premium, would use a productivity tool. They do not, do not, and do not. Pretotyping requires *behavioral* signal, not stated.

**Bad example:**
> Survey: "Would you pay $19/month for an AI writing assistant?" Result: 67% yes. Decision: build.

**Good example:**
> Smoke test: landing page with $19/month price and "Buy Now" button (routes to "coming soon, get notified" form requiring email + credit-card-on-file). Result: 4.2% of 5,000 visitors completed form. Decision: above 3% threshold, proceed."

**How to catch it.** Does the result rely on what people *say*, or what they *do*? If the former, redesign.

---

## Red Flag 3: Sample Size Too Small to Mean Anything

**Symptom.** Experiment ran with 8 users. 5 of them clicked the button. Team declares "62.5% conversion" and proceeds.

**Why it's bad.** Small samples produce noisy results. A 5-of-8 result could easily be 2-of-8 or 7-of-8 in a different sample. Decisions made on small samples are coin flips with confidence theater.

**Bad example:**
> "8 users tested. 5 clicked Upgrade. Conversion = 62.5%. Decision: ship."

**Good example:**
> "Target: 200 users in landing-page test. Stopping rule: 95% confidence band must exclude 0%-or-baseline. Pre-registered threshold: 4% conversion. Actual: 247 users, 11 conversions (4.5%), confidence interval [2.5%, 7.1%]. Decision: proceed (lower bound > baseline)."

**How to catch it.** State your minimum sample size *before* running. Do not stop early just because the result looks good.

---

## Red Flag 4: Mixing Variables (Can't Tell What Caused What)

**Symptom.** Experiment changes the headline, the button color, the price, and the call-to-action all at once. Some metric moves. Nobody knows which change drove it.

**Why it's bad.** Confounded experiments produce uninterpretable results. Multi-variable tests have a place (multivariate testing) but require either much larger samples or sequential isolation. Default to one variable per experiment.

**Bad example:**
> A/B test compares "Old page" vs "New page" where new page has new headline, new image, new price, and new CTA. Conversion +12%. Decision: ship new page.

**Good example:**
> Sequential single-variable tests: (1) headline test — flat. (2) image test — +3%. (3) price test — +8%. (4) CTA test — +1%. Total understanding: price was the driver. New experiment: explore price elasticity further."

**How to catch it.** How many variables changed in the variant? If more than 1, you have a confounded design.

---

## Red Flag 5: Pretotype That Costs Too Much to Be a Pretotype

**Symptom.** "Quick smoke test" took 6 weeks and 3 engineers. By the time it ran, the team was already committed to the idea.

**Why it's bad.** The whole point of pretotyping is *speed and cheapness*. A pretotype that costs 6 weeks loses its purpose — by the time it returns data, the sunk-cost fallacy ensures the team will ship regardless. Pretotypes should cost hours, not weeks.

**Bad example:**
> "Pretotype: built a working prototype with backend, login, and 3 features. 6 weeks engineering effort."

**Good example:**
> "Pretotype: landing page with mockup screenshots and a 'Get Early Access' form. Built in 2 hours using Carrd. Live for 7 days, drove traffic via $200 LinkedIn ads. 11% form completion. Decision: above 7% threshold, build MVP."

**How to catch it.** Time from idea to live experiment. If above 1 week, it is not a pretotype.

---

## Red Flag 6: No Counter-Metric (Only Looking at What Goes Up)

**Symptom.** Experiment measures "clicks on Upgrade button" but ignores whether users who clicked actually paid, retained, or were happy.

**Why it's bad.** Optimizing one metric without watching counter-metrics is how teams ship growth hacks that damage NPS. The experiment "succeeds" on the local metric and harms the global outcome.

**Bad example:**
> Test: aggressive upsell modal. Result: Upgrade clicks +280%. Decision: ship.

**Good example:**
> Test: aggressive upsell modal. Primary: Upgrade clicks +280%. Counter-metrics: 30-day refund rate +45%, NPS for upgraders -12 points, support tickets +60%. Decision: kill — net negative."

**How to catch it.** Did you pre-declare a counter-metric? If not, you are not measuring damage.

---

## Red Flag 7: Hypothesis Without "Why" (No Causal Theory)

**Symptom.** "Let's try adding social proof to the landing page." No theory of why it should work, no prediction of magnitude.

**Why it's bad.** Experiments without causal theory teach you nothing transferable. Even if the result is positive, you do not know why, so you cannot generalize. The "X% of Y will do Z" format requires the *why* to be explicit.

**Bad example:**
> "Add social proof. See if conversion goes up."

**Good example:**
> "Hypothesis: SMB buyers (Y) on our landing page are blocked by trust uncertainty. Adding logos of recognizable customers (treatment) will increase signup conversion by at least 15% (X = 15pp lift from current 6% baseline). If true, trust-signaling is a real lever and we should test pricing-page logos next."

**How to catch it.** Can you state the causal theory in one sentence? If not, the experiment will not generalize.

---

## Red Flag 8: Running Experiments Without Pre-Registration

**Symptom.** Test runs for a week. Looks at results. Defines "what counts as success" after seeing the numbers. Reports it as a win.

**Why it's bad.** Post-hoc threshold-setting is p-hacking. Any random data set will have *something* that looks like a win when you choose the metric after looking. Pre-registration (writing down what you'll measure and what threshold counts) eliminates this.

**Bad example:**
> "We ran the test for 10 days. Conversion was flat, but session length went up 8%. We're calling it a win."

**Good example:**
> "Pre-registered: primary = conversion to signup, threshold +15%. Secondary tracked but not decision-making: session length, page-view depth. Result: conversion -2% (not significant), session length +8%. Pre-registered decision: not a win, do not ship."

**How to catch it.** Is the metric + threshold + decision rule written down *before* the test started? If not, you are p-hacking.

---

## Red Flag 9: Treating Statistical Significance as Practical Significance

**Symptom.** A/B test result: variant +0.4% conversion at p<0.05 (statistically significant). Team ships and celebrates.

**Why it's bad.** Statistical significance just means "this result is unlikely under the null." It does not mean the effect is large enough to be worth the engineering cost. A 0.4% lift in conversion may not pay for the maintenance burden of the new code path.

**Bad example:**
> "+0.4%, p<0.05. Ship it."

**Good example:**
> "+0.4%, p<0.05 (statistically significant). Practical significance: 0.4% of 1M monthly users at $40 ARPU = $192K ARR. Engineering cost to ship + maintain: ~$50K/year. Net positive. Ship. But: do not pursue similar 0.4%-lift experiments without first checking expected ROI — most won't clear the bar."

**How to catch it.** Did you compare effect size to maintenance cost? If only the p-value is in the report, the decision is incomplete.

---

## Red Flag 10: Selection Bias in the Test Audience

**Symptom.** Experiment runs on power users (logged in, 30-day-active) and projects results to all users.

**Why it's bad.** Power users behave differently from average users. A feature that wins among power users may fail among casual users. Selection bias produces over-optimistic projections that fail in production rollout.

**Bad example:**
> "Ran beta with our 50 most engaged customers. 80% loved it. Projecting full rollout will see strong adoption."

**Good example:**
> "Ran beta with stratified sample: 20 power users (30-day-active), 20 casual (7-30 day active), 20 lapsed (30-90 day inactive). Adoption: 80%, 35%, 8% respectively. Full rollout will see ~25% blended adoption — adjust expectations and rollout plan."

**How to catch it.** Does your test audience match your target audience? If you tested on a slice, do not project to the whole.

---

## Red Flag 11: Experiment That Cannot Be Stopped (No Kill Switch)

**Symptom.** Test runs hot — engagement drops 15%, error rate climbs — but there is no clear mechanism to halt it. Discussion drags on for days while damage continues.

**Why it's bad.** Every experiment must have a kill switch and a kill criterion. Experiments that cannot be stopped quickly become outages.

**Bad example:**
> A/B test deployed via code. Rollback requires a new deploy. Discussion: "do we kill it?" takes 3 days while error rate stays elevated.

**Good example:**
> A/B test deployed via feature flag with kill criteria: error rate +20% triggers automatic flag-off; manual override available 24/7. Documented kill switch + on-call ownership. Test rolled back within 15 minutes when criterion hit on day 4."

**How to catch it.** Can you turn off this experiment in under 15 minutes without a deploy? If not, you have no kill switch.

---

## Red Flag 12: Treating One Successful Experiment as Strategic Validation

**Symptom.** One A/B test confirms a smaller change works. Team uses this as evidence to commit to a 6-month strategic bet.

**Why it's bad.** Tactical experiments validate tactical hypotheses. They do not validate strategic theses. A button-color win does not validate the product direction. The team is over-claiming the scope of validation.

**Bad example:**
> "Our 'Try Free' button A/B test showed +12% conversion. This validates our self-serve strategy."

**Good example:**
> "Our 'Try Free' button A/B test showed +12% conversion. This validates one tactical change on one page. The self-serve strategy requires separate validation: PMF signal in the self-serve segment, retention, expansion, support load. Separate experiments planned."

**How to catch it.** What is the scope of your validation? If it is a tactical change, do not claim strategic validation.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Confirmation-Biased Design | Is there a result that would kill the idea? |
| 2 | Opinions Instead of Behavior | Does the result come from what people do? |
| 3 | Sample Too Small | Pre-declared minimum n? Stopping rule? |
| 4 | Mixing Variables | Only 1 variable changed in variant? |
| 5 | Pretotype Took Too Long | Idea-to-live in under 1 week? |
| 6 | No Counter-Metric | Pre-declared counter-metric tracked? |
| 7 | Hypothesis Without Why | Causal theory in one sentence? |
| 8 | No Pre-Registration | Metric + threshold + decision rule written before test? |
| 9 | Statistical Not Practical | Effect size compared to maintenance cost? |
| 10 | Selection Bias | Test audience matches target audience? |
| 11 | No Kill Switch | Can you turn off in 15 min without deploy? |
| 12 | Tactical as Strategic | Scope of validation matches scope of claim? |

## Related Reading

- SKILL.md Troubleshooting section (for symptom -> root cause -> resolution)
- references/xyz-hypothesis.md (for the XYZ format, if present)
- identify-assumptions/references/red-flags.md (for assumption-prioritization patterns)
- activation-funnel/references/red-flags.md (for metric counter-metric patterns)
