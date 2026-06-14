# Red Flags: DACI Framework

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan the DACI chart before publishing or running a decision under it. Each red flag shows the *bad* version next to the *good* version, anchored to the Driver / Approver / Contributor / Informed role rules.

---

## Red Flag 1: Too many Approvers (gridlock by design)

**Symptom.** A decision row lists 4 Approvers. Decision sits for 6 weeks waiting for sign-off.

**Why it's bad.** Approvers have veto power. Each additional Approver multiplies the chance of stall. The DACI rule is 1-2 Approvers max — beyond that, the decision becomes consensus-by-veto, which is the opposite of clarity.

**Bad example:**
> "Decision: Backlog priorities. Approvers: VP Product, VP Eng, VP Marketing, CFO. (Decision pending since Q1; quarter ending; no movement.)"

**Good example:**
> "Decision: Backlog priorities. Driver: PM (Sarah K). Approver: VP Product (David T) — sole approval. Contributors: VP Eng (capacity input), VP Marketing (GTM input), CFO (budget input). Informed: exec team. Decision SLA: 5 business days from Driver proposal."

**How to catch it.** Count `A` cells per row. > 2 = the row is built to stall.

---

## Red Flag 2: Driver-by-committee

**Symptom.** A row shows D in two cells: PM and PMM both "drive" the launch decision.

**Why it's bad.** "Every decision has exactly one Driver" is the central DACI principle. Two Drivers means nobody is driving — each waits for the other; both blame the other when nothing moves. The decision becomes unowned.

**Bad example:**
> "Decision: GTM strategy. PM: D. PMM: D. Approver: VP Product. (Decision unresolved 8 weeks; PM thinks PMM is leading; PMM thinks PM is leading.)"

**Good example:**
> "Decision: GTM strategy. Driver: PMM (Jorge M) — accountable for process + timeline. Contributor: PM (Sarah K) — provides product context and launch dependency. Approver: VP Product. Single named owner; PMM runs the meeting and writes the memo."

**How to catch it.** Count `D` cells per row. > 1 = no Driver.

---

## Red Flag 3: Driver lacks authority

**Symptom.** Driver is a Junior PM. Approver is the CEO. Driver runs the meeting; CEO ignores Driver's framing and decides unilaterally.

**Why it's bad.** Authority follows the role's title. A Driver junior to the decision's stakes will be steamrolled. The DACI chart looks valid on paper; in practice, decisions skip the Driver entirely. Other teams learn the chart is decoration.

**Bad example:**
> "Decision: Architecture. Driver: Sr Eng (3y tenure). Approver: CTO. (Meeting reality: CTO walks in, restates the question, picks an answer; Driver thanks the team and goes home.)"

**Good example:**
> "Decision: Architecture. Driver: Eng Manager (peer of CTO's direct reports). Approver: CTO. Driver has the standing to push back on the Approver in the room. If the role's natural Driver is too junior for the stakes, escalate the Driver role (not the decision)."

**How to catch it.** Ask the Driver: "could you tell the Approver 'no, here is why' and have it land?" If not, the Driver lacks authority.

---

## Red Flag 4: Informed treated as Approver

**Symptom.** Marketing was marked I (Informed) on the launch-date decision. Three days before launch, Marketing objects and the date slips.

**Why it's bad.** Late objections destroy DACI. Informed means notified, not consulted. If Marketing has objection rights, they should have been Contributor or Approver from the start. The chart promised one thing; behavior delivered another.

**Bad example:**
> "Launch decision: Driver PM, Approver VP Product, Marketing as I. (T-3: 'wait, Marketing can't support this date'. Slip 2 weeks.)"

**Good example:**
> "Launch decision: Driver PM, Approver VP Product, Contributor PMM (input on GTM readiness), Contributor Marketing (input on demand-gen capacity), Informed: rest of team. PMM and Marketing get to weigh in at T-30 and T-21; their concerns shape the date. After date-lock at T-21, they cannot reopen at T-3 without escalating to the Approver."

**How to catch it.** When a role objects late, ask: "what was their DACI role?" Marketing-as-I objecting at T-3 is a chart violation.

---

## Red Flag 5: Everyone is a Contributor

**Symptom.** Most cells in the chart are C. Team uses "everyone contributes" as a default to avoid hard accountability conversations.

**Why it's bad.** Defaulting to C is a polite refusal to assign accountability. The chart loses information; nothing is signal because everything is signal. Decisions slow because everyone expects to be consulted.

**Bad example:**
> "DACI chart: 10 decisions × 8 roles. 70% of cells are C. (Everyone feels included; no one feels accountable.)"

**Good example:**
> "DACI chart: 10 decisions × 8 roles. Per decision: 1 D, 1 A, 3-4 C maximum, rest I (or blank). C is reserved for roles with substantive expertise to add. If a role has nothing to contribute, leave the cell blank or mark I — do not default to C to 'be polite'."

**How to catch it.** Count C cells per row. > 5 C's = the row is consensus theater.

---

## Red Flag 6: DACI built but never referenced

**Symptom.** Chart published in Confluence. Six months later, no team meeting has referenced it. New joiners do not know it exists.

**Why it's bad.** A DACI chart that nobody references provides no clarity. Decision velocity is whatever it was before; the document is a fossil. The exercise of building it produced alignment in the room; the artifact produces nothing afterward.

**Bad example:**
> "DACI built March 1; last referenced March 5 (in the meeting that built it). Decision X stalled in May with three people debating ownership; nobody opened the chart."

**Good example:**
> "DACI is referenced at: (1) every kickoff meeting for new initiatives ('per the DACI, the Driver here is …'); (2) onboarding for new joiners (1-hour walkthrough); (3) escalations ('we are in conflict; per the chart, the Approver is …'). Chart link pinned in the team channel. Quarterly review and refresh."

**How to catch it.** Open the chart. When was it last referenced? Last-modified date alone is not enough — was it actually used?

---

## Red Flag 7: Approvers overrule without explanation

**Symptom.** Driver proposes; Approver vetoes with "I don't think so". No written rationale. Two months later, the decision recurs because the team doesn't understand why option A was killed.

**Why it's bad.** Veto without explanation undermines authority. The team cannot learn the Approver's pattern; the same debate recurs. Worse, junior team members generalize ("Approver hates option A") and self-censor on adjacent decisions.

**Bad example:**
> "Driver: 'I propose option A.' Approver: 'No.' [End of meeting. No written follow-up.]"

**Good example:**
> "Driver proposes option A in a 1-page memo. Approver responds in writing: 'Vetoing. Three reasons: (1) data privacy concern around X; (2) conflict with our enterprise positioning; (3) prefer option B because of Y. Open to a counter-proposal that addresses 1 and 2.' Rationale becomes a decision record."

**How to catch it.** Look at the last 5 vetoes. Did each have a written rationale? If no, the Approver is exercising veto without accountability.

---

## Red Flag 8: New decisions never added to chart

**Symptom.** DACI built at team formation. Six new decision categories have emerged. None are on the chart.

**Why it's bad.** A static DACI ages out. Teams take on new responsibilities — pricing changes, AI feature decisions, partnership reviews — and the chart silently becomes incomplete. New decisions get assigned ad-hoc; ad-hoc assignment is what DACI was supposed to replace.

**Bad example:**
> "DACI v1 covers 12 decisions. Team has added AI feature scope, pricing experiments, and customer-data partnerships since. None on the chart."

**Good example:**
> "DACI v3 (current). Quarterly refresh adds new decision categories: 'AI feature scope (Driver: PM, Approver: VP Product + Safety lead)', 'Pricing experiments (Driver: PM, Approver: VP Product, Contributors: Finance, Legal)'. Refresh date logged; outdated rows removed."

**How to catch it.** Look at the chart's last refresh date. If > 6 months old, new decision types have probably emerged but not been added.

---

## Red Flag 9: Treating DACI as RACI for tasks

**Symptom.** Chart lists "Build the feature", "Test the feature", "Deploy the feature" with D/A/C/I assignments.

**Why it's bad.** DACI is for *decisions*, not *tasks*. Task assignment is RACI (Responsible/Accountable/Consulted/Informed). Mixing them produces confusion — the chart looks comprehensive but is doing two different jobs poorly.

**Bad example:**
> "DACI row: 'Build the new dashboard'. Driver: PM. Approver: Eng Lead. (This is a task. The decision was 'do we build it?'; the task is 'build it once approved'.)"

**Good example:**
> "DACI rows are decisions: 'Whether to build the new dashboard' (D: PM, A: VP Product). 'Architecture for the dashboard' (D: Eng Lead, A: Eng Manager). Task execution lives in the sprint backlog / RACI / ticket assignment, not in the DACI."

**How to catch it.** Read each row's title. Does it start with "Whether to…" or imply a decision? If it starts with "Build/Test/Deploy", it is a task.

---

## Red Flag 10: Chart doesn't match how decisions actually happen

**Symptom.** Chart says "Driver: PM". In practice, every decision is made in a Slack thread between the Eng Manager and the VP Eng; PM is informed afterward.

**Why it's bad.** Chart-vs-reality mismatch is worse than no chart. New joiners learn the chart, then experience the actual workflow, and lose trust in both the chart and the leaders who published it.

**Bad example:**
> "Chart (published, signed-off): Driver = PM. Reality: every decision in a 2-person Slack thread between EM and VPE; PM informed in #product-updates."

**Good example:**
> "Step 1 in building the chart: map the *current-state* DACI — how decisions actually happen, not how leadership wishes they happened. Then design *target-state*. If current shows EM/VPE making decisions, that is the baseline. Either change behavior (PM becomes Driver, EM moves to C) or update the chart to match reality (PM is C, EM is D). Do not publish a fiction."

**How to catch it.** Ask 3 team members independently: "for the last 3 decisions, who actually drove them?" Compare to chart.

---

## Red Flag 11: Decision cycle time not tracked

**Symptom.** Team has DACI. Cannot answer "how long does a P0 decision take?" No data.

**Why it's bad.** The point of DACI is faster, cleaner decisions. Without tracking decision cycle time, you cannot tell if it's working. The team is doing the ritual without the metric.

**Bad example:**
> "DACI rollout summary: 'chart published, all decisions assigned'. No metric on cycle time, escalation rate, or reversal rate."

**Good example:**
> "DACI health metrics (tracked monthly): (1) Decision cycle time for P0 decisions: target < 5 business days. Current: 6.2d, trending down from 11d pre-DACI. (2) Decision reversal rate: target < 10%. Current: 8%. (3) Escalation rate (decisions escalated past Approver): target < 15%. Current: 12%. (4) Stakeholder confidence ('do you know who decides X?'): quarterly survey; current 78%."

**How to catch it.** Ask the DACI owner for the cycle-time number. No answer = the framework is theater.

---

## Red Flag 12: DACI imposed without team buy-in

**Symptom.** VP brings a pre-built DACI to the team meeting. "Here is how decisions work now." Team nods. Six weeks later, nothing has changed.

**Why it's bad.** DACI requires cultural buy-in. A chart imposed from above without the team's input lacks legitimacy. The team interprets it as a control move, not a clarity tool. They comply nominally and route around it.

**Bad example:**
> "VP's announcement: 'I have drafted a DACI for our team. Effective Monday.' Team meeting: 5 minutes of Q&A, no substantive discussion. Outcome: chart published, behavior unchanged."

**Good example:**
> "DACI workshop (2 hours, all team members): (1) Each person lists 3 decisions they have felt unclear on in the last quarter. (2) Group clusters into ~10 decision categories. (3) Per category, the group debates Driver and Approver assignments. (4) Disagreements escalate to the team's manager in real-time. (5) Chart is committed at end of workshop with everyone in the room. Re-reviewed at 30, 60, 90 days."

**How to catch it.** Ask team members: "did you help build this DACI?" If most say no, ownership is missing.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Too many Approvers | Any row with > 2 A's? |
| 2 | Driver-by-committee | Any row with > 1 D? |
| 3 | Driver lacks authority | Can Driver push back on Approver and have it land? |
| 4 | Informed treated as Approver | Has any I role objected late and caused a slip? |
| 5 | Everyone is Contributor | Any row with > 5 C's? |
| 6 | Built but never referenced | When was the chart last cited in a meeting? |
| 7 | Veto without explanation | Last 5 vetoes — written rationale present? |
| 8 | New decisions not added | Chart's last refresh date? |
| 9 | DACI as task list | Do rows start with "Build/Test" instead of "Whether to"? |
| 10 | Chart doesn't match reality | Ask 3 team members independently: who actually decides? |
| 11 | Cycle time not tracked | Current decision cycle time number? |
| 12 | Imposed without buy-in | Did team help build the chart? |

## Related Reading

- SKILL.md Troubleshooting
- `create-prd/` (Contacts section often maps to DACI roles)
- `post-mortem/` (action items frequently need DACI to assign owners)
- `dependency-map/` (cross-team decisions where DACI assigns the seam owner)
- Productside DACI guidance for product teams
