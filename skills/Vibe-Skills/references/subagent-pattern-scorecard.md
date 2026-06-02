# Subagent Handoff Scorecard

The handoff scorecard focuses on traceability and overlap risk.

| Dimension | Healthy signal |
|---|---|
| `scope_clarity` | bounded write scope and done definition are explicit |
| `ownership_boundary` | downstream role does not assume orchestration authority |
| `evidence_portability` | evidence refs and replay handles survive the handoff |
| `rollback_owner` | rollback owner is named and contactable |
| `overlap_risk` | duplicated responsibility is called out before execution |

High score does not grant authority; it only reduces handoff ambiguity.
