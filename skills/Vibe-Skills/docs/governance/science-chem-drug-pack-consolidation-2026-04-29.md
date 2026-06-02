# Science Chem Drug Pack Consolidation

Date: 2026-04-29

Superseded by the high-prune second pass on 2026-04-30:
`docs/governance/science-chem-drug-high-prune-2026-04-30.md`.

## Summary

`science-chem-drug` was consolidated into a direct chem/drug specialist routing pack.

This cleanup keeps the six-stage Vibe runtime unchanged and preserves the binary usage model:

```text
skill_routing.selected -> skill_usage.used / unused
```

No `primary/secondary`, `consult`, `advisory`, or stage-assistant execution semantics were added.

## Before And After

| Field | Before | After |
| --- | ---: | ---: |
| `skill_candidates` | 13 | 11 |
| `route_authority_candidates` | 0 | 11 |
| `stage_assistant_candidates` | 0 | 0 |
| physical directory deletion | 0 | 0 |

## Kept Route Authorities

| Skill | Boundary |
| --- | --- |
| `rdkit` | SMILES/SDF parsing, descriptors, Morgan fingerprints, similarity, substructure, reactions, molecular drawing, and datamol-style molecule standardization prompts |
| `medchem` | Drug-likeness, PAINS, Lipinski, structural alerts, SAR, hit-to-lead and lead optimization |
| `diffdock` | Protein-ligand docking pose prediction from PDB plus SMILES |
| `deepchem` | Molecular property prediction, ADMET/toxicity model building, MoleculeNet, GNN, ChemBERTa/MolFeat-style embedding workflows |
| `pytdc` | Therapeutics Data Commons datasets, ADMET benchmarks, scaffold splits, therapeutic ML benchmark access |
| `chembl-database` | Target-ligand bioactivity, IC50/Ki/Kd, assay retrieval, SAR activity tables |
| `drugbank-database` | Approved drug metadata, drug-drug interactions, pharmacology, targets, pathways |
| `pubchem-database` | PubChem CID, SMILES/InChI, formula, compound properties |
| `zinc-database` | ZINC IDs, purchasable compound libraries, virtual-screening source libraries |
| `brenda-database` | BRENDA EC numbers, Km/kcat/Vmax, enzyme kinetics, substrate specificity |
| `hmdb-database` | HMDB IDs, metabolites, MS/MS and NMR reference spectra, metabolomics lookup |

`route_authority_candidates` mirrors `skill_candidates` for compatibility and documentation. The actual simplification is enforced by shrinking `skill_candidates`.

## Moved Out Of Ordinary Routing

| Skill | Reason |
| --- | --- |
| `datamol` | Useful RDKit wrapper, but it does not own a distinct user route; ordinary datamol standardization prompts route to `rdkit` |
| `molfeat` | Useful featurization library, but broad user routes should choose `deepchem` for molecular ML embeddings or `rdkit` for pure fingerprints/descriptors |

Moved-out skills remain on disk. They were not physically deleted because useful references and examples need migration review before deletion.

## Protected Route Boundaries

| Prompt | Expected route |
| --- | --- |
| `用RDKit解析SMILES并计算Morgan fingerprint` | `science-chem-drug / rdkit` |
| `在 ChEMBL 查询某靶点的 IC50 / Ki / Kd 活性数据` | `science-chem-drug / chembl-database` |
| `查询 DrugBank 药物相互作用、药物靶点和药理信息` | `science-chem-drug / drugbank-database` |
| `查询 PubChem CID、SMILES、InChI 和化合物物性` | `science-chem-drug / pubchem-database` |
| `从 ZINC 下载可购买小分子库用于 virtual screening` | `science-chem-drug / zinc-database` |
| `在 BRENDA 查询 EC number 的 Km、kcat 和酶动力学参数` | `science-chem-drug / brenda-database` |
| `在 HMDB 里按 MS/MS 谱和代谢物名称做 metabolite identification` | `science-chem-drug / hmdb-database` |
| `做药物化学 SAR 分析、PAINS 过滤和先导化合物优化建议` | `science-chem-drug / medchem` |
| `用 DiffDock 做 docking pose prediction：给定 PDB + SMILES 输出结合构象` | `science-chem-drug / diffdock` |
| `用 DeepChem 训练分子属性预测模型，做 scaffold split、ADMET 毒性预测和 GNN` | `science-chem-drug / deepchem` |
| `用 Therapeutics Data Commons / PyTDC 加载 ADMET benchmark 数据集` | `science-chem-drug / pytdc` |
| `用 datamol 批量标准化 SMILES 并生成分子指纹` | `science-chem-drug / rdkit` |
| `用 MolFeat 生成 ChemBERTa 分子 embedding 和 ECFP 特征用于分子机器学习` | `science-chem-drug / deepchem` |
| `bulk RNA-seq 差异表达 / GO KEGG 富集` | not `science-chem-drug` |
| `PubMed 检索 / BibTeX / 文献综述` | not `science-chem-drug` |
| `ClinicalTrials.gov / NCT / FDA label` | not `science-chem-drug` |

## Verification

Focused:

```powershell
python -m pytest tests/runtime_neutral/test_science_chem_drug_pack_consolidation.py -q
```

Broader probes and gates:

```powershell
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```
