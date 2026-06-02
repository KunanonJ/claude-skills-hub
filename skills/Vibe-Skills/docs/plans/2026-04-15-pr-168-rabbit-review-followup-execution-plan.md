# PR 168 Rabbit Review Follow-Up Execution Plan

## Execution Summary
Governed plan for closing the validated PR `#168` review defects, tightening nearby contracts, and restacking the branch onto current `main`.

## Frozen Inputs
- Requirement doc: `docs/requirements/2026-04-15-pr-168-rabbit-review-followup.md`
- Source task: strictly self-review PR `#168`, repair the Rabbit findings, and fix the PR so gate review can proceed cleanly

## Primary Objective
Remove the validated Rabbit review defects and stale-base ancestry from PR `#168` while preserving the approved issue `#167` payload repair.

## Validation Material Role
Focused unit tests, issue `#167` lifecycle tests, governed doc portability checks, and the final branch ancestry against `origin/main` are the proof bundle for this run.

## Intended Scope
- `apps/vgo-cli/src/vgo_cli/external.py`
- `apps/vgo-cli/src/vgo_cli/repo.py`
- issue `#167` install and uninstall runtime-surface tests
- directly related test helpers
- governed docs touched by this PR
- git history restack for this branch only

## Internal Grade Decision
- Grade: L
- Reason: this is a serial, bounded repair lane with shared context and one final ancestry rewrite step.

## Wave Plan
- Wave 1: freeze this requirement and plan, inspect current local and remote PR state, and confirm each review item against code reality.
- Wave 2: add or sharpen failing tests for the runtime hardening defects and prepare the shared surface fixture change.
- Wave 3: implement the bounded code, test, and doc fixes.
- Wave 4: run targeted verification for units, lifecycle coverage, and regression diagnostics.
- Wave 5: rebase the branch onto current `origin/main`, rerun a confidence slice if needed, then update the remote PR branch.

## Delivery Acceptance Plan
- Accept the code repair only when the focused verification slice is green.
- Accept the PR repair only when the rebased branch is the remote PR head and the stale-base ancestry is gone.
- If remote update is blocked, stop short of claiming full closure.

## Artifact Review Strategy
- Review runtime behavior first: timeout parsing and git capture timeout.
- Review contract coverage second: shared issue `#167` surfaces across install and uninstall tests.
- Review diagnostic and docs cleanups third: assertion message quality and portable paths.
- Review history last: ensure the final diff is based on current `origin/main`.

## Code Task TDD Evidence Plan
- Red phase 1: add a focused test for malformed `VGO_OPTIONAL_INSTALL_TIMEOUT_SECONDS`.
- Red phase 2: add a focused test for `_run_git_capture()` timeout handling.
- Red phase 3: use existing issue `#167` lifecycle tests plus the shared-surface helper to expose the missing payload surface coverage.
- Green phase: implement only what is required to satisfy those failures.

## Ownership Boundaries
- Keep all writes inside the checked-out worktree for branch `fix/issue-167-installed-runtime-coverage`.
- Do not rewrite any branch other than `fix/issue-167-installed-runtime-coverage`.
- Do not disturb unrelated files that are not part of this PR repair.

## Verification Commands
- `python3 -m pytest tests/unit/test_vgo_cli_external.py tests/unit/test_vgo_cli_repo.py -q`
- `python3 -m pytest tests/runtime_neutral/test_installed_runtime_scripts.py tests/runtime_neutral/test_installed_runtime_uninstall.py -q`
- `python3 -m pytest tests/integration/test_runtime_payload_dependency_coverage.py -q`
- `git diff --check`
- `git merge-base HEAD origin/main`
- `git log --oneline --decorate --max-count=6`

## Rollback Plan
- If a repair path proves incorrect, revert only the files changed in this follow-up and keep the prior issue `#167` work intact.
- If the rebase introduces unexpected conflicts or regressions, stop, inspect, and replay only the intended commits rather than force-resetting unrelated work.

## Phase Cleanup Contract
- Leave behind this requirement doc, this execution plan, fresh verification outputs, and the final rebased diff.
- Do not close out the run until local evidence and remote PR state match.
