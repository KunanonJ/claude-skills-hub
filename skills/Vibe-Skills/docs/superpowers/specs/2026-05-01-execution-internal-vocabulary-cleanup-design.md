# Execution Internal Vocabulary Cleanup Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-05-01

## Goal

Clean up the remaining execution-internal `specialist_dispatch` vocabulary while
preserving the current routing model, six governed stages, and existing runtime
behavior.

The current public model remains:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused
```

The six governed stages remain:

```text
skeleton_check
deep_interview
requirement_doc
xl_plan
plan_execute
phase_cleanup
```

This cleanup is scoped to execution artifacts, execution accounting tests, and
scan gates. It does not change pack routing, skill selection, skill deletion, or
the governed stage sequence.

## Current Problem

The hard cleanup gate now proves that current docs and current behavior tests no
longer depend on retired root routing fields:

```text
Current docs retired-term violations: 0
Current behavior test retired-field reads: 0
Historical docs without retired marker: 0
```

However, the scan still reports execution-internal allowlisted references:

```text
Execution-internal specialist_dispatch allowlist references: 29
```

Those references are currently acceptable because they are execution internals
derived from `skill_routing.selected`, not root packet routing authority.
Keeping them indefinitely still creates developer confusion because public
runtime vocabulary now says `skill_routing`, `skill_usage`, and
`skill_execution`, while execution internals still use `specialist_dispatch`
names.

## Non-Goals

- Do not change the six governed stages.
- Do not change the public routing model.
- Do not delete skills or skill packs.
- Do not rewrite pack routing rules.
- Do not restore old root packet fields such as `specialist_dispatch`,
  `specialist_recommendations`, `legacy_skill_routing`, or
  `stage_assistant_hints`.
- Do not maintain old-format routing compatibility inputs.
- Do not globally search-replace `specialist_dispatch` without preserving
  behavior through tests.

## Preferred Vocabulary

Execution-internal fields should move toward the execution layer vocabulary
already defined in `docs/governance/current-runtime-field-contract.md`:

```text
approved_skill_execution
skill_execution_units
selected_skill_execution
execution_skill_outcomes
```

The implementation should prefer these field replacements:

| Current internal field | Preferred current field |
| --- | --- |
| `specialist_dispatch_unit_count` | `skill_execution_unit_count` |
| `specialist_dispatch_outcome_count` | `execution_skill_outcome_count` |
| `specialist_dispatch_outcomes` | `execution_skill_outcomes` |
| `specialist_dispatch_resolution_path` | `skill_execution_resolution_path` |
| `approved_dispatch` | `selected_skill_execution` |
| `approved_dispatch_count` | `selected_skill_execution_count` |
| `blocked_specialist_units` | `blocked_skill_execution_units` |
| `blocked_specialist_unit_count` | `blocked_skill_execution_unit_count` |
| `degraded_specialist_units` | `degraded_skill_execution_units` |
| `degraded_specialist_unit_count` | `degraded_skill_execution_unit_count` |

The cleanup should avoid introducing new conceptual names. The replacement
terms are direct execution-layer names for fields that already exist.

## Design

### Phase 1: Inventory And Guard

Use the existing hard cleanup scan as the inventory source. Add explicit summary
expectations for execution-internal references so the current count is visible
and future work can drive it down intentionally.

The expected starting point is:

```text
execution_internal_specialist_dispatch_reference_count = 29
```

The target is:

```text
execution_internal_specialist_dispatch_reference_count = 0
```

If a full zero target exposes a real compatibility risk, the implementation may
keep a very small allowlist only when the entry has a precise reason and a
follow-up path. Generic historical residue is not acceptable.

### Phase 2: Add Current Execution Fields First

Before removing old execution-internal fields, ensure every execution artifact
that currently reports specialist dispatch accounting also reports current
execution vocabulary.

The critical artifacts are:

- `execution-manifest.json`
- governed execution proof manifest
- plan execute receipt
- execution topology/accounting projections consumed by tests

Current aliases already exist for:

```text
skill_execution_unit_count
execution_skill_outcome_count
execution_skill_outcomes
```

This phase should fill any remaining gaps, including selected, blocked, degraded,
and resolution fields.

### Phase 3: Move Current Tests To Current Fields

Current behavior tests should read the current execution fields, not the retired
execution-internal names.

Tests that prove old names are absent or retired may remain in retired-behavior
test files only. Current behavior tests should validate:

- selected skill execution count and units
- execution skill outcomes
- blocked skill execution units
- degraded skill execution units
- skill execution resolution path
- equality between current execution fields and existing behavior before old
  names are removed

### Phase 4: Stop Writing Old Execution Names In Current Outputs

After current tests are migrated, current runtime outputs should stop writing
old execution-internal names where downstream current behavior no longer needs
them.

This phase must preserve behavior:

- selected skills still execute or route directly according to current policy
- blocked skills remain blocked
- degraded skills remain degraded
- proof manifests still show execution evidence
- plan execute receipts still point to the same artifacts

### Phase 5: Tighten Gates

Update `vibe-routing-terminology-hard-cleanup-scan.ps1` and
`vibe-current-routing-contract-scan.ps1` so execution-internal
`specialist_dispatch` references are no longer accepted by default.

The preferred final state is:

```text
Execution-internal specialist_dispatch allowlist references: 0
Gate Result: PASS
```

If any allowlist remains, the scan output must name it explicitly and the final
report must explain why it is still required.

## Data Flow

The runtime data flow after cleanup should be:

```text
skill_routing.selected
  -> selected_skill_execution
  -> skill_execution_units
  -> execution_skill_outcomes
  -> skill_usage.used / skill_usage.unused with evidence
```

Blocked and degraded paths should flow through the same vocabulary:

```text
specialist_decision.blocked_skill_ids
  -> blocked_skill_execution_units
  -> execution_skill_outcomes
```

```text
specialist_decision.degraded_skill_ids
  -> degraded_skill_execution_units
  -> execution_skill_outcomes
```

Routing remains separate from use proof. Execution outcomes are still not usage
claims unless `skill_usage.used` and `skill_usage.evidence` support the claim.

## Error Handling

The cleanup must preserve existing safety behavior:

- If a selected skill is blocked by `specialist_decision.blocked_skill_ids`, it
  must not be executed as selected skill execution.
- If a selected skill is degraded, the degraded execution unit must explain the
  reason and preserve evidence.
- If a current execution field is missing, current behavior tests should fail.
- If an old execution-internal name appears in current outputs after removal,
  the hard cleanup scan should fail.

## Testing

Minimum focused tests:

```text
tests/runtime_neutral/test_routing_terminology_hard_cleanup.py
tests/runtime_neutral/test_current_routing_contract_scan.py
tests/runtime_neutral/test_l_xl_native_execution_topology.py
tests/runtime_neutral/test_plan_execute_receipts.py
tests/runtime_neutral/test_runtime_contract_schema.py
tests/runtime_neutral/test_runtime_delivery_acceptance.py
tests/runtime_neutral/test_skill_promotion_destructive_gate.py
```

Minimum gates:

```text
scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1
scripts/verify/vibe-current-routing-contract-scan.ps1
scripts/verify/vibe-pack-routing-smoke.ps1
scripts/verify/vibe-offline-skills-gate.ps1
scripts/verify/vibe-config-parity-gate.ps1
scripts/verify/vibe-version-packaging-gate.ps1
scripts/verify/vibe-version-consistency-gate.ps1
```

## Success Criteria

The work is complete when:

- Current routing model remains
  `skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused`.
- Six governed stages remain unchanged.
- Current root runtime packets still do not expose retired root routing fields.
- Current execution artifacts expose current execution vocabulary.
- Current behavior tests no longer read old execution-internal field names.
- Hard cleanup scan reports zero current docs retired terms.
- Hard cleanup scan reports zero current behavior test retired-field reads.
- Hard cleanup scan reports zero historical docs without retired markers.
- Hard cleanup scan reports zero execution-internal `specialist_dispatch`
  references, or a small explicit allowlist with named residual risk.
- Pack routing smoke and version/config gates continue to pass.

## Rollback Strategy

If a downstream current test fails because a consumer still depends on an old
execution-internal field, restore the old field only as a temporary alias beside
the current field, then add a test that proves the current field carries the
same value. Do not restore old root routing packet fields.

## Review Notes

This is a high-force cleanup of internal vocabulary, not a routing redesign.
The implementation should be incremental and evidence-driven because execution
artifacts are used by proof manifests, receipts, and tests.
