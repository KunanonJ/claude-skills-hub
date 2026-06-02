# Zero Route Authority Pack Consolidation Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the first five zero-route-authority packs use explicit direct route owners, with no stage assistants and with regression coverage for duplicate and misplaced skill boundaries.

**Architecture:** This is a routing-contract cleanup. The live behavior is driven by `config/pack-manifest.json`, `config/skill-keyword-index.json`, and `config/skill-routing-rules.json`; tests call `vgo_runtime.router_contract_runtime.route_prompt()` and the existing PowerShell route probes.

**Tech Stack:** Python unittest/pytest, PowerShell verification scripts, JSON routing config, Vibe-Skills bundled skill metadata.

---

## File Map

- Create `tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py`: focused manifest and route regression coverage for this cleanup.
- Modify `config/pack-manifest.json`: add direct route owners, remove duplicate/misplaced candidates, keep `stage_assistant_candidates` empty.
- Modify `config/skill-keyword-index.json`: add/narrow keywords for the direct owners and add Playwright keyword index coverage.
- Modify `config/skill-routing-rules.json`: add/narrow positive and negative routing rules for false-positive boundaries.
- Modify `scripts/verify/probe-scientific-packs.ps1`: add missing route probes for medical imaging, finance, geospatial, Zarr/Polars, and TileDB-VCF boundaries.
- Modify `scripts/verify/vibe-skill-index-routing-audit.ps1`: add representative skill-index route cases for the new direct owners.
- Modify `scripts/verify/vibe-pack-regression-matrix.ps1`: add broader regression matrix cases for the cleaned pack boundaries.
- Create `docs/governance/zero-route-authority-pack-consolidation-2026-04-29.md`: governance record for the pass.
- Modify `config/skills-lock.json`: refresh after config/docs/test changes are stable.

## Task 1: Focused RED Tests

**Files:**
- Create: `tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py`

- [ ] **Step 1: Write the focused manifest and routing tests**

Create `tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py` with this structure:

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


def route(prompt: str, task_type: str = "research", grade: str = "M") -> dict[str, object]:
    return route_prompt(prompt=prompt, grade=grade, task_type=task_type, repo_root=REPO_ROOT)


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


def load_pack(pack_id: str) -> dict[str, object]:
    manifest = json.loads((REPO_ROOT / "config" / "pack-manifest.json").read_text(encoding="utf-8-sig"))
    return next(pack for pack in manifest["packs"] if pack["id"] == pack_id)


class ZeroRouteAuthorityPackConsolidationTests(unittest.TestCase):
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

    def test_manifest_makes_medical_imaging_direct_owners(self) -> None:
        pack = load_pack("science-medical-imaging")
        expected = ["pydicom", "imaging-data-commons", "histolab", "omero-integration", "pathml"]
        self.assertEqual(expected, pack["skill_candidates"])
        self.assertEqual(expected, pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])

    def test_manifest_makes_finance_direct_owners(self) -> None:
        pack = load_pack("finance-edgar-macro")
        expected = [
            "edgartools",
            "alpha-vantage",
            "fred-economic-data",
            "usfiscaldata",
            "hedgefundmonitor",
            "market-research-reports",
            "datacommons-client",
        ]
        self.assertEqual(expected, pack["skill_candidates"])
        self.assertEqual(expected, pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])

    def test_manifest_removes_tiledbvcf_from_zarr_polars_and_assigns_single_owner(self) -> None:
        zarr_pack = load_pack("science-zarr-polars")
        tiledb_pack = load_pack("science-tiledbvcf")
        self.assertEqual(["polars", "vaex", "zarr-python"], zarr_pack["skill_candidates"])
        self.assertEqual(["polars", "vaex", "zarr-python"], zarr_pack["route_authority_candidates"])
        self.assertEqual([], zarr_pack["stage_assistant_candidates"])
        self.assertEqual(["tiledbvcf"], tiledb_pack["skill_candidates"])
        self.assertEqual(["tiledbvcf"], tiledb_pack["route_authority_candidates"])
        self.assertEqual([], tiledb_pack["stage_assistant_candidates"])

    def test_manifest_removes_geo_database_from_geospatial(self) -> None:
        pack = load_pack("science-geospatial")
        self.assertEqual(["geopandas", "geomaster"], pack["skill_candidates"])
        self.assertEqual(["geopandas", "geomaster"], pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])
        self.assertNotEqual("geo-database", pack["defaults_by_task"]["research"])

    def test_manifest_makes_web_scraping_direct_owners(self) -> None:
        pack = load_pack("web-scraping")
        self.assertEqual(["scrapling", "playwright"], pack["skill_candidates"])
        self.assertEqual(["scrapling", "playwright"], pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])
```

Add route tests below the manifest tests for each owner:

```python
    def test_medical_imaging_routes_to_direct_owners(self) -> None:
        self.assert_selected("用 pydicom 读取 DICOM tags 并匿名化患者字段", "science-medical-imaging", "pydicom", task_type="coding")
        self.assert_selected("从 Imaging Data Commons 查询 TCIA cancer imaging cohort 并下载 DICOMWeb 样例", "science-medical-imaging", "imaging-data-commons")
        self.assert_selected("用 histolab 对 whole slide image 做 tissue detection 和 tile extraction", "science-medical-imaging", "histolab", task_type="coding")
        self.assert_selected("用 OMERO 读取 microscopy image server 里的 ROI annotations", "science-medical-imaging", "omero-integration", task_type="coding")
        self.assert_selected("用 PathML 构建 digital pathology WSI 分析流程", "science-medical-imaging", "pathml", task_type="planning")

    def test_finance_routes_to_direct_owners(self) -> None:
        self.assert_selected("用 EDGAR 拉取 AAPL 10-K 并解析 XBRL financial statements", "finance-edgar-macro", "edgartools")
        self.assert_selected("用 Alpha Vantage 获取 AAPL stock price 日线行情并输出 CSV", "finance-edgar-macro", "alpha-vantage", task_type="coding")
        self.assert_selected("用 FRED 获取 CPI unemployment federal funds rate 时间序列", "finance-edgar-macro", "fred-economic-data")
        self.assert_selected("用 U.S. Treasury Fiscal Data 查询 national debt 和 federal spending", "finance-edgar-macro", "usfiscaldata")
        self.assert_selected("查询 OFR Hedge Fund Monitor 和 Form PF aggregate statistics", "finance-edgar-macro", "hedgefundmonitor")
        self.assert_selected("生成 consulting-style market research report 和 competitive analysis", "finance-edgar-macro", "market-research-reports", task_type="planning")
        self.assert_selected("用 Data Commons 查询 public statistical data 和人口经济指标", "finance-edgar-macro", "datacommons-client")

    def test_zarr_polars_and_tiledbvcf_have_separate_owners(self) -> None:
        self.assert_selected("用 Polars 读取 Parquet 并做 lazy groupby aggregation", "science-zarr-polars", "polars", task_type="coding")
        self.assert_selected("用 Vaex 做 out-of-core big dataframe filtering", "science-zarr-polars", "vaex", task_type="coding")
        self.assert_selected("用 Zarr 存储 chunked N-D array 到 S3 并并行读取", "science-zarr-polars", "zarr-python", task_type="coding")
        self.assert_selected("用 TileDB-VCF 管理大规模 VCF BCF 并查询基因区域 variant", "science-tiledbvcf", "tiledbvcf", task_type="coding")

    def test_geospatial_routes_and_blocks_ncbi_geo(self) -> None:
        self.assert_selected("用 GeoPandas 读取 Shapefile 并导出 GeoJSON，做 spatial join", "science-geospatial", "geopandas", task_type="coding")
        self.assert_selected("做 remote sensing earth observation workflow，包含投影和经纬度坐标转换", "science-geospatial", "geomaster", task_type="planning")
        result = route("查询 NCBI GEO 的 GSE 和 GSM gene expression dataset")
        self.assertNotEqual("science-geospatial", selected(result)[0], ranked_summary(result))

    def test_web_scraping_routes_to_direct_owners_and_blocks_generic_research(self) -> None:
        self.assert_selected("用 scrapling 抓取网页并用 CSS selector 提取 #main a 链接", "web-scraping", "scrapling", task_type="coding")
        self.assert_selected("用 Playwright 做 browser automation，登录表单并截图调试动态页面", "web-scraping", "playwright", task_type="debug")
        result = route("检索 PubMed website 上的文献并整理 citation references")
        self.assertNotEqual("web-scraping", selected(result)[0], ranked_summary(result))
```

- [ ] **Step 2: Run focused test and verify RED**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py -q
```

Expected: FAIL. The failure must include missing or mismatched `route_authority_candidates`, `stage_assistant_candidates`, `science-zarr-polars` still containing `tiledbvcf`, or `science-geospatial` still containing `geo-database`.

## Task 2: Routing Config Implementation

**Files:**
- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`

- [ ] **Step 1: Update pack manifest**

Apply these manifest changes:

```text
science-medical-imaging.route_authority_candidates =
  pydicom, imaging-data-commons, histolab, omero-integration, pathml
science-medical-imaging.stage_assistant_candidates = []

finance-edgar-macro.route_authority_candidates =
  edgartools, alpha-vantage, fred-economic-data, usfiscaldata,
  hedgefundmonitor, market-research-reports, datacommons-client
finance-edgar-macro.stage_assistant_candidates = []

science-zarr-polars.skill_candidates =
  polars, vaex, zarr-python
science-zarr-polars.route_authority_candidates =
  polars, vaex, zarr-python
science-zarr-polars.stage_assistant_candidates = []
science-zarr-polars.trigger_keywords removes tiledb and tiledbvcf

science-tiledbvcf.route_authority_candidates = tiledbvcf
science-tiledbvcf.stage_assistant_candidates = []

science-geospatial.skill_candidates =
  geopandas, geomaster
science-geospatial.route_authority_candidates =
  geopandas, geomaster
science-geospatial.stage_assistant_candidates = []
science-geospatial.defaults_by_task.research = geomaster

web-scraping.route_authority_candidates =
  scrapling, playwright
web-scraping.stage_assistant_candidates = []
```

- [ ] **Step 2: Update keyword index**

Use these keyword targets:

```text
playwright:
  playwright, browser automation, headless browser, browser test,
  form filling, login flow, dynamic page, screenshot flow,
  页面自动化, 浏览器自动化, 登录表单, 动态页面, 截图调试

geo-database:
  ncbi geo, gene expression omnibus, gse, gsm, gpl,
  geo dataset, expression dataset, 基因表达数据库, 表达谱数据

tiledbvcf:
  tiledb-vcf, tiledb vcf, tiledbvcf, vcf, bcf,
  variant storage, genomics storage, population genomics, 变异存储
```

Keep owner-specific keyword entries for medical imaging, finance, Zarr/Polars, and geospatial skills concrete. Do not add broad generic words as decisive keywords.

- [ ] **Step 3: Update routing rules**

Add or adjust negative boundaries:

```text
market-research-reports.negative_keywords +=
  edgar, sec, 10-k, 10q, xbrl, fred, cpi, alpha vantage,
  treasury, fiscal data, hedge fund monitor, data commons

polars.negative_keywords += vcf, bcf, tiledbvcf, genomics storage, variant storage
vaex.negative_keywords += vcf, bcf, tiledbvcf, genomics storage, variant storage
zarr-python.negative_keywords += vcf, bcf, tiledbvcf, variant storage
tiledbvcf.positive_keywords += tiledb-vcf, tiledb vcf, bcf, population genomics, variant query
tiledbvcf.negative_keywords += polars, vaex, zarr, parquet, dataframe, chunked array
tiledbvcf.equivalent_group = genomic-variant-storage

geopandas.negative_keywords += ncbi geo, gene expression omnibus, gse, gsm, gene expression
geomaster.positive_keywords += remote sensing, earth observation, raster, satellite, 遥感, 地球观测
geomaster.negative_keywords += ncbi geo, gene expression omnibus, gse, gsm, gene expression
geo-database.positive_keywords = ncbi geo, gene expression omnibus, gse, gsm, gpl, expression dataset
geo-database.negative_keywords += geospatial, gis, shapefile, geojson, map, 地理, 地图
geo-database.equivalent_group = bio-expression-database

scrapling.negative_keywords += browser automation, playwright, form filling, login flow, screenshot
playwright.positive_keywords += browser automation, playwright, headless browser, form filling, login flow, screenshot, dynamic page
playwright.negative_keywords += pubmed, citation, references, bibtex, literature review
```

- [ ] **Step 4: Run focused test and verify GREEN**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py -q
```

Expected: PASS.

## Task 3: Script Probe Coverage

**Files:**
- Modify: `scripts/verify/probe-scientific-packs.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`

- [ ] **Step 1: Extend scientific route probes**

Add cases to `probe-scientific-packs.ps1` for:

```text
imaging_histolab_tiles -> science-medical-imaging / histolab
imaging_omero_roi -> science-medical-imaging / omero-integration
finance_usfiscal_debt -> finance-edgar-macro / usfiscaldata
finance_hedgefundmonitor -> finance-edgar-macro / hedgefundmonitor
finance_market_research_report -> finance-edgar-macro / market-research-reports
finance_datacommons_public_stats -> finance-edgar-macro / datacommons-client
bigdata_vaex_out_of_core -> science-zarr-polars / vaex
geo_ncbi_geo_not_geospatial -> blocked pack science-geospatial
```

- [ ] **Step 2: Extend skill-index audit**

Add representative cases to `vibe-skill-index-routing-audit.ps1`:

```text
medical histolab wsi -> science-medical-imaging / histolab
medical omero microscopy -> science-medical-imaging / omero-integration
finance us fiscal -> finance-edgar-macro / usfiscaldata
finance hedge fund monitor -> finance-edgar-macro / hedgefundmonitor
finance data commons -> finance-edgar-macro / datacommons-client
zarr vaex -> science-zarr-polars / vaex
tiledbvcf owner -> science-tiledbvcf / tiledbvcf
ncbi geo not geospatial -> blocked pack science-geospatial
web playwright automation -> web-scraping / playwright
generic pubmed website not scraping -> blocked pack web-scraping
```

- [ ] **Step 3: Extend pack regression matrix**

Add broader cases to `vibe-pack-regression-matrix.ps1`:

```text
medical imaging pydicom direct owner
finance edgar direct owner
finance market report direct owner
zarr polars direct owner
tiledbvcf single owner
geospatial geopandas direct owner
geospatial blocks ncbi geo
web scraping playwright direct owner
web scraping blocks generic website research
```

- [ ] **Step 4: Run script checks**

Run:

```powershell
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
```

Expected: all pass, with no failed assertions.

## Task 4: Governance Note

**Files:**
- Create: `docs/governance/zero-route-authority-pack-consolidation-2026-04-29.md`

- [ ] **Step 1: Write governance record**

Create a concise note with:

```text
Title: Zero Route Authority Pack Consolidation
Scope: first pass over five high-value zero-authority packs
Before: each selected pack had skill_candidates and zero route_authority_candidates
After:
  science-medical-imaging: 5 direct owners, 0 stage assistants
  finance-edgar-macro: 7 direct owners, 0 stage assistants
  science-zarr-polars: 3 direct owners, tiledbvcf moved to science-tiledbvcf
  science-tiledbvcf: 1 direct owner, 0 stage assistants
  science-geospatial: 2 direct owners, geo-database removed from geospatial
  web-scraping: 2 direct owners, 0 stage assistants
Deletion: no physical skill directories deleted in this pass
Verification: list focused tests and route gates
```

- [ ] **Step 2: Run focused test again**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py -q
```

Expected: PASS.

## Task 5: Full Verification And Commits

**Files:**
- Modify: `config/skills-lock.json`

- [ ] **Step 1: Run broader route/config gates**

Run:

```powershell
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

Expected:

```text
vibe-pack-routing-smoke: 0 failed assertions
vibe-generate-skills-lock: regenerates config/skills-lock.json
vibe-offline-skills-gate: PASS
vibe-config-parity-gate: PASS
git diff --check: exit 0
```

- [ ] **Step 2: Inspect diffs**

Run:

```powershell
git status --short --branch
git diff --stat
git diff -- config/skills-lock.json
```

Expected: routing/config/test/script/governance changes plus `skills-lock.json` generated timestamp only.

- [ ] **Step 3: Commit implementation without lock timestamp**

Stage and commit:

```powershell
git add config/pack-manifest.json config/skill-keyword-index.json config/skill-routing-rules.json `
  docs/governance/zero-route-authority-pack-consolidation-2026-04-29.md `
  scripts/verify/probe-scientific-packs.ps1 scripts/verify/vibe-pack-regression-matrix.ps1 `
  scripts/verify/vibe-skill-index-routing-audit.ps1 `
  tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py
git commit -m "fix: define direct owners for zero authority packs"
```

- [ ] **Step 4: Commit lock refresh separately**

If `config/skills-lock.json` changed only by `generated_at`, run:

```powershell
git add config/skills-lock.json
git commit -m "chore: refresh skills lock after zero authority cleanup"
```

- [ ] **Step 5: Final status check**

Run:

```powershell
git status --short --branch
git log -3 --oneline
```

Expected: clean working tree and new commits on `main`.
