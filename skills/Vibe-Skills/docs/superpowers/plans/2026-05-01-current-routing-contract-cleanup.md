# Current Routing Contract Cleanup Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the current Vibe routing surface explainable as `skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused` while keeping legacy artifact compatibility readable.

**Architecture:** Add current-surface tests first, then clean generated runtime text and summaries so current outputs prefer `skill_routing` and `skill_usage`. Keep old consultation code behind a clearly labeled legacy compatibility boundary and add a residual-debt scan so future cleanup can distinguish current violations from intentional legacy references.

**Tech Stack:** PowerShell runtime scripts, Python `unittest` / `pytest`, Markdown governance docs, existing Vibe verification gates.

---

## File Structure

- Create: `tests/runtime_neutral/test_current_routing_contract_cleanup.py`
  - Current-surface contract tests for new runtime sessions, generated docs,
    lifecycle text, host briefing, and legacy boundary wording.
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
  - Tighten current lifecycle and host-briefing text.
  - Keep consultation projection text clearly legacy-only.
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
  - Remove active legacy wording from current generated requirement docs.
  - Keep nullable legacy receipt handling.
- Modify: `scripts/runtime/Write-XlPlan.ps1`
  - Remove active legacy wording from current generated execution plans.
  - Keep nullable legacy receipt handling.
- Modify: `scripts/runtime/VibeConsultation.Common.ps1`
  - Add a top-level legacy compatibility comment and avoid presenting the
    module as a current route module.
- Create: `docs/governance/current-routing-contract.md`
  - Current terminology contract for future development.
- Create: `scripts/verify/vibe-current-routing-contract-scan.ps1`
  - A focused scan that reports current-surface violations separately from
    legacy compatibility and historical references.
- Create: `tests/runtime_neutral/test_current_routing_contract_scan.py`
  - Tests the scan script on synthetic text and the live repository.

Do not delete `scripts/runtime/VibeConsultation.Common.ps1` in this plan.
Do not physically delete skill directories in this plan.
Do not change pack routing config unless a focused test proves a current-surface
regression depends on it.

---

### Task 1: Add Current Runtime Surface Contract Tests

**Files:**
- Create: `tests/runtime_neutral/test_current_routing_contract_cleanup.py`

- [ ] **Step 1: Create the test file**

Create `tests/runtime_neutral/test_current_routing_contract_cleanup.py` with:

```python
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "invoke-vibe-runtime.ps1"
RUNTIME_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeRuntime.Common.ps1"

CURRENT_TASK = (
    "Build a scikit-learn classification baseline, include a result figure, "
    "and explain which selected skills were used or unused."
)

ACTIVE_FORBIDDEN_PATTERNS = [
    r"\bstage assistant\b",
    r"\broute owner\b",
    r"\broute authority\b",
    r"\bprimary skill\b",
    r"\bsecondary skill\b",
    r"\bconsultation expert\b",
    r"\bauxiliary expert\b",
    r"\bconsulted units\b",
    r"\bapproved consultation\b",
    r"## Specialist Consultation",
]


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

    run_id = "pytest-current-routing-contract-" + uuid.uuid4().hex[:10]
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


def assert_current_text_clean(testcase: unittest.TestCase, text: str, *, label: str) -> None:
    lowered = text.lower()
    for pattern in ACTIVE_FORBIDDEN_PATTERNS:
        testcase.assertIsNone(
            re.search(pattern, lowered, flags=re.IGNORECASE),
            msg=f"{label} contains active legacy routing wording matching {pattern!r}",
        )


class CurrentRoutingContractCleanupTests(unittest.TestCase):
    def test_new_runtime_outputs_only_current_routing_and_usage_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            payload = run_runtime(CURRENT_TASK, Path(tempdir))

            summary = payload["summary"]
            artifacts = summary["artifacts"]
            session_root = Path(payload["session_root"])

            self.assertIsNone(summary.get("specialist_consultation"))
            self.assertIsNone(artifacts.get("discussion_specialist_consultation"))
            self.assertIsNone(artifacts.get("planning_specialist_consultation"))
            self.assertEqual(
                [],
                sorted(path.name for path in session_root.glob("*specialist-consultation*.json")),
            )

            lifecycle = summary["specialist_lifecycle_disclosure"]
            self.assertEqual("skill_routing_usage_evidence", lifecycle["truth_model"])
            self.assertIn("skill_usage.used", lifecycle["rendered_text"])
            self.assertIn("selected skills", lifecycle["rendered_text"].lower())
            assert_current_text_clean(self, lifecycle["rendered_text"], label="lifecycle rendered text")

            requirement_doc = Path(artifacts["requirement_doc"]).read_text(encoding="utf-8")
            execution_plan = Path(artifacts["execution_plan"]).read_text(encoding="utf-8")
            host_briefing = Path(artifacts["host_user_briefing"]).read_text(encoding="utf-8")

            for label, text in {
                "requirement doc": requirement_doc,
                "execution plan": execution_plan,
                "host briefing": host_briefing,
            }.items():
                assert_current_text_clean(self, text, label=label)
                self.assertIn("skill_usage", text, msg=f"{label} should mention skill_usage evidence")

            self.assertIn("## Skill Usage", requirement_doc)
            self.assertIn("## Binary Skill Usage Plan", execution_plan)

    def test_runtime_packet_keeps_legacy_fields_boxed_under_legacy_skill_routing(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            payload = run_runtime(CURRENT_TASK, Path(tempdir))
            packet_path = Path(payload["summary"]["artifacts"]["runtime_input_packet"])
            packet = load_json(packet_path)

            self.assertIn("skill_routing", packet)
            self.assertIn("skill_usage", packet)
            self.assertIn("legacy_skill_routing", packet)
            self.assertNotIn("specialist_recommendations", packet)
            self.assertNotIn("specialist_dispatch", packet)
            self.assertNotIn("stage_assistant_hints", packet)
            self.assertIn("specialist_recommendations", packet["legacy_skill_routing"])
            self.assertIn("specialist_dispatch", packet["legacy_skill_routing"])
            self.assertIn("stage_assistant_hints", packet["legacy_skill_routing"])

    def test_legacy_consultation_projection_is_explicitly_legacy(self) -> None:
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
            "$lifecycle = New-VibeSpecialistLifecycleDisclosureProjection -RuntimeInputPacket $null -DiscussionConsultationReceipt $receipt; "
            "$markdown = Get-VibeSpecialistLifecycleDisclosureMarkdownLines -LifecycleDisclosure $lifecycle; "
            "[pscustomobject]@{ "
            "layer_id = $layer.layer_id; "
            "truth_layer = $layer.truth_layer; "
            "truth_model = $lifecycle.truth_model; "
            "markdown = ($markdown -join \"`n\") "
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
        self.assertEqual("legacy_routing_consultation_execution_separated", payload["truth_model"])
        self.assertIn("## Legacy Specialist Lifecycle Disclosure", payload["markdown"])
        self.assertIn("Usage claims still require `skill_usage.used` evidence", payload["markdown"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the current-surface tests and verify the red state**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_contract_cleanup.py -q
```

Expected: at least one test fails because current generated host briefing or
runtime text still contains active legacy-routing wording such as `stage
assistant`, `route owner`, `approved consultation`, or `## Specialist
Consultation` in a current context.

Do not commit this red state.

---

### Task 2: Clean Current Runtime Output Text

**Files:**
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
- Modify: `scripts/runtime/Write-XlPlan.ps1`
- Test: `tests/runtime_neutral/test_current_routing_contract_cleanup.py`

- [ ] **Step 1: Update current lifecycle wording in `VibeRuntime.Common.ps1`**

In `Get-VibeSpecialistLifecycleDisclosureMarkdownLines`, keep the legacy branch
unchanged and make the non-legacy branch use current contract wording only.
Replace the non-legacy line array with:

```powershell
@(
    '## Skill Routing And Usage Evidence',
    'This disclosure records selected skills and material-use evidence. A selected skill is not a `used` claim; material use requires `skill_usage.used` plus `skill_usage.evidence`.'
)
```

This keeps the old legacy branch readable while ensuring new current sessions
describe only selection and usage evidence.

- [ ] **Step 2: Remove active dispatch wording from current host briefing text**

In `New-VibeHostUserBriefingSegmentProjection`, keep legacy consultation segment
text only inside the branch whose `$segmentId` matches `discussion_consultation`
or `planning_consultation`. For the `execution_dispatch` branch, change the
current wording so it does not describe dispatch as usage.

Use this wording for the execution segment:

```powershell
$segmentLines += 'Selected skills are available for execution. This is not a `used` claim; final use must come from `skill_usage.used` and evidence.'
```

Keep any existing skill bullet rendering after that line.

- [ ] **Step 3: Clean current requirement-doc selected-skill wording**

In `scripts/runtime/Write-RequirementDoc.ps1`, keep the `## Selected Skill`
section. Ensure the explanatory text uses:

```powershell
'Router candidates remain in `runtime-input-packet.json` for audit. The current work surface records selected skills here and material use in `skill_usage.used` / `skill_usage.unused`.'
```

If the section still contains current-session explanatory lines that describe
selected skills as `stage assistant`, `primary skill`, or `secondary skill`,
rewrite those lines to the wording above. Do not remove nullable legacy receipt
handling from compatibility-only branches.

- [ ] **Step 4: Clean current XL-plan wording**

In `scripts/runtime/Write-XlPlan.ps1`, keep `## Binary Skill Usage Plan`.
Ensure the current explanatory lines include:

```powershell
'- This section lists only skills selected into the six-stage work through `skill_routing.selected`.'
'- Execution must preserve the loaded skill workflow and report final use only from `skill_usage.used` / `skill_usage.unused`.'
```

If a current-session line says `approved consultation`, `stage assistant`,
`primary skill`, or `secondary skill`, replace it with the two lines above
unless the line is inside a branch that renders a non-null legacy consultation
receipt.

- [ ] **Step 5: Run the new current-surface tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_contract_cleanup.py -q
```

Expected: all tests in `test_current_routing_contract_cleanup.py` pass.

- [ ] **Step 6: Run focused existing routing and usage tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_active_consultation_simplification.py tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_runtime_route_output_shape.py -q
```

Expected: all selected tests pass.

- [ ] **Step 7: Commit current output cleanup**

Run:

```powershell
git add scripts/runtime/VibeRuntime.Common.ps1 scripts/runtime/Write-RequirementDoc.ps1 scripts/runtime/Write-XlPlan.ps1 tests/runtime_neutral/test_current_routing_contract_cleanup.py
git commit -m "fix: clean current routing output surface"
```

Expected: commit succeeds.

---

### Task 3: Mark Consultation Runtime As Legacy Compatibility

**Files:**
- Modify: `scripts/runtime/VibeConsultation.Common.ps1`
- Modify: `tests/runtime_neutral/test_vibe_specialist_consultation.py`
- Test: `tests/runtime_neutral/test_vibe_specialist_consultation.py`
- Test: `tests/runtime_neutral/test_current_routing_contract_cleanup.py`

- [ ] **Step 1: Add a top-level legacy compatibility comment**

At the top of `scripts/runtime/VibeConsultation.Common.ps1`, after any initial
strict-mode or helper prologue, add this comment block:

```powershell
# Legacy compatibility boundary:
# This module reads and verifies old specialist-consultation receipts. It is not
# part of the current default routing model. New runtime sessions use
# skill_routing.selected plus skill_usage.used / skill_usage.unused for current
# skill selection and material-use proof.
```

Do not change function signatures in this step.

- [ ] **Step 2: Add a legacy marker constant for tests and future scans**

Near the comment block, add:

```powershell
$script:VibeConsultationCompatibilityBoundary = 'legacy_consultation_compatibility_only'
```

Do not export this as a new public API. It exists so scans and future readers
can identify the module boundary.

- [ ] **Step 3: Add a direct module-boundary test**

Append this method to `VibeSpecialistConsultationTests` in
`tests/runtime_neutral/test_vibe_specialist_consultation.py`:

```python
    def test_consultation_module_declares_legacy_compatibility_boundary(self) -> None:
        text = CONSULTATION_SCRIPT.read_text(encoding="utf-8")

        self.assertIn("Legacy compatibility boundary:", text)
        self.assertIn("legacy_consultation_compatibility_only", text)
        self.assertIn("New runtime sessions use", text)
        self.assertIn("skill_routing.selected", text)
        self.assertIn("skill_usage.used / skill_usage.unused", text)
```

- [ ] **Step 4: Rename the old direct-window test names to show legacy scope**

In `tests/runtime_neutral/test_vibe_specialist_consultation.py`, rename these
methods without changing their behavior:

```text
test_consultation_window_invokes_specialist_and_emits_progressive_disclosure
  -> test_legacy_consultation_window_invokes_specialist_and_emits_progressive_disclosure

test_consultation_window_bypasses_codex_repo_check_for_non_git_roots
  -> test_legacy_consultation_window_bypasses_codex_repo_check_for_non_git_roots

test_consultation_window_fails_verification_when_non_git_working_root_is_modified
  -> test_legacy_consultation_window_fails_verification_when_non_git_working_root_is_modified

test_consultation_window_falls_back_to_writable_artifact_root_when_repo_root_is_read_only
  -> test_legacy_consultation_window_falls_back_to_writable_artifact_root_when_repo_root_is_read_only

test_live_consultation_with_empty_guidance_routes_directly_and_keeps_freeze_gate_green
  -> test_legacy_consultation_with_empty_guidance_routes_directly_and_keeps_freeze_gate_green
```

Do not rename the class in this task. Keeping the file stable avoids broad test
discovery churn.

- [ ] **Step 5: Run legacy consultation tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_current_routing_contract_cleanup.py -q
```

Expected: all selected tests pass.

- [ ] **Step 6: Commit legacy boundary marking**

Run:

```powershell
git add scripts/runtime/VibeConsultation.Common.ps1 tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_current_routing_contract_cleanup.py
git commit -m "test: mark consultation runtime legacy-only"
```

Expected: commit succeeds.

---

### Task 4: Add Current Routing Governance Document

**Files:**
- Create: `docs/governance/current-routing-contract.md`
- Modify: `tests/runtime_neutral/test_current_routing_contract_cleanup.py`

- [ ] **Step 1: Create the governance document**

Create `docs/governance/current-routing-contract.md` with:

```markdown
# Current Routing Contract

Date: 2026-05-01

## Current Model

The current Vibe-Skills routing model is:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused
```

This is the only model current user-facing docs and generated runtime outputs
should teach.

## Terms

| Term | Meaning |
| --- | --- |
| `candidate` | A skill was considered by routing. This is not a use claim. |
| `selected` | A skill was chosen into the work surface through `skill_routing.selected`. This is not a use claim. |
| `used` | A selected or loaded skill shaped an artifact and appears in `skill_usage.used` with evidence. |
| `unused` | A selected or loaded skill did not shape an artifact and appears in `skill_usage.unused`. |
| `evidence` | A stage, artifact reference, and impact summary proving material skill use. |
| `legacy compatibility` | Old routing, consultation, or dispatch records remain readable for history, but they do not define current behavior. |

## Usage Proof

A skill may be reported as used only when all of these are true:

1. The skill appears in `skill_usage.used`.
2. The skill has at least one `skill_usage.evidence` record.
3. The evidence names a concrete stage and artifact impact.

Routing, selection, old consultation receipts, and old dispatch records are not
usage proof.

## Current Output Rules

Current runtime outputs should use these names:

```text
skill_candidates
skill_routing.selected
skill_usage.used
skill_usage.unused
skill_usage.evidence
```

Current runtime outputs should not teach old routing mechanisms as active
behavior. Historical fields may appear only in clearly labeled legacy
compatibility sections.

## Legacy Compatibility Boundary

The following old fields may exist only for compatibility with old artifacts:

```text
legacy_skill_routing
specialist_recommendations
specialist_dispatch
stage_assistant_hints
discussion_specialist_consultation
planning_specialist_consultation
approved_consultation
consulted_units
discussion_consultation
planning_consultation
```

When current and legacy fields are both present, current code should prefer
`skill_routing` and `skill_usage`.

## Non-Goals

This contract does not delete old artifacts. It defines how current routing and
current usage claims should be explained and verified.
```

- [ ] **Step 2: Add a governance document test**

Append this method to `CurrentRoutingContractCleanupTests`:

```python
    def test_current_routing_governance_doc_defines_only_current_terms(self) -> None:
        path = REPO_ROOT / "docs" / "governance" / "current-routing-contract.md"
        text = path.read_text(encoding="utf-8")

        self.assertIn("skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused", text)
        for required in [
            "`candidate`",
            "`selected`",
            "`used`",
            "`unused`",
            "`evidence`",
            "`legacy compatibility`",
        ]:
            self.assertIn(required, text)

        active_section = text.split("## Legacy Compatibility Boundary", 1)[0]
        for forbidden in [
            "route owner",
            "primary skill",
            "secondary skill",
            "consultation expert",
            "auxiliary expert",
        ]:
            self.assertNotIn(forbidden, active_section.lower())
```

- [ ] **Step 3: Run the governance doc test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_contract_cleanup.py::CurrentRoutingContractCleanupTests::test_current_routing_governance_doc_defines_only_current_terms -q
```

Expected: the new test passes.

- [ ] **Step 4: Commit governance document**

Run:

```powershell
git add docs/governance/current-routing-contract.md tests/runtime_neutral/test_current_routing_contract_cleanup.py
git commit -m "docs: define current routing contract"
```

Expected: commit succeeds.

---

### Task 5: Add Current Routing Residual-Debt Scan

**Files:**
- Create: `scripts/verify/vibe-current-routing-contract-scan.ps1`
- Create: `tests/runtime_neutral/test_current_routing_contract_scan.py`

- [ ] **Step 1: Create the scan script**

Create `scripts/verify/vibe-current-routing-contract-scan.ps1` with:

```powershell
param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path,
    [switch]$Json
)

$ErrorActionPreference = 'Stop'

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

$currentSurfaceFiles = @(
    'SKILL.md',
    'README.md',
    'docs/governance/current-routing-contract.md',
    'scripts/runtime/Write-RequirementDoc.ps1',
    'scripts/runtime/Write-XlPlan.ps1',
    'scripts/runtime/invoke-vibe-runtime.ps1'
)

$legacyAllowedFiles = @(
    'scripts/runtime/VibeConsultation.Common.ps1',
    'tests/runtime_neutral/test_vibe_specialist_consultation.py',
    'tests/runtime_neutral/test_active_consultation_simplification.py'
)

$historicalRoots = @(
    'docs/superpowers/plans/',
    'docs/superpowers/specs/'
)

$activeForbiddenPatterns = @(
    'route owner',
    'primary skill',
    'secondary skill',
    'consultation expert',
    'auxiliary expert',
    'approved consultation',
    'consulted units'
)

$findings = New-Object System.Collections.Generic.List[object]

foreach ($relative in $currentSurfaceFiles) {
    $fullPath = Join-Path $RepoRoot $relative
    $lines = @(Get-TextFileLines -Path $fullPath)
    for ($index = 0; $index -lt $lines.Count; $index++) {
        $lineText = [string]$lines[$index]
        foreach ($pattern in $activeForbiddenPatterns) {
            if ($lineText.IndexOf($pattern, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
                $isLegacyLine = (
                    $lineText.IndexOf('legacy', [System.StringComparison]::OrdinalIgnoreCase) -ge 0 -or
                    $lineText.IndexOf('old artifact', [System.StringComparison]::OrdinalIgnoreCase) -ge 0 -or
                    $lineText.IndexOf('compatibility', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
                )
                if (-not $isLegacyLine) {
                    $findings.Add((New-Finding -Category 'current_surface_violation' -Path $relative -Line ($index + 1) -Pattern $pattern -Text $lineText)) | Out-Null
                }
            }
        }
    }
}

$legacyReferenceCount = 0
foreach ($relative in $legacyAllowedFiles) {
    $fullPath = Join-Path $RepoRoot $relative
    foreach ($line in @(Get-TextFileLines -Path $fullPath)) {
        if ($line -match 'consultation|stage_assistant|approved_consultation|consulted_units') {
            $legacyReferenceCount += 1
        }
    }
}

$historicalReferenceCount = 0
foreach ($root in $historicalRoots) {
    $fullRoot = Join-Path $RepoRoot $root
    if (-not (Test-Path -LiteralPath $fullRoot)) {
        continue
    }
    foreach ($file in Get-ChildItem -LiteralPath $fullRoot -Recurse -File -Include *.md) {
        foreach ($line in @(Get-Content -LiteralPath $file.FullName -Encoding UTF8)) {
            if ($line -match 'consultation|stage assistant|route owner|primary skill|secondary skill') {
                $historicalReferenceCount += 1
            }
        }
    }
}

$summary = [pscustomobject]@{
    current_surface_violation_count = @($findings | Where-Object { $_.category -eq 'current_surface_violation' }).Count
    legacy_reference_count = [int]$legacyReferenceCount
    historical_reference_count = [int]$historicalReferenceCount
    findings = [object[]]$findings.ToArray()
}

if ($Json) {
    $summary | ConvertTo-Json -Depth 20
} else {
    '=== VCO Current Routing Contract Scan ==='
    ('Current surface violations: {0}' -f [int]$summary.current_surface_violation_count)
    ('Legacy compatibility references: {0}' -f [int]$summary.legacy_reference_count)
    ('Historical doc references: {0}' -f [int]$summary.historical_reference_count)
    foreach ($finding in @($summary.findings)) {
        '[FAIL] {0}:{1} [{2}] {3}' -f $finding.path, $finding.line, $finding.pattern, $finding.text
    }
    if ([int]$summary.current_surface_violation_count -eq 0) {
        'Gate Result: PASS'
    } else {
        'Gate Result: FAIL'
    }
}

if ([int]$summary.current_surface_violation_count -gt 0) {
    exit 1
}
exit 0
```

- [ ] **Step 2: Create scan tests**

Create `tests/runtime_neutral/test_current_routing_contract_scan.py` with:

```python
from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCAN_SCRIPT = REPO_ROOT / "scripts" / "verify" / "vibe-current-routing-contract-scan.ps1"


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


class CurrentRoutingContractScanTests(unittest.TestCase):
    def test_scan_script_reports_json_and_no_current_surface_violations(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available")

        completed = subprocess.run(
            [shell, "-NoLogo", "-NoProfile", "-File", str(SCAN_SCRIPT), "-Json"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        payload = json.loads(completed.stdout)

        self.assertEqual(0, int(payload["current_surface_violation_count"]))
        self.assertIn("legacy_reference_count", payload)
        self.assertIn("historical_reference_count", payload)
        self.assertEqual([], payload["findings"])

    def test_scan_script_plain_output_has_pass_gate(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available")

        completed = subprocess.run(
            [shell, "-NoLogo", "-NoProfile", "-File", str(SCAN_SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )

        self.assertIn("VCO Current Routing Contract Scan", completed.stdout)
        self.assertIn("Gate Result: PASS", completed.stdout)
```

- [ ] **Step 3: Run scan tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_contract_scan.py -q
```

Expected: scan tests pass.

- [ ] **Step 4: Run the scan directly**

Run:

```powershell
.\scripts\verify\vibe-current-routing-contract-scan.ps1
```

Expected:

```text
Gate Result: PASS
```

- [ ] **Step 5: Commit scan script**

Run:

```powershell
git add scripts/verify/vibe-current-routing-contract-scan.ps1 tests/runtime_neutral/test_current_routing_contract_scan.py
git commit -m "test: add current routing contract scan"
```

Expected: commit succeeds.

---

### Task 6: Run Focused Runtime Regression Matrix

**Files:**
- No new edits unless a focused failure points to a specific changed file.

- [ ] **Step 1: Run focused pytest matrix**

Run:

```powershell
python -m pytest tests/unit/test_runtime_stage_machine.py tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py tests/runtime_neutral/test_active_consultation_simplification.py tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_runtime_route_output_shape.py -q
```

Expected: all selected tests pass.

- [ ] **Step 2: Fix any focused regression before continuing**

If Step 1 fails, read the first failure fully. Fix only the failing current
contract or legacy boundary behavior. Re-run the exact failing test first, then
re-run Step 1.

Expected after the fix:

```text
all selected tests pass
```

- [ ] **Step 3: Commit focused regression fix if needed**

If Step 2 changed files, run:

```powershell
git status --short
git add scripts/runtime/VibeRuntime.Common.ps1 scripts/runtime/Write-RequirementDoc.ps1 scripts/runtime/Write-XlPlan.ps1 scripts/runtime/VibeConsultation.Common.ps1 tests/runtime_neutral/test_current_routing_contract_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py tests/runtime_neutral/test_vibe_specialist_consultation.py
git commit -m "fix: stabilize current routing contract regression"
```

Expected: commit succeeds. If Step 2 made no changes, skip this commit step.
If `git status --short` shows a different focused regression file, add that
exact file instead and do not add unrelated workspace changes.

---

### Task 7: Run Broad Gates And Final Surface Report

**Files:**
- No new edits unless a verification failure points to a specific changed file.

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

- [ ] **Step 5: Run current routing contract scan**

Run:

```powershell
.\scripts\verify\vibe-current-routing-contract-scan.ps1
```

Expected:

```text
Current surface violations: 0
Gate Result: PASS
```

- [ ] **Step 6: Run whitespace check**

Run:

```powershell
git diff --check
```

Expected: no output.

- [ ] **Step 7: Confirm working tree**

Run:

```powershell
git status --short --branch
git log --oneline -n 8
```

Expected:

```text
git status shows no uncommitted source changes
latest commits include the current routing contract cleanup commits
```

- [ ] **Step 8: Final report requirements**

In the final report, state these facts:

- Current runtime routing is explained as
  `skill_candidates -> skill_routing.selected -> skill_usage.used / unused`.
- Legacy consultation remains readable but is not a current routing layer.
- `VibeConsultation.Common.ps1` was not deleted in this slice.
- Six governed stages are unchanged.
- Pack routing smoke, offline skills gate, config parity, version packaging,
  version consistency, current routing contract scan, and `git diff --check`
  results.
- Do not claim all historical consultation strings were deleted.
