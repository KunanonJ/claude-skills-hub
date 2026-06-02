# Multi-Host Real Host Root Defaults

## Goal

Change the public multi-host installation defaults so `claude-code`, `windsurf`, `openclaw`, and `opencode` default to their real host roots instead of isolated fallback directories.

## Deliverable

- Registry defaults point the four requested hosts at their real host roots.
- Runtime fallback resolution uses the same real host roots.
- Targeted tests prove the new defaults.
- Public install documentation no longer describes isolated fallback directories as the default path for those four hosts.

## Constraints

- Preserve existing user changes already present in the worktree.
- Do not silently widen repo ownership beyond what each host profile actually supports.
- For `opencode`, keep the real `opencode.json` host-managed unless existing implementation explicitly supports writing it.

## Acceptance Criteria

- `claude-code` defaults to `~/.claude`
- `windsurf` defaults to `~/.codeium/windsurf`
- `openclaw` defaults to `~/.openclaw`
- `opencode` defaults to `~/.config/opencode`
- runtime fallback behavior matches registry behavior for the same hosts
- targeted verification passes
- public docs reflect the new defaults truthfully

## Product Acceptance Criteria

- Default install behavior should place skills / commands / sidecars under the real host roots for the requested hosts unless the operator explicitly overrides the target root.
- Public wording should no longer imply isolated fallback roots are the normal default path for those hosts.

## Manual Spot Checks

- Inspect host-profile and settings-map files for the four hosts.
- Verify installer/runtime fallback code paths.
- Re-run targeted unit/runtime/doc tests after the change.

## Completion Language Policy

- No completion claim without passing test evidence.
- Distinguish verified default-root changes from remaining host-managed surfaces.

## Delivery Truth Contract

- Report exact files changed.
- Report exact commands run.
- State any remaining host-managed limitations explicitly.

## Non-Goals

- Rebaseline `cursor` in the same change.
- Force repo ownership of host-managed provider credentials or plugin provisioning.
- Make unsupported host-managed config surfaces writable if they are explicitly out of scope.

## Autonomy Mode

- Single-session governed execution with targeted TDD and verification.

## Inferred Assumptions

- The user wants “usable by default in the real host” to win over isolated fallback convenience.
- Installing into the real host root is acceptable for preview/runtime-core hosts as long as host-managed boundaries remain explicit.
