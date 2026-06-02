# Rollout Proposal Contract

Every bounded suggestion row must include the fields below.

| Field | Why it matters |
|---|---|
| `knob` | identifies the threshold under review |
| `current` | records the current governed value |
| `proposed` | records the reviewed proposal |
| `delta` | proves the proposal stays within bounded adjustments |
| `rationale` | keeps the proposal auditable and human-readable |
| `apply_policy` | preserves manual review required posture |

The contract is incomplete if the suggestion bundle is missing.
