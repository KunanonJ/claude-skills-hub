# PR 168 Rabbit Review Follow-Up

## Summary
Repair the validated CodeRabbit findings on PR `#168`, tighten nearby test and document contracts, and restack the branch on the current `main` base so the PR can be reviewed and gated cleanly.

## Goal
Remove the remaining review-blocking defects and ancestry drift from PR `#168` without reopening the already-approved issue `#167` payload-scope decision.

## Deliverable
A bounded change set that:
- fixes the validated runtime hardening defects raised in review
- expands the issue `#167` install and uninstall surface contracts to the actual managed payload
- removes non-portable absolute-path references from governed docs
- improves diagnostic quality where current assertions hide missing surfaces
- rebases the branch onto current `origin/main`
- proves the result with focused automated verification

## Constraints
- Stay inside canonical `vibe` governance with this requirement doc and its paired execution plan as the only truth surfaces for this follow-up.
- Preserve the approved issue `#167` direction: installed runtime payload coverage remains broadened; do not redesign the runtime to avoid those dependencies.
- Do not revert unrelated user changes in this worktree or in other worktrees.
- Treat CodeRabbit comments as hypotheses to verify, not instructions to obey blindly.
- Keep the write scope bounded to the reviewed defects, their directly duplicated test fixtures, governed docs touched by this PR, and the branch ancestry repair.

## Acceptance Criteria
- `apps/vgo-cli/src/vgo_cli/external.py` no longer raises import-time `ValueError` when `VGO_OPTIONAL_INSTALL_TIMEOUT_SECONDS` is unset, malformed, or non-numeric.
- `apps/vgo-cli/src/vgo_cli/repo.py` bounds `git` capture calls with a timeout and degrades cleanly on `TimeoutExpired`.
- The issue `#167` installed-runtime surface contract includes `scripts/verify/vibe-bootstrap-doctor-gate.ps1`.
- The issue `#167` uninstall contract covers all managed governed protocol files tracked by the uninstall service.
- Shared issue `#167` surface definitions are centralized enough to avoid duplicate drift between install and uninstall tests.
- The governed docs changed by this PR do not embed machine-specific absolute filesystem paths.
- The runtime payload dependency coverage assertion reports which surfaces are missing when it fails.
- The branch is replayed onto current `origin/main` so PR `#168` no longer carries stale-base ancestry.

## Product Acceptance Criteria
- Malformed environment configuration cannot crash the CLI before it starts optional install handling.
- Gitless or stalled git metadata lookup still degrades to empty metadata rather than hanging.
- Install and uninstall lifecycle tests actually cover the governed payload surfaces shipped for issue `#167`.
- Review and gate tooling can reason about the PR without stale-base noise in the diff.

## Manual Spot Checks
No manual spot checks are required if the frozen automated verification slice passes and the PR diff is clean against current `main`.

## Completion Language Policy
- Report full completion only if the targeted tests pass, the rebase onto current `origin/main` is complete, and the PR branch is updated remotely.
- If code changes are complete but the remote branch update cannot be performed, report the implementation as partial and name the remaining delivery blocker.

## Delivery Truth Contract
- Governance truth: all edits trace back to this requirement doc and the paired execution plan.
- Engineering truth: each validated defect has red-phase evidence or direct code inspection evidence before implementation, and targeted verification is rerun after the fix.
- Workflow truth: local branch ancestry and remote PR state both reflect the repaired change set.
- Product truth: PR `#168` no longer contains the validated Rabbit regressions or stale-base diff pollution.

## Artifact Review Requirements
- Review the runtime hardening fixes with their focused unit tests.
- Review the issue `#167` surface inventory as a single contract shared across install and uninstall coverage.
- Review governed doc edits only for path portability, not for unrelated prose churn.
- Review the final diff against current `origin/main`, not against the stale merge base.

## Code Task TDD Evidence Requirements
- Add or extend focused tests for invalid optional-install timeout parsing and `git` capture timeout behavior before production edits.
- Use the existing install and uninstall lifecycle tests as contract tests for the issue `#167` surface inventory; sharpen them only as needed to expose the missing surfaces directly.
- Rerun the targeted verification slice after implementation.

## Task-Specific Acceptance Extensions
- Prefer sharing the issue `#167` surface tuple through a small helper module instead of keeping duplicate local constants.
- Keep timeout defaults small and deterministic enough for tests.
- Preserve current degrade-cleanly behavior for git metadata capture.

## Non-Goals
- Do not broaden the issue `#167` payload beyond the governed surfaces already required by runtime consumers and uninstall tracking.
- Do not refactor unrelated installer, bootstrap, or release flows.
- Do not claim gate success based only on local code changes without updating the PR branch.

## Autonomy Mode
interactive_governed

## Assumptions
- The four open CodeRabbit findings on PR `#168` are still unresolved at implementation start.
- The local worktree contains the intended PR content plus additional unpushed fixes.
- Updating the remote PR branch is possible through either normal git transport or the GitHub API.

## Evidence Inputs
- PR `#168`: `https://github.com/foryourhealth111-pixel/Vibe-Skills/pull/168`
- Issue `#167`: `https://github.com/foryourhealth111-pixel/Vibe-Skills/issues/167`
- Prior requirement: `docs/requirements/2026-04-15-vibe-issue-167-installed-runtime-dependency-coverage.md`
- Prior follow-up requirement: `docs/requirements/2026-04-15-broader-regression-followup-after-issue-167.md`
