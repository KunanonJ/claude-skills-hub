# Notion OKR Template

Database schema and review cadence for OKRs in Notion, using Christina Wodtke's confidence model (10 / 7 / 5 / 3).

---

## Database properties

| Property | Type | Notes |
|---|---|---|
| Title | title | "Activation rate hits 45%" or "Become the easiest analytics tool to onboard" |
| ID | unique_id | Prefix: `OKR` |
| Type | select | `Objective` (qualitative, inspirational) / `Key Result` (quantitative, measurable) |
| Parent Objective | relation (self) | KRs link to their parent Objective |
| Quarter | select | `Q1 2026`, `Q2 2026`, `Q3 2026`, `Q4 2026`, ... |
| Owner | people | Single accountable owner (one human) |
| Status | status | To-do: `Not started` · In progress: `On track`, `At risk`, `Off track` · Complete: `Hit`, `Missed` |
| Confidence | select | `10` (very confident) / `7` (likely) / `5` (toss-up) / `3` (unlikely) |
| Confidence Trend | select | `Up`, `Flat`, `Down` (week-over-week) |
| Target | rich_text | Measurable target ("30% → 45%") |
| Current | rich_text | Latest value ("38%") |
| Progress | number (percent) | (Current − Start) / (Target − Start); manual or formula |
| Update Cadence | select | `Weekly` (default) / `Biweekly` / `Monthly` |
| Last Updated | date | Set on every check-in |
| Update Streak | formula | Days since Last Updated; flag if > cadence |
| PRDs | relation → PRDs | Contributing PRDs |
| Initiatives | relation → Roadmap | Contributing roadmap initiatives |
| Notes | rich_text | Blockers, context, hypotheses |

---

## Wodtke confidence scale

| Score | Meaning | Action |
|---|---|---|
| **10** | "We will absolutely hit this." | Probably too easy; consider raising the bar. |
| **7** | "We feel good but not certain." | The sweet spot for ambitious OKRs. |
| **5** | "Coin flip; could go either way." | Acceptable for stretch goals; needs weekly attention. |
| **3** | "Probably won't hit, but we're trying." | Acceptable for moonshots; needs explicit exec backing. |

Aim to set OKRs at **5-7** confidence at the start of the quarter. By end of quarter, expect distribution to shift toward 7-10 if execution is healthy or toward 3 if priorities changed.

---

## Page body template (for each OKR row)

### For an Objective

```
# <Objective>

> [!NOTE]
> **Quarter:** Q3 2026 · **Owner:** @PM
> **Why this objective:** <2-3 sentences on strategic rationale>

## Strategic context
Why this objective matters this quarter, and what alternative objectives were considered.

## Key Results
Linked below via relation:
- @OKR-014: Activation rate hits 45%
- @OKR-015: Time-to-first-value < 5 min
- @OKR-016: Trial-to-paid conversion hits 12%

## Risks
- <Risk 1>
- <Risk 2>

## Quarterly update log
### YYYY-MM-DD — Week 1
- Confidence: 7 → 7
- Notes: ...

### YYYY-MM-DD — Week 2
- Confidence: 7 → 5
- Notes: <why dropped>
```

### For a Key Result

```
# <Key Result>

> [!NOTE]
> **Parent Objective:** @OKR-007 (Become the easiest analytics tool to onboard)
> **Owner:** @PM · **Quarter:** Q3 2026
> **Target:** 30% → 45% · **Current:** 38% · **Confidence:** 7

## How we measure
- **Source:** Mixpanel funnel `activation_v3`
- **Definition:** % of new signups that complete the onboarding checklist within 7 days
- **Refresh cadence:** daily; reviewed weekly

## Contributing PRDs
Linked via PRDs relation:
- @PRD-018: New self-serve signup flow
- @PRD-024: Sample data on signup

## Why this KR
- Activation is the single largest revenue lever (per Q1 retention analysis).
- Each +1pp activation = ~$120k ARR.

## Risks and dependencies
- Risk: A/B test sample sizes are insufficient if signup volume drops.
- Dependency: Auth rewrite (target end of July) must land for PRD-018.

## Weekly update log
| Date | Current | Confidence | Note |
|---|---|---|---|
| 2026-07-04 | 32% | 7 | Baseline |
| 2026-07-11 | 33% | 7 | Onboarding tweak shipped |
| 2026-07-18 | 35% | 7 | New signup flow at 10% |
| 2026-07-25 | 38% | 7 | New signup flow at 50% |
```

---

## Recommended views

### View 1: This Quarter — Tree

- **Type:** Table
- **Filter:** Quarter = current
- **Group by:** Parent Objective
- **Sort by:** Type (Objective first), then Title
- **Visible properties:** Title, Type, Owner, Status, Confidence, Confidence Trend, Target, Current, Progress, Last Updated
- **Use:** Default view; weekly OKR review

### View 2: My OKRs

- **Type:** Table
- **Filter:** Owner contains me; Quarter = current
- **Sort:** Status (At Risk first), Confidence ascending
- **Visible properties:** Title, Status, Confidence, Target, Current, Last Updated

### View 3: At Risk / Off Track

- **Type:** Board
- **Group by:** Status
- **Filter:** Quarter = current AND Status in (At Risk, Off Track)
- **Visible properties:** Owner, Confidence, Target, Current, Notes
- **Use:** Leadership escalation discussions

### View 4: Confidence Distribution

- **Type:** Board
- **Group by:** Confidence
- **Filter:** Quarter = current; Type = Key Result
- **Use:** Calibrate ambition at quarter start; track drift

### View 5: Stale Updates

- **Type:** Table
- **Filter:** Update Streak > cadence-implied-days (e.g. > 8 for Weekly)
- **Sort:** Update Streak descending
- **Visible properties:** Title, Owner, Last Updated, Status
- **Use:** Nudge owners who have not checked in

### View 6: Annual History

- **Type:** Table
- **Filter:** (none)
- **Group by:** Quarter (descending)
- **Sort by:** Status, Confidence
- **Use:** Year-over-year retrospective

---

## Cadence and rituals

| Ritual | Frequency | Owner | What happens |
|---|---|---|---|
| Weekly check-in | Weekly (Monday) | KR Owner | Update Current, Confidence, Confidence Trend, Notes |
| OKR review | Weekly (Friday) | Head of Product | Walk View 1, focus on View 3 |
| Mid-quarter recalibration | Once mid-quarter | Leadership | Kill or rebaseline OKRs whose context has shifted |
| Quarterly retro | End of quarter | Leadership | Score each KR Hit/Missed; capture learnings in a Decisions DB entry |
| Annual review | End of year | Leadership | Score by quarter; identify systemic patterns |

---

## Scoring rubric (end of quarter)

| Final state | Confidence at end | Score |
|---|---|---|
| Target achieved | 10 | **Hit** |
| Target nearly achieved (≥80%) | 7-10 | **Hit** (with caveat) |
| Target partially achieved (40-79%) | 5-7 | **Missed** (but learning captured) |
| Target far missed (<40%) | 3-5 | **Missed** |
| Killed mid-quarter due to priority shift | n/a | **Killed** (not counted as Hit or Miss) |

Record the score in the `Status` property at quarter end. Aggregate Hit/Missed ratios per quarter on a separate dashboard page.

---

## Anti-patterns

- **Setting all OKRs at confidence 10** — defeats the purpose of stretch goals.
- **Letting OKRs go 3+ weeks without an update** — Status drifts from reality; trust erodes.
- **Pushing all hard targets into Q4** — back-loaded quarters tend to fail.
- **One person owning more than 3 KRs** — diluted attention; one will rot.
- **Treating Hit-rate as the only metric** — 100% Hit rate means goals were too easy; aim for 60-70% on a 5-7 baseline.
