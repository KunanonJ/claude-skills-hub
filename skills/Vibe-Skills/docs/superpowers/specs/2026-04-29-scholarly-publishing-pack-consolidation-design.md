# Scholarly Publishing Pack Consolidation Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-29

## Goal

Consolidate `scholarly-publishing-workflow` into a focused publishing and manuscript-delivery pack.

This pass keeps the six-stage Vibe runtime unchanged and preserves the simplified skill-use model:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / unused
```

The pack should answer publishing workflow problems directly, while figure creation, slide creation, and citation retrieval remain owned by their dedicated packs.

## Current State

`scholarly-publishing-workflow` currently has 13 `skill_candidates`, no explicit `route_authority_candidates`, and no `stage_assistant_candidates`.

Current candidates:

```text
scholarly-publishing
submission-checklist
manuscript-as-code
latex-submission-pipeline
slides-as-code
scientific-writing
scientific-visualization
scientific-schematics
venue-templates
citation-management
paper-2-web
latex-posters
scientific-slides
```

Several candidates duplicate ownership already present in other packs:

| Skill | Existing stronger owner |
| --- | --- |
| `scientific-visualization` | `science-figures-visualization` |
| `scientific-schematics` | `science-figures-visualization` |
| `slides-as-code` | `science-communication-slides` |
| `scientific-slides` | `science-communication-slides` |
| `citation-management` | `science-literature-citations` |

## Target Routing Contract

After consolidation:

| Field | Before | After |
| --- | ---: | ---: |
| `skill_candidates` | 13 | 8 |
| `route_authority_candidates` | 0 | 8 |
| `stage_assistant_candidates` | 0 | 0 |
| physical directory deletion | 0 | 0 |

`route_authority_candidates` is a compatibility mirror of `skill_candidates`, not a second execution model. No `primary/secondary`, `consult`, `advisory`, or stage-assistant execution semantics are introduced.

## Kept Route Owners

| User problem | Skill |
| --- | --- |
| End-to-end journal/conference publishing workflow, submission package planning, camera-ready coordination | `scholarly-publishing` |
| Pre-submission checklist, cover letter, rebuttal matrix, response-to-reviewers workflow | `submission-checklist` |
| Reproducible manuscript repository, version control, figure pipeline structure, CI build discipline | `manuscript-as-code` |
| LaTeX manuscript/PDF build, latexmk, chktex, latexindent, BibTeX/Biber build, submission zip | `latex-submission-pipeline` |
| Scientific manuscript prose: IMRAD, abstract, introduction, methods, results, discussion | `scientific-writing` |
| Venue-specific templates and formatting requirements | `venue-templates` |
| LaTeX poster or conference poster build | `latex-posters` |
| Paper-to-web, paper-to-video, paper-to-poster dissemination assets | `paper-2-web` |

## Moved Out Of This Pack

These skills remain valuable and should not be physically deleted in this pass. They are removed only from `scholarly-publishing-workflow` routing ownership.

| Skill | Target boundary | Rationale |
| --- | --- | --- |
| `scientific-visualization` | `science-figures-visualization` | Result figures, publication plots, and model-evaluation plots already have a dedicated figure pack. |
| `scientific-schematics` | `science-figures-visualization` | Diagrams and schematics are figure assets, not manuscript workflow owners. |
| `slides-as-code` | `science-communication-slides` | Slidev/Marp/Reveal/Quarto deck building belongs to the slides pack. |
| `scientific-slides` | `science-communication-slides` | Scientific talks, seminar slides, and defense decks belong to the slides pack. |
| `citation-management` | `science-literature-citations` | Citation formatting and BibTeX management belongs to literature/citation tooling. |

## Defaults

Use conservative defaults:

```json
{
  "planning": "scholarly-publishing",
  "coding": "latex-submission-pipeline",
  "research": "scientific-writing"
}
```

Reasoning:

- `planning` should default to the end-to-end publishing owner.
- `coding` should default to the executable LaTeX/build owner.
- `research` should default to manuscript prose unless a narrower trigger such as `venue template` or `paper2web` is present.

## Routing Keywords

The implementation should tighten `config/skill-keyword-index.json` and `config/skill-routing-rules.json` for the 8 kept skills.

Required positive routing examples:

| Prompt | Expected route |
| --- | --- |
| `规划一套期刊投稿工作流，包含投稿包、校样和 camera-ready` | `scholarly-publishing-workflow / scholarly-publishing` |
| `写 cover letter 和 response to reviewers rebuttal matrix` | `scholarly-publishing-workflow / submission-checklist` |
| `把论文仓库改成 manuscript-as-code，可复现构建 PDF` | `scholarly-publishing-workflow / manuscript-as-code` |
| `配置 latexmk/chktex/latexindent 编译论文 PDF 并打包 submission zip` | `scholarly-publishing-workflow / latex-submission-pipeline` |
| `请按 IMRAD 结构写科研论文正文` | `scholarly-publishing-workflow / scientific-writing` |
| `查 NeurIPS 模板和匿名投稿格式要求` | `scholarly-publishing-workflow / venue-templates` |
| `用 beamerposter 做会议学术海报` | `scholarly-publishing-workflow / latex-posters` |
| `把论文转换成 paper2web 项目主页和视频摘要` | `scholarly-publishing-workflow / paper-2-web` |

Required false-positive protections:

| Prompt | Expected route |
| --- | --- |
| `绘制机器学习模型评估结果图和投稿图` | `science-figures-visualization / scientific-visualization` |
| `画一个机制示意图和流程图` | `science-figures-visualization / scientific-schematics` |
| `用 Slidev 做组会汇报并导出 PDF` | `science-communication-slides / slides-as-code` |
| `顶级PPT制作：组会汇报 slide deck` | `science-communication-slides / scientific-slides` |
| `整理参考文献格式，修正 DOI，生成 Nature 格式 bibliography` | `science-literature-citations / citation-management` |
| `读取 PDF 并提取正文` | `docs-media / pdf` |
| `科研技术报告：包含方法结果讨论，输出 HTML 和 PDF` | `science-reporting / scientific-reporting` |

## Test Plan

Add focused Python route tests:

```text
tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py
```

The tests should verify:

- Manifest candidate count shrinks from 13 to 8.
- `route_authority_candidates` mirrors the 8 kept skills.
- `stage_assistant_candidates` is empty.
- All 8 kept owners route correctly.
- The 5 moved-out skills no longer live in this pack.
- Figure, schematic, slide, citation, PDF extraction, and reporting prompts stay outside this pack.

Add script-level coverage to:

```text
scripts/verify/vibe-skill-index-routing-audit.ps1
scripts/verify/vibe-pack-regression-matrix.ps1
```

Run focused tests first, then existing broader gates:

```powershell
python -m pytest tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py -q
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1
git diff --check
```

## Governance Note

The implementation should add:

```text
docs/governance/scholarly-publishing-pack-consolidation-2026-04-29.md
```

The governance note should record:

- before/after counts
- kept route owners and their problem boundaries
- moved-out skills and their target packs
- no physical deletion
- protected route probes
- verification commands and results

## Non-Goals

This pass does not:

- delete any bundled skill directory
- update `config/skills-lock.json` unless a later implementation physically changes bundled skill directories
- change canonical Vibe launch or six-stage runtime behavior
- introduce advisory, consultation, primary/secondary, or stage-assistant execution semantics
- merge `science-figures-visualization`, `science-communication-slides`, `science-literature-citations`, or `science-reporting` into the publishing pack

## Implementation Sequence

1. Add focused failing tests for the target manifest and route boundaries.
2. Shrink `scholarly-publishing-workflow` in `config/pack-manifest.json`.
3. Tighten keyword index and routing rules for the 8 kept skills and the 5 moved-out boundaries.
4. Add script-level route probes.
5. Add governance note.
6. Run focused and broad verification.
7. Commit changes in small checkpoints.
