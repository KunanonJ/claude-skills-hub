# Red Flags: Story Splitting

> Common ways this skill's output goes wrong -- concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan every split before tickets enter a sprint. Each red flag has bad and good quoted examples.

---

## Red Flag 1: Horizontal Slicing (UI Before Backend)

**Symptom.** A user story is split by layer: "Story 1: UI only", "Story 2: API endpoints", "Story 3: data model".
**Why it's bad.** Each slice is unshippable. The "UI only" story has nothing to fetch from. The "API only" story has no consumer. The team cannot demonstrate user value at the end of any sprint until the third sprint, and there is no learning signal in between.
**Bad example:**
> "Story 'Filter candidates by skill' split into:
> - Story A: UI filter component (no backend).
> - Story B: /candidates?skill=X endpoint.
> - Story C: skill index in the candidate table."
**Good example:**
> "Story 'Filter candidates by skill' split *vertically* by user value:
> - Slice 1: filter by a single hard-coded skill from a hard-coded list (full stack, shippable).
> - Slice 2: filter by any skill from the live skill table.
> - Slice 3: multi-skill AND filter.
> Every slice is end-to-end demonstrable."
**How to catch it.** Any split where one slice is 'just the UI' or 'just the API' = re-split vertically.

---

## Red Flag 2: Splits That Lose User Value

**Symptom.** Story is split into pieces, none of which deliver any visible user benefit alone.
**Why it's bad.** The point of splitting is to deliver smaller increments of *user value*, not smaller increments of *work*. If no slice is independently valuable, you have just made the original story more painful to track.
**Bad example:**
> "'Bulk-edit candidates' split into:
> - Slice A: add checkboxes to candidate rows (does nothing).
> - Slice B: add an Edit button (does nothing).
> - Slice C: wire the button to the API.
> (No slice can be released to users.)"
**Good example:**
> "'Bulk-edit candidates' split by operation:
> - Slice 1: bulk-tag (5 candidates at a time, one tag).
> - Slice 2: bulk-tag (any number, multiple tags).
> - Slice 3: bulk status-change.
> - Slice 4: bulk-assign-to-recruiter.
> Each slice could ship and recruiters could use it."
**How to catch it.** Ask: "if we shipped only slice N to users this week, would they get value?" If no, re-split.

---

## Red Flag 3: Slices Larger Than the Original

**Symptom.** Original story was 8 points. After splitting, slices total 25 points.
**Why it's bad.** Splitting should clarify scope, not expand it. When the slices total more than the original, the team has discovered scope they did not see -- which means the original estimate was wrong, but they often forget to remove the original from velocity calcs. Burndown gets distorted.
**Bad example:**
> "Original story: 8 points. After splitting into 4 slices: 8 + 5 + 8 + 5 = 26 points. (Velocity assumes 8.)"
**Good example:**
> "Original story: 8 points. After splitting into 4 slices: 5 + 3 + 5 + 5 = 18 points. Reasons for growth: discovered need for migration + analytics + admin UI; team chose to keep all in scope. Original closed; velocity refers to slices only."
**How to catch it.** Total slice points > 1.5x original = either close the original and re-estimate or reduce scope.

---

## Red Flag 4: Splitting by Acceptance Criteria

**Symptom.** Story has 6 acceptance criteria; PM splits the story so each AC becomes its own story.
**Why it's bad.** Acceptance criteria define when a story is *done*, not where it should split. Splitting by AC creates micro-stories that each carry overhead (testing, deploy, design review) disproportionate to their value, and the user experience is fragmented.
**Bad example:**
> "Story 'Send offer letter' with 6 ACs split into 6 stories: validate inputs, render PDF, attach signature, save to S3, email candidate, log audit event."
**Good example:**
> "Story 'Send offer letter' kept as 1 story (5 points) -- the ACs are checks on completion, not splitting candidates. If story is too big, split by user-facing operation: 'send simple offer letter' (text only) and 'send offer letter with PDF + signature'."
**How to catch it.** Slice count > AC count = re-think.

---

## Red Flag 5: Spike Disguised as a Story

**Symptom.** The story reads: "Investigate options for the bulk-edit feature."
**Why it's bad.** This is a spike (research / exploration), not a story. It produces a document or decision, not user value. Mixing spikes into the story rank inflates velocity and hides that the team is in discovery, not delivery.
**Bad example:**
> "Story: 'Investigate options for bulk-edit feature.' Estimate: 3 points."
**Good example:**
> "Spike: 'Investigate options for bulk-edit feature.' Time-boxed: 2 days. Owner: <name>. Output: 1-pager comparing 3 approaches with recommendation. (Tracked separately from velocity; ticket type 'Spike'.)"
**How to catch it.** Story title verbs are 'investigate', 'spike', 'research', 'explore' = re-classify.

---

## Red Flag 6: Splits That Recombine Mid-Sprint

**Symptom.** Stories A and B were split for tracking but they cannot ship independently; the team treats them as one and only marks both done together.
**Why it's bad.** This is the worst of both worlds -- the overhead of two tickets without the benefit of two ships. It usually means the original split was theatrical, not real.
**Bad example:**
> "Story A: backend changes for new filter. Story B: UI for new filter. Both must merge in the same PR or feature flag is incoherent. Marked done together at end of sprint."
**Good example:**
> "Story A: backend filter API (live behind a feature flag; tested via internal admin UI).
> Story B: customer-facing UI for the filter (toggled by feature flag).
> A ships first; B ships when ready. Flag flips when both are stable."
**How to catch it.** Any two stories that always close together = either re-merge or use feature flags to make them independently shippable.

---

## Red Flag 7: Edge-Cases Sliced Into Separate Stories

**Symptom.** "Story 1: happy path. Story 2: error handling. Story 3: edge cases."
**Why it's bad.** Edge cases are not optional. Slicing them off implies "the happy path ships first" -- and in practice the edge-case story gets deprioritized, leaving fragile production. Worse, design / QA / docs still have to cover all paths anyway, so the split saves no time.
**Bad example:**
> "Story 1: 'sign up happy path'. Story 2: 'sign up errors'."
**Good example:**
> "Story 'sign up' includes the happy path and the high-frequency errors (invalid email, password too short, email already exists). Rare edge cases (network drop mid-submission, browser back during submit) are tracked separately as a follow-up under the same epic, with a measured-and-mitigated approach."
**How to catch it.** Story titles include 'happy path' / 'error path' / 'edge cases' = consolidate.

---

## Red Flag 8: Splitting Without a Pattern

**Symptom.** Splits are ad-hoc, no reference to Lawrence's 9 patterns (workflow, business-rule variations, simple/complex, ...).
**Why it's bad.** Ad-hoc splits tend to fall into the anti-patterns above (horizontal, AC-based, edge-case-extracted). The named patterns prevent this by forcing the splitter to choose a vertical seam.
**Bad example:**
> "PM splits stories by intuition; team agrees in sprint planning; ~30% of splits are horizontal in retrospect."
**Good example:**
> "Splits choose from Lawrence's 9 patterns explicitly. PR template requires the splitter to name the pattern (e.g. 'Split-by-workflow-step', 'Split-by-business-rule-variation'). Reviewers reject splits that do not name a pattern."
**How to catch it.** Split lacks a named pattern = reject in refinement.

---

## Red Flag 9: Splitting to Hit Sprint Capacity, Not for Value

**Symptom.** The team is over capacity by 4 points. PM splits a story to "make it fit" by carving off a small piece.
**Why it's bad.** Splits motivated by capacity, not value, produce artificial micro-stories that often regress (re-merged next sprint, or the "carved off" half is never built). This is rearranging deckchairs, not honest sprint planning.
**Bad example:**
> "Sprint capacity is 28; backlog has 32 points; PM splits a 5-point story into '3 + 2', commits the 3 to the sprint."
**Good example:**
> "Sprint capacity is 28; backlog has 32 points. PM holds the line: defers a 5-point story to next sprint, commits 27 points. (If the 5-point story should genuinely be split for *value*, that decision is made in refinement, not at the capacity wall.)"
**How to catch it.** Split happens during sprint planning specifically because capacity is tight = defer instead.

---

## Red Flag 10: Story Splits Without Updating the Map

**Symptom.** Stories are split in refinement but the story map still shows the original card.
**Why it's bad.** The map is the team's shared model of the user journey and release plan. When splits do not propagate, the map shows a coarser truth than the backlog, and the team plans releases against a stale view.
**Bad example:**
> "'Bulk-edit candidates' card on the map; backlog has 4 split stories under it. Map last updated 5 weeks ago."
**Good example:**
> "Splits propagate to the map: original card becomes a feature header; sub-cards under it represent the slices, each tagged with which release-slice it belongs to. Map and backlog reconcile weekly."
**How to catch it.** Diff card count on map vs ticket count in backlog. If > 30% gap, sync.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Horizontal slicing | Any slice that is 'just UI' or 'just API'? |
| 2 | Splits lose user value | Does each slice ship value? |
| 3 | Slices larger than original | Total slice points <= 1.5x original? |
| 4 | Split by AC | Slice count > AC count? |
| 5 | Spike disguised as story | Title verb is 'investigate' / 'research'? |
| 6 | Splits that always close together | Use feature flags or re-merge |
| 7 | Edge cases sliced off | 'Happy path' / 'edge cases' in title? |
| 8 | No named pattern | Splitter must cite a Lawrence pattern |
| 9 | Splitting to hit capacity | Split timing tied to capacity wall? |
| 10 | Splits not on the map | Card count on map matches backlog? |

## Related Reading

- `SKILL.md` -- the 9 Lawrence patterns
- `references/lawrence-patterns.md` -- workflow step, business-rule, simple/complex, etc.
- Sibling skill: `execution/story-mapping/` -- map cards become split slices
- Sibling skill: `execution/backlog-refinement/` -- INVEST checks on each slice
- Sibling skill: `execution/feature-flag-strategy/` -- ship slices independently
- Sibling skill: `execution/wwas/` -- the Why-What-Acceptance structure for each slice
