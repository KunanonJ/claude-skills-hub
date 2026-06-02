# Figures And Reporting Stage Assistant Removal Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-29

## 1. Goal

Clean `science-figures-visualization` and `science-reporting` so they follow the simplified skill-routing model:

```text
candidate -> selected -> used / unused
```

The public six-stage Vibe runtime is unchanged. This pass only removes old pack-level helper semantics from two high-impact scientific output packs.

## 2. Problem

Both packs still carry `stage_assistant_candidates`:

```text
science-figures-visualization:
  matplotlib
  seaborn
  plotly

science-reporting:
  scientific-visualization
  scientific-schematics
  markdown-mermaid-writing
```

That keeps the old idea that a skill can be a helper, assistant, or secondary participant without directly entering work. It conflicts with the approved simplified contract:

```text
Selected skill enters work.
Unselected skill does not enter work.
Actual use is proven only by skill_usage.used / skill_usage.unused.
```

## 3. Approved Direction

Use strict binary pack membership:

```text
In skill_candidates = eligible to be selected as the direct skill for a task slice.
Out of skill_candidates = not routed by this pack.
stage_assistant_candidates = []
```

Do not promote every library wrapper into a direct expert. A direct expert must own a user problem, not merely name an implementation library.

## 4. Target Pack Contracts

### science-figures-visualization

Target candidates:

```text
scientific-visualization
scientific-schematics
```

Target route owners:

```text
scientific-visualization
scientific-schematics
```

Target stage assistants:

```text
[]
```

Ownership:

| Skill | Owns |
| --- | --- |
| `scientific-visualization` | Result figures, publication figures, multi-panel figures, model-evaluation plots, data visualization, 600dpi/TIFF/SVG/vector output, colorblind palettes, error bars, significance annotations. |
| `scientific-schematics` | Mechanism schematics, workflow diagrams, flowcharts, system diagrams, graphical abstracts, Mermaid-like scientific diagrams. |

Moved out of this pack:

| Skill | Reason |
| --- | --- |
| `matplotlib` | Plotting library, not an expert role. It can be used inside `scientific-visualization` work but should not be selected as a separate routed skill. |
| `seaborn` | Plotting library, not an expert role. It belongs inside visualization implementation choices. |
| `plotly` | Interactive plotting library, not a scientific-output owner. It should not enter work as an auxiliary expert. |

### science-reporting

Target candidates:

```text
scientific-reporting
scientific-writing
```

Target route owners:

```text
scientific-reporting
scientific-writing
```

Target stage assistants:

```text
[]
```

Ownership:

| Skill | Owns |
| --- | --- |
| `scientific-reporting` | Scientific, technical, analysis, and project reports; HTML/PDF report outputs; Quarto/RMarkdown style reports; executive summaries; appendices; reproducibility sections. |
| `scientific-writing` | Scientific prose and manuscript body writing: IMRAD, abstract, introduction, methods, results, discussion, and journal manuscript text. |

Moved out of this pack:

| Skill | Reason |
| --- | --- |
| `scientific-visualization` | Already owned by `science-figures-visualization`; report generation may request figures, but figure ownership should be a separate selected task slice. |
| `scientific-schematics` | Already owned by `science-figures-visualization`; Mermaid/diagram prompts should not be hidden reporting helpers. |
| `markdown-mermaid-writing` | Mermaid authoring is not a reporting owner. Mermaid/flowchart work should route to `scientific-schematics` or remain explicit outside this pack. |

## 5. Composite Task Behavior

For a composite task such as:

```text
论文研究 + 机器学习建模 + 数据可视化 + 论文撰写
```

The system should split the work into direct task slices. It must not model one skill as a main expert with hidden assistants.

Expected routing pattern:

| Task slice | Pack / skill |
| --- | --- |
| Literature or citation work | `science-literature-citations` and the matching literature/citation skill |
| Machine-learning modeling | `data-ml` and the matching ML skill, such as `scikit-learn` |
| Result figures or model-evaluation plots | `science-figures-visualization / scientific-visualization` |
| Mechanism diagram or flowchart | `science-figures-visualization / scientific-schematics` |
| Scientific report output | `science-reporting / scientific-reporting` |
| Manuscript prose | `science-reporting / scientific-writing` or `scholarly-publishing-workflow / scientific-writing`, depending on the final publishing workflow |
| LaTeX manuscript build | `scholarly-publishing-workflow / latex-submission-pipeline` |

Every selected skill must later be proven through:

```text
full SKILL.md load -> task_slice binding -> artifact impact -> skill_usage.used
```

If it is selected but not materially used, it must be recorded as unused.

## 6. Config Changes

Modify only routing/config/test/governance surfaces:

```text
config/pack-manifest.json
config/skill-keyword-index.json
config/skill-routing-rules.json
tests/runtime_neutral/*
scripts/verify/*
docs/governance/*
config/skills-lock.json
```

Expected manifest changes:

```text
science-figures-visualization.skill_candidates =
  scientific-visualization, scientific-schematics

science-figures-visualization.route_authority_candidates =
  scientific-visualization, scientific-schematics

science-figures-visualization.stage_assistant_candidates = []

science-reporting.skill_candidates =
  scientific-reporting, scientific-writing

science-reporting.route_authority_candidates =
  scientific-reporting, scientific-writing

science-reporting.stage_assistant_candidates = []
```

Do not physically delete skill directories in this pass.

## 7. Test Strategy

Add focused tests that assert:

- `science-figures-visualization.stage_assistant_candidates == []`.
- `science-reporting.stage_assistant_candidates == []`.
- `matplotlib`, `seaborn`, and `plotly` are not selected as `science-figures-visualization` skills.
- `scientific-visualization` still owns publication figures, result figures, model-evaluation plots, and data visualization.
- `scientific-schematics` still owns Mermaid/flowchart/mechanism diagram prompts.
- `scientific-reporting` still owns scientific or technical reports with HTML/PDF output.
- `scientific-writing` still owns IMRAD and manuscript prose prompts.
- `science-reporting` no longer carries visualization, schematics, or Mermaid as assistant candidates.

Update existing tests that still expect `matplotlib`, `seaborn`, or `plotly` to appear as `route_stage_assistant`. Those expectations are legacy behavior and should be replaced with binary selected/rejected expectations.

Run verification:

```powershell
python -m pytest tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py -q
python -m pytest tests/runtime_neutral/test_bundled_stage_assistant_freeze.py tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py -q
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

## 8. Non-Goals

- Do not change Vibe's public six-stage runtime.
- Do not reintroduce primary/secondary skill state.
- Do not add advisory, consult, or auxiliary expert semantics.
- Do not delete `matplotlib`, `seaborn`, `plotly`, `markdown-mermaid-writing`, or any bundled skill directory.
- Do not broaden this pass to `data-ml`, `code-quality`, `ruc-nlpir-augmentation`, or `aios-core`.

## 9. Acceptance Criteria

The cleanup is accepted when:

1. Both target packs have zero `stage_assistant_candidates`.
2. Both target packs expose only direct problem-owner candidates.
3. Figure and report prompts still route to the intended direct owners.
4. Legacy stage-assistant assertions are updated to the simplified model.
5. Focused tests and broad routing gates pass.
6. Governance notes clearly state that this is config/routing cleanup, not physical skill deletion.
