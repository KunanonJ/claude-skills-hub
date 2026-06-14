# Red Flags: Dependency Map

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan the dependency JSON and `dependency_graph.py` output before the weekly cross-team sync. Each red flag shows the *bad* version next to the *good* version, anchored to the Critical Path Method (Kelley & Walker) and Conway's Law.

---

## Red Flag 1: Invisible dependencies

**Symptom.** A team blocks another team for 3 weeks. Only discovered at the all-hands when the blocked team's lead complains.

**Why it's bad.** Dependencies that exist but are not captured in the JSON do not get critical-path analysis, do not appear in the weekly sync, and do not get explicit ownership. They surface as surprises — usually at the worst possible time.

**Bad example:**
> "JSON has 8 dependencies. (Reality: 22 cross-team dependencies actually exist this quarter. The other 14 live in Slack DMs, sprint goals, and individual engineers' heads.)"

**Good example:**
> "Quarterly inventory session (90 min): each team lead lists every cross-team need for the planning period. Combined into a single JSON with one sentence per dependency. Updated weekly. Any dependency that surfaces outside the JSON is logged within 24 hours; root cause discussed in the next sync."

**How to catch it.** Compare the JSON's count to a fresh 90-min team-by-team interview. If you find > 30% new dependencies, the map is missing the majority.

---

## Red Flag 2: No due dates on the arrows

**Symptom.** Dependencies are listed but `needed_by` and `expected_delivery` are blank or "TBD".

**Why it's bad.** Without dates, the critical-path algorithm cannot compute slack. Risk classification fails. The team sees a graph of arrows with no urgency signal. The map looks comprehensive but is decorative.

**Bad example:**
> "DEP-014: Mobile needs OAuth refresh-token API from Platform. needed_by: TBD. expected_delivery: TBD. status: not_started. (Critical path computation: empty.)"

**Good example:**
> "DEP-014: Mobile needs OAuth refresh-token API from Platform. needed_by: 2026-06-15 (the date Mobile's iOS auth refactor hits the integration milestone). expected_delivery: 2026-06-10 (Platform's lead committed in last week's sync). status: in_progress. slack: +5 days. criticality: critical. owner: Alex Lee."

**How to catch it.** Filter the JSON for items missing `needed_by` or `expected_delivery`. Each one is invisible to critical-path analysis.

---

## Red Flag 3: Stale map (4-week-old reality)

**Symptom.** Map was updated 4 weeks ago. Three dependencies have shifted dates; two were completed; one new one emerged. None reflected.

**Why it's bad.** A 2-week-old map is misleading; a 4-week-old map is harmful. Teams plan against false signal; the weekly sync walks a graph that no longer exists; trust in the artifact erodes.

**Bad example:**
> "Mermaid diagram from Apr 8 still posted in Confluence. Current date May 22. Three dependencies have completed; one new critical dependency added in Slack but not the map."

**Good example:**
> "Map update SLA: every Friday before 4pm. Owner: the program manager. Update process: each team lead confirms their dependencies via 5-min async ping; PM applies updates; Mermaid regenerated; new critical path computed. If the map is > 7 days old, the weekly sync is cancelled until the map is refreshed (forcing the discipline)."

**How to catch it.** Look at the map's last-updated timestamp. > 7 days = stale.

---

## Red Flag 4: Recurring dependencies between same two teams ignored

**Symptom.** Mobile depends on Platform in 8 out of 14 quarterly dependencies. This has been true for 4 quarters. Nobody has raised it as a structural issue.

**Why it's bad.** Conway's Law: when the same two teams generate dependencies every quarter, the org structure *is* the dependency. Three responses exist (merge, permanent interface, dedicated program manager). Ignoring the pattern means re-litigating the same coordination problem every 90 days.

**Bad example:**
> "Q1: 6 Mobile-needs-Platform deps. Q2: 7. Q3: 8. Q4 planning: 9 already on the list. 'Same as last quarter.'"

**Good example:**
> "Quarterly Conway's Law review: Mobile↔Platform dependency volume tracked. Q4 review surfaces the pattern: '8 dependencies/quarter sustained over a year. Recommendation: either (a) consolidate Mobile and Platform under one EM with shared planning, (b) build a stable internal API contract (Platform-as-Service) with quarterly versioning so Mobile no longer ad-hoc-requests, or (c) add a permanent Mobile-Platform integration PM. Decision: option (b). Q1 next year: API contract v1 ships, Mobile self-services from it, dep count drops to 3.'"

**How to catch it.** Pivot the `by_team_pair` output across the last 4 quarters. Any pair with sustained > 5 deps/quarter is a structural problem.

---

## Red Flag 5: Granularity too fine

**Symptom.** JSON has 80 dependencies. Most are at task level ("Frontend needs button asset from Design", "Backend needs DB column from DBA").

**Why it's bad.** Task-level dependency tracking is unmaintainable. The map becomes a worse version of Jira. Real cross-team blockers get lost in noise. The Mermaid diagram is unreadable.

**Bad example:**
> "80 deps. Includes 'Frontend needs button asset', 'Mobile needs icon update', 'Backend needs column added'. Mermaid unrenderable; PM gives up on the visual."

**Good example:**
> "12 deps at the epic level. Each represents 1-2 weeks of cross-team work. Intra-team dependencies (Frontend needing asset from in-team Designer) live in the team's sprint board, not the cross-team map. The map answers: 'who is blocking whom across team boundaries this quarter?'"

**How to catch it.** Count dependencies. > ~25 per program is granularity too fine. Aggregate to epic.

---

## Red Flag 6: Status field always reads "at_risk"

**Symptom.** 60% of dependencies are status `at_risk`. Team treats it as a generic "this is hard" flag.

**Why it's bad.** When everything is at-risk, nothing is at-risk. The signal is lost. The weekly sync devolves into reading the list aloud with no prioritization.

**Bad example:**
> "16 deps, 11 marked `at_risk`. Weekly sync agenda: 'walk all 11 at-risk items'. Meeting runs 90 min; no decisions made."

**Good example:**
> "Status definitions enforced: `at_risk` = dates are slipping OR scope is changing OR owner has flagged blocker. Default for normal in-flight work is `in_progress`. Of 16 deps: 2 at_risk (specific reasons named), 10 in_progress, 3 done, 1 blocked. Weekly sync focuses on the 2 + 1 = 3 items needing decisions."

**How to catch it.** Compute the % of deps at `at_risk` or `blocked`. > 30% sustained = status definitions are loose.

---

## Red Flag 7: Critical path has no named owner

**Symptom.** The critical path includes 5 dependencies. The `owner` field is blank for 3 of them.

**Why it's bad.** Critical-path items determine the earliest possible delivery date. An unowned critical item drifts. The team will discover the slip at the next milestone, with no person to escalate to.

**Bad example:**
> "Critical path (5 items): DEP-001 owner Alex; DEP-007 owner: blank; DEP-014 owner: blank; DEP-022 owner Sarah; DEP-031 owner: blank."

**Good example:**
> "Critical path (5 items), all owned: DEP-001 (Alex L), DEP-007 (Tomas R), DEP-014 (Marcus B), DEP-022 (Sarah K), DEP-031 (Priya N). Weekly sync requires each owner to give a 30-sec status; missing owner = the program manager fills in temporarily and the team lead picks one before next sync."

**How to catch it.** Filter critical_path for items where `owner` is empty or "TBD". Any = unowned critical work.

---

## Red Flag 8: Mermaid unreadable with too many nodes

**Symptom.** Mermaid diagram has 30+ nodes. Rendered, it is an illegible spaghetti tangle. Team stops looking at it.

**Why it's bad.** A diagram that no one reads provides no coordination value. The visual stops being a tool and becomes a chore.

**Bad example:**
> "Full Mermaid render: 34 nodes, ~50 edges, three colors. Confluence page loads slowly; nobody opens it."

**Good example:**
> "Filtered views: (1) `--criticality critical,high` shows the 7 critical/high deps in a readable graph; (2) `--team Mobile,Platform` shows just the Mobile-Platform seam; (3) full graph available on request but not the default. Each filtered view is publishable as a separate Confluence section."

**How to catch it.** Open the rendered diagram. If a team member cannot trace one dependency in 5 seconds, the view is too dense — filter.

---

## Red Flag 9: Dependency JSON not the single source of truth

**Symptom.** Same dependencies live in 3 places: the JSON, a Confluence spreadsheet, and a slide in the weekly exec deck. Each has slightly different states.

**Why it's bad.** Multiple sources of truth means no source of truth. The team spends time reconciling rather than coordinating. New joiners do not know which is current.

**Bad example:**
> "Confluence sheet says DEP-014 is 'in progress'. JSON says 'at_risk'. Exec deck shows 'on track'. Three readers, three answers."

**Good example:**
> "JSON is the single source of truth. The Confluence page and exec deck are *rendered from* the JSON via `dependency_graph.py --format confluence` and `--format markdown`. The spreadsheet is retired. Update process: edit the JSON; regenerate the views; never edit downstream."

**How to catch it.** Ask 3 team members where to find the current dependency status. If they name different sources, the system is fragmented.

---

## Red Flag 10: Conversation skipped because "the map is updated"

**Symptom.** Program manager updates the JSON Friday afternoon. Skips the weekly sync. Assumes the document does the coordination work.

**Why it's bad.** The map surfaces what to talk about; the talking still has to happen. A map updated but unspoken-to does not produce coordination. Trust between teams is built in conversation, not in artifact-reading.

**Bad example:**
> "PM: 'I updated the map; please review async. Cancelling the weekly sync this week — saves us 30 min.' (4 weeks later: two teams have drifted; one critical path item slipped 2 weeks.)"

**Good example:**
> "Weekly sync is non-negotiable, 25 minutes, agenda set by the map. Walk: (1) critical path items — each owner gives 30-sec status; (2) at-risk items — 1-min decision per; (3) newly added since last week; (4) Conway's Law observation if pattern emerging. PM updates JSON during/after the meeting based on conversation."

**How to catch it.** Last sync date and last map-update date. If updates happen but no sync, talking is being skipped.

---

## Red Flag 11: Dependencies modeled in the wrong direction

**Symptom.** DEP-014 says `from_team: Platform`, `to_team: Mobile`, `description: "deliver OAuth API"`. Direction is reversed.

**Why it's bad.** The model assumes `from_team` = the team that NEEDS the work; `to_team` = the team that OWES the work. Reversed direction breaks the critical-path computation and the risk classification.

**Bad example:**
> "DEP-014: from_team: Platform (the producer). to_team: Mobile (the consumer). (Critical path computation: incorrect.)"

**Good example:**
> "DEP-014: from_team: Mobile (the consumer/blocked party). to_team: Platform (the producer/blocker). description: 'OAuth refresh-token API'. needed_by: 2026-06-15. (Mobile needs it from Platform; Platform owes it.)"

**How to catch it.** Read a few dependency descriptions. Does the arrow point from consumer to producer? If reversed, the direction convention is broken.

---

## Red Flag 12: Critical path treated as fixed

**Symptom.** Critical path was computed at the start of the quarter. Six weeks in, no one has recomputed. New dependencies have been added, but the team is still focused on the old critical path.

**Why it's bad.** The critical path is dynamic. A single new dependency can shift it. Working hard on the formerly-critical path while ignoring a newer one is misallocated attention.

**Bad example:**
> "Q3 kickoff: critical path computed (5 items). Week 7: 3 new deps added but `dependency_graph.py` not re-run. Team continues to focus on the original 5; meanwhile DEP-040 (added week 4) is now critical and unowned."

**Good example:**
> "`dependency_graph.py` runs every Friday as part of the map refresh. Critical path is recomputed; new critical items are highlighted in the weekly sync agenda. Old critical items that lost criticality are noted but no longer the top focus."

**How to catch it.** Last time the critical path was recomputed? If > 14 days and the JSON has changed since, the focus is stale.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Invisible dependencies | Fresh team-by-team interview vs JSON count |
| 2 | No due dates on arrows | Any dep with blank needed_by/expected_delivery? |
| 3 | Stale map | Map's last-updated timestamp |
| 4 | Recurring same-team deps ignored | Pivot by_team_pair across last 4 quarters |
| 5 | Granularity too fine | Total dep count > 25? |
| 6 | Always "at_risk" | What % of deps have status at_risk or blocked? |
| 7 | Critical path unowned | Any critical-path dep with empty owner? |
| 8 | Mermaid unreadable | Can a team member trace one dep in 5 seconds? |
| 9 | Multiple sources of truth | Ask 3 people where to find current status |
| 10 | Map updated but no sync | Last sync date vs last map-update date |
| 11 | Direction reversed | Does arrow point consumer → producer? |
| 12 | Critical path treated as fixed | When was critical path last recomputed? |

## Related Reading

- SKILL.md Troubleshooting
- references/dependency-management-guide.md
- Kelley, James E., and Morgan R. Walker, "Critical-Path Planning and Scheduling" (1959)
- Conway, Melvin E., "How Do Committees Invent?" (1968)
- `program-manager/` (the role that maintains the map)
- `pre-mortem/` (tigers often map to specific dependencies)
- `cycle-time-analyzer/` (long cycle times often correlate with cross-team blocks)
