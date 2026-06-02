# Governed Entry Lineage And Child Envelope Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

## Summary
Strengthen governance only inside the official `vibe` governed entry and the child lanes it derives. The design does not attempt host-level sandboxing, OS-level interception, or prevention of direct manual script execution. Instead, it makes the governed path materially harder to bypass by adding runtime-validated lineage, a root-authored child delegation envelope, and a strict split between canonical truth surfaces and child-local receipts.

This design is an additive hardening layer on top of the existing root/child hierarchy contract. It turns several rules that are currently mostly protocol discipline or post-hoc contract gates into runtime-checked entry conditions for the governed path.

## Problem
The current governed runtime already defines:

- a fixed 6-stage state machine
- one canonical requirement surface
- one canonical execution-plan surface
- root versus child governance lanes
- `$vibe` tail discipline for delegated prompts

That is useful, but some important invariants are still enforced primarily by:

- protocol wording
- review discipline
- contract gates that run after artifacts exist
- smoke tests that prove expected topology rather than block bad topology at startup

This leaves a gap inside the governed path itself:

- the root lane can describe stage order, but later stages do not yet require a signed lineage receipt proving the preceding stage actually completed under the same governed run
- child lanes can inherit hierarchy metadata, but startup does not yet require a root-authored delegation envelope that binds inherited requirement and plan truth, allowed scope, and specialist permissions
- child lanes are forbidden from creating a second canonical requirement or plan surface, but much of that protection still behaves like a contract expectation rather than a startup-time runtime rejection

The result is that official `vibe` entry is disciplined, but not as sealed as it should be for the specific invariants the user wants to strengthen.

## Goals
- Make the governed 6-stage path runtime-validated inside the official entrypoint.
- Make child-governed lanes startup-validate inherited governance instead of trusting loose convention.
- Keep one canonical requirement truth and one canonical plan truth per root-governed task.
- Enforce that child lanes reuse inherited canonical truth and emit only local receipts/evidence.
- Strengthen `$vibe` tail discipline and child-lane prompt governance as part of delegated execution metadata.
- Keep the canonical router as route authority and keep `vibe` as governed runtime authority.

## Non-Goals
- No host-kernel or OS-level sandboxing.
- No attempt to block arbitrary direct manual execution of scripts outside the official governed entry.
- No new visible startup surface, parallel router, or second planning ritual.
- No redesign of the full router ranking or specialist recommendation engine.
- No cryptographic trust model beyond repository-local runtime artifacts and deterministic validation rules.

For clarity in the rest of this document, terms like "signed" or "sealed" mean run-bound, root-authored runtime validation artifacts, not cryptographic signatures.

## Scope Boundary
This design covers only:

- the official governed runtime entry
- the stage transitions inside that entry
- child lanes derived from that root-governed run
- delegated specialist execution approval boundaries inside those lanes

This design explicitly does not cover:

- manual execution that bypasses the official runtime entry
- arbitrary shell sessions outside governed execution
- generic repository-wide policy enforcement for unrelated scripts

## Design Options Considered

### Option A: Keep post-hoc contract gates only
Pros:
- minimal implementation churn
- preserves current loose flexibility

Cons:
- violations are discovered after artifacts are already written
- child-lane discipline remains easier to drift from at execution time
- does not materially strengthen the governed runtime itself

### Option B: Runtime sealed lineage plus child delegation envelope
Pros:
- strengthens the official governed path without pretending to solve OS-level enforcement
- keeps additive compatibility with the current hierarchy model
- converts key invariants into startup or transition-time failures instead of review-time surprises

Cons:
- requires new runtime artifacts and validation logic
- slightly increases orchestration complexity

### Option C: Full host-level hard gate across all script entrypoints
Pros:
- strongest theoretical enforcement

Cons:
- out of scope for current architecture
- conflicts with the requirement to cover only official governed entry and derived child lanes
- much higher risk of brittle developer ergonomics

## Decision
Choose Option B.

The repository should harden the governed path by adding:

1. a root-run governance capsule plus stage-lineage validation
2. a root-authored delegation envelope for child lanes
3. runtime rejection when child lanes try to reopen canonical requirement or plan truth

## Existing Surfaces To Extend
- `scripts/runtime/invoke-vibe-runtime.ps1`
- `scripts/runtime/VibeRuntime.Common.ps1`
- `scripts/runtime/Invoke-PlanExecute.ps1`
- `scripts/runtime/Invoke-DelegatedLaneUnit.ps1`
- `scripts/runtime/Write-RequirementDoc.ps1`
- `scripts/runtime/Write-XlPlan.ps1`
- `protocols/runtime.md`
- `protocols/team.md`
- governed runtime verification gates and runtime-neutral tests

The design should remain additive relative to the current root/child hierarchy contract rather than replacing it.

## Architecture

### 1. Governance Capsule
The official root-governed entry writes a `governance-capsule.json` under the run output directory at startup.

Its purpose is to establish the root authority context that every later stage and delegated child lane can validate against.

Minimum fields:

- `run_id`
- `root_run_id`
- `governance_scope`
- `runtime_selected_skill`
- `state_machine_version`
- `allowed_stage_sequence`
- `requirement_truth_owner`
- `plan_truth_owner`
- `created_at`

Rules:

- for root-governed runs, `run_id == root_run_id`
- `runtime_selected_skill` must remain `vibe`
- only the official governed entry may originate a new root capsule
- child lanes may reference root capsule authority, but may not create a competing root capsule

### 2. Stage Lineage Ledger
Each stage transition writes a lineage receipt into `stage-lineage.json`.

Its purpose is to make later stages prove they are continuing the same governed run in the correct order instead of merely receiving loosely compatible parameters.

Minimum fields per stage record:

- `stage_name`
- `run_id`
- `root_run_id`
- `previous_stage_name`
- `previous_stage_receipt_path`
- `current_receipt_path`
- `transition_validated`
- `validated_at`

Rules:

- `requirement_doc` cannot execute unless `deep_interview` receipt exists and matches the current governed run
- `xl_plan` cannot execute unless requirement receipt exists and points at the canonical requirement doc path
- `plan_execute` cannot execute unless plan receipt exists and points at the canonical plan doc path
- `phase_cleanup` cannot complete unless execution receipts exist for the current governed run
- missing, out-of-order, or mismatched lineage is a runtime failure inside official entry

### 3. Delegation Envelope
Before spawning a child-governed lane, the root lane writes a `delegation-envelope.json`.

Its purpose is to bind the child lane to the inherited root truth surface and approved execution boundaries.

Minimum fields:

- `root_run_id`
- `parent_run_id`
- `parent_unit_id`
- `child_run_id`
- `governance_scope`
- `requirement_doc_path`
- `execution_plan_path`
- `write_scope`
- `approved_specialists`
- `review_mode`
- `prompt_tail_required`
- `allow_requirement_freeze`
- `allow_plan_freeze`
- `allow_root_completion_claim`

Rules:

- `governance_scope` must be `child_governed`
- `prompt_tail_required` must be `$vibe`
- child startup must fail if the envelope is missing
- child startup must fail if inherited requirement/plan paths are missing or do not match the root-governed truth
- child startup must fail if the write scope or specialist approval surface is absent

### 4. Child Truth-Surface Split
Canonical truth remains root-owned.

Root-governed lanes may:

- write canonical requirement docs under `docs/requirements/`
- write canonical plans under `docs/plans/`
- publish full-task completion claims

Child-governed lanes may:

- read inherited canonical requirement and plan paths
- emit local execution receipts
- emit delegation validation receipts
- emit bounded evidence and escalation artifacts

Child-governed lanes must not:

- create a second canonical requirement doc
- create a second canonical plan doc
- publish final completion claims for the full root task
- self-approve new global specialist dispatch outside the root-approved envelope

### 5. Delegation Validation Receipt
Every child lane should write `delegation-validation-receipt.json` before executing its bounded unit.

Purpose:

- prove that the child lane validated inherited truth and governance metadata
- make child startup audit-friendly without reopening canonical docs

Minimum fields:

- `child_run_id`
- `root_run_id`
- `envelope_path`
- `requirement_doc_path`
- `execution_plan_path`
- `write_scope_valid`
- `prompt_tail_valid`
- `specialist_approval_valid`
- `validated_at`

## Component Boundaries

### Root runtime entry validator
Responsibilities:

- originate the governance capsule for a root-governed run
- validate that the runtime-selected skill remains `vibe`
- reject any attempt to start a competing root authority surface from child context

Interface:

- input: run metadata plus official entry parameters
- output: `governance-capsule.json`

### Stage lineage validator
Responsibilities:

- validate ordered stage transitions for the current run
- confirm prior stage receipt ownership and canonical requirement/plan references
- append authoritative lineage entries or fail the transition

Interface:

- input: current stage name, prior receipt path, run identifiers
- output: stage-lineage entry or runtime failure

### Delegation envelope emitter
Responsibilities:

- create the child startup contract before dispatch
- bind inherited requirement and plan truth
- bind write scope, specialist approval, and prompt-tail policy

Interface:

- input: root run metadata, child unit contract, inherited canonical paths
- output: `delegation-envelope.json`

### Child lane startup validator
Responsibilities:

- verify delegation envelope presence and internal consistency
- verify inherited canonical truth references
- verify child-only permissions before any bounded execution

Interface:

- input: child runtime parameters plus delegation envelope reference
- output: `delegation-validation-receipt.json` or startup failure

### Canonical write guard
Responsibilities:

- allow canonical requirement/plan writes only for root-governed lanes
- reject child attempts to write under `docs/requirements/` or `docs/plans/`
- preserve child ability to emit local receipts and evidence

Interface:

- input: requested write target plus governance scope metadata
- output: allowed write or runtime rejection

## Runtime Flow

### Root-governed path
1. Official entry starts run and writes `governance-capsule.json`.
2. `skeleton_check` writes its receipt and stage-lineage entry.
3. `deep_interview` writes intent contract and stage-lineage entry.
4. `requirement_doc` writes the canonical requirement doc and stage-lineage entry.
5. `xl_plan` writes the canonical execution plan and stage-lineage entry.
6. `plan_execute` validates lineage before running.
7. When delegation is needed, root writes `delegation-envelope.json` per child lane before dispatch.
8. `phase_cleanup` verifies execution receipts plus lineage completeness before final cleanup receipt.

### Child-governed path
1. Child lane receives inherited runtime parameters plus delegation envelope reference.
2. Child startup validates the envelope before doing any bounded work.
3. Child writes `delegation-validation-receipt.json`.
4. Child executes only within write scope and approved specialist boundary.
5. Child emits local receipts or escalation artifacts.
6. Child returns evidence to root without creating canonical requirement or plan artifacts.

## Specialist Dispatch Rules
The design keeps the existing distinction:

- `approved_dispatch`: root-approved specialist usage frozen into the plan or delegation envelope
- `local_suggestion`: child-detected specialist need that remains advisory until root approval

Runtime strengthening:

- child lanes may execute only specialists listed in the envelope's approved specialist surface
- child lanes may surface escalation receipts for unapproved specialists, but must not directly activate them
- root aggregation remains the only authority that can transform a `local_suggestion` into executable approved dispatch

## Failure Model
The governed path should fail fast for these conditions:

- missing governance capsule in a root-governed late-stage transition
- stage executed out of order relative to lineage ledger
- stage receipt belongs to another run or root run
- child lane missing delegation envelope
- child lane envelope missing canonical requirement or plan reference
- child lane attempts canonical requirement or plan writes
- child lane attempts final full-task completion claim
- child lane attempts specialist dispatch not approved by root
- delegated prompt metadata shows `$vibe` tail is not preserved

These failures are runtime-authoritative only for the official governed path. They do not claim system-wide sandbox authority beyond that boundary.

## Data And Artifact Model
Root-run artifacts under `outputs/runtime/vibe-sessions/<run-id>/`:

- `governance-capsule.json`
- `stage-lineage.json`

Child-lane/session artifacts under the delegated child root:

- `delegation-envelope.json`
- `delegation-validation-receipt.json`

Important design constraint:

- these artifacts are governance evidence and runtime-control surfaces
- they are not a second requirement surface or second plan surface
- canonical requirement truth remains under `docs/requirements/`
- canonical plan truth remains under `docs/plans/`

## Compatibility Notes
- The canonical router remains authoritative for route selection.
- `vibe` remains the governed runtime authority.
- Existing root/child hierarchy semantics remain conceptually valid and become more enforceable.
- The design is additive and should not require re-baselining the public mental model.
- Direct manual execution outside official entry is still possible and intentionally remains out of scope.

## Error Handling And Recovery
- Validation failures should be explicit and receipt-backed, not silent downgrades.
- The runtime may report actionable recovery guidance such as "restart from official entry" or "regenerate child lane from root with valid envelope."
- The runtime must not auto-heal by silently inventing missing requirement or plan truth.
- If a child lane lacks approved specialist coverage, the correct recovery path is escalation back to root rather than silent dispatch.

## Testing Strategy

### Runtime-neutral tests
Add or extend tests proving:

- late-stage root transitions require matching lineage
- child lane startup requires delegation envelope
- child lane reuses inherited requirement and plan paths
- child lane cannot publish canonical requirement or plan surfaces
- child lane cannot activate unapproved specialist dispatch

Suggested test names:

- `test_official_runtime_requires_stage_lineage_for_late_stage_transition`
- `test_child_lane_requires_delegation_envelope`
- `test_child_lane_reuses_inherited_requirement_and_plan`
- `test_child_lane_rejects_unapproved_specialist_dispatch`

### Governed gates
Extend or add governed verification so the runtime contract is checked at execution-policy level, not docs alone:

- governed runtime contract gate should assert lineage/capsule expectations
- duplicate canonical surface gate should assert child runtime rejection paths
- child specialist escalation gate should assert envelope-bounded specialist execution

## Risks
- Artifact bloat: more runtime files may make sessions noisier.
- False rigidity: some current flows may rely on loose child startup and now fail until updated.
- Partial enforcement: if some internal path bypasses validation helpers, governance appears stronger than it is.

## Mitigations
- Keep artifact schema minimal and purpose-specific.
- Centralize validation helpers in runtime common utilities rather than scattering ad-hoc checks.
- Add tests that exercise real stage transitions and delegated startup rather than asserting docs only.
- Keep scope narrow to official entry and child lanes so claims remain accurate.

## Rollout Guidance
Implementation should happen in this order:

1. define artifact schema and validation helpers
2. harden root stage transitions
3. harden delegated child startup
4. enforce child truth-surface split in write paths
5. update protocol docs and verification gates
6. run targeted tests and governed verification

This order reduces the chance of landing documentation or tests that describe enforcement not yet wired into the runtime.

## Acceptance Criteria
- Official governed entry writes a root-run governance capsule and validates lineage across late-stage transitions.
- Child-governed lanes require a root-authored delegation envelope before executing bounded work.
- Child lanes reuse inherited canonical requirement and plan truth and cannot create new canonical truth surfaces.
- Child lanes cannot self-approve new specialist execution beyond root-approved envelope metadata.
- Runtime failures are explicit and receipt-backed when these invariants are violated.
- Existing authority split remains intact: router selects route, `vibe` governs runtime, child lanes execute bounded work.

## Open Questions
No blocking open questions remain for planning.

The main remaining work is implementation detail, not product-direction uncertainty:

- where to centralize schema validation helpers
- whether lineage should be stored as one cumulative ledger or one receipt per transition
- how much of prompt-tail validation is enforced from metadata versus audited from dispatch surfaces
