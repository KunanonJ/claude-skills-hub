# Bio-Science Pack Consolidation Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the `bio-science` pack into a problem-first routing surface with explicit expert ownership, stage-assistant boundaries, route probes, and deletion caveats.

**Architecture:** Add a focused `bio-science` problem-map audit, then update pack manifest roles, keyword index entries, routing rules, and route regression probes. The first implementation keeps all 26 skill directories and treats physical deletion as a separate asset-migration pass.

**Tech Stack:** Python standard library, PowerShell verify gates, JSON routing config, existing Vibe-Skills bundled skill layout, pytest runtime-neutral tests.

---

## File Structure

- Create: `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`
  - Owns the 26-row `bio-science` problem map, role decisions, asset summaries, artifact writing, and CLI.
- Create: `scripts/verify/runtime_neutral/bio_science_pack_consolidation_audit.py`
  - Thin runtime-neutral wrapper that bootstraps `verification-core` onto `sys.path`.
- Create: `scripts/verify/vibe-bio-science-pack-consolidation-audit-gate.ps1`
  - PowerShell gate that runs the Python audit and optionally writes artifacts.
- Create: `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`
  - Tests the problem-map decisions, artifact writer, wrapper, and final live manifest role split.
- Modify: `config/pack-manifest.json`
  - Adds `bio-science.route_authority_candidates` and `bio-science.stage_assistant_candidates`.
  - Keeps all 26 `skill_candidates`.
- Modify: `config/skill-keyword-index.json`
  - Adds missing `gget` and `bioservices` entries and strengthens narrow positive signals for the ten route owners.
- Modify: `config/skill-routing-rules.json`
  - Adds positive and negative boundaries so `scanpy` and `biopython` stop absorbing specific bio-science and cross-pack prompts.
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
  - Adds skill-level route expectations for all ten retained `bio-science` route authorities and cross-pack false positives.
- Modify: `scripts/verify/probe-scientific-packs.ps1`
  - Extends the black-box scientific pack probe matrix for `bio-science` route owners.
- Create: `docs/governance/bio-science-problem-first-consolidation-2026-04-28.md`
  - Records before/after counts, role decisions, protected probes, and deletion boundaries.
- Modify generated: `config/skills-lock.json`
  - Refresh only after all config and bundled-skill changes are stable.
- Create generated: `outputs/skills-audit/bio-science-problem-map.json`
- Create generated: `outputs/skills-audit/bio-science-problem-map.csv`
- Create generated: `outputs/skills-audit/bio-science-problem-consolidation.md`

## Execution Boundary

- Only govern the `bio-science` pack in this plan.
- Do not rewrite the router selection algorithm.
- Do not physically delete `bundled/skills/**` directories in this plan.
- Do not move skills between adjacent science packs except through negative-boundary route protection.
- Do not launch canonical `$vibe`; this is repo-local implementation work from an already approved Superpowers plan.

---

### Task 1: Add Failing Bio-Science Audit Tests

**Files:**
- Create: `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`
- Implementation target: `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`

- [ ] **Step 1: Create the test file**

Create `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py` with this content:

```python
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
VERIFICATION_CORE_SRC = REPO_ROOT / "packages" / "verification-core" / "src"
if str(VERIFICATION_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(VERIFICATION_CORE_SRC))

from vgo_verify.bio_science_pack_consolidation_audit import (
    BIO_SCIENCE_ROUTE_AUTHORITIES,
    BIO_SCIENCE_STAGE_ASSISTANTS,
    audit_bio_science_problem_map,
    write_bio_science_problem_artifacts,
)


BIO_SCIENCE_CANDIDATES = [
    "alphafold-database",
    "anndata",
    "biopython",
    "bioservices",
    "cellxgene-census",
    "clinvar-database",
    "cosmic-database",
    "deeptools",
    "ensembl-database",
    "gene-database",
    "gget",
    "gwas-database",
    "kegg-database",
    "opentargets-database",
    "pdb-database",
    "pydeseq2",
    "pysam",
    "reactome-database",
    "scanpy",
    "scvi-tools",
    "arboreto",
    "cobrapy",
    "esm",
    "flowio",
    "geniml",
    "string-database",
]


class BioSciencePackConsolidationAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self._write_fixture_repo()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _write(self, relative_path: str, content: str) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    def _write_json(self, relative_path: str, payload: object) -> None:
        self._write(relative_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    def _write_skill(
        self,
        skill_id: str,
        *,
        scripts: bool = False,
        references: bool = False,
        assets: bool = False,
    ) -> None:
        self._write(
            f"bundled/skills/{skill_id}/SKILL.md",
            "---\n"
            f"name: {skill_id}\n"
            f"description: Fixture skill for {skill_id}.\n"
            "---\n\n"
            f"# {skill_id}\n\n"
            f"Use {skill_id} for its explicit bio-science workflow.\n",
        )
        if scripts:
            self._write(f"bundled/skills/{skill_id}/scripts/run.py", "print('ok')\n")
        if references:
            self._write(f"bundled/skills/{skill_id}/references/guide.md", "# Guide\n\nConcrete guidance.\n")
        if assets:
            self._write(f"bundled/skills/{skill_id}/assets/example.txt", "asset\n")

    def _write_fixture_repo(self) -> None:
        self._write_json(
            "config/pack-manifest.json",
            {
                "packs": [
                    {
                        "id": "bio-science",
                        "skill_candidates": BIO_SCIENCE_CANDIDATES,
                        "defaults_by_task": {
                            "planning": "biopython",
                            "coding": "biopython",
                            "research": "scanpy",
                        },
                    },
                    {
                        "id": "science-chem-drug",
                        "skill_candidates": ["rdkit"],
                        "defaults_by_task": {"coding": "rdkit"},
                    },
                ]
            },
        )
        self._write_json("config/skill-keyword-index.json", {"skills": {}})
        self._write_json("config/skill-routing-rules.json", {"skills": {}})
        for skill_id in BIO_SCIENCE_CANDIDATES:
            self._write_skill(
                skill_id,
                scripts=skill_id in {"scanpy", "pysam", "cobrapy", "flowio"},
                references=skill_id.endswith("-database") or skill_id in {"biopython", "gget", "esm"},
                assets=skill_id in {"cellxgene-census", "pdb-database"},
            )

    def test_problem_map_covers_all_candidates_and_target_roles(self) -> None:
        artifact = audit_bio_science_problem_map(self.root)
        rows = {row.skill_id: row for row in artifact.rows}

        self.assertEqual(set(BIO_SCIENCE_CANDIDATES), set(rows))
        self.assertEqual(set(BIO_SCIENCE_ROUTE_AUTHORITIES), {row.skill_id for row in artifact.rows if row.target_role == "keep"})
        self.assertEqual(set(BIO_SCIENCE_STAGE_ASSISTANTS), {row.skill_id for row in artifact.rows if row.target_role == "stage-assistant"})
        self.assertEqual(10, artifact.to_dict()["summary"]["target_route_authority_count"])
        self.assertEqual(16, artifact.to_dict()["summary"]["target_stage_assistant_count"])

    def test_problem_map_records_primary_problem_owners(self) -> None:
        artifact = audit_bio_science_problem_map(self.root)
        rows = {row.skill_id: row for row in artifact.rows}

        self.assertEqual("single_cell_rnaseq", rows["scanpy"].primary_problem_id)
        self.assertEqual("bulk_rnaseq_differential_expression", rows["pydeseq2"].primary_problem_id)
        self.assertEqual("alignment_variant_files", rows["pysam"].primary_problem_id)
        self.assertEqual("sequence_io_entrez", rows["biopython"].primary_problem_id)
        self.assertEqual("gene_symbol_lookup", rows["gget"].primary_problem_id)
        self.assertEqual("protein_language_models", rows["esm"].primary_problem_id)
        self.assertEqual("metabolic_flux_modeling", rows["cobrapy"].primary_problem_id)
        self.assertEqual("flow_cytometry_fcs_io", rows["flowio"].primary_problem_id)
        self.assertEqual("gene_regulatory_networks", rows["arboreto"].primary_problem_id)
        self.assertEqual("genomic_ml_embeddings", rows["geniml"].primary_problem_id)

    def test_database_and_data_structure_helpers_are_stage_assistants(self) -> None:
        artifact = audit_bio_science_problem_map(self.root)
        rows = {row.skill_id: row for row in artifact.rows}

        for skill_id in [
            "alphafold-database",
            "anndata",
            "bioservices",
            "cellxgene-census",
            "clinvar-database",
            "cosmic-database",
            "deeptools",
            "ensembl-database",
            "gene-database",
            "gwas-database",
            "kegg-database",
            "opentargets-database",
            "pdb-database",
            "reactome-database",
            "scvi-tools",
            "string-database",
        ]:
            self.assertEqual("stage-assistant", rows[skill_id].target_role)
            self.assertFalse(rows[skill_id].delete_allowed_after_migration)
            self.assertIn("not a broad route authority", rows[skill_id].routing_change)

    def test_artifact_writer_outputs_json_csv_and_markdown(self) -> None:
        artifact = audit_bio_science_problem_map(self.root)
        output_dir = self.root / "outputs" / "skills-audit"
        written = write_bio_science_problem_artifacts(self.root, artifact, output_dir)

        self.assertTrue(written["json"].exists())
        self.assertTrue(written["csv"].exists())
        self.assertTrue(written["markdown"].exists())
        self.assertIn("bio-science-problem-map", written["json"].name)

        csv_text = written["csv"].read_text(encoding="utf-8")
        self.assertIn("skill_id,problem_ids,primary_problem_id", csv_text)
        self.assertIn("scanpy", csv_text)
        self.assertIn("pydeseq2", csv_text)

        markdown_text = written["markdown"].read_text(encoding="utf-8")
        self.assertIn("# Bio-Science Problem-First Consolidation", markdown_text)
        self.assertIn("## Route Authorities", markdown_text)
        self.assertIn("## Stage Assistants", markdown_text)

    def test_audit_and_writer_do_not_modify_live_config(self) -> None:
        config_paths = [
            self.root / "config" / "pack-manifest.json",
            self.root / "config" / "skill-keyword-index.json",
            self.root / "config" / "skill-routing-rules.json",
        ]
        before = {path: path.read_text(encoding="utf-8") for path in config_paths}

        artifact = audit_bio_science_problem_map(self.root)
        write_bio_science_problem_artifacts(self.root, artifact, self.root / "outputs" / "skills-audit")

        after = {path: path.read_text(encoding="utf-8") for path in config_paths}
        self.assertEqual(before, after)

    def test_runtime_neutral_wrapper_exposes_main(self) -> None:
        wrapper = REPO_ROOT / "scripts" / "verify" / "runtime_neutral" / "bio_science_pack_consolidation_audit.py"
        text = wrapper.read_text(encoding="utf-8")
        self.assertIn("from vgo_verify.bio_science_pack_consolidation_audit import", text)
        self.assertIn("raise SystemExit(main())", text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new test and confirm the expected failure**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
```

Expected: fail with `ModuleNotFoundError: No module named 'vgo_verify.bio_science_pack_consolidation_audit'`.

---

### Task 2: Implement The Problem-Map Audit

**Files:**
- Create: `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`
- Create: `scripts/verify/runtime_neutral/bio_science_pack_consolidation_audit.py`
- Create: `scripts/verify/vibe-bio-science-pack-consolidation-audit-gate.ps1`

- [ ] **Step 1: Create the audit module**

Create `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py` with this content:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROBLEM_MAP_CSV_FIELDS = [
    "skill_id",
    "problem_ids",
    "primary_problem_id",
    "current_role",
    "target_role",
    "target_owner",
    "overlap_with",
    "unique_assets",
    "routing_change",
    "delete_allowed_after_migration",
    "risk_level",
    "rationale",
]

BIO_SCIENCE_ROUTE_AUTHORITIES = [
    "scanpy",
    "pydeseq2",
    "pysam",
    "biopython",
    "gget",
    "esm",
    "cobrapy",
    "flowio",
    "arboreto",
    "geniml",
]

BIO_SCIENCE_STAGE_ASSISTANTS = [
    "anndata",
    "scvi-tools",
    "deeptools",
    "bioservices",
    "alphafold-database",
    "clinvar-database",
    "cosmic-database",
    "ensembl-database",
    "gene-database",
    "gwas-database",
    "kegg-database",
    "opentargets-database",
    "pdb-database",
    "reactome-database",
    "string-database",
    "cellxgene-census",
]

BIO_SCIENCE_PROBLEM_DECISIONS: dict[str, dict[str, Any]] = {
    "scanpy": {
        "problem_ids": ["single_cell_rnaseq"],
        "primary_problem_id": "single_cell_rnaseq",
        "target_role": "keep",
        "target_owner": "",
        "overlap_with": "anndata; scvi-tools; cellxgene-census; pydeseq2",
        "routing_change": "keep as route authority for single-cell RNA-seq clustering, annotation, marker genes, and h5ad/10X workflows",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Single-cell RNA-seq is a distinct high-value user problem and scanpy is the clearest owner.",
    },
    "pydeseq2": {
        "problem_ids": ["bulk_rnaseq_differential_expression"],
        "primary_problem_id": "bulk_rnaseq_differential_expression",
        "target_role": "keep",
        "target_owner": "",
        "overlap_with": "scanpy; statistical-analysis",
        "routing_change": "keep as route authority for bulk RNA-seq differential expression, DESeq2-style statistics, MA plots, and volcano plots",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Bulk RNA-seq differential expression must not be absorbed by scanpy or biopython.",
    },
    "pysam": {
        "problem_ids": ["alignment_variant_files"],
        "primary_problem_id": "alignment_variant_files",
        "target_role": "keep",
        "target_owner": "",
        "overlap_with": "biopython; tiledbvcf",
        "routing_change": "keep as route authority for BAM/SAM/CRAM/VCF parsing, pileup, coverage, and variant-file handling",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Alignment and variant files are concrete coding/research tasks with a dedicated Python owner.",
    },
    "biopython": {
        "problem_ids": ["sequence_io_entrez"],
        "primary_problem_id": "sequence_io_entrez",
        "target_role": "keep",
        "target_owner": "",
        "overlap_with": "gget; pysam; database assistants",
        "routing_change": "keep as planning/coding default only for sequence IO, FASTA, GenBank, SeqIO, Entrez, and sequence conversion",
        "delete_allowed_after_migration": False,
        "risk_level": "medium",
        "rationale": "Biopython is broad and useful, but negative routing boundaries must stop it from swallowing single-cell, DESeq2, BAM/VCF, ESM, COBRApy, and flow cytometry prompts.",
    },
    "gget": {
        "problem_ids": ["gene_symbol_lookup"],
        "primary_problem_id": "gene_symbol_lookup",
        "target_role": "keep",
        "target_owner": "",
        "overlap_with": "biopython; bioservices; ensembl-database; gene-database",
        "routing_change": "keep as route authority for quick gene, transcript, Ensembl, BLAST, and symbol lookup",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Quick lookup is a separate user intent from full single-cell or differential-expression workflows.",
    },
    "esm": {
        "problem_ids": ["protein_language_models"],
        "primary_problem_id": "protein_language_models",
        "target_role": "keep",
        "target_owner": "",
        "overlap_with": "alphafold-database; pdb-database; string-database",
        "routing_change": "keep as route authority for ESM, protein language models, and protein embeddings",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Protein embedding tasks are bio-ML tasks and should not be routed to generic sequence handling.",
    },
    "cobrapy": {
        "problem_ids": ["metabolic_flux_modeling"],
        "primary_problem_id": "metabolic_flux_modeling",
        "target_role": "keep",
        "target_owner": "",
        "overlap_with": "kegg-database; reactome-database; bioservices",
        "routing_change": "keep as route authority for COBRApy, FBA, flux balance, and constraint-based metabolic models",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Metabolic flux modeling is a problem owner, not a generic pathway lookup.",
    },
    "flowio": {
        "problem_ids": ["flow_cytometry_fcs_io"],
        "primary_problem_id": "flow_cytometry_fcs_io",
        "target_role": "keep",
        "target_owner": "",
        "overlap_with": "anndata",
        "routing_change": "keep as route authority for FCS and flow cytometry channel matrix handling",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "FCS/flow cytometry file IO is a specific task that should not fall back to biopython.",
    },
    "arboreto": {
        "problem_ids": ["gene_regulatory_networks"],
        "primary_problem_id": "gene_regulatory_networks",
        "target_role": "keep",
        "target_owner": "",
        "overlap_with": "scanpy; geniml",
        "routing_change": "keep as route authority for pySCENIC, GRN, gene regulatory network, and transcription-factor network tasks",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Gene regulatory network inference is distinct from ordinary single-cell clustering.",
    },
    "geniml": {
        "problem_ids": ["genomic_ml_embeddings"],
        "primary_problem_id": "genomic_ml_embeddings",
        "target_role": "keep",
        "target_owner": "",
        "overlap_with": "esm; data-ml",
        "routing_change": "keep as route authority for genomic ML and genome embedding tasks",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Genome embeddings are a bio-specific ML surface and need a precise owner.",
    },
    "anndata": {
        "problem_ids": ["single_cell_data_container"],
        "primary_problem_id": "single_cell_data_container",
        "target_role": "stage-assistant",
        "target_owner": "scanpy",
        "overlap_with": "scanpy; scvi-tools; cellxgene-census",
        "routing_change": "keep as stage assistant for AnnData/h5ad containers, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "AnnData is a data structure layer used inside single-cell workflows.",
    },
    "scvi-tools": {
        "problem_ids": ["single_cell_latent_models"],
        "primary_problem_id": "single_cell_latent_models",
        "target_role": "stage-assistant",
        "target_owner": "scanpy",
        "overlap_with": "scanpy; anndata",
        "routing_change": "keep as stage assistant for scVI-style modeling, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "medium",
        "rationale": "scVI is useful inside single-cell workflows but should not absorb broad single-cell prompts in the first split.",
    },
    "deeptools": {
        "problem_ids": ["genomics_track_processing"],
        "primary_problem_id": "genomics_track_processing",
        "target_role": "stage-assistant",
        "target_owner": "pysam",
        "overlap_with": "pysam",
        "routing_change": "keep as stage assistant for genomics signal/track processing, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "medium",
        "rationale": "deepTools is a genomics processing helper with a narrower route surface than pysam.",
    },
    "bioservices": {
        "problem_ids": ["cross_database_aggregation"],
        "primary_problem_id": "cross_database_aggregation",
        "target_role": "stage-assistant",
        "target_owner": "database-assistant",
        "overlap_with": "kegg-database; reactome-database; uniprot-like services",
        "routing_change": "keep as cross-database stage assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "medium",
        "rationale": "Cross-service lookup is valuable but must not override a more specific workflow owner.",
    },
    "alphafold-database": {
        "problem_ids": ["protein_structure_evidence"],
        "primary_problem_id": "protein_structure_evidence",
        "target_role": "stage-assistant",
        "target_owner": "esm",
        "overlap_with": "pdb-database; esm",
        "routing_change": "keep as evidence assistant for predicted protein structures, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Structure evidence supports protein workflows but does not own the main task.",
    },
    "clinvar-database": {
        "problem_ids": ["variant_clinical_evidence"],
        "primary_problem_id": "variant_clinical_evidence",
        "target_role": "stage-assistant",
        "target_owner": "pysam",
        "overlap_with": "cosmic-database; gwas-database",
        "routing_change": "keep as clinical variant evidence assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "ClinVar lookup is evidence retrieval inside a variant interpretation workflow.",
    },
    "cosmic-database": {
        "problem_ids": ["cancer_variant_evidence"],
        "primary_problem_id": "cancer_variant_evidence",
        "target_role": "stage-assistant",
        "target_owner": "pysam",
        "overlap_with": "clinvar-database; gwas-database",
        "routing_change": "keep as cancer variant evidence assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "COSMIC is supporting evidence for cancer variant work.",
    },
    "ensembl-database": {
        "problem_ids": ["ensembl_annotation_evidence"],
        "primary_problem_id": "ensembl_annotation_evidence",
        "target_role": "stage-assistant",
        "target_owner": "gget",
        "overlap_with": "gget; gene-database",
        "routing_change": "keep as Ensembl evidence assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Ensembl lookup should support gget and sequence workflows.",
    },
    "gene-database": {
        "problem_ids": ["gene_annotation_evidence"],
        "primary_problem_id": "gene_annotation_evidence",
        "target_role": "stage-assistant",
        "target_owner": "gget",
        "overlap_with": "ensembl-database; opentargets-database",
        "routing_change": "keep as gene evidence assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Gene lookup supports annotation but should not own whole workflows.",
    },
    "gwas-database": {
        "problem_ids": ["gwas_trait_evidence"],
        "primary_problem_id": "gwas_trait_evidence",
        "target_role": "stage-assistant",
        "target_owner": "gget",
        "overlap_with": "clinvar-database; opentargets-database",
        "routing_change": "keep as GWAS evidence assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "GWAS evidence is supporting context for genetics workflows.",
    },
    "kegg-database": {
        "problem_ids": ["pathway_metabolism_evidence"],
        "primary_problem_id": "pathway_metabolism_evidence",
        "target_role": "stage-assistant",
        "target_owner": "cobrapy",
        "overlap_with": "reactome-database; bioservices",
        "routing_change": "keep as pathway evidence assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "KEGG is useful evidence for pathway and metabolism workflows.",
    },
    "opentargets-database": {
        "problem_ids": ["target_disease_evidence"],
        "primary_problem_id": "target_disease_evidence",
        "target_role": "stage-assistant",
        "target_owner": "gget",
        "overlap_with": "gene-database; gwas-database",
        "routing_change": "keep as target-disease evidence assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "OpenTargets supports target evidence, not the main computational workflow.",
    },
    "pdb-database": {
        "problem_ids": ["protein_structure_evidence"],
        "primary_problem_id": "protein_structure_evidence",
        "target_role": "stage-assistant",
        "target_owner": "esm",
        "overlap_with": "alphafold-database; string-database",
        "routing_change": "keep as protein structure evidence assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "PDB lookup supports structural interpretation but is not the primary route for protein embeddings.",
    },
    "reactome-database": {
        "problem_ids": ["pathway_evidence"],
        "primary_problem_id": "pathway_evidence",
        "target_role": "stage-assistant",
        "target_owner": "cobrapy",
        "overlap_with": "kegg-database; bioservices",
        "routing_change": "keep as pathway evidence assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Reactome supports pathway interpretation inside larger workflows.",
    },
    "string-database": {
        "problem_ids": ["protein_interaction_evidence"],
        "primary_problem_id": "protein_interaction_evidence",
        "target_role": "stage-assistant",
        "target_owner": "esm",
        "overlap_with": "pdb-database; alphafold-database",
        "routing_change": "keep as protein interaction evidence assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "STRING lookup is supporting evidence for protein workflows.",
    },
    "cellxgene-census": {
        "problem_ids": ["single_cell_reference_evidence"],
        "primary_problem_id": "single_cell_reference_evidence",
        "target_role": "stage-assistant",
        "target_owner": "scanpy",
        "overlap_with": "scanpy; anndata",
        "routing_change": "keep as single-cell reference evidence assistant, not a broad route authority",
        "delete_allowed_after_migration": False,
        "risk_level": "low",
        "rationale": "Cellxgene Census supports single-cell reference lookup inside scanpy workflows.",
    },
}


@dataclass(frozen=True)
class ProblemMapRow:
    skill_id: str
    problem_ids: str
    primary_problem_id: str
    current_role: str
    target_role: str
    target_owner: str
    overlap_with: str
    unique_assets: str
    routing_change: str
    delete_allowed_after_migration: bool
    risk_level: str
    rationale: str


@dataclass(frozen=True)
class ProblemMapArtifact:
    generated_at: str
    repo_root: str
    rows: list[ProblemMapRow]

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "repo_root": self.repo_root,
            "summary": {
                "bio_science_skill_count": len(self.rows),
                "target_route_authority_count": sum(1 for row in self.rows if row.target_role == "keep"),
                "target_stage_assistant_count": sum(1 for row in self.rows if row.target_role == "stage-assistant"),
                "target_manual_review_count": sum(1 for row in self.rows if row.target_role == "manual-review"),
                "target_merge_delete_count": sum(1 for row in self.rows if row.target_role == "merge-delete-after-migration"),
            },
            "target_route_authority_candidates": BIO_SCIENCE_ROUTE_AUTHORITIES,
            "target_stage_assistant_candidates": BIO_SCIENCE_STAGE_ASSISTANTS,
            "rows": [asdict(row) for row in self.rows],
        }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _bio_science_pack(pack_manifest: dict[str, Any]) -> dict[str, Any]:
    for pack in _as_list(pack_manifest.get("packs")):
        if isinstance(pack, dict) and str(pack.get("id", "")).strip() == "bio-science":
            return pack
    return {}


def _pack_index(pack_manifest: dict[str, Any]) -> dict[str, dict[str, set[str]]]:
    index: dict[str, dict[str, set[str]]] = {}
    for pack in _as_list(pack_manifest.get("packs")):
        if not isinstance(pack, dict):
            continue
        pack_id = str(pack.get("id", "")).strip()
        if not pack_id:
            continue
        for role_key in ("skill_candidates", "route_authority_candidates", "stage_assistant_candidates"):
            for value in _as_list(pack.get(role_key)):
                skill_id = str(value).strip()
                if not skill_id:
                    continue
                record = index.setdefault(skill_id, {"packs": set(), "route_authority": set(), "stage_assistant": set(), "defaults": set()})
                record["packs"].add(pack_id)
                if role_key == "route_authority_candidates":
                    record["route_authority"].add(pack_id)
                if role_key == "stage_assistant_candidates":
                    record["stage_assistant"].add(pack_id)
        defaults_by_task = pack.get("defaults_by_task")
        if isinstance(defaults_by_task, dict):
            for value in defaults_by_task.values():
                skill_id = str(value).strip()
                if not skill_id:
                    continue
                record = index.setdefault(skill_id, {"packs": set(), "route_authority": set(), "stage_assistant": set(), "defaults": set()})
                record["packs"].add(pack_id)
                record["defaults"].add(pack_id)
    return index


def _current_role(record: dict[str, set[str]]) -> str:
    if record["route_authority"]:
        return "route_authority"
    if record["stage_assistant"]:
        return "stage_assistant"
    if record["defaults"]:
        return "default"
    return "candidate"


def _file_count(directory: Path) -> int:
    if not directory.is_dir():
        return 0
    return sum(1 for item in directory.rglob("*") if item.is_file())


def _asset_summary(skill_dir: Path) -> str:
    return "; ".join(
        [
            f"scripts={_file_count(skill_dir / 'scripts')}",
            f"references={_file_count(skill_dir / 'references')}",
            f"assets={_file_count(skill_dir / 'assets')}",
        ]
    )


def _decision_for(skill_id: str) -> dict[str, Any]:
    return BIO_SCIENCE_PROBLEM_DECISIONS.get(
        skill_id,
        {
            "problem_ids": ["manual_review"],
            "primary_problem_id": "manual_review",
            "target_role": "manual-review",
            "target_owner": "",
            "overlap_with": "",
            "routing_change": "manual review required before changing bio-science membership",
            "delete_allowed_after_migration": False,
            "risk_level": "high",
            "rationale": "Skill is not registered in the bio-science problem decision table.",
        },
    )


def audit_bio_science_problem_map(repo_root: Path) -> ProblemMapArtifact:
    repo_root = repo_root.resolve()
    pack_manifest = _read_json(repo_root / "config" / "pack-manifest.json")
    pack_index = _pack_index(pack_manifest)
    bio_pack = _bio_science_pack(pack_manifest)
    candidates = [str(item).strip() for item in _as_list(bio_pack.get("skill_candidates")) if str(item).strip()]
    skill_ids = list(dict.fromkeys(candidates + list(BIO_SCIENCE_PROBLEM_DECISIONS)))
    rows: list[ProblemMapRow] = []

    for skill_id in skill_ids:
        record = pack_index.get(skill_id, {"packs": set(), "route_authority": set(), "stage_assistant": set(), "defaults": set()})
        decision = _decision_for(skill_id)
        skill_dir = repo_root / "bundled" / "skills" / skill_id
        rows.append(
            ProblemMapRow(
                skill_id=skill_id,
                problem_ids="; ".join(_as_list(decision.get("problem_ids"))),
                primary_problem_id=str(decision.get("primary_problem_id", "")),
                current_role=_current_role(record),
                target_role=str(decision.get("target_role", "manual-review")),
                target_owner=str(decision.get("target_owner", "")),
                overlap_with=str(decision.get("overlap_with", "")),
                unique_assets=_asset_summary(skill_dir),
                routing_change=str(decision.get("routing_change", "")),
                delete_allowed_after_migration=bool(decision.get("delete_allowed_after_migration", False)),
                risk_level=str(decision.get("risk_level", "high")),
                rationale=str(decision.get("rationale", "")),
            )
        )
    return ProblemMapArtifact(generated_at=datetime.now(timezone.utc).isoformat(), repo_root=str(repo_root), rows=rows)


def _markdown_table(rows: list[ProblemMapRow], fields: list[str]) -> list[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join(["---"] * len(fields)) + " |"]
    for row in rows:
        data = asdict(row)
        values = [str(data[field]).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return lines


def _write_problem_markdown(path: Path, artifact: ProblemMapArtifact) -> None:
    route_rows = [row for row in artifact.rows if row.target_role == "keep"]
    stage_rows = [row for row in artifact.rows if row.target_role == "stage-assistant"]
    manual_rows = [row for row in artifact.rows if row.target_role == "manual-review"]
    merge_rows = [row for row in artifact.rows if row.target_role == "merge-delete-after-migration"]
    lines: list[str] = [
        "# Bio-Science Problem-First Consolidation",
        "",
        f"- Generated At: `{artifact.generated_at}`",
        f"- Current Bio-Science Skills: {len(artifact.rows)}",
        f"- Target Route Authorities: {len(route_rows)}",
        f"- Target Stage Assistants: {len(stage_rows)}",
        f"- Manual Review: {len(manual_rows)}",
        f"- Merge/Delete After Migration: {len(merge_rows)}",
        "",
        "## Route Authorities",
        "",
    ]
    lines.extend(_markdown_table(route_rows, ["skill_id", "primary_problem_id", "current_role", "overlap_with", "rationale"]))
    lines.extend(["", "## Stage Assistants", ""])
    lines.extend(_markdown_table(stage_rows, ["skill_id", "primary_problem_id", "target_owner", "unique_assets", "rationale"]))
    lines.extend(["", "## Manual Review", ""])
    if manual_rows:
        lines.extend(_markdown_table(manual_rows, ["skill_id", "primary_problem_id", "unique_assets", "rationale"]))
    else:
        lines.append("- none")
    lines.extend(["", "## Merge/Delete After Migration", ""])
    if merge_rows:
        lines.extend(_markdown_table(merge_rows, ["skill_id", "target_owner", "unique_assets", "rationale"]))
    else:
        lines.append("- none")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_bio_science_problem_artifacts(
    repo_root: Path,
    artifact: ProblemMapArtifact,
    output_dir: Path | None = None,
) -> dict[str, Path]:
    repo_root = repo_root.resolve()
    output_dir = output_dir or repo_root / "outputs" / "skills-audit"
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "bio-science-problem-map.json"
    csv_path = output_dir / "bio-science-problem-map.csv"
    markdown_path = output_dir / "bio-science-problem-consolidation.md"

    json_path.write_text(json.dumps(artifact.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROBLEM_MAP_CSV_FIELDS)
        writer.writeheader()
        for row in artifact.rows:
            writer.writerow(asdict(row))
    _write_problem_markdown(markdown_path, artifact)
    return {"json": json_path, "csv": csv_path, "markdown": markdown_path}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit bio-science pack problem ownership before consolidation.")
    parser.add_argument("--repo-root", help="Optional repository root. Defaults to the current working directory.")
    parser.add_argument("--write-artifacts", action="store_true", help="Write JSON/CSV/Markdown artifacts.")
    parser.add_argument("--output-directory", help="Optional output directory for artifacts.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path.cwd().resolve()
    artifact = audit_bio_science_problem_map(repo_root)
    if args.write_artifacts:
        output_dir = Path(args.output_directory).resolve() if args.output_directory else None
        write_bio_science_problem_artifacts(repo_root, artifact, output_dir)
    print(json.dumps(artifact.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Create the runtime-neutral wrapper**

Create `scripts/verify/runtime_neutral/bio_science_pack_consolidation_audit.py` with this content:

```python
from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
VERIFICATION_CORE_SRC = REPO_ROOT / "packages" / "verification-core" / "src"
if str(VERIFICATION_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(VERIFICATION_CORE_SRC))

from vgo_verify.bio_science_pack_consolidation_audit import main


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 3: Create the PowerShell audit gate**

Create `scripts/verify/vibe-bio-science-pack-consolidation-audit-gate.ps1` with this content:

```powershell
[CmdletBinding()]
param(
    [string]$RepoRoot,
    [switch]$WriteArtifacts,
    [string]$OutputDirectory
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
} else {
    $RepoRoot = (Resolve-Path $RepoRoot).Path
}

$runnerPath = Join-Path $RepoRoot 'scripts/verify/runtime_neutral/bio_science_pack_consolidation_audit.py'
if (-not (Test-Path -LiteralPath $runnerPath)) {
    throw "Bio-science pack consolidation audit runner missing: $runnerPath"
}

. (Join-Path $RepoRoot 'scripts/common/vibe-governance-helpers.ps1')
$pythonInvocation = Get-VgoPythonCommand

$runnerArgs = @(
    $runnerPath,
    '--repo-root', $RepoRoot
)
if ($WriteArtifacts) {
    $runnerArgs += '--write-artifacts'
}
if ($OutputDirectory) {
    $runnerArgs += @('--output-directory', $OutputDirectory)
}

& $pythonInvocation.host_path @($pythonInvocation.prefix_arguments) @runnerArgs
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    throw "vibe-bio-science-pack-consolidation-audit-gate failed with exit code $exitCode"
}

Write-Host '[PASS] vibe-bio-science-pack-consolidation-audit-gate passed' -ForegroundColor Green
```

- [ ] **Step 4: Run the focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
```

Expected: pass once the module, wrapper, and gate exist.

- [ ] **Step 5: Commit the audit foundation**

Run:

```powershell
git add packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py scripts/verify/runtime_neutral/bio_science_pack_consolidation_audit.py scripts/verify/vibe-bio-science-pack-consolidation-audit-gate.ps1 tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py
git commit -m "test: add bio-science pack consolidation audit"
```

---

### Task 3: Add Live Manifest Role-Split Assertion

**Files:**
- Modify: `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`
- Implementation target: `config/pack-manifest.json`

- [ ] **Step 1: Add the live manifest assertion**

Add this test method before `test_runtime_neutral_wrapper_exposes_main()`:

```python
    def test_real_bio_science_pack_has_target_role_split(self) -> None:
        manifest = json.loads((REPO_ROOT / "config" / "pack-manifest.json").read_text(encoding="utf-8-sig"))
        bio_pack = next(pack for pack in manifest["packs"] if pack["id"] == "bio-science")

        self.assertEqual(BIO_SCIENCE_CANDIDATES, bio_pack["skill_candidates"])
        self.assertEqual(BIO_SCIENCE_ROUTE_AUTHORITIES, bio_pack["route_authority_candidates"])
        self.assertEqual(BIO_SCIENCE_STAGE_ASSISTANTS, bio_pack["stage_assistant_candidates"])
        self.assertEqual(
            {
                "planning": "biopython",
                "coding": "biopython",
                "research": "scanpy",
            },
            bio_pack["defaults_by_task"],
        )
```

- [ ] **Step 2: Run the test and confirm the expected failure**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py::BioSciencePackConsolidationAuditTests::test_real_bio_science_pack_has_target_role_split -q
```

Expected: fail because `bio-science.route_authority_candidates` and `bio-science.stage_assistant_candidates` are not present yet.

---

### Task 4: Split The Bio-Science Pack Roles

**Files:**
- Modify: `config/pack-manifest.json`

- [ ] **Step 1: Keep the candidate list unchanged**

Confirm `bio-science.skill_candidates` remains exactly:

```json
[
  "alphafold-database",
  "anndata",
  "biopython",
  "bioservices",
  "cellxgene-census",
  "clinvar-database",
  "cosmic-database",
  "deeptools",
  "ensembl-database",
  "gene-database",
  "gget",
  "gwas-database",
  "kegg-database",
  "opentargets-database",
  "pdb-database",
  "pydeseq2",
  "pysam",
  "reactome-database",
  "scanpy",
  "scvi-tools",
  "arboreto",
  "cobrapy",
  "esm",
  "flowio",
  "geniml",
  "string-database"
]
```

- [ ] **Step 2: Add `route_authority_candidates`**

Add this property to the `bio-science` pack:

```json
"route_authority_candidates": [
  "scanpy",
  "pydeseq2",
  "pysam",
  "biopython",
  "gget",
  "esm",
  "cobrapy",
  "flowio",
  "arboreto",
  "geniml"
]
```

- [ ] **Step 3: Add `stage_assistant_candidates`**

Add this property to the `bio-science` pack:

```json
"stage_assistant_candidates": [
  "anndata",
  "scvi-tools",
  "deeptools",
  "bioservices",
  "alphafold-database",
  "clinvar-database",
  "cosmic-database",
  "ensembl-database",
  "gene-database",
  "gwas-database",
  "kegg-database",
  "opentargets-database",
  "pdb-database",
  "reactome-database",
  "string-database",
  "cellxgene-census"
]
```

- [ ] **Step 4: Keep defaults unchanged**

Confirm `defaults_by_task` remains:

```json
{
  "planning": "biopython",
  "coding": "biopython",
  "research": "scanpy"
}
```

- [ ] **Step 5: Run the live manifest assertion**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py::BioSciencePackConsolidationAuditTests::test_real_bio_science_pack_has_target_role_split -q
```

Expected: pass.

- [ ] **Step 6: Run the full audit test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
```

Expected: pass.

- [ ] **Step 7: Commit the manifest role split**

Run:

```powershell
git add config/pack-manifest.json tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py
git commit -m "feat: split bio-science pack routing roles"
```

---

### Task 5: Tighten Keywords And Routing Boundaries

**Files:**
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`

- [ ] **Step 1: Update keyword index entries for route authorities**

Ensure these keyword index entries exist:

```json
{
  "scanpy": {
    "keywords": ["scanpy", "single-cell", "single-cell clustering", "scRNA", "h5ad", "10x", "leiden", "marker genes", "单细胞聚类", "细胞注释", "marker基因"]
  },
  "pydeseq2": {
    "keywords": ["pydeseq2", "deseq2", "bulk RNA-seq", "differential expression", "volcano plot", "MA plot", "padj", "差异表达", "差异表达分析", "de分析", "rna-seq差异"]
  },
  "pysam": {
    "keywords": ["pysam", "bam", "sam", "cram", "vcf", "pileup", "coverage", "测序比对文件", "变异文件", "变异文件解析", "覆盖度"]
  },
  "biopython": {
    "keywords": ["biopython", "seqio", "fasta", "genbank", "entrez", "sequence conversion", "序列格式转换", "序列解析", "生物序列处理"]
  },
  "gget": {
    "keywords": ["gget", "Ensembl lookup", "gene symbol", "transcript lookup", "quick BLAST", "快速生信查询", "基因symbol", "Ensembl ID"]
  },
  "esm": {
    "keywords": ["esm", "protein language model", "protein embedding", "protein embeddings", "protein lm", "蛋白语言模型", "蛋白嵌入"]
  },
  "cobrapy": {
    "keywords": ["cobrapy", "COBRApy", "fba", "flux balance", "metabolic model", "constraint-based metabolic model", "代谢建模", "通量平衡"]
  },
  "flowio": {
    "keywords": ["flowio", "flow cytometry", "fcs", "cytometry", "channel matrix", "流式细胞", "FCS"]
  },
  "arboreto": {
    "keywords": ["arboreto", "pyscenic", "pySCENIC", "grn", "gene regulatory network", "transcription factor network", "基因调控网络", "转录因子网络"]
  },
  "geniml": {
    "keywords": ["geniml", "genomic ml", "genomic machine learning", "genome embedding", "基因组机器学习", "基因组嵌入"]
  },
  "bioservices": {
    "keywords": ["bioservices", "cross database", "uniprot", "kegg", "chembl", "多数据库", "跨数据库查询"]
  }
}
```

- [ ] **Step 2: Update routing rules for `scanpy`**

Set `scanpy` routing rules to:

```json
{
  "task_allow": ["research", "coding"],
  "positive_keywords": ["scanpy", "single-cell", "single cell", "scRNA", "h5ad", "10x", "leiden", "marker genes", "单细胞", "单细胞聚类", "细胞注释"],
  "negative_keywords": ["bulk RNA-seq", "DESeq2", "pydeseq2", "BAM", "SAM", "CRAM", "VCF", "pysam", "protein embedding", "ESM", "FBA", "COBRApy", "flow cytometry", "FCS", "RDKit", "SMILES", "PubMed", "BibTeX", "DICOM", "cover letter", "rebuttal"],
  "equivalent_group": null,
  "canonical_for_task": ["research"]
}
```

- [ ] **Step 3: Update routing rules for `pydeseq2`, `pysam`, `biopython`, and `gget`**

Use these rule payloads:

```json
{
  "pydeseq2": {
    "task_allow": ["research", "coding"],
    "positive_keywords": ["pydeseq2", "deseq2", "bulk RNA-seq", "differential expression", "volcano plot", "MA plot", "padj", "差异表达", "差异表达分析"],
    "negative_keywords": ["scanpy", "single-cell", "h5ad", "BAM", "VCF", "pysam", "ESM", "protein embedding", "COBRApy", "FBA", "flow cytometry", "RDKit", "SMILES", "PubMed", "DICOM"],
    "equivalent_group": null,
    "canonical_for_task": []
  },
  "pysam": {
    "task_allow": ["research", "coding"],
    "positive_keywords": ["pysam", "BAM", "SAM", "CRAM", "VCF", "pileup", "coverage", "变异文件", "覆盖度"],
    "negative_keywords": ["scanpy", "single-cell", "DESeq2", "volcano plot", "ESM", "protein embedding", "COBRApy", "FBA", "flow cytometry", "RDKit", "PubMed", "DICOM"],
    "equivalent_group": null,
    "canonical_for_task": []
  },
  "biopython": {
    "task_allow": ["planning", "coding", "research"],
    "positive_keywords": ["biopython", "SeqIO", "FASTA", "GenBank", "Entrez", "sequence conversion", "序列格式转换", "序列处理"],
    "negative_keywords": ["scanpy", "single-cell", "h5ad", "DESeq2", "pydeseq2", "BAM", "VCF", "pysam", "ESM", "protein embedding", "FBA", "COBRApy", "flow cytometry", "FCS", "RDKit", "SMILES", "PubMed", "BibTeX", "DICOM", "cover letter", "rebuttal"],
    "equivalent_group": null,
    "canonical_for_task": ["planning", "coding"]
  },
  "gget": {
    "task_allow": ["research", "coding"],
    "positive_keywords": ["gget", "Ensembl lookup", "gene symbol", "transcript lookup", "quick BLAST", "快速生信查询", "Ensembl ID"],
    "negative_keywords": ["scanpy", "single-cell", "h5ad", "DESeq2", "pydeseq2", "bulk RNA-seq", "BAM", "VCF", "pysam", "COBRApy", "FBA", "flow cytometry", "DICOM", "cover letter", "rebuttal"],
    "equivalent_group": null,
    "canonical_for_task": []
  }
}
```

- [ ] **Step 4: Update routing rules for `esm`, `cobrapy`, `flowio`, `arboreto`, and `geniml`**

Use these rule payloads:

```json
{
  "esm": {
    "task_allow": ["coding", "research"],
    "positive_keywords": ["ESM", "esm", "protein language model", "protein embedding", "protein embeddings", "protein lm", "蛋白语言模型", "蛋白嵌入"],
    "negative_keywords": ["scanpy", "single-cell", "DESeq2", "BAM", "VCF", "COBRApy", "FBA", "flow cytometry", "RDKit", "SMILES", "DICOM", "PubMed", "patent"],
    "equivalent_group": "bio-ml",
    "canonical_for_task": ["coding"]
  },
  "cobrapy": {
    "task_allow": ["coding", "research"],
    "positive_keywords": ["COBRApy", "cobrapy", "FBA", "flux balance", "metabolic model", "constraint-based metabolic model", "代谢建模", "通量平衡"],
    "negative_keywords": ["scanpy", "single-cell", "DESeq2", "BAM", "VCF", "ESM", "protein embedding", "flow cytometry", "RDKit", "SMILES", "DICOM", "PubMed", "patent"],
    "equivalent_group": "bio-systems",
    "canonical_for_task": ["coding"]
  },
  "flowio": {
    "task_allow": ["coding", "research"],
    "positive_keywords": ["flowio", "flow cytometry", "FCS", "fcs", "cytometry", "channel matrix", "流式细胞"],
    "negative_keywords": ["scanpy", "single-cell", "DESeq2", "BAM", "VCF", "ESM", "protein embedding", "COBRApy", "FBA", "RDKit", "DICOM", "patent"],
    "equivalent_group": "bio-data-io",
    "canonical_for_task": ["coding"]
  },
  "arboreto": {
    "task_allow": ["coding", "research"],
    "positive_keywords": ["arboreto", "pySCENIC", "pyscenic", "GRN", "gene regulatory network", "transcription factor network", "基因调控网络", "转录因子网络"],
    "negative_keywords": ["bulk RNA-seq", "DESeq2", "BAM", "VCF", "ESM", "protein embedding", "COBRApy", "FBA", "flow cytometry", "RDKit", "DICOM", "patent"],
    "equivalent_group": "bio-systems",
    "canonical_for_task": ["coding"]
  },
  "geniml": {
    "task_allow": ["coding", "research"],
    "positive_keywords": ["geniml", "genomic ML", "genomic machine learning", "genome embedding", "基因组机器学习", "基因组嵌入"],
    "negative_keywords": ["scanpy", "single-cell", "DESeq2", "BAM", "VCF", "ESM", "protein embedding", "COBRApy", "FBA", "flow cytometry", "RDKit", "DICOM", "patent"],
    "equivalent_group": "bio-ml",
    "canonical_for_task": ["coding"]
  }
}
```

- [ ] **Step 5: Keep database assistants stage-only**

Do not add database assistants to `bio-science.route_authority_candidates`. Existing routing-rule entries for database helpers may remain for explicit lookup support, but they must not be broad canonical defaults for `planning`, `coding`, or `research` in the `bio-science` pack.

- [ ] **Step 6: Run a focused config sanity check**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
```

Expected: pass.

- [ ] **Step 7: Commit keyword and rule boundaries**

Run:

```powershell
git add config/skill-keyword-index.json config/skill-routing-rules.json tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py
git commit -m "fix: tighten bio-science routing boundaries"
```

---

### Task 6: Add Route Regression Probes

**Files:**
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
- Modify: `scripts/verify/probe-scientific-packs.ps1`

- [ ] **Step 1: Extend `vibe-skill-index-routing-audit.ps1` positive bio-science cases**

Add or update these cases in `$cases`:

```powershell
[pscustomobject]@{ Name = "scanpy single-cell"; Prompt = "做单细胞RNA-seq聚类与注释，使用scanpy"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "scanpy" },
[pscustomobject]@{ Name = "scanpy h5ad marker genes"; Prompt = "读取h5ad，做Leiden clustering和marker genes"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "scanpy" },
[pscustomobject]@{ Name = "pydeseq2 bulk de"; Prompt = "进行bulk RNA-seq差异表达分析并画volcano plot"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "pydeseq2" },
[pscustomobject]@{ Name = "pysam bam vcf coverage"; Prompt = "解析BAM和VCF文件并统计覆盖度"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "pysam" },
[pscustomobject]@{ Name = "biopython fasta genbank"; Prompt = "用BioPython处理FASTA序列并转换GenBank格式"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "biopython" },
[pscustomobject]@{ Name = "gget gene symbol"; Prompt = "用gget快速查询基因symbol和Ensembl ID"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "gget" },
[pscustomobject]@{ Name = "esm protein embeddings"; Prompt = "用ESM生成protein embeddings"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "esm" },
[pscustomobject]@{ Name = "cobrapy fba"; Prompt = "用COBRApy做FBA代谢通量分析"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "cobrapy" },
[pscustomobject]@{ Name = "flowio fcs"; Prompt = "读取FCS流式细胞文件并提取通道矩阵"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "flowio" },
[pscustomobject]@{ Name = "arboreto grn"; Prompt = "用pySCENIC/arboreto推断基因调控网络"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "arboreto" },
[pscustomobject]@{ Name = "geniml genome embedding"; Prompt = "用geniml做基因组机器学习和genome embedding"; Grade = "L"; TaskType = "research"; ExpectedPack = "bio-science"; ExpectedSkill = "geniml" },
```

- [ ] **Step 2: Extend `vibe-skill-index-routing-audit.ps1` false-positive cases**

Add these cross-pack expectations:

```powershell
[pscustomobject]@{ Name = "rdkit smiles not bio"; Prompt = "用RDKit解析SMILES并计算Morgan fingerprint"; Grade = "L"; TaskType = "research"; ExpectedPack = "science-chem-drug"; ExpectedSkill = "rdkit" },
[pscustomobject]@{ Name = "pubmed bibtex not bio"; Prompt = "在PubMed检索文献并导出BibTeX"; Grade = "L"; TaskType = "research"; ExpectedPack = "science-literature-citations"; ExpectedSkill = "pubmed-database" },
[pscustomobject]@{ Name = "submission rebuttal not bio"; Prompt = "写论文投稿cover letter和rebuttal matrix"; Grade = "L"; TaskType = "planning"; ExpectedPack = "scholarly-publishing-workflow"; ExpectedSkill = "submission-checklist" },
[pscustomobject]@{ Name = "sklearn cross validation not bio"; Prompt = "用scikit-learn训练分类模型并交叉验证"; Grade = "L"; TaskType = "research"; ExpectedPack = "data-ml"; ExpectedSkill = "scikit-learn" },
[pscustomobject]@{ Name = "dicom tags not bio"; Prompt = "读取DICOM并提取tags"; Grade = "L"; TaskType = "research"; ExpectedPack = "science-medical-imaging"; ExpectedSkill = "pydicom" },
```

- [ ] **Step 3: Extend `probe-scientific-packs.ps1` bio-science cases**

In the existing `# bio-science extensions` block, keep `bio_esm_embeddings` and `bio_cobrapy_fba`, then add:

```powershell
[pscustomobject]@{
    name = "bio_scanpy_h5ad_marker_genes"
    group = "bio-science"
    prompt = "/vibe 读取 h5ad，做 Leiden clustering 和 marker genes"
    grade = "M"
    task_type = "research"
    expected_pack = "bio-science"
    expected_skill = "scanpy"
    requested_skill = $null
},
[pscustomobject]@{
    name = "bio_pydeseq2_bulk_de"
    group = "bio-science"
    prompt = "/vibe 进行 bulk RNA-seq 差异表达分析并画 volcano plot"
    grade = "M"
    task_type = "research"
    expected_pack = "bio-science"
    expected_skill = "pydeseq2"
    requested_skill = $null
},
[pscustomobject]@{
    name = "bio_pysam_bam_vcf_coverage"
    group = "bio-science"
    prompt = "/vibe 解析 BAM 和 VCF 文件并统计 coverage"
    grade = "M"
    task_type = "research"
    expected_pack = "bio-science"
    expected_skill = "pysam"
    requested_skill = $null
},
[pscustomobject]@{
    name = "bio_gget_gene_symbol"
    group = "bio-science"
    prompt = "/vibe 用 gget 快速查询 gene symbol 和 Ensembl ID"
    grade = "M"
    task_type = "research"
    expected_pack = "bio-science"
    expected_skill = "gget"
    requested_skill = $null
},
[pscustomobject]@{
    name = "bio_flowio_fcs"
    group = "bio-science"
    prompt = "/vibe 读取 FCS 流式细胞文件并提取通道矩阵"
    grade = "M"
    task_type = "coding"
    expected_pack = "bio-science"
    expected_skill = "flowio"
    requested_skill = $null
},
[pscustomobject]@{
    name = "bio_arboreto_grn"
    group = "bio-science"
    prompt = "/vibe 用 pySCENIC 和 arboreto 推断 gene regulatory network"
    grade = "M"
    task_type = "research"
    expected_pack = "bio-science"
    expected_skill = "arboreto"
    requested_skill = $null
},
[pscustomobject]@{
    name = "bio_geniml_embedding"
    group = "bio-science"
    prompt = "/vibe 用 geniml 做 genomic ML 和 genome embedding"
    grade = "M"
    task_type = "research"
    expected_pack = "bio-science"
    expected_skill = "geniml"
    requested_skill = $null
}
```

- [ ] **Step 4: Run the skill-index route audit**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected: pass for all assertions, including the new bio-science route-owner probes and false-positive probes.

- [ ] **Step 5: Run the scientific probe matrix**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify\probe-scientific-packs.ps1 -Unattended
```

Expected: pass and write scientific probe artifacts under `outputs/verify/route-probe-scientific`.

- [ ] **Step 6: Commit route probes**

Run:

```powershell
git add scripts/verify/vibe-skill-index-routing-audit.ps1 scripts/verify/probe-scientific-packs.ps1
git commit -m "test: cover bio-science route ownership"
```

---

### Task 7: Generate Artifacts And Governance Note

**Files:**
- Create generated: `outputs/skills-audit/bio-science-problem-map.json`
- Create generated: `outputs/skills-audit/bio-science-problem-map.csv`
- Create generated: `outputs/skills-audit/bio-science-problem-consolidation.md`
- Create: `docs/governance/bio-science-problem-first-consolidation-2026-04-28.md`

- [ ] **Step 1: Run the audit gate with artifacts**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-bio-science-pack-consolidation-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs\skills-audit
```

Expected: prints `[PASS] vibe-bio-science-pack-consolidation-audit-gate passed` and writes the three `bio-science-*` audit artifacts.

- [ ] **Step 2: Create the governance note**

Create `docs/governance/bio-science-problem-first-consolidation-2026-04-28.md` with this content:

```markdown
# Bio-Science Problem-First Consolidation

Date: 2026-04-28

## Summary

This pass governs only the `bio-science` pack.

The pack keeps all 26 physical skill directories, but changes the routing contract from a flat candidate list into explicit route authorities and stage assistants.

| field | before | after |
| --- | ---: | ---: |
| `skill_candidates` | 26 | 26 |
| `route_authority_candidates` | 0 | 10 |
| `stage_assistant_candidates` | 0 | 16 |
| physical directory deletion | 0 | 0 |

Physical deletion is deferred because every candidate either owns a distinct problem or has database, reference, script, or asset value that needs a migration review before removal.

## Route Authorities

| user problem | owner |
| --- | --- |
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

## Stage Assistants

| assistant | target owner | why stage-only |
| --- | --- | --- |
| `anndata` | `scanpy` | AnnData/h5ad is a data container inside single-cell workflows. |
| `scvi-tools` | `scanpy` | scVI modeling is useful but should not own broad single-cell prompts in this split. |
| `deeptools` | `pysam` | Genomics track processing is narrower than alignment/variant file handling. |
| `bioservices` | database assistants | Cross-database lookup should not override a specific workflow owner. |
| `alphafold-database` | `esm` | Predicted structure evidence supports protein workflows. |
| `clinvar-database` | `pysam` | Clinical variant evidence supports variant interpretation. |
| `cosmic-database` | `pysam` | Cancer variant evidence supports variant interpretation. |
| `ensembl-database` | `gget` | Ensembl evidence supports quick gene/transcript lookup. |
| `gene-database` | `gget` | Gene annotation evidence supports lookup and annotation workflows. |
| `gwas-database` | `gget` | Trait evidence supports genetics workflows. |
| `kegg-database` | `cobrapy` | KEGG evidence supports metabolism and pathway workflows. |
| `opentargets-database` | `gget` | Target-disease evidence supports gene/target workflows. |
| `pdb-database` | `esm` | Protein structure evidence supports protein workflows. |
| `reactome-database` | `cobrapy` | Pathway evidence supports metabolism and pathway interpretation. |
| `string-database` | `esm` | Protein interaction evidence supports protein workflows. |
| `cellxgene-census` | `scanpy` | Single-cell reference evidence supports scanpy workflows. |

## Protected Route Probes

| prompt | expected |
| --- | --- |
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
| `用geniml做基因组机器学习和genome embedding` | `bio-science / geniml` |

## False-Positive Protection

| prompt | expected |
| --- | --- |
| `用RDKit解析SMILES并计算Morgan fingerprint` | `science-chem-drug / rdkit` |
| `在PubMed检索文献并导出BibTeX` | `science-literature-citations / pubmed-database` |
| `写论文投稿cover letter和rebuttal matrix` | `scholarly-publishing-workflow / submission-checklist` |
| `用scikit-learn训练分类模型并交叉验证` | `data-ml / scikit-learn` |
| `读取DICOM并提取tags` | `science-medical-imaging / pydicom` |

## Audit Artifacts

The problem-map gate writes:

```text
outputs/skills-audit/bio-science-problem-map.json
outputs/skills-audit/bio-science-problem-map.csv
outputs/skills-audit/bio-science-problem-consolidation.md
```

Expected audit summary:

| category | count |
| --- | ---: |
| route authorities | 10 |
| stage assistants | 16 |
| manual review | 0 |
| merge/delete after migration | 0 |

## Deletion Boundary

This pass performs routing and config cleanup only.

No physical skill directory is deleted in this pass. A future deletion pass must prove all of the following before removing any directory:

1. The skill has no distinct user problem after problem-map review.
2. Useful references, scripts, examples, and assets have been migrated or intentionally rejected.
3. No live route, profile, test, lockfile, or packaging surface depends on the directory.
4. Offline skills, config parity, and route regression gates pass after removal.

## Verification

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-bio-science-pack-consolidation-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs\skills-audit
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\probe-scientific-packs.ps1 -Unattended
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-generate-skills-lock.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
```

Report any unrelated pre-existing route or metadata failures separately from this pack.
```

- [ ] **Step 3: Commit artifacts and governance note**

Run:

```powershell
git add outputs/skills-audit/bio-science-problem-map.json outputs/skills-audit/bio-science-problem-map.csv outputs/skills-audit/bio-science-problem-consolidation.md docs/governance/bio-science-problem-first-consolidation-2026-04-28.md
git commit -m "docs: record bio-science pack consolidation"
```

---

### Task 8: Refresh Lockfile And Run Final Gates

**Files:**
- Modify generated: `config/skills-lock.json`

- [ ] **Step 1: Refresh `skills-lock.json`**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected: exit code `0`. If `config/skills-lock.json` changes, keep the generated diff.

- [ ] **Step 2: Run focused and broad verification**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-bio-science-pack-consolidation-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs\skills-audit
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\probe-scientific-packs.ps1 -Unattended
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
```

Expected: all bio-science-specific assertions pass. Any unrelated pre-existing failure must be copied into the final report with the failing command and failure count.

- [ ] **Step 3: Commit lockfile and final generated changes**

Run:

```powershell
git add config/skills-lock.json outputs/skills-audit/bio-science-problem-map.json outputs/skills-audit/bio-science-problem-map.csv outputs/skills-audit/bio-science-problem-consolidation.md
git commit -m "chore: refresh bio-science consolidation artifacts"
```

- [ ] **Step 4: Report implementation evidence**

The final implementation report must include:

```text
branch
commit hash
before/after counts
kept route authorities
stage assistants
moved-out skills: none
merge/delete-after-migration skills: none in this pass
physical directory deletion: deferred
verification commands and pass/fail counts
remaining caveats
```
