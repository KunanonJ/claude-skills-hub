# Immediate Technical Debt Audit Design

## Summary

This design defines a narrow, evidence-first technical-debt audit for
`<repo-root>`.

The user selected the immediate-fixable debt path. The audit should therefore
prioritize debt that can be fixed inside the current repository with bounded
code, config, test, or documentation changes. It should not become a broad
architecture rewrite or a historical terminology cleanup pass.

The initial exploration found that the current routing terminology gates are
green, but other practical debt remains:

- tracked runtime outputs conflict with the output artifact boundary policy;
- the test baseline audit can classify tests by risk layer, but layer execution
  still maps to broad pytest directories;
- the quality-debt overlay gate has a small working-tree side-effect risk when
  it rewrites and restores JSON policy files;
- local `main` is ahead of `origin/main` by 50 commits, so release and sync
  debt must be separated from code-quality debt;
- several critical runtime, router, and verification files are large enough to
  be recorded as maintainability debt, but they should not dominate this pass.

## Current Evidence

Repository state after exploration:

```text
## main...origin/main [ahead 50]
```

The final worktree check was clean:

```text
## main...origin/main [ahead 50]
```

Current routing debt gate:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
```

Observed summary:

```text
status = pass
P0 = 0
P1 = 0
P2 = 0
P3 = 0
```

Routing terminology hard cleanup scan:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
```

Observed summary:

```text
status = pass
fail_count = 0
review_count = 0
```

Quality debt overlay gate:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-quality-debt-overlay-gate.ps1
```

Observed result:

```text
Total assertions: 26
Passed: 26
Failed: 0
Quality debt overlay gate passed.
```

During exploration, this gate left a trailing-blank-line diff in
`config/quality-debt-overlay.json` even though the script printed that it had
restored the original content. The diff was removed before this design was
written, and `git status --short --branch` returned to clean.

Repo cleanliness gate after cleanup:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-repo-cleanliness-gate.ps1
```

Observed result:

```text
Dirty paths: 0
Repo zero-dirty          : True
```

Test baseline audit:

```powershell
python scripts\verify\test-baseline-audit.py --collect-only
```

Observed result:

```text
[INFO] total_nodes=1410 layers=4 risks=6
```

Expanded local analysis of the same baseline showed:

```text
contract_unit: 284 nodes, 45 files
runtime_neutral_fast: 523 nodes, 83 files
runtime_neutral_heavy: 413 nodes, 46 files
integration_host_boundary: 190 nodes, 61 files
```

Core contract and unit layer:

```powershell
python -m pytest tests\contract tests\unit -q
```

Observed result:

```text
284 passed in 2.34s
```

Output artifact boundary gate:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-output-artifact-boundary-gate.ps1
```

Observed failure:

```text
Tracked outputs : 9
[FAIL] [outputs] all tracked outputs are explicitly allowlisted
[FAIL] [outputs] no tracked outputs exist under disallowed generated-output roots
[FAIL] [outputs] tracked output count matches policy registry
```

The tracked generated outputs include:

```text
outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/cleanup-receipt.json
outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/governance-capsule.json
outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/intent-contract.json
outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/phase-plan-execute.json
outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/skeleton-receipt.json
outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/stage-lineage.json
outputs/skills-audit/bio-science-problem-consolidation.md
outputs/skills-audit/bio-science-problem-map.csv
outputs/skills-audit/bio-science-problem-map.json
```

The policy at `config/outputs-boundary-policy.json` declares:

```text
expected_tracked_output_count = 0
strict_requires_zero_tracked_outputs = true
```

## Goals

1. Produce a ranked, fixable technical-debt list with concrete evidence.
2. Separate blocking debt from background maintainability debt.
3. Keep the first implementation pass bounded to repository-local changes.
4. Preserve the existing green routing terminology gates.
5. Avoid deleting or rewriting generated artifacts until the migration boundary
   is explicit and verified.
6. Prevent test-baseline evidence from implying that a risk layer was executed
   when only a broad directory command was run.
7. Keep release-sync debt visible without mixing it into code-quality findings.

## Non-Goals

- Do not perform the debt fixes in this design step.
- Do not push local commits to `origin`.
- Do not deploy or install into Codex or any host root.
- Do not write to the local Codex root.
- Do not run broad, unbounded test sweeps as part of the design.
- Do not reopen current routing terminology cleanup unless a gate fails.
- Do not remove tracked outputs without a follow-up implementation plan.
- Do not split large runtime/router files in this first audit unless a blocking
  bug requires touching them.
- Do not treat historical or explicitly allowlisted legacy terms as current
  blocking debt.

## Debt Severity Model

### P0: Blocking Debt

Use `P0` for issues that currently fail a gate, break a release boundary, or
make repository state claims false.

Initial candidate:

- `vibe-output-artifact-boundary-gate.ps1` fails because tracked `outputs/**`
  files conflict with the strict output boundary policy.

### P1: Misleading Verification Debt

Use `P1` for issues where a test or audit surface exists but can mislead an
operator about what was actually verified.

Initial candidates:

- `test-baseline-audit.py` classifies `runtime_neutral_fast` and
  `runtime_neutral_heavy`, but `run_layer()` still builds pytest commands from
  broad `pytest_args`. Both runtime-neutral layers therefore point at
  `tests/runtime_neutral`, not at the classified node sets.
- `vibe-quality-debt-overlay-gate.ps1` rewrites a policy file during the gate
  and restored the semantic content, but left a trailing-blank-line diff during
  exploration. A gate that validates cleanliness-sensitive behavior should not
  leave any byte-level diff after success.

### P2: Maintainability Debt

Use `P2` for issues that increase repair cost but do not currently fail a gate.

Initial candidates:

- large PowerShell runtime/router files such as
  `scripts\runtime\VibeRuntime.Common.ps1`,
  `scripts\runtime\VibeExecution.Common.ps1`,
  `scripts\runtime\Invoke-PlanExecute.ps1`, and
  `scripts\router\modules\48-llm-acceleration-overlay.ps1`;
- large Python functions such as
  `evaluate_delivery_acceptance()`, `route_prompt()`,
  `probe_advice_connectivity()`, and `select_pack_candidate()`;
- short wave gate wrappers whose behavior depends on shared manifests and
  `scripts\common\vibe-wave-gate-runner.ps1`. These wrappers may be valid, but
  the audit should record whether their evidence is discoverable enough for a
  release operator.

### P3: Recorded But Not Scheduled

Use `P3` for debt that is historical, explicitly allowed, or outside the
immediate fixable scope.

Initial candidates:

- historical retired terminology in marked historical documents;
- known compatibility paths under `scripts/runtime/legacy` and
  `scripts/router/legacy`;
- release-sync state from local `main` being 50 commits ahead of `origin/main`.

## Audit Scope

The audit should inspect:

- `scripts/verify/**`
- `scripts/common/**`
- `config/*policy*.json`
- `config/*manifest*.json`
- `packages/verification-core/**`
- `tests/runtime_neutral/**`
- `tests/integration/**`
- `tests/unit/**`
- tracked `outputs/**`
- tracked `dist/**`
- `origin/main..main`

The audit should not inspect bundled skill content as first-class debt unless a
gate points to it. Bundled skills, vendor content, third-party content,
generated distributions, and historical proof bundles can easily dominate text
searches while not representing current repository control-plane debt.

## Proposed Audit Output

The implementation plan should create a Markdown debt register, either as a
checked-in document or generated evidence, with this shape:

```text
Debt ID
Severity
Title
Evidence command
Observed result
Affected files
Why this is debt
Recommended fix boundary
Verification after fix
Out of scope
```

The first register should include at least the initial P0 and P1 candidates
from this design. P2 items can be summarized unless they become blockers during
verification.

## Validation Strategy

Each accepted debt item must have a verification command.

For the output artifact boundary debt:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-output-artifact-boundary-gate.ps1
```

For the baseline audit execution debt:

```powershell
python scripts\verify\test-baseline-audit.py --collect-only
python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

If implementation changes layer execution, add a focused test proving that
`runtime_neutral_fast` does not execute nodes classified as
`runtime_neutral_heavy`.

For the quality-debt overlay gate side-effect debt:

```powershell
git status --short --branch
powershell -NoLogo -NoProfile -File scripts\verify\vibe-quality-debt-overlay-gate.ps1
git diff -- config/quality-debt-overlay.json
git status --short --branch
```

The expected post-gate result is no diff and a clean worktree.

For routing terminology guardrails:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
```

These must remain green if any implementation touches routing, verification, or
policy files.

## Implementation Boundaries For The Next Plan

The follow-up implementation plan should start with the P0 output artifact
boundary because it is a known failing gate. It should then address P1
verification debt in small independent patches.

The output boundary fix should choose one explicit policy direction:

1. move or remove the tracked `outputs/**` files after confirming fixture
   mirrors exist and the strict policy is correct; or
2. update the policy to allowlist the tracked outputs if strict zero-output mode
   is not yet intended.

The design preference is option 1 because the policy already says strict zero
tracked outputs. The implementation plan must still verify the fixture mirrors
before any removal.

The baseline audit fix should not create a custom pytest runner larger than the
problem requires. A focused node-list execution path, a generated file-list
selection, or an explicit `--run-classified-layer` behavior is acceptable if it
is tested and documented.

The quality-debt overlay side-effect fix should preserve the gate's behavior
while ensuring byte-for-byte restoration, preferably by avoiding persistent
writes when possible or by restoring the original bytes exactly.

## Acceptance Criteria

The design is ready for implementation planning when:

- the user accepts that the first pass is limited to immediately fixable debt;
- P0/P1/P2/P3 meanings are clear;
- the initial candidates are evidence-backed and bounded;
- the follow-up plan will not delete artifacts, change runtime behavior, or push
  commits without a specific implementation step and verification command.

After implementation, the minimum evidence should include:

- output artifact boundary gate passing or a documented decision that changes
  the policy honestly;
- test baseline audit unit tests passing;
- quality debt overlay gate leaving no worktree diff;
- repo cleanliness gate passing;
- routing terminology gates still passing if touched.
