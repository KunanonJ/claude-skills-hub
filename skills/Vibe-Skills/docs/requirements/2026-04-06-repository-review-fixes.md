# Repository Review Fixes Requirement

Date: 2026-04-06
Run ID: 20260406-repository-review-fixes
Mode: interactive_governed
Runtime lane: root_governed

## Goal

Fix the three concrete issues confirmed during the repository review:

- PowerShell `install.ps1` and `check.ps1` treat `-?` as a real execution path instead of a safe help path
- the governed runtime golden fixture is stale relative to current `host_closure` behavior
- the canonical Python validation target list omits the runtime contract golden test that is currently failing

## Deliverable

A narrow implementation that:

- adds a no-side-effect help path for the top-level PowerShell install and check wrappers
- updates the governed runtime golden fixture to match the current normalized packet shape
- expands the canonical Python validation target list to include the governed runtime golden contract test
- adds focused tests for the new PowerShell help behavior

## Constraints

- Keep scope limited to the three confirmed issues above
- Do not widen into installer architecture redesign or broad CI restructuring
- Preserve existing install and check behavior for non-help invocations
- Keep completion claims bounded to focused verification only

## Acceptance Criteria

- `pwsh -NoProfile -File ./install.ps1 -?` exits successfully without performing installation work
- `pwsh -NoProfile -File ./check.ps1 -?` exits successfully without running the health check
- `tests/runtime_neutral/test_runtime_contract_goldens.py` passes
- the canonical Python validation contract and target list both include the governed runtime golden test

## Product Acceptance Criteria

- Users can safely discover PowerShell wrapper usage without mutating local runtime state
- runtime contract goldens reflect the current governed runtime packet shape
- the main Python validation path is less likely to miss this specific runtime contract regression again

## Manual Spot Checks

- Confirm help output is shown for `install.ps1` and `check.ps1`
- Confirm no target root is created by help-path invocations
- Re-run the targeted runtime contract and validation tests

## Completion Language Policy

- Claim only the reviewed issues fixed by executed verification
- Do not claim repo-wide no-regression

## Delivery Truth Contract

- Implementation plus focused verification only

## Non-Goals

- Redesigning wrapper help text across every script in the repository
- Expanding the canonical Python validation surface to the full test suite
- Refactoring governed runtime packet generation logic

## Autonomy Mode

interactive_governed with inferred assumptions

## Inferred Assumptions

- The user wants the concrete regressions fixed now, not a broader cleanup
- A focused CI-target expansion is preferable to a large validation policy rewrite
