# Vibe Upgrade And Version Reminder Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a visible `vibe-upgrade` entry plus a real shared upgrade flow and a 24-hour cached update reminder for canonical `vibe`.

**Architecture:** Keep `vibe-upgrade` as a thin wrapper surface and place all real upgrade behavior in `vgo-cli`. Persist per-install upgrade state under `.vibeskills/upgrade-status.json`, refresh upstream state only when the cache is stale, and let canonical `vibe` emit a single advisory reminder line without creating a second startup surface.

**Tech Stack:** Python `vgo-cli`, PowerShell runtime entrypoint, installer-core materialization/uninstall services, JSON sidecar state, pytest/unittest runtime-neutral tests

---

## Chunk 1: Repo Truth And Visible Wrapper Surface

### Task 1: Freeze official self-repo upgrade metadata

**Files:**
- Modify: `config/version-governance.json`
- Modify: `tests/unit/test_vgo_cli_repo.py`
- Modify: `tests/integration/test_version_governance_runtime_roles.py`

- [ ] Add an explicit self-repo upgrade source block under `source_of_truth` or an adjacent governance-owned field that names:
  - official repo URL
  - official default branch
  - canonical local root
- [ ] Write a unit test in `tests/unit/test_vgo_cli_repo.py` proving the repo helper returns the explicit official repo metadata instead of guessing `origin/main`.
- [ ] Run the focused repo-metadata tests and confirm they fail before implementation.
  Run: `python3 -m pytest -q tests/unit/test_vgo_cli_repo.py tests/integration/test_version_governance_runtime_roles.py`
  Expected: failure because the new governance-backed metadata helper and assertions do not exist yet.
- [ ] Implement the minimal governance metadata helper in `apps/vgo-cli/src/vgo_cli/repo.py`.
- [ ] Re-run the focused repo-metadata tests and confirm they pass.
- [ ] Commit.

```bash
git add config/version-governance.json apps/vgo-cli/src/vgo_cli/repo.py tests/unit/test_vgo_cli_repo.py tests/integration/test_version_governance_runtime_roles.py
git commit -m "feat: add official repo metadata for upgrade checks"
```

### Task 2: Add `vibe-upgrade` to the visible wrapper family

**Files:**
- Create: `bundled/skills/vibe-upgrade/SKILL.md`
- Modify: `config/skills-lock.json`
- Modify: `config/runtime-core-packaging.json`
- Modify: `config/runtime-core-packaging.full.json`
- Modify: `packages/installer-core/src/vgo_installer/materializer.py`
- Modify: `packages/installer-core/src/vgo_installer/uninstall_service.py`
- Modify: `tests/contract/test_repo_layout_contract.py`
- Modify: `tests/integration/test_runtime_core_packaging_roles.py`
- Modify: `tests/integration/test_dist_manifest_surface_roles.py`
- Modify: `tests/runtime_neutral/test_install_profile_differentiation.py`
- Modify: `tests/runtime_neutral/test_installed_runtime_scripts.py`

- [ ] Create `bundled/skills/vibe-upgrade/SKILL.md` as a thin wrapper that:
  - states upgrade intent only
  - delegates to canonical product entry behavior
  - forbids second runtime authority
- [ ] Add `vibe-upgrade` to the same Codex full-profile wrapper packaging lists that already carry `vibe-what-do-i-want`, `vibe-how-do-we-do`, and `vibe-do-it`.
- [ ] Extend `materializer.py` and `uninstall_service.py` so install/uninstall treat `skills/vibe-upgrade` like the other visible wrapper skills.
- [ ] Add a contract test proving `bundled/skills/vibe-upgrade/SKILL.md` exists.
- [ ] Add/install/runtime assertions that Codex full-profile installs materialize `skills/vibe-upgrade/SKILL.md`.
- [ ] Run the wrapper-surface test slice and confirm it fails before implementation.
  Run: `python3 -m pytest -q tests/contract/test_repo_layout_contract.py tests/integration/test_runtime_core_packaging_roles.py tests/integration/test_dist_manifest_surface_roles.py tests/runtime_neutral/test_install_profile_differentiation.py tests/runtime_neutral/test_installed_runtime_scripts.py -k 'vibe_upgrade or vibe-upgrade or wrapper'`
  Expected: failure because `vibe-upgrade` is absent from repo layout, packaging, and installed skill surfaces.
- [ ] Implement the minimal packaging/materialization updates.
- [ ] Re-run the wrapper-surface test slice and confirm it passes.
- [ ] Commit.

```bash
git add bundled/skills/vibe-upgrade/SKILL.md config/skills-lock.json config/runtime-core-packaging.json config/runtime-core-packaging.full.json packages/installer-core/src/vgo_installer/materializer.py packages/installer-core/src/vgo_installer/uninstall_service.py tests/contract/test_repo_layout_contract.py tests/integration/test_runtime_core_packaging_roles.py tests/integration/test_dist_manifest_surface_roles.py tests/runtime_neutral/test_install_profile_differentiation.py tests/runtime_neutral/test_installed_runtime_scripts.py
git commit -m "feat: project vibe-upgrade into codex wrapper surface"
```

## Chunk 2: Shared Upgrade State And CLI Backend

### Task 3: Add upgrade-state persistence and cache rules

**Files:**
- Create: `apps/vgo-cli/src/vgo_cli/upgrade_state.py`
- Modify: `apps/vgo-cli/src/vgo_cli/repo.py`
- Modify: `apps/vgo-cli/src/vgo_cli/install_support.py`
- Modify: `tests/unit/test_vgo_cli_repo.py`
- Create: `tests/unit/test_vgo_cli_upgrade_state.py`

- [ ] Create `upgrade_state.py` with focused helpers to:
  - resolve `<target-root>/.vibeskills/upgrade-status.json`
  - load/save JSON state
  - decide whether the 24-hour upstream cache is stale
  - merge installed-version and upstream-version observations
- [ ] Extend `repo.py` with helpers that read:
  - official repo metadata from governance
  - local release metadata from `config/version-governance.json`
  - local commit SHA from the canonical repo checkout
- [ ] Update `install_support.py` so every successful install refreshes installed-version fields in `upgrade-status.json`, even before the upgrade command exists.
- [ ] Add unit tests covering:
  - first-write sidecar creation
  - 24-hour cache fresh/stale boundaries
  - preservation of cached upstream data when only installed-version fields change
- [ ] Run the upgrade-state unit slice and confirm it fails before implementation.
  Run: `python3 -m pytest -q tests/unit/test_vgo_cli_repo.py tests/unit/test_vgo_cli_upgrade_state.py`
  Expected: failure because `upgrade_state.py` and new repo helpers do not exist.
- [ ] Implement the minimal sidecar persistence and cache helpers.
- [ ] Re-run the upgrade-state unit slice and confirm it passes.
- [ ] Commit.

```bash
git add apps/vgo-cli/src/vgo_cli/upgrade_state.py apps/vgo-cli/src/vgo_cli/repo.py apps/vgo-cli/src/vgo_cli/install_support.py tests/unit/test_vgo_cli_repo.py tests/unit/test_vgo_cli_upgrade_state.py
git commit -m "feat: persist upgrade status for installed runtimes"
```

### Task 4: Add `vgo-cli upgrade`

**Files:**
- Modify: `apps/vgo-cli/src/vgo_cli/main.py`
- Modify: `apps/vgo-cli/src/vgo_cli/commands.py`
- Create: `apps/vgo-cli/src/vgo_cli/upgrade_service.py`
- Modify: `apps/vgo-cli/src/vgo_cli/process.py`
- Modify: `tests/unit/test_vgo_cli_commands.py`
- Create: `tests/unit/test_vgo_cli_upgrade_service.py`

- [ ] Add an `upgrade` subcommand to `main.py` with the same host/profile/frontend argument shape as `install`.
- [ ] Add `upgrade_command(args)` in `commands.py` that:
  - normalizes host
  - resolves target root
  - consults `upgrade_state`
  - delegates actual work to `upgrade_service`
- [ ] Implement `upgrade_service.py` with focused helpers for:
  - no-op when local install already matches cached/fresh upstream state
  - refreshing upstream state when cache is stale
  - fetching/resetting the canonical repo checkout to the official default branch latest commit
  - re-running shared install/bootstrap postconditions
  - running `check`
  - printing concise upgrade output
- [ ] Add unit tests for:
  - parser exposure of `upgrade`
  - no-op behavior when already current
  - refresh path when cache is stale
  - failure propagation if repo refresh or check fails
- [ ] Run the upgrade-command unit slice and confirm it fails before implementation.
  Run: `python3 -m pytest -q tests/unit/test_vgo_cli_commands.py tests/unit/test_vgo_cli_upgrade_service.py`
  Expected: failure because the `upgrade` subcommand, service, and tests do not yet exist.
- [ ] Implement the minimal CLI/service wiring.
- [ ] Re-run the upgrade-command unit slice and confirm it passes.
- [ ] Commit.

```bash
git add apps/vgo-cli/src/vgo_cli/main.py apps/vgo-cli/src/vgo_cli/commands.py apps/vgo-cli/src/vgo_cli/upgrade_service.py apps/vgo-cli/src/vgo_cli/process.py tests/unit/test_vgo_cli_commands.py tests/unit/test_vgo_cli_upgrade_service.py
git commit -m "feat: add shared vgo-cli upgrade command"
```

## Chunk 3: Canonical `vibe` Reminder Hook

### Task 5: Emit a cached upgrade reminder from the runtime entrypoint

**Files:**
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Create: `apps/vgo-cli/src/vgo_cli/version_reminder.py`
- Modify: `config/version-governance.json`
- Modify: `tests/runtime_neutral/test_governed_runtime_bridge.py`
- Create: `tests/runtime_neutral/test_vibe_upgrade_reminder.py`
- Modify: `tests/unit/test_vgo_cli_upgrade_state.py`

- [ ] Add a tiny reminder bridge in Python or PowerShell that:
  - reads `upgrade-status.json`
  - refreshes upstream state only if the cache is stale
  - returns either “no reminder” or one advisory line
- [ ] Call that bridge near the top of `scripts/runtime/invoke-vibe-runtime.ps1`, before stage execution starts, without changing runtime authority or startup branching.
- [ ] Add runtime-neutral tests covering:
  - stale cache refresh path
  - fresh cache no-network path
  - advisory one-line output when `update_available = true`
  - no hard failure when upstream refresh errors
- [ ] Run the reminder test slice and confirm it fails before implementation.
  Run: `python3 -m pytest -q tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_vibe_upgrade_reminder.py`
  Expected: failure because no reminder hook or reminder bridge exists yet.
- [ ] Implement the minimal reminder hook.
- [ ] Re-run the reminder test slice and confirm it passes.
- [ ] Commit.

```bash
git add scripts/runtime/invoke-vibe-runtime.ps1 scripts/runtime/VibeRuntime.Common.ps1 apps/vgo-cli/src/vgo_cli/version_reminder.py config/version-governance.json tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_vibe_upgrade_reminder.py tests/unit/test_vgo_cli_upgrade_state.py
git commit -m "feat: warn when upstream vibe update is available"
```

## Chunk 4: End-To-End Upgrade Verification

### Task 6: Prove install, upgrade, and reminder work together

**Files:**
- Modify: `tests/runtime_neutral/test_installed_runtime_scripts.py`
- Modify: `tests/runtime_neutral/test_mcp_auto_provision.py`
- Modify: `tests/unit/test_vgo_cli_commands.py`
- Inspect: `docs/superpowers/specs/2026-04-09-vibe-upgrade-and-version-reminder-design.md`

- [ ] Add or extend runtime-neutral tests to simulate:
  - an installed host with stale cached upstream state
  - a no-op upgrade when already current
  - an actual upgrade that rewrites `upgrade-status.json`
  - a post-upgrade `check` run
- [ ] Keep the end-to-end tests network-free by stubbing the upstream query and repo refresh steps.
- [ ] Run the focused end-to-end slice and confirm it fails before the final integration changes.
  Run: `python3 -m pytest -q tests/runtime_neutral/test_installed_runtime_scripts.py tests/unit/test_vgo_cli_commands.py -k 'upgrade or reminder'`
  Expected: failure until the end-to-end upgrade and reminder wiring is complete.
- [ ] Implement the remaining glue code and test doubles needed to make the slice pass.
- [ ] Run the end-to-end slice again and confirm it passes.
- [ ] Commit.

```bash
git add tests/runtime_neutral/test_installed_runtime_scripts.py tests/runtime_neutral/test_mcp_auto_provision.py tests/unit/test_vgo_cli_commands.py
git commit -m "test: cover vibe upgrade and reminder flow"
```

## Chunk 5: Final Verification And Delivery

### Task 7: Run the full targeted verification bundle

**Files:**
- Inspect: all files touched in Chunks 1-4

- [ ] Run the complete targeted verification bundle.

```bash
python3 -m pytest -q \
  tests/unit/test_vgo_cli_repo.py \
  tests/unit/test_vgo_cli_upgrade_state.py \
  tests/unit/test_vgo_cli_upgrade_service.py \
  tests/unit/test_vgo_cli_commands.py \
  tests/contract/test_repo_layout_contract.py \
  tests/integration/test_runtime_core_packaging_roles.py \
  tests/integration/test_dist_manifest_surface_roles.py \
  tests/integration/test_version_governance_runtime_roles.py \
  tests/runtime_neutral/test_install_profile_differentiation.py \
  tests/runtime_neutral/test_installed_runtime_scripts.py \
  tests/runtime_neutral/test_governed_runtime_bridge.py \
  tests/runtime_neutral/test_vibe_upgrade_reminder.py
```

- [ ] Read the full output and confirm there are zero failures.
- [ ] Inspect `git diff --stat` and confirm the change set remains within:
  - wrapper surface
  - upgrade CLI/backend
  - version sidecar/cache
  - runtime reminder
  - related tests
- [ ] If verification is green, create the final integration commit.

```bash
git add bundled/skills/vibe-upgrade/SKILL.md config/version-governance.json config/skills-lock.json config/runtime-core-packaging.json config/runtime-core-packaging.full.json apps/vgo-cli/src/vgo_cli/main.py apps/vgo-cli/src/vgo_cli/commands.py apps/vgo-cli/src/vgo_cli/repo.py apps/vgo-cli/src/vgo_cli/process.py apps/vgo-cli/src/vgo_cli/install_support.py apps/vgo-cli/src/vgo_cli/upgrade_state.py apps/vgo-cli/src/vgo_cli/upgrade_service.py apps/vgo-cli/src/vgo_cli/version_reminder.py packages/installer-core/src/vgo_installer/materializer.py packages/installer-core/src/vgo_installer/uninstall_service.py scripts/runtime/invoke-vibe-runtime.ps1 scripts/runtime/VibeRuntime.Common.ps1 tests/unit/test_vgo_cli_repo.py tests/unit/test_vgo_cli_upgrade_state.py tests/unit/test_vgo_cli_upgrade_service.py tests/unit/test_vgo_cli_commands.py tests/contract/test_repo_layout_contract.py tests/integration/test_runtime_core_packaging_roles.py tests/integration/test_dist_manifest_surface_roles.py tests/integration/test_version_governance_runtime_roles.py tests/runtime_neutral/test_install_profile_differentiation.py tests/runtime_neutral/test_installed_runtime_scripts.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_vibe_upgrade_reminder.py
git commit -m "feat: add vibe upgrade flow and version reminder"
```

- [ ] Summarize any residual risks separately from verified behavior.

