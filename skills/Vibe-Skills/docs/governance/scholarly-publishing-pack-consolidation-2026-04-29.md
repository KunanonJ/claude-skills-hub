# Scholarly Publishing Pack Consolidation

Date: 2026-04-29

## Summary

This pass shrinks `scholarly-publishing-workflow` into a focused publishing and manuscript-delivery pack. It keeps submission workflow, rebuttal/checklist handling, reproducible manuscript engineering, LaTeX manuscript/PDF builds, scientific manuscript prose, venue templates, LaTeX posters, and paper-to-web/video/poster dissemination.

The six-stage Vibe runtime is unchanged, and skill usage remains binary:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / unused
```

## Counts

| Field | Before | After |
| --- | ---: | ---: |
| `skill_candidates` | 13 | 8 |
| `route_authority_candidates` | 0 | 8 |
| `stage_assistant_candidates` | 0 | 0 |
| physical directory deletion | 0 | 0 |

`route_authority_candidates` is retained only as a compatibility mirror of `skill_candidates`. It is not a second execution model.

## Kept Publishing Owners

| User problem | Skill |
| --- | --- |
| End-to-end journal/conference publishing workflow and submission package planning | `scholarly-publishing` |
| Submission checklist, cover letter, rebuttal matrix, response-to-reviewers workflow | `submission-checklist` |
| Reproducible manuscript repository, version control, figure pipeline, CI build discipline | `manuscript-as-code` |
| LaTeX manuscript/PDF build, latexmk, chktex, latexindent, BibTeX/Biber, submission zip | `latex-submission-pipeline` |
| Scientific manuscript prose: IMRAD, abstract, methods, results, discussion | `scientific-writing` |
| Venue-specific templates, formatting requirements, anonymous submission, page limits | `venue-templates` |
| LaTeX poster or conference poster build | `latex-posters` |
| Paper-to-web, paper-to-video, paper-to-poster dissemination assets | `paper-2-web` |

## Moved Out Of Scholarly Publishing

| Skill | Action | Rationale |
| --- | --- | --- |
| `scientific-visualization` | Removed from `scholarly-publishing-workflow` routing surface | Result figures and publication plots belong to `science-figures-visualization`. |
| `scientific-schematics` | Removed from `scholarly-publishing-workflow` routing surface | Scientific diagrams and schematics belong to `science-figures-visualization`. |
| `slides-as-code` | Removed from `scholarly-publishing-workflow` routing surface | Slidev/Marp/Reveal/Quarto deck building belongs to `science-communication-slides`. |
| `scientific-slides` | Removed from `scholarly-publishing-workflow` routing surface | Scientific talks, seminar slides, and defense decks belong to `science-communication-slides`. |
| `citation-management` | Removed from `scholarly-publishing-workflow` routing surface | Citation formatting and BibTeX management belongs to `science-literature-citations`. |

## No Physical Deletion

No bundled skill directory is physically deleted in this pass. Moved-out skills remain available through their target packs.

## Protected Boundaries

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
| `绘制机器学习模型评估结果图和投稿图` | `science-figures-visualization / scientific-visualization` |
| `画一个机制示意图和流程图` | `science-figures-visualization / scientific-schematics` |
| `用 Slidev 做组会汇报并导出 PDF` | `science-communication-slides / slides-as-code` |
| `顶级PPT制作：组会汇报 slide deck` | `science-communication-slides / scientific-slides` |
| `整理参考文献格式，修正 DOI，生成 Nature 格式 bibliography` | `science-literature-citations / citation-management` |
| `读取 PDF 并提取正文` | `docs-media / pdf` |
| `科研技术报告：包含方法结果讨论，输出 HTML 和 PDF` | `science-reporting / scientific-reporting` |

## Verification

Required checks:

```powershell
python -m pytest tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py -q
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1
git diff --check
```
