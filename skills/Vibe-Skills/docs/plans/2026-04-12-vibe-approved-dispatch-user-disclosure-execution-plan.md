# Vibe Approved Dispatch User Disclosure Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a governed pre-execution disclosure that tells the user which routed Skills will actually run and which real entrypoint path each one uses.

**Architecture:** Build one runtime-backed disclosure projection from effective `approved_dispatch` after same-round dispatch resolution and before specialist execution. Persist the disclosure in execution artifacts and align the governed contract text so the behavior is treated as mandatory execution transparency rather than optional metadata.

**Tech Stack:** PowerShell runtime scripts, JSON policy, Markdown contract docs, Python runtime-neutral tests

---

## Chunk 1: Freeze Contract and TDD Targets

### Task 1: Lock the disclosure contract in docs and tests

**Files:**
- Modify: `SKILL.md`
- Modify: `protocols/runtime.md`
- Modify: `protocols/team.md`
- Modify: `config/runtime-input-packet-policy.json`
- Modify: `tests/runtime_neutral/test_governed_runtime_bridge.py`
- Modify: `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`

- [ ] **Step 1: Add contract wording for unified pre-dispatch disclosure**

State that when effective `approved_dispatch` is non-empty, governed `vibe` must emit one unified user-facing disclosure before execution, listing only actually executing Skills and each real `native_skill_entrypoint`.

- [ ] **Step 2: Add policy knobs for disclosure semantics**

Add a small disclosure policy block to `config/runtime-input-packet-policy.json` defining:

- enabled
- stage `plan_execute`
- scope `approved_dispatch_only`
- timing `before_execution`
- aggregation `unified_once`
- path source `native_skill_entrypoint`

- [ ] **Step 3: Write failing runtime assertions**

Add failing assertions to `tests/runtime_neutral/test_governed_runtime_bridge.py` that a specialist-bearing run produces a disclosure object and that the object contains:

- non-empty routed skills
- `skill_id`
- `native_skill_entrypoint`
- rendered text

- [ ] **Step 4: Write failing freeze-side assertions where appropriate**

If the freeze packet already contains the path truth needed downstream, add assertions in `tests/runtime_neutral/test_skill_promotion_freeze_contract.py` that approved dispatch entries carry `native_skill_entrypoint` and can support execution disclosure without path synthesis.

- [ ] **Step 5: Run the targeted tests and confirm failure**

Run: `python3 -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py -q`

Expected: FAIL on missing disclosure surface or missing assertions.

## Chunk 2: Runtime Disclosure Projection

### Task 2: Build the runtime-backed disclosure object

**Files:**
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`

- [ ] **Step 1: Add a disclosure projection helper**

Create a helper that accepts effective `approved_dispatch` and returns a disclosure object with:

- `enabled`
- `mode`
- `timing`
- `scope`
- `path_source`
- `routed_skill_count`
- `routed_skills`
- `rendered_text`

- [ ] **Step 2: Use only effective executable dispatch**

Build the disclosure from effective `approved_dispatch` after child same-round auto-absorb or other dispatch resolution has completed.

- [ ] **Step 3: Preserve execution truth and ordering**

De-duplicate repeated skill ids while preserving first execution order, and never include blocked, degraded, or local-suggestion-only entries.

- [ ] **Step 4: Store the disclosure in execution artifacts**

Attach the disclosure to the plan-execute output surface so governed runtime tests and downstream hosts can consume it from execution truth artifacts.

- [ ] **Step 5: Run the targeted tests and confirm green for the new surface**

Run: `python3 -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py -q`

Expected: PASS for disclosure assertions introduced in Chunk 1.

## Chunk 3: Narrative Surface Alignment

### Task 3: Make the governed text surfaces describe the new behavior

**Files:**
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
- Modify: `scripts/runtime/Write-XlPlan.ps1`

- [ ] **Step 1: Update requirement narrative**

Make the requirement surface explain that routed specialist execution is user-disclosed before execution and that only actually executing Skills are listed.

- [ ] **Step 2: Update plan narrative**

Make the plan surface describe the unified pre-dispatch disclosure and keep the explanation separate from router candidate or advisory surfaces.

- [ ] **Step 3: Ensure no second authority is implied**

Keep wording explicit that disclosure is an execution-transparency surface under `vibe`, not a separate route or approval layer.

- [ ] **Step 4: Run the main governed runtime bridge test again**

Run: `python3 -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py -q`

Expected: PASS

## Chunk 4: Full Verification

### Task 4: Verify behavior and inspect drift

**Files:**
- No new files expected beyond touched contract/runtime/test surfaces

- [ ] **Step 1: Run the focused governed runtime verification slice**

Run: `python3 -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_skill_promotion_metrics.py -q`

Expected: PASS

- [ ] **Step 2: Inspect the touched diff only**

Run: `git diff -- SKILL.md protocols/runtime.md protocols/team.md config/runtime-input-packet-policy.json scripts/runtime/VibeRuntime.Common.ps1 scripts/runtime/Invoke-PlanExecute.ps1 scripts/runtime/Write-RequirementDoc.ps1 scripts/runtime/Write-XlPlan.ps1 tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py docs/superpowers/specs/2026-04-12-vibe-approved-dispatch-user-disclosure-design.md docs/requirements/2026-04-12-vibe-approved-dispatch-user-disclosure.md docs/plans/2026-04-12-vibe-approved-dispatch-user-disclosure-execution-plan.md`

Expected: only disclosure-contract, runtime, and test changes.

- [ ] **Step 3: Summarize residual risks**

Capture whether any remaining host-specific work is still required to surface the disclosure directly in every adapter transcript.

- [ ] **Step 4: Verify before claiming completion**

Run the exact verification commands again immediately before any completion claim and report the actual output status.
