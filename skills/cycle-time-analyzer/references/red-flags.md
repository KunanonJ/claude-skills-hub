# Red Flags: Cycle Time Analyzer

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan the `flow_metrics.py` output before sharing in retro or exec review. Each red flag shows the *bad* version next to the *good* version, anchored to Daniel Vacanti's flow metrics and Little's Law.

---

## Red Flag 1: Optimizing for the wrong percentile

**Symptom.** Team reports "average cycle time: 4 days, looking great". Variance is huge — 20% of items take 14+ days.

**Why it's bad.** Vacanti's central argument: report cycle time as a distribution (50th, 85th, 95th percentile), never as an average. The mean hides the long tail; commitments based on the mean miss 30-40% of the time. The team commits to "4 days" and ships 30% of items in 14 days, then is surprised when stakeholders complain.

**Bad example:**
> "Sprint metrics summary: 'Average cycle time 4.1 days. Throughput 6/week. Stable and healthy.'"

**Good example:**
> "Cycle time distribution (Vacanti style): p50 = 4 days, p85 = 11 days, p95 = 18 days. 'We finish half our work in 4 days but the long tail extends to 18 days; commitments at p50 will miss 50% of the time. Use p85 for stakeholder commitments.' Throughput: 6/week (range 3-9 across last 8 weeks)."

**How to catch it.** Look at the metrics output. If only `average` or `mean` appears (no `p85` or `p95`), the distribution is hidden.

---

## Red Flag 2: Ignoring aging WIP

**Symptom.** Daily standup reads the same 4 in-progress tickets each day. Nobody talks about the one that has been "In Progress" for 23 days.

**Why it's bad.** Aging WIP is the single most actionable flow metric for daily use. Items older than the team's p85 cycle time are statistical outliers — they will keep aging unless someone intervenes. Ignoring them means the team's actual cycle time is worse than reported, hidden in a few quiet long tails.

**Bad example:**
> "Standup: each engineer goes through their tickets. ENG-117 'still investigating' — same answer every day for 3 weeks. No one flags it."

**Good example:**
> "Standup opens with aging WIP report (auto-generated): 'ENG-117 in 'In Progress' for 23 days (p85 cycle time is 11 days; this is 2x outlier). Bartek to triage in 30 min after standup.' At triage: close it, split it, restart it, or escalate. ENG-117 either advances or is killed within 48 hours."

**How to catch it.** Pull the aging WIP list. Any item > 1.5x team's p85? If yes and it's not on the standup agenda, aging is being ignored.

---

## Red Flag 3: Flow metrics used to rank individuals

**Symptom.** "Engineer A's average cycle time is 3 days; Engineer B's is 7 days; we should coach B."

**Why it's bad.** Flow metrics are team-level signals. Per-assignee cycle time produces local optimization (engineers avoid hard tickets, hand off prematurely, gaming starts) and destroys team behavior. Vacanti and Anderson are explicit: do not use these metrics to evaluate individuals.

**Bad example:**
> "Quarterly perf review for Engineer B: 'Your average cycle time of 7 days is double the team average. Improve velocity.'"

**Good example:**
> "Flow metrics are reported team-level only. Engineer B happens to take on the most complex bugs and architecturally-risky stories — that's by design. Performance reviews use different signals (peer feedback, design quality, mentorship). Tooling does not expose per-assignee cycle time."

**How to catch it.** Look at where flow metrics are reported. If they appear in any performance review document, the line has been crossed.

---

## Red Flag 4: "In Progress" defined too narrowly

**Symptom.** Cycle time looks low (median 3 days). Team feels slow. Long "In Review" and "Blocked" periods are excluded from the calculation.

**Why it's bad.** The team's lived experience is the total time from "start" to "finish". If the metric excludes Review and Blocked, it understates real cycle time. The team distrusts the data because it does not match reality.

**Bad example:**
> "Config: `--in-progress-state 'In Progress'`. Median cycle time: 3.2 days. Team morale: 'these numbers can't be right.'"

**Good example:**
> "Config: `--in-progress-state 'In Progress' --in-progress-state 'In Review' --in-progress-state 'Blocked'`. Median cycle time: 6.8 days. Team validates: 'this matches what we feel.' Decision: investigate 'In Review' (mean 2.1 days) as the constraint."

**How to catch it.** Ask the team: "does the metric match what you feel?" If no, the state mapping is wrong.

---

## Red Flag 5: WIP limits set by guess, not by data

**Symptom.** Team adopts WIP=5 per engineer based on "feels right" rather than the team's current histogram.

**Why it's bad.** Little's Law: Throughput = WIP / Cycle Time. WIP limits below the team's current 50th percentile aggressively reduce cycle time but cause queue starvation upstream. Above the team's 85th percentile and they have no effect. Calibrating by guess produces no improvement.

**Bad example:**
> "Team standardizes on WIP limit = 5 per engineer because 'that feels manageable'."

**Good example:**
> "WIP histogram analysis: team currently averages 3.2 in-flight items per engineer, with 85th percentile at 5. New WIP limit set at 3 per engineer (just below current 50th percentile). Goal: force finishing before starting. Re-measure cycle time after 4 weeks; expect 15-25% reduction if Little's Law holds."

**How to catch it.** Ask: "how was this WIP limit set?" If the answer doesn't reference the team's actual WIP distribution, it's a guess.

---

## Red Flag 6: Story-point velocity as the primary metric

**Symptom.** Team reports "30 SP velocity, 95% completion rate" but ships less actual work than 3 quarters ago when they reported 22 SP.

**Why it's bad.** Story points are subject to estimation drift — teams inflate estimates over time. Vacanti's argument: count throughput (atomic completed units), not story points. Throughput is bias-resistant. Comparing SP-velocity over quarters compares two different yardsticks.

**Bad example:**
> "Q3 review: '30 SP velocity, up from 22 in Q2. Team is shipping more.' Engineering complains: 'we feel slower than ever.'"

**Good example:**
> "Q3 review: 'Throughput 6.2 items/week (Q2: 6.8). SP velocity increased because estimates inflated. Real picture: throughput flat, with longer-tail outliers in Q3. Investigate the 2 stories that took > p85 cycle time; they consumed 30% of capacity.'"

**How to catch it.** Compare throughput trend (items/week) to SP trend. Divergence means SP estimates are drifting.

---

## Red Flag 7: Goodhart's gaming

**Symptom.** A month after introducing cycle-time targets, the team's median cycle time drops from 6 days to 3.5 days. Throughput also drops. Customers don't notice improvement.

**Why it's bad.** Goodhart's Law: when a measure becomes a target, it ceases to be a good measure. Teams game cycle time by splitting work artificially, marking tickets "done" before they truly are, or skipping review. The number goes down; real delivery does not improve.

**Bad example:**
> "OKR: 'reduce median cycle time from 6 days to 3 days by Q3 end.' Team hits 3 days. Throughput drops 20%. Customer-visible regressions up 3x. 'But the metric is green!'"

**Good example:**
> "Cycle time is a diagnostic, not a target. Quarterly review tracks the trend across 3 metrics: cycle time p85, throughput, and quality (escaped defects, customer-reported regressions). If cycle time drops but throughput or quality also drops, the gaming hypothesis is on the table. Goal is to lower cycle time *while sustaining* throughput and quality."

**How to catch it.** Look at cycle time trend together with throughput and quality trends. If cycle time improves and the others degrade, gaming is suspected.

---

## Red Flag 8: Mixed work types reported together

**Symptom.** "Median cycle time 4.5 days" — but the team mixes bugs (median 1 day), features (median 6 days), and spikes (median 9 days) in one number.

**Why it's bad.** Predictability comes from like-with-like comparison. A team that ships 70% bugs in March and 70% features in April will show cycle-time "improvement" in March that's actually mix shift, not improvement.

**Bad example:**
> "March: median 3 days. April: median 6 days. 'We got slower.' (Actually: March was 80% bug-fix sprint; April was 80% feature sprint. Like-with-like cycle time was unchanged.)"

**Good example:**
> "Cycle time reported per work type: bugs (p50 1.2d, p85 3d), features (p50 6d, p85 11d), spikes (p50 4d, p85 9d). Trends compared within type. Mix-adjusted overall trend shown separately."

**How to catch it.** Look for `--type` filtering in the report. If everything is aggregated, mix shift is hidden.

---

## Red Flag 9: Lead time conflated with cycle time

**Symptom.** Exec asks "how long does it take you to ship a feature?" Team answers 6 days (cycle time). Customer-perceived time from request to delivery is 11 weeks (lead time).

**Why it's bad.** Lead time is the customer view ("from when I asked to when I got it"). Cycle time is the team view ("from when we started to when we finished"). They are different metrics. Reporting cycle time as the answer to a lead-time question creates expectation mismatches.

**Bad example:**
> "Exec: 'how long to ship this?' Team: '6 days.' Exec messages customer: '6 days.' Customer's actual experience: 11 weeks because the item sat in backlog for 10 weeks before starting."

**Good example:**
> "Exec: 'how long to ship this?' Team: 'Cycle time p85 is 11 days once we start. Lead time p85 — from when the request entered the backlog — is 52 days because the backlog is currently 6 weeks deep. If you want to commit a customer to a date, use lead time.' Exec commits 11 weeks; customer is pleasantly surprised at 7."

**How to catch it.** Per stakeholder, which metric matters? Customers care about lead time. Engineering planning cares about cycle time. Report both with labels.

---

## Red Flag 10: CFD shown without context

**Symptom.** Cumulative Flow Diagram is shared in retro. Engineers stare at it. Nobody can act on it.

**Why it's bad.** A CFD is information-dense; without annotation and a narrative, it's noise. Bands widening = WIP growing. Bands flattening = throughput dropping. Without the team knowing what to look for, the diagram does not produce action.

**Bad example:**
> "Sprint retro slide: CFD chart. Caption: 'here is our CFD.' Team: 'okay.'"

**Good example:**
> "CFD with annotations: 'Note widening of 'In Review' band starting Week 12 — review backlog growing. Throughput in Week 13 dropped from 7/week to 4/week, coinciding with two engineers on PTO. Discussion: should we cap concurrent reviews per engineer to prevent recurrence?' Specific narrative + 1 question to discuss."

**How to catch it.** Read the retro deck. Does the CFD have annotations and a discussion question? If not, it's decoration.

---

## Red Flag 11: Throughput trend reported as a single sprint number

**Symptom.** Status update reads "Sprint 23 throughput: 6 items". Next sprint: 4. Next: 9. Each reported in isolation.

**Why it's bad.** Single-sprint numbers fluctuate wildly with vacations, holidays, scope of work. Trends only emerge over 6-8 sprints. Reporting one-sprint snapshots leads to false-alarm panics and false-celebration parties.

**Bad example:**
> "Sprint 24 update: 'Throughput dropped to 4 items this sprint, down from 6. Investigating slowdown.'"

**Good example:**
> "Sprint 24 update: 'Throughput 4 items this sprint. 8-week rolling: 5.8 items/week (range 3-9). Sprint 24 is within normal variance; no investigation needed. Trend is stable.' Annotations: '2 engineers on PTO this sprint.'"

**How to catch it.** Is the throughput metric reported as a single number or as a trend with a window? Single = noise.

---

## Red Flag 12: Long-stuck items hidden in backlog states

**Symptom.** Backlog has 80 items. Nobody knows that 18 of them have been in "Backlog" for over 12 months. Lead time on those is meaningless but they pollute the data.

**Why it's bad.** Stale backlog items inflate lead time without representing real work. They also distort prioritization — the team thinks they "have a lot of work" when 25% of the queue is dead. Vacanti's discipline: prune the backlog regularly; report lead time only for items committed within the last quarter.

**Bad example:**
> "Lead time p85: 142 days. 'We are slow.' (Reality: 18 items have been in backlog for 400+ days and skew the distribution.)"

**Good example:**
> "Quarterly backlog hygiene: items in 'Backlog' state > 90 days reviewed; 18 closed as stale ('no longer aligned with strategy'), 4 split into smaller stories. Lead time p85 recomputed on committed-in-last-quarter cohort: 38 days."

**How to catch it.** Filter backlog items by age. If > 20% of the backlog is older than 6 months, lead time is being polluted.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Optimizing for the wrong percentile | Is p85 (or p95) shown alongside the median? |
| 2 | Ignoring aging WIP | Is aging WIP report part of standup? |
| 3 | Per-individual ranking | Does any perf review document show per-assignee cycle time? |
| 4 | "In Progress" too narrow | Does the metric match the team's felt experience? |
| 5 | WIP limits by guess | Was the WIP limit calibrated to the team's distribution? |
| 6 | Story-point velocity as primary | Throughput trend vs SP trend — diverging? |
| 7 | Goodhart's gaming | Did cycle time improve while throughput/quality dropped? |
| 8 | Mixed work types together | Is cycle time reported per type? |
| 9 | Lead time vs cycle time confusion | Which metric matters for this stakeholder? |
| 10 | CFD without context | Does the CFD have annotations + a discussion question? |
| 11 | Single-sprint throughput | Is the trend reported with a rolling window? |
| 12 | Stale backlog polluting lead time | What % of backlog is > 6 months old? |

## Related Reading

- SKILL.md Troubleshooting
- references/flow-metrics-guide.md
- Daniel Vacanti, *Actionable Agile Metrics for Predictability* (2015)
- Daniel Vacanti, *When Will It Be Done?* (2020)
- `scrum-master/` (for SP velocity and Monte Carlo forecasting)
- `dependency-map/` (for cross-team coordination affecting cycle time)
