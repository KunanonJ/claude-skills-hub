# Research Design Pack Consolidation

Date: 2026-04-29

Superseded note: the retained-owner set in this first-pass document was reduced again on 2026-04-30 by `research-design-high-prune-2026-04-30.md`.

## Summary

This pass shrinks `research-design` into a research-methods pack. It keeps research design, scientific ideation, hypothesis formulation, experiment failure analysis, causal/regression methodology, literature-combination matrices, and grant proposal planning.

The six-stage Vibe runtime is unchanged, and skill usage remains binary:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / unused
```

## Counts

| Field | Before | After |
| --- | ---: | ---: |
| `skill_candidates` | 22 | 9 |
| `route_authority_candidates` | 14 | 9 |
| `stage_assistant_candidates` | 3 | 0 |
| physical directory deletion | 0 | 0 |

`route_authority_candidates` is retained only as a compatibility mirror of `skill_candidates`. It is not a second execution model.

## Kept Research-Method Owners

| User problem | Skill |
| --- | --- |
| Quasi-experimental design, DiD, ITS, synthetic control | `designing-experiments` |
| Experiment failure root-cause analysis and recovery planning | `experiment-failure-analysis` |
| Automated hypothesis generation and testing with HypoGeniC | `hypogenic` |
| Testable scientific hypothesis formulation | `hypothesis-generation` |
| Paper-combination matrices and research idea maps | `literature-matrix` |
| Causal analysis and treatment-effect methodology | `performing-causal-analysis` |
| Regression analysis and interpretation | `performing-regression-analysis` |
| Research grant and proposal structure | `research-grants` |
| Scientific mechanism and research-gap brainstorming | `scientific-brainstorming` |

## Moved Out Of Research Design

| Skill | Action | Rationale |
| --- | --- | --- |
| `architecture-patterns` | Removed from `research-design` routing surface | Backend architecture is not research-method ownership. |
| `comprehensive-research-agent` | Removed from `research-design` routing surface | Generic research-agent behavior is orchestration guidance, not a specific method expert. |
| `hypothesis-testing` | Removed from `research-design` routing surface | This is Python Hypothesis/property-based testing, not scientific hypothesis testing. |
| `playwright` | Removed from `research-design` routing surface | Browser automation belongs outside research design; current owner is `web-scraping / playwright` or screen capture when screenshot dominates. |
| `property-based-testing` | Removed from `research-design` routing surface | Software testing is not scientific research design. |
| `research-lookup` | Removed from `research-design` routing surface | Literature lookup belongs to literature/deep-research retrieval surfaces. |
| `scientific-data-preprocessing` | Removed from `research-design` routing surface | Data preprocessing is useful but should not own research-method prompts. |
| `skill-creator` | Removed from `research-design` routing surface | Skill authoring is a meta-skill surface. |
| `skill-lookup` | Removed from `research-design` routing surface | Skill discovery is a meta-skill surface. |
| `ux-researcher-designer` | Removed from `research-design` routing surface | UX research/design is not scientific research-method ownership. |
| `verification-quality-assurance` | Removed from `research-design` routing surface | Verification governance is not a research-method route owner. |
| `report-generator` | Removed from `research-design` routing surface | Report output overlaps with `science-reporting`. |
| `structured-content-storage` | Removed from `research-design` routing surface | Storage discipline can assist projects but is not a research-method owner. |

## No Physical Deletion

No bundled skill directory is physically deleted in this pass. Many moved-out skills have scripts, references, or substantial content. Any later pruning pass must separately prove content migration or low-quality duplication before deletion.

## Protected Boundaries

| Prompt | Expected route |
| --- | --- |
| `帮我设计准实验方法，比较 DiD 和 ITS` | `research-design / designing-experiments` |
| `分析实验失败原因，判断是否继续优化还是放弃该方案` | `research-design / experiment-failure-analysis` |
| `用 HypoGeniC 从数据和文献中生成并测试科研假设` | `research-design / hypogenic` |
| `根据实验观察生成可检验的科研假设和预测` | `research-design / hypothesis-generation` |
| `构建论文组合矩阵，寻找 A+B 的研究创新点` | `research-design / literature-matrix` |
| `用 DID 和 synthetic control 做因果分析方案` | `research-design / performing-causal-analysis` |
| `做回归分析并解释系数、置信区间和诊断结果` | `research-design / performing-regression-analysis` |
| `写 NSF 科研基金申请书的 significance 和 innovation` | `research-design / research-grants` |
| `围绕这个生物机制做科研头脑风暴，提出可能机制和实验方向` | `research-design / scientific-brainstorming` |
| `检索 PubMed 文献并导出 BibTeX` | `science-literature-citations / pubmed-database` |
| `科研技术报告：包含方法结果讨论，输出 HTML 和 PDF` | `science-reporting / scientific-reporting` |
| `把这个 Figma 设计稿还原为可运行代码` | `design-implementation / figma-implement-design` |

## Verification

Required checks:

```powershell
python -m pytest tests/runtime_neutral/test_research_design_pack_consolidation.py -q
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1
git diff --check
```
