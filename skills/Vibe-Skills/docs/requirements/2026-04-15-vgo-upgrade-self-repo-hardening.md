# Vgo Upgrade Self Repo Hardening Requirement

## Summary

Repair the shared Vibe-Skills upgrade path so it can always resolve the official self-repository metadata needed for upstream refresh, and prevent failed refresh attempts from polluting the installed upgrade-status state.

## Goal

Make `vgo upgrade` trustworthy for already-installed users by fixing the runtime's own upgrade metadata source and by ensuring failed upstream refreshes do not leave behind misleading or unusable upgrade state.

## Deliverable

A bounded hardening change that:

- restores authoritative `official_self_repo` metadata in `config/version-governance.json`
- makes repo metadata resolution safe even when governance data is partially populated
- avoids persisting broken `repo_remote` and `repo_default_branch` values before upstream refresh succeeds
- proves the behavior with focused unit and runtime-neutral tests

## Constraints

- canonical governed runtime authority remains `vibe`
- the fix must target the shared upgrader path, not just a one-off recovery script
- do not rely on manual fallback copying as the primary success path
- do not overwrite unrelated user state under target roots
- do not regress the existing successful install and upgrade reminder flows
- keep the change narrowly scoped to upgrade metadata resolution and status persistence hardening

## Acceptance Criteria

- `config/version-governance.json` declares `source_of_truth.official_self_repo.repo_url`
- `config/version-governance.json` declares `source_of_truth.official_self_repo.default_branch`
- `get_official_self_repo_metadata()` returns the official repo URL and default branch for the real repository config
- `refresh_upstream_status()` can refresh from official upstream metadata without requiring previously persisted non-empty `repo_remote`
- if upstream refresh fails, `.vibeskills/upgrade-status.json` is not rewritten with empty `repo_remote` or `repo_default_branch`
- `upgrade_runtime()` still no-ops cleanly when already current and still runs reset, reinstall, and check when an update is available

## Product Acceptance Criteria

- an already-installed user can upgrade from the official repo checkout without hitting `git fetch '' main`
- `upgrade-status.json` remains a truthful cache of the last known-good install/upstream state, not a record of partial failed attempts
- future releases cannot omit `official_self_repo` metadata without a red test

## User-Visible Behavior

- successful upgrades continue to report exact before/after version and commit evidence
- failed upstream refreshes still fail closed, but they no longer corrupt the recorded repo remote or branch
- the official repository metadata is now encoded directly in release governance and can be audited in-repo

## Manual Spot Checks

- run the focused repo and upgrade unit tests and confirm the new contract passes
- run the runtime-neutral slice that asserts install-generated `upgrade-status.json` contains `main` and an official repo URL
- inspect `config/version-governance.json` and confirm `official_self_repo` matches the official GitHub repository and default branch

## Completion Language Policy

Do not claim this hardening is complete until the shared upgrader tests and the runtime-neutral `upgrade-status` check both pass from the patched repository state.

## Delivery Truth Contract

This work is successful only if all of the following are true at the same time:

- the repo can self-describe its official upstream remote and default branch
- the shared upgrader can use that metadata without depending on stale installed status
- failed refresh attempts do not write misleading empty upstream metadata into installed state
- targeted tests prove both the bug fix and the future-release guardrail

## Specialist Recommendation

- no dedicated release-engineering or upgrader specialist skill is available in the current skill set
- fallback: native bounded implementation under canonical `vibe`
- dispatch mode: native fallback, no second runtime

## Artifact Review Requirements

- review the metadata source of truth and confirm it points to the official repository only
- review the upgrade-status persistence boundary and confirm writes happen only after validated data is available
- review the new tests and confirm they would fail if `official_self_repo` were removed again

## Code Task TDD Evidence Requirements

- add a red test proving the live repo config exposes official self-repo metadata
- add a red test proving failed upstream refresh does not persist an empty remote or branch
- add a red test proving refresh can derive missing persisted metadata from repo governance when needed

## Code Task TDD Exceptions

No code-task TDD exceptions were frozen for this run.

## Non-Goals

- redesigning the full release process
- adding a new recovery UI or interactive upgrader wizard
- changing host bootstrap or router governance behavior
- supporting arbitrary non-official upgrade remotes in this change

## Autonomy Mode

Interactive governed execution with serial native implementation in an isolated git worktree.

## Assumptions

- the official repository remains `https://github.com/foryourhealth111-pixel/Vibe-Skills.git`
- the official default branch remains `main`
- the broken upgrade behavior is in shared Python upgrade code, not only in a single host wrapper

## Evidence Inputs

- `apps/vgo-cli/src/vgo_cli/repo.py`
- `apps/vgo-cli/src/vgo_cli/upgrade_service.py`
- `apps/vgo-cli/src/vgo_cli/install_support.py`
- `apps/vgo-cli/src/vgo_cli/upgrade_state.py`
- `config/version-governance.json`
- `tests/unit/test_vgo_cli_repo.py`
- `tests/unit/test_vgo_cli_upgrade_service.py`
- `tests/runtime_neutral/test_installed_runtime_scripts.py`
