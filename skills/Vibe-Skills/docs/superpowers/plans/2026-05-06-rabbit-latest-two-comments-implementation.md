# Rabbit Latest Two Comments Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the valid PR 228 CodeRabbit finding by making `audit.run_layer()` raise `PolicyError` for unknown layer IDs even when `collected_nodes=None`, while leaving selected-lock reconciliation semantics unchanged.

**Architecture:** Keep the patch local to the baseline-audit module. Reuse the same `layer_by_id(policy)` validation pattern already used by `select_layer_files()` and `build_run_layer_command()`, then add a direct-call regression test that exercises the previously uncovered `run_layer()` path.

**Tech Stack:** Python, pytest, unittest, existing verification-core baseline audit helpers

---

## File Structure

- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
  - Add a narrow unknown-layer guard near the top of `run_layer()`.
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`
  - Add a regression test for direct `run_layer()` calls with `collected_nodes=None`.
- Keep unchanged: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`
  - The no-active-lock `passing` behavior remains as-is because the spec rejected that Rabbit suggestion.

### Task 1: Add the failing regression test

**Files:**
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`
- Reference: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`

- [ ] **Step 1: Write the failing test**

```python
    def test_run_layer_raises_policy_error_for_unknown_layer_without_collected_nodes(self) -> None:
        policy = copy.deepcopy(audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json"))

        with self.assertRaisesRegex(audit.PolicyError, "Unknown layer id: missing_layer"):
            audit.run_layer(
                REPO_ROOT,
                policy,
                "missing_layer",
                collected_nodes=None,
                runner=FakeRunner(),
            )
```

- [ ] **Step 2: Run the targeted test to verify it fails**

Run: `pytest tests/runtime_neutral/test_test_baseline_audit.py -k "unknown_layer_without_collected_nodes" -q`
Expected: `FAIL` because `run_layer()` currently raises `KeyError` instead of `audit.PolicyError`.

- [ ] **Step 3: Commit the red test checkpoint**

```bash
git add tests/runtime_neutral/test_test_baseline_audit.py
git commit -m "test: cover run_layer unknown layer direct call"
```

### Task 2: Implement the minimal guard in `run_layer()`

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
- Test: `tests/runtime_neutral/test_test_baseline_audit.py`

- [ ] **Step 1: Add the smallest possible validation block**

```python
def run_layer(
    repo_root: Path,
    policy: dict[str, Any],
    layer_id: str,
    *,
    collected_nodes: list[str] | None = None,
    runner=subprocess.run,
    progress: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    layers = layer_by_id(policy)
    if layer_id not in layers:
        raise PolicyError(f"Unknown layer id: {layer_id}")

    selected_files: list[str] = []
    if collected_nodes is not None:
        selected_files = select_layer_files(collected_nodes, repo_root, policy, layer_id)
    layer = layers[layer_id]
```

- [ ] **Step 2: Run the targeted test to verify it passes**

Run: `pytest tests/runtime_neutral/test_test_baseline_audit.py -k "unknown_layer_without_collected_nodes" -q`
Expected: `1 passed`

- [ ] **Step 3: Commit the implementation checkpoint**

```bash
git add packages/verification-core/src/vgo_verify/test_baseline_audit.py tests/runtime_neutral/test_test_baseline_audit.py
git commit -m "fix: validate run_layer layer ids"
```

### Task 3: Verify no regression in adjacent coverage

**Files:**
- Test: `tests/runtime_neutral/test_test_baseline_audit.py`
- Test: `packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py`
- Test: `tests/runtime_neutral/test_runtime_delivery_acceptance.py`

- [ ] **Step 1: Run the focused baseline-audit suite**

Run: `pytest tests/runtime_neutral/test_test_baseline_audit.py -q`
Expected: `PASS`

- [ ] **Step 2: Re-run the selected-lock coverage to prove the rejected Rabbit comment stayed unchanged**

Run: `pytest packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py tests/runtime_neutral/test_runtime_delivery_acceptance.py -q`
Expected: `PASS`

- [ ] **Step 3: Run diff hygiene checks**

Run: `git diff --check`
Expected: no output

- [ ] **Step 4: Commit the verification checkpoint if any plan-doc adjustments were needed**

```bash
git status --short
```

Expected: no unexpected unstaged changes before PR update work.

## Self-Review

- Spec coverage: the plan covers the one valid Rabbit finding, explicitly preserves the rejected selected-lock semantics, and includes the validation commands from the approved spec.
- Placeholder scan: no `TODO`/`TBD` markers or vague "handle this later" steps remain.
- Type consistency: the plan uses the existing `audit.run_layer(...)`, `audit.PolicyError`, `FakeRunner`, and `REPO_ROOT` names already present in the current test module.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-06-rabbit-latest-two-comments-implementation.md`.

Execution mode for this run: **Inline Execution**. The change is a single-path bugfix with one regression test, so batching it in this session is the narrowest path.
