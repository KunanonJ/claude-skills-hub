# Data-ML Problem-First Consolidation Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 收敛 `data-ml` pack 到问题场景导向的 8 个核心 skills，并产出可审计的问题矩阵证据。

**Architecture:** 扩展现有 ML pruning audit，使它同时输出 `data-ml` problem map；再按 problem map 收敛 `config/pack-manifest.json` 的 `data-ml` candidates、route authority 和 stage assistant。带资产的重叠 skill 不在本计划直接删除目录，只先从 `data-ml` 移出，并在治理文档中记录后续迁移/删除条件。

**Tech Stack:** Python standard library, PowerShell verify gates, JSON config, existing Vibe-Skills bundled skill layout.

---

## 文件分工

- Modify: `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`
  - 增加 `data-ml` 问题类型常量、问题矩阵 dataclass、`audit_data_ml_problem_map()`、`write_data_ml_problem_artifacts()`。
  - `--write-artifacts` 时同时写旧 pruning artifact 和新 problem map artifact。
- Modify: `tests/runtime_neutral/test_ml_skills_pruning_audit.py`
  - 增加 problem-first 审计测试，确认目标保留、移出、合并角色。
- Modify: `config/pack-manifest.json`
  - 将 `data-ml.skill_candidates` 收敛到 8 个。
  - 将 `data-ml.route_authority_candidates` 收敛到 7 个。
  - 将 `data-ml.stage_assistant_candidates` 收敛到 1 个。
- Modify: `config/skill-keyword-index.json`
  - 收紧保留 skill 的关键词边界，避免宽泛 helper 继续抢普通 ML 语义。
- Modify: `config/skill-routing-rules.json`
  - 收紧 `shap`、`aeon`、`ml-data-leakage-guard`、`preprocessing-data-with-automated-pipelines` 等边界。
- Create: `docs/governance/data-ml-problem-first-consolidation-2026-04-27.md`
  - 中文治理证据，说明每个 skill 为什么保留、移出或后续合并。
- Modify: `config/skills-lock.json`
  - 运行 `scripts/verify/vibe-generate-skills-lock.ps1` 刷新。

## 执行边界

- 本计划只治理 `data-ml` pack。
- 本计划先不删除带 scripts/references/assets 的目录。
- 本计划不移动 `ml-stable-baselines3`、`ml-torch-geometric`、`science-timesfm-forecasting` 等相邻 pack。
- 如果验证发现被移出 `data-ml` 的 skill 仍被其他配置强依赖，不强行删除或重定向。

## Task 1: 扩展审计测试

**Files:**
- Modify: `tests/runtime_neutral/test_ml_skills_pruning_audit.py`
- Later implementation target: `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`

- [ ] **Step 1: 添加 problem map import**

在现有 import 中加入：

```python
from vgo_verify.ml_skills_pruning_audit import (
    audit_data_ml_problem_map,
    audit_repository,
    write_artifacts,
    write_data_ml_problem_artifacts,
)
```

- [ ] **Step 2: 写 problem map 行为测试**

添加测试：

```python
    def test_data_ml_problem_map_marks_targets_for_consolidation(self) -> None:
        artifact = audit_data_ml_problem_map(self.root)
        rows = {row.skill_id: row for row in artifact.rows}

        self.assertEqual("keep", rows["scikit-learn"].target_role)
        self.assertEqual("ml_tabular_modeling", rows["scikit-learn"].primary_problem_id)
        self.assertEqual("keep", rows["ml-data-leakage-guard"].target_role)
        self.assertEqual("ml_leakage_audit", rows["ml-data-leakage-guard"].primary_problem_id)

        self.assertEqual("merge-delete-after-migration", rows["training-machine-learning-models"].target_role)
        self.assertEqual("scikit-learn", rows["training-machine-learning-models"].target_owner)
        self.assertTrue(rows["training-machine-learning-models"].delete_allowed_after_migration)
```

- [ ] **Step 3: 写 problem artifact 输出测试**

添加测试：

```python
    def test_problem_artifact_writer_outputs_json_csv_and_markdown(self) -> None:
        artifact = audit_data_ml_problem_map(self.root)
        output_dir = self.root / "outputs" / "skills-audit"
        written = write_data_ml_problem_artifacts(self.root, artifact, output_dir)

        self.assertTrue(written["json"].exists())
        self.assertTrue(written["csv"].exists())
        self.assertTrue(written["markdown"].exists())
        self.assertIn("data-ml-problem-map", written["json"].name)

        csv_text = written["csv"].read_text(encoding="utf-8")
        self.assertIn("skill_id,problem_ids,primary_problem_id", csv_text)
        self.assertIn("training-machine-learning-models", csv_text)

        markdown_text = written["markdown"].read_text(encoding="utf-8")
        self.assertIn("# Data-ML Problem-First Consolidation", markdown_text)
        self.assertIn("## 目标保留", markdown_text)
```

- [ ] **Step 4: 运行测试确认失败**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
```

Expected: fail because `audit_data_ml_problem_map` does not exist yet.

## Task 2: 实现 problem-first audit

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`

- [ ] **Step 1: 添加问题矩阵 dataclass**

在 `AuditArtifact` 之后添加 `ProblemMapRow` 和 `ProblemMapArtifact`，字段包括：

```python
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
```

- [ ] **Step 2: 添加目标配置常量**

新增常量：

```python
DATA_ML_TARGET_SKILLS = {
    "aeon",
    "evaluating-machine-learning-models",
    "exploratory-data-analysis",
    "ml-data-leakage-guard",
    "ml-pipeline-workflow",
    "preprocessing-data-with-automated-pipelines",
    "scikit-learn",
    "shap",
}
```

并为 17 个当前 `data-ml` skills 定义 `DATA_ML_PROBLEM_DECISIONS`，包含 primary problem、target role、owner、overlap、rationale。

- [ ] **Step 3: 添加 asset summary**

实现 `_asset_summary(skill_dir: Path) -> str`，统计 scripts、references、assets 文件数，输出如 `scripts=6; references=1; assets=4`。

- [ ] **Step 4: 添加 `audit_data_ml_problem_map()`**

读取 `pack-manifest.json`，只遍历 `data-ml.skill_candidates`，根据 `DATA_ML_PROBLEM_DECISIONS` 生成 rows。没有 decision 的候选用 `manual-review`，避免静默丢失。

- [ ] **Step 5: 添加 artifact writer**

实现：

```python
def write_data_ml_problem_artifacts(repo_root: Path, artifact: ProblemMapArtifact, output_dir: Path | None = None) -> dict[str, Path]:
```

写出：

```text
data-ml-problem-map.json
data-ml-problem-map.csv
data-ml-problem-consolidation.md
```

- [ ] **Step 6: 让 CLI 写 problem artifacts**

在 `main()` 中，如果 `--write-artifacts` 为真，调用 `write_data_ml_problem_artifacts()`。

- [ ] **Step 7: 运行测试确认通过**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
```

Expected: all tests pass.

## Task 3: 收敛 live data-ml 配置

**Files:**
- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`

- [ ] **Step 1: 修改 `data-ml.skill_candidates`**

替换为：

```json
[
  "aeon",
  "evaluating-machine-learning-models",
  "exploratory-data-analysis",
  "ml-data-leakage-guard",
  "ml-pipeline-workflow",
  "preprocessing-data-with-automated-pipelines",
  "scikit-learn",
  "shap"
]
```

- [ ] **Step 2: 修改 `data-ml.route_authority_candidates`**

替换为：

```json
[
  "aeon",
  "evaluating-machine-learning-models",
  "exploratory-data-analysis",
  "ml-data-leakage-guard",
  "ml-pipeline-workflow",
  "scikit-learn",
  "shap"
]
```

- [ ] **Step 3: 修改 `data-ml.stage_assistant_candidates`**

替换为：

```json
[
  "preprocessing-data-with-automated-pipelines"
]
```

- [ ] **Step 4: 收紧关键词索引**

确保 `scikit-learn`、`shap`、`ml-data-leakage-guard`、`preprocessing-data-with-automated-pipelines` 关键词偏窄；被移出 `data-ml` 的 skill 关键词保留但不新增宽泛“machine learning”词。

- [ ] **Step 5: 收紧 routing rules**

确保：

- `shap` 的 positive keywords 包含 `shap`、`feature attribution`、`model explainability`、`模型解释`。
- `ml-data-leakage-guard` 继续是 coding/review/research canonical。
- `preprocessing-data-with-automated-pipelines` 不 canonical，只作为 stage assistant。
- `statsmodels`、`statistical-analysis`、`umap-learn` 不新增 canonical。

- [ ] **Step 6: 检查 data-ml count**

Run:

```powershell
$m = Get-Content .\config\pack-manifest.json -Raw | ConvertFrom-Json
$p = $m.packs | Where-Object id -eq 'data-ml'
$p.skill_candidates.Count
$p.route_authority_candidates.Count
$p.stage_assistant_candidates.Count
```

Expected:

```text
8
7
1
```

## Task 4: 写治理证据文档

**Files:**
- Create: `docs/governance/data-ml-problem-first-consolidation-2026-04-27.md`

- [ ] **Step 1: 运行 artifact 输出**

Run:

```powershell
.\scripts\verify\vibe-ml-skills-pruning-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs/skills-audit
```

Expected: command passes and writes `data-ml-problem-map.*` files.

- [ ] **Step 2: 写中文治理文档**

文档必须说明：

- 收敛前：`data-ml` 有 17 个 candidates、11 个 route authority、4 个 stage assistant。
- 收敛后：`data-ml` 有 8 个 candidates、7 个 route authority、1 个 stage assistant。
- 保留 8 个 skill 的问题场景。
- 移出 9 个 skill 的原因。
- 哪些目录未删除，因为还需要资产迁移或属于显式工具/统计/可视化场景。

## Task 5: 刷新 lock 并验证

**Files:**
- Modify: `config/skills-lock.json`

- [ ] **Step 1: 刷新 skills lock**

Run:

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected: command passes.

- [ ] **Step 2: 运行验证**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
.\scripts\verify\vibe-ml-skills-pruning-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs/skills-audit
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
```

Expected: all pass, except any known unrelated `skill-metadata-gate` issue is not part of this command set.

- [ ] **Step 3: 提交修改**

Run:

```powershell
git status --short
git add packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py tests/runtime_neutral/test_ml_skills_pruning_audit.py config/pack-manifest.json config/skill-keyword-index.json config/skill-routing-rules.json config/skills-lock.json docs/governance/data-ml-problem-first-consolidation-2026-04-27.md docs/superpowers/plans/2026-04-27-data-ml-problem-first-consolidation.md
git commit -m "feat: consolidate data ml problem routing"
```
