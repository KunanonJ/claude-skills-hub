# Research Design Pack Consolidation Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Shrink `research-design` into a clear research-methods pack and remove unrelated skills from its selectable routing surface.

**Architecture:** Add failing route and manifest tests first, then shrink the pack manifest, tighten keyword/routing rules for the kept research-method skills, add probe coverage, and record the governance boundary. This pass changes routing/config only; it does not delete bundled skill directories or change the six-stage Vibe runtime.

**Tech Stack:** Python `unittest`/pytest route tests, PowerShell route-probe scripts, JSON config files, Markdown governance docs.

---

## File Map

- Create: `tests/runtime_neutral/test_research_design_pack_consolidation.py`
- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`
- Create: `docs/governance/research-design-pack-consolidation-2026-04-29.md`

No `config/skills-lock.json` change is expected because this plan does not physically delete skill directories.

## Task 1: Add Focused Failing Tests

**Files:**
- Create: `tests/runtime_neutral/test_research_design_pack_consolidation.py`

- [ ] **Step 1: Create the focused route and manifest test file**

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


RESEARCH_DESIGN_SKILLS = [
    "designing-experiments",
    "experiment-failure-analysis",
    "hypogenic",
    "hypothesis-generation",
    "literature-matrix",
    "performing-causal-analysis",
    "performing-regression-analysis",
    "research-grants",
    "scientific-brainstorming",
]

MOVED_OUT_SKILLS = [
    "architecture-patterns",
    "comprehensive-research-agent",
    "hypothesis-testing",
    "playwright",
    "property-based-testing",
    "research-lookup",
    "scientific-data-preprocessing",
    "skill-creator",
    "skill-lookup",
    "ux-researcher-designer",
    "verification-quality-assurance",
    "report-generator",
    "structured-content-storage",
]


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
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    packs = manifest.get("packs")
    assert isinstance(packs, list), manifest
    for pack in packs:
        assert isinstance(pack, dict), pack
        if pack.get("id") == pack_id:
            return pack
    raise AssertionError(f"pack missing: {pack_id}")


class ResearchDesignPackConsolidationTests(unittest.TestCase):
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

    def assert_not_research_design(
        self,
        prompt: str,
        *,
        task_type: str = "research",
        grade: str = "L",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertNotEqual("research-design", selected(result)[0], ranked_summary(result))

    def test_research_design_manifest_is_research_methods_only(self) -> None:
        pack = pack_by_id("research-design")
        self.assertEqual(RESEARCH_DESIGN_SKILLS, pack.get("skill_candidates"))
        self.assertEqual(RESEARCH_DESIGN_SKILLS, pack.get("route_authority_candidates"))
        self.assertEqual([], pack.get("stage_assistant_candidates"))
        for moved_skill in MOVED_OUT_SKILLS:
            self.assertNotIn(moved_skill, pack.get("skill_candidates") or [])

    def test_quasi_experiment_design_routes_to_designing_experiments(self) -> None:
        self.assert_selected(
            "帮我设计准实验方法，比较 DiD 和 ITS",
            "research-design",
            "designing-experiments",
            task_type="planning",
        )

    def test_experiment_failure_analysis_routes_to_failure_analysis(self) -> None:
        self.assert_selected(
            "分析实验失败原因，判断是否继续优化还是放弃该方案",
            "research-design",
            "experiment-failure-analysis",
            task_type="review",
        )

    def test_hypogenic_routes_to_hypogenic(self) -> None:
        self.assert_selected(
            "用 HypoGeniC 从数据和文献中生成并测试科研假设",
            "research-design",
            "hypogenic",
            task_type="research",
        )

    def test_scientific_hypothesis_generation_routes_to_hypothesis_generation(self) -> None:
        self.assert_selected(
            "根据实验观察生成可检验的科研假设和预测",
            "research-design",
            "hypothesis-generation",
            task_type="planning",
        )

    def test_literature_matrix_routes_to_literature_matrix(self) -> None:
        self.assert_selected(
            "构建论文组合矩阵，寻找 A+B 的研究创新点",
            "research-design",
            "literature-matrix",
            task_type="planning",
        )

    def test_causal_method_routes_to_causal_analysis(self) -> None:
        self.assert_selected(
            "用 DID 和 synthetic control 做因果分析方案",
            "research-design",
            "performing-causal-analysis",
            task_type="research",
        )

    def test_regression_method_routes_to_regression_analysis(self) -> None:
        self.assert_selected(
            "做回归分析并解释系数、置信区间和诊断结果",
            "research-design",
            "performing-regression-analysis",
            task_type="research",
        )

    def test_research_grant_routes_to_research_grants(self) -> None:
        self.assert_selected(
            "写 NSF 科研基金申请书的 significance 和 innovation",
            "research-design",
            "research-grants",
            task_type="planning",
        )

    def test_scientific_brainstorming_routes_to_scientific_brainstorming(self) -> None:
        self.assert_selected(
            "围绕这个生物机制做科研头脑风暴，提出可能机制和实验方向",
            "research-design",
            "scientific-brainstorming",
            task_type="planning",
        )

    def test_pubmed_literature_lookup_stays_outside_research_design(self) -> None:
        self.assert_selected(
            "检索 PubMed 文献并导出 BibTeX",
            "science-literature-citations",
            "pubmed-database",
            task_type="research",
        )

    def test_scientific_report_stays_outside_research_design(self) -> None:
        self.assert_selected(
            "科研技术报告：包含方法结果讨论，输出 HTML 和 PDF",
            "science-reporting",
            "scientific-reporting",
            task_type="planning",
        )

    def test_figma_implementation_stays_outside_research_design(self) -> None:
        self.assert_selected(
            "把这个 Figma 设计稿还原为可运行代码",
            "design-implementation",
            "figma-implement-design",
            task_type="coding",
        )

    def test_playwright_browser_automation_does_not_route_to_research_design(self) -> None:
        result = route("用 Playwright 打开网页并截图", task_type="coding", grade="M")
        self.assertIn(selected(result)[0], {"web-scraping", "screen-capture"}, ranked_summary(result))
        self.assertNotEqual("research-design", selected(result)[0], ranked_summary(result))

    def test_property_based_testing_does_not_route_to_research_design(self) -> None:
        self.assert_not_research_design(
            "为 Python 函数写 property-based testing",
            task_type="coding",
            grade="M",
        )

    def test_backend_architecture_does_not_route_to_research_design(self) -> None:
        self.assert_not_research_design(
            "为后端系统设计 Clean Architecture 架构",
            task_type="planning",
            grade="M",
        )

    def test_skill_creation_does_not_route_to_research_design(self) -> None:
        self.assert_not_research_design(
            "创建一个新的 Codex skill",
            task_type="planning",
            grade="M",
        )

    def test_ux_research_does_not_route_to_research_design(self) -> None:
        self.assert_not_research_design(
            "做用户访谈、persona 和用户旅程图",
            task_type="research",
            grade="M",
        )

    def test_data_preprocessing_guard_does_not_route_to_research_design(self) -> None:
        self.assert_not_research_design(
            "对科研数据做缺失值处理和标准化，避免数据泄漏",
            task_type="planning",
            grade="M",
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and confirm it fails before implementation**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_research_design_pack_consolidation.py -q
```

Expected: FAIL. At minimum, the manifest test fails because `research-design` still has 22 candidates, and several route tests fail because `experiment-failure-analysis`, `hypogenic`, `literature-matrix`, `performing-causal-analysis`, and `scientific-brainstorming` do not yet have stable keyword/routing rules.

Do not commit this failing test alone.

## Task 2: Shrink `research-design` In Pack Manifest

**Files:**
- Modify: `config/pack-manifest.json`

- [ ] **Step 1: Replace the `research-design` routing surface**

In the `research-design` object in `config/pack-manifest.json`, set these fields exactly:

```json
"trigger_keywords": [
  "research design",
  "research methodology",
  "methodology",
  "experimental design",
  "experiment design",
  "quasi-experimental",
  "difference-in-differences",
  "difference in differences",
  "did",
  "interrupted time series",
  "its",
  "synthetic control",
  "causal analysis",
  "causal inference",
  "regression analysis",
  "scientific hypothesis",
  "hypothesis generation",
  "hypogenic",
  "research grant",
  "grant proposal",
  "research proposal",
  "scientific brainstorming",
  "literature matrix",
  "研究设计",
  "研究方法",
  "方法学",
  "实验设计",
  "准实验",
  "差分中的差分",
  "中断时间序列",
  "合成控制",
  "因果分析",
  "因果推断",
  "回归分析",
  "科研假设",
  "假设生成",
  "科研基金",
  "基金申请",
  "研究创新点",
  "科研头脑风暴",
  "实验失败"
],
"skill_candidates": [
  "designing-experiments",
  "experiment-failure-analysis",
  "hypogenic",
  "hypothesis-generation",
  "literature-matrix",
  "performing-causal-analysis",
  "performing-regression-analysis",
  "research-grants",
  "scientific-brainstorming"
],
"route_authority_candidates": [
  "designing-experiments",
  "experiment-failure-analysis",
  "hypogenic",
  "hypothesis-generation",
  "literature-matrix",
  "performing-causal-analysis",
  "performing-regression-analysis",
  "research-grants",
  "scientific-brainstorming"
],
"stage_assistant_candidates": [],
"defaults_by_task": {
  "planning": "designing-experiments",
  "review": "experiment-failure-analysis",
  "research": "hypothesis-generation"
}
```

Do not delete any directories under `bundled/skills/`.

- [ ] **Step 2: Run the focused test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_research_design_pack_consolidation.py -q
```

Expected: manifest assertions pass; route assertions for missing or weak skills may still fail until Task 3.

Do not commit yet.

## Task 3: Tighten Keyword Index And Routing Rules

**Files:**
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`

- [ ] **Step 1: Update keyword index entries for the nine kept skills**

In `config/skill-keyword-index.json`, ensure the `skills` object contains these entries with the listed `keywords` arrays. Preserve the surrounding JSON structure.

```json
"designing-experiments": {
  "keywords": [
    "research design",
    "experimental design",
    "experiment design",
    "quasi-experimental",
    "quasi experimental",
    "did",
    "difference-in-differences",
    "difference in differences",
    "its",
    "interrupted time series",
    "synthetic control",
    "regression discontinuity",
    "准实验",
    "实验设计",
    "研究设计",
    "差分中的差分",
    "中断时间序列",
    "合成控制",
    "断点回归"
  ]
},
"experiment-failure-analysis": {
  "keywords": [
    "experiment failure",
    "failed experiment",
    "failure analysis",
    "root cause experiment",
    "optimization setback",
    "abandon experiment",
    "validation plan",
    "实验失败",
    "失败复盘",
    "失败原因",
    "优化失败",
    "是否放弃",
    "验证计划"
  ]
},
"hypogenic": {
  "keywords": [
    "hypogenic",
    "automated hypothesis generation",
    "automated hypothesis testing",
    "llm hypothesis",
    "hypothesis discovery",
    "generate and test hypotheses",
    "从数据生成假设",
    "自动假设生成",
    "自动假设验证",
    "科研假设自动化"
  ]
},
"hypothesis-generation": {
  "keywords": [
    "hypothesis",
    "hypotheses",
    "hypothesis generation",
    "research hypothesis",
    "scientific hypothesis",
    "testable hypothesis",
    "falsifiable",
    "prediction",
    "mechanism",
    "假设生成",
    "研究假设",
    "科学假设",
    "科研假设",
    "可检验",
    "可证伪",
    "预测",
    "机制假设"
  ]
},
"literature-matrix": {
  "keywords": [
    "literature matrix",
    "paper combination matrix",
    "research idea matrix",
    "method combination",
    "a+b research idea",
    "unified framework",
    "paper combination",
    "论文组合矩阵",
    "文献矩阵",
    "研究创新点",
    "方法组合",
    "统一框架",
    "A+B"
  ]
},
"performing-causal-analysis": {
  "keywords": [
    "causal analysis",
    "causal inference",
    "causal model",
    "treatment effect",
    "impact evaluation",
    "difference-in-differences",
    "did",
    "synthetic control",
    "interrupted time series",
    "regression discontinuity",
    "因果分析",
    "因果推断",
    "因果模型",
    "处理效应",
    "政策评估",
    "DID",
    "合成控制",
    "中断时间序列",
    "断点回归"
  ]
},
"performing-regression-analysis": {
  "keywords": [
    "regression analysis",
    "linear regression",
    "multiple regression",
    "glm",
    "ols",
    "coefficient",
    "confidence interval",
    "regression diagnostics",
    "回归分析",
    "线性回归",
    "多元回归",
    "回归建模",
    "回归诊断",
    "系数",
    "置信区间"
  ]
},
"research-grants": {
  "keywords": [
    "research grant",
    "grant",
    "grants",
    "grant proposal",
    "proposal",
    "nih",
    "nsf",
    "nsfc",
    "darpa",
    "significance",
    "innovation",
    "broader impacts",
    "funding",
    "科研基金",
    "基金申请",
    "基金申请书",
    "基金标书",
    "项目申请书",
    "立项依据",
    "创新性"
  ]
},
"scientific-brainstorming": {
  "keywords": [
    "scientific brainstorming",
    "research brainstorming",
    "research ideation",
    "research gaps",
    "mechanism brainstorming",
    "scientific mechanism",
    "experimental direction",
    "科研头脑风暴",
    "科研创意",
    "研究思路",
    "研究空白",
    "可能机制",
    "实验方向"
  ]
}
```

- [ ] **Step 2: Update routing rules for the nine kept skills**

In `config/skill-routing-rules.json`, ensure the `skills` object contains or updates these rules. Preserve unrelated fields outside each rule.

```json
"designing-experiments": {
  "task_allow": ["planning", "research"],
  "positive_keywords": [
    "research design",
    "experimental design",
    "experiment design",
    "quasi-experimental",
    "quasi experimental",
    "did",
    "difference-in-differences",
    "difference in differences",
    "its",
    "interrupted time series",
    "synthetic control",
    "regression discontinuity",
    "准实验",
    "实验设计",
    "研究设计",
    "差分中的差分",
    "中断时间序列",
    "合成控制",
    "断点回归"
  ],
  "negative_keywords": [
    "python hypothesis",
    "property-based",
    "pytest",
    "browser automation",
    "figma",
    "bibtex",
    "pubmed",
    "report"
  ],
  "canonical_for_task": ["planning"]
}
```

```json
"experiment-failure-analysis": {
  "task_allow": ["planning", "review", "research"],
  "positive_keywords": [
    "experiment failure",
    "failed experiment",
    "failure analysis",
    "root cause experiment",
    "optimization setback",
    "abandon experiment",
    "validation plan",
    "实验失败",
    "失败复盘",
    "失败原因",
    "优化失败",
    "是否放弃",
    "验证计划"
  ],
  "negative_keywords": [
    "ci failure",
    "test failure",
    "pytest failure",
    "github actions",
    "build failure",
    "browser automation"
  ],
  "canonical_for_task": ["review"]
}
```

```json
"hypogenic": {
  "task_allow": ["planning", "research"],
  "positive_keywords": [
    "hypogenic",
    "automated hypothesis generation",
    "automated hypothesis testing",
    "llm hypothesis",
    "hypothesis discovery",
    "generate and test hypotheses",
    "从数据生成假设",
    "自动假设生成",
    "自动假设验证",
    "科研假设自动化"
  ],
  "negative_keywords": [
    "pytest",
    "python hypothesis",
    "property-based",
    "unit test"
  ],
  "canonical_for_task": ["research"]
}
```

```json
"hypothesis-generation": {
  "task_allow": ["planning", "research"],
  "positive_keywords": [
    "hypothesis generation",
    "research hypothesis",
    "scientific hypothesis",
    "testable hypothesis",
    "falsifiable",
    "mechanism",
    "prediction",
    "假设生成",
    "研究假设",
    "科学假设",
    "科研假设",
    "可检验",
    "可证伪",
    "机制假设",
    "预测"
  ],
  "negative_keywords": [
    "python hypothesis",
    "property-based",
    "pytest",
    "unit test",
    "business hypothesis"
  ],
  "canonical_for_task": ["planning"]
}
```

```json
"literature-matrix": {
  "task_allow": ["planning", "research"],
  "positive_keywords": [
    "literature matrix",
    "paper combination matrix",
    "research idea matrix",
    "method combination",
    "a+b research idea",
    "unified framework",
    "paper combination",
    "论文组合矩阵",
    "文献矩阵",
    "研究创新点",
    "方法组合",
    "统一框架",
    "A+B"
  ],
  "negative_keywords": [
    "pubmed",
    "bibtex",
    "zotero",
    "citation format",
    "pdf extraction",
    "full-text evidence table"
  ],
  "canonical_for_task": ["planning", "research"]
}
```

```json
"performing-causal-analysis": {
  "task_allow": ["planning", "research", "review"],
  "positive_keywords": [
    "causal analysis",
    "causal inference",
    "causal model",
    "treatment effect",
    "impact evaluation",
    "difference-in-differences",
    "did",
    "synthetic control",
    "interrupted time series",
    "regression discontinuity",
    "因果分析",
    "因果推断",
    "因果模型",
    "处理效应",
    "政策评估",
    "DID",
    "合成控制",
    "中断时间序列",
    "断点回归"
  ],
  "negative_keywords": [
    "python hypothesis",
    "property-based",
    "bibtex",
    "pubmed",
    "figma",
    "browser automation"
  ],
  "canonical_for_task": ["research", "review"]
}
```

```json
"performing-regression-analysis": {
  "task_allow": ["planning", "research", "review"],
  "positive_keywords": [
    "regression analysis",
    "linear regression",
    "multiple regression",
    "glm",
    "ols",
    "coefficient",
    "confidence interval",
    "regression diagnostics",
    "回归分析",
    "线性回归",
    "多元回归",
    "回归建模",
    "回归诊断",
    "系数",
    "置信区间"
  ],
  "negative_keywords": [
    "causal inference",
    "difference-in-differences",
    "synthetic control",
    "grant proposal",
    "research report",
    "data leakage",
    "figma",
    "browser automation"
  ],
  "canonical_for_task": ["research", "review"]
}
```

```json
"research-grants": {
  "task_allow": ["planning", "research"],
  "positive_keywords": [
    "research grant",
    "grant",
    "grants",
    "grant proposal",
    "proposal",
    "nih",
    "nsf",
    "nsfc",
    "darpa",
    "significance",
    "innovation",
    "broader impacts",
    "funding",
    "科研基金",
    "基金申请",
    "基金申请书",
    "基金标书",
    "项目申请书",
    "立项依据",
    "创新性"
  ],
  "negative_keywords": [
    "tender",
    "bid",
    "招标",
    "投标",
    "采购",
    "docking",
    "smiles",
    "figma"
  ],
  "canonical_for_task": ["planning"]
}
```

```json
"scientific-brainstorming": {
  "task_allow": ["planning", "research"],
  "positive_keywords": [
    "scientific brainstorming",
    "research brainstorming",
    "research ideation",
    "research gaps",
    "mechanism brainstorming",
    "scientific mechanism",
    "experimental direction",
    "科研头脑风暴",
    "科研创意",
    "研究思路",
    "研究空白",
    "可能机制",
    "实验方向"
  ],
  "negative_keywords": [
    "figma",
    "browser automation",
    "property-based",
    "pubmed",
    "bibtex",
    "technical report"
  ],
  "canonical_for_task": ["planning"]
}
```

- [ ] **Step 3: Tighten misleading moved-out software-testing rules**

In `config/skill-routing-rules.json`, update these two existing rules so software testing language cannot steal scientific hypothesis prompts if they are later reintroduced into a pack:

```json
"hypothesis-testing": {
  "task_allow": ["coding", "review"],
  "positive_keywords": [
    "python hypothesis",
    "hypothesis library",
    "@given",
    "property-based",
    "property based",
    "pytest hypothesis"
  ],
  "negative_keywords": [
    "scientific hypothesis",
    "research hypothesis",
    "hypothesis generation",
    "科研假设",
    "研究假设",
    "假设生成",
    "clinical hypothesis",
    "business hypothesis"
  ],
  "canonical_for_task": ["coding", "review"]
}
```

```json
"property-based-testing": {
  "task_allow": ["coding", "review"],
  "positive_keywords": [
    "property-based testing",
    "property based testing",
    "property testing",
    "fast-check",
    "quickcheck",
    "hypothesis library",
    "@given",
    "性质测试"
  ],
  "negative_keywords": [
    "scientific hypothesis",
    "research hypothesis",
    "hypothesis generation",
    "科研假设",
    "研究假设",
    "假设生成",
    "clinical hypothesis"
  ],
  "canonical_for_task": ["coding", "review"]
}
```

- [ ] **Step 4: Run the focused test**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_research_design_pack_consolidation.py -q
```

Expected: all focused tests pass.

- [ ] **Step 5: Commit focused pack and route-rule changes**

Run:

```powershell
git add config\pack-manifest.json config\skill-keyword-index.json config\skill-routing-rules.json tests\runtime_neutral\test_research_design_pack_consolidation.py
git commit -m "fix: consolidate research design routing"
```

Expected: commit succeeds.

## Task 4: Add Script-Level Route Probe Coverage

**Files:**
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`

- [ ] **Step 1: Add skill-index audit cases**

In `scripts/verify/vibe-skill-index-routing-audit.ps1`, append these cases near the existing `grant proposal` and `experiment design` cases:

```powershell
    [pscustomobject]@{ Name = "experiment failure analysis"; Prompt = "分析实验失败原因，判断是否继续优化还是放弃该方案"; Grade = "L"; TaskType = "review"; ExpectedPack = "research-design"; ExpectedSkill = "experiment-failure-analysis" },
    [pscustomobject]@{ Name = "hypogenic automated hypothesis"; Prompt = "用 HypoGeniC 从数据和文献中生成并测试科研假设"; Grade = "L"; TaskType = "research"; ExpectedPack = "research-design"; ExpectedSkill = "hypogenic" },
    [pscustomobject]@{ Name = "scientific hypothesis generation"; Prompt = "根据实验观察生成可检验的科研假设和预测"; Grade = "L"; TaskType = "planning"; ExpectedPack = "research-design"; ExpectedSkill = "hypothesis-generation" },
    [pscustomobject]@{ Name = "literature matrix research ideas"; Prompt = "构建论文组合矩阵，寻找 A+B 的研究创新点"; Grade = "L"; TaskType = "planning"; ExpectedPack = "research-design"; ExpectedSkill = "literature-matrix" },
    [pscustomobject]@{ Name = "causal analysis did synthetic control"; Prompt = "用 DID 和 synthetic control 做因果分析方案"; Grade = "L"; TaskType = "research"; ExpectedPack = "research-design"; ExpectedSkill = "performing-causal-analysis" },
    [pscustomobject]@{ Name = "regression coefficient confidence interval"; Prompt = "做回归分析并解释系数、置信区间和诊断结果"; Grade = "L"; TaskType = "research"; ExpectedPack = "research-design"; ExpectedSkill = "performing-regression-analysis" },
    [pscustomobject]@{ Name = "scientific brainstorming mechanisms"; Prompt = "围绕这个生物机制做科研头脑风暴，提出可能机制和实验方向"; Grade = "L"; TaskType = "planning"; ExpectedPack = "research-design"; ExpectedSkill = "scientific-brainstorming" },
```

If the last existing case in the array currently has no trailing comma, add a comma before appending these rows so the PowerShell array remains valid.

- [ ] **Step 2: Add pack-regression matrix cases**

In `scripts/verify/vibe-pack-regression-matrix.ps1`, append these rows near the existing `research-design planning` case:

```powershell
    [pscustomobject]@{ Name = "research-design hypothesis generation"; Prompt = "根据实验观察生成可检验的科研假设和预测"; Grade = "L"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = "research-design"; AllowedModes = @("pack_overlay", "confirm_required") },
    [pscustomobject]@{ Name = "research-design causal analysis"; Prompt = "用 DID 和 synthetic control 做因果分析方案"; Grade = "L"; TaskType = "research"; RequestedSkill = $null; ExpectedPack = "research-design"; AllowedModes = @("pack_overlay", "confirm_required") },
    [pscustomobject]@{ Name = "research-design grant proposal"; Prompt = "写 NSF 科研基金申请书的 significance 和 innovation"; Grade = "L"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = "research-design"; AllowedModes = @("pack_overlay", "confirm_required") },
```

Do not add weak negative cases to the pack-regression matrix if there is no stable expected owner yet. Keep those in the focused Python test as `not research-design`.

- [ ] **Step 3: Run route probe scripts**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
```

Expected:

```text
VCO Skill-Index Routing Audit: Failed: 0
VCO Pack Regression Matrix: Failed: 0
```

- [ ] **Step 4: Commit probe updates**

Run:

```powershell
git add scripts\verify\vibe-skill-index-routing-audit.ps1 scripts\verify\vibe-pack-regression-matrix.ps1
git commit -m "test: cover research design routing boundaries"
```

Expected: commit succeeds.

## Task 5: Add Governance Note

**Files:**
- Create: `docs/governance/research-design-pack-consolidation-2026-04-29.md`

- [ ] **Step 1: Create the governance note**

Use `apply_patch` to add this exact file:

````markdown
# Research Design Pack Consolidation

Date: 2026-04-29

## Summary

This pass shrinks `research-design` into a research-methods pack. It keeps research design, scientific ideation, hypothesis formulation, experiment failure analysis, causal/regression methodology, literature-combination matrices, and grant proposal planning.

The six-stage Vibe runtime is unchanged, and skill usage remains binary:

```text
skill_candidates -> skill_routing.selected -> skill_usage.used / unused
```

## Counts

| Field | Before | After |
| --- | ---: | ---: |
| `skill_candidates` | 22 | 9 |
| `route_authority_candidates` | 14 | 9 |
| `stage_assistant_candidates` | 3 | 0 |
| physical directory deletion | 0 | 0 |

`route_authority_candidates` is retained only as a compatibility mirror of `skill_candidates`. It is not a second execution model.

## Kept Research-Method Owners

| User problem | Skill |
| --- | --- |
| Quasi-experimental design, DiD, ITS, synthetic control | `designing-experiments` |
| Experiment failure root-cause analysis and recovery planning | `experiment-failure-analysis` |
| Automated hypothesis generation and testing with HypoGeniC | `hypogenic` |
| Testable scientific hypothesis formulation | `hypothesis-generation` |
| Paper-combination matrices and research idea maps | `literature-matrix` |
| Causal analysis and treatment-effect methodology | `performing-causal-analysis` |
| Regression analysis and interpretation | `performing-regression-analysis` |
| Research grant and proposal structure | `research-grants` |
| Scientific mechanism and research-gap brainstorming | `scientific-brainstorming` |

## Moved Out Of Research Design

| Skill | Action | Rationale |
| --- | --- | --- |
| `architecture-patterns` | Removed from `research-design` routing surface | Backend architecture is not research-method ownership. |
| `comprehensive-research-agent` | Removed from `research-design` routing surface | Generic research-agent behavior is orchestration guidance, not a specific method expert. |
| `hypothesis-testing` | Removed from `research-design` routing surface | This is Python Hypothesis/property-based testing, not scientific hypothesis testing. |
| `playwright` | Removed from `research-design` routing surface | Browser automation belongs outside research design; current owner is `web-scraping / playwright` or screen capture when screenshot dominates. |
| `property-based-testing` | Removed from `research-design` routing surface | Software testing is not scientific research design. |
| `research-lookup` | Removed from `research-design` routing surface | Literature lookup belongs to literature/deep-research retrieval surfaces. |
| `scientific-data-preprocessing` | Removed from `research-design` routing surface | Data preprocessing is useful but should not own research-method prompts. |
| `skill-creator` | Removed from `research-design` routing surface | Skill authoring is a meta-skill surface. |
| `skill-lookup` | Removed from `research-design` routing surface | Skill discovery is a meta-skill surface. |
| `ux-researcher-designer` | Removed from `research-design` routing surface | UX research/design is not scientific research-method ownership. |
| `verification-quality-assurance` | Removed from `research-design` routing surface | Verification governance is not a research-method route owner. |
| `report-generator` | Removed from `research-design` routing surface | Report output overlaps with `science-reporting`. |
| `structured-content-storage` | Removed from `research-design` routing surface | Storage discipline can assist projects but is not a research-method owner. |

## No Physical Deletion

No bundled skill directory is physically deleted in this pass. Many moved-out skills have scripts, references, or substantial content. Any later pruning pass must separately prove content migration or low-quality duplication before deletion.

## Protected Boundaries

| Prompt | Expected route |
| --- | --- |
| `帮我设计准实验方法，比较 DiD 和 ITS` | `research-design / designing-experiments` |
| `分析实验失败原因，判断是否继续优化还是放弃该方案` | `research-design / experiment-failure-analysis` |
| `用 HypoGeniC 从数据和文献中生成并测试科研假设` | `research-design / hypogenic` |
| `根据实验观察生成可检验的科研假设和预测` | `research-design / hypothesis-generation` |
| `构建论文组合矩阵，寻找 A+B 的研究创新点` | `research-design / literature-matrix` |
| `用 DID 和 synthetic control 做因果分析方案` | `research-design / performing-causal-analysis` |
| `做回归分析并解释系数、置信区间和诊断结果` | `research-design / performing-regression-analysis` |
| `写 NSF 科研基金申请书的 significance 和 innovation` | `research-design / research-grants` |
| `围绕这个生物机制做科研头脑风暴，提出可能机制和实验方向` | `research-design / scientific-brainstorming` |
| `检索 PubMed 文献并导出 BibTeX` | `science-literature-citations / pubmed-database` |
| `科研技术报告：包含方法结果讨论，输出 HTML 和 PDF` | `science-reporting / scientific-reporting` |
| `把这个 Figma 设计稿还原为可运行代码` | `design-implementation / figma-implement-design` |

## Verification

Required checks:

```powershell
python -m pytest tests/runtime_neutral/test_research_design_pack_consolidation.py -q
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1
git diff --check
```
````

- [ ] **Step 2: Commit governance note**

Run:

```powershell
git add docs\governance\research-design-pack-consolidation-2026-04-29.md
git commit -m "docs: record research design boundary"
```

Expected: commit succeeds.

## Task 6: Run Full Verification And Final Status

**Files:**
- No additional source files expected.

- [ ] **Step 1: Run focused and broad checks**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_research_design_pack_consolidation.py -q
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1
git diff --check
```

Expected:

```text
test_research_design_pack_consolidation.py: all tests pass
vibe-skill-index-routing-audit.ps1: Failed: 0
vibe-pack-regression-matrix.ps1: Failed: 0
vibe-pack-routing-smoke.ps1: Failed: 0
vibe-offline-skills-gate.ps1: PASS
vibe-config-parity-gate.ps1: PASS
git diff --check: no output
```

- [ ] **Step 2: Confirm no physical deletion occurred**

Run:

```powershell
git diff --name-status HEAD~3..HEAD
```

Expected: no `D` entries under `bundled/skills/`.

- [ ] **Step 3: Final status check**

Run:

```powershell
git status --short --branch
git log --oneline -8
```

Expected: worktree is clean. Recent commits include:

```text
docs: record research design boundary
test: cover research design routing boundaries
fix: consolidate research design routing
```

No lockfile commit is expected unless a later implementation intentionally deletes or adds bundled skill directories.
