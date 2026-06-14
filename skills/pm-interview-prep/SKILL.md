---
name: pm-interview-prep
description: >
  Structured PM interview preparation across product sense, execution, strategy,
  behavioral, and technical rounds, using CIRCLES, AARM, STAR, and the estimation
  framework. Calibrated to APM, PM, Senior PM, and Group PM rubrics.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-career
  updated: 2026-05-21
  tech-stack: pm-interviews, product-sense, execution, behavioral, frameworks
---
# PM Interview Prep Expert

## Overview

PM interviews test five distinct skills, each with its own format, frameworks, and rubric: product sense, execution, strategy, behavioral, and technical. This skill organizes preparation across all five round types and calibrates expectations to the level you are interviewing for (APM, PM, Senior PM, Group PM).

The skill bundles the most-used PM interview frameworks: Lewis Lin's CIRCLES Method for product design questions, the AARM Method for product improvement and metric questions, STAR for behavioral questions, and a 5-step estimation framework for market sizing. It also includes question banks per round and structured answer templates calibrated by level.

### When to Use

- **Preparing for PM interviews** -- You have a loop scheduled and need a structured plan to cover all rounds.
- **Mock interview prep** -- You are interviewing peers and want consistent rubrics.
- **Self-assessment** -- You want to identify your weakest interview category before investing prep time.
- **Switching levels** -- You are an IC PM moving to Senior or Senior moving to Group, and need to understand how the bar shifts.

### When NOT to Use

- General career planning -- use `pm-career-ladder/` for promotion and growth rubrics.
- Hiring as an interviewer -- this skill is calibrated for the candidate side, not the interviewer side.
- Engineering or design interview prep -- this is PM-specific.

## The Five Round Types

| Round | Tests | Typical Length | Primary Framework |
|-------|-------|----------------|-------------------|
| Product Sense (Design) | Customer empathy, problem framing, creative solutioning, prioritization | 45-60 min | CIRCLES (Lin) |
| Product Improvement | Metric diagnosis, root-cause analysis, solution generation | 45-60 min | AARM |
| Strategy | Market analysis, competitive positioning, go-to-market thinking | 45-60 min | Porter / 3Cs / Ansoff |
| Behavioral | Leadership, influence, conflict, impact storytelling | 45-60 min | STAR |
| Technical / Analytical | Systems thinking, data fluency, SQL, A/B test design, estimation | 45-60 min | Estimation 5-step / metric trees |

Not every loop covers all five. APM loops emphasize product sense and behavioral. Senior PM loops emphasize strategy and execution. Group PM loops emphasize cross-team strategy and people leadership.

## Framework 1: CIRCLES (Product Sense)

Lewis Lin's CIRCLES Method from *Decode and Conquer* is the canonical product design framework.

| Step | Question | Time |
|------|----------|------|
| **C**omprehend | Clarify the scope, constraints, and goals of the question. Ask 2-3 clarifying questions. | 3-5 min |
| **I**dentify the customer | Pick a specific user segment. Justify why. | 2-3 min |
| **R**eport customer needs | List 3-5 needs of the chosen segment. Categorize by JTBD or pain/gain. | 5-7 min |
| **C**ut through prioritization | Pick 1-2 top needs to solve. Justify with a criterion (impact, frequency, severity, strategic fit). | 3-5 min |
| **L**ist solutions | Generate 3-5 distinct solutions for the prioritized need. Include at least one creative/non-obvious idea. | 8-10 min |
| **E**valuate trade-offs | Compare solutions on impact, effort, risk, and strategic fit. | 5-7 min |
| **S**ummarize | State your recommendation, the why, and the next step. | 2 min |

**Common failure modes:**

- Skipping Comprehend (jumping to solutions before scope is clear)
- Picking "all users" as the segment (no segmentation = no signal of customer empathy)
- Listing 10 generic solutions instead of 3-5 distinct ones
- Forgetting to summarize (interviewer leaves without a clear answer)

## Framework 2: AARM (Product Improvement / Metric Diagnosis)

For "How would you improve X?" or "Why is metric Y down?" questions:

| Step | Action |
|------|--------|
| **A**lign on the goal | Confirm what "improve" means: revenue? engagement? retention? satisfaction? |
| **A**nalyze the current state | Map the funnel or user journey. Identify drop-off points or weak metrics. |
| **R**ecommend interventions | Propose 2-3 interventions targeting the weakest step. Tie each to a measurable outcome. |
| **M**easure success | Define the success metric, guardrail metrics, and how you would A/B test. |

AARM forces the candidate to ground recommendations in data, not opinion. It also signals senior-level instincts (guardrails, measurement) that distinguish PM from Senior PM.

## Framework 3: STAR (Behavioral)

Standard but worth re-stating because most candidates do it poorly.

| Component | Length | Common Mistake |
|-----------|--------|----------------|
| **S**ituation | 30s | Spending 3 minutes on context |
| **T**ask | 30s | Burying the "what was your job" in narrative |
| **A**ction | 2-3 min | Saying "we" instead of "I" -- interviewers cannot grade the team |
| **R**esult | 1 min | No quantified outcome; no "what I learned" |

**Senior PM and above:** Add a 5th element -- **Reflection.** What would you do differently? What did this teach you about your leadership style? This signals self-awareness.

**Prepare 8-12 stories** that cover the canonical behavioral themes:

1. Time you influenced without authority
2. Time you disagreed with your manager
3. Time you killed a feature/project
4. Time you handled a major mistake
5. Time you turned around a struggling project
6. Time you said no to a stakeholder
7. Time you missed a deadline
8. Most ambitious project / biggest impact
9. Time you worked with a difficult cross-functional partner
10. Time you mentored or developed someone (Senior+)
11. Time you built or evolved team processes (Senior+)
12. Time you set strategy that others adopted (Group+)

## Framework 4: Estimation (Market Sizing)

Five-step framework for "How many X are sold in Y per year?" questions:

1. **Clarify scope** -- Geographic boundary, time period, what counts as X.
2. **Pick an approach** -- Top-down (start from population) or bottom-up (start from units). State which and why.
3. **Decompose** -- Break the calculation into 3-5 multiplied factors. Each factor is something you can estimate within an order of magnitude.
4. **Estimate each factor** -- State your assumption and justify it briefly. Use round numbers.
5. **Sanity check** -- Compare the result to a known benchmark. State whether the answer feels high, low, or right and why.

**Example:** Yearly coffee cups sold in San Francisco.

- Scope: SF city (not Bay Area), 12 months, includes home + cafe.
- Approach: Bottom-up via population x cups-per-day.
- Decompose: Population (850K) x % coffee drinkers (60%) x cups/day (2) x 365 = ~370M cups/year.
- Sanity check: SF has ~1,500 coffee shops; if each sells 500/day = 275M shop cups/year. Plus home consumption (~30% of total). Total feels right.

## Level Calibration

Same question, different bar by level:

### Product sense ("Design a product for X")

| Level | Bar |
|-------|-----|
| APM | Picks a clear segment, lists 3 reasonable solutions, summarizes a pick |
| PM | + Articulates trade-offs, considers measurement, surfaces a non-obvious solution |
| Senior PM | + Connects to a business goal, considers downstream eng/design effort, names a v2/v3 path |
| Group PM | + Frames the opportunity strategically, identifies platform / cross-team implications, designs the operating cadence to learn fast |

### Behavioral ("Tell me about a time you...")

| Level | Bar |
|-------|-----|
| APM | Clean STAR, quantified result, owns their part |
| PM | + Shows judgment under uncertainty, surfaces what they learned |
| Senior PM | + Demonstrates influence at the org level, names trade-offs and counterfactuals |
| Group PM | + Demonstrates org-design / people leadership, story spans quarters not weeks |

### Strategy ("How would you grow product X?")

| Level | Bar |
|-------|-----|
| APM | Usually not asked this round |
| PM | Maps growth levers using a known framework (AARRR, Ansoff) |
| Senior PM | + Identifies the highest-leverage lever with reasoning, considers competitor response |
| Group PM | + Defines the operating system to run the strategy (teams, metrics, cadence, decision rights) |

## Workflow

1. **Diagnose your starting point.** Use `assets/self_assessment.md` to rate yourself across the five round types. Identify your weakest two.
2. **Build a question bank.** Use `references/question-bank.md` to pull 5-10 questions per round type targeted at your level.
3. **Practice solo first.** For each question, write a structured answer using the appropriate framework. Time yourself.
4. **Mock with a peer.** Schedule 2-3 mocks per round type. Use `assets/mock_feedback_form.md` for structured feedback.
5. **Refine stories.** Rewrite the 8-12 behavioral stories until each is under 5 minutes and quantified. Practice the opening line of each.
6. **Final week prep.** Re-read the company's product, recent press, and any teardown. Prepare 2-3 thoughtful questions to ask each interviewer.

## Question Banks (Excerpt -- see references/question-bank.md for full set)

### Product Sense

- "Design a product for a deaf person to navigate a city."
- "How would you redesign the airport experience for elderly travelers?"
- "Design a new feature for Spotify that drives daily engagement."

### Product Improvement

- "Why are Instagram Stories views down 5%?"
- "How would you improve Google Maps for commuters?"
- "How would you increase host signups on Airbnb?"

### Strategy

- "Should Netflix enter gaming?"
- "How should Shopify defend against Amazon's small-business push?"
- "What is the most important metric for Slack and why?"

### Behavioral

- See the 12-story prompt list above.

### Technical / Analytical

- "Estimate the storage cost of YouTube."
- "Design an A/B test for a new checkout flow. What is the minimum sample size?"
- "Walk me through how you would diagnose a 20% spike in API errors."

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| You run out of time in product sense rounds | Spending too long in Comprehend or List Solutions | Allocate time per CIRCLES step and self-monitor; aim for solutions in 25 min, summary in 5 min |
| Interviewer keeps asking "and why?" follow-ups | Answers lack reasoning chains | Every answer should include the rationale -- "I picked X because Y, with trade-off Z"; explicitly state trade-offs unprompted |
| Behavioral stories sound generic | STAR is too high-level; "we" instead of "I"; no quantification | Rewrite to be specific to one event; replace "we" with "I"; add 1-2 numbers per story |
| You blank on the metric question | No mental model of the product's metric tree | Before the interview, sketch the product's likely metric tree (NSM + input metrics); rehearse 2-3 diagnostic patterns |
| Estimation answers are off by 100x | Skipping the sanity check step | Always compare to a known benchmark (population, GDP, daily users) before stating the final number |
| You feel under-leveled in feedback | Examples scoped too small (project-level for a Senior role) | Pick larger-scope stories that span multiple teams or quarters; for Group PM, lead with stories about org design, not feature design |
| You over-prepared frameworks but bombed | Robotic delivery; framework became scaffolding visible to interviewer | Use frameworks invisibly -- never name CIRCLES out loud; let the structure show through your answer, not your vocabulary |

## Success Criteria

- You have a structured answer template for each of the five round types
- You have 8-12 behavioral stories written, timed under 5 minutes each
- You have completed >=2 mocks per round type with structured feedback
- You can run CIRCLES end-to-end on a novel question in under 45 minutes
- You can do market sizing within 10 minutes including sanity check
- You have 2-3 thoughtful questions prepared for each interviewer
- You know the level-appropriate bar -- you are not under-scoping (sounds like an APM in a Sr PM loop) or over-scoping (sounds like a Director in a PM loop)

## Scope & Limitations

**In Scope:**
- Framework-based preparation for all five PM round types
- Level calibration from APM through Group PM
- Question banks and structured answer templates
- Behavioral story development and STAR refinement
- Self-assessment and mock-interview feedback tools

**Out of Scope:**
- Director / VP / CPO interviews -- those test executive judgment, board influence, and P&L ownership. Use a leadership-coaching engagement.
- Technical screens for technical-PM roles at specific companies -- consult the role's published rubric.
- Salary negotiation and offer evaluation -- a separate workflow.
- Resume and outreach prep -- use `personal-productivity/resume/` and related skills.

**Important Caveats:**
- Frameworks are scaffolds, not scripts. Interviewers down-rank candidates who recite frameworks verbatim. Internalize them so the structure is invisible.
- Every company has its own rubric. Adjust emphasis based on the company's published interview guide and the recruiter's call.
- Mock interviewing with a current PM at the target company beats reading any book. Invest disproportionately in mocks.

## Integration Points

| Integration | Direction | What Flows |
|-------------|-----------|------------|
| `pm-career-ladder/` | Bidirectional | Use the ladder rubric to understand the level you are interviewing for |
| `pm-onboarding/` | Feeds into | Once hired, the onboarding skill takes over for first 90 days |
| `personal-productivity/resume/` | Feeds from | A clean resume with quantified impact feeds the behavioral stories |
| `discovery/brainstorm-ideas/` | Reuses | Product sense rounds reuse the same ideation discipline as Product Trio sessions |
| `execution/prioritization-frameworks/` | Reuses | RICE, ICE, and Opportunity Score reasoning shows up in CIRCLES Step 4 (Cut through) |

## References

- `references/question-bank.md` -- 100+ questions across all five round types
- `references/framework-deep-dive.md` -- Worked examples for CIRCLES, AARM, STAR, Estimation
- `assets/self_assessment.md` -- Pre-prep diagnostic across the five round types
- `assets/mock_feedback_form.md` -- Structured feedback form for mock interviews
- `assets/story_worksheet.md` -- Worksheet for the 12 canonical behavioral stories

External:

- Lin, L. *Decode and Conquer*. (CIRCLES Method)
- McDowell, G. & Bavaro, J. *Cracking the PM Interview*.
- Lin, L. *The Product Manager Interview*. (AARM and 165 sample questions)
- Bock, L. *Work Rules!* (Google interviewing philosophy)
