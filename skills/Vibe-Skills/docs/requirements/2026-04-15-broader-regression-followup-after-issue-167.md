# Broader Regression Follow-Up After Issue 167

## Summary
Repair the four broader-regression failures discovered after the issue #167 payload-coverage fix without reopening the already-fixed issue-167 scope.

## Goal
Restore broader installed-runtime regression coverage by fixing the remaining failures in deep shell check, OpenClaw one-shot bootstrap, PowerShell install without Python on PATH, and upgrade status metadata generation.

## Deliverable
A bounded change set that addresses the validated root causes behind the four failing tests, preserves the issue-167 payload fix, and proves the repairs with targeted automated verification.

## Constraints
- Keep canonical `vibe` governance with a single requirement and plan surface for this follow-up run.
- Do not revert or disturb the already-implemented issue-167 manifest and test changes.
- Treat the four failures as follow-up regression work, not as justification to widen the earlier payload-repair scope.
- Fix only validated root causes.
- Prefer the smallest code change that resolves each failure cluster.

## Acceptance Criteria
- `test_installed_check_sh_deep_does_not_reference_unbound_runtime_target_rel` passes.
- `test_installed_runtime_bootstrap_supports_openclaw_without_self_deleting_source` passes.
- `test_powershell_install_succeeds_without_python_on_path` passes.
- `test_shell_install_writes_upgrade_status_sidecar` passes with stable branch metadata expectations.
- The previously passing issue-167 targeted verification slice remains green after the follow-up fixes.

## Product Acceptance Criteria
- Installed `check.sh --deep` no longer fails because a required deep-check gate is absent from the installed runtime contract.
- Installed OpenClaw bootstrap can resolve its runtime entry surface from an installed runtime root without requiring a canonical repo layout.
- PowerShell install remains functional when Python is unavailable on PATH and does not fail merely because `git` is missing.
- Upgrade status sidecar records coherent metadata instead of empty default-branch values.

## Manual Spot Checks
No manual spot checks were frozen for this run if the targeted automated regression slice passes.

## Completion Language Policy
- Report this follow-up as complete only if the four failing tests are green and the issue-167 targeted slice still passes.
- If any one of the four remains failing, report partial status and name the unresolved cluster explicitly.

## Delivery Truth Contract
- Governance truth: this follow-up remains traceable to its own requirement and plan docs.
- Engineering truth: the previously failing tests must be rerun fresh and pass after implementation.
- Workflow truth: follow-up fixes must not regress the issue-167 runtime-payload contract.
- Product truth: installed runtime flows behave correctly in the scenarios encoded by the four failing tests.

## Artifact Review Requirements
- Review the fixes by root-cause cluster rather than by file count.
- Confirm no new payload widening is introduced unless a failing test proves it is required.

## Code Task TDD Evidence Requirements
- Use the four existing failing tests as the red phase evidence.
- If a failure needs a sharper reproduction, add a focused test before changing production code.
- After implementation, rerun the four-test slice and the issue-167 targeted slice.

## Code Task TDD Exceptions
No code-task TDD exceptions were frozen for this run.

## Baseline Document Quality Dimensions
No baseline document quality dimensions were frozen for this run.

## Baseline UI Quality Dimensions
No baseline UI quality dimensions were frozen for this run.

## Task-Specific Acceptance Extensions
- Group failures by validated shared root cause before editing code.
- Prefer code-path hardening over test relaxation.
- If one failure proves to be environment-only rather than product behavior, record that explicitly and fix the environment assumption at source.

## Research Augmentation Sources
- `tests/runtime_neutral/test_installed_runtime_scripts.py`
- `check.sh`
- `scripts/bootstrap/one-shot-setup.sh`
- `packages/installer-core/src/vgo_installer/*`
- `apps/vgo-cli/src/vgo_cli/*`
- `packages/contracts/src/vgo_contracts/*`

> Fill the anti-drift fields once here. Downstream governed plan and completion surfaces should reuse them rather than restate them.

## Primary Objective
Repair the four broader-regression failures discovered after the issue-167 fix while keeping the issue-167 payload repair intact.

## Non-Objective Proxy Signals
- only local reproduction notes
- one of four tests fixed
- side effects that make tests pass by weakening coverage

## Validation Material Role
The four failing tests plus the preserved issue-167 targeted slice are the authoritative validation boundary for this run.

## Anti-Proxy-Goal-Drift Tier
Tier 1 regression-closure fidelity.

## Intended Scope
Deep installed check, OpenClaw installed bootstrap, PowerShell install without Python on PATH, and upgrade sidecar metadata generation.

## Abstraction Layer Target
Installed-runtime shell entrypoints, bootstrap discovery, installer metadata generation, and bounded runtime verification behavior.

## Completion State
Complete when the four failing tests pass and the earlier issue-167 targeted slice remains green.

## Generalization Evidence Bundle
- fresh output from the four failing tests turning green
- fresh output from the issue-167 targeted slice staying green
- bounded diff showing the root-cause fixes

## Non-Goals
- Do not reopen the approved issue-167 contract design.
- Do not fix unrelated legacy failures outside the four identified tests.
- Do not rewrite installer architecture without test pressure.

## Autonomy Mode
interactive_governed

## Assumptions
- The four failures are fixable inside the existing worktree without discarding the issue-167 changes.
- At least two of the four failures share upgrade metadata or installed-runtime discovery logic, allowing bounded fixes.

## Evidence Inputs
- Source task: continue and fix the remaining 4 broader-regression failures
- Prior requirement doc: `docs/requirements/2026-04-15-vibe-issue-167-installed-runtime-dependency-coverage.md`
- Prior plan doc: `docs/plans/2026-04-15-vibe-issue-167-installed-runtime-dependency-coverage-execution-plan.md`
