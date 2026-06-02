# Research Design Boundary Hardening

Date: 2026-04-30

Superseded note: this boundary-hardening pass kept 9 owners. A later 2026-04-30 high-prune pass reduced `research-design` to 5 owners and physically deleted 4 directories; see `research-design-high-prune-2026-04-30.md`.

## Summary

This pass hardens the already-pruned `research-design` pack. It keeps all 9 retained research-method owners, removes stale cross-skill/helper language, and protects the internal boundaries with focused route probes.

The six-stage runtime is unchanged. Skill usage remains binary:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / unused
```

No advisory state, stage assistant state, primary/secondary hierarchy, or helper-expert dispatch was added.

## Counts

| Field | Before | After |
| --- | ---: | ---: |
| `skill_candidates` | 9 | 9 |
| `route_authority_candidates` | 9 | 9 |
| `stage_assistant_candidates` | 0 | 0 |
| physical directory deletion | 0 | 0 |

## Retained Owners

| Skill | Boundary |
| --- | --- |
| `designing-experiments` | Study-design choice and experiment/quasi-experiment specification before analysis |
| `performing-causal-analysis` | Existing-data causal effect estimation, robustness checks, and fitted-result interpretation |
| `performing-regression-analysis` | Regression modeling, diagnostics, coefficient interpretation, and residual analysis |
| `hypothesis-generation` | Testable hypotheses, predictions, mechanisms, and validation experiments from observations |
| `scientific-brainstorming` | Open-ended research ideation, gaps, mechanisms, and possible directions |
| `hypogenic` | Explicit HypoGeniC or automated LLM hypothesis generation/testing workflows |
| `literature-matrix` | Literature matrix, paper-combination, A+B idea generation, and unified frameworks |
| `experiment-failure-analysis` | Failed experiment diagnosis and recovery/abandonment decisions |
| `research-grants` | Grant aims, significance, innovation, budgets, and review logic |

## Removed Cross-Skill Language

| Skill | Cleanup |
| --- | --- |
| `hypothesis-generation` | Removed mandatory `scientific-schematics` and `venue-templates` cross-skill language |
| `research-grants` | Removed mandatory `scientific-schematics` cross-skill language |
| `scientific-brainstorming` | Reworded consultation-style references as local reference usage |

## Protected Route Boundaries

| Prompt type | Expected owner |
| --- | --- |
| Design quasi-experiment and do not model yet | `designing-experiments` |
| Existing panel data causal effect estimation | `performing-causal-analysis` |
| Plain hypothesis generation without HypoGeniC | `hypothesis-generation` |
| Open-ended scientific ideation | `scientific-brainstorming` |
| Explicit HypoGeniC workflow | `hypogenic` |
| Literature matrix / A+B innovation | `literature-matrix` |
| LaTeX/PDF paper build | `scholarly-publishing-workflow / latex-submission-pipeline`, not `research-design` |

## Verification

| Command | Result |
| --- | --- |
| `python -m pytest tests/runtime_neutral/test_research_design_pack_consolidation.py -q` | PASS, 25 tests |
| `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1` | PASS, 548 assertions |
| `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1` | PASS, 531 assertions |
| `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\probe-scientific-packs.ps1` | PASS, 118 cases, bad=0; `research-design` 5 cases at 100% pack and skill match |
| `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1` | PASS |
| `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1` | PASS, 45/45 config pairs matched |
| `git diff --check` | PASS |

## Verification Repair

`vibe-offline-skills-gate.ps1` previously read JSON with default PowerShell encoding and could misparse UTF-8 Chinese strings in `pack-manifest.json`. This pass changed that script to read JSON through UTF-8 file APIs, then regenerated `config/skills-lock.json` with the existing repository generator.

## Remaining Caveat

Route selection is not proof of material skill use. This pass only makes selection clearer and removes stale helper semantics.
