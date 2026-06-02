# Rabbit Latest Three Comments Design

## Context

PR 228 has three unresolved CodeRabbit inline threads after the previous
follow-up patch. The branch is `review/pr226-pr227-combined`.

This design covers only the currently unresolved actionable threads:

1. A stale lock-loader snippet in the original specialist execution lock plan.
2. A stale installer-helper finding in the previous follow-up design.
3. Missing selected-lock mismatch detail in runtime delivery `residual_risks`.

## Verified Findings

### Stale Lock Loader Plan Snippet

`docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md`
still documents `_load_skill_execution_lock()` and
`_load_specialist_lock_resolution()` returning the first dictionary they see,
including empty dictionaries. Current runtime code now treats empty dictionaries
as absent payloads by requiring `isinstance(payload, dict) and payload` before
returning.

The Rabbit finding is valid as a documentation consistency issue. The running
implementation already uses the corrected non-empty-dictionary behavior.

### Stale Installer Helper Design Finding

`docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md`
states that `scripts/install/Install-VgoAdapter.ps1` defines
`Test-VgoSkillEntryPoint` and recommends removing it. Current repository state
shows no such function in `scripts/install/Install-VgoAdapter.ps1`; repository
search finds the name only in prior spec/plan documentation.

The Rabbit finding is valid. The design document should record that the
installer-helper finding no longer applies to current code and that no installer
code change is required for that item.

### Selected Lock Missing Residual Risk

`packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`
already exposes selected-lock mismatches through
`truth_results["selected_lock_reconciliation_truth"]["details"]` and the
top-level `selected_lock_reconciliation` field. However, `residual_risks` only
includes specialist lock `failed`, `unresolved`, and `deferred` buckets. It does
not include `selected_lock_lists["missing"]`.

The Rabbit finding is valid as a runtime report clarity issue. If
`selected_lock_reconciliation_truth` is the only non-passing layer, the report
can require manual review without a readable residual-risk item naming the
selected or approved skills missing from the active lock.

## Design

Use the minimal-fix path.

### Documentation Updates

Update the stale lock-loader snippet in
`docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md` so the
documented code matches the current runtime behavior:

- `manifest_lock` returns only when it is a non-empty dictionary.
- `accounting_lock` returns only when it is a non-empty dictionary.
- `packet_lock` returns only when it is a non-empty dictionary.
- `manifest_resolution` returns only when it is a non-empty dictionary.
- `accounting_resolution` returns only when it is a non-empty dictionary.

Update
`docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md` to
replace the obsolete remove-helper design with the current-state conclusion:

- `Test-VgoSkillEntryPoint` is not present in the installer script.
- The installer-helper finding is no longer applicable to current code.
- No installer code change is required for that item.

### Runtime Report Update

In
`packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`,
append a residual risk when selected or approved specialist obligations are
missing from the active execution lock:

```python
if selected_lock_lists["missing"]:
    residual_risks.append(
        "Selected/approved specialist execution was not locked for: "
        + ", ".join(selected_lock_lists["missing"])
        + "."
    )
```

Place this near the existing specialist lock residual-risk block so lock-related
reporting stays grouped. Do not change gate result calculation, truth-layer
states, or the `selected_lock_reconciliation` details payload.

## Tests

Add a focused assertion to the existing selected-lock reconciliation integration
test in
`packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py`.
The scenario already creates an active lock for `latex-submission-pipeline` while
selected or approved routing also requires `literature-review`. The test should
continue to assert:

- `gate_result == "MANUAL_REVIEW_REQUIRED"`
- `completion_language_allowed is False`
- `selected_lock_reconciliation_truth.state == "manual_review_required"`
- `selected_lock_reconciliation.missing == ["literature-review"]`

Add one assertion that `report["residual_risks"]` includes:

```text
Selected/approved specialist execution was not locked for: literature-review.
```

## Validation

After implementation, run:

1. `pytest packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py -q`
2. `pytest tests/runtime_neutral/test_runtime_delivery_acceptance.py packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py -q`
3. `git diff --check`
4. GitHub PR thread query for PR 228 to confirm unresolved threads are reduced.
5. `gh pr checks 228 --repo foryourhealth111-pixel/Vibe-Skills` after the branch
   update.

## Non-Goals

- Do not broaden cleanup to historical, already-resolved Rabbit threads.
- Do not rewrite all prior specs or implementation plans.
- Do not refactor lock reconciliation architecture.
- Do not change installer code for `Test-VgoSkillEntryPoint`, because current
  code no longer contains that function.
