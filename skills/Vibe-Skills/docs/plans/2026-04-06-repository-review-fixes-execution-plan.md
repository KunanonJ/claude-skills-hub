# Repository Review Fixes Execution Plan

Date: 2026-04-06
Run ID: 20260406-repository-review-fixes
Internal grade: L
Runtime lane: root_governed

## Scope

Implement and verify the three confirmed fixes from the repository review: safe PowerShell help paths, updated governed runtime golden fixture, and a widened canonical Python validation target list for that golden test.

## Serial Execution Units

1. Freeze requirement and runtime receipts for the repair pass
2. Add failing tests for PowerShell help-path behavior and CI validation target expectations
3. Implement safe help handling in `install.ps1` and `check.ps1`
4. Update the governed runtime golden fixture and canonical Python validation target list
5. Run focused verification for the new help-path behavior, the golden test, and the validation contract
6. Emit phase and cleanup receipts

## Ownership Boundaries

- Root lane owns all edits, receipts, and final reporting
- No child-governed lanes planned
- No specialist dispatch planned

## Verification Commands

- `python3 -B -m pytest -q tests/runtime_neutral/test_powershell_entrypoint_help.py`
- `python3 -B -m pytest -q tests/runtime_neutral/test_runtime_contract_goldens.py`
- `python3 -B -m pytest -q tests/runtime_neutral/test_python_validation_contract.py`
- `python3 -B -m pytest -q tests/integration/test_pwsh_wrapper_contract.py`

## Delivery Acceptance Plan

- Help-path tests must prove `-?` exits cleanly without executing install/check flows
- The golden test must pass without fixture drift
- The validation contract must assert the widened target list and pass

## Completion Language Rules

- "Fixed" only for the three reviewed issues
- No repo-wide green claim

## Rollback Rules

- If help-path changes alter non-help wrapper behavior, revert to the prior wrapper flow and isolate help handling
- If the golden fixture update reveals a deeper packet contract mismatch, stop after aligning the test and inspect the runtime packet separately

## Phase Cleanup Expectations

- Leave only intentional code, test, and governed artifact changes
- No lingering temp roots or background processes
