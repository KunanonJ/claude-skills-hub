# Research Design Pack Consolidation Design

Date: 2026-04-29

## Goal

Shrink `research-design` into a clear research-methods pack.

The pack should own research design, scientific ideation, hypothesis formulation, experiment failure analysis, causal/regression methodology, literature-combination matrices, and grant proposal planning. It should not own browser automation, backend architecture, skill management, UX research, generic report generation, structured code storage, or software testing helpers.

The six-stage Vibe runtime stays unchanged. The simplified routing contract also stays unchanged:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / unused
```

## Current Evidence

Current `research-design` has 22 skill candidates:

```text
architecture-patterns
comprehensive-research-agent
designing-experiments
experiment-failure-analysis
hypogenic
hypothesis-generation
hypothesis-testing
literature-matrix
performing-causal-analysis
performing-regression-analysis
playwright
property-based-testing
research-lookup
research-grants
scientific-brainstorming
scientific-data-preprocessing
skill-creator
skill-lookup
ux-researcher-designer
verification-quality-assurance
report-generator
structured-content-storage
```

The latest global pack audit ranks `research-design` as the top structural risk:

| signal | value |
| --- | ---: |
| `skill_candidates` | 22 |
| `route_authority_candidates` | 14 |
| `stage_assistant_candidates` | 3 |
| suspected overlap pairs | 2 |
| asset-heavy candidates | 13 |

Manual inspection found several candidates that do not describe research-method ownership:

| Skill | Current issue |
| --- | --- |
| `architecture-patterns` | Backend architecture, not research design. |
| `playwright` | Browser automation; already has a better owner in `web-scraping`. |
| `property-based-testing` | Software testing; belongs with code quality or testing governance. |
| `skill-creator` | Skill authoring meta-tool, not research methodology. |
| `skill-lookup` | Skill discovery meta-tool, not research methodology. |
| `ux-researcher-designer` | UX research/design surface, not scientific research design. |
| `report-generator` | Generic report output, overlaps with `science-reporting`. |
| `structured-content-storage` | Project organization helper, not a research-method owner. |
| `scientific-data-preprocessing` | Data-preprocessing guard; useful, but not a broad research-design owner. |
| `verification-quality-assurance` | Verification governance, not research-method routing. |
| `research-lookup` | Research retrieval/execution; overlaps with literature and deep-research packs. |
| `hypothesis-testing` | Misleading name: this is Python Hypothesis/property-based testing, not scientific statistical hypothesis testing. |

## Target Ownership

`research-design` should keep only skills that can be the main answer to a research-method request.

| User problem | Target skill |
| --- | --- |
| Choose or design experiments, quasi-experiments, DiD, ITS, synthetic control | `designing-experiments` |
| Analyze failed experiments and decide recovery or abandonment plans | `experiment-failure-analysis` |
| Generate and test hypotheses with the HypoGeniC workflow | `hypogenic` |
| Formulate testable scientific hypotheses from observations | `hypothesis-generation` |
| Build paper-combination matrices and research idea maps | `literature-matrix` |
| Perform causal-method planning or causal model analysis | `performing-causal-analysis` |
| Perform regression-method analysis and interpretation | `performing-regression-analysis` |
| Write or structure research grant proposals | `research-grants` |
| Brainstorm scientific mechanisms, gaps, and research directions | `scientific-brainstorming` |

Target count:

| Field | Before | Target |
| --- | ---: | ---: |
| `skill_candidates` | 22 | 9 |
| `route_authority_candidates` | 14 | 9 compatibility mirror |
| `stage_assistant_candidates` | 3 | 0 |
| physical directory deletion | 0 | 0 |

The legacy `route_authority_candidates` field may mirror the kept `skill_candidates` for compatibility with current gates, but it must not introduce a separate primary/secondary/assistant model. `stage_assistant_candidates` should be empty for this pack.

## Move Out Of Research Design

These skills should be removed from `research-design.skill_candidates` in the implementation pass.

| Skill | Target action | Rationale |
| --- | --- | --- |
| `architecture-patterns` | move-out-of-pack | Backend architecture has no research-method ownership. A future architecture/system-design route can own it if needed. |
| `comprehensive-research-agent` | move-out-of-pack | Generic research-agent behavior is orchestration guidance, not a specific research-method expert. |
| `hypothesis-testing` | move-out-of-pack | Name conflicts with scientific hypothesis testing, but content is software property-based testing. |
| `playwright` | move-out-of-pack | Browser automation is already represented by `web-scraping / playwright`. |
| `property-based-testing` | move-out-of-pack | Software testing belongs with code quality/testing surfaces. |
| `research-lookup` | move-out-of-pack | Literature/current-info lookup belongs to literature or deep-research retrieval surfaces, not research design. |
| `scientific-data-preprocessing` | move-out-of-pack | Valuable guard skill, but it should not own broad research-method prompts. A data/ML or future science-data pack is a better fit. |
| `skill-creator` | move-out-of-pack | Skill authoring meta-tool, not a research-method expert. |
| `skill-lookup` | move-out-of-pack | Skill discovery meta-tool, not a research-method expert. |
| `ux-researcher-designer` | move-out-of-pack | UX research/design should not be routed through scientific research design. |
| `verification-quality-assurance` | move-out-of-pack | Verification governance should not own research-design prompts. |
| `report-generator` | move-out-of-pack | Generic report generation overlaps with `science-reporting`. |
| `structured-content-storage` | move-out-of-pack | Storage discipline can assist projects, but is not a research-method owner. |

No physical deletion is in scope for this pass. Many moved-out skills have scripts, references, or substantial content. Physical pruning must be a later review that proves the content is low quality, duplicated, or migrated.

## Routing Rules

Implementation should update routing in this order:

1. Add focused route tests that express the desired boundaries.
2. Shrink `research-design` in `config/pack-manifest.json`.
3. Add or tighten keywords for the nine kept research-method skills.
4. Add negative guards to moved-out skills or competing packs only where tests show false positives.
5. Update route probe scripts or skill-index audits with the protected cases.
6. Write a governance note under `docs/governance/`.

Important guardrails:

- Research-method prompts should still route to `research-design`.
- Browser automation should route to `web-scraping / playwright`.
- Figma implementation should remain in `design-implementation / figma-implement-design`.
- Scientific reporting should route to `science-reporting / scientific-reporting`.
- Literature search and evidence extraction should not be forced through `research-design / research-lookup`.
- The Python Hypothesis/property-based testing skill must not be confused with scientific hypothesis testing.

## Regression Probes

Add route probes for the kept owners:

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

Add negative boundary probes:

| Prompt | Expected boundary |
| --- | --- |
| `用 Playwright 打开网页并截图` | `web-scraping / playwright` or existing screen-capture behavior if screenshot dominates |
| `把这个 Figma 设计稿还原为可运行代码` | `design-implementation / figma-implement-design` |
| `为 Python 函数写 property-based testing` | not `research-design` |
| `检索 PubMed 文献并导出 BibTeX` | `science-literature-citations / pubmed-database` |
| `科研技术报告：包含方法结果讨论，输出 HTML 和 PDF` | `science-reporting / scientific-reporting` |
| `为后端系统设计 Clean Architecture 架构` | not `research-design` |
| `创建一个新的 Codex skill` | not `research-design` |
| `做用户访谈、persona 和用户旅程图` | not `research-design` |
| `对科研数据做缺失值处理和标准化，避免数据泄漏` | not `research-design` |

Where the expected non-research owner is not yet cleanly represented by an existing pack, the test should assert `not research-design` rather than inventing a new pack in this pass.

## Verification

Focused checks:

```powershell
python -m pytest tests/runtime_neutral/test_research_design_pack_consolidation.py -q
```

Broader checks:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1
git diff --check
```

If physical directories are later deleted, also regenerate `config/skills-lock.json` and rerun offline skills gates. This design does not require lockfile changes because it does not delete bundled skill directories.

## Options Considered

### Option A: Minimal Keyword Patch

Only add negative keywords to the worst false positives.

Tradeoff: fast, but leaves 22 candidates in `research-design` and does not solve the unclear expert boundary.

### Option B: Problem-First Pack Shrink

Reduce `research-design` to nine research-method owners, remove unrelated skills from the pack routing surface, and add route regressions.

Tradeoff: moderate work, but it directly addresses the pack boundary problem without deleting useful assets.

### Option C: Broad Rehoming And Physical Pruning

Create or modify multiple packs for architecture, UX, skill management, testing, and reporting, then physically delete low-quality skills.

Tradeoff: too broad for this pass. It would make it harder to prove which route change fixed which problem.

Recommended option: Option B.

## Non-Goals

This pass will not:

- Delete physical skill directories.
- Change the six-stage Vibe runtime.
- Reintroduce primary/secondary, advisory, consult, or stage-assistant execution states.
- Claim selected skills were materially used without `skill_usage.used` evidence.
- Redesign all moved-out destination packs.
- Install or deploy this checkout into the live Codex host.

## Acceptance Criteria

This cleanup is accepted when:

- `research-design.skill_candidates` is reduced from 22 to the nine research-method owners.
- Legacy route/stage fields do not add a second execution model.
- Research-method prompts still route to the correct kept skills.
- Non-research prompts no longer route through `research-design`.
- Focused and broad routing gates pass.
- A governance note records the before/after counts, kept owners, moved-out skills, and no-deletion boundary.
