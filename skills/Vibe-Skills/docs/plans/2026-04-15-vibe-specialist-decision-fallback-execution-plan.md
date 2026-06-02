# Vibe Specialist Decision And Repo-Asset Fallback Execution Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a governed `specialist_decision` contract that keeps no-match specialist resolution explicit, including traceable repo-asset fallback.

**Architecture:** Extend the runtime artifact projections with a shared `specialist_decision` object, surface it in requirement and plan docs, and evaluate it through a new `specialist_decision_truth` delivery-acceptance layer. Keep approved specialist disclosure logic intact and use an optional `specialist-decision.json` session sidecar only for task-specific repo-asset fallback details.

**Tech Stack:** PowerShell runtime scripts, Python verification core, Markdown governed docs, runtime-neutral pytest suite

---

## Chunk 1: Red Tests And Contract Freeze

### Task 1: Lock the behavior in docs and runtime-neutral tests

**Files:**
- Modify: `config/project-delivery-acceptance-contract.json`
- Modify: `tests/runtime_neutral/test_runtime_delivery_acceptance.py`
- Modify: `tests/runtime_neutral/test_governed_runtime_bridge.py`
- Add: `docs/requirements/2026-04-15-vibe-specialist-decision-fallback.md`
- Add: `docs/plans/2026-04-15-vibe-specialist-decision-fallback-execution-plan.md`

- [ ] **Step 1: Extend the delivery-acceptance contract**

Add `specialist_decision_truth` to the contract truth-layer vocabulary and required report fields.

- [ ] **Step 2: Add failing delivery-acceptance tests**

Write red tests proving:

- missing no-match resolution becomes non-green
- traceable repo-asset fallback becomes `PASS_DEGRADED`
- incomplete repo-asset fallback disclosure becomes `FAIL`

- [ ] **Step 3: Add failing governed-runtime bridge assertions**

Require runtime artifacts, requirement docs, and execution plans to expose `specialist_decision`.

- [ ] **Step 4: Run the targeted red suite**

Run:

`pytest -q tests/runtime_neutral/test_runtime_delivery_acceptance.py -k "specialist_decision or repo_asset_fallback or clean_root_run"`

Expected: FAIL until implementation lands.

## Chunk 2: Runtime Artifact Projection

### Task 2: Project `specialist_decision` through the governed runtime

**Files:**
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`

- [ ] **Step 1: Add a shared specialist-decision projection**

Create a runtime helper that derives structural decision state from approved dispatch, blocked, degraded, and advisory-only specialist outcomes.

- [ ] **Step 2: Support a governed repo-asset fallback sidecar**

Allow `specialist-decision.json` in the session root to enrich the structural decision with repo-asset fallback paths, reason, legal basis, and traceability basis.

- [ ] **Step 3: Write the decision into execution artifacts**

Emit `specialist_decision` into `runtime-input-packet.json`, `execution-manifest.json`, `phase-execute.json`, and `runtime-summary.json`.

- [ ] **Step 4: Re-run the bridge test**

Run:

`pytest -q tests/runtime_neutral/test_governed_runtime_bridge.py -k six_stage_closure`

Expected: PASS

## Chunk 3: Governed Requirement And Plan Surfaces

### Task 3: Make the decision visible in docs

**Files:**
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
- Modify: `scripts/runtime/Write-XlPlan.ps1`

- [ ] **Step 1: Add `## Specialist Decision` to requirement docs**

Always record the frozen specialist decision, including pending no-match resolution guidance when no dedicated specialist exists.

- [ ] **Step 2: Add `## Specialist Decision Plan` to execution plans**

Tell execution exactly when `specialist-decision.json` must be written and what fields it must contain for repo-asset fallback.

- [ ] **Step 3: Keep the existing dispatch section intact**

Do not regress the existing approved specialist dispatch and disclosure documentation.

## Chunk 4: Delivery-Acceptance Semantics

### Task 4: Gate no-match specialist resolution explicitly

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_support.py`
- Modify: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`

- [ ] **Step 1: Resolve the optional specialist-decision payload**

Support inline `phase-execute.json`, explicit `specialist_decision_path`, and default `specialist-decision.json` sidecar loading.

- [ ] **Step 2: Add `specialist_decision_truth` evaluation**

Implement the minimum rules:

- approved dispatch without matching decision -> `FAIL`
- no-match with pending resolution -> `MANUAL_REVIEW_REQUIRED`
- no-match with `no_specialist_needed` -> `PASS`
- no-match with complete repo-asset fallback -> `PASS_DEGRADED`
- no-match with incomplete repo-asset fallback -> `FAIL`

- [ ] **Step 3: Keep completion wording blocked for non-green fallback**

Do not allow repo-asset fallback to collapse into green completion.

- [ ] **Step 4: Re-run delivery-acceptance tests**

Run:

`pytest -q tests/runtime_neutral/test_runtime_delivery_acceptance.py`

Expected: PASS

## Chunk 5: Focused Verification

### Task 5: Verify the touched surfaces only

**Files:**
- No additional files expected beyond the runtime scripts, verification core, tests, and governed docs above

- [ ] **Step 1: Run the focused verification slice**

Run:

`pytest -q tests/runtime_neutral/test_runtime_delivery_acceptance.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py`

Expected: PASS

- [ ] **Step 2: Re-run the no-silent-fallback contract gate**

Run:

`pwsh -NoLogo -File scripts/verify/vibe-no-silent-fallback-contract-gate.ps1`

Expected: PASS

- [ ] **Step 3: Inspect only the touched diff**

Run:

`git diff -- config/project-delivery-acceptance-contract.json scripts/runtime/VibeRuntime.Common.ps1 scripts/runtime/Write-RequirementDoc.ps1 scripts/runtime/Write-XlPlan.ps1 scripts/runtime/Invoke-PlanExecute.ps1 scripts/runtime/invoke-vibe-runtime.ps1 packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_support.py packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py tests/runtime_neutral/test_runtime_delivery_acceptance.py tests/runtime_neutral/test_governed_runtime_bridge.py docs/requirements/2026-04-15-vibe-specialist-decision-fallback.md docs/plans/2026-04-15-vibe-specialist-decision-fallback-execution-plan.md`

Expected: only specialist-decision governance changes.

- [ ] **Step 4: Verify before claiming completion**

Re-run the exact focused verification commands immediately before any completion claim and report the actual results.
