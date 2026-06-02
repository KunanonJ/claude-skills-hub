# Root/Child Vibe Hierarchy Governance Plan

## Execution Summary
Land a hierarchy model for XL governed execution so one user task has one root `vibe` runtime, child agents inherit `vibe` as subordinate execution lanes, and specialist skills remain bounded assistants rather than recursive governance owners. The design must preserve current explicit `vibe` authority, prevent duplicate canonical surfaces, and produce proof that the new hierarchy is stable, usable, and intelligent under realistic task delegation flows.

## Frozen Inputs
- Requirement doc: `docs/requirements/2026-03-28-root-child-vibe-hierarchy-governance.md`
- Problem statement: recursive child-agent `vibe` use currently risks layered governance, repeated specialist dispatch, and ambiguous completion authority
- Existing authority invariants:
  - canonical router keeps route authority
  - explicit `vibe` remains runtime owner
  - no second requirement truth
  - no second execution-plan truth

## Internal Grade Decision
- Grade: XL
- The change spans runtime packet policy, execution topology, manifests, protocol docs, and proof gates.
- Parallel implementation is justified, but final authority semantics must be integrated and verified as one coherent contract.

## Design Overview

### Target Model
- `root_governed`: the only runtime allowed to freeze canonical requirement and plan surfaces and make final completion claims
- `child_governed`: a subordinate `vibe` lane that inherits frozen context, keeps verification/cleanup discipline, and emits local receipts only
- `specialist_native`: a bounded helper execution style that can be root-approved for direct use or child-suggested for escalation

### Runtime Packet Additions
- `governance_scope`: `root` or `child`
- `root_run_id`
- `parent_run_id`
- `parent_unit_id`
- `inherited_requirement_doc_path`
- `inherited_execution_plan_path`
- `allow_requirement_freeze`
- `allow_plan_freeze`
- `allow_global_dispatch`
- `allow_completion_claim`
- `approved_specialist_dispatch`
- `local_specialist_suggestions`
- `escalation_required`

### Authority Split
- Root owns:
  - requirement freeze
  - plan freeze
  - global specialist approval
  - overall completion claim
  - root execution manifest
- Child owns:
  - bounded execution inside assigned scope
  - local receipts and proof
  - escalation requests when approved specialist coverage is insufficient
- Specialists own:
  - native workflow execution only
  - skill-specific validation notes and outputs
  - no runtime ownership and no top-level completion claims

## Wave Plan

### Wave 1: Contract Freeze
- Update requirement, plan, and stable governance docs to define the hierarchy model.
- Freeze naming for root versus child governance scope and approved dispatch versus local suggestion surfaces.
- Confirm which existing runtime packet fields can be extended without breaking current proofs.

### Wave 2: Runtime Packet and Policy
- Extend `config/runtime-input-packet-policy.json` with hierarchy fields and scope-specific authority flags.
- Update `scripts/runtime/Freeze-RuntimeInputPacket.ps1` to emit root or child packets.
- Ensure explicit `vibe` authority remains the runtime-selected skill for both scopes.

### Wave 3: Execution Topology and Artifact Boundaries
- Update `scripts/runtime/Invoke-PlanExecute.ps1` to spawn child lanes as subordinate runs instead of fresh top-level governed runs.
- Ensure child lanes inherit frozen requirement/plan paths and cannot write canonical docs.
- Add child receipt and escalation artifact surfaces under root-owned runtime outputs.

### Wave 4: Specialist Dispatch Semantics
- Split specialist data into:
  - root-approved dispatch
  - child-local suggestion
- Prevent child lanes from activating new global specialists without escalation approval.
- Preserve native specialist workflow, inputs, outputs, and verification expectations.

### Wave 5: Protocol and Operator Documentation
- Update `SKILL.md`, `protocols/runtime.md`, and `protocols/team.md` with root/child hierarchy semantics.
- Add a stable governance explainer for operator use and future implementation alignment.
- Clarify the user-facing mental model: child `$vibe` keeps discipline, not recursive top-level governance.

### Wave 6: Verification, Simulation, and Proof
- Add runtime-neutral tests for root/child packet semantics and child escalation behavior.
- Add governed gates for:
  - no duplicate canonical requirement surface
  - no duplicate canonical execution-plan surface
  - child cannot issue final completion claim
  - specialist suggestions remain advisory until root approval
- Run realistic delegation simulations:
  - root `vibe` planning task with child ML lane
  - root `vibe` debug task with child systematic-debugging lane
  - child requesting an extra specialist not pre-approved by root

### Wave 7: Rollout and Cleanup
- Re-run targeted gates after integration.
- Remove temporary artifacts and stale test scratch space.
- Audit for zombie node residue.
- Leave only intended source/docs/test changes and generated proof artifacts.

## Ownership Boundaries
- Runtime packet contract: `config/runtime-input-packet-policy.json`, `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- Execution topology and child-lane handoff: `scripts/runtime/Invoke-PlanExecute.ps1`
- Requirement/plan write restrictions: `scripts/runtime/Write-RequirementDoc.ps1`, `scripts/runtime/Write-XlPlan.ps1`
- Runtime authority docs: `SKILL.md`, `protocols/runtime.md`, `protocols/team.md`
- Stable explanatory doc: `docs/root-child-vibe-hierarchy-governance.md`
- Verification: `tests/runtime_neutral/*`, `scripts/verify/*`

## Implementation Steps
1. Freeze the new requirement and plan.
2. Add the stable governance explainer doc and wire it into docs navigation.
3. Extend runtime packet policy and packet emission for root/child scope.
4. Restrict canonical requirement/plan writes to root scope only.
5. Add approved specialist dispatch versus local suggestion semantics.
6. Update plan-execute so child lanes inherit context and emit subordinate receipts.
7. Update protocol docs and public-facing authority wording.
8. Add tests and governed gates for hierarchy invariants.
9. Run simulation scenarios and targeted verification commands.
10. Clean temp artifacts, audit node processes, and emit closure receipts.

## Verification Commands
- `git diff --check`
- `python3 -m pytest tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_governed_runtime_bridge.py`
- `python3 -m pytest tests/runtime_neutral -k "hierarchy or child or specialist or completion"`
- `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-governed-runtime-contract-gate.ps1`
- `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-benchmark-autonomous-proof-gate.ps1`
- `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-no-silent-fallback-contract-gate.ps1`
- new targeted gates:
  - `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-root-child-hierarchy-gate.ps1`
  - `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-no-duplicate-canonical-surface-gate.ps1`
  - `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-child-specialist-escalation-gate.ps1`
- targeted repo checks:
  - `rg -n "governance_scope|allow_requirement_freeze|allow_plan_freeze|allow_global_dispatch|allow_completion_claim|approved_specialist_dispatch|local_specialist_suggestions" config scripts/runtime protocols tests`

## Stability Proof Strategy
- Determinism:
  - same root input yields the same root authority fields and child-lane restrictions
- Non-duplication:
  - one root run cannot create more than one canonical requirement or plan
- Boundedness:
  - child lanes cannot widen into top-level governance
- Recovery:
  - escalation paths remain explicit and do not silently self-approve
- Regression safety:
  - existing explicit `vibe` specialist-accounting proofs continue to pass after hierarchy support lands

## Usability Proof Strategy
- Operators can explain the model in one sentence:
  - root `vibe` governs, child `vibe` executes, specialists assist
- Execution artifacts make authority obvious without reading chat history.
- Child-lane receipts show inherited context and limits clearly enough for debugging and audit.
- Failure paths produce actionable escalation surfaces instead of ambiguous re-planning.

## Intelligence Proof Strategy
- Root routing can still identify the best high-level specialist pattern without surrendering runtime authority.
- Child lanes can still use domain-specific specialist help inside approved boundaries.
- Ambiguous child requests produce escalation instead of unsafe self-expansion.
- Low-signal prompts still honor fallback hazard and non-authoritative truth semantics.

## Risks and Mitigations
- Risk: child lanes accidentally reopen requirement or plan surfaces
  - Mitigation: hard authority flags plus gates that fail on duplicate canonical surfaces
- Risk: specialist approval and child suggestion semantics drift apart
  - Mitigation: explicit separate fields and dedicated escalation artifacts
- Risk: hierarchy metadata becomes verbose but unenforced
  - Mitigation: add execution-path gates that inspect real artifacts, not docs only
- Risk: parent/child packet inheritance breaks current explicit `vibe` proofs
  - Mitigation: keep additive contract design and run existing governed gates before claiming completion

## Rollback Rules
- If root authority becomes ambiguous, stop and restore the last state where explicit `vibe` remained the sole runtime owner.
- If child lanes can write canonical requirement or plan surfaces, block completion until that regression is repaired.
- If specialist escalation cannot be kept explicit, fall back to root-approved specialist dispatch only.
- Do not revert unrelated user changes or existing untracked docs.

## Phase Cleanup Contract
- Remove scratch artifacts created for hierarchy simulation or gate fixtures.
- Audit and clear stale managed node processes if any appear.
- Keep only intended source/docs/test changes and proof artifacts.
- Emit cleanup receipts for the verification wave before claiming closure.
