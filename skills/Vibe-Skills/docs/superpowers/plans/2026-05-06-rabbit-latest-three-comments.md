# Rabbit Latest Three Comments Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the three currently unresolved CodeRabbit threads on PR 228 with minimal documentation and runtime-report changes.

**Architecture:** Keep this as a narrow review-cleanup patch. Documentation files are synchronized with current repository facts, and runtime delivery acceptance adds one residual-risk message without changing gate calculations or truth-layer payloads.

**Tech Stack:** Markdown documentation, Python runtime verification code, pytest.

---

## File Structure

- `docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md`
  - Responsibility: historical implementation plan for specialist execution locks.
  - Change: update the embedded loader snippet so it no longer documents empty dictionaries as authoritative lock payloads.
- `docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md`
  - Responsibility: prior Rabbit follow-up design record.
  - Change: replace the obsolete installer-helper finding with a current-state finding that the helper is absent and no installer code change is required.
- `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`
  - Responsibility: build runtime delivery acceptance reports.
  - Change: include selected/approved lock misses in `residual_risks`.
- `packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py`
  - Responsibility: focused lock reconciliation tests.
  - Change: add a failing assertion for the selected-lock residual-risk message.

## Task 1: Add The Failing Residual-Risk Assertion

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py:434-439`

- [ ] **Step 1: Add the expected residual-risk assertion**

Update the end of the selected-lock integration test from:

```python
    assert report["summary"]["gate_result"] == "MANUAL_REVIEW_REQUIRED"
    assert report["summary"]["completion_language_allowed"] is False
    assert report["truth_results"]["selected_lock_reconciliation_truth"]["state"] == "manual_review_required"
    assert report["selected_lock_reconciliation"]["missing"] == ["literature-review"]
```

to:

```python
    assert report["summary"]["gate_result"] == "MANUAL_REVIEW_REQUIRED"
    assert report["summary"]["completion_language_allowed"] is False
    assert report["truth_results"]["selected_lock_reconciliation_truth"]["state"] == "manual_review_required"
    assert report["selected_lock_reconciliation"]["missing"] == ["literature-review"]
    assert (
        "Selected/approved specialist execution was not locked for: literature-review."
        in report["residual_risks"]
    )
```

- [ ] **Step 2: Run the focused test to verify it fails**

Run:

```powershell
pytest packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py::test_delivery_acceptance_manual_review_when_selected_skill_missing_from_lock -q
```

Expected before implementation: the test fails because `report["residual_risks"]` does not contain the selected-lock missing message.

## Task 2: Add Selected-Lock Missing Residual Risk

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py:1269-1274`

- [ ] **Step 1: Add the runtime residual-risk message**

Change the lock-related residual-risk block from:

```python
    if specialist_lock_lists["failed"]:
        residual_risks.append("Locked specialist execution failed for: " + ", ".join(specialist_lock_lists["failed"]) + ".")
    if specialist_lock_lists["unresolved"]:
        residual_risks.append("Locked specialist execution remains unresolved for: " + ", ".join(specialist_lock_lists["unresolved"]) + ".")
    if specialist_lock_lists["deferred"]:
        residual_risks.append("Locked specialist execution was deferred for: " + ", ".join(specialist_lock_lists["deferred"]) + ".")
```

to:

```python
    if specialist_lock_lists["failed"]:
        residual_risks.append("Locked specialist execution failed for: " + ", ".join(specialist_lock_lists["failed"]) + ".")
    if specialist_lock_lists["unresolved"]:
        residual_risks.append("Locked specialist execution remains unresolved for: " + ", ".join(specialist_lock_lists["unresolved"]) + ".")
    if specialist_lock_lists["deferred"]:
        residual_risks.append("Locked specialist execution was deferred for: " + ", ".join(specialist_lock_lists["deferred"]) + ".")
    if selected_lock_lists["missing"]:
        residual_risks.append(
            "Selected/approved specialist execution was not locked for: "
            + ", ".join(selected_lock_lists["missing"])
            + "."
        )
```

- [ ] **Step 2: Run the focused test to verify it passes**

Run:

```powershell
pytest packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py::test_delivery_acceptance_manual_review_when_selected_skill_missing_from_lock -q
```

Expected after implementation: the test passes.

- [ ] **Step 3: Run the full focused lock reconciliation test file**

Run:

```powershell
pytest packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py -q
```

Expected: all tests in this file pass.

## Task 3: Sync The Stale Lock Loader Plan Snippet

**Files:**
- Modify: `docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md:1229-1253`

- [ ] **Step 1: Update the embedded loader predicates**

Change the documented snippet from:

```python
def _load_skill_execution_lock(runtime_packet: dict[str, object], execution_manifest: dict[str, object]) -> dict[str, object]:
    manifest_lock = execution_manifest.get("skill_execution_lock")
    if isinstance(manifest_lock, dict):
        return manifest_lock
    accounting = execution_manifest.get("specialist_accounting")
    if isinstance(accounting, dict):
        accounting_lock = accounting.get("skill_execution_lock")
        if isinstance(accounting_lock, dict):
            return accounting_lock
    packet_lock = runtime_packet.get("skill_execution_lock")
    if isinstance(packet_lock, dict):
        return packet_lock
    return {}


def _load_specialist_lock_resolution(execution_manifest: dict[str, object]) -> dict[str, object]:
    manifest_resolution = execution_manifest.get("specialist_lock_resolution")
    if isinstance(manifest_resolution, dict):
        return manifest_resolution
    accounting = execution_manifest.get("specialist_accounting")
    if isinstance(accounting, dict):
        accounting_resolution = accounting.get("specialist_lock_resolution")
        if isinstance(accounting_resolution, dict):
            return accounting_resolution
    return {}
```

to:

```python
def _load_skill_execution_lock(runtime_packet: dict[str, object], execution_manifest: dict[str, object]) -> dict[str, object]:
    manifest_lock = execution_manifest.get("skill_execution_lock")
    if isinstance(manifest_lock, dict) and manifest_lock:
        return manifest_lock
    accounting = execution_manifest.get("specialist_accounting")
    if isinstance(accounting, dict):
        accounting_lock = accounting.get("skill_execution_lock")
        if isinstance(accounting_lock, dict) and accounting_lock:
            return accounting_lock
    packet_lock = runtime_packet.get("skill_execution_lock")
    if isinstance(packet_lock, dict) and packet_lock:
        return packet_lock
    return {}


def _load_specialist_lock_resolution(execution_manifest: dict[str, object]) -> dict[str, object]:
    manifest_resolution = execution_manifest.get("specialist_lock_resolution")
    if isinstance(manifest_resolution, dict) and manifest_resolution:
        return manifest_resolution
    accounting = execution_manifest.get("specialist_accounting")
    if isinstance(accounting, dict):
        accounting_resolution = accounting.get("specialist_lock_resolution")
        if isinstance(accounting_resolution, dict) and accounting_resolution:
            return accounting_resolution
    return {}
```

- [ ] **Step 2: Confirm the stale predicates are gone from that snippet**

Run:

```powershell
$p = 'docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md'
$lines = Get-Content -LiteralPath $p
$snippet = $lines[1228..1252] -join "`n"
$snippet
```

Expected: each loader return predicate in the snippet uses `and <payload_name>` before returning a dictionary.

## Task 4: Correct The Obsolete Installer-Helper Design Text

**Files:**
- Modify: `docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md:22-40`

- [ ] **Step 1: Replace the stale finding and design item**

Replace this section:

```markdown
### Unused Installer Helper

`scripts/install/Install-VgoAdapter.ps1` defines `Test-VgoSkillEntryPoint`.
Repository search shows only the function definition and no call sites. The
function is not established as an exported public helper in this script surface.
Removing the unused helper is lower risk than documenting it as a public API
without an actual consumer.
```

with:

```markdown
### Installer Helper Finding No Longer Applies

`scripts/install/Install-VgoAdapter.ps1` does not currently define
`Test-VgoSkillEntryPoint`. Repository search finds that symbol only in prior
spec and plan documents, not in installer code. The original remove-helper
finding no longer matches the current repository state.
```

Then replace this design paragraph:

```markdown
1. Replace `host approved additions` with `host-approved additions` in the
   follow-up plan checklist.
2. Remove the unused `Test-VgoSkillEntryPoint` function block from
   `scripts/install/Install-VgoAdapter.ps1`.

No behavior should change for installed runtime payloads because the removed
function has no repository call sites.
```

with:

```markdown
1. Replace `host approved additions` with `host-approved additions` in the
   follow-up plan checklist.
2. Record that the `Test-VgoSkillEntryPoint` removal is no longer applicable
   because current installer code does not contain that function.

No installer behavior should change because this item requires only a design
document correction against current repository state.
```

- [ ] **Step 2: Confirm installer code still has no helper definition**

Run:

```powershell
rg -n "function Test-VgoSkillEntryPoint|Test-VgoSkillEntryPoint" scripts packages tests
```

Expected: no matches in code or tests. Mentions in `docs/superpowers` are acceptable because they document the prior review history and the current correction.

## Task 5: Run Targeted Regression Checks

**Files:**
- Validate: runtime tests and changed Markdown/Python files.

- [ ] **Step 1: Run the focused runtime delivery tests**

Run:

```powershell
pytest tests/runtime_neutral/test_runtime_delivery_acceptance.py packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py -q
```

Expected: all selected runtime delivery acceptance tests pass.

- [ ] **Step 2: Run whitespace validation**

Run:

```powershell
git diff --check
```

Expected: no output and exit code `0`.

- [ ] **Step 3: Check for generated Python cache files under repo-owned paths**

Run:

```powershell
$paths = @('apps', 'packages', 'tests', 'scripts')
$count = 0
foreach ($p in $paths) {
    if (Test-Path -LiteralPath $p) {
        $count += @(Get-ChildItem -LiteralPath $p -Recurse -Force -Include '__pycache__','*.pyc' -ErrorAction SilentlyContinue).Count
    }
}
$count
```

Expected: `0`. If this prints a non-zero count, remove only generated `__pycache__` directories and `*.pyc` files under those repo-owned paths, then rerun this step.

## Task 6: Commit The Local Patch

**Files:**
- Commit all files changed by Tasks 1-4.

- [ ] **Step 1: Review the diff**

Run:

```powershell
git diff -- docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py
```

Expected: the diff contains only the two documentation corrections, the one residual-risk runtime addition, and the one test assertion.

- [ ] **Step 2: Commit the implementation**

Run:

```powershell
git add -- docs/superpowers/plans/2026-05-05-vibe-specialist-execution-lock.md docs/superpowers/specs/2026-05-06-rabbit-followup-two-comments-design.md packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py
git commit -m "fix: address latest rabbit review comments"
```

Expected: a new local implementation commit is created after the plan commit.

## Task 7: Update The PR Branch And Verify GitHub State

**Files:**
- No file edits.

- [ ] **Step 1: Attempt normal push**

Run:

```powershell
git push origin HEAD:review/pr226-pr227-combined
```

Expected: if the push succeeds, continue to Step 2. If the push is rejected as
non-fast-forward or fails because the network resets, stop the PR update step and
report the exact push error before using any branch-rewrite strategy. Do not use
`--force`, `--force-with-lease`, or the GitHub Git Database API without an
explicit follow-up approval for that push strategy.

- [ ] **Step 2: Verify remote and local trees match**

Run:

```powershell
$remoteCommit = gh api repos/foryourhealth111-pixel/Vibe-Skills/git/ref/heads/review/pr226-pr227-combined --jq .object.sha
$remoteTree = gh api repos/foryourhealth111-pixel/Vibe-Skills/git/commits/$remoteCommit --jq .tree.sha
$localTree = git show -s --format=%T HEAD
[pscustomobject]@{
  remote_commit = $remoteCommit
  remote_tree = $remoteTree
  local_head = (git rev-parse HEAD)
  local_tree = $localTree
  tree_matches = ($remoteTree -eq $localTree)
} | Format-List
```

Expected: `tree_matches : True`.

- [ ] **Step 3: Verify PR review threads**

Run:

```powershell
$query = @'
query($owner:String!, $repo:String!, $number:Int!) {
  repository(owner:$owner, name:$repo) {
    pullRequest(number:$number) {
      headRefOid
      mergeStateStatus
      reviewThreads(first: 100) {
        nodes {
          isResolved
          isOutdated
          path
          line
          comments(first: 20) {
            nodes {
              author { login }
              createdAt
              body
              url
            }
          }
        }
      }
    }
  }
}
'@
$json = gh api graphql -f query=$query -f owner='foryourhealth111-pixel' -f repo='Vibe-Skills' -F number=228 | ConvertFrom-Json
$pr = $json.data.repository.pullRequest
$threads = @($pr.reviewThreads.nodes)
$unresolved = @($threads | Where-Object { -not $_.isResolved })
[pscustomobject]@{
  headRefOid = $pr.headRefOid
  mergeStateStatus = $pr.mergeStateStatus
  total_threads = $threads.Count
  unresolved_threads = $unresolved.Count
  unresolved_paths = (@($unresolved | ForEach-Object { $_.path }) -join ', ')
} | Format-List
```

Expected: unresolved threads for the three current Rabbit comments are resolved or outdated. If CodeRabbit posts new comments, repeat the review process rather than assuming they are valid.

- [ ] **Step 4: Verify PR checks**

Run:

```powershell
gh pr checks 228 --repo foryourhealth111-pixel/Vibe-Skills
```

Expected: `CodeRabbit`, `gates`, and `python-validation` report `pass`. If checks are still pending, wait for completion before reporting final status.
