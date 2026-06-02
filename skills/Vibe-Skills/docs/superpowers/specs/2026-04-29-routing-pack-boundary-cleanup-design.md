# Routing Pack Boundary Cleanup Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-29

## 1. Goal

This design defines the next cleanup step for Vibe-Skills routing after the `scientific-visualization` and `latex-submission-pipeline` fix.

The goal is to clarify pack ownership where routing evidence still shows conflict:

```text
docs-media XL boundary
research-design non-research skill leakage
scholarly-publishing-workflow overlap with figures and slides
PDF / LaTeX / report / slides / Figma regression coverage
```

This is a routing-boundary cleanup. It must not change the public six-stage Vibe runtime, and it must not reintroduce primary/secondary/stage-assistant complexity. The authority model remains:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / unused
```

## 2. Current Evidence

The current branch is `main`, with the last routing fix committed as:

```text
b27130ea fix: route figures and latex builds to precise skills
```

Fresh probes showed three different evidence levels:

| Check | Result | Meaning |
| --- | --- | --- |
| `vibe-pack-routing-smoke.ps1` | 971 passed, 0 failed | broad config and smoke checks are healthy |
| `vibe-pack-regression-matrix.ps1` | 124 passed, 1 failed | a stricter pack boundary still conflicts with current config |
| `vibe-skill-index-routing-audit.ps1` | 170 passed, 1 failed | one skill-level expectation is stale or misplaced |
| `probe-scientific-packs.ps1` | 41 scientific cases, 100% pack/skill match | science and bio-science probes are currently stable |

The two concrete failures are:

```text
docs-media blocked in XL:
  prompt: xlsx and docx parallel processing
  grade: XL
  requested_skill: xlsx
  current: docs-media / xlsx
  old expectation: not docs-media

figma implementation:
  prompt: 把这个Figma设计稿还原为可运行代码
  grade: L
  task_type: planning
  current: research-design / figma-implement-design
  old expectation: research-design / designing-experiments
```

Additional probing showed a stronger issue for Figma in coding mode:

```text
prompt: 把这个Figma设计稿还原为可运行代码
grade: L
task_type: coding
current: scholarly-publishing-workflow / latex-submission-pipeline
```

That result is a real misroute. The planning-mode Figma result is more reasonable than the old test expectation, but the skill is sitting in the wrong pack boundary.

## 3. Problem Boundaries

### 3.1 docs-media XL Boundary

`docs-media` was expanded to include `XL` so explicit PDF extraction can route correctly in large composite tasks:

```text
读取 PDF 并提取正文 -> docs-media / pdf
```

This is useful, but it conflicts with an older policy that blocked `docs-media` from XL entirely. The old blanket block is too broad after the LaTeX/PDF fix.

The correct boundary should be narrower:

```text
explicit existing-file operations are allowed in XL
generic multi-document orchestration should not be owned by docs-media by default
```

### 3.2 research-design Non-Research Leakage

`research-design` currently contains research-method skills and unrelated implementation helpers in the same pack:

```text
designing-experiments
hypothesis-generation
research-grants
performing-causal-analysis
performing-regression-analysis
figma
figma-implement-design
playwright
property-based-testing
skill-creator
ux-researcher-designer
```

This makes the pack too broad. `figma-implement-design` can be a valid skill, but it does not belong under a research-method ownership surface. It should not be expected to route as `designing-experiments`, and it should not disappear for coding tasks.

### 3.3 Scholarly Publishing Overlap

`scholarly-publishing-workflow` still contains skills that overlap with specialized packs:

```text
scientific-visualization
scientific-schematics
scientific-slides
slides-as-code
```

The recent LaTeX fix made the most important paper-PDF route stable, but the pack remains structurally broad. It should primarily own publication workflow tasks:

```text
submission
rebuttal
revision
venue templates
LaTeX manuscript build
submission package
```

Scientific figures and slides should normally be owned by:

```text
science-figures-visualization
science-communication-slides
```

### 3.4 Document / Report / Slides / LaTeX Boundaries

These boundaries now work in focused probes, but they need regression protection because all of them contain `pdf`-like language:

| User intent | Desired owner |
| --- | --- |
| read or extract existing PDF | `docs-media / pdf` |
| convert PDF to Markdown | `docs-markitdown-conversion / markitdown` |
| compile LaTeX manuscript PDF | `scholarly-publishing-workflow / latex-submission-pipeline` |
| write scientific report with PDF output | `science-reporting / scientific-reporting` |
| build Slidev or slides-as-code deck and export PDF | `science-communication-slides / slides-as-code` |
| make result figures or model plots | `science-figures-visualization / scientific-visualization` |

## 4. Options

### Option A: Patch Only The Two Failing Tests

This would update the stale `figma implementation` expectation and the old `docs-media blocked in XL` expectation.

Tradeoff: fast, but it would only hide the structural issues. It would not fix the coding-mode Figma misroute or protect the overlapping PDF/report/slides boundaries.

### Option B: Boundary Cleanup With Focused Regression Expansion

This keeps the current architecture and makes narrow changes:

1. Redefine `docs-media` XL policy as explicit-file-only rather than blanket-blocked.
2. Move or reroute Figma implementation out of `research-design`, or make its pack/task boundary explicit.
3. Keep `scholarly-publishing-workflow` focused on publication and LaTeX build tasks.
4. Add focused regression cases for PDF, Markdown conversion, LaTeX, report, slides, Figma, and experiment design.

Tradeoff: slightly more work, but it directly addresses the failure evidence and prevents repeated boundary regressions.

### Option C: Broad Pack Restructure

This would split many packs at once: research, design, docs, publishing, slides, and front-end implementation.

Tradeoff: too large for this step. It increases risk and would make it harder to prove which change fixed which route.

## 5. Recommended Design

Use Option B.

The cleanup should be implemented as a narrow routing-boundary pass. It should not delete skill directories and should not change the six-stage runtime.

### 5.1 docs-media Rule

`docs-media` can remain XL-capable, but regression tests should distinguish explicit file operations from broad orchestration.

Allowed XL examples:

```text
读取 PDF 并提取正文 -> docs-media / pdf
process xlsx workbook and preserve formulas -> docs-media / xlsx
检查 Word 文档排版 -> docs-media / docx
```

Blocked or non-owner examples:

```text
xlsx and docx parallel processing -> not auto-owned by docs-media unless explicit file-operation terms are present
创建 Jupyter notebook 教程 -> not docs-media
```

If config cannot express this cleanly, prefer adjusting trigger/rule negative keywords before changing runtime code.

### 5.2 research-design Rule

`research-design` should own research-method and research-planning problems:

```text
experimental design
quasi-experimental design
DiD / ITS / synthetic control
hypothesis generation
research grant structure
literature matrix
methodology critique
```

It should not own UI implementation work as a research-design problem. The implementation should create a narrow routing owner for this surface:

```text
design-implementation -> figma-implement-design
```

The new pack should be config-only unless a later migration explicitly needs directory movement. It should cover Figma-to-code and design implementation prompts, not research methodology.

The stale audit expectation should be corrected:

```text
把这个Figma设计稿还原为可运行代码 -> figma-implement-design
帮我设计准实验方法，比较DiD和ITS -> designing-experiments
```

### 5.3 Scholarly Publishing Rule

`scholarly-publishing-workflow` should keep ownership of publication packaging:

```text
rebuttal
submission checklist
venue template
LaTeX manuscript PDF build
camera-ready package
```

It should not steal:

```text
result figures -> scientific-visualization
slides as code -> slides-as-code under science-communication-slides
scientific report -> scientific-reporting
PDF extraction -> pdf
PDF to Markdown -> markitdown
```

The implementation should first add regression tests for these boundaries. Only then should it remove or downgrade overlapping candidates if tests prove current overlap still causes incorrect ownership.

## 6. Test Design

Create or extend a focused routing-boundary test file such as:

```text
tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py
```

Required cases:

| Prompt | Expected |
| --- | --- |
| `读取 PDF 并提取正文` | `docs-media / pdf` |
| `把 PDF 转成 Markdown` | `docs-markitdown-conversion / markitdown` |
| `用 LaTeX 写论文并构建 PDF` | `scholarly-publishing-workflow / latex-submission-pipeline` |
| `科研技术报告：包含方法结果讨论，输出 HTML 和 PDF` | `science-reporting / scientific-reporting` |
| `用 Slidev 做组会汇报并导出 PDF` | `science-communication-slides / slides-as-code` |
| `把这个 Figma 设计稿还原为可运行代码` with `task_type=coding` | `design-implementation / figma-implement-design` |
| `帮我设计准实验方法，比较 DiD 和 ITS` | `research-design / designing-experiments` |
| `xlsx and docx parallel processing` with `grade=XL` | not a weak fallback to `docs-media` unless the final rule explicitly allows it |

Update the existing script expectations only after the new dedicated tests make the intended contract explicit.

## 7. Verification

Focused verification:

```powershell
python -m pytest tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py -q
python -m pytest tests/runtime_neutral/test_scientific_visualization_latex_routing.py -q
```

Existing route and config verification:

```powershell
python -m pytest tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_python_validation_contract.py -q
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1
git diff --check
```

If a gate expectation is intentionally updated, the implementation must explain why the old expectation was wrong or outdated.

## 8. Non-Goals

This pass will not:

- Delete skill directories.
- Change the six-stage runtime.
- Change `skill_routing.selected` or `skill_usage.used / unused`.
- Reintroduce primary/secondary skill states.
- Deploy this checkout into Codex.
- Claim routed skills were materially used.

## 9. Acceptance Criteria

This cleanup is accepted when:

- `docs-media` has a clear XL policy and regression coverage.
- Figma implementation no longer misroutes to `latex-submission-pipeline` in coding mode.
- `research-design` keeps experiment/research-method ownership.
- Publication, report, slides, PDF extraction, PDF-to-Markdown, and LaTeX build prompts route to distinct owners.
- `vibe-pack-regression-matrix.ps1` and `vibe-skill-index-routing-audit.ps1` pass with expectations that match the new contract.
- Existing smoke, offline skills, and config parity gates pass.
