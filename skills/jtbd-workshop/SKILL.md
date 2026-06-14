---
name: jtbd-workshop
description: >
  Run a full Jobs-To-Be-Done discovery workshop with switch interviews,
  forces-of-progress mapping, and outcome statement generation across 2hr,
  4hr, and 8hr formats.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-discovery
  updated: 2026-05-22
  tech-stack: jobs-to-be-done, switch-interviews, forces-of-progress, odi
---
# JTBD Workshop Expert

## Overview

Run a Jobs-To-Be-Done (JTBD) workshop end-to-end. This skill is the workshop facilitation companion to the `execution/job-stories/` skill (which is the *writing format* for backlog stories). Where `job-stories/` produces When/Want/So statements for individual backlog items, this skill produces the *upstream discovery output* -- the job hierarchy, the forces driving customers' switching behavior, and the desired-outcome statements that anchor the entire product strategy.

The workshop synthesizes four JTBD schools of thought. Clayton Christensen's *milkshake* lens treats jobs as the underlying progress a customer is hiring a product to make. Anthony Ulwick's Outcome-Driven Innovation (ODI) decomposes jobs into measurable desired outcomes with importance and satisfaction scoring. Alan Klement's JTBD canvas surfaces the situation-motivation-outcome structure that became the *job story* format. And Bob Moesta's switch interview method uses the moment of purchase as a forcing function to reveal the four forces of progress (push, pull, anxiety, habit).

A well-run JTBD workshop produces three artifacts: (1) a ranked job hierarchy with measurable outcome statements, (2) a forces-of-progress map showing what drives and blocks switching, and (3) a prioritized opportunity list ready to feed into PRDs, OKRs, or roadmap themes.

### When to Use

- **New product or new segment.** You need to understand the underlying progress customers are trying to make before building.
- **Pivot or strategy reset.** Your team is stuck debating features; reset by re-grounding in the customer's job.
- **Pre-roadmap.** Define the job hierarchy before committing to a quarterly or annual roadmap.
- **Stalled adoption.** Customers signed up but did not retain; switch interviews reveal which forces went wrong.
- **Onboarding a new product team.** Workshop creates shared mental model of what the customer is hiring the product to do.

## JTBD Foundations

### Christensen: Hiring a Product to Make Progress

Christensen's framing: customers "hire" products to do a job. They "fire" a product when a better candidate appears. The job is the customer's underlying desired progress -- not the product category, and not the demographic.

The famous milkshake example: customers buying milkshakes at 8am were not hiring the shake as a beverage. They were hiring it to make their morning commute less boring (job) and tide them over until lunch (outcome). The competition was not Burger King -- it was bananas, bagels, and boredom itself.

**Implications:**

- Define competition by alternative *hires* for the job, not by product category.
- A job is timeless and stable. Solutions change; jobs do not.
- Functional, social, and emotional dimensions all matter (the milkshake also signaled "I'm taking care of myself").

### Ulwick: Outcome-Driven Innovation

Ulwick's ODI argues that a job is too abstract to act on without measurable outcomes. He decomposes a job into a hierarchy:

```
Job: [Verb] + [Object] + [Context]
  e.g., "Close the books at month-end"
   |
   +-- Desired Outcome 1: Minimize [time/effort/error/cost] of [step]
   |   e.g., "Minimize time to reconcile payment processor to general ledger"
   +-- Desired Outcome 2: Minimize ...
   +-- Desired Outcome N: Minimize ...
```

Each desired outcome is scored on:

- **Importance** (1-10): How important is this outcome to the customer?
- **Satisfaction** (1-10): How well are current solutions performing?

**Opportunity score** = Importance + max(Importance - Satisfaction, 0)

Outcomes with high importance and low satisfaction are the highest-value innovation opportunities.

### Klement: The JTBD Canvas

Klement's JTBD canvas surfaces the *situation-motivation-outcome* structure that became the job story format:

```
When [situation],
I want to [motivation],
So I can [outcome].
```

The situation is the trigger context. The motivation is the customer's desire in that moment. The outcome is the progress they want to make. This format is the bridge from workshop output to backlog (`execution/job-stories/`).

### Moesta: Switch Interviews and Forces of Progress

Bob Moesta (working with Christensen) developed the switch interview method to surface the *moment* a customer hired or fired a product. The interview reconstructs the timeline:

```
[First Thought] -> [Passive Looking] -> [Active Looking] -> [Deciding] -> [First Use]
```

At each step, four forces are in play:

| Force | Direction | Description |
|-------|-----------|-------------|
| **Push of the situation** | Pro-switch | What is bad about the current state? |
| **Pull of the new solution** | Pro-switch | What is attractive about the alternative? |
| **Anxiety of the new solution** | Anti-switch | What worries the customer about switching? |
| **Habit of the present** | Anti-switch | What ties the customer to the status quo? |

A switch happens when Push + Pull > Anxiety + Habit. Most products under-invest in reducing Anxiety and Habit, and over-invest in increasing Pull.

## Workshop Formats

### Format A: 2-Hour Mini-Workshop

**Use when:** Team needs a fast reset; existing job hypothesis to validate; tight stakeholder calendar.

**Outcome:** Validated top 3 jobs and an aligned vocabulary.

| Time | Block | Outcome |
|------|-------|---------|
| 0:00 | Welcome + JTBD primer (10 min) | Shared vocabulary |
| 0:10 | Read 2 pre-workshop switch interview transcripts (15 min) | Grounded in customer voice |
| 0:25 | Job statement drafting -- individuals, then group (20 min) | 5-10 candidate job statements |
| 0:45 | Dot vote on top 3 jobs (10 min) | Top 3 jobs identified |
| 0:55 | Decompose top 3 into 3-5 desired outcomes each (30 min) | Outcome list |
| 1:25 | Forces-of-progress quick-map for the #1 job (20 min) | Push/Pull/Anxiety/Habit list |
| 1:45 | Synthesis + next-steps (15 min) | Owner per outcome, 90-day plan |

### Format B: 4-Hour Half-Day Workshop

**Use when:** Team has interview transcripts but no shared job hierarchy; pre-roadmap planning.

**Outcome:** Ranked job hierarchy, outcome scoring, forces map, and 5-10 opportunity statements.

| Time | Block | Outcome |
|------|-------|---------|
| 0:00 | Welcome + JTBD primer (20 min) | Shared vocabulary |
| 0:20 | Review 4-6 switch interview summaries (30 min) | Customer voice grounding |
| 0:50 | Job statement drafting individually (20 min) | Individual lists |
| 1:10 | Group cluster + write job hierarchy (40 min) | Big job + sub-jobs |
| 1:50 | Break (10 min) | -- |
| 2:00 | Decompose top 3 jobs into outcomes (45 min) | Outcome list per job |
| 2:45 | Score outcomes (Importance x Satisfaction) (30 min) | Opportunity scores |
| 3:15 | Forces-of-progress map for top job (30 min) | Forces canvas filled |
| 3:45 | Synthesis: prioritized opportunity list + next steps (15 min) | Deliverables agreed |

### Format C: 8-Hour Full-Day Workshop (or 2 x 4hr)

**Use when:** New product, new segment, or major strategy reset; minimum 6 participants from the product trio plus 2 customer-facing roles.

**Outcome:** Full job hierarchy, ODI-scored outcomes, completed forces map for top 3 jobs, journey map, and a 10-15 opportunity statement bank with owners.

| Time | Block | Outcome |
|------|-------|---------|
| 0:00 | Welcome + JTBD primer + workshop contracts (30 min) | Vocabulary, ground rules |
| 0:30 | Live switch interview with a customer (60 min, recorded) | Live customer voice |
| 1:30 | Group debrief: extract jobs, pains, gains from interview (30 min) | First snippet wall |
| 2:00 | Break (15 min) | -- |
| 2:15 | Review 6-10 additional transcripts; build snippet wall (60 min) | Coded snippets |
| 3:15 | Lunch (45 min) | -- |
| 4:00 | Cluster snippets into job hierarchy (60 min) | Big job + 5-8 sub-jobs |
| 5:00 | Decompose into desired outcomes (45 min) | 25-40 outcomes total |
| 5:45 | Break (15 min) | -- |
| 6:00 | Score outcomes with ODI (Importance x Satisfaction) (45 min) | Opportunity scores |
| 6:45 | Forces-of-progress map for top 3 jobs (45 min) | 3 forces canvases |
| 7:30 | Synthesis: write opportunity statements + assign owners (30 min) | Deliverables |

## The Switch Interview Script (Bob Moesta)

The switch interview is the engine of a JTBD workshop. It is a specialized form of the customer interview script (`discovery/customer-interview-script/`) focused on reconstructing the moment of purchase.

### Setup

- Interview customers who recently switched TO or FROM your product (or a competitor).
- "Recently" = within 90 days. Older switches are reconstructions.
- 60-90 minutes. Recorded with consent.

### Script structure

```text
"Today I want to walk through your decision to start using [product] step
by step. I'll be asking a lot of questions about WHEN things happened --
not just what -- because I'm trying to understand the timeline.

Let's start at the beginning. Take me back to the FIRST TIME you thought
you needed something like [product]. What was happening that day?"
```

### The four timeline anchors

For each anchor, probe deeply with story-pulling questions:

#### 1. First Thought

- "When did you first realize you needed [solution category]?"
- "What was happening that day?"
- "What were you using before?"
- "What made you think 'there must be a better way'?"

**Goal:** Identify the PUSH from the current situation.

#### 2. Passive Looking

- "Between that first thought and when you started actively researching, what happened?"
- "Did you mention it to anyone?"
- "Did anything happen that made you think about it again?"

**Goal:** Identify what kept the job *latent* and what re-triggered it.

#### 3. Active Looking

- "When did you start actively comparing options?"
- "What was the trigger that moved you from thinking to doing?"
- "What did you do first -- Google, ask a colleague, read reviews?"
- "What options were on your shortlist?"

**Goal:** Identify the PULL of alternatives and the moment urgency crossed threshold.

#### 4. Deciding

- "Walk me through the conversation where you decided."
- "Who was involved?"
- "What was the single biggest factor?"
- "What almost made you choose differently?"
- "What were you worried about?"

**Goal:** Identify ANXIETY and HABIT forces that almost stopped the switch.

#### 5. First Use

- "Walk me through the first time you used [product]."
- "What surprised you -- good or bad?"
- "Did you go back to the old way for anything? What?"

**Goal:** Identify ANXIETY that persisted after purchase and HABIT residue.

## Forces of Progress: Mapping the Switch

For each job, fill the forces canvas:

```text
                  PRO-SWITCH FORCES                ANTI-SWITCH FORCES
              ----------------------------    ----------------------------
              |                          |    |                          |
              |  PUSH                    |    |  ANXIETY                 |
              |  (of the situation)      |    |  (of the new solution)   |
              |                          |    |                          |
              |  - [What's bad about     |    |  - [What worries me      |
              |     current state?]      |    |     about switching?]    |
              |                          |    |                          |
              ----------------------------    ----------------------------
              ----------------------------    ----------------------------
              |                          |    |                          |
              |  PULL                    |    |  HABIT                   |
              |  (of the new solution)   |    |  (of the present)        |
              |                          |    |                          |
              |  - [What's attractive    |    |  - [What ties me to      |
              |     about the new way?]  |    |     the current way?]    |
              |                          |    |                          |
              ----------------------------    ----------------------------

  A switch happens when:  Push + Pull > Anxiety + Habit
```

### Strategic implications

Most products focus on Pull (increasing the attractiveness of the new way). The forces map reveals that Anxiety and Habit are usually the bigger barriers. Common moves:

- **Reduce Anxiety:** money-back guarantee, free trial, migration assistance, social proof, security certifications
- **Reduce Habit:** import tools, side-by-side comparison, "use both for 30 days" patterns
- **Sharpen Push:** make the pain of the status quo more visible (in marketing copy, in onboarding)
- **Refine Pull:** specific differentiators against named alternatives (not generic benefits)

## Outcome Statement Format (Ulwick ODI)

A desired outcome statement follows a strict format:

```text
Minimize [time / effort / likelihood / cost] of [verb] [object] [context]
```

Examples:

- "Minimize the time to reconcile Stripe transactions to the general ledger at month-end."
- "Minimize the likelihood of audit findings caused by mismatched payment records."
- "Minimize the effort to onboard a new finance team member to the reconciliation workflow."

For each outcome, score:

- **Importance (1-10):** How important is this to the customer?
- **Satisfaction (1-10):** How well are current solutions performing?

**Opportunity Score** = `Importance + max(0, Importance - Satisfaction)`

Outcomes with score >= 12 are high-opportunity (high importance, underserved). Score < 10 = saturated or unimportant.

## Common Workshop Traps

| Trap | Symptom | Fix |
|------|---------|-----|
| **Solution-mode** | Team writes features instead of jobs | Force the format: "Customer is trying to [verb] [object] [context]" |
| **Demographic substitution** | "Millennials" or "Enterprise" instead of jobs | Reject demographic framing; ask "What job does this person have?" |
| **Too abstract** | Job statements are slogans, not actionable | Decompose into Ulwick outcomes with time/effort/likelihood verbs |
| **Single transcript** | Workshop built on one interview | Require at least 6 transcripts; 10+ for the 8-hour format |
| **Skipping forces** | Team focuses only on Pull | Force the four-quadrant map; spend equal time on Anxiety and Habit |
| **Owner-less outcomes** | Workshop produces a list with no follow-through | Assign each top-5 outcome to a named owner with a 30-day next step |
| **No customer in the room** | All assumptions, no validation | Schedule a live switch interview during the 8-hour format; otherwise read transcripts aloud |
| **Premature scoring** | ODI scoring on outcomes before they are well-formed | Tighten outcome statements first (the verb test); then score |

## Workflow

1. **Plan.** Pick a format (2h / 4h / 8h) based on stakes and stakeholder availability. Define the segment.
2. **Recruit.** Identify 6-12 customers for switch interviews. Aim for recent switchers (90 days).
3. **Run pre-work switch interviews.** Use the script in this skill. Capture transcripts and summaries.
4. **Send pre-work to participants.** 2-3 transcript summaries to read before the workshop.
5. **Facilitate the workshop.** Follow the agenda for the chosen format.
6. **Capture outputs live.** Use Miro/FigJam or printed canvas templates from `assets/`.
7. **Score outcomes.** Either during the workshop (Format C) or as homework (Format A, B).
8. **Write opportunity statements.** Convert top-scored outcomes into opportunity statements (`<verb> <object> <context>`).
9. **Hand off.** Feed opportunities into `discovery/identify-assumptions/`, `discovery/brainstorm-experiments/`, or directly into `execution/create-prd/`.
10. **Re-visit quarterly.** Job hierarchy is stable; satisfaction scores shift as the market evolves.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| Workshop produces feature lists instead of jobs | Solution-mode bias; no customer voice in room | Read transcripts aloud during the workshop; reject any output that names a feature |
| Job statements are too abstract to act on | Stopped at the Christensen level; never decomposed | Apply Ulwick: each job gets 3-5 desired outcomes with time/effort/likelihood verbs |
| Forces map is lopsided (mostly Pull) | Team thinks like marketers, not switchers | Re-read switch interview transcripts focused on Anxiety and Habit moments |
| ODI scores cluster (all 8-9 Importance) | Participants score from team perspective, not customer | Score from a specific named customer; or use interview data to derive scores |
| Outputs do not survive past the workshop day | No owner per outcome; no follow-up cadence | Assign owners during the workshop; schedule a 30-day check-in |
| Team disagrees on the "main" job | Two segments mixed into one workshop | Split into segment-specific workshops; each segment has its own job hierarchy |
| Switch interview reveals customer never really switched | Recruiting criteria too loose | Tighten recruiting: must have switched in last 90 days; must have used both options |
| 8-hour workshop runs out of time before forces map | Spent too long on snippet wall | Time-box ruthlessly; the forces map is the highest-leverage block, not the snippet wall |

## Success Criteria

- At least 6 switch interview transcripts in the room (in summary or full)
- Job hierarchy produced: 1 big job + 5-8 sub-jobs
- 15+ desired outcomes statements in Ulwick format with Importance x Satisfaction scoring
- Forces-of-progress map filled for at least the top job (Format B) or top 3 jobs (Format C)
- Top 5 opportunities have named owners and 30-day next steps
- Workshop output handed off to at least one downstream skill (`identify-assumptions/`, `brainstorm-experiments/`, `create-prd/`, or `outcome-roadmap/`)
- Job hierarchy reviewed quarterly and confirmed stable (or revised with reason)

## Scope & Limitations

**In Scope:**
- 2-hour, 4-hour, and 8-hour workshop formats
- Switch interview script and four-anchor timeline
- Forces-of-progress mapping (push, pull, anxiety, habit)
- Ulwick desired outcome statement format with Importance x Satisfaction scoring
- Klement situation-motivation-outcome decomposition (bridge to `execution/job-stories/`)
- Pre-work email and participant brief

**Out of Scope:**
- Writing individual backlog stories (see `execution/job-stories/` for When/Want/So format)
- Quantitative ODI surveying at scale (this skill produces sample scoring; large-N surveys require dedicated research tooling)
- Live workshop recording and transcription tooling
- Recruiting operations (panel sourcing, screening, incentive management)
- Personas (the JTBD framework is segment-by-job, not persona-by-demographic)

**Important Caveats:**
- Switch interviews require *recent* (90-day) switchers. Reconstructed older switches are unreliable.
- The 2-hour format produces a thin output suitable for validation, not for primary discovery. New products should use Format C.
- ODI scoring is sensitive to who is in the room. Internal scoring is a hypothesis; customer-derived scores (via surveys) are the truth.
- A workshop without customer voice (transcripts, recorded interviews, or live participant) produces team-aligned fiction. Always anchor in real customer voice.

## Integration Points

| Integration | Direction | What Flows |
|-------------|-----------|------------|
| `discovery/customer-interview-script/` | Receives from | Switch interviews use the base interview script structure |
| `discovery/interview-synthesis/` | Receives from | Synthesized themes seed the snippet wall on workshop day |
| `discovery/identify-assumptions/` | Feeds into | Top outcomes become assumptions to test |
| `discovery/brainstorm-experiments/` | Feeds into | Forces-of-progress weaknesses become experiment hypotheses |
| `discovery/value-proposition-canvas/` | Feeds into | Jobs, pains, gains populate the Customer Profile |
| `execution/job-stories/` | Feeds into | Job + outcome decomposition becomes When/Want/So backlog stories |
| `execution/create-prd/` | Feeds into | Job hierarchy populates PRD Section 5; outcomes populate Section 6 |
| `execution/outcome-roadmap/` | Feeds into | Top desired outcomes become roadmap themes |
| `execution/north-star-metric/` | Feeds into | The highest-priority outcome often becomes the input metric tree root |

## References

- `references/jtbd-method-guide.md` -- Full JTBD methodology (Christensen, Ulwick, Klement, Moesta) with worked examples
- `assets/workshop_agenda_2hr.md` -- 2-hour mini-workshop agenda
- `assets/workshop_agenda_4hr.md` -- 4-hour half-day agenda
- `assets/workshop_agenda_8hr.md` -- 8-hour full-day agenda
- `assets/pre_work_email.md` -- Participant pre-work email template
- `assets/switch_interview_script.md` -- Switch interview script with the four timeline anchors
- `assets/forces_of_progress_canvas.md` -- Forces-of-progress mapping canvas
