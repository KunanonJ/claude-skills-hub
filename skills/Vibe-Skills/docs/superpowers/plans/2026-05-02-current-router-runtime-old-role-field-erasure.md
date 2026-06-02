# Current Router Runtime Old-Role Field Erasure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove retired route-authority and stage-assistant role fields from current router/runtime-core implementation paths while preserving current skill selection behavior.

**Architecture:** Make `skill_candidates` the only current pack candidate source, use `_selection_usable` and `_route_usable` as the only internal usability flags, and stop generating or reading old role fields in Python, PowerShell, and runtime packet assembly. Extend the current-routing debt gate so the removed role fields become guarded retired terms rather than hidden implementation residue.

**Tech Stack:** Python 3, pytest, PowerShell 5.1+/pwsh-compatible scripts, JSON policy files, Vibe-Skills runtime-neutral router tests.

---

## File Structure

- Modify: `config/current-routing-debt-erasure.json`
  - Owns the current field chain, retired terms, high-risk retired fields, scan scopes, and success thresholds for current routing debt.
- Modify: `tests/runtime_neutral/test_current_routing_debt_erasure_policy.py`
  - Verifies that the policy treats old role fields as retired/high-risk terms.
- Modify: `tests/runtime_neutral/test_current_routing_debt_gate.py`
  - Verifies the debt gate scans old role fields and that selected current source files no longer contain old role reads.
- Modify: `tests/unit/test_router_contract_selection_guards.py`
  - Verifies Python candidate selection ignores old manifest-only role fields and no longer returns old internal role fields.
- Modify: `packages/runtime-core/src/vgo_runtime/router_contract_selection.py`
  - Owns Python candidate extraction, candidate scoring, and current selection result shape.
- Modify: `tests/runtime_neutral/test_custom_admission_bridge.py`
  - Verifies custom admission uses `_route_usable` and does not expose or store `route_authority_eligible`.
- Modify: `packages/runtime-core/src/vgo_runtime/custom_admission.py`
  - Owns custom workflow/skill admission and current custom pack metadata.
- Modify: `packages/runtime-core/src/vgo_runtime/router_contract_runtime.py`
  - Owns Python route orchestration, custom metadata use, public route output shaping, and admitted candidate public summaries.
- Modify: `tests/runtime_neutral/test_runtime_route_output_shape.py`
  - Verifies Python and PowerShell public route output remains clean and PowerShell no longer extracts old manifest-only candidates.
- Modify: `scripts/router/modules/41-candidate-selection.ps1`
  - Owns PowerShell candidate extraction, scoring, and current selection result shape.
- Modify: `scripts/router/resolve-pack-route.ps1`
  - Owns PowerShell route orchestration, route usability, public route output shaping, and custom metadata use.
- Modify: `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
  - Owns runtime input packet freezing and sibling specialist recommendation logic.

## Current Retired Role Terms

The implementation must remove these terms from current code paths:

```text
route_authority_candidates
stage_assistant_candidates
route_authority_eligible
legacy_role
_legacy_role
_legacy_stage_assistant_candidates
```

After Task 1, these terms may appear only in:

- policy files that define the retired terms;
- tests that assert absence or retired status;
- historical or retired-context docs and plans under allowed paths;
- explicitly retired/legacy compatibility files.

## Task 1: Extend Current Routing Debt Policy For Old Role Fields

**Files:**
- Modify: `config/current-routing-debt-erasure.json`
- Modify: `tests/runtime_neutral/test_current_routing_debt_erasure_policy.py`
- Modify: `tests/runtime_neutral/test_current_routing_debt_gate.py`

- [ ] **Step 1: Add policy tests for retired old role fields**

In `tests/runtime_neutral/test_current_routing_debt_erasure_policy.py`, add this constant after `POLICY_PATH`:

```python
OLD_ROLE_TERMS = [
    "route_authority_candidates",
    "stage_assistant_candidates",
    "route_authority_eligible",
    "legacy_role",
    "_legacy_role",
    "_legacy_stage_assistant_candidates",
]
```

In `test_policy_defines_current_field_chain_and_retired_terms`, after the existing retired-term loop, add:

```python
    for term in OLD_ROLE_TERMS:
        assert term in retired_terms

    high_risk_terms = set(policy["high_risk_retired_fields"])
    for term in OLD_ROLE_TERMS:
        assert term in high_risk_terms
```

- [ ] **Step 2: Add debt gate source-scan tests for old role fields**

In `tests/runtime_neutral/test_current_routing_debt_gate.py`, add this constant after `POLICY`:

```python
OLD_ROLE_TERMS = [
    "route_authority_candidates",
    "stage_assistant_candidates",
    "route_authority_eligible",
    "legacy_role",
    "_legacy_role",
    "_legacy_stage_assistant_candidates",
]
```

Add these tests after `test_gate_policy_file_exists_and_is_valid_json`:

```python
def test_gate_policy_scans_retired_old_role_fields() -> None:
    payload = json.loads(POLICY.read_text(encoding="utf-8"))
    retired_terms = set(payload["retired_terms"])
    high_risk_terms = set(payload["high_risk_retired_fields"])

    for term in OLD_ROLE_TERMS:
        assert term in retired_terms
        assert term in high_risk_terms


def test_current_router_runtime_sources_do_not_contain_retired_old_role_fields() -> None:
    source_files = [
        REPO_ROOT / "packages" / "runtime-core" / "src" / "vgo_runtime" / "router_contract_selection.py",
        REPO_ROOT / "packages" / "runtime-core" / "src" / "vgo_runtime" / "router_contract_runtime.py",
        REPO_ROOT / "packages" / "runtime-core" / "src" / "vgo_runtime" / "custom_admission.py",
        REPO_ROOT / "scripts" / "router" / "modules" / "41-candidate-selection.ps1",
        REPO_ROOT / "scripts" / "router" / "resolve-pack-route.ps1",
        REPO_ROOT / "scripts" / "runtime" / "Freeze-RuntimeInputPacket.ps1",
    ]
    for path in source_files:
        text = path.read_text(encoding="utf-8")
        for term in OLD_ROLE_TERMS:
            assert term not in text, f"{term} remains in {path}"
```

- [ ] **Step 3: Run the policy tests and verify they fail**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_debt_erasure_policy.py -q
```

Expected: FAIL because `config/current-routing-debt-erasure.json` does not yet list the old role fields in `retired_terms` and `high_risk_retired_fields`.

- [ ] **Step 4: Run the source-scan test and verify it fails**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_debt_gate.py::test_current_router_runtime_sources_do_not_contain_retired_old_role_fields -q
```

Expected: FAIL and name current source files containing old role terms, including `router_contract_selection.py`, `custom_admission.py`, `resolve-pack-route.ps1`, `41-candidate-selection.ps1`, and `Freeze-RuntimeInputPacket.ps1`.

- [ ] **Step 5: Update the current routing debt policy**

In `config/current-routing-debt-erasure.json`, add these strings to `retired_terms` after `"stage assistant"`:

```json
    "route_authority_candidates",
    "stage_assistant_candidates",
    "route_authority_eligible",
    "legacy_role",
    "_legacy_role",
    "_legacy_stage_assistant_candidates"
```

Add the same strings to `high_risk_retired_fields` after `"consulted_units"`:

```json
    "route_authority_candidates",
    "stage_assistant_candidates",
    "route_authority_eligible",
    "legacy_role",
    "_legacy_role",
    "_legacy_stage_assistant_candidates"
```

- [ ] **Step 6: Run the policy tests and verify they pass**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_debt_erasure_policy.py -q
```

Expected: PASS.

- [ ] **Step 7: Commit the red source-scan guard**

Run:

```powershell
git add config/current-routing-debt-erasure.json tests/runtime_neutral/test_current_routing_debt_erasure_policy.py tests/runtime_neutral/test_current_routing_debt_gate.py
git commit -m "test: require old role field erasure"
```

Expected: commit succeeds. The focused source-scan test still fails until later tasks remove the old role fields from current sources.

## Task 2: Remove Old Role Fields From Python Candidate Selection

**Files:**
- Modify: `tests/unit/test_router_contract_selection_guards.py`
- Modify: `packages/runtime-core/src/vgo_runtime/router_contract_selection.py`

- [ ] **Step 1: Update Python selection tests for hard-cut behavior**

In `test_pack_skill_candidates_prefer_unified_field_over_legacy_roles`, update the pack fixture so old role fields are marked as retired fixture fields on the same line:

```python
    pack = {
        "skill_candidates": ["primary", "assistant"],
        "route_authority_candidates": ["legacy-only-primary"],  # retired fixture field
        "stage_assistant_candidates": ["legacy-only-assistant"],  # retired fixture field
    }
```

In `tests/unit/test_router_contract_selection_guards.py`, replace `test_pack_skill_candidates_fall_back_to_legacy_role_union_for_old_fixtures` with:

```python
def test_pack_skill_candidates_ignore_retired_role_fields_for_old_fixtures() -> None:
    pack = {
        "route_authority_candidates": ["primary", "shared"],  # retired fixture field
        "stage_assistant_candidates": ["assistant", "shared"],  # retired fixture field
    }

    assert get_pack_skill_candidates(pack) == []
```

In `test_requested_subagent_bypasses_guard`, add this assertion after the existing reason assertion:

```python
    assert "_legacy_stage_assistant_candidates" not in selection
```

In `test_active_skill_candidates_do_not_need_legacy_role_fields`, replace the final assertions with:

```python
    assert selection["selected"] == "helper"
    assert "legacy_role" not in selection["ranking"][0]
    assert "_legacy_role" not in selection["ranking"][0]
    assert "route_authority_eligible" not in selection["ranking"][0]
    assert "_legacy_stage_assistant_candidates" not in selection
    assert "routing_role" not in selection["ranking"][0]
```

- [ ] **Step 2: Run Python selection tests and verify they fail**

Run:

```powershell
python -m pytest tests/unit/test_router_contract_selection_guards.py -q
```

Expected: FAIL because `get_pack_skill_candidates()` still falls back to old role fields and `select_pack_candidate()` still returns `_legacy_stage_assistant_candidates`.

- [ ] **Step 3: Replace Python candidate extraction with skill-candidates-only extraction**

In `packages/runtime-core/src/vgo_runtime/router_contract_selection.py`, replace `get_pack_skill_candidates` with:

```python
def get_pack_skill_candidates(pack: dict[str, Any]) -> list[str]:
    direct_candidates = [
        str(item).strip()
        for item in (pack.get("skill_candidates") or [])
        if str(item).strip()
    ]
    return list(dict.fromkeys(direct_candidates))
```

- [ ] **Step 4: Remove old role constants and old role helper**

In `packages/runtime-core/src/vgo_runtime/router_contract_selection.py`, replace:

```python
INTERNAL_CANDIDATE_USABLE = "_candidate_usable"
INTERNAL_LEGACY_ROLE = "_legacy_role"
INTERNAL_SELECTION_USABLE = "_selection_usable"
INTERNAL_LEGACY_STAGE_ASSISTANTS = "_legacy_stage_assistant_candidates"
```

with:

```python
INTERNAL_CANDIDATE_USABLE = "_candidate_usable"
INTERNAL_SELECTION_USABLE = "_selection_usable"
```

Replace `public_candidate_row` with:

```python
def public_candidate_row(row: dict[str, Any]) -> dict[str, Any]:
    public = dict(row)
    public.pop(INTERNAL_CANDIDATE_USABLE, None)
    return public
```

Replace `candidate_is_usable` with:

```python
def candidate_is_usable(row: dict[str, Any]) -> bool:
    if INTERNAL_CANDIDATE_USABLE in row:
        return bool(row[INTERNAL_CANDIDATE_USABLE])
    return True
```

Delete the entire `candidate_legacy_role` function.

- [ ] **Step 5: Remove old role fields from requested and fallback returns**

In `select_pack_candidate`, update the requested-candidate return inside the `if not filtered_candidates` block so the ranking row does not include `INTERNAL_LEGACY_ROLE` and the returned object does not include `INTERNAL_LEGACY_STAGE_ASSISTANTS`:

```python
            return {
                "selected": requested_candidate,
                "score": 1.0,
                "reason": "requested_skill",
                "ranking": public_candidate_rows([
                    {
                        "skill": requested_candidate,
                        "score": 1.0,
                        "keyword_score": 1.0,
                        "name_score": 1.0,
                        "positive_score": 1.0,
                        "negative_score": 0.0,
                        "canonical_for_task_hit": 1.0,
                        INTERNAL_CANDIDATE_USABLE: True,
                    }
                ]),
                "top1_top2_gap": 1.0,
                "filtered_out_by_task": blocked_by_task,
                INTERNAL_SELECTION_USABLE: True,
                "relevance_score": 1.0,
            }
```

Remove `INTERNAL_LEGACY_STAGE_ASSISTANTS: []` from both filtered-candidate fallback return objects in that same block.

- [ ] **Step 6: Remove role allowlists and old role ranking**

In `select_pack_candidate`, delete this block:

```python
    authority_allowlist = normalize_candidate_keys(pack.get("route_authority_candidates"))
    stage_assistant_allowlist = normalize_candidate_keys(pack.get("stage_assistant_candidates")) if "stage_assistant_candidates" in pack else set()
```

Inside the scoring loop, delete:

```python
        legacy_role = "skill_candidate"
        if candidate_key in authority_allowlist:
            legacy_role = "route_authority"
        elif candidate_key in stage_assistant_allowlist:
            legacy_role = "stage_assistant"
```

Remove `INTERNAL_LEGACY_ROLE: legacy_role,` from the `scored.append` row.

Delete:

```python
    stage_assistant_ranked = [
        row
        for row in ranked_all
        if candidate_legacy_role(row) == "stage_assistant"
    ]
```

- [ ] **Step 7: Remove old role fields from final selection returns**

In the requested-candidate return later in `select_pack_candidate`, remove `INTERNAL_LEGACY_ROLE` from the ranking row and remove `INTERNAL_LEGACY_STAGE_ASSISTANTS` from the returned dict.

In the `not top` return, remove:

```python
            INTERNAL_LEGACY_STAGE_ASSISTANTS: public_candidate_rows(stage_assistant_ranked[:4]),
```

In the fallback return, remove:

```python
            INTERNAL_LEGACY_STAGE_ASSISTANTS: public_candidate_rows([
                row for row in stage_assistant_ranked if row.get("skill") != fallback
            ][:4]),
```

In the final keyword-ranked return, remove:

```python
        INTERNAL_LEGACY_STAGE_ASSISTANTS: public_candidate_rows([
            row for row in stage_assistant_ranked if row.get("skill") != top.get("skill")
        ][:4]),
```

- [ ] **Step 8: Remove the unused normalizer helper if it has no callers**

After deleting old role allowlists, remove this function if `rg "normalize_candidate_keys" packages/runtime-core/src/vgo_runtime/router_contract_selection.py` shows no remaining caller:

```python
def normalize_candidate_keys(values: list[Any] | None) -> set[str]:
    return {
        normalize_text(value)
        for value in (values or [])
        if normalize_text(value)
    }
```

- [ ] **Step 9: Run Python selection tests and verify they pass**

Run:

```powershell
python -m pytest tests/unit/test_router_contract_selection_guards.py -q
```

Expected: PASS.

- [ ] **Step 10: Commit Python candidate selection cleanup**

Run:

```powershell
git add tests/unit/test_router_contract_selection_guards.py packages/runtime-core/src/vgo_runtime/router_contract_selection.py
git commit -m "refactor: erase python old role selection fields"
```

Expected: commit succeeds.

## Task 3: Replace Custom Admission Old Role Eligibility With `_route_usable`

**Files:**
- Modify: `tests/runtime_neutral/test_custom_admission_bridge.py`
- Modify: `packages/runtime-core/src/vgo_runtime/custom_admission.py`
- Modify: `packages/runtime-core/src/vgo_runtime/router_contract_runtime.py`

- [ ] **Step 1: Add direct custom admission metadata assertions**

In `tests/runtime_neutral/test_custom_admission_bridge.py`, add this source-path setup after `REPO_ROOT`:

```python
RUNTIME_SRC = REPO_ROOT / "packages" / "runtime-core" / "src"
if str(RUNTIME_SRC) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SRC))

from vgo_runtime.custom_admission import load_custom_admission  # noqa: E402
```

Add this test at the start of `CustomAdmissionBridgeTests`:

```python
    def test_custom_admission_internal_metadata_uses_route_usable_not_old_role_field(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            target_root = Path(tempdir) / ".codex"
            write_custom_skill(target_root, skill_id="genomics-qc-flow", trigger_mode="auto")

            admission = load_custom_admission(
                repo_root=REPO_ROOT,
                target_root=target_root,
                requested_canonical=None,
            )

            self.assertEqual("admitted", admission["status"])
            admitted = admission["admitted_candidates"][0]
            self.assertIn("_route_usable", admitted)
            self.assertTrue(bool(admitted["_route_usable"]))
            self.assertNotIn("route_authority_eligible", admitted)
            self.assertEqual(admitted["_route_usable"], admitted["pack"]["custom_admission"]["_route_usable"])
            self.assertNotIn("route_authority_eligible", admitted["pack"]["custom_admission"])
```

In `test_runtime_neutral_router_admits_advisory_custom_candidate_without_route_authority`, inside the loop over `admitted_candidates`, add:

```python
                self.assertNotIn("_route_usable", admitted)
```

- [ ] **Step 2: Run custom admission tests and verify they fail**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_custom_admission_bridge.py::CustomAdmissionBridgeTests::test_custom_admission_internal_metadata_uses_route_usable_not_old_role_field tests/runtime_neutral/test_custom_admission_bridge.py::CustomAdmissionBridgeTests::test_runtime_neutral_router_admits_advisory_custom_candidate_without_route_authority -q
```

Expected: FAIL because internal admission still writes `route_authority_eligible`.

- [ ] **Step 3: Rename the custom admission eligibility helper**

In `packages/runtime-core/src/vgo_runtime/custom_admission.py`, replace:

```python
def _route_authority_eligible(trigger_mode: str, requested_canonical: str | None, skill_id: str) -> bool:
    if trigger_mode == "auto":
        return True
    if requested_canonical and _normalize_text(requested_canonical) == _normalize_text(skill_id):
        return True
    return False
```

with:

```python
def _route_usable(trigger_mode: str, requested_canonical: str | None, skill_id: str) -> bool:
    if trigger_mode == "auto":
        return True
    if requested_canonical and _normalize_text(requested_canonical) == _normalize_text(skill_id):
        return True
    return False
```

- [ ] **Step 4: Write `_route_usable` into admitted metadata**

In the `admitted = { ... }` dict, replace:

```python
        "route_authority_eligible": _route_authority_eligible(trigger_mode, requested_canonical, skill_id),
```

with:

```python
        "_route_usable": _route_usable(trigger_mode, requested_canonical, skill_id),
```

In `custom_summary`, replace:

```python
        "_route_usable": admitted["route_authority_eligible"],
```

with:

```python
        "_route_usable": admitted["_route_usable"],
```

- [ ] **Step 5: Remove Python runtime fallback to old custom metadata**

In `packages/runtime-core/src/vgo_runtime/router_contract_runtime.py`, update `_public_custom_metadata` to:

```python
def _public_custom_metadata(value: object) -> object:
    if not isinstance(value, dict):
        return value
    public = dict(value)
    public.pop(INTERNAL_ROUTE_USABLE, None)
    return public
```

Update `_public_pack_row` to remove only current internal route usability:

```python
def _public_pack_row(row: dict[str, object]) -> dict[str, object]:
    public = dict(row)
    public.pop(INTERNAL_ROUTE_USABLE, None)
    public["candidate_ranking"] = public_candidate_rows(list(public.get("candidate_ranking") or []))
    public["custom_admission"] = _public_custom_metadata(public.get("custom_admission"))
    return public
```

Update `_public_admitted_candidates` to:

```python
def _public_admitted_candidates(rows: object) -> list[dict[str, object]]:
    public_rows: list[dict[str, object]] = []
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        public_row = dict(row)
        public_row.pop(INTERNAL_ROUTE_USABLE, None)
        public_rows.append(public_row)
    return public_rows
```

In `route_prompt`, replace:

```python
            route_usable = route_usable and bool(
                custom_metadata.get(INTERNAL_ROUTE_USABLE, custom_metadata.get("route_authority_eligible", False))
            )
```

with:

```python
            route_usable = route_usable and bool(custom_metadata.get(INTERNAL_ROUTE_USABLE, False))
```

- [ ] **Step 6: Run custom admission tests and verify they pass**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_custom_admission_bridge.py -q
```

Expected: PASS.

- [ ] **Step 7: Commit custom admission cleanup**

Run:

```powershell
git add tests/runtime_neutral/test_custom_admission_bridge.py packages/runtime-core/src/vgo_runtime/custom_admission.py packages/runtime-core/src/vgo_runtime/router_contract_runtime.py
git commit -m "refactor: replace old custom admission role eligibility"
```

Expected: commit succeeds.

## Task 4: Remove Old Role Fields From PowerShell Candidate Selection

**Files:**
- Modify: `tests/runtime_neutral/test_runtime_route_output_shape.py`
- Modify: `scripts/router/modules/41-candidate-selection.ps1`
- Modify: `scripts/router/resolve-pack-route.ps1`

- [ ] **Step 1: Add PowerShell old manifest-only candidate extraction test**

In `tests/runtime_neutral/test_runtime_route_output_shape.py`, add this helper after `assert_public_route_output_shape`:

```python
def run_powershell_old_manifest_candidate_probe(testcase: unittest.TestCase) -> list[str]:
    shell = resolve_powershell()
    if shell is None:
        testcase.skipTest("PowerShell executable not available")

    module_path = REPO_ROOT / "scripts" / "router" / "modules" / "41-candidate-selection.ps1"
    script = (
        f". '{module_path}'; "
        "$pack = [pscustomobject]@{ "
        "route_authority_candidates = @('primary','shared'); "  # retired fixture field
        "stage_assistant_candidates = @('assistant','shared') "  # retired fixture field
        "}; "
        "$result = @(Get-PackSkillCandidates -Pack $pack); "
        "$result | ConvertTo-Json -Depth 5"
    )
    completed = subprocess.run(
        [shell, "-NoLogo", "-NoProfile", "-Command", script],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    output = completed.stdout.strip()
    if not output:
        return []
    payload = json.loads(output)
    return payload if isinstance(payload, list) else [payload]
```

Add this test inside `RuntimeRouteOutputShapeTests` before the route-output tests:

```python
    def test_powershell_pack_skill_candidates_ignore_retired_role_fields(self) -> None:
        self.assertEqual([], run_powershell_old_manifest_candidate_probe(self))
```

- [ ] **Step 2: Run the PowerShell candidate extraction test and verify it fails**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_runtime_route_output_shape.py::RuntimeRouteOutputShapeTests::test_powershell_pack_skill_candidates_ignore_retired_role_fields -q
```

Expected: FAIL because `Get-PackSkillCandidates` still returns old role-field candidates.

- [ ] **Step 3: Replace PowerShell candidate extraction**

In `scripts/router/modules/41-candidate-selection.ps1`, replace `Get-PackSkillCandidates` with:

```powershell
function Get-PackSkillCandidates {
    param(
        [object]$Pack
    )

    if (-not $Pack) { return @() }

    if (-not ($Pack.PSObject.Properties.Name -contains 'skill_candidates')) {
        return @()
    }

    $directCandidates = @($Pack.skill_candidates | ForEach-Object { ([string]$_).Trim() } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    return @($directCandidates | Select-Object -Unique)
}
```

- [ ] **Step 4: Remove old role field stripping and fallback from PowerShell selection**

In `ConvertTo-PublicCandidateRanking`, replace the old-field filter:

```powershell
            if ($property.Name -in @('_candidate_usable', '_legacy_role', 'route_authority_eligible', 'legacy_role')) {
                continue
            }
```

with:

```powershell
            if ($property.Name -in @('_candidate_usable')) {
                continue
            }
```

In `Test-CandidateUsable`, remove the old fallback block and leave:

```powershell
function Test-CandidateUsable {
    param([AllowNull()] [object]$Row)

    if ($null -eq $Row) {
        return $false
    }
    if ($Row.PSObject.Properties.Name -contains '_candidate_usable') {
        return [bool]$Row._candidate_usable
    }
    return $true
}
```

Delete the entire `Get-CandidateLegacyRole` function.

- [ ] **Step 5: Replace requested-skill helper**

In `scripts/router/modules/41-candidate-selection.ps1`, replace `New-RequestedSkillSelection` with:

```powershell
function New-RequestedSkillSelection {
    param(
        [string]$RequestedCandidate,
        [object[]]$BlockedByTask
    )

    return [pscustomobject]@{
        selected = $RequestedCandidate
        score = 1.0
        reason = "requested_skill"
        ranking = @(ConvertTo-PublicCandidateRanking -Rows @(
            [pscustomobject]@{
                skill = $RequestedCandidate
                score = 1.0
                keyword_score = 1.0
                name_score = 1.0
                positive_score = 1.0
                negative_score = 0.0
                canonical_for_task_hit = 1.0
                _candidate_usable = $true
            }
        ))
        top1_top2_gap = 1.0
        filtered_out_by_task = @($BlockedByTask)
        _selection_usable = $true
        relevance_score = 1.0
    }
}
```

Update both calls to `New-RequestedSkillSelection` so they pass only:

```powershell
return New-RequestedSkillSelection -RequestedCandidate $requestedCandidate -BlockedByTask @($blockedByTask)
```

- [ ] **Step 6: Remove role allowlists and legacy fields from PowerShell scoring**

In `Select-PackCandidate`, delete:

```powershell
    $authorityAllowlist = @()
    if ($Pack.PSObject.Properties.Name -contains 'route_authority_candidates') {
        $authorityAllowlist = @($Pack.route_authority_candidates | ForEach-Object { ([string]$_).Trim().ToLowerInvariant() } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    }
    $stageAssistantAllowlist = @()
    if ($Pack.PSObject.Properties.Name -contains 'stage_assistant_candidates') {
        $stageAssistantAllowlist = @($Pack.stage_assistant_candidates | ForEach-Object { ([string]$_).Trim().ToLowerInvariant() } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    }
```

Delete:

```powershell
        $legacyRole = if ($authorityAllowlist -contains $candidateKey) { "route_authority" } elseif ($stageAssistantAllowlist -contains $candidateKey) { "stage_assistant" } else { "skill_candidate" }
```

Remove this property from scored rows:

```powershell
            _legacy_role = $legacyRole
```

Delete:

```powershell
    $stageAssistantRanked = @($ranked | Where-Object { [string](Get-CandidateLegacyRole -Row $_) -eq 'stage_assistant' })
```

Remove every `_legacy_stage_assistant_candidates = ...` property from return objects in this function.

- [ ] **Step 7: Remove old role usability fallback from PowerShell route orchestration**

In `scripts/router/resolve-pack-route.ps1`, replace:

```powershell
    $routeUsable = if ($selection.PSObject.Properties.Name -contains '_selection_usable') { [bool]$selection._selection_usable } elseif ($selection.PSObject.Properties.Name -contains 'route_authority_eligible') { [bool]$selection.route_authority_eligible } else { -not [string]::IsNullOrWhiteSpace([string]$selection.selected) }
```

with:

```powershell
    $routeUsable = if ($selection.PSObject.Properties.Name -contains '_selection_usable') { [bool]$selection._selection_usable } else { -not [string]::IsNullOrWhiteSpace([string]$selection.selected) }
```

Replace:

```powershell
    if ($null -ne $customMetadata -and $customMetadata.PSObject.Properties.Name -contains '_route_usable') {
        $routeUsable = $routeUsable -and [bool]$customMetadata._route_usable
    } elseif ($null -ne $customMetadata -and $customMetadata.PSObject.Properties.Name -contains 'route_authority_eligible') {
        $routeUsable = $routeUsable -and [bool]$customMetadata.route_authority_eligible
    }
```

with:

```powershell
    if ($null -ne $customMetadata -and $customMetadata.PSObject.Properties.Name -contains '_route_usable') {
        $routeUsable = $routeUsable -and [bool]$customMetadata._route_usable
    }
```

In `ConvertTo-PublicRouteCustomMetadata`, remove `route_authority_eligible` from the filtered list:

```powershell
        if ($property.Name -in @('_route_usable')) {
            continue
        }
```

In `ConvertTo-PublicAdmittedCandidates`, remove `route_authority_eligible` from the filtered list:

```powershell
            if ($property.Name -in @('_route_usable')) {
                continue
            }
```

In `ConvertTo-PublicRoutePackRow`, remove old role fields from the filtered list:

```powershell
        if ($property.Name -in @('_route_usable')) {
            continue
        }
```

- [ ] **Step 8: Run PowerShell route output tests and verify they pass**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_runtime_route_output_shape.py -q
```

Expected: PASS.

- [ ] **Step 9: Commit PowerShell router cleanup**

Run:

```powershell
git add tests/runtime_neutral/test_runtime_route_output_shape.py scripts/router/modules/41-candidate-selection.ps1 scripts/router/resolve-pack-route.ps1
git commit -m "refactor: erase powershell old role selection fields"
```

Expected: commit succeeds.

## Task 5: Remove Old Role Eligibility From Runtime Packet Sibling Recommendations

**Files:**
- Modify: `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- Modify: `tests/runtime_neutral/test_current_routing_debt_gate.py`

- [ ] **Step 1: Add targeted runtime packet source assertion**

In `tests/runtime_neutral/test_current_routing_debt_gate.py`, add this test after `test_current_router_runtime_sources_do_not_contain_retired_old_role_fields`:

```python
def test_runtime_packet_sibling_recommendations_use_neutral_ranking_language() -> None:
    text = (REPO_ROOT / "scripts" / "runtime" / "Freeze-RuntimeInputPacket.ps1").read_text(encoding="utf-8")

    assert "route_authority_eligible" not in text
    assert "additional XL route-authority specialist candidate" not in text
    assert "additional XL ranked specialist candidate" in text
```

- [ ] **Step 2: Run targeted runtime packet assertion and verify it fails**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_debt_gate.py::test_runtime_packet_sibling_recommendations_use_neutral_ranking_language -q
```

Expected: FAIL because `Freeze-RuntimeInputPacket.ps1` still reads `route_authority_eligible` and still uses route-authority wording in the sibling recommendation reason.

- [ ] **Step 3: Replace sibling eligibility check with neutral score checks**

In `scripts/runtime/Freeze-RuntimeInputPacket.ps1`, replace:

```powershell
            $siblingRouteAuthorityEligible = if ($sibling.PSObject.Properties.Name -contains 'route_authority_eligible') { [bool]$sibling.route_authority_eligible } else { $false }
            if (-not $siblingRouteAuthorityEligible) {
                continue
            }
            $siblingScore = if ($sibling.PSObject.Properties.Name -contains 'score') { [double]$sibling.score } else { 0.0 }
```

with:

```powershell
            $siblingScore = if ($sibling.PSObject.Properties.Name -contains 'score') { [double]$sibling.score } else { 0.0 }
```

Keep the existing score floor:

```powershell
            if ($siblingScore -lt 0.2) {
                continue
            }
```

Keep the existing close-score guard:

```powershell
            if ($selectedCandidateScore -gt 0.0 -and (($selectedCandidateScore - $siblingScore) -gt 0.1)) {
                continue
            }
```

- [ ] **Step 4: Replace sibling recommendation reason**

In the same block, replace:

```powershell
            $reason = "additional XL route-authority specialist candidate from pack '{0}'" -f ([string]$ranked.pack_id)
```

with:

```powershell
            $reason = "additional XL ranked specialist candidate from pack '{0}'" -f ([string]$ranked.pack_id)
```

- [ ] **Step 5: Run runtime packet source tests and verify they pass**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_debt_gate.py::test_runtime_packet_sibling_recommendations_use_neutral_ranking_language tests/runtime_neutral/test_current_routing_debt_gate.py::test_current_router_runtime_sources_do_not_contain_retired_old_role_fields -q
```

Expected: PASS if Tasks 2-5 removed all current-source old role terms.

- [ ] **Step 6: Run governed runtime bridge tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py -q
```

Expected: PASS.

- [ ] **Step 7: Commit runtime packet cleanup**

Run:

```powershell
git add scripts/runtime/Freeze-RuntimeInputPacket.ps1 tests/runtime_neutral/test_current_routing_debt_gate.py
git commit -m "refactor: remove old role sibling recommendation gate"
```

Expected: commit succeeds.

## Task 6: Close Debt Gate And Routing Regression Matrix

**Files:**
- Verify only unless a focused regression exposes a missed old role field or route drift.

- [ ] **Step 1: Run the full current routing debt gate tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_debt_gate.py -q
```

Expected: PASS.

- [ ] **Step 2: Run the current routing debt gate directly**

Run:

```powershell
powershell.exe -NoLogo -NoProfile -File .\scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
```

Expected: exit code `0`, JSON `status` is `pass`, and `summary.P0`, `summary.P1`, and `summary.P2` are all `0`.

- [ ] **Step 3: Run Python and PowerShell route output shape tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_runtime_route_output_shape.py -q
```

Expected: PASS.

- [ ] **Step 4: Run router bridge and simplified routing contract tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_simplified_skill_routing_contract.py -q
```

Expected: PASS.

- [ ] **Step 5: Run custom admission and runtime bridge tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_custom_admission_bridge.py tests/runtime_neutral/test_governed_runtime_bridge.py -q
```

Expected: PASS.

- [ ] **Step 6: Run route smoke if time permits**

Run:

```powershell
powershell.exe -NoLogo -NoProfile -File .\scripts\verify\vibe-pack-routing-smoke.ps1
```

Expected: exit code `0`. If this command is slow or environment-dependent, keep the exact failure output and run the focused route tests from Steps 3-5.

- [ ] **Step 7: Run whitespace check**

Run:

```powershell
git diff --check
```

Expected: no output and exit code `0`.

- [ ] **Step 8: Commit final verification notes only if a tracked artifact changed**

Run:

```powershell
git status --short
```

Expected: no uncommitted tracked changes after previous commits. If a verification artifact under `docs/audits` was intentionally updated by `-WriteArtifacts`, stage only that artifact and commit:

```powershell
git add docs/audits/2026-05-02-current-routing-debt-audit.md
git commit -m "docs: refresh old role field debt audit"
```

If no tracked artifact changed, do not create an empty commit.

## Final Verification Checklist

Before reporting completion, confirm:

```text
1. config/pack-manifest.json has no route_authority_candidates or stage_assistant_candidates.
2. packages/runtime-core/src/vgo_runtime/router_contract_selection.py has none of the old role terms.
3. packages/runtime-core/src/vgo_runtime/router_contract_runtime.py has none of the old role terms.
4. packages/runtime-core/src/vgo_runtime/custom_admission.py has none of the old role terms.
5. scripts/router/modules/41-candidate-selection.ps1 has none of the old role terms.
6. scripts/router/resolve-pack-route.ps1 has none of the old role terms.
7. scripts/runtime/Freeze-RuntimeInputPacket.ps1 has none of the old role terms.
8. tests prove old manifest-only packs no longer create current candidates.
9. public route output remains free of old role fields.
10. custom admission uses _route_usable internally and strips it from public summaries.
11. debt gate reports P0/P1/P2 = 0/0/0.
```

Use this command for the source-term check:

```powershell
rg -n "route_authority_candidates|stage_assistant_candidates|route_authority_eligible|legacy_role|_legacy_role|_legacy_stage_assistant_candidates" packages/runtime-core/src/vgo_runtime scripts/router scripts/runtime/Freeze-RuntimeInputPacket.ps1
```

Expected: no output.
