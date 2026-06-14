# Red Flags: Backlog Refinement

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan before promoting stories from "candidate" to "Refined". Each red flag shows the *bad* version next to the *good* version, anchored to Bill Wake's INVEST and Richard Lawrence's nine splitting patterns.

---

## Red Flag 1: INVEST checkbox theater

**Symptom.** Every story scores 6/6 on the `refinement_scorer.py` output, but planning meetings still drag and rollover rate is 30%+.

**Why it's bad.** The scorer grades *structural form* — does the story have a Why, a What, and 4+ ACs. A story can pass every form check and still be the wrong work, miscommunicate scope, or hide assumptions. Treating the 6/6 score as a green light produces velocity theater.

**Bad example:**
> "STORY-117 passes INVEST 6/6. Why: 'improves onboarding'. What: 'rebuild the signup flow'. Estimate: 4 days. 4 ACs. READY."

**Good example:**
> "STORY-117 passes 6/6 form check. But: the Why is generic ('improves onboarding' — which step, which metric?), the What is sweeping ('rebuild the signup flow' — that's a 6-week project), and the 4 ACs describe activities, not outcomes. Send back to refinement: tie the Why to the activation KR, narrow the What to one step of the funnel, rewrite ACs as observable outcomes."

**How to catch it.** After the scorer passes a story, re-read the Why aloud. If it could describe any feature in the product, it is not specific enough.

---

## Red Flag 2: Horizontal slicing dressed up as stories

**Symptom.** A feature is split into "API endpoint", "Frontend page", "Database migration", each a separate story.

**Why it's bad.** Horizontal slices violate INVEST-V (no single slice delivers user value) and INVEST-I (every slice depends on the others). Shipping the API without the UI is invisible to users; shipping the UI without the API is broken. The team feels productive ("we shipped 3 stories!") while delivering zero outcomes.

**Bad example:**
> "Feature: Saved searches.
> STORY-201: Build /searches POST endpoint
> STORY-202: Build saved-searches UI panel
> STORY-203: Add saved_searches table migration"

**Good example:**
> "Feature: Saved searches. Apply Lawrence pattern 1 (workflow steps) and 2 (business rules):
> STORY-201: User can save a search and re-run it (one search per user, default sort) — end-to-end
> STORY-202: User can name their saved searches (rename + display)
> STORY-203: User can save up to 25 searches (volume limit + paywall messaging)
> Each slice ships value end-to-end; each can be released independently."

**How to catch it.** For each slice, ask "who benefits if this is the only thing we ship?" If the answer is "nobody until the others land", the slice is horizontal.

---

## Red Flag 3: DoR scope creep

**Symptom.** Definition of Ready has grown to 18+ items. Stories sit in "Candidate" for 3+ sessions waiting for design, telemetry plans, legal review, security review.

**Why it's bad.** A too-strict DoR creates a backlog of "almost ready" stories that nobody can ship. Teams either thrash trying to satisfy it, or quietly bypass it. Both outcomes destroy the DoR's authority.

**Bad example:**
> "DoR (18 items): title, why, what, 8+ ACs, INVEST 6/6, all dependencies cleared, design approved by Design Lead, security reviewed, privacy reviewed, telemetry spec'd, copy reviewed, accessibility audited, performance estimate, rollback plan, owner assigned in 3 systems, sprint goal tagged, business case attached, exec sponsor signed off..."

**Good example:**
> "DoR (10 items, capped): title; Why tied to OKR/outcome; What in 1-2 paragraphs; 4+ ACs as observable outcomes; INVEST >= 5/6; cross-team dependencies named; design linked or TBD-by-date; estimated; no open blocker questions; sprint goal tagged. Separate DoRs for spikes (3 items) and bugs (4 items)."

**How to catch it.** Count DoR items. If above 12, audit which ones have ever caused a real story to fail. Cut those that have not.

---

## Red Flag 4: "Negotiated in" stories at planning

**Symptom.** Sprint planning admits stories that explicitly fail DoR. Reasoning: "we have capacity, let's negotiate".

**Why it's bad.** The DoR is meaningless if planning can override it. Teams that "negotiate in" failing stories produce rollovers and unplanned discovery work inside the sprint. The cost is paid mid-sprint, not at planning.

**Bad example:**
> "STORY-302 scores 4/6 (Why is missing baseline metric; AC #3 vague). Team: 'let's take it anyway, we'll figure out the metric during the sprint'."

**Good example:**
> "STORY-302 scores 4/6. Team: 'leave it out of the sprint. The PM will get the baseline by Wednesday; we'll re-grade in Thursday's refinement and consider it for next sprint. Sprint is under-full by 5 points — acceptable, we'd rather ship 35 clean points than 42 messy ones.'"

**How to catch it.** Watch one sprint planning. Count how many admitted stories failed the DoR. If above zero, the DoR has no authority.

---

## Red Flag 5: Spike as a permanent state

**Symptom.** A spike story shows up in 3+ consecutive sprints, never producing a refined story.

**Why it's bad.** Spikes are Lawrence's "last resort" pattern (#9) — a time-boxed investigation that should *produce* a refined story by end of timebox. A spike that recurs is a research project mislabeled as a story; the team treats it as productive work while the actual feature stalls.

**Bad example:**
> "STORY-410: SPIKE: Investigate authentication options. (Sprint 12: in progress. Sprint 13: in progress. Sprint 14: in progress.)"

**Good example:**
> "STORY-410: SPIKE: Investigate authentication options. Timebox: 3 days. Deliverable: a decision memo recommending one option with cost/risk/timeline, plus a refined STORY-411 for the implementation. Owner: Tomas R. If not delivered by sprint end, escalate to Eng Lead."

**How to catch it.** Filter the backlog for "SPIKE" in the title. Count sprints in flight. Anything > 1 is a flag.

---

## Red Flag 6: Acceptance criteria describe implementation steps

**Symptom.** ACs read like a coding checklist: "API returns 200", "React component renders", "DB column added".

**Why it's bad.** Implementation-step ACs cannot be validated by QA, design, or product. They lock in a specific implementation, violating INVEST-N (negotiable). Worst, they let stories pass DoD without ever validating user value.

**Bad example:**
> "AC 1: POST /searches returns 201
> AC 2: New SearchPanel React component renders
> AC 3: saved_searches table populated
> AC 4: Redux store updates on save"

**Good example:**
> "AC 1: When a user clicks 'Save search' on a result page, the search appears in their Saved list within 1 second.
> AC 2: A saved search can be re-run from the Saved list, producing the same results.
> AC 3: A saved search persists across logout/login.
> AC 4: If a user has 25 saved searches, the 26th save attempt shows a paywall message with upgrade CTA."

**How to catch it.** Read each AC aloud. If it contains "API", "endpoint", "component", "table", or HTTP status codes, it is an implementation step.

---

## Red Flag 7: Estimates with no shared baseline

**Symptom.** Two engineers estimate the same story at 1 day and 5 days respectively, with no conversation about why.

**Why it's bad.** INVEST-E (estimable) fails. The 5x spread indicates one of: (a) the story is ambiguous, (b) the engineers have different assumptions, or (c) the team has no shared sense of "1 day" vs "5 days". Refining estimates without resolving the disagreement is theater.

**Bad example:**
> "Engineer A: 1 day. Engineer B: 5 days. Team: 'average to 3 days, move on'."

**Good example:**
> "Engineer A: 1 day (assumes existing search service already supports save endpoint).
> Engineer B: 5 days (assumes new endpoint + new persistence layer + Redux refactor).
> Refinement: clarify what exists today. After 10 min: existing service has no save endpoint but persistence layer is reusable. Re-estimate: A and B both 3 days. Story now has a 'Assumptions' note attached."

**How to catch it.** When estimates span > 2x, do not average — investigate.

---

## Red Flag 8: DoD without deployment + telemetry

**Symptom.** Definition of Done is "merged + reviewed + tested". No deployment requirement, no analytics instrumentation.

**Why it's bad.** A story merged but not deployed is not done — users have not received the value. A story shipped without telemetry cannot be measured against the outcome it was supposed to deliver. The team produces output but cannot defend outcomes.

**Bad example:**
> "DoD: merged to main; code reviewed; tests passing."

**Good example:**
> "DoD: merged to main; code reviewed by >= 1 engineer; unit + integration tests passing; deployed to production behind feature flag (or directly released for trunk-based teams); analytics events instrumented for the value-claim metric; manual QA pass; WCAG AA pass on user-facing UI; help center / runbook updated; PO accepted."

**How to catch it.** Read the DoD. Search for the word "deployed" and "telemetry" or "analytics". If missing, the DoD is incomplete.

---

## Red Flag 9: Same story refined 3+ times without progress

**Symptom.** STORY-410 has been on the refinement candidate list for 3 weeks. It never gets promoted to Refined. Notes are similar each week.

**Why it's bad.** A story that cannot be refined in 3 sessions is not a refinement problem — it is a discovery problem. The team is missing information that no amount of INVEST grading will surface.

**Bad example:**
> "Week 3 refinement notes on STORY-410: 'discussed scope; need to understand integration; ML to look into it.'"

**Good example:**
> "Week 3: STORY-410 hits the 3-strike rule. Send back to discovery (`discovery/identify-assumptions/`). The blocker is an unvalidated assumption about integration capability, not a story-quality issue. The PM owns the assumption test by Friday; if validated, the story re-enters refinement. If invalidated, the story is killed."

**How to catch it.** Tag each refinement candidate with a session counter. At session 3 without promotion, route to discovery, not back into refinement.

---

## Red Flag 10: Splits by team, not by user value

**Symptom.** A feature is split as "Mobile team story" + "Backend team story" + "Data team story".

**Why it's bad.** Splitting by team violates INVEST-I (independent) and INVEST-V (valuable). Each team-slice depends on the others; no slice ships value alone. The split serves coordination, not delivery.

**Bad example:**
> "Feature: Push notifications for new messages.
> STORY-501: Backend — message-event publisher (Backend team)
> STORY-502: Notification service consumer (Platform team)
> STORY-503: Mobile push subscription (Mobile team)"

**Good example:**
> "Apply Lawrence pattern 2 (business rule variations):
> STORY-501: A user receives a push notification when they get a 1:1 message from someone they follow (end-to-end, single rule)
> STORY-502: Notifications respect quiet-hours setting (rule variation)
> STORY-503: Group-chat messages produce a single batched notification per minute (rule variation, performance-deferral)
> Cross-team coordination happens within each story, not across stories."

**How to catch it.** If a story name contains a team name, it is a task, not a story.

---

## Red Flag 11: 2-hour stories that pretend to be features

**Symptom.** The backlog is full of 0.5-day stories ("rename label", "fix typo", "bump version").

**Why it's bad.** These are tasks, not stories. They flood the refinement pipeline, inflate completion counts, and obscure real progress. They also force the team to estimate work whose total cost (planning + standup + review) exceeds the work itself.

**Bad example:**
> "STORY-601: Change button label from 'Save' to 'Save and continue' — 0.5d
> STORY-602: Update help link in footer — 0.5d
> STORY-603: Increment minor version in package.json — 0.1d"

**Good example:**
> "Roll into a single chore: STORY-601: 'UX polish batch — May 2026: 7 small label/copy/link updates listed below'. Treat as one INVEST-S-bound story. Skip refinement grading for individual items; QA verifies the batch."

**How to catch it.** Filter the backlog for estimates <= 1 day. If more than ~20% of the backlog falls under this, the team is task-cataloguing, not story-writing.

---

## Red Flag 12: Refinement scorer gives 6/6 but assumptions are unvalidated

**Symptom.** Story passes the scorer cleanly, but the team realizes mid-build that "the third-party API supports filtering" was an unvalidated assumption — and it doesn't.

**Why it's bad.** The Python scorer grades form, not substance. Risk lives in assumptions, not in word count or AC count. A perfectly-formed story can still be the wrong work.

**Bad example:**
> "STORY-701 passes 6/6. Estimate: 3 days. (Mid-sprint: 'turns out the API doesn't support the filter we need. Rescope: 8 days.')"

**Good example:**
> "STORY-701 passes 6/6 form check. Refinement pause: name the top 3 assumptions. Top assumption: 'third-party API supports filter by tenant_id'. Spike (1 day) before committing: confirm via API docs and a smoke test. If confirmed, story stays at 3 days. If not, story splits into 'investigate alternative' + the original."

**How to catch it.** Ask: "What has to be true for this story to be 3 days?" If the team cannot answer, route through `discovery/identify-assumptions/` before commit.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | INVEST checkbox theater | Could the Why describe any feature in the product? |
| 2 | Horizontal slicing | Does any slice ship user value alone? |
| 3 | DoR scope creep | Are there more than 12 DoR items? |
| 4 | "Negotiated in" stories | Did any admitted story fail DoR at planning? |
| 5 | Spike as permanent state | Is any spike in flight > 1 sprint? |
| 6 | ACs are implementation steps | Do ACs contain "API", "endpoint", or HTTP codes? |
| 7 | Estimate spread > 2x ignored | Was the gap investigated or averaged away? |
| 8 | DoD without deploy + telemetry | Does DoD include "deployed" and "instrumented"? |
| 9 | Same story refined 3+ times | Did it get routed to discovery? |
| 10 | Splits by team | Does any story name contain a team name? |
| 11 | 2-hour stories pretending to be features | Are > 20% of stories <= 1 day? |
| 12 | 6/6 form, unvalidated substance | What has to be true for the estimate to hold? |

## Related Reading

- SKILL.md Troubleshooting
- references/invest-and-splitting-guide.md
- `discovery/identify-assumptions/` (for routing failing stories)
- `discovery/pre-mortem/` (for substantive risk)
- `prioritization-frameworks/` (for sequencing the refined queue)
