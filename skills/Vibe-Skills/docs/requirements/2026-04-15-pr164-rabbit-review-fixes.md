# PR164 Rabbit Review Fixes

## Goal

Repair the confirmed lifecycle and doctor defects on PR `#164` without adding cosmetic churn or changing unrelated host-bootstrap behavior.

## Deliverable

- fix the confirmed bootstrap parser, receipt, uninstall, and doctor defects on `feat/host-global-bootstrap-pr`
- add regression coverage for every confirmed defect before implementation
- rerun the focused verification slice and push the repaired PR head
- reply to the review threads with evidence-backed resolution notes

## Constraints

- treat CodeRabbit comments as suggestions to verify, not instructions to implement blindly
- fix only the findings that are technically real for the current codebase
- keep canonical governed runtime authority with `vibe`
- do not widen scope into README, install-copy, or unrelated delivery-contract work
- do not regress the already-proven managed-block insertion, update, and uninstall behavior for supported hosts

## Acceptance Criteria

- managed-block parsing no longer treats literal end-marker text inside user-authored Markdown as a real terminator
- bootstrap receipts are scoped so one host bootstrap surface does not overwrite another host's receipt inside the same target root
- uninstall removes an empty host instruction file only when that file was installer-created for the managed block
- uninstall receipts distinguish real file deletion from managed-block-only mutation truthfully
- bootstrap doctor can surface `missing_receipt` even when `host-closure.json` is absent or corrupt
- focused regression coverage proves each repaired path

## Product Acceptance Criteria

- a pre-existing empty `AGENTS.md` or `CLAUDE.md` is preserved on uninstall
- a host instruction file that keeps user content after managed-block removal is reported as mutated, not deleted
- explicit bootstrap-health checks do not silently downgrade a real missing-receipt state into `not_applicable`
- lifecycle evidence remains auditable even if multiple host installs share one temp-root test target

## Manual Spot Checks

- reproduce the empty pre-existing file uninstall case and confirm the file survives
- reproduce the installer-created file plus user-tail case and confirm uninstall receipt reports mutation, not deletion
- reproduce the literal end-marker-in-code-fence case and confirm parsing stays healthy
- reproduce doctor evaluation with bootstrap target present but no host-closure and no receipt, and confirm `missing_receipt`

## Completion Language Policy

Do not claim the PR is repaired until the new regression tests fail first, pass after the fixes, the focused verification slice passes fresh, and the PR branch has been updated.

## Delivery Truth Contract

- report which CodeRabbit findings were fixed
- report which review comments were intentionally left as non-blocking nits
- report the exact verification commands and outputs used for the repaired branch
- report the updated PR head commit and thread-resolution status

## Non-Goals

- refactoring duplicate test scaffolding only for style
- renaming variables or narrowing exception types unless needed for a real fix
- broad redesign of host bootstrap governance beyond the confirmed defects

## Autonomy Mode

Interactive governed execution with local TDD-first bug-fixing, bounded to the PR `#164` review-fix scope.

## Inferred Assumptions

- the user wants PR `#164` repaired in place, not replaced with a new PR
- the clean worktree branch `feat/host-global-bootstrap-pr` remains the correct repair surface
- review-thread replies should be grounded in fresh local verification rather than generic acknowledgements
