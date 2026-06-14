# JTBD Method Guide

A consolidated reference for the four JTBD schools used in the workshop: Christensen, Ulwick, Klement, Moesta.

---

## 1. Why JTBD exists

Traditional segmentation by demographics ("women aged 30-45", "enterprises with >1000 employees") fails to predict purchase behavior. Two demographically identical customers can buy completely different products because the underlying job they are trying to do differs.

JTBD shifts the frame from *who is the customer* to *what is the customer trying to accomplish*. Jobs are stable over time even as solutions, technologies, and demographics shift. A finance lead in 1980 hired a paper ledger; in 2000 hired a spreadsheet; in 2020 hired SaaS reconciliation -- same job, different hire.

---

## 2. Christensen: The Milkshake and the Hiring Frame

Clayton Christensen and colleagues introduced JTBD via the milkshake story (later popularized in *Competing Against Luck*, 2016). McDonald's wanted to grow milkshake sales and ran demographic studies that produced no insight.

Then the team asked: *what job are customers hiring this milkshake to do?* They discovered two distinct jobs:

- **Morning commute** (8am, single buyer, ordered with no extras, drank slowly): the milkshake was hired to make a boring commute interesting and to fight hunger until lunch. Competitors: bananas, bagels, donuts -- not other milkshakes.
- **Afternoon parent treat** (4pm, parent + child): the milkshake was hired to be a "yes" that felt indulgent for the kid while being containable for the parent. Competitors: candy bars, parental guilt.

Two completely different products needed -- one thicker (so the morning commute lasts), one smaller (so the afternoon doesn't ruin dinner).

### Key insights

- **A job is timeless.** The job of "make my commute less boring" existed before milkshakes and will outlast them.
- **Competition is defined by alternative hires, not category.** McDonald's competes with bananas.
- **Jobs have functional, social, and emotional dimensions.** The milkshake fights hunger (functional), signals self-care (social), and makes the commute pleasant (emotional).

### The Christensen job statement format

```text
[Customer] is trying to [verb] [object] when [situation]
so that [outcome / progress].
```

Example: "A finance lead is trying to reconcile payment data to the general ledger at month-end so that the books close accurately within 5 days."

---

## 3. Ulwick: Outcome-Driven Innovation (ODI)

Anthony Ulwick (founder of Strategyn) developed ODI in the 1990s, formalized in *What Customers Want* (2005) and *Jobs to Be Done: Theory to Practice* (2016).

Ulwick argues that a job statement alone is too abstract. You cannot prioritize features against "reconcile the books." You need *measurable desired outcomes*.

### The outcome statement format

```text
Minimize [time / effort / likelihood / number / cost] of
[verb] [object] [context].
```

Examples:

- "Minimize the **time** required to match payment records to invoices."
- "Minimize the **likelihood** of audit findings caused by reconciliation errors."
- "Minimize the **effort** required to onboard a new team member to the workflow."
- "Minimize the **number** of manual interventions during month-end close."

The strict verb set (minimize/maximize) and metric (time/effort/likelihood/number/cost) forces actionability. You can measure each outcome; you can score current solutions against each outcome.

### ODI scoring

Each outcome is scored on two dimensions, ideally via large-N customer survey:

- **Importance (1-10):** How important is achieving this outcome to the customer?
- **Satisfaction (1-10):** How well are current solutions performing on this outcome?

**Opportunity Score = Importance + max(0, Importance - Satisfaction)**

| Importance | Satisfaction | Opportunity Score | Interpretation |
|------------|--------------|-------------------|----------------|
| 9 | 4 | 14 | High-opportunity (important + underserved) |
| 9 | 8 | 9 | Saturated (important but already well-served) |
| 4 | 2 | 6 | Low-priority (unimportant; gap is irrelevant) |
| 9 | 9 | 9 | Saturated (delight territory; hard to differentiate further) |

Opportunity scores >= 12 typically indicate clear innovation targets.

### Outcome statement quality test

Before scoring, every outcome statement should pass:

- [ ] Starts with "Minimize" or "Maximize"
- [ ] Contains a measurable metric (time, effort, likelihood, number, cost)
- [ ] Specifies the verb-object-context
- [ ] Does not name a solution or feature
- [ ] Can be independently verified (you can imagine measuring it)

---

## 4. Klement: The JTBD Canvas and Job Stories

Alan Klement (*When Coffee and Kale Compete*, 2016) reframed JTBD for software product teams and introduced the situation-motivation-outcome structure that became the *job story* format.

### The Klement format

```text
When [situation],
I want to [motivation],
So I can [outcome].
```

Example:

```text
When I'm closing the books at month-end and I notice that my payment
processor data doesn't match the general ledger,
I want to identify the specific transactions causing the mismatch in
under 5 minutes,
So I can fix them before the CFO review.
```

The When/Want/So format is the bridge from the JTBD workshop to the backlog. Each top desired outcome can be decomposed into 2-4 job stories (different *situations* triggering the same motivation).

This format is the backbone of `execution/job-stories/`.

### The job story canvas

Klement also introduced a workshop canvas:

```
Job Statement (Christensen format)
  |
  +-- Job Stories (Klement format, multiple per job)
        |
        +-- Forces of Progress
        +-- Customer Constraints
        +-- Desired Outcomes
```

This canvas blends Christensen (job hierarchy), Klement (job stories), Moesta (forces), and Ulwick (outcomes).

---

## 5. Moesta: Switch Interviews and the Forces of Progress

Bob Moesta (collaborator with Christensen on milkshake work) developed the *switch interview* method. The switch interview is the most-used JTBD interview format in B2B software.

### The premise

A "switch" is the moment a customer hired your product (or fired a competitor). The switch is the highest-evidence moment in the customer's life -- they took action, spent money or time, and broke an existing habit. Reconstructing the switch reveals the four forces.

### Recruiting for switch interviews

- Customers who switched TO your product within 90 days (recent switchers)
- Customers who switched FROM your product to a competitor (churn switchers)
- Customers who considered switching and did not (non-switchers -- the forces that *prevented* the switch)

Three flavors of switch interview, each revealing different forces. A workshop ideally has at least one of each.

### The four-anchor timeline

| Anchor | Question | Force Revealed |
|--------|----------|----------------|
| First Thought | "When did you first think you needed something different?" | Push |
| Passive Looking | "What happened between then and starting to research?" | Latent push, re-trigger events |
| Active Looking | "When did you start actively comparing options?" | Pull of alternatives |
| Deciding | "Walk me through the conversation where you decided." | Anxiety, Habit |
| First Use | "First time you used it, what surprised you?" | Persistent anxiety, habit residue |

### The four forces

| Force | Direction | What it captures |
|-------|-----------|------------------|
| **Push of the situation** | Pro-switch | Pain of the current state; what makes the customer dissatisfied |
| **Pull of the new solution** | Pro-switch | Appeal of the alternative; what makes it desirable |
| **Anxiety of the new solution** | Anti-switch | Worry about the switch -- will it work? will I look bad? what's the cost? |
| **Habit of the present** | Anti-switch | Comfort with the current way; sunk cost; familiarity |

### The switch equation

A switch happens when:

```text
Push + Pull > Anxiety + Habit
```

### Strategic moves per force

| Force | Common over-investment | Higher-leverage move |
|-------|------------------------|----------------------|
| Push | Already obvious from the customer's pain | Sharpen messaging to remind them how bad the current state is |
| Pull | Most marketing here (feature lists, benefits) | Specific differentiation against named alternatives |
| Anxiety | Often ignored | Free trial, money-back guarantee, migration assistance, social proof, security certifications |
| Habit | Often ignored | Import tools, side-by-side comparison, "use both for 30 days" |

Most product teams over-invest in Pull and under-invest in reducing Anxiety and Habit. The leverage is in the latter two.

---

## 6. Putting it all together: the workshop logic

The four schools combine in a layered output:

```
Layer 1 (Christensen): The big job
   "Customer is trying to [verb] [object] when [situation]
    so that [progress]."
        |
Layer 2 (Klement): Sub-jobs as job stories
   "When [situation], I want to [motivation], so I can [outcome]."
        |
Layer 3 (Ulwick): Desired outcomes per job story
   "Minimize [time/effort/likelihood/number/cost] of [verb] [object] [context]"
   scored on Importance x Satisfaction
        |
Layer 4 (Moesta): Forces of progress for the top jobs
   Push, Pull, Anxiety, Habit
```

The workshop produces all four layers. The top layer (Christensen) is the strategic anchor. The bottom layer (Moesta) is the tactical playbook. The middle two layers bridge them.

---

## 7. Worked Example: Reconciliation Workflow

### Layer 1 -- Christensen Job

"A finance lead at a 100-500 person B2B SaaS is trying to close the books accurately when month-end approaches, so that the company has reliable financials within 5 working days."

### Layer 2 -- Klement Job Stories

- "When I'm closing the books at month-end and I notice my payment processor data doesn't match the general ledger, I want to identify the specific transactions causing the mismatch in under 5 minutes, so I can fix them before the CFO review."
- "When a transaction volume spike happens (e.g., end-of-quarter renewals), I want my reconciliation process to scale without breaking, so I can keep my 5-day close commitment."
- "When auditors request the reconciliation history, I want to produce a complete audit trail in under an hour, so I can satisfy the audit without delaying other work."

### Layer 3 -- Ulwick Outcomes (sampled with scores)

| Outcome | Importance | Satisfaction | Opportunity |
|---------|------------|--------------|-------------|
| Minimize the time to match payment records to invoices | 9 | 3 | 15 |
| Minimize the likelihood of audit findings from reconciliation | 9 | 5 | 13 |
| Minimize the effort to onboard a new finance team member | 7 | 4 | 10 |
| Minimize the number of manual interventions per close | 8 | 4 | 12 |
| Minimize the cost of running the reconciliation workflow | 6 | 7 | 6 (saturated) |

Top opportunities: time to match, audit findings, manual interventions. Cost is saturated (not a differentiator).

### Layer 4 -- Moesta Forces (for the top job, "close the books accurately")

**Push (current state pain):**
- 11 hours of manual matching per close
- 2 audit findings last year tied to reconciliation errors
- CFO publicly frustrated during month-end

**Pull (new solution attraction):**
- 60-second automated matching
- Audit log with rule-level traceability
- 2-day close instead of 5-day

**Anxiety (worry about switching):**
- "What if the automation misses something?"
- "What if my CFO doesn't trust the new system?"
- "Implementation might take longer than the time it saves"

**Habit (tied to current way):**
- Existing spreadsheet workflows trained team members rely on
- Reports formatted in specific way for auditor
- Personal pride in "knowing the data" through manual review

**Strategic moves:**
- Reduce anxiety: include a 90-day side-by-side reconciliation; offer a "shadow run" before cutover
- Reduce habit: provide spreadsheet export of automated matches so the existing review workflow still applies
- Sharpen push: marketing emphasizes audit-finding risk with specific examples

---

## 8. References

- Christensen, Clayton M.; Hall, Taddy; Dillon, Karen; Duncan, David S. *Competing Against Luck*. HarperBusiness, 2016.
- Ulwick, Anthony W. *What Customers Want*. McGraw-Hill, 2005.
- Ulwick, Anthony W. *Jobs to Be Done: Theory to Practice*. Idea Bite Press, 2016.
- Klement, Alan. *When Coffee and Kale Compete*. NYC Publishing, 2016.
- Moesta, Bob; Spiek, Chris. *Demand-Side Sales 101*. Lioncrest, 2020.
- Spiek, Chris; Moesta, Bob. *The Jobs-to-be-Done Handbook*. Re-Wired Group, 2014.
- Wunker, Stephen; Wattman, Jessica; Farber, David. *Jobs to Be Done: A Roadmap for Customer-Centered Innovation*. AMACOM, 2016.
