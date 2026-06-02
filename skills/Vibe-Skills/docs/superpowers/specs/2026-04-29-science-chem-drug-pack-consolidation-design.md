# Science Chem Drug Pack Consolidation Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-29

## 1. Goal

This design freezes the next routing cleanup wave for the `science-chem-drug` pack.

The goal is to keep the current six-stage Vibe runtime unchanged while making chem/drug skill routing simple and enforceable:

- A routed skill is either selected for use or not selected.
- No primary/secondary, consult, advisory, or stage-assistant semantics are introduced.
- Each retained skill must own a distinct user problem.
- Low-boundary helper skills are removed from ordinary routing before any physical directory deletion is considered.
- Regression probes must prove both positive ownership and false-positive boundaries.

## 2. Current State

Current `science-chem-drug` in `config/pack-manifest.json` has:

| Metric | Current value |
|---|---:|
| `skill_candidates` | 13 |
| `route_authority_candidates` | 0 |
| `stage_assistant_candidates` | 0 |
| explicit role split | no |

Current candidates:

```text
chembl-database
drugbank-database
pubchem-database
brenda-database
hmdb-database
zinc-database
datamol
deepchem
medchem
rdkit
diffdock
molfeat
pytdc
```

Current defaults:

```json
{
  "planning": "medchem",
  "coding": "rdkit",
  "research": "chembl-database"
}
```

Observed issues:

- Database lookup skills, cheminformatics toolkits, molecular ML skills, medicinal chemistry filters, and docking workflows compete in one flat pool.
- `route_authority_candidates` is missing, so the pack does not explicitly say which skills can own a route.
- `stage_assistant_candidates` is missing, which is compatible with the old flat model but not with the current simplified "use or not use" contract.
- `datamol` overlaps heavily with `rdkit`.
- `molfeat` overlaps with `rdkit` for fingerprints/descriptors and with `deepchem` for ML featurization.
- Generic ADMET/property prediction can currently drift to `data-ml / scikit-learn` instead of a chem/drug specialist.
- Existing scientific-pack probes only cover `rdkit`, `chembl-database`, and `diffdock`, leaving most boundaries unprotected.

## 3. Non-Goals

This wave will not:

- Change the six-stage Vibe runtime.
- Add a new database pack or subpack.
- Introduce assistant, advisory, consult, or primary/secondary routing concepts.
- Physically delete skill directories in the first implementation pass.
- Declare `datamol` or `molfeat` low-quality only because they are removed from ordinary routing.

## 4. Target Routing Contract

The pack should become a direct route-authority surface.

Target counts:

| Metric | Target value |
|---|---:|
| `skill_candidates` | 11 |
| `route_authority_candidates` | 11 |
| `stage_assistant_candidates` | 0 |

`route_authority_candidates` is used here only as a compatibility field for the selectable skill list. It does not create a new execution state.

Target kept route authorities:

| Skill | Owns user problems like | Boundary |
|---|---|---|
| `rdkit` | SMILES/SDF parsing, descriptors, fingerprints, similarity, substructure, reactions, molecular drawing | General cheminformatics implementation owner |
| `medchem` | drug-likeness, PAINS, structural alerts, SAR, lead optimization | Medicinal chemistry filtering and decision support |
| `diffdock` | protein-ligand docking pose prediction from PDB plus SMILES | Docking pose only, not generic affinity prediction |
| `deepchem` | molecular property prediction, ADMET/toxicity models, MoleculeNet, GNN workflows | Model-building owner for chem/drug ML |
| `pytdc` | TDC datasets, ADMET benchmark groups, scaffold splits, therapeutic ML benchmarks | Dataset and benchmark owner, not general model implementation |
| `chembl-database` | target-ligand activity, IC50/Ki/Kd, assay retrieval, SAR data tables | Bioactivity database owner |
| `drugbank-database` | approved drug metadata, drug-drug interactions, pharmacology, targets, pathways | Drug information and interaction owner |
| `pubchem-database` | CID lookup, SMILES/InChI, formula/properties, PubChem compound records | Compound identifier and property lookup owner |
| `zinc-database` | purchasable compound libraries, ZINC IDs, virtual screening source libraries | Screening-library source owner |
| `brenda-database` | EC numbers, Km/kcat/Vmax, enzyme kinetics, enzyme substrate specificity | Enzyme database owner |
| `hmdb-database` | HMDB IDs, metabolites, MS/MS or NMR reference spectra, biomarker/metabolomics lookup | Metabolomics database owner |

Target moved out of ordinary routing:

| Skill | Target role | Rationale | Physical deletion |
|---|---|---|---|
| `datamol` | remove from `science-chem-drug` `skill_candidates` | Useful wrapper, but no distinct route ownership beyond `rdkit` for current user-facing routing | defer until useful examples are reviewed and migrated |
| `molfeat` | remove from `science-chem-drug` `skill_candidates` | Useful featurization library, but overlaps with `rdkit` and `deepchem`; route should choose the broader problem owner | defer until ChemBERTa/featurization notes are migrated |

`stage_assistant_candidates` should be an explicit empty array:

```json
"stage_assistant_candidates": []
```

## 5. Problem Map

| User problem | Expected pack/skill | Notes |
|---|---|---|
| `用RDKit解析SMILES并计算Morgan fingerprint` | `science-chem-drug / rdkit` | Existing cross-pack boundary from bio-science cleanup must remain stable |
| `在 ChEMBL 查询某靶点 IC50 / Ki 活性数据` | `science-chem-drug / chembl-database` | Database lookup, not PubChem or DrugBank |
| `查询 DrugBank 药物相互作用和靶点` | `science-chem-drug / drugbank-database` | Interaction/pharmacology owner |
| `查询 PubChem CID、SMILES、InChI 和化合物物性` | `science-chem-drug / pubchem-database` | Identifier/property lookup owner |
| `从 ZINC 下载可购买小分子库用于虚拟筛选` | `science-chem-drug / zinc-database` | Library-source owner |
| `在 BRENDA 查询 EC number 的 Km 和 kcat` | `science-chem-drug / brenda-database` | Enzyme kinetics owner |
| `在 HMDB 用 MS/MS 谱鉴定代谢物` | `science-chem-drug / hmdb-database` | Metabolomics lookup owner |
| `做药物化学 SAR、PAINS 过滤和先导优化` | `science-chem-drug / medchem` | Medicinal chemistry owner |
| `用 DiffDock 做 PDB + SMILES docking pose prediction` | `science-chem-drug / diffdock` | Structure-based pose owner |
| `用 DeepChem 训练分子属性预测模型，做 scaffold split 和 GNN` | `science-chem-drug / deepchem` | Molecular ML implementation owner |
| `用 PyTDC 加载 ADMET benchmark 数据集` | `science-chem-drug / pytdc` | Therapeutic benchmark dataset owner |
| `用 datamol 批量标准化 SMILES 并生成分子指纹` | `science-chem-drug / rdkit` | Route to RDKit; preserve datamol content only as migration source |
| `用 MolFeat 生成 ChemBERTa embedding 和 ECFP 特征` | `science-chem-drug / deepchem` or `rdkit` by wording | Embedding/model context should prefer DeepChem; pure fingerprint context should prefer RDKit |
| `bulk RNA-seq 差异表达 / GO KEGG 富集` | not `science-chem-drug` | Should stay with `bio-science` |
| `PubMed 检索 / BibTeX / 文献综述` | not `science-chem-drug` | Should stay with literature/citation packs |
| `ClinicalTrials.gov / NCT / FDA label` | not `science-chem-drug` | Should stay with clinical/regulatory packs |

## 6. Routing Changes To Implement Later

After this spec is approved, the implementation plan should cover:

1. Update `config/pack-manifest.json`:
   - shrink `skill_candidates` from 13 to 11;
   - add `route_authority_candidates` with the same 11 kept skills;
   - add `stage_assistant_candidates: []`;
   - keep defaults as `planning: medchem`, `coding: rdkit`, `research: chembl-database`.
2. Update `config/skill-keyword-index.json`:
   - keep concrete positive keywords for the 11 retained owners;
   - remove or neutralize ordinary route keywords for `datamol` and `molfeat`;
   - add Chinese and English phrases for ADMET, scaffold split, docking pose, DrugBank interactions, HMDB metabolite identification, BRENDA enzyme kinetics, and ZINC screening libraries.
3. Update `config/skill-routing-rules.json`:
   - add stronger positive signals for retained owners;
   - add negative boundaries for PubMed, clinical trials, bulk RNA-seq, GO/KEGG gene enrichment, DICOM, and generic document work;
   - keep `datamol` and `molfeat` from winning ordinary prompts.
4. Refresh lock/config parity only after routing files are stable.

## 7. Regression Evidence

Focused route probes should be added or extended before claiming this pack is cleaned:

| Probe | Expected |
|---|---|
| `chem_rdkit_fingerprint` | `science-chem-drug / rdkit` |
| `chem_chembl_ic50` | `science-chem-drug / chembl-database` |
| `chem_drugbank_interaction` | `science-chem-drug / drugbank-database` |
| `chem_pubchem_cid` | `science-chem-drug / pubchem-database` |
| `chem_zinc_library` | `science-chem-drug / zinc-database` |
| `chem_brenda_kinetics` | `science-chem-drug / brenda-database` |
| `chem_hmdb_msms` | `science-chem-drug / hmdb-database` |
| `chem_medchem_sar` | `science-chem-drug / medchem` |
| `chem_diffdock_pose` | `science-chem-drug / diffdock` |
| `chem_deepchem_admet_model` | `science-chem-drug / deepchem` |
| `chem_pytdc_admet_benchmark` | `science-chem-drug / pytdc` |
| `chem_datamol_standardize_routes_rdkit` | `science-chem-drug / rdkit` |
| `chem_molfeat_embedding_routes_deepchem` | `science-chem-drug / deepchem` |
| `bio_bulk_rnaseq_not_chem` | not `science-chem-drug` |
| `pubmed_bibtex_not_chem` | not `science-chem-drug` |
| `clinical_trials_not_chem` | not `science-chem-drug` |

Expected verification sequence after implementation:

```powershell
python -m pytest tests/runtime_neutral/test_science_chem_drug_pack_consolidation.py -q
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

## 8. Completion Criteria

The implementation is complete only when:

- `science-chem-drug` has an explicit 11-skill selectable route-authority list.
- `stage_assistant_candidates` is explicitly empty.
- `datamol` and `molfeat` cannot win ordinary route prompts.
- RDKit, ChEMBL, DrugBank, PubChem, ZINC, BRENDA, HMDB, MedChem, DiffDock, DeepChem, and PyTDC each have at least one protected route probe.
- False-positive prompts for bulk RNA-seq, PubMed/BibTeX, and clinical trials do not route to `science-chem-drug`.
- Physical deletion is not claimed unless a later review migrates useful content and explicitly removes directories.
