# Active Consultation Simplification Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-05-01

## Goal

Finish the next terminology and runtime-surface cleanup slice by removing
active `specialist consultation` semantics from the current governed routing
model, while preserving the six Vibe stages and the existing selected-skill
usage evidence chain.

The active model remains:

```text
skill_candidates -> selected skill -> used / unused
```

This design does not change how packs select a skill. It changes what happens
after selection: new sessions should not present consultation, auxiliary
expert, primary/secondary, or stage-assistant concepts as another live layer.
The only current usage state is whether a selected skill was used or unused.

## Current Findings

The preceding cleanup slices already simplified the main route surface:

| Check | Current result |
| --- | --- |
| Active packs in `config/pack-manifest.json` | 41 |
| Old pack fields in active manifest | 0 packs with `route_authority_candidates`, `stage_assistant_candidates`, `route_authority_eligible`, or `legacy_role` |
| Focused routing and usage contract tests | `12 passed` |
| Pack routing smoke | `1014 passed`, `0 failed` |
| Offline skills gate | `present_skills=259`, `lock_skills=259`, pass |
| Config parity gate | `45 / 45` matched, pass |
| Version packaging gate | pass |

The remaining active complexity is not in `pack-manifest.json`. It is in the
runtime consultation path:

- `config/specialist-consultation-policy.json` is still enabled.
- The policy still uses `max_consults_per_window`, `bucket_limits.primary`,
  and `bucket_limits.stage_assistant`.
- Runtime files still create and project consultation receipts such as
  `discussion_specialist_consultation` and `planning_specialist_consultation`.
- Tests still assert `approved_consultation`, `consulted_units`, and
  `discussion_consultation` / `planning_consultation` surfaces.

This makes the project harder to understand because the active route surface
now says "selected skill plus used/unused", while the runtime still exposes a
separate consultation chain.

There is also one unrelated release metadata drift:

```text
vibe-version-consistency-gate.ps1: 9 passed, 1 failed
failure: SKILL.md Updated marker does not match config/version-governance.json
```

That drift is not a routing regression, but it should be fixed in the final
cleanup pass or a small release-metadata pass.

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

2. Keep pack route behavior intact.
3. Keep `skill_routing.selected` as the selected-skill record.
4. Keep `skill_usage.used` and `skill_usage.unused` as the only current proof
   of material skill use.
5. Do not claim a selected skill was used unless `skill_usage.used` records
   evidence.
6. Keep old artifact readability through a compatibility path until a later
   deletion slice explicitly retires it.
7. Do not introduce replacement terms for consultation, auxiliary expert,
   primary skill, secondary skill, stage assistant, or route owner.

## Approved Direction

Use a compatibility-first cleanup:

1. Stop treating consultation as an active current-session layer.
2. Keep old consultation readers only for historical artifacts.
3. Move new user-facing and runtime summaries to:

```text
skill_routing.selected
skill_usage.used
skill_usage.unused
```

4. Update tests so they prove selected-skill use still works without relying
   on consultation fields.
5. Leave physical skill deletion and pack pruning out of this slice.

This is safer than deleting all consultation code in one pass because the
current runtime, requirement document writer, XL plan writer, and tests still
reference consultation receipts.

## Target Behavior

### New Runtime Sessions

New runtime packets and stage outputs should describe skill selection and usage
with current fields only:

```text
skill_routing.selected
skill_usage.loaded_skills
skill_usage.used
skill_usage.unused
skill_usage.evidence
```

New runtime packets should not create new active consultation artifacts such as:

```text
discussion_specialist_consultation
planning_specialist_consultation
approved_consultation
consulted_units
discussion_consultation
planning_consultation
```

If a selected skill is loaded but has not shaped an artifact yet, it remains in
`skill_usage.unused` with a reason. If it shapes requirement, plan, execution,
or cleanup artifacts, it is promoted into `skill_usage.used`.

### Old Runtime Artifacts

Old artifacts may still contain consultation fields. Compatibility readers may
interpret those fields only as legacy input.

Allowed compatibility behavior:

| Old artifact surface | Allowed handling |
| --- | --- |
| `discussion_specialist_consultation` | Read only when an old packet already has it. |
| `planning_specialist_consultation` | Read only when an old packet already has it. |
| `approved_consultation` | Map to historical disclosure only, not proof of use. |
| `consulted_units` | Map to historical disclosure only, not proof of use. |
| `discussion_consultation` / `planning_consultation` lifecycle segments | Preserve old report readability only. |

Current code must prefer `skill_routing` and `skill_usage` whenever both old and
current fields are present.

### User-Facing Text

New user-facing text should say:

```text
selected skill
used skill
unused skill
skill usage evidence
```

New user-facing text should not present these as current concepts:

```text
consultation
consulted units
auxiliary expert
primary skill
secondary skill
stage assistant
route owner
```

Historical notes may mention those names only in a clearly marked legacy or
compatibility context.

## Affected Areas

Expected implementation files:

- `config/specialist-consultation-policy.json`
- `scripts/runtime/VibeConsultation.Common.ps1`
- `scripts/runtime/VibeRuntime.Common.ps1`
- `scripts/runtime/Write-RequirementDoc.ps1`
- `scripts/runtime/Write-XlPlan.ps1`
- `scripts/runtime/invoke-vibe-runtime.ps1`
- `scripts/runtime/Invoke-PlanExecute.ps1`
- `tests/runtime_neutral/test_vibe_specialist_consultation.py`
- `tests/runtime_neutral/test_simplified_skill_routing_contract.py`
- `tests/runtime_neutral/test_binary_skill_usage_contract.py`

Potentially affected docs:

- `docs/governance/terminology-governance.md`
- active README glossary sections if they still describe consultation as a
  current behavior
- active runtime architecture docs if they still list consultation as a normal
  stage-like flow

This slice should not edit historical plans and archives unless they are linked
as current guidance.

## Implementation Slices

### Slice 1: Freeze The New Contract

Add tests that define the new intended current-session behavior:

- New runtime summaries do not require consultation receipts.
- New runtime packet interpretation uses `skill_routing.selected`.
- Material use is still proven only through `skill_usage.used`.
- Selected-but-not-materially-used skills remain in `skill_usage.unused`.
- Six-stage runtime tests still pass.

These tests should fail before implementation if active consultation is still
required for normal runtime closure.

### Slice 2: Disable Active Consultation Generation

Change the active policy and runtime entry points so new sessions do not create
discussion/planning consultation receipts by default.

Expected direction:

- Treat `specialist-consultation-policy.json` as legacy compatibility policy or
  mark it disabled for active sessions.
- Skip consultation receipt creation in new runtime paths.
- Remove consultation receipt requirements from requirement-doc and plan writers.
- Keep old-reader functions available for old packet interpretation.

This slice must not remove `skill_usage` promotion behavior.

### Slice 3: Rewrite Current Output Text

Update current generated requirement, plan, summary, and lifecycle text so it
does not use consultation vocabulary as active behavior.

The replacement is direct:

```text
selected skill -> used / unused
```

Do not introduce a new middle state.

### Slice 4: Compatibility Isolation

Move remaining consultation parsing behind clearly named compatibility helpers
or legacy-only paths.

The goal is not a repo-wide word-count cleanup. The goal is that a reader can
tell which code is current and which code only reads old artifacts.

### Slice 5: Metadata And Gate Cleanup

Fix the release marker drift found during assessment:

```text
SKILL.md Updated: 2026-04-26
config/version-governance.json release.updated: 2026-04-25
```

Then rerun version consistency. This is a small metadata correction, not a
routing behavior change.

## Non-Goals

This slice must not:

- Rename or remove any of the six governed stages.
- Delete more skill directories.
- Continue pack quality pruning.
- Change pack selection thresholds unless a regression test proves it is needed.
- Add new terms that replace consultation with another middle layer.
- Remove historical artifact readability in the same pass.
- Rewrite all old plans, archived reports, or old governance notes.

## Testing Strategy

Minimum focused tests:

```powershell
python -m pytest tests/unit/test_runtime_stage_machine.py tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_runtime_route_output_shape.py -q
```

Consultation-specific tests should be changed from "active consultation is
required" to "old consultation artifacts remain readable when present." The
replacement test shape should prove:

- New runtime flow can close without active consultation receipts.
- Old consultation receipts can still be interpreted as historical disclosure.
- Neither route selection nor historical consultation proves material use.
- `skill_usage.used` remains the only positive use claim.

Recurring gates:

```powershell
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1
.\scripts\verify\vibe-version-packaging-gate.ps1
.\scripts\verify\vibe-version-consistency-gate.ps1
git diff --check
```

The version consistency gate is expected to fail before Slice 5 because of the
known metadata drift. It must pass before final completion is claimed.

## Success Criteria

The cleanup is complete only when:

1. New runtime sessions do not emit active consultation artifacts by default.
2. New user-facing runtime text uses selected skill, used skill, unused skill,
   and skill usage evidence.
3. `skill_routing.selected` still records selected skills.
4. `skill_usage.used` and `skill_usage.unused` still record the final usage
   state.
5. Old consultation artifacts remain readable through compatibility code.
6. No selected-only, routed-only, dispatch-only, or consultation-only record is
   treated as proof of skill use.
7. Pack routing smoke remains green.
8. Offline skills gate remains green.
9. Config parity remains green.
10. Version consistency is green after the metadata drift is fixed.
11. Six-stage runtime behavior remains intact.

## Risks And Controls

| Risk | Control |
| --- | --- |
| Runtime writers still expect consultation paths | Add tests that close requirement and plan artifacts without consultation receipts. |
| Old artifacts become unreadable | Keep compatibility-reader tests with old packet fixtures. |
| Skill usage evidence weakens | Keep binary usage tests and require `skill_usage.used` for use claims. |
| A new middle-layer term replaces consultation | Add terminology assertions for active docs and current output text. |
| Metadata fix gets mixed with behavior changes | Keep the release-marker correction small and verify it separately. |

## Review Boundary

After this design is approved, the next step is a written implementation plan.
The implementation plan should be narrow: tests first, runtime output second,
compatibility isolation third, gates last.

No runtime code should be changed until the implementation plan is approved.
