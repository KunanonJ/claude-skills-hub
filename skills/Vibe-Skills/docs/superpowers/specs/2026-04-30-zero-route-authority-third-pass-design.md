# Zero Route Authority Third Pass Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-30

## 1. Goal

This design defines the third cleanup pass for Vibe-Skills packs that still have
`skill_candidates` but no `route_authority_candidates`.

The goal is to continue reducing the remaining zero-route-authority surface
without changing the public six-stage Vibe runtime. Retained skills must fit the
simplified skill-use model:

```text
candidate skill -> selected skill -> used / unused
```

This pass must not reintroduce helper experts, stage assistants,
primary/secondary skill states, advisory routing, consultation routing, or hidden
assistant ownership.

## 2. Current Evidence

The working tree was clean before this design was written:

```text
main...origin/main [ahead 167]
```

The latest merged cleanup completed the second zero-route-authority pass:

```text
18316ec0 chore: refresh skills lock after zero route second pass
2453c1b6 docs: record zero route authority second pass
1a5f3b23 fix: clean zero route authority second pass
```

A fresh manifest scan after that merge showed:

```text
total packs: 44
missing skill directories: 0
route/stage candidates outside skill_candidates: 0
non-empty stage_assistant_candidates: 0
zero-route-authority packs: 14
```

The remaining zero-route-authority packs are:

```text
docs-markitdown-conversion
ip-uspto-patents
science-astropy
science-pymatgen
science-simpy-simulation
science-fluidsim-cfd
science-matchms-spectra
science-matlab-octave
science-neuropixels
science-pymc-bayesian
science-pymoo-optimization
science-rowan-chemistry
ml-stable-baselines3
science-timesfm-forecasting
```

Representative strong-name route probes currently select the expected skills for
all 14 packs. The remaining issue is the manifest and rule contract: retained
skills are not declared as direct route owners, and 10 of the 14 lack explicit
`skill-routing-rules` entries.

## 3. Scope

### 3.1 In Scope

This pass will:

- Add explicit direct route authority for retained single-skill packs.
- Add focused route rules and keyword-index coverage for retained skills,
  especially the 10 packs that currently lack `skill-routing-rules`.
- Physically delete a skill only when inspection shows it is low-value for the
  direct route surface and has no useful assets that must be migrated.
- Mark a skill as manual-review instead of deleting it when it has useful
  scripts, references, examples, or assets but cannot yet justify direct route
  ownership.
- Add regression tests proving prompt-level routing behavior and deletion or
  manual-review cleanup.
- Write a governance record documenting retained owners, deleted or deferred
  skills, and remaining route concerns.
- Refresh `config/skills-lock.json` only after config, skill, test, and
  governance changes are stable.

### 3.2 Out Of Scope

This pass will not:

- Change the six-stage Vibe runtime.
- Modify `config/specialist-consultation-policy.json`.
- Remove runtime or presentation compatibility fields such as
  `stage_assistant_candidates`, `primary_skill`, `accept_primary`, or
  `consultation_bucket`.
- Audit dense packs such as `bio-science`, `docs-media`, `data-ml`,
  `science-chem-drug`, or `scholarly-publishing-workflow`.
- Treat route selection as proof that a skill was materially used in a real
  task.
- Add stage assistants, primary/secondary skill states, advisory routing, or
  consultation routing.

## 4. Retention And Deletion Rules

### 4.1 Keep As Direct Route Owner

A skill should remain as direct route owner only when all three tests pass:

1. The user problem can be stated in one sentence.
2. This skill is more appropriate than existing packs for owning that problem.
3. The directory contains useful content, such as a readable `SKILL.md`,
   references, scripts, examples, or assets.

### 4.2 Delete Candidate

A skill enters deletion review when any of these are true:

1. It is only a narrow library wrapper with no likely direct user request.
2. It overlaps an existing pack and cannot justify independent route ownership.
3. Its directory is thin and lacks scripts, references, examples, assets, or
   unique instructions.
4. It only routes when the exact library name is mentioned and does not cover
   natural-language tasks.
5. It adds more route noise than practical capability.

Deletion is allowed only after checking the skill directory for useful assets.

### 4.3 Manual Review

Manual review is the fallback when a skill should not become a direct route
owner yet, but its directory has useful content that should not be discarded in
this pass.

Manual-review skills must be removed from the direct route surface for this pass
and documented in governance notes with the reason review is still needed.

## 5. Pack Decisions

### 5.1 Low-Risk Direct Owner Completion

These four packs already have route rules and strong-name probes that select the
expected skill. The target decision is to keep each as a direct route owner and
add focused regression coverage.

| Pack | Skill | Direct user problem |
| --- | --- | --- |
| `docs-markitdown-conversion` | `markitdown` | Convert PDF, DOCX, PPTX, XLSX, images, or office documents into Markdown through MarkItDown. |
| `ip-uspto-patents` | `uspto-database` | Search and retrieve USPTO patent records, patent text, claims, inventors, and patent metadata. |
| `science-astropy` | `astropy` | Work with astronomy data, FITS files, WCS coordinates, units, tables, and Astropy workflows. |
| `science-pymatgen` | `pymatgen` | Parse and analyze materials structures, CIF files, crystal structures, compositions, and pymatgen workflows. |

### 5.2 Direct Owner Candidates Requiring Rule Completion

These skills have useful directories and clear task boundaries. They should be
kept as direct route owners unless implementation review discovers contradicting
quality evidence.

| Pack | Skill | Current assets | Direct user problem |
| --- | --- | --- | --- |
| `science-simpy-simulation` | `simpy` | scripts and references | Build discrete-event simulations such as queues, resource systems, processes, and SimPy models. |
| `science-matchms-spectra` | `matchms` | references | Process, filter, compare, and score mass spectra with matchms. |
| `science-matlab-octave` | `matlab` | references | Write, debug, or convert MATLAB/Octave scripts and matrix workflows without capturing generic Python numeric work. |
| `science-neuropixels` | `neuropixels-analysis` | scripts, references, assets | Analyze Neuropixels electrophysiology data, spike sorting outputs, SpikeGLX/Open Ephys data, and related neuroscience workflows. |
| `science-pymc-bayesian` | `pymc` | scripts, references, assets | Build Bayesian statistical models, hierarchical models, MCMC/NUTS workflows, posterior checks, and PyMC models. |
| `science-pymoo-optimization` | `pymoo` | scripts and references | Build multi-objective and constrained optimization workflows with pymoo, including NSGA-II and Pareto analysis. |
| `ml-stable-baselines3` | `stable-baselines3` | scripts and references | Train and evaluate reinforcement-learning agents with Stable-Baselines3, including PPO/SAC/DQN workflows. |
| `science-timesfm-forecasting` | `timesfm-forecasting` | scripts, references, examples | Run TimesFM or foundation-model time-series forecasting, including zero-shot forecasts and prediction intervals. |

### 5.3 Delete Or Manual-Review Candidates

These two skills are not pre-approved for direct route ownership. Implementation
must inspect their actual directory content before deleting or deferring them.

| Pack | Skill | Initial concern | Target decision rule |
| --- | --- | --- | --- |
| `science-fluidsim-cfd` | `fluidsim` | CFD library surface may be too narrow for direct routing. | Delete if it is mostly a narrow library wrapper; keep or manual-review if references show a clear CFD simulation task owner. |
| `science-rowan-chemistry` | `rowan` | Quaternion rotation library may be too narrow and tool-like. | Delete if it only wraps a quaternion utility; keep or manual-review if it has clear chemistry or molecular-geometry task ownership. |

The implementation plan must not delete either directory blindly.

## 6. Options Considered

### Option A: Third-Pass Single-Skill Cleanup

Clean the remaining single-skill zero-authority packs, keep the clear direct
owners, and inspect the two narrow candidates before deletion or manual review.

Benefits:

- Directly reduces the remaining zero-authority class.
- Preserves useful specialist skills where the task boundary is clear.
- Allows physical deletion where the skill is truly low value.
- Keeps the blast radius limited to pack routing and skill directories.

Cost:

- Requires several route regression cases.
- May leave a small manual-review remainder if `fluidsim` or `rowan` contain
  useful assets but cannot justify direct ownership.

This is the recommended option.

### Option B: Delete Narrow Science Skills First

Start with physical deletion of all cold or niche science skills.

Benefits:

- Shrinks the skill catalog fastest.

Cost:

- High risk of deleting asset-bearing domain skills without enough review.
- Would conflict with the observed asset counts for many remaining skills.

### Option C: Runtime Terminology Cleanup First

Pause pack cleanup and remove or rename the remaining runtime/presentation
compatibility terms such as `primary_skill`, `stage_assistant_candidates`, and
`consultation_bucket`.

Benefits:

- Addresses broader architecture vocabulary.

Cost:

- Touches runtime behavior and compatibility surfaces.
- Does not reduce the current 14 zero-route-authority pack gap.

## 7. Proposed Design

Proceed with Option A.

Implementation should use an evidence-first route cleanup:

1. Add focused RED tests for retained direct owners and delete/manual-review
   decisions.
2. Inspect `fluidsim` and `rowan` directories before deciding deletion,
   retention, or manual review.
3. Update `config/pack-manifest.json`:
   - retained packs get `route_authority_candidates` equal to their retained
     direct owner skill
   - retained packs get `stage_assistant_candidates: []`
   - deleted/manual-review packs are removed from the active direct route
     surface according to the implementation decision
4. Update `config/skill-keyword-index.json` with narrow natural-language
   keywords for retained skills.
5. Update `config/skill-routing-rules.json` with positive and negative
   boundaries for retained skills.
6. Delete `fluidsim` and/or `rowan` directories only if inspection proves deletion
   is safe.
7. Write the governance note.
8. Refresh `config/skills-lock.json`.
9. Run focused tests and broader routing/config gates before completion.

## 8. Verification Requirements

Focused tests must prove:

- Retained packs have explicit `route_authority_candidates`.
- Retained packs have empty `stage_assistant_candidates`.
- Representative prompts select each retained skill:
  - MarkItDown document conversion
  - USPTO patent search
  - Astropy FITS/WCS work
  - pymatgen CIF/materials work
  - SimPy discrete-event simulation
  - matchms mass-spectra processing
  - MATLAB/Octave scripting
  - Neuropixels spike-sorting or electrophysiology analysis
  - PyMC Bayesian modeling
  - pymoo multi-objective optimization
  - Stable-Baselines3 reinforcement learning
  - TimesFM time-series forecasting
- Generic false positives remain blocked where important:
  - MATLAB should not capture generic Python/NumPy work.
  - Stable-Baselines3 should not capture ordinary supervised machine learning.
  - TimesFM should not capture generic scikit-learn regression without time-series
    forecasting intent.
  - matchms should not capture broad untargeted literature or generic plotting.
- `fluidsim` and `rowan` are either:
  - retained with direct-owner tests and rules, or
  - physically deleted with no manifest/index/rules/lock references, or
  - removed from active route ownership and documented as manual-review.
- The remaining zero-route-authority count matches the implementation decision:
  - `0` if both `fluidsim` and `rowan` are deleted or retained as direct owners
  - `1` or `2` only if one or both are intentionally deferred as manual-review
    and governance explains why.

Expected focused test file:

```text
tests/runtime_neutral/test_zero_route_authority_third_pass.py
```

Expected governance note:

```text
docs/governance/zero-route-authority-third-pass-2026-04-30.md
```

Broader verification should include:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_third_pass.py -q
python -m pytest tests/runtime_neutral/test_zero_route_authority_second_pass.py tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py -q
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
```

## 9. Success Criteria

This pass is complete only when:

- Every retained pack in scope has explicit direct route ownership.
- No pack in scope has non-empty `stage_assistant_candidates`.
- All retained skills have focused route probes.
- `fluidsim` and `rowan` have evidence-backed keep/delete/manual-review
  decisions.
- Any physically deleted skill is removed from bundled skills, manifest,
  keyword-index, routing rules, and skills lock.
- The governance note records before/after counts, retained direct owners,
  deletion or manual-review rationale, verification commands, and any remaining
  route gaps.
- The completion report does not claim runtime consultation or dense-pack cleanup
  was completed in this pass.
