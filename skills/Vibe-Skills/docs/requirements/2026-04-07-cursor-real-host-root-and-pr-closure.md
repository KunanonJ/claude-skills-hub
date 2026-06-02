# Cursor Real Host Root And PR Closure

## Goal

Close the remaining default-root mismatch by moving `cursor` to the real host root by default, then package the full host-root convergence work into a reviewable pull request.

## Deliverable

- `cursor` defaults to the real host root `~/.cursor`
- runtime fallback matches that default
- public docs no longer present `~/.vibeskills/targets/cursor` as the default path
- the resulting change set is committed and opened as a pull request

## Constraints

- Preserve existing work already staged in the current branch.
- Keep Cursor host-managed boundaries explicit.
- Do not claim repo ownership of broader Cursor-native extension/config surfaces beyond the documented managed settings surface.

## Acceptance Criteria

- registry, SDK, installer, and runtime fallback resolve `cursor` to `~/.cursor` by default
- regression tests pass
- public docs align with the new `cursor` default
- branch is committed and a PR is opened against the repository

## Product Acceptance Criteria

- Installing for Cursor should land under the real host root by default so skills/commands/settings surfaces live where the host expects them.
- Public docs must still state that broader Cursor-native behavior remains host-managed.

## Manual Spot Checks

- inspect Cursor host-profile and settings-map
- verify registry and runtime fallback code paths
- verify PR branch diff only includes intended host-root convergence changes

## Completion Language Policy

- no completion claim without fresh verification and a created PR
- distinguish code changes from PR publication

## Delivery Truth Contract

- report the commit and PR identifiers
- report the exact verification commands run

## Non-Goals

- redesign Cursor capability boundaries
- modify unrelated install surfaces

## Autonomy Mode

- governed single-lane execution ending in a concrete PR

## Inferred Assumptions

- “收口” means finishing the remaining host-root inconsistency and shipping the branch for review.
