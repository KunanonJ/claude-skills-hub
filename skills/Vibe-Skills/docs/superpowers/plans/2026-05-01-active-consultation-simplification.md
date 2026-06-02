# Active Consultation Simplification Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stop new governed runtime sessions from creating or presenting active specialist-consultation layers while preserving six-stage execution, skill selection, and binary `used / unused` skill evidence.

**Architecture:** Keep the existing route and usage model intact. Disable consultation as a default active runtime path, skip discussion/planning consultation receipt generation when disabled, and keep the old consultation functions as legacy compatibility readers/tests only. New output should describe selected skills through `skill_routing.selected` and material usage through `skill_usage.used` / `skill_usage.unused`.

**Tech Stack:** PowerShell runtime scripts, JSON config, Python `unittest` / `pytest`, existing Vibe verification gates.

---

## File Structure

- Create: `tests/runtime_neutral/test_active_consultation_simplification.py`
  - New current-contract tests for default runtime behavior after consultation is disabled.
  - Also includes one legacy projection test proving old consultation receipts remain readable but do not prove use.
- Modify: `config/specialist-consultation-policy.json`
  - Mark active consultation disabled by default and remove live bucket configuration from active policy.
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`
  - Skip `Invoke-VibeSpecialistConsultationWindow` calls when the resolved policy is disabled.
  - Pass consultation paths and consultation projections only when receipts exist.
  - Preserve runtime stops at `requirement_doc` and `xl_plan`.
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
  - Keep old consultation lifecycle projection readable.
  - Make lifecycle truth text current when no consultation layer is present.
  - Avoid consultation wording in new current-session lifecycle markdown when the layer set only contains routing and execution.
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
  - Keep old receipt loading optional.
  - Remove active consultation section from normal output when no receipt is passed.
  - Replace current "Specialist Recommendations" wording with selected-skill wording.
- Modify: `scripts/runtime/Write-XlPlan.ps1`
  - Keep old receipt loading optional.
  - Remove active consultation section from normal output when no receipt is passed.
  - Exclude consultation lifecycle layer IDs from current markdown when receipts are absent.
- Modify: `tests/runtime_neutral/test_vibe_specialist_consultation.py`
  - Retain direct consultation function tests as legacy compatibility coverage by passing explicit enabled test policies.
  - Replace runtime-level tests that expect default discussion/planning consultation artifacts.
- Modify: `SKILL.md`
  - Align the `Updated` maintenance marker with `config/version-governance.json` release metadata.

Do not modify pack routing files or skill directories in this plan.

---

### Task 1: Add Current Active-Consultation Simplification Tests

**Files:**
- Create: `tests/runtime_neutral/test_active_consultation_simplification.py`

- [ ] **Step 1: Create the test file**

Create `tests/runtime_neutral/test_active_consultation_simplification.py` with this complete content:

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


SPECIALIST_TASK = (
    "I have a failing test and a stack trace. Help me debug systematically "
    "before proposing fixes."
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


def load_json(path: str | Path) -> dict[str, object]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_runtime(task: str, artifact_root: Path) -> dict[str, object]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available in PATH")

    run_id = "pytest-active-consult-off-" + uuid.uuid4().hex[:10]
    completed = subprocess.run(
        [
            shell,
            "-NoLogo",
            "-NoProfile",
            "-File",
            str(RUNTIME_SCRIPT),
            "-Task",
            task,
            "-Mode",
            "interactive_governed",
            "-RunId",
            run_id,
            "-ArtifactRoot",
            str(artifact_root),
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


class ActiveConsultationSimplificationTests(unittest.TestCase):
    def test_default_runtime_closes_without_active_consultation_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            payload = run_runtime(SPECIALIST_TASK, Path(tempdir))

            summary = payload["summary"]
            artifacts = summary["artifacts"]
            session_root = Path(payload["session_root"])

            self.assertIsNone(artifacts.get("discussion_specialist_consultation"))
            self.assertIsNone(artifacts.get("planning_specialist_consultation"))
            self.assertIsNone(summary.get("specialist_consultation"))
            self.assertEqual(
                [],
                sorted(path.name for path in session_root.glob("*specialist-consultation*.json")),
            )

            lifecycle = summary["specialist_lifecycle_disclosure"]
            layer_ids = [str(layer["layer_id"]) for layer in list(lifecycle["layers"])]
            self.assertIn("discussion_routing", layer_ids)
            self.assertNotIn("discussion_consultation", layer_ids)
            self.assertNotIn("planning_consultation", layer_ids)
            self.assertNotIn("consultation", str(lifecycle["truth_model"]).lower())

            requirement_doc = Path(artifacts["requirement_doc"]).read_text(encoding="utf-8")
            execution_plan = Path(artifacts["execution_plan"]).read_text(encoding="utf-8")
            for text in (requirement_doc, execution_plan, lifecycle["rendered_text"]):
                self.assertNotIn("## Specialist Consultation", text)
                self.assertNotIn("consultation truth", text)
                self.assertNotIn("stage assistant", text.lower())
            self.assertIn("## Skill Usage", requirement_doc)
            self.assertIn("## Binary Skill Usage Plan", execution_plan)
            self.assertIn("used` / `unused", requirement_doc)
            self.assertIn("skill_usage.used` / `skill_usage.unused", execution_plan)

    def test_legacy_consultation_projection_remains_readable_without_usage_claim(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available in PATH")

        script = (
            "& { "
            f". {ps_quote(str(RUNTIME_COMMON))}; "
            "$receipt = [pscustomobject]@{ "
            "enabled = $true; "
            "window_id = 'discussion'; "
            "stage = 'deep_interview'; "
            "user_disclosures = @([pscustomobject]@{ "
            "skill_id = 'legacy-skill'; "
            "why_now = 'old packet disclosure'; "
            "native_skill_entrypoint = 'C:\\legacy\\SKILL.md'; "
            "native_skill_description = 'legacy compatibility only' "
            "}); "
            "consulted_units = @(); "
            "routed_units = @([pscustomobject]@{ "
            "skill_id = 'legacy-skill'; "
            "status = 'routed_pending_current_session'; "
            "summary = 'old routed receipt, not use evidence' "
            "}); "
            "summary = [pscustomobject]@{ consulted_unit_count = 0; routed_unit_count = 1 }; "
            "freeze_gate = [pscustomobject]@{ passed = $true; errors = @() } "
            "}; "
            "$layer = New-VibeSpecialistConsultationLifecycleLayerProjection -ConsultationReceipt $receipt; "
            "$segment = New-VibeHostUserBriefingSegmentProjection -LifecycleLayer $layer -ConsultationReceipt $receipt; "
            "[pscustomobject]@{ "
            "layer_id = $layer.layer_id; "
            "truth_layer = $layer.truth_layer; "
            "skill_state = $layer.skills[0].state; "
            "segment_category = $segment.category; "
            "rendered_text = $segment.rendered_text "
            "} | ConvertTo-Json -Depth 20 "
            "}"
        )
        completed = subprocess.run(
            [shell, "-NoLogo", "-NoProfile", "-Command", script],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        payload = json.loads(completed.stdout)

        self.assertEqual("discussion_consultation", payload["layer_id"])
        self.assertEqual("consultation", payload["truth_layer"])
        self.assertEqual("routed_pending_current_session", payload["skill_state"])
        self.assertEqual("consultation", payload["segment_category"])
        self.assertIn("Usage claims still require `skill_usage` evidence", payload["rendered_text"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new tests and verify they fail for the right reason**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_active_consultation_simplification.py -q
```

Expected: at least `test_default_runtime_closes_without_active_consultation_artifacts` fails because current runtime still creates `discussion_specialist_consultation` and `planning_specialist_consultation` artifacts.

Do not commit this red state.

---

### Task 2: Disable Active Consultation In The Policy File

**Files:**
- Modify: `config/specialist-consultation-policy.json`

- [ ] **Step 1: Replace the active consultation policy**

Replace the full contents of `config/specialist-consultation-policy.json` with:

```json
{
  "version": 2,
  "policy_id": "specialist-consultation-legacy-compat-v2",
  "updated_at": "2026-05-01",
  "enabled": false,
  "mode": "direct_current_session_route",
  "allowed_windows": [],
  "legacy_compatibility_only": true,
  "compatibility_note": "Old consultation receipts remain readable for historical artifacts. New runtime sessions use skill_routing.selected plus skill_usage.used and skill_usage.unused."
}
```

Rationale: `mode` stays `direct_current_session_route` because `Get-VibeSpecialistConsultationPolicy` currently accepts only that active mode. The disabled flag and empty window list are what make the policy non-active.

- [ ] **Step 2: Run the focused policy sanity check**

Run:

```powershell
python - <<'PY'
import json
from pathlib import Path
policy = json.loads(Path('config/specialist-consultation-policy.json').read_text(encoding='utf-8'))
assert policy['enabled'] is False
assert policy['allowed_windows'] == []
assert 'bucket_limits' not in policy
assert 'max_consults_per_window' not in policy
assert 'stage_assistant' not in json.dumps(policy)
print('policy disabled and free of active bucket fields')
PY
```

Expected:

```text
policy disabled and free of active bucket fields
```

- [ ] **Step 3: Run the new tests again**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_active_consultation_simplification.py -q
```

Expected: the default-runtime test still fails because `invoke-vibe-runtime.ps1` still calls `Invoke-VibeSpecialistConsultationWindow`, which writes disabled receipt artifacts even when policy is disabled.

Do not commit yet.

---

### Task 3: Skip Consultation Windows In New Runtime Sessions

**Files:**
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`

- [ ] **Step 1: Add one resolved policy variable before the discussion window**

In `scripts/runtime/invoke-vibe-runtime.ps1`, after the line that creates `$requirementMemoryContext`, add:

```powershell
$resolvedSpecialistConsultationPolicy = Get-VibeSpecialistConsultationPolicy -Policy $runtime.specialist_consultation_policy
$activeSpecialistConsultationEnabled = [bool]$resolvedSpecialistConsultationPolicy.enabled
```

- [ ] **Step 2: Wrap the discussion consultation call**

Replace the current unconditional `$discussionConsultation = Invoke-VibeSpecialistConsultationWindow ...` block with:

```powershell
$discussionConsultation = $null
if ($activeSpecialistConsultationEnabled) {
    $discussionConsultation = Invoke-VibeSpecialistConsultationWindow `
        -Task $Task `
        -RunId $RunId `
        -SessionRoot ([string]$skeleton.session_root) `
        -RepoRoot ([string]$runtime.repo_root) `
        -WindowId 'discussion' `
        -Stage 'deep_interview' `
        -SourceArtifactPath ([string]$interview.receipt_path) `
        -Recommendations @(Get-VibeRuntimeSpecialistRecommendations -RuntimeInputPacket $runtimeInputPacket) `
        -Policy $runtime.specialist_consultation_policy
}
$discussionConsultationLayer = if ($discussionConsultation) {
    New-VibeSpecialistConsultationLifecycleLayerProjection -ConsultationReceipt $discussionConsultation.receipt
} else {
    $null
}
```

Keep the existing `if ($discussionConsultationLayer) { ... }` disclosure block unchanged below it.

- [ ] **Step 3: Pass the discussion consultation path only when it exists**

In the `$requirementArgs = @{ ... }` hashtable, remove this entry:

```powershell
DiscussionConsultationPath = $discussionConsultation.receipt_path
```

After the hashtable is created, add:

```powershell
if ($discussionConsultation) {
    $requirementArgs.DiscussionConsultationPath = [string]$discussionConsultation.receipt_path
}
```

- [ ] **Step 4: Wrap the planning consultation call**

Replace the current unconditional `$planningConsultation = Invoke-VibeSpecialistConsultationWindow ...` block with:

```powershell
$planningConsultation = $null
if ($activeSpecialistConsultationEnabled) {
    $planningConsultation = Invoke-VibeSpecialistConsultationWindow `
        -Task $Task `
        -RunId $RunId `
        -SessionRoot ([string]$skeleton.session_root) `
        -RepoRoot ([string]$runtime.repo_root) `
        -WindowId 'planning' `
        -Stage 'requirement_doc' `
        -SourceArtifactPath ([string]$requirement.requirement_doc_path) `
        -Recommendations @(Get-VibeRuntimeSpecialistRecommendations -RuntimeInputPacket $runtimeInputPacket) `
        -Policy $runtime.specialist_consultation_policy
}
$planningConsultationLayer = if ($planningConsultation) {
    New-VibeSpecialistConsultationLifecycleLayerProjection -ConsultationReceipt $planningConsultation.receipt
} else {
    $null
}
```

Keep the existing `if ($planningConsultationLayer) { ... }` disclosure block unchanged below it.

- [ ] **Step 5: Pass consultation paths to `Write-XlPlan.ps1` only when they exist**

Replace:

```powershell
$planArgs.DiscussionConsultationPath = $discussionConsultation.receipt_path
$planArgs.PlanningConsultationPath = $planningConsultation.receipt_path
```

with:

```powershell
if ($discussionConsultation) {
    $planArgs.DiscussionConsultationPath = [string]$discussionConsultation.receipt_path
}
if ($planningConsultation) {
    $planArgs.PlanningConsultationPath = [string]$planningConsultation.receipt_path
}
```

- [ ] **Step 6: Make all runtime stop calls safe with null consultation values**

Search in `scripts/runtime/invoke-vibe-runtime.ps1` for:

```powershell
-DiscussionConsultation $discussionConsultation
-PlanningConsultation $planningConsultation
```

Keep those arguments; the `Complete-VibeGovernedRuntimeStop` parameters already allow null. Do not pass `.receipt` or `.receipt_path` directly in stop arguments.

- [ ] **Step 7: Make final lifecycle disclosure creation conditional**

Replace the final lifecycle creation block that passes `$discussionConsultation.receipt` and `$planningConsultation.receipt` directly with:

```powershell
$specialistLifecycleDisclosure = New-VibeSpecialistLifecycleDisclosureProjection `
    -RuntimeInputPacket $runtimeInputPacket `
    -DiscussionConsultationReceipt $(if ($discussionConsultation) { $discussionConsultation.receipt } else { $null }) `
    -PlanningConsultationReceipt $(if ($planningConsultation) { $planningConsultation.receipt } else { $null }) `
    -SpecialistUserDisclosure $(if ($execute -and $execute.receipt -and $execute.receipt.PSObject.Properties.Name -contains 'specialist_user_disclosure') { $execute.receipt.specialist_user_disclosure } else { $null }) `
    -ExecutionManifest $executionManifestDocument
```

Use the same conditional receipt expressions anywhere else in the file that calls `New-VibeSpecialistLifecycleDisclosureProjection`.

- [ ] **Step 8: Make final summary artifacts conditional**

In the final `New-VibeRuntimeSummaryArtifactProjection` call, replace:

```powershell
-DiscussionSpecialistConsultationPath ([string]$discussionConsultation.receipt_path) `
-PlanningSpecialistConsultationPath ([string]$planningConsultation.receipt_path) `
```

with:

```powershell
-DiscussionSpecialistConsultationPath $(if ($discussionConsultation) { [string]$discussionConsultation.receipt_path } else { '' }) `
-PlanningSpecialistConsultationPath $(if ($planningConsultation) { [string]$planningConsultation.receipt_path } else { '' }) `
```

- [ ] **Step 9: Make final summary consultation projection null when no receipts exist**

Before the final `New-VibeRuntimeSummaryProjection` call, add:

```powershell
$specialistConsultationProjection = if ($discussionConsultation -or $planningConsultation) {
    New-VibeSpecialistConsultationRuntimeProjection -Receipts @(
        $(if ($discussionConsultation) { $discussionConsultation.receipt } else { $null }),
        $(if ($planningConsultation) { $planningConsultation.receipt } else { $null })
    )
} else {
    $null
}
```

Then replace:

```powershell
-SpecialistConsultation (New-VibeSpecialistConsultationRuntimeProjection -Receipts @($discussionConsultation.receipt, $planningConsultation.receipt)) `
```

with:

```powershell
-SpecialistConsultation $specialistConsultationProjection `
```

- [ ] **Step 10: Apply the same null projection rule in `Complete-VibeGovernedRuntimeStop`**

Inside `Complete-VibeGovernedRuntimeStop`, add this before the `$summary = New-VibeRuntimeSummaryProjection` call:

```powershell
$specialistConsultationProjection = if ($DiscussionConsultation -or $PlanningConsultation) {
    New-VibeSpecialistConsultationRuntimeProjection -Receipts @(
        $(if ($DiscussionConsultation) { $DiscussionConsultation.receipt } else { $null }),
        $(if ($PlanningConsultation) { $PlanningConsultation.receipt } else { $null })
    )
} else {
    $null
}
```

Then replace the existing `-SpecialistConsultation (...)` argument with:

```powershell
-SpecialistConsultation $specialistConsultationProjection `
```

- [ ] **Step 11: Run the new current-contract tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_active_consultation_simplification.py -q
```

Expected: the artifact/path assertions pass. The lifecycle wording assertion may still fail until Task 4 changes `VibeRuntime.Common.ps1`.

Do not commit yet.

---

### Task 4: Update Lifecycle Projection Text For Current Routing And Usage

**Files:**
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`

- [ ] **Step 1: Make the lifecycle truth model conditional**

In `New-VibeSpecialistLifecycleDisclosureProjection`, replace the fixed return field:

```powershell
truth_model = 'routing_consultation_execution_separated'
```

with:

```powershell
truth_model = if (@($layerArray | Where-Object { [string]$_.truth_layer -eq 'consultation' }).Count -gt 0) {
    'legacy_routing_consultation_execution_separated'
} else {
    'skill_routing_usage_evidence'
}
```

This preserves old artifact readability while making new sessions stop advertising consultation in the truth model.

- [ ] **Step 2: Make lifecycle markdown use current wording when no consultation layer exists**

In `Get-VibeSpecialistLifecycleDisclosureMarkdownLines`, replace the fixed `$lines = @(...` initialization with:

```powershell
$hasConsultationLayer = @($LifecycleDisclosure.layers | Where-Object { [string]$_.truth_layer -eq 'consultation' }).Count -gt 0
$lines = if ($hasConsultationLayer) {
    @(
        '## Legacy Specialist Lifecycle Disclosure',
        'This legacy disclosure keeps old routing, consultation, and execution records readable. Usage claims still require `skill_usage.used` evidence.'
    )
} else {
    @(
        '## Skill Routing And Usage Evidence',
        'This disclosure records selected skills and execution evidence. Routing or dispatch alone is not a `used` claim; material use requires `skill_usage.used` evidence.'
    )
}
```

- [ ] **Step 3: Keep old consultation briefing text legacy-only and usage-safe**

In `New-VibeHostUserBriefingSegmentProjection`, keep the `discussion_consultation` and `planning_consultation` branches, but make routed-only legacy consultation text explicitly not a use claim.

Replace:

```powershell
$segmentLines += ('Vibe routed these Skills for direct current-session consultation during {0}; freeze gate: {1}.' -f $windowId, $gateStatus)
```

with:

```powershell
$segmentLines += ('Vibe routed these Skills for legacy consultation disclosure during {0}; freeze gate: {1}. Usage claims still require `skill_usage` evidence.' -f $windowId, $gateStatus)
```

Do not rename those branches in this task.

- [ ] **Step 4: Run lifecycle-focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_active_consultation_simplification.py -q
```

Expected:

```text
2 passed
```

The exact elapsed time may vary.

Do not commit yet; the runtime docs still need output text cleanup.

---

### Task 5: Rewrite Requirement And Plan Output Away From Active Consultation Wording

**Files:**
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
- Modify: `scripts/runtime/Write-XlPlan.ps1`

- [ ] **Step 1: Update the requirement-doc selected-skill section**

In `scripts/runtime/Write-RequirementDoc.ps1`, find the block that starts:

```powershell
if (@($legacySpecialistRecommendations).Count -gt 0 -or @($approvedSpecialistDispatch).Count -gt 0) {
    $lines += @(
        '',
        '## Specialist Recommendations',
        'Raw router candidates remain in `runtime-input-packet.json` for audit and are not frozen as user-facing requirements.',
        'Only host-adopted or effective approved specialist dispatch is shown here; non-adopted candidates and stage assistants stay out of the requirement surface.'
    )
```

Replace the heading and first lines with:

```powershell
if (@($selectedSkillRouting).Count -gt 0 -or @($approvedSpecialistDispatch).Count -gt 0) {
    $lines += @(
        '',
        '## Selected Skill',
        'Router candidates remain in `runtime-input-packet.json` for audit. The current work surface records selected skills here and material use in `skill_usage.used` / `skill_usage.unused`.',
        'Rejected candidates stay out of the requirement surface.'
    )
```

Then replace:

```powershell
if (@($approvedSpecialistDispatch).Count -eq 0) {
    $lines += 'No specialist dispatch was adopted for user-facing execution in this run.'
}
foreach ($recommendation in $approvedSpecialistDispatch) {
```

with:

```powershell
if (@($approvedSpecialistDispatch).Count -eq 0) {
    $lines += 'No selected skill was adopted for user-facing execution in this run.'
}
foreach ($recommendation in $approvedSpecialistDispatch) {
```

In the same loop, replace the label:

```powershell
"- Adopted Skill: $([string]$recommendation.skill_id)",
```

with:

```powershell
"- Selected Skill: $([string]$recommendation.skill_id)",
```

Leave the compatibility variable `$approvedSpecialistDispatch` name unchanged in this slice.

- [ ] **Step 2: Keep requirement consultation output conditional**

Leave the existing block:

```powershell
if ($discussionConsultation -and [bool]$discussionConsultation.enabled) {
```

unchanged. Because Task 3 stops passing new consultation paths by default, this block becomes legacy-only.

- [ ] **Step 3: Update the XL plan lifecycle layer IDs**

In `scripts/runtime/Write-XlPlan.ps1`, replace:

```powershell
$lifecycleLines = Get-VibeSpecialistLifecycleDisclosureMarkdownLines `
    -LifecycleDisclosure $stageLifecycleDisclosure `
    -IncludeLayerIds @('discussion_routing', 'discussion_consultation', 'planning_consultation')
```

with:

```powershell
$currentLifecycleLayerIds = @('discussion_routing')
if ($discussionConsultation) {
    $currentLifecycleLayerIds += 'discussion_consultation'
}
if ($planningConsultation) {
    $currentLifecycleLayerIds += 'planning_consultation'
}
$lifecycleLines = Get-VibeSpecialistLifecycleDisclosureMarkdownLines `
    -LifecycleDisclosure $stageLifecycleDisclosure `
    -IncludeLayerIds @($currentLifecycleLayerIds)
```

- [ ] **Step 4: Keep XL plan consultation section conditional**

Leave the existing block:

```powershell
if ($planningConsultation -and [bool]$planningConsultation.enabled) {
```

unchanged. Because Task 3 stops passing new planning consultation paths by default, this block becomes legacy-only.

- [ ] **Step 5: Run the current-contract tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_active_consultation_simplification.py -q
```

Expected:

```text
2 passed
```

- [ ] **Step 6: Run the focused route and usage tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_runtime_route_output_shape.py -q
```

Expected: all selected tests pass.

- [ ] **Step 7: Commit the first green implementation slice**

Run:

```powershell
git add config/specialist-consultation-policy.json scripts/runtime/invoke-vibe-runtime.ps1 scripts/runtime/VibeRuntime.Common.ps1 scripts/runtime/Write-RequirementDoc.ps1 scripts/runtime/Write-XlPlan.ps1 tests/runtime_neutral/test_active_consultation_simplification.py
git commit -m "fix: disable active consultation runtime layer"
```

Expected: commit succeeds.

---

### Task 6: Convert Existing Consultation Tests To Legacy Compatibility Coverage

**Files:**
- Modify: `tests/runtime_neutral/test_vibe_specialist_consultation.py`

- [ ] **Step 1: Add an explicit legacy active policy helper**

After `consultation_native_subprocess_test_overrides`, add:

```python
def legacy_active_consultation_policy_ps(max_consults: int = 3) -> str:
    return (
        "[pscustomobject]@{ "
        "enabled = $true; "
        "version = 1; "
        "policy_id = 'legacy-consultation-test-policy'; "
        "mode = 'direct_current_session_route'; "
        f"max_consults_per_window = {max_consults}; "
        "selection_mode = 'bucketed_with_backfill'; "
        "bucket_limits = [pscustomobject]@{ primary = 2; stage_assistant = 1 }; "
        "allowed_windows = @('discussion', 'planning'); "
        "require_contract_complete = $true; "
        "require_native_workflow = $true; "
        "require_native_usage_required = $true; "
        "require_entrypoint_path = $true; "
        "progressive_disclosure_enabled = $true; "
        "defer_unapproved_to_execution = $true; "
        "freeze_gate_enabled = $true; "
        "require_outcome_coverage_for_approved_skills = $true; "
        "require_disclosure_coverage_for_approved_skills = $true; "
        "require_non_empty_summary_for_live_results = $true; "
        "require_consultation_notes_for_live_results = $true; "
        "require_adoption_notes_for_live_results = $true; "
        "require_verification_notes_for_live_results = $true; "
        "fail_freeze_on_live_degraded_results = $true; "
        "window_prompts = [pscustomobject]@{ "
        "discussion = 'Legacy compatibility test discussion prompt.'; "
        "planning = 'Legacy compatibility test planning prompt.' "
        "} "
        "}"
    )
```

This keeps old direct-function tests alive without relying on the default runtime policy.

- [ ] **Step 2: Rename the bucket-selection test to mark it legacy-only**

Rename:

```python
def test_bucketed_consultation_selection_keeps_stage_assistant_visible(self) -> None:
```

to:

```python
def test_legacy_bucketed_consultation_selection_remains_readable(self) -> None:
```

Inside that test, replace the inline `$policy = [pscustomobject]@{ ... }` construction with:

```python
f"$policy = {legacy_active_consultation_policy_ps()}; "
```

Keep the existing assertions in this test. They now document legacy bucket behavior only.

- [ ] **Step 3: Replace default-runtime consultation projection assertions**

Delete the old runtime-level method:

```python
def test_runtime_projects_consultation_truth_into_summary_requirement_and_plan(self) -> None:
```

Replace it with:

```python
def test_runtime_projects_skill_routing_usage_without_default_consultation(self) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
        artifact_root = Path(tempdir)
        payload = run_runtime(
            SPECIALIST_TASK,
            artifact_root,
            extra_env={
                "VGO_NATIVE_SPECIALIST_EXECUTION_MODE": "",
                "VGO_SPECIALIST_CONSULTATION_MODE": "",
                "VGO_DISABLE_NATIVE_SPECIALIST_EXECUTION": "1",
            },
        )
        summary = payload["summary"]
        artifacts = summary["artifacts"]

        self.assertIsNone(artifacts.get("discussion_specialist_consultation"))
        self.assertIsNone(artifacts.get("planning_specialist_consultation"))
        self.assertIsNone(summary.get("specialist_consultation"))

        requirement_receipt = load_json(artifacts["requirement_receipt"])
        plan_receipt = load_json(artifacts["execution_plan_receipt"])
        requirement_doc = Path(artifacts["requirement_doc"]).read_text(encoding="utf-8")
        execution_plan = Path(artifacts["execution_plan"]).read_text(encoding="utf-8")

        self.assertIsNone(requirement_receipt["discussion_consultation_path"])
        self.assertEqual(0, int(requirement_receipt["discussion_consultation_count"]))
        self.assertIsNone(plan_receipt["planning_consultation_path"])
        self.assertEqual(0, int(plan_receipt["planning_consultation_count"]))

        lifecycle = summary["specialist_lifecycle_disclosure"]
        layer_ids = [str(layer["layer_id"]) for layer in list(lifecycle["layers"])]
        self.assertIn("discussion_routing", layer_ids)
        self.assertNotIn("discussion_consultation", layer_ids)
        self.assertNotIn("planning_consultation", layer_ids)
        self.assertEqual("skill_routing_usage_evidence", lifecycle["truth_model"])

        host_stage_disclosure = summary["host_stage_disclosure"]
        event_ids = [str(event["event_id"]) for event in list(host_stage_disclosure["events"])]
        self.assertIn("discussion_routing_frozen", event_ids)
        self.assertNotIn("discussion_consultation_routed", event_ids)
        self.assertNotIn("planning_consultation_routed", event_ids)

        host_user_briefing = summary["host_user_briefing"]
        segment_ids = [str(segment["segment_id"]) for segment in list(host_user_briefing["segments"])]
        self.assertIn("discussion_routing", segment_ids)
        self.assertNotIn("discussion_consultation", segment_ids)
        self.assertNotIn("planning_consultation", segment_ids)

        self.assertNotIn("## Specialist Consultation", requirement_doc)
        self.assertNotIn("## Specialist Consultation", execution_plan)
        self.assertIn("## Skill Usage", requirement_doc)
        self.assertIn("## Binary Skill Usage Plan", execution_plan)
        self.assertIn("systematic-debugging", requirement_doc)
        self.assertIn("systematic-debugging", execution_plan)
```

- [ ] **Step 4: Update direct window tests that still need active consultation**

For each test that calls `Invoke-VibeSpecialistConsultationWindow` directly and passes:

```python
f"-Policy $runtime.specialist_consultation_policy; "
```

change the PowerShell script setup to define:

```python
f"$legacyPolicy = {legacy_active_consultation_policy_ps()}; "
```

and pass:

```python
f"-Policy $legacyPolicy; "
```

Apply this to the direct consultation-window tests around the existing calls near the old line ranges:

- live consultation window invokes specialist
- non-git consultation window
- write-attempt consultation window
- read-only fallback consultation window
- empty guidance routes directly

Do not change `Invoke-VibeSpecialistConsultationUnit` tests unless they rely on default disabled policy. Unit tests can also pass `$legacyPolicy` when they expect active schema/completeness behavior.

- [ ] **Step 5: Replace the default runtime freeze-green consultation test**

Delete:

```python
def test_runtime_keeps_freeze_green_when_live_consultation_routes_directly(self) -> None:
```

Replace it with:

```python
def test_runtime_keeps_freeze_green_without_default_consultation(self) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
        artifact_root = Path(tempdir)
        completed = run_runtime(
            SPECIALIST_TASK,
            artifact_root,
            extra_env={
                "VGO_ENABLE_NATIVE_SPECIALIST_EXECUTION": "1",
                "VGO_DISABLE_NATIVE_SPECIALIST_EXECUTION": "0",
                "VGO_SPECIALIST_CONSULTATION_MODE": "host_subprocess",
                "VGO_NATIVE_SPECIALIST_EXECUTION_MODE": "host_subprocess",
            },
            check=False,
        )

        self.assertEqual(0, completed.returncode)
        payload = json.loads(completed.stdout)
        artifacts = payload["summary"]["artifacts"]
        self.assertIsNone(artifacts.get("discussion_specialist_consultation"))
        self.assertIsNone(artifacts.get("planning_specialist_consultation"))
        combined_output = f"{completed.stdout}\n{completed.stderr}"
        self.assertNotIn("specialist consultation freeze gate failed", combined_output)
```

- [ ] **Step 6: Run consultation tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_active_consultation_simplification.py -q
```

Expected: all tests pass. If a remaining direct consultation test fails because it is using the disabled default policy, update that test to use `legacy_active_consultation_policy_ps()`.

- [ ] **Step 7: Commit compatibility test cleanup**

Run:

```powershell
git add tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_active_consultation_simplification.py
git commit -m "test: keep consultation legacy-only"
```

Expected: commit succeeds.

---

### Task 7: Fix Release Metadata Drift

**Files:**
- Modify: `SKILL.md`

- [ ] **Step 1: Align the maintenance marker**

In `SKILL.md`, replace:

```markdown
- Updated: 2026-04-26
```

with:

```markdown
- Updated: 2026-04-25
```

Do not change the version marker:

```markdown
- Version: 3.1.0
```

Rationale: `config/version-governance.json`, `references/changelog.md`, and `references/release-ledger.jsonl` already use release date `2026-04-25`. The root `SKILL.md` marker is the drift.

- [ ] **Step 2: Run the version consistency gate**

Run:

```powershell
.\scripts\verify\vibe-version-consistency-gate.ps1
```

Expected:

```text
Gate Result: PASS
```

- [ ] **Step 3: Commit metadata fix**

Run:

```powershell
git add SKILL.md
git commit -m "fix: align skill release marker"
```

Expected: commit succeeds.

---

### Task 8: Final Regression Verification

**Files:**
- No new edits unless a verification failure points to a specific changed file.

- [ ] **Step 1: Run focused runtime and routing tests**

Run:

```powershell
python -m pytest tests/unit/test_runtime_stage_machine.py tests/runtime_neutral/test_active_consultation_simplification.py tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_runtime_route_output_shape.py -q
```

Expected: all selected tests pass.

- [ ] **Step 2: Run pack routing smoke**

Run:

```powershell
.\scripts\verify\vibe-pack-routing-smoke.ps1
```

Expected:

```text
Failed: 0
Pack routing smoke checks passed.
```

- [ ] **Step 3: Run offline skills gate**

Run:

```powershell
.\scripts\verify\vibe-offline-skills-gate.ps1
```

Expected:

```text
[PASS] offline skill closure gate passed.
```

- [ ] **Step 4: Run config parity gate**

Run:

```powershell
.\scripts\verify\vibe-config-parity-gate.ps1
```

Expected:

```text
Gate Result: PASS
```

- [ ] **Step 5: Run version packaging and consistency gates**

Run:

```powershell
.\scripts\verify\vibe-version-packaging-gate.ps1
.\scripts\verify\vibe-version-consistency-gate.ps1
```

Expected:

```text
Gate Result: PASS
```

for both gates.

- [ ] **Step 6: Run whitespace check**

Run:

```powershell
git diff --check
```

Expected: no output.

- [ ] **Step 7: Inspect final active consultation surface**

Run:

```powershell
rg -n "discussion_specialist_consultation|planning_specialist_consultation|approved_consultation|consulted_units|stage_assistant" config scripts/runtime tests/runtime_neutral/test_active_consultation_simplification.py tests/runtime_neutral/test_vibe_specialist_consultation.py
```

Expected:

- No hits in `config/specialist-consultation-policy.json` for `stage_assistant`, `approved_consultation`, or `consulted_units`.
- Runtime hits remain only in legacy compatibility functions, null-safe optional paths, and old consultation tests.
- New `test_active_consultation_simplification.py` asserts default runtime does not create active consultation artifacts.

- [ ] **Step 8: Report final status**

In the final implementation report, state these facts exactly:

- New runtime sessions no longer create active discussion/planning consultation artifacts by default.
- Old consultation functions remain for legacy compatibility tests.
- `skill_routing.selected` remains the selection record.
- `skill_usage.used` / `skill_usage.unused` remain the material-use proof.
- Six governed stages are unchanged.
- Pack routing smoke, offline skills gate, config parity, version packaging, version consistency, and `git diff --check` results.

Do not claim all historical consultation strings are deleted. That is not the goal of this plan.
