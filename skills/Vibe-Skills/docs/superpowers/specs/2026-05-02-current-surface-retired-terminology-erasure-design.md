# Current Surface Retired Terminology Erasure Design

Date: 2026-05-02

## Summary

The previous cleanup removed retired role fields from the active runtime and router behavior. The remaining debt is different: retired terminology still appears across current-facing audit modules, gates, tests, reports, and active documentation. That makes the repository feel only partially cleaned even when the active routing model no longer depends on those fields.

This design moves the current maintenance surface to one positive terminology model:

```text
skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage.used / skill_usage.unused / skill_usage.evidence
```

The cleanup is intentionally not a repo-wide historical rewrite. Historical plans, specs, and archived decision records may keep retired terms as evidence of past designs. Current code, current reports, active docs, and test output must not describe retired role concepts as the present architecture.

## Goals

- Remove retired role terminology from current-facing audit, verification, gate, test, report, and active documentation surfaces.
- Keep the active routing vocabulary centered on skill candidates, skill routing, selected skill execution, and skill usage evidence.
- Add a lightweight terminology budget gate so retired terms do not re-enter the current surface.
- Preserve historical design records instead of rewriting past decisions.
- Keep this work scoped to the repository checkout. It does not install or deploy the branch into any host.

## Non-Goals

- Do not rewrite `docs/superpowers/plans/**` or older historical specs only to reduce global search hits.
- Do not remove compatibility readers that are still needed to recognize retired input shapes, as long as they are clearly named as compatibility or retired-input handling.
- Do not change the runtime data model unless current audit code still depends on retired fields as positive current inputs.
- Do not perform broad mechanical find-and-replace across the repository.

## Retired Terms

The following terms are retired for positive current-surface use:

- `route_authority_candidates`
- `stage_assistant_candidates`
- `route_authority_eligible`
- `legacy_role`
- `_legacy_role`
- `_legacy_stage_assistant_candidates`
- positive-use `stage assistant`
- positive-use `route authority`
- positive-use `legacy admission role`
- current-report use of old pack-consolidation role language

These terms may still appear in explicitly negative assertions, compatibility handling, migration notes, or historical records.

## Current Terminology

Use the following replacements for current architecture language:

| Retired positive wording | Current wording |
| --- | --- |
| route authority candidates | skill candidates |
| stage assistant candidates | candidate skills for the stage |
| route authority eligible | routing-eligible skill |
| route authority selection | skill routing selection |
| stage assistant | skill |
| selected assistant | selected skill execution |
| legacy role | retired input or compatibility input |
| role usage proof | skill usage evidence |
| pack consolidation role | pack routing policy or skill routing policy |

Compatibility names should be explicit. For example, a reader that accepts an old input shape should use wording such as `retired_input`, `compatibility_input`, or `migration_input`, not current role wording.

## Surface Classification

### Current Surface

Retired terms must not appear as positive current concepts in these areas:

- `packages/runtime-core`
- `packages/verification-core`
- `scripts/router`
- `scripts/runtime`
- `scripts/verify`
- `tests`
- root README and current install/check/governance docs
- active docs under `docs/` that are not historical plans, specs, or archives

### Allowed Historical Surface

Retired terms may remain as historical evidence in:

- `docs/superpowers/plans/**`
- older design specs and archived docs
- changelog entries describing past behavior
- explicit migration records that explain why a retired concept was removed

Historical files should not be used as current routing or governance authority by the terminology gate.

### Allowed Negative Assertions

Retired terms may appear in tests and gates only when they are the subject of a ban or absence assertion. The surrounding names and messages should make that clear, for example:

- acceptable: "retired field leaked into current routing output"
- acceptable: "current surface forbids retired route-authority field"
- not acceptable: "route authority selects the stage assistant"

### Compatibility Surface

Compatibility code may mention retired terms only when recognizing old input and converting it into the current model. Such code should:

- be visibly named as compatibility, migration, or retired-input handling;
- not emit retired terms as current report fields;
- not re-export retired field names from current runtime or router output.

## Terminology Budget Gate

The cleanup should add or extend a lightweight gate that classifies retired-term hits by path and context.

The gate result categories are:

- `fail`: retired terminology appears as a positive current concept in the current surface.
- `allowed_negative`: retired terminology appears in a test or gate that asserts absence or forbids leakage.
- `allowed_historical`: retired terminology appears in historical plans, specs, archives, or changelog evidence.
- `review`: retired terminology appears in compatibility or migration code and needs explicit judgment.

The gate does not require zero matches across the repository. It requires no positive current-surface matches.

The gate report should make the cleanup state understandable without reading raw search output. It should show counts by category and include enough file references to fix regressions.

## Implementation Shape

Implementation should proceed in small, reviewable passes:

1. Add or update the terminology budget gate.
2. Clean current audit and verification modules, especially under `packages/verification-core/src/vgo_verify`.
3. Clean current tests, gate names, assertion messages, and report output.
4. Clean active documentation and current governance text.
5. Run the gate and targeted regression tests, then tighten allowlists where needed.

The gate can be introduced before the full cleanup if it initially reports current debt. The final acceptance state must be passing.

## Audit And Verification Layer

The verification layer is the main current-facing place where retired terminology can keep the old model visible. Audit modules should be migrated to current vocabulary without weakening their checks.

Expected changes:

- Report titles and fields use skill-routing and skill-usage evidence language.
- Audit errors describe retired-field leakage, not current role failure.
- Compatibility inputs are named as retired or compatibility inputs.
- Audit outputs do not emit retired role fields as first-class current fields.

The audit purpose remains the same: prove that routing outputs are clean, skill usage evidence is real, and retired fields do not re-enter the current governance surface.

## Test Strategy

Verification should include:

- terminology budget gate passes with no `fail` findings;
- existing current routing debt gate still passes;
- runtime output shape tests still pass;
- router contract and selection guard tests still pass;
- verification-core tests covering updated audit outputs pass;
- current routing and pack routing smoke tests pass where practical;
- `git diff --check` reports no whitespace or formatting problems.

Manual spot checks should use `rg` for the retired terms against current paths and confirm remaining hits are historical, negative, or compatibility-classified.

## Risks And Controls

| Risk | Control |
| --- | --- |
| Historical evidence is accidentally rewritten | Keep historical plans/specs out of the cleanup target and gate them as `allowed_historical`. |
| Compatibility code is mistaken for current architecture | Rename it to compatibility or retired-input handling and classify it as `review` until accepted. |
| Search results still feel noisy | Separate current-surface failure counts from historical and negative counts in the gate output. |
| Runtime behavior changes unintentionally | Keep model changes out of scope unless audit code proves it still depends on retired fields. |
| Tests keep old concepts alive through names and messages | Rename tests and assertions around current-surface leakage and retired-field bans. |

## Acceptance Criteria

This design is complete when:

- current-facing code and active docs no longer use retired role terms as positive current architecture language;
- retired-term hits are classified as historical, negative, compatibility/review, or failure;
- the terminology budget gate passes with zero `fail` findings;
- existing routing/runtime contract tests still pass;
- audit reports use current skill-routing and skill-usage evidence terminology;
- historical plans/specs remain available as evidence rather than being rewritten for cosmetic cleanliness.
