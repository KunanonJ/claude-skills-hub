# Science Medical Imaging Pack Consolidation Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden `science-medical-imaging` routing boundaries while keeping the current 5 direct route owners and zero stage assistants.

**Architecture:** Keep the Vibe six-stage runtime unchanged and keep the simplified routing model as `candidate skill -> selected skill -> used / unused`. This implementation only adjusts route evidence, skill trigger text, pack-specific tests, verification scripts, and governance notes for `science-medical-imaging`; it does not add advisory experts, main/sub-skill state, consultation routing, or stage assistants.

**Tech Stack:** Python `unittest`/`pytest`, PowerShell verification scripts, JSON route configuration, bundled Markdown skill docs, skills lock generation, Git.

---

## Scope

This plan implements the approved design:

```text
docs/superpowers/specs/2026-04-30-science-medical-imaging-pack-consolidation-design.md
```

Keep these 5 direct route owners:

```text
pydicom
imaging-data-commons
histolab
omero-integration
pathml
```

Keep this pack invariant:

```text
skill_candidates = 5
route_authority_candidates = 5
stage_assistant_candidates = []
```

Do not physically delete any `bundled/skills/*` directory in this pass.

Do not claim real task material skill use from these changes. This work proves routing/config/bundled-doc cleanup and regression coverage only.

## File Map

- Create `tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py`: pack-specific route/config/doc regression tests.
- Modify `config/skill-keyword-index.json`: strengthen precise owner triggers for the five retained medical-imaging skills.
- Modify `config/skill-routing-rules.json`: add positive and negative route boundaries for all five medical-imaging owners.
- Modify `bundled/skills/pydicom/SKILL.md`: add a short route boundary note.
- Modify `bundled/skills/imaging-data-commons/SKILL.md`: add a short route boundary note distinguishing IDC from generic Data Commons.
- Modify `bundled/skills/histolab/SKILL.md`: add a short route boundary note distinguishing histolab from full PathML workflows.
- Modify `bundled/skills/omero-integration/SKILL.md`: add a short route boundary note requiring OMERO/server/API/ROI context.
- Modify `bundled/skills/pathml/SKILL.md`: add a short route boundary note distinguishing PathML workflows from basic histolab tiling and generic image segmentation.
- Modify `scripts/verify/vibe-pack-regression-matrix.ps1`: add medical-imaging positive and negative route cases.
- Modify `scripts/verify/vibe-skill-index-routing-audit.ps1`: add missing medical-imaging positive cases and blocked cases.
- Modify `scripts/verify/probe-scientific-packs.ps1`: add negative medical-imaging cases because the script already supports `blocked_pack` and `blocked_skill`.
- Create `docs/governance/science-medical-imaging-pack-consolidation-2026-04-30.md`: governance note with results.
- Modify `config/skills-lock.json`: refresh after bundled skill file edits.

## Task 1: Add Failing Pack-Specific Tests

**Files:**
- Create: `tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py`

- [ ] **Step 1: Create the test file**

Create `tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py` with this exact content:

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


MEDICAL_IMAGING_SKILLS = [
    "pydicom",
    "imaging-data-commons",
    "histolab",
    "omero-integration",
    "pathml",
]


def route(prompt: str, task_type: str = "research", grade: str = "M") -> dict[str, object]:
    return route_prompt(prompt=prompt, grade=grade, task_type=task_type, repo_root=REPO_ROOT)


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


def skill_keywords(skill_id: str) -> list[str]:
    path = REPO_ROOT / "config" / "skill-keyword-index.json"
    index = json.loads(path.read_text(encoding="utf-8-sig"))
    skill = index.get("skills", {}).get(skill_id)
    assert isinstance(skill, dict), skill_id
    keywords = skill.get("keywords")
    assert isinstance(keywords, list), skill
    return [str(keyword).lower() for keyword in keywords]


def routing_rule(skill_id: str) -> dict[str, object]:
    path = REPO_ROOT / "config" / "skill-routing-rules.json"
    rules = json.loads(path.read_text(encoding="utf-8-sig"))
    skill = rules.get("skills", {}).get(skill_id)
    assert isinstance(skill, dict), skill_id
    return skill


def positive_keywords(skill_id: str) -> list[str]:
    keywords = routing_rule(skill_id).get("positive_keywords")
    assert isinstance(keywords, list), skill_id
    return [str(keyword).lower() for keyword in keywords]


def negative_keywords(skill_id: str) -> list[str]:
    keywords = routing_rule(skill_id).get("negative_keywords")
    assert isinstance(keywords, list), skill_id
    return [str(keyword).lower() for keyword in keywords]


def skill_body(skill_id: str) -> str:
    path = REPO_ROOT / "bundled" / "skills" / skill_id / "SKILL.md"
    text = path.read_text(encoding="utf-8-sig")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lower()
    return text.lower()


class ScienceMedicalImagingPackConsolidationTests(unittest.TestCase):
    def assert_selected(
        self,
        prompt: str,
        expected_pack: str,
        expected_skill: str,
        *,
        task_type: str = "research",
        grade: str = "M",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertEqual((expected_pack, expected_skill), selected(result), ranked_summary(result))

    def assert_not_selected(
        self,
        prompt: str,
        blocked_pack: str | None = None,
        blocked_skill: str | None = None,
        *,
        task_type: str = "research",
        grade: str = "M",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        chosen_pack, chosen_skill = selected(result)
        if blocked_pack is not None:
            self.assertNotEqual(blocked_pack, chosen_pack, ranked_summary(result))
        if blocked_skill is not None:
            self.assertNotEqual(blocked_skill, chosen_skill, ranked_summary(result))

    def test_manifest_keeps_five_direct_owners_and_no_stage_assistants(self) -> None:
        pack = pack_by_id("science-medical-imaging")
        self.assertEqual(MEDICAL_IMAGING_SKILLS, pack.get("skill_candidates"))
        self.assertEqual(MEDICAL_IMAGING_SKILLS, pack.get("route_authority_candidates"))
        self.assertEqual([], pack.get("stage_assistant_candidates"))
        defaults = pack.get("defaults_by_task")
        self.assertIsInstance(defaults, dict)
        for task_name in ["planning", "coding", "research"]:
            self.assertIn(defaults.get(task_name), MEDICAL_IMAGING_SKILLS, defaults)

    def test_medical_imaging_positive_routes_hit_direct_owners(self) -> None:
        self.assert_selected(
            "用 pydicom 读取 CT DICOM tags，匿名化 PatientName，并导出 pixel array",
            "science-medical-imaging",
            "pydicom",
            task_type="coding",
        )
        self.assert_selected(
            "从 NCI Imaging Data Commons 查询 TCIA cancer imaging cohort 并下载 DICOMWeb 样例",
            "science-medical-imaging",
            "imaging-data-commons",
        )
        self.assert_selected(
            "用 histolab 对 whole slide image 做 tissue detection 和 H&E tile extraction",
            "science-medical-imaging",
            "histolab",
            task_type="coding",
        )
        self.assert_selected(
            "用 OMERO server Python API 读取 microscopy image server 的 ROI annotations",
            "science-medical-imaging",
            "omero-integration",
            task_type="coding",
        )
        self.assert_selected(
            "用 PathML 构建 computational pathology WSI pipeline，包含 nucleus segmentation 和 spatial graph",
            "science-medical-imaging",
            "pathml",
            task_type="planning",
        )

    def test_generic_datacommons_does_not_select_imaging_data_commons(self) -> None:
        self.assert_not_selected(
            "用 Data Commons 查询 population indicators、statistical variables 和 DCID，不涉及 Imaging Data Commons 或 DICOMWeb",
            blocked_pack="science-medical-imaging",
            blocked_skill="imaging-data-commons",
        )

    def test_literature_clinical_and_publishing_do_not_select_medical_imaging(self) -> None:
        self.assert_not_selected(
            "查询 PubMed 文献并整理 PMID citation evidence table",
            blocked_pack="science-medical-imaging",
        )
        self.assert_not_selected(
            "从 ClinicalTrials.gov 查询 NCT01234567 的终点和入排标准",
            blocked_pack="science-medical-imaging",
        )
        self.assert_not_selected(
            "写 LaTeX 论文并用 latexmk 构建 submission PDF",
            blocked_pack="science-medical-imaging",
            task_type="coding",
            grade="XL",
        )
        self.assert_not_selected(
            "写一篇科研报告，包含 methods results discussion 并导出 PDF",
            blocked_pack="science-medical-imaging",
            task_type="planning",
            grade="L",
        )

    def test_generic_image_processing_and_bioinformatics_do_not_select_medical_imaging(self) -> None:
        self.assert_not_selected(
            "对普通 PNG 图片做 OCR、截图裁剪和图像增强，不涉及 DICOM、WSI、OMERO 或 PathML",
            blocked_pack="science-medical-imaging",
            task_type="coding",
        )
        self.assert_not_selected(
            "分析 scRNA-seq h5ad，做 marker genes、KEGG enrichment 和 UMAP 可视化",
            blocked_pack="science-medical-imaging",
        )
        self.assert_not_selected(
            "用 RDKit 解析 SMILES 并做 molecule docking",
            blocked_pack="science-medical-imaging",
            task_type="coding",
        )

    def test_histolab_and_pathml_split_is_stable(self) -> None:
        self.assert_selected(
            "用 histolab 做 WSI tile extraction、tissue detection 和 H&E tile dataset preparation",
            "science-medical-imaging",
            "histolab",
            task_type="coding",
        )
        self.assert_not_selected(
            "用 histolab 做 WSI tile extraction、tissue detection 和 H&E tile dataset preparation",
            blocked_skill="pathml",
            task_type="coding",
        )
        self.assert_selected(
            "用 PathML 构建 digital pathology workflow，包含 nucleus segmentation、multiplex pathology 和 tissue graph",
            "science-medical-imaging",
            "pathml",
            task_type="planning",
        )
        self.assert_not_selected(
            "用 PathML 构建 digital pathology workflow，包含 nucleus segmentation、multiplex pathology 和 tissue graph",
            blocked_skill="histolab",
            task_type="planning",
        )

    def test_keyword_index_uses_specific_medical_imaging_terms(self) -> None:
        required = {
            "pydicom": ["dicom anonymization", "dicom pixel data", "medical scan"],
            "imaging-data-commons": ["nci imaging data commons", "tcia", "dicomweb", "cancer imaging cohort"],
            "histolab": ["wsi tile extraction", "tissue detection", "h&e tile"],
            "omero-integration": ["omero server", "roi annotation", "microscopy image server"],
            "pathml": ["computational pathology", "nucleus segmentation", "spatial pathology", "multiplex pathology"],
        }
        for skill_id, terms in required.items():
            with self.subTest(skill_id=skill_id):
                keywords = skill_keywords(skill_id)
                for term in terms:
                    self.assertIn(term, keywords)

    def test_routing_rules_encode_medical_imaging_owner_boundaries(self) -> None:
        expected_negative = {
            "pydicom": [
                "pubmed",
                "clinicaltrials",
                "latex",
                "scientific report",
                "generic image processing",
                "ocr",
                "screenshot",
                "scRNA-seq",
                "rdkit",
                "data commons",
            ],
            "imaging-data-commons": [
                "generic data commons",
                "population indicators",
                "statistical variables",
                "dcid",
                "pubmed",
                "clinicaltrials",
                "latex",
                "scientific report",
                "generic public dataset",
            ],
            "histolab": [
                "dicom",
                "dicomweb",
                "omero",
                "pathml workflow",
                "nucleus segmentation",
                "pubmed",
                "clinicaltrials",
                "generic image processing",
                "ocr",
            ],
            "omero-integration": [
                "pubmed",
                "clinicaltrials",
                "dicom",
                "tcia",
                "histolab",
                "pathml",
                "generic microscopy literature",
                "scRNA-seq",
                "rna-seq",
            ],
            "pathml": [
                "dicom tag",
                "dicom anonymization",
                "imaging data commons",
                "tcia",
                "omero server",
                "histolab tile extraction",
                "pubmed",
                "clinicaltrials",
                "generic image processing",
                "generic machine learning",
            ],
        }
        for skill_id, required_terms in expected_negative.items():
            with self.subTest(skill_id=skill_id):
                negatives = negative_keywords(skill_id)
                for term in required_terms:
                    self.assertIn(term.lower(), negatives)

    def test_kept_skill_docs_state_routing_boundaries(self) -> None:
        expected_phrases = {
            "pydicom": ["routing boundary", "dicom files, tags, pixel data, anonymization"],
            "imaging-data-commons": ["routing boundary", "not generic data commons"],
            "histolab": ["routing boundary", "basic wsi tile extraction"],
            "omero-integration": ["routing boundary", "omero server"],
            "pathml": ["routing boundary", "full computational pathology"],
        }
        for skill_id, phrases in expected_phrases.items():
            with self.subTest(skill_id=skill_id):
                body = skill_body(skill_id)
                for phrase in phrases:
                    self.assertIn(phrase, body)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and confirm it fails before implementation**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py -q
```

Expected result before implementation:

```text
FAILED
```

Expected failures include at least:

```text
test_keyword_index_uses_specific_medical_imaging_terms
test_routing_rules_encode_medical_imaging_owner_boundaries
test_kept_skill_docs_state_routing_boundaries
```

Route negative tests may also fail before implementation. Do not weaken the test to make current behavior pass.

- [ ] **Step 3: Commit the failing test**

Run:

```powershell
git add tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py
git diff --cached --check
git commit -m "test: add medical imaging pack consolidation coverage"
```

Expected result:

```text
Git creates a commit with message: test: add medical imaging pack consolidation coverage
```

## Task 2: Harden Medical-Imaging Keyword Index And Routing Rules

**Files:**
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`
- Test: `tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py`

- [ ] **Step 1: Update `config/skill-keyword-index.json` medical-imaging entries**

Replace the five medical-imaging skill keyword blocks with these exact arrays:

```json
"pydicom": {
  "keywords": ["pydicom", "dicom", "dicom tag", "dicom metadata", "dicom anonymization", "dicom pixel data", "medical scan", "ct", "mri", "pet", "x-ray", "radiology", "医学影像", "dicom文件", "影像tag", "DICOM"]
},
"imaging-data-commons": {
  "keywords": ["nci imaging data commons", "imaging data commons", "idc", "tcia", "dicomweb", "cancer imaging cohort", "public cancer imaging data", "radiology dataset", "dicom dataset", "影像数据集", "癌症影像队列", "IDC"]
},
"histolab": {
  "keywords": ["histolab", "whole slide image", "wsi", "wsi tile extraction", "tile extraction", "tissue detection", "h&e tile", "histopathology", "病理切片", "全视野切片", "组织检测", "WSI"]
},
"omero-integration": {
  "keywords": ["omero", "omero server", "omero python api", "microscopy image server", "image server", "roi annotation", "roi annotations", "microscopy dataset", "high-content screening", "bioimaging server", "显微图像", "图像服务器", "ROI标注"]
},
"pathml": {
  "keywords": ["pathml", "digital pathology", "computational pathology", "wsi analysis pipeline", "nucleus segmentation", "spatial pathology", "multiplex pathology", "tissue graph", "cell graph", "multiparametric imaging", "数字病理", "病理图像分析", "细胞核分割", "空间病理"]
}
```

Keep the JSON object ordering style already used by the file. Validate the file after editing:

```powershell
python -m json.tool config/skill-keyword-index.json > $null
```

- [ ] **Step 2: Update `config/skill-routing-rules.json` medical-imaging entries**

For each skill below, keep the existing `task_allow`, `equivalent_group`, and `canonical_for_task` values unless shown otherwise. Replace only `positive_keywords` and `negative_keywords` with the exact arrays below.

`pydicom`:

```json
"positive_keywords": ["dicom", "pydicom", "dicom tag", "dicom metadata", "dicom anonymization", "dicom pixel data", "medical scan", "ct", "mri", "pet", "x-ray", "radiology", "pacs", "医学影像", "dicom文件"],
"negative_keywords": ["pubmed", "pmid", "clinicaltrials", "clinical trials", "nct", "latex", "submission pdf", "scientific report", "paper writing", "generic image processing", "ocr", "screenshot", "png image", "jpeg image", "scRNA-seq", "rna-seq", "h5ad", "bam", "vcf", "flow cytometry", "rdkit", "smiles", "docking", "data commons", "statistical variables"]
```

`imaging-data-commons`:

```json
"positive_keywords": ["nci imaging data commons", "imaging data commons", "idc", "tcia", "dicomweb", "cancer imaging cohort", "public cancer imaging data", "radiology dataset", "dicom dataset", "影像数据集", "癌症影像队列"],
"negative_keywords": ["generic data commons", "data commons statistical", "population indicators", "statistical variables", "dcid", "public statistical data", "generic public dataset", "open dataset search", "pubmed", "pmid", "clinicaltrials", "clinical trials", "nct", "latex", "submission pdf", "scientific report", "paper writing", "fred", "treasury fiscal data", "sec filing"]
```

`histolab`:

```json
"positive_keywords": ["histolab", "whole slide", "whole slide image", "wsi", "wsi tile extraction", "tile extraction", "tissue detection", "h&e tile", "histopathology", "病理切片", "全视野切片", "组织检测"],
"negative_keywords": ["dicom", "pydicom", "dicomweb", "ct", "mri", "pet", "omero", "omero server", "pathml workflow", "pathml", "nucleus segmentation", "spatial pathology", "multiplex pathology", "pubmed", "pmid", "clinicaltrials", "generic image processing", "ocr", "screenshot", "generic machine learning"]
```

`omero-integration`:

```json
"positive_keywords": ["omero", "omero server", "omero python api", "microscopy image server", "image server", "roi annotation", "roi annotations", "ome-tiff", "microscopy dataset", "high-content screening", "显微镜", "显微图像", "图像服务器", "ROI标注", "OME"],
"negative_keywords": ["pubmed", "pmid", "clinicaltrials", "clinical trials", "nct", "dicom", "pydicom", "dicom tag", "tcia", "imaging data commons", "histolab", "wsi tile", "pathml", "computational pathology", "generic microscopy literature", "scRNA-seq", "rna-seq", "h5ad", "flow cytometry", "generic image processing"]
```

`pathml`:

```json
"positive_keywords": ["pathml", "digital pathology", "computational pathology", "wsi analysis pipeline", "nucleus segmentation", "spatial pathology", "multiplex pathology", "tissue graph", "cell graph", "multiparametric imaging", "数字病理", "病理分析", "细胞核分割", "空间病理"],
"negative_keywords": ["dicom tag", "dicom anonymization", "pydicom", "imaging data commons", "tcia", "dicomweb", "omero server", "roi annotation", "histolab tile extraction", "histolab", "basic wsi tile extraction", "pubmed", "pmid", "clinicaltrials", "clinical trials", "nct", "latex", "submission pdf", "scientific report", "generic image processing", "generic machine learning", "scikit-learn", "rdkit", "smiles"]
```

Validate the file after editing:

```powershell
python -m json.tool config/skill-routing-rules.json > $null
```

- [ ] **Step 3: Run focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py -q
```

Expected result after this task:

```text
The routing and keyword/rule tests pass, but test_kept_skill_docs_state_routing_boundaries may still fail until Task 3.
```

If a positive route fails because a neighboring medical-imaging owner wins, fix the relevant positive/negative keywords. Do not allow generic Data Commons, PubMed, ClinicalTrials, LaTeX/PDF, generic image-processing, bioinformatics, or chemistry prompts to select `science-medical-imaging`.

- [ ] **Step 4: Commit routing config hardening**

Run:

```powershell
git add config/skill-keyword-index.json config/skill-routing-rules.json
git diff --cached --check
git commit -m "fix: harden medical imaging route boundaries"
```

Expected result:

```text
Git creates a commit with message: fix: harden medical imaging route boundaries
```

## Task 3: Add Boundary Notes To Retained Skill Docs

**Files:**
- Modify: `bundled/skills/pydicom/SKILL.md`
- Modify: `bundled/skills/imaging-data-commons/SKILL.md`
- Modify: `bundled/skills/histolab/SKILL.md`
- Modify: `bundled/skills/omero-integration/SKILL.md`
- Modify: `bundled/skills/pathml/SKILL.md`
- Test: `tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py`

- [ ] **Step 1: Add a routing boundary note to `bundled/skills/pydicom/SKILL.md`**

Insert this section after the `## Overview` paragraph and before `## When to Use This Skill`:

```markdown
## Routing Boundary

Use this skill for DICOM files, tags, pixel data, anonymization, CT/MRI/PET/X-ray medical scans, PACS-oriented processing, and pydicom-specific coding. Generic PNG/JPEG image processing, OCR, screenshots, PubMed/literature search, ClinicalTrials.gov lookup, LaTeX/PDF builds, bioinformatics, chemistry, or generic Data Commons tasks are outside this skill.
```

- [ ] **Step 2: Add a routing boundary note to `bundled/skills/imaging-data-commons/SKILL.md`**

Insert this section after the `## Overview` section and before the existing `**Current IDC Data Version...` line:

```markdown
## Routing Boundary

Use this skill for NCI Imaging Data Commons, IDC, TCIA cancer imaging cohorts, DICOMWeb, public cancer imaging data, radiology datasets, and DICOM imaging cohort retrieval. This is not generic Data Commons, public statistical data, population indicators, statistical variables, DCIDs, PubMed, ClinicalTrials.gov, or generic public dataset search.
```

- [ ] **Step 3: Add a routing boundary note to `bundled/skills/histolab/SKILL.md`**

Insert this section after the `## Overview` paragraph and before `## Installation`:

```markdown
## Routing Boundary

Use this skill for basic WSI tile extraction, tissue detection, H&E tile preprocessing, and quick histolab dataset preparation. Full computational pathology workflows, PathML pipelines, nucleus segmentation, spatial pathology, multiplex pathology, DICOM/IDC retrieval, OMERO server work, and generic image-processing tasks are outside this skill.
```

- [ ] **Step 4: Add a routing boundary note to `bundled/skills/omero-integration/SKILL.md`**

Insert this section after the `## Overview` paragraph and before `## When to Use This Skill`:

```markdown
## Routing Boundary

Use this skill for OMERO server access, OMERO Python API work, microscopy image server data retrieval, ROI annotation, image metadata management, and high-content screening image management. Generic microscopy literature search, DICOM tags, IDC/TCIA retrieval, histolab tiling, PathML computational pathology, scRNA-seq, flow cytometry, and generic image processing are outside this skill.
```

- [ ] **Step 5: Add a routing boundary note to `bundled/skills/pathml/SKILL.md`**

Insert this section after the `## Overview` paragraph and before `## When to Use This Skill`:

```markdown
## Routing Boundary

Use this skill for full computational pathology workflows, PathML pipelines, WSI analysis, nucleus segmentation, tissue or cell graphs, spatial pathology, multiplex pathology, and multiparametric imaging. Basic WSI tile extraction should stay with histolab, DICOM tag/anonymization work with pydicom, IDC/TCIA/DICOMWeb retrieval with imaging-data-commons, and OMERO server or ROI management with omero-integration.
```

- [ ] **Step 6: Run focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py -q
```

Expected result:

```text
all tests pass
```

- [ ] **Step 7: Commit bundled skill boundary notes**

Run:

```powershell
git add bundled/skills/pydicom/SKILL.md bundled/skills/imaging-data-commons/SKILL.md bundled/skills/histolab/SKILL.md bundled/skills/omero-integration/SKILL.md bundled/skills/pathml/SKILL.md
git diff --cached --check
git commit -m "fix: clarify medical imaging skill boundaries"
```

Expected result:

```text
Git creates a commit with message: fix: clarify medical imaging skill boundaries
```

## Task 4: Expand Route Script Regressions

**Files:**
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
- Modify: `scripts/verify/probe-scientific-packs.ps1`

- [ ] **Step 1: Add medical-imaging cases to `vibe-pack-regression-matrix.ps1`**

Near the existing row named `medical imaging pydicom direct owner`, replace that single medical-imaging row with these rows:

```powershell
    [pscustomobject]@{ Name = "medical imaging pydicom direct owner"; Prompt = "用 pydicom 读取 CT DICOM tags，匿名化 PatientName，并导出 pixel array"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "pydicom"; AllowedModes = @("pack_overlay", "confirm_required") },
    [pscustomobject]@{ Name = "medical imaging idc direct owner"; Prompt = "从 NCI Imaging Data Commons 查询 TCIA cancer imaging cohort 并下载 DICOMWeb 样例"; Grade = "M"; TaskType = "research"; RequestedSkill = $null; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "imaging-data-commons"; AllowedModes = @("pack_overlay", "confirm_required") },
    [pscustomobject]@{ Name = "medical imaging histolab direct owner"; Prompt = "用 histolab 对 whole slide image 做 tissue detection 和 H&E tile extraction"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "histolab"; AllowedModes = @("pack_overlay", "confirm_required") },
    [pscustomobject]@{ Name = "medical imaging omero direct owner"; Prompt = "用 OMERO server Python API 读取 microscopy image server 的 ROI annotations"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "omero-integration"; AllowedModes = @("pack_overlay", "confirm_required") },
    [pscustomobject]@{ Name = "medical imaging pathml direct owner"; Prompt = "用 PathML 构建 computational pathology WSI pipeline，包含 nucleus segmentation 和 spatial graph"; Grade = "M"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "pathml"; AllowedModes = @("pack_overlay", "confirm_required") },
    [pscustomobject]@{ Name = "medical imaging blocks generic datacommons"; Prompt = "用 Data Commons 查询 population indicators、statistical variables 和 DCID，不涉及 Imaging Data Commons 或 DICOMWeb"; Grade = "M"; TaskType = "research"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "science-medical-imaging"; BlockedSkill = "imaging-data-commons"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "medical imaging blocks pubmed evidence"; Prompt = "查询 PubMed 文献并整理 PMID citation evidence table"; Grade = "M"; TaskType = "research"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "science-medical-imaging"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "medical imaging blocks clinicaltrials"; Prompt = "从 ClinicalTrials.gov 查询 NCT01234567 的终点和入排标准"; Grade = "M"; TaskType = "research"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "science-medical-imaging"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "medical imaging blocks latex submission pdf"; Prompt = "写 LaTeX 论文并用 latexmk 构建 submission PDF"; Grade = "XL"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = "scholarly-publishing-workflow"; ExpectedSkill = "latex-submission-pipeline"; BlockedPack = "science-medical-imaging"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "medical imaging blocks generic image processing"; Prompt = "对普通 PNG 图片做 OCR、截图裁剪和图像增强，不涉及 DICOM、WSI、OMERO 或 PathML"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "science-medical-imaging"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "medical imaging histolab not pathml"; Prompt = "用 histolab 做 WSI tile extraction、tissue detection 和 H&E tile dataset preparation"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "histolab"; BlockedSkill = "pathml"; AllowedModes = @("pack_overlay", "confirm_required") },
    [pscustomobject]@{ Name = "medical imaging pathml not histolab"; Prompt = "用 PathML 构建 digital pathology workflow，包含 nucleus segmentation、multiplex pathology 和 tissue graph"; Grade = "M"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "pathml"; BlockedSkill = "histolab"; AllowedModes = @("pack_overlay", "confirm_required") },
```

- [ ] **Step 2: Add medical-imaging cases to `vibe-skill-index-routing-audit.ps1`**

Near the current `dicom tags not bio`, `medical histolab wsi`, and `medical omero microscopy` rows, replace those three rows with:

```powershell
    [pscustomobject]@{ Name = "medical pydicom dicom tags"; Prompt = "用 pydicom 读取 CT DICOM tags，匿名化 PatientName，并导出 pixel array"; Grade = "M"; TaskType = "coding"; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "pydicom" },
    [pscustomobject]@{ Name = "medical imaging data commons"; Prompt = "从 NCI Imaging Data Commons 查询 TCIA cancer imaging cohort 并下载 DICOMWeb 样例"; Grade = "M"; TaskType = "research"; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "imaging-data-commons" },
    [pscustomobject]@{ Name = "medical histolab wsi"; Prompt = "用 histolab 对 whole slide image 做 tissue detection 和 H&E tile extraction"; Grade = "M"; TaskType = "coding"; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "histolab" },
    [pscustomobject]@{ Name = "medical omero microscopy"; Prompt = "用 OMERO server Python API 读取 microscopy image server 的 ROI annotations"; Grade = "M"; TaskType = "coding"; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "omero-integration" },
    [pscustomobject]@{ Name = "medical pathml workflow"; Prompt = "用 PathML 构建 computational pathology WSI pipeline，包含 nucleus segmentation 和 spatial graph"; Grade = "M"; TaskType = "planning"; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "pathml" },
    [pscustomobject]@{ Name = "medical generic datacommons blocked"; Prompt = "用 Data Commons 查询 population indicators、statistical variables 和 DCID，不涉及 Imaging Data Commons 或 DICOMWeb"; Grade = "M"; TaskType = "research"; BlockedPack = "science-medical-imaging"; BlockedSkill = "imaging-data-commons" },
    [pscustomobject]@{ Name = "medical pubmed evidence blocked"; Prompt = "查询 PubMed 文献并整理 PMID citation evidence table"; Grade = "M"; TaskType = "research"; BlockedPack = "science-medical-imaging" },
    [pscustomobject]@{ Name = "medical clinicaltrials blocked"; Prompt = "从 ClinicalTrials.gov 查询 NCT01234567 的终点和入排标准"; Grade = "M"; TaskType = "research"; BlockedPack = "science-medical-imaging" },
    [pscustomobject]@{ Name = "medical generic image processing blocked"; Prompt = "对普通 PNG 图片做 OCR、截图裁剪和图像增强，不涉及 DICOM、WSI、OMERO 或 PathML"; Grade = "M"; TaskType = "coding"; BlockedPack = "science-medical-imaging" },
```

- [ ] **Step 3: Add negative medical-imaging cases to `probe-scientific-packs.ps1`**

After the existing `imaging_pathml_wsi` case, add:

```powershell
    [pscustomobject]@{
        name = "imaging_generic_datacommons_blocked"
        group = "science-medical-imaging"
        prompt = "/vibe 用 Data Commons 查询 population indicators、statistical variables 和 DCID，不涉及 Imaging Data Commons 或 DICOMWeb"
        grade = "M"
        task_type = "research"
        expected_pack = $null
        expected_skill = $null
        blocked_pack = "science-medical-imaging"
        blocked_skill = "imaging-data-commons"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "imaging_pubmed_evidence_blocked"
        group = "science-medical-imaging"
        prompt = "/vibe 查询 PubMed 文献并整理 PMID citation evidence table"
        grade = "M"
        task_type = "research"
        expected_pack = $null
        expected_skill = $null
        blocked_pack = "science-medical-imaging"
        blocked_skill = $null
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "imaging_generic_image_processing_blocked"
        group = "science-medical-imaging"
        prompt = "/vibe 对普通 PNG 图片做 OCR、截图裁剪和图像增强，不涉及 DICOM、WSI、OMERO 或 PathML"
        grade = "M"
        task_type = "coding"
        expected_pack = $null
        expected_skill = $null
        blocked_pack = "science-medical-imaging"
        blocked_skill = $null
        requested_skill = $null
    },
```

- [ ] **Step 4: Run route script checks**

Run:

```powershell
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected result:

```text
all cases pass
```

If a blocked case selects a clearly correct neighboring owner, keep the blocked assertion and do not force `$null`. The key rule is that generic Data Commons, PubMed, ClinicalTrials, LaTeX/PDF, and generic image-processing prompts must not select `science-medical-imaging`.

- [ ] **Step 5: Commit verification script expansion**

Run:

```powershell
git add scripts/verify/vibe-pack-regression-matrix.ps1 scripts/verify/vibe-skill-index-routing-audit.ps1 scripts/verify/probe-scientific-packs.ps1
git diff --cached --check
git commit -m "test: expand medical imaging route regressions"
```

Expected result:

```text
Git creates a commit with message: test: expand medical imaging route regressions
```

## Task 5: Add Governance Note

**Files:**
- Create: `docs/governance/science-medical-imaging-pack-consolidation-2026-04-30.md`

- [ ] **Step 1: Create the governance note**

Create `docs/governance/science-medical-imaging-pack-consolidation-2026-04-30.md` with this content:

```markdown
# Science Medical Imaging Pack Consolidation

Date: 2026-04-30

## Conclusion

`science-medical-imaging` remains a 5-owner direct routing pack with no stage assistants.

This pass hardens route boundaries for DICOM/pydicom workflows, NCI Imaging Data Commons/IDC cohort retrieval, histolab WSI tile preprocessing, OMERO microscopy server workflows, and PathML computational pathology workflows.

This pass does not physically delete any of the 5 retained skill directories.

## Direct Owners

| Problem ID | User Task Boundary | Direct Owner |
|---|---|---|
| `dicom_file_workflow` | DICOM files, pydicom, DICOM tags, metadata extraction, anonymization, CT/MRI/PET/X-ray medical pixel data, PACS-oriented processing | `pydicom` |
| `cancer_imaging_data_commons` | NCI Imaging Data Commons, IDC, TCIA cancer imaging cohort, DICOMWeb, public radiology/pathology imaging cohorts | `imaging-data-commons` |
| `wsi_tile_preprocessing` | Histolab, whole-slide image tile extraction, tissue detection, H&E tile preprocessing, basic WSI dataset preparation | `histolab` |
| `omero_microscopy_server` | OMERO, microscopy image server, image datasets/projects, ROI annotations, high-content screening image management | `omero-integration` |
| `computational_pathology_workflow` | PathML, digital pathology workflow, WSI analysis pipeline, nucleus segmentation, tissue/cell graphs, spatial pathology, multiplex pathology | `pathml` |

## Simplified Routing State

```text
candidate skill -> selected skill -> used / unused
```

No extra routing state was added:

```text
stage_assistant_candidates = 0
advisory / consultation state = not used
primary / secondary skill hierarchy = not used
```

## Boundary Fixes

### DICOM / pydicom

`pydicom` owns DICOM files, tags, metadata, anonymization, pixel data, CT/MRI/PET/X-ray medical scans, and PACS-oriented workflows.

It should not own generic PNG/JPEG image processing, OCR, screenshots, PubMed, ClinicalTrials.gov, LaTeX/PDF builds, bioinformatics, chemistry, or generic Data Commons tasks.

### Imaging Data Commons

`imaging-data-commons` owns NCI Imaging Data Commons, IDC, TCIA cancer imaging cohorts, DICOMWeb, and cancer imaging dataset retrieval.

It should not own generic Data Commons statistical graph prompts, population indicators, statistical variables, DCIDs, broad public dataset search, PubMed, ClinicalTrials.gov, or finance/macro Data Commons prompts.

### Histolab vs PathML

`histolab` owns basic WSI tile extraction, tissue detection, H&E tile preprocessing, and quick tile dataset preparation.

`pathml` owns full computational pathology workflows, PathML pipelines, nucleus segmentation, spatial pathology, multiplex pathology, tissue graphs, and multiparametric imaging.

### OMERO

`omero-integration` owns OMERO server/API work, microscopy image server retrieval, ROI annotations, image metadata management, and high-content screening image management.

It should not own generic microscopy literature, DICOM/IDC retrieval, histolab tiling, PathML computational pathology, scRNA-seq, flow cytometry, or generic image processing.

## Verification Results

Run after implementation:

```powershell
python -m pytest tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py -q
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
git diff --check
```

Final verification evidence is added in a later commit after the commands in this note have been run.

## Evidence Boundary

This governance note proves routing configuration, bundled skill documentation, tests, and verification scripts were consolidated.

It does not prove that these skills were materially used in a real Vibe task. Material use still requires task-run artifacts such as specialist execution records, produced files, scripts, logs, figures, reports, or final deliverables.
```

- [ ] **Step 2: Commit the initial governance note**

Run:

```powershell
git add docs/governance/science-medical-imaging-pack-consolidation-2026-04-30.md
git diff --cached --check
git commit -m "docs: record medical imaging consolidation"
```

Expected result:

```text
Git creates a commit with message: docs: record medical imaging consolidation
```

## Task 6: Refresh Skills Lock

**Files:**
- Modify: `config/skills-lock.json`

- [ ] **Step 1: Regenerate the skills lock**

Run:

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected result:

```text
skills lock generated successfully
```

The exact skill count should remain stable because no skill directory is deleted.

- [ ] **Step 2: Inspect the lock diff**

Run:

```powershell
git diff -- config/skills-lock.json
```

Expected result:

```text
only hashes or metadata tied to the five edited medical-imaging skill files changed
```

If the diff shows removed skill entries, stop and inspect before committing. This pass does not delete skills.

- [ ] **Step 3: Run the offline skills gate**

Run:

```powershell
.\scripts\verify\vibe-offline-skills-gate.ps1
```

Expected result:

```text
present_skills equals lock_skills
```

- [ ] **Step 4: Commit the refreshed lock**

Run:

```powershell
git add config/skills-lock.json
git diff --cached --check
git commit -m "chore: refresh medical imaging skill lock"
```

Expected result:

```text
Git creates a commit with message: chore: refresh medical imaging skill lock
```

## Task 7: Full Verification And Final Governance Update

**Files:**
- Modify: `docs/governance/science-medical-imaging-pack-consolidation-2026-04-30.md`

- [ ] **Step 1: Run full verification**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py -q
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
git diff --check
```

Expected result:

```text
all commands pass
```

- [ ] **Step 2: Update the governance verification section**

Replace the `## Verification Results` section in `docs/governance/science-medical-imaging-pack-consolidation-2026-04-30.md` with exact observed command results from Step 1.

Use a table with these seven commands. Each `Result` cell must contain a concrete copied value from the just-run command output before the file is committed; do not leave descriptive template text in the governance note.

```markdown
## Verification Results

Passed on 2026-04-30:

| Command | Result |
|---|---|
| `python -m pytest tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py -q` | copied pytest pass summary, for example `N passed in X.XXs` |
| `.\scripts\verify\probe-scientific-packs.ps1` | copied probe summary from script output and `outputs\verify\route-probe-scientific\summary.json` |
| `.\scripts\verify\vibe-skill-index-routing-audit.ps1` | copied total/passed/failed summary |
| `.\scripts\verify\vibe-pack-regression-matrix.ps1` | copied total/passed/failed summary |
| `.\scripts\verify\vibe-pack-routing-smoke.ps1` | copied total/passed/failed summary |
| `.\scripts\verify\vibe-offline-skills-gate.ps1` | copied present_skills/lock_skills summary |
| `git diff --check` | `no whitespace errors` |
```

- [ ] **Step 3: Confirm no draft instruction text leaked into committed docs or tests**

Run:

```powershell
rg -n "copied pytest|copied probe|copied total|copied present|Final verification evidence is added|instruction cell|draft instruction" docs/governance/science-medical-imaging-pack-consolidation-2026-04-30.md tests/runtime_neutral/test_science_medical_imaging_pack_consolidation.py config/skill-keyword-index.json config/skill-routing-rules.json bundled/skills/pydicom/SKILL.md bundled/skills/imaging-data-commons/SKILL.md bundled/skills/histolab/SKILL.md bundled/skills/omero-integration/SKILL.md bundled/skills/pathml/SKILL.md
```

Expected result:

```text
no matches
```

- [ ] **Step 4: Commit final verification evidence**

Run:

```powershell
git add docs/governance/science-medical-imaging-pack-consolidation-2026-04-30.md
git diff --cached --check
git commit -m "docs: add medical imaging verification evidence"
```

Expected result:

```text
Git creates a commit with message: docs: add medical imaging verification evidence
```

## Task 8: Final State Report

**Files:**
- No file changes.

- [ ] **Step 1: Confirm clean worktree and recent commits**

Run:

```powershell
git status --short --branch
git log --oneline -8
```

Expected result:

```text
status output reports branch main against origin/main with a clean worktree
```

and the recent log includes the medical-imaging consolidation commits from this plan.

- [ ] **Step 2: Final answer to the user**

Report in Chinese with:

```text
已完成 science-medical-imaging 的实际整治。

保留：5 个 direct route owner。
保持：stage_assistant_candidates = []。
删除：本轮没有物理删除 skill 目录。
简化状态：仍然是 candidate skill -> selected skill -> used / unused。

已修复：
- pydicom 只稳定处理 DICOM/tag/metadata/anonymization/pixel/medical scan。
- imaging-data-commons 与 generic Data Commons 分清。
- histolab 与 pathml 的 WSI/pathology 分工稳定。
- omero-integration 需要 OMERO/server/API/ROI/image-server 信号。
- PubMed、ClinicalTrials、LaTeX/PDF、generic image processing、bioinformatics、chem/drug、generic ML 不再被 medical-imaging 抢。

已验证：
- Include each verification command from Task 7 with its observed pass summary.

边界说明：这证明路由和 bundled skills 清理完成，不证明真实 Vibe 任务中已经 material use。

提交：
- list the commit hashes and messages created during execution
```

Do not report this work as installed into Codex unless a separate install/deploy task is performed.

## Self-Review Checklist

- [ ] The plan keeps the existing six-stage Vibe runtime unchanged.
- [ ] The plan keeps routing semantics simple: `candidate skill -> selected skill -> used / unused`.
- [ ] The plan does not add `stage_assistant_candidates`, advisory mode, auxiliary experts, or main/sub-skill hierarchy.
- [ ] The plan keeps all 5 medical-imaging skills and physically deletes none.
- [ ] The plan adds a failing test before implementation.
- [ ] The plan hardens `pydicom` against generic image processing, reports, literature, clinical, bioinformatics, chemistry, and Data Commons prompts.
- [ ] The plan hardens `imaging-data-commons` against generic Data Commons and public dataset prompts.
- [ ] The plan protects the `histolab` vs `pathml` split.
- [ ] The plan protects `omero-integration` against generic microscopy literature and unrelated bio-image prompts.
- [ ] The plan includes focused tests, script regressions, skills lock refresh, and governance evidence.
- [ ] The plan separates routing/config cleanup from real task material skill use.
