# Rabbit Four Doc Comments Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the four currently unresolved PR 228 CodeRabbit documentation comments by synchronizing stale plan text, removing committed local-path leakage, and keeping runtime code unchanged.

**Architecture:** Treat this as a documentation-alignment patch, not a runtime patch. One task synchronizes the specialist-execution-lock implementation plan with the current runtime helper shape, one task rewrites the outdated no-longer-applicable installer-helper removal plan, and one task removes the local Windows worktree path from the affected spec documents.

**Tech Stack:** Markdown documentation, PowerShell snippets embedded in docs, ripgrep, GitHub CLI, git diff hygiene checks

---

## File Structure

- Modify: `docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md`
  - Sync the documented `New-VibeSkillExecutionLockProjection` snippet with the guarded `previousDispatch` pattern and include the `Get-VibeSkillExecutionLockSkillIds` helper.
- Modify: `docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md`
  - Rewrite the obsolete installer-helper removal task into a no-op verification/document-alignment task.
- Modify: `docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md`
- Modify: `docs/superpowers/specs/2026-05-06-rabbit-followup-three-comments-design.md`
- Modify: `docs/superpowers/specs/2026-05-06-rabbit-latest-two-comments-design.md`
- Modify: `docs/superpowers/specs/2026-05-06-rabbit-latest-three-comments-design.md`
  - Remove the committed absolute worktree path and leave only the branch identifier.

### Task 1: Sync The Specialist Execution Lock Plan Snippet

**Files:**
- Modify: `docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md`
- Reference: `scripts/runtime/VibeRuntime.Common.ps1`

- [ ] **Step 1: Confirm the current documentation drift**

Run:

```powershell
$plan = 'docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md'
Select-String -Path $plan -Pattern 'foreach \(\$entry in @\(\$previousLock\.locked_dispatch\)\)|function New-VibeSkillExecutionLockSummaryProjection|Get-VibeSkillExecutionLockSkillIds' |
  ForEach-Object { '{0}:{1}' -f $_.LineNumber, $_.Line }
```

Expected:

```text
570:        foreach ($entry in @($previousLock.locked_dispatch)) {
598:function New-VibeSkillExecutionLockSummaryProjection {
604:    $lockedSkillIds = if ($active) { @(Get-VibeSkillExecutionLockSkillIds -SkillExecutionLock $SkillExecutionLock) } else { @() }
```

- [ ] **Step 2: Update the documented helper block**

Replace the unguarded previous-lock dispatch loop and add the missing helper so the plan text includes these shapes:

```powershell
function Get-VibeSkillExecutionLockSkillIds {
    param(
        [AllowNull()] [object]$SkillExecutionLock = $null
    )

    if ($null -eq $SkillExecutionLock) {
        return @()
    }

    $fromIdList = if (Test-VibeObjectHasProperty -InputObject $SkillExecutionLock -PropertyName 'locked_skill_ids') {
        @(Get-VibeNormalizedStringList -Values $SkillExecutionLock.locked_skill_ids)
    } else {
        @()
    }
    $fromDispatch = if (Test-VibeObjectHasProperty -InputObject $SkillExecutionLock -PropertyName 'locked_dispatch') {
        @($SkillExecutionLock.locked_dispatch | ForEach-Object {
            if ($null -ne $_ -and (Test-VibeObjectHasProperty -InputObject $_ -PropertyName 'skill_id')) { [string]$_.skill_id } else { '' }
        } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    } else {
        @()
    }

    return @((@($fromIdList) + @($fromDispatch)) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
}
```

```powershell
$previousLock = Get-VibeSkillExecutionLockFromRuntimeInputPacket -RuntimeInputPacket $PreviousRuntimeInputPacket
if ((Test-VibeSkillExecutionLockActive -SkillExecutionLock $previousLock) -and -not $curatedOnly -and -not $explicitZeroHostApproval) {
    $previousDispatch = if (Test-VibeObjectHasProperty -InputObject $previousLock -PropertyName 'locked_dispatch') { @($previousLock.locked_dispatch) } else { @() }
    foreach ($entry in @($previousDispatch)) {
        $skillId = if (Test-VibeObjectHasProperty -InputObject $entry -PropertyName 'skill_id') { [string]$entry.skill_id } else { '' }
        if (-not [string]::IsNullOrWhiteSpace($skillId) -and $skillId -in @($hostExcluded)) {
            continue
        }
        $state = if ($skillId -in @($currentSelectedSkillIds)) { 'current_surfaced' } else { 'inherited_not_currently_surfaced' }
        Add-VibeSkillExecutionLockRecord -Rows $rows -Seen $seen -Record (Copy-VibeSkillExecutionLockDispatchRecord -Record $entry -LockSource 'previous_skill_execution_lock' -ReconciliationState $state)
    }
    foreach ($skillId in @(Get-VibeSkillExecutionLockSkillIds -SkillExecutionLock $previousLock)) {
        if ($skillId -in @($hostExcluded)) {
            continue
        }
        if ($seen.ContainsKey($skillId)) {
            continue
        }
        $state = if ($skillId -in @($currentSelectedSkillIds)) { 'current_surfaced' } else { 'inherited_not_currently_surfaced' }
        Add-VibeSkillExecutionLockRecord -Rows $rows -Seen $seen -Record (New-VibeMinimalSkillExecutionLockDispatchRecord -SkillId $skillId -LockSource 'previous_skill_execution_lock' -ReconciliationState $state)
    }
}
```

- [ ] **Step 3: Verify the plan now documents the guarded path**

Run:

```powershell
$plan = 'docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md'
rg -n "previousDispatch|Get-VibeSkillExecutionLockSkillIds|previousLock\.locked_dispatch" $plan
```

Expected:

```text
Matches for `previousDispatch` and `Get-VibeSkillExecutionLockSkillIds` appear.
No match remains for `previousLock.locked_dispatch`.
```

- [ ] **Step 4: Commit the specialist-lock plan sync**

Run:

```powershell
git add docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md
git commit -m "docs: sync specialist execution lock plan snippet"
```

### Task 2: Rewrite The Obsolete Installer-Helper Removal Plan

**Files:**
- Modify: `docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md`

- [ ] **Step 1: Confirm the current task is internally outdated**

Run:

```powershell
rg -n "Test-VgoSkillEntryPoint|Remove Unused Installer Helper|Expected before the edit" docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md
rg -n "Test-VgoSkillEntryPoint" scripts/install/Install-VgoAdapter.ps1 scripts tests packages -S
```

Expected:

```text
The plan file contains the obsolete removal task text.
The repository search for scripts/install/Install-VgoAdapter.ps1, scripts, tests, and packages returns no code matches.
```

- [ ] **Step 2: Replace Task 2 with a no-op verification task**

Rewrite the Task 2 section to this content:

````markdown
### Task 2: Confirm The Installer Helper Is Already Gone

**Files:**
- Modify: `docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md`

- [ ] **Step 1: Confirm the helper is absent**

Run:

```powershell
rg -n "Test-VgoSkillEntryPoint" scripts/install/Install-VgoAdapter.ps1 scripts tests packages -S
```

Expected: no matches. `Test-VgoSkillEntryPoint` is not present in the current
installer codebase.

- [ ] **Step 2: Record the no-op conclusion**

Replace the old removal instructions with a short explanation that the earlier
review item no longer applies because the helper is already absent from current
installer code.

- [ ] **Step 3: Verify the updated task is self-consistent**

Run:

```powershell
rg -n "Test-VgoSkillEntryPoint|no-op|already absent|Remove Unused Installer Helper" docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md
```

Expected: the file still names `Test-VgoSkillEntryPoint`, explains the no-op
state, and no longer uses the heading `Remove Unused Installer Helper`.
````

- [ ] **Step 3: Verify the rewritten task text**

Run:

```powershell
Get-Content docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md | Select-Object -Index (55..110)
```

Expected:

```text
Task 2 now describes a no-op verification/document-alignment outcome rather than deleting a function block from Install-VgoAdapter.ps1.
```

- [ ] **Step 4: Commit the follow-up plan rewrite**

Run:

```powershell
git add docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md
git commit -m "docs: align rabbit followup two-comment plan"
```

### Task 3: Remove Local Worktree Paths From The Affected Specs

**Files:**
- Modify: `docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md`
- Modify: `docs/superpowers/specs/2026-05-06-rabbit-followup-three-comments-design.md`
- Modify: `docs/superpowers/specs/2026-05-06-rabbit-latest-two-comments-design.md`
- Modify: `docs/superpowers/specs/2026-05-06-rabbit-latest-three-comments-design.md`

- [ ] **Step 1: Confirm all four path leaks**

Run:

```powershell
rg -n "F:\\vibe\\Vibe-Skills\\.worktrees\\pr226-pr227-combined" docs/superpowers/specs
```

Expected:

```text
Four matches appear, one in each affected 2026-05-06 rabbit spec.
```

- [ ] **Step 2: Replace the local path text in every affected file**

In each of the four files, replace:

```markdown
The branch is `review/pr226-pr227-combined` in the worktree
`F:\vibe\Vibe-Skills\.worktrees\pr226-pr227-combined`.
```

with:

```markdown
The branch is `review/pr226-pr227-combined`.
```

- [ ] **Step 3: Verify the path leak is gone**

Run:

```powershell
rg -n "F:\\vibe\\Vibe-Skills\\.worktrees\\pr226-pr227-combined" docs/superpowers/specs
Get-Content docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md -TotalCount 10
Get-Content docs/superpowers/specs/2026-05-06-rabbit-followup-three-comments-design.md -TotalCount 10
Get-Content docs/superpowers/specs/2026-05-06-rabbit-latest-two-comments-design.md -TotalCount 10
Get-Content docs/superpowers/specs/2026-05-06-rabbit-latest-three-comments-design.md -TotalCount 10
```

Expected:

```text
The ripgrep command returns no matches.
Each file now states only `The branch is review/pr226-pr227-combined.`
```

- [ ] **Step 4: Commit the spec cleanup**

Run:

```powershell
git add docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md docs/superpowers/specs/2026-05-06-rabbit-followup-three-comments-design.md docs/superpowers/specs/2026-05-06-rabbit-latest-two-comments-design.md docs/superpowers/specs/2026-05-06-rabbit-latest-three-comments-design.md
git commit -m "docs: remove local worktree paths from rabbit specs"
```

### Task 4: Validate The Documentation-Only Patch

**Files:**
- Check: `docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md`
- Check: `docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md`
- Check: `docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md`
- Check: `docs/superpowers/specs/2026-05-06-rabbit-followup-three-comments-design.md`
- Check: `docs/superpowers/specs/2026-05-06-rabbit-latest-two-comments-design.md`
- Check: `docs/superpowers/specs/2026-05-06-rabbit-latest-three-comments-design.md`

- [ ] **Step 1: Run diff hygiene validation**

Run:

```powershell
git diff --check
```

Expected:

```text
No output.
```

- [ ] **Step 2: Re-run the repository-state checks**

Run:

```powershell
rg -n "Test-VgoSkillEntryPoint" scripts/install/Install-VgoAdapter.ps1 scripts tests packages -S
rg -n "F:\\vibe\\Vibe-Skills\\.worktrees\\pr226-pr227-combined" docs/superpowers/specs
```

Expected:

```text
Both commands return no matches from current code or committed specs.
```

- [ ] **Step 3: Confirm GitHub review threads are cleared**

Run:

```powershell
$query = @'
query($owner:String!, $repo:String!, $number:Int!) {
  repository(owner:$owner, name:$repo) {
    pullRequest(number:$number) {
      reviewThreads(first:100) {
        nodes { isResolved }
      }
    }
  }
}
'@
$json = gh api graphql -f owner='foryourhealth111-pixel' -f repo='Vibe-Skills' -F number=228 -f query="$query" | ConvertFrom-Json
$threads = $json.data.repository.pullRequest.reviewThreads.nodes
$resolved = ($threads | Where-Object { $_.isResolved }).Count
$total = $threads.Count
"total=$total resolved=$resolved unresolved=$($total - $resolved)"
```

Expected:

```text
The output reports `unresolved=0`.
```

- [ ] **Step 4: Confirm branch cleanliness before push**

Run:

```powershell
git status --short --branch
```

Expected:

```text
The working tree is clean aside from being ahead of origin by the new documentation commits.
```

## Self-Review

- Spec coverage: Task 1 covers both unresolved comments on `2026-05-05-vibe-specialist-execution-lock.md`; Task 2 covers the outdated `rabbit-followup-two-comments` plan; Task 3 covers the four spec path leaks; Task 4 matches the spec's validation section.
- Placeholder scan: no placeholder markers or vague deferred-work wording remains; every task includes explicit file targets, commands, and expected outcomes.
- Type consistency: the plan consistently uses `Get-VibeSkillExecutionLockSkillIds`, `previousDispatch`, `Test-VgoSkillEntryPoint`, and `review/pr226-pr227-combined`, matching the approved spec and current repository terminology.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-06-rabbit-four-doc-comments-implementation.md`.
