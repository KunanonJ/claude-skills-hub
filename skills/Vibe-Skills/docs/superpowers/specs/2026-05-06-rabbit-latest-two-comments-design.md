# Rabbit Latest Two Comments Design

## Context

PR 228 has two newly unresolved CodeRabbit inline threads after the previous
latest-three-comments patch landed on the remote branch. The branch is
`review/pr226-pr227-combined`.

This design covers only the two currently unresolved actionable threads:

1. A selected-lock reconciliation suggestion in
   `runtime_delivery_acceptance_runtime.py`.
2. An unknown-layer error-path suggestion in `test_baseline_audit.py`.

## Verified Findings

### Selected Lock Reconciliation Suggestion Is Not Valid

`packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`
currently returns `passing` from `_evaluate_selected_lock_reconciliation()` when
`required_skill_ids` exist but no active lock is present:

```python
if not required_skill_ids:
    return "passing", ["No selected/approved specialist execution obligations were present."], lists
if not lock_active:
    return "passing", ["No active specialist execution lock was present."], lists
```

CodeRabbit suggested changing the no-active-lock case to
`manual_review_required`. That suggestion conflicts with the current tested
behavior in
`packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py`,
which explicitly asserts that required specialist obligations still produce a
`passing` selected-lock reconciliation result when no active lock exists.

The existing behavior is therefore intentional in the current codebase. The
Rabbit finding should be rejected for this patch. Changing it would be a
behavior change, not a narrow review cleanup.

### Unknown Layer Error Path Is Valid

`packages/verification-core/src/vgo_verify/test_baseline_audit.py` validates
unknown layer IDs in `build_run_layer_command()` and `select_layer_files()`, but
`run_layer()` still accesses `layer_by_id(policy)[layer_id]` directly when
`collected_nodes is None`:

```python
selected_files: list[str] = []
if collected_nodes is not None:
    selected_files = select_layer_files(collected_nodes, repo_root, policy, layer_id)
layer = layer_by_id(policy)[layer_id]
```

In that direct-call path, an unknown `layer_id` raises a raw `KeyError` instead
of the structured `PolicyError` used elsewhere in the module. The CLI path does
not currently hit this bug because `main()` validates earlier, but the
programmatic `run_layer()` surface still has the gap.

This Rabbit finding is valid and can be fixed with a narrow guard in
`run_layer()`.

## Design

Use the minimal-fix path.

### Runtime Delivery Acceptance

Do not change `_evaluate_selected_lock_reconciliation()` in this patch. The
current no-active-lock behavior is already covered by tests and should stay
stable. This thread should be resolved by code-review reasoning, not by a code
change that widens scope.

### Baseline Audit Guard

Update `run_layer()` in
`packages/verification-core/src/vgo_verify/test_baseline_audit.py` to validate
`layer_id` before any direct dictionary access. The narrow form is:

```python
layers = layer_by_id(policy)
if layer_id not in layers:
    raise PolicyError(f"Unknown layer id: {layer_id}")
```

Then reuse `layers[layer_id]` instead of recomputing the mapping.

This keeps `run_layer()` aligned with `build_run_layer_command()` and
`select_layer_files()` so all public call paths raise `PolicyError` for an
unknown layer ID.

## Tests

Add a focused regression test in
`tests/runtime_neutral/test_test_baseline_audit.py` that calls
`audit.run_layer()` directly with:

- a valid `repo_root`
- a valid `policy`
- an invalid `layer_id`
- `collected_nodes=None`

The test must assert `PolicyError("Unknown layer id: ...")`.

Do not change the selected-lock reconciliation tests in this patch. Their
current assertions are part of the reason the first Rabbit suggestion is being
rejected.

## Validation

After implementation, run:

1. `pytest tests/runtime_neutral/test_test_baseline_audit.py -q`
2. `pytest packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py tests/runtime_neutral/test_runtime_delivery_acceptance.py -q`
3. `git diff --check`
4. GitHub PR thread query for PR 228 to confirm the two current unresolved
   threads are closed or outdated.
5. `gh pr checks 228 --repo foryourhealth111-pixel/Vibe-Skills` after the branch
   update.

## Non-Goals

- Do not change selected-lock reconciliation semantics for the no-active-lock
  case.
- Do not broaden the patch to new Rabbit nitpicks outside these two threads.
- Do not refactor the baseline audit CLI beyond the unknown-layer guard in
  `run_layer()`.
