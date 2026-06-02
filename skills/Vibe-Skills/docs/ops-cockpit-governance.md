# Ops Cockpit Governance

## Purpose

Wave124 upgrades the ops cockpit from a passive summary into **actionable panels**. The cockpit remains a governance surface, not a second orchestrator.

## Required writing rule

Every panel must produce: **结论 + blocker + evidence pointer**.

That rule applies to both `ops-dashboard.json` and the human-readable dashboard markdown.

## Required Panels

| Panel | What it must show |
| --- | --- |
| `freshness` | runtime freshness, packaging drift, missing evidence |
| `promotion` | promotion-board posture, scorecard gaps, next stage |
| `replay` | replay coverage, missing checkpoints, evidence quality |
| `rollback` | rollback drill readiness, unresolved rollback blockers |
| `release` | release train readiness, stop-ship gaps, operator handoff |

## Governance Rules

1. actionable panels read governed evidence only.
2. Each panel must declare blockers, evidence pointers, and next action.
3. `outputs/dashboard/ops-dashboard.json` is the machine-readable cockpit artifact.
4. The gap matrix is maintained in `references/ops-cockpit-gap-matrix.md`.
5. The cockpit never invents promotion or release state.

## Inputs

- `config/promotion-board.json`
- `config/ops-cockpit-panel-contract.json`
- `references/ops-cockpit-gap-matrix.md`
- governed verify artifacts under `outputs/verify`
