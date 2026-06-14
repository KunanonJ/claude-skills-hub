# Red Flags: Feature Flag Strategy

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan the rollout plan and flag inventory before opening any ramp stage. Each red flag shows the *bad* version next to the *good* version, anchored to Martin Fowler's flag taxonomy (release / experiment / ops / permission) and standard rollout shapes.

---

## Red Flag 1: Zombie flags (flag debt)

**Symptom.** Flag inventory has 200+ live flags. Search for flags last toggled > 90 days ago returns 140 results.

**Why it's bad.** Every live flag is technical debt. Test matrices grow combinatorially. Code branches diverge. Mystery behaviors appear when two flags interact unexpectedly. A team shipping 20 features/quarter without retirement discipline accumulates 80+ dead flags per year.

**Bad example:**
> "Flag inventory (audit Mar 2026): 217 live flags. Of those: 88 at 100% for > 60 days (release toggles that should have been retired); 24 at 0% for > 90 days (dead experiments); 31 not toggled in > 180 days (mystery)."

**Good example:**
> "Flag governance:
> • New flag creation requires a retirement date.
> • Quarterly audit: any release/experiment flag aged > 90 days surfaces in the report.
> • Retirement PR is a normal sprint task, not a periodic cleanup.
> • Flag count trend reported monthly; goal is stable or declining.
> Current state: 47 live flags, 19 retired this quarter, net -3."

**How to catch it.** Run a flag inventory. Count flags older than 90 days that are not Ops or Permission type. > 10% of total = debt is accumulating.

---

## Red Flag 2: No kill-switch criteria

**Symptom.** Rollout plan describes the ramp shape but does not say at what error rate or customer-impact threshold the team flips the kill-switch.

**Why it's bad.** Without pre-agreed thresholds, kill-switch decisions are made in the heat of incident — usually too slowly. The on-call hesitates because "is this bad enough?" Customers experience the bug for an extra 20 minutes while leadership debates.

**Bad example:**
> "Rollout plan: 'Monitor metrics during rollout. If anything looks wrong, contact PM to discuss next steps.'"

**Good example:**
> "Kill-switch criteria (pre-agreed, in rollout plan):
> • Error rate > 0.5% sustained 5 min on flagged surface OR
> • p95 latency > 2x baseline for 10 min OR
> • >= 3 independent paid-customer reports of same issue OR
> • Major-customer-blocked event.
> Authority: on-call engineer flips without escalation; logs to #incidents; PM and Eng Lead notified by automation. Flag stays off until root cause + fix; re-ramp from 0%."

**How to catch it.** Read the rollout plan. Search for numbers and "threshold". If none, the kill-switch is improvised.

---

## Red Flag 3: Release toggle treated as permanent

**Symptom.** Flag `web__new_checkout__v2` was created for the new-checkout launch in 2024. Still in the codebase 18 months later, still at 100%. Now functionally a permission gate.

**Why it's bad.** Fowler's taxonomy: release toggles are temporary; permission toggles are permanent. Conflating them means the codebase carries dead branches forever; the test matrix is bloated; the next refactor stumbles into a "flag" that nobody owns.

**Bad example:**
> "`web__new_checkout__v2` at 100% since Sept 2024. Not retired. New engineer asks: 'do I need to test both branches?' Nobody knows."

**Good example:**
> "Quarterly audit Q1: `web__new_checkout__v2` at 100% for 18 months. Retired. PR removes both code branches (`if (flag.new_checkout_v2) { newPath() } else { oldPath() }` → `newPath()` only). Config entry deleted. Documentation updated. Final state archived to flag-retirement log: 'created 2024-09, retired 2026-03, owned by checkout team, controlled the new checkout flow which is now the only flow'."

**How to catch it.** For each flag at 100% for > 30 days, ask: "is this a permanent permission gate or an unretired release toggle?" If the latter, retire.

---

## Red Flag 4: Flag flipped without metric gates

**Symptom.** Engineer thinks "looks good, let's go to 25%". Flips the flag. No metric was the gate.

**Why it's bad.** Without metric gates, advancement is intuition. Sometimes intuition is right. Often it isn't. Production reveals a 3-percentage-point conversion drop two days after a 25% ramp because nobody was watching the right number.

**Bad example:**
> "Ramp log: '5% → 25% on Tuesday. Eng team felt good about the data. No specific metric check.'"

**Good example:**
> "Ramp gates (pre-agreed in rollout plan):
> Stage → Gate metric to advance:
> • 1% → 5%: no crashes for 24h; eval acceptance >= baseline.
> • 5% → 25%: conversion rate within 95% CI of control for 72h; error rate < baseline + 0.2%; p95 latency within +10% of baseline.
> • 25% → 50%: above metrics held for 5 days; no top-tier-customer incident.
> • 50% → 100%: above held for 7 days; positive cohort retention signal.
> Advancement decision: owner reviews the dashboard at the gate; documents pass/fail with the metric values."

**How to catch it.** Read the rollout plan. For each advancement, is the gate metric named? If not, advancement is by feel.

---

## Red Flag 5: Mobile flag without version gate

**Symptom.** Mobile feature flag flipped at 100%. App on old client version crashes because the feature requires a server response the old client cannot parse.

**Why it's bad.** Mobile clients have long-tail version distribution. ~30% of users may be on a client version > 60 days old on launch day. A flag flip without a minimum-client-version check breaks those users immediately, with no recovery until they update.

**Bad example:**
> "Flag `mobile__new_search` flipped to 100%. Day 1: crash reports from iOS 12.4 (released 3 months ago). 8% of MAU stuck on a broken app."

**Good example:**
> "Flag `mobile__new_search` configured with prerequisite: client_version >= 14.2 (released 2026-02-14, 95% adoption confirmed via app analytics). Flag returns false for older clients; old behavior persists. Older clients receive an in-app upgrade prompt. Plan: full rollout after >= 98% adoption of 14.2."

**How to catch it.** For every mobile flag, ask: "what is the minimum client version that supports the new behavior?" If unanswered, the flag is unsafe.

---

## Red Flag 6: Permissions too loose on critical flag

**Symptom.** Anyone with engineer access can flip the billing-related kill-switch. One engineer accidentally toggles it during routine work.

**Why it's bad.** Critical-surface flags (billing, auth, data deletion) need two-person rules. Loose permissions plus a single typo in the flag UI equals a self-inflicted incident.

**Bad example:**
> "`billing__new_card_flow` flag. Permissions: all engineering. One engineer toggles it from 50% to 0% by mistake during a separate task. 2 hours of revenue lost; 47 stuck transactions."

**Good example:**
> "`billing__new_card_flow` permissions: two-person rule. Toggle requires one engineer to propose + a second to approve in the flag service before the change takes effect. Authority limited to billing team + on-call rota. Audit log emails the team channel on every change. High-tier flags (billing, auth, account-deletion, data-export) all gated this way."

**How to catch it.** List the team's high-tier flags (billing, auth, etc.). For each, check who has flip authority. If > 5 people without two-person rule, permissions are loose.

---

## Red Flag 7: Holdout killed when experiment "shipped"

**Symptom.** An A/B test concludes; the team rolls the winner to 100%; the holdout group is also exposed because "the experiment is over".

**Why it's bad.** Holdouts are valuable post-launch — they let the team measure long-term lift. Killing the holdout at launch means losing 30-90 days of lift attribution data. Long-term cohort retention impacts become invisible.

**Bad example:**
> "Experiment concludes; variant wins +8% conversion. Roll to 100%, including the 5% holdout. Quarter later: cannot answer 'what was the long-term retention impact?'"

**Good example:**
> "Experiment design includes a short-term and long-term holdout:
> • Short-term: powers the experiment readout (consumed at conclusion).
> • Long-term: 5% holdout maintained for 90 days post-launch to measure retention lift.
> Holdout retirement is a separate decision after long-term measurement. Re-exposure of the holdout group is planned (likely with a small conversion event when finally exposed) and documented."

**How to catch it.** Open any experiment's design doc. Is there a long-term holdout policy? If not, the team will lose post-launch measurement.

---

## Red Flag 8: Flag name doesn't follow conventions

**Symptom.** Flag inventory includes `johnsTest`, `featureV3final`, `tryNewWay`. Six months later, nobody knows what they do.

**Why it's bad.** Flag names are read more often than written. Non-conventional names (camelCase, personal names, version suffixes without context) become unfindable in audits. Searching for "all checkout flags on web" returns nothing because nobody can match the pattern.

**Bad example:**
> "Flag names: `newCheckout`, `johnsExperiment`, `featureA`, `testFlag2`, `final_v3_v2_real`."

**Good example:**
> "Naming convention: `<scope>__<feature>__<purpose>__<version>`.
> Examples:
> • `web__checkout__new_flow__v2` (release toggle, web)
> • `api__search__relevance__experiment_q3` (experiment, API)
> • `infra__search__circuit_breaker` (ops, permanent)
> • `product__enterprise_admin__permission` (permission, permanent)
> Enforced via PR review checklist. CI lints flag names against the regex."

**How to catch it.** Open the flag inventory. Filter for names not matching `<scope>__<feature>__<purpose>__<version>`. If > 10%, the convention is unenforced.

---

## Red Flag 9: Flag dependency chains > 2 levels deep

**Symptom.** Flag A depends on flag B depends on flag C depends on flag D. The team cannot answer "what is the user experience when only A is enabled?"

**Why it's bad.** Each level of dependency multiplies the combinatorial test matrix. Beyond 2-3 levels, the team cannot reason about interactions. Mystery bugs appear when flags interact in ways nobody modeled.

**Bad example:**
> "Flag dependency graph:
> ai_chatbot → ai_chatbot_v2 → ai_chatbot_v2_premium → ai_chatbot_v2_premium_streaming → ai_chatbot_v2_premium_streaming_eu
> (Test matrix: 32 combinations. Tested: 4.)"

**Good example:**
> "Flag dependency rule: max 2 levels.
> If the natural design requires deeper chains, flatten:
> • Parent flag: `ai_chatbot_v2_full` (rolls the whole feature).
> • Child variation flags: `ai_chatbot_v2_streaming_enabled`, `ai_chatbot_v2_eu_compliance`, all flat children of the parent.
> Test matrix: parent x 2-3 children = 6-12 combos, manageable. Document the design."

**How to catch it.** Map your flag dependencies. Any chain > 2 levels = flatten before the next ramp.

---

## Red Flag 10: Rollback requires code revert

**Symptom.** Production incident. To roll back the feature, engineering must merge a revert PR and deploy. 45 minutes elapsed.

**Why it's bad.** A flag whose rollback path is a code revert defeats the purpose of having a flag. Real rollback is a single config change, in < 60 seconds. If the team has to deploy to roll back, they will hesitate, and customers experience extended impact.

**Bad example:**
> "Incident timeline: error spike at 14:02. Decision to rollback at 14:08. PR opened at 14:11; review at 14:18; merge at 14:24; deploy completes at 14:47. 45-minute customer impact."

**Good example:**
> "Incident timeline: error spike at 14:02. Decision to flip kill-switch at 14:05. On-call flips flag in LaunchDarkly UI at 14:06. Error rate normalizes at 14:08. 6-minute customer impact. Post-incident analysis happens at leisure; the kill-switch did its job."

**How to catch it.** Drill the rollback in non-production once per quarter. Time it. If > 5 minutes, the kill-switch is broken.

---

## Red Flag 11: Owner has left the company

**Symptom.** Flag `web__feature_x` exists in production. Audit asks "who owns this?" Owner field: Jane Doe. Jane Doe left 8 months ago.

**Why it's bad.** Ownership by individual is brittle. People leave. Flags persist. An unowned flag has no champion for retirement, no on-call escalation path, and accumulates dust until it causes an incident.

**Bad example:**
> "Flag `web__feature_x`: owner Jane Doe (terminated 2025-09). No re-assignment. Flag at 100% for 14 months."

**Good example:**
> "Ownership policy: flags owned by team, not individual. Field captures `owning_team`: 'checkout-team'. Onboarding for new team members includes a 30-min flag review for the team. Quarterly: orphaned flags (team disbanded / re-org) get auto-assigned to the engineering management team for triage."

**How to catch it.** Audit owner field across all flags. Cross-reference with current employee list. Orphans = re-assign to team.

---

## Red Flag 12: No metric validated before 100% ramp

**Symptom.** Flag ramped 1% → 5% → 25% → 100% on schedule. No metric was actually validated at any stage. Team realizes at 100% that activation dropped 4 points.

**Why it's bad.** Ramping is supposed to *reveal* problems at low blast radius. If the team does not look at the data at each stage, the ramp is decoration — the same blast radius as a big-bang launch, but with extra steps.

**Bad example:**
> "Ramp log: 'May 1: 1%. May 3: 5%. May 6: 25%. May 13: 100%.' Owner: 'we were busy with other things, didn't look at the dashboard.'"

**Good example:**
> "Ramp gate validation: at each stage, owner posts in #rollout-channel: 'Stage: 25%. Window: 72h. Metrics: conversion 4.1% vs control 4.0% (within CI); error rate 0.03% vs 0.04%; p95 latency 412ms vs 405ms (within 10%). Decision: ADVANCE.' Asynchronous review by Eng Lead before advancing. Documented for the launch retro."

**How to catch it.** Read the ramp log. For each stage, are metrics posted? If no, the gates were not enforced.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Zombie flags | What % of release/experiment flags are aged > 90 days? |
| 2 | No kill-switch criteria | Are thresholds (error %, latency, customer count) named? |
| 3 | Release toggle treated as permanent | Any release flag at 100% > 30 days unretired? |
| 4 | Flag flipped without metric gates | At each advancement, what number was the gate? |
| 5 | Mobile flag without version gate | What minimum client version supports the new behavior? |
| 6 | Loose permissions on critical flag | Two-person rule on billing/auth/data flags? |
| 7 | Holdout killed when experiment "shipped" | Is there a long-term (90d+) holdout post-launch? |
| 8 | Flag name doesn't follow conventions | Match against `<scope>__<feature>__<purpose>__<version>` |
| 9 | Dependency chains > 2 levels | Map dependencies; flatten if > 2 deep |
| 10 | Rollback requires code revert | Drill the kill-switch; > 5 min? |
| 11 | Owner has left the company | Cross-reference owner field with employee list |
| 12 | No metric validated before 100% | At each stage, were metrics posted? |

## Related Reading

- SKILL.md Troubleshooting
- references/fowler-feature-toggle-taxonomy-guide.md
- references/rollout-shape-comparison-guide.md
- Martin Fowler, "Feature Toggles" essay
- `launch-playbook/` (the rollout plan is part of the broader launch)
- `ai-feature-prd/` (AI deployment ramps use this skill)
- `pricing-prd/` (pricing rollouts use this skill)
- `eol-communication/` (reverse-ramp Shape F)
