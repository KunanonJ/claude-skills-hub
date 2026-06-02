# Rollout Proposal Boundedness Governance

## Purpose

Wave98 turns adaptive suggestions into bounded rollout proposals that stay manually reviewed and quantitatively capped. The proposals must remain within explicit bounded adjustments.
The proposal layer constrains telemetry-driven suggestions so they can inform operators without silently mutating router thresholds.

## Governance Scope

- Rollout proposals must use the same bounded-adjustment maxima defined by `config/observability-policy.json`.
- Every proposal must state current value, proposed value, delta, rationale, and apply policy.
- The bounded proposal file is generated evidence and must remain subordinate to manual apply policy.

## Required Invariants

- `apply_policy = manual_review_required` remains fixed.
- `confirm_required_max_delta`, `min_top_gap_max_delta`, and `fallback_threshold_max_delta` cap each proposal.
- A missing suggestion bundle is a governance gap, not an implicit pass.
- No proposal may widen beyond the configured maxima or auto-apply itself.

## Non-Goals

- No direct edit of `router-thresholds.json` is allowed here.
- No proposal may claim release readiness by itself.

Validation is performed by `scripts/verify/vibe-rollout-proposal-boundedness-gate.ps1`.
