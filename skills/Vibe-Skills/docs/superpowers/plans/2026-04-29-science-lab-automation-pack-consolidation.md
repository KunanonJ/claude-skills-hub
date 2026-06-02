# Science Lab Automation Pack Consolidation Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate `science-lab-automation` into a six-skill direct route-authority pack with no assistant/consult routing semantics and protected boundaries for Opentrons, PyLabRobot, protocols.io, Benchling, LabArchives, and Ginkgo Cloud Lab.

**Architecture:** Add focused route tests first, then shrink `skill_candidates` because the router selects from pack candidates. Keep `route_authority_candidates` as a compatibility mirror of the selectable six skills and make `stage_assistant_candidates` explicitly empty. Tighten pack triggers, skill keywords, and routing rules so LatchBio bioinformatics workflow prompts no longer enter this wet-lab automation pack.

**Tech Stack:** Python `unittest`/pytest route tests, PowerShell scientific route probes, JSON routing configs, lock/parity verification scripts, Markdown governance docs.

---

## File Map

- Create: `tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py`
- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`
- Modify: `scripts/verify/probe-scientific-packs.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
- Create: `docs/governance/science-lab-automation-pack-consolidation-2026-04-29.md`
- Modify: `config/skills-lock.json` after running `.\scripts\verify\vibe-generate-skills-lock.ps1`

Do not modify `bundled/skills/vibe/config/*`; this checkout does not have that retired mirror. Do not physically delete any skill directory in this plan.

## Task 1: Add Focused Failing Tests

**Files:**
- Create: `tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py`

- [ ] **Step 1: Create the route and manifest test file**

Use `apply_patch` to add this exact file:

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


KEPT_SKILLS = [
    "opentrons-integration",
    "pylabrobot",
    "protocolsio-integration",
    "benchling-integration",
    "labarchive-integration",
    "ginkgo-cloud-lab",
]

MOVED_OUT_SKILLS = [
    "latchbio-integration",
]


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


def pack_by_id(pack_id: str) -> dict[str, object]:
    manifest_path = REPO_ROOT / "config" / "pack-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    packs = manifest.get("packs")
    assert isinstance(packs, list), manifest
    for pack in packs:
        assert isinstance(pack, dict), pack
        if pack.get("id") == pack_id:
            return pack
    raise AssertionError(f"pack missing: {pack_id}")


class ScienceLabAutomationPackConsolidationTests(unittest.TestCase):
    def assert_selected(
        self,
        prompt: str,
        expected_pack: str,
        expected_skill: str,
        *,
        task_type: str = "research",
        grade: str = "L",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertEqual((expected_pack, expected_skill), selected(result), ranked_summary(result))

    def assert_not_science_lab_automation(
        self,
        prompt: str,
        *,
        task_type: str = "research",
        grade: str = "L",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertNotEqual("science-lab-automation", selected(result)[0], ranked_summary(result))

    def test_manifest_shrinks_to_six_route_owners(self) -> None:
        pack = pack_by_id("science-lab-automation")
        self.assertEqual(KEPT_SKILLS, pack.get("skill_candidates"))
        self.assertEqual(KEPT_SKILLS, pack.get("route_authority_candidates"))
        self.assertEqual([], pack.get("stage_assistant_candidates"))

    def test_manifest_removes_latchbio_from_lab_automation(self) -> None:
        pack = pack_by_id("science-lab-automation")
        candidates = set(pack.get("skill_candidates") or [])
        for skill in MOVED_OUT_SKILLS:
            self.assertNotIn(skill, candidates)

    def test_defaults_match_kept_route_owners(self) -> None:
        pack = pack_by_id("science-lab-automation")
        self.assertEqual(
            {
                "planning": "protocolsio-integration",
                "coding": "opentrons-integration",
                "research": "protocolsio-integration",
            },
            pack.get("defaults_by_task"),
        )

    def test_opentrons_ot2_protocol_routes_to_opentrons(self) -> None:
        self.assert_selected(
            "写一个 Opentrons OT-2 protocol：96孔板分液 + 混匀，输出可运行脚本",
            "science-lab-automation",
            "opentrons-integration",
            task_type="coding",
            grade="M",
        )

    def test_opentrons_flex_module_routes_to_opentrons(self) -> None:
        self.assert_selected(
            "用 Opentrons Flex 和 thermocycler module 写一个 PCR setup protocol",
            "science-lab-automation",
            "opentrons-integration",
            task_type="coding",
            grade="M",
        )

    def test_pylabrobot_hamilton_tecan_routes_to_pylabrobot(self) -> None:
        self.assert_selected(
            "用 PyLabRobot 控制 Hamilton 和 Tecan 液体处理机器人，统一调度 plate reader",
            "science-lab-automation",
            "pylabrobot",
            task_type="coding",
            grade="M",
        )

    def test_pylabrobot_simulation_routes_to_pylabrobot(self) -> None:
        self.assert_selected(
            "用 pylabrobot resources 模拟 liquid handling workflow 和 deck layout",
            "science-lab-automation",
            "pylabrobot",
            task_type="coding",
            grade="M",
        )

    def test_protocolsio_pcr_routes_to_protocolsio(self) -> None:
        self.assert_selected(
            "在 protocols.io 查找 PCR protocol，并总结关键步骤与关键试剂",
            "science-lab-automation",
            "protocolsio-integration",
            grade="M",
        )

    def test_protocolsio_publish_routes_to_protocolsio(self) -> None:
        self.assert_selected(
            "用 protocols.io API 创建并发布一个实验 protocol，包含 workspace 和文件附件",
            "science-lab-automation",
            "protocolsio-integration",
            task_type="coding",
            grade="M",
        )

    def test_benchling_registry_inventory_routes_to_benchling(self) -> None:
        self.assert_selected(
            "查询 Benchling registry 里的 DNA sequence 和 inventory containers，并导出样品表",
            "science-lab-automation",
            "benchling-integration",
            task_type="coding",
            grade="M",
        )

    def test_benchling_eln_export_routes_to_benchling(self) -> None:
        self.assert_selected(
            "自动化 Benchling ELN entry 和 Data Warehouse export，把 workflow tasks 同步到表格",
            "science-lab-automation",
            "benchling-integration",
            task_type="coding",
            grade="M",
        )

    def test_labarchives_backup_routes_to_labarchive(self) -> None:
        self.assert_selected(
            "备份 LabArchives notebook，导出 entries、attachments 和 JSON metadata",
            "science-lab-automation",
            "labarchive-integration",
            task_type="coding",
            grade="M",
        )

    def test_labarchives_upload_routes_to_labarchive(self) -> None:
        self.assert_selected(
            "把自动化实验输出上传到 LabArchives entry，并附加 CSV 和图片附件",
            "science-lab-automation",
            "labarchive-integration",
            task_type="coding",
            grade="M",
        )

    def test_ginkgo_cloud_lab_order_routes_to_ginkgo(self) -> None:
        self.assert_selected(
            "在 Ginkgo Cloud Lab / cloud.ginkgo.bio 准备下单输入并估算 protocol pricing",
            "science-lab-automation",
            "ginkgo-cloud-lab",
            task_type="planning",
            grade="M",
        )

    def test_ginkgo_cell_free_expression_routes_to_ginkgo(self) -> None:
        self.assert_selected(
            "提交 Ginkgo Cloud Lab cell-free protein expression validation run",
            "science-lab-automation",
            "ginkgo-cloud-lab",
            task_type="planning",
            grade="M",
        )

    def test_latchbio_nextflow_does_not_route_to_lab_automation(self) -> None:
        self.assert_not_science_lab_automation(
            "用 LatchBio / Latch SDK 部署 Nextflow RNA-seq workflow，管理 LatchFile 和 LatchDir",
            task_type="coding",
            grade="M",
        )

    def test_generic_markdown_protocol_does_not_route_to_protocolsio(self) -> None:
        self.assert_not_science_lab_automation(
            "写一个普通 wet-lab protocol 的 Markdown 文档，不使用 protocols.io 或机器人",
            task_type="planning",
            grade="M",
        )

    def test_pubmed_methods_does_not_route_to_lab_automation(self) -> None:
        self.assert_selected(
            "在 PubMed 检索 wet-lab methods papers 并导出 BibTeX",
            "science-literature-citations",
            "pubmed-database",
            grade="M",
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and confirm it fails**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py -q
```

Expected: fails because `science-lab-automation` still has 7 candidates, lacks `route_authority_candidates`, lacks explicit empty `stage_assistant_candidates`, and routes several new probes incorrectly.

- [ ] **Step 3: Commit the failing tests**

Run:

```powershell
git add tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py
git commit -m "test: cover science lab automation routing boundaries"
```

## Task 2: Shrink The Pack Manifest

**Files:**
- Modify: `config/pack-manifest.json`

- [ ] **Step 1: Update the top-level pack manifest**

In `config/pack-manifest.json`, replace the `science-lab-automation` object with this target content while preserving neighboring packs:

```json
{
  "id": "science-lab-automation",
  "priority": 86,
  "grade_allow": [
    "M",
    "L",
    "XL"
  ],
  "task_allow": [
    "planning",
    "coding",
    "research"
  ],
  "trigger_keywords": [
    "opentrons",
    "ot-2",
    "ot2",
    "opentrons flex",
    "pylabrobot",
    "hamilton",
    "tecan",
    "protocols.io",
    "protocolsio",
    "benchling",
    "labarchives",
    "labarchive",
    "ginkgo cloud lab",
    "cloud.ginkgo.bio",
    "ginkgo bioworks cloud lab",
    "liquid handling robot",
    "pipetting robot",
    "lims",
    "实验室自动化",
    "移液机器人",
    "液体处理机器人",
    "电子实验记录",
    "云实验室"
  ],
  "skill_candidates": [
    "opentrons-integration",
    "pylabrobot",
    "protocolsio-integration",
    "benchling-integration",
    "labarchive-integration",
    "ginkgo-cloud-lab"
  ],
  "route_authority_candidates": [
    "opentrons-integration",
    "pylabrobot",
    "protocolsio-integration",
    "benchling-integration",
    "labarchive-integration",
    "ginkgo-cloud-lab"
  ],
  "stage_assistant_candidates": [],
  "defaults_by_task": {
    "planning": "protocolsio-integration",
    "coding": "opentrons-integration",
    "research": "protocolsio-integration"
  }
}
```

- [ ] **Step 2: Run the focused test again**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py -q
```

Expected: manifest tests pass, but several route tests still fail until keyword/rule edits are applied.

- [ ] **Step 3: Commit the manifest change**

Run:

```powershell
git add config/pack-manifest.json tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py
git commit -m "fix: shrink science lab automation route candidates"
```

## Task 3: Tighten Skill Keywords And Routing Rules

**Files:**
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`

- [ ] **Step 1: Replace the seven lab skill keyword entries**

In `config/skill-keyword-index.json`, replace the entries for these skills with the exact entries below:

```json
"opentrons-integration": {
  "keywords": [
    "opentrons",
    "ot-2",
    "ot2",
    "opentrons flex",
    "opentrons protocol",
    "protocol api",
    "opentrons module",
    "pipetting robot",
    "移液机器人",
    "opentrons脚本"
  ]
},
"pylabrobot": {
  "keywords": [
    "pylabrobot",
    "hamilton",
    "tecan",
    "multi-vendor lab automation",
    "liquid handler",
    "lab robot",
    "plate reader",
    "resource simulation",
    "实验室机器人",
    "多厂商实验室自动化"
  ]
},
"protocolsio-integration": {
  "keywords": [
    "protocols.io",
    "protocolsio",
    "protocols.io api",
    "protocol search",
    "publish protocol",
    "protocol workspace",
    "protocol file attachment",
    "实验协议检索",
    "实验协议发布"
  ]
},
"benchling-integration": {
  "keywords": [
    "benchling",
    "benchling registry",
    "benchling inventory",
    "benchling eln",
    "benchling data warehouse",
    "benchling workflow",
    "benchling app",
    "样品管理",
    "benchling电子实验记录"
  ]
},
"labarchive-integration": {
  "keywords": [
    "labarchives",
    "labarchive",
    "labarchives api",
    "labarchives notebook",
    "labarchives entry",
    "notebook backup",
    "entry attachment",
    "实验记录备份",
    "labarchives电子实验记录"
  ]
},
"latchbio-integration": {
  "keywords": [
    "latchbio",
    "latch sdk",
    "latch workflow",
    "latchfile",
    "latchdir",
    "nextflow",
    "snakemake",
    "serverless bioinformatics workflow",
    "生信工作流部署"
  ]
},
"ginkgo-cloud-lab": {
  "keywords": [
    "ginkgo cloud lab",
    "cloud.ginkgo.bio",
    "ginkgo bioworks cloud lab",
    "cell-free protein expression",
    "fluorescent pixel art",
    "cloud lab order",
    "protocol pricing",
    "云实验室",
    "ginkgo云实验室"
  ]
}
```

- [ ] **Step 2: Replace the seven lab routing-rule entries**

In `config/skill-routing-rules.json`, replace the entries for these skills with the exact entries below:

```json
"opentrons-integration": {
  "task_allow": [
    "planning",
    "coding"
  ],
  "positive_keywords": [
    "opentrons",
    "ot-2",
    "ot2",
    "opentrons flex",
    "protocol api",
    "opentrons module",
    "pipetting robot",
    "移液机器人"
  ],
  "negative_keywords": [
    "pylabrobot",
    "hamilton",
    "tecan",
    "protocols.io",
    "benchling",
    "labarchives",
    "ginkgo",
    "latchbio",
    "nextflow",
    "snakemake",
    "pubmed",
    "dicom",
    "sec"
  ],
  "equivalent_group": "lab-automation",
  "canonical_for_task": [
    "coding"
  ],
  "requires_positive_keyword_match": true
},
"pylabrobot": {
  "task_allow": [
    "planning",
    "coding"
  ],
  "positive_keywords": [
    "pylabrobot",
    "hamilton",
    "tecan",
    "multi-vendor lab automation",
    "liquid handler",
    "lab robot",
    "plate reader",
    "resource simulation",
    "实验室机器人"
  ],
  "negative_keywords": [
    "opentrons protocol api",
    "protocols.io",
    "benchling",
    "labarchives",
    "ginkgo",
    "latchbio",
    "nextflow",
    "snakemake",
    "pubmed",
    "dicom",
    "sec"
  ],
  "equivalent_group": "lab-automation",
  "canonical_for_task": [
    "coding"
  ],
  "requires_positive_keyword_match": true
},
"protocolsio-integration": {
  "task_allow": [
    "planning",
    "coding",
    "research"
  ],
  "positive_keywords": [
    "protocols.io",
    "protocolsio",
    "protocols.io api",
    "protocol search",
    "publish protocol",
    "protocol workspace",
    "实验协议检索",
    "实验协议发布"
  ],
  "negative_keywords": [
    "generic markdown protocol",
    "普通 wet-lab protocol",
    "opentrons",
    "pylabrobot",
    "benchling",
    "labarchives",
    "ginkgo",
    "latchbio",
    "nextflow",
    "snakemake",
    "pubmed",
    "dicom",
    "sec"
  ],
  "equivalent_group": "lab-automation",
  "canonical_for_task": [
    "planning",
    "research"
  ],
  "requires_positive_keyword_match": true
},
"benchling-integration": {
  "task_allow": [
    "planning",
    "coding"
  ],
  "positive_keywords": [
    "benchling",
    "benchling registry",
    "benchling inventory",
    "benchling eln",
    "benchling data warehouse",
    "benchling workflow",
    "benchling app",
    "样品管理"
  ],
  "negative_keywords": [
    "labarchives",
    "protocols.io",
    "opentrons",
    "pylabrobot",
    "ginkgo",
    "latchbio",
    "nextflow",
    "snakemake",
    "pubmed",
    "dicom",
    "sec"
  ],
  "equivalent_group": "lab-automation",
  "canonical_for_task": [
    "coding"
  ],
  "requires_positive_keyword_match": true
},
"labarchive-integration": {
  "task_allow": [
    "planning",
    "coding"
  ],
  "positive_keywords": [
    "labarchives",
    "labarchive",
    "labarchives api",
    "labarchives notebook",
    "labarchives entry",
    "notebook backup",
    "entry attachment",
    "实验记录备份"
  ],
  "negative_keywords": [
    "benchling",
    "protocols.io",
    "opentrons",
    "pylabrobot",
    "ginkgo",
    "latchbio",
    "nextflow",
    "snakemake",
    "pubmed",
    "dicom",
    "sec"
  ],
  "equivalent_group": "lab-automation",
  "canonical_for_task": [
    "coding"
  ],
  "requires_positive_keyword_match": true
},
"latchbio-integration": {
  "task_allow": [
    "planning",
    "coding",
    "research"
  ],
  "positive_keywords": [
    "latchbio",
    "latch sdk",
    "latch workflow",
    "latchfile",
    "latchdir",
    "nextflow",
    "snakemake",
    "serverless bioinformatics workflow",
    "生信工作流部署"
  ],
  "negative_keywords": [
    "opentrons",
    "pylabrobot",
    "protocols.io",
    "benchling",
    "labarchives",
    "ginkgo cloud lab",
    "移液机器人",
    "云实验室"
  ],
  "equivalent_group": "bioinformatics-workflow-platform",
  "canonical_for_task": [
    "coding"
  ],
  "requires_positive_keyword_match": true
},
"ginkgo-cloud-lab": {
  "task_allow": [
    "planning",
    "research"
  ],
  "positive_keywords": [
    "ginkgo cloud lab",
    "cloud.ginkgo.bio",
    "ginkgo bioworks cloud lab",
    "cell-free protein expression",
    "fluorescent pixel art",
    "cloud lab order",
    "protocol pricing",
    "云实验室"
  ],
  "negative_keywords": [
    "opentrons",
    "pylabrobot",
    "protocols.io",
    "benchling",
    "labarchives",
    "latchbio",
    "nextflow",
    "snakemake",
    "pubmed",
    "dicom",
    "sec"
  ],
  "equivalent_group": "lab-automation",
  "canonical_for_task": [
    "planning"
  ],
  "requires_positive_keyword_match": true
}
```

- [ ] **Step 3: Run the focused test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py -q
```

Expected: all focused lab automation tests pass. If one route still falls back to the wrong retained lab skill, inspect the `ranked_summary` assertion output and tune only the relevant positive or negative keyword list.

- [ ] **Step 4: Commit routing keyword/rule changes**

Run:

```powershell
git add config/skill-keyword-index.json config/skill-routing-rules.json tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py
git commit -m "fix: tighten science lab automation routing rules"
```

## Task 4: Extend Scientific Probe Coverage

**Files:**
- Modify: `scripts/verify/probe-scientific-packs.ps1`

- [ ] **Step 1: Replace the `science-lab-automation` probe block**

In `scripts/verify/probe-scientific-packs.ps1`, replace the two existing `science-lab-automation` cases with this block:

```powershell
    # science-lab-automation
    [pscustomobject]@{
        name = "lab_opentrons_ot2_protocol"
        group = "science-lab-automation"
        prompt = "/vibe 写一个 Opentrons OT-2 protocol：96孔板分液 + 混匀，输出可运行脚本"
        grade = "M"
        task_type = "coding"
        expected_pack = "science-lab-automation"
        expected_skill = "opentrons-integration"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "lab_opentrons_flex_module"
        group = "science-lab-automation"
        prompt = "/vibe 用 Opentrons Flex 和 thermocycler module 写一个 PCR setup protocol"
        grade = "M"
        task_type = "coding"
        expected_pack = "science-lab-automation"
        expected_skill = "opentrons-integration"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "lab_pylabrobot_hamilton_tecan"
        group = "science-lab-automation"
        prompt = "/vibe 用 PyLabRobot 控制 Hamilton 和 Tecan 液体处理机器人，统一调度 plate reader"
        grade = "M"
        task_type = "coding"
        expected_pack = "science-lab-automation"
        expected_skill = "pylabrobot"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "lab_protocolsio_pcr"
        group = "science-lab-automation"
        prompt = "/vibe 在 protocols.io 查找 PCR protocol，并总结关键步骤与关键试剂"
        grade = "M"
        task_type = "research"
        expected_pack = "science-lab-automation"
        expected_skill = "protocolsio-integration"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "lab_protocolsio_publish"
        group = "science-lab-automation"
        prompt = "/vibe 用 protocols.io API 创建并发布一个实验 protocol，包含 workspace 和文件附件"
        grade = "M"
        task_type = "coding"
        expected_pack = "science-lab-automation"
        expected_skill = "protocolsio-integration"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "lab_benchling_registry_inventory"
        group = "science-lab-automation"
        prompt = "/vibe 查询 Benchling registry 里的 DNA sequence 和 inventory containers，并导出样品表"
        grade = "M"
        task_type = "coding"
        expected_pack = "science-lab-automation"
        expected_skill = "benchling-integration"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "lab_labarchives_backup"
        group = "science-lab-automation"
        prompt = "/vibe 备份 LabArchives notebook，导出 entries、attachments 和 JSON metadata"
        grade = "M"
        task_type = "coding"
        expected_pack = "science-lab-automation"
        expected_skill = "labarchive-integration"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "lab_ginkgo_cloud_lab_order"
        group = "science-lab-automation"
        prompt = "/vibe 在 Ginkgo Cloud Lab / cloud.ginkgo.bio 准备下单输入并估算 protocol pricing"
        grade = "M"
        task_type = "planning"
        expected_pack = "science-lab-automation"
        expected_skill = "ginkgo-cloud-lab"
        requested_skill = $null
    },
```

- [ ] **Step 2: Run the focused scientific probe**

Run:

```powershell
.\scripts\verify\probe-scientific-packs.ps1
```

Expected: the script exits `0`, and the lab automation cases all report the expected pack/skill.

- [ ] **Step 3: Commit scientific probe coverage**

Run:

```powershell
git add scripts/verify/probe-scientific-packs.ps1
git commit -m "test: expand science lab automation route probes"
```

## Task 5: Add Routing Audit Cases

**Files:**
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`

- [ ] **Step 1: Add lab automation cases to the `$cases` array**

In `scripts/verify/vibe-skill-index-routing-audit.ps1`, add these cases near the other science pack cases:

```powershell
    [pscustomobject]@{ Name = "lab automation opentrons ot2"; Prompt = "写一个 Opentrons OT-2 protocol：96孔板分液 + 混匀，输出可运行脚本"; Grade = "M"; TaskType = "coding"; ExpectedPack = "science-lab-automation"; ExpectedSkill = "opentrons-integration" },
    [pscustomobject]@{ Name = "lab automation pylabrobot hamilton"; Prompt = "用 PyLabRobot 控制 Hamilton 和 Tecan 液体处理机器人"; Grade = "M"; TaskType = "coding"; ExpectedPack = "science-lab-automation"; ExpectedSkill = "pylabrobot" },
    [pscustomobject]@{ Name = "lab automation protocolsio publish"; Prompt = "用 protocols.io API 创建并发布一个实验 protocol"; Grade = "M"; TaskType = "coding"; ExpectedPack = "science-lab-automation"; ExpectedSkill = "protocolsio-integration" },
    [pscustomobject]@{ Name = "lab automation benchling registry"; Prompt = "查询 Benchling registry 里的 DNA sequence 和 inventory containers"; Grade = "M"; TaskType = "coding"; ExpectedPack = "science-lab-automation"; ExpectedSkill = "benchling-integration" },
    [pscustomobject]@{ Name = "lab automation labarchives backup"; Prompt = "备份 LabArchives notebook，导出 entries 和 attachments"; Grade = "M"; TaskType = "coding"; ExpectedPack = "science-lab-automation"; ExpectedSkill = "labarchive-integration" },
    [pscustomobject]@{ Name = "lab automation ginkgo cloud lab"; Prompt = "在 Ginkgo Cloud Lab / cloud.ginkgo.bio 准备下单输入"; Grade = "M"; TaskType = "planning"; ExpectedPack = "science-lab-automation"; ExpectedSkill = "ginkgo-cloud-lab" },
    [pscustomobject]@{ Name = "lab automation blocks latchbio"; Prompt = "用 LatchBio / Latch SDK 部署 Nextflow RNA-seq workflow"; Grade = "M"; TaskType = "coding"; BlockedPack = "science-lab-automation" },
```

- [ ] **Step 2: Run the routing audit**

Run:

```powershell
.\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected: exits `0` with all lab automation assertions passing.

- [ ] **Step 3: Commit audit coverage**

Run:

```powershell
git add scripts/verify/vibe-skill-index-routing-audit.ps1
git commit -m "test: audit science lab automation routing boundaries"
```

## Task 6: Add Governance Note

**Files:**
- Create: `docs/governance/science-lab-automation-pack-consolidation-2026-04-29.md`

- [ ] **Step 1: Create the governance note**

Use `apply_patch` to add this exact file:

````markdown
# Science Lab Automation Pack Consolidation

Date: 2026-04-29

## Summary

`science-lab-automation` was consolidated into a wet-lab automation specialist routing pack.

This cleanup keeps the six-stage Vibe runtime unchanged and preserves the binary usage model:

```text
skill_routing.selected -> skill_usage.used / unused
```

No `primary/secondary`, `consult`, `advisory`, or stage-assistant execution semantics were added.

## Before And After

| Field | Before | After |
| --- | ---: | ---: |
| `skill_candidates` | 7 | 6 |
| `route_authority_candidates` | 0 | 6 |
| `stage_assistant_candidates` | 0 | 0 |
| physical directory deletion | 0 | 0 |

## Kept Route Authorities

| Skill | Boundary |
| --- | --- |
| `opentrons-integration` | Opentrons OT-2/Flex Protocol API, deck setup, pipetting scripts, and Opentrons module protocols |
| `pylabrobot` | Multi-vendor lab automation across Hamilton, Tecan, Opentrons backends, plate readers, pumps, resources, and simulation |
| `protocolsio-integration` | protocols.io search, create, update, publish, workspace/file, and collaboration workflows |
| `benchling-integration` | Benchling registry, inventory, ELN entries, workflows, apps, and data warehouse automation |
| `labarchive-integration` | LabArchives notebooks, entries, attachments, backups, and API workflows |
| `ginkgo-cloud-lab` | Ginkgo Cloud Lab protocol selection, cloud.ginkgo.bio ordering, cell-free protein expression, and pricing/input preparation |

`route_authority_candidates` mirrors `skill_candidates` for compatibility and documentation. The actual simplification is enforced by shrinking `skill_candidates`.

## Moved Out Of This Pack

| Skill | Reason |
| --- | --- |
| `latchbio-integration` | LatchBio is a computational bioinformatics workflow platform for Latch SDK, LatchFile/LatchDir, Nextflow/Snakemake, and serverless pipelines. It is not a wet-lab automation route owner. |

Moved-out skills remain on disk. No physical deletion was performed in this pass.

## Protected Route Boundaries

| Prompt | Expected route |
| --- | --- |
| `Opentrons OT-2 protocol：96孔板分液 + 混匀` | `science-lab-automation / opentrons-integration` |
| `Opentrons Flex thermocycler module PCR setup` | `science-lab-automation / opentrons-integration` |
| `PyLabRobot 控制 Hamilton 和 Tecan 液体处理机器人` | `science-lab-automation / pylabrobot` |
| `protocols.io 查找 PCR protocol` | `science-lab-automation / protocolsio-integration` |
| `protocols.io API 创建并发布实验 protocol` | `science-lab-automation / protocolsio-integration` |
| `Benchling registry / inventory / DNA sequence` | `science-lab-automation / benchling-integration` |
| `Benchling ELN / Data Warehouse export` | `science-lab-automation / benchling-integration` |
| `LabArchives notebook backup / entries / attachments` | `science-lab-automation / labarchive-integration` |
| `LabArchives entry upload with CSV/image attachments` | `science-lab-automation / labarchive-integration` |
| `Ginkgo Cloud Lab / cloud.ginkgo.bio order preparation` | `science-lab-automation / ginkgo-cloud-lab` |
| `Ginkgo Cloud Lab cell-free protein expression validation` | `science-lab-automation / ginkgo-cloud-lab` |
| `LatchBio / Latch SDK / Nextflow RNA-seq workflow` | not `science-lab-automation` |
| `generic wet-lab protocol Markdown without protocols.io or robots` | not `science-lab-automation` |
| `PubMed wet-lab methods papers / BibTeX` | not `science-lab-automation` |

## Verification

Focused:

```powershell
python -m pytest tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py -q
```

Broader probes and gates:

```powershell
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```
````

- [ ] **Step 2: Commit governance note**

Run:

```powershell
git add docs/governance/science-lab-automation-pack-consolidation-2026-04-29.md
git commit -m "docs: record science lab automation boundary"
```

## Task 7: Refresh Lock And Run Full Verification

**Files:**
- Modify: `config/skills-lock.json`

- [ ] **Step 1: Refresh the skills lock**

Run:

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected: exits `0`. If `config/skills-lock.json` changes, keep the generated change.

- [ ] **Step 2: Run focused verification**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py -q
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected:

```text
tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py passes
probe-scientific-packs.ps1 exits 0
vibe-skill-index-routing-audit.ps1 exits 0
```

- [ ] **Step 3: Run broader regression gates**

Run:

```powershell
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

Expected:

```text
vibe-pack-regression-matrix.ps1 exits 0
vibe-pack-routing-smoke.ps1 exits 0
vibe-offline-skills-gate.ps1 exits 0
vibe-config-parity-gate.ps1 exits 0
git diff --check prints no whitespace errors
```

- [ ] **Step 4: Commit generated lock and final clean state**

Run:

```powershell
git add config/skills-lock.json
git commit -m "chore: refresh skills lock after lab automation routing cleanup"
git status --short --branch
```

Expected: branch is ahead of `origin/main`, and no unintended files remain modified.

## Completion Checklist

- [ ] `science-lab-automation` has exactly six selectable `skill_candidates`.
- [ ] `route_authority_candidates` mirrors the six selectable skills.
- [ ] `stage_assistant_candidates` is explicitly `[]`.
- [ ] `latchbio-integration` is no longer a candidate for this pack.
- [ ] Opentrons, PyLabRobot, protocols.io, Benchling, LabArchives, and Ginkgo Cloud Lab each have a positive route test or probe.
- [ ] LatchBio / Nextflow / Snakemake computational workflow prompts do not route to this pack.
- [ ] Generic Markdown wet-lab protocol writing does not route to this pack unless protocols.io or a retained product/hardware owner is named.
- [ ] No skill directory is physically deleted.
- [ ] Focused tests, scientific probes, routing audit, pack matrix, routing smoke, offline gate, config parity, and whitespace checks pass.
