# Science Literature Citations Peer Review Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Shrink `science-literature-citations`, delete the low-fit `open-notebook` skill, and make scholarly review route cleanly to `science-peer-review`.

**Architecture:** Treat `science-literature-citations` as the literature/citation/evidence-extraction owner and `science-peer-review` as the paper-review/evidence-critique/scoring owner. Lock the boundary with failing route tests first, then update manifest roles, keyword/routing rules, live references, lockfile, and governance notes.

**Tech Stack:** PowerShell router scripts, Python `unittest`, JSON config files, Vibe-Skills bundled skill directories.

---

## File Map

- Create: `tests/runtime_neutral/test_science_literature_peer_review_consolidation.py`
- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`
- Delete: `bundled/skills/open-notebook/`
- Modify: `scripts/verify/probe-scientific-packs.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
- Modify: `config/skills-lock.json`
- Create: `docs/governance/science-literature-peer-review-consolidation-2026-04-29.md`

## Task 1: Add Failing Boundary Tests

**Files:**
- Create: `tests/runtime_neutral/test_science_literature_peer_review_consolidation.py`

- [ ] **Step 1: Create the route regression test file**

Use `apply_patch` to add this exact file:

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


def route(prompt: str, task_type: str = "research", grade: str = "L") -> dict[str, object]:
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


def pack_by_id(pack_id: str) -> dict[str, object]:
    manifest_path = REPO_ROOT / "config" / "pack-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    packs = manifest.get("packs")
    assert isinstance(packs, list), manifest
    for pack in packs:
        assert isinstance(pack, dict), pack
        if pack.get("id") == pack_id:
            return pack
    raise AssertionError(f"pack missing: {pack_id}")


class ScienceLiteraturePeerReviewConsolidationTests(unittest.TestCase):
    def assert_selected(
        self,
        prompt: str,
        expected_pack: str,
        expected_skill: str,
        *,
        task_type: str = "research",
        grade: str = "L",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertEqual((expected_pack, expected_skill), selected(result), ranked_summary(result))

    def test_literature_pack_manifest_is_literature_only(self) -> None:
        pack = pack_by_id("science-literature-citations")
        self.assertEqual(
            [
                "pubmed-database",
                "openalex-database",
                "biorxiv-database",
                "bgpt-paper-search",
                "pyzotero",
                "citation-management",
                "literature-review",
            ],
            pack.get("skill_candidates"),
        )
        self.assertEqual(pack.get("skill_candidates"), pack.get("route_authority_candidates"))
        self.assertEqual([], pack.get("stage_assistant_candidates"))

    def test_peer_review_pack_has_explicit_route_authorities(self) -> None:
        pack = pack_by_id("science-peer-review")
        self.assertEqual(
            ["peer-review", "scientific-critical-thinking", "scholar-evaluation"],
            pack.get("skill_candidates"),
        )
        self.assertEqual(pack.get("skill_candidates"), pack.get("route_authority_candidates"))
        self.assertEqual([], pack.get("stage_assistant_candidates"))

    def test_open_notebook_skill_directory_is_removed(self) -> None:
        self.assertFalse((REPO_ROOT / "bundled" / "skills" / "open-notebook").exists())

    def test_pubmed_bibtex_stays_in_literature_pack(self) -> None:
        self.assert_selected(
            "在 PubMed 检索文献并导出 BibTeX",
            "science-literature-citations",
            "pubmed-database",
        )

    def test_pyzotero_api_stays_in_literature_pack(self) -> None:
        self.assert_selected(
            "用 pyzotero 连接 Zotero library，批量整理条目并导出 BibTeX",
            "science-literature-citations",
            "pyzotero",
            task_type="coding",
            grade="M",
        )

    def test_citation_formatting_stays_in_literature_pack(self) -> None:
        self.assert_selected(
            "整理参考文献格式，修正 DOI，生成 Nature 格式 bibliography",
            "science-literature-citations",
            "citation-management",
            task_type="planning",
            grade="M",
        )

    def test_systematic_review_stays_in_literature_pack(self) -> None:
        self.assert_selected(
            "做系统综述和 meta-analysis，输出 PRISMA 流程和纳排标准",
            "science-literature-citations",
            "literature-review",
        )

    def test_full_text_evidence_table_stays_in_literature_pack(self) -> None:
        self.assert_selected(
            "做 full-text 文献检索，提取样本量、effect size、方法学细节，生成系统综述证据表",
            "science-literature-citations",
            "bgpt-paper-search",
        )

    def test_formal_peer_review_routes_to_peer_review_pack(self) -> None:
        self.assert_selected(
            "请对这篇论文做 peer review，指出方法学缺陷和可复现性风险",
            "science-peer-review",
            "peer-review",
            task_type="review",
        )

    def test_scholareval_routes_to_scholar_evaluation(self) -> None:
        self.assert_selected(
            "用 ScholarEval rubric 评估这篇论文的问题 formulation、methodology、analysis 和 writing",
            "science-peer-review",
            "scholar-evaluation",
            task_type="review",
        )

    def test_evidence_strength_routes_to_scientific_critical_thinking(self) -> None:
        self.assert_selected(
            "批判性分析这篇论文的证据强度、偏倚和混杂因素",
            "science-peer-review",
            "scientific-critical-thinking",
            task_type="review",
        )

    def test_publishing_rebuttal_stays_with_publishing_workflow(self) -> None:
        self.assert_selected(
            "写论文投稿 cover letter 和 response to reviewers rebuttal matrix",
            "scholarly-publishing-workflow",
            "submission-checklist",
            task_type="planning",
        )

    def test_latex_paper_build_stays_with_latex_pipeline(self) -> None:
        self.assert_selected(
            "用 LaTeX 写论文并构建 PDF",
            "scholarly-publishing-workflow",
            "latex-submission-pipeline",
            task_type="coding",
            grade="XL",
        )
```

- [ ] **Step 2: Run the new test and confirm it fails for the current repo**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_literature_peer_review_consolidation.py -q
```

Expected: FAIL. At minimum, these assertions should fail before implementation:

```text
test_literature_pack_manifest_is_literature_only
test_peer_review_pack_has_explicit_route_authorities
test_open_notebook_skill_directory_is_removed
test_scholareval_routes_to_scholar_evaluation
test_evidence_strength_routes_to_scientific_critical_thinking
```

Do not commit this failing test alone.

## Task 2: Shrink Pack Manifest Roles

**Files:**
- Modify: `config/pack-manifest.json`

- [ ] **Step 1: Replace `science-literature-citations` with the narrow candidate set**

In `config/pack-manifest.json`, update only the `science-literature-citations` object so these fields match exactly:

```json
"skill_candidates": [
  "pubmed-database",
  "openalex-database",
  "biorxiv-database",
  "bgpt-paper-search",
  "pyzotero",
  "citation-management",
  "literature-review"
],
"route_authority_candidates": [
  "pubmed-database",
  "openalex-database",
  "biorxiv-database",
  "bgpt-paper-search",
  "pyzotero",
  "citation-management",
  "literature-review"
],
"stage_assistant_candidates": [],
"defaults_by_task": {
  "planning": "literature-review",
  "coding": "pubmed-database",
  "review": "literature-review",
  "research": "pubmed-database"
}
```

Do not remove `paper-2-web` from `scholarly-publishing-workflow`.

- [ ] **Step 2: Add explicit `science-peer-review` authorities**

In the `science-peer-review` object, set the fields to:

```json
"skill_candidates": [
  "peer-review",
  "scientific-critical-thinking",
  "scholar-evaluation"
],
"route_authority_candidates": [
  "peer-review",
  "scientific-critical-thinking",
  "scholar-evaluation"
],
"stage_assistant_candidates": [],
"defaults_by_task": {
  "planning": "scientific-critical-thinking",
  "review": "peer-review",
  "research": "peer-review"
}
```

- [ ] **Step 3: Run the focused test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_literature_peer_review_consolidation.py -q
```

Expected: manifest-count tests pass, but route tests may still fail until routing rules are tightened.

Do not commit yet.

## Task 3: Tighten Keyword Index And Routing Rules

**Files:**
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`

- [ ] **Step 1: Update `config/skill-keyword-index.json`**

Remove the top-level `open-notebook` entry from `skills`.

Ensure these skill keyword arrays include the listed values. Preserve useful existing keywords and append missing ones.

```json
"peer-review": {
  "keywords": [
    "peer review",
    "reviewer comments",
    "manuscript review",
    "grant review",
    "methodology review",
    "statistical validity",
    "reproducibility risk",
    "同行评审",
    "审稿意见",
    "审稿",
    "论文评审",
    "方法学缺陷",
    "可复现性风险"
  ]
},
"scholar-evaluation": {
  "keywords": [
    "scholar evaluation",
    "scholareval",
    "paper evaluation",
    "paper quality",
    "research quality",
    "methodology scoring",
    "scoring rubric",
    "rubric",
    "score paper",
    "论文评价",
    "论文质量",
    "学术评估",
    "评估论文",
    "评分 rubric",
    "量化评分"
  ]
},
"scientific-critical-thinking": {
  "keywords": [
    "critical thinking",
    "scientific critique",
    "methodology critique",
    "evidence strength",
    "bias",
    "confounders",
    "GRADE",
    "Cochrane",
    "risk of bias",
    "批判性思维",
    "科研批判",
    "方法学批判",
    "证据强度",
    "偏倚",
    "混杂因素"
  ]
}
```

- [ ] **Step 2: Remove `open-notebook` from `config/skill-routing-rules.json`**

Delete the top-level `open-notebook` rule from `skills`.

- [ ] **Step 3: Strengthen `science-peer-review` skill rules**

In `config/skill-routing-rules.json`, ensure these rules include the listed positive and negative keywords. Preserve existing useful values.

```json
"peer-review": {
  "task_allow": ["review", "research"],
  "positive_keywords": [
    "peer review",
    "review this paper",
    "review my paper",
    "manuscript review",
    "grant review",
    "reviewer comments",
    "methodology defects",
    "statistical validity",
    "reproducibility risk",
    "审稿",
    "同行评审",
    "论文评审",
    "方法学缺陷",
    "可复现性风险"
  ],
  "negative_keywords": [
    "bibtex",
    "zotero",
    "latex",
    "cover letter",
    "rebuttal matrix"
  ],
  "canonical_for_task": ["review"]
}
```

```json
"scholar-evaluation": {
  "task_allow": ["review", "research"],
  "positive_keywords": [
    "scholareval",
    "evaluate paper",
    "score paper",
    "paper quality",
    "research quality",
    "methodology scoring",
    "scoring rubric",
    "rubric",
    "论文质量",
    "论文评价",
    "学术评估",
    "评估论文",
    "评分 rubric",
    "量化评分"
  ],
  "negative_keywords": [
    "model evaluation",
    "模型评估",
    "代码质量",
    "code review",
    "pubmed api",
    "openalex api"
  ],
  "canonical_for_task": ["review"]
}
```

```json
"scientific-critical-thinking": {
  "task_allow": ["planning", "review", "research"],
  "positive_keywords": [
    "critical thinking",
    "critique",
    "challenge assumptions",
    "evidence strength",
    "bias",
    "confounders",
    "GRADE",
    "Cochrane",
    "risk of bias",
    "批判性思维",
    "科研批判",
    "证据强度",
    "偏倚",
    "混杂因素"
  ],
  "negative_keywords": [
    "excel",
    "xlsx",
    "source of truth",
    "repo evidence",
    "router config",
    "配置出处"
  ],
  "canonical_for_task": ["planning", "review"]
}
```

- [ ] **Step 4: Add negative guards to false-positive competitors**

In `config/skill-routing-rules.json`, append these negative keywords:

For `code-reviewer`:

```json
"negative_keywords": [
  "paper quality",
  "research quality",
  "scholareval",
  "methodology scoring",
  "论文质量",
  "学术评估",
  "评估论文"
]
```

For `evaluating-machine-learning-models`:

```json
"negative_keywords": [
  "paper quality",
  "research quality",
  "scholareval",
  "peer review",
  "论文质量",
  "学术评估",
  "同行评审"
]
```

For `flashrag-evidence`:

```json
"negative_keywords": [
  "paper quality",
  "research quality",
  "methodology critique",
  "evidence strength",
  "bias",
  "confounders",
  "论文质量",
  "证据强度",
  "偏倚",
  "混杂因素"
]
```

- [ ] **Step 5: Run the focused route tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_literature_peer_review_consolidation.py -q
```

Expected: all tests pass except `test_open_notebook_skill_directory_is_removed`, which will pass after Task 4.

Do not commit yet.

## Task 4: Delete `open-notebook` And Clean Live References

**Files:**
- Delete: `bundled/skills/open-notebook/`
- Modify: `config/skills-lock.json` after lock regeneration in Task 7

- [ ] **Step 1: Verify the deletion target is inside the repo**

Run:

```powershell
$repo = (Resolve-Path .).Path
$target = (Resolve-Path .\bundled\skills\open-notebook).Path
if (-not $target.StartsWith($repo, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "Refusing to delete outside repo: $target"
}
$target
```

Expected: prints `F:\vibe\Vibe-Skills\bundled\skills\open-notebook`.

- [ ] **Step 2: Delete the directory**

Run:

```powershell
Remove-Item -LiteralPath .\bundled\skills\open-notebook -Recurse -Force
```

- [ ] **Step 3: Check remaining live references**

Run:

```powershell
rg -n "open-notebook" config tests scripts README.md README.zh.md bundled
```

Expected before lock regeneration: only `config/skills-lock.json` may still mention `open-notebook`. No references should remain in `config/pack-manifest.json`, `config/skill-keyword-index.json`, or `config/skill-routing-rules.json`.

- [ ] **Step 4: Run the focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_literature_peer_review_consolidation.py -q
```

Expected: all tests pass.

- [ ] **Step 5: Commit focused routing and deletion work**

Run:

```powershell
git add config\pack-manifest.json config\skill-keyword-index.json config\skill-routing-rules.json tests\runtime_neutral\test_science_literature_peer_review_consolidation.py
git add -A bundled\skills\open-notebook
git commit -m "fix: consolidate literature and peer review routing"
```

Expected: commit succeeds.

## Task 5: Update Route Probe Scripts

**Files:**
- Modify: `scripts/verify/probe-scientific-packs.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`

- [ ] **Step 1: Update `probe-scientific-packs.ps1` cases**

In the `# science-literature-citations` case block, replace the three current cases with these eight cases:

```powershell
    [pscustomobject]@{
        name = "lit_pubmed_pmid_bibtex"
        group = "science-literature-citations"
        prompt = "/vibe 在 PubMed 检索文献并导出 BibTeX"
        grade = "M"
        task_type = "research"
        expected_pack = "science-literature-citations"
        expected_skill = "pubmed-database"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "lit_pyzotero_library_bibtex"
        group = "science-literature-citations"
        prompt = "/vibe 用 pyzotero 连接 Zotero library，批量整理条目并导出 BibTeX"
        grade = "M"
        task_type = "coding"
        expected_pack = "science-literature-citations"
        expected_skill = "pyzotero"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "lit_citation_formatting"
        group = "science-literature-citations"
        prompt = "/vibe 整理参考文献格式，修正 DOI，生成 Nature 格式 bibliography"
        grade = "M"
        task_type = "planning"
        expected_pack = "science-literature-citations"
        expected_skill = "citation-management"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "lit_systematic_review_prisma"
        group = "science-literature-citations"
        prompt = "/vibe 做系统综述和 meta-analysis，输出 PRISMA 流程和纳排标准"
        grade = "L"
        task_type = "research"
        expected_pack = "science-literature-citations"
        expected_skill = "literature-review"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "lit_full_text_evidence_table"
        group = "science-literature-citations"
        prompt = "/vibe 做 full-text 文献检索，提取样本量、effect size、方法学细节，生成系统综述证据表"
        grade = "L"
        task_type = "research"
        expected_pack = "science-literature-citations"
        expected_skill = "bgpt-paper-search"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "peer_review_formal"
        group = "science-peer-review"
        prompt = "/vibe 请对这篇论文做 peer review，指出方法学缺陷和可复现性风险"
        grade = "L"
        task_type = "review"
        expected_pack = "science-peer-review"
        expected_skill = "peer-review"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "peer_review_scholareval"
        group = "science-peer-review"
        prompt = "/vibe 用 ScholarEval rubric 评估这篇论文的问题 formulation、methodology、analysis 和 writing"
        grade = "L"
        task_type = "review"
        expected_pack = "science-peer-review"
        expected_skill = "scholar-evaluation"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "peer_review_critical_evidence"
        group = "science-peer-review"
        prompt = "/vibe 批判性分析这篇论文的证据强度、偏倚和混杂因素"
        grade = "L"
        task_type = "review"
        expected_pack = "science-peer-review"
        expected_skill = "scientific-critical-thinking"
        requested_skill = $null
    },
```

- [ ] **Step 2: Add skill-index audit cases**

In `scripts/verify/vibe-skill-index-routing-audit.ps1`, append these cases near the existing PubMed case:

```powershell
    [pscustomobject]@{ Name = "pyzotero library bibtex"; Prompt = "用 pyzotero 连接 Zotero library，批量整理条目并导出 BibTeX"; Grade = "M"; TaskType = "coding"; ExpectedPack = "science-literature-citations"; ExpectedSkill = "pyzotero" },
    [pscustomobject]@{ Name = "citation formatting"; Prompt = "整理参考文献格式，修正 DOI，生成 Nature 格式 bibliography"; Grade = "M"; TaskType = "planning"; ExpectedPack = "science-literature-citations"; ExpectedSkill = "citation-management" },
    [pscustomobject]@{ Name = "systematic review prisma"; Prompt = "做系统综述和 meta-analysis，输出 PRISMA 流程和纳排标准"; Grade = "L"; TaskType = "research"; ExpectedPack = "science-literature-citations"; ExpectedSkill = "literature-review" },
    [pscustomobject]@{ Name = "full text evidence table"; Prompt = "做 full-text 文献检索，提取样本量、effect size、方法学细节，生成系统综述证据表"; Grade = "L"; TaskType = "research"; ExpectedPack = "science-literature-citations"; ExpectedSkill = "bgpt-paper-search" },
    [pscustomobject]@{ Name = "scholareval paper quality"; Prompt = "用 ScholarEval rubric 评估这篇论文的问题 formulation、methodology、analysis 和 writing"; Grade = "L"; TaskType = "review"; ExpectedPack = "science-peer-review"; ExpectedSkill = "scholar-evaluation" },
    [pscustomobject]@{ Name = "critical evidence strength"; Prompt = "批判性分析这篇论文的证据强度、偏倚和混杂因素"; Grade = "L"; TaskType = "review"; ExpectedPack = "science-peer-review"; ExpectedSkill = "scientific-critical-thinking" },
```

- [ ] **Step 3: Run probe scripts**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\probe-scientific-packs.ps1 -Unattended
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected:

```text
probe-scientific-packs: all cases pass, including science-literature-citations and science-peer-review
VCO Skill-Index Routing Audit: Failed: 0
```

- [ ] **Step 4: Commit probe updates**

Run:

```powershell
git add scripts\verify\probe-scientific-packs.ps1 scripts\verify\vibe-skill-index-routing-audit.ps1
git commit -m "test: cover literature peer review boundaries"
```

Expected: commit succeeds.

## Task 6: Add Governance Note

**Files:**
- Create: `docs/governance/science-literature-peer-review-consolidation-2026-04-29.md`

- [ ] **Step 1: Create the governance note**

Use `apply_patch` to add:

````markdown
# Science Literature And Peer Review Consolidation

Date: 2026-04-29

## Summary

This pass shrinks `science-literature-citations` into a literature discovery, citation management, and evidence extraction pack. Scholarly paper review and paper-quality scoring now belong to `science-peer-review`.

The six-stage Vibe runtime is unchanged, and skill usage remains binary:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / unused
```

## Counts

| Pack | Field | Before | After |
| --- | --- | ---: | ---: |
| `science-literature-citations` | `skill_candidates` | 12 | 7 |
| `science-literature-citations` | `route_authority_candidates` | 10 | 7 |
| `science-literature-citations` | `stage_assistant_candidates` | 2 | 0 |
| `science-peer-review` | `skill_candidates` | 3 | 3 |
| `science-peer-review` | `route_authority_candidates` | 0 | 3 |
| `science-peer-review` | `stage_assistant_candidates` | 0 | 0 |

## Kept Literature Owners

| User problem | Skill |
| --- | --- |
| PubMed, PMID, MeSH, MEDLINE | `pubmed-database` |
| OpenAlex, DOI, authors, institutions, citation graph | `openalex-database` |
| bioRxiv and life-science preprints | `biorxiv-database` |
| Full-text evidence extraction and evidence tables | `bgpt-paper-search` |
| Zotero API and Zotero library automation | `pyzotero` |
| BibTeX, DOI validation, bibliography formatting | `citation-management` |
| Systematic review, meta-analysis, PRISMA | `literature-review` |

## Peer Review Owners

| User problem | Skill |
| --- | --- |
| Formal manuscript or grant review | `peer-review` |
| Evidence strength, bias, confounders, GRADE, Cochrane-style critique | `scientific-critical-thinking` |
| ScholarEval, paper-quality rubric, quantitative research scoring | `scholar-evaluation` |

## Removed Or Moved

| Skill | Action |
| --- | --- |
| `open-notebook` | Physically deleted after live-reference cleanup; it is a broad notebook/document-chat product integration, not a literature/citation expert. |
| `paper-2-web` | Removed from `science-literature-citations`; retained for publishing/promotion surfaces. |
| `peer-review` | Removed from `science-literature-citations`; owned by `science-peer-review`. |
| `scholar-evaluation` | Removed from `science-literature-citations`; owned by `science-peer-review`. |
| `scientific-critical-thinking` | Removed from `science-literature-citations`; owned by `science-peer-review`. |

## Protected Boundaries

| Prompt | Expected route |
| --- | --- |
| `在 PubMed 检索文献并导出 BibTeX` | `science-literature-citations / pubmed-database` |
| `用 pyzotero 连接 Zotero library，批量整理条目并导出 BibTeX` | `science-literature-citations / pyzotero` |
| `整理参考文献格式，修正 DOI，生成 Nature 格式 bibliography` | `science-literature-citations / citation-management` |
| `做系统综述和 meta-analysis，输出 PRISMA 流程和纳排标准` | `science-literature-citations / literature-review` |
| `做 full-text 文献检索，提取样本量、effect size、方法学细节，生成系统综述证据表` | `science-literature-citations / bgpt-paper-search` |
| `请对这篇论文做 peer review，指出方法学缺陷和可复现性风险` | `science-peer-review / peer-review` |
| `用 ScholarEval rubric 评估这篇论文的问题 formulation、methodology、analysis 和 writing` | `science-peer-review / scholar-evaluation` |
| `批判性分析这篇论文的证据强度、偏倚和混杂因素` | `science-peer-review / scientific-critical-thinking` |
| `写论文投稿 cover letter 和 response to reviewers rebuttal matrix` | `scholarly-publishing-workflow / submission-checklist` |
| `用 LaTeX 写论文并构建 PDF` | `scholarly-publishing-workflow / latex-submission-pipeline` |

## Verification

Required checks:

```powershell
python -m pytest tests/runtime_neutral/test_science_literature_peer_review_consolidation.py -q
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\probe-scientific-packs.ps1 -Unattended
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1
git diff --check
```
````

- [ ] **Step 2: Commit governance note**

Run:

```powershell
git add docs\governance\science-literature-peer-review-consolidation-2026-04-29.md
git commit -m "docs: record literature peer review boundary"
```

Expected: commit succeeds.

## Task 7: Refresh Lockfile And Run Full Verification

**Files:**
- Modify: `config/skills-lock.json`

- [ ] **Step 1: Regenerate skills lock**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected: `config/skills-lock.json` is updated and no longer contains `open-notebook`.

- [ ] **Step 2: Verify `open-notebook` has no live references**

Run:

```powershell
rg -n "open-notebook" config tests scripts README.md README.zh.md bundled
```

Expected: no output except historical docs under `docs/superpowers/` or `docs/governance/` if the search is broadened beyond live surfaces. For this exact command, expected output is empty.

- [ ] **Step 3: Run focused and broad checks**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_science_literature_peer_review_consolidation.py -q
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\probe-scientific-packs.ps1 -Unattended
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1
git diff --check
```

Expected:

```text
new pytest: all passed
probe-scientific-packs: all selected routes match expected routes
vibe-pack-regression-matrix: Failed: 0
vibe-skill-index-routing-audit: Failed: 0
vibe-pack-routing-smoke: Failed: 0
vibe-offline-skills-gate: PASS
vibe-config-parity-gate: PASS
git diff --check: no output
```

- [ ] **Step 4: Commit lockfile refresh**

Run:

```powershell
git add config\skills-lock.json
git commit -m "chore: refresh skills lock after literature cleanup"
```

Expected: commit succeeds.

- [ ] **Step 5: Final status check**

Run:

```powershell
git status --short --branch
git log --oneline -5
```

Expected: branch is clean and recent commits include the focused routing/deletion commit, probe commit, governance commit, and lockfile refresh commit.
