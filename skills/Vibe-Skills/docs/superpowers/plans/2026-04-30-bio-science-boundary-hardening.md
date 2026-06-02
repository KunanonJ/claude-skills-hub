# Bio-Science Boundary Hardening Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden `bio-science` routing boundaries while preserving the public six-stage runtime and the simplified `candidate skill -> selected skill -> used / unused` model.

**Architecture:** Keep all 26 current `bio-science` skills as direct route owners, keep `stage_assistant_candidates` empty, and fix routing precision through focused tests, narrow trigger additions, negative boundaries, and one small Chinese negation parser correction. This plan does not add helper experts, advisory routing, primary/secondary skill states, consultation buckets, or physical skill deletion.

**Tech Stack:** Python `unittest`/`pytest`, Vibe router contract runtime, JSON routing configs, PowerShell verification gates.

---

## Current Evidence

The current `main` branch starts at commit `49ae5fda docs: design bio science boundary hardening`.

Current state:

```text
bio-science skill_candidates: 26
bio-science route_authority_candidates: 26
bio-science stage_assistant_candidates: 0
```

Current live probes expose three concrete boundary problems:

```text
Prompt: 对 BED genomic intervals 做 embeddings 和 similarity search。
Current: ai-llm / similarity-search-patterns
Target: bio-science / geniml

Prompt: 用 random forest 对普通临床表格做 machine learning，不是 genomic ML。
Current: bio-science / geniml
Target: not bio-science / geniml

Prompt: 做 single-cell RNA-seq clustering 和 UMAP，不是 flow cytometry，也不是 FCS 文件解析。
Current: bio-science / flowio
Target: bio-science / scanpy
```

The third failure is not only a `flowio` config problem. The runtime negation scope currently recognizes `不用` but not `不是`, so negated Chinese technical terms still count as positive route evidence.

## File Structure

Create:

- `tests/runtime_neutral/test_bio_science_boundary_hardening.py`
  Focused routing regression tests for the bio-science boundary pass.

- `docs/governance/bio-science-boundary-hardening-2026-04-30.md`
  Human-readable governance record for counts, kept route owners, boundary decisions, probes, and remaining caveats.

Modify:

- `packages/runtime-core/src/vgo_runtime/router_contract_support.py`
  Add Chinese negation operators `不是`, `并非`, `不属于`, `不涉及`, and `不做` to the existing negation-scope regex.

- `config/pack-manifest.json`
  Keep the 26 candidates and empty `stage_assistant_candidates`; add narrow `bio-science` pack triggers for genomic intervals and genomic ML.

- `config/skill-keyword-index.json`
  Add narrow keywords for `geniml` and `scanpy`; do not add broad `bio`, `biology`, or generic `analysis`.

- `config/skill-routing-rules.json`
  Add `geniml` positive/negative boundaries, `scanpy` positive triggers, and cross-pack negatives for `similarity-search-patterns` and `rdkit` where they currently steal genomic interval prompts.

- `bundled/skills/vibe/config/pack-manifest.json`
  Mirror the root config after root config edits.

- `bundled/skills/vibe/config/skill-keyword-index.json`
  Mirror the root config after root config edits.

- `bundled/skills/vibe/config/skill-routing-rules.json`
  Mirror the root config after root config edits.

- `config/skills-lock.json`
  Refresh after all config, code, test, and docs changes are stable.

Do not modify:

- `config/specialist-consultation-policy.json`
- `bio-science.stage_assistant_candidates`
- physical directories under `bundled/skills/<skill-id>/`

---

### Task 1: Add Failing Boundary Tests

**Files:**
- Create: `tests/runtime_neutral/test_bio_science_boundary_hardening.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/runtime_neutral/test_bio_science_boundary_hardening.py` with this exact initial content:

```python
from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


def route(prompt: str, task_type: str = "research", grade: str = "M") -> dict[str, object]:
    return route_prompt(
        prompt=prompt,
        grade=grade,
        task_type=task_type,
        repo_root=REPO_ROOT,
    )


def selected(result: dict[str, object]) -> tuple[str, str]:
    selected_row = result.get("selected")
    assert isinstance(selected_row, dict), result
    return str(selected_row.get("pack_id") or ""), str(selected_row.get("skill") or "")


def ranked_summary(result: dict[str, object]) -> list[tuple[str, str, float, str]]:
    ranked = result.get("ranked")
    assert isinstance(ranked, list), result
    rows: list[tuple[str, str, float, str]] = []
    for row in ranked[:8]:
        assert isinstance(row, dict), row
        rows.append(
            (
                str(row.get("pack_id") or ""),
                str(row.get("selected_candidate") or ""),
                float(row.get("score") or 0.0),
                str(row.get("candidate_selection_reason") or ""),
            )
        )
    return rows


class BioScienceBoundaryHardeningTests(unittest.TestCase):
    def assert_selected(
        self,
        prompt: str,
        expected_pack: str,
        expected_skill: str,
        *,
        task_type: str = "research",
        grade: str = "M",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertEqual((expected_pack, expected_skill), selected(result), ranked_summary(result))

    def assert_not_selected(
        self,
        prompt: str,
        blocked_pack: str,
        blocked_skill: str,
        *,
        task_type: str = "research",
        grade: str = "M",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertNotEqual((blocked_pack, blocked_skill), selected(result), ranked_summary(result))

    def test_geniml_owns_bed_genomic_interval_embeddings(self) -> None:
        self.assert_selected(
            "对 BED genomic intervals 做 embeddings 和 similarity search。",
            "bio-science",
            "geniml",
        )

    def test_negated_genomic_ml_does_not_route_to_geniml(self) -> None:
        self.assert_not_selected(
            "用 random forest 对普通临床表格做 machine learning，不是 genomic ML。",
            "bio-science",
            "geniml",
        )

    def test_chinese_bu_shi_negation_keeps_flowio_from_stealing_scanpy(self) -> None:
        self.assert_selected(
            "做 single-cell RNA-seq clustering 和 UMAP，不是 flow cytometry，也不是 FCS 文件解析。",
            "bio-science",
            "scanpy",
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new tests and verify the current failures**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_boundary_hardening.py -q
```

Expected: FAIL with these three mismatches:

```text
test_geniml_owns_bed_genomic_interval_embeddings
expected ('bio-science', 'geniml')
current ('ai-llm', 'similarity-search-patterns')

test_negated_genomic_ml_does_not_route_to_geniml
blocked ('bio-science', 'geniml') is currently selected

test_chinese_bu_shi_negation_keeps_flowio_from_stealing_scanpy
expected ('bio-science', 'scanpy')
current ('bio-science', 'flowio')
```

- [ ] **Step 3: Commit the failing test**

Run:

```powershell
git add tests/runtime_neutral/test_bio_science_boundary_hardening.py
git commit -m "test: capture bio science boundary failures"
```

---

### Task 2: Fix Chinese Negation Scope

**Files:**
- Modify: `packages/runtime-core/src/vgo_runtime/router_contract_support.py`
- Test: `tests/runtime_neutral/test_bio_science_boundary_hardening.py`

- [ ] **Step 1: Update `NEGATION_SCOPE_PATTERN`**

In `packages/runtime-core/src/vgo_runtime/router_contract_support.py`, replace the current `NEGATION_SCOPE_PATTERN` block with:

```python
NEGATION_SCOPE_PATTERN = re.compile(
    r"(不是|并非|不属于|不涉及|不做|不使用|不指定|不需要|不要|不用|无需|避免|排除|without\b|no\b|not\s+using\b|do\s+not\s+use\b|don't\s+use\b|not\b)",
    re.IGNORECASE,
)
```

This keeps the existing English and Chinese negation behavior and adds the Chinese forms observed in the failing probe.

- [ ] **Step 2: Run the focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_boundary_hardening.py -q
```

Expected: the flowio negation test and the negated genomic ML test now pass because `不是` is recognized. The geniml BED interval test still fails until Task 3 adds genomic interval routing signals.

- [ ] **Step 3: Commit the negation fix**

Run:

```powershell
git add packages/runtime-core/src/vgo_runtime/router_contract_support.py tests/runtime_neutral/test_bio_science_boundary_hardening.py
git commit -m "fix: recognize chinese negation in route keywords"
```

---

### Task 3: Harden Genomic Interval And Generic ML Boundaries

**Files:**
- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`
- Modify: `bundled/skills/vibe/config/pack-manifest.json`
- Modify: `bundled/skills/vibe/config/skill-keyword-index.json`
- Modify: `bundled/skills/vibe/config/skill-routing-rules.json`
- Test: `tests/runtime_neutral/test_bio_science_boundary_hardening.py`

- [ ] **Step 1: Add narrow `bio-science` pack triggers**

In the `bio-science.trigger_keywords` array in `config/pack-manifest.json`, add these exact strings near the existing genomics/protein/RNA terms:

```json
"genomic interval",
"genomic intervals",
"BED genomic intervals",
"regulatory region",
"genomic ML",
"genome embedding",
"基因组区间",
"基因组嵌入"
```

Keep `skill_candidates`, `route_authority_candidates`, `stage_assistant_candidates`, and `defaults_by_task` unchanged.

- [ ] **Step 2: Strengthen `geniml` keyword-index triggers**

In `config/skill-keyword-index.json`, replace the `geniml.keywords` array with:

```json
[
  "geniml",
  "genomic ml",
  "genomic machine learning",
  "genome embedding",
  "genome embeddings",
  "genomic interval",
  "genomic intervals",
  "BED genomic intervals",
  "regulatory region embedding",
  "regulatory region similarity",
  "基因组机器学习",
  "基因组嵌入",
  "基因组区间"
]
```

- [ ] **Step 3: Strengthen `geniml` routing rules**

In `config/skill-routing-rules.json`, replace the `geniml.positive_keywords` array with:

```json
[
  "geniml",
  "genomic ML",
  "genomic machine learning",
  "genome embedding",
  "genome embeddings",
  "genomic interval",
  "genomic intervals",
  "BED genomic intervals",
  "regulatory region embedding",
  "regulatory region similarity",
  "基因组机器学习",
  "基因组嵌入",
  "基因组区间"
]
```

In the same `geniml` rule, replace the `negative_keywords` array with:

```json
[
  "scanpy",
  "single-cell",
  "single cell",
  "scRNA-seq",
  "DESeq2",
  "bulk RNA-seq",
  "BAM",
  "VCF",
  "pysam",
  "ESM",
  "protein embedding",
  "COBRApy",
  "FBA",
  "flow cytometry",
  "FCS",
  "RDKit",
  "SMILES",
  "DICOM",
  "patent",
  "ordinary clinical table",
  "ordinary tabular",
  "generic tabular",
  "random forest",
  "scikit-learn",
  "not genomic ML",
  "不是 genomic ML",
  "不是基因组机器学习",
  "不是 genome embedding",
  "不是基因组嵌入"
]
```

- [ ] **Step 4: Add cross-pack negatives for generic similarity and chemistry**

In `config/skill-routing-rules.json`, extend `similarity-search-patterns.negative_keywords` to:

```json
[
  "release notes",
  "genomic interval",
  "genomic intervals",
  "BED genomic intervals",
  "regulatory region",
  "geniml",
  "基因组区间"
]
```

In `config/skill-routing-rules.json`, extend `rdkit.negative_keywords` with these exact strings while preserving the existing negatives:

```json
"genomic interval",
"genomic intervals",
"BED genomic intervals",
"regulatory region",
"geniml",
"基因组区间"
```

- [ ] **Step 5: Strengthen `scanpy` for explicit single-cell RNA-seq analysis**

In `config/skill-keyword-index.json`, extend `scanpy.keywords` with:

```json
"single-cell RNA-seq",
"single cell RNA-seq",
"scRNA-seq",
"UMAP",
"QC",
"单细胞 RNA-seq",
"单细胞RNA-seq"
```

In `config/skill-routing-rules.json`, extend `scanpy.positive_keywords` with:

```json
"single-cell RNA-seq",
"single cell RNA-seq",
"scRNA-seq",
"UMAP",
"QC",
"单细胞 RNA-seq",
"单细胞RNA-seq"
```

- [ ] **Step 6: Mirror root config into bundled Vibe config**

Run these exact commands:

```powershell
Copy-Item -LiteralPath config\pack-manifest.json -Destination bundled\skills\vibe\config\pack-manifest.json -Force
Copy-Item -LiteralPath config\skill-keyword-index.json -Destination bundled\skills\vibe\config\skill-keyword-index.json -Force
Copy-Item -LiteralPath config\skill-routing-rules.json -Destination bundled\skills\vibe\config\skill-routing-rules.json -Force
```

- [ ] **Step 7: Run the focused boundary tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_boundary_hardening.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 8: Commit the boundary config changes**

Run:

```powershell
git add config/pack-manifest.json config/skill-keyword-index.json config/skill-routing-rules.json bundled/skills/vibe/config/pack-manifest.json bundled/skills/vibe/config/skill-keyword-index.json bundled/skills/vibe/config/skill-routing-rules.json tests/runtime_neutral/test_bio_science_boundary_hardening.py
git commit -m "fix: harden bio science genomic interval routing"
```

---

### Task 4: Expand The Bio-Science Boundary Regression Matrix

**Files:**
- Modify: `tests/runtime_neutral/test_bio_science_boundary_hardening.py`

- [ ] **Step 1: Add positive ownership tests**

Append these tests inside `BioScienceBoundaryHardeningTests`:

```python
    def test_biopython_owns_sequence_conversion(self) -> None:
        self.assert_selected(
            "用 Biopython SeqIO 把 FASTA 转 GenBank，并通过 Entrez 拉取序列记录",
            "bio-science",
            "biopython",
        )

    def test_anndata_owns_container_editing(self) -> None:
        self.assert_selected(
            "编辑 AnnData h5ad 文件的 obs/var 元数据、layers 和 backed mode",
            "bio-science",
            "anndata",
        )

    def test_scvi_tools_owns_latent_single_cell_models(self) -> None:
        self.assert_selected(
            "用 scVI 训练 single-cell latent model 做 batch correction 和 scANVI 注释",
            "bio-science",
            "scvi-tools",
        )

    def test_cellxgene_owns_census_queries(self) -> None:
        self.assert_selected(
            "查询 CELLxGENE Census 里 human lung epithelial cells 的 tissue disease metadata",
            "bio-science",
            "cellxgene-census",
        )

    def test_pydeseq2_owns_bulk_rnaseq_de(self) -> None:
        self.assert_selected(
            "用 PyDESeq2 对 bulk RNA-seq count matrix 做 Wald test、FDR 和 volcano plot",
            "bio-science",
            "pydeseq2",
        )

    def test_pysam_owns_alignment_variant_files(self) -> None:
        self.assert_selected(
            "用 pysam 读取 BAM/CRAM/VCF 做 pileup、coverage 和 region extraction",
            "bio-science",
            "pysam",
        )

    def test_deeptools_owns_genomics_signal_tracks(self) -> None:
        self.assert_selected(
            "用 deepTools bamCoverage 把 BAM 转 bigWig，并用 computeMatrix plotHeatmap 围绕 TSS 作图",
            "bio-science",
            "deeptools",
        )

    def test_bioservices_owns_explicit_multi_service_aggregation(self) -> None:
        self.assert_selected(
            "用 BioServices 同时查询 UniProt、KEGG、Reactome 并做跨数据库 ID mapping",
            "bio-science",
            "bioservices",
        )

    def test_gget_owns_quick_lookup(self) -> None:
        self.assert_selected(
            "用 gget 做 quick BLAST、gene symbol 和 transcript lookup",
            "bio-science",
            "gget",
        )

    def test_cobrapy_owns_flux_balance_analysis(self) -> None:
        self.assert_selected(
            "用 COBRApy 构建 metabolic model 并做 FBA flux balance analysis",
            "bio-science",
            "cobrapy",
        )

    def test_esm_owns_protein_embeddings(self) -> None:
        self.assert_selected(
            "用 ESM protein language model 生成蛋白 embedding，不做 Biopython 序列解析",
            "bio-science",
            "esm",
        )

    def test_flowio_owns_real_fcs_flow_cytometry(self) -> None:
        self.assert_selected(
            "读取 FCS flow cytometry 文件，提取 channel matrix 和 compensation",
            "bio-science",
            "flowio",
        )
```

- [ ] **Step 2: Add intra-pack false-positive tests**

Append these tests inside `BioScienceBoundaryHardeningTests`:

```python
    def test_scanpy_loses_to_anndata_for_container_only_work(self) -> None:
        self.assert_selected(
            "只需要整理 h5ad AnnData 的 obs、var、layers、raw 和 backed mode，不做聚类分析",
            "bio-science",
            "anndata",
        )

    def test_scanpy_loses_to_cellxgene_for_census_query(self) -> None:
        self.assert_selected(
            "从 CELLxGENE Census 下载细胞图谱，然后在后续可能用 scanpy 分析",
            "bio-science",
            "cellxgene-census",
        )

    def test_biopython_loses_to_pysam_for_bam_vcf_files(self) -> None:
        self.assert_selected(
            "解析 BAM/VCF 文件，计算 coverage 和 pileup，不做序列格式转换",
            "bio-science",
            "pysam",
        )

    def test_bioservices_loses_to_kegg_for_explicit_kegg_rest(self) -> None:
        self.assert_selected(
            "用 KEGG REST 做 pathway mapping、ID conversion 和 metabolic pathway 查询，不使用 BioServices",
            "bio-science",
            "kegg-database",
        )

    def test_bioservices_loses_to_reactome_for_explicit_reactome(self) -> None:
        self.assert_selected(
            "用 Reactome API 做 pathway enrichment 和 gene-pathway mapping，不使用 BioServices",
            "bio-science",
            "reactome-database",
        )

    def test_gget_loses_to_opentargets_for_target_evidence(self) -> None:
        self.assert_selected(
            "用 Open Targets 做 target-disease association、tractability 和 known drugs evidence，不使用 gget",
            "bio-science",
            "opentargets-database",
        )
```

- [ ] **Step 3: Add cross-pack boundary tests**

Append these tests inside `BioScienceBoundaryHardeningTests`:

```python
    def test_rdkit_smiles_stays_in_chem_drug_pack(self) -> None:
        self.assert_selected(
            "用 RDKit 处理 SMILES、Morgan fingerprints 和分子描述符",
            "science-chem-drug",
            "rdkit",
        )

    def test_pubmed_bibtex_stays_in_literature_pack(self) -> None:
        self.assert_selected(
            "做 PubMed 文献综述，导出 BibTeX 和引用格式",
            "science-literature-citations",
            "citation-management",
        )

    def test_clinicaltrials_stays_in_clinical_regulatory_pack(self) -> None:
        self.assert_selected(
            "查询 ClinicalTrials.gov NCT 试验入排标准和 endpoint",
            "science-clinical-regulatory",
            "clinicaltrials-database",
        )

    def test_dicom_tags_stay_in_medical_imaging_pack(self) -> None:
        self.assert_selected(
            "用 pydicom 读取 DICOM metadata 和影像 tag",
            "science-medical-imaging",
            "pydicom",
        )

    def test_generic_scikit_learn_stays_in_data_ml_pack(self) -> None:
        self.assert_selected(
            "用 scikit-learn random forest 对普通 tabular data 做监督学习和交叉验证",
            "data-ml",
            "scikit-learn",
        )

    def test_result_figures_stay_in_scientific_visualization_pack(self) -> None:
        self.assert_selected(
            "把机器学习模型评估结果做成投稿级结果图，600dpi，多面板，色盲友好",
            "science-figures-visualization",
            "scientific-visualization",
        )

    def test_latex_pdf_stays_in_submission_pipeline(self) -> None:
        self.assert_selected(
            "用 LaTeX 写成论文 PDF，latexmk 编译，生成可投稿 PDF",
            "scholarly-publishing-workflow",
            "latex-submission-pipeline",
        )
```

- [ ] **Step 4: Run the expanded matrix**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_boundary_hardening.py -q
```

Expected:

```text
28 passed
```

- [ ] **Step 5: Commit the expanded regression matrix**

Run:

```powershell
git add tests/runtime_neutral/test_bio_science_boundary_hardening.py
git commit -m "test: expand bio science boundary matrix"
```

---

### Task 5: Add Governance Record

**Files:**
- Create: `docs/governance/bio-science-boundary-hardening-2026-04-30.md`

- [ ] **Step 1: Write the governance note**

Create `docs/governance/bio-science-boundary-hardening-2026-04-30.md` with this exact content:

````markdown
# Bio-Science Boundary Hardening - 2026-04-30

## Scope

This pass hardens the `bio-science` routing boundary. It does not change the public six-stage Vibe runtime and does not introduce helper experts, advisory routing, consultation routing, primary/secondary skill states, or stage assistants.

The live skill-use model remains:

```text
candidate skill -> selected skill -> used / unused
```

## Counts

| Metric | Before | After |
| --- | ---: | ---: |
| `skill_candidates` | 26 | 26 |
| `route_authority_candidates` | 26 | 26 |
| `stage_assistant_candidates` | 0 | 0 |
| physically deleted skill directories | 0 | 0 |

## Retained Direct Owners

All current `bio-science` candidates remain direct route owners:

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

## Boundary Decisions

| Problem family | Direct owners |
| --- | --- |
| Sequence and general bio Python | `biopython` |
| Single-cell analysis and containers | `scanpy`, `anndata`, `scvi-tools`, `cellxgene-census` |
| Bulk RNA-seq and NGS files | `pydeseq2`, `pysam`, `deeptools` |
| Gene, variant, and target evidence | `clinvar-database`, `cosmic-database`, `ensembl-database`, `gene-database`, `gget`, `gwas-database`, `opentargets-database` |
| Pathway, interaction, and systems biology | `kegg-database`, `reactome-database`, `string-database`, `cobrapy`, `arboreto` |
| Protein structure and protein ML | `alphafold-database`, `pdb-database`, `esm` |
| Specialized bio data and genomic ML | `flowio`, `geniml`, `bioservices` |

## Changes

- Added Chinese `不是`-family negation handling so negated biomedical terms do not count as positive routing evidence.
- Added narrow `geniml` triggers for BED/genomic interval embeddings and regulatory region similarity.
- Added `geniml` negatives for ordinary tabular ML, scikit-learn/random forest prompts, and explicit non-genomic ML prompts.
- Added cross-pack negatives so generic similarity search and RDKit do not capture BED/genomic interval embedding tasks.
- Added Scanpy single-cell RNA-seq analysis triggers so explicit scRNA-seq clustering remains with `scanpy` even when flow cytometry/FCS terms are negated.

## Protected Probes

Positive bio-science ownership:

- `biopython`: FASTA/GenBank/SeqIO/Entrez conversion.
- `scanpy`: single-cell RNA-seq QC, clustering, UMAP, and marker genes.
- `anndata`: h5ad container metadata and backed mode.
- `scvi-tools`: scVI/scANVI latent modeling and batch correction.
- `cellxgene-census`: CELLxGENE Census cell/tissue/disease queries.
- `pydeseq2`: bulk RNA-seq differential expression.
- `pysam`: BAM/CRAM/VCF pileup and coverage.
- `deeptools`: BAM-to-bigWig, computeMatrix, and plotHeatmap.
- `bioservices`: explicit BioServices multi-service aggregation.
- `gget`: explicit gget quick lookup.
- `geniml`: BED/genomic interval embeddings and regulatory region similarity.
- `flowio`: real FCS flow cytometry parsing.

False-positive boundaries:

- `geniml` must not own ordinary clinical-table random forest prompts that say the task is not genomic ML.
- `flowio` must not own single-cell RNA-seq prompts that only mention flow cytometry/FCS under `不是` negation.
- `scanpy` must lose to AnnData, scVI, and CELLxGENE when those explicit owner signals appear.
- `biopython` must lose to pysam, ESM, and COBRApy when those explicit owner signals appear.
- `bioservices` must lose to KEGG and Reactome when the prompt names those deeper database workflows.
- `gget` must lose to Open Targets when the prompt names target-disease evidence.
- RDKit, PubMed/citations, ClinicalTrials.gov, DICOM, generic scikit-learn, scientific visualization, and LaTeX PDF build remain in their neighboring packs.

## Remaining Caveats

- This pass does not shrink the 26-skill candidate count.
- This pass does not claim that a selected skill was materially used in a real task. Material use still requires task artifacts or execution evidence.
- Physical deletion remains deferred because every retained directory already had a distinct route owner role or asset-bearing content.
````

- [ ] **Step 2: Run Markdown grep checks**

Run:

```powershell
rg -n "helper expert|stage assistant|primary/secondary|consultation|advisory" docs/governance/bio-science-boundary-hardening-2026-04-30.md
```

Expected: hits only in the sentence that says these states were not introduced.

- [ ] **Step 3: Commit the governance note**

Run:

```powershell
git add docs/governance/bio-science-boundary-hardening-2026-04-30.md
git commit -m "docs: record bio science boundary hardening"
```

---

### Task 6: Refresh Lock And Run Verification Gates

**Files:**
- Modify: `config/skills-lock.json`

- [ ] **Step 1: Refresh `skills-lock.json`**

Run:

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected output includes:

```text
skills-lock generated:
```

- [ ] **Step 2: Run focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_boundary_hardening.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_direct_owner_routing.py -q
```

Expected:

```text
passed
```

- [ ] **Step 3: Run cross-pack focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_chem_drug_pack_consolidation.py tests/runtime_neutral/test_science_literature_peer_review_consolidation.py tests/runtime_neutral/test_science_clinical_regulatory_pack_consolidation.py tests/runtime_neutral/test_ml_skills_pruning_audit.py tests/runtime_neutral/test_scientific_visualization_latex_routing.py -q
```

Expected:

```text
passed
```

- [ ] **Step 4: Run broad routing and packaging gates**

Run:

```powershell
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
git diff --check
```

Expected:

```text
vibe-pack-routing-smoke.ps1: 0 failed
vibe-offline-skills-gate.ps1: PASS
vibe-config-parity-gate.ps1: PASS
vibe-version-packaging-gate.ps1: PASS
git diff --check: no output
```

- [ ] **Step 5: Commit refreshed lock**

Run:

```powershell
git add config/skills-lock.json
git commit -m "chore: refresh skills lock after bio science hardening"
```

---

### Task 7: Final Sanity Check

**Files:**
- Read-only check over repository state.

- [ ] **Step 1: Verify no stage assistants were reintroduced**

Run:

```powershell
@'
import json
from pathlib import Path
manifest = json.loads(Path("config/pack-manifest.json").read_text(encoding="utf-8-sig"))
bio = next(pack for pack in manifest["packs"] if pack["id"] == "bio-science")
print("skill_candidates", len(bio["skill_candidates"]))
print("route_authority_candidates", len(bio["route_authority_candidates"]))
print("stage_assistant_candidates", bio["stage_assistant_candidates"])
'@ | python -
```

Expected:

```text
skill_candidates 26
route_authority_candidates 26
stage_assistant_candidates []
```

- [ ] **Step 2: Verify physical directories were not deleted**

Run:

```powershell
@'
from pathlib import Path
skills = [
    "alphafold-database", "anndata", "biopython", "bioservices",
    "cellxgene-census", "clinvar-database", "cosmic-database", "deeptools",
    "ensembl-database", "gene-database", "gget", "gwas-database",
    "kegg-database", "opentargets-database", "pdb-database", "pydeseq2",
    "pysam", "reactome-database", "scanpy", "scvi-tools", "arboreto",
    "cobrapy", "esm", "flowio", "geniml", "string-database",
]
root = Path("bundled/skills")
missing = [skill for skill in skills if not (root / skill / "SKILL.md").exists()]
print("missing", missing)
'@ | python -
```

Expected:

```text
missing []
```

- [ ] **Step 3: Review final diff**

Run:

```powershell
git status --short --branch
git log --oneline -8
```

Expected:

```text
## <branch>...
```

The only uncommitted files at this point should be intentional generated artifacts from parity/version gates. Either commit required generated config changes or remove non-required verification outputs before final merge.

---

## Completion Criteria

The implementation is complete when all of the following are true:

- `bio-science.skill_candidates` remains 26.
- `bio-science.route_authority_candidates` remains 26.
- `bio-science.stage_assistant_candidates` remains `[]`.
- No `bio-science` skill directory is physically deleted.
- The new boundary test file passes.
- Existing bio-science direct-owner and pack-audit tests pass.
- Cross-pack science/ML/visualization/LaTeX routing tests pass.
- Offline skills, config parity, version packaging, and routing smoke gates pass.
- The governance note clearly says selection is not the same thing as material use.
