# Bio-Science Boundary Hardening Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-30

## 1. Goal

This design freezes the next routing cleanup wave for the `bio-science` pack.

The goal is to keep the public six-stage Vibe runtime unchanged while making
`bio-science` less likely to steal routes from neighboring packs or from its own
more specific specialists.

The routing model remains deliberately simple:

```text
candidate skill -> selected skill -> used / unused
```

This pass must not reintroduce helper experts, stage assistants,
primary/secondary skill states, advisory routing, consultation routing, or
hidden assistant ownership.

## 2. Current Evidence

The current `main` branch has already completed the zero-route-authority cleanup:

```text
ZERO_ROUTE_COUNT 0
NONEMPTY_STAGE_ASSISTANT_COUNT 0
```

The current `bio-science` manifest state is:

| Metric | Current value |
| --- | ---: |
| `skill_candidates` | 26 |
| `route_authority_candidates` | 26 |
| `stage_assistant_candidates` | 0 |
| missing skill directories | 0 |
| candidates missing routing rules | 0 |
| candidates missing keyword-index entries | 0 |

The current direct owners are:

```text
alphafold-database
anndata
biopython
bioservices
cellxgene-census
clinvar-database
cosmic-database
deeptools
ensembl-database
gene-database
gget
gwas-database
kegg-database
opentargets-database
pdb-database
pydeseq2
pysam
reactome-database
scanpy
scvi-tools
arboreto
cobrapy
esm
flowio
geniml
string-database
```

The previous `bio-science` consolidation intentionally removed active
`stage_assistant_candidates` and made every retained candidate a direct route
owner. That solved the old helper-state problem. It did not fully solve the
dense-pack boundary problem: 26 specialists still compete inside one pack.

Representative current route probes are healthy:

| Prompt class | Current selected route |
| --- | --- |
| bulk RNA-seq differential expression and GO/KEGG enrichment | `bio-science / pydeseq2` |
| single-cell clustering with Scanpy | `bio-science / scanpy` |
| RDKit SMILES and Morgan fingerprints | `science-chem-drug / rdkit` |
| existing PDF extraction | `docs-media / pdf` |
| LaTeX manuscript PDF build | `scholarly-publishing-workflow / latex-submission-pipeline` |
| ML result figures and data visualization | `science-figures-visualization / scientific-visualization` |

This means the pack is not currently broken in the zero-route sense. The next
problem is route precision under dense specialist competition.

## 3. Problem Statement

`bio-science` covers too many problem families in a single route surface:

- general sequence and NCBI/Entrez work
- single-cell data containers and single-cell analysis
- bulk RNA-seq and NGS file processing
- gene, variant, pathway, target, and interaction databases
- protein structure and protein language model work
- metabolic network modeling and gene regulatory networks
- flow cytometry and genomic interval ML

All 26 skills can currently own a route. That is simple in state semantics, but
it leaves three practical risks:

1. A broad owner such as `biopython`, `scanpy`, `bioservices`, or `gget` can
   capture prompts that should route to a narrower specialist.
2. A narrow database skill can capture a whole workflow when the user only named
   the database as supporting evidence.
3. Neighboring packs such as `science-chem-drug`,
   `science-clinical-regulatory`, `science-literature-citations`,
   `science-medical-imaging`, and `data-ml` need stronger negative boundaries
   against broad biomedical language.

## 4. Non-Goals

This pass will not:

- Change the six-stage Vibe runtime.
- Change `config/specialist-consultation-policy.json`.
- Add stage assistants or advisory/consultation behavior.
- Reintroduce primary/secondary skill states.
- Split the repository into new physical subpacks.
- Physically delete asset-bearing skill directories in the first implementation
  pass.
- Claim route selection proves actual material skill use in a real task.

## 5. Options Considered

### Option A: Add Boundary Tests Only

Keep all config as-is and add more cross-pack regression probes.

Benefits:

- Lowest blast radius.
- Fast to implement.
- Protects against obvious regression without changing live behavior.

Cost:

- Does not reduce dense-pack ambiguity.
- Leaves broad skills and narrow database skills equally eligible for route
  ownership.
- Does not update the governance problem map to reflect current risks.

### Option B: Boundary-Harden The Current 26 Direct Owners

Keep all 26 candidates as direct route owners, but narrow the trigger boundary
for broad and database-like skills. Add tests for intra-pack specialist
selection and cross-pack false positives.

Benefits:

- Preserves the simplified two-state skill-use model.
- Avoids deleting asset-bearing directories prematurely.
- Directly addresses the current risk: route precision, not route authority
  absence.
- Keeps the change explainable and reversible.

Cost:

- Candidate count remains 26.
- Requires a focused test matrix and careful rule tuning.

This is the recommended option.

### Option C: Delete Or Move Narrow Skills First

Start by deleting or moving cold/narrow skills such as `bioservices`, `gget`,
`flowio`, `geniml`, `arboreto`, or `cobrapy`.

Benefits:

- Shrinks the catalog fastest.

Cost:

- Current directory inspection shows these skills are not empty shells.
- Premature deletion risks losing useful references/scripts/assets.
- It would optimize for size before proving replacement ownership.

## 6. Proposed Design

Proceed with Option B.

The implementation should harden `bio-science` boundaries in three layers:

1. **Problem-family map**

   Group the 26 current route owners into clear problem families:

   | Family | Skills |
   | --- | --- |
   | sequence and general bio Python | `biopython` |
   | single-cell analysis and containers | `scanpy`, `anndata`, `scvi-tools`, `cellxgene-census` |
   | bulk RNA-seq and NGS files | `pydeseq2`, `pysam`, `deeptools` |
   | gene, variant, and target evidence | `clinvar-database`, `cosmic-database`, `ensembl-database`, `gene-database`, `gget`, `gwas-database`, `opentargets-database` |
   | pathway, interaction, and systems biology | `kegg-database`, `reactome-database`, `string-database`, `cobrapy`, `arboreto` |
   | protein structure and protein ML | `alphafold-database`, `pdb-database`, `esm` |
   | specialized data types and genomic ML | `flowio`, `geniml`, `bioservices` |

2. **Intra-pack boundary rules**

   The following broad skills need tighter positive and negative boundaries:

   | Skill | Boundary risk | Target rule |
   | --- | --- | --- |
   | `biopython` | broad default can swallow many bio tasks | Own FASTA/GenBank/SeqIO/Entrez/sequence conversion; lose to Scanpy, PyDESeq2, pysam, ESM, COBRApy, and flow cytometry when those signals are explicit. |
   | `scanpy` | broad single-cell owner can swallow container/reference/modeling tasks | Own single-cell clustering, QC, marker genes, UMAP/t-SNE, annotation; lose to AnnData, scVI, and CELLxGENE when those signals are explicit. |
   | `bioservices` | cross-database wrapper can overlap KEGG/Reactome/OpenTargets/Gene/Ensembl | Own explicit BioServices or multi-service aggregation prompts; lose to named database specialists. |
   | `gget` | quick lookup tool can overlap gene/ensembl/alphafold/opentargets | Own explicit gget, quick BLAST, Enrichr, and fast gene/transcript lookup; lose to named database specialists when the prompt asks for their deeper workflow. |
   | `pydeseq2` | bulk RNA-seq can overlap Scanpy and generic statistics | Own DESeq2-style bulk RNA-seq counts, Wald tests, FDR, volcano/MA plots; lose to single-cell prompts and generic regression. |
   | `pysam` | NGS file IO can overlap Biopython and TileDB-VCF | Own BAM/SAM/CRAM/VCF parsing, pileup, coverage, and region extraction; lose to generic sequence parsing and TileDB-VCF storage prompts. |
   | `deeptools` | genomics signal tracks can overlap plotting/visualization | Own BAM-to-bigWig, heatmap/profile plots around genomic features, and deepTools QC; lose to generic scientific figures. |

3. **Cross-pack boundary tests**

   Add regression probes proving `bio-science` does not steal:

   - `science-chem-drug / rdkit` for SMILES, Morgan fingerprints, molecule
     descriptors, docking, ChEMBL, PubChem, DrugBank, and ADMET benchmarks.
   - `science-clinical-regulatory` for ClinicalTrials.gov, FDA labels,
     treatment plans, CPIC/ClinPGx, and ISO 13485.
   - `science-literature-citations` for PubMed literature retrieval, BibTeX,
     Zotero, citation formatting, and systematic literature review.
   - `science-medical-imaging` for DICOM, pathology images, IDC, PathML, and
     OMERO.
   - `data-ml` for generic supervised ML, feature engineering, leakage checks,
     model evaluation, SHAP, and non-bio tabular ML.

## 7. Candidate Decisions

No physical deletion is pre-approved for this pass.

The current target is:

| Category | Decision |
| --- | --- |
| high-confidence direct owners | keep all 26 for now |
| stage assistants | none |
| manual-review candidates | none by default; only create if focused inspection finds a skill cannot own a distinct user problem |
| deletion candidates | none by default; only after asset inspection and replacement-owner proof |

Skills that deserve the closest inspection during implementation:

| Skill | Why inspect |
| --- | --- |
| `bioservices` | A broad wrapper over many databases; may need explicit BioServices/multi-service trigger only. |
| `gget` | Quick lookup overlaps multiple named database specialists. |
| `biopython` | Broad default owner and sequence toolkit; must not be generic bio fallback for everything. |
| `scanpy` | Strong single-cell default; must not steal scVI/AnnData/CELLxGENE prompts. |
| `geniml` | Bio-specific ML surface; must not steal generic ML or protein ESM prompts. |
| `flowio` | Narrow FCS/flow cytometry owner; likely should require explicit FCS/flow cytometry signal. |

## 8. Test Design

Focused tests should be added or extended under:

```text
tests/runtime_neutral/test_bio_science_boundary_hardening.py
```

Required positive probes:

| Prompt class | Expected route |
| --- | --- |
| FASTA/GenBank/SeqIO/Entrez sequence conversion | `bio-science / biopython` |
| Scanpy single-cell QC, UMAP, Leiden, marker genes | `bio-science / scanpy` |
| AnnData h5ad container, obs/var, backed mode | `bio-science / anndata` |
| scVI/scANVI latent model or batch correction | `bio-science / scvi-tools` |
| CELLxGENE Census cell/tissue/disease query | `bio-science / cellxgene-census` |
| PyDESeq2 bulk RNA-seq differential expression | `bio-science / pydeseq2` |
| pysam BAM/CRAM/VCF pileup or coverage | `bio-science / pysam` |
| deepTools BAM-to-bigWig or heatmap/profile | `bio-science / deeptools` |
| BioServices explicit multi-database aggregation | `bio-science / bioservices` |
| gget quick BLAST/gene lookup | `bio-science / gget` |
| COBRApy FBA/flux balance | `bio-science / cobrapy` |
| ESM protein embeddings | `bio-science / esm` |
| FCS flow cytometry parsing | `bio-science / flowio` |
| Genomic interval embeddings | `bio-science / geniml` |

Required intra-pack false-positive probes:

| Prompt class | Must not select |
| --- | --- |
| explicit scVI latent model | `scanpy` |
| explicit AnnData container editing | `scanpy` |
| explicit CELLxGENE Census query | `scanpy` |
| explicit BAM/VCF parsing | `biopython` |
| explicit ESM protein embedding | `biopython` |
| explicit COBRApy FBA | `biopython` |
| explicit KEGG REST pathway mapping | `bioservices` |
| explicit Reactome enrichment | `bioservices` |
| explicit Open Targets evidence | `gget` |

Required cross-pack false-positive probes:

| Prompt class | Expected non-bio owner |
| --- | --- |
| RDKit SMILES Morgan fingerprints | `science-chem-drug / rdkit` |
| ChEMBL IC50/Ki/Kd lookup | `science-chem-drug / chembl-database` |
| PubMed literature review and BibTeX export | `science-literature-citations` |
| ClinicalTrials.gov NCT trial criteria | `science-clinical-regulatory / clinicaltrials-database` |
| DICOM metadata and medical image tags | `science-medical-imaging / pydicom` |
| generic scikit-learn random forest on tabular data | `data-ml / scikit-learn` |

## 9. Config Changes

Implementation should be config-first:

1. Keep `bio-science.skill_candidates` unchanged unless focused inspection
   proves a candidate lacks a distinct problem.
2. Keep `bio-science.route_authority_candidates` equal to retained candidates.
3. Keep `bio-science.stage_assistant_candidates` as `[]`.
4. Update `config/skill-keyword-index.json` only with narrow, concrete trigger
   phrases.
5. Update `config/skill-routing-rules.json` to add negative boundaries for
   over-broad skills and positive boundaries for explicit specialist intent.
6. Refresh `config/skills-lock.json` only after test/config/doc changes are
   stable.

Avoid broad new keywords such as only `bio`, `biology`, `omics`, or `analysis`.
They are too wide for a dense pack.

## 10. Governance Record

Implementation should create:

```text
docs/governance/bio-science-boundary-hardening-2026-04-30.md
```

The governance note must record:

- current and final candidate counts
- whether any candidate was removed
- whether any directory was physically deleted
- the final problem-family map
- the broad-skill boundary decisions
- the exact positive and false-positive probes
- remaining risks that were intentionally deferred

## 11. Verification Requirements

Focused verification:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_boundary_hardening.py -q
python -m pytest tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_direct_owner_routing.py -q
```

Broader verification:

```powershell
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
git diff --check
```

If any routing change affects chemistry, literature, clinical, imaging, or ML
boundaries, run the affected focused tests too:

```powershell
python -m pytest tests/runtime_neutral/test_science_chem_drug_pack_consolidation.py tests/runtime_neutral/test_science_literature_peer_review_consolidation.py tests/runtime_neutral/test_science_clinical_regulatory_pack_consolidation.py tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
```

## 12. Success Criteria

This pass is complete only when:

- `bio-science` still has no stage-assistant semantics.
- Every retained `bio-science` direct owner has a clear one-sentence problem
  boundary.
- Broad owners no longer steal explicit specialist prompts.
- Neighboring packs retain their own obvious domains.
- Any removed candidate is documented with a replacement owner and asset
  migration rationale.
- Any physical deletion is backed by asset inspection, config cleanup, lock
  refresh, and offline-skill verification.
- Completion wording does not claim dense-pack cleanup outside `bio-science`.
