# ML Skills Pruning Audit Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 先做一套不删文件的 ML skills 审计工具，找出重复、很薄、模板化的通用 ML skills，并在删除前产出清楚的证据清单。

**Architecture:** 在 `verification-core` 里加一个能读仓库配置的 Python 审计模块，再按现有 runtime-neutral runner 模式暴露出来，最后用 PowerShell gate 包一层。第一阶段只产出审计文件和人能看懂的候选文档；删除 skill 目录必须等作者确认具体 skill ID 后再做。

**Tech Stack:** Python standard library, PowerShell gate wrappers, `pytest`/`unittest`, existing JSON config files under `config/`, bundled skill folders under `bundled/skills/`.

---

## 先说人话

这个计划先做三件事：

1. 找出所有 ML 相关的内置 skills。它不只看 `data-ml` pack，如果别的 pack 里有明显 ML 相关的 skill，也会纳入。
2. 给每个 skill 打分，但分数必须能解释：行数、有没有 scripts、有没有 references、当前路由角色、质量分、重复分、接管 skill、风险。
3. 生成一份作者能直接看的审计报告。作者确认前，不删目录。

这个计划不删除 skill 目录。这是故意设置的边界。你要求“深入阅读和比较再动刀子”，所以第一步只能先拿出具体证据，不能猜着删。

## 文件分工

- Create: `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`
  - 负责发现 ML skills、打分、写 CSV/Markdown/JSON 审计文件，以及提供 CLI。
- Create: `scripts/verify/runtime_neutral/ml_skills_pruning_audit.py`
  - 很薄的一层 runtime-neutral wrapper，写法跟现有 `release_notes_quality.py` 对齐。
- Create: `scripts/verify/vibe-ml-skills-pruning-audit-gate.ps1`
  - PowerShell 入口，通过 `Get-VgoPythonCommand` 调 Python runner。
- Create: `tests/runtime_neutral/test_ml_skills_pruning_audit.py`
  - 用小型假仓库测试 ML 发现、评分、专业工具暂缓、审计文件写出。
- Create after running the audit: `docs/governance/ml-skills-pruning-candidates-2026-04-27.md`
  - 根据审计结果整理出来的作者复核文档，中文说明，并写清楚迁移映射。

## 执行边界

本计划执行到“候选证据文档创建并提交”为止。不要在这个计划里删除 `bundled/skills/` 目录。后续真正删除时，必须以作者批准过的证据文档为准。

## Task 1: 先写审计测试

**Files:**
- Create: `tests/runtime_neutral/test_ml_skills_pruning_audit.py`
- Later implementation target: `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`

- [ ] **Step 1: 写一个会先失败的测试**

Create `tests/runtime_neutral/test_ml_skills_pruning_audit.py` with this content:

```python
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from vgo_verify.ml_skills_pruning_audit import audit_repository, write_artifacts


class MlSkillsPruningAuditTests(unittest.TestCase):
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

    def _write_skill(self, skill_id: str, description: str, body: str, *, scripts: bool = False, references: bool = False) -> None:
        self._write(
            f"bundled/skills/{skill_id}/SKILL.md",
            "---\n"
            f"name: {skill_id}\n"
            f"description: {description}\n"
            "---\n\n"
            f"# {skill_id}\n\n"
            f"{body}\n",
        )
        if scripts:
            self._write(f"bundled/skills/{skill_id}/scripts/run.py", "print('ok')\n")
        if references:
            self._write(f"bundled/skills/{skill_id}/references/guide.md", "# Guide\n\nConcrete guidance.\n")

    def _write_fixture_repo(self) -> None:
        self._write_json(
            "config/pack-manifest.json",
            {
                "packs": [
                    {
                        "id": "data-ml",
                        "skill_candidates": [
                            "scikit-learn",
                            "anomaly-detector",
                            "training-machine-learning-models",
                            "shap",
                        ],
                        "route_authority_candidates": [
                            "scikit-learn",
                            "training-machine-learning-models",
                        ],
                        "stage_assistant_candidates": [
                            "anomaly-detector",
                        ],
                        "defaults_by_task": {
                            "planning": "scikit-learn",
                            "coding": "scikit-learn",
                        },
                    },
                    {
                        "id": "ai-llm",
                        "skill_candidates": [
                            "transformers",
                        ],
                        "defaults_by_task": {
                            "coding": "transformers",
                        },
                    },
                ]
            },
        )
        self._write_json(
            "config/skill-keyword-index.json",
            {
                "skills": {
                    "scikit-learn": {"keywords": ["machine learning", "sklearn", "classification"]},
                    "anomaly-detector": {"keywords": ["anomaly detection", "outlier", "machine learning"]},
                    "training-machine-learning-models": {"keywords": ["train model", "machine learning"]},
                    "shap": {"keywords": ["shap", "feature importance", "explain model"]},
                    "transformers": {"keywords": ["transformers", "fine tune model", "deep learning"]},
                }
            },
        )
        self._write_json(
            "config/skill-routing-rules.json",
            {
                "skills": {
                    "scikit-learn": {
                        "task_allow": ["coding", "research"],
                        "positive_keywords": ["sklearn", "classification"],
                        "negative_keywords": [],
                        "canonical_for_task": ["traditional_ml"],
                    },
                    "anomaly-detector": {
                        "task_allow": ["coding"],
                        "positive_keywords": ["anomaly"],
                        "negative_keywords": [],
                        "canonical_for_task": [],
                    },
                    "training-machine-learning-models": {
                        "task_allow": ["coding"],
                        "positive_keywords": ["train model"],
                        "negative_keywords": [],
                        "canonical_for_task": [],
                    },
                    "shap": {
                        "task_allow": ["review"],
                        "positive_keywords": ["shap"],
                        "negative_keywords": [],
                        "canonical_for_task": ["explainability"],
                    },
                    "transformers": {
                        "task_allow": ["coding"],
                        "positive_keywords": ["transformers"],
                        "negative_keywords": [],
                        "canonical_for_task": ["deep_learning"],
                    },
                }
            },
        )
        self._write_skill(
            "scikit-learn",
            "Traditional machine-learning owner for sklearn models.",
            "\n".join(
                [
                    "Use this for scikit-learn classification, regression, pipelines, cross validation, metrics, and reproducible model training.",
                    "Do not use it as the owner for deep-learning framework internals.",
                    "It should absorb generic training and evaluation templates when those templates add no independent workflow.",
                ]
                * 8
            ),
            references=True,
        )
        self._write_skill(
            "anomaly-detector",
            "Generic anomaly detector helper.",
            "Use this skill for anomaly detection. Pick a method, run it, and report anomalies.",
        )
        self._write_skill(
            "training-machine-learning-models",
            "Generic ML training helper.",
            "Use this skill for training machine-learning models. Split data, train, evaluate, and report results.",
        )
        self._write_skill(
            "shap",
            "SHAP explainability tool skill.",
            "Use this when the request explicitly needs SHAP values or model explanations.",
        )
        self._write_skill(
            "transformers",
            "Transformers deep-learning framework skill.",
            "Use this for transformer model fine-tuning, tokenizers, inference, and deep-learning workflows.",
            scripts=True,
        )

    def test_audit_marks_generic_template_ml_helpers_as_delete_candidates(self) -> None:
        artifact = audit_repository(self.root)
        rows = {row.skill_id: row for row in artifact.rows}

        self.assertEqual("delete", rows["anomaly-detector"].recommended_action)
        self.assertEqual("scikit-learn", rows["anomaly-detector"].replacement_skill)
        self.assertLessEqual(rows["anomaly-detector"].quality_score, 2)
        self.assertGreaterEqual(rows["anomaly-detector"].duplication_score, 4)
        self.assertEqual("low", rows["anomaly-detector"].risk_level)

        self.assertEqual("delete", rows["training-machine-learning-models"].recommended_action)
        self.assertEqual("scikit-learn", rows["training-machine-learning-models"].replacement_skill)

    def test_audit_keeps_or_defers_owner_and_specialist_skills(self) -> None:
        artifact = audit_repository(self.root)
        rows = {row.skill_id: row for row in artifact.rows}

        self.assertEqual("keep", rows["scikit-learn"].recommended_action)
        self.assertEqual("主专家", rows["scikit-learn"].category)
        self.assertGreaterEqual(rows["scikit-learn"].quality_score, 4)

        self.assertEqual("defer-specialist-review", rows["shap"].recommended_action)
        self.assertEqual("工具型", rows["shap"].category)
        self.assertEqual("medium", rows["shap"].risk_level)

        self.assertEqual("defer-specialist-review", rows["transformers"].recommended_action)
        self.assertEqual("工具型", rows["transformers"].category)
        self.assertTrue(rows["transformers"].has_scripts)

    def test_artifact_writer_outputs_json_csv_and_markdown(self) -> None:
        artifact = audit_repository(self.root)
        output_dir = self.root / "outputs" / "skills-audit"
        written = write_artifacts(self.root, artifact, output_dir)

        self.assertTrue(written["json"].exists())
        self.assertTrue(written["csv"].exists())
        self.assertTrue(written["markdown"].exists())

        csv_text = written["csv"].read_text(encoding="utf-8")
        self.assertIn("skill_id,category,current_pack,current_role", csv_text)
        self.assertIn("anomaly-detector", csv_text)

        markdown_text = written["markdown"].read_text(encoding="utf-8")
        self.assertIn("# ML Skills Pruning Audit", markdown_text)
        self.assertIn("## 删除候选", markdown_text)
        self.assertIn("anomaly-detector", markdown_text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 跑测试，确认它先失败**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
```

预期结果：

```text
ModuleNotFoundError: No module named 'vgo_verify.ml_skills_pruning_audit'
```

- [ ] **Step 3: 只有项目允许红灯提交时，才提交失败测试**

本仓库默认不要提交红灯状态。先保留测试文件，等 Task 2 通过后再一起提交。

## Task 2: 实现不删文件的审计模块

**Files:**
- Create: `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`
- Test: `tests/runtime_neutral/test_ml_skills_pruning_audit.py`

- [ ] **Step 1: 创建审计模块**

Create `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py` with these public entry points:

```python
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ML_KEYWORDS = {
    "machine learning", "ml", "sklearn", "scikit", "classification", "regression",
    "clustering", "feature", "training", "model evaluation", "cross validation",
    "deep learning", "transformers", "time series", "forecast", "anomaly",
    "机器学习", "模型", "分类", "回归", "聚类", "特征", "训练", "预测", "评估",
}

SPECIALIST_DEFER_SKILLS = {
    "shap", "umap-learn", "statsmodels", "tensorboard", "weights-and-biases",
    "transformers", "torch-geometric", "stable-baselines3", "timesfm-forecasting",
    "scikit-survival", "deepchem", "torchdrug",
}

OWNER_SKILLS = {
    "scikit-learn",
    "ml-pipeline-workflow",
    "exploratory-data-analysis",
    "ml-data-leakage-guard",
    "LQF_Machine_Learning_Expert_Guide",
    "statistical-analysis",
    "statsmodels",
    "aeon",
}

DEFAULT_REPLACEMENTS = {
    "anomaly-detector": "scikit-learn",
    "confusion-matrix-generator": "scikit-learn",
    "correlation-analyzer": "exploratory-data-analysis",
    "data-normalization-tool": "preprocessing-data-with-automated-pipelines",
    "data-quality-checker": "exploratory-data-analysis",
    "engineering-features-for-machine-learning": "preprocessing-data-with-automated-pipelines",
    "evaluating-machine-learning-models": "scikit-learn",
    "feature-importance-analyzer": "shap",
    "regression-analysis-helper": "scikit-learn",
    "running-clustering-algorithms": "scikit-learn",
    "training-machine-learning-models": "scikit-learn",
}


@dataclass(frozen=True)
class AuditRow:
    skill_id: str
    category: str
    current_pack: str
    current_role: str
    lines: int
    has_scripts: bool
    has_references: bool
    quality_score: int
    duplication_score: int
    recommended_action: str
    replacement_skill: str
    deletion_reason: str
    config_cleanup_required: str
    risk_level: str


@dataclass(frozen=True)
class AuditArtifact:
    generated_at: str
    repo_root: str
    rows: list[AuditRow]

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "repo_root": self.repo_root,
            "summary": {
                "ml_skill_count": len(self.rows),
                "delete_candidate_count": sum(1 for row in self.rows if row.recommended_action == "delete"),
                "specialist_deferred_count": sum(1 for row in self.rows if row.recommended_action == "defer-specialist-review"),
            },
            "rows": [asdict(row) for row in self.rows],
        }
```

The module must also define these functions with the exact names used by the tests:

```python
def audit_repository(repo_root: Path) -> AuditArtifact:
    ...

def write_artifacts(repo_root: Path, artifact: AuditArtifact, output_dir: Path | None = None) -> dict[str, Path]:
    ...

def main(argv: list[str] | None = None) -> int:
    ...
```

实现规则：

- Read `config/pack-manifest.json`, `config/skill-keyword-index.json`, and `config/skill-routing-rules.json`.
- Read each candidate `bundled/skills/<skill_id>/SKILL.md`.
- Treat a skill as ML-related if any of these is true:
  - it belongs to the `data-ml` pack;
  - its skill ID, keywords, route metadata, or `SKILL.md` text contains ML keywords;
  - it is in `SPECIALIST_DEFER_SKILLS`.
- Compute `current_role` from `pack-manifest.json`:
  - `route_authority` if listed in `route_authority_candidates`;
  - `stage_assistant` if listed in `stage_assistant_candidates`;
  - `default` if used by `defaults_by_task`;
  - `candidate` otherwise.
- Compute `has_scripts` by checking for `scripts/` with at least one file.
- Compute `has_references` by checking for `references/` with at least one file.
- Score quality from visible evidence:
  - start at `1`;
  - add `1` when `SKILL.md` has at least 80 lines or 3500 characters;
  - add `1` when it has scripts;
  - add `1` when it has references;
  - add `1` when it is an owner skill;
  - cap at `5`.
- Score duplication:
  - `5` when the skill is in `DEFAULT_REPLACEMENTS` and has no scripts or references;
  - `4` when it is a stage assistant with short prose and a replacement owner;
  - `3` when it overlaps ML keywords but has some independent evidence;
  - `1` for owner skills and specialist tools.
- Assign actions:
  - `keep` for owner skills with quality score at least `4`;
  - `defer-specialist-review` for `SPECIALIST_DEFER_SKILLS`;
  - `delete` only when `quality_score <= 2`, `duplication_score >= 4`, no scripts, no references, replacement exists, and risk is not `high`;
  - `merge-into` for weak but not delete-safe generic helpers;
  - `keep` for everything else.
- Write artifacts with stable names:
  - `ml-skills-pruning-audit.json`
  - `ml-skills-pruning-candidates.csv`
  - `ml-skills-pruning-candidates.md`

- [ ] **Step 2: 跑聚焦测试**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
```

预期结果：

```text
3 passed
```

- [ ] **Step 3: 提交审计模块和测试**

Run:

```powershell
git add packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py tests/runtime_neutral/test_ml_skills_pruning_audit.py
git commit -m "feat: add ML skills pruning audit"
```

预期结果：一个提交，只包含审计模块和测试文件。

## Task 3: 增加 runtime-neutral 和 PowerShell gate 入口

**Files:**
- Create: `scripts/verify/runtime_neutral/ml_skills_pruning_audit.py`
- Create: `scripts/verify/vibe-ml-skills-pruning-audit-gate.ps1`
- Test: `tests/runtime_neutral/test_ml_skills_pruning_audit.py`

- [ ] **Step 1: 增加 runtime-neutral Python wrapper**

Create `scripts/verify/runtime_neutral/ml_skills_pruning_audit.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from runpy import run_path

ensure_verification_core_src_on_path = run_path(str(Path(__file__).with_name("_bootstrap.py")))["ensure_verification_core_src_on_path"]
ensure_verification_core_src_on_path()

from vgo_verify.ml_skills_pruning_audit import AuditArtifact, AuditRow, audit_repository, main, write_artifacts

__all__ = [
    "AuditArtifact",
    "AuditRow",
    "audit_repository",
    "main",
    "write_artifacts",
]

if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 增加 PowerShell gate**

Create `scripts/verify/vibe-ml-skills-pruning-audit-gate.ps1`:

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

$runnerPath = Join-Path $RepoRoot 'scripts/verify/runtime_neutral/ml_skills_pruning_audit.py'
if (-not (Test-Path -LiteralPath $runnerPath)) {
    throw "ML skills pruning audit runner missing: $runnerPath"
}

. (Join-Path $RepoRoot 'scripts/common/vibe-governance-helpers.ps1')
$pythonInvocation = Get-VgoPythonCommand

$args = @(
    $runnerPath,
    '--repo-root', $RepoRoot
)
if ($WriteArtifacts) {
    $args += '--write-artifacts'
}
if ($OutputDirectory) {
    $args += @('--output-directory', $OutputDirectory)
}

& $pythonInvocation.host_path @($pythonInvocation.prefix_arguments) @args
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    throw "vibe-ml-skills-pruning-audit-gate failed with exit code $exitCode"
}

Write-Host '[PASS] vibe-ml-skills-pruning-audit-gate passed' -ForegroundColor Green
```

- [ ] **Step 3: 增加一个 wrapper smoke test**

Append this test to `tests/runtime_neutral/test_ml_skills_pruning_audit.py`:

```python
    def test_runtime_neutral_wrapper_exposes_main(self) -> None:
        wrapper = Path(__file__).resolve().parents[2] / "scripts" / "verify" / "runtime_neutral" / "ml_skills_pruning_audit.py"
        text = wrapper.read_text(encoding="utf-8")
        self.assertIn("from vgo_verify.ml_skills_pruning_audit import", text)
        self.assertIn("raise SystemExit(main())", text)
```

- [ ] **Step 4: 跑聚焦测试和 gate**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
.\scripts\verify\vibe-ml-skills-pruning-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs/skills-audit
```

预期结果：

```text
4 passed
[PASS] vibe-ml-skills-pruning-audit-gate passed
```

- [ ] **Step 5: 提交入口文件**

Run:

```powershell
git add scripts/verify/runtime_neutral/ml_skills_pruning_audit.py scripts/verify/vibe-ml-skills-pruning-audit-gate.ps1 tests/runtime_neutral/test_ml_skills_pruning_audit.py
git commit -m "feat: expose ML skills pruning audit gate"
```

预期结果：一个提交，只包含 wrapper、gate 和 wrapper 测试。

## Task 4: 在真实仓库生成审计文件

**Files:**
- Generated: `outputs/skills-audit/ml-skills-pruning-audit.json`
- Generated: `outputs/skills-audit/ml-skills-pruning-candidates.csv`
- Generated: `outputs/skills-audit/ml-skills-pruning-candidates.md`

- [ ] **Step 1: 在真实仓库跑审计**

Run:

```powershell
.\scripts\verify\vibe-ml-skills-pruning-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs/skills-audit
```

预期结果：

```text
[PASS] vibe-ml-skills-pruning-audit-gate passed
```

- [ ] **Step 2: 查看删除候选**

Run:

```powershell
Import-Csv outputs/skills-audit/ml-skills-pruning-candidates.csv |
  Where-Object { $_.recommended_action -eq 'delete' } |
  Select-Object skill_id,current_pack,current_role,quality_score,duplication_score,replacement_skill,risk_level
```

预期结果：输出一张删除候选表，每一行都有非空 `replacement_skill`，并且 `risk_level` 不是 `high`。

- [ ] **Step 3: 查看暂缓的专业工具型 skills**

Run:

```powershell
Import-Csv outputs/skills-audit/ml-skills-pruning-candidates.csv |
  Where-Object { $_.recommended_action -eq 'defer-specialist-review' } |
  Select-Object skill_id,current_pack,current_role,replacement_skill,risk_level
```

预期结果：`shap`、`umap-learn`、`statsmodels`、`transformers` 或类似工具绑定型 skills 被标记为暂缓，而不是第一轮删除。

## Task 5: 写作者复核用的证据文档

**Files:**
- Create: `docs/governance/ml-skills-pruning-candidates-2026-04-27.md`
- Source artifacts: `outputs/skills-audit/ml-skills-pruning-candidates.csv`, `outputs/skills-audit/ml-skills-pruning-candidates.md`

- [ ] **Step 1: 创建可读的复核文档**

Create `docs/governance/ml-skills-pruning-candidates-2026-04-27.md` with this structure:

```markdown
# ML Skills 第一轮瘦身候选清单

日期：2026-04-27

## 结论先看

本文件只是一份删除前证据清单，不是删除补丁。

- `delete`：建议第一轮删除，但仍需作者确认。
- `merge-into`：有重复，但证据还不足以直接删。
- `defer-specialist-review`：专业工具型 skill，本轮不删。
- `keep`：保留。

## 删除候选

从 `outputs/skills-audit/ml-skills-pruning-candidates.csv` 中复制 `recommended_action=delete` 的行，并保留这些列：

| skill_id | 当前 pack | 当前角色 | 质量分 | 重复分 | 接管 skill | 风险 | 删除理由 |
|---|---|---:|---:|---:|---|---|---|

## 合并但暂不删除

从 CSV 中复制 `recommended_action=merge-into` 的行。这里的 skill 不直接删，只作为下一轮人工比较对象。

## 专业工具型暂缓

从 CSV 中复制 `recommended_action=defer-specialist-review` 的行。这里要明确写一句：这些 skill 第一轮不删。

## 迁移映射

对每个 `delete` 行写成：

| 原 skill | 删除后使用 |
|---|---|

## 人工复核记录

每个 `delete` 候选必须人工打开 `bundled/skills/<skill_id>/SKILL.md` 看一遍，并记录：

| skill_id | 是否读过 SKILL.md | 是否有 scripts | 是否有 references | 是否同意删除 | 复核备注 |
|---|---|---:|---:|---:|---|

## 作者确认区

只有作者确认后，下一步才允许删除目录。
```

然后用生成出来的 CSV 填表。文字要短、直接。CSV 里没有的候选，不允许凭感觉加进去。

- [ ] **Step 2: 对每个删除候选查全仓引用**

Run this command after replacing `<skill-id>` with each delete candidate from the CSV:

```powershell
rg -n "<skill-id>" bundled config docs tests scripts packages
```

预期结果：每个引用都能归到下面几类之一：

- skill 自己的目录；
- 作者批准后需要清理的路由配置；
- 需要写迁移说明的文档；
- 作者批准后需要更新的测试或 fixture。

- [ ] **Step 3: 提交证据文档**

Run:

```powershell
git add docs/governance/ml-skills-pruning-candidates-2026-04-27.md
git commit -m "docs: add ML skills pruning evidence list"
```

预期结果：一个提交，只包含作者复核证据文档。

## Task 6: 验证这次审计工作

**Files:**
- Audit code and tests from Tasks 1-3
- Evidence document from Task 5

- [ ] **Step 1: 跑聚焦 Python 测试**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
```

预期结果：

```text
4 passed
```

- [ ] **Step 2: 跑这次工作相关的现有治理 gate**

Run:

```powershell
.\scripts\verify\vibe-ml-skills-pruning-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs/skills-audit
.\scripts\verify\vibe-built-in-skill-governance-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
```

预期结果：

```text
[PASS] vibe-ml-skills-pruning-audit-gate passed
Pack routing smoke checks passed.
[PASS] offline skill closure gate passed.
```

built-in governance gate 也应该没有 autonomous wording 失败项。

- [ ] **Step 3: 检查有没有误删目录**

Run:

```powershell
git status --short
git diff --name-status HEAD
```

预期结果：这个计划里不能出现被删除的 `bundled/skills/<skill-id>/` 目录。

## Task 7: 停下来等作者确认

**Files:**
- Review: `docs/governance/ml-skills-pruning-candidates-2026-04-27.md`

- [ ] **Step 1: 把证据清单汇报给作者**

Report these items in Chinese:

```text
1. 发现了多少个 ML 相关 skill。
2. 其中多少个建议第一轮删除。
3. 哪些专业工具型 skill 被暂缓，不删。
4. 每个删除候选由哪个 skill 接管。
5. 本次没有删除任何目录。
```

- [ ] **Step 2: 请求确认具体删除名单**

请作者确认 `docs/governance/ml-skills-pruning-candidates-2026-04-27.md` 里的具体删除名单。

除非作者明确确认这些具体 skill ID，否则不能进入删除。

## 后续删除补丁边界

作者确认后，再创建一个单独的删除补丁，并且只处理作者确认过的具体 skill ID。那个补丁应该：

- delete only approved `bundled/skills/<skill-id>/` directories;
- remove approved IDs from `config/pack-manifest.json`;
- remove approved IDs from `config/skill-keyword-index.json`;
- remove approved IDs from `config/skill-routing-rules.json`;
- regenerate `config/skills-lock.json` with `.\scripts\verify\vibe-generate-skills-lock.ps1`;
- run `.\scripts\verify\vibe-offline-skills-gate.ps1`;
- run `.\scripts\verify\vibe-pack-routing-smoke.ps1`;
- run `.\scripts\verify\vibe-built-in-skill-governance-gate.ps1 -WriteArtifacts`;
- search the repo for each deleted skill ID and clean any stale references.

删除补丁不能新增 retired 占位目录。作者批准过的 replacement mapping 就是迁移说明。

## 自检

- 规格覆盖：计划覆盖了 ML-wide 发现、第一轮通用模板型过滤、专业工具暂缓、评分字段、证据文件、迁移映射和审批边界。
- 占位检查：在审计结果出来前，不猜删除 ID。
- 类型一致：测试和实现都使用 `AuditRow`、`AuditArtifact`、`audit_repository` 和 `write_artifacts`。
- 安全性：先产出证据，再谈删除；本计划明确停在破坏性操作之前。
