# Vibe Issue 167 Installed Runtime Dependency Coverage Execution Plan

## Execution Summary
Governed implementation plan for repairing issue #167 in an isolated worktree using failing-first tests and targeted lifecycle verification.

## Frozen Inputs
- Requirement doc: `docs/requirements/2026-04-15-vibe-issue-167-installed-runtime-dependency-coverage.md`
- Source task: fix issue #167 with full lifecycle coverage
- Approved direction: Option A, broaden installed runtime payload coverage

## Anti-Proxy-Goal-Drift Controls

Prefill from the frozen requirement doc where available. Only diverge with explicit justification.

### Primary Objective
Restore governed runtime dependency coverage in installed `skills/vibe` payloads and prove the repair across the runtime lifecycle.

### Non-Objective Proxy Signals
- manifest files updated only
- one new test added only
- CI green without lifecycle coverage

### Validation Material Role
Repository manifests, governed runtime consumers, and targeted lifecycle tests are the source of truth for this run.

### Declared Tier
Tier B

### Intended Scope
Installed runtime payload coverage, governed dependency surfaces, lifecycle verification alignment, and directly conflicting tests for issue #167.

### Abstraction Layer Target
Packaging manifests, governed runtime dependency contracts, and installed-runtime verification behavior.

### Completion State Target
full

### Generalization Evidence Plan
- capture a red test proving missing dependency coverage
- capture green verification for the targeted manifest and lifecycle slice
- keep the diff bounded to manifests, affected tests, and any strictly necessary lifecycle code

## Internal Grade Decision
- Grade: L
- Reason: the task spans several related surfaces but stays bounded enough for serial native execution without parallel delegation.

## Wave Plan
- Wave 1: confirm clean worktree state, freeze governed docs, and inspect runtime dependency consumers and conflicting tests.
- Wave 2: write failing tests for governed dependency coverage and lifecycle contract alignment.
- Wave 3: implement the minimal fix across manifests and any required lifecycle code.
- Wave 4: run the targeted verification slice, inspect results, and leave a clear proof bundle for closeout.

## Delivery Acceptance Plan
- Treat the issue as fixed only when payload projection, governed runtime bridge expectations, and lifecycle checks agree.
- Use targeted pytest slices to prove the installed runtime contract instead of relying on manifest editing alone.
- Keep manual review out of the critical path unless automation leaves an unresolved gap.

## Artifact Review Strategy
- Review `config/version-governance.json`, `config/runtime-script-manifest.json`, and `config/runtime-config-manifest.json` together so payload truth and role-group truth stay aligned.
- Review changed tests for false positives, especially prior assertions that intentionally excluded `docs` and `protocols`.
- If lifecycle code changes are needed, verify they are strictly in service of the broadened payload contract.

## Code Task TDD Evidence Plan
- Start with the directly impacted test files and add a focused dependency-coverage test if the existing suite does not expose the gap clearly enough.
- Run the red test slice before any manifest edits.
- After the fix, rerun the same targeted slice plus any lifecycle-specific test added or updated during implementation.

## Baseline Document Quality Mapping
No baseline document quality dimensions were frozen for this run.

## Baseline UI Quality Mapping
No baseline UI quality dimensions were frozen for this run.

## Task-Specific Acceptance Mapping
- Map each newly included governed surface to at least one live consumer or gate.
- Keep the explicit-projection packaging style intact for scripts and config files.
- Prefer manifest changes first, then escalate to installer or verification code only if tests prove a remaining lifecycle gap.

## Research Augmentation Plan
- Reuse the prior analysis doc as background context.
- Recheck the live issue body and current worktree files before implementation so the frozen scope stays current.

## Completion Language Rules
- Do not claim the bug is fixed if the targeted red test was never observed failing.
- Do not claim full completion if any targeted verification is skipped, flaky, or left unresolved.

## Ownership Boundaries
- Only modify files in the isolated worktree branch `fix/issue-167-installed-runtime-coverage`.
- Do not touch unrelated dirty files in the main workspace.
- Keep the write scope focused on manifests, relevant tests, governed docs, and only the lifecycle code that the tests force us to touch.

## Verification Commands
- `git status --short --branch`
- `uv run --no-project --with pytest python -m pytest tests/runtime_neutral/test_bundled_runtime_mirror.py tests/runtime_neutral/test_governed_runtime_bridge.py::GovernedRuntimeBridgeTests::test_version_governance_bridges_governed_runtime_surfaces tests/integration/test_runtime_config_manifest_roles.py tests/integration/test_runtime_script_manifest_roles.py tests/integration/test_version_governance_runtime_roles.py -q`
- `uv run --no-project --with pytest python -m pytest tests/integration/test_runtime_payload_dependency_coverage.py -q`
- Add any lifecycle-specific verification command required by newly added or updated tests.

## Rollback Plan
- Revert only the files changed for this issue in the isolated worktree if the approach proves invalid.
- Do not rewrite unrelated repository history and do not touch the dirty main workspace.

## Phase Cleanup Contract
- Leave behind the requirement doc, execution plan, git diff, and verification outputs needed to justify the fix.
- Keep the worktree clean except for the intentional issue-167 changes at the end of implementation.
