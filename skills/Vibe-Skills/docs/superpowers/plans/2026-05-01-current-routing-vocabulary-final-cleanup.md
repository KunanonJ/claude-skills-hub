# Current Routing Vocabulary Final Cleanup Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish the current routing vocabulary cleanup so active policy, runtime helpers, receipts, handoffs, and scans use the current `skill_routing.selected -> selected_skill_execution -> skill_usage.used / skill_usage.unused` vocabulary without changing route behavior.

**Architecture:** Add failing runtime-neutral vocabulary guards first, then rename one active surface at a time: policy JSON, packet freeze readers, runtime projection helpers, user-visible generated text, and scan gates. The six governed stages, pack routing, skill selection, execution joining, and usage-proof semantics stay unchanged; old-format compatibility is not reintroduced as current behavior.

**Tech Stack:** PowerShell runtime scripts and verification gates, JSON policy/config files, Python `unittest` / `pytest` runtime-neutral tests, Markdown governance docs, Git commits per cleanup slice.

---

## Fixed Boundaries

- Keep the six governed stages unchanged: `skeleton_check`, `deep_interview`, `requirement_doc`, `xl_plan`, `plan_execute`, `phase_cleanup`.
- Keep the current route model unchanged: `skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused`.
- Keep the current execution join model unchanged: `selected_skill_execution -> skill_execution_units -> execution_skill_outcomes`.
- Do not delete skills, packs, pack manifests, route thresholds, or route scores in this plan.
- Do not deploy to the live Codex host in this plan.
- Do not add dual-write current output fields for old root routing names.
- Keep `specialist_recommendations` bridge-only when a current reader still needs it; do not use it as a current public state or material-use proof.
- Do not perform a repo-wide search-replace. Every rename below is scoped to the listed active surfaces.

---

## File Structure

- Create: `tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py`
  - Static guard for active policy/helper/output vocabulary.
- Modify: `config/runtime-input-packet-policy.json`
  - Replace active dispatch contract names with skill execution contract names.
  - Remove old root routing fields from `required_fields`.
  - Rename interactive disclosure policy from dispatch wording to selected skill execution wording.
- Modify: `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
  - Read `skill_execution_contract` from policy.
  - Stop reading `specialist_dispatch_contract` as a current policy field.
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
  - Rename the current selected execution projection helper.
  - Rename host skill execution contract and markdown helper names.
  - Stop reading root `specialist_dispatch` inside the current projection helper.
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
  - Read `host_skill_execution_decision`.
  - Emit `## Host Skill Execution Decision`.
- Modify: `scripts/runtime/Write-XlPlan.ps1`
  - Read `host_skill_execution_decision`.
  - Emit `## Host Skill Execution Decision`.
  - Change child handoff field to `selected_skill_execution_count`.
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
  - Call `Get-VibeRuntimeSelectedSkillExecutionProjection`.
  - Rename current accounting field `dispatch_unit_count` to `skill_execution_unit_count` only.
  - Keep already-current `selected_skill_execution`, `blocked_skill_execution_units`, `degraded_skill_execution_units`, and `execution_skill_outcomes`.
- Modify: `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1`
  - Add a current policy/helper dispatch vocabulary scan category.
- Modify: `scripts/verify/vibe-current-routing-contract-scan.ps1`
  - Surface and enforce the new hard-cleanup policy/helper count.
- Modify: `config/routing-terminology-hard-cleanup.json`
  - Add active policy/helper scan files and exact forbidden current patterns.
- Modify: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
  - Assert the new scan count exists and is zero.
- Modify: `tests/runtime_neutral/test_current_routing_contract_scan.py`
  - Assert the current routing contract scan relays the new count and keeps it zero.
- Modify: `tests/runtime_neutral/test_simplified_skill_routing_contract.py`
  - Update current helper expectations away from the removed projection helper.
- Modify as focused failures require:
  - `tests/runtime_neutral/test_runtime_contract_schema.py`
  - `tests/runtime_neutral/test_governed_runtime_bridge.py`
  - `tests/runtime_neutral/test_l_xl_native_execution_topology.py`
  - `tests/runtime_neutral/test_custom_admission_bridge.py`
  - `tests/runtime_neutral/test_structured_bounded_reentry_continuation.py`
  - `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`
  - `tests/runtime_neutral/test_runtime_delivery_acceptance.py`
- Modify: `docs/governance/current-runtime-field-contract.md`
  - Align the current execution anchors with `selected_skill_execution`.

Do not modify historical docs, retired plans, bundled skill directories, or pack membership in this plan.

---

### Task 1: Add Current Vocabulary Guard Tests

**Files:**
- Create: `tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py`

- [ ] **Step 1: Write the failing guard test**

Create `tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py`:

```python
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = REPO_ROOT / "config" / "runtime-input-packet-policy.json"
RUNTIME_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeRuntime.Common.ps1"
FREEZE_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "Freeze-RuntimeInputPacket.ps1"
PLAN_EXECUTE = REPO_ROOT / "scripts" / "runtime" / "Invoke-PlanExecute.ps1"
WRITE_REQUIREMENT_DOC = REPO_ROOT / "scripts" / "runtime" / "Write-RequirementDoc.ps1"
WRITE_XL_PLAN = REPO_ROOT / "scripts" / "runtime" / "Write-XlPlan.ps1"
CURRENT_FIELD_DOC = REPO_ROOT / "docs" / "governance" / "current-runtime-field-contract.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class CurrentRoutingVocabularyFinalCleanupTests(unittest.TestCase):
    def test_policy_uses_current_skill_execution_contract_fields(self) -> None:
        policy = json.loads(read(POLICY_PATH))
        required_fields = set(policy["required_fields"])

        self.assertIn("skill_routing", required_fields)
        self.assertIn("skill_usage", required_fields)
        self.assertNotIn("specialist_dispatch", required_fields)
        self.assertNotIn("specialist_recommendations", required_fields)

        self.assertIn("skill_execution_contract", policy)
        self.assertIn("host_skill_execution_contract", policy)
        self.assertIn("interactive_skill_execution_disclosure", policy)
        self.assertNotIn("specialist_dispatch_contract", policy)
        self.assertNotIn("host_specialist_dispatch_contract", policy)
        self.assertNotIn("interactive_specialist_disclosure", policy)

        disclosure = policy["interactive_skill_execution_disclosure"]
        self.assertEqual("selected_skill_execution_only", disclosure["scope"])
        self.assertEqual("Pre-execution skill disclosure:", disclosure["header"])

    def test_current_runtime_projection_helper_has_current_name_and_no_root_dispatch_fallback(self) -> None:
        text = read(RUNTIME_COMMON)

        self.assertIn("function Get-VibeRuntimeSelectedSkillExecutionProjection", text)
        self.assertNotIn("function Get-VibeRuntimeSpecialistDispatchProjection", text)
        self.assertNotIn("RuntimeInputPacket.specialist_dispatch", text)
        self.assertNotIn("PropertyName 'specialist_dispatch'", text)

        helper_match = re.search(
            r"function Get-VibeRuntimeSelectedSkillExecutionProjection\s*\{(?P<body>.*?)\n\}",
            text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(helper_match)
        helper_body = helper_match.group("body")
        for field in [
            "selected_skill_execution",
            "blocked_skill_execution",
            "degraded_skill_execution",
            "selected_skill_ids",
            "blocked_skill_ids",
            "degraded_skill_ids",
            "source = 'skill_routing.selected'",
        ]:
            self.assertIn(field, helper_body)
        for field in [
            "approved_dispatch",
            "local_specialist_suggestions",
            "approved_skill_ids",
        ]:
            self.assertNotIn(field, helper_body)

    def test_active_policy_readers_use_current_contract_names(self) -> None:
        for path in [FREEZE_SCRIPT, RUNTIME_COMMON]:
            text = read(path)
            self.assertIn("skill_execution_contract", text, path)
            self.assertNotIn("specialist_dispatch_contract", text, path)
            self.assertIn("host_skill_execution_contract", text, path)
            self.assertNotIn("host_specialist_dispatch_contract", text, path)

    def test_generated_current_artifacts_do_not_use_dispatch_headings_or_counts(self) -> None:
        combined = "\n".join(
            [
                read(WRITE_REQUIREMENT_DOC),
                read(WRITE_XL_PLAN),
                read(PLAN_EXECUTE),
            ]
        )

        self.assertIn("Host Skill Execution Decision", combined)
        self.assertIn("selected_skill_execution_count", combined)
        self.assertNotIn("Host Specialist Dispatch Decision", combined)
        self.assertNotIn("approved_specialist_dispatch_count", combined)
        self.assertNotRegex(combined, r"(?m)^\s*dispatch_unit_count\s*=")

    def test_current_runtime_field_doc_uses_selected_skill_execution_anchor(self) -> None:
        text = read(CURRENT_FIELD_DOC)
        current_section = text.split("## Retired Layer", 1)[0]

        self.assertIn("selected_skill_execution", current_section)
        self.assertIn("skill_execution_units", current_section)
        self.assertIn("execution_skill_outcomes", current_section)
        self.assertNotIn("approved_skill_execution", current_section)
        self.assertNotIn("specialist_dispatch as root routing packet field", current_section)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new guard test and confirm it fails for the current residue**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py -q
```

Expected: `FAIL` with assertions naming current residue such as `specialist_dispatch_contract`, `host_specialist_dispatch_contract`, `Get-VibeRuntimeSpecialistDispatchProjection`, `Host Specialist Dispatch Decision`, or `approved_specialist_dispatch_count`.

- [ ] **Step 3: Commit the failing guard**

Run:

```powershell
git add tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py
git commit -m "test: guard current routing vocabulary final cleanup"
```

---

### Task 2: Rename Active Runtime Input Policy Fields

**Files:**
- Modify: `config/runtime-input-packet-policy.json`
- Modify: `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`

- [ ] **Step 1: Replace the policy required fields with current route fields**

In `config/runtime-input-packet-policy.json`, replace the current `required_fields` array with:

```json
"required_fields": [
  "run_id",
  "governance_scope",
  "host_adapter",
  "hierarchy",
  "task",
  "runtime_mode",
  "internal_grade",
  "canonical_router",
  "route_snapshot",
  "skill_routing",
  "skill_usage",
  "overlay_decisions",
  "authority_flags",
  "divergence_shadow",
  "provenance"
],
```

This removes `specialist_recommendations` and root `specialist_dispatch` from the current required packet surface. Existing bridge knobs may stay outside `required_fields` until a later deletion slice proves they are unread.

- [ ] **Step 2: Rename the active skill execution contract object**

In `config/runtime-input-packet-policy.json`, rename the `specialist_dispatch_contract` object to `skill_execution_contract` without changing its values:

```json
"skill_execution_contract": {
  "bounded_role": "specialist_assist",
  "native_usage_required": true,
  "must_preserve_workflow": true,
  "dispatch_phase": "in_execution",
  "execution_priority": 50,
  "lane_policy": "inherit_grade",
  "parallelizable_in_root_xl": true,
  "write_scope_template": "specialist:{skill_id}",
  "review_mode": "native_contract",
  "required_inputs": [
    "bounded specialist subtask contract",
    "frozen requirement context",
    "relevant source files or domain artifacts"
  ],
  "expected_outputs": [
    "bounded specialist findings or code changes",
    "verification notes aligned with the specialist skill"
  ],
  "verification_expectation": "Preserve the specialist skill's native workflow, boundaries, and validation style."
},
```

Keep inner values unchanged in this task to avoid altering execution behavior. Field-level vocabulary inside the contract can be reduced in a later safe deletion slice after current readers no longer depend on it.

- [ ] **Step 3: Rename the active host contract object**

In `config/runtime-input-packet-policy.json`, rename `host_specialist_dispatch_contract` to `host_skill_execution_contract`:

```json
"host_skill_execution_contract": {
  "enabled": true,
  "scope": "root_only",
  "selection_modes": [
    "inherit_runtime_default",
    "curated_only"
  ],
  "default_selection_mode": "inherit_runtime_default"
},
```

- [ ] **Step 4: Rename the interactive disclosure policy object**

In `config/runtime-input-packet-policy.json`, replace `interactive_specialist_disclosure` with:

```json
"interactive_skill_execution_disclosure": {
  "enabled": true,
  "stage": "plan_execute",
  "scope": "selected_skill_execution_only",
  "timing": "before_execution",
  "aggregation": "unified_once",
  "path_source": "native_skill_entrypoint",
  "require_entrypoint_path": true,
  "include_description": true,
  "header": "Pre-execution skill disclosure:"
},
```

- [ ] **Step 5: Update policy readers in `Freeze-RuntimeInputPacket.ps1`**

In both contract lookup blocks in `scripts/runtime/Freeze-RuntimeInputPacket.ps1`, replace the old policy read:

```powershell
$dispatchContract = if ($Policy.PSObject.Properties.Name -contains 'specialist_dispatch_contract' -and $null -ne $Policy.specialist_dispatch_contract) {
    $Policy.specialist_dispatch_contract
} else {
```

with the current policy read:

```powershell
$dispatchContract = if ($Policy.PSObject.Properties.Name -contains 'skill_execution_contract' -and $null -ne $Policy.skill_execution_contract) {
    $Policy.skill_execution_contract
} else {
```

Do not add fallback reads to `specialist_dispatch_contract`.

- [ ] **Step 6: Update host contract reader in `VibeRuntime.Common.ps1`**

Rename the function and its policy read:

```powershell
function Get-VibeHostSkillExecutionContract {
    param(
        [AllowNull()] [object]$Policy = $null
    )

    $dispatchPolicy = $null
    if ($null -ne $Policy -and (Test-VibeObjectHasProperty -InputObject $Policy -PropertyName 'host_skill_execution_contract')) {
        $dispatchPolicy = $Policy.host_skill_execution_contract
    }
```

Then replace calls to `Get-VibeHostSpecialistDispatchContract` with `Get-VibeHostSkillExecutionContract`.

- [ ] **Step 7: Update interactive disclosure policy reader in `VibeRuntime.Common.ps1`**

Rename `Get-VibeInteractiveSpecialistDisclosurePolicy` to `Get-VibeInteractiveSkillExecutionDisclosurePolicy` and use the new policy key:

```powershell
function Get-VibeInteractiveSkillExecutionDisclosurePolicy {
    param(
        [AllowNull()] [object]$RuntimeInputPacketPolicy
    )

    $policy = $null
    if ($null -ne $RuntimeInputPacketPolicy -and (Test-VibeObjectHasProperty -InputObject $RuntimeInputPacketPolicy -PropertyName 'interactive_skill_execution_disclosure')) {
        $policy = $RuntimeInputPacketPolicy.interactive_skill_execution_disclosure
    }

    return [pscustomobject]@{
        enabled = if ($null -ne $policy -and (Test-VibeObjectHasProperty -InputObject $policy -PropertyName 'enabled')) { [bool]$policy.enabled } else { $false }
        stage = if ($null -ne $policy -and (Test-VibeObjectHasProperty -InputObject $policy -PropertyName 'stage') -and -not [string]::IsNullOrWhiteSpace([string]$policy.stage)) { [string]$policy.stage } else { 'plan_execute' }
        mode = 'selected_skill_execution_pre_execution_unified_once'
        timing = if ($null -ne $policy -and (Test-VibeObjectHasProperty -InputObject $policy -PropertyName 'timing') -and -not [string]::IsNullOrWhiteSpace([string]$policy.timing)) { [string]$policy.timing } else { 'before_execution' }
        scope = if ($null -ne $policy -and (Test-VibeObjectHasProperty -InputObject $policy -PropertyName 'scope') -and -not [string]::IsNullOrWhiteSpace([string]$policy.scope)) { [string]$policy.scope } else { 'selected_skill_execution_only' }
        aggregation = if ($null -ne $policy -and (Test-VibeObjectHasProperty -InputObject $policy -PropertyName 'aggregation') -and -not [string]::IsNullOrWhiteSpace([string]$policy.aggregation)) { [string]$policy.aggregation } else { 'unified_once' }
        path_source = if ($null -ne $policy -and (Test-VibeObjectHasProperty -InputObject $policy -PropertyName 'path_source') -and -not [string]::IsNullOrWhiteSpace([string]$policy.path_source)) { [string]$policy.path_source } else { 'native_skill_entrypoint' }
        require_entrypoint_path = if ($null -ne $policy -and (Test-VibeObjectHasProperty -InputObject $policy -PropertyName 'require_entrypoint_path')) { [bool]$policy.require_entrypoint_path } else { $true }
        include_description = if ($null -ne $policy -and (Test-VibeObjectHasProperty -InputObject $policy -PropertyName 'include_description')) { [bool]$policy.include_description } else { $true }
        header = if ($null -ne $policy -and (Test-VibeObjectHasProperty -InputObject $policy -PropertyName 'header') -and -not [string]::IsNullOrWhiteSpace([string]$policy.header)) { [string]$policy.header } else { 'Pre-execution skill disclosure:' }
    }
}
```

Update `New-VibeSpecialistUserDisclosureProjection` to call `Get-VibeInteractiveSkillExecutionDisclosurePolicy` when no policy is passed.

- [ ] **Step 8: Run policy-focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py::CurrentRoutingVocabularyFinalCleanupTests::test_policy_uses_current_skill_execution_contract_fields tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py::CurrentRoutingVocabularyFinalCleanupTests::test_active_policy_readers_use_current_contract_names -q
```

Expected: `PASS`.

- [ ] **Step 9: Commit the policy field cleanup**

Run:

```powershell
git add config/runtime-input-packet-policy.json scripts/runtime/Freeze-RuntimeInputPacket.ps1 scripts/runtime/VibeRuntime.Common.ps1 tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py
git commit -m "refactor: rename current skill execution policy fields"
```

---

### Task 3: Rename the Current Selected Skill Execution Projection Helper

**Files:**
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
- Modify: `scripts/verify/vibe-child-specialist-escalation-gate.ps1`
- Modify: `scripts/verify/vibe-skill-promotion-execution-gate.ps1`
- Modify: `scripts/verify/vibe-specialist-dispatch-closure-gate.ps1`
- Modify: `tests/runtime_neutral/test_simplified_skill_routing_contract.py`
- Modify as focused failures require: `tests/runtime_neutral/test_retired_old_routing_compat.py`

- [ ] **Step 1: Replace the projection helper body in `VibeRuntime.Common.ps1`**

Replace `function Get-VibeRuntimeSpecialistDispatchProjection` with:

```powershell
function Get-VibeRuntimeSelectedSkillExecutionProjection {
    param(
        [AllowNull()] [object]$RuntimeInputPacket = $null
    )

    if (
        $null -eq $RuntimeInputPacket -or
        -not (Test-VibeObjectHasProperty -InputObject $RuntimeInputPacket -PropertyName 'skill_routing') -or
        $null -eq $RuntimeInputPacket.skill_routing -or
        -not (Test-VibeObjectHasProperty -InputObject $RuntimeInputPacket.skill_routing -PropertyName 'selected')
    ) {
        return $null
    }

    $selectedSkillExecution = [object[]]@($RuntimeInputPacket.skill_routing.selected)
    $specialistDecision = if (
        (Test-VibeObjectHasProperty -InputObject $RuntimeInputPacket -PropertyName 'specialist_decision') -and
        $null -ne $RuntimeInputPacket.specialist_decision
    ) {
        $RuntimeInputPacket.specialist_decision
    } else {
        $null
    }

    $blockedSkillIds = if (
        $null -ne $specialistDecision -and
        (Test-VibeObjectHasProperty -InputObject $specialistDecision -PropertyName 'blocked_skill_ids') -and
        $null -ne $specialistDecision.blocked_skill_ids
    ) {
        @($specialistDecision.blocked_skill_ids | ForEach-Object { [string]$_ } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
    } else {
        @()
    }
    $degradedSkillIds = if (
        $null -ne $specialistDecision -and
        (Test-VibeObjectHasProperty -InputObject $specialistDecision -PropertyName 'degraded_skill_ids') -and
        $null -ne $specialistDecision.degraded_skill_ids
    ) {
        @($specialistDecision.degraded_skill_ids | ForEach-Object { [string]$_ } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
    } else {
        @()
    }
    $nonExecutableSkillIds = @(@($blockedSkillIds) + @($degradedSkillIds)) | Select-Object -Unique
    $directSelectedSkillExecution = [object[]]@($selectedSkillExecution | Where-Object {
            $skillId = [string](Get-VibePropertySafe -InputObject $_ -PropertyName 'skill_id' -DefaultValue '')
            [string]::IsNullOrWhiteSpace($skillId) -or ($skillId -notin @($nonExecutableSkillIds))
        })
    $blockedSkillExecution = [object[]]@($selectedSkillExecution | Where-Object {
            $skillId = [string](Get-VibePropertySafe -InputObject $_ -PropertyName 'skill_id' -DefaultValue '')
            -not [string]::IsNullOrWhiteSpace($skillId) -and ($skillId -in @($blockedSkillIds))
        })
    $degradedSkillExecution = [object[]]@($selectedSkillExecution | Where-Object {
            $skillId = [string](Get-VibePropertySafe -InputObject $_ -PropertyName 'skill_id' -DefaultValue '')
            -not [string]::IsNullOrWhiteSpace($skillId) -and ($skillId -in @($degradedSkillIds))
        })
    if (@($selectedSkillExecution).Count -eq 0 -and $null -eq $specialistDecision) {
        return $null
    }

    $selectedSkillIds = @($directSelectedSkillExecution | ForEach-Object {
        [string](Get-VibePropertySafe -InputObject $_ -PropertyName 'skill_id' -DefaultValue '')
    } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)

    return [pscustomobject]@{
        selected_skill_execution = [object[]]@($directSelectedSkillExecution)
        blocked_skill_execution = [object[]]@($blockedSkillExecution)
        degraded_skill_execution = [object[]]@($degradedSkillExecution)
        selected_skill_ids = @($selectedSkillIds)
        blocked_skill_ids = @($blockedSkillIds)
        degraded_skill_ids = @($degradedSkillIds)
        surfaced_skill_ids = @($selectedSkillIds)
        matched_skill_ids = @($selectedSkillIds)
        status = 'derived_from_skill_routing_selected'
        source = 'skill_routing.selected'
    }
}
```

Do not keep a same-name wrapper for `Get-VibeRuntimeSpecialistDispatchProjection`.

- [ ] **Step 2: Update `New-VibeSpecialistDecisionProjection` to read the new projection shape**

In `VibeRuntime.Common.ps1`, replace the `$dispatchSource` assignment and the old field reads with current names:

```powershell
$executionSource = Get-VibeRuntimeSelectedSkillExecutionProjection -RuntimeInputPacket $RuntimeInputPacket

$approvedDispatchArray = if ((Get-VibeSafeArrayCount -InputObject $ApprovedDispatch) -gt 0) {
    @($ApprovedDispatch)
} elseif ($null -ne $executionSource -and (Test-VibeObjectHasProperty -InputObject $executionSource -PropertyName 'selected_skill_execution')) {
    @($executionSource.selected_skill_execution)
} else {
    @()
}
$localSuggestionArray = if ((Get-VibeSafeArrayCount -InputObject $LocalSuggestions) -gt 0) {
    @($LocalSuggestions)
} else {
    @()
}
$blockedDispatchArray = if ((Get-VibeSafeArrayCount -InputObject $BlockedDispatch) -gt 0) {
    @($BlockedDispatch)
} elseif ($null -ne $executionSource -and (Test-VibeObjectHasProperty -InputObject $executionSource -PropertyName 'blocked_skill_execution')) {
    @($executionSource.blocked_skill_execution)
} else {
    @()
}
$degradedDispatchArray = if ((Get-VibeSafeArrayCount -InputObject $DegradedDispatch) -gt 0) {
    @($DegradedDispatch)
} elseif ($null -ne $executionSource -and (Test-VibeObjectHasProperty -InputObject $executionSource -PropertyName 'degraded_skill_execution')) {
    @($executionSource.degraded_skill_execution)
} else {
    @()
}
```

Then update downstream reads from `$dispatchSource.local_suggestion_skill_ids`, `$dispatchSource.blocked_skill_ids`, `$dispatchSource.degraded_skill_ids`, `$dispatchSource.matched_skill_ids`, and `$dispatchSource.surfaced_skill_ids` to `$executionSource.<same_current_id_field>`. Keep `approved_dispatch_skill_ids` in `specialist_decision` for this task only when tests prove current delivery acceptance still consumes it.

- [ ] **Step 3: Update `Invoke-PlanExecute.ps1` helper calls and local variables**

Replace both calls:

```powershell
$runtimeSpecialistDispatch = Get-VibeRuntimeSpecialistDispatchProjection -RuntimeInputPacket $RuntimeInputPacket
```

and:

```powershell
$runtimeSpecialistDispatch = Get-VibeRuntimeSpecialistDispatchProjection -RuntimeInputPacket $runtimeInputPacket
```

with:

```powershell
$runtimeSelectedSkillExecution = Get-VibeRuntimeSelectedSkillExecutionProjection -RuntimeInputPacket $RuntimeInputPacket
```

and:

```powershell
$runtimeSelectedSkillExecution = Get-VibeRuntimeSelectedSkillExecutionProjection -RuntimeInputPacket $runtimeInputPacket
```

Then update reads in the same local blocks:

```powershell
@($runtimeSelectedSkillExecution.selected_skill_execution)
@($runtimeSelectedSkillExecution.blocked_skill_execution)
@($runtimeSelectedSkillExecution.degraded_skill_execution)
```

- [ ] **Step 4: Update verification scripts that call the removed helper**

In the listed verification scripts, replace `Get-VibeRuntimeSpecialistDispatchProjection` with `Get-VibeRuntimeSelectedSkillExecutionProjection` and update field reads:

```powershell
$selectedSkillExecution = Get-VibeRuntimeSelectedSkillExecutionProjection -RuntimeInputPacket $runtimeInput
$selected = if ($null -ne $selectedSkillExecution -and $selectedSkillExecution.PSObject.Properties.Name -contains 'selected_skill_execution') {
    @($selectedSkillExecution.selected_skill_execution)
} else {
    @()
}
```

Use the same pattern for root and child runtime packets.

- [ ] **Step 5: Update current helper tests**

In `tests/runtime_neutral/test_simplified_skill_routing_contract.py`, replace tests that call the removed projection helper with tests that prove:

```python
self.assertEqual(["new-authority"], as_list(payload["selected_skill_ids"]))
self.assertEqual([], as_list(payload["selected_skill_ids"]))
```

through `Get-VibeSkillRoutingSelectedSkillIds` and `Get-VibeRuntimeSelectedSkillExecutionProjection`. Keep explicitly legacy fixture construction only in tests whose names contain `legacy`.

- [ ] **Step 6: Run focused helper tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py::CurrentRoutingVocabularyFinalCleanupTests::test_current_runtime_projection_helper_has_current_name_and_no_root_dispatch_fallback tests/runtime_neutral/test_simplified_skill_routing_contract.py -q
```

Expected: `PASS`.

- [ ] **Step 7: Commit the helper rename**

Run:

```powershell
git add scripts/runtime/VibeRuntime.Common.ps1 scripts/runtime/Invoke-PlanExecute.ps1 scripts/verify/vibe-child-specialist-escalation-gate.ps1 scripts/verify/vibe-skill-promotion-execution-gate.ps1 scripts/verify/vibe-specialist-dispatch-closure-gate.ps1 tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_retired_old_routing_compat.py tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py
git commit -m "refactor: rename selected skill execution projection helper"
```

---

### Task 4: Rename Current Host Decision and Generated Output Wording

**Files:**
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`
- Modify: `scripts/runtime/Write-XlPlan.ps1`
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
- Modify as focused failures require:
  - `tests/runtime_neutral/test_runtime_contract_schema.py`
  - `tests/runtime_neutral/test_governed_runtime_bridge.py`
  - `tests/runtime_neutral/test_l_xl_native_execution_topology.py`
  - `tests/runtime_neutral/test_custom_admission_bridge.py`
  - `tests/runtime_neutral/test_structured_bounded_reentry_continuation.py`
  - `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`
  - `tests/runtime_neutral/test_runtime_delivery_acceptance.py`

- [ ] **Step 1: Rename the host decision packet field**

In `New-VibeRuntimeInputPacketProjection`, replace:

```powershell
host_specialist_dispatch_decision = $HostSpecialistDispatchDecision
```

with:

```powershell
host_skill_execution_decision = $HostSpecialistDispatchDecision
```

Keep the parameter name for this task if renaming it would create a wide PowerShell signature migration. The output field is the current contract being cleaned here.

- [ ] **Step 2: Rename the host markdown helper**

Rename `Get-VibeHostSpecialistDispatchDecisionMarkdownLines` to:

```powershell
function Get-VibeHostSkillExecutionDecisionMarkdownLines {
    param(
        [AllowNull()] [object]$Decision = $null
    )
```

Move the existing function body under the new function name and keep the output lines semantically identical except for wording that says dispatch as the current action. Replace wording such as `approved dispatch` with `selected skill execution` in the returned Markdown lines.

- [ ] **Step 3: Update `Write-RequirementDoc.ps1` generated section**

Replace the host decision read:

```powershell
$hostSpecialistDispatchDecision = if (
    $runtimeInputPacket.PSObject.Properties.Name -contains 'host_specialist_dispatch_decision' -and
    $null -ne $runtimeInputPacket.host_specialist_dispatch_decision
) {
    $runtimeInputPacket.host_specialist_dispatch_decision
} else {
    $null
}
$hostSpecialistDispatchLines = @(Get-VibeHostSpecialistDispatchDecisionMarkdownLines -Decision $hostSpecialistDispatchDecision)
if (@($hostSpecialistDispatchLines).Count -gt 0) {
    $lines += @(
        '',
        '## Host Specialist Dispatch Decision'
    )
    $lines += @($hostSpecialistDispatchLines)
}
```

with:

```powershell
$hostSkillExecutionDecision = if (
    $runtimeInputPacket.PSObject.Properties.Name -contains 'host_skill_execution_decision' -and
    $null -ne $runtimeInputPacket.host_skill_execution_decision
) {
    $runtimeInputPacket.host_skill_execution_decision
} else {
    $null
}
$hostSkillExecutionLines = @(Get-VibeHostSkillExecutionDecisionMarkdownLines -Decision $hostSkillExecutionDecision)
if (@($hostSkillExecutionLines).Count -gt 0) {
    $lines += @(
        '',
        '## Host Skill Execution Decision'
    )
    $lines += @($hostSkillExecutionLines)
}
```

- [ ] **Step 4: Update `Write-XlPlan.ps1` generated section**

Apply the same `host_skill_execution_decision` read and `Get-VibeHostSkillExecutionDecisionMarkdownLines` call in `Write-XlPlan.ps1`.

Replace child handoff line:

```powershell
('- approved_specialist_dispatch_count: {0}' -f @($approvedDispatch).Count),
```

with:

```powershell
('- selected_skill_execution_count: {0}' -f @($approvedDispatch).Count),
```

- [ ] **Step 5: Rename current execution accounting field in `Invoke-PlanExecute.ps1`**

In `specialist_accounting`, remove:

```powershell
dispatch_unit_count = [int]$specialistDispatchUnitCount
```

Keep the existing current field:

```powershell
skill_execution_unit_count = [int]$specialistDispatchUnitCount
```

Do not add a replacement alias for `dispatch_unit_count`.

- [ ] **Step 6: Update tests that read generated current output fields**

Update current behavior tests to assert current fields:

```python
self.assertIn("host_skill_execution_decision", runtime_input_packet)
self.assertNotIn("host_specialist_dispatch_decision", runtime_input_packet)
self.assertGreaterEqual(execute_receipt["skill_execution_unit_count"], 1)
self.assertGreaterEqual(execution_manifest["plan_shadow"]["skill_execution_unit_count"], 1)
self.assertEqual("selected_skill_execution_only", specialist_disclosure["scope"])
```

Where a test validates old decision state strings such as `approved_dispatch`, keep that assertion only if the field is inside `specialist_decision` and delivery acceptance still requires it in this slice. Add a comment in the test explaining the boundary:

```python
# specialist_decision still exposes historical decision-state values in this slice;
# selected/executed/used evidence comes from current skill_execution and skill_usage fields.
```

- [ ] **Step 7: Run current output tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py::CurrentRoutingVocabularyFinalCleanupTests::test_generated_current_artifacts_do_not_use_dispatch_headings_or_counts tests/runtime_neutral/test_runtime_contract_schema.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_l_xl_native_execution_topology.py -q
```

Expected: `PASS`.

- [ ] **Step 8: Commit output wording cleanup**

Run:

```powershell
git add scripts/runtime/VibeRuntime.Common.ps1 scripts/runtime/Write-RequirementDoc.ps1 scripts/runtime/Write-XlPlan.ps1 scripts/runtime/Invoke-PlanExecute.ps1 tests/runtime_neutral/test_runtime_contract_schema.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_l_xl_native_execution_topology.py tests/runtime_neutral/test_custom_admission_bridge.py tests/runtime_neutral/test_structured_bounded_reentry_continuation.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_runtime_delivery_acceptance.py tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py
git commit -m "refactor: use skill execution wording in current outputs"
```

---

### Task 5: Tighten Terminology Scans for Active Policy and Helper Surfaces

**Files:**
- Modify: `config/routing-terminology-hard-cleanup.json`
- Modify: `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1`
- Modify: `scripts/verify/vibe-current-routing-contract-scan.ps1`
- Modify: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
- Modify: `tests/runtime_neutral/test_current_routing_contract_scan.py`

- [ ] **Step 1: Add policy/helper scan configuration**

In `config/routing-terminology-hard-cleanup.json`, add:

```json
"current_policy_helper_files": [
  "config/runtime-input-packet-policy.json",
  "scripts/runtime/VibeRuntime.Common.ps1",
  "scripts/runtime/Freeze-RuntimeInputPacket.ps1",
  "scripts/runtime/Write-RequirementDoc.ps1",
  "scripts/runtime/Write-XlPlan.ps1",
  "scripts/runtime/Invoke-PlanExecute.ps1"
],
"current_policy_helper_forbidden_patterns": [
  "specialist_dispatch_contract",
  "host_specialist_dispatch_contract",
  "interactive_specialist_disclosure",
  "Get-VibeRuntimeSpecialistDispatchProjection",
  "Get-VibeHostSpecialistDispatchContract",
  "Get-VibeHostSpecialistDispatchDecisionMarkdownLines",
  "host_specialist_dispatch_decision",
  "approved_specialist_dispatch_count",
  "Host Specialist Dispatch Decision",
  "dispatch_unit_count ="
],
```

- [ ] **Step 2: Add scan category in `vibe-routing-terminology-hard-cleanup-scan.ps1`**

After the execution-internal scan block, add:

```powershell
$currentPolicyHelperCount = 0
$currentPolicyHelperFiles = @()
if ($config.PSObject.Properties.Name -contains 'current_policy_helper_files') {
    $currentPolicyHelperFiles = @($config.current_policy_helper_files)
}
$currentPolicyHelperForbiddenPatterns = @()
if ($config.PSObject.Properties.Name -contains 'current_policy_helper_forbidden_patterns') {
    $currentPolicyHelperForbiddenPatterns = @($config.current_policy_helper_forbidden_patterns)
}
foreach ($relative in @($currentPolicyHelperFiles)) {
    $path = Join-Path $repoRoot ([string]$relative)
    if (-not (Test-Path -LiteralPath $path)) {
        continue
    }
    $lines = @(Get-Content -LiteralPath $path -Encoding UTF8)
    for ($index = 0; $index -lt $lines.Count; $index += 1) {
        $lineText = [string]$lines[$index]
        foreach ($pattern in @($currentPolicyHelperForbiddenPatterns)) {
            if ([string]::IsNullOrWhiteSpace([string]$pattern)) {
                continue
            }
            if ($lineText.IndexOf([string]$pattern, [System.StringComparison]::Ordinal) -ge 0) {
                $currentPolicyHelperCount += 1
                $findings.Add((New-Finding -Category 'current_policy_helper_dispatch_vocabulary_reference' -Path ([string]$relative) -Line ($index + 1) -Pattern ([string]$pattern) -Text $lineText)) | Out-Null
            }
        }
    }
}
```

Add this field to `$summary`:

```powershell
current_policy_helper_dispatch_vocabulary_reference_count = [int]$currentPolicyHelperCount
```

Add this line to plain output:

```powershell
('Current policy/helper dispatch vocabulary references: {0}' -f [int]$summary.current_policy_helper_dispatch_vocabulary_reference_count)
```

Add the count to the fail condition:

```powershell
if (
    [int]$summary.current_doc_retired_term_violation_count -gt 0 -or
    [int]$summary.current_behavior_test_retired_field_read_count -gt 0 -or
    [int]$summary.historical_doc_unmarked_retired_term_count -gt 0 -or
    [int]$summary.execution_internal_specialist_dispatch_reference_count -gt 0 -or
    [int]$summary.current_policy_helper_dispatch_vocabulary_reference_count -gt 0
) {
    exit 1
}
```

- [ ] **Step 3: Relay the new count in `vibe-current-routing-contract-scan.ps1`**

In the summary object, add:

```powershell
hard_cleanup_current_policy_helper_dispatch_vocabulary_reference_count = if ($hardCleanup) { [int]$hardCleanup.current_policy_helper_dispatch_vocabulary_reference_count } else { 0 }
```

Add a plain output line:

```powershell
('Hard cleanup current policy/helper dispatch vocabulary references: {0}' -f [int]$summary.hard_cleanup_current_policy_helper_dispatch_vocabulary_reference_count)
```

Add it to the gate fail condition so nonzero values fail the current routing contract scan.

- [ ] **Step 4: Update hard-cleanup scan tests**

In `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`, add:

```python
self.assertIn("current_policy_helper_dispatch_vocabulary_reference_count", payload)
self.assertEqual(0, payload["current_policy_helper_dispatch_vocabulary_reference_count"])
```

- [ ] **Step 5: Update current routing contract scan tests**

In `tests/runtime_neutral/test_current_routing_contract_scan.py`, add:

```python
self.assertIn("hard_cleanup_current_policy_helper_dispatch_vocabulary_reference_count", payload)
self.assertEqual(0, int(payload["hard_cleanup_current_policy_helper_dispatch_vocabulary_reference_count"]))
```

Also assert plain output contains:

```python
self.assertIn("Hard cleanup current policy/helper dispatch vocabulary references: 0", completed.stdout)
```

- [ ] **Step 6: Run scan tests and scripts**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_routing_terminology_hard_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py -q
.\scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1
.\scripts\verify\vibe-current-routing-contract-scan.ps1
```

Expected: all pass and both scripts print `Gate Result: PASS`.

- [ ] **Step 7: Commit scan tightening**

Run:

```powershell
git add config/routing-terminology-hard-cleanup.json scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 scripts/verify/vibe-current-routing-contract-scan.ps1 tests/runtime_neutral/test_routing_terminology_hard_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py
git commit -m "test: scan current policy helper routing vocabulary"
```

---

### Task 6: Align Current Runtime Field Documentation

**Files:**
- Modify: `docs/governance/current-runtime-field-contract.md`
- Modify: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
- Modify: `tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py`

- [ ] **Step 1: Update current execution anchors in the governance doc**

In `docs/governance/current-runtime-field-contract.md`, ensure the current execution section uses:

```markdown
selected_skill_execution
skill_execution_units
execution_skill_outcomes
```

Replace current-section references to `approved_skill_execution` with `selected_skill_execution`.

Keep root `specialist_dispatch` only in the retired layer, for example:

```markdown
## Retired Layer

The following names are historical or compatibility-only and must not be used
as current routing state:

- `specialist_dispatch` as root routing packet field
- `approved_dispatch` as current execution accounting field
- `approved_specialist_dispatch_count` as current receipt field
```

- [ ] **Step 2: Update doc test expectation**

In `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`, replace:

```python
"`approved_skill_execution`",
```

with:

```python
"`selected_skill_execution`",
```

Keep the existing assertions for `skill_execution_units` and `execution_skill_outcomes`.

- [ ] **Step 3: Run doc-focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py::CurrentRoutingVocabularyFinalCleanupTests::test_current_runtime_field_doc_uses_selected_skill_execution_anchor tests/runtime_neutral/test_routing_terminology_hard_cleanup.py::RoutingTerminologyHardCleanupTests::test_current_runtime_field_contract_defines_allowed_layers -q
```

Expected: `PASS`.

- [ ] **Step 4: Commit doc cleanup**

Run:

```powershell
git add docs/governance/current-runtime-field-contract.md tests/runtime_neutral/test_routing_terminology_hard_cleanup.py tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py
git commit -m "docs: align current runtime field vocabulary"
```

---

### Task 7: Focused Regression for Current Routing Behavior

**Files:**
- Modify only files that fail because they still read old current fields:
  - `tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py`
  - `tests/runtime_neutral/test_simplified_skill_routing_contract.py`
  - `tests/runtime_neutral/test_terminology_field_simplification.py`
  - `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
  - `tests/runtime_neutral/test_current_routing_contract_scan.py`
  - `tests/runtime_neutral/test_l_xl_native_execution_topology.py`
  - `tests/runtime_neutral/test_runtime_delivery_acceptance.py`
  - `tests/runtime_neutral/test_runtime_contract_schema.py`
  - `tests/runtime_neutral/test_governed_runtime_bridge.py`

- [ ] **Step 1: Run the focused regression suite**

Run:

```powershell
python -m pytest `
  tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py `
  tests/runtime_neutral/test_simplified_skill_routing_contract.py `
  tests/runtime_neutral/test_terminology_field_simplification.py `
  tests/runtime_neutral/test_routing_terminology_hard_cleanup.py `
  tests/runtime_neutral/test_current_routing_contract_scan.py `
  tests/runtime_neutral/test_l_xl_native_execution_topology.py `
  tests/runtime_neutral/test_runtime_delivery_acceptance.py `
  tests/runtime_neutral/test_runtime_contract_schema.py `
  tests/runtime_neutral/test_governed_runtime_bridge.py -q
```

Expected: `PASS`.

- [ ] **Step 2: If a test fails on an old current field read, update that test to current fields**

Use these replacements only in current behavior tests:

```text
host_specialist_dispatch_decision -> host_skill_execution_decision
approved_specialist_dispatch_count -> selected_skill_execution_count
specialist_dispatch_unit_count -> skill_execution_unit_count
dispatch_unit_count -> skill_execution_unit_count
approved_dispatch fixture variable -> selected_skill_execution fixture variable
approved_dispatch_only disclosure scope -> selected_skill_execution_only disclosure scope
```

Do not change tests under `retired_behavior_tests` unless they call a removed current helper and block the focused suite.

- [ ] **Step 3: Re-run the focused regression suite**

Run the same command from Step 1.

Expected: `PASS`.

- [ ] **Step 4: Commit focused regression fixes**

Run:

```powershell
git add tests/runtime_neutral scripts/runtime scripts/verify config docs/governance
git commit -m "test: update current routing vocabulary regressions"
```

If Step 2 made no file changes, skip this commit and record the focused suite result in the final execution summary.

---

### Task 8: Broad Verification Gates

**Files:**
- No planned edits.

- [ ] **Step 1: Run broad verification gates**

Run:

```powershell
.\scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1
.\scripts\verify\vibe-current-routing-contract-scan.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-governed-runtime-contract-gate.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1
.\scripts\verify\vibe-version-packaging-gate.ps1
.\scripts\verify\vibe-version-consistency-gate.ps1
.\scripts\verify\vibe-skill-promotion-execution-gate.ps1
```

Expected:

```text
Gate Result: PASS
```

for each gate that prints a gate result. `vibe-pack-routing-smoke.ps1` should report all pack routing smoke cases passing.

- [ ] **Step 2: Run final formatting and status checks**

Run:

```powershell
git diff --check
git status --short --branch
```

Expected:

```text
git diff --check
```

prints no errors. `git status --short --branch` shows only intentional committed changes or a clean working tree after the final commit.

- [ ] **Step 3: Commit verification-only adjustments if gates required narrow fixes**

If broad gates required narrow code or test adjustments, commit them:

```powershell
git add scripts/runtime scripts/verify config tests docs/governance
git commit -m "fix: stabilize current routing vocabulary cleanup"
```

If broad gates required no file changes, do not create an empty commit.

---

## Acceptance Checklist

- [ ] `config/runtime-input-packet-policy.json` current required fields include `skill_routing` and `skill_usage`, and do not include root `specialist_dispatch` or `specialist_recommendations`.
- [ ] Current policy fields use `skill_execution_contract`, `host_skill_execution_contract`, and `interactive_skill_execution_disclosure`.
- [ ] Current runtime helper is `Get-VibeRuntimeSelectedSkillExecutionProjection`.
- [ ] Current runtime helper does not read root `specialist_dispatch`.
- [ ] Current generated requirement and plan docs say `Host Skill Execution Decision`.
- [ ] Child execution handoff says `selected_skill_execution_count`.
- [ ] Current execution accounting does not emit `dispatch_unit_count`.
- [ ] Current docs use `selected_skill_execution`, `skill_execution_units`, and `execution_skill_outcomes` as execution anchors.
- [ ] `skill_candidates -> skill_routing.selected -> skill_usage.used / skill_usage.unused` behavior remains intact.
- [ ] `selected_skill_execution -> skill_execution_units -> execution_skill_outcomes` behavior remains intact.
- [ ] A selected skill is still not counted as used unless `skill_usage.used` records evidence.
- [ ] Hard cleanup scan reports `current_policy_helper_dispatch_vocabulary_reference_count = 0`.
- [ ] Current routing contract scan reports `hard_cleanup_current_policy_helper_dispatch_vocabulary_reference_count = 0`.
- [ ] Focused tests pass.
- [ ] Broad gates pass.
- [ ] `git diff --check` passes.

---

## Rollback Plan

If a slice changes behavior instead of vocabulary:

```powershell
git status --short
git show --stat --oneline HEAD
```

Identify the last slice commit and revert only that commit:

```powershell
git revert <commit>
```

Then re-run the focused suite from Task 7 before continuing. Do not use `git reset --hard`.
