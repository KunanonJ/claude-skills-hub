# PR153 Rabbit Review Fixes

## Goal

Close the real review gaps on PR #153 with evidence-backed fixes, not cosmetic churn.

## Deliverable

- verify every unresolved Rabbit finding against the current `release/v3.0.2` branch state
- repair confirmed defects in code, config, and release/governance surfaces
- add regression coverage for any production-script bug that can break maintained-branch release flow
- rerun the relevant verification stack and push the updated PR head

## Constraints

- treat external review as suggestions to validate, not instructions to follow blindly
- do not change behavior for comments that are false positives or that only propose subjective wording churn
- use TDD for any `scripts/**` behavior fix: write the failing test first, watch it fail, then implement the minimal repair
- do not revert unrelated release work already present on `release/v3.0.2`

## Acceptance Criteria

- `release-cut.ps1` no longer assumes `sync-bundled-vibe.ps1` declares every preview/apply convenience parameter
- the `wave64-82` planning board contains readable UTF-8 `primary_goal` values instead of question-mark corruption
- release/governance evidence surfaces no longer ship placeholders or missing declared assets where the PR claims a governed release is complete
- targeted verification passes after the fixes
- the repaired branch is pushed to the PR head branch

## Product Acceptance Criteria

- a maintained branch with an older or slimmer `sync-bundled-vibe.ps1` contract can still complete release preview/apply instead of crashing on unknown parameters
- governance boards and manifests remain auditable because declared assets and planning goals are readable and internally consistent
- release readers do not encounter TODO-like placeholders in the published release evidence path

## Manual Spot Checks

- inspect the `release-cut.ps1` sync invocation path to confirm parameter guards are explicit and readable
- inspect `config/wave64-82-planning-board.json` to confirm every repaired `primary_goal` aligns with the formal Wave64-82 execution plan
- inspect the final diff to confirm false-positive Rabbit suggestions were intentionally left untouched

## Completion Language Policy

- do not claim the PR is fixed until the new regression test fails first, passes after the repair, the broader verification commands pass, and the branch update is pushed

## Delivery Truth Contract

- report which Rabbit findings were confirmed versus rejected
- report the exact verification commands run and whether they passed
- report the final pushed commit SHA for the updated PR branch

## Non-Goals

- rewriting historical governance language solely for stylistic consistency
- normalizing every `Agent-S` display-name reference to `agent-s` where the repository intentionally uses the upstream display name
- refactoring duplicate helper logic in gate scripts unless it blocks a confirmed defect

## Autonomy Mode

- governed XL floor with local execution: audit first, then bounded repairs, then verification and push

## Inferred Assumptions

- the user wants PR #153 repaired in place on `release/v3.0.2`, not replaced with a new PR
- Rabbit's high-signal findings should be fixed, while false positives should be documented as rejected rather than implemented
- release/governance documents committed by this PR are allowed to change if they materially improve release truth and auditability
