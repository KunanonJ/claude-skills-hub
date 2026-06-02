# Bio-Science Problem-First Pack Consolidation Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-28

## 1. Goal

This design freezes the next routing cleanup wave for the `bio-science` pack.

The goal is to turn `bio-science` from a flat list of tool and database skills into a problem-first specialist surface where each retained expert has a clear user task, route role, adjacent-skill boundary, and regression probe.

The cleanup must make these facts explicit:

- Which `bio-science` skills can own a main user route.
- Which skills are useful only as stage assistants or evidence/database helpers.
- Which skills should stay available only for explicit/manual review until their value is proven.
- Which low-quality or duplicate skills may be deleted only after asset migration review.
- Which prompts prove the new route behavior.

## 2. Current State

Current `bio-science` in `config/pack-manifest.json` has:

| Metric | Current value |
|---|---:|
| `skill_candidates` | 26 |
| `route_authority_candidates` | 0 |
| `stage_assistant_candidates` | 0 |

The current candidate list is:

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

Current defaults are:

```json
{
  "planning": "biopython",
  "coding": "biopython",
  "research": "scanpy"
}
```

The current problem is not only skill count. The pack lacks explicit role split:

- Tool-like workflow skills and database lookup skills compete in the same pool.
- Many candidate directories have references, scripts, or assets, so first-pass physical deletion is unsafe.
- Several skills are present in `skill_candidates` but are not connected in both `skill-keyword-index.json` and `skill-routing-rules.json`.
- `biopython` and `scanpy` behave like broad defaults, but the intended boundaries against `pydeseq2`, `pysam`, `gget`, `esm`, and `cobrapy` are not explicit enough.

## 3. Scope

This wave directly governs only the `bio-science` pack.

In scope:

```text
config/pack-manifest.json
config/skill-keyword-index.json
config/skill-routing-rules.json
config/skills-lock.json
bundled/skills/<bio-science-related-skill>/SKILL.md
packages/verification-core/src/vgo_verify/*
scripts/verify/*
tests/runtime_neutral/*
docs/governance/*
outputs/skills-audit/*
```

Out of scope except for negative-boundary protection:

- `science-chem-drug`
- `science-literature-citations`
- `scholarly-publishing-workflow`
- `science-lab-automation`
- `science-medical-imaging`
- `data-ml`

This wave does not rewrite the router and does not physically delete asset-heavy skill directories as a first step.

## 4. Design Choice

Use a problem-map plus route-role split.

Rejected alternatives:

| Alternative | Why not |
|---|---|
| Conservative role split only | It would add `route_authority_candidates` and `stage_assistant_candidates` but leave low-quality and unconnected skills unexplained. |
| Hard deletion first | Most `bio-science` directories have references, scripts, or assets. Deleting before migration review risks losing useful material. |

Chosen approach:

1. Build a machine-readable `bio-science` problem map.
2. Split candidates into route authorities, stage assistants, explicit/manual review, and merge/delete-after-migration candidates.
3. Tighten keyword and routing boundaries for the retained route authorities.
4. Add route regression probes for positive ownership and false-positive protection.
5. Write a governance note with before/after counts and remaining deletion caveats.

## 5. Target Role Model

The pack should use five role layers.

| Role layer | Meaning | Initial members |
|---|---|---|
| Main problem experts | Can independently own a user route | `scanpy`, `pydeseq2`, `pysam`, `biopython`, `gget`, `esm`, `cobrapy`, `flowio`, `arboreto`, `geniml` |
| Database/evidence assistants | Useful for annotation, evidence, or lookup inside a workflow; should not normally own broad prompts | `clinvar-database`, `cosmic-database`, `ensembl-database`, `gene-database`, `gwas-database`, `kegg-database`, `reactome-database`, `pdb-database`, `string-database`, `opentargets-database`, `alphafold-database`, `cellxgene-census` |
| Data structure / intermediate helpers | Useful inside specific workflows but not usually the final user goal | `anndata`, `scvi-tools`, `deeptools` |
| Cross-database aggregation assistant | Valuable, but must not override a more specific expert | `bioservices` |
| Quality-review backlog | Keep until content and assets are reviewed for migration or deletion | Unconnected or database-like candidates without protected route probes |

## 6. Main Expert Ownership

Route authority must be assigned by user problem, not by package name.

| User problem | Target owner |
|---|---|
| Single-cell RNA-seq clustering, annotation, marker genes, UMAP/t-SNE, h5ad/10X workflow | `scanpy` |
| Bulk RNA-seq differential expression, DESeq2-style statistics, volcano/MA plots | `pydeseq2` |
| BAM/SAM/CRAM/VCF parsing, pileup, coverage, variant-file handling | `pysam` |
| FASTA/GenBank/SeqIO, sequence conversion, NCBI Entrez Python workflow | `biopython` |
| Quick gene, transcript, BLAST, Ensembl, or symbol lookup | `gget` |
| Protein language model tasks and protein embeddings | `esm` |
| Metabolic network modeling, FBA, constraint-based metabolic models | `cobrapy` |
| FCS / flow cytometry file reading and channel matrix handling | `flowio` |
| Gene regulatory network inference, pySCENIC, transcription-factor network tasks | `arboreto` |
| Genomic ML and genome embedding tasks | `geniml` |

## 7. Target Pack Manifest Shape

Target `route_authority_candidates`:

```text
scanpy
pydeseq2
pysam
biopython
gget
esm
cobrapy
flowio
arboreto
geniml
```

Target `stage_assistant_candidates`:

```text
anndata
scvi-tools
deeptools
bioservices
alphafold-database
clinvar-database
cosmic-database
ensembl-database
gene-database
gwas-database
kegg-database
opentargets-database
pdb-database
reactome-database
string-database
cellxgene-census
```

`skill_candidates` should initially keep all 26 candidates. Physical deletion is a later migration step.

Target defaults:

```json
{
  "planning": "biopython",
  "coding": "biopython",
  "research": "scanpy"
}
```

`biopython` can remain the coding/planning default only if negative keywords stop it from absorbing single-cell, differential-expression, BAM/VCF, protein-embedding, and metabolic-model prompts.

## 8. Keyword and Rule Boundaries

### Positive ownership signals

| Owner | Add or strengthen signals |
|---|---|
| `scanpy` | `h5ad`, `10x`, `leiden`, `marker genes`, `single-cell clustering`, `单细胞聚类`, `细胞注释` |
| `pydeseq2` | `bulk RNA-seq`, `volcano plot`, `MA plot`, `padj`, `DESeq2`, `差异表达分析` |
| `pysam` | `BAM`, `SAM`, `CRAM`, `VCF`, `pileup`, `coverage`, `变异文件`, `覆盖度` |
| `biopython` | `SeqIO`, `FASTA`, `GenBank`, `Entrez`, `sequence conversion`, `序列格式转换` |
| `gget` | `gget`, `Ensembl lookup`, `gene symbol`, `quick BLAST`, `快速生信查询` |
| `esm` | `ESM`, `protein language model`, `protein embedding`, `蛋白嵌入` |
| `cobrapy` | `COBRApy`, `FBA`, `flux balance`, `metabolic model`, `通量平衡` |
| `flowio` | `FCS`, `flow cytometry`, `cytometry`, `流式细胞` |
| `arboreto` | `pySCENIC`, `GRN`, `gene regulatory network`, `转录因子网络` |
| `geniml` | `genomic ML`, `genome embedding`, `基因组机器学习` |

### Negative boundaries

Examples:

- `biopython` should not win prompts that clearly mention `scanpy`, `single-cell`, `DESeq2`, `BAM`, `VCF`, `ESM`, `FBA`, `COBRApy`, or `flow cytometry`.
- `scanpy` should not win prompts for bulk RNA-seq, BAM/VCF parsing, protein embeddings, metabolic modeling, RDKit/SMILES, PubMed citation export, DICOM, or manuscript submission.
- `gget` should not win full single-cell workflows or DESeq2 workflows just because they mention gene symbols.
- Database assistants should not become broad route authorities unless an explicit route probe proves an independent high-value user problem.

### Cross-pack false-positive protection

`bio-science` must not steal prompts that belong to:

| Prompt class | Expected pack |
|---|---|
| RDKit, SMILES, Morgan fingerprint, molecular descriptors | `science-chem-drug` |
| PubMed search, BibTeX export, citation management | `science-literature-citations` |
| Cover letter, rebuttal matrix, submission package | `scholarly-publishing-workflow` |
| General scikit-learn classification or cross-validation | `data-ml` |
| DICOM, pydicom, medical image tags | `science-medical-imaging` |

## 9. Problem Map Artifact

Implementation should add a focused audit artifact with one row per candidate.

Required fields:

```text
skill_id
problem_ids
primary_problem_id
current_role
target_role
target_owner
overlap_with
unique_assets
routing_change
delete_allowed_after_migration
risk_level
rationale
```

Allowed `target_role` values:

```text
keep
stage-assistant
explicit-only
merge-delete-after-migration
defer-specialist-review
manual-review
```

The key rule: if a skill cannot own a distinct user problem, it must not remain a route authority by default.

## 10. Verification Design

Verification has three layers.

| Layer | Purpose | Expected implementation |
|---|---|---|
| Problem-map audit | Prove all 26 candidates were classified and route authorities have distinct problems | New `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`; new or reused `packages/verification-core/src/vgo_verify/*bio_science*_audit.py` |
| Route regression | Prove real prompts hit the intended expert and false-positive prompts do not hit `bio-science` | Extend `scripts/verify/vibe-skill-index-routing-audit.ps1` and `scripts/verify/probe-scientific-packs.ps1` |
| Global regression | Prove the cleanup did not break existing pack behavior | Run pack regression, pack routing smoke, keyword precision audit, and relevant pytest suites |

Positive route probes:

| Prompt | Expected route |
|---|---|
| `做单细胞RNA-seq聚类与注释，使用scanpy` | `bio-science / scanpy` |
| `读取h5ad，做Leiden clustering和marker genes` | `bio-science / scanpy` |
| `进行bulk RNA-seq差异表达分析并画volcano plot` | `bio-science / pydeseq2` |
| `解析BAM和VCF文件并统计覆盖度` | `bio-science / pysam` |
| `用BioPython处理FASTA序列并转换GenBank格式` | `bio-science / biopython` |
| `用gget快速查询基因symbol和Ensembl ID` | `bio-science / gget` |
| `用ESM生成protein embeddings` | `bio-science / esm` |
| `用COBRApy做FBA代谢通量分析` | `bio-science / cobrapy` |
| `读取FCS流式细胞文件并提取通道矩阵` | `bio-science / flowio` |
| `用pySCENIC/arboreto推断基因调控网络` | `bio-science / arboreto` |

False-positive probes:

| Prompt | Expected route |
|---|---|
| `用RDKit解析SMILES并计算Morgan fingerprint` | `science-chem-drug / rdkit` |
| `在PubMed检索文献并导出BibTeX` | `science-literature-citations / pubmed-database` |
| `写论文投稿cover letter和rebuttal matrix` | `scholarly-publishing-workflow / submission-checklist` |
| `用scikit-learn训练分类模型并交叉验证` | `data-ml / scikit-learn` |
| `读取DICOM并提取tags` | `science-medical-imaging / pydicom` |

## 11. Governance Notes

Implementation should add:

```text
docs/governance/bio-science-problem-first-consolidation-2026-04-28.md
```

The governance note must include:

- before/after counts
- kept route authorities and their problem ownership
- stage assistants and why they are not primary owners
- explicit/manual-review candidates
- merge/delete-after-migration candidates and asset caveats
- exact probes or tests protecting the new behavior

The note must clearly distinguish routing/config cleanup from physical directory cleanup.

## 12. Deletion Boundary

This design does not approve immediate deletion of asset-heavy skill directories.

Deletion is allowed only after all conditions are true:

- The skill has no unique user problem after problem-map review.
- Useful references, scripts, examples, or assets have been migrated or intentionally rejected.
- No live route, profile, test, lockfile, or packaging surface depends on the directory.
- Offline skill, config parity, and route regression gates pass after removal.

First implementation should prefer:

```text
routing/config cleanup: yes
physical directory deletion: deferred unless proven safe
```

## 13. Success Criteria

This design is successfully implemented when:

- `bio-science` has explicit `route_authority_candidates` and `stage_assistant_candidates`.
- The 26 candidate skills are represented in a problem map.
- Every retained route authority has a primary user problem and at least one positive route probe.
- Database and evidence helpers no longer behave as broad main-route owners.
- `biopython` and `scanpy` no longer absorb prompts belonging to more specific `bio-science` experts.
- Cross-pack false-positive prompts stay with `science-chem-drug`, `science-literature-citations`, `scholarly-publishing-workflow`, `data-ml`, or `science-medical-imaging`.
- A governance note records before/after counts, role decisions, probes, and deletion caveats.

## 14. Recommended Implementation Order

1. Add the focused `bio-science` problem-map audit with a failing test first.
2. Classify all 26 skills into target roles and asset-risk categories.
3. Update `config/pack-manifest.json` for route authorities and stage assistants.
4. Tighten `config/skill-keyword-index.json` and `config/skill-routing-rules.json`.
5. Add positive and false-positive route probes.
6. Refresh `config/skills-lock.json` only after content and routing changes are stable.
7. Write the governance note.
8. Run focused tests, route probes, pack regression, smoke, keyword precision, and offline skills gates.
9. Commit implementation separately from this design.

## 15. Approved Decision

Proceed with the problem-map plus role-split approach for `bio-science`.

This is the next cleanup wave after the prior `data-ml`, `code-quality`, `docs-media`, and `orchestration-core` work. It should not broaden into other scientific packs until `bio-science` has a verified role model and governance note.
