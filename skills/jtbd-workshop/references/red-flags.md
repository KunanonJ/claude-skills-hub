# Red Flags: JTBD Workshop

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them. Pair with the SKILL.md and Troubleshooting table.

## How to use this document

When you have just facilitated or designed a JTBD workshop, scan the red flags below before publishing the job hierarchy or forces map. Each red flag shows the *bad* and *good* version, anchored in Christensen, Ulwick, Klement, and Moesta's JTBD lineages.

---

## Red Flag 1: Jobs That Are Just Features (Solution-Coded Jobs)

**Symptom.** Workshop output lists "jobs" like "use our calendar feature" or "open the AI assistant." These are solutions, not jobs.

**Why it's bad.** A job (Christensen) is the underlying progress the customer is trying to make, independent of any solution. "Use our calendar" is product usage; "schedule a recurring team meeting without double-booking anyone" is a job. Confusing the two locks the team into one solution and misses the broader competitive set.

**Bad example:**
> "Job: Use our analytics dashboard."

**Good example:**
> "Job: 'When a leadership review is coming up, I want to know which metrics are off-track so I can prepare an explanation.' (Solution-agnostic; could be solved by dashboard, email digest, ChatGPT analysis, or a junior analyst.)"

**How to catch it.** Does the job statement name a tool, feature, or interface? If yes, you wrote a usage statement, not a job.

---

## Red Flag 2: Missing the Forces of Progress

**Symptom.** Workshop produces a job hierarchy but no forces-of-progress map. Team knows what customers are trying to do but not what drives or blocks the switch.

**Why it's bad.** Moesta's four forces (push, pull, anxiety, habit) are the operational core of JTBD. Push (what is broken today) + pull (what attracts to the new) drive switching; anxiety (worry about the new) + habit (comfort with the old) resist. Without forces, you cannot predict whether customers will actually switch to your solution.

**Bad example:**
> Workshop output: 12 jobs. No forces map.

**Good example:**
> Workshop output: 5 priority jobs. For each, a forces map. For top job: Push = 'reports take 2 hours every Monday'. Pull = 'auto-generated drafts'. Anxiety = 'what if it gets numbers wrong?'. Habit = 'I trust my Excel formulas.' Highest force: anxiety. First experiment: build trust signals (confidence intervals, source links) before optimizing speed."

**How to catch it.** Does the workshop output include a forces map for at least the top job? If not, you mapped jobs without their dynamics.

---

## Red Flag 3: No Switch Interviews (Speculation Instead of Evidence)

**Symptom.** Workshop team brainstorms what customers' jobs are, based on team knowledge. No actual switch interviews conducted.

**Why it's bad.** Christensen's milkshake and Moesta's switch method are evidence-based. Speculation produces team consensus on what customers *should* want; only switch interviews reveal what they actually do. A workshop without switch data is internal opinion-fest dressed in JTBD vocabulary.

**Bad example:**
> "We discussed who our customers are and what jobs they have. Settled on these 8 jobs."

**Good example:**
> "Conducted 6 switch interviews (3 with users who switched to us, 3 with users who switched away) prior to workshop. Workshop synthesized switch data into 5 jobs with forces. Each job traceable to specific interview moments."

**How to catch it.** How many switch interviews informed the workshop? If zero, the output is hypothesis, not synthesis.

---

## Red Flag 4: Job Statements Without "When" (Missing Situation)

**Symptom.** Job statements: "I want to be more productive." "I want to save time." No situational trigger.

**Why it's bad.** Klement's situation-motivation-outcome (SMO) format requires the *when* — the situation that triggers the job. Jobs without situation are universal aspirations, not actionable opportunities. "Saving time" is everyone's job everywhere; it leads nowhere.

**Bad example:**
> "Job: I want to be more productive."

**Good example:**
> "When (situation): a customer email comes in at 9pm and I am on my phone. I want to (motivation): respond with the right context without opening my laptop. So I can (outcome): close the loop before the next morning without sacrificing my evening."

**How to catch it.** Does every job statement include a specific situation? If not, the job is too abstract to act on.

---

## Red Flag 5: Outcome Statements That Are Not Measurable

**Symptom.** Ulwick's ODI calls for measurable desired outcomes. Workshop produces outcome statements like "make the user feel valued" or "improve the experience."

**Why it's bad.** Ulwick's whole framework rests on outcomes being *measurable* — importance and satisfaction can only be scored if the outcome is concrete. Fuzzy outcomes produce fuzzy prioritization.

**Bad example:**
> "Desired outcome: 'Make customers feel valued.'"

**Good example:**
> "Desired outcome: 'Minimize the time it takes to identify which deal is at risk this week.' Measurable: cycle time from data-update to risk-flag. Currently 45 min average; target <5 min. Importance 9, satisfaction 3 -> opportunity score 15."

**How to catch it.** Could you measure the outcome with a stopwatch, count, percentage, or dollar value? If not, the outcome is fuzzy.

---

## Red Flag 6: Facilitation Failure — Loudest Voice Wins

**Symptom.** Workshop is a free-form discussion. The senior PM or VP dominates; quieter participants do not contribute. Output reflects the loudest voice's view of customer jobs.

**Why it's bad.** JTBD workshops require diverse input. The most useful jobs come from engineers, support reps, and salespeople who hear the customer language daily. A workshop that filters everyone through the senior voice produces a narrow, executive-confirming output.

**Bad example:**
> Workshop: open discussion, senior PM speaks 60% of the time, output reflects PM's pre-workshop view.

**Good example:**
> Workshop: silent generation (5 min individual writing) before any group discussion. Round-robin sharing. Affinity clustering with sticky-note voting. Facilitator explicitly invites support and engineering voices."

**How to catch it.** Did everyone in the workshop contribute at least 3 sticky notes? If some contributed zero, facilitation failed.

---

## Red Flag 7: Job Hierarchy Without Ranking

**Symptom.** 12 jobs listed, all equal. No importance scoring, no segment-fit assessment.

**Why it's bad.** A flat job list is unrankable. Ulwick's ODI explicitly produces importance + satisfaction scores; without them, the team has no basis for prioritization. The hierarchy is in the SKILL.md output for a reason.

**Bad example:**
> Job list: 12 jobs, no scores.

**Good example:**
> Job hierarchy: 12 jobs, each scored on importance (1-10) and current satisfaction (1-10). Opportunity score = importance + max(0, importance - satisfaction). Top 3 jobs by opportunity score advance to roadmap. Bottom 4 jobs (low importance) parked."

**How to catch it.** Is there a ranking column with numerical scores? If all jobs look equal, you produced inventory.

---

## Red Flag 8: Mixing Functional, Social, and Emotional Without Distinction

**Symptom.** Job list lumps functional jobs ("complete the reconciliation") together with social ("look competent") and emotional ("avoid month-end dread") without distinction.

**Why it's bad.** Different job dimensions require different solutions. A social job ("look competent in front of finance director") may need a polish/presentation layer that solving the functional job alone misses. Christensen's full model includes all three; collapsing them flattens the solution space.

**Bad example:**
> "Jobs: Complete reconciliation. Look smart. Feel less stressed." (Listed as a flat list.)

**Good example:**
> "Functional: Complete the reconciliation accurately. Social: Look competent in the month-end review meeting. Emotional: Avoid the dread of month-end close. Top 1 solution candidate must address all three (e.g., automated reconciliation + audit-ready report + early-warning alerts that prevent surprises)."

**How to catch it.** Each job tagged with functional / social / emotional? If only functional are listed, you missed two dimensions.

---

## Red Flag 9: Switch Story Treated as Anecdote, Not Pattern

**Symptom.** One customer tells a compelling switch story. Team uses it as the canonical narrative for the segment without checking whether the pattern repeats.

**Why it's bad.** N=1 is anecdote. Moesta recommends multiple switch interviews to find the *pattern* — the recurring forces across customers, not the specific story of one. Anecdote-driven JTBD locks the team onto an unrepresentative narrative.

**Bad example:**
> "Customer X switched from competitor to us because of feature Y. This is our story for the segment."

**Good example:**
> "6 switch interviews. Common pattern across 4 of 6: push = competitor's reporting delays, pull = our real-time dashboards, anxiety = data-migration risk, habit = 'we have always used X.' One outlier (price-driven switch) noted but not generalized."

**How to catch it.** How many switch interviews support the dominant narrative? Fewer than 4 = anecdote risk.

---

## Red Flag 10: Conflating Buyer and User Jobs

**Symptom.** Workshop output treats "the customer" as one persona. In reality, the buyer (procurement, finance) and the user (operator) have different jobs.

**Why it's bad.** B2B JTBD has separate buyer and user jobs that often conflict. The buyer hires the product to reduce vendor risk; the user hires it to do their daily work. Solutions optimized for one fail the other. JTBD workshops for B2B must explicitly separate them.

**Bad example:**
> "Customer job: 'Get reports done faster.'" (Buyer is a CFO; user is a financial analyst. CFO wants compliance; analyst wants speed.)

**Good example:**
> "Buyer job (CFO): 'Demonstrate financial controls to auditors with minimal effort.' User job (analyst): 'Get reports done by Friday without weekend work.' Solution must serve both: speed for analyst, audit trail for CFO."

**How to catch it.** For B2B contexts, did you separate buyer from user? If they are one persona, you compressed.

---

## Red Flag 11: Workshop Format Mismatched to Maturity

**Symptom.** 2-hour workshop attempted for a 0-to-1 new-product question. Or 8-hour workshop attempted for a known segment with abundant existing data.

**Why it's bad.** The SKILL.md offers 2/4/8-hour formats because different questions require different depths. 2-hour formats work for known segments; 8-hour formats are needed for new segments or strategy resets. Mismatch produces shallow output or wasted time.

**Bad example:**
> 2-hour workshop on entering a new vertical the team has zero customer data on.

**Good example:**
> 8-hour workshop (2 days, 4 hours each) for new vertical. Day 1: switch interviews review + initial job hypothesis. Day 2: forces map + outcome statements + opportunity ranking. Pre-work: 5 switch interviews completed."

**How to catch it.** Does the workshop length match the question's complexity? New segments need at least 4-8 hours; refinement work can do 2.

---

## Red Flag 12: Workshop Output Has No Owner for Operationalization

**Symptom.** Workshop produces 5 priority jobs. Two weeks later, nothing has happened. The job statements live on a Miro board.

**Why it's bad.** Workshop output is upstream of PRDs, OKRs, and roadmaps. Without an owner to translate jobs into product decisions, the workshop's value evaporates. Discovery work that does not change downstream artifacts is theater.

**Bad example:**
> Workshop ends. Jobs documented in Miro. No owner. No follow-up plan.

**Good example:**
> Workshop ends. PM owns: translate top job into Q+1 OKR (due Friday); revise the roadmap to anchor on top 3 jobs (due in 2 weeks); draft a PRD for the top experiment (due in 3 weeks). Review cadence: monthly check-in for 1 quarter."

**How to catch it.** What changes in the team's artifacts (OKRs, roadmap, PRD) within 4 weeks of the workshop? If nothing, the workshop did not land.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Jobs Are Just Features | Job statement is solution-agnostic? |
| 2 | Missing Forces of Progress | Forces map for top jobs? |
| 3 | No Switch Interviews | Workshop informed by 4+ switch interviews? |
| 4 | No Situation in Job | Each job includes specific "when"? |
| 5 | Outcomes Not Measurable | Could you measure with stopwatch/count/percent? |
| 6 | Loudest Voice Wins | Everyone contributed 3+ notes? |
| 7 | Hierarchy Not Ranked | Importance + satisfaction scores per job? |
| 8 | Functional Only | Functional + social + emotional tagged? |
| 9 | Switch Story as Anecdote | Pattern across 4+ switch interviews? |
| 10 | Buyer/User Conflated | B2B: buyer and user jobs separated? |
| 11 | Format Mismatched | Workshop length matches question depth? |
| 12 | No Owner | Downstream artifacts change within 4 weeks? |

## Related Reading

- SKILL.md Troubleshooting section (for symptom -> root cause -> resolution)
- references/forces-of-progress.md (for Moesta's four forces, if present)
- references/odi-outcome-statements.md (for Ulwick's measurable outcomes, if present)
- customer-interview-script/references/red-flags.md (for switch-interview craft)
- value-proposition-canvas/references/red-flags.md (for jobs/pains/gains mapping)
