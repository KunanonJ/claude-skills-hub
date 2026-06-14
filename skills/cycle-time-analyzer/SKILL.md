---
name: cycle-time-analyzer
description: >
  Flow metrics analyzer (lead time, cycle time, throughput, WIP, aging WIP)
  for sprint and team health, with cumulative flow diagrams.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-execution
  updated: 2026-05-21
  python-tools: flow_metrics.py
  tech-stack: kanban, flow-metrics, cfd, littles-law, aging-wip
---
# Cycle Time Analyzer (Flow Metrics)

## Overview

Compute and visualize the four core Kanban flow metrics -- lead time, cycle time, throughput, and work-in-progress -- from issue history data exported from Jira, Linear, GitHub Projects, or any tracker that records status transitions. The output is a dashboard suitable for sprint retrospectives, executive reporting, and bottleneck analysis, plus a Mermaid cumulative flow diagram that visualizes work accumulation over time.

Flow metrics are the most useful diagnostic for team and process health, far more so than velocity or story points. Daniel Vacanti's body of work (notably *Actionable Agile Metrics for Predictability*, 2015) makes the case that a team's predictability and throughput are governed by Little's Law (`Throughput = WIP / Cycle Time`), and that the most reliable way to improve delivery is to lower WIP and stabilize cycle time -- not to estimate harder.

This skill ingests a JSON file of issues with status transition history and produces all four flow metrics plus aging WIP (the work-in-progress that is older than the team's 85th percentile cycle time -- the items most at risk). All outputs support the shared `--format` schema (json, markdown, mermaid, confluence, notion, linear).

### When to Use

- **Sprint retrospective** -- A team wants data-driven discussion of why some sprints feel slow.
- **Bottleneck investigation** -- Throughput has fallen and the team needs to identify the constraining step.
- **Quarterly delivery review** -- Leadership wants a real picture of delivery performance beyond story-point velocity.
- **Predictability analysis** -- Stakeholders want delivery forecasts grounded in actual cycle time distributions (use with Monte Carlo via `scrum-master/`).
- **WIP-limit calibration** -- A Kanban team is setting WIP limits and needs a baseline of current behavior.

### When NOT to Use

- For story-point velocity tracking, use `scrum-master/velocity_analyzer.py`.
- For sprint capacity calculation, use `scrum-master/sprint_capacity_calculator.py`.
- For per-person performance evaluation -- flow metrics are team-level signals; using them to rank individuals destroys the team behavior they measure.

## The Four Flow Metrics (Vacanti)

### 1. Lead Time

The total elapsed time from the moment a work item is committed (created or moved out of backlog into "Ready") to the moment it is delivered (closed / deployed / accepted).

Lead time is the customer's view: "how long from when I asked to when I got it?"

### 2. Cycle Time

The elapsed time from when work actively started (item moves to "In Progress") to delivery. Cycle time excludes time the item sat in "Ready" or "To Do."

Cycle time is the team's view: "how long does it take us to finish what we start?"

Always report cycle time as a distribution (50th, 85th, 95th percentile), never as an average. Averages hide variability and lead to over-confident commitments.

### 3. Throughput

The count of items completed per unit time (typically per week or per sprint). Throughput is the team's delivery rate.

Throughput is more reliable than story-point velocity because it counts atomic units (one completed thing = one), avoiding estimation bias.

### 4. Work-In-Progress (WIP)

The count of items started but not yet finished at a point in time. WIP includes everything in any "in flight" state (In Progress, In Review, Blocked, etc.).

### Little's Law

The relationship that ties the four together (John D. C. Little, 1961):

```
Average Cycle Time = Average WIP / Average Throughput
```

The practical implication: **the fastest way to reduce cycle time is to reduce WIP.** Working on fewer things at once forces finishing before starting and exposes the bottlenecks.

### Aging WIP

The aging WIP report lists every item currently in flight and its age (days since started). Items older than the team's 85th-percentile cycle time are flagged as "at risk" -- they are statistical outliers and warrant explicit attention in standups and refinements.

Aging WIP is the single most actionable flow metric for daily use. Most teams ignore it. Most teams have a few items quietly aging in the corners.

## Workflow

1. **Export issue history** from your tracker as JSON. Required fields per issue: `id`, `title`, `created_at`, `status_history` (list of `{status, entered_at}`), and ideally `team` and `type`. See `references/flow-metrics-guide.md` for tracker-specific export instructions.
2. **Define your states.** Tell the tool which status names map to "Ready" (commitment), "In Progress" (active work start), and "Done" (delivery). Defaults: `Ready`/`To Do`, `In Progress`, `Done`.
3. **Run the analyzer.** `python scripts/flow_metrics.py --input issues.json --format markdown`
4. **Review the distribution.** Look at 85th-percentile cycle time, not the average. Identify aging WIP that exceeds it.
5. **Generate the CFD.** Use `--format mermaid` to produce a cumulative flow diagram for share-back in retrospectives or exec reports.
6. **Calibrate WIP limits.** Use the WIP histogram to set per-state WIP limits at roughly the team's current 50th percentile.
7. **Re-run weekly.** Track the trend, not the snapshot. Flow metrics drift; only sustained changes are meaningful.

## Tools

| Tool | Purpose | Command |
|------|---------|---------|
| `flow_metrics.py` | Compute lead time, cycle time, throughput, WIP, aging WIP, CFD | `python scripts/flow_metrics.py --input issues.json --format markdown` |

Demo mode: `python scripts/flow_metrics.py --demo --format markdown` produces sample output without input data.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Cycle time looks great but team feels slow | "In Progress" defined too narrowly; long "In Review" or "Blocked" time excluded | Map all in-flight states to the active set; verify with the team that the boundary matches "start" and "finish" reality |
| Throughput is unstable week-over-week | Sprint commitment volume changes; team-size changes; vacation periods | Report a rolling 6-8 week trend; annotate the chart with known events |
| Lead time is enormous compared to cycle time | Items sit in backlog for months before commitment | Either accept (lead time is bounded by intake, not delivery) or close stale backlog items; report lead time only for items committed within the last quarter |
| Aging WIP list is enormous | Stale items left "In Progress" without movement | Triage during standup; close, split, or restart each item; consider a WIP limit to prevent recurrence |
| 85th percentile cycle time differs sharply between work types | Mixed bugs, features, spikes in one stream | Filter by `type` and report per-type cycle time; predictability comes from like-with-like comparison |
| CFD lines flatten then jump | Status transitions logged in batch (end-of-day or weekly sync) rather than real-time | Either accept the visual artifact or migrate to real-time updates in the tracker |
| Tool errors on missing `status_history` | Tracker export incomplete; some issues lack transition data | Use `--ignore-missing` to skip incomplete items; investigate the export query |

## Success Criteria

- All four flow metrics are computed and reported with both central tendency (median) and tail (85th percentile).
- The cumulative flow diagram is generated and shared in at least one retrospective per sprint.
- Aging WIP list is reviewed at least weekly; items exceeding 85th percentile cycle time get explicit attention.
- WIP limits are set per state based on observed flow rather than guessed.
- Trend reporting uses rolling windows (6-8 weeks), not single snapshots.
- Cycle time distribution is reported, never just an average.
- Flow metrics are used at the team level only; never for individual performance ranking.

## Scope & Limitations

**In Scope:**
- Lead time, cycle time, throughput, WIP, aging WIP calculation
- Cumulative flow diagram generation (Mermaid)
- Per-type filtering (bug, feature, spike)
- All six output formats per `SHARED_OUTPUT_SCHEMA.md`

**Out of Scope:**
- Monte Carlo delivery forecasting (use `scrum-master/velocity_analyzer.py`)
- Story-point velocity (use `scrum-master/`)
- Resource capacity planning (use `senior-pm/resource_capacity_planner.py`)
- Code-level metrics (PR review time, deploy frequency -- use DevOps-focused tools)

**Important Caveats:**
- Flow metrics depend on accurate status transitions. If your team batch-updates the board once a day, the cycle time data will be discretized by that batch interval.
- A team that gamifies flow metrics will produce better-looking numbers without changing real delivery. Use these metrics as a diagnostic, not a target. (Goodhart's Law.)
- Cycle time is a team property, not an individual property. Resist the urge to compute per-assignee cycle time -- it will incentivize hand-offs that hurt the team.

## Integration Points

| Integration | Direction | What Flows |
|-------------|-----------|------------|
| `scrum-master/` | Complementary | Flow metrics + velocity together provide the full delivery picture |
| `scrum-master/retrospective_analyzer.py` | Feeds into | Flow trends inform retro topics |
| `dependency-map/` | Complementary | Long cycle times often correlate with cross-team dependencies |
| `sprint-retrospective/` | Feeds into | CFD and aging WIP are standard retro inputs |
| `senior-pm/project_health_dashboard.py` | Feeds into | Throughput trends feed portfolio health |
| `status-update-generator/` | Feeds into | Weekly status includes throughput and aging WIP highlights |
| `agile-coach/` | Used by | Coaches use flow metrics to assess team maturity |

## Tool Reference

### flow_metrics.py

Computes the four core flow metrics plus aging WIP and a Mermaid cumulative flow diagram from issue status-transition history.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--input` | path | (required unless `--demo`) | JSON file with issue history |
| `--demo` | flag | off | Use built-in sample data instead of `--input` |
| `--format` | string | `markdown` | One of `json`, `markdown`, `mermaid`, `confluence`, `notion`, `linear` |
| `--output` | path | stdout | Output file path |
| `--ready-state` | string (repeatable) | `Ready`, `To Do` | Status name(s) representing committed-not-started |
| `--in-progress-state` | string (repeatable) | `In Progress`, `In Review` | Status name(s) representing active work |
| `--done-state` | string (repeatable) | `Done`, `Closed` | Status name(s) representing delivered |
| `--type` | string | (none) | Filter by issue type (e.g., `bug`, `feature`) |
| `--window-days` | int | 60 | Trailing window in days for throughput trend |
| `--ignore-missing` | flag | off | Skip issues that lack required fields |
| `--as-of` | ISO date | today | Compute metrics as of this date (for historical review) |

### Input JSON schema

```json
{
  "issues": [
    {
      "id": "ENG-101",
      "title": "Add CSV export",
      "type": "feature",
      "team": "platform",
      "created_at": "2026-04-01T10:00:00Z",
      "status_history": [
        {"status": "Backlog",     "entered_at": "2026-04-01T10:00:00Z"},
        {"status": "Ready",       "entered_at": "2026-04-15T09:00:00Z"},
        {"status": "In Progress", "entered_at": "2026-04-17T11:30:00Z"},
        {"status": "In Review",   "entered_at": "2026-04-22T16:00:00Z"},
        {"status": "Done",        "entered_at": "2026-04-24T10:00:00Z"}
      ]
    }
  ]
}
```

### Output JSON schema

Wrapped per `SHARED_OUTPUT_SCHEMA.md`:

```json
{
  "schema": "pm/cycle-time-analyzer/v1",
  "generated_at": "2026-05-21T00:00:00Z",
  "data": {
    "as_of": "2026-05-21",
    "summary": {
      "lead_time_p50_days": 9.5,
      "lead_time_p85_days": 22.1,
      "cycle_time_p50_days": 4.2,
      "cycle_time_p85_days": 11.0,
      "throughput_per_week": 6.4,
      "wip_count": 12
    },
    "aging_wip": [
      {"id": "ENG-117", "title": "...", "age_days": 14.2, "status": "In Progress"}
    ],
    "cumulative_flow": [
      {"date": "2026-04-01", "Backlog": 32, "Ready": 6, "In Progress": 4, "In Review": 1, "Done": 18}
    ]
  }
}
```

## References

- `references/flow-metrics-guide.md` -- Vacanti-style deep dive: lead vs cycle, distributions vs averages, Little's Law, aging WIP, common anti-patterns.
- Vacanti, Daniel S. *Actionable Agile Metrics for Predictability*. ActionableAgile Press, 2015.
- Vacanti, Daniel S. *When Will It Be Done?* ActionableAgile Press, 2020.
- Little, John D. C. "A Proof for the Queuing Formula: L = λW." Operations Research, 1961.
- Anderson, David J. *Kanban: Successful Evolutionary Change for Your Technology Business*. Blue Hole Press, 2010.
