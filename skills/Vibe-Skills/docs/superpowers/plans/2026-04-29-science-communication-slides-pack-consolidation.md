# Science Communication Slides Pack Consolidation Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Shrink `science-communication-slides` into a focused scientific-presentation pack that owns slide decks, slides-as-code, explicit PPTX posters, and explicit infographics while removing Mermaid, MarkItDown, document dispatcher, and general image-generation noise.

**Architecture:** Add focused route tests first, then shrink `skill_candidates` directly because the current router does not use `route_authority_candidates` as an exclusion filter. Tighten pack triggers and per-skill routing rules so slide prompts stay in `science-communication-slides`, flowcharts and result figures route to `science-figures-visualization`, file conversion routes to `docs-markitdown-conversion`, and ordinary research posters route to `scholarly-publishing-workflow / latex-posters`. This pass changes routing/config/tests/docs only; it does not delete bundled skill directories or change the six-stage Vibe runtime.

**Tech Stack:** Python `unittest`/pytest route tests, PowerShell route-probe scripts, JSON config files, Markdown governance docs.

---

## File Map

- Create: `tests/runtime_neutral/test_science_communication_slides_pack_consolidation.py`
- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`
- Modify: `scripts/verify/probe-scientific-packs.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
- Create: `docs/governance/science-communication-slides-pack-consolidation-2026-04-29.md`
- Optionally modify: `config/skills-lock.json` only if `.\scripts\verify\vibe-generate-skills-lock.ps1` produces a real diff.

No bundled skill directory should be physically deleted in this plan.

## Task 1: Add Focused Failing Tests

**Files:**
- Create: `tests/runtime_neutral/test_science_communication_slides_pack_consolidation.py`

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
    "scientific-slides",
    "slides-as-code",
    "pptx-posters",
    "infographics",
]

MOVED_OUT_SKILLS = [
    "markdown-mermaid-writing",
    "markitdown",
    "document-skills",
    "generate-image",
]

REMOVED_PACK_TRIGGERS = [
    "poster",
    "infographic",
    "mermaid",
    "diagram",
    "flowchart",
    "海报",
    "信息图",
    "流程图",
    "示意图",
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


class ScienceCommunicationSlidesPackConsolidationTests(unittest.TestCase):
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

    def assert_not_science_communication(
        self,
        prompt: str,
        *,
        task_type: str = "research",
        grade: str = "L",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertNotEqual("science-communication-slides", selected(result)[0], ranked_summary(result))

    def test_manifest_shrinks_to_four_route_owners(self) -> None:
        pack = pack_by_id("science-communication-slides")
        self.assertEqual(KEPT_SKILLS, pack.get("skill_candidates"))
        self.assertEqual(KEPT_SKILLS, pack.get("route_authority_candidates"))
        self.assertEqual([], pack.get("stage_assistant_candidates"))

    def test_manifest_removes_moved_out_skills(self) -> None:
        pack = pack_by_id("science-communication-slides")
        candidates = set(pack.get("skill_candidates") or [])
        for skill in MOVED_OUT_SKILLS:
            self.assertNotIn(skill, candidates)

    def test_pack_triggers_are_slide_specific(self) -> None:
        pack = pack_by_id("science-communication-slides")
        triggers = set(pack.get("trigger_keywords") or [])
        for keyword in REMOVED_PACK_TRIGGERS:
            self.assertNotIn(keyword, triggers)
        for keyword in ["slides", "slide deck", "ppt", "pptx", "powerpoint", "slidev", "marp", "reveal.js", "幻灯片", "演示文稿", "组会汇报", "答辩"]:
            self.assertIn(keyword, triggers)

    def test_defaults_match_kept_slide_owners(self) -> None:
        pack = pack_by_id("science-communication-slides")
        self.assertEqual(
            {
                "planning": "scientific-slides",
                "coding": "slides-as-code",
                "research": "scientific-slides",
            },
            pack.get("defaults_by_task"),
        )

    def test_scientific_slide_deck_routes_to_scientific_slides(self) -> None:
        self.assert_selected(
            "顶级PPT制作：组会汇报 slide deck，需要讲述结构与视觉规范",
            "science-communication-slides",
            "scientific-slides",
            task_type="planning",
            grade="L",
        )

    def test_slidev_pdf_export_routes_to_slides_as_code(self) -> None:
        self.assert_selected(
            "用 Slidev 做组会汇报并导出 PDF",
            "science-communication-slides",
            "slides-as-code",
            task_type="coding",
            grade="L",
        )

    def test_marp_pdf_export_routes_to_slides_as_code(self) -> None:
        self.assert_selected(
            "用 Marp 做科研 presentation 并导出 PDF",
            "science-communication-slides",
            "slides-as-code",
            task_type="coding",
            grade="L",
        )

    def test_pptx_poster_routes_to_pptx_posters(self) -> None:
        self.assert_selected(
            "制作 PowerPoint PPTX 学术海报",
            "science-communication-slides",
            "pptx-posters",
            task_type="planning",
            grade="L",
        )

    def test_plain_conference_poster_routes_to_latex_posters(self) -> None:
        self.assert_selected(
            "制作学术海报 conference poster",
            "scholarly-publishing-workflow",
            "latex-posters",
            task_type="planning",
            grade="L",
        )

    def test_explicit_infographic_routes_to_infographics(self) -> None:
        self.assert_selected(
            "做一个研究结论信息图 infographic visual summary",
            "science-communication-slides",
            "infographics",
            task_type="planning",
            grade="L",
        )

    def test_mermaid_flowchart_leaves_slides_pack(self) -> None:
        self.assert_selected(
            "用 Mermaid 写一个实验流程图 flowchart，并给出可复制的 markdown",
            "science-figures-visualization",
            "scientific-schematics",
            task_type="coding",
            grade="M",
        )

    def test_mechanism_flowchart_routes_to_scientific_schematics(self) -> None:
        self.assert_selected(
            "画一个机制示意图和流程图",
            "science-figures-visualization",
            "scientific-schematics",
            task_type="planning",
            grade="L",
        )

    def test_result_figures_route_to_scientific_visualization(self) -> None:
        self.assert_selected(
            "绘制机器学习模型评估结果图和投稿图",
            "science-figures-visualization",
            "scientific-visualization",
            task_type="coding",
            grade="L",
        )

    def test_pdf_to_markdown_routes_to_markitdown_pack(self) -> None:
        self.assert_selected(
            "把 PDF 转成 Markdown，要求保留表格与标题结构",
            "docs-markitdown-conversion",
            "markitdown",
            task_type="coding",
            grade="M",
        )

    def test_general_image_generation_does_not_route_to_slides_pack(self) -> None:
        self.assert_not_science_communication(
            "生成一张产品概念图 image generation",
            task_type="planning",
            grade="M",
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused tests and verify they fail for the current reason**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_communication_slides_pack_consolidation.py -q
```

Expected before implementation: FAIL. The failures should include at least:

```text
test_manifest_shrinks_to_four_route_owners
test_pack_triggers_are_slide_specific
test_defaults_match_kept_slide_owners
```

The current repo still has 8 candidates, broad pack triggers, and `coding -> markdown-mermaid-writing`.

- [ ] **Step 3: Commit the failing test**

Run:

```powershell
git add tests/runtime_neutral/test_science_communication_slides_pack_consolidation.py
git commit -m "test: cover science communication slides boundaries"
```

Expected: commit succeeds with only the new test file staged.

## Task 2: Shrink The Pack Manifest

**Files:**
- Modify: `config/pack-manifest.json`

- [ ] **Step 1: Replace only the `science-communication-slides` pack block**

Use `apply_patch` to update the block whose `"id"` is `"science-communication-slides"` to this contract:

```json
{
  "id": "science-communication-slides",
  "priority": 85,
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
    "slides",
    "slide deck",
    "ppt",
    "pptx",
    "powerpoint",
    "presentation",
    "talk",
    "seminar",
    "defense",
    "slidev",
    "marp",
    "reveal.js",
    "quarto slides",
    "slides as code",
    "幻灯片",
    "演示文稿",
    "组会汇报",
    "答辩",
    "路演",
    "学术报告"
  ],
  "skill_candidates": [
    "scientific-slides",
    "slides-as-code",
    "pptx-posters",
    "infographics"
  ],
  "route_authority_candidates": [
    "scientific-slides",
    "slides-as-code",
    "pptx-posters",
    "infographics"
  ],
  "stage_assistant_candidates": [],
  "defaults_by_task": {
    "planning": "scientific-slides",
    "coding": "slides-as-code",
    "research": "scientific-slides"
  }
}
```

Keep the existing JSON formatting style used by the file. Do not touch unrelated packs.

- [ ] **Step 2: Run the focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_communication_slides_pack_consolidation.py -q
```

Expected: manifest tests pass. Route tests may still fail until keyword and rule edits are complete.

- [ ] **Step 3: Commit the manifest change**

Run:

```powershell
git add config/pack-manifest.json
git commit -m "fix: shrink science communication slides pack"
```

Expected: commit succeeds with only `config/pack-manifest.json` staged.

## Task 3: Tighten Keyword Index And Routing Rules

**Files:**
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`

- [ ] **Step 1: Update `config/skill-keyword-index.json` entries for kept skills**

Use `apply_patch` to replace the four skill entries with these keyword lists:

```json
"scientific-slides": {
  "keywords": ["scientific slides", "slide deck", "ppt", "pptx", "powerpoint", "presentation", "research talk", "seminar talk", "defense slides", "group meeting slides", "科研幻灯片", "学术幻灯片", "组会汇报", "答辩幻灯片", "路演PPT"]
},
"pptx-posters": {
  "keywords": ["pptx poster", "powerpoint poster", "ppt poster", "PPT海报", "PowerPoint海报", "可编辑海报"]
},
"infographics": {
  "keywords": ["infographic", "visual summary", "visual one-pager", "research summary graphic", "信息图", "可视化总结", "视觉摘要"]
},
```

Keep the existing `slides-as-code` entry but expand it to:

```json
"slides-as-code": {
  "keywords": ["slidev", "marp", "reveal.js", "quarto slides", "decktape", "slides as code", "text-first slides", "markdown slides", "组会汇报", "导出pdf", "可复现幻灯片", "源码化幻灯片"]
},
```

Do not delete the global entries for `markdown-mermaid-writing`, `markitdown`, `document-skills`, or `generate-image`; they are only removed from this pack.

- [ ] **Step 2: Update `config/skill-routing-rules.json` for `scientific-slides`**

Use `apply_patch` to replace the `scientific-slides` rule with:

```json
"scientific-slides": {
  "task_allow": [
    "planning",
    "research"
  ],
  "positive_keywords": [
    "slides",
    "slide deck",
    "ppt",
    "pptx",
    "powerpoint",
    "presentation",
    "research talk",
    "seminar",
    "defense",
    "grant pitch",
    "roadshow",
    "group meeting",
    "幻灯片",
    "演示文稿",
    "组会汇报",
    "答辩",
    "路演",
    "学术报告"
  ],
  "negative_keywords": [
    "excel",
    "xlsx",
    "markitdown",
    "pdf to markdown",
    "docx to markdown",
    "mermaid",
    "flowchart",
    "diagram",
    "schematic",
    "示意图",
    "流程图",
    "投稿图",
    "结果图",
    "600dpi",
    "tiff"
  ],
  "equivalent_group": "science-communication",
  "canonical_for_task": [
    "planning",
    "research"
  ]
}
```

- [ ] **Step 3: Update `config/skill-routing-rules.json` for `slides-as-code`**

Replace the `slides-as-code` rule with:

```json
"slides-as-code": {
  "task_allow": [
    "planning",
    "coding",
    "research"
  ],
  "positive_keywords": [
    "slides as code",
    "slidev",
    "marp",
    "reveal.js",
    "quarto slides",
    "decktape",
    "md slides",
    "markdown slides",
    "text-first slides",
    "pdf export",
    "export pdf",
    "deck",
    "speaker notes",
    "演示文稿",
    "幻灯片",
    "组会汇报",
    "导出 PDF",
    "可复现导出"
  ],
  "negative_keywords": [
    "tiff",
    "600dpi",
    "subplot",
    "figure",
    "poster",
    "conference poster",
    "academic poster",
    "beamerposter",
    "tikzposter",
    "mermaid",
    "flowchart",
    "diagram",
    "示意图",
    "流程图"
  ],
  "equivalent_group": "slides",
  "canonical_for_task": [
    "coding"
  ]
}
```

- [ ] **Step 4: Update `config/skill-routing-rules.json` for `pptx-posters`**

Replace the `pptx-posters` rule with:

```json
"pptx-posters": {
  "task_allow": [
    "planning",
    "coding",
    "research"
  ],
  "positive_keywords": [
    "pptx poster",
    "powerpoint poster",
    "ppt poster",
    "editable powerpoint poster",
    "PPT海报",
    "PowerPoint海报",
    "可编辑海报"
  ],
  "negative_keywords": [
    "latex",
    "beamerposter",
    "tikzposter",
    "baposter",
    "conference poster",
    "academic poster",
    "research poster",
    "学术海报",
    "科研海报",
    "会议海报",
    "dicom",
    "clinicaltrials"
  ],
  "equivalent_group": "science-communication",
  "canonical_for_task": [
    "planning",
    "coding"
  ]
}
```

The negative keywords intentionally push ordinary academic-poster prompts to `latex-posters`. `制作 PowerPoint PPTX 学术海报` still selects `pptx-posters` because it contains strong positive PowerPoint/PPTX signals.

- [ ] **Step 5: Update `config/skill-routing-rules.json` for `infographics`**

Replace the `infographics` rule with:

```json
"infographics": {
  "task_allow": [
    "planning",
    "research"
  ],
  "positive_keywords": [
    "infographic",
    "visual summary",
    "visual one-pager",
    "research summary graphic",
    "information graphic",
    "信息图",
    "可视化总结",
    "视觉摘要"
  ],
  "negative_keywords": [
    "unit test",
    "pytest",
    "subplot",
    "multi-panel",
    "result figure",
    "publication figure",
    "model evaluation plot",
    "flowchart",
    "schematic",
    "diagram",
    "投稿图",
    "结果图",
    "流程图",
    "示意图"
  ],
  "equivalent_group": "science-communication",
  "canonical_for_task": [
    "planning",
    "research"
  ]
}
```

- [ ] **Step 6: Run focused tests and inspect any route miss**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_communication_slides_pack_consolidation.py -q
```

Expected after this task: all focused tests pass. If `test_pptx_poster_routes_to_pptx_posters` fails by selecting `scientific-slides`, strengthen only `pptx-posters` positives or add `poster` / `海报` to `scientific-slides.negative_keywords`. Do not add broad `poster` back to pack triggers.

- [ ] **Step 7: Commit keyword and routing rule changes**

Run:

```powershell
git add config/skill-keyword-index.json config/skill-routing-rules.json
git commit -m "fix: tighten science communication slide routing"
```

Expected: commit succeeds with only the two config files staged.

## Task 4: Update Route Probe Scripts

**Files:**
- Modify: `scripts/verify/probe-scientific-packs.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`

- [ ] **Step 1: Update `scripts/verify/probe-scientific-packs.ps1` communication rows**

Find the `# science-communication-slides` block. Keep `comm_scientific_slides`, replace the old `comm_mermaid_flowchart` row, and add PPTX poster and plain poster rows so the block contains these objects:

```powershell
[pscustomobject]@{
    name = "comm_scientific_slides"
    group = "science-communication-slides"
    prompt = "/vibe 把这篇论文做成 10 页学术汇报 slides（pptx），包含方法/结果/局限性"
    grade = "L"
    task_type = "planning"
    expected_pack = "science-communication-slides"
    expected_skill = "scientific-slides"
    requested_skill = $null
},
[pscustomobject]@{
    name = "comm_slidev_as_code"
    group = "science-communication-slides"
    prompt = "/vibe 用 Slidev 做组会汇报并导出 PDF"
    grade = "L"
    task_type = "coding"
    expected_pack = "science-communication-slides"
    expected_skill = "slides-as-code"
    requested_skill = $null
},
[pscustomobject]@{
    name = "figures_mermaid_flowchart"
    group = "science-figures-visualization"
    prompt = "/vibe 用 Mermaid 写一个实验流程图（flowchart），并给出可复制的 markdown"
    grade = "M"
    task_type = "coding"
    expected_pack = "science-figures-visualization"
    expected_skill = "scientific-schematics"
    requested_skill = $null
},
[pscustomobject]@{
    name = "comm_pptx_poster"
    group = "science-communication-slides"
    prompt = "/vibe 制作 PowerPoint PPTX 学术海报"
    grade = "L"
    task_type = "planning"
    expected_pack = "science-communication-slides"
    expected_skill = "pptx-posters"
    requested_skill = $null
},
[pscustomobject]@{
    name = "publishing_plain_conference_poster"
    group = "scholarly-publishing-workflow"
    prompt = "/vibe 制作学术海报 conference poster"
    grade = "L"
    task_type = "planning"
    expected_pack = "scholarly-publishing-workflow"
    expected_skill = "latex-posters"
    requested_skill = $null
},
```

Keep the existing `comm_pdf_to_markdown` row if it is still useful as a document-conversion guard.

- [ ] **Step 2: Add three audit rows to `scripts/verify/vibe-skill-index-routing-audit.ps1`**

Immediately after the existing `top ppt deck` and `slidev slides as code` rows, add:

```powershell
[pscustomobject]@{ Name = "pptx poster"; Prompt = "制作PowerPoint PPTX学术海报，需要可编辑PPT输出"; Grade = "L"; TaskType = "planning"; ExpectedPack = "science-communication-slides"; ExpectedSkill = "pptx-posters" },
[pscustomobject]@{ Name = "plain conference poster"; Prompt = "制作学术海报 conference poster，准备会议展示"; Grade = "L"; TaskType = "planning"; ExpectedPack = "scholarly-publishing-workflow"; ExpectedSkill = "latex-posters" },
[pscustomobject]@{ Name = "mermaid flowchart belongs to figures"; Prompt = "用Mermaid写一个实验流程图flowchart，并给出可复制markdown"; Grade = "M"; TaskType = "coding"; ExpectedPack = "science-figures-visualization"; ExpectedSkill = "scientific-schematics" },
```

- [ ] **Step 3: Run focused script probes**

Run:

```powershell
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected: both scripts pass. If a route miss occurs, fix the config rule causing the miss before proceeding.

- [ ] **Step 4: Commit probe updates**

Run:

```powershell
git add scripts/verify/probe-scientific-packs.ps1 scripts/verify/vibe-skill-index-routing-audit.ps1
git commit -m "test: update science communication route probes"
```

Expected: commit succeeds with only the two PowerShell scripts staged.

## Task 5: Add Governance Note

**Files:**
- Create: `docs/governance/science-communication-slides-pack-consolidation-2026-04-29.md`

- [ ] **Step 1: Add the governance note**

Use `apply_patch` to add this exact file:

````markdown
# Science Communication Slides Pack Consolidation

Date: 2026-04-29

## Summary

`science-communication-slides` was consolidated into a focused scientific presentation and communication-deliverable pack.

This cleanup keeps the six-stage Vibe runtime unchanged and preserves the binary usage model:

```text
skill_routing.selected -> skill_usage.used / unused
```

No `primary/secondary`, `consult`, `advisory`, or stage-assistant execution semantics were added.

## Before And After

| Field | Before | After |
| --- | ---: | ---: |
| `skill_candidates` | 8 | 4 |
| `route_authority_candidates` | 0 | 4 |
| `stage_assistant_candidates` | 0 | 0 |
| physical directory deletion | 0 | 0 |

## Kept Route Authorities

| Skill | Boundary |
| --- | --- |
| `scientific-slides` | Scientific slide decks, PowerPoint decks, research talks, group meetings, seminars, defenses, roadshows, grant pitches |
| `slides-as-code` | Slidev, Marp, Reveal.js, Quarto slides, text-first slide source, reproducible PDF export |
| `pptx-posters` | Explicit PPTX / PowerPoint / PPT poster requests where editable PowerPoint output is required |
| `infographics` | Explicit infographic, visual summary, or visual one-pager requests |

`route_authority_candidates` mirrors `skill_candidates` for compatibility and documentation. The actual simplification is enforced by shrinking `skill_candidates`.

## Moved Out

| Skill | New boundary |
| --- | --- |
| `markdown-mermaid-writing` | Documentation/reporting or figure/schematic boundaries; Mermaid flowcharts no longer route through the slides pack |
| `markitdown` | `docs-markitdown-conversion / markitdown` |
| `document-skills` | Document dispatcher surface, not a slide expert |
| `generate-image` | General image-generation surface, not a scientific slide route authority |

Moved-out skills remain on disk. They were not physically deleted because several contain scripts, references, templates, or assets.

## Protected Route Boundaries

| Prompt | Expected route |
| --- | --- |
| `顶级PPT制作：组会汇报 slide deck，需要讲述结构与视觉规范` | `science-communication-slides / scientific-slides` |
| `用 Slidev 做组会汇报并导出 PDF` | `science-communication-slides / slides-as-code` |
| `用 Marp 做科研 presentation 并导出 PDF` | `science-communication-slides / slides-as-code` |
| `制作 PowerPoint PPTX 学术海报` | `science-communication-slides / pptx-posters` |
| `制作学术海报 conference poster` | `scholarly-publishing-workflow / latex-posters` |
| `做一个研究结论信息图 infographic visual summary` | `science-communication-slides / infographics` |
| `用 Mermaid 写一个实验流程图 flowchart，并给出可复制的 markdown` | `science-figures-visualization / scientific-schematics` |
| `画一个机制示意图和流程图` | `science-figures-visualization / scientific-schematics` |
| `绘制机器学习模型评估结果图和投稿图` | `science-figures-visualization / scientific-visualization` |
| `把 PDF 转成 Markdown，要求保留表格与标题结构` | `docs-markitdown-conversion / markitdown` |

## Verification

Focused:

```powershell
python -m pytest tests/runtime_neutral/test_science_communication_slides_pack_consolidation.py -q
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

- [ ] **Step 2: Commit the governance note**

Run:

```powershell
git add docs/governance/science-communication-slides-pack-consolidation-2026-04-29.md
git commit -m "docs: record science communication slides boundary"
```

Expected: commit succeeds with only the governance file staged.

## Task 6: Run Full Verification And Commit Any Lock Diff

**Files:**
- Possibly modify: `config/skills-lock.json`

- [ ] **Step 1: Run the focused pytest again**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_communication_slides_pack_consolidation.py -q
```

Expected:

```text
15 passed
```

The exact count may be one higher or lower if the test file was adjusted during implementation, but all tests in the file must pass.

- [ ] **Step 2: Run broader routing probes**

Run:

```powershell
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
```

Expected: all probes pass. Report any failure by command name and failing route row.

- [ ] **Step 3: Regenerate lock if the repo expects it**

Run:

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
git status --short config/skills-lock.json
```

Expected: either no diff, or a real deterministic update to `config/skills-lock.json`. If a diff appears, inspect it with:

```powershell
git diff -- config/skills-lock.json
```

Only commit the lock file if the diff is directly caused by the current routing/config changes.

- [ ] **Step 4: Run offline/config gates and whitespace check**

Run:

```powershell
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

Expected: all gates pass and `git diff --check` prints no whitespace errors.

- [ ] **Step 5: Commit any lock diff if needed**

If `config/skills-lock.json` changed, run:

```powershell
git add config/skills-lock.json
git commit -m "chore: refresh skills lock after slides routing cleanup"
```

If no lock diff exists, skip this step and state that no lock commit was needed.

## Task 7: Final Review

**Files:**
- No new edits expected.

- [ ] **Step 1: Inspect final history and working tree**

Run:

```powershell
git status --short --branch
git log --oneline -n 8
```

Expected:

```text
## main...origin/main [ahead N]
```

with no unstaged or untracked files.

- [ ] **Step 2: Produce final implementation report**

Report these exact items:

```text
branch:
commits:
before/after counts:
kept route authorities:
stage assistants:
moved-out skills:
physical deletion:
verification:
remaining caveats:
```

Expected content:

```text
before/after counts: 8 candidates -> 4 candidates; 0 route authorities -> 4 route authorities; 0 stage assistants -> 0
kept route authorities: scientific-slides, slides-as-code, pptx-posters, infographics
stage assistants: none
moved-out skills: markdown-mermaid-writing, markitdown, document-skills, generate-image
physical deletion: none in this pass
remaining caveats: ordinary academic posters now route to latex-posters; PPTX/PowerPoint posters route to pptx-posters
```

Do not claim every remaining pack is clean. Only claim `science-communication-slides` routing/config cleanup if all verification commands passed.
