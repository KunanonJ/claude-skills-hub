---
name: customer-interview-script
description: >
  Run high-signal customer discovery interviews using a scripted question
  hierarchy, behavior-over-opinion probes, and rapport techniques drawn from
  Portigal, Torres, Fitzpatrick, and Lewis Lin.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-discovery
  updated: 2026-05-22
  tech-stack: customer-interviews, discovery, jobs-to-be-done, mom-test
---
# Customer Interview Script Expert

## Overview

Running a customer interview is harder than it looks. The difference between a 60-minute conversation that produces three actionable insights and one that produces zero is almost entirely method: what you ask, when you ask it, and what you do *not* ask. This skill is the live-interview companion to `discovery/interview-synthesis/` (which handles post-interview analysis) and `discovery/identify-assumptions/` (which produces the questions you go in to test).

The script structure draws from four canonical sources: Steve Portigal's *Interviewing Users* (rapport, listening, "tell me about the last time"), Teresa Torres' *Continuous Discovery Habits* (story-based probing, weekly cadence), Rob Fitzpatrick's *The Mom Test* (avoiding compliments, opinions, and futures), and Lewis Lin's behavioral interviewing patterns (concrete-recent-relevant). The goal is to leave each interview with at least one story, one contradiction, and one surprise.

### When to Use

- **Problem discovery** -- You have a hypothesis about a customer pain and need to learn whether it is real, who has it, and how acute it is.
- **Solution validation** -- You have a wireframe, prototype, or written concept and want feedback grounded in past behavior, not hypothetical reactions.
- **Journey research** -- You need to understand the end-to-end flow of how a customer accomplishes a job today (tools, workarounds, handoffs).
- **Churn or win/loss interviews** -- You need to understand why customers left, stayed, or chose a competitor.
- **Continuous discovery cadence** -- Weekly customer touchpoints to keep the team grounded in real evidence rather than internal opinion.

## Frameworks

### Portigal: Rapport and Active Listening

Portigal's central insight is that interview quality is bounded by rapport quality. The first 5-10 minutes are not "warm-up" -- they are the foundation of every honest answer that follows.

**Rapport rules:**

1. **Introduce yourself as a learner, not an expert.** "I'm here to learn from you" produces openness. "I'm the PM for this product" produces sales calls.
2. **Establish that there are no wrong answers.** Explicitly say: "There's nothing you can say that's wrong -- I'm here to understand your world."
3. **Ask permission to record.** State the use, the storage policy, and offer the option to decline without consequence.
4. **Make the first question easy.** Something they can answer in 2 minutes without thinking ("Walk me through your role").
5. **Use silence as a tool.** After the participant finishes a sentence, count to 3 before speaking. They will often add the most important detail in that gap.

### Torres: Story-Based Probing

Torres' *Continuous Discovery Habits* argues that opinions are low-evidence ("I would like a faster dashboard") but stories are high-evidence ("Last Tuesday I tried to pull the Q3 report and gave up after 11 minutes"). Every meaningful question should pull for a story.

**Story prompts:**

- "Tell me about the last time you [did the job]."
- "Walk me through what happened."
- "What did you do right before that? What did you do right after?"
- "Who else was involved? What did they say?"
- "Where were you? What tools did you have open?"

**The story funnel:**

```
Broad: "Tell me about a recent time you needed [X]."
  -> Narrow: "What specifically were you trying to accomplish?"
    -> Concrete: "What did you do first?"
      -> Behavioral: "Show me how you did that."
        -> Emotional: "How did you feel when [event]?"
```

### Fitzpatrick: The Mom Test

Fitzpatrick's *The Mom Test* lists three things that bias interviews toward false positives -- things even your mother would say to be polite:

1. **Compliments** ("That's a great idea!")
2. **Fluff** -- hypotheticals, generics, opinions about the future ("I would probably use it")
3. **Ideas** -- the participant pitching you a feature ("You should add X")

**The three Mom Test rules:**

1. Talk about their life, not your idea.
2. Ask about specifics in the past, not generics or opinions about the future.
3. Talk less, listen more.

**Conversion table -- bad question -> good question:**

| Bad (low-evidence) | Good (high-evidence) |
|--------------------|----------------------|
| Would you use a product that... | Tell me about the last time you tried to... |
| Do you think X is a problem? | When was the last time X happened? What did you do? |
| How often do you do X? | When was the last time you did X? Walk me through it. |
| Would you pay for X? | What do you currently spend on solving this? Show me the invoice. |
| What features do you want? | What is the most frustrating part of [job] today? |

### Lewis Lin: Concrete-Recent-Relevant

Lewis Lin's behavioral interviewing distills story quality into three properties:

- **Concrete** -- A specific event with names, dates, tools, outcomes (not a generalized pattern).
- **Recent** -- Within the last 30-90 days (memory decays; old stories are reconstructions).
- **Relevant** -- The job-to-be-done you care about, not a tangentially related anecdote.

If a story is missing any of the three, probe for one that has all three: "Has anything like that happened more recently?"

## The Interview Script Structure

Every interview, regardless of type, follows this 5-phase structure. Total time: 45, 60, or 90 minutes.

### Phase 1: Opening (5 min)

**Goal:** Establish rapport, consent, and frame.

```text
"Thanks for making time today. Before we start I want to share three things:

1. There are no wrong answers. I'm here to learn how you work, not to test you.
2. I'd like to record this for my notes. The recording stays internal and
   will be deleted in 90 days. Is that okay?
3. We have [45/60/90] minutes. If anything I ask is uncomfortable or
   confusing, just say so and we'll move on.

To start, can you walk me through your role -- what you do day to day?"
```

### Phase 2: Context & Background (5-10 min)

**Goal:** Understand the participant's environment so later stories have context.

Sample questions:
- "What does a typical week look like for you?"
- "Who do you work with most closely?"
- "What tools do you spend the most time in?"
- "What does success look like in your role -- how is it measured?"

### Phase 3: Story Collection (25-40 min) -- THE MEAT

**Goal:** Collect 2-4 concrete-recent-relevant stories about the job-to-be-done.

**Opening story prompt** (varies by interview type -- see Question Bank below):

> "Tell me about the last time you [job-to-be-done]."

**Then probe with the 5 Whys and story funnel:**

1. "Walk me through what happened."
2. "What did you do right before that?"
3. "What were you trying to accomplish?" (Why #1)
4. "Why was that important?" (Why #2)
5. "What would have happened if you had not done that?" (Why #3)
6. "Who else was involved?" (expands the story to the system)
7. "What tools or systems did you use?"
8. "What was the outcome? How did you feel?"

**Collect 2-4 stories.** Each story should produce 5-10 snippets for synthesis.

### Phase 4: Probing & Synthesis (10-15 min)

**Goal:** Test contradictions, fill evidence gaps, validate or invalidate top assumptions.

- "Earlier you said X. Later you mentioned Y. Help me understand how those fit together."
- "If [current workaround] disappeared tomorrow, what would you do?"
- "What would have to be true for you to [behavior change]?"
- "Who else should I talk to about this?"

### Phase 5: Closing (5 min)

**Goal:** Leave the door open for follow-up.

```text
"That was incredibly helpful. A few last things:

- Is there anything I should have asked but didn't?
- Can I follow up if I have a clarifying question?
- Who else do you think I should talk to about [topic]?

Thanks again for your time."
```

## Question Bank by Interview Type

### Problem Discovery

- "Tell me about the last time you tried to [job]."
- "What is the most frustrating part of [job] today?"
- "What workarounds have you built to deal with [problem]?"
- "What does it cost you when [problem] happens -- time, money, stress?"
- "Who else on your team deals with this?"

### Solution Validation (with prototype)

- "Walk me through what you see here -- what do you think this is?"
- "If you were trying to [job], where would you click first?"
- "What's confusing or surprising?"
- "When in your week would you actually use this?"
- "What would have to be true for you to start using this tomorrow?" (Then probe past behavior for evidence.)

### Journey Mapping

- "Walk me through the last time you did [end-to-end process], from the moment it started to the moment it ended."
- "Where did you get stuck? Where did you have to wait?"
- "Who else touched this process?"
- "What did you wish was different?"

### Churn / Win-Loss

- "What were you trying to accomplish when you signed up?"
- "When did you start feeling like it was not working?"
- "Walk me through the conversation when you decided to leave/choose [competitor]."
- "What were you doing before? What are you doing now?"
- "If we had done one thing differently, what would have changed your mind?"

## What NOT to Ask

| Anti-pattern | Why it fails | Fix |
|--------------|--------------|-----|
| "Would you use a feature that..." | Hypothetical -- participant gives polite answer | "Tell me about the last time you needed to..." |
| "Do you like X?" | Compliment-seeking; biased | "Walk me through how you used X last week" |
| "How often do you...?" | Generic; produces averaged guess | "When was the last time? And before that?" |
| "What do you think we should build?" | Solution-mode; participant becomes designer | "What is the hardest part of [job]?" |
| "Don't you agree that...?" | Leading; confirmation bias | Remove the framing -- ask open-ended |
| "If you had X, would you Y?" | Double-hypothetical | "Tell me what you do today" |
| "Why don't you just...?" | Implies the participant is wrong | "Walk me through what you tried" |

## Interview Pacing

| Length | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | When to Use |
|--------|---------|---------|---------|---------|---------|-------------|
| 45 min | 3 min | 5 min | 25 min | 8 min | 4 min | Tight-window participants (execs, customers under contract) |
| 60 min | 5 min | 8 min | 32 min | 10 min | 5 min | Standard discovery interview -- default |
| 90 min | 5 min | 10 min | 50 min | 15 min | 10 min | Deep journey mapping, switch interviews, complex B2B workflows |

**Pacing rules:**

- If you have collected only 1 story by the halfway point, abandon Phase 2 and push deeper into Phase 3.
- If you have collected 4 stories with 20 minutes remaining, move to Phase 4 to test contradictions.
- Never run over without explicit consent. Ending on time is a rapport-builder.

## Pair Interviewing vs. Solo

| Mode | When | Roles |
|------|------|-------|
| **Solo** | Async-friendly contexts; short interviews; experienced interviewer | One person both leads and notes |
| **Pair: lead + note-taker** | Standard discovery; first 5-10 interviews of a study | Lead drives the conversation; note-taker writes verbatim quotes and timestamps |
| **Pair: lead + silent observer** | Stakeholder ride-alongs; cross-functional alignment | Observer learns the method; never speaks during interview |
| **Trio: lead + note + observer** | High-stakes B2B; complex multi-stakeholder workflows | Add one stakeholder as silent observer (Eng or Design) |

**Pair coordination:**

- Lead and note-taker agree on a hand-signal for "wrap this thread" before the interview.
- Note-taker writes quotes verbatim, not paraphrased. Mark timestamps for top quotes.
- Debrief within 30 minutes of the interview while it is fresh.

## Recording, Consent & Storage

- **Always ask permission** before recording, even if your terms of service technically allow it.
- **State the storage policy** verbally and in writing: where, who has access, how long.
- **Default retention: 90 days** for raw recordings; transcripts retained indefinitely with PII redacted.
- **Offer a non-recorded alternative.** Participants who decline recording often share the most candid information when they know it is off the record.
- **For B2B**, secure a recording consent clause in the participant's NDA or research agreement.

## Handling Silence

Silence is the most underused interview technique. After the participant finishes a sentence:

1. Count to 3 (Mississippi-style) before speaking.
2. If they are still silent at 5 seconds, lightly nod or write a note -- don't speak.
3. 80% of the time they will add the most important detail in that gap ("...actually, the real reason was...").

If the silence stretches past 10 seconds and feels uncomfortable, break it with a non-leading prompt: "Take your time" or "What were you about to say?"

## Workflow

1. **Define the study.** Pull top assumptions from `discovery/identify-assumptions/` and write 2-3 must-answer questions per interview.
2. **Pick the interview type.** Problem discovery / solution validation / journey / churn -- this selects your Question Bank section.
3. **Customize the script.** Start from `assets/interview_script_template.md`, replace placeholders, and write 4-6 backup story prompts.
4. **Recruit participants.** Aim for 5-7 per segment; saturate when new themes stop appearing.
5. **Send pre-interview email.** Include time, agenda preview, recording consent ask, and a 1-sentence framing.
6. **Run the interview.** Follow the 5-phase script. Resist the urge to pitch.
7. **Debrief within 30 minutes.** Write down your three biggest surprises before they decay.
8. **Hand off to synthesis.** Feed the transcript into `discovery/interview-synthesis/` for theme clustering.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| Participant gives only opinions, no stories | You asked "do you / would you" questions | Pivot to "Tell me about the last time..." and probe for a specific event |
| Participant pitches you features | You asked "what should we build" | Redirect: "Before we get to solutions, help me understand the problem -- when was the last time it happened?" |
| Interview runs out of time with no usable stories | Phase 1 + 2 ran long; Phase 3 got squeezed | Cap Phase 1 at 5 min, Phase 2 at 8 min; if Phase 2 is dragging, jump to first story prompt |
| Participant seems guarded or short-answering | Rapport never established; recording disclosure may have spooked them | Offer to pause recording; restart with low-stakes context question; share something about yourself first |
| Same answers from every participant -- no new insights | Recruiting too homogenous; questions too narrow | Expand recruiting criteria; broaden Phase 3 opening prompt |
| Contradictions go unprobed | Interviewer too focused on getting through the script | Mark contradictions in your notes during the interview; reserve Phase 4 to revisit them |
| Stakeholders distrust the findings | Single-source quotes; no behavioral evidence | Require >=3 participants per theme; surface stories, not paraphrased takeaways |

## Success Criteria

- Every interview produces at least 1 concrete-recent-relevant story per must-answer question
- At least 60% of Phase 3 time is the participant talking (not the interviewer)
- Zero compliments, futures, or "would you" questions in the recorded portion (audit the transcript)
- Debrief notes written within 30 minutes of the interview
- 5+ interviews per segment before declaring saturation
- Transcript hands off cleanly to `discovery/interview-synthesis/` (one row per Q&A pair)
- Recording consent documented in writing for every participant

## Scope & Limitations

**In Scope:**
- Live customer discovery interview script structure and pacing
- Question banks for problem discovery, solution validation, journey, churn/win-loss
- Rapport-building, listening techniques, silence handling
- Recording consent and retention policy
- Pair-interviewing role definitions

**Out of Scope:**
- Interview synthesis and theme clustering (see `discovery/interview-synthesis/`)
- Assumption mapping before interviews (see `discovery/identify-assumptions/`)
- Survey design and quantitative research
- Usability testing protocols (different methodology -- task-based, not story-based)
- Recruiting operations (panel sourcing, screening, incentive management)

**Important Caveats:**
- This skill produces high-quality interview *technique*. It does not replace research operations (recruiting, scheduling, incentives).
- Story-based interviewing is bounded by participant memory. Events older than 90 days are reconstructions, not recall.
- B2B enterprise interviews often require a procurement-style approval process; build 2-4 weeks into recruiting timelines.
- Continuous discovery (Torres) assumes weekly customer touchpoints. One-off interview rounds produce shallower evidence trees -- weight findings accordingly.

## Integration Points

| Integration | Direction | What Flows |
|-------------|-----------|------------|
| `discovery/identify-assumptions/` | Receives from | Top assumptions become the must-answer questions for each interview |
| `discovery/interview-synthesis/` | Feeds into | Transcripts and debrief notes are the input for theme clustering |
| `discovery/brainstorm-ideas/` | Bidirectional | Pre-interview hypotheses; post-interview ideas are seeded by themes |
| `discovery/brainstorm-experiments/` | Feeds into | Validated pains become experiment hypotheses |
| `discovery/jtbd-workshop/` | Complementary | Switch interviews use this script structure as their foundation |
| `discovery/value-proposition-canvas/` | Feeds into | Jobs, pains, and gains captured in stories populate the Customer Profile |
| `execution/create-prd/` | Feeds into | Direct quotes from interviews strengthen PRD Background and Market Segments |

## References

- `references/interviewing-methodology-guide.md` -- Full method with worked examples (Portigal, Torres, Fitzpatrick, Lin)
- `assets/interview_script_template.md` -- Ready-to-customize 5-phase interview script
- `assets/question_bank.md` -- Question bank organized by interview type (problem / solution / journey / churn)
