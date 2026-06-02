# Connector Simulation Scenarios

The scenarios below are enough to prove sandbox discipline without widening authority.

| Scenario | Risk class | Required evidence |
|---|---|---|
| `read_only_catalog_lookup` | low | provider slug, evidence refs, no install side effects |
| `draft_write_preview` | medium | confirm mode, preview artifact, rollback plan |
| `confirm_write_simulation` | high | explicit operator ack, replay handle, action ledger row |
| `rollback_drill_simulation` | high | revert path, owner, post-drill verification |

All scenarios remain subordinate to connector admission governance.
