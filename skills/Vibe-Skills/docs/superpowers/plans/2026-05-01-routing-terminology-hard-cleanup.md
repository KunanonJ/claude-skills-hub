# Routing Terminology Hard Cleanup Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove retired routing terminology from current docs, tests, scan gates, and packet contracts while preserving the current six-stage runtime and the `skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused` model.

**Architecture:** Add a current runtime field contract and a hard cleanup scan first, then migrate current behavior tests away from retired packet fields, isolate historical docs with explicit retired markers, and add execution-output aliases only where needed to avoid breaking current execution accounting. Existing execution internals may keep `specialist_dispatch` names temporarily, but public/current packet and test contracts must use current routing, usage, and execution vocabulary.

**Tech Stack:** PowerShell runtime and verify scripts, Python `pytest` runtime-neutral tests, Markdown governance docs, existing Vibe verification gates.

---

## File Structure

- Create: `docs/governance/current-runtime-field-contract.md`
  - Current contract for routing, usage, execution, and retired fields.
- Create: `config/routing-terminology-hard-cleanup.json`
  - Scan configuration for current docs, current behavior tests, retired tests, historical docs, and execution-internal allowlists.
- Create: `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1`
  - Strong scan that fails when retired fields return to current docs/tests/runtime contracts.
- Create: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
  - Tests for the contract doc and hard cleanup scan.
- Modify: `tests/runtime_neutral/test_root_child_hierarchy_bridge.py`
  - Stop reading `runtime_input_packet["specialist_dispatch"]` as current child runtime contract.
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
  - Add current execution vocabulary aliases to execution manifests and receipts while keeping old internal counters temporarily.
- Modify: `tests/runtime_neutral/test_l_xl_native_execution_topology.py`
  - Assert current execution alias fields are present and derived from existing execution accounting.
- Modify: historical docs with retired markers:
  - `docs/governance/binary-skill-usage-routing-2026-04-28.md`
  - `docs/governance/simplified-skill-routing-2026-04-29.md`
  - `docs/governance/terminology-governance.md`
  - `docs/governance/specialist-dispatch-governance.md`
  - `docs/superpowers/specs/2026-04-10-vibe-aggressive-specialist-routing-design.md`
  - `docs/superpowers/specs/2026-04-12-vibe-approved-dispatch-user-disclosure-design.md`
  - `docs/superpowers/specs/2026-04-12-vibe-discussion-time-specialist-consultation-design.md`
  - `docs/superpowers/specs/2026-04-12-vibe-host-stage-disclosure-protocol-design.md`
- Modify: `scripts/verify/vibe-current-routing-contract-scan.ps1` only if the new hard cleanup scan exposes a gap that should be part of the existing gate.

Do not modify pack-routing configs or delete bundled skills in this plan.

---

### Task 1: Add Current Runtime Field Contract

**Files:**
- Create: `docs/governance/current-runtime-field-contract.md`
- Create: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`

- [ ] **Step 1: Write the failing contract-doc test**

Create `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py` with this initial content:

```python
from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_DOC = REPO_ROOT / "docs" / "governance" / "current-runtime-field-contract.md"
HARD_SCAN = REPO_ROOT / "scripts" / "verify" / "vibe-routing-terminology-hard-cleanup-scan.ps1"


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


class RoutingTerminologyHardCleanupTests(unittest.TestCase):
    def test_current_runtime_field_contract_defines_allowed_layers(self) -> None:
        self.assertTrue(CONTRACT_DOC.exists(), "current runtime field contract must exist")
        text = CONTRACT_DOC.read_text(encoding="utf-8")

        self.assertIn("skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused", text)
        for required in [
            "## Routing Layer",
            "## Usage Layer",
            "## Execution Layer",
            "## Retired Layer",
            "`skill_routing.selected`",
            "`skill_usage.used`",
            "`skill_usage.unused`",
            "`skill_usage.evidence`",
            "`approved_skill_execution`",
            "`skill_execution_units`",
            "`execution_skill_outcomes`",
        ]:
            self.assertIn(required, text)

        current_section = text.split("## Retired Layer", 1)[0].lower()
        for forbidden in [
            "primary skill",
            "secondary skill",
            "route owner",
            "consultation expert",
            "auxiliary expert",
            "stage assistant",
        ]:
            self.assertNotIn(forbidden, current_section)

    def test_hard_cleanup_scan_reports_json(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available")

        completed = subprocess.run(
            [shell, "-NoLogo", "-NoProfile", "-File", str(HARD_SCAN), "-Json"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        payload = json.loads(completed.stdout)
        self.assertIn("current_doc_retired_term_violation_count", payload)
        self.assertIn("current_behavior_test_retired_field_read_count", payload)
        self.assertIn("historical_doc_unmarked_retired_term_count", payload)
        self.assertIn("execution_internal_specialist_dispatch_reference_count", payload)
        self.assertEqual([], payload["findings"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new test and verify red state**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_routing_terminology_hard_cleanup.py::RoutingTerminologyHardCleanupTests::test_current_runtime_field_contract_defines_allowed_layers -q
```

Expected: fail because `docs/governance/current-runtime-field-contract.md` does not exist.

- [ ] **Step 3: Add the current runtime field contract**

Create `docs/governance/current-runtime-field-contract.md` with:

```markdown
# Current Runtime Field Contract

Date: 2026-05-01

## Purpose

This document defines the current Vibe-Skills runtime field vocabulary.

The current routing and usage model is:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused
```

Current docs, runtime packets, generated plans, tests, and gates should use
this model unless they are explicitly marked as historical or retired-behavior
fixtures.

## Routing Layer

Allowed current routing fields:

```text
skill_candidates
skill_routing
skill_routing.candidates
skill_routing.selected
skill_routing.rejected
```

Meaning:

- `candidate`: a skill was considered by routing. This is not a use claim.
- `selected`: a skill was chosen into the governed work surface. This is not a
  use claim.
- `rejected`: a skill was considered but not selected.

## Usage Layer

Allowed current usage fields:

```text
skill_usage
skill_usage.used
skill_usage.unused
skill_usage.evidence
```

Meaning:

- `used`: a selected or loaded skill materially shaped an artifact.
- `unused`: a selected or loaded skill did not materially shape an artifact.
- `evidence`: the stage, artifact, and impact proof for material use.

Final used claims require `skill_usage.used` plus matching
`skill_usage.evidence`. Routing and selection alone are not use proof.

## Execution Layer

Preferred current execution vocabulary:

```text
approved_skill_execution
skill_execution_units
selected_skill_execution
execution_skill_outcomes
```

Execution artifacts may temporarily contain internal implementation names that
include `specialist_dispatch` when those values are derived from
`skill_routing.selected`. Those names are execution internals, not routing
authority and not final use proof.

Current root runtime packets should not expose `specialist_dispatch` as a
routing contract field.

## Retired Layer

Retired current-routing fields and sections:

```text
legacy_skill_routing
specialist_recommendations
stage_assistant_hints
specialist_dispatch as root routing packet field
## Specialist Consultation
discussion_specialist_consultation
planning_specialist_consultation
approved_consultation
consulted_units
discussion_consultation
planning_consultation
primary skill
secondary skill
route owner
consultation expert
auxiliary expert
stage assistant
```

These may appear only in retired-behavior tests, historical fixtures, archived
historical docs, or narrow execution-internal allowlists with an explicit scan
reason.

## Current Behavior Rule

Current runtime behavior must derive selected skills from
`skill_routing.selected`. Current material use must be recorded in
`skill_usage.used`, `skill_usage.unused`, and `skill_usage.evidence`.

Old routing, old consultation, old recommendation, and old stage-assistant
fields are not maintained compatibility inputs.
```

- [ ] **Step 4: Run the contract-doc test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_routing_terminology_hard_cleanup.py::RoutingTerminologyHardCleanupTests::test_current_runtime_field_contract_defines_allowed_layers -q
```

Expected: `1 passed`.

- [ ] **Step 5: Commit the contract doc**

Run:

```powershell
git add docs/governance/current-runtime-field-contract.md tests/runtime_neutral/test_routing_terminology_hard_cleanup.py
git commit -m "docs: define current runtime field contract"
```

Expected: commit succeeds.

---

### Task 2: Add Hard Cleanup Scan With Explicit Buckets

**Files:**
- Create: `config/routing-terminology-hard-cleanup.json`
- Create: `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1`
- Modify: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`

- [ ] **Step 1: Add scan config**

Create `config/routing-terminology-hard-cleanup.json`:

```json
{
  "current_docs": [
    "README.md",
    "SKILL.md",
    "docs/governance/current-routing-contract.md",
    "docs/governance/current-runtime-field-contract.md"
  ],
  "current_runtime_files": [
    "scripts/runtime/VibeSkillRouting.Common.ps1",
    "scripts/runtime/VibeRuntime.Common.ps1",
    "scripts/runtime/Freeze-RuntimeInputPacket.ps1",
    "scripts/runtime/Write-RequirementDoc.ps1",
    "scripts/runtime/Write-XlPlan.ps1",
    "scripts/runtime/invoke-vibe-runtime.ps1"
  ],
  "current_behavior_tests": [
    "tests/runtime_neutral/test_root_child_hierarchy_bridge.py",
    "tests/runtime_neutral/test_runtime_contract_schema.py",
    "tests/runtime_neutral/test_runtime_delivery_acceptance.py",
    "tests/runtime_neutral/test_skill_promotion_destructive_gate.py",
    "tests/runtime_neutral/test_l_xl_native_execution_topology.py",
    "tests/runtime_neutral/test_governed_runtime_bridge.py",
    "tests/runtime_neutral/test_installed_host_runtime_simulation.py"
  ],
  "retired_behavior_tests": [
    "tests/runtime_neutral/test_retired_old_routing_compat.py",
    "tests/runtime_neutral/test_simplified_skill_routing_contract.py",
    "tests/runtime_neutral/test_current_routing_contract_cleanup.py"
  ],
  "historical_docs": [
    "docs/governance/binary-skill-usage-routing-2026-04-28.md",
    "docs/governance/simplified-skill-routing-2026-04-29.md",
    "docs/governance/terminology-governance.md",
    "docs/governance/specialist-dispatch-governance.md",
    "docs/superpowers/specs/2026-04-10-vibe-aggressive-specialist-routing-design.md",
    "docs/superpowers/specs/2026-04-12-vibe-approved-dispatch-user-disclosure-design.md",
    "docs/superpowers/specs/2026-04-12-vibe-discussion-time-specialist-consultation-design.md",
    "docs/superpowers/specs/2026-04-12-vibe-host-stage-disclosure-protocol-design.md"
  ],
  "execution_internal_allowlist": [
    {
      "path": "scripts/runtime/Invoke-PlanExecute.ps1",
      "reason": "execution manifest and lane accounting internals derived from skill_routing.selected"
    },
    {
      "path": "scripts/runtime/VibeExecution.Common.ps1",
      "reason": "execution lane internals derived from selected skill execution units"
    },
    {
      "path": "scripts/runtime/Invoke-DelegatedLaneUnit.ps1",
      "reason": "delegated execution lane internals"
    },
    {
      "path": "tests/runtime_neutral/test_plan_execute_receipts.py",
      "reason": "execution-internal receipt tests"
    }
  ],
  "retired_terms": [
    "legacy_skill_routing",
    "specialist_recommendations",
    "stage_assistant_hints",
    "## Specialist Consultation",
    "primary skill",
    "secondary skill",
    "route owner",
    "consultation expert",
    "auxiliary expert",
    "stage assistant"
  ],
  "current_behavior_test_forbidden_patterns": [
    "runtime_input_packet[\"specialist_dispatch\"]",
    "packet[\"specialist_dispatch\"]",
    ".get(\"specialist_dispatch\")",
    "legacy_skill_routing",
    "specialist_recommendations",
    "stage_assistant_hints"
  ],
  "historical_markers": [
    "Historical / Retired Note",
    "Historical Note",
    "Retired Note",
    "Superseded"
  ]
}
```

- [ ] **Step 2: Add the scan script**

Create `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1` with:

```powershell
param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path,
    [switch]$Json
)

$ErrorActionPreference = 'Stop'

function Read-JsonFile {
    param([Parameter(Mandatory)] [string]$Path)
    Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Get-TextFileLines {
    param([Parameter(Mandatory)] [string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        return @()
    }
    return Get-Content -LiteralPath $Path -Encoding UTF8
}

function New-Finding {
    param(
        [Parameter(Mandatory)] [string]$Category,
        [Parameter(Mandatory)] [string]$Path,
        [Parameter(Mandatory)] [int]$Line,
        [Parameter(Mandatory)] [string]$Pattern,
        [Parameter(Mandatory)] [string]$Text
    )
    [pscustomobject]@{
        category = $Category
        path = $Path
        line = $Line
        pattern = $Pattern
        text = $Text.Trim()
    }
}

function Test-LineHasRetiredContext {
    param([Parameter(Mandatory)] [string]$Line)
    foreach ($marker in @('retired', 'historical', 'old-format', 'old routing', 'not current', 'deprecated')) {
        if ($Line.IndexOf($marker, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
            return $true
        }
    }
    return $false
}

$configPath = Join-Path $RepoRoot 'config\routing-terminology-hard-cleanup.json'
$config = Read-JsonFile -Path $configPath
$findings = New-Object System.Collections.Generic.List[object]

foreach ($relative in @($config.current_docs)) {
    $fullPath = Join-Path $RepoRoot $relative
    $lines = @(Get-TextFileLines -Path $fullPath)
    for ($index = 0; $index -lt $lines.Count; $index++) {
        $lineText = [string]$lines[$index]
        foreach ($pattern in @($config.retired_terms)) {
            if ($lineText.IndexOf([string]$pattern, [System.StringComparison]::OrdinalIgnoreCase) -lt 0) {
                continue
            }
            if (-not (Test-LineHasRetiredContext -Line $lineText)) {
                $findings.Add((New-Finding -Category 'current_doc_retired_term' -Path $relative -Line ($index + 1) -Pattern ([string]$pattern) -Text $lineText)) | Out-Null
            }
        }
    }
}

foreach ($relative in @($config.current_behavior_tests)) {
    $fullPath = Join-Path $RepoRoot $relative
    $lines = @(Get-TextFileLines -Path $fullPath)
    for ($index = 0; $index -lt $lines.Count; $index++) {
        $lineText = [string]$lines[$index]
        foreach ($pattern in @($config.current_behavior_test_forbidden_patterns)) {
            if ($lineText.IndexOf([string]$pattern, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
                $findings.Add((New-Finding -Category 'current_behavior_test_retired_field_read' -Path $relative -Line ($index + 1) -Pattern ([string]$pattern) -Text $lineText)) | Out-Null
            }
        }
    }
}

foreach ($relative in @($config.historical_docs)) {
    $fullPath = Join-Path $RepoRoot $relative
    $lines = @(Get-TextFileLines -Path $fullPath)
    if ($lines.Count -eq 0) {
        continue
    }
    $hasRetiredTerm = $false
    foreach ($lineText in @($lines)) {
        foreach ($pattern in @($config.retired_terms)) {
            if ([string]$lineText -and [string]$lineText.IndexOf([string]$pattern, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
                $hasRetiredTerm = $true
                break
            }
        }
        if ($hasRetiredTerm) { break }
    }
    if (-not $hasRetiredTerm) {
        continue
    }
    $header = (@($lines | Select-Object -First 20) -join "`n")
    $hasMarker = $false
    foreach ($marker in @($config.historical_markers)) {
        if ($header.IndexOf([string]$marker, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
            $hasMarker = $true
            break
        }
    }
    if (-not $hasMarker) {
        $findings.Add((New-Finding -Category 'historical_doc_unmarked_retired_term' -Path $relative -Line 1 -Pattern 'historical_marker' -Text 'Historical document contains retired terms but lacks a retired/historical marker in the first 20 lines.')) | Out-Null
    }
}

$executionInternalCount = 0
foreach ($entry in @($config.execution_internal_allowlist)) {
    $relative = [string]$entry.path
    $fullPath = Join-Path $RepoRoot $relative
    foreach ($lineText in @(Get-TextFileLines -Path $fullPath)) {
        if ([string]$lineText -and $lineText.IndexOf('specialist_dispatch', [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
            $executionInternalCount += 1
        }
    }
}

$summary = [pscustomobject]@{
    current_doc_retired_term_violation_count = @($findings | Where-Object { $_.category -eq 'current_doc_retired_term' }).Count
    current_behavior_test_retired_field_read_count = @($findings | Where-Object { $_.category -eq 'current_behavior_test_retired_field_read' }).Count
    historical_doc_unmarked_retired_term_count = @($findings | Where-Object { $_.category -eq 'historical_doc_unmarked_retired_term' }).Count
    execution_internal_specialist_dispatch_reference_count = [int]$executionInternalCount
    findings = [object[]]$findings.ToArray()
}

if ($Json) {
    $summary | ConvertTo-Json -Depth 20
} else {
    '=== VCO Routing Terminology Hard Cleanup Scan ==='
    ('Current docs retired-term violations: {0}' -f [int]$summary.current_doc_retired_term_violation_count)
    ('Current behavior test retired-field reads: {0}' -f [int]$summary.current_behavior_test_retired_field_read_count)
    ('Historical docs without retired marker: {0}' -f [int]$summary.historical_doc_unmarked_retired_term_count)
    ('Execution-internal specialist_dispatch allowlist references: {0}' -f [int]$summary.execution_internal_specialist_dispatch_reference_count)
    foreach ($finding in @($summary.findings)) {
        '[FAIL] {0}:{1} [{2}] {3}' -f $finding.path, $finding.line, $finding.pattern, $finding.text
    }
    if (@($summary.findings).Count -eq 0) {
        'Gate Result: PASS'
    } else {
        'Gate Result: FAIL'
    }
}

if (@($summary.findings).Count -gt 0) {
    exit 1
}
exit 0
```

- [ ] **Step 3: Run the scan test and verify red state**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_routing_terminology_hard_cleanup.py::RoutingTerminologyHardCleanupTests::test_hard_cleanup_scan_reports_json -q
```

Expected: fail because `test_root_child_hierarchy_bridge.py` reads `specialist_dispatch` as a current behavior packet field and selected historical docs lack retired markers.

- [ ] **Step 4: Commit the scan red-state infrastructure only if no source behavior changed**

Do not commit a failing gate as final state. If committing intermediate red-state is not desired, keep Task 2 changes uncommitted and continue Task 3 and Task 4 before the first commit. If committing is acceptable for a work-in-progress branch, use:

```powershell
git add config/routing-terminology-hard-cleanup.json scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 tests/runtime_neutral/test_routing_terminology_hard_cleanup.py
git commit -m "test: add routing terminology hard cleanup scan"
```

Expected: commit only on an isolated implementation branch, not on `main`.

---

### Task 3: Remove Retired Root Packet Reads From Child Hierarchy Tests

**Files:**
- Modify: `tests/runtime_neutral/test_root_child_hierarchy_bridge.py`
- Test: `tests/runtime_neutral/test_root_child_hierarchy_bridge.py`
- Test: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`

- [ ] **Step 1: Rewrite root approved-skill extraction**

In `tests/runtime_neutral/test_root_child_hierarchy_bridge.py`, replace:

```python
            root_approved_dispatch = list(
                (root_runtime_input_packet.get("specialist_dispatch") or {}).get("approved_dispatch") or []
            )
            approved_skill_ids: list[str] = []
            if root_approved_dispatch:
                first_skill_id = str(root_approved_dispatch[0].get("skill_id", "")).strip()
                if first_skill_id:
                    approved_skill_ids = [first_skill_id]
```

with:

```python
            root_selected_skills = list(root_runtime_input_packet["skill_routing"]["selected"])
            approved_skill_ids: list[str] = []
            if root_selected_skills:
                first_skill_id = str(root_selected_skills[0].get("skill_id", "")).strip()
                if first_skill_id and first_skill_id != "vibe":
                    approved_skill_ids = [first_skill_id]
```

- [ ] **Step 2: Rewrite child packet specialist decision assertions**

In the same test file, replace:

```python
            specialist_dispatch = runtime_input_packet["specialist_dispatch"]
            local_suggestions = list(specialist_dispatch.get("local_specialist_suggestions") or [])
            approved_dispatch = list(specialist_dispatch.get("approved_dispatch") or [])
            approved_ids = {str(entry.get("skill_id", "")) for entry in approved_dispatch}

            if local_suggestions:
                self.assertTrue(bool(specialist_dispatch.get("escalation_required", False)))
                self.assertEqual("root_approval_required", str(specialist_dispatch.get("escalation_status", "")))
                for suggestion in local_suggestions:
                    with self.subTest(suggestion=str(suggestion.get("skill_id", ""))):
                        self.assertNotIn(str(suggestion.get("skill_id", "")), approved_ids)

            self.assertEqual("auto_promote_when_safe_same_round", str(specialist_dispatch.get("status", "")))
```

with:

```python
            self.assertNotIn("specialist_dispatch", runtime_input_packet)
            specialist_decision = runtime_input_packet["specialist_decision"]
            local_suggestions = list(specialist_decision.get("local_suggestion_skill_ids") or [])
            approved_ids = {
                str(skill_id)
                for skill_id in list(specialist_decision.get("approved_dispatch_skill_ids") or [])
                if str(skill_id).strip()
            }

            if local_suggestions:
                self.assertEqual("local_suggestion_only", str(specialist_decision.get("decision_state", "")))
                for suggestion_skill_id in local_suggestions:
                    with self.subTest(suggestion=str(suggestion_skill_id)):
                        self.assertNotIn(str(suggestion_skill_id), approved_ids)
            else:
                self.assertIn(
                    str(specialist_decision.get("decision_state", "")),
                    {"approved_dispatch", "no_specialist_recommendations"},
                )
```

If this replacement fails because the child runtime still emits
`specialist_dispatch`, stop and inspect `New-VibeRuntimeInputPacketProjection`.
Do not remove child governance assertions; only migrate the packet field used
for the assertion.

- [ ] **Step 3: Run the child hierarchy test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_root_child_hierarchy_bridge.py -q
```

Expected: all tests in the file pass. If behavior differs, fix the test to
assert `skill_routing` and `specialist_decision`, not old root packet
`specialist_dispatch`.

- [ ] **Step 4: Run the hard cleanup scan test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_routing_terminology_hard_cleanup.py::RoutingTerminologyHardCleanupTests::test_hard_cleanup_scan_reports_json -q
```

Expected: still fail only on historical-doc markers if Task 4 has not been
completed. There should be no `current_behavior_test_retired_field_read`
finding for `test_root_child_hierarchy_bridge.py`.

- [ ] **Step 5: Commit the test boundary cleanup**

Run:

```powershell
git add tests/runtime_neutral/test_root_child_hierarchy_bridge.py
git commit -m "test: remove retired dispatch reads from child hierarchy tests"
```

Expected: commit succeeds after `test_root_child_hierarchy_bridge.py` passes.

---

### Task 4: Add Current Execution Vocabulary Aliases

**Files:**
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
- Modify: `tests/runtime_neutral/test_l_xl_native_execution_topology.py`

- [ ] **Step 1: Add failing assertions for execution alias fields**

In `tests/runtime_neutral/test_l_xl_native_execution_topology.py`, find the
test that reads `execution_manifest["specialist_accounting"]` and asserts
`specialist_dispatch_outcomes`. Add assertions near the existing accounting
checks:

```python
            self.assertIn("skill_execution_unit_count", execution_manifest["specialist_accounting"])
            self.assertIn("execution_skill_outcomes", execution_manifest["specialist_accounting"])
            self.assertEqual(
                execution_manifest["specialist_accounting"]["specialist_dispatch_unit_count"],
                execution_manifest["specialist_accounting"]["skill_execution_unit_count"],
            )
            self.assertEqual(
                len(list(execution_manifest["specialist_accounting"]["specialist_dispatch_outcomes"])),
                len(list(execution_manifest["specialist_accounting"]["execution_skill_outcomes"])),
            )
```

If the file has multiple manifest-accounting tests, add the assertion to the
smallest test that already runs a governed runtime and inspects
`specialist_accounting`.

- [ ] **Step 2: Run the targeted test and verify red state**

Run the exact test containing the new assertions, for example:

```powershell
python -m pytest tests/runtime_neutral/test_l_xl_native_execution_topology.py::LXLNativeExecutionTopologyTests::test_approved_specialist_dispatch_routes_directly_in_current_session_by_default -q
```

Expected: fail because `skill_execution_unit_count` and
`execution_skill_outcomes` are not emitted yet.

- [ ] **Step 3: Add alias fields in execution manifest projections**

In `scripts/runtime/Invoke-PlanExecute.ps1`, locate the two objects that emit
`specialist_accounting` and contain:

```powershell
    specialist_dispatch_unit_count = [int]$specialistDispatchUnitCount
    specialist_dispatch_outcome_count = $totalSpecialistDispatchOutcomeCount
    specialist_dispatch_outcomes = @(@($nonDegradedExecutedSpecialistUnits) + @($blockedSpecialistUnits) + @($degradedSpecialistUnits))
```

Add current vocabulary aliases immediately beside the existing fields:

```powershell
    skill_execution_unit_count = [int]$specialistDispatchUnitCount
    execution_skill_outcome_count = $totalSpecialistDispatchOutcomeCount
    execution_skill_outcomes = @(@($nonDegradedExecutedSpecialistUnits) + @($blockedSpecialistUnits) + @($degradedSpecialistUnits))
```

Do not remove the old internal fields in this task. Removing them is a later
compatibility step after downstream tests use the current aliases.

- [ ] **Step 4: Run the targeted topology test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_l_xl_native_execution_topology.py::LXLNativeExecutionTopologyTests::test_approved_specialist_dispatch_routes_directly_in_current_session_by_default -q
```

Expected: pass.

- [ ] **Step 5: Run the full topology file**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_l_xl_native_execution_topology.py -q
```

Expected: pass.

- [ ] **Step 6: Commit execution alias fields**

Run:

```powershell
git add scripts/runtime/Invoke-PlanExecute.ps1 tests/runtime_neutral/test_l_xl_native_execution_topology.py
git commit -m "feat: expose current skill execution accounting aliases"
```

Expected: commit succeeds.

---

### Task 5: Mark Historical Retired Routing Docs

**Files:**
- Modify historical docs listed below.
- Test: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`

- [ ] **Step 1: Add retired markers to governance docs**

For each of these files, add this block immediately after the H1 heading:

```markdown
> Historical / Retired Note: This document records a previous routing design or
> migration state. Current routing authority is defined by
> `docs/governance/current-routing-contract.md` and
> `docs/governance/current-runtime-field-contract.md`.
```

Files:

```text
docs/governance/binary-skill-usage-routing-2026-04-28.md
docs/governance/simplified-skill-routing-2026-04-29.md
docs/governance/terminology-governance.md
docs/governance/specialist-dispatch-governance.md
```

If `terminology-governance.md` already claims to be the current terminology
source, replace that claim with a pointer to
`current-runtime-field-contract.md`; do not leave two current terminology
authorities.

- [ ] **Step 2: Add retired markers to old superpowers specs**

For each of these files, add the same historical marker immediately after the
H1 heading:

```text
docs/superpowers/specs/2026-04-10-vibe-aggressive-specialist-routing-design.md
docs/superpowers/specs/2026-04-12-vibe-approved-dispatch-user-disclosure-design.md
docs/superpowers/specs/2026-04-12-vibe-discussion-time-specialist-consultation-design.md
docs/superpowers/specs/2026-04-12-vibe-host-stage-disclosure-protocol-design.md
```

- [ ] **Step 3: Run the hard cleanup scan**

Run:

```powershell
.\scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1
```

Expected:

```text
Historical docs without retired marker: 0
Gate Result: PASS
```

If it still fails, fix only the named document markers or current behavior test
reads. Do not broaden allowlists to hide real current-surface violations.

- [ ] **Step 4: Run the hard cleanup test file**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_routing_terminology_hard_cleanup.py -q
```

Expected: all tests pass.

- [ ] **Step 5: Commit historical markers**

Run:

```powershell
git add docs/governance/binary-skill-usage-routing-2026-04-28.md docs/governance/simplified-skill-routing-2026-04-29.md docs/governance/terminology-governance.md docs/governance/specialist-dispatch-governance.md docs/superpowers/specs/2026-04-10-vibe-aggressive-specialist-routing-design.md docs/superpowers/specs/2026-04-12-vibe-approved-dispatch-user-disclosure-design.md docs/superpowers/specs/2026-04-12-vibe-discussion-time-specialist-consultation-design.md docs/superpowers/specs/2026-04-12-vibe-host-stage-disclosure-protocol-design.md
git commit -m "docs: mark retired routing history"
```

Expected: commit succeeds.

---

### Task 6: Integrate Hard Cleanup Scan Into Current Routing Gate

**Files:**
- Modify: `scripts/verify/vibe-current-routing-contract-scan.ps1`
- Modify: `tests/runtime_neutral/test_current_routing_contract_scan.py`

- [ ] **Step 1: Add failing expectation to current scan test**

In `tests/runtime_neutral/test_current_routing_contract_scan.py`, update the JSON test to assert these fields:

```python
self.assertIn("hard_cleanup_current_doc_retired_term_violation_count", payload)
self.assertIn("hard_cleanup_current_behavior_test_retired_field_read_count", payload)
self.assertIn("hard_cleanup_historical_doc_unmarked_retired_term_count", payload)
self.assertEqual(0, int(payload["hard_cleanup_current_doc_retired_term_violation_count"]))
self.assertEqual(0, int(payload["hard_cleanup_current_behavior_test_retired_field_read_count"]))
self.assertEqual(0, int(payload["hard_cleanup_historical_doc_unmarked_retired_term_count"]))
```

Update the plain-output test to assert:

```python
self.assertIn("Hard cleanup current behavior test retired-field reads: 0", completed.stdout)
```

- [ ] **Step 2: Run the current scan test and verify red state**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_contract_scan.py -q
```

Expected: fail because the existing current scan does not include hard cleanup
summary fields.

- [ ] **Step 3: Call hard cleanup scan from current scan**

In `scripts/verify/vibe-current-routing-contract-scan.ps1`, after the existing
`$summary` is built, invoke the hard cleanup scan in JSON mode:

```powershell
$hardCleanupScript = Join-Path $RepoRoot 'scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1'
$hardCleanup = $null
if (Test-Path -LiteralPath $hardCleanupScript) {
    $hardJson = & $hardCleanupScript -RepoRoot $RepoRoot -Json
    $hardCleanup = $hardJson | ConvertFrom-Json
}
```

Add these properties to the summary object:

```powershell
hard_cleanup_current_doc_retired_term_violation_count = if ($hardCleanup) { [int]$hardCleanup.current_doc_retired_term_violation_count } else { 0 }
hard_cleanup_current_behavior_test_retired_field_read_count = if ($hardCleanup) { [int]$hardCleanup.current_behavior_test_retired_field_read_count } else { 0 }
hard_cleanup_historical_doc_unmarked_retired_term_count = if ($hardCleanup) { [int]$hardCleanup.historical_doc_unmarked_retired_term_count } else { 0 }
hard_cleanup_execution_internal_specialist_dispatch_reference_count = if ($hardCleanup) { [int]$hardCleanup.execution_internal_specialist_dispatch_reference_count } else { 0 }
```

In plain output, add:

```powershell
('Hard cleanup current docs retired-term violations: {0}' -f [int]$summary.hard_cleanup_current_doc_retired_term_violation_count)
('Hard cleanup current behavior test retired-field reads: {0}' -f [int]$summary.hard_cleanup_current_behavior_test_retired_field_read_count)
('Hard cleanup historical docs without retired marker: {0}' -f [int]$summary.hard_cleanup_historical_doc_unmarked_retired_term_count)
```

Update PASS/FAIL logic so it fails if any of the three hard cleanup violation
counts are greater than zero.

- [ ] **Step 4: Run current scan tests and both scan scripts**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_contract_scan.py tests/runtime_neutral/test_routing_terminology_hard_cleanup.py -q
.\scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1
.\scripts\verify\vibe-current-routing-contract-scan.ps1
```

Expected:

```text
Gate Result: PASS
```

for both scripts.

- [ ] **Step 5: Commit scan integration**

Run:

```powershell
git add scripts/verify/vibe-current-routing-contract-scan.ps1 tests/runtime_neutral/test_current_routing_contract_scan.py
git commit -m "test: include hard cleanup scan in routing contract gate"
```

Expected: commit succeeds.

---

### Task 7: Focused Regression Matrix

**Files:**
- No planned edits unless a focused test failure identifies a current-format regression.

- [ ] **Step 1: Run routing terminology and contract tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_routing_terminology_hard_cleanup.py tests/runtime_neutral/test_retired_old_routing_compat.py tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py -q
```

Expected: all selected tests pass.

- [ ] **Step 2: Run child/runtime execution tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_root_child_hierarchy_bridge.py tests/runtime_neutral/test_runtime_contract_schema.py tests/runtime_neutral/test_runtime_delivery_acceptance.py tests/runtime_neutral/test_skill_promotion_destructive_gate.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_l_xl_native_execution_topology.py -q
```

Expected: all selected tests pass.

- [ ] **Step 3: Fix only current-format regressions**

If Step 1 or Step 2 fails, fix only one of these categories:

```text
current routing field contract
current behavior test retired-field reads
historical doc retired markers
execution alias fields derived from existing accounting
scan false positives with an explicit allowlist reason
```

Do not reintroduce old packet compatibility or old consultation sections.

- [ ] **Step 4: Commit regression fixes if needed**

If files changed in Step 3, run:

```powershell
git status --short
git add docs/governance/current-runtime-field-contract.md config/routing-terminology-hard-cleanup.json scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 scripts/verify/vibe-current-routing-contract-scan.ps1 scripts/runtime/Invoke-PlanExecute.ps1 tests/runtime_neutral/test_routing_terminology_hard_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py tests/runtime_neutral/test_root_child_hierarchy_bridge.py tests/runtime_neutral/test_l_xl_native_execution_topology.py
git commit -m "fix: stabilize routing terminology hard cleanup"
```

Expected: commit succeeds. If no files changed, skip this commit.

---

### Task 8: Broad Gates And Merge Readiness

**Files:**
- No planned edits unless a broad gate identifies a current-format bug.

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

Expected:

```text
Gate Result: PASS
```

for both gates.

- [ ] **Step 5: Run routing scans**

Run:

```powershell
.\scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1
.\scripts\verify\vibe-current-routing-contract-scan.ps1
```

Expected:

```text
Gate Result: PASS
```

for both scans, with:

```text
Current behavior test retired-field reads: 0
Historical docs without retired marker: 0
Current runtime old-format fallbacks: 0
```

- [ ] **Step 6: Run whitespace and status checks**

Run:

```powershell
git diff --check
git status --short --branch
git log --oneline -n 12
```

Expected:

```text
git diff --check has no output
git status shows no uncommitted source changes except explicitly ignored local runtime artifacts
latest commits include the hard cleanup contract, scan, test migration, historical markers, and scan integration
```

- [ ] **Step 7: Final report requirements**

Final report must state:

- Current model remains `skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused`.
- Six governed stages are unchanged.
- Current docs and current behavior tests are guarded by the hard cleanup scan.
- Historical retired docs are marked instead of silently acting as current guidance.
- Current root runtime packets still do not emit retired routing fields.
- Any remaining `specialist_dispatch` references are execution-internal allowlisted references or retired tests.
- All focused tests and broad gates run in this task, with exact pass/fail counts or gate outputs.

After all tasks complete, use `superpowers:finishing-a-development-branch`.
