# Broader Regression Follow-Up After Issue 167 Execution Plan

## Execution Summary
Governed follow-up plan for the four broader-regression failures exposed by the wider post-issue-167 test sweep.

## Frozen Inputs
- Requirement doc: `docs/requirements/2026-04-15-broader-regression-followup-after-issue-167.md`
- Source task: continue and fix the remaining 4 broader-regression failures

## Anti-Proxy-Goal-Drift Controls

Prefill from the frozen requirement doc where available. Only diverge with explicit justification.

### Primary Objective
Repair the four broader-regression failures discovered after the issue-167 fix while keeping the issue-167 payload repair intact.

### Non-Objective Proxy Signals
- only local reproduction notes
- one of four tests fixed
- side effects that make tests pass by weakening coverage

### Validation Material Role
The four failing tests plus the preserved issue-167 targeted slice are the validation boundary for this run.

### Declared Tier
Tier B

### Intended Scope
Deep installed check, OpenClaw installed bootstrap, PowerShell install without Python on PATH, and upgrade sidecar metadata generation.

### Abstraction Layer Target
Installed-runtime shell entrypoints, bootstrap discovery, installer metadata generation, and bounded runtime verification behavior.

### Completion State Target
full

### Generalization Evidence Plan
- reproduce the four failures fresh
- fix by root-cause cluster
- rerun the four-test slice and the issue-167 targeted slice

## Internal Grade Decision
- Grade: L
- Reason: the task spans multiple files but remains a serial debugging and repair lane with shared context.

## Wave Plan
- Wave 1: freeze docs and inspect the three likely root-cause clusters.
- Wave 2: confirm whether existing tests are already sufficient red-phase evidence; add focused tests only if required.
- Wave 3: implement minimal fixes for each validated root cause.
- Wave 4: rerun the four-test slice, then rerun the issue-167 targeted slice to protect the earlier fix.

## Delivery Acceptance Plan
- Accept this follow-up only when the four named tests pass and the issue-167 targeted slice remains green.
- Treat unrelated failing tests outside this boundary as out of scope unless the new changes cause them.

## Artifact Review Strategy
- Review changes by cluster:
- deep installed check gate coverage
- installed OpenClaw bootstrap discovery
- upgrade metadata and gitless install behavior

## Code Task TDD Evidence Plan
- Use the reproduced four-test failure slice as the red phase.
- If current failures are too indirect, add minimal sharper tests first.
- After implementation, rerun the same four tests and then the issue-167 targeted slice.

## Baseline Document Quality Mapping
No baseline document quality dimensions were frozen for this run.

## Baseline UI Quality Mapping
No baseline UI quality dimensions were frozen for this run.

## Task-Specific Acceptance Mapping
- Confirm each code edit maps to one of the three validated root-cause clusters.
- Avoid mixing unrelated cleanup into the fix.

## Research Augmentation Plan
- Reuse the reproduced failure outputs from the broader post-issue-167 sweep.
- Compare failing code paths with nearby working installed-runtime flows in the same codebase.

## Completion Language Rules
- Do not claim the broader regression follow-up is complete until the four-test slice and the issue-167 slice both pass fresh.

## Ownership Boundaries
- Keep all writes inside the existing worktree branch.
- Do not disturb the main dirty workspace.

## Verification Commands
- `python3 -m pytest tests/runtime_neutral/test_installed_runtime_scripts.py::InstalledRuntimeScriptsTests::test_installed_check_sh_deep_does_not_reference_unbound_runtime_target_rel tests/runtime_neutral/test_installed_runtime_scripts.py::InstalledRuntimeScriptsTests::test_installed_runtime_bootstrap_supports_openclaw_without_self_deleting_source tests/runtime_neutral/test_installed_runtime_scripts.py::InstalledRuntimeScriptsTests::test_powershell_install_succeeds_without_python_on_path tests/runtime_neutral/test_installed_runtime_scripts.py::InstalledRuntimeScriptsTests::test_shell_install_writes_upgrade_status_sidecar -q`
- `python3 -m pytest tests/runtime_neutral/test_bundled_runtime_mirror.py tests/runtime_neutral/test_governed_runtime_bridge.py::GovernedRuntimeBridgeTests::test_version_governance_bridges_governed_runtime_surfaces tests/integration/test_runtime_config_manifest_roles.py tests/integration/test_runtime_script_manifest_roles.py tests/integration/test_version_governance_runtime_roles.py tests/integration/test_runtime_payload_dependency_coverage.py tests/runtime_neutral/test_installed_runtime_scripts.py::InstalledRuntimeScriptsTests::test_shell_install_materializes_issue_167_governed_runtime_dependency_surfaces tests/runtime_neutral/test_installed_runtime_scripts.py::InstalledRuntimeScriptsTests::test_shell_reinstall_restores_issue_167_governed_runtime_dependency_surfaces tests/runtime_neutral/test_installed_runtime_uninstall.py::InstalledRuntimeUninstallTests::test_codex_uninstall_removes_issue_167_governed_runtime_dependency_surfaces -q`

## Rollback Plan
- Revert only the follow-up changes if they do not resolve the four failures.
- Preserve the issue-167 manifest repair unless a new regression directly disproves it.

## Phase Cleanup Contract
- Leave behind this requirement doc, this plan, the final diff, and fresh verification evidence for both the four-test slice and the preserved issue-167 slice.
