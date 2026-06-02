# PR164 Rabbit Follow-up Fixes

## Goal

Repair the remaining technically real CodeRabbit findings on PR `#164` without widening the bootstrap lifecycle scope beyond the current shared-root and doctor contracts.

## Deliverable

- fix the remaining shared-root block identity collision in host global-instruction bootstrap handling
- make bootstrap doctor robust against malformed receipt scalar fields instead of raising
- add regression coverage for both repaired paths before implementation
- optionally clean the non-blocking requirement-document wording nit while touching the follow-up artifact set
- rerun the focused verification slice and update the existing PR head plus review threads

## Constraints

- treat external review comments as findings to verify, not instructions to copy verbatim
- keep canonical governed runtime authority with `vibe`
- do not widen this bugfix into a full migration framework for historic host-surface moves
- do not regress the already-repaired receipt scoping, uninstall truth contract, or bootstrap doctor missing-receipt behavior

## Acceptance Criteria

- shared-root installs that place multiple host bootstrap blocks in the same instruction file distinguish blocks by `(host_id, block_id)` rather than `block_id` alone
- bootstrap merge/update/remove logic no longer targets another host's block when the file and `managed_block_id` are shared
- malformed bootstrap receipt scalar values such as non-integer `template_version` do not raise from doctor inspection and instead produce an unhealthy result
- focused regression coverage proves the repaired behavior

## Product Acceptance Criteria

- installing `codex` then `opencode` into the same temp target root preserves two independent managed bootstrap blocks in `AGENTS.md`
- removing the `codex` block from a shared-root `AGENTS.md` leaves the `opencode` block intact
- doctor inspection with a malformed scoped bootstrap receipt reports a result object instead of throwing

## Manual Spot Checks

- reproduce the shared-root `codex` then `opencode` install case and confirm both bootstrap blocks remain present
- reproduce shared-root removal of one host block and confirm the sibling host block survives
- reproduce doctor inspection with `template_version: "oops"` and confirm it returns an unhealthy payload instead of raising

## Completion Language Policy

Do not claim the PR follow-up is repaired until the new regression tests fail first, pass after the fixes, the focused verification slice passes fresh, and the PR branch has been updated.

## Delivery Truth Contract

- report whether the two remaining technical CodeRabbit findings were fixed
- report whether the wording nit was fixed or intentionally left as non-blocking
- report the exact verification commands and outputs used for the updated PR head
- report the updated PR head commit and review-thread reply status

## Non-Goals

- building a generic migration system for future host bootstrap surface renames
- redesigning receipt schema beyond what is required for the defensive parse
- unrelated README or install-surface documentation cleanup

## Autonomy Mode

Interactive governed execution with local TDD-first bug-fixing, bounded to the remaining PR `#164` review follow-up scope.

## Inferred Assumptions

- the user wants the existing PR `#164` updated in place
- the shared-root multi-host lifecycle is in scope because the current PR already scopes receipts per host/surface and tests same-root host installs
- review-thread replies should clearly separate fixed defects from broader deferred design work
