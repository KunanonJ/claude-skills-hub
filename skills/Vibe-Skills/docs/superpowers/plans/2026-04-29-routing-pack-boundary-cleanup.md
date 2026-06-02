# Routing Pack Boundary Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make PDF, Markdown conversion, LaTeX manuscript builds, scientific reports, slides, figures, Figma implementation, and research-method prompts route to their intended packs without changing the public six-stage Vibe runtime.

**Architecture:** This is a config-first routing-boundary cleanup. Keep the simplified routing model as `skill_candidates -> skill_routing.selected -> skill_usage.used / unused`, add a narrow `design-implementation` pack for Figma-to-code, tighten `docs-media` so generic XL multi-document prompts do not become weak document fallbacks, and protect publishing/report/slides/figure boundaries with focused regression tests.

**Tech Stack:** Python `unittest` route probes through `vgo_runtime.router_contract_runtime.route_prompt`, PowerShell verification gates, JSON routing config files under `config/`, and Markdown governance docs.

---

## File Structure

- Create: `tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py`
  - Owns the new executable routing contract for docs, publishing, reporting, slides, figures, Figma implementation, and research-design boundaries.
- Modify: `config/pack-manifest.json`
  - Adds `design-implementation`.
  - Removes Figma implementation candidates from `research-design`.
  - Keeps `docs-media` XL-capable but relies on explicit file-operation signals.
- Modify: `config/skill-keyword-index.json`
  - Adds concrete Figma-to-code phrases and keeps document conversion / LaTeX / reporting keywords distinct.
- Modify: `config/skill-routing-rules.json`
  - Strengthens Figma implementation and adds negative guards against publishing fallback.
  - Tightens `xlsx`, `docx`, and `pdf` so extension-only generic prompts do not become weak route authority.
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`
  - Replaces the stale blanket `docs-media blocked in XL` case with explicit-request and generic-no-request boundary cases.
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
  - Updates stale Figma expectation to `design-implementation / figma-implement-design` and adds coding-mode coverage.
- Create: `docs/governance/2026-04-29-routing-pack-boundary-cleanup.md`
  - Records before/after ownership and the route probes protecting the new contract.

---

### Task 1: Add Focused Failing Routing Tests

**Files:**
- Create: `tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py`

- [ ] **Step 1: Write the failing test file**

Create `tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py` with this complete content:

```python
from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


def route(
    prompt: str,
    task_type: str = "research",
    grade: str = "L",
    requested_skill: str | None = None,
) -> dict[str, object]:
    return route_prompt(
        prompt=prompt,
        grade=grade,
        task_type=task_type,
        requested_skill=requested_skill,
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


class DocsResearchPublishingBoundaryRoutingTests(unittest.TestCase):
    def assert_selected(self, prompt: str, expected_pack: str, expected_skill: str, **kwargs: object) -> None:
        result = route(prompt, **kwargs)
        self.assertEqual((expected_pack, expected_skill), selected(result), ranked_summary(result))

    def test_existing_pdf_extraction_routes_to_pdf(self) -> None:
        self.assert_selected(
            "读取 PDF 并提取正文",
            "docs-media",
            "pdf",
            grade="XL",
            task_type="coding",
        )

    def test_pdf_to_markdown_routes_to_markitdown(self) -> None:
        self.assert_selected(
            "把 PDF 转成 Markdown",
            "docs-markitdown-conversion",
            "markitdown",
            grade="L",
            task_type="coding",
        )

    def test_latex_manuscript_pdf_build_routes_to_latex_pipeline(self) -> None:
        self.assert_selected(
            "用 LaTeX 写论文并构建 PDF",
            "scholarly-publishing-workflow",
            "latex-submission-pipeline",
            grade="XL",
            task_type="coding",
        )

    def test_scientific_report_routes_to_science_reporting(self) -> None:
        self.assert_selected(
            "科研技术报告：包含方法结果讨论，输出 HTML 和 PDF",
            "science-reporting",
            "scientific-reporting",
            grade="L",
            task_type="planning",
        )

    def test_slidev_pdf_export_routes_to_slides_as_code(self) -> None:
        self.assert_selected(
            "用 Slidev 做组会汇报并导出 PDF",
            "science-communication-slides",
            "slides-as-code",
            grade="L",
            task_type="coding",
        )

    def test_result_figures_route_to_scientific_visualization(self) -> None:
        self.assert_selected(
            "绘制机器学习模型评估结果图和投稿图",
            "science-figures-visualization",
            "scientific-visualization",
            grade="L",
            task_type="coding",
        )

    def test_figma_implementation_planning_routes_to_design_implementation(self) -> None:
        self.assert_selected(
            "把这个 Figma 设计稿还原为可运行代码",
            "design-implementation",
            "figma-implement-design",
            grade="L",
            task_type="planning",
        )

    def test_figma_implementation_coding_routes_to_design_implementation(self) -> None:
        self.assert_selected(
            "把这个 Figma 设计稿还原为可运行代码",
            "design-implementation",
            "figma-implement-design",
            grade="L",
            task_type="coding",
        )

    def test_quasi_experiment_design_stays_in_research_design(self) -> None:
        self.assert_selected(
            "帮我设计准实验方法，比较 DiD 和 ITS",
            "research-design",
            "designing-experiments",
            grade="L",
            task_type="planning",
        )

    def test_generic_xlsx_docx_parallel_prompt_is_not_docs_media_without_explicit_file_operation(self) -> None:
        result = route("xlsx and docx parallel processing", grade="XL", task_type="coding")
        self.assertNotEqual("docs-media", selected(result)[0], ranked_summary(result))

    def test_explicit_requested_xlsx_still_routes_to_docs_media_in_xl(self) -> None:
        self.assert_selected(
            "process xlsx workbook and preserve formulas",
            "docs-media",
            "xlsx",
            grade="XL",
            task_type="coding",
            requested_skill="xlsx",
        )
```

- [ ] **Step 2: Run the new test and confirm it fails for the known gaps**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py -q
```

Expected now: FAIL. At minimum, these assertions should fail before implementation:

```text
test_figma_implementation_coding_routes_to_design_implementation
  expected: design-implementation / figma-implement-design
  current known bad route: scholarly-publishing-workflow / latex-submission-pipeline

test_figma_implementation_planning_routes_to_design_implementation
  expected: design-implementation / figma-implement-design
  current known misplaced route: research-design / figma-implement-design

test_generic_xlsx_docx_parallel_prompt_is_not_docs_media_without_explicit_file_operation
  expected: selected pack is not docs-media
  current known route: docs-media / docx
```

- [ ] **Step 3: Commit the failing test**

```powershell
git add tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py
git commit -m "test: capture docs research publishing boundary routes"
```

---

### Task 2: Add A Narrow Design Implementation Pack

**Files:**
- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`

- [ ] **Step 1: Add `design-implementation` to `config/pack-manifest.json`**

Insert this pack before `research-design` so Figma-to-code has its own ownership surface and does not live under research methodology:

```json
{
  "id": "design-implementation",
  "priority": 98,
  "grade_allow": [
    "M",
    "L",
    "XL"
  ],
  "task_allow": [
    "planning",
    "coding"
  ],
  "trigger_keywords": [
    "figma",
    "figma to code",
    "implement design",
    "design implementation",
    "design to code",
    "frontend implementation",
    "Figma 设计稿",
    "figma设计稿",
    "设计稿还原",
    "还原为可运行代码",
    "设计转代码",
    "按 Figma 开发",
    "按figma开发",
    "UI 还原",
    "UI还原"
  ],
  "skill_candidates": [
    "figma-implement-design",
    "figma"
  ],
  "route_authority_candidates": [
    "figma-implement-design",
    "figma"
  ],
  "defaults_by_task": {
    "planning": "figma-implement-design",
    "coding": "figma-implement-design"
  }
}
```

- [ ] **Step 2: Remove Figma implementation from `research-design` candidates**

In the existing `research-design` block, remove only these entries from `skill_candidates`:

```json
"figma",
"figma-implement-design",
```

Do not remove `designing-experiments`, `research-grants`, `performing-causal-analysis`, `performing-regression-analysis`, `hypothesis-generation`, or `research-lookup`.

- [ ] **Step 3: Strengthen Figma keywords in `config/skill-keyword-index.json`**

Replace the `figma-implement-design` keyword list with:

```json
"figma-implement-design": {
  "keywords": [
    "figma to code",
    "implement design",
    "design implementation",
    "design to code",
    "frontend implementation",
    "Figma 设计稿",
    "figma设计稿",
    "设计稿还原",
    "figma实现",
    "按figma开发",
    "按 Figma 开发",
    "还原代码",
    "还原为可运行代码",
    "设计转代码",
    "UI还原"
  ]
}
```

Keep the existing `figma` entry if present. It may remain a route candidate for Figma context handling.

- [ ] **Step 4: Strengthen Figma routing rules in `config/skill-routing-rules.json`**

Replace the `figma-implement-design` rule with:

```json
"figma-implement-design": {
  "task_allow": [
    "coding",
    "planning"
  ],
  "positive_keywords": [
    "figma",
    "figma to code",
    "implement design",
    "design implementation",
    "design to code",
    "frontend implementation",
    "Figma 设计稿",
    "figma设计稿",
    "设计稿还原",
    "还原设计稿",
    "还原为可运行代码",
    "可运行代码",
    "设计转代码",
    "按figma开发",
    "按 Figma 开发",
    "UI还原"
  ],
  "negative_keywords": [
    "quasi-experimental",
    "difference-in-differences",
    "DiD",
    "ITS",
    "准实验",
    "中断时间序列",
    "合成控制"
  ],
  "equivalent_group": "figma-workflow",
  "canonical_for_task": [
    "coding",
    "planning"
  ]
}
```

- [ ] **Step 5: Add publishing fallback guards**

In `config/skill-routing-rules.json`, add these Figma/design implementation phrases to `latex-submission-pipeline.negative_keywords`:

```json
"figma",
"figma to code",
"Figma 设计稿",
"figma设计稿",
"设计稿还原",
"还原为可运行代码",
"设计转代码",
"UI还原"
```

Also add the same phrases to `scholarly-publishing.negative_keywords` if that rule exists. This prevents high-priority publishing fallback from stealing implementation prompts when no LaTeX terms are present.

- [ ] **Step 6: Run the focused Figma tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py::DocsResearchPublishingBoundaryRoutingTests::test_figma_implementation_planning_routes_to_design_implementation tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py::DocsResearchPublishingBoundaryRoutingTests::test_figma_implementation_coding_routes_to_design_implementation tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py::DocsResearchPublishingBoundaryRoutingTests::test_quasi_experiment_design_stays_in_research_design -q
```

Expected: PASS for all three tests.

- [ ] **Step 7: Commit the Figma pack boundary change**

```powershell
git add config/pack-manifest.json config/skill-keyword-index.json config/skill-routing-rules.json
git commit -m "fix: route figma implementation to design pack"
```

---

### Task 3: Tighten `docs-media` XL Generic Fallback

**Files:**
- Modify: `config/skill-routing-rules.json`
- Modify: `config/pack-manifest.json` only if the routing rules are insufficient

- [ ] **Step 1: Tighten `xlsx` route authority**

In `config/skill-routing-rules.json`, update the `xlsx` rule so bare extension mentions are not enough for route authority. Use this exact rule:

```json
"xlsx": {
  "task_allow": [
    "coding",
    "research"
  ],
  "positive_keywords": [
    "workbook",
    "preserve formulas",
    "excel file",
    "xlsx formatting",
    "spreadsheet formatting",
    "formula retention",
    "保留公式",
    "工作簿",
    "excel公式",
    "公式"
  ],
  "negative_keywords": [
    "docx",
    "markdown docs",
    "audio transcription",
    "large csv",
    "big csv",
    "streaming csv",
    "pdf",
    "parallel processing",
    "parallel",
    "generic orchestration",
    "并行处理",
    "批量编排"
  ],
  "requires_positive_keyword_match": true,
  "equivalent_group": "tabular-processing",
  "canonical_for_task": []
}
```

- [ ] **Step 2: Tighten `docx` route authority**

In `config/skill-routing-rules.json`, update the `docx` rule so bare extension mentions are not enough for route authority. Use this exact rule:

```json
"docx": {
  "task_allow": [
    "coding",
    "research"
  ],
  "positive_keywords": [
    "docx formatting",
    "layout fidelity",
    "tracked changes",
    "word document",
    "word formatting",
    "修订",
    "文档排版",
    "word文档",
    "格式保真"
  ],
  "negative_keywords": [
    "xlsx",
    "spreadsheet",
    "csv",
    "pdf",
    "screenshot",
    "批注",
    "回复批注",
    "comment reply",
    "comments.xml",
    "audio transcription",
    "parallel processing",
    "parallel",
    "generic orchestration",
    "并行处理",
    "批量编排"
  ],
  "requires_positive_keyword_match": true,
  "equivalent_group": "doc-authoring",
  "canonical_for_task": []
}
```

- [ ] **Step 3: Tighten `pdf` route authority without breaking extraction**

In `config/skill-routing-rules.json`, update the `pdf` rule so PDF extraction still routes, while generic PDF output and LaTeX build prompts remain outside `docs-media`. Use this exact rule:

```json
"pdf": {
  "task_allow": [
    "coding",
    "research"
  ],
  "positive_keywords": [
    "pdf extract",
    "pdf extraction",
    "extract text",
    "render pages",
    "读取pdf",
    "读取 PDF",
    "提取pdf文本",
    "提取 PDF 文本",
    "提取正文",
    "pdf正文",
    "PDF 正文"
  ],
  "negative_keywords": [
    "audio transcription",
    "docx",
    "word",
    "xlsx",
    "spreadsheet",
    "csv",
    "screenshot",
    "markitdown",
    "convert to markdown",
    "pdf to markdown",
    "docx to markdown",
    "markdown",
    "转成markdown",
    "转成 markdown",
    "markdown转换",
    "latex",
    "latexmk",
    "tex",
    "LaTeX 论文",
    "LaTeX 写论文",
    "论文 PDF",
    "PDF 构建",
    "生成论文 PDF",
    "编译论文",
    "论文编译",
    "compile latex",
    "build pdf",
    "paper build",
    "manuscript build"
  ],
  "requires_positive_keyword_match": true,
  "equivalent_group": null,
  "canonical_for_task": []
}
```

- [ ] **Step 4: Run focused docs-media boundary tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py::DocsResearchPublishingBoundaryRoutingTests::test_existing_pdf_extraction_routes_to_pdf tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py::DocsResearchPublishingBoundaryRoutingTests::test_generic_xlsx_docx_parallel_prompt_is_not_docs_media_without_explicit_file_operation tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py::DocsResearchPublishingBoundaryRoutingTests::test_explicit_requested_xlsx_still_routes_to_docs_media_in_xl -q
```

Expected: PASS for all three tests.

- [ ] **Step 5: Only if Step 4 still selects `docs-media` for the generic XL case, reduce pack-level extension-only triggers**

If the generic case still selects `docs-media`, edit `config/pack-manifest.json` and remove only these three bare extension trigger keywords from `docs-media.trigger_keywords`:

```json
"docx",
"pdf",
"xlsx"
```

Keep explicit triggers such as:

```json
"pdf extract",
"pdf extraction",
"extract text",
"读取pdf",
"读取 PDF",
"提取pdf文本",
"提取 PDF 文本",
"提取正文",
"PDF 正文",
"spreadsheet",
"excel",
"表格",
"电子表格",
"批注",
"回复批注"
```

Then rerun the command from Step 4 and expect PASS.

- [ ] **Step 6: Commit the docs-media boundary change**

```powershell
git add config/pack-manifest.json config/skill-routing-rules.json
git commit -m "fix: tighten docs media xl fallback"
```

---

### Task 4: Update Existing PowerShell Gate Expectations

**Files:**
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`

- [ ] **Step 1: Replace stale `docs-media blocked in XL` case**

In `scripts/verify/vibe-pack-regression-matrix.ps1`, replace the existing case:

```powershell
[pscustomobject]@{ Name = "docs-media blocked in XL"; Prompt = "xlsx and docx parallel processing"; Grade = "XL"; TaskType = "coding"; RequestedSkill = "xlsx"; ExpectedPack = $null; AllowedModes = @("legacy_fallback", "confirm_required"); BlockedPack = "docs-media" },
```

with these two cases:

```powershell
[pscustomobject]@{ Name = "docs-media explicit requested xlsx XL"; Prompt = "process xlsx workbook and preserve formulas"; Grade = "XL"; TaskType = "coding"; RequestedSkill = "xlsx"; ExpectedPack = "docs-media"; ExpectedSkill = "xlsx"; AllowedModes = @("pack_overlay", "confirm_required") },
[pscustomobject]@{ Name = "docs-media generic multi-doc XL not weak owner"; Prompt = "xlsx and docx parallel processing"; Grade = "XL"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = $null; AllowedModes = @("pack_overlay", "legacy_fallback", "confirm_required"); BlockedPack = "docs-media" },
```

- [ ] **Step 2: Update stale Figma skill-index audit expectation**

In `scripts/verify/vibe-skill-index-routing-audit.ps1`, replace:

```powershell
[pscustomobject]@{ Name = "figma implementation"; Prompt = "把这个Figma设计稿还原为可运行代码"; Grade = "L"; TaskType = "planning"; ExpectedPack = "research-design"; ExpectedSkill = "designing-experiments" },
```

with:

```powershell
[pscustomobject]@{ Name = "figma implementation planning"; Prompt = "把这个Figma设计稿还原为可运行代码"; Grade = "L"; TaskType = "planning"; ExpectedPack = "design-implementation"; ExpectedSkill = "figma-implement-design" },
[pscustomobject]@{ Name = "figma implementation coding"; Prompt = "把这个Figma设计稿还原为可运行代码"; Grade = "L"; TaskType = "coding"; ExpectedPack = "design-implementation"; ExpectedSkill = "figma-implement-design" },
```

Keep the existing experiment-design case:

```powershell
[pscustomobject]@{ Name = "experiment design"; Prompt = "帮我设计准实验方法，比较DiD和ITS"; Grade = "L"; TaskType = "planning"; ExpectedPack = "research-design"; ExpectedSkill = "designing-experiments" }
```

- [ ] **Step 3: Run the two gate scripts that previously failed**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected:

```text
vibe-pack-regression-matrix.ps1: 0 failed
vibe-skill-index-routing-audit.ps1: 0 failed
```

- [ ] **Step 4: Commit gate expectation updates**

```powershell
git add scripts/verify/vibe-pack-regression-matrix.ps1 scripts/verify/vibe-skill-index-routing-audit.ps1
git commit -m "test: update routing boundary gate expectations"
```

---

### Task 5: Add Governance Note

**Files:**
- Create: `docs/governance/2026-04-29-routing-pack-boundary-cleanup.md`

- [ ] **Step 1: Write the governance note**

Create `docs/governance/2026-04-29-routing-pack-boundary-cleanup.md` with this complete content:

````markdown
# Routing Pack Boundary Cleanup

Date: 2026-04-29

## Scope

This cleanup clarifies routing ownership for document media, Figma implementation, publishing, reporting, slides, figures, and research-method prompts.

It does not change the public six-stage Vibe runtime and does not change the simplified skill-use contract:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / unused
```

It also does not delete skill directories.

## Ownership Contract

| User intent | Pack | Skill |
| --- | --- | --- |
| Read or extract existing PDF text | `docs-media` | `pdf` |
| Convert PDF or DOCX to Markdown | `docs-markitdown-conversion` | `markitdown` |
| Compile a LaTeX manuscript PDF | `scholarly-publishing-workflow` | `latex-submission-pipeline` |
| Write scientific or technical report with HTML/PDF output | `science-reporting` | `scientific-reporting` |
| Build Slidev / slides-as-code deck and export PDF | `science-communication-slides` | `slides-as-code` |
| Build publication/result/model-evaluation figures | `science-figures-visualization` | `scientific-visualization` |
| Implement Figma/design mockup as code | `design-implementation` | `figma-implement-design` |
| Design quasi-experimental methodology | `research-design` | `designing-experiments` |

## Boundary Decisions

`docs-media` remains XL-capable for explicit existing-file operations, including PDF extraction and requested XLSX workbook edits. It should not own generic XL multi-document orchestration from extension-only prompts.

`design-implementation` owns Figma-to-code and design implementation prompts. Figma implementation no longer lives under `research-design`.

`research-design` remains responsible for research methods, experiment design, causal design, hypothesis generation, and grant planning.

`scholarly-publishing-workflow` owns submission, rebuttal, venue template, camera-ready, manuscript-as-code, and LaTeX manuscript build workflows. It should not steal figures, slides, reports, PDF extraction, PDF-to-Markdown, or Figma implementation.

## Regression Evidence

Protected by:

```text
tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py
scripts/verify/vibe-pack-regression-matrix.ps1
scripts/verify/vibe-skill-index-routing-audit.ps1
```

Required acceptance probes:

```text
读取 PDF 并提取正文 -> docs-media / pdf
把 PDF 转成 Markdown -> docs-markitdown-conversion / markitdown
用 LaTeX 写论文并构建 PDF -> scholarly-publishing-workflow / latex-submission-pipeline
科研技术报告：包含方法结果讨论，输出 HTML 和 PDF -> science-reporting / scientific-reporting
用 Slidev 做组会汇报并导出 PDF -> science-communication-slides / slides-as-code
绘制机器学习模型评估结果图和投稿图 -> science-figures-visualization / scientific-visualization
把这个 Figma 设计稿还原为可运行代码 -> design-implementation / figma-implement-design
帮我设计准实验方法，比较 DiD 和 ITS -> research-design / designing-experiments
xlsx and docx parallel processing -> not docs-media without explicit file-operation or requested skill
process xlsx workbook and preserve formulas, requested xlsx -> docs-media / xlsx
```
````

- [ ] **Step 2: Commit the governance note**

```powershell
git add docs/governance/2026-04-29-routing-pack-boundary-cleanup.md
git commit -m "docs: record routing pack boundary contract"
```

---

### Task 6: Run Full Verification

**Files:**
- Verify only; no edits expected.

- [ ] **Step 1: Run focused Python routing tests**

```powershell
python -m pytest tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py -q
python -m pytest tests/runtime_neutral/test_scientific_visualization_latex_routing.py -q
```

Expected:

```text
tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py: all tests passed
tests/runtime_neutral/test_scientific_visualization_latex_routing.py: 7 passed
```

- [ ] **Step 2: Run existing runtime-neutral contract tests**

```powershell
python -m pytest tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_python_validation_contract.py tests/runtime_neutral/test_simplified_skill_routing_contract.py -q
```

Expected: all tests passed.

- [ ] **Step 3: Run routing gates**

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
```

Expected:

```text
vibe-pack-regression-matrix.ps1: 0 failed
vibe-skill-index-routing-audit.ps1: 0 failed
vibe-pack-routing-smoke.ps1: 0 failed
```

- [ ] **Step 4: Run config/package gates**

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1
git diff --check
```

Expected:

```text
vibe-offline-skills-gate.ps1: PASS
vibe-config-parity-gate.ps1: PASS
git diff --check: no output
```

- [ ] **Step 5: Inspect final status and commit any remaining verification-only expectation fixes**

```powershell
git status --short
```

Expected: clean worktree after the final implementation commits.

If a verification gate exposes another stale expectation directly caused by this cleanup, update that expectation with a narrow explanation in the commit message:

```powershell
git add <changed-gate-file>
git commit -m "test: align stale routing expectation with boundary contract"
```

Do not broaden the cleanup to unrelated packs in this task.

---

## Self-Review

Spec coverage:

- `docs-media` XL policy is covered by Task 1, Task 3, and Task 4.
- Figma implementation leaving `research-design` is covered by Task 1, Task 2, and Task 4.
- `scholarly-publishing-workflow` not stealing figures, slides, reports, PDF extraction, PDF-to-Markdown, or Figma is covered by Task 1 and Task 2.
- PowerShell gate failures are covered by Task 4.
- Governance note is covered by Task 5.
- Full verification is covered by Task 6.

Placeholder scan:

- No placeholder markers or unspecified implementation steps remain.
- Every code or config change step includes exact file paths and concrete snippets.

Type and naming consistency:

- The new pack id is consistently `design-implementation`.
- The selected Figma skill remains `figma-implement-design`.
- The research-method owner remains `research-design / designing-experiments`.
- The simplified skill usage model remains `skill_candidates -> skill_routing.selected -> skill_usage.used / unused`.
