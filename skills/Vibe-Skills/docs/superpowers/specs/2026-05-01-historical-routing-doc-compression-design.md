# Historical Routing Document Compression Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

## Summary

Compress and quarantine historical routing terminology so current Vibe-Skills
readers see one simple model:

```text
skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage
```

This is a documentation and governance cleanup design. It must not change the
six-stage runtime, current routing fields, skill execution behavior, pack routing
selection, or delivery-acceptance semantics.

## Current State

The current active routing surface is already clean:

```text
current_surface_violation_count: 0
current_runtime_old_format_fallback_count: 0
hard_cleanup_current_doc_retired_term_violation_count: 0
hard_cleanup_current_behavior_test_retired_field_read_count: 0
hard_cleanup_current_policy_helper_dispatch_vocabulary_reference_count: 0
```

Remaining noise is historical:

```text
retired_old_format_reference_count: 33
historical_reference_count: 952
```

Those references are not current runtime regressions, but they make the project
harder to understand because old terms such as dispatch, consultation, primary
skill, stage assistant, and route owner still appear in older plans, specs, and
requirements.

## Goals

- Keep the current routing explanation small and stable.
- Reduce the number of old routing terms a maintainer sees while reading current
  docs.
- Keep necessary historical context available, but clearly retired.
- Preserve auditability: a reader should still be able to learn why the old
  model was removed.
- Add or tighten checks so historical wording cannot leak back into current
  docs, current runtime generators, or current gate messages.

## Non-Goals

- Do not rename deep runtime JSON containers such as `specialist_accounting` or
  `specialist_decision`.
- Do not remove historical records that are still useful as design rationale.
- Do not mechanically replace all old terms across the repository.
- Do not alter pack routing, skill selection, phase decomposition, or native
  skill execution.
- Do not change the public six-stage governed runtime.

## Document Classes

The cleanup should classify files into four groups.

### Current Surface

Examples:

```text
README.md
SKILL.md
protocols/runtime.md
protocols/team.md
docs/governance/current-routing-contract.md
docs/governance/current-runtime-field-contract.md
scripts/runtime/Write-RequirementDoc.ps1
scripts/runtime/Write-XlPlan.ps1
```

Rule: current surface files must use the current vocabulary only. Old terms may
appear only in explicitly named retired sections when the current scan allows
that context.

### Historical Rationale

Examples:

```text
docs/governance/*old-routing*
docs/governance/*terminology*
docs/superpowers/specs/*routing*
docs/superpowers/plans/*routing*
docs/requirements/*specialist*
```

Rule: files that still explain retired behavior must have a clear
`Historical / Retired Note` near the top and must point readers to the current
contract.

### Compressible History

Examples:

```text
older superpowers design drafts
superseded execution plans
duplicated retired terminology notes
```

Rule: if multiple documents repeat the same retired routing model, keep one
summary note and either move the rest behind a clearly marked archive surface or
delete only when their content is provably duplicated and unreferenced.

### Test Fixtures And Regression Evidence

Examples:

```text
tests/runtime_neutral/test_retired_old_routing_compat.py
tests/runtime_neutral/test_simplified_skill_routing_contract.py
tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py
```

Rule: tests may mention old terms only when they are explicitly asserting that
old fields are absent, retired, or not current. Current-behavior tests should not
read old-format routing fields.

## Proposed Approach

### Phase 1: Inventory

Generate a report of old routing terminology references grouped by:

- current surface
- historical rationale
- compressible history
- tests and fixtures
- runtime or verification scripts

The report should include path, line count, term family, and recommended action.
This phase should not edit files.

### Phase 2: Mark And Redirect

For historical rationale files that should remain, add a short note near the
top:

```text
Historical / Retired Note:
This document describes a retired routing design. The current routing model is
skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage.
```

The note should be short and consistent. It should not introduce new routing
concepts.

### Phase 3: Compress Duplicates

For repeated old-routing specs or plans, keep one concise historical summary and
remove or archive duplicated prose only when:

- the document is not referenced by current docs, scripts, or tests;
- the document does not contain unique implementation decisions;
- the removal is covered by a git diff and scan output.

Deletion must be conservative. A file with unique rationale should be retained
with a retired marker rather than deleted.

### Phase 4: Guard Current Vocabulary

Tighten `vibe-current-routing-contract-scan.ps1` and
`vibe-routing-terminology-hard-cleanup-scan.ps1` only where needed so they
distinguish:

- current-surface violations;
- marked historical references;
- unmarked historical references;
- test-only negative assertions.

The gate should not require `historical_reference_count` to be zero. The target
is that old terms either disappear from current surfaces or live in explicitly
marked historical locations.

## Data Flow

1. Scan repository text for retired routing terminology.
2. Classify each hit by path group and context.
3. Apply one of three actions:
   - keep current wording unchanged;
   - add retired marker and redirect to current contract;
   - compress/delete duplicated historical prose.
4. Re-run routing terminology gates.
5. Re-run smoke gates that prove current behavior did not regress.

## Error Handling

- If a file cannot be confidently classified, leave it unchanged and add it to a
  manual-review list.
- If a historical file is referenced by current docs, scripts, tests, or release
  notes, do not delete it in this phase.
- If a scan starts failing on current runtime files, stop and fix the current
  surface before touching more historical docs.
- If behavior gates fail after documentation cleanup, treat that as a regression
  and revert the risky doc or scan change rather than changing runtime behavior
  to satisfy the cleanup.

## Testing Plan

Focused checks:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-current-routing-contract-scan.ps1
python -m pytest tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py -q
```

Behavior checks:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-governed-runtime-contract-gate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-runtime-execution-proof-gate.ps1
git diff --check
```

Success criteria:

- current-surface violations remain zero;
- current runtime old-format fallbacks remain zero;
- unmarked historical references are zero;
- current vocabulary tests pass;
- pack routing smoke still passes;
- governed runtime and runtime execution proof gates still pass;
- no implementation or runtime contract field is renamed in this cleanup.

## Review Boundary

This design authorizes only documentation classification, historical marker
normalization, conservative duplicate compression, and scan tightening. It does
not authorize runtime field renames, pack deletion, skill deletion, or changes
to the six-stage governed runtime.
