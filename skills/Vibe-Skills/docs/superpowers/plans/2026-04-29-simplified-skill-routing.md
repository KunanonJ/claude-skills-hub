# Simplified Skill Routing Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the expert-skill routing authority with `skill_routing.selected` and keep final usage truth in `skill_usage.used / skill_usage.unused`.

**Architecture:** Add a focused routing helper module, make freeze produce `skill_routing`, then convert requirement, plan, execute, cleanup, and delivery acceptance to read selected skills from that object. Legacy specialist fields may be read only when a previous artifact has no `skill_routing`; new artifacts isolate legacy data under `legacy_skill_routing`.

**Tech Stack:** PowerShell runtime scripts, Python `unittest` runtime-neutral tests, existing Vibe verification gates.

---

## Scope Check

This plan covers one subsystem: expert skill routing and usage authority inside the governed Vibe runtime. It does not delete skill directories, change canonical `$vibe` launch, or complete pack-by-pack skill pruning.

## File Structure

- Create: `scripts/runtime/VibeSkillRouting.Common.ps1`
  - Owns the new `skill_routing` contract, selected-skill accessors, legacy projection, and summary helpers.
- Modify: `scripts/runtime/VibeSkillUsage.Common.ps1`
  - Adds canonical `used` and `unused` arrays while preserving existing `used_skills`, `unused_skills`, `loaded_skills`, and `evidence` for compatibility during the migration.
- Modify: `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
  - Builds `skill_routing`, loads every selected skill, and passes routing into the packet projection.
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
  - Adds `SkillRouting` to `New-VibeRuntimeInputPacketProjection`, emits `skill_routing`, moves old specialist fields under `legacy_skill_routing`, and adds selected-skill decision projection helpers.
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
  - Reads selected skills from `skill_routing.selected` and stops treating `specialist_dispatch.approved_dispatch` as the new authority.
- Modify: `scripts/runtime/Write-XlPlan.ps1`
  - Uses selected skills for the specialist work section and execution topology input.
- Modify: `scripts/runtime/VibeExecution.Common.ps1`
  - Adds `SelectedSkills` support to `New-VibeExecutionTopology`; keeps `ApprovedDispatch` as legacy fallback only.
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
  - Uses `skill_routing.selected` as the execution authority and writes routing summaries rather than duplicating full dispatch objects in primary manifest fields.
- Modify: `scripts/runtime/Invoke-PhaseCleanup.ps1`
  - Summarizes canonical `skill_usage.used / unused`.
- Modify: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`
  - Evaluates new `skill_routing` and new `skill_usage` shapes, with read-only legacy fallback.
- Modify: `tests/runtime_neutral/test_binary_skill_usage_contract.py`
  - Updates usage assertions to include the new canonical `used / unused` arrays.
- Create: `tests/runtime_neutral/test_simplified_skill_routing_contract.py`
  - Focused helper and freeze-contract tests for the new routing model.
- Modify: `tests/runtime_neutral/test_runtime_delivery_acceptance.py`
  - Adds acceptance tests proving legacy dispatch cannot drive usage and selected skills must load full `SKILL.md`.
- Modify: existing specialist-dispatch tests only where they assert old root-level packet fields.
  - Keep behavior coverage, rename assertions to `skill_routing.selected` and `legacy_skill_routing`.

## Task 1: Add Contract Tests For The New Routing Helper

**Files:**
- Create: `tests/runtime_neutral/test_simplified_skill_routing_contract.py`
- Test command: `python -m pytest tests/runtime_neutral/test_simplified_skill_routing_contract.py -q`

- [ ] **Step 1: Write the failing helper tests**

Create `tests/runtime_neutral/test_simplified_skill_routing_contract.py` with this content:

```python
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeRuntime.Common.ps1"
SKILL_USAGE_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeSkillUsage.Common.ps1"
SKILL_ROUTING_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeSkillRouting.Common.ps1"
FREEZE_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "Freeze-RuntimeInputPacket.ps1"


def resolve_powershell() -> str | None:
    candidates = [
        shutil.which("pwsh"),
        shutil.which("pwsh.exe"),
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        shutil.which("powershell"),
        shutil.which("powershell.exe"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate))
    return None


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def run_ps_json(script: str) -> dict[str, object]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available")
    completed = subprocess.run(
        [shell, "-NoLogo", "-NoProfile", "-Command", script],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return json.loads(completed.stdout)


def as_list(value: object) -> list[object]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


class SimplifiedSkillRoutingContractTests(unittest.TestCase):
    def test_helper_builds_candidate_selected_rejected_from_legacy_inputs(self) -> None:
        payload = run_ps_json(
            "& { "
            f". {ps_quote(str(RUNTIME_COMMON))}; "
            f". {ps_quote(str(SKILL_USAGE_COMMON))}; "
            f". {ps_quote(str(SKILL_ROUTING_COMMON))}; "
            "$recommendations = @( "
            "[pscustomobject]@{ skill_id = 'scikit-learn'; reason = 'model training'; native_skill_entrypoint = 'skills/scikit/SKILL.md'; dispatch_phase = 'in_execution'; parallelizable_in_root_xl = $true }, "
            "[pscustomobject]@{ skill_id = 'plotly'; reason = 'optional charting'; native_skill_entrypoint = 'skills/plotly/SKILL.md'; dispatch_phase = 'post_execution'; parallelizable_in_root_xl = $false } "
            "); "
            "$hints = @([pscustomobject]@{ skill_id = 'matplotlib'; reason = 'legacy stage helper' }); "
            "$dispatch = [pscustomobject]@{ "
            "approved_dispatch = @($recommendations[0]); "
            "local_specialist_suggestions = @($recommendations[1]); "
            "blocked = @(); degraded = @() "
            "}; "
            "$routing = New-VibeSkillRoutingFromLegacy "
            "-RouterSelectedSkill 'scikit-learn' "
            "-Recommendations @($recommendations) "
            "-StageAssistantHints @($hints) "
            "-SpecialistDispatch $dispatch; "
            "$routing | ConvertTo-Json -Depth 20 "
            "}"
        )

        self.assertEqual("simplified_skill_routing_v1", payload["schema_version"])
        candidate_ids = [item["skill_id"] for item in as_list(payload["candidates"])]
        selected_ids = [item["skill_id"] for item in as_list(payload["selected"])]
        rejected_ids = [item["skill_id"] for item in as_list(payload["rejected"])]
        self.assertEqual(["scikit-learn"], selected_ids)
        self.assertIn("scikit-learn", candidate_ids)
        self.assertIn("plotly", candidate_ids)
        self.assertIn("matplotlib", candidate_ids)
        self.assertIn("plotly", rejected_ids)
        self.assertIn("matplotlib", rejected_ids)
        selected = as_list(payload["selected"])[0]
        self.assertEqual("in_execution", selected["dispatch_phase"])
        self.assertEqual("model training", selected["reason"])

    def test_selected_skill_ids_prefer_skill_routing_over_legacy_dispatch(self) -> None:
        payload = run_ps_json(
            "& { "
            f". {ps_quote(str(RUNTIME_COMMON))}; "
            f". {ps_quote(str(SKILL_ROUTING_COMMON))}; "
            "$packet = [pscustomobject]@{ "
            "skill_routing = [pscustomobject]@{ selected = @([pscustomobject]@{ skill_id = 'new-authority' }) }; "
            "specialist_dispatch = [pscustomobject]@{ approved_dispatch = @([pscustomobject]@{ skill_id = 'legacy-only' }) } "
            "}; "
            "$ids = Get-VibeSkillRoutingSelectedSkillIds -RuntimeInputPacket $packet; "
            "[pscustomobject]@{ selected_skill_ids = $ids } | ConvertTo-Json -Depth 20 "
            "}"
        )

        self.assertEqual(["new-authority"], payload["selected_skill_ids"])

    def test_selected_skill_ids_fall_back_to_legacy_only_when_skill_routing_is_absent(self) -> None:
        payload = run_ps_json(
            "& { "
            f". {ps_quote(str(RUNTIME_COMMON))}; "
            f". {ps_quote(str(SKILL_ROUTING_COMMON))}; "
            "$packet = [pscustomobject]@{ "
            "specialist_dispatch = [pscustomobject]@{ approved_dispatch = @([pscustomobject]@{ skill_id = 'legacy-skill' }) } "
            "}; "
            "$ids = Get-VibeSkillRoutingSelectedSkillIds -RuntimeInputPacket $packet; "
            "[pscustomobject]@{ selected_skill_ids = $ids } | ConvertTo-Json -Depth 20 "
            "}"
        )

        self.assertEqual(["legacy-skill"], payload["selected_skill_ids"])

    def test_freeze_emits_skill_routing_with_selected_skills(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available")
        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir) / "artifacts"
            completed = subprocess.run(
                [
                    shell,
                    "-NoLogo",
                    "-NoProfile",
                    "-File",
                    str(FREEZE_SCRIPT),
                    "-Task",
                    "Build a scikit-learn tabular classification baseline and compare cross-validation metrics.",
                    "-Mode",
                    "interactive_governed",
                    "-RunId",
                    "pytest-simplified-skill-routing-freeze",
                    "-ArtifactRoot",
                    str(artifact_root),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            self.assertIn("packet_path", completed.stdout)
            packet_path = next(artifact_root.rglob("runtime-input-packet.json"))
            packet = json.loads(packet_path.read_text(encoding="utf-8"))

        routing = packet["skill_routing"]
        selected_ids = [item["skill_id"] for item in as_list(routing["selected"])]
        self.assertIn("scikit-learn", selected_ids)
        self.assertGreaterEqual(len(as_list(routing["candidates"])), len(selected_ids))
        for selected in as_list(routing["selected"]):
            self.assertIn("skill_id", selected)
            self.assertIn("task_slice", selected)
            self.assertIn("skill_md_path", selected)
```

- [ ] **Step 2: Run the helper tests and confirm failure**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_simplified_skill_routing_contract.py -q
```

Expected: FAIL because `scripts/runtime/VibeSkillRouting.Common.ps1` and its functions do not exist yet.

- [ ] **Step 3: Commit the failing test**

```powershell
git add tests/runtime_neutral/test_simplified_skill_routing_contract.py
git commit -m "test: define simplified skill routing contract"
```

## Task 2: Add The Skill Routing Helper Module

**Files:**
- Create: `scripts/runtime/VibeSkillRouting.Common.ps1`
- Test: `tests/runtime_neutral/test_simplified_skill_routing_contract.py`

- [ ] **Step 1: Implement the helper module**

Create `scripts/runtime/VibeSkillRouting.Common.ps1`:

```powershell
Set-StrictMode -Version Latest

function Get-VibeSkillRoutingProperty {
    param(
        [AllowNull()] [object]$InputObject,
        [Parameter(Mandatory)] [string]$PropertyName,
        [AllowNull()] [object]$DefaultValue = $null
    )

    if ($null -ne $InputObject -and $InputObject.PSObject.Properties.Name -contains $PropertyName) {
        return $InputObject.$PropertyName
    }
    return $DefaultValue
}

function New-VibeSkillRoutingEntry {
    param(
        [Parameter(Mandatory)] [string]$SkillId,
        [AllowNull()] [object]$Source = $null,
        [AllowEmptyString()] [string]$Reason = '',
        [AllowEmptyString()] [string]$State = 'candidate'
    )

    $sourceReason = [string](Get-VibeSkillRoutingProperty -InputObject $Source -PropertyName 'reason' -DefaultValue '')
    $nativeEntrypoint = [string](Get-VibeSkillRoutingProperty -InputObject $Source -PropertyName 'native_skill_entrypoint' -DefaultValue '')
    $skillMdPath = [string](Get-VibeSkillRoutingProperty -InputObject $Source -PropertyName 'skill_md_path' -DefaultValue '')
    if ([string]::IsNullOrWhiteSpace($skillMdPath)) {
        $skillMdPath = $nativeEntrypoint
    }
    $dispatchPhase = [string](Get-VibeSkillRoutingProperty -InputObject $Source -PropertyName 'dispatch_phase' -DefaultValue 'in_execution')
    if ([string]::IsNullOrWhiteSpace($dispatchPhase)) {
        $dispatchPhase = 'in_execution'
    }
    $taskSlice = [string](Get-VibeSkillRoutingProperty -InputObject $Source -PropertyName 'task_slice' -DefaultValue '')
    if ([string]::IsNullOrWhiteSpace($taskSlice)) {
        $taskSlice = if ([string]::IsNullOrWhiteSpace($sourceReason)) { ('Use {0} for its selected specialist workflow.' -f $SkillId) } else { $sourceReason }
    }

    return [pscustomobject]@{
        skill_id = $SkillId
        skill_md_path = if ([string]::IsNullOrWhiteSpace($skillMdPath)) { $null } else { $skillMdPath }
        reason = if ([string]::IsNullOrWhiteSpace($Reason)) { $sourceReason } else { $Reason }
        task_slice = $taskSlice
        state = $State
        dispatch_phase = $dispatchPhase
        parallelizable_in_root_xl = [bool](Get-VibeSkillRoutingProperty -InputObject $Source -PropertyName 'parallelizable_in_root_xl' -DefaultValue $false)
        native_usage_required = [bool](Get-VibeSkillRoutingProperty -InputObject $Source -PropertyName 'native_usage_required' -DefaultValue $true)
        native_skill_entrypoint = if ([string]::IsNullOrWhiteSpace($nativeEntrypoint)) { $null } else { $nativeEntrypoint }
        legacy_source = [string](Get-VibeSkillRoutingProperty -InputObject $Source -PropertyName 'source' -DefaultValue '')
    }
}

function Add-VibeSkillRoutingEntry {
    param(
        [Parameter(Mandatory)] [System.Collections.Generic.List[object]]$Rows,
        [Parameter(Mandatory)] [hashtable]$Seen,
        [Parameter(Mandatory)] [object]$Entry
    )

    $skillId = [string](Get-VibeSkillRoutingProperty -InputObject $Entry -PropertyName 'skill_id' -DefaultValue '')
    if ([string]::IsNullOrWhiteSpace($skillId) -or $Seen.ContainsKey($skillId)) {
        return
    }
    $Rows.Add($Entry) | Out-Null
    $Seen[$skillId] = $true
}

function New-VibeSkillRoutingFromLegacy {
    param(
        [AllowEmptyString()] [string]$RouterSelectedSkill = '',
        [AllowEmptyCollection()] [AllowNull()] [object[]]$Recommendations = @(),
        [AllowEmptyCollection()] [AllowNull()] [object[]]$StageAssistantHints = @(),
        [AllowNull()] [object]$SpecialistDispatch = $null
    )

    $candidateRows = New-Object System.Collections.Generic.List[object]
    $selectedRows = New-Object System.Collections.Generic.List[object]
    $rejectedRows = New-Object System.Collections.Generic.List[object]
    $candidateSeen = @{}
    $selectedSeen = @{}
    $rejectedSeen = @{}

    foreach ($recommendation in @($Recommendations)) {
        $skillId = [string](Get-VibeSkillRoutingProperty -InputObject $recommendation -PropertyName 'skill_id' -DefaultValue '')
        if ([string]::IsNullOrWhiteSpace($skillId)) {
            continue
        }
        Add-VibeSkillRoutingEntry -Rows $candidateRows -Seen $candidateSeen -Entry (New-VibeSkillRoutingEntry -SkillId $skillId -Source $recommendation -State 'candidate')
    }

    foreach ($hint in @($StageAssistantHints)) {
        $skillId = [string](Get-VibeSkillRoutingProperty -InputObject $hint -PropertyName 'skill_id' -DefaultValue '')
        if ([string]::IsNullOrWhiteSpace($skillId)) {
            continue
        }
        Add-VibeSkillRoutingEntry -Rows $candidateRows -Seen $candidateSeen -Entry (New-VibeSkillRoutingEntry -SkillId $skillId -Source $hint -State 'candidate')
    }

    $approvedDispatch = @()
    if ($null -ne $SpecialistDispatch -and $SpecialistDispatch.PSObject.Properties.Name -contains 'approved_dispatch') {
        $approvedDispatch = @($SpecialistDispatch.approved_dispatch)
    }

    foreach ($dispatch in $approvedDispatch) {
        $skillId = [string](Get-VibeSkillRoutingProperty -InputObject $dispatch -PropertyName 'skill_id' -DefaultValue '')
        if ([string]::IsNullOrWhiteSpace($skillId)) {
            continue
        }
        Add-VibeSkillRoutingEntry -Rows $candidateRows -Seen $candidateSeen -Entry (New-VibeSkillRoutingEntry -SkillId $skillId -Source $dispatch -State 'candidate')
        Add-VibeSkillRoutingEntry -Rows $selectedRows -Seen $selectedSeen -Entry (New-VibeSkillRoutingEntry -SkillId $skillId -Source $dispatch -State 'selected')
    }

    if (-not [string]::IsNullOrWhiteSpace($RouterSelectedSkill) -and -not $selectedSeen.ContainsKey($RouterSelectedSkill)) {
        $matching = @($Recommendations | Where-Object { [string](Get-VibeSkillRoutingProperty -InputObject $_ -PropertyName 'skill_id' -DefaultValue '') -eq $RouterSelectedSkill } | Select-Object -First 1)
        $source = if (@($matching).Count -gt 0) { $matching[0] } else { $null }
        Add-VibeSkillRoutingEntry -Rows $candidateRows -Seen $candidateSeen -Entry (New-VibeSkillRoutingEntry -SkillId $RouterSelectedSkill -Source $source -Reason 'router selected skill' -State 'candidate')
        Add-VibeSkillRoutingEntry -Rows $selectedRows -Seen $selectedSeen -Entry (New-VibeSkillRoutingEntry -SkillId $RouterSelectedSkill -Source $source -Reason 'router selected skill' -State 'selected')
    }

    foreach ($candidate in @($candidateRows.ToArray())) {
        $skillId = [string]$candidate.skill_id
        if (-not $selectedSeen.ContainsKey($skillId)) {
            Add-VibeSkillRoutingEntry -Rows $rejectedRows -Seen $rejectedSeen -Entry (New-VibeSkillRoutingEntry -SkillId $skillId -Source $candidate -Reason 'not_selected' -State 'rejected')
        }
    }

    return [pscustomobject]@{
        schema_version = 'simplified_skill_routing_v1'
        candidates = [object[]]$candidateRows.ToArray()
        selected = [object[]]$selectedRows.ToArray()
        rejected = [object[]]$rejectedRows.ToArray()
    }
}

function Get-VibeSkillRoutingSelected {
    param(
        [AllowNull()] [object]$RuntimeInputPacket = $null,
        [AllowNull()] [object]$SkillRouting = $null
    )

    $routing = if ($null -ne $SkillRouting) {
        $SkillRouting
    } elseif ($null -ne $RuntimeInputPacket -and $RuntimeInputPacket.PSObject.Properties.Name -contains 'skill_routing') {
        $RuntimeInputPacket.skill_routing
    } else {
        $null
    }

    if ($null -ne $routing -and $routing.PSObject.Properties.Name -contains 'selected') {
        return @($routing.selected)
    }

    if ($null -ne $RuntimeInputPacket -and $RuntimeInputPacket.PSObject.Properties.Name -contains 'specialist_dispatch' -and $null -ne $RuntimeInputPacket.specialist_dispatch) {
        $dispatch = $RuntimeInputPacket.specialist_dispatch
        if ($dispatch.PSObject.Properties.Name -contains 'approved_dispatch') {
            return @($dispatch.approved_dispatch)
        }
    }

    return @()
}

function Get-VibeSkillRoutingSelectedSkillIds {
    param(
        [AllowNull()] [object]$RuntimeInputPacket = $null,
        [AllowNull()] [object]$SkillRouting = $null
    )

    return [object[]]@(Get-VibeSkillRoutingSelected -RuntimeInputPacket $RuntimeInputPacket -SkillRouting $SkillRouting | ForEach-Object {
        [string](Get-VibeSkillRoutingProperty -InputObject $_ -PropertyName 'skill_id' -DefaultValue '')
    } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
}

function Convert-VibeSkillRoutingSelectedToDispatch {
    param(
        [AllowNull()] [object]$SkillRouting = $null,
        [AllowNull()] [object]$RuntimeInputPacket = $null
    )

    return [object[]]@(Get-VibeSkillRoutingSelected -RuntimeInputPacket $RuntimeInputPacket -SkillRouting $SkillRouting | ForEach-Object {
        $entry = $_
        [pscustomobject]@{
            skill_id = [string]$entry.skill_id
            reason = [string]$entry.reason
            task_slice = [string]$entry.task_slice
            native_skill_entrypoint = $entry.native_skill_entrypoint
            skill_md_path = $entry.skill_md_path
            dispatch_phase = if ($entry.PSObject.Properties.Name -contains 'dispatch_phase') { [string]$entry.dispatch_phase } else { 'in_execution' }
            parallelizable_in_root_xl = if ($entry.PSObject.Properties.Name -contains 'parallelizable_in_root_xl') { [bool]$entry.parallelizable_in_root_xl } else { $false }
            native_usage_required = if ($entry.PSObject.Properties.Name -contains 'native_usage_required') { [bool]$entry.native_usage_required } else { $true }
        }
    })
}

function New-VibeSkillRoutingSummary {
    param(
        [AllowNull()] [object]$SkillRouting = $null,
        [AllowNull()] [object]$SkillUsage = $null
    )

    $usedCount = if ($null -ne $SkillUsage -and $SkillUsage.PSObject.Properties.Name -contains 'used') { @($SkillUsage.used).Count } elseif ($null -ne $SkillUsage -and $SkillUsage.PSObject.Properties.Name -contains 'used_skills') { @($SkillUsage.used_skills).Count } else { 0 }
    $unusedCount = if ($null -ne $SkillUsage -and $SkillUsage.PSObject.Properties.Name -contains 'unused') { @($SkillUsage.unused).Count } elseif ($null -ne $SkillUsage -and $SkillUsage.PSObject.Properties.Name -contains 'unused_skills') { @($SkillUsage.unused_skills).Count } else { 0 }

    return [pscustomobject]@{
        candidate_count = if ($null -ne $SkillRouting -and $SkillRouting.PSObject.Properties.Name -contains 'candidates') { @($SkillRouting.candidates).Count } else { 0 }
        selected_count = if ($null -ne $SkillRouting -and $SkillRouting.PSObject.Properties.Name -contains 'selected') { @($SkillRouting.selected).Count } else { 0 }
        rejected_count = if ($null -ne $SkillRouting -and $SkillRouting.PSObject.Properties.Name -contains 'rejected') { @($SkillRouting.rejected).Count } else { 0 }
        used_count = [int]$usedCount
        unused_count = [int]$unusedCount
    }
}
```

- [ ] **Step 2: Run the focused helper tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_simplified_skill_routing_contract.py::SimplifiedSkillRoutingContractTests::test_helper_builds_candidate_selected_rejected_from_legacy_inputs tests/runtime_neutral/test_simplified_skill_routing_contract.py::SimplifiedSkillRoutingContractTests::test_selected_skill_ids_prefer_skill_routing_over_legacy_dispatch tests/runtime_neutral/test_simplified_skill_routing_contract.py::SimplifiedSkillRoutingContractTests::test_selected_skill_ids_fall_back_to_legacy_only_when_skill_routing_is_absent -q
```

Expected: PASS.

- [ ] **Step 3: Commit the helper**

```powershell
git add scripts/runtime/VibeSkillRouting.Common.ps1
git commit -m "feat: add simplified skill routing helpers"
```

## Task 3: Emit `skill_routing` During Runtime Freeze

**Files:**
- Modify: `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Test: `tests/runtime_neutral/test_simplified_skill_routing_contract.py`

- [ ] **Step 1: Source the routing helper in freeze**

In `scripts/runtime/Freeze-RuntimeInputPacket.ps1`, after the existing `VibeSkillUsage.Common.ps1` import, add:

```powershell
. (Join-Path $PSScriptRoot 'VibeSkillRouting.Common.ps1')
```

- [ ] **Step 2: Build `skill_routing` before `skill_usage`**

In `scripts/runtime/Freeze-RuntimeInputPacket.ps1`, replace the current single-skill load block around `$loadedMainSkill` with:

```powershell
$skillRouting = New-VibeSkillRoutingFromLegacy `
    -RouterSelectedSkill ([string]$routerSelectedSkill) `
    -Recommendations @($specialistRecommendations) `
    -StageAssistantHints @($stageAssistantHints) `
    -SpecialistDispatch $specialistDispatch

$selectedSkillLoads = @()
foreach ($selectedSkill in @(Get-VibeSkillRoutingSelected -SkillRouting $skillRouting)) {
    $selectedSkillId = [string]$selectedSkill.skill_id
    if ([string]::IsNullOrWhiteSpace($selectedSkillId)) {
        continue
    }
    $selectedSkillLoads += New-VibeSkillUsageLoadedSkill `
        -RepoRoot $runtime.repo_root `
        -SkillId $selectedSkillId `
        -LoadedAtStage 'skeleton_check' `
        -TargetRoot $routerTargetRoot `
        -HostId $routerHostId
}

$routingTouchedSkills = @(
    @($skillRouting.candidates | ForEach-Object { [pscustomobject]@{ skill_id = [string]$_.skill_id; reason = 'not_selected' } }) +
    @($skillRouting.selected | ForEach-Object { [pscustomobject]@{ skill_id = [string]$_.skill_id; reason = 'selected_but_no_artifact_impact' } })
)
$skillUsage = New-VibeInitialSkillUsage `
    -LoadedSkills @($selectedSkillLoads) `
    -TouchedSkills @($routingTouchedSkills + @($skillUsageTouched.ToArray()))
```

Then pass the new value into the packet projection:

```powershell
    -SkillRouting $skillRouting `
```

- [ ] **Step 3: Add `SkillRouting` to packet projection**

In `scripts/runtime/VibeRuntime.Common.ps1`, add this parameter to `New-VibeRuntimeInputPacketProjection`:

```powershell
[AllowNull()] [object]$SkillRouting = $null,
```

In the returned packet object, add canonical routing and isolate legacy fields:

```powershell
skill_routing = if ($null -ne $SkillRouting) {
    $SkillRouting
} else {
    [pscustomobject]@{
        schema_version = 'simplified_skill_routing_v1'
        candidates = @()
        selected = @()
        rejected = @()
    }
}
legacy_skill_routing = [pscustomobject]@{
    specialist_recommendations = @($SpecialistRecommendations)
    stage_assistant_hints = @($StageAssistantHints)
    specialist_dispatch = [pscustomobject]@{
        approved_dispatch = [object[]]@($SpecialistDispatch.approved_dispatch)
        local_specialist_suggestions = [object[]]@($SpecialistDispatch.local_specialist_suggestions)
        blocked = @($(if ($SpecialistDispatch.PSObject.Properties.Name -contains 'blocked' -and $null -ne $SpecialistDispatch.blocked) { $SpecialistDispatch.blocked } else { @() }))
        degraded = @($(if ($SpecialistDispatch.PSObject.Properties.Name -contains 'degraded' -and $null -ne $SpecialistDispatch.degraded) { $SpecialistDispatch.degraded } else { @() }))
        promotion_outcomes = @($(if ($SpecialistDispatch.PSObject.Properties.Name -contains 'promotion_outcomes' -and $null -ne $SpecialistDispatch.promotion_outcomes) { $SpecialistDispatch.promotion_outcomes } else { @() }))
    }
}
```

During this task, keep the existing root-level legacy fields so older tests still pass. Removing or moving those root fields happens in Task 7 after delivery acceptance and gate updates are ready.

- [ ] **Step 4: Run the freeze routing test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_simplified_skill_routing_contract.py::SimplifiedSkillRoutingContractTests::test_freeze_emits_skill_routing_with_selected_skills -q
```

Expected: PASS.

- [ ] **Step 5: Run existing binary usage freeze test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_binary_skill_usage_contract.py::BinarySkillUsageContractTests::test_runtime_freeze_emits_initial_binary_skill_usage -q
```

Expected: PASS after updating the test in Task 4 to assert both old and new usage shapes.

- [ ] **Step 6: Commit freeze integration**

```powershell
git add scripts/runtime/Freeze-RuntimeInputPacket.ps1 scripts/runtime/VibeRuntime.Common.ps1 tests/runtime_neutral/test_simplified_skill_routing_contract.py
git commit -m "feat: emit simplified skill routing in freeze"
```

## Task 4: Make `skill_usage.used / unused` The Canonical Shape

**Files:**
- Modify: `scripts/runtime/VibeSkillUsage.Common.ps1`
- Modify: `tests/runtime_neutral/test_binary_skill_usage_contract.py`
- Modify: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`

- [ ] **Step 1: Update usage tests to assert canonical and compatibility fields**

In `tests/runtime_neutral/test_binary_skill_usage_contract.py`, update `test_artifact_impact_promotes_loaded_skill_to_used_and_removes_unused_reason` with these additional assertions:

```python
self.assertEqual(["demo-skill"], [item["skill_id"] for item in payload["used"]])
self.assertEqual([], payload["unused"])
self.assertEqual("demo-skill", payload["used"][0]["skill_id"])
self.assertEqual("xl_plan", payload["used"][0]["evidence"][0]["stage"])
```

Update `test_runtime_freeze_emits_initial_binary_skill_usage` with:

```python
self.assertIn(selected_skill, [item["skill_id"] for item in usage["unused"]])
self.assertIn(
    "selected_but_no_artifact_impact",
    [item["reason"] for item in usage["unused"] if item["skill_id"] == selected_skill],
)
```

- [ ] **Step 2: Update `New-VibeInitialSkillUsage`**

In `scripts/runtime/VibeSkillUsage.Common.ps1`, change the returned object from `New-VibeInitialSkillUsage` so it includes canonical fields:

```powershell
return [pscustomobject]@{
    schema_version = 2
    state_model = 'binary_used_unused'
    used = @()
    unused = [object[]]$unusedRows.ToArray()
    used_skills = @()
    unused_skills = [object[]]@($unusedRows.ToArray() | ForEach-Object { [string]$_.skill_id } | Select-Object -Unique)
    loaded_skills = [object[]]@($loaded)
    evidence = @()
    unused_reasons = [object[]]$unusedRows.ToArray()
}
```

Update the default reason for loaded selected skills from `loaded_but_no_artifact_impact` to:

```powershell
selected_but_no_artifact_impact
```

- [ ] **Step 3: Update `Update-VibeSkillUsageArtifactImpact`**

In the same file, build canonical `used` records and remove the skill from canonical `unused`:

```powershell
$existingUsedRows = if ($SkillUsage.PSObject.Properties.Name -contains 'used') { @($SkillUsage.used) } else { @() }
$existingUnusedRows = if ($SkillUsage.PSObject.Properties.Name -contains 'unused') { @($SkillUsage.unused) } else { @($SkillUsage.unused_reasons) }
$usedRows = @($existingUsedRows | Where-Object { [string]$_.skill_id -ne $SkillId })
$unusedRows = @($existingUnusedRows | Where-Object { [string]$_.skill_id -ne $SkillId })
$impactRecord = [pscustomobject]@{
    stage = $Stage
    artifact_path = $ArtifactRef
    impact = $ImpactSummary
}
$usedRows += [pscustomobject]@{
    skill_id = $SkillId
    skill_md_path = if (@($loadedRecord).Count -gt 0) { [string]$loadedRecord[0].skill_md_path } else { $null }
    skill_md_sha256 = if (@($loadedRecord).Count -gt 0) { [string]$loadedRecord[0].skill_md_sha256 } else { $null }
    evidence = @($impactRecord)
}
```

Return both new and compatibility fields:

```powershell
return [pscustomobject]@{
    schema_version = 2
    state_model = 'binary_used_unused'
    used = [object[]]$usedRows
    unused = [object[]]$unusedRows
    used_skills = [object[]]@($usedRows | ForEach-Object { [string]$_.skill_id } | Select-Object -Unique)
    unused_skills = [object[]]@($unusedRows | ForEach-Object { [string]$_.skill_id } | Select-Object -Unique)
    loaded_skills = [object[]]$loaded
    evidence = [object[]]$evidence
    unused_reasons = [object[]]$unusedRows
}
```

- [ ] **Step 4: Update delivery acceptance usage evaluation**

In `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`, update `_evaluate_skill_usage_truth` to prefer the new shape:

```python
used_rows = list(skill_usage.get("used") or [])
unused_rows = list(skill_usage.get("unused") or [])
used_skill_ids = _normalize_skill_id_list([row.get("skill_id") for row in used_rows] or skill_usage.get("used_skills") or [])
unused_skill_ids = _normalize_skill_id_list([row.get("skill_id") for row in unused_rows] or skill_usage.get("unused_skills") or [])
```

When checking used evidence, accept either the row-level `evidence` array or the legacy top-level `evidence` array:

```python
row_evidence = []
for row in used_rows:
    if str(row.get("skill_id") or "") == skill_id:
        row_evidence.extend(list(row.get("evidence") or []))
skill_evidence = [
    item for item in [*row_evidence, *evidence_records]
    if str(item.get("skill_id") or skill_id) == skill_id
]
```

- [ ] **Step 5: Run usage tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_runtime_delivery_acceptance.py::RuntimeDeliveryAcceptanceTests::test_binary_skill_usage_passes_with_full_load_and_artifact_impact tests/runtime_neutral/test_runtime_delivery_acceptance.py::RuntimeDeliveryAcceptanceTests::test_binary_skill_usage_fails_when_used_skill_lacks_artifact_impact -q
```

Expected: PASS.

- [ ] **Step 6: Commit usage shape migration**

```powershell
git add scripts/runtime/VibeSkillUsage.Common.ps1 tests/runtime_neutral/test_binary_skill_usage_contract.py packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py
git commit -m "feat: make skill usage used unused canonical"
```

## Task 5: Read Selected Skills In Requirement And Plan Stages

**Files:**
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
- Modify: `scripts/runtime/Write-XlPlan.ps1`
- Modify: `scripts/runtime/VibeExecution.Common.ps1`
- Test: `tests/runtime_neutral/test_simplified_skill_routing_contract.py`

- [ ] **Step 1: Source routing helper in requirement and plan scripts**

Add to both `Write-RequirementDoc.ps1` and `Write-XlPlan.ps1` after `VibeSkillUsage.Common.ps1`:

```powershell
. (Join-Path $PSScriptRoot 'VibeSkillRouting.Common.ps1')
```

- [ ] **Step 2: Replace approved-dispatch reads with selected-skill reads**

In `Write-RequirementDoc.ps1`, replace:

```powershell
$approvedSpecialistDispatch = if (
    $runtimeInputPacket.PSObject.Properties.Name -contains 'specialist_dispatch' -and
    $null -ne $runtimeInputPacket.specialist_dispatch -and
    $runtimeInputPacket.specialist_dispatch.PSObject.Properties.Name -contains 'approved_dispatch'
) {
    @($runtimeInputPacket.specialist_dispatch.approved_dispatch)
} else {
    @()
}
```

with:

```powershell
$selectedSkillRouting = @(Get-VibeSkillRoutingSelected -RuntimeInputPacket $runtimeInputPacket)
$approvedSpecialistDispatch = @(Convert-VibeSkillRoutingSelectedToDispatch -RuntimeInputPacket $runtimeInputPacket)
```

Keep the variable name in this task to reduce diff size, but add a nearby comment:

```powershell
# Compatibility variable name; authority is skill_routing.selected.
```

- [ ] **Step 3: Update XL plan topology input**

In `Write-XlPlan.ps1`, replace:

```powershell
$approvedDispatch = if ($runtimeInputPacket -and $runtimeInputPacket.specialist_dispatch) { @($runtimeInputPacket.specialist_dispatch.approved_dispatch) } else { @() }
$localSuggestions = if ($runtimeInputPacket -and $runtimeInputPacket.specialist_dispatch) { @($runtimeInputPacket.specialist_dispatch.local_specialist_suggestions) } else { @() }
```

with:

```powershell
$selectedSkillRouting = @(Get-VibeSkillRoutingSelected -RuntimeInputPacket $runtimeInputPacket)
$approvedDispatch = @(Convert-VibeSkillRoutingSelectedToDispatch -RuntimeInputPacket $runtimeInputPacket)
$localSuggestions = @()
```

Change the plan text lines from `approved_dispatch` wording to selected-skill wording:

```powershell
'- This section lists only skills selected into the six-stage work through `skill_routing.selected`.',
'- Before specialist execution starts, governed `vibe` emits one unified disclosure for selected skills using each skill''s real `skill_md_path` or `native_skill_entrypoint`.',
'- Execution must preserve the loaded skill workflow and report final use only from `skill_usage.used` / `skill_usage.unused`.'
```

- [ ] **Step 4: Add `SelectedSkills` to `New-VibeExecutionTopology`**

In `scripts/runtime/VibeExecution.Common.ps1`, change the function parameters:

```powershell
[AllowEmptyCollection()] [object[]]$ApprovedDispatch = @(),
[AllowEmptyCollection()] [object[]]$SelectedSkills = @()
```

At the top of the function, add:

```powershell
$effectiveSelectedSkills = if (@($SelectedSkills).Count -gt 0) { @($SelectedSkills) } else { @($ApprovedDispatch) }
```

Then replace uses of `$ApprovedDispatch` inside the function with `$effectiveSelectedSkills`, except when writing compatibility field names that existing gates still read.

- [ ] **Step 5: Pass selected skills into topology from XL plan**

In `Write-XlPlan.ps1`, change the topology call:

```powershell
    -ApprovedDispatch @($approvedDispatch)
```

to:

```powershell
    -ApprovedDispatch @()
    -SelectedSkills @($approvedDispatch)
```

- [ ] **Step 6: Run focused plan generation tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_runtime_flow.py::BinarySkillUsageRuntimeFlowTests::test_plan_execute_and_cleanup_preserve_skill_usage_truth -q
```

Expected: PASS.

- [ ] **Step 7: Commit stage routing read migration**

```powershell
git add scripts/runtime/Write-RequirementDoc.ps1 scripts/runtime/Write-XlPlan.ps1 scripts/runtime/VibeExecution.Common.ps1 tests/runtime_neutral/test_simplified_skill_routing_contract.py
git commit -m "feat: drive planning from selected skills"
```

## Task 6: Drive Plan Execute From `skill_routing.selected`

**Files:**
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
- Modify: `scripts/runtime/Invoke-PhaseCleanup.ps1`
- Test: `tests/runtime_neutral/test_binary_skill_usage_runtime_flow.py`
- Test: `tests/runtime_neutral/test_governed_runtime_bridge.py`

- [ ] **Step 1: Source routing helper in execute and cleanup**

Add to `Invoke-PlanExecute.ps1` and `Invoke-PhaseCleanup.ps1` after `VibeSkillUsage.Common.ps1`:

```powershell
. (Join-Path $PSScriptRoot 'VibeSkillRouting.Common.ps1')
```

- [ ] **Step 2: Replace frozen approved-dispatch authority in execute**

In `Invoke-PlanExecute.ps1`, replace the frozen dispatch reads:

```powershell
$frozenApprovedDispatch = if ($runtimeInputPacket -and $runtimeInputPacket.specialist_dispatch) { @($runtimeInputPacket.specialist_dispatch.approved_dispatch) } else { @() }
$frozenLocalSuggestions = if ($runtimeInputPacket -and $runtimeInputPacket.specialist_dispatch) { @($runtimeInputPacket.specialist_dispatch.local_specialist_suggestions) } else { @() }
```

with:

```powershell
$skillRouting = if ($runtimeInputPacket -and $runtimeInputPacket.PSObject.Properties.Name -contains 'skill_routing') {
    $runtimeInputPacket.skill_routing
} else {
    $null
}
$selectedSkills = @(Convert-VibeSkillRoutingSelectedToDispatch -RuntimeInputPacket $runtimeInputPacket -SkillRouting $skillRouting)
$frozenApprovedDispatch = @($selectedSkills)
$frozenLocalSuggestions = @()
```

Keep `$frozenApprovedDispatch` only as a compatibility variable name in this task.

- [ ] **Step 3: Skip auto-absorb when `skill_routing.selected` exists**

Before calling `Resolve-VibeEffectiveSpecialistDispatch`, add:

```powershell
$hasCanonicalSelectedSkills = $null -ne $skillRouting -and @($skillRouting.selected).Count -gt 0
```

If `$hasCanonicalSelectedSkills` is true, set:

```powershell
$approvedDispatch = @($selectedSkills)
$localSuggestions = @()
$autoApprovedDispatch = @()
$specialistDispatchResolution = [pscustomobject]@{
    effective_approved_dispatch = @($selectedSkills)
    residual_local_specialist_suggestions = @()
    auto_approved_dispatch = @()
    auto_absorb_gate = [pscustomobject]@{
        enabled = $false
        receipt_path = $null
        reason = 'skill_routing_selected_is_authority'
    }
}
```

Otherwise keep the existing legacy resolution branch.

- [ ] **Step 4: Add routing summary to execution manifest**

In the execution manifest object, add:

```powershell
skill_routing_path = $runtimeInputPath
skill_routing_summary = New-VibeSkillRoutingSummary -SkillRouting $skillRouting -SkillUsage $skillUsage
selected_skill_ids = @(Get-VibeSkillRoutingSelectedSkillIds -RuntimeInputPacket $runtimeInputPacket -SkillRouting $skillRouting)
```

Keep the current `specialist_accounting` object during this task. Its values should be derived from `$approvedDispatch`, which now comes from selected skills.

- [ ] **Step 5: Add cleanup summary from canonical usage**

In `Invoke-PhaseCleanup.ps1`, change the summary counts to prefer new fields:

```powershell
$skillUsageSummary = [pscustomobject]@{
    used_skill_count = if ($skillUsage -and $skillUsage.PSObject.Properties.Name -contains 'used') { @($skillUsage.used).Count } elseif ($skillUsage) { @($skillUsage.used_skills).Count } else { 0 }
    unused_skill_count = if ($skillUsage -and $skillUsage.PSObject.Properties.Name -contains 'unused') { @($skillUsage.unused).Count } elseif ($skillUsage) { @($skillUsage.unused_skills).Count } else { 0 }
}
```

- [ ] **Step 6: Run runtime flow tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_binary_skill_usage_runtime_flow.py tests/runtime_neutral/test_governed_runtime_bridge.py -q
```

Expected: PASS. If legacy-specific assertions fail, update them to assert `skill_routing.selected` plus compatibility accounting rather than root-level `specialist_dispatch` authority.

- [ ] **Step 7: Commit execute migration**

```powershell
git add scripts/runtime/Invoke-PlanExecute.ps1 scripts/runtime/Invoke-PhaseCleanup.ps1 tests/runtime_neutral/test_binary_skill_usage_runtime_flow.py tests/runtime_neutral/test_governed_runtime_bridge.py
git commit -m "feat: execute selected skills as routing authority"
```

## Task 7: Isolate Legacy Routing Fields And Shrink Primary JSON

**Files:**
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Modify: `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`
- Modify: `tests/runtime_neutral/test_bundled_stage_assistant_freeze.py`
- Modify: `tests/runtime_neutral/test_governed_runtime_bridge.py`
- Modify: `scripts/verify/vibe-canonical-entry-truth-gate.ps1`
- Modify: `scripts/verify/vibe-no-silent-fallback-contract-gate.ps1`
- Modify: `scripts/verify/vibe-root-child-hierarchy-gate.ps1`

- [ ] **Step 1: Add a test that legacy fields are isolated**

In `tests/runtime_neutral/test_simplified_skill_routing_contract.py`, add:

```python
def test_new_freeze_packet_isolates_legacy_specialist_fields(self) -> None:
    shell = resolve_powershell()
    if shell is None:
        self.skipTest("PowerShell executable not available")
    with tempfile.TemporaryDirectory() as tempdir:
        artifact_root = Path(tempdir) / "artifacts"
        subprocess.run(
            [
                shell,
                "-NoLogo",
                "-NoProfile",
                "-File",
                str(FREEZE_SCRIPT),
                "-Task",
                "Use biopython to parse FASTA and summarize sequence lengths.",
                "-Mode",
                "interactive_governed",
                "-RunId",
                "pytest-skill-routing-legacy-isolation",
                "-ArtifactRoot",
                str(artifact_root),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        packet_path = next(artifact_root.rglob("runtime-input-packet.json"))
        packet = json.loads(packet_path.read_text(encoding="utf-8"))

    self.assertIn("skill_routing", packet)
    self.assertIn("legacy_skill_routing", packet)
    self.assertNotIn("stage_assistant_hints", packet)
    self.assertNotIn("specialist_recommendations", packet)
    self.assertNotIn("specialist_dispatch", packet)
    self.assertIn("specialist_recommendations", packet["legacy_skill_routing"])
    self.assertIn("specialist_dispatch", packet["legacy_skill_routing"])
```

- [ ] **Step 2: Remove root legacy fields from packet projection**

In `New-VibeRuntimeInputPacketProjection`, remove these root fields from the returned object:

```powershell
specialist_recommendations = @($SpecialistRecommendations)
stage_assistant_hints = @($StageAssistantHints)
specialist_dispatch = [pscustomobject]@{ ... }
```

Keep the same data under:

```powershell
legacy_skill_routing = [pscustomobject]@{
    specialist_recommendations = @($SpecialistRecommendations)
    stage_assistant_hints = @($StageAssistantHints)
    specialist_dispatch = [pscustomobject]@{ ... }
}
```

- [ ] **Step 3: Update tests that read root legacy fields**

Replace root reads with legacy reads. Example:

```python
legacy = packet["legacy_skill_routing"]
dispatch = legacy["specialist_dispatch"]
recommendations = legacy["specialist_recommendations"]
```

For new authority assertions, use:

```python
selected_ids = [item["skill_id"] for item in packet["skill_routing"]["selected"]]
self.assertIn("scikit-learn", selected_ids)
```

- [ ] **Step 4: Update verification gates**

In each affected PowerShell gate, replace checks for root `specialist_dispatch` with:

```powershell
$hasSkillRouting = Test-ObjectHasProperty -InputObject $runtimeInputPacket -PropertyName 'skill_routing'
$hasLegacyRouting = Test-ObjectHasProperty -InputObject $runtimeInputPacket -PropertyName 'legacy_skill_routing'
Add-Assertion -Assertions $assertions -Pass $hasSkillRouting -Message 'runtime packet exposes canonical skill_routing'
Add-Assertion -Assertions $assertions -Pass $hasLegacyRouting -Message 'runtime packet isolates legacy skill routing'
```

Where a gate needs selected ids, use:

```powershell
$selectedSkillIds = @($runtimeInputPacket.skill_routing.selected | ForEach-Object { [string]$_.skill_id } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
```

- [ ] **Step 5: Run isolation and gate tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_bundled_stage_assistant_freeze.py tests/runtime_neutral/test_governed_runtime_bridge.py -q
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-canonical-entry-truth-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-no-silent-fallback-contract-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-root-child-hierarchy-gate.ps1
```

Expected: PASS.

- [ ] **Step 6: Commit legacy isolation**

```powershell
git add scripts/runtime/VibeRuntime.Common.ps1 tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_bundled_stage_assistant_freeze.py tests/runtime_neutral/test_governed_runtime_bridge.py scripts/verify/vibe-canonical-entry-truth-gate.ps1 scripts/verify/vibe-no-silent-fallback-contract-gate.ps1 scripts/verify/vibe-root-child-hierarchy-gate.ps1
git commit -m "refactor: isolate legacy skill routing fields"
```

## Task 8: Update Delivery Acceptance To Treat Selected Skills As Authority

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`
- Modify: `tests/runtime_neutral/test_runtime_delivery_acceptance.py`

- [ ] **Step 1: Add selected-skill fixture support**

In `tests/runtime_neutral/test_runtime_delivery_acceptance.py`, update the helper method signature:

```python
skill_routing: dict[str, object] | None = None,
```

When building `runtime_input_packet_payload`, add:

```python
if skill_routing is not None:
    runtime_input_packet_payload["skill_routing"] = skill_routing
```

- [ ] **Step 2: Add acceptance test for legacy dispatch not being authority**

Add this test:

```python
def test_legacy_dispatch_without_skill_routing_selected_does_not_count_as_selected(self) -> None:
    report = self.run_acceptance(
        approved_dispatch=[
            {
                "skill_id": "scanpy",
                "native_skill_entrypoint": "bundled/skills/scanpy/SKILL.md",
            }
        ],
        skill_routing={"candidates": [], "selected": [], "rejected": []},
        skill_usage={"schema_version": 2, "state_model": "binary_used_unused", "used": [], "unused": []},
    )

    self.assertEqual("PASS", report["skill_usage_truth"]["state"])
    self.assertEqual([], report["execution_context"]["selected_skill_ids"])
```

- [ ] **Step 3: Add acceptance test for selected skill missing load evidence**

Add:

```python
def test_selected_skill_without_load_evidence_fails_usage_truth(self) -> None:
    report = self.run_acceptance(
        skill_routing={
            "candidates": [{"skill_id": "scanpy"}],
            "selected": [{"skill_id": "scanpy", "skill_md_path": "bundled/skills/scanpy/SKILL.md"}],
            "rejected": [],
        },
        skill_usage={
            "schema_version": 2,
            "state_model": "binary_used_unused",
            "used": [],
            "unused": [{"skill_id": "scanpy", "reason": "selected_but_not_loaded"}],
            "loaded_skills": [],
        },
    )

    self.assertEqual("FAIL", report["skill_usage_truth"]["state"])
    self.assertIn("selected_skill_missing_load_evidence", report["skill_usage_truth"]["failure_reasons"])
```

- [ ] **Step 4: Implement selected-skill extraction in delivery acceptance**

In `runtime_delivery_acceptance_runtime.py`, after loading `runtime_input_packet`, add:

```python
skill_routing = runtime_input_packet.get("skill_routing") or {}
selected_skill_ids = _normalize_skill_id_list(
    [item.get("skill_id") for item in (skill_routing.get("selected") or [])]
)
```

Only if `skill_routing` is absent, fall back:

```python
if not skill_routing:
    selected_skill_ids = approved_dispatch_skill_ids
```

Add `selected_skill_ids` to `execution_context`.

- [ ] **Step 5: Enforce selected-skill load evidence**

In `_evaluate_skill_usage_truth`, accept an optional `selected_skill_ids` argument and add:

```python
loaded_skill_ids = _normalize_skill_id_list([item.get("skill_id") for item in loaded_records])
for skill_id in selected_skill_ids:
    if skill_id not in loaded_skill_ids:
        failure_reasons.append("selected_skill_missing_load_evidence")
```

Keep the current used-skill evidence checks.

- [ ] **Step 6: Run delivery acceptance tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_runtime_delivery_acceptance.py::RuntimeDeliveryAcceptanceTests::test_legacy_dispatch_without_skill_routing_selected_does_not_count_as_selected tests/runtime_neutral/test_runtime_delivery_acceptance.py::RuntimeDeliveryAcceptanceTests::test_selected_skill_without_load_evidence_fails_usage_truth tests/runtime_neutral/test_runtime_delivery_acceptance.py::RuntimeDeliveryAcceptanceTests::test_approved_dispatch_without_skill_usage_does_not_count_as_used -q
```

Expected: PASS.

- [ ] **Step 7: Commit delivery acceptance migration**

```powershell
git add packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py tests/runtime_neutral/test_runtime_delivery_acceptance.py
git commit -m "test: enforce selected skill usage authority"
```

## Task 9: Add Pack Manifest `skill_candidates` Compatibility

**Files:**
- Modify: `config/pack-manifest.json`
- Modify: router code that reads `route_authority_candidates` / `stage_assistant_candidates`
- Test: add or update the closest routing audit test that loads `config/pack-manifest.json`

- [ ] **Step 1: Add a manifest test for unified candidates**

Create or update a runtime-neutral manifest test with this assertion:

```python
for pack in manifest["packs"]:
    skill_candidates = set(pack.get("skill_candidates") or [])
    old_route = set(pack.get("route_authority_candidates") or [])
    old_stage = set(pack.get("stage_assistant_candidates") or [])
    self.assertTrue(skill_candidates)
    self.assertTrue(old_route.union(old_stage).issubset(skill_candidates))
```

- [ ] **Step 2: Generate `skill_candidates` as union of old fields**

For each pack in `config/pack-manifest.json`, add:

```json
"skill_candidates": [
  "... union of route_authority_candidates and stage_assistant_candidates ..."
]
```

Do not remove the old config fields in this task. They become legacy config until pack-specific tests are updated.

- [ ] **Step 3: Make router prefer `skill_candidates`**

In the router code path that enumerates pack candidates, change the source priority to:

```text
skill_candidates
fallback: route_authority_candidates + stage_assistant_candidates
```

The routing result should no longer classify candidates as route authority or stage assistant for execution. If the router still records old classification for audit, write it only as `legacy_role`.

- [ ] **Step 4: Run routing manifest tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_global_pack_consolidation_audit.py tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
```

Expected: PASS after updating expected manifest rows to include `skill_candidates`.

- [ ] **Step 5: Run pack gates**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
```

Expected: PASS.

- [ ] **Step 6: Commit pack manifest compatibility**

```powershell
git add config/pack-manifest.json tests/runtime_neutral/test_global_pack_consolidation_audit.py tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py
git commit -m "refactor: add unified skill candidates to packs"
```

## Task 10: Full Verification And Documentation

**Files:**
- Create: `docs/governance/simplified-skill-routing-2026-04-29.md`
- Modify: `docs/superpowers/specs/2026-04-29-simplified-skill-routing-design.md` only if implementation reveals a precise correction.

- [ ] **Step 1: Write governance note**

Create `docs/governance/simplified-skill-routing-2026-04-29.md`:

````markdown
# Simplified Skill Routing Governance Note

Date: 2026-04-29

## Decision

Expert skill routing now has one execution authority:

```text
skill_routing.selected
```

Final usage claims have one authority:

```text
skill_usage.used / skill_usage.unused
```

## Deprecated Authority

The following fields are legacy-only and cannot drive new execution decisions:

- `specialist_recommendations`
- `stage_assistant_hints`
- `specialist_dispatch.approved_dispatch`
- `specialist_dispatch.local_specialist_suggestions`
- `consultation_bucket`
- `promotion_state`
- `primary`
- `stage_assistant`

## Runtime Rule

Selected skills must be attempted, loaded from full `SKILL.md`, and recorded as `used` only when artifact impact evidence exists.

## Compatibility

Legacy routing data may remain under `legacy_skill_routing` for old artifact interpretation and migration tests. It is non-authoritative.
```
````

- [ ] **Step 2: Run focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_binary_skill_usage_runtime_flow.py tests/runtime_neutral/test_runtime_delivery_acceptance.py -q
```

Expected: PASS.

- [ ] **Step 3: Run broader runtime tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_bundled_stage_assistant_freeze.py -q
```

Expected: PASS.

- [ ] **Step 4: Run verification gates**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-governed-runtime-contract-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-runtime-execution-proof-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

Expected: all gates PASS and `git diff --check` has no output.

- [ ] **Step 5: Commit governance note**

```powershell
git add docs/governance/simplified-skill-routing-2026-04-29.md docs/superpowers/specs/2026-04-29-simplified-skill-routing-design.md
git commit -m "docs: record simplified skill routing governance"
```

## Implementation Notes

- Use `skill_routing.selected` for all new execution decisions.
- Use legacy fields only when reading artifacts that do not contain `skill_routing`.
- Keep old compatibility fields in `skill_usage` until all delivery acceptance and runtime gates use the new `used / unused` arrays.
- Do not delete skill directories in this implementation.
- Do not change canonical `$vibe` / `/vibe` launch behavior.
- If a verification gate still expects `specialist_dispatch`, update the gate to assert `skill_routing` first and `legacy_skill_routing` only as historical context.
