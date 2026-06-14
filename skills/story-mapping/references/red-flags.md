# Red Flags: Story Mapping

> Common ways this skill's output goes wrong -- concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan every story map before using it for release planning. Each red flag has bad and good quoted examples.

---

## Red Flag 1: Map-as-Gantt

**Symptom.** The "story map" is a horizontal timeline with dates and dependencies. Cards are stacked left-to-right in delivery order.
**Why it's bad.** A story map is a 2D model of the *user journey* with a release-slice axis. A Gantt is a delivery plan. Conflating them loses the customer narrative -- the map shows when work happens, not what experience users will have. Releases become arbitrary date cuts, not coherent user journeys.
**Bad example:**
> "[Horizontal timeline]:
> Sprint 1: stories A, B, C.
> Sprint 2: stories D, E, F.
> ...
> (No journey backbone, no customer activities, just sprints.)"
**Good example:**
> "[Story map with two axes]:
> Backbone (left to right, customer journey): *Discover -> Sign up -> Activate -> Use daily -> Pay -> Upgrade*.
> Slices (top to bottom, releases): R1 (walking skeleton across the journey), R2 (richer activation), R3 (upgrade flow).
> Each card sits at a (journey-step, release) coordinate."
**How to catch it.** No customer-journey backbone label across the top = not a story map.

---

## Red Flag 2: Missing the Customer Journey Backbone

**Symptom.** Map starts directly with stories grouped by feature area ("Auth", "Search", "Settings"), no user activities at the top.
**Why it's bad.** Feature-area grouping is a system view, not a user view. The whole point of Patton's story mapping is to keep the customer journey visible so the team can spot gaps and prioritize end-to-end value. Without the backbone, the map devolves into a categorized backlog.
**Bad example:**
> "Top of map: Auth | Search | Settings | Notifications | Admin.
> (These are system buckets, not user activities.)"
**Good example:**
> "Top of map (customer journey backbone): *Find a candidate -> Schedule interview -> Conduct interview -> Send offer -> Onboard hire*.
> Cards underneath each activity describe what the user does (e.g. 'filter candidates by skill', 'add interview panel', 'send offer letter'). System areas are tags on cards, not the backbone."
**How to catch it.** Backbone columns are nouns (system areas) instead of verbs (user activities) = rewrite the backbone.

---

## Red Flag 3: Walking Skeleton Skipped

**Symptom.** First release slice contains 100% of the activation flow polish but only 50% of the journey -- payment and upgrade flows are not present at all.
**Why it's bad.** The walking skeleton (R1) should be the thinnest possible end-to-end vertical slice that covers the entire journey, even if each step is minimal. Skipping it means R1 ships a half-product that does not deliver end-to-end value; users cannot complete a real workflow.
**Bad example:**
> "R1: 18 stories under Sign-up + Activate. R2 promised to add Pay and Upgrade.
> (Users cannot pay in R1.)"
**Good example:**
> "R1 (walking skeleton): 1-3 stories per backbone step covering the full journey end-to-end. Sign-up flow is functional but minimal. Activate has 1 path. Pay accepts one method. Upgrade exists but only manual.
> R2: enrich the steps where data shows friction."
**How to catch it.** R1 has zero stories under one or more backbone columns = no walking skeleton.

---

## Red Flag 4: Personas Mixed in One Map

**Symptom.** A single map mixes the recruiter journey, the candidate journey, and the admin journey in one set of columns.
**Why it's bad.** Different personas have different journeys with different rhythms. Mashing them creates incoherent backbones ("recruiter signs up -> candidate gets email -> admin sets permissions"), and stories cannot be released coherently. Cross-persona dependencies become invisible.
**Bad example:**
> "Backbone: Sign-up | Schedule | Take interview | Review | Send offer.
> (Mixing recruiter and candidate activities in one row.)"
**Good example:**
> "Three story maps, one per persona:
> - *Recruiter map*: Find candidate -> Schedule interview -> Send offer.
> - *Candidate map*: Receive invite -> Take interview -> Receive decision.
> - *Admin map*: Set roles -> Configure templates -> Audit usage.
> Cross-persona dependencies marked with arrows between maps."
**How to catch it.** Single map has cards owned by different personas in the same backbone column = split.

---

## Red Flag 5: Stories That Are Implementation Tasks

**Symptom.** Cards say "set up the database schema", "configure Kubernetes", "write API endpoint" -- engineering tasks, not user stories.
**Why it's bad.** The map is a user-experience artifact. Implementation tasks belong in tickets, not on the map. Mixing them obscures the user journey and confuses prioritization (you cannot meaningfully release "set up Kubernetes" to a user).
**Bad example:**
> "Cards under 'Sign up': set up Postgres, configure Auth0, write /users API endpoint, deploy to staging."
**Good example:**
> "Cards under 'Sign up': enter email and password, verify via email link, set up profile, choose plan.
> (Implementation tasks live as sub-tickets in Jira, not on the map.)"
**How to catch it.** Card content describes systems / infrastructure / code, not user actions = rewrite as a user story.

---

## Red Flag 6: Map Becomes a Static Wall Decoration

**Symptom.** The map was created at the start of the project and has not been touched in 4 months.
**Why it's bad.** A map is a thinking tool, not a deliverable. If it does not evolve as the team learns, it lies -- showing a plan that no longer matches reality. New team members read it as truth and waste time aligning to the wrong picture.
**Bad example:**
> "Map last updated: January. Today: May. R1 shipped in March; R2 in progress; nothing on the map reflects this."
**Good example:**
> "Map updated weekly in the backlog refinement session: stories moved from Up Next to In Progress to Done; new stories added based on user research; releases re-sliced based on what we learned. Snapshots committed to git per release."
**How to catch it.** Map's last edit > 3 weeks ago = map is dead.

---

## Red Flag 7: No Release Slicing Strategy

**Symptom.** Cards are listed under journey steps but there are no horizontal lines or labels showing R1 / R2 / R3.
**Why it's bad.** The second axis of the map is the whole point -- it forces the team to decide *what is in this release vs. later*. Without it, the map is just a categorized backlog, and the team ends up releasing whatever happens to be done.
**Bad example:**
> "Map shows 200 cards under the journey backbone. No release slicing."
**Good example:**
> "Map shows 200 cards. Horizontal slice 1 (R1, walking skeleton): 32 cards, ships end of Q2. Slice 2 (R2, depth in activation): 48 cards, Q3. Slice 3 (R3, enterprise journey): 60 cards, Q4. Remaining 60 unsliced (future)."
**How to catch it.** No release labels on the vertical axis = add them.

---

## Red Flag 8: Mapping a Solution, Not a Problem

**Symptom.** The map describes the team's planned product, not the user's actual current journey.
**Why it's bad.** Story mapping is most powerful when it surfaces the gap between the current user journey (with all its workarounds) and the future product. Mapping only the proposed solution skips the diagnostic step and means the team builds without seeing where users today get stuck.
**Bad example:**
> "Map shows the new product's flow: sign up -> create dashboard -> share -> upgrade. No mention of how users do this today (e.g. in spreadsheets)."
**Good example:**
> "Two-state map:
> - Top row: *current user journey* (with workarounds, friction points marked in red).
> - Bottom row: *future product journey* (same backbone, redesigned).
> The gaps between top and bottom are the team's bets."
**How to catch it.** Map only shows the future state = add the current-state row before slicing releases.

---

## Red Flag 9: Cards Without Acceptance Criteria

**Symptom.** The map has user-friendly cards ("filter candidates by skill") but no acceptance criteria, INVEST checks, or testable behavior.
**Why it's bad.** A story map is the planning artifact; cards eventually become stories that need to be testable. Treating the map as the final form means stories enter sprints under-defined, get extended mid-sprint, and the slicing collapses.
**Bad example:**
> "Card: 'filter candidates by skill'.
> Sprint starts; team realizes there are 4 interpretations; story splits into 3 mid-sprint."
**Good example:**
> "Card: 'filter candidates by skill'.
> When the card moves from the map into a sprint, it gets enriched (see `backlog-refinement` skill): persona, scenario, acceptance criteria (Given/When/Then), INVEST check. The map keeps the short card form for the journey view."
**How to catch it.** Stories pulled into a sprint without enrichment = link map to `backlog-refinement` skill.

---

## Red Flag 10: One-Person Map

**Symptom.** The PM built the map alone and is now presenting it to the team.
**Why it's bad.** The value of story mapping is the *building* -- the shared understanding that emerges when PM, design, and engineering co-create. A one-person map is a delivery document, missing the assumptions challenge, the technical-feasibility input, and the design alternatives.
**Bad example:**
> "PM spent the weekend building the map. Presenting it Monday for team review."
**Good example:**
> "Map built in a 3-hour workshop: PM, design lead, eng lead, customer-success rep. Each persona's journey researched ahead of time (interview-synthesis outputs). Map exits with shared understanding, surfaced assumptions logged separately."
**How to catch it.** Map has a single author = re-do as a workshop.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Map-as-Gantt | Backbone column labels are journey verbs? |
| 2 | No journey backbone | Top row uses verbs (activities), not nouns (areas)? |
| 3 | Walking skeleton skipped | R1 has stories under every backbone step? |
| 4 | Personas mixed | One persona per map? |
| 5 | Stories are implementation tasks | Cards describe user actions, not systems? |
| 6 | Map gone stale | Last edit < 3 weeks ago? |
| 7 | No release slicing | Release labels on vertical axis? |
| 8 | Mapping a solution, not a problem | Current-state row included? |
| 9 | Cards lack acceptance criteria | Enrichment linkage to refinement skill? |
| 10 | One-person map | Built collaboratively in a workshop? |

## Related Reading

- `SKILL.md` -- Patton's user story mapping
- `references/mapping-patterns.md` -- backbone / slice / walking-skeleton patterns
- Sibling skill: `discovery/interview-synthesis/` -- the customer-journey research that feeds the backbone
- Sibling skill: `execution/backlog-refinement/` -- enrich map cards into INVEST stories
- Sibling skill: `execution/story-splitting/` -- vertical-slice patterns for over-large cards
- Sibling skill: `execution/outcome-roadmap/` -- map fits between roadmap and refined backlog
