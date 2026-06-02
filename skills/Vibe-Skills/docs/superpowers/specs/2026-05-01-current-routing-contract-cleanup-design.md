# Current Routing Contract Cleanup Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-05-01

## Goal

Continue the routing cleanup in a deeper but controlled pass. The current Vibe
routing model must stay simple, explicit, and verifiable:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused
```

This design cleans fields, runtime output, compatibility boundaries, tests, and
current documentation without reducing routing capability, skill usage evidence,
or the six governed stages.

The cleanup must make the current work model easy to explain:

- `candidate` means a skill was considered.
- `selected` means a skill was chosen into the work surface.
- `used` means a selected or loaded skill shaped an artifact and has evidence.
- `unused` means a selected or loaded skill did not shape an artifact.
- `evidence` means the specific artifact impact that supports a `used` claim.
- `legacy compatibility` means old artifacts remain readable but do not define
  the current routing model.

## Current Findings

The latest cleanup already removed active specialist consultation generation
from new runtime sessions and kept old consultation readers for compatibility.
The current verified state is:

- New runtime sessions no longer create default discussion/planning
  consultation artifacts.
- `config/specialist-consultation-policy.json` is disabled and marked
  `legacy_compatibility_only`.
- Active pack manifests no longer use historical role fields such as
  `route_authority_candidates`, `stage_assistant_candidates`,
  `route_authority_eligible`, or `legacy_role`.
- Focused runtime and routing tests pass.
- Pack routing smoke, offline skills gate, config parity, version packaging,
  version consistency, and whitespace checks pass.

Remaining complexity is concentrated in compatibility surfaces:

- `scripts/runtime/VibeConsultation.Common.ps1` still contains old consultation
  machinery.
- `scripts/runtime/VibeRuntime.Common.ps1` still has legacy readers and
  projection helpers.
- `Write-RequirementDoc.ps1`, `Write-XlPlan.ps1`, and
  `invoke-vibe-runtime.ps1` still carry optional consultation parameters and
  artifact slots for old receipts.
- Tests still include legacy consultation and stage-assistant coverage.
- Historical docs and older plans still describe previous routing designs.

These remnants are not all active runtime behavior, but they make the project
hard to understand. The next pass should reduce what current users and
developers see while keeping old artifacts readable until a later deletion
slice proves they can be removed.

## Non-Negotiable Principles

1. Keep the six governed stages unchanged:

```text
skeleton_check
deep_interview
requirement_doc
xl_plan
plan_execute
phase_cleanup
```

2. Keep pack routing capability intact.
3. Keep `skill_routing.selected` as the current selection record.
4. Keep `skill_usage.used` and `skill_usage.unused` as the only current
   material-use proof.
5. Never claim a skill was used unless `skill_usage.used` and
   `skill_usage.evidence` support it.
6. Do not introduce replacement middle states between `selected` and
   `used / unused`.
7. Do not treat legacy consultation, dispatch, or stage-assistant fields as
   current routing concepts.
8. Do not physically delete legacy runtime modules until compatibility tests
   and current-runtime tests prove the deletion is safe.
9. Keep every cleanup slice small enough to verify independently.

## Target Current Contract

### Current Fields

Current runtime and documentation should use these fields and terms:

```text
skill_candidates
skill_routing
skill_routing.selected
skill_usage
skill_usage.loaded_skills
skill_usage.used
skill_usage.unused
skill_usage.used_skills
skill_usage.unused_skills
skill_usage.evidence
```

The current model should read as:

```text
candidate -> selected -> used / unused
```

### Legacy Compatibility Fields

These fields may remain only behind explicit compatibility boundaries:

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

Allowed use:

- Read old artifacts.
- Preserve old compatibility tests.
- Compare old and current data during migration.
- Prove old fields do not count as material skill use.

Disallowed use:

- Present these fields as current runtime state.
- Use them as evidence that a skill was used.
- Teach users to reason about current routing through these fields.
- Generate new default consultation artifacts in current sessions.

### Current User-Facing Text

Current generated outputs should use:

```text
selected skill
used skill
unused skill
skill usage evidence
current routing contract
legacy compatibility
```

Current generated outputs should not present these as active concepts:

```text
consultation expert
auxiliary expert
primary skill
secondary skill
stage assistant
route owner
route authority
consulted units
approved consultation
```

Historical or compatibility text may mention those names only when the section
is clearly labeled as legacy compatibility or archived history.

## Architecture

The cleaned architecture has two explicit layers.

### Current Layer

The current layer is the only layer used to explain new runs:

```text
pack routing
  -> skill_candidates
  -> skill_routing.selected
  -> stage artifacts
  -> skill_usage.used / skill_usage.unused
  -> completion evidence
```

Files expected to stay in the current layer:

- `scripts/runtime/VibeSkillRouting.Common.ps1`
- `scripts/runtime/VibeSkillUsage.Common.ps1`
- `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- `scripts/runtime/Write-RequirementDoc.ps1`
- `scripts/runtime/Write-XlPlan.ps1`
- `scripts/runtime/Invoke-PlanExecute.ps1`
- `scripts/runtime/Invoke-PhaseCleanup.ps1`
- `scripts/runtime/invoke-vibe-runtime.ps1`

These files may still read legacy input temporarily, but their current output
should prefer `skill_routing` and `skill_usage`.

### Legacy Compatibility Layer

The legacy layer exists only to keep old data readable:

```text
old consultation receipts
old specialist recommendation records
old dispatch records
old stage-assistant hint records
  -> compatibility projection
  -> clearly labeled legacy output
```

Files expected to remain in this layer for now:

- `scripts/runtime/VibeConsultation.Common.ps1`
- legacy parts of `scripts/runtime/VibeRuntime.Common.ps1`
- legacy-only tests in `tests/runtime_neutral/test_vibe_specialist_consultation.py`

This layer must not be invoked by default to generate current-session routing
or usage artifacts.

## Data Flow

### New Runtime Session

For a new session, the intended data flow is:

```text
pack-manifest / keyword index / routing rules
  -> route snapshot
  -> skill_candidates
  -> skill_routing.selected
  -> initial skill_usage
  -> requirement_doc artifact impact
  -> xl_plan artifact impact
  -> plan_execute artifact impact
  -> phase_cleanup summary
```

Selection and use remain separate:

- `skill_routing.selected` records what should be brought into the work.
- `skill_usage.loaded_skills` records which selected skills were loaded.
- `skill_usage.used` records only skills with material artifact impact.
- `skill_usage.unused` records selected or loaded skills without material
  impact.
- `skill_usage.evidence` records the file, stage, and impact summary.

### Old Artifact Read

For an old artifact, the intended data flow is:

```text
old runtime artifact
  -> legacy reader
  -> legacy compatibility projection
  -> current output says usage still requires skill_usage
```

Old routing, consultation, or dispatch records may explain historical lineage.
They must not become current `used` evidence.

## Scope For The Next Implementation Plan

The next implementation plan should be staged.

### Slice 1: Current Surface Contract Tests

Add or tighten tests that prove current outputs are clean:

- Default runtime summary does not expose active consultation artifacts.
- Requirement docs and XL plans explain selected skills and usage evidence only.
- Current lifecycle text uses `skill_routing_usage_evidence` when no legacy
  receipt exists.
- Current outputs do not present stage-assistant, primary/secondary, or
  consultation wording as active behavior.
- Legacy text remains allowed only in legacy compatibility tests.

### Slice 2: Runtime Output Cleanup

Clean user-facing and summary output:

- Prefer `skill_routing.selected` in requirement and plan text.
- Prefer `skill_usage.used` / `skill_usage.unused` in completion and cleanup
  summaries.
- Keep consultation paths nullable and absent from current summary unless an
  old receipt is explicitly loaded.
- Remove or rewrite active wording around consultation, dispatch, and
  stage-assistant concepts.

### Slice 3: Legacy Boundary Isolation

Make the boundary explicit:

- Rename comments and tests so legacy consultation coverage is visibly legacy.
- Centralize old-field reads behind compatibility helpers where practical.
- Ensure `VibeConsultation.Common.ps1` is not described as a current route
  module.
- Keep old receipt readability tests.

### Slice 4: Documentation Cleanup

Create a current governance document:

```text
docs/governance/current-routing-contract.md
```

It should define only:

```text
candidate
selected
used
unused
evidence
legacy compatibility
```

Update current docs that still describe old routing mechanisms as active. Do
not rewrite historical plans/specs unless they are linked as current guidance.
Historical docs should be left alone or labeled as historical when necessary.

### Slice 5: Verification And Residual Debt Report

Run focused and broad verification:

```powershell
python -m pytest tests/unit/test_runtime_stage_machine.py tests/runtime_neutral/test_active_consultation_simplification.py tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_runtime_route_output_shape.py -q
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1
.\scripts\verify\vibe-version-packaging-gate.ps1
.\scripts\verify\vibe-version-consistency-gate.ps1
git diff --check
```

Also produce a residual-debt scan that separates:

- Current-surface violations that must be fixed.
- Legacy compatibility references that remain intentionally.
- Historical docs that are not current guidance.
- Candidate modules for a later physical deletion pass.

## Out Of Scope For This Slice

This design does not approve immediate deletion of:

- `scripts/runtime/VibeConsultation.Common.ps1`
- old consultation receipt readers
- old compatibility tests
- execution-layer dispatch internals
- host install/runtime package compatibility paths

This design also does not approve broad physical deletion of skill directories.
Skill directory deletion remains a separate pack-by-pack cleanup with its own
problem map and verification.

## Error Handling

The cleanup should fail closed:

- If a current runtime output still needs an old field to close, the test should
  fail and the implementation should fix the current path rather than re-enable
  the old model.
- If a legacy artifact cannot be read, the compatibility test should fail and
  the old reader should be repaired or explicitly retired in a separate plan.
- If a field appears in both current and legacy forms, current code should
  prefer `skill_routing` and `skill_usage`.
- If a selected skill lacks artifact impact, output must keep it in `unused`
  rather than promoting it to `used`.

## Testing Strategy

Tests should protect behavior at four levels:

1. Current contract tests:
   - Current outputs use `skill_routing.selected`.
   - Usage claims require `skill_usage.used` and evidence.
   - Default current sessions do not create active consultation receipts.

2. Legacy compatibility tests:
   - Old consultation receipts remain readable.
   - Old consultation or dispatch fields do not prove `used`.
   - Legacy tests are named or grouped so they do not look like current route
     behavior.

3. Routing regression tests:
   - Pack routing smoke stays green.
   - High-value route examples still select the same current skills.
   - Scientific visualization and LaTeX routes remain protected by their
     existing route tests.

4. Governance gates:
   - Offline skills gate passes.
   - Config parity passes.
   - Version packaging and consistency pass.
   - `git diff --check` is clean.

## Success Criteria

The cleanup is successful when:

- New runtime sessions can be explained with only
  `skill_candidates -> skill_routing.selected -> skill_usage.used / unused`.
- Current user-facing docs and generated outputs no longer teach old
  consultation or stage-assistant concepts as active routing behavior.
- Legacy compatibility remains readable and clearly labeled.
- Six-stage governed execution still works.
- Pack routing smoke reports zero failures.
- Skill usage proof still requires `skill_usage` evidence.
- The final report distinguishes current cleanup from legacy compatibility and
  does not claim all historical strings were deleted.

## Future Deletion Pass

After this cleanup lands and remains stable, a later deletion pass can evaluate
whether to physically remove legacy consultation code. That later pass should
only start after:

- Current outputs no longer depend on old consultation modules.
- Old artifact compatibility requirements are explicitly accepted or retired.
- Tests prove the runtime can close without loading consultation code.
- Host install/package compatibility has been checked.

The later deletion pass should be a separate design and plan, not an implicit
side effect of this cleanup.
