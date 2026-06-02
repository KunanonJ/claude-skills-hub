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
