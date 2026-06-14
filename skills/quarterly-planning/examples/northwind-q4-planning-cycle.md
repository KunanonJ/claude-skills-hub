# Example: Q4 Planning Cycle for Northwind SaaS

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Northwind SaaS is a Series C fintech, 200 people, building a treasury platform for mid-market companies. The PMO is running its first formally facilitated quarterly cycle after a chaotic Q3 where the team committed to 14 initiatives and finished 6. The Head of Product (Ines) is determined to deliver three real artifacts -- a kickoff, a mid-quarter check-in, and a close-out retro -- with explicit decisions captured at each.

The CEO wants the quarter to deliver three OKRs: lift activation, ship the Multi-Entity feature for a flagship customer, and bring two compliance audits to ready-for-review. Engineering capacity is 110 person-weeks across three squads.

## Inputs

- Three squads (Activation, Treasury Core, Compliance), 35 engineers total
- Q4 dates: Oct 6, 2026 -- Jan 2, 2027 (13 weeks)
- 14 candidate initiatives carried over plus 5 new ones
- Q3 hit-rate: 43% (6 of 14 delivered)
- CEO has pre-committed Multi-Entity to a flagship customer for late November

## Applying the skill

1. **Kickoff (Oct 6).** Capacity-bound the quarter, set OKRs, write the explicit "won't do" list, and produce a one-page commitment from each squad.
2. **Mid-quarter check-in (Nov 10).** Three squads each give a 7-minute structured update with a R/Y/G traffic light and ask for help. Re-baseline if any squad is Red.
3. **Close (Jan 5 -- adjusted for holidays).** Score every initiative against its OKR. Capture two "keep doing" and two "stop doing" decisions for Q1 2027.

## The artifact

---

### Artifact 1: Q4 Kickoff Document

**Date:** 2026-10-06
**Facilitator:** Ines (Head of Product)
**Attendees:** CEO, VP Eng, VP Sales, Head of Compliance, three squad leads

#### Q4 OKRs (locked)

**O1: Convert new signups into paying teams faster.**
- KR1: Activation rate (signup -> first treasury transaction) from 18% to 28% by Dec 31
- KR2: Time-to-first-transaction from 6 days to <48 hours (median)

**O2: Land the Multi-Entity feature with one flagship customer.**
- KR1: Multi-Entity GA-eligible by Nov 24 (committed to Skyway Logistics)
- KR2: At least 3 design-partner accounts using Multi-Entity in production by Dec 20

**O3: Bring SOC 2 Type II + ISO 27001 to ready-for-review.**
- KR1: SOC 2 Type II evidence collection 100% complete by Dec 15
- KR2: ISO 27001 gap analysis closed for 24 of 24 controls by Dec 31

#### Capacity allocation

| Squad | Engineers | Person-weeks | Allocation |
|-------|-----------|-------------|------------|
| Activation | 12 | 38 | 35% |
| Treasury Core (Multi-Entity) | 14 | 44 | 40% |
| Compliance | 9 | 28 | 25% |
| **Total** | **35** | **110** | **100%** |

#### Initiatives committed (top 9)

1. Onboarding wizard v3 (Activation, 12 PW)
2. Email re-engagement sequences (Activation, 6 PW)
3. Activation analytics dashboard (Activation, 8 PW)
4. Auto-detect industry templates (Activation, 12 PW)
5. Multi-Entity data model migration (Treasury, 14 PW)
6. Multi-Entity UI + permission layer (Treasury, 18 PW)
7. Multi-Entity API and webhook v2 (Treasury, 12 PW)
8. SOC 2 Type II evidence sprint (Compliance, 16 PW)
9. ISO 27001 gap closure (Compliance, 12 PW)

**Total committed: 110 PW = 100% of capacity. No slack reserved -- explicit risk noted below.**

#### Explicit "won't do" list

- Embedded analytics SDK (defer to Q1 2027)
- New billing currency support (defer to Q1 2027)
- Slack integration v2 (defer; no flagship customer demand)
- Customer success portal (defer; CS using current tools through Q1)

#### Risks called out at kickoff

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| Multi-Entity scope creep from Skyway feedback | High | High | Weekly Skyway sync, change-control process | Tomas (Treasury lead) |
| SOC 2 evidence depends on infra team | Medium | High | Weekly cross-team standup with Infra | Hari (Compliance lead) |
| No capacity buffer -- any incident eats the quarter | Medium | Medium | Pre-agree to drop Init #4 if 1 week behind by Nov 10 | Ines |

---

### Artifact 2: Mid-Quarter Check-In

**Date:** 2026-11-10
**Format:** 30 minutes async-first, 30 minutes sync for Reds only
**Facilitator:** Ines

#### Status snapshot

| Squad | R/Y/G | Why | Top ask |
|-------|------|-----|---------|
| Activation | Yellow | Onboarding wizard v3 is 1 week late; analytics dashboard on track | One more analytics engineer for 2 weeks |
| Treasury Core | Red | Data model migration revealed unmodeled FX edge cases; 2 weeks behind on Multi-Entity API | Defer Init #4 (auto-detect industry templates); accept Skyway slip to Dec 4 |
| Compliance | Green | SOC 2 evidence 65% complete; ISO 27001 gap analysis 80% closed | None |

#### Decisions made at the check-in

1. **Drop Init #4 (Auto-detect industry templates).** Activation team retains 12 PW; reassign one engineer to Treasury Core temporarily.
2. **Slip Multi-Entity GA from Nov 24 to Dec 4** with Skyway approval. Sales VP to call Skyway by Nov 12.
3. **Hold capacity allocation.** Do not pull in new work. The buffer this creates is the *whole* mitigation.
4. **Re-baseline KR1 of O2** from "GA-eligible by Nov 24" to "GA-eligible by Dec 4." Tracked as a planned re-baseline, not a miss.

---

### Artifact 3: Q4 Close-Out Retro

**Date:** 2027-01-05
**Format:** 90-minute facilitated session
**Facilitator:** Ines + scrum-master rotation

#### Scoreboard

| OKR | KR | Target | Actual | Score |
|-----|----|--------|--------|-------|
| O1: Activate faster | Activation rate 18% -> 28% | 28% | 25% | 0.6 |
| O1 | Time-to-first <48h | 48h | 41h | 1.0 |
| O2: Multi-Entity | GA-eligible by Dec 4 (rebased) | Dec 4 | Dec 9 | 0.7 |
| O2 | 3 design-partner accounts | 3 | 2 | 0.5 |
| O3: Compliance | SOC 2 evidence 100% | 100% | 100% | 1.0 |
| O3 | ISO 27001 24/24 closed | 24 | 22 | 0.7 |

**Composite OKR score: 0.75** (target was 0.6-0.8; healthy aspirational range)

#### Keep doing

- Explicit capacity allocation in person-weeks, not "story points percent."
- Mid-quarter Red triggers an explicit re-baseline. The team trusted the process and the slip did not bleed into Q1.
- "Won't do" list named four initiatives. Stakeholders did not re-litigate them once written down.

#### Stop doing

- 100% capacity allocation with no buffer. Build in 10% slack for unknowns -- the Multi-Entity FX edge cases would have been absorbed.
- Activation OKR depended on a tooling change that was 60% of the work (Init #4) -- which got dropped. Activation rate moved less than projected. Lesson: do not tie an OKR to one initiative; have two paths.

#### Action items for Q1 2027

1. Reserve 10% capacity buffer in Q1 kickoff. Owner: Ines.
2. Multi-Entity follow-up with two more design partners. Owner: VP Sales, by Jan 31.
3. Activation: design a second lever beyond onboarding wizard v3. Owner: Activation lead, by Jan 20.
4. Promote ISO 27001 follow-up (2 controls remaining) into Compliance Q1 plan. Owner: Hari.

## Why this works

- Three distinct artifacts (kickoff, check-in, close), each with explicit decisions captured. The cycle is auditable.
- Capacity allocated in real units (person-weeks), not abstract points. No "we have room for one more" arguments.
- Explicit "won't do" list deflates re-litigation in week 6.
- Mid-quarter check-in had a *named* trigger (one week late by Nov 10) for re-baselining. The team did not freeze when Multi-Entity slipped.
- Scoring is honest, not heroic. 0.75 is the right number when KR1 of O1 missed.

## What's next

- Use `../brainstorm-okrs/` to draft Q1 2027 OKRs informed by the close-out scoreboard.
- Run `../status-update-generator/` weekly through Q1 to push the check-in cadence one level down.
- Use `../../sprint-retrospective/` for the squad-level retros that feed into the quarterly close.
- Apply `../prioritization-frameworks/` to the carryover list before Q1 kickoff.
