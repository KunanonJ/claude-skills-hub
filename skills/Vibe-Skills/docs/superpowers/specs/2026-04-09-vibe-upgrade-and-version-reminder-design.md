# Vibe Upgrade Skill And Version Reminder Design

## Summary
Add a user-facing `vibe-upgrade` entry to the `vibe` wrapper family and back it with a real upgrade flow in `vgo-cli`.

The new flow upgrades an already-installed Vibe-Skills runtime for a supported host to the latest state of the official repository default branch, then re-runs install/bootstrap and validation for that host.

Also add a lightweight version detector for canonical `vibe` so sessions can warn when the local installation is behind the upstream default branch. The detector must use a 24-hour cache and must not become a blocking startup gate.

## Problem
The current product surface gives users install, bootstrap, and check entrypoints, but not a first-class upgrade entry.

That creates several problems:

- users must know the repository location and upgrade steps manually
- upgrade behavior is not standardized across hosts
- there is no built-in way for `vibe` to say "your local runtime is behind upstream"
- users can remain on stale local installs without a clear recovery path

The desired product model is:

- the user sees an upgrade-oriented `vibe` family entry in the visible skill list
- calling that entry upgrades the local installation for a supported host
- canonical `vibe` can warn when an update exists without becoming noisy or blocking

## Goals
- Add a `vibe-upgrade` user entry to the visible `vibe` family.
- Keep `vibe` as the only canonical governed runtime authority.
- Provide one shared upgrade implementation instead of host-specific upgrade scripts.
- Upgrade only from the official repository default branch.
- Support only known hosts already recognized by the adapter registry.
- Reuse existing host resolution, target-root resolution, install/bootstrap, and check contracts.
- Add a 24-hour cached version detector that lets canonical `vibe` emit a short update reminder.

## Non-Goals
- Do not support arbitrary remotes, arbitrary branches, tags, or commit pins.
- Do not support upgrading arbitrary filesystem paths outside known host target-root contracts.
- Do not create a second governed runtime.
- Do not add interactive upgrade prompts before every `vibe` session.
- Do not preserve local modifications inside the Vibe-Skills repository as part of this user flow.
- Do not redesign the install, bootstrap, or check contracts in this turn.

## User Contract

### 1. Visible Upgrade Entry
The `vibe` family gains a new user-facing wrapper entry:

- `vibe-upgrade`

This wrapper is a thin intent surface, not a second runtime authority. Its purpose is to express:

- upgrade my local Vibe-Skills installation
- target a supported host
- use the official repository default branch only

### 2. Upgrade Behavior
Calling the upgrade flow should perform this closed loop:

1. Resolve the requested host and target root.
2. Resolve local installed version state for that target root.
3. Consult cached upstream version state.
4. Refresh upstream state only if the cache is older than 24 hours.
5. If local and upstream are already aligned, report that status and exit cleanly.
6. If local is behind upstream:
   - fetch the official repository default branch
   - update the local repository checkout to that latest default-branch state
   - re-run the supported install/bootstrap path for the requested host
   - run the supported check path
   - write refreshed version state into the install sidecar
   - print an upgrade summary

### 3. Reminder Behavior
Canonical `vibe` checks version state during startup:

- use cached state if the last upstream check is still fresh
- refresh upstream state only when the cache age exceeds 24 hours
- if an update is available, print one short reminder line
- never block or fail session startup because of version-check refresh problems

The reminder is advisory only.

## Design Options Considered

### Option A: Wrapper skill only, manual commands underneath
Add `vibe-upgrade` as a documentation wrapper that tells the user what to run manually.

Pros:

- very small implementation
- almost no runtime risk

Cons:

- does not satisfy the requirement for quick local upgrade
- keeps upgrade knowledge in user space instead of product behavior

### Option B: Wrapper skill plus shared `vgo-cli upgrade`
Add `vibe-upgrade` as the user entry and implement real upgrade behavior once in `vgo-cli`.

Pros:

- matches the existing shared installer architecture
- keeps host resolution and post-install verification centralized
- allows the same backend to serve future wrapper or CLI entrypoints

Cons:

- requires new version-state and remote-check components

### Option C: Host-specific upgrade logic in wrapper scripts
Teach each shell/PowerShell/bootstrap entrypoint to upgrade itself independently.

Pros:

- can reuse some existing host-specific scripts quickly

Cons:

- duplicates logic
- drifts across shell and PowerShell surfaces
- increases verification burden

## Decision
Choose **Option B**.

`vibe-upgrade` becomes a thin user-facing wrapper, while the real upgrade operation lives in a shared `vgo-cli upgrade` command and supporting library code.

## Architecture

### 1. Wrapper Layer
`vibe-upgrade` belongs to the same wrapper family as:

- `vibe`
- `vibe-what-do-i-want`
- `vibe-how-do-we-do`
- `vibe-do-it`

This wrapper must:

- express upgrade intent only
- delegate into the canonical product entry surface
- avoid defining a second runtime authority

Initial visibility scope:

- host-visible wrapper skill surface for Codex full-profile installs, matching the existing wrapper-skill family model

### 2. CLI Upgrade Layer
Add `upgrade` to `vgo-cli`.

Minimum arguments:

- `--repo-root`
- `--frontend`
- `--profile`
- `--host`
- `--target-root`
- `--skip-runtime-freshness-gate` if needed for parity with install flows

Behavior:

- normalize host id
- resolve target root
- validate host/root intent
- consult version state
- update repository checkout to the official default branch latest state
- re-run install or bootstrap postconditions through shared code
- run check
- print a concise outcome summary

The upgrade command must not invent a parallel install pathway. It should reuse the current install/bootstrap/check contracts wherever possible.

### 3. Version State Layer
Store version state per install root in:

`<target-root>/.vibeskills/upgrade-status.json`

Required fields:

- `host_id`
- `target_root`
- `repo_remote`
- `repo_default_branch`
- `installed_version`
- `installed_commit`
- `installed_recorded_at`
- `remote_latest_commit`
- `remote_latest_version`
- `remote_latest_checked_at`
- `update_available`

The file is authoritative for reminder decisions and upgrade reporting for that install root.

### 4. Upstream Query Layer
Implement a small service that:

- knows the official repository remote
- knows how to resolve the default branch
- knows how to read the latest upstream commit and, when available, release/version metadata
- enforces the 24-hour cache TTL

This service should be used by both:

- `vgo-cli upgrade`
- canonical `vibe` reminder checks

### 5. Reminder Hook Layer
Canonical `vibe` startup consults the version service before normal runtime execution:

- no confirmation UI
- no extra startup workflow branch
- no failure if remote refresh cannot be completed

If `update_available = true`, print one short line and continue.

## Data And State Rules

### Cache TTL
- Fixed TTL: 24 hours
- If `remote_latest_checked_at` is newer than 24 hours ago, do not query the network
- If older, attempt refresh

### Refresh Failure
If remote refresh fails:

- keep existing cached upstream data
- do not fail `vibe` startup
- do not mark the install broken solely because of network unavailability

### Installed Version Source
Installed version should be derived from current authoritative installation metadata, preferably from the installed governance/release metadata plus the repository commit used for the current install record.

### Multi-Host Isolation
Upgrade state must remain scoped per target root so one host installation does not overwrite another host's upgrade cache or installed-version record.

## UX Contract

### Upgrade Success Output
The upgrade flow should report:

- host
- target root
- local version before upgrade
- upstream version after refresh
- final installed version after re-install
- check result

### Upgrade No-Op Output
If already current, output one short success-status message and exit without reinstalling.

### Reminder Output
Reminder format should stay to one line, for example:

`[INFO] Vibe-Skills update available: local=3.0.1@abc123 latest=3.0.2@def456. Run vibe-upgrade for host codex.`

This keeps the reminder visible but not noisy.

## Safety And Scope Rules
- Only the official repository remote is allowed.
- Only the repository default branch is allowed.
- Only supported hosts from the adapter registry are allowed.
- Upgrade is overwrite-oriented by design for this user-facing flow.
- Upgrade must not delete user files outside managed install surfaces.
- Upgrade must fail clearly if fetch, reset/update, reinstall, or check fails.
- `vibe` reminder checks must degrade to warning-free continuation on remote refresh errors.

## Testing Strategy

### Contract Tests
- `vgo-cli` parser exposes `upgrade`
- wrapper-skill packaging includes `vibe-upgrade` in the visible family

### Unit Tests
- version cache TTL logic
- remote refresh bypass when cache is fresh
- remote refresh performed when cache is stale
- upgrade-status serialization and merge behavior
- reminder rendering when update is available

### Runtime-Neutral Tests
- upgrade flow resolves known host and target root correctly
- no-op upgrade when installed state already matches upstream
- successful upgrade path refreshes sidecar state and triggers install/check
- failed upstream refresh does not block `vibe` startup reminder path

### Integration Tests
- Codex full-profile install materializes `vibe-upgrade`
- canonical `vibe` emits a short reminder when cached state says update is available
- wrapper family remains thin and does not introduce a second runtime authority

## Rollout Notes
- This feature should be introduced as a bounded extension of the existing wrapper-skill work.
- The upgrade backend should be added before or alongside the new visible `vibe-upgrade` wrapper so the user-facing entry is never a dead surface.
- Reminder rollout should begin as advisory only.

## Open Questions
None. The current design is intentionally narrowed to:

- official remote only
- default branch only
- known hosts only
- 24-hour cache only
- advisory reminder only
