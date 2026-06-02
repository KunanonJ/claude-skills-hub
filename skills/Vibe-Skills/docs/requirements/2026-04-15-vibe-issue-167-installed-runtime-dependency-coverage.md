# Vibe Issue 167 Installed Runtime Dependency Coverage

## Summary
Repair issue #167 by restoring governed runtime dependency coverage in the installed `skills/vibe` payload and proving the fix across install, update, check, and uninstall lifecycle surfaces.

## Goal
Ensure an installed `skills/vibe` runtime contains the governed files it explicitly references or transitively requires, so governed execution and verification gates do not ship in a self-inconsistent state.

## Deliverable
A repository change set that broadens the installed runtime payload to cover the missing governed dependency surfaces, updates conflicting manifest-role tests, adds dependency-coverage verification, and proves the lifecycle behavior with targeted automated checks.

## Constraints
- Follow canonical `vibe` governance and keep a single requirement and plan surface for this run.
- Do not modify or revert unrelated dirty changes in the main workspace.
- Use the isolated worktree as the only write surface for code and docs in this run.
- Keep the fix bounded to the approved Option A direction: broaden installed runtime payload coverage rather than redesign governed runtime to avoid the existing dependencies.
- Treat install, reinstall or upgrade, freshness or coherence checks, and uninstall cleanup as one lifecycle contract.

## Acceptance Criteria
- `config/version-governance.json` runtime payload installs the governed dependency surfaces required by issue #167, including `protocols`, `docs`, and `core/skill-contracts/v1/vibe.json`.
- `config/runtime-script-manifest.json` includes the governed verification gates still consumed by the installed runtime contract.
- `config/runtime-config-manifest.json` includes `config/operator-preview-contract.json`.
- Existing tests that enforced exclusion of governed dependency surfaces are updated to reflect the approved payload contract.
- At least one targeted automated test proves runtime dependency coverage from payload manifests to governed consumers rather than only manifest self-consistency.
- Targeted lifecycle verification passes for the approved issue scope.

## Product Acceptance Criteria
- A freshly materialized installed runtime can satisfy governed runtime bridge expectations without missing required governed dependency surfaces.
- Installed-runtime freshness and coherence verification remain aligned with the broadened payload contract.
- Uninstall cleanup continues to remove only installed runtime artifacts and receipts without leaving the lifecycle in a contradictory state.
- Completion wording is blocked unless the targeted verification slice passes in the clean worktree.

## Manual Spot Checks
No manual spot checks were frozen for this run if the targeted automated lifecycle slice passes.

## Completion Language Policy
- Report the task as complete only if the governed requirement and plan artifacts exist, the code and tests are updated, and the targeted verification slice passes in the isolated worktree.
- If any targeted verification is skipped or fails, report the run as partial and name the remaining risk explicitly.

## Delivery Truth Contract
- Governance truth: the implementation traces back to this requirement doc and the paired execution plan.
- Engineering truth: failing-first evidence exists before production edits, and the approved verification slice passes after implementation.
- Workflow truth: manifest, bridge, and lifecycle surfaces agree on the installed runtime contract.
- Product truth: the installed `skills/vibe` payload is no longer missing governed dependency surfaces required by governed execution and gates.

## Artifact Review Requirements
- Review the changed manifests, affected tests, and any lifecycle verification additions for consistency with the approved Option A scope.
- Confirm the fix adds only the governed surfaces required for installed runtime correctness and does not silently widen unrelated payload policy.

## Code Task TDD Evidence Requirements
- Record at least one failing-first test step that proves the pre-fix payload contract is insufficient for governed runtime dependency coverage.
- Run the targeted red tests before changing production manifests or lifecycle code.
- After implementation, rerun the targeted slice that covers runtime payload dependency coverage, manifest roles, and governed runtime bridge behavior.

## Code Task TDD Exceptions
No code-task TDD exceptions were frozen for this run.

## Baseline Document Quality Dimensions
No baseline document quality dimensions were frozen for this run.

## Baseline UI Quality Dimensions
No baseline UI quality dimensions were frozen for this run.

## Task-Specific Acceptance Extensions
- Distinguish facts about missing dependency surfaces from any optional cleanup or refactor ideas.
- Prefer manifest-only implementation if it fully satisfies lifecycle truth; change installer or verification code only if manifest expansion is insufficient.
- Preserve the existing explicit file-projection model where possible rather than replacing it with broad directory projection for scripts or config.

## Research Augmentation Sources
- GitHub issue `#167`
- `SKILL.md`
- `config/version-governance.json`
- `config/runtime-script-manifest.json`
- `config/runtime-config-manifest.json`
- `scripts/runtime/Invoke-SkeletonCheck.ps1`
- `scripts/verify/vibe-governed-runtime-contract-gate.ps1`
- `scripts/common/vibe-governance-helpers.ps1`
- `tests/runtime_neutral/test_bundled_runtime_mirror.py`
- `tests/runtime_neutral/test_governed_runtime_bridge.py`
- `tests/integration/test_runtime_config_manifest_roles.py`
- `tests/integration/test_runtime_script_manifest_roles.py`
- `tests/integration/test_version_governance_runtime_roles.py`

> Fill the anti-drift fields once here. Downstream governed plan and completion surfaces should reuse them rather than restate them.

## Primary Objective
Restore governed runtime dependency coverage in installed `skills/vibe` payloads and prove the repair across the runtime lifecycle.

## Non-Objective Proxy Signals
- manifest files updated only
- one new test added only
- CI green without lifecycle coverage

## Validation Material Role
Repository manifests, governed runtime consumers, and targeted lifecycle tests are the source of truth for this implementation run.

## Anti-Proxy-Goal-Drift Tier
Tier 1 installed-runtime contract preservation.

## Intended Scope
Installed runtime payload coverage, governed dependency surfaces, lifecycle verification alignment, and directly conflicting tests for issue #167.

## Abstraction Layer Target
Packaging manifests, governed runtime dependency contracts, and installed-runtime verification behavior.

## Completion State
Complete when the approved Option A fix is implemented, failing-first evidence is recorded, and the targeted lifecycle verification slice passes.

## Generalization Evidence Bundle
- failing-first test output for dependency coverage
- final targeted verification output for manifest roles and governed runtime bridge coverage
- diff of changed manifests and tests

## Non-Goals
- Do not redesign governed runtime to avoid these dependencies.
- Do not refactor unrelated installer or release-train behavior.
- Do not clean up unrelated dirty files in the main workspace.
- Do not widen payload policy beyond what the governed runtime currently requires for correctness.

## Autonomy Mode
interactive_governed

## Assumptions
- The approved Option A direction remains the desired fix.
- The isolated worktree shares enough toolchain state with the main clone to run the targeted pytest slice.
- Manifest expansion is likely sufficient, but lifecycle code will be updated if verification proves otherwise.

## Evidence Inputs
- Source task: fix issue #167 with full lifecycle coverage
- Prior governed analysis: `docs/requirements/2026-04-15-vibe-issue-167-installed-runtime-dependency-coverage-analysis.md`
- Prior analysis plan: `docs/plans/2026-04-15-vibe-issue-167-installed-runtime-dependency-coverage-analysis-execution-plan.md`
- GitHub issue URL: `https://github.com/foryourhealth111-pixel/Vibe-Skills/issues/167`
