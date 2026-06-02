# Data-ML 物理删除记录

日期：2026-04-28

## 范围

本轮只处理 `data-ml` 里已经退出 live 路由面的 merge/delete 候选目录。目标是减少安装包里的低质量、重复模板型 skill，而不是重新改写 `data-ml` 的主路由分工。

## 已删除目录

| skill 目录 | 接管者 | 删除判断 |
| --- | --- | --- |
| `bundled/skills/data-exploration-visualization` | `exploratory-data-analysis` | 删除。该目录是 EDA/可视化混合教程包；拆分为 EDA owner 和可视化 pack 后，不再拥有独立路由问题。 |
| `bundled/skills/engineering-features-for-machine-learning` | `preprocessing-data-with-automated-pipelines` | 删除。特征工程归入预处理阶段助手。 |
| `bundled/skills/running-clustering-algorithms` | `scikit-learn` | 删除。普通聚类归传统 ML 主 owner。 |
| `bundled/skills/training-machine-learning-models` | `scikit-learn` / `ml-pipeline-workflow` | 删除。通用训练任务拆给传统建模 owner 和端到端流程 owner。 |

## 资产复核

被删除目录里包含示例脚本、notebook、模板和 README 式参考资料。本轮没有复制迁移这些资产，而是判定为可丢弃：保留 owner 已经用更清楚的任务边界覆盖了相同问题，继续复制会把旧模板噪声带回安装包。

| 被删内容类型 | 处理 |
| --- | --- |
| EDA 和绘图 helper 脚本 | 数据理解归 `exploratory-data-analysis`；正式作图归可视化 pack。 |
| 特征工程模板 | 归 `preprocessing-data-with-automated-pipelines`。 |
| K-means/DBSCAN/hierarchical 聚类脚本 | 归 `scikit-learn`。 |
| 通用 train/evaluate/load/save 脚本 | 归 `scikit-learn`、`ml-pipeline-workflow` 和 `evaluating-machine-learning-models`。 |

## Live 引用清理

同步清理了仍指向被删 skill 的 live 引用：

- `config/ml-lifecycle-overlay.json`
- `config/framework-interop-overlay.json`
- `config/capability-catalog.json`
- `README.md`
- `README.zh.md`
- 相邻 ML skill 的边界说明：`bundled/skills/*/SKILL.md`
- `bundled/skills/autonomous-builder/references/skill-scheduling.md`
- `config/skills-lock.json` 重新生成后不再包含这 4 个目录

历史计划、审计和 archived output 仍可保留这些名字，作为旧治理决策的证据；它们不是 live routing 引用。

## 验证目标

删除后至少需要通过以下检查：

```powershell
python -m pytest tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-ml-skills-pruning-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs\skills-audit
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-generate-skills-lock.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
```
