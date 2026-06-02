# Governed Entry Lineage Hardening Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement runtime-validated governed-entry lineage and child-lane delegation-envelope enforcement so the official `vibe` path rejects out-of-order stages, child truth-surface reopening, and unapproved child specialist activation.

**Architecture:** Extend the existing root/child hierarchy contract rather than replacing it. Add minimal runtime artifacts and shared validation helpers in the runtime common layer, wire those helpers into root stage transitions and child startup, then update docs and verification gates so the runtime contract and the proof surfaces say the same thing.

**Tech Stack:** PowerShell 7+, JSON runtime policy/config, Python `pytest` runtime-neutral tests, existing governed verification gates

---

## File Structure

### Runtime control and artifact helpers
- Modify: `config/runtime-input-packet-policy.json`
  Responsibility: declare new governance artifact names and delegation-envelope validation expectations in one policy surface.
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
  Responsibility: centralize path helpers, artifact writers, and validation helpers for governance capsule, stage lineage, delegation envelope, and delegation validation receipts.

### Root governed runtime flow
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`
  Responsibility: originate root governance capsule, validate stage lineage before late-stage transitions, and expose new artifacts in the runtime summary.

### Child lane dispatch and enforcement
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`
  Responsibility: accept and propagate child delegation-envelope references during official child-lane startup.
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
  Responsibility: emit root-authored delegation envelopes before delegated child execution and record child validation outputs in execution manifests.
- Modify: `scripts/runtime/Invoke-DelegatedLaneUnit.ps1`
  Responsibility: reject child startup without a valid delegation envelope and write `delegation-validation-receipt.json`.
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
  Responsibility: keep root-owned canonical requirement writes and reject child attempts to reopen canonical truth.
- Modify: `scripts/runtime/Write-XlPlan.ps1`
  Responsibility: keep root-owned canonical plan writes and reject child attempts to reopen canonical truth.

### Contract docs
- Modify: `SKILL.md`
  Responsibility: reflect that governed-entry lineage and child envelope checks are runtime-validated inside official `vibe` entry.
- Modify: `protocols/runtime.md`
  Responsibility: describe governance capsule, stage-lineage validation, child delegation envelope, and runtime failure model.
- Modify: `protocols/team.md`
  Responsibility: describe child-lane envelope validation and the split between root-owned truth and child-local receipts.

### Runtime-neutral tests
- Create: `tests/runtime_neutral/test_governed_runtime_lineage.py`
  Responsibility: focused runtime tests for governance capsule and ordered stage-lineage behavior.
- Modify: `tests/runtime_neutral/test_root_child_hierarchy_bridge.py`
  Responsibility: assert child envelope validation, inherited truth reuse, and rejection of unapproved child specialist activation.
- Modify: `tests/runtime_neutral/test_governed_runtime_bridge.py`
  Responsibility: assert runtime summaries now include governance lineage artifacts and keep six-stage closure intact.

### Governed verification gates
- Modify: `scripts/verify/vibe-governed-runtime-contract-gate.ps1`
  Responsibility: assert the official governed path now emits and validates capsule/lineage artifacts.
- Modify: `scripts/verify/vibe-no-duplicate-canonical-surface-gate.ps1`
  Responsibility: assert child paths cannot reopen canonical requirement/plan truth.
- Modify: `scripts/verify/vibe-child-specialist-escalation-gate.ps1`
  Responsibility: assert child specialist execution remains envelope-bounded.
- Modify: `scripts/verify/vibe-root-child-hierarchy-gate.ps1`
  Responsibility: assert child lanes require root-authored delegation metadata and emit local validation receipts only.

## Chunk 1: Runtime Artifact Schema And Root Lineage

### Task 1: Define governance artifact policy and helper surfaces

**Files:**
- Modify: `config/runtime-input-packet-policy.json`
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Test: `tests/runtime_neutral/test_governed_runtime_lineage.py`

- [ ] **Step 1: Write the failing policy/helper test**

```python
class GovernedRuntimeLineageTests(unittest.TestCase):
    def test_runtime_policy_declares_governance_artifact_contract(self) -> None:
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        artifact_contract = policy["hierarchy_contract"]["governance_artifacts"]
        self.assertEqual("governance-capsule.json", artifact_contract["capsule"])
        self.assertEqual("stage-lineage.json", artifact_contract["lineage"])
        self.assertEqual("delegation-envelope.json", artifact_contract["delegation_envelope"])
        self.assertEqual("delegation-validation-receipt.json", artifact_contract["delegation_validation"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/runtime_neutral/test_governed_runtime_lineage.py::test_runtime_policy_declares_governance_artifact_contract -v`

Expected: `FAIL` because `governance_artifacts` is not present yet.

- [ ] **Step 3: Add minimal policy and helper support**

```powershell
function Get-VibeGovernanceArtifactPath {
    param(
        [Parameter(Mandatory)] [string]$SessionRoot,
        [Parameter(Mandatory)] [string]$ArtifactName
    )

    return Join-Path $SessionRoot $ArtifactName
}

function Write-VibeGovernanceCapsule {
    param(
        [Parameter(Mandatory)] [string]$SessionRoot,
        [Parameter(Mandatory)] [string]$RunId,
        [Parameter(Mandatory)] [string]$RootRunId,
        [Parameter(Mandatory)] [string]$GovernanceScope
    )

    $path = Get-VibeGovernanceArtifactPath -SessionRoot $SessionRoot -ArtifactName 'governance-capsule.json'
    Write-VibeJsonArtifact -Path $path -Value ([pscustomobject]@{
        run_id = $RunId
        root_run_id = $RootRunId
        governance_scope = $GovernanceScope
        runtime_selected_skill = 'vibe'
    })
    return $path
}
```

- [ ] **Step 4: Run the targeted test to verify it passes**

Run: `python3 -m pytest tests/runtime_neutral/test_governed_runtime_lineage.py::test_runtime_policy_declares_governance_artifact_contract -v`

Expected: `PASS`

- [ ] **Step 5: Commit**

```bash
git add config/runtime-input-packet-policy.json scripts/runtime/VibeRuntime.Common.ps1 tests/runtime_neutral/test_governed_runtime_lineage.py
git commit -m "feat: add governance artifact policy helpers"
```

### Task 2: Wire governance capsule and stage-lineage enforcement into root runtime

**Files:**
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Modify: `tests/runtime_neutral/test_governed_runtime_bridge.py`
- Test: `tests/runtime_neutral/test_governed_runtime_lineage.py`

- [ ] **Step 1: Write the failing runtime test for capsule and lineage artifacts**

```python
class GovernedRuntimeLineageTests(unittest.TestCase):
    def test_root_runtime_writes_capsule_and_stage_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            payload = run_governed_runtime(
                "Root runtime lineage smoke.",
                artifact_root=Path(tempdir),
            )
            artifacts = payload["summary"]["artifacts"]
            capsule = json.loads(Path(artifacts["governance_capsule"]).read_text(encoding="utf-8"))
            lineage = json.loads(Path(artifacts["stage_lineage"]).read_text(encoding="utf-8"))

            self.assertEqual("vibe", capsule["runtime_selected_skill"])
            self.assertEqual(
                ["skeleton_check", "deep_interview", "requirement_doc", "xl_plan", "plan_execute", "phase_cleanup"],
                [entry["stage_name"] for entry in lineage["stages"]],
            )
```

- [ ] **Step 2: Run the new lineage-focused tests and confirm failure**

Run: `python3 -m pytest tests/runtime_neutral/test_governed_runtime_lineage.py tests/runtime_neutral/test_governed_runtime_bridge.py -k "capsule or lineage" -v`

Expected: `FAIL` because summary artifacts and stage-lineage receipts do not exist yet.

- [ ] **Step 3: Implement root capsule creation and ordered lineage validation**

```powershell
$capsulePath = Write-VibeGovernanceCapsule `
    -SessionRoot ([string]$skeleton.session_root) `
    -RunId $RunId `
    -RootRunId ([string]$hierarchyState.root_run_id) `
    -GovernanceScope ([string]$hierarchyState.governance_scope)

Assert-VibeStageTransition `
    -SessionRoot ([string]$skeleton.session_root) `
    -RunId $RunId `
    -RootRunId ([string]$hierarchyState.root_run_id) `
    -StageName 'xl_plan' `
    -PreviousStageName 'requirement_doc' `
    -PreviousReceiptPath ([string]$requirement.receipt_path)
```

- [ ] **Step 4: Extend runtime summary projection to publish new artifacts**

```powershell
$summaryArtifacts = New-VibeRuntimeSummaryArtifactProjection `
    -GovernanceCapsulePath $capsulePath `
    -StageLineagePath $stageLineagePath `
    -SkeletonReceiptPath ([string]$skeleton.receipt_path)
```

- [ ] **Step 5: Re-run the lineage-focused tests**

Run: `python3 -m pytest tests/runtime_neutral/test_governed_runtime_lineage.py tests/runtime_neutral/test_governed_runtime_bridge.py -k "capsule or lineage" -v`

Expected: `PASS`

- [ ] **Step 6: Commit**

```bash
git add scripts/runtime/invoke-vibe-runtime.ps1 scripts/runtime/VibeRuntime.Common.ps1 tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_governed_runtime_lineage.py
git commit -m "feat: enforce governed root stage lineage"
```

## Chunk 2: Child Delegation Envelope And Canonical Truth Guards

### Task 3: Emit and validate child delegation envelopes

**Files:**
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
- Modify: `scripts/runtime/Invoke-DelegatedLaneUnit.ps1`
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Modify: `tests/runtime_neutral/test_root_child_hierarchy_bridge.py`

- [ ] **Step 1: Add the failing child-envelope test**

```python
class RootChildHierarchyBridgeTests(unittest.TestCase):
    def test_child_runtime_requires_delegation_envelope(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir)
            root_payload = run_governed_runtime("Root envelope seed.", artifact_root=artifact_root)
            with self.assertRaises(subprocess.CalledProcessError):
                run_child_runtime(
                    task="Child envelope enforcement smoke.",
                    root_run_id=str(root_payload["summary"]["run_id"]),
                    inherited_requirement_doc_path=Path(root_payload["summary"]["artifacts"]["requirement_doc"]),
                    inherited_execution_plan_path=Path(root_payload["summary"]["artifacts"]["execution_plan"]),
                    artifact_root=artifact_root,
                    delegation_envelope_path=None,
                )
```

- [ ] **Step 2: Run the failing child-envelope test**

Run: `python3 -m pytest tests/runtime_neutral/test_root_child_hierarchy_bridge.py -k "delegation_envelope" -v`

Expected: `FAIL` because child execution currently does not require a delegation envelope.

- [ ] **Step 3: Emit the envelope from root and validate it in child startup**

```powershell
$envelopePath = Write-VibeDelegationEnvelope `
    -SessionRoot $laneRoot `
    -RootRunId ([string]$HierarchyState.root_run_id) `
    -ParentRunId $RunId `
    -ParentUnitId ([string]$LaneEntry.source_unit_id) `
    -ChildRunId ([string]$LaneEntry.lane_id) `
    -RequirementDocPath $RequirementPath `
    -ExecutionPlanPath $PlanPath `
    -WriteScope ([string]$LaneEntry.write_scope) `
    -ApprovedSpecialists @($ApprovedSkillIds)

$validationReceipt = Assert-VibeDelegationEnvelope `
    -LaneSpec $laneSpec `
    -EnvelopePath ([string]$laneSpec.delegation_envelope_path)
```

- [ ] **Step 3a: Thread envelope-path plumbing through official child entry**

```powershell
param(
    [Parameter(Mandatory)] [string]$Task,
    [string]$Mode = 'interactive_governed',
    [string]$RunId = '',
    [string]$ArtifactRoot = '',
    [AllowEmptyString()] [string]$GovernanceScope = '',
    [AllowEmptyString()] [string]$RootRunId = '',
    [AllowEmptyString()] [string]$ParentRunId = '',
    [AllowEmptyString()] [string]$ParentUnitId = '',
    [AllowEmptyString()] [string]$InheritedRequirementDocPath = '',
    [AllowEmptyString()] [string]$InheritedExecutionPlanPath = '',
    [AllowEmptyString()] [string]$DelegationEnvelopePath = ''
)

if ($hierarchyState.governance_scope -eq 'child' -and [string]::IsNullOrWhiteSpace($DelegationEnvelopePath)) {
    throw 'Child-governed runtime requires DelegationEnvelopePath.'
}
```

- [ ] **Step 4: Persist delegation validation receipts**

```powershell
Write-VibeJsonArtifact -Path $delegationValidationPath -Value ([pscustomobject]@{
    child_run_id = [string]$laneSpec.run_id
    root_run_id = [string]$laneSpec.root_run_id
    envelope_path = [string]$laneSpec.delegation_envelope_path
    prompt_tail_valid = $true
    specialist_approval_valid = $true
})
```

- [ ] **Step 5: Re-run the child-envelope test**

Run: `python3 -m pytest tests/runtime_neutral/test_root_child_hierarchy_bridge.py -k "delegation_envelope" -v`

Expected: `PASS`

- [ ] **Step 6: Commit**

```bash
git add scripts/runtime/invoke-vibe-runtime.ps1 scripts/runtime/Invoke-PlanExecute.ps1 scripts/runtime/Invoke-DelegatedLaneUnit.ps1 scripts/runtime/VibeRuntime.Common.ps1 tests/runtime_neutral/test_root_child_hierarchy_bridge.py
git commit -m "feat: require child delegation envelopes"
```

### Task 4: Enforce canonical truth reuse and child specialist boundaries

**Files:**
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
- Modify: `scripts/runtime/Write-XlPlan.ps1`
- Modify: `scripts/runtime/Invoke-DelegatedLaneUnit.ps1`
- Modify: `tests/runtime_neutral/test_root_child_hierarchy_bridge.py`

- [ ] **Step 1: Add failing tests for child truth-surface reuse and specialist rejection**

```python
class RootChildHierarchyBridgeTests(unittest.TestCase):
    def test_child_lane_reuses_inherited_requirement_and_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir)
            root_payload = run_governed_runtime("Child truth reuse seed.", artifact_root=artifact_root)
            envelope_path = write_delegation_envelope_fixture(
                artifact_root=artifact_root,
                root_payload=root_payload,
                approved_specialists=[],
            )
            child_payload = run_child_runtime(
                task="Child truth reuse smoke.",
                root_run_id=str(root_payload["summary"]["run_id"]),
                inherited_requirement_doc_path=Path(root_payload["summary"]["artifacts"]["requirement_doc"]),
                inherited_execution_plan_path=Path(root_payload["summary"]["artifacts"]["execution_plan"]),
                artifact_root=artifact_root,
                approved_specialist_skill_ids=[],
                delegation_envelope_path=envelope_path,
            )
            requirement_receipt = json.loads(Path(child_payload["summary"]["artifacts"]["requirement_receipt"]).read_text(encoding="utf-8"))
            plan_receipt = json.loads(Path(child_payload["summary"]["artifacts"]["execution_plan_receipt"]).read_text(encoding="utf-8"))
            self.assertFalse(requirement_receipt["canonical_write_allowed"])
            self.assertFalse(plan_receipt["canonical_write_allowed"])

    def test_child_lane_rejects_unapproved_specialist_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir)
            root_payload = run_governed_runtime("Child specialist guard seed.", artifact_root=artifact_root)
            envelope_path = write_delegation_envelope_fixture(
                artifact_root=artifact_root,
                root_payload=root_payload,
                approved_specialists=[],
            )
            with self.assertRaises(subprocess.CalledProcessError):
                run_child_runtime(
                    task="Child specialist guard smoke.",
                    root_run_id=str(root_payload["summary"]["run_id"]),
                    inherited_requirement_doc_path=Path(root_payload["summary"]["artifacts"]["requirement_doc"]),
                    inherited_execution_plan_path=Path(root_payload["summary"]["artifacts"]["execution_plan"]),
                    artifact_root=artifact_root,
                    approved_specialist_skill_ids=[],
                    delegation_envelope_path=envelope_path,
                )
```

- [ ] **Step 2: Run the truth-surface and specialist tests**

Run: `python3 -m pytest tests/runtime_neutral/test_root_child_hierarchy_bridge.py -k "reuses_inherited or rejects_unapproved" -v`

Expected: at least one `FAIL` because child execution is not yet envelope-bounded for specialist activation and validation receipts.

- [ ] **Step 3: Tighten child requirement/plan guards**

```powershell
if ($isChildScope -and [string]::IsNullOrWhiteSpace([string]$hierarchyState.inherited_requirement_doc_path)) {
    throw 'Child-governed requirement stage requires inherited canonical requirement truth.'
}
if ($isChildScope -and [string]::IsNullOrWhiteSpace([string]$hierarchyState.inherited_execution_plan_path)) {
    throw 'Child-governed plan stage requires inherited canonical execution plan truth.'
}
```

- [ ] **Step 4: Reject unapproved child specialist dispatch**

```powershell
if ($laneKind -eq 'specialist_dispatch' -and -not (Test-VibeApprovedChildSpecialist `
    -LaneSpec $laneSpec `
    -Dispatch $dispatch)) {
    throw ("Child-governed lane attempted unapproved specialist dispatch: {0}" -f [string]$dispatch.skill_id)
}
```

- [ ] **Step 5: Re-run the targeted child hierarchy tests**

Run: `python3 -m pytest tests/runtime_neutral/test_root_child_hierarchy_bridge.py -k "reuses_inherited or rejects_unapproved or delegation_validation" -v`

Expected: `PASS`

- [ ] **Step 6: Commit**

```bash
git add scripts/runtime/Write-RequirementDoc.ps1 scripts/runtime/Write-XlPlan.ps1 scripts/runtime/Invoke-DelegatedLaneUnit.ps1 tests/runtime_neutral/test_root_child_hierarchy_bridge.py
git commit -m "feat: guard child canonical truth and specialist scope"
```

## Chunk 3: Contract Docs, Gates, And End-To-End Verification

### Task 5: Align docs and governed verification with runtime enforcement

**Files:**
- Modify: `SKILL.md`
- Modify: `protocols/runtime.md`
- Modify: `protocols/team.md`
- Modify: `scripts/verify/vibe-governed-runtime-contract-gate.ps1`
- Modify: `scripts/verify/vibe-no-duplicate-canonical-surface-gate.ps1`
- Modify: `scripts/verify/vibe-child-specialist-escalation-gate.ps1`
- Modify: `scripts/verify/vibe-root-child-hierarchy-gate.ps1`
- Modify: `tests/runtime_neutral/test_governed_runtime_bridge.py`
- Modify: `tests/runtime_neutral/test_root_child_hierarchy_bridge.py`

- [ ] **Step 1: Add failing assertions for docs and gates**

```python
def test_runtime_protocol_mentions_stage_lineage_and_delegation_envelope() -> None:
    text = (REPO_ROOT / "protocols" / "runtime.md").read_text(encoding="utf-8")
    assert "governance capsule" in text
    assert "stage-lineage" in text
    assert "delegation-envelope" in text
```

- [ ] **Step 2: Run the doc/gate alignment tests**

Run: `python3 -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_root_child_hierarchy_bridge.py -k "stage_lineage or delegation_envelope or validation_receipt" -v`

Expected: `FAIL` until docs and runtime summary assertions are aligned.

- [ ] **Step 3: Update contract docs to match actual enforcement**

```markdown
- official governed entry writes `governance-capsule.json`
- late-stage transitions validate `stage-lineage.json`
- child-governed startup requires `delegation-envelope.json`
- child-governed lanes emit `delegation-validation-receipt.json`
```

- [ ] **Step 4: Tighten governed gates to inspect the new artifacts**

```powershell
if (-not (Test-Path -LiteralPath $governanceCapsulePath)) {
    throw 'Governed runtime contract gate requires governance-capsule.json.'
}
if (-not (Test-Path -LiteralPath $delegationValidationReceiptPath)) {
    throw 'Root/child hierarchy gate requires delegation-validation-receipt.json for child lanes.'
}
```

- [ ] **Step 5: Run the targeted tests and governed gates**

Run: `python3 -m pytest tests/runtime_neutral/test_governed_runtime_lineage.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_root_child_hierarchy_bridge.py -v`

Expected: `PASS`

Run: `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-governed-runtime-contract-gate.ps1`

Expected: exit code `0`

Run: `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-no-duplicate-canonical-surface-gate.ps1`

Expected: exit code `0`

Run: `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-child-specialist-escalation-gate.ps1`

Expected: exit code `0`

Run: `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-root-child-hierarchy-gate.ps1`

Expected: exit code `0`

- [ ] **Step 6: Run final hygiene verification**

Run: `git diff --check`

Expected: no output

Run: `git status --short`

Expected: only intended tracked changes remain

- [ ] **Step 7: Commit**

```bash
git add SKILL.md protocols/runtime.md protocols/team.md scripts/verify/vibe-governed-runtime-contract-gate.ps1 scripts/verify/vibe-no-duplicate-canonical-surface-gate.ps1 scripts/verify/vibe-child-specialist-escalation-gate.ps1 scripts/verify/vibe-root-child-hierarchy-gate.ps1 tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_root_child_hierarchy_bridge.py tests/runtime_neutral/test_governed_runtime_lineage.py
git commit -m "docs: align governed runtime enforcement contracts"
```

## Cross-Chunk Verification Notes
- Prefer helper-level validation in `scripts/runtime/VibeRuntime.Common.ps1` instead of duplicating JSON-shape checks across entrypoints.
- Keep new artifact names stable once Chunk 1 lands; later chunks should consume those names rather than inventing aliases.
- Do not claim stronger-than-scope guarantees. Every updated doc and gate should say this enforcement covers the official governed entry and derived child lanes, not arbitrary manual script execution.
- If any existing schema or golden test fails because runtime summary artifacts expanded, update the exact failing assertion in that same chunk instead of deferring cleanup to the end.

## Rollback Rules
- If lineage validation causes legitimate root runs to fail before receipt creation, revert the most recent lineage-only commit and keep the old runtime flow intact while debugging.
- If child envelope validation breaks delegated execution entirely, keep root runtime hardening and roll back only the child-envelope commit.
- Do not revert unrelated user changes or prior PR 127 fixes.

## Ready Check
Plan is complete when all three chunks can be executed in order, each chunk ends with passing targeted verification and a focused commit, and the final gates confirm that governed-entry lineage plus child delegation enforcement are active without expanding scope beyond the official governed path.
