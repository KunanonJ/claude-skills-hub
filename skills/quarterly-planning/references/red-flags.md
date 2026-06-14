# Red Flags: Quarterly Planning

> Common ways this skill's output goes wrong -- concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan before publishing the quarterly plan (kick-off deck, OKR doc, capacity model, mid-Q check-in, close-out retro). Each red flag is paired with bad and good examples.

---

## Red Flag 1: OKR Theater

**Symptom.** Each team writes OKRs in a vacuum, presents them at kick-off, and never references them again until close-out.
**Why it's bad.** OKRs are a coordination mechanism, not a ritual. If teams do not reference them weekly to make trade-offs, they become a parallel-track artifact -- the work that actually happens has no relation to the OKRs that were written. By close-out, scores are rationalized post-hoc.
**Bad example:**
> "OKRs were set in the Q kick-off in January. Mid-quarter check-in canceled because of release crunch. Close-out: 3/4 KRs scored 0.7+."
**Good example:**
> "OKRs reviewed in every weekly leadership sync (15 min). Mid-Q check-in surfaced that KR2 was off-track due to staffing; team explicitly re-baselined to 0.5-of-0.7 and documented the trade-off. Close-out scores match what we tracked weekly -- no surprises."
**How to catch it.** OKRs not referenced in any weekly artifact during the quarter = theater.

---

## Red Flag 2: Capacity Planned in Story Points, Reality Lived in Calendar Days

**Symptom.** "Engineering has 240 story points of capacity this quarter" -- but the team has not calibrated story points to time, and PTO / on-call / interview load are not subtracted.
**Why it's bad.** Story points are a relative-sizing tool, not a capacity-planning tool. Treating them as if they convert to days produces a fiction. Teams over-commit, slip, and learn to distrust planning.
**Bad example:**
> "Team A: 240 points capacity, committing to 240 points of work."
**Good example:**
> "Team A: 12 ICs x 60 working days = 720 IC-days. Subtract on-call (60), PTO (90), interviews (30), required maintenance (90) = 450 productive IC-days. Allocate 70% to OKR work (315 days), 20% to keep-the-lights-on (90 days), 10% buffer (45 days). Convert to ~22 story-points of OKR work at our calibrated 14 IC-days / point."
**How to catch it.** No documented PTO / on-call subtraction = capacity model is fiction.

---

## Red Flag 3: Planning Poker for Capacity

**Symptom.** "Each team voted on how many initiatives they could take. Average is 4." -- treating capacity as a democratic vote rather than a calculation.
**Why it's bad.** Planning poker is calibrated to relative effort comparisons, not to absolute capacity. When asked "how many initiatives can you ship?", engineers anchor on past quarters (which were over-committed) and the group converges on a number that is wrong in the same direction.
**Bad example:**
> "We polled all 6 teams: each said they could take 4 large initiatives this quarter. So 24 initiatives in the slate."
**Good example:**
> "Capacity model in `capacity-q2.xlsx` per team: each team has 450 productive IC-days. Average initiative size (calibrated against last 4 quarters): 90 IC-days. So 5 initiatives per team, ~30 in the slate. Then we cut 25% buffer = 22 in the committed slate."
**How to catch it.** Capacity expressed only as integer initiative counts with no IC-day basis.

---

## Red Flag 4: Kickoff Without Last Quarter's Retro

**Symptom.** New quarter kicks off Monday. Previous quarter never had a structured retrospective.
**Why it's bad.** Quarterly planning compounds knowledge. Without a retro, every team makes the same estimation mistakes, takes on the same dependencies, and misses the same external constraints. The org loses 4x learning velocity.
**Bad example:**
> "Q1 over Friday. Q2 kickoff Monday. No retro -- 'we already know what went wrong'."
**Good example:**
> "Q1 retro Tue / Wed of week 1 of Q2. Three artifacts: (1) what we got wrong about capacity, (2) which dependencies blew up, (3) which OKRs we should never have written. Outputs explicitly feed Q2 planning -- 'we will not write 'launch X' as a KR again; KRs are outcome-based'."
**How to catch it.** Kickoff date earlier than retro date = retro is missing.

---

## Red Flag 5: Stretch Goals as Committed Slate

**Symptom.** "We aim high" -- every KR is set at an aspirational level (Google-style "0.6-0.7 = great"), but the slate is committed and execs expect all KRs to hit 1.0.
**Why it's bad.** Mixing aspirational and committed goals is a category error. If execs expect 1.0, the team writes safe goals (and innovation drops). If the team writes aspirational goals, execs treat misses as failure. Pick one or split explicitly.
**Bad example:**
> "Q2 OKRs are stretch. (Side conversation with CEO: 'I expect all green at close.')"
**Good example:**
> "Q2 has two OKR tiers, explicit. Committed: 4 KRs at 1.0 expectation, scored as deliver / miss. Aspirational: 3 KRs at 0.7 expectation, scored on a 0-1 scale. Compensation review only references committed."
**How to catch it.** OKR doc has one tier + side-conversation expectations = split into two tiers.

---

## Red Flag 6: Quarter as a Container for All Strategic Work

**Symptom.** Everything strategic in the company gets squeezed into a 90-day OKR.
**Why it's bad.** Some work has a natural cadence of 18-36 months (platform rewrites, regulatory programs, new market entry). Forcing it into a 90-day OKR produces fake milestones ("KR: ship phase 1") that do not represent customer-visible outcomes.
**Bad example:**
> "KR: Complete phase 1 of the multi-region platform rewrite (year-long program)."
**Good example:**
> "Multi-region rewrite is tracked as a *program* on a separate dashboard with quarterly milestones and an annual budget. The Q2 OKR slate has one KR derived from the program ('99.95% availability in EU region, measured from June 1') -- a quarter-bounded outcome, not a phase."
**How to catch it.** KR uses words like "phase 1", "milestone X", "kick off Y" = wrong artifact.

---

## Red Flag 7: KRs That Are Activities, Not Outcomes

**Symptom.** "KR: ship the new pricing page" -- the KR is a deliverable, not a measurable change in the world.
**Why it's bad.** Activity-based KRs let the team ship and feel successful even if the shipped thing did nothing. Outcome KRs ("free-to-paid conversion at 4.5% in June") force the team to confront whether the shipped thing worked.
**Bad example:**
> "KR: launch new pricing page by June 1."
**Good example:**
> "KR: free-to-paid conversion >= 4.5% across all paid plans by June 30, measured from Q2-cohort signups. (Pricing-page redesign is the *bet* we are making on this KR, not the KR itself.)"
**How to catch it.** KR contains a verb of delivery (ship, launch, build, complete) without a downstream metric = rewrite.

---

## Red Flag 8: Cross-Team Dependencies Discovered Mid-Quarter

**Symptom.** Team A planned an initiative that needs Team B's API. Team B did not include that work in their slate. Discovered week 6.
**Why it's bad.** Mid-quarter dependency discovery is the leading cause of slippage. By week 6 there is no slack to absorb it, and one team's slip cascades into 2-3 others.
**Bad example:**
> "Team A blocked on Team B API in week 6. Team B's capacity now reallocated; their own KR3 slips."
**Good example:**
> "Pre-kickoff: every team listed initiatives + dependencies in `q2-dependencies.json`. Cross-team session week 0 reconciled 14 dependencies. 3 dependencies resulted in scope cuts (Team A descoped Initiative X because Team B could not commit). Week 6: zero new cross-team dependencies discovered."
**How to catch it.** No documented dependency-reconciliation session in week 0 = mid-Q surprises guaranteed.

---

## Red Flag 9: 14 KRs Per Team

**Symptom.** "We have 14 KRs to be comprehensive."
**Why it's bad.** Doerr's original guidance is 3-5 objectives, 3-5 KRs each, max. Beyond that, attention diffuses and *nothing* is prioritized. Teams with 14 KRs ship the easy ones and rationalize away the hard ones at close.
**Bad example:**
> "Team A Q2: O1 (3 KRs), O2 (4 KRs), O3 (3 KRs), O4 (4 KRs). 14 KRs total."
**Good example:**
> "Team A Q2: 2 objectives, 3 KRs each. 6 KRs total. Remaining work is keep-the-lights-on (tracked separately, not OKR-bound) or moved to Q3."
**How to catch it.** KR count per team > 7 = collapse or defer.

---

## Red Flag 10: Mid-Q Check-In Without Rebaselining Authority

**Symptom.** Mid-quarter check-in identifies that KR2 is off-track, but the team is told to "just push harder", with no authority to descope.
**Why it's bad.** The check-in's purpose is to surface trade-offs while there is still time to make them. Without rebaselining authority, the check-in is reduced to a status meeting and the org loses the chance to redirect.
**Bad example:**
> "Mid-Q: KR2 off-track. 'Catch up by quarter-end.' (No descope, no scope swap.)"
**Good example:**
> "Mid-Q: KR2 off-track. Three options presented: (a) descope KR2 from 5000 -> 3000 users, (b) borrow 60 IC-days from Team B who is ahead on their KR1, (c) drop KR3 to free capacity. Decision documented: option (a), CEO signs off."
**How to catch it.** Mid-Q outputs no rebaseline decisions = it was status, not planning.

---

## Red Flag 11: Quarterly Plan With No Bet Framing

**Symptom.** The plan lists what teams will do but never says *what we expect to learn* or *what could be wrong*.
**Why it's bad.** A quarterly plan is a portfolio of bets. Skipping the "what could be wrong" step means the team executes confidently on assumptions that may be false, and discovers the failure only at close-out.
**Bad example:**
> "Q2 plan: ship X, Y, Z, hit OKRs."
**Good example:**
> "Q2 plan with 5 explicit bets: (1) 'pricing redesign moves conversion from 3.2% to 4.5%' -- could be wrong if elasticity is lower than estimated; (2) 'enterprise tier launches with 8 design partners' -- could be wrong if procurement cycles are > 90 days. Each bet has a hypothesis, a tripwire, and a documented owner."
**How to catch it.** Plan does not list assumptions and tripwires = run the `pre-mortem` skill before publishing.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | OKR theater | OKRs referenced in any weekly artifact during Q? |
| 2 | Capacity in story points only | PTO / on-call / interviews subtracted? |
| 3 | Planning poker for capacity | Capacity grounded in IC-days? |
| 4 | Kickoff before last retro | Retro date < kickoff date? |
| 5 | Stretch vs committed mixed | Two tiers, explicitly labeled? |
| 6 | Multi-year work in 90-day KR | KR has "phase X" / "kick off"? |
| 7 | KRs as activities | Verb of delivery without downstream metric? |
| 8 | Dependencies discovered mid-Q | Week-0 reconciliation session held? |
| 9 | 14 KRs per team | KR count > 7 per team? |
| 10 | Check-in without rebaseline | Mid-Q outputs include scope swap / descope? |
| 11 | No bet framing | Plan lists assumptions and tripwires? |

## Related Reading

- `SKILL.md` -- the kickoff -> mid-Q -> close-out cycle
- `references/okr-patterns.md` -- OKR writing patterns
- Sibling skill: `execution/brainstorm-okrs/` -- generate candidate OKRs
- Sibling skill: `execution/prioritization-frameworks/` -- rank initiatives within the slate
- Sibling skill: `execution/dependency-map/` -- week-0 dependency reconciliation
- Sibling skill: `discovery/pre-mortem/` -- bet framing and tripwires
- Sibling skill: `sprint-retrospective/` -- quarter retro patterns
