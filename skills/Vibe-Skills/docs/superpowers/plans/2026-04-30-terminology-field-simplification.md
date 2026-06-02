# Terminology Field Simplification Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the active skill routing skeleton use only `skill_candidates -> selected skill -> used / unused` while preserving six-stage runtime behavior and old artifact compatibility.

**Architecture:** Active pack configuration becomes field-minimal: `skill_candidates` is the only candidate list in `config/pack-manifest.json`. Runtime helper code keeps old-field fallback readers for old fixtures, but new active config and public docs stop presenting `route_authority_candidates` and `stage_assistant_candidates` as current concepts.

**Tech Stack:** JSON config, Python pytest, PowerShell runtime/router helpers, Markdown docs.

---

## File Structure

- Create: `docs/governance/terminology-governance.md`
  - Canonical active vocabulary and deprecated vocabulary for current development.
- Create: `tests/runtime_neutral/test_terminology_field_simplification.py`
  - Field-shape and public terminology guardrail tests.
- Modify: `README.md`
  - Replace public routing wording that says `primary route` or `specialist Skills` with selected-skill vocabulary.
- Modify: `README.zh.md`
  - Replace public Chinese wording such as `专家助手` and `主路线` with `选中 Skills` / `候选 skill` wording.
- Modify: `config/pack-manifest.json`
  - Remove `route_authority_candidates` and `stage_assistant_candidates` from every active pack.
- Modify: `tests/unit/test_router_contract_selection_guards.py`
  - Keep old-field fallback fixture coverage, add active-pack coverage where old fields are absent.
- Modify: route and pack tests that currently assert old active fields:
  - `tests/runtime_neutral/test_ai_llm_pack_consolidation.py`
  - `tests/runtime_neutral/test_aios_core_hard_removal.py`
  - `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`
  - `tests/runtime_neutral/test_bio_science_second_pass_consolidation.py`
  - `tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py`
  - `tests/runtime_neutral/test_cold_platform_quantum_pack_deletion.py`
  - `tests/runtime_neutral/test_design_implementation_pack_consolidation.py`
  - `tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py`
  - `tests/runtime_neutral/test_final_stage_assistant_removal.py`
  - `tests/runtime_neutral/test_finance_edgar_macro_pack_consolidation.py`
  - `tests/runtime_neutral/test_global_pack_consolidation_audit.py`
  - `tests/runtime_neutral/test_integration_devops_pack_consolidation.py`
  - `tests/runtime_neutral/test_longtail_science_ml_pack_cleanup.py`
  - `tests/runtime_neutral/test_ml_skills_pruning_audit.py`
  - `tests/runtime_neutral/test_research_design_pack_consolidation.py`
  - `tests/runtime_neutral/test_router_bridge.py`
  - `tests/runtime_neutral/test_ruc_nlpir_augmentation_cleanup.py`
  - `tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py`
  - `tests/runtime_neutral/test_science_chem_drug_pack_consolidation.py`
  - `tests/runtime_neutral/test_science_clinical_regulatory_pack_consolidation.py`
  - `tests/runtime_neutral/test_science_communication_slides_pack_consolidation.py`
  - `tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py`
  - `tests/runtime_neutral/test_science_literature_peer_review_consolidation.py`
  - `tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py`
  - `tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py`
  - `tests/runtime_neutral/test_zero_route_authority_second_pass.py`
  - `tests/runtime_neutral/test_zero_route_authority_third_pass.py`

---

### Task 1: Add Failing Field And Terminology Guardrail Tests

**Files:**
- Create: `tests/runtime_neutral/test_terminology_field_simplification.py`

- [ ] **Step 1: Create the failing contract test**

Create `tests/runtime_neutral/test_terminology_field_simplification.py` with this full content:

```python
from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PACK_MANIFEST = REPO_ROOT / "config" / "pack-manifest.json"
TERMINOLOGY_DOC = REPO_ROOT / "docs" / "governance" / "terminology-governance.md"
PUBLIC_DOCS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "README.zh.md",
]

DEPRECATED_ACTIVE_PATTERNS = [
    r"\bprimary route\b",
    r"\bprimary skill\b",
    r"\bsecondary skill\b",
    r"\bdirect owner\b",
    r"\broute owner\b",
    r"\bstage assistant\b",
    r"\bspecialist skills\b",
    r"\bspecialist Skills\b",
    "主路由",
    "主路线",
    "主技能",
    "次技能",
    "阶段助手",
    "辅助专家",
    "咨询专家",
    "专家助手",
]


def load_manifest() -> dict[str, object]:
    return json.loads(PACK_MANIFEST.read_text(encoding="utf-8-sig"))


def test_active_pack_manifest_uses_only_skill_candidates() -> None:
    manifest = load_manifest()
    packs = manifest.get("packs")
    assert isinstance(packs, list)
    assert packs

    for pack in packs:
        assert isinstance(pack, dict)
        pack_id = str(pack.get("id") or "")
        assert pack_id
        assert "route_authority_candidates" not in pack, pack_id
        assert "stage_assistant_candidates" not in pack, pack_id
        skill_candidates = pack.get("skill_candidates")
        assert isinstance(skill_candidates, list), pack_id
        assert skill_candidates, pack_id
        assert all(isinstance(item, str) and item.strip() for item in skill_candidates), pack_id


def test_pack_defaults_point_to_skill_candidates() -> None:
    manifest = load_manifest()
    for pack in manifest["packs"]:
        pack_id = str(pack["id"])
        candidates = set(pack.get("skill_candidates") or [])
        defaults = pack.get("defaults_by_task") or {}
        assert isinstance(defaults, dict), pack_id
        for task_type, skill_id in defaults.items():
            assert skill_id in candidates, f"{pack_id}:{task_type}:{skill_id}"


def test_terminology_governance_doc_exists_and_defines_active_model() -> None:
    text = TERMINOLOGY_DOC.read_text(encoding="utf-8")
    assert "skill_candidates -> selected skill -> used / unused" in text
    assert "`skill_candidates`" in text
    assert "`skill_routing.selected`" in text
    assert "`skill_usage.used`" in text
    assert "`skill_usage.unused`" in text
    assert "Legacy compatibility" in text


def test_public_docs_do_not_use_deprecated_routing_terms_as_active_language() -> None:
    failures: list[str] = []
    for path in PUBLIC_DOCS:
        text = path.read_text(encoding="utf-8")
        for pattern in DEPRECATED_ACTIVE_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                failures.append(f"{path.relative_to(REPO_ROOT)} contains {pattern!r}")
    assert failures == []
```

- [ ] **Step 2: Run the new test and confirm it fails for the current repo**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_terminology_field_simplification.py -q
```

Expected: FAIL. The failure must mention at least one of:

```text
route_authority_candidates
stage_assistant_candidates
terminology-governance.md
primary route
specialist Skills
专家助手
主路线
```

- [ ] **Step 3: Commit the failing test**

Run:

```powershell
git add tests/runtime_neutral/test_terminology_field_simplification.py
git commit -m "test: add terminology field simplification guard"
```

Expected: commit succeeds with only the new test file.

---

### Task 2: Add Canonical Terminology Governance And Clean Public README Wording

**Files:**
- Create: `docs/governance/terminology-governance.md`
- Modify: `README.md`
- Modify: `README.zh.md`
- Test: `tests/runtime_neutral/test_terminology_field_simplification.py`

- [ ] **Step 1: Add the terminology governance document**

Create `docs/governance/terminology-governance.md` with this full content:

```markdown
# Terminology Governance

Date: 2026-04-30

## Active Model

Current routing and usage language is:

```text
skill_candidates -> selected skill -> used / unused
```

This vocabulary is the active product and implementation language for new routing work.

## Active Terms

| Term | Meaning |
| --- | --- |
| `skill` | A bounded capability with a `SKILL.md` entrypoint. |
| `skill_candidates` | The active pack field listing skills that may be selected for that pack. |
| `selected skill` | A skill selected for the current task, stage, or bounded work unit. |
| `skill_routing.selected` | Runtime evidence that a skill was selected into the governed workflow. |
| `skill_usage.used` | Runtime evidence that a selected skill was loaded and materially shaped artifacts. |
| `skill_usage.unused` | Runtime evidence that a selected skill was not materially used, with a reason. |
| `legacy_skill_routing` | Legacy compatibility container used only to read older runtime artifacts. |

## Deprecated Terms

Do not introduce these names as active concepts in new docs, config, tests, or runtime output:

| Deprecated name | Replacement |
| --- | --- |
| `route_authority` / `route owner` / `direct owner` | `skill_candidates` or `selected skill` |
| `primary route` / `primary skill` / `secondary skill` | `selected skill` or `candidate skill` |
| `stage_assistant` | Legacy compatibility only |
| `specialist Skills` as an active routing class | `selected Skills` |
| `approved dispatch` as evidence of use | `skill_usage.used` / `skill_usage.unused` |
| `主路由` / `主路线` / `主技能` / `次技能` | `候选 skill` or `选中 skill` |
| `阶段助手` / `辅助专家` / `咨询专家` / `专家助手` | Do not use as an active concept |

## Legacy Compatibility

Old runtime artifacts may still contain `specialist_dispatch`, `specialist_recommendations`, `stage_assistant_hints`, `route_authority_candidates`, or `stage_assistant_candidates`.

Readers may keep compatibility paths while old fixtures exist. New active configuration must not write those pack fields, and new public docs must not present those names as current routing concepts.

## Evidence Rule

Selection and usage are separate:

- `skill_routing.selected` means a skill was selected.
- `skill_usage.used` means a selected skill was loaded and materially shaped artifacts.
- `skill_usage.unused` means a selected skill did not materially shape artifacts.

Do not claim a skill was used from candidate, selected, or dispatch data alone.
```

- [ ] **Step 2: Replace English README public routing wording**

In `README.md`, make these exact replacements:

```text
which specialist Skills should help
```

to:

```text
which Skills are selected for the current task or stage
```

```text
The router picks bounded roles, and specialist Skills stay scoped to the current phase or work unit.
```

to:

```text
The router selects Skills with bounded scope, and selected Skills stay scoped to the current phase or work unit.
```

```text
After selecting the primary route, the runtime also chooses the execution grade based on task complexity:
```

to:

```text
After selecting the route, the runtime also chooses the execution grade based on task complexity:
```

```text
The system decides the main route first, then assigns skills to each bounded unit under the same governed coordinator.
```

to:

```text
The system selects the route first, then selects Skills for each bounded unit under the same governed coordinator.
```

```text
When specialist skills such as `tdd-guide` or `code-review` are called, they assist a phase or a bounded unit. They do not take over global coordination.
```

to:

```text
When Skills such as `tdd-guide` or `code-review` are selected, they work only inside the current phase or bounded unit. They do not take over global coordination.
```

```text
In XL multi-agent work, worker lanes can suggest specialist help, but the coordinator approves the final assignment.
```

to:

```text
In XL multi-agent work, worker lanes can surface candidate Skills, but the coordinator confirms the selected Skills.
```

- [ ] **Step 3: Replace Chinese README public routing wording**

In `README.zh.md`, make these exact replacements:

```text
Skills 变成按阶段、按任务调用的专家助手。
```

to:

```text
Skills 变成按阶段、按任务选中的工作能力。
```

```text
什么时候让专家 Skills 介入
```

to:

```text
什么时候选择相关 Skills 加入当前阶段
```

```text
按阶段自动调度专家
```

to:

```text
按阶段选择 Skills
```

```text
为什么大量专家 Skills 可以共存
```

to:

```text
为什么大量 Skills 可以共存
```

```text
选定主路线之后，运行时还会根据任务复杂度决定执行级别：
```

to:

```text
选定路线之后，运行时还会根据任务复杂度决定执行级别：
```

```text
系统会先定主路线，再把技能分配给有边界的任务单元，整个过程仍由同一个受管协调者控制。
```

to:

```text
系统会先选定路线，再为有边界的任务单元选择 Skills，整个过程仍由同一个受管协调者控制。
```

```text
在 XL 多代理流程里，子代理可以提出专项技能建议，但最终由协调者确认分配。
```

to:

```text
在 XL 多代理流程里，子代理可以提出候选 skill，但最终由协调者确认选中项。
```

- [ ] **Step 4: Run the terminology test and confirm only manifest shape still fails**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_terminology_field_simplification.py -q
```

Expected: FAIL only because `config/pack-manifest.json` still contains `route_authority_candidates` and `stage_assistant_candidates`.

- [ ] **Step 5: Commit terminology docs and README cleanup**

Run:

```powershell
git add docs/governance/terminology-governance.md README.md README.zh.md
git commit -m "docs: define active skill routing terminology"
```

Expected: commit succeeds with the governance doc and README updates only.

---

### Task 3: Remove Legacy Candidate Fields From Active Pack Manifest

**Files:**
- Modify: `config/pack-manifest.json`
- Test: `tests/runtime_neutral/test_terminology_field_simplification.py`

- [ ] **Step 1: Remove legacy fields mechanically from active manifest**

Run this PowerShell command from the repo root:

```powershell
$path = 'config/pack-manifest.json'
$json = Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($pack in @($json.packs)) {
  if ($pack.PSObject.Properties.Name -contains 'route_authority_candidates') {
    $pack.PSObject.Properties.Remove('route_authority_candidates')
  }
  if ($pack.PSObject.Properties.Name -contains 'stage_assistant_candidates') {
    $pack.PSObject.Properties.Remove('stage_assistant_candidates')
  }
}
$json | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $path -Encoding UTF8
```

- [ ] **Step 2: Verify field-shape test now passes**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_terminology_field_simplification.py -q
```

Expected:

```text
4 passed
```

- [ ] **Step 3: Inspect the manifest diff**

Run:

```powershell
git diff -- config/pack-manifest.json
```

Expected: only `route_authority_candidates` and `stage_assistant_candidates` entries are removed. No pack IDs, `skill_candidates`, `defaults_by_task`, `trigger_keywords`, grade boundaries, or task boundaries are removed.

- [ ] **Step 4: Commit active manifest simplification**

Run:

```powershell
git add config/pack-manifest.json
git commit -m "config: remove legacy pack candidate fields"
```

Expected: commit succeeds with only `config/pack-manifest.json`.

---

### Task 4: Update Unit-Level Selection Compatibility Tests

**Files:**
- Modify: `tests/unit/test_router_contract_selection_guards.py`

- [ ] **Step 1: Update the synthetic active-pack fixture in `_selection`**

In `tests/unit/test_router_contract_selection_guards.py`, change the `pack={...}` argument inside `_selection()` from:

```python
        pack={
            "id": "synthetic-process-pack",
            "skill_candidates": ["subagent-driven-development"],
            "route_authority_candidates": ["subagent-driven-development"],
            "stage_assistant_candidates": [],
            "defaults_by_task": {},
        },
```

to:

```python
        pack={
            "id": "synthetic-process-pack",
            "skill_candidates": ["subagent-driven-development"],
            "defaults_by_task": {},
        },
```

- [ ] **Step 2: Keep old-field fallback coverage but label it as legacy fixture coverage**

Rename:

```python
def test_pack_skill_candidates_fall_back_to_legacy_role_union() -> None:
```

to:

```python
def test_pack_skill_candidates_fall_back_to_legacy_role_union_for_old_fixtures() -> None:
```

Keep the test body unchanged. It proves old fixture support still exists when `skill_candidates` is absent.

- [ ] **Step 3: Replace active stage-role test with active candidate-only test**

Replace `test_legacy_stage_role_does_not_block_selection_when_skill_candidate_matches` with this full test:

```python
def test_active_skill_candidates_do_not_need_legacy_role_fields() -> None:
    selection = select_pack_candidate(
        prompt_lower="use helper for specialized cleanup",
        candidates=["primary", "helper"],
        task_type="coding",
        requested_canonical=None,
        skill_keyword_index={
            "selection": {
                "weights": {"keyword_match": 0.8, "name_match": 0.2},
                "fallback_to_first_when_score_below": 0.2,
            },
            "skills": {
                "primary": {"keywords": ["primary"]},
                "helper": {"keywords": ["helper", "cleanup"]},
            },
        },
        routing_rules={"skills": {}},
        pack={
            "id": "synthetic-pack",
            "skill_candidates": ["primary", "helper"],
            "defaults_by_task": {},
        },
        candidate_selection_config={
            "rule_positive_keyword_bonus": 0.2,
            "rule_negative_keyword_penalty": 0.25,
            "canonical_for_task_bonus": 0.12,
        },
    )

    assert selection["selected"] == "helper"
    assert selection["ranking"][0]["legacy_role"] == "skill_candidate"
    assert selection["stage_assistant_candidates"] == []
    assert "routing_role" not in selection["ranking"][0]
```

- [ ] **Step 4: Run the unit selection tests**

Run:

```powershell
python -m pytest tests/unit/test_router_contract_selection_guards.py -q
```

Expected:

```text
6 passed
```

- [ ] **Step 5: Commit selection compatibility test update**

Run:

```powershell
git add tests/unit/test_router_contract_selection_guards.py
git commit -m "test: keep legacy candidate fallback compatibility"
```

Expected: commit succeeds with one test file.

---

### Task 5: Update Pack And Route Tests Away From Old Active Fields

**Files:**
- Modify every test file listed in the File Structure section that asserts active `route_authority_candidates` or `stage_assistant_candidates`.

- [ ] **Step 1: Apply the standard active-pack assertion pattern**

For active pack tests, use this assertion pattern:

```python
self.assertEqual(EXPECTED_SKILLS, pack.get("skill_candidates"))
self.assertNotIn("route_authority_candidates", pack)
self.assertNotIn("stage_assistant_candidates", pack)
```

When the file uses `assert` instead of `self.assert*`, use:

```python
assert pack.get("skill_candidates") == EXPECTED_SKILLS
assert "route_authority_candidates" not in pack
assert "stage_assistant_candidates" not in pack
```

Replace all active-field assertions of this shape:

```python
self.assertEqual(EXPECTED_SKILLS, pack.get("route_authority_candidates"))
self.assertEqual([], pack.get("stage_assistant_candidates"))
```

with the active-pack assertion pattern above.

- [ ] **Step 2: Update deletion and absence tests**

When a deletion test loops over old role fields like this:

```python
for field in ("skill_candidates", "route_authority_candidates", "stage_assistant_candidates"):
```

replace the loop with explicit active and deleted-field checks:

```python
self.assertNotIn(deleted_skill, pack.get("skill_candidates") or [])
self.assertNotIn("route_authority_candidates", pack)
self.assertNotIn("stage_assistant_candidates", pack)
```

When the test checks for zero-route packs with:

```python
if pack.get("skill_candidates") and not pack.get("route_authority_candidates")
```

replace the assertion with:

```python
for pack in manifest["packs"]:
    self.assertTrue(pack.get("skill_candidates"), pack["id"])
    self.assertNotIn("route_authority_candidates", pack)
    self.assertNotIn("stage_assistant_candidates", pack)
```

- [ ] **Step 3: Update router result tests that inspect `legacy_role`**

In `tests/runtime_neutral/test_router_bridge.py`, active manifest candidates no longer have `route_authority_candidates`, so ranking rows should report `legacy_role == "skill_candidate"` for active packs.

Replace assertions like:

```python
self.assertEqual("route_authority", ranking_by_skill["scientific-visualization"]["legacy_role"])
```

with:

```python
self.assertEqual("skill_candidate", ranking_by_skill["scientific-visualization"]["legacy_role"])
```

Apply the same replacement to active route-result assertions for:

```text
scientific-visualization
scientific-schematics
webthinker-deep-research
flashrag-evidence
preprocessing-data-with-automated-pipelines
```

Keep assertions that `stage_assistant_candidates` in route results are empty. Runtime output cleanup is a later phase, so route result rows may still contain the empty runtime field.

- [ ] **Step 4: Search for remaining active manifest old-field assertions**

Run:

```powershell
rg -n "pack\\.get\\(\"route_authority_candidates\"|pack\\[\"route_authority_candidates\"|pack\\.get\\(\"stage_assistant_candidates\"|pack\\[\"stage_assistant_candidates\"" tests
```

Expected: no matches for active manifest assertions. Matches inside synthetic legacy fixture tests are allowed only in `tests/unit/test_router_contract_selection_guards.py`.

- [ ] **Step 5: Run updated route and pack tests**

Run:

```powershell
python -m pytest tests/unit/test_router_contract_selection_guards.py tests/runtime_neutral/test_terminology_field_simplification.py tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py tests/runtime_neutral/test_zero_route_authority_third_pass.py -q
```

Expected: all selected tests pass.

- [ ] **Step 6: Commit pack and route test updates**

Run:

```powershell
git add tests
git commit -m "test: assert active packs use skill candidates only"
```

Expected: commit succeeds with test changes only.

---

### Task 6: Full Verification And Final Cleanup

**Files:**
- Verify: `config/pack-manifest.json`
- Verify: `README.md`
- Verify: `README.zh.md`
- Verify: `docs/governance/terminology-governance.md`
- Verify: tests changed in earlier tasks

- [ ] **Step 1: Run core pytest coverage**

Run:

```powershell
python -m pytest tests/unit/test_runtime_stage_machine.py tests/unit/test_router_contract_selection_guards.py tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py tests/runtime_neutral/test_terminology_field_simplification.py tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py tests/runtime_neutral/test_zero_route_authority_third_pass.py -q
```

Expected: all tests pass. `test_runtime_stage_machine.py` proves the six governed stages remain unchanged.

- [ ] **Step 2: Run pack routing smoke**

Run:

```powershell
pwsh -NoLogo -NoProfile -File .\scripts\verify\vibe-pack-routing-smoke.ps1
```

Expected:

```text
Pack routing smoke checks passed.
```

- [ ] **Step 3: Run offline skill closure**

Run:

```powershell
pwsh -NoLogo -NoProfile -File .\scripts\verify\vibe-offline-skills-gate.ps1
```

Expected: the gate exits with code `0` and reports no missing active skill directories.

- [ ] **Step 4: Run config parity gate**

Run:

```powershell
pwsh -NoLogo -NoProfile -File .\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
```

Expected: the gate exits with code `0`. If it writes artifacts, inspect `git status --short` and include only intentional source changes in the next commit.

- [ ] **Step 5: Run whitespace check**

Run:

```powershell
git diff --check
```

Expected: no output.

- [ ] **Step 6: Confirm no old active pack fields remain**

Run:

```powershell
@'
import json
from pathlib import Path
manifest = json.loads(Path('config/pack-manifest.json').read_text(encoding='utf-8-sig'))
bad = [
    pack['id']
    for pack in manifest['packs']
    if 'route_authority_candidates' in pack or 'stage_assistant_candidates' in pack
]
print({'bad_pack_count': len(bad), 'bad_packs': bad})
raise SystemExit(1 if bad else 0)
'@ | python -
```

Expected:

```text
{'bad_pack_count': 0, 'bad_packs': []}
```

- [ ] **Step 7: Commit verification-driven cleanup if needed**

If Steps 1-6 required additional source changes, run:

```powershell
git add config README.md README.zh.md docs/governance tests
git commit -m "fix: stabilize terminology field simplification"
```

Expected: commit succeeds only if there are source changes. If there are no changes, skip this commit.

- [ ] **Step 8: Report final status**

Run:

```powershell
git status --short --branch
git log --oneline -n 6
```

Expected: worktree is clean except generated verification artifacts that are intentionally left untracked or ignored. Final report must list:

- whether active `pack-manifest.json` old fields are gone
- whether six-stage tests passed
- whether routing smoke passed
- whether offline skill closure passed
- whether config parity passed
- commit hashes created during the implementation
