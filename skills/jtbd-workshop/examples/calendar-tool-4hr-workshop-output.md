# Example: Northwind Calendar — 4-Hour JTBD Workshop Output

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Northwind Calendar is a Series-A B2B calendar tool (38 employees, ~$3M ARR, ~6,000 paying users) competing in a crowded space (Calendly, Cal.com, Reclaim). The team has been adding features for two years but retention is flat and the founder believes the team has lost sight of what customers are actually trying to do. The new VP Product (4 weeks in role) has scheduled a half-day JTBD workshop with the product trio + 2 customer success leads + 1 sales engineer.

The jtbd-workshop skill is being applied to run the 4-hour format. Inputs include 6 switch interviews completed in the previous 2 weeks (the previous PM's last project), plus access to retention and feature-usage data. The output of the workshop will anchor the next two quarters of roadmap.

## Inputs

- Product: Northwind Calendar (scheduling tool for client-facing teams: sales, consulting, healthcare practitioners)
- Recent switch interviews: 6 customers who switched TO Northwind in the last 90 days
- Workshop participants: 7 people (VP Product, 1 PM, 1 designer, 1 engineer, 2 CS leads, 1 sales engineer)
- Workshop duration: 4 hours (08:30-12:30, with 15-min break)
- Constraint: workshop output must be share-ready for engineering planning the following Monday
- Constraint: no consultant facilitating; VP Product runs it

## Applying the skill

1. **Used the 4-hour format, not 2hr or 8hr.** 2hr is for refresh; 8hr is for full discovery. 4hr fits Northwind's situation (some prior interview data, need converged output by EOD).
2. **Brought 6 switch interviews as raw material.** Each participant read 2 transcripts before the workshop. Workshop time is for synthesis, not extraction.
3. **Worked through Christensen, Ulwick, Klement, and Moesta in sequence.** Did not jump to outcome statements without the job hierarchy first. The order matters because each layer constrains the next.
4. **Used the Forces of Progress framework live.** The four forces (push, pull, anxiety, habit) were mapped on a whiteboard, with sticky notes from the switch interviews placed under each.
5. **Generated outcome statements with Ulwick's importance/satisfaction scoring.** Each outcome was scored by the room; ties were resolved by referring back to interview evidence, not consensus.
6. **Produced three artifacts.** Job hierarchy. Forces map. Outcome statements with opportunity scores.

## The artifact

```
================================================================
  NORTHWIND CALENDAR — JTBD WORKSHOP OUTPUT
  Format:   4-hour
  Date:     2026-05-22, 08:30-12:30 PT
  Facilitator: VP Product
  Attendees: 7
================================================================


PART 1 — THE PRIMARY JOB

After 90 minutes of synthesis, the room converged on:

  Primary job statement:
  "When my time is split between client conversations and
   focused work, I want to keep client scheduling effortless
   for both sides, so I can stop being the bottleneck and
   keep my energy for the actual conversation."

Christensen lens:
  - What customers are "hiring" the product to do:
    eliminate scheduling-back-and-forth as a precondition
    to delivering their actual professional value.
  - What customers are "firing" when they switch to Northwind:
    email-based scheduling (most common), generic Calendly
    (second most), or a default calendar app that doesn't
    handle availability rules.
  - The competition: NOT other scheduling products. The
    competition is "the way I scheduled before" (email),
    "letting clients pick anything on my calendar," or
    "delegating scheduling to an assistant."

Functional, social, emotional dimensions:
  Functional   reduce time spent on scheduling logistics
  Social       look professional to clients
  Emotional    feel in control of my time; reduce dread of
               "what's on my calendar tomorrow"


PART 2 — JOB HIERARCHY (ULWICK ODI)

Primary job: Keep client scheduling effortless
  |
  +-- Sub-job 1: Make my availability visible to clients
  |     - Outcome 1.1: Minimize the time to publish my
  |       availability to clients
  |     - Outcome 1.2: Minimize the chance my availability
  |       is wrong because of a recent calendar change
  |     - Outcome 1.3: Minimize the friction for a client
  |       to find a slot that works for both of us
  |
  +-- Sub-job 2: Reduce the back-and-forth before a meeting
  |     - Outcome 2.1: Minimize the email exchanges needed
  |       to confirm a meeting
  |     - Outcome 2.2: Minimize the cognitive load of
  |       coordinating across time zones
  |     - Outcome 2.3: Minimize the rate of mis-scheduled
  |       meetings (wrong time, wrong place)
  |
  +-- Sub-job 3: Protect my focus time
  |     - Outcome 3.1: Minimize the chance a low-priority
  |       meeting takes a high-focus slot
  |     - Outcome 3.2: Minimize the friction to block focus
  |       time at the start of the day
  |     - Outcome 3.3: Minimize the time spent rescheduling
  |       when a focus slot is requested
  |
  +-- Sub-job 4: Handle the unexpected gracefully
        - Outcome 4.1: Minimize the time to reschedule a
          meeting when something comes up
        - Outcome 4.2: Minimize the chance both parties
          don't see the reschedule
        - Outcome 4.3: Minimize the awkwardness of a no-show
          (mine or theirs)


PART 3 — OUTCOME SCORING

Each outcome was scored by the room (median of 7 votes).
Importance scored 1-10; Satisfaction (with current
Northwind product) scored 1-10. Opportunity score =
Importance + max(Importance - Satisfaction, 0).

OUTCOMES IN ORDER OF OPPORTUNITY SCORE

  Outcome                                    Imp  Sat  Opp
  ----------------------------------------   ---  ---  ---
  3.2 Block focus time at start of day        9    3   15
  2.2 Coordinate across time zones            9    4   14
  3.1 Low-priority meeting in high-focus slot 8    3   13
  4.3 Reduce awkwardness of no-show           7    3   11
  2.3 Reduce rate of mis-scheduled meetings   8    5   11
  1.3 Reduce friction for client to find slot 9    7   11
  4.2 Both parties see the reschedule         8    5   11
  3.3 Reschedule when focus slot is requested 7    4   10
  4.1 Time to reschedule when something
      comes up                                8    6   10
  2.1 Reduce email exchanges                  9    7   11 *
  1.1 Time to publish availability            8    7    9
  1.2 Availability wrong from calendar change 7    5    9

  * Outcome 2.1 has a positive gap (Imp 9 - Sat 7 = 2);
    opportunity score is Imp + 2 = 11.

HIGH-OPPORTUNITY ZONE (Opp >= 13):
  - Outcome 3.2 (focus blocking at day start)
  - Outcome 2.2 (cross-time-zone coordination)
  - Outcome 3.1 (low-priority taking focus slots)

These three are where current solutions (including Northwind)
poorly serve a high-importance need. This is the white space.


PART 4 — FORCES OF PROGRESS MAP (MOESTA)

From the 6 switch interviews, the room mapped the forces
driving customers TO Northwind and OUT of their previous
tool.

PUSH forces (what made them leave the old tool):
  - "Every meeting started with 6 emails." (4 of 6)
  - "I missed a meeting because my calendar wasn't updated."
    (3 of 6)
  - "My assistant left and scheduling collapsed." (1 of 6)
  - "Calendly was fine but I needed time-zone smarts." (2 of 6)
  - "I felt like I was always the bottleneck." (5 of 6)

PULL forces (what attracted them to Northwind):
  - "A friend recommended it." (4 of 6)
  - "I saw a competitor link on a sales person's email and
     liked the experience." (3 of 6)
  - "I wanted automatic focus time." (2 of 6)
  - "Time-zone handling was promised." (3 of 6)

ANXIETY forces (what almost stopped them switching):
  - "Will my clients accept a new scheduling link?" (5 of 6)
  - "Will I lose meetings during the migration?" (3 of 6)
  - "What if it breaks during a critical week?" (2 of 6)
  - "Is the pricing going to surprise me?" (4 of 6)

HABIT forces (what kept them on the old way):
  - "Email scheduling is what I know." (5 of 6)
  - "Calendly works fine; I never thought about switching."
    (2 of 6)
  - "I have a calendar template; it works for me." (1 of 6)
  - "I already paid for Calendly through end of year." (2 of 6)

Net effect:
  Push (5/6 "felt like the bottleneck") + Pull
  (friend recommendation) overcame Anxiety (client
  acceptance) and Habit (email).

The biggest unaddressed Anxiety is "will my clients
accept this link?" — appearing in 5 of 6 interviews.
This is a marketing/onboarding lever, not a feature
lever.


PART 5 — JOB STORIES (KLEMENT FORMAT)

Five high-leverage job stories generated from the top
opportunities:

JS-1 (from Outcome 3.2):
  When I start a new workday and I'm dreading interruptions,
  I want my morning focus block to auto-create with
  reasonable defaults,
  so I can default-protect my best hours without thinking
  about it.

JS-2 (from Outcome 2.2):
  When I'm scheduling a meeting with someone in a different
  time zone,
  I want the calendar to surface only times that are
  reasonable for both of us,
  so I can avoid offering someone 3am or being asked to
  show up at 6am.

JS-3 (from Outcome 3.1):
  When a low-priority meeting request comes in,
  I want the system to suggest a non-focus slot first,
  so my best hours stay clear without me having to enforce
  rules manually.

JS-4 (from Outcome 4.3):
  When a meeting is missed (no-show on either side),
  I want a graceful, one-click follow-up that doesn't
  embarrass either party,
  so I can keep the relationship clean.

JS-5 (from Anxiety force):
  When I'm about to send a new client a Northwind link
  for the first time,
  I want assurance that they'll find the experience
  easy,
  so I don't worry about whether they'll bounce.


PART 6 — PRIORITIZED OPPORTUNITY LIST FOR ROADMAP

The workshop output produced a single ranked list to feed
quarterly planning:

  Rank  Opportunity                       Source
  ----  --------------------------------  --------
  1     Auto focus-time block at day      JS-1, OPP 15
        start
  2     Time-zone-smart slot selection    JS-2, OPP 14
  3     Priority-aware slot suggestion    JS-3, OPP 13
  4     Client experience reassurance     JS-5, anxiety
        (onboarding/UX/marketing)         force, anxiety
                                          5 of 6 interviews
  5     Graceful no-show recovery         JS-4, OPP 11


PART 7 — WHAT THE WORKSHOP DID NOT PRODUCE

  - A feature spec. The output is jobs and outcomes, not
    features. Engineering will scope features later.
  - A pricing decision. Pricing came up but was deferred —
    JTBD anchors the WHAT, not the HOW MUCH.
  - A competitor analysis. The Christensen lens reframed
    competition as "the way I scheduled before," not
    Calendly. A traditional competitor matrix would have
    distracted.
  - An AI feature plan. The room considered "AI-driven
    scheduling" but landed on: AI is an implementation
    detail of the outcomes above, not its own opportunity.


PART 8 — WORKSHOP TIMELINE (HOW THE 4 HOURS WENT)

  08:30 - 08:45  Kickoff, ground rules, share-out from
                 pre-read
  08:45 - 09:30  Christensen exercise: what are customers
                 firing? What are they hiring?
                 Output: primary job statement candidates;
                 converged on one.
  09:30 - 10:30  Ulwick exercise: job hierarchy + outcome
                 statements
                 Output: 12 outcomes across 4 sub-jobs
  10:30 - 10:45  BREAK
  10:45 - 11:15  Outcome scoring (importance x satisfaction)
                 Output: opportunity scores, top 3 identified
  11:15 - 11:45  Moesta exercise: forces of progress map
                 Output: push/pull/anxiety/habit per
                 interview
  11:45 - 12:15  Klement job story drafting for top 5
                 outcomes
                 Output: 5 job stories
  12:15 - 12:30  Convergence on prioritized list and next
                 steps


PART 9 — DELIVERABLES TO ENGINEERING (MONDAY HANDOFF)

  - Primary job statement (one paragraph)
  - Job hierarchy (4 sub-jobs, 12 outcomes)
  - Outcome opportunity scores (ranked table)
  - Forces of progress map (annotated whiteboard photo
    + transcribed Confluence page)
  - 5 job stories
  - Top 5 prioritized opportunities for next 2 quarters
  - 6 switch-interview transcripts (Dovetail links)


PART 10 — RISKS & FOLLOW-UPS

R1  Sample of 6 switch interviews is small. Top-3
    opportunities are well-supported (each cited in
    4-6 of 6) but ranks 4-12 have thinner evidence.

R2  No interviews with churned customers in this batch —
    only customers who switched IN. Adding 3 interviews
    with customers who switched OUT (to a competitor)
    would round out the Forces map.

R3  Opportunity 4 (client experience reassurance) is not
    a product opportunity — it's marketing/onboarding.
    Risk that engineering takes it as a feature spec.
    Mitigation: hand-off doc explicitly notes this.

R4  Engineering risk: 2 of the top 3 outcomes (focus
    blocking + priority-aware slotting) require calendar
    write-back semantics that Northwind currently doesn't
    have. Estimated 1 engineer-quarter to introduce.
```

## Why this works

- **Used the 4-hour format deliberately.** 4 hours is the minimum format that allows all four schools (Christensen, Ulwick, Klement, Moesta) to land. A 2-hour workshop would have skipped the forces map; an 8-hour workshop would have added breadth without changing the top-3 conclusion.
- **Read switch interviews before the workshop.** The 4 hours were used for synthesis, not transcription. Without the pre-read, the first 90 minutes would have been spent re-discovering basic facts.
- **Worked through schools in sequence, not parallel.** Christensen first to anchor the job. Ulwick next to decompose. Klement to convert to actionable job stories. Moesta to map forces. Skipping the order produces hierarchies that don't match the underlying job.
- **Outcome scoring used opportunity score, not just importance.** The opportunity score (Importance + max(Importance - Satisfaction, 0)) is what surfaces underserved-but-important outcomes. Sorting by importance alone would have ranked "Reduce friction for client to find slot" higher; sorting by opportunity score surfaces "Block focus time" — because clients are already satisfied with the former.
- **Reframed competition.** The Christensen lens reframed competition as "email," not "Calendly." This is the single biggest mental-model shift the workshop produced. The team had been spec'ing features to compete with Calendly; the real opportunity is against email.
- **Anxiety force is non-product.** Rank 4 ("client experience reassurance") is honestly named as marketing/onboarding, not feature work. Less-experienced facilitators try to convert every Anxiety into a feature.
- **Refused to spec features.** The workshop output is jobs and outcomes. Features come from engineering scoping next week. Mixing them in the same room produces compromised outputs of both.

## What's next

- The 5 job stories feed [`../../execution/job-stories/`](../../execution/job-stories/) for backlog grooming.
- The top 3 opportunities feed [`../../execution/outcome-roadmap/`](../../execution/outcome-roadmap/) for next-quarter planning.
- The forces map informs [`../../execution/activation-funnel/`](../../execution/activation-funnel/) work on onboarding.
- The 3 follow-up switch-out interviews use [`../customer-interview-script/`](../customer-interview-script/) and then [`../interview-synthesis/`](../interview-synthesis/).
- The top-3 features each require an assumption map via [`../identify-assumptions/`](../identify-assumptions/) before commit.
- The full opportunity list goes into Confluence following [`../../confluence-expert/`](../../confluence-expert/) IA conventions.
