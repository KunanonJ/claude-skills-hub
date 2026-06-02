# PR 119 Fix Pass Execution Plan

Date: 2026-04-05
Run ID: 20260405-pr119-fix-pass
Internal grade: L
Runtime lane: root_governed

## Wave Structure

1. Red: tighten tests for workflow empty-target guard, non-mutating hygiene setup, and full canonical target coverage
2. Green: implement the smallest workflow and test-setup changes needed to satisfy those tests
3. Verify: run focused tests, then broader gate-parity validation, then repo hygiene checks
4. Closeout: clean temporary artifacts, commit, push, and update the existing PR branch

## Ownership Boundaries

- Root lane owns requirement, plan, receipts, code edits, verification, and PR update
- No child-governed lanes planned because the write surface is small and tightly coupled
- No specialist dispatch unless verification exposes a blocking subsystem

## Verification Commands

- `python3 -B -m pytest -q tests/runtime_neutral/test_python_validation_contract.py`
- `python3 -B -m pytest -q tests/runtime_neutral/test_apps_surface_hygiene.py`
- `python3 -B -m pytest -q tests/contract/test_repo_layout_contract.py tests/integration/test_runtime_surface_contract_cutover.py tests/runtime_neutral/test_custom_admission_bridge.py tests/runtime_neutral/test_docs_readme_encoding.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_install_profile_differentiation.py tests/runtime_neutral/test_python_validation_contract.py`
- `git diff --check`

## Delivery Acceptance Plan

- Final branch update may be claimed only after fresh verification output is inspected
- Any unresolved review item must be reported explicitly instead of implied fixed
- Existing PR #119 should be updated in place rather than opening a duplicate PR

## Completion Language Rules

- Say fixed only for issues with passing verification evidence
- Describe unverified risks as risks, not resolved defects

## Rollback Rules

- If broader verification reveals unrelated regressions, revert only the minimal local fix set
- Do not revert unrelated user or branch changes

## Phase Cleanup Expectations

- Remove temporary local artifacts created during verification
- Audit repo-scoped node processes and avoid killing unrelated workloads
- Leave governance receipts for this run under `outputs/runtime/vibe-sessions/20260405-pr119-fix-pass/`
