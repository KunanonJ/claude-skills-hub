# AIOS Core Hard Removal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the non-self-contained AIOS role pack and all `aios-*` bundled skill directories from Vibe-Skills live routing.

**Architecture:** This is a hard removal across routing config, skill corpus, route gates, and replay fixtures. The change removes `aios-core` as a selectable pack instead of rewriting it into a new role framework; PRD/backlog/product-owner prompts must no longer select AIOS and may fall to an existing owner or confirmation. Verification is anchored by a focused runtime-neutral test plus existing route smoke, stability, OpenSpec, offline-skill, and config-parity gates.

**Tech Stack:** JSON routing configs, Python unittest/pytest, PowerShell route gates, Git-tracked bundled skill directories, generated `config/skills-lock.json`.

---

## File Map

- Create `tests/runtime_neutral/test_aios_core_hard_removal.py`: focused RED/GREEN contract for removing `aios-core`, `aios-*` skill directories, AIOS config keys, and AIOS route selections.
- Modify `config/pack-manifest.json`: delete the entire `aios-core` pack object.
- Modify `config/skill-keyword-index.json`: remove AIOS skill keyword entries.
- Modify `config/skill-routing-rules.json`: remove AIOS skill routing rules.
- Modify `config/capability-catalog.json`: remove `aios-dev`, `aios-architect`, and `aios-devops` from capability skill lists.
- Delete `bundled/skills/aios-analyst`, `bundled/skills/aios-architect`, `bundled/skills/aios-data-engineer`, `bundled/skills/aios-dev`, `bundled/skills/aios-devops`, `bundled/skills/aios-master`, `bundled/skills/aios-pm`, `bundled/skills/aios-po`, `bundled/skills/aios-qa`, `bundled/skills/aios-sm`, `bundled/skills/aios-squad-creator`, and `bundled/skills/aios-ux-design-expert`.
- Modify `scripts/verify/vibe-pack-regression-matrix.ps1`: replace the positive AIOS expectation with a blocked-pack assertion.
- Modify `scripts/verify/vibe-pack-routing-smoke.ps1`: remove `aios-core` from required pack IDs.
- Modify `scripts/verify/vibe-routing-stability-gate.ps1`: replace AIOS expected-pack route cases with blocked-pack route cases.
- Modify `scripts/verify/vibe-openspec-governance-gate.ps1`: replace the AIOS expected-pack case with a no-AIOS planning case and assert blocked pack support.
- Modify `tests/runtime_neutral/test_router_bridge.py`: add replay-fixture support for `blocked_pack` and ensure the recovery fixture can assert no AIOS route.
- Modify `tests/replay/route/recovery-wave-curated-prompts.json`: change the `prd_backlog` case from expected `aios-core` to blocked `aios-core`.
- Modify `tests/replay/route/router-contract-gate-golden.json`: update or replace the AIOS golden case after route output is regenerated.
- Modify `tests/replay/route/openclaw-runtime-core-preview.json`: update the OpenClaw preview route expectation away from AIOS.
- Create `docs/governance/aios-core-hard-removal-2026-04-29.md`: governance record for deletion rationale and verification.
- Modify `config/skills-lock.json`: refresh after deleting the bundled skill directories.

## Task 1: Focused RED Test

**Files:**
- Create: `tests/runtime_neutral/test_aios_core_hard_removal.py`

- [ ] **Step 1: Write the focused hard-removal test**

Create `tests/runtime_neutral/test_aios_core_hard_removal.py`:

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


AIOS_SKILLS = {
    "aios-analyst",
    "aios-architect",
    "aios-data-engineer",
    "aios-dev",
    "aios-devops",
    "aios-master",
    "aios-pm",
    "aios-po",
    "aios-qa",
    "aios-sm",
    "aios-squad-creator",
    "aios-ux-design-expert",
}


def load_json(relative_path: str) -> Any:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8-sig"))


def route(prompt: str, task_type: str = "planning", grade: str = "L") -> dict[str, object]:
    return route_prompt(prompt=prompt, grade=grade, task_type=task_type, repo_root=REPO_ROOT)


def selected(result: dict[str, object]) -> tuple[str, str]:
    selected_row = result.get("selected")
    assert isinstance(selected_row, dict), result
    return str(selected_row.get("pack_id") or ""), str(selected_row.get("skill") or "")


def walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        found: list[str] = []
        for item in value:
            found.extend(walk_strings(item))
        return found
    if isinstance(value, dict):
        found = []
        for key, item in value.items():
            found.append(str(key))
            found.extend(walk_strings(item))
        return found
    return []


def ranked_pack_ids(result: dict[str, object]) -> set[str]:
    ranked = result.get("ranked")
    assert isinstance(ranked, list), result
    return {
        str(row.get("pack_id") or "")
        for row in ranked
        if isinstance(row, dict)
    }


def ranked_candidate_skills(result: dict[str, object]) -> set[str]:
    ranked = result.get("ranked")
    assert isinstance(ranked, list), result
    skills: set[str] = set()
    for row in ranked:
        if not isinstance(row, dict):
            continue
        ranking = row.get("candidate_ranking")
        if isinstance(ranking, list):
            skills.update(
                str(item.get("skill") or "")
                for item in ranking
                if isinstance(item, dict)
            )
        stage_candidates = row.get("stage_assistant_candidates")
        if isinstance(stage_candidates, list):
            skills.update(
                str(item.get("skill") or "")
                for item in stage_candidates
                if isinstance(item, dict)
            )
    return skills


class AiosCoreHardRemovalTests(unittest.TestCase):
    def test_pack_manifest_has_no_aios_core_or_aios_skills(self) -> None:
        manifest = load_json("config/pack-manifest.json")
        packs = manifest["packs"]
        self.assertNotIn("aios-core", {pack["id"] for pack in packs})
        for pack in packs:
            for field in ("skill_candidates", "route_authority_candidates", "stage_assistant_candidates"):
                values = set(pack.get(field) or [])
                self.assertFalse(values & AIOS_SKILLS, (pack["id"], field, sorted(values & AIOS_SKILLS)))

    def test_bundled_aios_skill_directories_are_deleted(self) -> None:
        remaining = {
            path.name
            for path in (REPO_ROOT / "bundled" / "skills").glob("aios-*")
            if path.is_dir()
        }
        self.assertEqual(set(), remaining)

    def test_live_routing_configs_have_no_aios_skill_keys(self) -> None:
        keyword_index = load_json("config/skill-keyword-index.json")
        routing_rules = load_json("config/skill-routing-rules.json")
        capability_catalog = load_json("config/capability-catalog.json")
        self.assertFalse(set(keyword_index["skills"]) & AIOS_SKILLS)
        self.assertFalse(set(routing_rules["skills"]) & AIOS_SKILLS)
        capability_strings = set(walk_strings(capability_catalog))
        self.assertFalse(capability_strings & AIOS_SKILLS)

    def test_skills_lock_has_no_aios_skills(self) -> None:
        lock = load_json("config/skills-lock.json")
        locked = {str(row.get("name") or "") for row in lock["skills"]}
        self.assertFalse(locked & AIOS_SKILLS, sorted(locked & AIOS_SKILLS))

    def test_product_planning_prompts_do_not_select_aios(self) -> None:
        prompts = [
            "create PRD and user story backlog with quality gate",
            "输出用户故事和产品需求文档",
            "product owner style backlog prioritization and acceptance criteria",
            "draft product roadmap and PRD scope for next release",
        ]
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = route(prompt)
                pack_id, skill = selected(result)
                self.assertNotEqual("aios-core", pack_id, result)
                self.assertNotIn(skill, AIOS_SKILLS, result)
                self.assertNotIn("aios-core", ranked_pack_ids(result), result)
                self.assertFalse(ranked_candidate_skills(result) & AIOS_SKILLS, result)

    def test_aios_words_do_not_resurrect_aios_routes(self) -> None:
        prompts = [
            "aios master orchestrator should plan this project",
            "use Synkra AIOS role team for product owner and scrum master planning",
            "敏捷智能体 产品负责人 质量门禁",
        ]
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = route(prompt)
                pack_id, skill = selected(result)
                self.assertNotEqual("aios-core", pack_id, result)
                self.assertNotIn(skill, AIOS_SKILLS, result)
                self.assertNotIn("aios-core", ranked_pack_ids(result), result)
                self.assertFalse(ranked_candidate_skills(result) & AIOS_SKILLS, result)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run focused test and verify RED**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_aios_core_hard_removal.py -q
```

Expected: FAIL. The expected failures are:

- `aios-core` still exists in `config/pack-manifest.json`.
- `bundled/skills/aios-*` directories still exist.
- AIOS keys still exist in keyword/routing/capability configs.
- product-planning prompts still route to `aios-core / aios-master`.

## Task 2: Delete AIOS Pack And Skill Corpus

**Files:**
- Modify: `config/pack-manifest.json`
- Delete: `bundled/skills/aios-analyst`
- Delete: `bundled/skills/aios-architect`
- Delete: `bundled/skills/aios-data-engineer`
- Delete: `bundled/skills/aios-dev`
- Delete: `bundled/skills/aios-devops`
- Delete: `bundled/skills/aios-master`
- Delete: `bundled/skills/aios-pm`
- Delete: `bundled/skills/aios-po`
- Delete: `bundled/skills/aios-qa`
- Delete: `bundled/skills/aios-sm`
- Delete: `bundled/skills/aios-squad-creator`
- Delete: `bundled/skills/aios-ux-design-expert`

- [ ] **Step 1: Remove the `aios-core` pack from the manifest**

In `config/pack-manifest.json`, delete the first pack object whose id is `aios-core`. This is the block beginning with:

```json
{
  "id": "aios-core",
  "priority": 96,
```

and ending at its `defaults_by_task` object:

```json
"defaults_by_task": {
  "debug": "aios-master",
  "planning": "aios-master",
  "research": "aios-master",
  "coding": "aios-master",
  "review": "aios-master"
}
```

After the edit, the first pack in the manifest should be `workflow-compatibility`.

- [ ] **Step 2: Physically delete the AIOS bundled skill directories**

Run:

```powershell
git rm -r `
  bundled/skills/aios-analyst `
  bundled/skills/aios-architect `
  bundled/skills/aios-data-engineer `
  bundled/skills/aios-dev `
  bundled/skills/aios-devops `
  bundled/skills/aios-master `
  bundled/skills/aios-pm `
  bundled/skills/aios-po `
  bundled/skills/aios-qa `
  bundled/skills/aios-sm `
  bundled/skills/aios-squad-creator `
  bundled/skills/aios-ux-design-expert
```

Expected: each deleted path shows as `D` in `git status --short`.

- [ ] **Step 3: Verify manifest JSON and deleted directories**

Run:

```powershell
python -m json.tool config/pack-manifest.json > $null
git status --short -- bundled/skills/aios-analyst bundled/skills/aios-architect bundled/skills/aios-data-engineer bundled/skills/aios-dev bundled/skills/aios-devops bundled/skills/aios-master bundled/skills/aios-pm bundled/skills/aios-po bundled/skills/aios-qa bundled/skills/aios-sm bundled/skills/aios-squad-creator bundled/skills/aios-ux-design-expert
```

Expected:

```text
python -m json.tool exits 0.
All twelve AIOS skill paths are deleted in git status.
```

## Task 3: Remove AIOS Routing Config References

**Files:**
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`
- Modify: `config/capability-catalog.json`

- [ ] **Step 1: Remove AIOS keyword-index entries**

In `config/skill-keyword-index.json`, remove these keys from the top-level `skills` object:

```text
aios-master
aios-dev
aios-architect
aios-pm
aios-qa
aios-sm
aios-po
aios-analyst
```

After the edit, `figma-implement-design` should be followed directly by `research-lookup` in that area of the file.

- [ ] **Step 2: Remove AIOS routing-rule entries**

In `config/skill-routing-rules.json`, remove these keys from the top-level `skills` object:

```text
aios-master
aios-pm
aios-po
aios-sm
aios-analyst
aios-architect
aios-dev
aios-devops
aios-qa
aios-data-engineer
aios-squad-creator
aios-ux-design-expert
```

After the edit, the non-AIOS rule before `aios-master` and the non-AIOS rule after `aios-ux-design-expert` should become adjacent with valid JSON comma placement.

- [ ] **Step 3: Remove AIOS capability-catalog skill references**

In `config/capability-catalog.json`, edit the relevant `skills` arrays:

For capability `implementation_execution`, remove only `aios-dev` so the list becomes:

```json
"skills": [
  "autonomous-builder",
  "tdd-guide",
  "systematic-debugging"
]
```

For capability `architecture_design`, remove only `aios-architect` so the list becomes:

```json
"skills": [
  "architecture-patterns",
  "vibe"
]
```

For the CI/CD or DevOps capability containing `aios-devops`, remove only `aios-devops` so the list becomes:

```json
"skills": [
  "gh-fix-ci",
  "netlify-deploy",
  "vercel-deploy",
  "mcp-integration"
]
```

- [ ] **Step 4: Verify JSON config and no live AIOS config references**

Run:

```powershell
python -m json.tool config/skill-keyword-index.json > $null
python -m json.tool config/skill-routing-rules.json > $null
python -m json.tool config/capability-catalog.json > $null
rg -n '"aios-|aios-core|aios-master' config/pack-manifest.json config/skill-keyword-index.json config/skill-routing-rules.json config/capability-catalog.json
```

Expected:

```text
All three json.tool commands exit 0.
rg returns no matches for these four live routing/config files.
```

## Task 4: Update Route Tests And Gates

**Files:**
- Modify: `tests/runtime_neutral/test_router_bridge.py`
- Modify: `tests/replay/route/recovery-wave-curated-prompts.json`
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`
- Modify: `scripts/verify/vibe-pack-routing-smoke.ps1`
- Modify: `scripts/verify/vibe-routing-stability-gate.ps1`
- Modify: `scripts/verify/vibe-openspec-governance-gate.ps1`

- [ ] **Step 1: Add `blocked_pack` support to recovery fixture assertions**

In `tests/runtime_neutral/test_router_bridge.py`, update the replay-fixture assertion loop so it supports `blocked_pack`.

Replace the current expected route assertions inside `test_recovery_wave_curated_fixture_routes` with this block:

```python
                if "allowed_route_modes" in expected:
                    self.assertIn(result["route_mode"], expected["allowed_route_modes"])
                if "selected_pack" in expected:
                    self.assertEqual(expected["selected_pack"], result["selected"]["pack_id"])
                if "selected_skill" in expected:
                    self.assertEqual(expected["selected_skill"], result["selected"]["skill"])
                if "blocked_pack" in expected:
                    self.assertNotEqual(expected["blocked_pack"], result["selected"]["pack_id"])
                if "blocked_skill_prefix" in expected:
                    self.assertFalse(
                        str(result["selected"]["skill"]).startswith(expected["blocked_skill_prefix"]),
                        result["selected"],
                    )
```

- [ ] **Step 2: Change the recovery fixture PRD case to blocked AIOS**

In `tests/replay/route/recovery-wave-curated-prompts.json`, replace the `prd_backlog` expected block with:

```json
"expected": {
  "allowed_route_modes": [
    "pack_overlay",
    "confirm_required",
    "legacy_fallback"
  ],
  "blocked_pack": "aios-core",
  "blocked_skill_prefix": "aios-"
}
```

- [ ] **Step 3: Replace the pack regression AIOS positive case**

In `scripts/verify/vibe-pack-regression-matrix.ps1`, replace:

```powershell
[pscustomobject]@{ Name = "aios-core planning"; Prompt = "create PRD and user story backlog with quality gate"; Grade = "L"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = "aios-core"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
```

with:

```powershell
[pscustomobject]@{ Name = "aios-core removed planning"; Prompt = "create PRD and user story backlog with quality gate"; Grade = "L"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "aios-core"; BlockedSkill = "aios-master"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
```

- [ ] **Step 4: Remove `aios-core` from required pack smoke list**

In `scripts/verify/vibe-pack-routing-smoke.ps1`, remove this entry from `$requiredPackIds`:

```powershell
"aios-core",
```

Do not change the other required pack IDs.

- [ ] **Step 5: Replace routing stability AIOS cases with blocked-pack cases**

In `scripts/verify/vibe-routing-stability-gate.ps1`, replace the five `aios-core-planning-*` cases with:

```powershell
    (New-TestCase -Group "aios-core-removed-planning" -Prompt "create PRD and backlog with user stories" -Grade "L" -TaskType "planning" -BlockedPack "aios-core"),
    (New-TestCase -Group "aios-core-removed-planning" -Prompt "输出用户故事和产品需求文档" -Grade "L" -TaskType "planning" -BlockedPack "aios-core"),
    (New-TestCase -Group "aios-core-removed-planning" -Prompt "draft product roadmap and PRD scope for next release" -Grade "L" -TaskType "planning" -BlockedPack "aios-core"),
    (New-TestCase -Group "aios-core-removed-product-owner" -Prompt "product owner style backlog prioritization and acceptance criteria" -Grade "L" -TaskType "planning" -BlockedPack "aios-core"),
    (New-TestCase -Group "aios-core-removed-product-owner" -Prompt "按PO视角做backlog优先级排序和验收标准" -Grade "L" -TaskType "planning" -BlockedPack "aios-core"),
```

- [ ] **Step 6: Add blocked-pack support to OpenSpec governance gate**

In `scripts/verify/vibe-openspec-governance-gate.ps1`, replace the AIOS case:

```powershell
[pscustomobject]@{
    Name = "L planning aios-core"
    Prompt = "create PRD and user story backlog with quality gate"
    Grade = "L"
    TaskType = "planning"
    RequestedSkill = $null
    ExpectedPack = "aios-core"
    ExpectedProfile = "full"
    ExpectedEnforcement = "required"
},
```

with:

```powershell
[pscustomobject]@{
    Name = "L planning aios-core removed"
    Prompt = "create PRD and user story backlog with quality gate"
    Grade = "L"
    TaskType = "planning"
    RequestedSkill = $null
    ExpectedPack = $null
    BlockedPack = "aios-core"
    ExpectedProfile = "full"
    ExpectedEnforcement = "required"
},
```

Then add this assertion immediately after the existing `if ($case.ExpectedPack) { ... }` block:

```powershell
        if ($case.BlockedPack) {
            $results += Assert-True -Condition ($route.selected.pack_id -ne $case.BlockedPack) -Message "[$($case.Name)] blocked pack not selected ($($case.BlockedPack))"
        }
```

- [ ] **Step 7: Run route tests and gates for this task**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_aios_core_hard_removal.py tests/runtime_neutral/test_router_bridge.py -q
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-routing-stability-gate.ps1
.\scripts\verify\vibe-openspec-governance-gate.ps1
```

Expected:

```text
Focused pytest and router bridge tests exit 0.
Pack regression matrix exits 0.
Pack routing smoke exits 0.
Routing stability gate exits 0.
OpenSpec governance gate exits 0.
```

## Task 5: Update Replay Fixtures And Governance Note

**Files:**
- Modify: `tests/replay/route/router-contract-gate-golden.json`
- Modify: `tests/replay/route/openclaw-runtime-core-preview.json`
- Create: `docs/governance/aios-core-hard-removal-2026-04-29.md`

- [ ] **Step 1: Refresh router contract golden AIOS case**

Run the current route for the `explicit-requested-skill` case:

```powershell
.\scripts\router\resolve-pack-route.ps1 -Prompt "please help with roadmap" -Grade "L" -TaskType "planning" -RequestedSkill "writing-plans" | ConvertFrom-Json | ConvertTo-Json -Depth 12
```

In `tests/replay/route/router-contract-gate-golden.json`, update the `explicit-requested-skill` expected block so it matches that output and no longer contains:

```text
selected_pack: aios-core
selected_skill: aios-master
```

The updated expected block must preserve the same fields the gate compares:

```json
"route_mode": "<actual route_mode from command>",
"route_reason": "<actual route_reason from command>",
"selected_pack": "<actual selected.pack_id from command>",
"selected_skill": "<actual selected.skill from command>",
"confidence": <actual confidence from command>,
"top1_top2_gap": <actual top1_top2_gap from command>,
"candidate_signal": <actual candidate_signal from command>
```

- [ ] **Step 2: Refresh OpenClaw preview fixture first case**

Run:

```powershell
.\scripts\router\resolve-pack-route.ps1 -Prompt "Install VibeSkills for OpenClaw with truthful runtime-core-preview boundaries and no overclaim." -Grade "M" -TaskType "planning" | ConvertFrom-Json | ConvertTo-Json -Depth 12
```

In `tests/replay/route/openclaw-runtime-core-preview.json`, update `openclaw_preview_install_story.expected.selected_pack` and `openclaw_preview_install_story.expected.selected_skill` to the actual selected route from the command. Preserve its existing `required_disclosures` array.

- [ ] **Step 3: Verify replay fixtures have no AIOS expectations**

Run:

```powershell
rg -n '"aios-core"|"aios-master"|selected_pack.*aios|selected_skill.*aios' tests/replay/route/router-contract-gate-golden.json tests/replay/route/recovery-wave-curated-prompts.json tests/replay/route/openclaw-runtime-core-preview.json
```

Expected: no matches.

- [ ] **Step 4: Write governance note**

Create `docs/governance/aios-core-hard-removal-2026-04-29.md`:

```markdown
# AIOS Core Hard Removal

Date: 2026-04-29

## Decision

`aios-core` was removed from live Vibe-Skills routing.

This was a hard removal because the AIOS bundled skills were thin activator wrappers, not self-contained skills. They pointed to `.aios-core/development/agents/*.md` or `.codex/agents/*.md`, but those source paths are absent in this checkout.

## Deleted Skill Directories

- `bundled/skills/aios-analyst`
- `bundled/skills/aios-architect`
- `bundled/skills/aios-data-engineer`
- `bundled/skills/aios-dev`
- `bundled/skills/aios-devops`
- `bundled/skills/aios-master`
- `bundled/skills/aios-pm`
- `bundled/skills/aios-po`
- `bundled/skills/aios-qa`
- `bundled/skills/aios-sm`
- `bundled/skills/aios-squad-creator`
- `bundled/skills/aios-ux-design-expert`

## Removed Routing Surfaces

| Surface | Before | After |
| --- | --- | --- |
| Pack | `aios-core` | removed |
| `skill_candidates` | 12 AIOS role skills | none |
| `route_authority_candidates` | `aios-master` | none |
| `stage_assistant_candidates` | 11 AIOS role skills | none |
| defaults | all task types to `aios-master` | none |

## Replacement Behavior

PRD, backlog, user-story, product-owner, scrum-master, and quality-gate prompts no longer route to an AIOS role team.

If an existing non-AIOS pack clearly owns the prompt, that pack may be selected. If no pack owns it clearly, confirmation is preferred over reintroducing AIOS as a catch-all.

## Simplified Routing Contract

The resulting model remains:

```text
candidate -> selected -> used / unused
```

AIOS no longer contributes primary, secondary, stage-assistant, role-team, or consultation-style routing surfaces.

## Verification

```powershell
python -m pytest tests/runtime_neutral/test_aios_core_hard_removal.py tests/runtime_neutral/test_router_bridge.py -q
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-routing-stability-gate.ps1
.\scripts\verify\vibe-openspec-governance-gate.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```
```

## Task 6: Lock Refresh, Full Verification, And Commits

**Files:**
- Modify: `config/skills-lock.json`

- [ ] **Step 1: Refresh skills lock**

Run:

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected: exits 0 and updates `config/skills-lock.json` so the twelve AIOS skills are absent and `skill_count` decreases by 12.

- [ ] **Step 2: Run full verification**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_aios_core_hard_removal.py tests/runtime_neutral/test_router_bridge.py -q
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-routing-stability-gate.ps1
.\scripts\verify\vibe-openspec-governance-gate.ps1
.\scripts\verify\vibe-router-contract-gate.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

Expected:

```text
pytest exits 0.
All PowerShell route/gate scripts exit 0.
vibe-router-contract-gate exits 0 after the golden fixture is refreshed.
offline skills gate reports PASS.
config parity gate reports PASS.
git diff --check exits 0.
```

- [ ] **Step 3: Inspect intended diff**

Run:

```powershell
git status --short --branch
git diff --stat
rg -n '"aios-|aios-core|aios-master' config/pack-manifest.json config/skill-keyword-index.json config/skill-routing-rules.json config/capability-catalog.json tests/replay/route scripts/verify tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_aios_core_hard_removal.py
```

Expected:

```text
Status shows only intended config, deleted bundled/skills/aios-* directories, tests, scripts, replay fixtures, governance note, and skills-lock changes.
rg may show only blocked-pack assertions or human-readable governance/design references; it must not show live positive route expectations for AIOS.
```

- [ ] **Step 4: Commit implementation without lock refresh if lock diff is large**

If `config/skills-lock.json` contains deleted AIOS skill entries plus generated metadata, include it in the implementation commit because physical directory deletion changes the lock content.

Run:

```powershell
git add config/pack-manifest.json `
  config/skill-keyword-index.json `
  config/skill-routing-rules.json `
  config/capability-catalog.json `
  config/skills-lock.json `
  tests/runtime_neutral/test_aios_core_hard_removal.py `
  tests/runtime_neutral/test_router_bridge.py `
  tests/replay/route/recovery-wave-curated-prompts.json `
  tests/replay/route/router-contract-gate-golden.json `
  tests/replay/route/openclaw-runtime-core-preview.json `
  scripts/verify/vibe-pack-regression-matrix.ps1 `
  scripts/verify/vibe-pack-routing-smoke.ps1 `
  scripts/verify/vibe-routing-stability-gate.ps1 `
  scripts/verify/vibe-openspec-governance-gate.ps1 `
  docs/governance/aios-core-hard-removal-2026-04-29.md `
  bundled/skills/aios-analyst `
  bundled/skills/aios-architect `
  bundled/skills/aios-data-engineer `
  bundled/skills/aios-dev `
  bundled/skills/aios-devops `
  bundled/skills/aios-master `
  bundled/skills/aios-pm `
  bundled/skills/aios-po `
  bundled/skills/aios-qa `
  bundled/skills/aios-sm `
  bundled/skills/aios-squad-creator `
  bundled/skills/aios-ux-design-expert
git commit -m "fix: remove aios core routing pack"
```

- [ ] **Step 5: Final status check**

Run:

```powershell
git status --short --branch
git log -4 --oneline
```

Expected:

```text
Working tree is clean.
The implementation commit is visible above the design and previous cleanup commits.
```

## Self-Review Notes

- Spec coverage: The plan removes `aios-core` from live routing, deletes all twelve AIOS skill directories, removes AIOS config references, updates replay/gate expectations, refreshes `skills-lock.json`, and records governance.
- Scope control: The plan does not modify `data-ml`, `code-quality`, `ruc-nlpir-augmentation`, or any unrelated pack.
- Runtime boundary: The plan does not change canonical `$vibe` six-stage launch or runtime stage behavior.
- Simplified routing: The plan removes AIOS primary/secondary/stage-assistant role-team semantics instead of rewriting them.
- Deletion boundary: Physical deletion is limited to the twelve AIOS directories that only contain `SKILL.md` wrappers and no assets.
