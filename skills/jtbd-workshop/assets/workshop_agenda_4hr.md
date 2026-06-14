# JTBD 4-Hour Half-Day Workshop Agenda

**Format:** 4-hour discovery workshop
**Output:** Ranked job hierarchy, ODI-scored outcomes, forces map for top job, 5-10 opportunity statements
**Participants:** 6-10 (full product trio + 2-3 customer-facing roles + at least 1 exec stakeholder)
**Required pre-work:** 4-6 switch interview transcripts read by all participants
**Facilitator:** PM or Researcher (consider co-facilitator pair)
**Materials:** Miro/FigJam board or printed canvases; timer; transcripts; sticky notes (physical or digital)

---

## 0:00 - 0:20 | Welcome + JTBD Primer (20 min)

- Round-robin intros (~30 sec each)
- Workshop goal: define the job hierarchy and ODI-scored outcomes for [segment]
- 5-minute JTBD primer:
  - The hiring frame: customers "hire" products to do jobs
  - Three layers we'll produce: job hierarchy (Christensen), outcomes (Ulwick), forces (Moesta)
  - The bridge to backlog: Klement job stories (When/Want/So) connect outcomes to features
- Ground rules:
  - No solutions during the morning blocks
  - No demographic framing
  - Every output must trace to customer voice
  - One job/pain/gain per sticky note

---

## 0:20 - 0:50 | Customer Voice Grounding (30 min)

- Read aloud Switch Interview Summary #1 (8 min)
- Discuss: what is this customer trying to accomplish? (4 min)
- Read aloud Switch Interview Summary #2 (8 min)
- Discuss (4 min)
- Pairs read summaries #3-4 silently and note top quotes (6 min)

---

## 0:50 - 1:10 | Individual Job Drafting (20 min)

- Silent writing: each participant writes 5-8 candidate job statements using the format:
  ```
  [Customer] is trying to [verb] [object] when [situation]
  so that [outcome].
  ```
- Each job on a separate sticky note

---

## 1:10 - 1:50 | Cluster + Build Job Hierarchy (40 min)

- All sticky notes on the board (5 min)
- Affinity clustering -- group near-duplicates (15 min)
- Identify the "big job" -- the highest-level outcome (5 min)
- Identify 5-8 sub-jobs that decompose the big job (10 min)
- Validate hierarchy against transcript quotes (5 min)

```
Example output:
  Big Job: Close the books accurately at month-end
    Sub-Job 1: Reconcile payment processor to GL
    Sub-Job 2: Investigate and fix mismatches
    Sub-Job 3: Generate audit trail
    Sub-Job 4: Onboard new team members to workflow
    Sub-Job 5: Communicate close status to CFO
```

---

## 1:50 - 2:00 | Break (10 min)

---

## 2:00 - 2:45 | Decompose Top 3 Sub-Jobs into Outcomes (45 min)

- Pick the top 3 sub-jobs by importance (dot vote, 5 min)
- For each (~13 min each):
  - Brainstorm 4-6 desired outcomes in Ulwick format:
    ```
    Minimize [time / effort / likelihood / number / cost] of
    [verb] [object] [context].
    ```
  - Quality test each statement (verb present? metric present? not a solution?)
- Capture 12-18 outcomes total

---

## 2:45 - 3:15 | Score Outcomes (Importance x Satisfaction) (30 min)

- For each outcome, score:
  - Importance (1-10): How important is this to the customer?
  - Satisfaction (1-10): How well are current solutions performing?
- Score from a specific named customer or from transcript evidence (5 min explanation)
- Pair scoring: pairs of participants score independently, then reconcile (20 min)
- Calculate opportunity score = Importance + max(0, Importance - Satisfaction) (5 min)
- Identify top 5 opportunities (highest scores)

---

## 3:15 - 3:45 | Forces-of-Progress Map for Top Job (30 min)

- For the #1 sub-job:
  - Push (current state pain) - 7 min
  - Pull (alternative attraction) - 7 min
  - Anxiety (switching worry) - 8 min
  - Habit (status quo tie) - 8 min
- Identify which forces are over- or under-invested

---

## 3:45 - 4:00 | Synthesis + Next Steps (15 min)

- Review artifacts produced:
  - Job hierarchy (1 big job + 5-8 sub-jobs)
  - 12-18 outcomes with ODI scores
  - Top 5 opportunities (high-score outcomes)
  - Forces-of-progress map for top job
- Assign owners for top 5 opportunities (named owner + 30-day next step)
- Define downstream hand-off (PRD, roadmap, experiments, assumption tests)
- Schedule a 30-day check-in

---

## Post-Workshop Deliverables

Within 48 hours, facilitator produces:

- One-page job hierarchy
- Outcome list with ODI scores (CSV or table)
- Top 5 opportunity statements with owners
- Forces-of-progress canvas (top job)
- Link to source switch interview transcripts

Hand off downstream:

- Top opportunities -> `discovery/identify-assumptions/` (validate riskiest assumptions)
- Top opportunities -> `discovery/brainstorm-experiments/` (design tests)
- Job hierarchy + outcomes -> `execution/create-prd/` Section 5 + 6
- Top desired outcomes -> `execution/outcome-roadmap/` (become roadmap themes)
- Job stories (Klement format) -> `execution/job-stories/` for backlog decomposition
