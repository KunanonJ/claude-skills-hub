# Current Routing Debt Erasure Design

> Historical / Retired Note: This document intentionally discusses retired
> routing terminology as cleanup targets. The current routing model is
> `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`;
> old terms here are debt targets, not current runtime states.

Date: 2026-05-02

## Goal

Erase old routing and runtime terminology debt from the current Vibe-Skills
execution model while preserving the safety contracts that make `$vibe`
trustworthy.

The target is not a cosmetic rename. The current runtime must have one active,
explainable field model:

```text
skill_candidates
  -> skill_routing.selected
  -> selected_skill_execution
  -> skill_usage.used / skill_usage.unused / skill_usage.evidence
```

Old fields and old role words should be removed from current runtime output,
current documentation, current behavior tests, and user-facing explanations.
Where old artifact support is still needed, it must be isolated behind explicit
legacy or retired boundaries and guarded so it cannot flow back into current
behavior.

## Problem

The repository has already made several cleanup passes around routing
terminology and compatibility output. The remaining debt is now less about one
obvious broken field and more about mixed mental models:

- current runtime and router code still has historical terminology nearby;
- old fields can appear in compatibility readers, fixtures, tests, or docs;
- some execution vocabulary still makes `selected`, `executed`, and `used`
  harder to distinguish;
- historical specs can read like active design unless they are clearly marked;
- tests and gates need to prove old terms do not return to current outputs.

The user goal is a safe but aggressive cleanup:

- make old terminology clear;
- make active fields clear;
- delete what can be deleted;
- isolate what cannot yet be deleted;
- add gates so this debt cannot silently re-enter current runtime paths.

## Current Field Contract

These are the active current fields:

```text
skill_candidates
skill_routing
skill_routing.candidates
skill_routing.selected
skill_routing.rejected
selected_skill_execution
skill_execution_units
approved_skill_execution
execution_skill_outcomes
skill_usage
skill_usage.loaded_skills
skill_usage.used
skill_usage.unused
skill_usage.used_skills
skill_usage.unused_skills
skill_usage.evidence
```

Their meanings are fixed:

| Field / term | Meaning |
| --- | --- |
| `candidate` | The router considered the skill or pack. This is not selection and not use. |
| `selected` | The skill was chosen into the governed work surface. This is not material use. |
| `selected_skill_execution` | The current execution-facing record derived from selected skills. |
| `used` | The skill materially shaped an artifact and has evidence. |
| `unused` | The skill was loaded, considered, or selected, but did not materially shape an artifact. |
| `evidence` | The stage, artifact, and impact record that supports a material-use claim. |

New fields are allowed only if they map cleanly to:

```text
candidate -> selected -> execution -> used / unused / evidence
```

New fields must not introduce another role layer such as assistant, authority,
consultation, primary, or secondary.

## Retired Terms And Fields

These old fields and terms are retired from the current model:

```text
legacy_skill_routing
specialist_recommendations
stage_assistant_hints
specialist_dispatch as root routing packet field
discussion_specialist_consultation
planning_specialist_consultation
approved_consultation
consulted_units
discussion_consultation
planning_consultation
route owner
route authority
primary skill
secondary skill
consultation expert
auxiliary expert
stage assistant
```

High-risk retired fields are fields that can pollute JSON packets, router
output, runtime output, or test assertions:

```text
legacy_skill_routing
specialist_recommendations
stage_assistant_hints
specialist_dispatch
approved_consultation
consulted_units
```

Medium-risk retired terms mostly pollute documentation, explanations, and test
names:

```text
route authority
stage assistant
consultation expert
primary skill
secondary skill
```

## Non-Goals

This cleanup must not:

- change the six governed stages:

```text
skeleton_check
deep_interview
requirement_doc
xl_plan
plan_execute
phase_cleanup
```

- change canonical `$vibe` entry behavior;
- rebuild the pack-router scoring system;
- delete bundled skills or prune skill packs as part of this slice;
- redefine `selected` as `used`;
- treat old artifact compatibility as current behavior;
- remove explicitly marked legacy fixtures only to make global grep results look
  clean;
- break install, packaging, or runtime freshness contracts.

## Cleanup Rule

The cleanup rule is deliberately strong:

```text
Can delete: delete.
Cannot delete yet: move behind legacy or retired boundaries.
Cannot move yet: add a gate proving it cannot enter current output, current docs,
or current behavior tests.
```

This is not a preserve-everything compatibility pass. Compatibility is allowed
only where it is explicit, bounded, and prevented from driving current behavior.

## Architecture

### Current Runtime Layer

This is the only layer allowed to explain new `$vibe` runs.

Primary file scope:

```text
SKILL.md
config/runtime-contract.json
config/pack-manifest.json
scripts/router/resolve-pack-route.ps1
scripts/router/modules/41-candidate-selection.ps1
scripts/router/modules/46-confirm-ui.ps1
scripts/runtime/Freeze-RuntimeInputPacket.ps1
scripts/runtime/VibeSkillRouting.Common.ps1
scripts/runtime/VibeSkillUsage.Common.ps1
scripts/runtime/Write-RequirementDoc.ps1
scripts/runtime/Write-XlPlan.ps1
scripts/runtime/Invoke-PlanExecute.ps1
scripts/runtime/Invoke-PhaseCleanup.ps1
scripts/runtime/invoke-vibe-runtime.ps1
packages/runtime-core/src/vgo_runtime/*router*
```

This layer may output only the current model:

```text
skill_candidates
skill_routing.selected
selected_skill_execution
skill_usage.used
skill_usage.unused
skill_usage.evidence
```

If this layer must temporarily read retired fields, the read must satisfy all
of these constraints:

- the function, module, or call site is explicitly named legacy or retired;
- the old field is read only to support old artifacts or prove it is ignored;
- the old field is not written into new runtime packets;
- the old field does not create a new current intermediate state;
- the old field is never evidence of material skill use.

### Legacy / Retired Compatibility Layer

This layer exists only to keep historical evidence readable or to prove that old
fields no longer drive current behavior.

Allowed locations:

```text
scripts/router/legacy/**
scripts/runtime/legacy/**
packages/runtime-core/src/vgo_runtime/legacy_compat.py
tests/**/legacy*
tests/**/retired*
tests/**/fixtures/**
docs/**/historical*
docs/**/retired*
docs/superpowers/specs/* with Historical / Retired Note
outputs/** as generated historical artifacts only
```

If `scripts/runtime/legacy/**` or `legacy_compat.py` do not exist yet, the
implementation plan should first check whether the existing repo style prefers
reusing an existing compatibility module before creating new paths.

In this layer, retired fields may appear only to:

- parse old fixtures;
- parse old artifacts;
- explain old behavior;
- compare old and current data during migration;
- assert that old fields do not drive current behavior.

### Guard / Gate Layer

The guard layer prevents old terms from returning to current surfaces.

Add or strengthen a gate with this contract:

```text
scripts/verify/vibe-current-routing-debt-gate.ps1
outputs/verify/current-routing-debt-gate.json
```

The gate should perform these checks:

```text
current_runtime_forbidden_fields_scan
current_docs_retired_terms_scan
current_tests_old_contract_dependency_scan
legacy_allowed_hits_scan
selected_used_evidence_chain_scan
```

The gate must not be a global mechanical ban on every retired string. It should
use a forbidden list for current paths and an allowlist for clearly legacy,
retired, historical, fixture, and generated-output paths.

## Output Surfaces That Must Stay Clean

These artifacts are trust surfaces and must not expose retired fields as current
contract:

```text
runtime-input-packet.json
host-launch-receipt.json
governance-capsule.json
stage-lineage.json
requirement_doc
xl_plan
phase-execute.json
cleanup-receipt.json
router confirm-required output
completion / delivery acceptance reports
```

They may express only:

```text
candidate
selected
selected execution
used
unused
evidence
```

They must not express active current behavior through:

```text
stage assistant
consultation expert
route authority
specialist recommendations
legacy skill routing
```

## Audit Scope

The audit should prioritize current paths:

```text
SKILL.md
config/*.json
scripts/router/**
scripts/runtime/**
packages/runtime-core/**
tests/runtime_neutral/**
tests/integration/**
tests/unit/**
scripts/verify/**
docs/*.md
docs/design/**
docs/runtime*
docs/status/**
docs/install/**
docs/superpowers/specs/**
```

The audit should exclude or demote these paths:

```text
dist/**
vendor/**
third_party/**
outputs/**
.pytest_cache/**
__pycache__/**
.worktrees/**
bundled/skills/**
docs/superpowers/plans/**
```

`bundled/skills/**` is out of the main cleanup scope because bundled skills
contain independent skill content, templates, and third-party references that
would create misleading false positives.

`docs/superpowers/plans/**` should not be treated as the main cleanup target.
Historical plans may be marked or summarized, but current runtime debt should
be fixed in current runtime, router, documentation, tests, and gates first.

## Audit Categories

Each retired-term hit should be classified into one of four categories.

### P0: Current Output Pollution

A hit is P0 if any of these are true:

- new runtime packets write retired fields;
- current router output writes retired fields;
- requirement docs or XL plans present retired terms as current model;
- completion reports turn selected, routed, or loaded into used;
- current behavior tests assert retired fields as normal output.

Treatment:

- delete the output;
- replace it with current fields;
- add regression tests for absence;
- add gate coverage.

### P1: Current Code Dependency

A hit is P1 if any of these are true:

- current runtime path reads retired fields as fallback;
- current router path uses retired fields for selection or presentation;
- current tests construct retired fields without a legacy or retired marker;
- PowerShell and Python paths contain divergent retired-field compatibility
  logic.

Treatment:

- delete if possible;
- otherwise move into a legacy or retired adapter;
- ensure current paths call the adapter only at an explicit boundary;
- add tests proving retired fields do not affect current selection or usage
  evidence.

### P2: Current Documentation Pollution

A hit is P2 if any of these are true:

- current README, install docs, runtime docs, or status docs explain the active
  system with retired terms;
- old specs lack a Historical / Retired Note and read like current design;
- documentation mixes current and old fields without an explicit boundary.

Treatment:

- rewrite current docs to the current model;
- add Historical / Retired Note to old specs;
- compress repeated historical plans into an index or archive note when useful.

### P3: Allowed Historical Evidence

A hit is P3 if it appears only in:

- legacy fixtures;
- retired behavior tests;
- historical design notes;
- audit reports explaining prior state;
- generated old output artifacts.

Treatment:

- keep it;
- ensure the path, file name, or header clearly marks it as legacy, retired, or
  historical;
- add the location to the gate allowlist if needed.

## Audit Outputs

The audit should produce a human report and a machine-readable report:

```text
docs/audits/2026-05-02-current-routing-debt-audit.md
outputs/verify/current-routing-debt-audit.json
```

Each JSON record should use this shape:

```json
{
  "term": "legacy_skill_routing",
  "path": "scripts/runtime/Freeze-RuntimeInputPacket.ps1",
  "line": 123,
  "category": "P0",
  "current_layer": "current_runtime",
  "decision": "delete_output",
  "reason": "New runtime packets must not emit legacy routing fields.",
  "suggested_fix": "Remove writer and assert field absence in runtime packet tests."
}
```

The audit is successful when it can answer:

- which fields are active;
- which fields are retired;
- where retired fields still appear;
- which hits are P0, P1, P2, or P3;
- which hits can be deleted;
- which hits need legacy isolation;
- which hits need gate protection;
- which hits are historical evidence and should not be deleted.

## Implementation Phases

### Phase 1: Build The Debt Map

Create the audit report and JSON inventory without changing behavior.

Acceptance:

- every hit has a path and line number;
- every hit has a P0, P1, P2, or P3 category;
- bundled skills, third-party content, generated outputs, and worktrees are not
  mixed into the main debt list;
- direct-delete, isolate, gate, and keep decisions are visible.

### Phase 2: Remove P0 Current Output Pollution

Clean the highest-risk trust surfaces first:

```text
runtime-input-packet.json
router current output
requirement_doc
xl_plan
phase-execute.json
cleanup-receipt.json
completion / delivery acceptance reports
```

Acceptance:

- new runtime packets do not contain `legacy_skill_routing`;
- new runtime packets do not contain `stage_assistant_hints`;
- new runtime packets do not contain root `specialist_recommendations`;
- new runtime packets do not contain root `specialist_dispatch`;
- current requirement docs and XL plans do not present retired terms as active
  sections;
- `used` claims require `skill_usage.evidence`.

### Phase 3: Isolate Or Delete P1 Dependencies

Move remaining retired-field readers and helpers out of current paths.

Acceptance:

- current runtime paths do not directly read retired fields unless the call is
  through an explicit legacy or retired adapter;
- legacy adapters cannot write retired fields into current runtime packets;
- retired fields cannot affect current selection;
- retired fields cannot act as material-use evidence;
- PowerShell and Python compatibility logic follow the same contract.

### Phase 4: Clean P2 Docs And Tests

Update current documentation and current behavior tests.

Acceptance:

- README, runtime docs, install docs, and status docs explain the current field
  model;
- current behavior tests do not assert retired fields as normal output;
- retired behavior tests are explicitly named or marked;
- historical specs either carry a Historical / Retired Note or are removed from
  current navigation.

### Phase 5: Add The Regression Gate

Add or strengthen the current routing debt gate.

Expected output:

```json
{
  "status": "pass",
  "current_runtime_forbidden_hits": 0,
  "current_docs_forbidden_hits": 0,
  "current_tests_old_contract_hits": 0,
  "legacy_allowed_hits": 37,
  "retired_terms": [
    "legacy_skill_routing",
    "stage_assistant_hints",
    "specialist_recommendations"
  ],
  "current_fields": [
    "skill_candidates",
    "skill_routing.selected",
    "selected_skill_execution",
    "skill_usage.used",
    "skill_usage.unused",
    "skill_usage.evidence"
  ]
}
```

Acceptance:

- current runtime forbidden hits are zero;
- current docs forbidden hits are zero;
- current tests old-contract hits are zero;
- legacy allowed hits are reported rather than hidden;
- selected-to-used jumps are blocked unless evidence exists.

## Verification Plan

Run focused Python tests:

```powershell
python -m pytest tests/runtime_neutral -q
python -m pytest tests/unit -q
python -m pytest tests/integration -q
```

Run focused PowerShell gates:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-router-contract-gate.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-output-artifact-boundary-gate.ps1 -WriteArtifacts
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-current-routing-debt-gate.ps1 -WriteArtifacts
```

If implementation touches install, release, packaging, or copied runtime
payloads, also run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-version-consistency-gate.ps1 -WriteArtifacts
```

## Final Acceptance

The cleanup is accepted when:

- current runtime output has zero retired-field pollution;
- current router output has zero retired-field pollution;
- current documentation has zero active old-term explanations;
- current behavior tests have zero retired-contract dependency;
- legacy, retired, historical, and fixture hits are explicit and explainable;
- `selected` is never reported as `used`;
- `skill_usage.evidence` is required for material-use claims;
- pack routing capability does not regress;
- the six governed stages do not regress;
- the new or strengthened gate prevents retired terms from re-entering current
  paths.

The goal is not global zero matches for every old word. The goal is stronger:
current behavior is clean, old behavior is isolated, and future regressions are
blocked by executable evidence.
