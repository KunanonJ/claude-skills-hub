# Research Design Boundary Hardening Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-30

## Goal

Harden the already-pruned `research-design` pack without shrinking it again.

The previous consolidation reduced `research-design` from a mixed 22-skill surface to 9 research-method owners. This second pass keeps those 9 owners, removes old cross-skill and helper-style language, and tightens routing boundaries so each selected skill has a clear reason to be used.

The six-stage Vibe runtime remains unchanged. The simplified skill-use contract remains:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / unused
```

No advisory state, stage assistant state, primary/secondary hierarchy, or helper-expert dispatch should be introduced.

## Current State

Current `research-design` pack:

| Field | Current |
| --- | ---: |
| `skill_candidates` | 9 |
| `route_authority_candidates` | 9 |
| `stage_assistant_candidates` | 0 |
| physical deletion in this pass | 0 |

Current kept skills:

```text
designing-experiments
experiment-failure-analysis
hypogenic
hypothesis-generation
literature-matrix
performing-causal-analysis
performing-regression-analysis
research-grants
scientific-brainstorming
```

The pack is structurally much cleaner than before, but the remaining risk is boundary ambiguity inside the 9 retained skills.

## Problems To Fix

### 1. Causal Design Boundary

`designing-experiments` and `performing-causal-analysis` both mention DiD, interrupted time series, synthetic control, and regression discontinuity. This makes route ownership ambiguous.

Target boundary:

| User intent | Owner |
| --- | --- |
| Choose a study design, define treatment/control, design the experiment or quasi-experiment before analysis | `designing-experiments` |
| Estimate causal effects from existing data, fit models, run robustness checks, interpret treatment effects | `performing-causal-analysis` |

### 2. Ideation And Hypothesis Boundary

`scientific-brainstorming`, `hypothesis-generation`, `hypogenic`, and `literature-matrix` all live near research idea generation. They need sharper problem ownership.

Target boundary:

| User intent | Owner |
| --- | --- |
| Open-ended scientific ideation, mechanism exploration, research gaps, possible directions | `scientific-brainstorming` |
| Convert observations or data signals into testable hypotheses, predictions, and validation experiments | `hypothesis-generation` |
| Explicit HypoGeniC or automated LLM-driven hypothesis generation/testing workflows | `hypogenic` |
| Paper-combination matrix, A+B idea generation, literature matrix, unified framework from multiple papers | `literature-matrix` |

### 3. Cross-Skill And Helper Language

Some retained skill files still contain old instructions that imply mandatory use of other skills or consultation with helper skills. That contradicts the simplified model.

Known examples to clean:

| Skill | Problematic pattern |
| --- | --- |
| `hypothesis-generation` | Mandatory `scientific-schematics` use, `venue-templates` consultation language |
| `research-grants` | Mandatory `scientific-schematics` use and helper-style wording |
| `scientific-brainstorming` | `consulted` style language |

Target wording:

```text
This skill owns its selected task directly.
It may mention output types or optional artifacts, but it must not require or imply a secondary expert route.
```

## Target Ownership

The 9 active route owners remain active. Their boundaries become:

| Skill | Owns | Does not own |
| --- | --- | --- |
| `designing-experiments` | Study-design choice, experimental design, quasi-experimental design before data analysis | Existing-data causal estimation |
| `performing-causal-analysis` | Treatment-effect analysis, causal model fitting, robustness checks on data | General experimental-design planning |
| `performing-regression-analysis` | Regression modeling, diagnostics, coefficient interpretation, residuals | Causal-route ownership when causal design/effect language is dominant |
| `hypothesis-generation` | Testable hypotheses, predictions, mechanisms, validation experiments from observations | Open-ended brainstorming, literature matrix construction, HypoGeniC-specific workflows |
| `scientific-brainstorming` | Open-ended scientific idea exploration and mechanism/gap discovery | Structured hypothesis report or validation plan as the main deliverable |
| `hypogenic` | Explicit HypoGeniC and automated hypothesis-generation/testing workflows | Generic hypothesis generation |
| `literature-matrix` | Paper matrix, A+B combinations, research idea maps, unified frameworks | General literature lookup, citation management, manuscript writing |
| `experiment-failure-analysis` | Failed experiment diagnosis, recovery, abandonment/redo decisions | Normal experiment design or planning |
| `research-grants` | Grant proposal aims, significance, innovation, budget/justification, review logic | Generic research proposal or paper writing unless grant/funding language is present |

## Planned Changes

### Skill Files

Edit only retained `research-design` skill files that need wording cleanup or boundary clarification:

```text
bundled/skills/designing-experiments/SKILL.md
bundled/skills/performing-causal-analysis/SKILL.md
bundled/skills/hypothesis-generation/SKILL.md
bundled/skills/scientific-brainstorming/SKILL.md
bundled/skills/hypogenic/SKILL.md
bundled/skills/literature-matrix/SKILL.md
bundled/skills/research-grants/SKILL.md
```

`performing-regression-analysis` and `experiment-failure-analysis` should be touched only if inspection finds stale helper or cross-skill language.

### Routing Configs

Tighten routing in the existing config surface:

```text
config/pack-manifest.json
config/skill-keyword-index.json
config/skill-routing-rules.json
```

Expected routing refinements:

- design-before-data prompts route to `designing-experiments`
- data-analysis causal prompts route to `performing-causal-analysis`
- explicit HypoGeniC prompts route to `hypogenic`
- generic testable-hypothesis prompts route to `hypothesis-generation`
- open-ended mechanism/gap ideation routes to `scientific-brainstorming`
- A+B paper combination or matrix prompts route to `literature-matrix`
- grant/funding language routes to `research-grants`

Do not add stage assistants. Do not add advisory mode. Do not create primary/secondary routing semantics.

### Regression Evidence

Add or update focused route probes for the retained boundaries.

Positive boundary probes:

| Prompt | Expected skill |
| --- | --- |
| `帮我设计准实验方案，先决定 DiD 还是中断时间序列，不要开始建模` | `designing-experiments` |
| `我已有面板数据，请用 DiD 估计政策的因果效应并做稳健性检验` | `performing-causal-analysis` |
| `根据异常实验现象生成可检验的科研假设、预测和验证实验` | `hypothesis-generation` |
| `围绕这个机制做科研头脑风暴，列出可能方向和研究空白` | `scientific-brainstorming` |
| `用 HypoGeniC 自动生成并测试假设` | `hypogenic` |
| `把这几篇论文做成 literature matrix，找 A+B 创新点` | `literature-matrix` |
| `写 NIH proposal 的 Specific Aims、Significance 和 Innovation` | `research-grants` |

Negative boundary probes:

| Prompt | Expected boundary |
| --- | --- |
| `只是设计实验方案，不分析已有数据` | not `performing-causal-analysis` |
| `已有数据做处理效应估计，不是设计实验` | not `designing-experiments` |
| `普通科研假设生成，没有提 HypoGeniC` | not `hypogenic` |
| `开放式科研构思，不要求形成可检验假设报告` | not `hypothesis-generation` |
| `文献检索和 BibTeX 导出` | not `research-design` |
| `论文撰写、LaTeX 构建或 PDF 投稿` | not `research-design` |

## Governance Note

Write a concise governance note under:

```text
docs/governance/research-design-boundary-hardening-2026-04-30.md
```

It should record:

- before/after counts stay 9/9/0
- no physical deletion
- no stage assistants
- no helper-expert semantics
- updated ownership table
- exact tests/probes used as evidence

## Verification

Focused checks:

```powershell
python -m pytest tests/runtime_neutral/test_research_design_pack_consolidation.py -q
```

Routing checks:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\probe-scientific-packs.ps1
```

General integrity checks:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1
git diff --check
```

If `skills-lock.json` changes are required by the repo gates after skill-file edits, regenerate it with the existing repo script and include the lockfile in the implementation commit. Do not manually edit the lockfile.

## Non-Goals

This pass will not:

- delete any retained `research-design` skill directory
- remove `hypogenic` or `scientific-brainstorming` from active routing
- create a new pack
- change the six-stage runtime
- add consultation, advisory, stage-assistant, or primary/secondary skill states
- turn route selection itself into proof of material skill use

## Acceptance Criteria

The implementation is acceptable when:

1. `research-design` still has 9 `skill_candidates`, 9 `route_authority_candidates`, and 0 `stage_assistant_candidates`.
2. Retained skill files no longer require or imply mandatory cross-skill invocation.
3. Causal design prompts and causal analysis prompts route to different intended owners.
4. Ideation, hypothesis generation, HypoGeniC, and literature-matrix prompts route to distinct intended owners.
5. Focused tests and route probes pass.
6. Governance notes state that this is boundary hardening, not physical pruning.
