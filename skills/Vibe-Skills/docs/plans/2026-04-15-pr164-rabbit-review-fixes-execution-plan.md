# PR164 Rabbit Review Fixes Execution Plan

## Execution Summary

Freeze the confirmed PR `#164` review defects, write failing regression coverage for them, implement the minimal lifecycle and doctor fixes, rerun the focused verification slice, and update the PR branch plus review threads.

## Frozen Inputs

- Requirement doc: `docs/requirements/2026-04-15-pr164-rabbit-review-fixes.md`
- PR: `#164`
- Base branch: `main`
- Head branch: `feat/host-global-bootstrap-pr`
- Review source: unresolved CodeRabbit review comments on PR `#164`

## Specialist Recommendation

- `receiving-code-review`: applicable and used as bounded review specialist assistance for validating external review findings
- no separate GitHub review-bot specialist exists in the current skill set
- dispatch mode: native fallback for git/GitHub MCP operations

## Internal Grade Decision

`L`

The work is tightly coupled and sequence-sensitive: confirm defects, add failing tests, implement minimal fixes, verify, then update the PR.

## Step Plan

1. Freeze governed requirement and plan artifacts for this repair run.
2. Add failing regression tests for the confirmed defects:
   - literal end-marker text must not corrupt parsing
   - host bootstrap receipts must stay surface-scoped
   - pre-existing empty instruction files must survive uninstall
   - uninstall receipts must classify file-preserved removal as mutation
   - bootstrap doctor must report `missing_receipt` without depending on a healthy host closure
3. Implement the minimal production fixes in:
   - `packages/installer-core/src/vgo_installer/global_instruction_merge.py`
   - `packages/installer-core/src/vgo_installer/global_instruction_service.py`
   - `packages/installer-core/src/vgo_installer/uninstall_service.py`
   - `packages/verification-core/src/vgo_verify/bootstrap_doctor_runtime.py`
   - `packages/verification-core/src/vgo_verify/bootstrap_doctor_support.py`
4. Rerun the focused verification slice and `git diff --check`.
5. Update the PR branch and reply to the relevant CodeRabbit threads with technical resolution notes.

## TDD Plan

- Red first in the relevant unit/runtime-neutral tests
- confirm the new tests fail for the expected reason
- implement the smallest behavior changes needed to turn them green
- avoid unrelated refactors during the green phase

## Verification Commands

- `python3 -m pytest tests/unit/test_global_instruction_merge.py tests/runtime_neutral/test_global_instruction_bootstrap_runtime.py tests/runtime_neutral/test_bootstrap_doctor.py tests/runtime_neutral/test_installed_runtime_uninstall.py tests/runtime_neutral/test_claude_preview_scaffold.py tests/runtime_neutral/test_opencode_managed_preview.py tests/integration/test_host_global_bootstrap_shell_lifecycle.py -q`
- `git diff --check`

## Rollback Rules

- if a new regression test does not fail first, fix the test before changing production code
- if a proposed fix requires broad redesign beyond the confirmed defect, stop and narrow the change
- do not resolve review threads until the fresh verification slice passes

## Phase Cleanup Expectations

- leave behind only the new requirement/plan artifacts, regression tests, production fixes, and truthful PR-thread replies
- do not leave temporary repro files in the repository
