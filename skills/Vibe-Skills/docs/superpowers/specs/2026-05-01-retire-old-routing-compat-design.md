# Retire Old Routing Compatibility Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-05-01

## Goal

Retire old routing-format adaptation while preserving current Vibe behavior.

The current model remains:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused
```

The project no longer promises compatibility for old routing packet formats,
old consultation receipts, or old specialist recommendation / dispatch /
stage-assistant hint fields. "No feature regression" means current-format
runtime behavior stays intact:

- Current six-stage governed runtime still launches and closes.
- Current pack routing still produces `skill_candidates`.
- Current selection still lives in `skill_routing.selected`.
- Current material-use proof still lives in `skill_usage.used`,
  `skill_usage.unused`, and `skill_usage.evidence`.
- Current generated requirement docs, XL plans, host briefings, execution
  manifests, and cleanup reports still work.
- Current pack routing, config parity, offline skills, and version gates still
  pass.

Old artifact readability is no longer a compatibility target.

## Current Findings

The current checkout has already cleaned the active routing surface:

```text
pack_count = 41
skill_candidates_total = 123
route_authority_candidates fields in active pack manifest = 0
stage_assistant_candidates fields in active pack manifest = 0
current_surface_violation_count = 0
```

The remaining complexity is old-format adaptation and historical vocabulary:

- `legacy_skill_routing` is still emitted in runtime packets.
- Runtime helpers still fall back from current routing to old
  `specialist_recommendations`, `specialist_dispatch`, and
  `stage_assistant_hints` fields.
- `VibeSkillRouting.Common.ps1` can still infer selected skills from old
  top-level `specialist_dispatch`.
- `Write-RequirementDoc.ps1` and `Write-XlPlan.ps1` still contain optional
  `## Specialist Consultation` branches.
- Several tests still assert old compatibility fields or old consultation
  receipt behavior.
- Historical governance docs still mention older terms. Those docs should not
  define current behavior.

This is not an active pack-routing failure. It is remaining old-format
compatibility debt.

## Required Behavior After This Cleanup

### Current Runtime Input

Current runtime input may use only current routing and usage fields for current
skill behavior:

```text
skill_candidates
skill_routing
skill_routing.selected
skill_usage
skill_usage.used
skill_usage.unused
skill_usage.evidence
```

Current runtime input must not use these old fields to infer current selected
skills, current usage, or current execution ownership:

```text
legacy_skill_routing
specialist_recommendations
specialist_dispatch
stage_assistant_hints
discussion_specialist_consultation
planning_specialist_consultation
approved_consultation
consulted_units
discussion_consultation
planning_consultation
```

If an old field appears in an input packet, current code should ignore it for
current routing decisions. It does not need to preserve old behavior, migrate
the packet, or render old consultation sections.

### Current Runtime Output

New runtime output should stop emitting old routing-compatibility boxes:

```text
legacy_skill_routing
specialist_recommendations
stage_assistant_hints
discussion_specialist_consultation
planning_specialist_consultation
```

The output may still include current execution artifacts that are part of the
current six-stage runtime. If a current execution artifact still has an
internal name such as `specialist_dispatch`, it must be derived from
`skill_routing.selected`, not from old compatibility input. Renaming current
execution internals is a separate, riskier cleanup and is not required for this
old-format retirement slice.

### Generated Documents

Current generated requirement docs, XL plans, lifecycle disclosures, and host
briefings must teach only:

```text
selected
used
unused
skill_usage evidence
```

They should not generate `## Specialist Consultation` sections in default
current runs or because an old-format input field exists. If such text remains
in historical docs, it must be outside current runtime output.

### Tests

Tests should stop requiring old-format compatibility. Tests that currently
assert old fields should be rewritten into one of these shapes:

1. Current-format behavior tests.
2. Retirement tests proving old fields are ignored by current routing.
3. Historical tests that inspect archived docs only and do not claim runtime
   support.

Tests should not assert that old consultation receipts stay readable. The user
has explicitly chosen not to maintain old format adaptation.

## Non-Goals

This cleanup does not:

- Change the six governed stages.
- Delete or prune skill directories.
- Change pack routing ownership or trigger keywords unless a failing current
  test proves it is necessary.
- Rename every internal variable or test fixture containing
  `specialist_dispatch`. Some of those names describe the current execution
  lane implementation. Removing old-format adaptation comes first.
- Preserve old session or old artifact readability.
- Preserve old `legacy_skill_routing` packet output.
- Preserve old consultation receipt rendering.

## Architecture

The architecture after this cleanup has one current routing path:

```text
pack routing
  -> skill_candidates
  -> skill_routing.selected
  -> current stage artifacts
  -> skill_usage.used / skill_usage.unused
  -> completion evidence
```

Old routing-format adaptation is removed from the current path:

```text
old specialist_recommendations
old specialist_dispatch
old stage_assistant_hints
old consultation receipts
  -> ignored for current routing
```

This avoids creating another transitional model. The project should not replace
old `route_authority` / `stage assistant` / `consultation` with another middle
state. The only current states remain:

```text
candidate
selected
used
unused
```

## Implementation Scope

### Runtime Routing Helpers

Update routing helpers so current selection reads only `skill_routing.selected`.

Expected changes:

- Remove fallback from `Get-VibeSkillRoutingSelected` to old
  `specialist_dispatch`.
- Stop exposing old `specialist_recommendations`,
  `specialist_dispatch`, and `stage_assistant_hints` as current routing input.
- Remove or retire helpers whose only purpose is old-format fallback.
- Keep current execution helpers that operate on current selected-skill data.

### Runtime Packet Shape

Update runtime packet creation so new packets no longer emit
`legacy_skill_routing` for compatibility. Current packet shape should focus on:

```text
skill_routing
skill_usage
host_specialist_dispatch_decision
specialist_decision
```

If a field remains because a current execution layer still needs it, tests must
prove it is derived from `skill_routing.selected` and is not an old-format
fallback.

### Requirement Doc And XL Plan

Remove default old consultation branches from current generated docs.

Expected changes:

- `Write-RequirementDoc.ps1` no longer writes `## Specialist Consultation`.
- `Write-XlPlan.ps1` no longer writes `## Specialist Consultation`.
- Current selected-skill and binary usage sections stay intact.
- Generated docs continue to mention `skill_usage.used`,
  `skill_usage.unused`, and evidence.

### Consultation Runtime

Retire consultation runtime as old-format support.

Safe options for implementation:

- Delete `scripts/runtime/VibeConsultation.Common.ps1` if no current tests or
  current runtime scripts depend on it after cleanup.
- Or keep a small retired stub that fails closed with a clear message if direct
  deletion would cause broader churn in the same slice.

The preferred end state is no current runtime dependency on consultation
receipt parsing or consultation receipt rendering.

### Governance Docs

Update `docs/governance/current-routing-contract.md` so old fields are described
as retired old-format fields, not compatibility fields. Historical governance
docs may remain, but a current index or current contract must make clear that
older docs are historical.

### Verification Gate

Add or extend a gate that reports:

```text
current_runtime_old_format_fallback_count
current_surface_violation_count
retired_old_format_reference_count
historical_reference_count
```

The gate should fail when current runtime code reads old routing fields for
current routing or emits old compatibility packet fields. It may allow old
terms in clearly historical docs and in tests that prove old fields are ignored.

## Risk Controls

### Current Capability Must Stay Green

These surfaces must continue passing:

- Current route selection.
- Current skill usage proof.
- Current requirement doc generation.
- Current XL plan generation.
- Current plan execution.
- Current phase cleanup.
- Pack routing smoke.
- Offline skills gate.
- Config parity gate.
- Version packaging and version consistency gates.

### Old Format Is Not A Required Capability

The following failures are acceptable after this cleanup when they come from
old-format input:

- Old packet does not populate selected skills.
- Old consultation receipt does not render into requirement docs or XL plans.
- Old `legacy_skill_routing` is absent from new runtime packets.
- Old `stage_assistant_hints` are ignored.

Those are intentional retirements, not regressions.

### Current Execution Naming Risk

Some current execution tests and runtime files still use names such as
`specialist_dispatch` for execution lanes. Removing old-format adaptation
should not force a wholesale rename of the execution layer in this slice.

The implementation should distinguish:

- Old format fields that are no longer supported as input/output
  compatibility.
- Current execution internals that are derived from `skill_routing.selected`.

If a current execution internal name causes user-facing confusion, it should be
handled in a later rename slice with its own tests.

## Required Tests

Add or update tests for these behaviors:

1. Current selection ignores old top-level `specialist_dispatch`.
2. Current selection ignores `legacy_skill_routing.specialist_dispatch`.
3. Current selection ignores old `specialist_recommendations`.
4. Current selection ignores old `stage_assistant_hints`.
5. New runtime packets do not emit `legacy_skill_routing`.
6. New runtime generated docs do not emit `## Specialist Consultation`.
7. `skill_usage.used` and `skill_usage.unused` still prove material use.
8. Current route output shape remains stable or simpler.
9. The old-format retirement scan fails on synthetic current-runtime fallback
   text and passes on the live repository.

Existing legacy-compatibility tests should be rewritten or deleted when their
only value is proving old artifact readability.

## Verification Plan

Focused verification:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_runtime_route_output_shape.py -q
```

Runtime and execution regression:

```powershell
python -m pytest tests/unit/test_runtime_stage_machine.py tests/runtime_neutral/test_active_consultation_simplification.py tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_plan_execute_receipts.py tests/runtime_neutral/test_l_xl_native_execution_topology.py -q
```

Broad gates:

```powershell
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1
.\scripts\verify\vibe-version-packaging-gate.ps1
.\scripts\verify\vibe-version-consistency-gate.ps1
.\scripts\verify\vibe-current-routing-contract-scan.ps1
```

Whitespace and final state:

```powershell
git diff --check
git status --short --branch
```

## Acceptance Criteria

The cleanup is complete only when all of these are true:

- Current runtime routing is still
  `skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused`.
- No active pack config contains old routing role fields.
- New runtime packets no longer emit `legacy_skill_routing`.
- Current selection does not fall back to old specialist fields.
- Current generated docs do not include `## Specialist Consultation`.
- Old consultation receipt readability is no longer tested as required
  functionality.
- Six governed stages are unchanged.
- Focused tests and broad gates pass.
- The final report explicitly says old format adaptation is retired and old
  artifact readability is not maintained.
