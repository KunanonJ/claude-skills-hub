# Example: Splitting an "Import Data from External Sources" Epic with All 9 Lawrence Patterns

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Pylon (devops/infra, Series A, 30 people) is building a new capability: "Import data from external sources." Customers want to bring in their existing config and metrics from competing tools (Datadog, PagerDuty, GitHub Actions, Jenkins). The PM (Sasha) wrote a single epic for it. The engineering lead, Marcus, pushed back: "this is a 6-month thing pretending to be one ticket."

Sasha is using Richard Lawrence's nine vertical-slicing patterns to break the epic into thin, end-to-end stories. The goal: every story is independently shippable and delivers some user-visible value.

## Inputs

- Original epic: "Import data from external sources"
- Original size estimate: ~14 weeks for one engineer
- Five candidate source systems: Datadog, PagerDuty, GitHub Actions, Jenkins, custom CSV
- Three data kinds per source: config, metrics, audit history
- Mix of access methods: API tokens, OAuth, file upload
- Two import modes: one-shot vs continuous sync

## Applying the skill

For each of Lawrence's 9 patterns, take the chunky epic and produce a before/after pair. The "after" is a thin story that has user-visible value on its own. The pattern's name tells you *what dimension* you sliced along.

## The artifact

### Original epic (the "before" -- in all 9 sections it stays the same)

> **As a** Pylon admin
> **I want** to import my config, metrics, and audit history from any of {Datadog, PagerDuty, GitHub Actions, Jenkins, custom CSV}
> **So that** I can switch to Pylon without rebuilding from scratch
> **Acceptance:** All 5 sources, all 3 data kinds, both one-shot and continuous sync, surfaced in the dashboard with full audit trail.
>
> Estimate: ~14 weeks. Cannot be sprint-committed. Not testable in one go.

---

### Pattern 1: Workflow Steps

**What you do:** Slice along the steps of the workflow. Deliver one step end-to-end first; deliver later steps in subsequent stories.

**After:**
- *Story 1a:* Admin can connect to Datadog with an API token and Pylon shows "Connected: Datadog" with the connection's last-validated timestamp. (Just the connect step, no import yet.)
- *Story 1b:* Admin can trigger a one-shot import from a connected Datadog and see "X items found, 0 imported" preview.
- *Story 1c:* Admin can run the actual import; imported items show up in the dashboard.

Each is testable. Each delivers user-visible value (connect, preview, import).

---

### Pattern 2: Business Rule Variations

**What you do:** Find the variations within a single rule and ship one variation first.

**After:**
- *Story 2a:* Import config from Datadog when the source workspace has fewer than 500 monitors. (Happy path, small workspace.)
- *Story 2b:* Import config from Datadog when source workspace has 500-5,000 monitors (introduces pagination + chunked write).
- *Story 2c:* Import config from Datadog with name-conflict resolution rules (the "what if a Pylon monitor of the same name exists?" rule set).

---

### Pattern 3: Happy/Unhappy Path

**What you do:** Ship the happy path. Ship error handling separately.

**After:**
- *Story 3a:* Import succeeds (happy path): valid token, source available, no conflicts. Importing items show up.
- *Story 3b:* Token-rejected unhappy path: clear error message + how-to-fix link.
- *Story 3c:* Source-timeout unhappy path: retry with backoff, partial-import save, resume button.
- *Story 3d:* Partial-failure unhappy path: imported 480/500 items; show the 20 that failed and why.

---

### Pattern 4: Input Options / Platform

**What you do:** Slice by input source -- one source at a time, not all five.

**After:**
- *Story 4a:* Datadog import end-to-end.
- *Story 4b:* PagerDuty import end-to-end.
- *Story 4c:* GitHub Actions import end-to-end.
- *Story 4d:* Jenkins import end-to-end.
- *Story 4e:* CSV upload import end-to-end.

Each can ship on its own. Datadog first because 60% of Pylon's pipeline customers come from Datadog.

---

### Pattern 5: Data Types or Parameters

**What you do:** Slice by data kind -- ship one kind at a time.

**After:**
- *Story 5a:* Import only config (monitors, dashboards) from Datadog.
- *Story 5b:* Import only metrics history from Datadog.
- *Story 5c:* Import only audit logs from Datadog.

Config first because it is the most-asked-for and unblocks the "switch from Datadog to Pylon" story.

---

### Pattern 6: Operations (CRUD-style)

**What you do:** Slice by what action the user can take on the imported data.

**After:**
- *Story 6a:* Read-only -- imported items visible in the dashboard. No editing.
- *Story 6b:* Edit -- admin can edit imported items. Original source not updated.
- *Story 6c:* Delete -- admin can delete imported items.
- *Story 6d:* Re-sync -- on demand, fetch latest from source and update local copy.

Read-only ships first. It is the smallest delivery that has value: "I can see my Datadog config in Pylon."

---

### Pattern 7: Test Scenarios / Test Data

**What you do:** Ship the smallest set of test scenarios first; add more as confidence grows.

**After:**
- *Story 7a:* Works for "Acme Analytics-shaped" data: ~200 monitors, 3 teams, English-only names. (Our happiest design-partner shape.)
- *Story 7b:* Works for "Skyway Logistics-shaped" data: 4,000 monitors, 18 teams, mixed-language names. (Pushes pagination + Unicode.)
- *Story 7c:* Works for "Northwind SaaS-shaped" data: regulated industry, audit-log retention rules, SSO-only access.

---

### Pattern 8: Defer Performance

**What you do:** Ship a slow-but-correct version first. Optimize later.

**After:**
- *Story 8a:* Single-threaded import. May take 30 minutes for a 5,000-monitor source. Functionally correct; slow.
- *Story 8b:* Parallel import with worker pool. 5,000 monitors in <3 minutes.
- *Story 8c:* Streaming import. User sees items appear as they import.

Story 8a is shippable. Customers will tolerate a 30-minute one-shot import because it is a one-time migration. Optimization comes later when the team has more signal.

---

### Pattern 9: Major Effort

**What you do:** Identify the single biggest engineering investment (typically the heart of the work) and call it out as its own story. Make sure it is part of a thin slice that also delivers value.

**After:**
- *Major-effort story (9a):* Build the import primitive itself -- the abstraction that any future source plugs into. Ship it with the Datadog plugin so the abstraction is validated by one real case. This is the architecture story.
- *Story 9b:* Add the PagerDuty plugin on top of the primitive.
- *Story 9c:* Add the GitHub Actions plugin on top of the primitive.

The Major Effort pattern is the recognition that some abstractions are inherently big. You do not try to "thin-slice the architecture" -- you ship the architecture *with* the smallest validating case.

---

### The combined first-month slice (using multiple patterns)

After splitting, the team picks the highest-value combination for the first sprint:

> **First-month deliverable** (combines Workflow Steps + Input Options + Data Types + Operations + Defer Performance):
>
> "Connect to Datadog with an API token, run a one-shot import of *config only* (no metrics, no audit), see imported items read-only in Pylon dashboard. Single-threaded import is fine. Happy path only -- token failures show 'try again' but other errors are deferred."
>
> This is ~3 weeks of work. It is genuinely shippable. It delivers the "switch from Datadog" story for the smallest customers. It validates the import primitive (Major Effort) with one real source.

### Before/after comparison

| Aspect | Before (original epic) | After (split + combined first slice) |
|--------|------------------------|--------------------------------------|
| Size | ~14 weeks | ~3 weeks for first slice |
| Users helped on day 1 of release | All or none | Datadog-coming customers (60% of pipeline) |
| Risk if cancelled mid-way | Total | Partial value already shipped |
| Testability | One giant end-to-end | Each slice testable independently |
| Discoverable bugs | Late | Early, on each slice |
| Customer feedback before full build | None | After 3 weeks |
| Re-prioritization possible | No | Yes, every 2-3 weeks |

### Backlog after splitting (full)

| ID | Story | Pattern | Estimate |
|----|-------|---------|----------|
| IMP-1 | Connect to Datadog (no import) | Workflow Steps | 1w |
| IMP-2 | Datadog config import, happy path, read-only | Combined | 2w |
| IMP-3 | Datadog config import: unhappy paths | Happy/Unhappy | 1w |
| IMP-4 | Datadog metrics import | Data Types | 2w |
| IMP-5 | Datadog: edit/delete/re-sync | Operations | 1w |
| IMP-6 | Parallel-worker performance pass | Defer Performance | 1w |
| IMP-7 | PagerDuty plugin | Input Options | 1.5w |
| IMP-8 | GitHub Actions plugin | Input Options | 1.5w |
| IMP-9 | Jenkins plugin | Input Options | 1.5w |
| IMP-10 | CSV upload plugin | Input Options | 1w |
| IMP-11 | Continuous-sync (vs one-shot) | Business Rule Variation | 2w |
| IMP-12 | Audit log import (all sources) | Data Types | 1.5w |

Total ~17 weeks of distributable work, but every 2-3 weeks ships a real thing.

## Why this works

- All 9 Lawrence patterns are applied -- the team can compare patterns and pick the most useful axes for *their* epic.
- Each split story passes the INVEST test (Independent, Negotiable, Valuable, Estimable, Small, Testable).
- The combined first slice picks the highest-value axes (Workflow Steps + Input Options + Data Types + Operations) and ships in 3 weeks instead of 14.
- The Major Effort pattern is called out explicitly. The team does not pretend the architecture work is "thin." It is bundled with the first validating case.
- Out-of-scope axes (CSV upload, continuous sync, audit history) are *named*, not hidden. They are in the backlog with sequence.

## What's next

- Score the split backlog with `../prioritization-frameworks/` (RICE).
- Roll the split stories into a story map via `../story-mapping/`.
- Convert stories to WWAS format via `../wwas/`.
- Define DoR/DoD for each via `../backlog-refinement/`.
- Track delivery via `../../sprint-retrospective/` and `../status-update-generator/`.
