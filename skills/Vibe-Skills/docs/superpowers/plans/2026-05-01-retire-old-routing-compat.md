# Retire Old Routing Compatibility Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retire old routing-format adaptation so current runtime behavior depends only on `skill_routing.selected` and `skill_usage.used / skill_usage.unused`.

**Architecture:** Add failing retirement tests first, then remove old-format fallbacks from selection, runtime packet generation, generated docs, and current-routing scans. Current execution internals may still use existing names such as `specialist_dispatch`, but any such data must be derived from `skill_routing.selected`, not from old packet fields.

**Tech Stack:** PowerShell runtime scripts, Python `unittest` / `pytest`, Markdown governance docs, existing Vibe verification gates.

---

## File Structure

- Create: `tests/runtime_neutral/test_retired_old_routing_compat.py`
  - Tests that old routing packet fields are ignored and new runtime packets do
    not emit `legacy_skill_routing`.
- Modify: `scripts/runtime/VibeSkillRouting.Common.ps1`
  - Remove selection fallback from old top-level `specialist_dispatch`.
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
  - Stop emitting `legacy_skill_routing`.
  - Make current specialist recommendation / dispatch projection helpers derive
    from `skill_routing.selected`.
  - Stop reading old `legacy_skill_routing`, old `specialist_recommendations`,
    and old `stage_assistant_hints`.
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
  - Remove old consultation receipt loading and `## Specialist Consultation`
    rendering from current requirement docs.
- Modify: `scripts/runtime/Write-XlPlan.ps1`
  - Remove old consultation receipt loading and `## Specialist Consultation`
    rendering from current XL plans.
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`
  - Stop creating or passing discussion/planning consultation receipts in
    current runtime launch.
- Modify: `scripts/runtime/VibeConsultation.Common.ps1`
  - Retire old consultation compatibility as a fail-closed legacy entrypoint or
    delete the file after current imports are removed.
- Modify: `docs/governance/current-routing-contract.md`
  - Change legacy wording from compatibility to retired old-format fields.
- Modify: `scripts/verify/vibe-current-routing-contract-scan.ps1`
  - Extend the scan to fail on current-runtime old-format fallback reads and
    old compatibility packet emission.
- Modify: `tests/runtime_neutral/test_current_routing_contract_cleanup.py`
  - Update assertions from "legacy fields boxed" to "legacy fields absent".
- Modify: `tests/runtime_neutral/test_current_routing_contract_scan.py`
  - Assert new scan counters.
- Modify: `tests/runtime_neutral/test_simplified_skill_routing_contract.py`
  - Replace old fallback expectations with retired old-format expectations.
- Modify or delete: `tests/runtime_neutral/test_vibe_specialist_consultation.py`
  - Remove old consultation receipt readability coverage. Keep only current
    default-off / retired behavior coverage.
- Modify current execution tests only when they assert old-format packet fields:
  - `tests/runtime_neutral/test_bundled_stage_assistant_freeze.py`
  - `tests/runtime_neutral/test_custom_admission_bridge.py`
  - `tests/runtime_neutral/test_governed_runtime_bridge.py`
  - `tests/runtime_neutral/test_l_xl_native_execution_topology.py`
  - `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`
  - `tests/runtime_neutral/test_installed_host_runtime_simulation.py`

Do not change pack routing config in this plan unless a current-format test
proves a pack config regression.

---

### Task 1: Add Old-Format Retirement Contract Tests

**Files:**
- Create: `tests/runtime_neutral/test_retired_old_routing_compat.py`

- [ ] **Step 1: Create the failing test file**

Create `tests/runtime_neutral/test_retired_old_routing_compat.py` with:

```python
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "invoke-vibe-runtime.ps1"
RUNTIME_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeRuntime.Common.ps1"
SKILL_ROUTING_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeSkillRouting.Common.ps1"

CURRENT_TASK = (
    "Build a scikit-learn classification baseline, include a result figure, "
    "and report selected skills and skill_usage evidence."
)


def resolve_powershell() -> str | None:
    candidates = [
        shutil.which("pwsh"),
        shutil.which("pwsh.exe"),
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        r"C:\Program Files\PowerShell\7-preview\pwsh.exe",
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


def run_runtime(task: str, artifact_root: Path) -> dict[str, object]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available")

    run_id = "pytest-retired-routing-compat-" + uuid.uuid4().hex[:10]
    completed = subprocess.run(
        [
            shell,
            "-NoLogo",
            "-NoProfile",
            "-Command",
            (
                "& { "
                f"$result = & {ps_quote(str(RUNTIME_SCRIPT))} "
                f"-Task {ps_quote(task)} "
                "-Mode interactive_governed "
                f"-RunId {ps_quote(run_id)} "
                f"-ArtifactRoot {ps_quote(str(artifact_root))}; "
                "$result | ConvertTo-Json -Depth 20 }"
            ),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        env={
            **os.environ,
            "VGO_DISABLE_NATIVE_SPECIALIST_EXECUTION": "1",
            "VGO_ENABLE_NATIVE_SPECIALIST_EXECUTION": "0",
            "VGO_SPECIALIST_CONSULTATION_MODE": "",
            "VGO_NATIVE_SPECIALIST_EXECUTION_MODE": "",
        },
    )
    return json.loads(completed.stdout)


def as_list(value: object) -> list[object]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


class RetiredOldRoutingCompatibilityTests(unittest.TestCase):
    def test_current_selection_ignores_old_top_level_specialist_dispatch(self) -> None:
        payload = run_ps_json(
            "& { "
            f". {ps_quote(str(RUNTIME_COMMON))}; "
            f". {ps_quote(str(SKILL_ROUTING_COMMON))}; "
            "$packet = [pscustomobject]@{ "
            "specialist_dispatch = [pscustomobject]@{ approved_dispatch = @([pscustomobject]@{ skill_id = 'legacy-only' }) } "
            "}; "
            "$ids = Get-VibeSkillRoutingSelectedSkillIds -RuntimeInputPacket $packet; "
            "[pscustomobject]@{ selected_skill_ids = @($ids) } | ConvertTo-Json -Depth 20 "
            "}"
        )

        self.assertEqual([], as_list(payload["selected_skill_ids"]))

    def test_current_selection_ignores_legacy_skill_routing_container(self) -> None:
        payload = run_ps_json(
            "& { "
            f". {ps_quote(str(RUNTIME_COMMON))}; "
            f". {ps_quote(str(SKILL_ROUTING_COMMON))}; "
            "$packet = [pscustomobject]@{ "
            "legacy_skill_routing = [pscustomobject]@{ "
            "specialist_recommendations = @([pscustomobject]@{ skill_id = 'legacy-recommendation' }); "
            "stage_assistant_hints = @([pscustomobject]@{ skill_id = 'legacy-helper' }); "
            "specialist_dispatch = [pscustomobject]@{ approved_dispatch = @([pscustomobject]@{ skill_id = 'legacy-dispatch' }) } "
            "} "
            "}; "
            "$ids = Get-VibeSkillRoutingSelectedSkillIds -RuntimeInputPacket $packet; "
            "$projection = Get-VibeRuntimeSpecialistDispatchProjection -RuntimeInputPacket $packet; "
            "$recommendations = @(Get-VibeRuntimeSpecialistRecommendations -RuntimeInputPacket $packet); "
            "$hints = @(Get-VibeRuntimeStageAssistantHints -RuntimeInputPacket $packet); "
            "[pscustomobject]@{ "
            "selected_skill_ids = @($ids); "
            "dispatch_is_null = ($null -eq $projection); "
            "recommendation_count = @($recommendations).Count; "
            "hint_count = @($hints).Count "
            "} | ConvertTo-Json -Depth 20 "
            "}"
        )

        self.assertEqual([], as_list(payload["selected_skill_ids"]))
        self.assertTrue(bool(payload["dispatch_is_null"]))
        self.assertEqual(0, int(payload["recommendation_count"]))
        self.assertEqual(0, int(payload["hint_count"]))

    def test_new_runtime_packet_does_not_emit_old_routing_compatibility_box(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            payload = run_runtime(CURRENT_TASK, Path(tempdir))
            packet_path = Path(payload["summary"]["artifacts"]["runtime_input_packet"])
            packet = json.loads(packet_path.read_text(encoding="utf-8"))

        self.assertIn("skill_routing", packet)
        self.assertIn("skill_usage", packet)
        self.assertNotIn("legacy_skill_routing", packet)
        self.assertNotIn("specialist_recommendations", packet)
        self.assertNotIn("stage_assistant_hints", packet)

    def test_new_runtime_generated_docs_do_not_emit_specialist_consultation_section(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            payload = run_runtime(CURRENT_TASK, Path(tempdir))
            artifacts = payload["summary"]["artifacts"]
            requirement_doc = Path(artifacts["requirement_doc"]).read_text(encoding="utf-8")
            execution_plan = Path(artifacts["execution_plan"]).read_text(encoding="utf-8")
            host_briefing = Path(artifacts["host_user_briefing"]).read_text(encoding="utf-8")

        for label, text in {
            "requirement_doc": requirement_doc,
            "execution_plan": execution_plan,
            "host_briefing": host_briefing,
        }.items():
            self.assertNotIn("## Specialist Consultation", text, msg=label)
            self.assertIn("skill_usage", text, msg=label)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new tests and verify red state**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_retired_old_routing_compat.py -q
```

Expected: at least two tests fail because current code still falls back from
old top-level `specialist_dispatch` and still emits `legacy_skill_routing`.

Do not commit this red state.

---

### Task 2: Remove Old Selection Fallback And Legacy Packet Output

**Files:**
- Modify: `scripts/runtime/VibeSkillRouting.Common.ps1`
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Modify: `tests/runtime_neutral/test_current_routing_contract_cleanup.py`
- Modify: `tests/runtime_neutral/test_simplified_skill_routing_contract.py`
- Test: `tests/runtime_neutral/test_retired_old_routing_compat.py`

- [ ] **Step 1: Remove old top-level dispatch fallback from selection**

In `scripts/runtime/VibeSkillRouting.Common.ps1`, replace
`Get-VibeSkillRoutingSelected` with:

```powershell
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

    return @()
}
```

- [ ] **Step 2: Stop emitting `legacy_skill_routing` in runtime packets**

In `scripts/runtime/VibeRuntime.Common.ps1`, inside
`New-VibeRuntimeInputPacketProjection`, remove this property from the returned
packet object:

```powershell
legacy_skill_routing = [pscustomobject]@{
    specialist_recommendations = @($SpecialistRecommendations)
    stage_assistant_hints = @($StageAssistantHints)
    specialist_dispatch = $specialistDispatchProjection
}
```

Keep `skill_routing` and `skill_usage` unchanged.

- [ ] **Step 3: Update current contract packet test**

In `tests/runtime_neutral/test_current_routing_contract_cleanup.py`, rename
`test_runtime_packet_keeps_legacy_fields_boxed_under_legacy_skill_routing` to:

```python
    def test_runtime_packet_does_not_emit_old_routing_compatibility_fields(self) -> None:
```

Replace the body with:

```python
        with tempfile.TemporaryDirectory() as tempdir:
            payload = run_runtime(CURRENT_TASK, Path(tempdir))
            packet_path = Path(payload["summary"]["artifacts"]["runtime_input_packet"])
            packet = load_json(packet_path)

            self.assertIn("skill_routing", packet)
            self.assertIn("skill_usage", packet)
            self.assertNotIn("legacy_skill_routing", packet)
            self.assertNotIn("specialist_recommendations", packet)
            self.assertNotIn("specialist_dispatch", packet)
            self.assertNotIn("stage_assistant_hints", packet)
```

- [ ] **Step 4: Update simplified routing tests that expected old fallback**

In `tests/runtime_neutral/test_simplified_skill_routing_contract.py`, rename
`test_selected_skill_ids_fall_back_to_legacy_only_when_skill_routing_is_absent`
to:

```python
    def test_selected_skill_ids_ignore_old_dispatch_when_skill_routing_is_absent(self) -> None:
```

Keep the PowerShell setup, but change the final assertion to:

```python
        self.assertEqual([], as_list(payload["selected_skill_ids"]))
```

Delete `test_stage_assistant_hint_reader_still_reads_old_legacy_container`.

In `test_new_freeze_packet_isolates_legacy_specialist_fields`, rename it to:

```python
    def test_new_freeze_packet_omits_old_routing_compatibility_fields(self) -> None:
```

Replace the assertions after `packet = ...` with:

```python
        self.assertIn("skill_routing", packet)
        self.assertIn("skill_usage", packet)
        self.assertNotIn("legacy_skill_routing", packet)
        self.assertNotIn("stage_assistant_hints", packet)
        self.assertNotIn("specialist_recommendations", packet)
        self.assertNotIn("specialist_dispatch", packet)
```

- [ ] **Step 5: Run targeted packet and selection tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_retired_old_routing_compat.py::RetiredOldRoutingCompatibilityTests::test_current_selection_ignores_old_top_level_specialist_dispatch tests/runtime_neutral/test_retired_old_routing_compat.py::RetiredOldRoutingCompatibilityTests::test_new_runtime_packet_does_not_emit_old_routing_compatibility_box tests/runtime_neutral/test_current_routing_contract_cleanup.py::CurrentRoutingContractCleanupTests::test_runtime_packet_does_not_emit_old_routing_compatibility_fields tests/runtime_neutral/test_simplified_skill_routing_contract.py::SimplifiedSkillRoutingContractTests::test_selected_skill_ids_ignore_old_dispatch_when_skill_routing_is_absent tests/runtime_neutral/test_simplified_skill_routing_contract.py::SimplifiedSkillRoutingContractTests::test_new_freeze_packet_omits_old_routing_compatibility_fields -q
```

Expected: all selected packet and selection tests pass. The helper test
`test_current_selection_ignores_legacy_skill_routing_container` is handled in
Task 3 because it requires changing `VibeRuntime.Common.ps1` helper readers.

- [ ] **Step 6: Commit packet and selection cleanup**

Run:

```powershell
git add scripts/runtime/VibeSkillRouting.Common.ps1 scripts/runtime/VibeRuntime.Common.ps1 tests/runtime_neutral/test_retired_old_routing_compat.py tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_simplified_skill_routing_contract.py
git commit -m "fix: retire old routing packet fallback"
```

Expected: commit succeeds only after the packet and selection tests named in
Step 5 pass. Do not include Task 3 helper-reader changes in this commit.

---

### Task 3: Rebase Runtime Specialist Projections On Current Routing

**Files:**
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1` only if tests show direct
  old-field assumptions after the helper change.
- Modify: `tests/runtime_neutral/test_retired_old_routing_compat.py`
- Test: `tests/runtime_neutral/test_retired_old_routing_compat.py`
- Test: `tests/runtime_neutral/test_runtime_route_output_shape.py`

- [ ] **Step 1: Replace old helper readers with current-derived projections**

In `scripts/runtime/VibeRuntime.Common.ps1`, replace
`Get-VibeRuntimeLegacySkillRouting`, `Get-VibeRuntimeSpecialistDispatchProjection`,
`Get-VibeRuntimeSpecialistRecommendations`, and
`Get-VibeRuntimeStageAssistantHints` with:

```powershell
function Get-VibeRuntimeSpecialistDispatchProjection {
    param(
        [AllowNull()] [object]$RuntimeInputPacket = $null
    )

    if (
        $null -ne $RuntimeInputPacket -and
        (Test-VibeObjectHasProperty -InputObject $RuntimeInputPacket -PropertyName 'specialist_dispatch') -and
        $null -ne $RuntimeInputPacket.specialist_dispatch
    ) {
        return $RuntimeInputPacket.specialist_dispatch
    }

    $approvedDispatch = @(Convert-VibeSkillRoutingSelectedToDispatch -RuntimeInputPacket $RuntimeInputPacket)
    if (@($approvedDispatch).Count -eq 0) {
        return $null
    }

    return [pscustomobject]@{
        approved_dispatch = [object[]]@($approvedDispatch)
        local_specialist_suggestions = @()
        blocked = @()
        degraded = @()
        approved_skill_ids = @($approvedDispatch | ForEach-Object { [string]$_.skill_id } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
        local_suggestion_skill_ids = @()
        blocked_skill_ids = @()
        degraded_skill_ids = @()
        surfaced_skill_ids = @($approvedDispatch | ForEach-Object { [string]$_.skill_id } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
        matched_skill_ids = @($approvedDispatch | ForEach-Object { [string]$_.skill_id } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
        status = 'derived_from_skill_routing_selected'
        source = 'skill_routing.selected'
    }
}

function Get-VibeRuntimeSpecialistRecommendations {
    param(
        [AllowNull()] [object]$RuntimeInputPacket = $null
    )

    $selected = @(Get-VibeSkillRoutingSelected -RuntimeInputPacket $RuntimeInputPacket)
    if (@($selected).Count -gt 0) {
        return [object[]]@($selected)
    }

    if (
        $null -ne $RuntimeInputPacket -and
        (Test-VibeObjectHasProperty -InputObject $RuntimeInputPacket -PropertyName 'skill_routing') -and
        $null -ne $RuntimeInputPacket.skill_routing -and
        (Test-VibeObjectHasProperty -InputObject $RuntimeInputPacket.skill_routing -PropertyName 'candidates')
    ) {
        return [object[]]@($RuntimeInputPacket.skill_routing.candidates)
    }

    return @()
}

function Get-VibeRuntimeStageAssistantHints {
    param(
        [AllowNull()] [object]$RuntimeInputPacket = $null
    )

    return @()
}
```

This keeps current execution code working while removing reads from
`legacy_skill_routing`, old top-level `specialist_recommendations`, and old
top-level `stage_assistant_hints`.

- [ ] **Step 2: Run helper-specific tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_retired_old_routing_compat.py::RetiredOldRoutingCompatibilityTests::test_current_selection_ignores_legacy_skill_routing_container -q
```

Expected: PASS.

- [ ] **Step 3: Run current route shape tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_runtime_route_output_shape.py tests/runtime_neutral/test_simplified_skill_routing_contract.py -q
```

Expected: all selected tests pass. If a test fails because it expects
`legacy_skill_routing`, rewrite that assertion to the retired format:

```python
self.assertNotIn("legacy_skill_routing", packet)
```

- [ ] **Step 4: Commit current-derived helper projection**

Run:

```powershell
git add scripts/runtime/VibeRuntime.Common.ps1 scripts/runtime/Invoke-PlanExecute.ps1 tests/runtime_neutral/test_retired_old_routing_compat.py tests/runtime_neutral/test_runtime_route_output_shape.py tests/runtime_neutral/test_simplified_skill_routing_contract.py
git commit -m "fix: derive specialist projections from selected skills"
```

Expected: commit succeeds.

---

### Task 4: Remove Consultation Rendering From Current Generated Docs

**Files:**
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
- Modify: `scripts/runtime/Write-XlPlan.ps1`
- Modify: `tests/runtime_neutral/test_current_routing_contract_cleanup.py`
- Modify: `tests/runtime_neutral/test_retired_old_routing_compat.py`
- Test: `tests/runtime_neutral/test_active_consultation_simplification.py`

- [ ] **Step 1: Remove requirement-doc consultation section**

In `scripts/runtime/Write-RequirementDoc.ps1`, delete the entire block that
starts with:

```powershell
if ($discussionConsultation -and [bool]$discussionConsultation.enabled) {
```

and ends immediately before:

```powershell
$lifecycleLines = Get-VibeSpecialistLifecycleDisclosureMarkdownLines `
```

Then change the lifecycle include list in the requirement doc from:

```powershell
-IncludeLayerIds @('discussion_routing', 'discussion_consultation')
```

to:

```powershell
-IncludeLayerIds @('discussion_routing')
```

- [ ] **Step 2: Remove XL-plan consultation section**

In `scripts/runtime/Write-XlPlan.ps1`, delete the entire block that starts with:

```powershell
if ($planningConsultation -and [bool]$planningConsultation.enabled) {
```

and ends immediately before:

```powershell
$currentLifecycleLayerIds = @('discussion_routing')
```

Then replace the lifecycle layer-id setup:

```powershell
$currentLifecycleLayerIds = @('discussion_routing')
if ($discussionConsultation) {
    $currentLifecycleLayerIds += 'discussion_consultation'
}
if ($planningConsultation) {
    $currentLifecycleLayerIds += 'planning_consultation'
}
```

with:

```powershell
$currentLifecycleLayerIds = @('discussion_routing')
```

- [ ] **Step 3: Remove consultation receipt path outputs from current doc receipts**

In `scripts/runtime/Write-RequirementDoc.ps1`, remove this output property from
the receipt object:

```powershell
discussion_consultation_path = if ($discussionConsultation) { $DiscussionConsultationPath } else { $null }
```

In `scripts/runtime/Write-XlPlan.ps1`, remove this output property from the
receipt object:

```powershell
planning_consultation_path = if ($planningConsultation) { $PlanningConsultationPath } else { $null }
```

- [ ] **Step 4: Run generated-doc tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_retired_old_routing_compat.py tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_active_consultation_simplification.py -q
```

Expected: all selected tests pass and no generated doc contains
`## Specialist Consultation`.

- [ ] **Step 5: Commit document rendering retirement**

Run:

```powershell
git add scripts/runtime/Write-RequirementDoc.ps1 scripts/runtime/Write-XlPlan.ps1 tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_retired_old_routing_compat.py tests/runtime_neutral/test_active_consultation_simplification.py
git commit -m "fix: remove old consultation sections from current docs"
```

Expected: commit succeeds.

---

### Task 5: Retire Consultation Runtime Entrypoint From Current Launch

**Files:**
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`
- Modify: `scripts/runtime/VibeConsultation.Common.ps1`
- Modify or delete: `tests/runtime_neutral/test_vibe_specialist_consultation.py`
- Modify: `tests/runtime_neutral/test_governed_runtime_bridge.py`
- Modify: `tests/runtime_neutral/test_l_xl_native_execution_topology.py`

- [ ] **Step 1: Remove current launch import of consultation runtime**

In `scripts/runtime/invoke-vibe-runtime.ps1`, remove:

```powershell
. (Join-Path $PSScriptRoot 'VibeConsultation.Common.ps1')
```

Then remove code paths that call these functions:

```powershell
Invoke-VibeSpecialistConsultationWindow
New-VibeSpecialistConsultationLifecycleLayerProjection
New-VibeHostUserBriefingSegmentProjection -ConsultationReceipt
```

Do not remove current host briefing generation for selected skills or execution
continuation.

- [ ] **Step 2: Stop passing consultation paths to doc writers**

In `scripts/runtime/invoke-vibe-runtime.ps1`, remove these argument assignments:

```powershell
$requirementArgs.DiscussionConsultationPath = [string]$discussionConsultation.receipt_path
$planArgs.DiscussionConsultationPath = [string]$discussionConsultation.receipt_path
$planArgs.PlanningConsultationPath = [string]$planningConsultation.receipt_path
```

Also remove summary artifact assignments for:

```text
discussion_specialist_consultation
planning_specialist_consultation
```

Expected current artifact maps should omit those keys or keep them absent. Do
not set them to paths.

- [ ] **Step 3: Replace consultation runtime with retired fail-closed stub**

Replace `scripts/runtime/VibeConsultation.Common.ps1` with:

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script:VibeConsultationCompatibilityBoundary = 'retired_old_routing_compat'

function Invoke-VibeRetiredConsultationCompatibility {
    throw 'Old specialist consultation compatibility is retired. Current runtime uses skill_routing.selected plus skill_usage.used / skill_usage.unused.'
}
```

This preserves a clear error for accidental direct imports without maintaining
old receipt parsing.

- [ ] **Step 4: Replace old consultation tests with retired behavior tests**

In `tests/runtime_neutral/test_vibe_specialist_consultation.py`, delete tests
that call old consultation receipt parsing or live consultation windows. Keep or
create these two tests:

```python
class VibeSpecialistConsultationTests(unittest.TestCase):
    def test_consultation_module_declares_retired_old_routing_boundary(self) -> None:
        text = CONSULTATION_SCRIPT.read_text(encoding="utf-8")

        self.assertIn("retired_old_routing_compat", text)
        self.assertIn("Old specialist consultation compatibility is retired", text)
        self.assertIn("skill_routing.selected", text)
        self.assertIn("skill_usage.used / skill_usage.unused", text)

    def test_runtime_keeps_freeze_green_without_default_consultation(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            payload = run_runtime(SPECIALIST_TASK, Path(tempdir))
            artifacts = payload["summary"]["artifacts"]
            session_root = Path(payload["session_root"])

            self.assertIsNone(artifacts.get("discussion_specialist_consultation"))
            self.assertIsNone(artifacts.get("planning_specialist_consultation"))
            self.assertEqual([], sorted(path.name for path in session_root.glob("*specialist-consultation*.json")))
```

Keep helper functions used by the retained tests. Delete unused helpers after
the old tests are removed.

- [ ] **Step 5: Update tests that expected consultation sections**

In `tests/runtime_neutral/test_governed_runtime_bridge.py` and
`tests/runtime_neutral/test_l_xl_native_execution_topology.py`, replace any
assertion that expects:

```python
self.assertIn("## Specialist Consultation", execution_plan)
```

with:

```python
self.assertNotIn("## Specialist Consultation", execution_plan)
self.assertIn("## Binary Skill Usage Plan", execution_plan)
```

If a test expected `discussion_specialist_consultation` or
`planning_specialist_consultation` artifact paths, replace those assertions
with:

```python
self.assertIsNone(artifacts.get("discussion_specialist_consultation"))
self.assertIsNone(artifacts.get("planning_specialist_consultation"))
```

- [ ] **Step 6: Run consultation retirement tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_l_xl_native_execution_topology.py -q
```

Expected: all selected tests pass. Any failure that depends on old receipt
readability should be rewritten to retired behavior.

- [ ] **Step 7: Commit consultation runtime retirement**

Run:

```powershell
git add scripts/runtime/invoke-vibe-runtime.ps1 scripts/runtime/VibeConsultation.Common.ps1 tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_l_xl_native_execution_topology.py
git commit -m "fix: retire old consultation compatibility runtime"
```

Expected: commit succeeds.

---

### Task 6: Update Governance Contract And Retirement Scan

**Files:**
- Modify: `docs/governance/current-routing-contract.md`
- Modify: `scripts/verify/vibe-current-routing-contract-scan.ps1`
- Modify: `tests/runtime_neutral/test_current_routing_contract_scan.py`
- Test: `tests/runtime_neutral/test_current_routing_contract_scan.py`

- [ ] **Step 1: Update governance wording**

In `docs/governance/current-routing-contract.md`, replace the
`legacy compatibility` term row with:

```markdown
| `retired old-format fields` | Old routing, consultation, and dispatch fields are not current inputs, current outputs, or maintained compatibility targets. |
```

Replace the `## Legacy Compatibility Boundary` section heading with:

```markdown
## Retired Old-Format Fields
```

Replace the paragraph under that heading with:

```markdown
The following old fields are retired. Current runtime code must not use them to
infer selected skills, material skill use, or current execution ownership:
```

Replace the final compatibility paragraph with:

```markdown
When current and retired fields are both present in an old artifact, current
runtime code should prefer `skill_routing` and `skill_usage` and ignore retired
fields for current behavior.
```

- [ ] **Step 2: Extend the scan script**

In `scripts/verify/vibe-current-routing-contract-scan.ps1`, add these files to
a new `$currentRuntimeFiles` list:

```powershell
$currentRuntimeFiles = @(
    'scripts/runtime/VibeSkillRouting.Common.ps1',
    'scripts/runtime/VibeRuntime.Common.ps1',
    'scripts/runtime/Write-RequirementDoc.ps1',
    'scripts/runtime/Write-XlPlan.ps1',
    'scripts/runtime/invoke-vibe-runtime.ps1'
)
```

Add these old-format patterns:

```powershell
$oldFormatFallbackPatterns = @(
    'legacy_skill_routing',
    'specialist_recommendations',
    'stage_assistant_hints',
    '## Specialist Consultation',
    'DiscussionConsultationPath',
    'PlanningConsultationPath'
)
```

For each line in `$currentRuntimeFiles`, add a finding with category
`current_runtime_old_format_fallback` when one of those patterns appears and the
line does not contain one of these allowed current-execution phrases:

```powershell
$allowedCurrentExecutionPhrases = @(
    'host_specialist_dispatch_decision',
    'specialist_dispatch_decision',
    'derived_from_skill_routing_selected',
    'source = ''skill_routing.selected'''
)
```

Update the summary object to include:

```powershell
current_runtime_old_format_fallback_count = @($findings | Where-Object { $_.category -eq 'current_runtime_old_format_fallback' }).Count
retired_old_format_reference_count = [int]$legacyReferenceCount
```

Rename plain output text from:

```powershell
Legacy compatibility references:
```

to:

```powershell
Retired old-format references:
```

Make the gate fail when either `current_surface_violation_count` or
`current_runtime_old_format_fallback_count` is greater than zero.

- [ ] **Step 3: Update scan tests**

In `tests/runtime_neutral/test_current_routing_contract_scan.py`, update
`test_scan_script_reports_json_and_no_current_surface_violations` to assert:

```python
self.assertEqual(0, int(payload["current_surface_violation_count"]))
self.assertEqual(0, int(payload["current_runtime_old_format_fallback_count"]))
self.assertIn("retired_old_format_reference_count", payload)
self.assertIn("historical_reference_count", payload)
self.assertEqual([], payload["findings"])
```

Update `test_scan_script_plain_output_has_pass_gate` to assert:

```python
self.assertIn("VCO Current Routing Contract Scan", completed.stdout)
self.assertIn("Retired old-format references:", completed.stdout)
self.assertIn("Gate Result: PASS", completed.stdout)
```

- [ ] **Step 4: Run scan tests and direct scan**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_contract_scan.py -q
.\scripts\verify\vibe-current-routing-contract-scan.ps1
```

Expected:

```text
Gate Result: PASS
```

- [ ] **Step 5: Commit governance and scan update**

Run:

```powershell
git add docs/governance/current-routing-contract.md scripts/verify/vibe-current-routing-contract-scan.ps1 tests/runtime_neutral/test_current_routing_contract_scan.py
git commit -m "test: gate retired old routing compatibility"
```

Expected: commit succeeds.

---

### Task 7: Update Current Tests That Still Assert Old Packet Fields

**Files:**
- Modify: `tests/runtime_neutral/test_bundled_stage_assistant_freeze.py`
- Modify: `tests/runtime_neutral/test_custom_admission_bridge.py`
- Modify: `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`
- Modify: `tests/runtime_neutral/test_installed_host_runtime_simulation.py`
- Modify additional tests only when the focused run names them.

- [ ] **Step 1: Locate remaining old packet assertions**

Run:

```powershell
rg -n "legacy_skill_routing|specialist_recommendations|stage_assistant_hints|discussion_specialist_consultation|planning_specialist_consultation" tests/runtime_neutral
```

Expected: remaining hits are only in retired-behavior tests, historical fixture
strings, or tests that still need updating.

- [ ] **Step 2: Rewrite old packet assertions to current shape**

For freeze/runtime packet tests, replace assertions that read:

```python
legacy = packet["legacy_skill_routing"]
self.assertIn("specialist_recommendations", legacy)
self.assertIn("stage_assistant_hints", legacy)
```

with assertions against current shape:

```python
self.assertIn("skill_routing", packet)
self.assertIn("skill_usage", packet)
self.assertNotIn("legacy_skill_routing", packet)
self.assertNotIn("specialist_recommendations", packet)
self.assertNotIn("stage_assistant_hints", packet)
```

For tests that need selected skills, derive them from:

```python
selected_ids = [item["skill_id"] for item in list(packet["skill_routing"]["selected"])]
```

For tests that need candidates, derive them from:

```python
candidate_ids = [item["skill_id"] for item in list(packet["skill_routing"]["candidates"])]
```

- [ ] **Step 3: Preserve current execution-lane tests**

Do not delete tests that assert current execution lane outcomes such as:

```text
specialist_dispatch_unit_count
specialist_dispatch_outcomes
lane_kind = specialist_dispatch
```

Those are current execution internals. Change them only if they read old input
fields such as `legacy_skill_routing`, `specialist_recommendations`, or
`stage_assistant_hints`.

- [ ] **Step 4: Run updated focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bundled_stage_assistant_freeze.py tests/runtime_neutral/test_custom_admission_bridge.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_installed_host_runtime_simulation.py -q
```

Expected: all selected tests pass.

- [ ] **Step 5: Commit test updates**

Run:

```powershell
git add tests/runtime_neutral/test_bundled_stage_assistant_freeze.py tests/runtime_neutral/test_custom_admission_bridge.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_installed_host_runtime_simulation.py
git commit -m "test: update routing tests for retired old format"
```

Expected: commit succeeds.

---

### Task 8: Run Focused Runtime Regression Matrix

**Files:**
- No new edits unless a focused failure points to a current-format regression.

- [ ] **Step 1: Run focused contract matrix**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_retired_old_routing_compat.py tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_runtime_route_output_shape.py -q
```

Expected: all selected tests pass.

- [ ] **Step 2: Run runtime and execution regression matrix**

Run:

```powershell
python -m pytest tests/unit/test_runtime_stage_machine.py tests/runtime_neutral/test_active_consultation_simplification.py tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_plan_execute_receipts.py tests/runtime_neutral/test_l_xl_native_execution_topology.py -q
```

Expected: all selected tests pass.

- [ ] **Step 3: Fix only current-format regressions**

If Step 1 or Step 2 fails, inspect the first failing assertion. Fix only one of
these categories:

```text
current skill_routing behavior
current skill_usage behavior
current generated docs
current execution derived from skill_routing.selected
tests that still assert old-format compatibility
```

Then rerun the exact failing test and rerun Step 1 and Step 2.

- [ ] **Step 4: Commit focused regression fix if files changed**

If Step 3 changed files, run:

```powershell
git status --short
git add scripts/runtime/VibeSkillRouting.Common.ps1 scripts/runtime/VibeRuntime.Common.ps1 scripts/runtime/Write-RequirementDoc.ps1 scripts/runtime/Write-XlPlan.ps1 scripts/runtime/invoke-vibe-runtime.ps1 scripts/runtime/VibeConsultation.Common.ps1 tests/runtime_neutral/test_retired_old_routing_compat.py tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_runtime_route_output_shape.py tests/runtime_neutral/test_active_consultation_simplification.py tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_plan_execute_receipts.py tests/runtime_neutral/test_l_xl_native_execution_topology.py
git commit -m "fix: stabilize retired old routing compatibility"
```

Expected: commit succeeds. If Step 3 made no changes, skip this commit step.

---

### Task 9: Run Broad Gates And Final Report

**Files:**
- No new edits unless a broad gate failure identifies a current-format bug.

- [ ] **Step 1: Run pack routing smoke**

Run:

```powershell
.\scripts\verify\vibe-pack-routing-smoke.ps1
```

Expected:

```text
Failed: 0
Pack routing smoke checks passed.
```

- [ ] **Step 2: Run offline skills gate**

Run:

```powershell
.\scripts\verify\vibe-offline-skills-gate.ps1
```

Expected:

```text
[PASS] offline skill closure gate passed.
```

- [ ] **Step 3: Run config parity gate**

Run:

```powershell
.\scripts\verify\vibe-config-parity-gate.ps1
```

Expected:

```text
Gate Result: PASS
```

- [ ] **Step 4: Run version gates**

Run:

```powershell
.\scripts\verify\vibe-version-packaging-gate.ps1
.\scripts\verify\vibe-version-consistency-gate.ps1
```

Expected for both gates:

```text
Gate Result: PASS
```

- [ ] **Step 5: Run retired routing compatibility scan**

Run:

```powershell
.\scripts\verify\vibe-current-routing-contract-scan.ps1
```

Expected:

```text
Current surface violations: 0
Current runtime old-format fallbacks: 0
Gate Result: PASS
```

- [ ] **Step 6: Run whitespace check and status**

Run:

```powershell
git diff --check
git status --short --branch
git log --oneline -n 12
```

Expected:

```text
git diff --check has no output
git status shows no uncommitted source changes
latest commits include the retired old routing compatibility cleanup commits
```

- [ ] **Step 7: Final report requirements**

Final report must state:

- Old routing-format adaptation is retired.
- Old artifact readability is not maintained.
- Current runtime routing remains
  `skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused`.
- Six governed stages are unchanged.
- Current execution internals may still use `specialist_dispatch` naming only
  when derived from `skill_routing.selected`.
- New runtime packets do not emit `legacy_skill_routing`.
- Current generated docs do not emit `## Specialist Consultation`.
- Pack routing smoke, offline skills gate, config parity, version packaging,
  version consistency, retired routing scan, and `git diff --check` results.
