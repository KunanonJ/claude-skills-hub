# Red Flags: Brainstorm Ideas

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them. Pair with the SKILL.md and Troubleshooting table.

## How to use this document

When you have just finished an ideation session, scan the red flags below before publishing the idea list or moving to prioritization. Each red flag shows a *bad* and *good* version.

---

## Red Flag 1: Ideation Theater (15 Ideas, 1 Used)

**Symptom.** The session produced 15 ideas across PM/Designer/Engineer perspectives. Two weeks later, the team is building the idea the PM walked in with.

**Why it's bad.** Ideation theater wastes the team's time and undermines trust in the discovery process. If the decision was pre-made, the workshop was just performance. The Product Trio approach exists to *change the decision*, not to ratify it.

**Bad example:**
> "We ran a great ideation session — 15 ideas! Decided to go with the one the PM had originally proposed."

**Good example:**
> "Ideation produced 15 ideas. After Opportunity Solution Tree scoring, top 3 candidates: A (PM's original), B (Designer-originated), C (Engineer-originated). Trio voted 2-1 for B based on confidence-of-evidence. PM dissent recorded; we'll experiment with B and revisit if data calls for A."

**How to catch it.** Did the chosen idea originate from one perspective or did the session genuinely change the selection? If the PM's idea won every time across multiple sessions, the process is theater.

---

## Red Flag 2: HiPPO Override (Highest Paid Person's Opinion Wins)

**Symptom.** Ideation produces 12 ideas; the VP or executive shows up at the end and picks their favorite, overriding the team's evidence-based ranking.

**Why it's bad.** HiPPO override defeats the purpose of involving the trio. The team learns that opinion outranks evidence, stops contributing real ideas, and starts predicting what the HiPPO wants. Continuous discovery dies.

**Bad example:**
> Trio recommends Idea B based on customer evidence. VP attends review, picks Idea D ("I have a hunch"). Build proceeds on D.

**Good example:**
> Trio recommends B. VP disagrees, prefers D. Resolution: VP signs a "VP override" note documenting their reasoning, success criteria, and a check-back date. If D fails, the override is reviewed. The team's recommendation stays in the record as the dissenting view."

**How to catch it.** When an executive overrides the team, is the override documented with criteria? If not, accountability evaporates.

---

## Red Flag 3: Ideas Are Just Features, Not Solutions to Opportunities

**Symptom.** Ideation produces a feature list ("dark mode, AI assistant, calendar integration") with no connection to a customer opportunity or outcome.

**Why it's bad.** Torres' Opportunity Solution Tree requires solutions to be *anchored* to a named opportunity, which is anchored to a desired outcome. Disconnected feature lists are wish lists; they ship, get adoption, and do not move the metric.

**Bad example:**
> Idea list: 1. Dark mode. 2. AI assistant. 3. Calendar sync. 4. Slack notifications. 5. Mobile app.

**Good example:**
> Outcome: increase weekly active usage 20%. Opportunity: 'Users forget to come back during workday.' Solutions: (a) calendar-based reminders, (b) Slack daily digest, (c) browser extension. Each idea scored on impact-to-opportunity, not generic appeal.

**How to catch it.** For each idea, can you name the opportunity it addresses? If multiple ideas address the same opportunity, that is healthy. If you cannot connect an idea to an opportunity, it is freelancing.

---

## Red Flag 4: Single-Perspective Ideation (Only PM Voice)

**Symptom.** Brainstorm includes PM only, or PM + Designer but no Engineer. Ideas are biased toward what PM-thinking considers possible.

**Why it's bad.** Product Trio exists because each perspective surfaces different ideas. Engineers see leverage in existing platform capability. Designers see flows and interaction patterns. PMs see customer evidence and business levers. Missing one perspective produces a flat, narrower idea set.

**Bad example:**
> Brainstorm: PM solo. 14 ideas, all customer-facing features. No leverage of existing infrastructure surfaced.

**Good example:**
> Brainstorm: PM, designer, engineer. 15 ideas. Eng surfaced 'enable the existing event-stream for this use case — 3 days of work, unlocks 3 use cases'. PM never would have thought of it."

**How to catch it.** Was the full trio present? If not, the idea set is incomplete.

---

## Red Flag 5: Ideating Before the Problem Space Is Framed

**Symptom.** "Let's brainstorm" — no clear target outcome, no defined segment, no constraints. Ideas range from a chrome extension to a B2B integration to a re-onboarding flow.

**Why it's bad.** Unframed ideation is fast but produces unranked, incomparable ideas. The Phase 1 framing in the SKILL.md (outcome, segment, constraints) exists because ideas are only useful relative to a frame. Skipping framing is how teams produce 20 ideas none of which can be compared.

**Bad example:**
> Workshop opens: "Today we'll brainstorm ideas for the product." 90 minutes of suggestions.

**Good example:**
> Workshop opens: "Outcome: reduce time-to-first-value from 12 min to 4 min. Segment: SMB self-serve trials in week 1. Constraints: $0 infra spend, 6 engineer-weeks. Generate ideas under this frame."

**How to catch it.** Is the frame written on the wall before ideation starts? If not, you are about to produce unrankable ideas.

---

## Red Flag 6: SCAMPER as Performance, Not Catalyst

**Symptom.** Team mechanically goes through each SCAMPER letter (Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse) for every concept, producing 49 cells of mediocre output.

**Why it's bad.** SCAMPER is a *catalyst* — apply selectively to break thinking patterns when stuck. Mechanically applying every letter to every concept produces volume, not insight, and trains the team to value process over outcome.

**Bad example:**
> "We applied SCAMPER to our onboarding. 7 letters x 5 stages = 35 ideas listed."

**Good example:**
> "We were stuck after generating 8 standard ideas. Applied 'Eliminate' specifically: what if we removed the entire setup wizard? Surfaced 2 strong ideas (defer setup until first use; pre-populate with sample data). 'Substitute' did not generate anything useful, skipped."

**How to catch it.** SCAMPER cells with no real insight should be empty, not filled with filler.

---

## Red Flag 7: Voting Before Evidence

**Symptom.** Team votes on ideas using dots or rankings before discussing customer evidence. Most-voted idea wins.

**Why it's bad.** Voting without evidence is opinion aggregation, not discovery. The Opportunity Solution Tree exists to anchor decisions to evidence. Voting first lets the most charismatic advocate win regardless of customer signal.

**Bad example:**
> "Dot vote on the 15 ideas. Idea D won with 7 dots. Building D."

**Good example:**
> "For each idea, name the customer evidence that suggests it would work. Idea D: 'Sounds good in meetings, no interview quotes support it.' Idea B: '3 interviews surfaced this exact need.' B advances to experiment design despite D having more emotional appeal."

**How to catch it.** When you ranked ideas, did you list evidence for each? If not, you ranked on vibes.

---

## Red Flag 8: How Might We (HMW) at Wrong Altitude

**Symptom.** HMW is either too narrow ("How might we change the button color?") or too broad ("How might we delight users?"). Either way, ideation under it is constrained or unfocused.

**Why it's bad.** HMW altitude controls ideation scope. Too narrow = micro-tweaks only. Too broad = unrankable ideas. The right altitude opens 5-15 distinct solution directions.

**Bad example:**
> HMW: "How might we use AI?" (Too broad — produces grab-bag of AI features.) Or: "How might we change the upgrade button copy?" (Too narrow — only produces variations of one tactic.)

**Good example:**
> HMW: "How might we help SMB users reach the activation moment within 5 minutes of signup?" Specific enough to constrain, broad enough to admit multiple solution approaches.

**How to catch it.** Does the HMW open 5-15 genuinely different solution directions? If fewer, narrow scope; if too many, raise altitude.

---

## Red Flag 9: No Confidence Score on Ideas

**Symptom.** Idea list has impact estimates but no measure of how confident the team is in those estimates.

**Why it's bad.** Two ideas with equal impact estimates may have very different confidence levels — one based on customer interviews, the other on a single team member's hunch. Confidence is a separate dimension that affects sequencing.

**Bad example:**
> "Idea A: high impact. Idea B: high impact. Both high impact, pick either."

**Good example:**
> "Idea A: high impact, high confidence (3 customer interviews, market data). Idea B: high impact, low confidence (one stakeholder hunch). Sequence: build A first; design experiment to raise confidence on B before building."

**How to catch it.** Does each idea have a confidence score (or evidence column)? If not, you cannot distinguish proven bets from hunches.

---

## Red Flag 10: Ideating Without Constraints

**Symptom.** "What's the best thing we could build?" — no budget, no timeline, no platform constraints. Ideas include "a fully autonomous AI agent" alongside "a button color change."

**Why it's bad.** Unconstrained ideation is sci-fi creative writing. Constraints are not limitations on creativity; they are the structure that produces buildable ideas. Skipping constraints produces a list mostly composed of ideas the team cannot ship.

**Bad example:**
> Open prompt: "Best ideas for next year?" Output mixes 6-month features with 5-year moonshots.

**Good example:**
> Constraints declared: 1 quarter timeline, current platform, 3-engineer team. Ideas that violate constraints are tagged "out of scope, parked for separate planning."

**How to catch it.** Are constraints written down before ideation? If not, parts of the output will be unbuildable.

---

## Red Flag 11: Mistaking Quantity for Quality

**Symptom.** Team measures the brainstorm by idea count. "We generated 47 ideas!" is celebrated; whether any are good is unexamined.

**Why it's bad.** Quantity is a proxy for divergent thinking, but it does not guarantee quality. 47 ideas where 40 are slight variations is worse than 12 ideas spanning genuinely different approaches.

**Bad example:**
> "Great session: 47 ideas." (38 of them are minor variations of 'add a tooltip to X'.)

**Good example:**
> "12 ideas spanning 5 distinct approaches: feature additions (3), removals (2), workflow changes (3), platform reuse (2), partner integrations (2). Each approach has at least one strong candidate."

**How to catch it.** Cluster the ideas by approach. If most ideas fall in one cluster, divergence was insufficient.

---

## Red Flag 12: Ideas with No Owner for the Next Step

**Symptom.** Workshop ends. The 15 ideas live on a Miro board. Two weeks later, no one has done anything with them. By week 4, they are forgotten.

**Why it's bad.** The output of ideation is *not the ideas* — it is the next steps. Without an owner for each candidate idea (or the top N), ideation is a feel-good session that produces no action.

**Bad example:**
> "Workshop done. 15 ideas captured. Will follow up." (Two months later, no follow-up.)

**Good example:**
> "Workshop output: top 3 ideas. Owner per idea: PM (idea A) will design a smoke test by Friday; designer (idea B) will prototype by next sprint; engineer (idea C) will spike feasibility by week 3. Review meeting in 4 weeks."

**How to catch it.** Each surviving idea must have an owner and a next step. If the doc ends with "we'll figure it out", the workshop fizzled.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Ideation Theater | Did the chosen idea differ from the PM's pre-walk-in idea? |
| 2 | HiPPO Override | When overridden, is the override documented with criteria? |
| 3 | Ideas Are Just Features | Each idea anchored to a named opportunity? |
| 4 | Single-Perspective | Full PM + Designer + Engineer trio present? |
| 5 | No Framing | Outcome + segment + constraints written before ideation? |
| 6 | SCAMPER as Performance | SCAMPER cells with no insight left empty? |
| 7 | Voting Before Evidence | Evidence listed per idea before voting? |
| 8 | HMW Wrong Altitude | Does HMW open 5-15 distinct solution directions? |
| 9 | No Confidence Score | Each idea has impact AND confidence? |
| 10 | Unconstrained | Constraints declared up front? |
| 11 | Quantity Over Quality | Ideas span multiple approach clusters? |
| 12 | No Owner for Next Step | Each surviving idea has owner + next step + date? |

## Related Reading

- SKILL.md Troubleshooting section (for symptom -> root cause -> resolution)
- references/opportunity-solution-tree.md (if present)
- brainstorm-experiments/references/red-flags.md (for experiment design)
- identify-assumptions/references/red-flags.md (for connecting ideas to assumptions)
