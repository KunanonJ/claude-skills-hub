# PR153 Rabbit Review Fixes Execution Plan

## Execution Summary

Audit PR #153 against the actual `release/v3.0.2` branch state, reject false-positive Rabbit comments, repair the confirmed defects with TDD where behavior changes, rerun verification, and push the repaired PR head.

## Frozen Inputs

- Requirement doc: `docs/requirements/2026-04-13-pr153-rabbit-review-fixes.md`
- PR: `#153`
- Base branch: `main` at `c2f98b53890dfecb3fd6160c0e690d93f7fb5fe4`
- Head branch: `release/v3.0.2` at `235e6e1a021bfc39b0284a4636fc6c2bdb68b318`
- Review source: unresolved CodeRabbit review and thread comments on PR `#153`

## Anti-Proxy-Goal-Drift Controls

### Primary Objective

Repair real defects in the PR, not merely silence review comments.

### Non-Objective Proxy Signals

- editing every commented file regardless of whether the finding is real
- applying wording-only nits that do not improve correctness or auditability
- claiming the PR is repaired before replaying tests and verification on the repaired branch

### Validation Material Role

Regression tests, targeted gates, git diff review, and push success determine completion.

### Declared Tier

Strict

### Intended Scope

`scripts/governance/release-cut.ps1`, its tests, the reviewed governance/config artifacts, and governed runtime receipts for this repair run.

### Abstraction Layer Target

Maintained-branch release operator compatibility plus release/governance evidence integrity.

### Completion State Target

Confirmed review findings fixed, false positives explicitly rejected by omission, verification rerun, and the updated branch pushed to `origin/release/v3.0.2`.

### Generalization Evidence Plan

Capture the failing regression test, the repaired script/config/docs, verification output, and the final pushed commit SHA.

## Internal Grade Decision

XL

The user explicitly requested `--xl`. Execution will still stay local and sequence-sensitive, but the audit/fix/verify phases are separated and the review surface spans code, config, docs, and release governance artifacts.

## Wave Plan

1. Freeze governed requirement, plan, and runtime lineage artifacts for this PR repair run.
2. Validate each unresolved Rabbit finding against local branch reality and separate true defects from false positives.
3. Add a failing regression test for the confirmed `release-cut.ps1` compatibility defect.
4. Implement the minimal script fix plus the confirmed config/docs repairs.
5. Run targeted verification, then the broader verification stack, inspect the final diff, and push to `release/v3.0.2`.
6. Emit execution and cleanup receipts.

## Delivery Acceptance Plan

- The release-cut regression test must fail before the script fix and pass after it.
- `config/wave64-82-planning-board.json` must have readable `primary_goal` text for all wave entries.
- `config/wave83-100-gate-manifest.json` must declare the release-evidence contract asset it already validates.
- release/governance docs touched in this repair must not contain the known placeholder wording left by the release cut.
- `git push origin HEAD:release/v3.0.2` must succeed.

## Artifact Review Strategy

- Inspect the repaired `release-cut.ps1` invocation blocks to ensure each optional sync parameter is guarded before use.
- Inspect the repaired planning-board text against `docs/plans/2026-03-07-vco-wave64-82-execution-plan.md`.
- Inspect the final diff to confirm the rejected Rabbit path-drift comment was not implemented because the compatibility entrypoints are deliberate.

## Code Task TDD Evidence Plan

- Red: add a regression test where `sync-bundled-vibe.ps1` intentionally omits `Preview`, `PreviewOutputPath`, and `PruneBundledExtras`, then run the targeted test and confirm failure on current `release-cut.ps1`.
- Green: implement guarded sync invocation in `release-cut.ps1`.
- Verify: rerun the targeted release-cut operator tests and confirm the new regression passes.

## Baseline Document Quality Mapping

- Repair only documents that currently weaken release truth, auditability, or manifest consistency.
- Keep historical run-specific evidence paths when they are intentionally frozen artifacts; do not genericize them without cause.
- Remove placeholder release wording and garbled planning-board content where it currently degrades correctness.

## Task-Specific Acceptance Mapping

- Reject Rabbit's governance-path-drift suggestion because the repository intentionally ships compatibility entrypoints under `docs/*.md` for historical boards.
- Leave the `Agent-S` display-name wording unchanged unless changing it is required to keep related keyword checks and governance text aligned.

## Verification Commands

- `python3 -m pytest -q tests/runtime_neutral/test_release_cut_operator.py -k sync`
- `python3 -m pytest -q tests/runtime_neutral/test_release_cut_operator.py`
- `pwsh -NoProfile -File scripts/verify/vibe-wave64-82-closure-gate.ps1 -WriteArtifacts`
- `pwsh -NoProfile -File scripts/verify/vibe-release-evidence-bundle-gate.ps1 -WriteArtifacts`
- `pwsh -NoProfile -File scripts/verify/vibe-output-artifact-boundary-gate.ps1`
- `git diff --check`

## Rollback Plan

- If the new regression test does not fail for the expected reason, fix the test first before touching production code.
- If a doc/config repair breaks an existing gate, revert only that local change and re-check whether the finding was a false positive.
- If push fails, leave the branch verified locally and report the exact remote failure.

## Phase Cleanup Contract

- Write execution and cleanup receipts under `outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/`.
- Record which Rabbit findings were confirmed versus rejected in the execution receipt.
- Leave the local repair branch available for inspection after push.
