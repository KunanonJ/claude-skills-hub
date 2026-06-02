# Rabbit Four Doc Comments Design

## Context

PR 228 currently has four unresolved CodeRabbit inline comments, all on
committed documentation rather than active runtime code.

These comments fall into three patterns:

1. A plan document contains an outdated PowerShell snippet that no longer
   matches the real runtime helper implementation.
2. A follow-up implementation plan still describes deleting an installer helper
   that no longer exists in the repository.
3. Several committed design docs embed the local Windows worktree absolute
   path.

The fix should stay narrow: correct only the documentation drift that is now
surfacing as unresolved review comments, and avoid unrelated runtime changes.

## Verified Findings

### 1. Strict-Mode `locked_dispatch` Comment Is Valid As A Documentation Drift Finding

`docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md` includes
an older version of the `New-VibeSkillExecutionLockProjection` snippet:

```powershell
if (Test-VibeSkillExecutionLockActive -SkillExecutionLock $previousLock) {
    foreach ($entry in @($previousLock.locked_dispatch)) {
```

Under `Set-StrictMode -Version Latest`, direct access to a missing property can
throw. CodeRabbit is therefore correct that this specific snippet is unsafe as
written.

However, the current runtime implementation in
`scripts/runtime/VibeRuntime.Common.ps1` is already guarded and no longer uses
that direct access pattern. The unresolved comment is therefore best treated as
a **plan drift** issue, not as evidence that current runtime code is still
broken.

### 2. Missing `Get-VibeSkillExecutionLockSkillIds` In The Plan Is Valid

The same plan document defines
`New-VibeSkillExecutionLockSummaryProjection` using
`Get-VibeSkillExecutionLockSkillIds`, but the helper is not defined in the
documented implementation block itself.

The helper does exist in the real runtime module
`scripts/runtime/VibeRuntime.Common.ps1`, so the problem is again plan drift:
the committed implementation plan is no longer self-contained for a reader
following it verbatim.

### 3. The `rabbit-followup-two-comments` Implementation Plan Is Internally Outdated

`docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md` still
contains Task 2 instructions to remove `Test-VgoSkillEntryPoint` from
`scripts/install/Install-VgoAdapter.ps1`.

Repository search shows that `Test-VgoSkillEntryPoint` does not exist in the
current installer code. That means the current CodeRabbit comment about the
expected `rg` output is valid, but the real issue is broader than one expected
line: the entire Task 2 still describes a deletion workflow for a symbol that
is already absent.

The correct fix is to rewrite that task into a no-op verification/doc-alignment
task rather than only editing one expectation sentence.

### 4. Local Worktree Absolute Paths In Specs Are Valid Review Findings

These committed spec documents currently embed the local Windows worktree path:

- `docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md`
- `docs/superpowers/specs/2026-05-06-rabbit-followup-three-comments-design.md`
- `docs/superpowers/specs/2026-05-06-rabbit-latest-two-comments-design.md`
- `docs/superpowers/specs/2026-05-06-rabbit-latest-three-comments-design.md`

The path adds no durable repository value and should be replaced with the branch
identifier alone.

This goes one file beyond the exact three-file set called out in the current
comment, but it is the same defect pattern and should be corrected in one pass.

## Design

Use the minimal closed-loop documentation fix.

### Specialist Execution Lock Plan

Update
`docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md` so the
documented helper block matches the current runtime helper shape closely enough
to remove the two unresolved review concerns:

1. Replace the unguarded `@($previousLock.locked_dispatch)` access with the
   guarded `previousDispatch` pattern already used by the real runtime file.
2. Include the `Get-VibeSkillExecutionLockSkillIds` helper in the documented
   implementation block so the plan remains self-contained.

This is a documentation synchronization change only. Do not alter
`scripts/runtime/VibeRuntime.Common.ps1` in this slice unless fresh verification
shows a real code defect, which is not the current finding.

### Follow-Up Two Comments Implementation Plan

Update
`docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md` to reflect
the already-verified current repository state:

1. Step 1 should expect zero code matches for `Test-VgoSkillEntryPoint`.
2. Task 2 should no longer instruct deletion of a nonexistent installer helper.
3. The task should instead document the no-op conclusion explicitly so the plan
   is internally consistent with its companion design document.

### Spec Path Cleanup

Remove the local absolute worktree path from all four affected spec documents
and leave only the branch identifier `review/pr226-pr227-combined`.

This keeps the edit narrowly pattern-based and avoids committing machine-local
filesystem details.

## Validation

After implementation, validate with:

1. `rg -n "Test-VgoSkillEntryPoint" scripts/install/Install-VgoAdapter.ps1 scripts tests packages -S`
   to confirm the helper is still absent from current code surfaces.
2. `rg -n "F:\\\\vibe\\\\Vibe-Skills\\\\.worktrees\\\\pr226-pr227-combined" docs/superpowers/specs`
   to confirm no committed spec retains that local path.
3. `git diff --check`
4. GitHub PR thread query for PR 228 to confirm the four current unresolved
   documentation comments are closed or outdated after the branch update.

## Non-Goals

- Do not change current runtime PowerShell implementation merely because an
  older plan snippet drifted out of date.
- Do not broaden this patch into new runtime tests unless verification uncovers
  an actual live defect.
- Do not refactor unrelated historical docs outside the small set implicated by
  the current unresolved threads.
