# PR164 Rabbit Follow-up Fixes Execution Plan

## Execution Summary

Freeze the remaining verified PR `#164` review follow-up defects, add failing regression coverage for them, implement the smallest lifecycle and doctor fixes, rerun the focused verification slice, and update the PR branch plus review threads.

## Frozen Inputs

- Requirement doc: `docs/requirements/2026-04-15-pr164-rabbit-followup-fixes.md`
- PR: `#164`
- Base branch: `main`
- Head branch: `feat/host-global-bootstrap-pr`
- Review source: the unresolved CodeRabbit follow-up comments still open on PR `#164`

## Specialist Recommendation

- `receiving-code-review`: applicable and used as bounded review specialist assistance for validating the remaining review findings
- no separate GitHub review-bot or doc-copy specialist exists in the current skill set
- dispatch mode: native fallback for git/GitHub MCP operations and minor requirement-doc wording cleanup

## Internal Grade Decision

`L`

The remaining work is tightly coupled and sequence-sensitive: reproduce, write red tests, implement small fixes, verify, then update the PR.

## Step Plan

1. Freeze governed requirement and plan artifacts for this follow-up run.
2. Add failing regression tests for:
   - shared-root multi-host bootstrap merge/update/remove keyed by `(host_id, block_id)`
   - malformed scoped bootstrap receipt fields returning unhealthy doctor state instead of raising
3. Implement the minimal production fixes in:
   - `packages/installer-core/src/vgo_installer/global_instruction_merge.py`
   - `packages/verification-core/src/vgo_verify/bootstrap_doctor_support.py`
4. Apply the non-blocking wording fix in the new requirement artifact if convenient.
5. Rerun the focused verification slice and `git diff --check`.
6. Update the PR branch and reply to the remaining review threads with technical resolution notes.

## TDD Plan

- red first in the relevant unit/runtime-neutral tests
- confirm the new tests fail for the expected reason
- implement the smallest behavior changes needed to turn them green
- avoid unrelated refactors during the green phase

## Verification Commands

- `python3 -m pytest tests/unit/test_global_instruction_merge.py tests/runtime_neutral/test_global_instruction_bootstrap_runtime.py tests/runtime_neutral/test_bootstrap_doctor.py tests/runtime_neutral/test_installed_runtime_uninstall.py tests/runtime_neutral/test_claude_preview_scaffold.py tests/runtime_neutral/test_opencode_managed_preview.py tests/integration/test_host_global_bootstrap_shell_lifecycle.py -q`
- `git diff --check`

## Rollback Rules

- if a new regression test does not fail first, fix the test before changing production code
- if the shared-root block identity fix requires broader bootstrap migration redesign, stop and narrow the change
- do not resolve the remaining review threads until the fresh verification slice passes

## Phase Cleanup Expectations

- leave behind only the new requirement/plan artifacts, regression tests, production fixes, and truthful PR-thread replies
- do not leave temporary repro files in the repository
