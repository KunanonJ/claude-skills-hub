# Cross-Team Dependency Management Reference Guide

A practical reference for tracking, analyzing, and acting on cross-team dependencies. Covers Critical Path Method (CPM), Design Structure Matrix (DSM) basics, Conway's Law-driven org diagnosis, and the recurring failure patterns this skill exists to prevent.

---

## 1. The Dependency Problem

Multi-team programs rarely fail because any single team is incompetent. They fail at the seams. Three patterns dominate post-mortems of failed cross-team programs:

1. **Silent dependencies.** Team A assumed Team B was building X; Team B never knew. Discovered at integration.
2. **Optimistic dates.** Both teams have plausible plans; both plans assume the other team's worst-case estimate is the best-case. Discovered at the deadline.
3. **Recurring dependencies that nobody owns.** Same two teams generate dependencies every quarter; nobody steps back to fix the structural cause.

A live dependency map prevents (1), exposes (2), and creates the data to drive (3).

---

## 2. The Six-Field Dependency Schema

A dependency that is missing any of these fields is not actionable. Add them before discussing the dependency, not after.

| Field | Why it matters |
|-------|----------------|
| `from_team` (consumer) | Names the party with the risk |
| `to_team` (producer) | Names the party with the obligation |
| `description` | One sentence; if you cannot say it in one sentence, it is two dependencies |
| `needed_by` | The consumer's drop-dead date |
| `expected_delivery` | The producer's commitment date |
| `status` | The current state (`not_started`, `in_progress`, `at_risk`, `blocked`, `done`) |

Optional but recommended: `owner` (named individual on the producer side), `criticality`, `notes`.

### Why `needed_by` and `expected_delivery` Are Both Required

A single "date" field collapses two pieces of information: what the consumer needs and what the producer is committing to. The gap between them is the **slack**, which is what tells you whether to worry.

- `expected_delivery <= needed_by`: positive slack, ok.
- `expected_delivery > needed_by`: negative slack, the dependency is structurally late.
- `expected_delivery > needed_by + 14 days`: critical, escalate.

---

## 3. Critical Path Method (CPM)

Kelley and Walker, 1959. Originally for chemical-plant construction, but the math is identical for any DAG of dated dependencies.

### Definition

Given a directed acyclic graph of activities (here: dependencies), each with a duration, the **critical path** is the longest chain. The total length of the critical path equals the minimum total time the program can take, regardless of how much you parallelize elsewhere.

### Why It Matters

Any delay on the critical path delays the entire program. Any delay off the critical path either:

- Eats slack but does not delay the program (until slack reaches zero), or
- Moves the critical path to a previously near-critical chain.

This means: spend coordination effort on the critical path first; spend remaining effort on near-critical chains (slack < 1 week); deprioritize the rest.

### Computing the Critical Path

For this skill's purposes, the simplified algorithm is:

1. Build a directed graph where nodes are dependencies and edges connect dependencies that share a team and form a chain (output of one team feeds another).
2. Compute earliest start and earliest finish for each node using `needed_by` and `expected_delivery`.
3. Compute latest start and latest finish via backward pass.
4. Slack = latest start - earliest start. Nodes with zero slack are on the critical path.

The tool reports the critical path plus the next-shortest-slack chain (the "near-critical").

### Limitations

- CPM assumes fixed durations. Real dependencies have probabilistic durations. PERT (Program Evaluation and Review Technique) adds uncertainty by using three-point estimates; it is overkill for most cross-team programs.
- CPM treats teams as fungible. In practice, two dependencies competing for the same person's attention behave like one (resource constraints). Watch for this.

---

## 4. Design Structure Matrix (DSM)

Steward, 1981. A square matrix where rows and columns are teams (or activities); cells mark dependencies. Useful for spotting clusters of mutual dependency that should be reorganized.

### Reading a DSM

```
              Mobile  Platform  Data  Design
Mobile          -      X        X     X
Platform        X      -        X
Data                   X        -
Design          X                     -
```

- Cell `(Mobile, Platform) = X` means Mobile depends on Platform.
- A symmetric pair (both directions filled) indicates mutual coupling -- a Conway's-Law signal.
- A cluster of dependencies along a band suggests those teams form a natural service group.

This skill does not generate DSMs directly, but the `by_team_pair` output in the JSON gives you the data you need to build one.

---

## 5. Conway's Law Applied

Conway, 1968: organizations ship copies of their communication structures. The corollary for dependency management: a recurring dependency between two teams is a feature of your org chart, not of any particular quarter's plan.

### Diagnostic

Quarterly, count dependencies by `(from_team, to_team)` pair. If a single pair accounts for >25% of all dependencies, you have a structural problem.

### Three Responses (in order of preference)

#### 1. Merge the Teams

If both teams spend more than 30% of their capacity on dependencies with each other, the boundary between them is destroying more value than it creates. Merge.

#### 2. Create a Permanent Interface

If merger is not feasible (different skills, different reporting lines, different SLAs):

- Define an explicit API or service-level agreement.
- Schedule a recurring sync (weekly to biweekly) that drains the inbox.
- Publish ownership and on-call for the interface itself.

#### 3. Add a Permanent Program Manager

For complex multi-team seams (5+ teams interacting), a dedicated program manager (see `program-manager/`) owns the dependency map and the weekly sync.

### Anti-Pattern

Renaming the dependency without fixing the structure. "We'll add a coordination meeting" without changing the org chart or interfaces will produce the same dependencies next quarter.

---

## 6. The Weekly Cross-Team Sync

The single highest-leverage coordination meeting in a multi-team program. Run it well.

### Cadence

Weekly, 30-45 minutes, same time and day. Skipping a week destroys the rhythm.

### Attendees

- Program manager or PM (facilitator)
- One named representative per team with current dependencies
- Optional: exec sponsor (monthly only, not weekly)

### Standard Agenda (45 min)

1. **Critical path walk** (15 min). Each item on the critical path: status, blockers, ask.
2. **At-risk items** (10 min). Items not on critical path but with negative or low slack.
3. **New dependencies** (5 min). Any new dependencies added since last week.
4. **Closed and unblocked** (2 min). Celebrate; mark `done` in the JSON.
5. **Conway's signals** (3 min). Anything that looks recurring; raise quarterly review topic.
6. **Action items and owners** (10 min). One owner per action; due before next sync.

### Anti-Pattern

A sync that walks every dependency in alphabetical order is a sync that nobody attends after week 3. Always lead with the critical path.

---

## 7. Recurring Failure Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Silent dependency discovered at integration** | Surprise blocker 2 weeks before launch | Mandatory monthly dependency-inventory session with team leads |
| **Optimistic delivery dates** | Slack always green, dependencies always late | Require producer team to date `expected_delivery` against current capacity, not aspirational |
| **Stale map** | Map says 12 deps; reality has 18 | Update before, not after, weekly sync; assign the update to the PM, not "everyone" |
| **Map sprawl** | 50+ dependencies, mostly noise | Aggregate at epic level; only model cross-team blocks, not within-team sequencing |
| **Conway's loop** | Same team pair causing 40% of dependencies, every quarter, no action | Quarterly Conway's review with the option to merge, interface, or PM-up the seam |
| **No owner on critical-path item** | Critical-path dep with `owner: TBD` for 3 weeks | Weekly sync requires owner on every critical-path dep; escalate to producer team lead if missing |
| **Status inflation** | Every dep is `at_risk`; signal lost | Define `at_risk` precisely (negative slack OR blocked OR within 7 days of `needed_by` with no progress); train teams |

---

## 8. Communicating Dependency Status Up

Executives do not want to read 30 dependencies. They want three numbers and one decision.

### Executive Summary Template

> **Program:** [name]
> **As of:** [date]
> **Critical path length:** [N items]
> **At-risk count:** [N]
> **Blocked count:** [N]
> **Asks of leadership:** [0-3 specific items]
> **Most-recurring team pair:** [Team A <-> Team B, N deps this quarter]

Generated by `dependency_graph.py` and pasted into the weekly status (see `status-update-generator/`).

---

## 9. JSON Maintenance Tips

- Store the JSON in a Git repo. The diff is the change log.
- One file per program. Do not mix programs in one file.
- Update the JSON via the same channel as everything else (PR, Notion edit, Confluence edit) -- not on a private spreadsheet.
- Archive done dependencies quarterly to keep the active list short. The tool can re-generate any historical view from the archive.

---

## 10. References

- Kelley, James E., and Morgan R. Walker. "Critical-Path Planning and Scheduling." Eastern Joint IRE-AIEE-ACM Computer Conference, 1959.
- Conway, Melvin E. "How Do Committees Invent?" Datamation, April 1968, 28-31.
- Steward, Donald V. "The Design Structure System: A Method for Managing the Design of Complex Systems." IEEE Transactions on Engineering Management, EM-28(3), 1981.
- Eppinger, Steven D., and Browning, Tyson R. *Design Structure Matrix Methods and Applications*. MIT Press, 2012.
- Skelton, Matthew, and Pais, Manuel. *Team Topologies*. IT Revolution Press, 2019. (Conway's Law for modern teams.)
