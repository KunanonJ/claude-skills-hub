# Rabbit Review Follow-up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the six still-valid CodeRabbit inline findings on PR 228 with minimal, verified changes.

**Architecture:** Keep each fix local to the component flagged by the review. Add narrow regression coverage beside the existing tests for the affected runtime, verifier, installer, and documentation surfaces.

**Tech Stack:** Python, pytest, PowerShell, repository markdown governance docs.

---

## File Map

- Modify: `docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md`
  - Align the stale Task 2 projection snippet with current selected-plus-host-approved lock semantics.
- Modify: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`
  - Add shared lock ID normalization from `locked_skill_ids` or `locked_dispatch`.
- Modify: `packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py`
  - Add regression tests for lock evaluators when only `locked_dispatch` is present.
- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
  - Catch collection timeouts and raise structured `RuntimeError`.
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`
  - Add regression coverage for collect-only timeout handling.
- Modify: `scripts/install/Install-VgoAdapter.ps1`
  - Remove the in-place early return and preserve pruning plus sanitization.
- Modify: installer-focused tests under `tests/runtime_neutral/`
  - Add a focused in-place corpus regression using the PowerShell installer path.
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
  - Make retired helper shims non-throwing and exclude host-deferred/rejected lock IDs.
- Modify: `tests/runtime_neutral/test_current_routing_contract_cleanup.py`
  - Update the missing-helper fallback expectation to no-op behavior.
- Modify: `tests/runtime_neutral/test_skill_execution_lock_contract.py`
  - Add coverage for host-deferred/rejected exclusion.
- Modify: `packages/runtime-core/src/vgo_runtime/test_skill_execution_lock_reconciliation.py`
  - Add lower-level lock projection coverage for host-deferred/rejected exclusion.

---

### Task 1: Python Delivery Acceptance Lock ID Fallback

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`
- Modify: `packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py`

- [ ] **Step 1: Add failing tests**

Add tests that pass an active lock with `locked_dispatch` but no
`locked_skill_ids`. `_evaluate_specialist_lock_resolution` should require the
dispatch skill to be resolved, and `_evaluate_selected_lock_reconciliation`
should treat the dispatch skill as locked.

- [ ] **Step 2: Run failing tests**

Run:

```powershell
pytest packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py -q
```

Expected before implementation: at least one new test fails because the code
treats the active lock as empty.

- [ ] **Step 3: Implement helper**

Add `_locked_skill_ids(skill_execution_lock)` that returns normalized
`locked_skill_ids` when present, otherwise normalizes
`locked_dispatch[*].skill_id`. Use it in both evaluators.

- [ ] **Step 4: Verify**

Run the same pytest command. Expected: all tests in the file pass.

### Task 2: Collection Timeout Error Handling

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`

- [ ] **Step 1: Add failing test**

Add a fake runner that raises `subprocess.TimeoutExpired` during
`run_collect_commands`. Assert the raised `RuntimeError` includes the pytest
args, source layer IDs, timeout, partial stdout, and partial stderr.

- [ ] **Step 2: Run failing test**

Run:

```powershell
pytest tests/runtime_neutral/test_test_baseline_audit.py -q
```

Expected before implementation: the new test fails or surfaces raw
`TimeoutExpired`.

- [ ] **Step 3: Implement catch**

Wrap the runner call in `try/except subprocess.TimeoutExpired` and re-raise a
structured `RuntimeError` with layer context and captured output.

- [ ] **Step 4: Verify**

Run the same pytest command. Expected: all tests in the file pass.

### Task 3: Runtime Shim And Lock Projection Fixes

**Files:**
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Modify: `tests/runtime_neutral/test_current_routing_contract_cleanup.py`
- Modify: `tests/runtime_neutral/test_skill_execution_lock_contract.py`
- Modify: `packages/runtime-core/src/vgo_runtime/test_skill_execution_lock_reconciliation.py`

- [ ] **Step 1: Add or update failing tests**

Update the missing retired consultation helper test so the fallback returns
without failure and yields `$null`. Add execution lock tests showing deferred
or rejected host decisions are excluded from current selected records, previous
lock rehydration, and host-approved additions.

- [ ] **Step 2: Run failing tests**

Run:

```powershell
pytest tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_skill_execution_lock_contract.py packages/runtime-core/src/vgo_runtime/test_skill_execution_lock_reconciliation.py -q
```

Expected before implementation: the new or updated tests fail on the current
throwing shim and non-excluding lock projection.

- [ ] **Step 3: Implement runtime fixes**

Remove throw paths from the three missing-retired-helper shim functions. Add a
normalized `$hostExcluded` set from `deferred_skill_ids` and
`rejected_skill_ids`; skip excluded IDs in all execution lock source loops.

- [ ] **Step 4: Verify**

Run the same pytest command. Expected: all selected tests pass.

### Task 4: PowerShell Installer In-place Corpus Fix

**Files:**
- Modify: `scripts/install/Install-VgoAdapter.ps1`
- Modify: focused installer tests under `tests/runtime_neutral/`

- [ ] **Step 1: Add failing test**

Create a regression that installs or invokes the PowerShell installer path with
the internal corpus source equal to its destination. Assert an unselected child
directory is pruned and selected skills have `SKILL.runtime-mirror.md`.

- [ ] **Step 2: Run failing test**

Run:

```powershell
pytest tests/runtime_neutral/test_generated_nested_bundled.py::InstallTimeGeneratedNestedBundledTests::test_powershell_fallback_in_place_internal_corpus_prunes_and_sanitizes -q
```

Expected before implementation: stale children remain or selected entrypoints
are not sanitized.

- [ ] **Step 3: Implement installer fix**

Delete the early return after `Add-VgoCreatedPath`. Compute selected names,
prune unselected in-place directories, skip `Copy-DirContent` when source and
destination are the same path, and always call
`Convert-SkillEntryPointToRuntimeMirror` for selected skills.

- [ ] **Step 4: Verify**

Run:

```powershell
pytest tests/runtime_neutral/test_generated_nested_bundled.py::InstallTimeGeneratedNestedBundledTests::test_powershell_fallback_in_place_internal_corpus_prunes_and_sanitizes -q
```

Expected: pass. This verifies the in-place path continues after
`Add-VgoCreatedPath`, avoids a self-copy through `Copy-DirContent`, and still
normalizes selected skills through `Convert-SkillEntryPointToRuntimeMirror`.

### Task 5: Documentation Snippet Alignment

**Files:**
- Modify: `docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md`

- [ ] **Step 1: Update snippet**

Replace the stale snippet so it derives selected IDs from
`Get-VibeSkillRoutingSelected`, preserves current selected records, and adds
host approved records as an augmentation.

- [ ] **Step 2: Verify text**

Run:

```powershell
rg -n "currentSkillIds|currentSelectedRecords|host_approved_added_to_lock" docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md
```

Expected: the snippet contains selected-only current ID derivation and additive
host approval wording.

### Task 6: Final Verification And Commit

**Files:**
- All modified files.

- [ ] **Step 1: Run targeted tests**

Run all targeted commands from Tasks 1 through 4.

- [ ] **Step 2: Run validation gate**

Run:

```powershell
pytest tests/runtime_neutral/test_test_baseline_audit.py packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_skill_execution_lock_contract.py packages/runtime-core/src/vgo_runtime/test_skill_execution_lock_reconciliation.py -q
```

Expected: pass.

- [ ] **Step 3: Check status and commit**

Run:

```powershell
git status --short
git add docs/superpowers/specs/2026-05-06-rabbit-review-followup-design.md docs/superpowers/plans/2026-05-06-rabbit-review-followup.md docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py packages/verification-core/src/vgo_verify/test_baseline_audit.py tests/runtime_neutral/test_test_baseline_audit.py scripts/install/Install-VgoAdapter.ps1 scripts/runtime/VibeRuntime.Common.ps1 tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_skill_execution_lock_contract.py packages/runtime-core/src/vgo_runtime/test_skill_execution_lock_reconciliation.py
git commit -m "fix: address remaining rabbit review findings"
```

Expected: commit succeeds on `review/pr226-pr227-combined`.

- [ ] **Step 4: Push**

Run:

```powershell
git push origin review/pr226-pr227-combined
```

Expected: PR 228 receives the new commit.
