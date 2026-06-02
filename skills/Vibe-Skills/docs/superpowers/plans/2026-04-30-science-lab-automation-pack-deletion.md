# Science Lab Automation Pack Deletion Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hard-delete the cold `science-lab-automation` pack and its six bundled skills from active Vibe-Skills routing.

**Architecture:** Convert the existing pack-consolidation tests into hard-removal tests first, then remove the pack, skill metadata, and bundled directories. Update route probes and governance evidence so Opentrons, PyLabRobot, protocols.io, Benchling, LabArchives, and Ginkgo Cloud Lab prompts prove the deleted pack is absent rather than selecting a replacement owner.

**Tech Stack:** Python `unittest` runtime-neutral router tests, PowerShell verification scripts, JSON routing config, bundled skill directory tree, Vibe-Skills governance docs.

---

## File Structure

Implementation touches only the deleted pack, its active routing surfaces, and verification surfaces.

| File or directory | Responsibility in this pass |
| --- | --- |
| `tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py` | Focused hard-removal regression tests for deleted pack, deleted skill ids, deleted directories, and blocked route prompts. |
| `config/pack-manifest.json` | Remove the `science-lab-automation` pack object. |
| `config/skill-keyword-index.json` | Remove six deleted skill keyword entries. |
| `config/skill-routing-rules.json` | Remove six deleted skill routing-rule entries. |
| `config/skills-lock.json` | Regenerate after physical directory deletion. |
| `bundled/skills/opentrons-integration` | Delete. |
| `bundled/skills/pylabrobot` | Delete. |
| `bundled/skills/protocolsio-integration` | Delete. |
| `bundled/skills/benchling-integration` | Delete. |
| `bundled/skills/labarchive-integration` | Delete. |
| `bundled/skills/ginkgo-cloud-lab` | Delete. |
| `scripts/verify/probe-scientific-packs.ps1` | Replace positive lab-automation route probes with deleted-pack blocked probes. |
| `scripts/verify/vibe-skill-index-routing-audit.ps1` | Replace positive lab-automation route audit cases with deleted-pack blocked cases. |
| `scripts/verify/vibe-pack-regression-matrix.ps1` | Add explicit deleted-pack blocked cases for all six old product/tool prompts. |
| `scripts/verify/vibe-pack-routing-smoke.ps1` | Add the six deleted skills to `$deletedSkillIds` so stale directories and config entries fail smoke. |
| `tests/runtime_neutral/test_zero_route_authority_third_pass.py` | Keep passing without adding `science-lab-automation`; no target owner should reference deleted skills. Modify only if stale assertions appear. |
| `docs/governance/science-lab-automation-pack-deletion-2026-04-30.md` | Record before/after counts, deleted directories, route migration, verification, and non-introduction of helper/advisory semantics. |

Deleted skill ids:

```text
opentrons-integration
pylabrobot
protocolsio-integration
benchling-integration
labarchive-integration
ginkgo-cloud-lab
```

Do not delete or reroute:

```text
latchbio-integration
```

---

### Task 1: Add Focused Hard-Removal Tests

**Files:**
- Modify: `tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py`

- [ ] **Step 1: Replace the focused test file with hard-removal assertions**

Use `apply_patch` to replace `tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py` with this content:

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


DELETED_PACK = "science-lab-automation"
DELETED_SKILLS = [
    "opentrons-integration",
    "pylabrobot",
    "protocolsio-integration",
    "benchling-integration",
    "labarchive-integration",
    "ginkgo-cloud-lab",
]

OUT_OF_SCOPE_SKILLS = [
    "latchbio-integration",
]


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def route(prompt: str, task_type: str = "research", grade: str = "L") -> dict[str, object]:
    return route_prompt(
        prompt=prompt,
        grade=grade,
        task_type=task_type,
        repo_root=REPO_ROOT,
    )


def selected(result: dict[str, object]) -> tuple[str, str]:
    selected_row = result.get("selected")
    assert isinstance(selected_row, dict), result
    return str(selected_row.get("pack_id") or ""), str(selected_row.get("skill") or "")


def ranked_summary(result: dict[str, object]) -> list[tuple[str, str, float, str]]:
    ranked = result.get("ranked")
    assert isinstance(ranked, list), result
    rows: list[tuple[str, str, float, str]] = []
    for row in ranked[:8]:
        assert isinstance(row, dict), row
        rows.append(
            (
                str(row.get("pack_id") or ""),
                str(row.get("selected_candidate") or ""),
                float(row.get("score") or 0.0),
                str(row.get("candidate_selection_reason") or ""),
            )
        )
    return rows


def manifest_pack_ids() -> set[str]:
    manifest = load_json(REPO_ROOT / "config" / "pack-manifest.json")
    packs = manifest.get("packs")
    assert isinstance(packs, list), manifest
    return {str(pack.get("id")) for pack in packs if isinstance(pack, dict)}


def manifest_skill_ids() -> set[str]:
    manifest = load_json(REPO_ROOT / "config" / "pack-manifest.json")
    packs = manifest.get("packs")
    assert isinstance(packs, list), manifest
    skill_ids: set[str] = set()
    for pack in packs:
        assert isinstance(pack, dict), pack
        for field in ("skill_candidates", "route_authority_candidates", "stage_assistant_candidates"):
            values = pack.get(field) or []
            assert isinstance(values, list), pack
            skill_ids.update(str(value) for value in values)
        defaults = pack.get("defaults_by_task") or {}
        assert isinstance(defaults, dict), pack
        skill_ids.update(str(value) for value in defaults.values())
    return skill_ids


def skill_index_ids() -> set[str]:
    payload = load_json(REPO_ROOT / "config" / "skill-keyword-index.json")
    skills = payload.get("skills")
    assert isinstance(skills, dict), payload
    return {str(key) for key in skills.keys()}


def routing_rule_ids() -> set[str]:
    payload = load_json(REPO_ROOT / "config" / "skill-routing-rules.json")
    skills = payload.get("skills")
    assert isinstance(skills, dict), payload
    return {str(key) for key in skills.keys()}


def lock_skill_ids() -> set[str]:
    payload = load_json(REPO_ROOT / "config" / "skills-lock.json")
    skills = payload.get("skills")
    assert isinstance(skills, list), payload
    return {str(row.get("name")) for row in skills if isinstance(row, dict)}


class ScienceLabAutomationPackDeletionTests(unittest.TestCase):
    def assert_deleted_pack_not_selected(
        self,
        prompt: str,
        *,
        task_type: str = "research",
        grade: str = "L",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        pack_id, skill_id = selected(result)
        self.assertNotEqual(DELETED_PACK, pack_id, ranked_summary(result))
        self.assertNotIn(skill_id, DELETED_SKILLS, ranked_summary(result))

    def test_pack_manifest_removes_deleted_pack(self) -> None:
        self.assertNotIn(DELETED_PACK, manifest_pack_ids())

    def test_deleted_skills_removed_from_manifest_surfaces(self) -> None:
        remaining_manifest_skills = manifest_skill_ids()
        for skill_id in DELETED_SKILLS:
            with self.subTest(skill_id=skill_id):
                self.assertNotIn(skill_id, remaining_manifest_skills)

    def test_deleted_skills_removed_from_keyword_index_and_routing_rules(self) -> None:
        keyword_ids = skill_index_ids()
        rule_ids = routing_rule_ids()
        for skill_id in DELETED_SKILLS:
            with self.subTest(skill_id=skill_id):
                self.assertNotIn(skill_id, keyword_ids)
                self.assertNotIn(skill_id, rule_ids)

    def test_deleted_skills_removed_from_skills_lock(self) -> None:
        lock_ids = lock_skill_ids()
        for skill_id in DELETED_SKILLS:
            with self.subTest(skill_id=skill_id):
                self.assertNotIn(skill_id, lock_ids)

    def test_deleted_skill_directories_are_absent(self) -> None:
        for skill_id in DELETED_SKILLS:
            with self.subTest(skill_id=skill_id):
                self.assertFalse((REPO_ROOT / "bundled" / "skills" / skill_id).exists())

    def test_out_of_scope_latchbio_is_not_deleted_by_this_pass(self) -> None:
        for skill_id in OUT_OF_SCOPE_SKILLS:
            with self.subTest(skill_id=skill_id):
                self.assertTrue((REPO_ROOT / "bundled" / "skills" / skill_id / "SKILL.md").is_file())

    def test_deleted_product_prompts_do_not_route_to_deleted_pack(self) -> None:
        cases = [
            ("写一个 Opentrons OT-2 protocol：96孔板分液 + 混匀，输出可运行脚本", "coding", "M"),
            ("用 Opentrons Flex 和 thermocycler module 写一个 PCR setup protocol", "coding", "M"),
            ("用 PyLabRobot 控制 Hamilton 和 Tecan 液体处理机器人，统一调度 plate reader", "coding", "M"),
            ("在 protocols.io 查找 PCR protocol，并总结关键步骤与关键试剂", "research", "M"),
            ("用 protocols.io API 创建并发布一个实验 protocol，包含 workspace 和文件附件", "coding", "M"),
            ("查询 Benchling registry 里的 DNA sequence 和 inventory containers，并导出样品表", "coding", "M"),
            ("备份 LabArchives notebook，导出 entries、attachments 和 JSON metadata", "coding", "M"),
            ("在 Ginkgo Cloud Lab / cloud.ginkgo.bio 准备下单输入并估算 protocol pricing", "planning", "M"),
        ]
        for prompt, task_type, grade in cases:
            with self.subTest(prompt=prompt):
                self.assert_deleted_pack_not_selected(prompt, task_type=task_type, grade=grade)

    def test_existing_negative_boundaries_still_do_not_route_to_deleted_pack(self) -> None:
        cases = [
            ("用 LatchBio / Latch SDK 部署 Nextflow RNA-seq workflow，管理 LatchFile 和 LatchDir", "coding", "M"),
            ("帮我整理电子实验记录 ELN 模板，不指定 Benchling 或 LabArchives", "planning", "M"),
            ("把实验图片和 CSV 附件整理到实验记录里，不使用 LabArchives 或 Benchling", "planning", "M"),
            ("写一个普通 wet-lab protocol 的 Markdown 文档，不使用 protocols.io 或机器人", "planning", "M"),
        ]
        for prompt, task_type, grade in cases:
            with self.subTest(prompt=prompt):
                self.assert_deleted_pack_not_selected(prompt, task_type=task_type, grade=grade)

    def test_pubmed_methods_still_route_to_literature_owner(self) -> None:
        result = route("在 PubMed 检索 wet-lab methods papers 并导出 BibTeX", task_type="research", grade="M")
        self.assertEqual(("science-literature-citations", "pubmed-database"), selected(result), ranked_summary(result))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify it fails before implementation**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py -q
```

Expected: FAIL. At least these assertions should fail before implementation:

```text
science-lab-automation is still in pack-manifest.json
opentrons-integration directory still exists
deleted product prompts still select science-lab-automation
```

Do not commit after this failing step.

---

### Task 2: Remove Pack, Skill Metadata, And Bundled Directories

**Files:**
- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`
- Modify: `config/skills-lock.json`
- Delete: `bundled/skills/opentrons-integration`
- Delete: `bundled/skills/pylabrobot`
- Delete: `bundled/skills/protocolsio-integration`
- Delete: `bundled/skills/benchling-integration`
- Delete: `bundled/skills/labarchive-integration`
- Delete: `bundled/skills/ginkgo-cloud-lab`

- [ ] **Step 1: Confirm deletion targets resolve inside `bundled/skills`**

Run:

```powershell
$repoRoot = (Resolve-Path .).Path
$skillsRoot = (Resolve-Path 'bundled\skills').Path
$deletedSkills = @(
  'opentrons-integration',
  'pylabrobot',
  'protocolsio-integration',
  'benchling-integration',
  'labarchive-integration',
  'ginkgo-cloud-lab'
)
foreach ($skill in $deletedSkills) {
  $target = Resolve-Path -LiteralPath (Join-Path $skillsRoot $skill)
  if (-not $target.Path.StartsWith($skillsRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to delete outside bundled skills: $($target.Path)"
  }
  Write-Host "delete target OK: $($target.Path)"
}
```

Expected: six `delete target OK` lines, all under `F:\vibe\Vibe-Skills\bundled\skills`.

- [ ] **Step 2: Remove the deleted pack and skill entries from config JSON**

Use structured JSON editing or precise `apply_patch` edits. The resulting config state must satisfy these invariants:

```text
config/pack-manifest.json:
- no pack object with id == "science-lab-automation"
- no skill_candidates / route_authority_candidates / stage_assistant_candidates / defaults_by_task value equals any deleted skill id

config/skill-keyword-index.json:
- no key under skills equals any deleted skill id

config/skill-routing-rules.json:
- no key under skills equals any deleted skill id
```

After editing, run this audit:

```powershell
$deletedPack = 'science-lab-automation'
$deletedSkills = @(
  'opentrons-integration',
  'pylabrobot',
  'protocolsio-integration',
  'benchling-integration',
  'labarchive-integration',
  'ginkgo-cloud-lab'
)
$manifest = Get-Content -LiteralPath 'config\pack-manifest.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$keyword = Get-Content -LiteralPath 'config\skill-keyword-index.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$rules = Get-Content -LiteralPath 'config\skill-routing-rules.json' -Raw -Encoding UTF8 | ConvertFrom-Json
if (@($manifest.packs | Where-Object { $_.id -eq $deletedPack }).Count -ne 0) { throw "deleted pack still present" }
$manifestText = Get-Content -LiteralPath 'config\pack-manifest.json' -Raw -Encoding UTF8
foreach ($skill in $deletedSkills) {
  if ($manifestText -match [regex]::Escape($skill)) { throw "deleted skill still in manifest: $skill" }
  if ($keyword.skills.PSObject.Properties.Name -contains $skill) { throw "deleted skill still in keyword index: $skill" }
  if ($rules.skills.PSObject.Properties.Name -contains $skill) { throw "deleted skill still in routing rules: $skill" }
}
Write-Host '[PASS] deleted pack and skill config entries removed'
```

Expected:

```text
[PASS] deleted pack and skill config entries removed
```

- [ ] **Step 3: Delete the six bundled skill directories safely**

Run:

```powershell
$skillsRoot = (Resolve-Path 'bundled\skills').Path
$deletedSkills = @(
  'opentrons-integration',
  'pylabrobot',
  'protocolsio-integration',
  'benchling-integration',
  'labarchive-integration',
  'ginkgo-cloud-lab'
)
foreach ($skill in $deletedSkills) {
  $targetPath = Join-Path $skillsRoot $skill
  $resolved = Resolve-Path -LiteralPath $targetPath
  if (-not $resolved.Path.StartsWith($skillsRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to delete outside bundled skills: $($resolved.Path)"
  }
  Remove-Item -LiteralPath $resolved.Path -Recurse -Force
  Write-Host "deleted: $skill"
}
```

Expected: six `deleted: <skill>` lines.

- [ ] **Step 4: Regenerate `config/skills-lock.json`**

Run:

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected: the script prints the generated lock path and a skill count six lower than before this deletion pass.

- [ ] **Step 5: Run focused test and commit config plus directory deletion**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py -q
```

Expected:

```text
passed
```

Then inspect and commit only intended files:

```powershell
git status --short
git add config/pack-manifest.json config/skill-keyword-index.json config/skill-routing-rules.json config/skills-lock.json tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py bundled/skills/opentrons-integration bundled/skills/pylabrobot bundled/skills/protocolsio-integration bundled/skills/benchling-integration bundled/skills/labarchive-integration bundled/skills/ginkgo-cloud-lab
git commit -m "fix: remove science lab automation pack"
```

Expected: commit includes the hard-removal test, three config JSON edits, refreshed lock, and six deleted skill directories.

---

### Task 3: Update Route Probes And Smoke Gates

**Files:**
- Modify: `scripts/verify/probe-scientific-packs.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`
- Modify: `scripts/verify/vibe-pack-routing-smoke.ps1`

- [ ] **Step 1: Replace positive scientific probe cases with deleted-pack blocked cases**

In `scripts/verify/probe-scientific-packs.ps1`, replace the current `# science-lab-automation` block with blocked cases like these:

```powershell
    # deleted science-lab-automation regressions
    [pscustomobject]@{ name = "deleted_lab_opentrons_ot2_blocked"; group = "deleted-science-lab-automation"; prompt = "/vibe 写一个 Opentrons OT-2 protocol：96孔板分液 + 混匀，输出可运行脚本"; grade = "M"; task_type = "coding"; expected_pack = $null; expected_skill = $null; blocked_pack = "science-lab-automation"; blocked_skill = "opentrons-integration"; requested_skill = $null },
    [pscustomobject]@{ name = "deleted_lab_opentrons_flex_blocked"; group = "deleted-science-lab-automation"; prompt = "/vibe 用 Opentrons Flex 和 thermocycler module 写一个 PCR setup protocol"; grade = "M"; task_type = "coding"; expected_pack = $null; expected_skill = $null; blocked_pack = "science-lab-automation"; blocked_skill = "opentrons-integration"; requested_skill = $null },
    [pscustomobject]@{ name = "deleted_lab_pylabrobot_blocked"; group = "deleted-science-lab-automation"; prompt = "/vibe 用 PyLabRobot 控制 Hamilton 和 Tecan 液体处理机器人，统一调度 plate reader"; grade = "M"; task_type = "coding"; expected_pack = $null; expected_skill = $null; blocked_pack = "science-lab-automation"; blocked_skill = "pylabrobot"; requested_skill = $null },
    [pscustomobject]@{ name = "deleted_lab_protocolsio_blocked"; group = "deleted-science-lab-automation"; prompt = "/vibe 用 protocols.io API 创建并发布一个实验 protocol，包含 workspace 和文件附件"; grade = "M"; task_type = "coding"; expected_pack = $null; expected_skill = $null; blocked_pack = "science-lab-automation"; blocked_skill = "protocolsio-integration"; requested_skill = $null },
    [pscustomobject]@{ name = "deleted_lab_benchling_blocked"; group = "deleted-science-lab-automation"; prompt = "/vibe 查询 Benchling registry 里的 DNA sequence 和 inventory containers，并导出样品表"; grade = "M"; task_type = "coding"; expected_pack = $null; expected_skill = $null; blocked_pack = "science-lab-automation"; blocked_skill = "benchling-integration"; requested_skill = $null },
    [pscustomobject]@{ name = "deleted_lab_labarchives_blocked"; group = "deleted-science-lab-automation"; prompt = "/vibe 备份 LabArchives notebook，导出 entries、attachments 和 JSON metadata"; grade = "M"; task_type = "coding"; expected_pack = $null; expected_skill = $null; blocked_pack = "science-lab-automation"; blocked_skill = "labarchive-integration"; requested_skill = $null },
    [pscustomobject]@{ name = "deleted_lab_ginkgo_blocked"; group = "deleted-science-lab-automation"; prompt = "/vibe 在 Ginkgo Cloud Lab / cloud.ginkgo.bio 准备下单输入并估算 protocol pricing"; grade = "M"; task_type = "planning"; expected_pack = $null; expected_skill = $null; blocked_pack = "science-lab-automation"; blocked_skill = "ginkgo-cloud-lab"; requested_skill = $null },
    [pscustomobject]@{ name = "deleted_lab_generic_markdown_blocked"; group = "deleted-science-lab-automation"; prompt = "/vibe 写一个普通 wet-lab protocol 的 Markdown 文档，不使用 protocols.io 或机器人"; grade = "M"; task_type = "planning"; expected_pack = $null; expected_skill = $null; blocked_pack = "science-lab-automation"; requested_skill = $null },
```

Run:

```powershell
.\scripts\verify\probe-scientific-packs.ps1
```

Expected: completed with zero failed assertions.

- [ ] **Step 2: Replace positive skill-index audit cases**

In `scripts/verify/vibe-skill-index-routing-audit.ps1`, replace these old positive cases:

```text
lab automation opentrons ot2
lab automation pylabrobot hamilton
lab automation protocolsio publish
lab automation benchling registry
lab automation labarchives backup
lab automation ginkgo cloud lab
```

with blocked-pack cases using the same prompts and these blocked skills:

```text
opentrons-integration
pylabrobot
protocolsio-integration
benchling-integration
labarchive-integration
ginkgo-cloud-lab
```

Each new case must have:

```powershell
ExpectedPack = $null
BlockedPack = "science-lab-automation"
BlockedSkill = "<deleted skill id>"
AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback")
```

Run:

```powershell
.\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected: completed with zero failed assertions.

- [ ] **Step 3: Expand pack regression matrix deleted-pack cases**

In `scripts/verify/vibe-pack-regression-matrix.ps1`, keep the existing three generic lab blocked cases and add explicit deleted product/tool cases:

```powershell
[pscustomobject]@{ Name = "deleted lab automation opentrons ot2"; Prompt = "写一个 Opentrons OT-2 protocol：96孔板分液 + 混匀，输出可运行脚本"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "science-lab-automation"; BlockedSkill = "opentrons-integration"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
[pscustomobject]@{ Name = "deleted lab automation pylabrobot"; Prompt = "用 PyLabRobot 控制 Hamilton 和 Tecan 液体处理机器人"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "science-lab-automation"; BlockedSkill = "pylabrobot"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
[pscustomobject]@{ Name = "deleted lab automation protocolsio"; Prompt = "用 protocols.io API 创建并发布一个实验 protocol"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "science-lab-automation"; BlockedSkill = "protocolsio-integration"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
[pscustomobject]@{ Name = "deleted lab automation benchling"; Prompt = "查询 Benchling registry 里的 DNA sequence 和 inventory containers"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "science-lab-automation"; BlockedSkill = "benchling-integration"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
[pscustomobject]@{ Name = "deleted lab automation labarchives"; Prompt = "备份 LabArchives notebook，导出 entries 和 attachments"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "science-lab-automation"; BlockedSkill = "labarchive-integration"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
[pscustomobject]@{ Name = "deleted lab automation ginkgo"; Prompt = "在 Ginkgo Cloud Lab / cloud.ginkgo.bio 准备下单输入"; Grade = "M"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "science-lab-automation"; BlockedSkill = "ginkgo-cloud-lab"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
```

Run:

```powershell
.\scripts\verify\vibe-pack-regression-matrix.ps1
```

Expected: completed with zero failed assertions.

- [ ] **Step 4: Add the six deleted skills to routing smoke's deleted list**

In `scripts/verify/vibe-pack-routing-smoke.ps1`, update `$deletedSkillIds` to include the previous deleted skills plus the six lab automation skills:

```powershell
$deletedSkillIds = @(
    "modal",
    "modal-labs",
    "qiskit",
    "cirq",
    "pennylane",
    "qutip",
    "opentrons-integration",
    "pylabrobot",
    "protocolsio-integration",
    "benchling-integration",
    "labarchive-integration",
    "ginkgo-cloud-lab"
)
```

Run:

```powershell
.\scripts\verify\vibe-pack-routing-smoke.ps1
```

Expected: completed with zero failed assertions and six new deleted-skill absence checks passing.

- [ ] **Step 5: Commit verification script updates**

Run:

```powershell
git status --short
git add scripts/verify/probe-scientific-packs.ps1 scripts/verify/vibe-skill-index-routing-audit.ps1 scripts/verify/vibe-pack-regression-matrix.ps1 scripts/verify/vibe-pack-routing-smoke.ps1
git commit -m "test: update lab automation deletion route probes"
```

Expected: commit contains only verification script changes.

---

### Task 4: Add Governance Evidence

**Files:**
- Create: `docs/governance/science-lab-automation-pack-deletion-2026-04-30.md`

- [ ] **Step 1: Create the governance note**

Create `docs/governance/science-lab-automation-pack-deletion-2026-04-30.md` with this content:

```markdown
# Science Lab Automation Pack Deletion

Date: 2026-04-30

## Decision

`science-lab-automation` is removed from the active Vibe-Skills routing surface.

This is a cold-pack hard removal. It is not a boundary narrowing pass and does not create a replacement explicit-only, helper, advisory, consultation, primary/secondary, or stage-assistant route.

The public six-stage Vibe runtime remains unchanged:

```text
skeleton_check -> deep_interview -> requirement_doc -> xl_plan -> plan_execute -> phase_cleanup
```

The skill usage model remains:

```text
candidate skill -> selected skill -> used / unused
```

## Before / After

| Surface | Before | After |
| --- | ---: | ---: |
| `science-lab-automation.skill_candidates` | 6 | 0, pack removed |
| `science-lab-automation.route_authority_candidates` | 6 | 0, pack removed |
| `science-lab-automation.stage_assistant_candidates` | 0 | 0, pack removed |
| deleted bundled skill directories | 0 | 6 |

## Deleted Skill Directories

| Skill id | Reason |
| --- | --- |
| `opentrons-integration` | Cold Opentrons OT-2/Flex product/API surface. |
| `pylabrobot` | Cold multi-vendor lab robot framework surface. |
| `protocolsio-integration` | Product-specific protocols.io API surface rather than a core expert role. |
| `benchling-integration` | Benchling SaaS/ELN/registry integration surface rather than core routing. |
| `labarchive-integration` | LabArchives ELN integration surface rather than core routing. |
| `ginkgo-cloud-lab` | Cold cloud-lab ordering/pricing service surface. |

## Out Of Scope

`latchbio-integration` is not deleted in this pass. It was already outside the `science-lab-automation` pack and represents computational bioinformatics workflow deployment, not wet-lab automation.

## Route Migration

The following prompts no longer select `science-lab-automation`:

| Prompt class | Old owner | Target behavior |
| --- | --- | --- |
| Opentrons OT-2/Flex protocol code | `science-lab-automation / opentrons-integration` | deleted pack not selected |
| Hamilton/Tecan/PyLabRobot automation | `science-lab-automation / pylabrobot` | deleted pack not selected |
| protocols.io API workflows | `science-lab-automation / protocolsio-integration` | deleted pack not selected |
| Benchling registry, inventory, ELN, workflow API | `science-lab-automation / benchling-integration` | deleted pack not selected |
| LabArchives notebook, entry, attachment backup | `science-lab-automation / labarchive-integration` | deleted pack not selected |
| Ginkgo Cloud Lab order preparation | `science-lab-automation / ginkgo-cloud-lab` | deleted pack not selected |

No replacement owner is required for these cold product-specific prompts.

## Verification

Focused checks:

```powershell
python -m pytest tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py -q
python -m pytest tests/runtime_neutral/test_zero_route_authority_third_pass.py tests/runtime_neutral/test_final_stage_assistant_removal.py -q
```

Routing and packaging gates:

```powershell
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

## Boundary

This evidence proves repository routing and bundled skill cleanup. It does not prove real task execution or material skill use in a live Vibe run.
```

- [ ] **Step 2: Commit governance note**

Run:

```powershell
git add docs/governance/science-lab-automation-pack-deletion-2026-04-30.md
git commit -m "docs: record science lab automation deletion"
```

Expected: commit contains only the governance note.

---

### Task 5: Final Verification And Cleanup

**Files:**
- Modify only files required by failing verification. Do not broaden scope.

- [ ] **Step 1: Run focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py -q
python -m pytest tests/runtime_neutral/test_zero_route_authority_third_pass.py tests/runtime_neutral/test_final_stage_assistant_removal.py -q
```

Expected:

```text
all tests passed
```

- [ ] **Step 2: Run route and config gates**

Run:

```powershell
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
```

Expected:

```text
all assertions passed
```

- [ ] **Step 3: Refresh and verify skills lock closure**

Run:

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
```

Expected:

```text
skills-lock generated
[PASS] offline skill closure gate passed
config parity gate passes
```

- [ ] **Step 4: Run diff cleanliness checks**

Run:

```powershell
git diff --check
rg -n "science-lab-automation|opentrons-integration|pylabrobot|protocolsio-integration|benchling-integration|labarchive-integration|ginkgo-cloud-lab" config tests scripts bundled -S
```

Expected:

```text
git diff --check has no output
rg output contains only intentional deleted-pack negative probes or no active config/bundled references
```

The `rg` command may still show references in verification scripts because those scripts now assert deleted-pack absence. It must not show:

```text
config/pack-manifest.json
config/skill-keyword-index.json
config/skill-routing-rules.json
config/skills-lock.json
bundled/skills/<deleted skill>
```

- [ ] **Step 5: Commit final verification-only adjustments**

If Task 5 required edits, commit them:

```powershell
git status --short
git add <only files changed during Task 5>
git commit -m "test: verify science lab automation deletion"
```

If Task 5 required no edits, do not create an empty commit.

- [ ] **Step 6: Report final state**

Collect:

```powershell
git status --short --branch
git log --oneline -5
```

Final report must include:

```text
branch
commit hash or hashes
deleted pack
deleted skill directories
verification commands and pass/fail summaries
remaining caveat: routing/config deletion does not prove material use
```

Do not say the package is fully cleaned globally. Say this deletion pass is complete if all checks above pass.

---

## Self-Review

Spec coverage:

- Hard-delete `science-lab-automation`: Task 2 removes the pack and six directories.
- Remove config/index/rules/lock entries: Task 2 covers all four config surfaces.
- Rewrite positive probes into absence checks: Tasks 1 and 3 cover Python tests and PowerShell route gates.
- Add governance evidence: Task 4 creates the governance note.
- Preserve six-stage runtime and binary skill usage model: Task 4 documents no runtime or helper-state changes.
- Do not delete `latchbio-integration`: Task 1 asserts its directory remains.
- Verify zero route authority and no stage assistants: Task 5 runs focused tests and smoke/config gates.

Placeholder scan:

- This plan contains no `TBD`, `TODO`, or open-ended implementation slots.
- File paths, skill ids, commands, and expected outcomes are explicit.

Type and naming consistency:

- Deleted pack id is consistently `science-lab-automation`.
- Deleted skill ids match the design spec and current manifest.
- Test helper names use Python `snake_case`.
- PowerShell fields match existing script conventions: `ExpectedPack`, `ExpectedSkill`, `BlockedPack`, `BlockedSkill`, `AllowedModes`, `expected_pack`, `expected_skill`, `blocked_pack`, `blocked_skill`.
