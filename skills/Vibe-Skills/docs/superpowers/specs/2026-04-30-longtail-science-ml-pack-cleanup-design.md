# Longtail Science ML Pack Cleanup Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-30

## 1. Goal

This pass audits and cleans up the longtail single-skill science and ML packs without changing the public Vibe six-stage runtime.

The routing model remains:

```text
candidate skill -> selected skill -> used / unused
```

This pass does not introduce advisory experts, consultation state, primary/secondary skill hierarchy, helper experts, or stage assistants.

The goal is to reduce ordinary-route noise from cold, vendor-specific, or overly broad single-tool packs while preserving genuinely useful specialist skills that have clear user problem ownership and useful bundled assets.

## 2. Scope

Target packs:

| Pack | Skill |
| --- | --- |
| `science-simpy-simulation` | `simpy` |
| `science-fluidsim-cfd` | `fluidsim` |
| `science-matchms-spectra` | `matchms` |
| `science-matlab-octave` | `matlab` |
| `science-neuropixels` | `neuropixels-analysis` |
| `science-pymc-bayesian` | `pymc` |
| `science-pymoo-optimization` | `pymoo` |
| `science-rowan-chemistry` | `rowan` |
| `ml-stable-baselines3` | `stable-baselines3` |
| `science-timesfm-forecasting` | `timesfm-forecasting` |
| `ml-torch-geometric` | `torch-geometric` |

All target packs currently have one direct route owner:

```text
skill_candidates = 1
route_authority_candidates = 1
stage_assistant_candidates = 0
```

This is a quality and boundary cleanup, not a structural stage-assistant cleanup.

## 3. Current Problems

### 3.1 Longtail Packs Are Ordinary Route Owners Without Main Matrix Coverage

The target packs are direct route owners but most are absent from the main route regression scripts:

```text
scripts/verify/vibe-pack-regression-matrix.ps1
scripts/verify/vibe-skill-index-routing-audit.ps1
scripts/verify/probe-scientific-packs.ps1
```

Some are covered by zero-route-authority tests, but that only proves direct ownership was assigned. It does not prove that each pack has stable boundaries against neighboring packs after the broader cleanup.

### 3.2 Several Packs Are Valuable But Cold

Some packs solve real specialist problems but are low-frequency and should not trigger on broad wording:

| Pack | Problem |
| --- | --- |
| `science-simpy-simulation` | SimPy and discrete-event simulations should not own generic simulation or planning prompts. |
| `science-fluidsim-cfd` | FluidSim/CFD should not own generic physics, Python simulation, or numerical PDE prompts unless CFD signals are explicit. |
| `science-neuropixels` | Neuropixels should remain narrow to electrophysiology, spike sorting, SpikeGLX/Open Ephys, Kilosort, and neural recording workflows. |
| `science-pymoo-optimization` | pymoo should not steal broad experiment design, regression, causal analysis, or generic optimization prompts. |
| `science-timesfm-forecasting` | TimesFM should not steal ordinary scikit-learn regression, generic time-series EDA, or business forecast prompts without TimesFM/foundation forecasting signals. |

### 3.3 Two Packs Are Strong Candidates For Ordinary-Route Removal Or Extreme Narrowing

| Pack | Concern |
| --- | --- |
| `science-rowan-chemistry` | Rowan is vendor/cloud-specific and overlaps with chemistry, drug, docking, conformer, pKa, geometry optimization, and quantum-chemistry work. It should not be a broad chemistry owner. |
| `science-matlab-octave` | MATLAB/Octave is a broad tool surface and can steal generic matrix, numerical computing, simulation, or data-analysis prompts that should remain with Python/data/science owners unless MATLAB/Octave is explicit. |

These two are the primary cleanup targets for this pass.

### 3.4 Three Packs Should Be Kept And Hardened

| Pack | Reason To Keep |
| --- | --- |
| `science-matchms-spectra` | Owns mass-spectra/MS/MS spectral similarity and metabolomics spectrum processing. |
| `science-pymc-bayesian` | Owns PyMC Bayesian modeling, MCMC/NUTS, posterior checks, hierarchical models, and probabilistic programming. |
| `ml-torch-geometric` | Owns PyTorch Geometric/PyG graph neural networks, graph classification, node classification, link prediction, and heterogeneous graphs. |

These are narrow enough to remain direct route owners, but they still need explicit false-positive probes.

## 4. Target Decisions

### 4.1 Keep And Harden

Keep these as direct route owners:

```text
science-matchms-spectra -> matchms
science-pymc-bayesian -> pymc
ml-torch-geometric -> torch-geometric
```

Required boundary tests:

- `matchms` wins explicit MS/MS, mass spectra, spectral similarity, metabolomics spectrum processing prompts.
- `matchms` does not win PubMed, generic chemistry, or non-spectral metabolomics prompts.
- `pymc` wins PyMC, Bayesian hierarchical model, MCMC/NUTS, posterior predictive checks, and probabilistic programming prompts.
- `pymc` does not win generic regression, causal analysis, or scikit-learn modeling prompts.
- `torch-geometric` wins PyG, torch_geometric, GNN, GCN, GAT, graph classification, node classification, and link prediction prompts.
- `torch-geometric` does not win generic neural-network, network graph visualization, or molecule-only prompts without PyG/GNN signals.

### 4.2 Keep Cold Specialists But Narrow Triggers

Keep these as direct route owners, but narrow their trigger contracts and add regression evidence:

```text
science-simpy-simulation -> simpy
science-fluidsim-cfd -> fluidsim
science-neuropixels -> neuropixels-analysis
science-pymoo-optimization -> pymoo
science-timesfm-forecasting -> timesfm-forecasting
ml-stable-baselines3 -> stable-baselines3
```

Required boundary direction:

- These packs should require explicit tool names or unmistakable domain signals.
- Generic "simulation", "optimization", "forecasting", "agent", "time series", "physics", "neural", or "modeling" prompts should not be enough by themselves.
- Chinese trigger terms should be added only where they are concrete and domain-specific.

### 4.3 Move Out Or Extreme-Narrow Ordinary Routing

Primary cleanup targets:

```text
science-rowan-chemistry -> rowan
science-matlab-octave -> matlab
```

Target decision:

- Remove them from broad ordinary routing if tests show they steal neighboring owner prompts.
- If not removed, make them explicit-tool routes only: route only when the prompt says Rowan / rowan-python / labs.rowansci.com, or MATLAB / Octave / Simulink / `.m` script.
- Do not physically delete directories in this pass unless a directory is proven to be a disposable alias with no unique scripts, references, examples, or assets.

Expected boundary:

- Rowan should not own generic chemistry, RDKit, docking, PubChem, ChEMBL, pKa, conformer search, quantum chemistry, or molecular ML prompts unless Rowan is explicit.
- MATLAB should not own generic NumPy, Python matrix, Jupyter, scientific visualization, data analysis, or numerical computing prompts unless MATLAB/Octave/Simulink/.m is explicit.

## 5. Non-Goals

This pass will not:

- Change Vibe's six-stage runtime.
- Add `stage_assistant_candidates`.
- Add advisory, consultation, helper, primary, or secondary skill states.
- Reintroduce auxiliary expert routing.
- Physically delete useful bundled skill directories without asset review.
- Install or deploy the changed repository into Codex.
- Claim real task material skill use from routing/config changes.

## 6. Implementation Surfaces

Expected files for the implementation plan:

```text
tests/runtime_neutral/test_longtail_science_ml_pack_cleanup.py
config/pack-manifest.json
config/skill-keyword-index.json
config/skill-routing-rules.json
scripts/verify/vibe-pack-regression-matrix.ps1
scripts/verify/vibe-skill-index-routing-audit.ps1
scripts/verify/probe-scientific-packs.ps1
docs/governance/longtail-science-ml-pack-cleanup-2026-04-30.md
config/skills-lock.json
```

`bundled/skills/<skill>/SKILL.md` should be changed only when the current skill text creates an ambiguous route boundary. Do not rewrite full skill documents for style only.

## 7. Regression Strategy

Focused Python tests should assert:

- Every target pack has either a retained direct owner or an intentional ordinary-route removal/narrowing decision.
- `stage_assistant_candidates` remains empty for every target pack.
- `rowan` and `matlab` no longer steal broad neighboring prompts.
- Kept packs still win explicit tool/domain prompts.
- Cold specialist packs do not win broad generic prompts.

PowerShell verification should add:

- Positive route cases for the retained high-value owners.
- False-positive cases for broad generic simulation, optimization, forecasting, matrix, chemistry, and ML prompts.
- Scientific probe coverage for the science/ML longtail packs that remain ordinary route owners.

## 8. Acceptance Criteria

The cleanup is acceptable when:

- `stage_assistant_candidates` remains empty for all target packs.
- The simplified routing model remains `candidate skill -> selected skill -> used / unused`.
- `rowan` and `matlab` are either removed from broad ordinary routing or made explicit-tool-only by tests.
- Retained cold specialists have narrow positive triggers and negative boundary coverage.
- Main route regression scripts include coverage for the retained longtail packs.
- `skills-lock.json` is refreshed if bundled skill docs or physical directories change.
- Governance evidence records exact pass counts and states that this is routing/config cleanup only, not real task material skill use.

## 9. Risk Handling

| Risk | Handling |
| --- | --- |
| Useful assets are lost by deleting a specialist directory | Do not physically delete asset-bearing directories in this pass. |
| Narrowing Rowan breaks explicit Rowan users | Keep explicit Rowan/tool-name prompts covered if Rowan remains routed. |
| Narrowing MATLAB breaks explicit MATLAB users | Keep explicit MATLAB/Octave/Simulink/.m prompts covered if MATLAB remains routed. |
| Cold specialists become invisible | Add precise positive probes for explicit domain/tool prompts. |
| Generic prompts lose all useful routing | Use blocked-pack assertions rather than forcing a different owner unless a correct neighboring owner is clear. |

## 10. Evidence Boundary

This pass proves routing/config/bundled-doc/test cleanup only. It does not prove that a real user task materially used any of these skills.

Material skill use still requires concrete task artifacts such as execution logs, produced code, generated reports, model outputs, figures, or other deliverables from an actual routed run.
