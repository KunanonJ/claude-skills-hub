# Bio-Science Second-Pass Consolidation Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce `bio-science` from 26 direct route owners to 13 direct owners by merging database/API wrappers into `bio-database-evidence` and physically deleting the merged directories after migration review.

**Architecture:** Keep the six-stage runtime and binary skill-use model unchanged. The pack remains a direct candidate list: workflow owners stay as route authorities, and all biological database/evidence lookups route through one new owner. No stage assistants, helper experts, advisory mode, or primary/secondary states are introduced.

**Tech Stack:** Python `unittest`/`pytest`, PowerShell verification scripts, JSON config files, bundled Codex skills, Vibe-Skills router contract runtime.

---

## File Structure

- Create: `tests/runtime_neutral/test_bio_science_second_pass_consolidation.py`
  - Owns the new manifest shape, deleted-skill absence checks, `bio-database-evidence` routing checks, and cross-pack boundary checks.
- Modify: `tests/runtime_neutral/test_bio_science_boundary_hardening.py`
  - Updates old database-wrapper expectations to `bio-database-evidence` while preserving workflow boundary tests.
- Modify: `tests/runtime_neutral/test_bio_science_direct_owner_routing.py`
  - Replaces old per-database direct-owner tests with unified evidence-owner tests.
- Modify: `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`
  - Changes expected audit target from 26 direct owners to 13 direct owners plus 14 merge/delete rows.
- Create: `bundled/skills/bio-database-evidence/SKILL.md`
  - Defines the single biological database/evidence route owner.
- Create: `bundled/skills/bio-database-evidence/references/database-evidence-sources.md`
  - Migrates concise source-specific evidence guidance from deleted database/API wrappers.
- Delete after migration review:
  - `bundled/skills/alphafold-database`
  - `bundled/skills/bioservices`
  - `bundled/skills/cellxgene-census`
  - `bundled/skills/clinvar-database`
  - `bundled/skills/cosmic-database`
  - `bundled/skills/ensembl-database`
  - `bundled/skills/gene-database`
  - `bundled/skills/gget`
  - `bundled/skills/gwas-database`
  - `bundled/skills/kegg-database`
  - `bundled/skills/opentargets-database`
  - `bundled/skills/pdb-database`
  - `bundled/skills/reactome-database`
  - `bundled/skills/string-database`
- Modify: `config/pack-manifest.json`
  - Shrinks `bio-science.skill_candidates` and `route_authority_candidates` to the 13 direct owners.
- Modify: `config/skill-keyword-index.json`
  - Removes deleted skill IDs and adds `bio-database-evidence`.
- Modify: `config/skill-routing-rules.json`
  - Removes deleted skill IDs and adds `bio-database-evidence` positives/negatives.
- Modify: `config/skills-lock.json`
  - Regenerated after physical deletion and new skill creation.
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
  - Updates old database-wrapper route assertions to expect `bio-database-evidence`.
- Modify: `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`
  - Updates the machine-readable problem map and expected target counts.
- Create: `docs/governance/bio-science-second-pass-consolidation-2026-04-30.md`
  - Records before/after counts, retained owners, merged/deleted directories, tests, and remaining caveats.

## Constants

Use these exact lists throughout the implementation.

```python
BIO_SCIENCE_DIRECT_OWNERS = [
    "biopython",
    "scanpy",
    "anndata",
    "scvi-tools",
    "pydeseq2",
    "pysam",
    "deeptools",
    "esm",
    "cobrapy",
    "geniml",
    "arboreto",
    "flowio",
    "bio-database-evidence",
]

MERGED_DATABASE_SKILLS = [
    "alphafold-database",
    "bioservices",
    "cellxgene-census",
    "clinvar-database",
    "cosmic-database",
    "ensembl-database",
    "gene-database",
    "gget",
    "gwas-database",
    "kegg-database",
    "opentargets-database",
    "pdb-database",
    "reactome-database",
    "string-database",
]
```

## Task 1: Add Failing Second-Pass Regression Tests

**Files:**
- Create: `tests/runtime_neutral/test_bio_science_second_pass_consolidation.py`

- [ ] **Step 1: Create the failing test file**

Create `tests/runtime_neutral/test_bio_science_second_pass_consolidation.py` with this complete content:

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


BIO_SCIENCE_DIRECT_OWNERS = [
    "biopython",
    "scanpy",
    "anndata",
    "scvi-tools",
    "pydeseq2",
    "pysam",
    "deeptools",
    "esm",
    "cobrapy",
    "geniml",
    "arboreto",
    "flowio",
    "bio-database-evidence",
]

MERGED_DATABASE_SKILLS = [
    "alphafold-database",
    "bioservices",
    "cellxgene-census",
    "clinvar-database",
    "cosmic-database",
    "ensembl-database",
    "gene-database",
    "gget",
    "gwas-database",
    "kegg-database",
    "opentargets-database",
    "pdb-database",
    "reactome-database",
    "string-database",
]


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8-sig"))


def pack_by_id(pack_id: str) -> dict[str, object]:
    manifest = load_json("config/pack-manifest.json")
    packs = manifest.get("packs")
    assert isinstance(packs, list), manifest
    for pack in packs:
        assert isinstance(pack, dict), pack
        if pack.get("id") == pack_id:
            return pack
    raise AssertionError(f"pack missing: {pack_id}")


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


class BioScienceSecondPassConsolidationTests(unittest.TestCase):
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

    def test_bio_science_manifest_has_thirteen_direct_owners(self) -> None:
        pack = pack_by_id("bio-science")

        self.assertEqual(BIO_SCIENCE_DIRECT_OWNERS, pack.get("skill_candidates"))
        self.assertEqual(BIO_SCIENCE_DIRECT_OWNERS, pack.get("route_authority_candidates"))
        self.assertEqual([], pack.get("stage_assistant_candidates") or [])
        self.assertEqual(
            {
                "planning": "biopython",
                "coding": "biopython",
                "research": "scanpy",
            },
            pack.get("defaults_by_task"),
        )

    def test_merged_database_skills_are_removed_from_live_surfaces(self) -> None:
        keyword_index = load_json("config/skill-keyword-index.json")
        routing_rules = load_json("config/skill-routing-rules.json")
        skills_lock = load_json("config/skills-lock.json")

        keyword_skills = keyword_index.get("skills") or {}
        routing_skills = routing_rules.get("skills") or {}
        lock_skills = skills_lock.get("skills") or []
        lock_names = {
            str(item.get("name"))
            for item in lock_skills
            if isinstance(item, dict) and item.get("name")
        }

        self.assertIn("bio-database-evidence", keyword_skills)
        self.assertIn("bio-database-evidence", routing_skills)
        self.assertTrue((REPO_ROOT / "bundled" / "skills" / "bio-database-evidence").exists())

        for skill_id in MERGED_DATABASE_SKILLS:
            self.assertNotIn(skill_id, keyword_skills)
            self.assertNotIn(skill_id, routing_skills)
            self.assertNotIn(skill_id, lock_names)
            self.assertFalse((REPO_ROOT / "bundled" / "skills" / skill_id).exists())

    def test_bio_database_evidence_owns_biological_database_lookup(self) -> None:
        self.assert_selected(
            "查询 ClinVar COSMIC Ensembl GWAS KEGG Reactome Open Targets PDB STRING 的生物数据库证据",
            "bio-science",
            "bio-database-evidence",
        )

    def test_bio_database_evidence_owns_quick_gene_lookup(self) -> None:
        self.assert_selected(
            "快速查询 TP53 gene symbol、Ensembl ID、NCBI Gene metadata 和 RefSeq 注释",
            "bio-science",
            "bio-database-evidence",
        )

    def test_bio_database_evidence_owns_structure_and_ppi_evidence(self) -> None:
        self.assert_selected(
            "查询 AlphaFold predicted structure、RCSB PDB 坐标和 STRING protein interaction network",
            "bio-science",
            "bio-database-evidence",
        )

    def test_scanpy_still_owns_single_cell_analysis(self) -> None:
        self.assert_selected(
            "做 single-cell RNA-seq 聚类、UMAP、marker genes 和细胞注释",
            "bio-science",
            "scanpy",
        )

    def test_pydeseq2_still_owns_bulk_differential_expression(self) -> None:
        self.assert_selected(
            "bulk RNA-seq count matrix 做 DESeq2 差异表达、Wald test、FDR 和 volcano plot",
            "bio-science",
            "pydeseq2",
        )

    def test_pysam_still_owns_alignment_variant_files(self) -> None:
        self.assert_selected(
            "读取 BAM VCF 做 pileup、coverage 和 region extraction",
            "bio-science",
            "pysam",
        )

    def test_esm_still_owns_protein_embeddings(self) -> None:
        self.assert_selected(
            "用 ESM protein language model 做 protein embedding 和 inverse folding",
            "bio-science",
            "esm",
        )

    def test_cobrapy_still_owns_flux_balance(self) -> None:
        self.assert_selected(
            "用 COBRApy 做 FBA flux balance analysis 和 SBML metabolic model",
            "bio-science",
            "cobrapy",
        )

    def test_geniml_still_owns_bed_interval_embedding(self) -> None:
        self.assert_selected(
            "对 BED genomic intervals 做 Region2Vec embedding 和 regulatory region similarity",
            "bio-science",
            "geniml",
        )

    def test_rdkit_stays_in_chem_drug(self) -> None:
        self.assert_selected(
            "用 RDKit 处理 SMILES 和 Morgan fingerprint",
            "science-chem-drug",
            "rdkit",
        )

    def test_pubmed_bibtex_stays_in_literature_pack(self) -> None:
        self.assert_selected(
            "检索 PubMed 文献并导出 BibTeX 引用",
            "science-literature-citations",
            "pubmed-database",
        )

    def test_latex_build_stays_in_submission_pipeline(self) -> None:
        self.assert_selected(
            "用 LaTeX 构建论文 PDF 和 submission zip",
            "scholarly-publishing-workflow",
            "latex-submission-pipeline",
            task_type="coding",
        )

    def test_result_figures_stay_in_scientific_visualization(self) -> None:
        self.assert_selected(
            "绘制论文结果图、统计图和多面板 figure",
            "science-figures-visualization",
            "scientific-visualization",
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new tests and verify they fail**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_second_pass_consolidation.py -q
```

Expected result:

```text
FAILED tests/runtime_neutral/test_bio_science_second_pass_consolidation.py::BioScienceSecondPassConsolidationTests::test_bio_science_manifest_has_thirteen_direct_owners
FAILED tests/runtime_neutral/test_bio_science_second_pass_consolidation.py::BioScienceSecondPassConsolidationTests::test_merged_database_skills_are_removed_from_live_surfaces
FAILED tests/runtime_neutral/test_bio_science_second_pass_consolidation.py::BioScienceSecondPassConsolidationTests::test_bio_database_evidence_owns_biological_database_lookup
```

The exact number of failures can be higher before implementation. The important evidence is that the new target shape is not already satisfied.

- [ ] **Step 3: Commit the failing tests**

```powershell
git add -- tests/runtime_neutral/test_bio_science_second_pass_consolidation.py
git commit -m "test: capture bio science second pass target"
```

## Task 2: Create The Unified Bio Database Evidence Skill

**Files:**
- Create: `bundled/skills/bio-database-evidence/SKILL.md`
- Create: `bundled/skills/bio-database-evidence/references/database-evidence-sources.md`

- [ ] **Step 1: Create the skill directory**

```powershell
New-Item -ItemType Directory -Force bundled\skills\bio-database-evidence\references | Out-Null
```

- [ ] **Step 2: Add `SKILL.md`**

Create `bundled/skills/bio-database-evidence/SKILL.md` with this content:

```markdown
---
name: bio-database-evidence
description: "Unified biological database evidence owner. Use for gene annotation, variant clinical significance, cancer mutation evidence, GWAS trait associations, pathway mapping, target-disease evidence, protein structures, protein interaction networks, reference single-cell census queries, and cross-database biological ID mapping. Do not use for full single-cell analysis, bulk RNA-seq differential expression, BAM/VCF processing, protein embedding models, metabolic flux modeling, or genomic interval ML."
---

# Bio Database Evidence

## Use This Skill For

Use this skill when the main task is biological database lookup, annotation, or evidence gathering across one or more biological sources:

- Gene annotation, identifiers, RefSeq, Ensembl IDs, orthologs, VEP, GO, and genomic coordinates.
- Variant clinical significance, VUS interpretation support, ClinVar review status, cancer mutations, and COSMIC evidence.
- GWAS Catalog trait associations, rs IDs, p-values, summary statistics, and genetic epidemiology evidence.
- Pathway mapping, ID conversion, KEGG pathways, Reactome enrichment, disease pathways, and pathway evidence.
- Target-disease association evidence, tractability, safety, known drugs, and Open Targets evidence.
- Protein structure evidence from AlphaFold DB or RCSB PDB, including UniProt IDs, mmCIF/PDB downloads, pLDDT, PAE, and structure metadata.
- Protein-protein interaction evidence, STRING networks, hub proteins, and enrichment evidence.
- Reference single-cell data lookup from CELLxGENE Census when the user asks for census metadata or expression data, not full downstream analysis.
- Cross-database biological ID mapping and evidence tables across multiple resources.

## Do Not Use This Skill For

- Single-cell RNA-seq analysis, clustering, UMAP, marker genes, or cell annotation. Use `scanpy`.
- AnnData or h5ad container editing. Use `anndata`.
- scVI/scANVI latent models and batch correction. Use `scvi-tools`.
- Bulk RNA-seq differential expression. Use `pydeseq2`.
- BAM, SAM, CRAM, VCF, pileup, coverage, or region extraction. Use `pysam`.
- deepTools signal-track processing and heatmaps. Use `deeptools`.
- Protein language models, embeddings, inverse folding, or design. Use `esm`.
- Constraint-based metabolic modeling or FBA. Use `cobrapy`.
- BED/genomic interval embeddings or genomic-region ML. Use `geniml`.
- Gene regulatory network inference. Use `arboreto`.
- FCS or flow cytometry file parsing. Use `flowio`.

## Workflow

1. Identify the biological entity type: gene, transcript, variant, pathway, target, protein structure, protein interaction, trait association, or reference cell population.
2. Pick the narrowest source that answers the evidence question.
3. Preserve source names, query terms, access dates, identifiers, and API caveats in the result.
4. Return evidence in a table when comparing multiple sources.
5. State when authentication, license, rate limits, or non-public access restricts a source.

## Source Guide

See `references/database-evidence-sources.md` for source-specific boundaries and query notes.
```

- [ ] **Step 3: Add source reference**

Create `bundled/skills/bio-database-evidence/references/database-evidence-sources.md` with this content:

````markdown
# Biological Database Evidence Sources

## Gene And Transcript Annotation

- Ensembl: gene, transcript, ortholog, coordinate, and VEP-style variant consequence lookup.
- NCBI Gene: gene symbol, RefSeq, GO, genomic location, phenotype, and batch gene metadata.
- gget-style quick lookup: fast gene symbol, Ensembl ID, transcript, BLAST-style lookup, and small evidence checks.
- BioServices-style cross-database mapping: ID mapping across UniProt, KEGG, Reactome, and other biological resources.

## Variant, Cancer, And Trait Evidence

- ClinVar: clinical significance, VUS, review status, condition names, and variant annotation evidence.
- COSMIC: cancer mutation, Cancer Gene Census, mutational signatures, gene fusion, and somatic evidence. Authentication may be required.
- GWAS Catalog: SNP-trait associations, rs IDs, p-values, summary statistics, disease/trait metadata, and genetic epidemiology evidence.

## Pathway, Target, And Systems Evidence

- KEGG: pathway mapping, ID conversion, metabolic pathway lookup, organism-specific gene-pathway mapping, and drug/pathway evidence. Respect academic-use restrictions.
- Reactome: pathway enrichment, gene-pathway mapping, reactions, disease pathways, and expression/pathway evidence.
- Open Targets: target-disease associations, tractability, safety, genetics evidence, omics evidence, known drugs, and therapeutic target support.
- STRING: protein-protein interaction networks, interaction partners, GO/KEGG enrichment, hub proteins, and network evidence.

## Protein Structure Evidence

- AlphaFold DB: predicted structures by UniProt ID, mmCIF/PDB downloads, pLDDT, PAE, and predicted model confidence.
- RCSB PDB: experimental structure search, sequence similarity search, structure metadata, ligand context, and coordinate downloads.

## Reference Single-Cell Evidence

- CELLxGENE Census: reference cell and tissue queries, disease metadata, expression retrieval, population-scale cell metadata, and source dataset evidence.
- Use `scanpy` after the task becomes downstream analysis such as QC, normalization, clustering, marker genes, or cell annotation.

## Evidence Output Pattern

For multi-source tasks, return a table with these columns:

```text
source
query
identifier
evidence_type
key_result
access_or_license_note
confidence_or_review_status
````
```

- [ ] **Step 4: Run a file presence check**

Run:

```powershell
Test-Path bundled\skills\bio-database-evidence\SKILL.md
Test-Path bundled\skills\bio-database-evidence\references\database-evidence-sources.md
```

Expected:

```text
True
True
```

- [ ] **Step 5: Commit the new unified skill**

```powershell
git add -- bundled/skills/bio-database-evidence
git commit -m "feat: add bio database evidence skill"
```

## Task 3: Update Bio-Science Manifest To 13 Direct Owners

**Files:**
- Modify: `config/pack-manifest.json`

- [ ] **Step 1: Update `bio-science` candidate arrays**

Use a structured JSON edit. This PowerShell snippet preserves the current JSON shape and sets the target arrays:

```powershell
$path = "config/pack-manifest.json"
$json = Get-Content $path -Raw | ConvertFrom-Json
$target = @(
  "biopython",
  "scanpy",
  "anndata",
  "scvi-tools",
  "pydeseq2",
  "pysam",
  "deeptools",
  "esm",
  "cobrapy",
  "geniml",
  "arboreto",
  "flowio",
  "bio-database-evidence"
)
foreach ($pack in $json.packs) {
  if ($pack.id -eq "bio-science") {
    $pack.skill_candidates = $target
    $pack.route_authority_candidates = $target
    $pack.stage_assistant_candidates = @()
    $pack.defaults_by_task.planning = "biopython"
    $pack.defaults_by_task.coding = "biopython"
    $pack.defaults_by_task.research = "scanpy"
  }
}
$json | ConvertTo-Json -Depth 100 | Set-Content $path -Encoding UTF8
```

- [ ] **Step 2: Run the manifest-only test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_second_pass_consolidation.py::BioScienceSecondPassConsolidationTests::test_bio_science_manifest_has_thirteen_direct_owners -q
```

Expected:

```text
1 passed
```

- [ ] **Step 3: Commit manifest shrink**

```powershell
git add -- config/pack-manifest.json
git commit -m "fix: shrink bio science direct owners"
```

## Task 4: Update Keyword Index And Routing Rules

**Files:**
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`

- [ ] **Step 1: Remove merged skill IDs and add `bio-database-evidence` to `skill-keyword-index.json`**

Use this PowerShell snippet:

```powershell
$merged = @(
  "alphafold-database",
  "bioservices",
  "cellxgene-census",
  "clinvar-database",
  "cosmic-database",
  "ensembl-database",
  "gene-database",
  "gget",
  "gwas-database",
  "kegg-database",
  "opentargets-database",
  "pdb-database",
  "reactome-database",
  "string-database"
)
$path = "config/skill-keyword-index.json"
$json = Get-Content $path -Raw | ConvertFrom-Json
foreach ($skill in $merged) {
  if ($json.skills.PSObject.Properties.Name -contains $skill) {
    $json.skills.PSObject.Properties.Remove($skill)
  }
}
$json.skills | Add-Member -Force -NotePropertyName "bio-database-evidence" -NotePropertyValue ([pscustomobject]@{
  keywords = @(
    "bio-database-evidence",
    "biological database evidence",
    "gene annotation",
    "variant clinical significance",
    "target-disease association",
    "pathway mapping",
    "protein structure lookup",
    "protein interaction network",
    "GWAS trait association",
    "reference single-cell census",
    "cross-database ID mapping",
    "生物数据库证据",
    "基因注释",
    "变异临床意义",
    "靶点疾病证据",
    "通路映射",
    "蛋白结构查询",
    "蛋白互作网络",
    "ClinVar",
    "COSMIC",
    "Ensembl",
    "NCBI Gene",
    "GWAS Catalog",
    "KEGG",
    "Reactome",
    "Open Targets",
    "AlphaFold",
    "RCSB PDB",
    "STRING",
    "CELLxGENE Census"
  )
})
$json | ConvertTo-Json -Depth 100 | Set-Content $path -Encoding UTF8
```

- [ ] **Step 2: Remove merged skill IDs and add `bio-database-evidence` to `skill-routing-rules.json`**

Use this PowerShell snippet:

```powershell
$merged = @(
  "alphafold-database",
  "bioservices",
  "cellxgene-census",
  "clinvar-database",
  "cosmic-database",
  "ensembl-database",
  "gene-database",
  "gget",
  "gwas-database",
  "kegg-database",
  "opentargets-database",
  "pdb-database",
  "reactome-database",
  "string-database"
)
$path = "config/skill-routing-rules.json"
$json = Get-Content $path -Raw | ConvertFrom-Json
foreach ($skill in $merged) {
  if ($json.skills.PSObject.Properties.Name -contains $skill) {
    $json.skills.PSObject.Properties.Remove($skill)
  }
}
$json.skills | Add-Member -Force -NotePropertyName "bio-database-evidence" -NotePropertyValue ([pscustomobject]@{
  task_allow = @("research", "coding")
  positive_keywords = @(
    "bio-database-evidence",
    "biological database evidence",
    "gene annotation",
    "variant clinical significance",
    "target-disease association",
    "pathway mapping",
    "protein structure lookup",
    "protein interaction network",
    "GWAS trait association",
    "reference single-cell census",
    "cross-database ID mapping",
    "ClinVar",
    "COSMIC",
    "Ensembl",
    "NCBI Gene",
    "GWAS Catalog",
    "KEGG",
    "Reactome",
    "Open Targets",
    "AlphaFold",
    "RCSB PDB",
    "STRING",
    "CELLxGENE Census",
    "生物数据库证据",
    "基因注释",
    "变异临床意义",
    "靶点疾病证据",
    "通路映射",
    "蛋白结构查询",
    "蛋白互作网络"
  )
  negative_keywords = @(
    "scanpy",
    "single-cell clustering",
    "marker genes",
    "Leiden",
    "scVI",
    "scANVI",
    "DESeq2",
    "PyDESeq2",
    "bulk RNA-seq differential expression",
    "BAM",
    "SAM",
    "CRAM",
    "VCF",
    "pileup",
    "coverage",
    "deepTools",
    "bamCoverage",
    "computeMatrix",
    "ESM",
    "protein embedding",
    "inverse folding",
    "COBRApy",
    "FBA",
    "flux balance",
    "BED genomic intervals",
    "Region2Vec",
    "GRNBoost2",
    "GENIE3",
    "flow cytometry",
    "FCS",
    "RDKit",
    "SMILES",
    "PubMed",
    "BibTeX",
    "DICOM",
    "LaTeX",
    "submission zip",
    "结果图",
    "scientific visualization"
  )
  equivalent_group = $null
  canonical_for_task = @("research")
})
$json | ConvertTo-Json -Depth 100 | Set-Content $path -Encoding UTF8
```

- [ ] **Step 3: Run focused routing tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_second_pass_consolidation.py -q
```

Expected at this point:

```text
FAILED tests/runtime_neutral/test_bio_science_second_pass_consolidation.py::BioScienceSecondPassConsolidationTests::test_merged_database_skills_are_removed_from_live_surfaces
```

The deletion/lock test should still fail because the old directories and stale lock entries still exist.

- [ ] **Step 4: Commit route config changes**

```powershell
git add -- config/skill-keyword-index.json config/skill-routing-rules.json
git commit -m "fix: route bio database evidence through unified owner"
```

## Task 5: Update Existing Bio-Science Routing Tests

**Files:**
- Modify: `tests/runtime_neutral/test_bio_science_boundary_hardening.py`
- Modify: `tests/runtime_neutral/test_bio_science_direct_owner_routing.py`

- [ ] **Step 1: Replace deleted-skill expectations in boundary-hardening tests**

Edit `tests/runtime_neutral/test_bio_science_boundary_hardening.py`:

- Rename `test_cellxgene_owns_census_queries` to `test_bio_database_evidence_owns_census_queries`.
- Change expected skill from `"cellxgene-census"` to `"bio-database-evidence"`.
- Rename `test_bioservices_owns_explicit_multi_service_aggregation` to `test_bio_database_evidence_owns_multi_service_aggregation`.
- Change expected skill from `"bioservices"` to `"bio-database-evidence"`.
- Rename `test_gget_owns_quick_lookup` to `test_bio_database_evidence_owns_quick_lookup`.
- Change expected skill from `"gget"` to `"bio-database-evidence"`.
- Rename `test_scanpy_loses_to_cellxgene_for_census_query` to `test_scanpy_loses_to_bio_database_evidence_for_census_query`.
- Change expected skill from `"cellxgene-census"` to `"bio-database-evidence"`.
- Rename `test_bioservices_loses_to_kegg_for_explicit_kegg_rest` to `test_bio_database_evidence_owns_explicit_kegg_rest`.
- Change expected skill from `"kegg-database"` to `"bio-database-evidence"`.
- Rename `test_bioservices_loses_to_reactome_for_explicit_reactome` to `test_bio_database_evidence_owns_explicit_reactome`.
- Change expected skill from `"reactome-database"` to `"bio-database-evidence"`.
- Rename `test_gget_loses_to_opentargets_for_target_evidence` to `test_bio_database_evidence_owns_target_evidence`.
- Change expected skill from `"opentargets-database"` to `"bio-database-evidence"`.

The replacement assertion pattern is:

```python
self.assert_selected(
    "用 Open Targets 做 target-disease association、tractability 和 known drugs evidence，不使用 gget",
    "bio-science",
    "bio-database-evidence",
)
```

- [ ] **Step 2: Replace direct-owner database tests**

Replace the database-wrapper methods in `tests/runtime_neutral/test_bio_science_direct_owner_routing.py` with these three tests:

```python
    def test_bio_database_evidence_routes_for_cross_database_queries(self) -> None:
        self.assert_selected("用 BioServices 同时查询 UniProt、KEGG、Reactome 并做 ID mapping", "bio-database-evidence")

    def test_bio_database_evidence_routes_for_variant_pathway_and_target_sources(self) -> None:
        self.assert_selected(
            "查询 ClinVar、COSMIC、GWAS Catalog、KEGG、Reactome 和 Open Targets 的生物数据库证据",
            "bio-database-evidence",
        )

    def test_bio_database_evidence_routes_for_structure_ppi_and_census_sources(self) -> None:
        self.assert_selected(
            "查询 AlphaFold Database、RCSB PDB、STRING API 和 CZ CELLxGENE Census 的 evidence metadata",
            "bio-database-evidence",
        )
```

Keep the existing `anndata`, `scvi-tools`, and `deeptools` tests unchanged.

- [ ] **Step 3: Run updated routing tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_boundary_hardening.py tests/runtime_neutral/test_bio_science_direct_owner_routing.py tests/runtime_neutral/test_bio_science_second_pass_consolidation.py -q
```

Expected at this point:

```text
FAILED tests/runtime_neutral/test_bio_science_second_pass_consolidation.py::BioScienceSecondPassConsolidationTests::test_merged_database_skills_are_removed_from_live_surfaces
```

The old directories and stale lock are still present, so that single category of failure remains.

- [ ] **Step 4: Commit test updates**

```powershell
git add -- tests/runtime_neutral/test_bio_science_boundary_hardening.py tests/runtime_neutral/test_bio_science_direct_owner_routing.py
git commit -m "test: update bio science database owner expectations"
```

## Task 6: Update Skill Index Routing Audit Script

**Files:**
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`

- [ ] **Step 1: Replace old database assertion expected skills**

In `scripts/verify/vibe-skill-index-routing-audit.ps1`, update these rows:

```powershell
[pscustomobject]@{ Name = "gget gene symbol"; Prompt = "用gget快速查询基因symbol和Ensembl ID"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "bioservices cross database"; Prompt = "用 BioServices 同时查询 UniProt、KEGG、Reactome 并做 ID mapping"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "alphafold predicted structure"; Prompt = "从 AlphaFold Database 按 UniProt ID 下载 mmCIF，并检查 pLDDT 和 PAE"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "clinvar clinical significance"; Prompt = "查询 ClinVar 中 BRCA1 variant 的 clinical significance、VUS 和 review stars"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "cosmic cancer mutation"; Prompt = "查询 COSMIC cancer mutation、Cancer Gene Census 和 mutational signatures"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "ensembl vep orthologs"; Prompt = "用 Ensembl REST 查询 gene、orthologs、VEP variant effect 和坐标转换"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "ncbi gene metadata"; Prompt = "用 NCBI Gene 查询 TP53 symbol、RefSeq、GO annotation 和基因位置"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "gwas catalog traits"; Prompt = "查询 GWAS Catalog 中 rs ID、trait association、p-value 和 summary statistics"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "kegg pathway mapping"; Prompt = "用 KEGG REST 做 pathway mapping、ID conversion 和 metabolic pathway 查询"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "open targets evidence"; Prompt = "用 Open Targets 查询 target-disease association、tractability、safety 和 known drugs"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "rcsb pdb structure"; Prompt = "在 RCSB PDB 按 sequence similarity 搜索结构并下载 PDB/mmCIF 坐标"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "reactome enrichment"; Prompt = "用 Reactome 做 pathway enrichment、gene-pathway mapping 和 disease pathway 分析"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "string ppi network"; Prompt = "用 STRING API 查询 protein-protein interaction network、GO enrichment 和 hub proteins"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
[pscustomobject]@{ Name = "cellxgene census"; Prompt = "查询 CZ CELLxGENE Census 的 human lung epithelial cells expression data 和 metadata"; Grade = "M"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "bio-database-evidence" },
```

- [ ] **Step 2: Run the skill-index audit**

Run:

```powershell
.\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected:

```text
Total assertions: 436
Passed: 436
Failed: 0
Skill-index routing audit passed.
```

The total assertion count can change only if the script adds or removes rows. This task changes expected skills only, so the total should remain `436`.

- [ ] **Step 3: Commit audit script update**

```powershell
git add -- scripts/verify/vibe-skill-index-routing-audit.ps1
git commit -m "test: route bio database audit cases to unified owner"
```

## Task 7: Update Bio-Science Pack Consolidation Audit

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`
- Modify: `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`

- [ ] **Step 1: Update audit constants**

In `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`, set:

```python
BIO_SCIENCE_ROUTE_AUTHORITIES = [
    "biopython",
    "scanpy",
    "anndata",
    "scvi-tools",
    "pydeseq2",
    "pysam",
    "deeptools",
    "esm",
    "cobrapy",
    "geniml",
    "arboreto",
    "flowio",
    "bio-database-evidence",
]

BIO_SCIENCE_STAGE_ASSISTANTS: list[str] = []
```

- [ ] **Step 2: Add merge/delete decisions**

Add this helper constant near the route authority list:

```python
BIO_SCIENCE_MERGE_DELETE_SKILLS = [
    "alphafold-database",
    "bioservices",
    "cellxgene-census",
    "clinvar-database",
    "cosmic-database",
    "ensembl-database",
    "gene-database",
    "gget",
    "gwas-database",
    "kegg-database",
    "opentargets-database",
    "pdb-database",
    "reactome-database",
    "string-database",
]
```

For each skill in `BIO_SCIENCE_MERGE_DELETE_SKILLS`, update `BIO_SCIENCE_PROBLEM_DECISIONS` to use:

```python
{
    "problem_ids": ["biological_database_evidence"],
    "primary_problem_id": "biological_database_evidence",
    "target_role": "merge-delete-after-migration",
    "target_owner": "bio-database-evidence",
    "overlap_with": "bio-database-evidence",
    "routing_change": "merge useful database evidence material into bio-database-evidence and remove this separate route owner",
    "delete_allowed_after_migration": True,
    "risk_level": "medium",
    "rationale": "This is useful biological evidence source material, but it should not remain a separate top-level route owner.",
}
```

Use `problem_ids = ["biological_database_evidence"]` for all merged database/API wrapper rows. The required target role and owner must match exactly.

Add a new decision for `bio-database-evidence`:

```python
"bio-database-evidence": {
    "problem_ids": ["biological_database_evidence"],
    "primary_problem_id": "biological_database_evidence",
    "target_role": "keep",
    "target_owner": "",
    "overlap_with": "biopython; scanpy; pydeseq2; pysam; esm; cobrapy; geniml",
    "routing_change": "keep as unified route authority for biological database evidence, annotation, pathway, variant, target, structure, interaction, reference census, and cross-database lookup tasks",
    "delete_allowed_after_migration": False,
    "risk_level": "low",
    "rationale": "A single evidence owner keeps useful database material without exposing every source wrapper as a separate route authority.",
},
```

- [ ] **Step 3: Update audit tests**

In `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`:

- Replace `BIO_SCIENCE_CANDIDATES` with `BIO_SCIENCE_DIRECT_OWNERS`.
- Add `MERGED_DATABASE_SKILLS`.
- Set `BIO_SCIENCE_DIRECT_ROUTE_OWNERS = BIO_SCIENCE_DIRECT_OWNERS`.
- Update fixture manifest `bio-science.skill_candidates` to `BIO_SCIENCE_DIRECT_OWNERS`.
- Write fixture skills for `BIO_SCIENCE_DIRECT_OWNERS + MERGED_DATABASE_SKILLS`.
- Change the target count assertion to `13`.
- Assert merge/delete rows count is `14`.
- Replace the old `rows["gget"].primary_problem_id` assertion with `rows["bio-database-evidence"].primary_problem_id == "biological_database_evidence"`.
- Replace `test_database_and_data_structure_helpers_are_direct_route_owners` with:

```python
    def test_database_wrappers_are_merge_delete_rows(self) -> None:
        artifact = audit_bio_science_problem_map(self.root)
        rows = {row.skill_id: row for row in artifact.rows}

        for skill_id in MERGED_DATABASE_SKILLS:
            self.assertEqual("merge-delete-after-migration", rows[skill_id].target_role)
            self.assertEqual("bio-database-evidence", rows[skill_id].target_owner)
            self.assertTrue(rows[skill_id].delete_allowed_after_migration)
```

- [ ] **Step 4: Run audit tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
```

Expected:

```text
7 passed
```

- [ ] **Step 5: Commit audit update**

```powershell
git add -- packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py
git commit -m "fix: update bio science consolidation audit target"
```

## Task 8: Review, Migrate, And Delete Merged Skill Directories

**Files:**
- Modify/Create: `bundled/skills/bio-database-evidence/references/database-evidence-sources.md`
- Delete: all directories in `MERGED_DATABASE_SKILLS`

- [ ] **Step 1: Inventory source directories before deletion**

Run:

```powershell
$merged = @(
  "alphafold-database",
  "bioservices",
  "cellxgene-census",
  "clinvar-database",
  "cosmic-database",
  "ensembl-database",
  "gene-database",
  "gget",
  "gwas-database",
  "kegg-database",
  "opentargets-database",
  "pdb-database",
  "reactome-database",
  "string-database"
)
foreach ($skill in $merged) {
  $dir = Join-Path "bundled\skills" $skill
  $files = if (Test-Path $dir) { Get-ChildItem $dir -Recurse -File | ForEach-Object { $_.FullName.Replace((Resolve-Path ".").Path + "\", "") } } else { @() }
  "[$skill]"
  $files
}
```

Expected:

```text
Each merged skill prints its current files for migration review.
```

- [ ] **Step 2: Confirm migrated reference covers every source**

Open `bundled/skills/bio-database-evidence/references/database-evidence-sources.md` and verify it contains these source names:

```text
AlphaFold
BioServices
CELLxGENE Census
ClinVar
COSMIC
Ensembl
NCBI Gene
gget-style
GWAS Catalog
KEGG
Open Targets
RCSB PDB
Reactome
STRING
```

Add one concise bullet for any missing source before deleting directories.

- [ ] **Step 3: Delete merged directories with path safety check**

Run:

```powershell
$repo = (Resolve-Path ".").Path
$skillsRoot = (Resolve-Path "bundled\skills").Path
$merged = @(
  "alphafold-database",
  "bioservices",
  "cellxgene-census",
  "clinvar-database",
  "cosmic-database",
  "ensembl-database",
  "gene-database",
  "gget",
  "gwas-database",
  "kegg-database",
  "opentargets-database",
  "pdb-database",
  "reactome-database",
  "string-database"
)
foreach ($skill in $merged) {
  $target = Join-Path $skillsRoot $skill
  if (-not (Test-Path -LiteralPath $target)) {
    continue
  }
  $resolved = (Resolve-Path -LiteralPath $target).Path
  if (-not $resolved.StartsWith($skillsRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to delete outside bundled skills root: $resolved"
  }
  Remove-Item -LiteralPath $resolved -Recurse -Force
}
```

- [ ] **Step 4: Run deletion presence check**

Run:

```powershell
$merged = @(
  "alphafold-database",
  "bioservices",
  "cellxgene-census",
  "clinvar-database",
  "cosmic-database",
  "ensembl-database",
  "gene-database",
  "gget",
  "gwas-database",
  "kegg-database",
  "opentargets-database",
  "pdb-database",
  "reactome-database",
  "string-database"
)
$merged | ForEach-Object { [pscustomobject]@{ skill = $_; exists = Test-Path (Join-Path "bundled\skills" $_) } }
```

Expected:

```text
All rows have exists = False.
```

- [ ] **Step 5: Commit migration and physical deletion**

```powershell
git add -- bundled/skills/bio-database-evidence bundled/skills/alphafold-database bundled/skills/bioservices bundled/skills/cellxgene-census bundled/skills/clinvar-database bundled/skills/cosmic-database bundled/skills/ensembl-database bundled/skills/gene-database bundled/skills/gget bundled/skills/gwas-database bundled/skills/kegg-database bundled/skills/opentargets-database bundled/skills/pdb-database bundled/skills/reactome-database bundled/skills/string-database
git commit -m "fix: merge bio database skills into evidence owner"
```

## Task 9: Refresh Skills Lock

**Files:**
- Modify: `config/skills-lock.json`

- [ ] **Step 1: Regenerate skills lock**

Run:

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected:

```text
skills-lock generated: F:\vibe\Vibe-Skills\config\skills-lock.json
```

- [ ] **Step 2: Run deleted-skill absence check**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_second_pass_consolidation.py::BioScienceSecondPassConsolidationTests::test_merged_database_skills_are_removed_from_live_surfaces -q
```

Expected:

```text
1 passed
```

- [ ] **Step 3: Commit lock refresh**

```powershell
git add -- config/skills-lock.json
git commit -m "chore: refresh skills lock after bio science pruning"
```

## Task 10: Write Governance Note

**Files:**
- Create: `docs/governance/bio-science-second-pass-consolidation-2026-04-30.md`

- [ ] **Step 1: Add governance note**

Create `docs/governance/bio-science-second-pass-consolidation-2026-04-30.md` with this structure and content:

````markdown
# Bio-Science Second-Pass Consolidation - 2026-04-30

## Scope

This pass shrinks `bio-science` from a broad database/tool list into a smaller direct-owner pack. It does not change the six-stage Vibe runtime and does not introduce helper experts, advisory routing, consultation routing, primary/secondary skill states, or stage assistants.

The live skill-use model remains:

```text
candidate skill -> selected skill -> used / unused
````

## Counts

| Metric | Before | After |
| --- | ---: | ---: |
| `skill_candidates` | 26 | 13 |
| `route_authority_candidates` | 26 | 13 |
| `stage_assistant_candidates` | 0 | 0 |
| physically deleted skill directories | 0 | 14 |

## Retained Direct Owners

| Skill | Problem owner |
| --- | --- |
| `biopython` | Sequence files, SeqIO, Entrez, FASTA/GenBank conversion. |
| `scanpy` | Single-cell RNA-seq analysis. |
| `anndata` | AnnData/h5ad container work. |
| `scvi-tools` | Single-cell latent models and batch correction. |
| `pydeseq2` | Bulk RNA-seq differential expression. |
| `pysam` | BAM/VCF alignment and variant-file processing. |
| `deeptools` | Genomics signal tracks and heatmap/profile workflows. |
| `esm` | Protein language models and embeddings. |
| `cobrapy` | Metabolic flux modeling and FBA. |
| `geniml` | Genomic interval embeddings and genomic-region ML. |
| `arboreto` | Gene regulatory network inference. |
| `flowio` | FCS and flow cytometry file parsing. |
| `bio-database-evidence` | Biological database evidence, annotation, pathway, variant, target, structure, interaction, reference census, and cross-database lookup. |

## Merged And Deleted

| Deleted skill | New owner |
| --- | --- |
| `alphafold-database` | `bio-database-evidence` |
| `bioservices` | `bio-database-evidence` |
| `cellxgene-census` | `bio-database-evidence` |
| `clinvar-database` | `bio-database-evidence` |
| `cosmic-database` | `bio-database-evidence` |
| `ensembl-database` | `bio-database-evidence` |
| `gene-database` | `bio-database-evidence` |
| `gget` | `bio-database-evidence` |
| `gwas-database` | `bio-database-evidence` |
| `kegg-database` | `bio-database-evidence` |
| `opentargets-database` | `bio-database-evidence` |
| `pdb-database` | `bio-database-evidence` |
| `reactome-database` | `bio-database-evidence` |
| `string-database` | `bio-database-evidence` |

## Verification

Record the final command outputs here after implementation:

```text
python -m pytest tests/runtime_neutral/test_bio_science_second_pass_consolidation.py tests/runtime_neutral/test_bio_science_boundary_hardening.py tests/runtime_neutral/test_bio_science_direct_owner_routing.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-bio-science-pack-consolidation-audit-gate.ps1
.\scripts\verify\vibe-global-pack-consolidation-audit-gate.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
git diff --check
```

## Caveats

- This is routing/config and bundled-skill cleanup, not proof that `bio-database-evidence` was materially used in a real task.
- Old governance notes may mention deleted skill IDs as historical state.
- Cross-pack boundaries for chemistry, literature, imaging, LaTeX submission, and scientific figures remain protected by regression tests.
```

- [ ] **Step 2: Commit governance note**

```powershell
git add -- docs/governance/bio-science-second-pass-consolidation-2026-04-30.md
git commit -m "docs: record bio science second pass consolidation"
```

## Task 11: Run Focused And Broad Verification

**Files:**
- No planned edits.

- [ ] **Step 1: Run focused Python tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_second_pass_consolidation.py tests/runtime_neutral/test_bio_science_boundary_hardening.py tests/runtime_neutral/test_bio_science_direct_owner_routing.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
```

Expected:

```text
All selected tests pass.
```

- [ ] **Step 2: Run skill-index route audit**

Run:

```powershell
.\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected:

```text
Total assertions: 436
Passed: 436
Failed: 0
Skill-index routing audit passed.
```

- [ ] **Step 3: Run pack routing smoke**

Run:

```powershell
.\scripts\verify\vibe-pack-routing-smoke.ps1
```

Expected:

```text
Total assertions: 958
Passed: 958
Failed: 0
Pack routing smoke checks passed.
```

- [ ] **Step 4: Run bio-science audit gate**

Run:

```powershell
.\scripts\verify\vibe-bio-science-pack-consolidation-audit-gate.ps1
```

Expected:

```text
[PASS] vibe-bio-science-pack-consolidation-audit-gate passed
```

- [ ] **Step 5: Run global pack audit gate**

Run:

```powershell
.\scripts\verify\vibe-global-pack-consolidation-audit-gate.ps1
```

Expected:

```text
[PASS] vibe-global-pack-consolidation-audit-gate passed
```

Also inspect the JSON summary and confirm `bio-science` no longer reports 26 route authorities.

- [ ] **Step 6: Run offline skills gate**

Run:

```powershell
.\scripts\verify\vibe-offline-skills-gate.ps1
```

Expected:

```text
[PASS] offline skill closure gate passed.
```

- [ ] **Step 7: Run whitespace check**

Run:

```powershell
git diff --check
```

Expected:

```text
No output and exit code 0.
```

## Task 12: Final Stale-ID Search And Final Commit

**Files:**
- Modify any file that still contains stale live-route expectations.

- [ ] **Step 1: Search for stale deleted skill IDs in live surfaces**

Run:

```powershell
rg "alphafold-database|bioservices|cellxgene-census|clinvar-database|cosmic-database|ensembl-database|gene-database|gget|gwas-database|kegg-database|opentargets-database|pdb-database|reactome-database|string-database" config scripts tests packages bundled
```

Expected allowed matches:

```text
packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py
tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py
tests/runtime_neutral/test_bio_science_second_pass_consolidation.py
```

No matches should remain under:

```text
config/
bundled/skills/
scripts/verify/vibe-skill-index-routing-audit.ps1
```

- [ ] **Step 2: Inspect final status**

Run:

```powershell
git status --short --branch
git diff --stat
```

Expected:

```text
Only intended bio-science second-pass files are modified.
```

- [ ] **Step 3: Commit remaining changes**

If every earlier task committed separately, this step should have nothing to commit. If any verified changes remain, commit them:

```powershell
git add -- config/pack-manifest.json config/skill-keyword-index.json config/skill-routing-rules.json config/skills-lock.json bundled/skills/bio-database-evidence bundled/skills/alphafold-database bundled/skills/bioservices bundled/skills/cellxgene-census bundled/skills/clinvar-database bundled/skills/cosmic-database bundled/skills/ensembl-database bundled/skills/gene-database bundled/skills/gget bundled/skills/gwas-database bundled/skills/kegg-database bundled/skills/opentargets-database bundled/skills/pdb-database bundled/skills/reactome-database bundled/skills/string-database scripts/verify/vibe-skill-index-routing-audit.ps1 packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_second_pass_consolidation.py tests/runtime_neutral/test_bio_science_boundary_hardening.py tests/runtime_neutral/test_bio_science_direct_owner_routing.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py docs/governance/bio-science-second-pass-consolidation-2026-04-30.md
git commit -m "fix: consolidate bio science database routing"
```

- [ ] **Step 4: Final report**

Report:

```text
branch
commit hash or hashes
before/after counts
retained direct owners
deleted merged directories
verification commands and pass/fail counts
remaining caveats
```

Make the report explicit that this proves routing/config cleanup, not material use in a real Vibe task.
