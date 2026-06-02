# Science Lab Automation Pack Consolidation Design

Date: 2026-04-29

## Goal

Consolidate `science-lab-automation` into a small, product- and workflow-specific routing surface for wet-lab automation tasks.

This pass keeps the existing six-stage Vibe runtime unchanged and preserves the simplified skill-use model:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / unused
```

There are no primary/secondary, consult, advisory, or stage-assistant execution states. A skill is either selected for the task or it is not selected.

## Current State

`science-lab-automation` currently has 7 candidates and no explicit route split:

| Metric | Current value |
| --- | ---: |
| `skill_candidates` | 7 |
| `route_authority_candidates` | 0 |
| `stage_assistant_candidates` | 0 |
| explicit role split | no |

Current candidates:

```text
opentrons-integration
pylabrobot
protocolsio-integration
benchling-integration
labarchive-integration
latchbio-integration
ginkgo-cloud-lab
```

Current defaults:

| Task | Default |
| --- | --- |
| `planning` | `protocolsio-integration` |
| `coding` | `opentrons-integration` |
| `research` | `protocolsio-integration` |

Observed issues:

- Lab robot protocol execution, multi-vendor robot control, protocol publishing/search, ELN/LIMS automation, cloud-lab ordering, and bioinformatics workflow deployment are mixed in one flat candidate pool.
- The pack has no explicit `route_authority_candidates`, so it does not declare which skills can own user tasks.
- Several broad keywords overlap: `protocol`, `liquid handling`, `ELN`, `lab notebook`, `data pipeline`, and `bioinformatics platform`.
- `latchbio-integration` is a bioinformatics workflow platform skill, not a wet-lab automation owner.
- The existing scientific-pack probe only covers Opentrons and protocols.io, leaving the other boundaries unprotected.

## Non-Goals

This wave will not:

- Change the six-stage Vibe runtime.
- Add a new pack for LatchBio.
- Physically delete any skill directory.
- Treat `latchbio-integration` as low-quality only because it is moved out of this pack.
- Introduce assistant, advisory, consult, or primary/secondary routing concepts.
- Keep any `stage_assistant_candidates` semantics for this pack.

## Target Routing Contract

After consolidation:

| Field | Before | After |
| --- | ---: | ---: |
| `skill_candidates` | 7 | 6 |
| `route_authority_candidates` | 0 | 6 |
| `stage_assistant_candidates` | 0 | 0 |
| physical directory deletion | 0 | 0 |

`route_authority_candidates` is a compatibility mirror of the selectable owner list. It does not create a second execution model.

Target kept route authorities:

| Skill | Owns user problems like | Boundary |
| --- | --- | --- |
| `opentrons-integration` | Opentrons OT-2/Flex protocol scripts, Protocol API v2, deck setup, pipetting steps, Opentrons modules | Opentrons hardware only; not multi-vendor robot orchestration |
| `pylabrobot` | Multi-vendor lab automation with Hamilton, Tecan, Opentrons backends, plate readers, pumps, resource simulation | Cross-vendor robot/equipment owner; not Opentrons-only official API |
| `protocolsio-integration` | protocols.io search, create, update, publish, workspace/file management, protocol discussion handling | protocols.io product/API owner; not every generic protocol-writing request |
| `benchling-integration` | Benchling registry, inventory, ELN entries, workflows, apps, data warehouse, R&D platform automation | Benchling product owner; not generic ELN unless Benchling is named |
| `labarchive-integration` | LabArchives notebooks, entries, attachments, backups, API workflows | LabArchives product owner; not generic ELN unless LabArchives is named |
| `ginkgo-cloud-lab` | Ginkgo Cloud Lab protocol selection, input preparation, pricing/order workflow, cloud.ginkgo.bio services | Ginkgo cloud-lab owner; not generic outsourcing or all lab services |

Moved out of this pack:

| Skill | Target role | Rationale | Physical deletion |
| --- | --- | --- | --- |
| `latchbio-integration` | remove from `science-lab-automation` candidates | LatchBio is for bioinformatics workflow deployment, Latch SDK, LatchFile/LatchDir, Nextflow/Snakemake, and serverless computational pipelines. It is not a wet-lab automation owner. | no deletion in this pass |

`stage_assistant_candidates` should be an explicit empty array:

```json
"stage_assistant_candidates": []
```

## Problem Map

| User problem | Expected pack/skill | Notes |
| --- | --- | --- |
| `write an Opentrons OT-2 96-well dispensing and mixing protocol` | `science-lab-automation / opentrons-integration` | Existing probe must remain stable |
| `write an Opentrons Flex thermocycler or magnetic module protocol` | `science-lab-automation / opentrons-integration` | Official Protocol API owner |
| `control Hamilton or Tecan with a unified Python lab automation framework` | `science-lab-automation / pylabrobot` | Multi-vendor owner |
| `simulate a liquid handling workflow with PyLabRobot resources` | `science-lab-automation / pylabrobot` | Simulation/resource owner |
| `search protocols.io for a PCR protocol and summarize reagents` | `science-lab-automation / protocolsio-integration` | Existing probe must remain stable |
| `create or publish a protocol on protocols.io` | `science-lab-automation / protocolsio-integration` | Product-specific protocol publishing |
| `query Benchling registry, DNA sequence inventory, or workflow tasks` | `science-lab-automation / benchling-integration` | Benchling R&D data owner |
| `automate Benchling ELN or data warehouse export` | `science-lab-automation / benchling-integration` | Benchling product owner |
| `backup a LabArchives notebook with entries and attachments` | `science-lab-automation / labarchive-integration` | LabArchives product owner |
| `upload automated experiment output to LabArchives` | `science-lab-automation / labarchive-integration` | LabArchives API owner |
| `submit a Ginkgo Cloud Lab cell-free protein expression validation run` | `science-lab-automation / ginkgo-cloud-lab` | Ginkgo Cloud Lab owner |
| `prepare cloud.ginkgo.bio order inputs and estimate protocol pricing` | `science-lab-automation / ginkgo-cloud-lab` | Ginkgo service owner |
| `deploy a Nextflow RNA-seq workflow with Latch SDK` | not `science-lab-automation`; should route to a bioinformatics/workflow owner if available | LatchBio should not win this pack |
| `build a bioinformatics data pipeline on LatchBio` | not `science-lab-automation` | Computational workflow, not lab automation |
| `write a generic wet-lab protocol in Markdown without protocols.io` | not necessarily `science-lab-automation` | Avoid over-routing generic writing to protocols.io |
| `use PubMed to find wet-lab methods papers` | not `science-lab-automation` | Literature/citation boundary |

## Routing Changes To Implement Later

After this spec is approved, the implementation plan should cover:

1. Update `config/pack-manifest.json`:
   - shrink `skill_candidates` from 7 to 6;
   - add `route_authority_candidates` with the same 6 kept skills;
   - add `stage_assistant_candidates: []`;
   - keep defaults as `planning: protocolsio-integration`, `coding: opentrons-integration`, and `research: protocolsio-integration`.
2. Update `config/skill-keyword-index.json`:
   - keep product- and hardware-specific keywords for the six retained owners;
   - remove or neutralize ordinary route keywords for `latchbio-integration` from this pack's effective selection path;
   - narrow generic terms such as `protocol`, `ELN`, `lab notebook`, and `cloud lab` with product-specific phrases.
3. Update `config/skill-routing-rules.json`:
   - add strong positive signals for Opentrons OT-2/Flex, PyLabRobot, protocols.io, Benchling, LabArchives, and Ginkgo Cloud Lab;
   - add negative boundaries for PubMed/literature search, DICOM/imaging, SEC/finance, LatchBio bioinformatics pipelines, Nextflow, Snakemake, RNA-seq, and generic data pipelines;
   - prevent `latchbio-integration` from winning ordinary lab-automation prompts.
4. Refresh `config/skills-lock.json` only after config and rule edits are stable.

## Regression Evidence

Focused route probes should be added or extended before claiming this pack is cleaned:

| Probe | Expected |
| --- | --- |
| `lab_opentrons_ot2_protocol` | `science-lab-automation / opentrons-integration` |
| `lab_opentrons_flex_module` | `science-lab-automation / opentrons-integration` |
| `lab_pylabrobot_hamilton_tecan` | `science-lab-automation / pylabrobot` |
| `lab_pylabrobot_simulation` | `science-lab-automation / pylabrobot` |
| `lab_protocolsio_pcr` | `science-lab-automation / protocolsio-integration` |
| `lab_protocolsio_publish` | `science-lab-automation / protocolsio-integration` |
| `lab_benchling_registry_inventory` | `science-lab-automation / benchling-integration` |
| `lab_benchling_eln_export` | `science-lab-automation / benchling-integration` |
| `lab_labarchives_backup` | `science-lab-automation / labarchive-integration` |
| `lab_labarchives_upload` | `science-lab-automation / labarchive-integration` |
| `lab_ginkgo_cloud_lab_order` | `science-lab-automation / ginkgo-cloud-lab` |
| `lab_ginkgo_cell_free_expression` | `science-lab-automation / ginkgo-cloud-lab` |
| `lab_latchbio_nextflow_not_lab_automation` | not `science-lab-automation` |
| `lab_generic_markdown_protocol_not_protocolsio` | not necessarily `science-lab-automation` |
| `lab_pubmed_methods_not_lab_automation` | not `science-lab-automation` |

Expected verification sequence after implementation:

```powershell
python -m pytest tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py -q
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

## Completion Criteria

The implementation is complete only when:

- `science-lab-automation` has an explicit six-skill selectable route-authority list.
- `stage_assistant_candidates` is explicitly empty.
- `latchbio-integration` is removed from this pack's ordinary route candidates.
- Opentrons, PyLabRobot, protocols.io, Benchling, LabArchives, and Ginkgo Cloud Lab each have protected positive route probes.
- LatchBio bioinformatics workflow prompts do not route to `science-lab-automation`.
- Generic protocol-writing, PubMed/literature, imaging, finance, and computational pipeline prompts do not falsely route to this pack.
- No physical directory deletion is claimed in this pass.
