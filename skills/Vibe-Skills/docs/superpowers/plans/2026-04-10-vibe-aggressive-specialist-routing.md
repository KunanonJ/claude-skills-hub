# Vibe Aggressive Specialist Routing Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `vibe` require specialist recommendations on every governed run and aggressively auto-promote safe recommendations into executable specialist dispatch.

**Architecture:** The change is policy-first and runtime-backed. We will update contract docs and runtime policy, then enforce the new behavior in runtime freeze and execute stages with test-first changes around fallback recommendation synthesis, child auto-absorb, and default native specialist execution.

**Tech Stack:** PowerShell runtime scripts, JSON policy files, Python `unittest` runtime-neutral tests

---

## Chunk 1: Test Baseline

### Task 1: Lock the new routing contract in tests

**Files:**
- Modify: `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`
- Modify: `tests/runtime_neutral/test_root_child_hierarchy_bridge.py`
- Modify: `tests/runtime_neutral/test_l_xl_native_execution_topology.py`
- Modify: `tests/runtime_neutral/test_skill_promotion_destructive_gate.py`

- [ ] **Step 1: Write or update failing assertions for mandatory recommendations**

Add assertions that a governed run always surfaces at least one specialist recommendation and at least one approved dispatch for safe tasks.

- [ ] **Step 2: Add a failing child-lane test for same-round auto-absorb without existing root dispatch**

Use a child-governed run where approved specialist ids do not overlap frozen local suggestions and assert that safe suggestions still auto-promote.

- [ ] **Step 3: Add a failing assertion for native specialist execution default-on**

Update the execution-policy expectation to require default enabled native specialist execution.

- [ ] **Step 4: Run the targeted test subset and confirm failures**

Run: `python -m pytest tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_root_child_hierarchy_bridge.py tests/runtime_neutral/test_l_xl_native_execution_topology.py tests/runtime_neutral/test_skill_promotion_destructive_gate.py -q`

Expected: failures reflecting the old conservative routing behavior.

## Chunk 2: Policy and Contract Surfaces

### Task 2: Update governed contract text and policy defaults

**Files:**
- Modify: `SKILL.md`
- Modify: `protocols/runtime.md`
- Modify: `protocols/team.md`
- Modify: `config/runtime-input-packet-policy.json`
- Modify: `config/skill-promotion-policy.json`
- Modify: `config/native-specialist-execution-policy.json`

- [ ] **Step 1: Update contract wording to make recommendation mandatory**

State that governed `vibe` must emit specialist recommendations and aggressively auto-promote eligible ones while preserving `vibe` as sole authority.

- [ ] **Step 2: Add aggressive routing policy knobs**

Add minimum recommendation floor and task-type fallback specialist mapping in `runtime-input-packet-policy.json`.

- [ ] **Step 3: Relax child auto-absorb gate policy**

Remove the implicit requirement for existing root-approved dispatch from policy semantics.

- [ ] **Step 4: Enable native specialist execution by default**

Switch the native specialist execution default from opt-in to opt-out.

## Chunk 3: Runtime Implementation

### Task 3: Enforce aggressive routing in freeze and execute stages

**Files:**
- Modify: `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
- Modify: `scripts/runtime/Write-XlPlan.ps1`

- [ ] **Step 1: Implement fallback specialist recommendation synthesis**

Teach runtime freeze to supplement router output with task-type fallback specialists until the minimum recommendation floor is met.

- [ ] **Step 2: Ensure safe fallback recommendations auto-promote in root scope**

Keep promotion metadata intact and verify synthesized recommendations carry complete native contract metadata.

- [ ] **Step 3: Remove existing-root-dispatch requirement from child same-round auto-absorb**

Update effective dispatch resolution so child lanes can auto-approve known safe recommendations even when frozen approved dispatch is empty.

- [ ] **Step 4: Update plan narrative surfaces**

Adjust plan text so generated execution plans describe specialist dispatch as default governed behavior instead of purely advisory help.

## Chunk 4: Verification and Cleanup

### Task 4: Prove the new routing behavior

**Files:**
- Modify as needed: relevant verification scripts only if contract wording/assertions break

- [ ] **Step 1: Run the targeted test subset until green**

Run: `python -m pytest tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_root_child_hierarchy_bridge.py tests/runtime_neutral/test_l_xl_native_execution_topology.py tests/runtime_neutral/test_skill_promotion_destructive_gate.py -q`

Expected: PASS

- [ ] **Step 2: Run one broader governed-runtime regression slice**

Run: `python -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py -q`

Expected: PASS

- [ ] **Step 3: Inspect git diff for touched files only**

Run: `git diff -- SKILL.md protocols/runtime.md protocols/team.md config/runtime-input-packet-policy.json config/skill-promotion-policy.json config/native-specialist-execution-policy.json scripts/runtime/Freeze-RuntimeInputPacket.ps1 scripts/runtime/Invoke-PlanExecute.ps1 scripts/runtime/Write-RequirementDoc.ps1 scripts/runtime/Write-XlPlan.ps1 tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_root_child_hierarchy_bridge.py tests/runtime_neutral/test_l_xl_native_execution_topology.py tests/runtime_neutral/test_skill_promotion_destructive_gate.py`

Expected: only aggressive specialist routing changes and aligned tests/docs.

- [ ] **Step 4: Summarize verification evidence**

Record which tests passed, which safeguards remain intentionally strict, and any residual routing edge cases not covered by this change.
