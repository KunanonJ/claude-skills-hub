# Data-ML Problem-First Strong Consolidation Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

日期：2026-04-27

## 1. 目标

本轮只治理 `data-ml` pack。

目标不是继续按 skill 名字做清单整理，而是把治理单位改成“用户问题类型”：

> 先定义 `data-ml` 应该解决哪些机器学习问题，再决定哪些 skill 有资格留下。

强收敛后的 `data-ml` 应该做到：

- pack 内 skill 数量从当前 17 个收敛到 8 个左右。
- 每个保留 skill 都能对应一个清楚的问题场景。
- 同一个问题场景只允许一个主 skill。
- 其他 skill 只能作为阶段助手、窄工具、显式调用对象，或者从 `data-ml` 移出。
- 删除目录前必须先迁移可复用脚本、references 或文案。

## 2. 当前问题

第一轮已经删除 7 个薄模板型 ML stage assistant，删除后审计结果是：

- `delete`: 0
- `merge-into`: 13
- `defer-specialist-review`: 12
- `keep`: 8

这说明“明显可直接删除的空壳”已经清掉，但 `data-ml` 的结构性问题仍在：

- `data-ml` 还有 17 个 skill candidates。
- 其中 11 个是 `route_authority_candidates`，主路由权力过多。
- 多个 skill 覆盖同一段 ML 生命周期，例如训练、评估、EDA、预处理、聚类。
- 一些 skill 有独立价值，但不应该继续留在 `data-ml` 里抢普通 ML 主路由。
- 当前配置还是 skill-first：先有 skill 列表，再尝试判断谁合适。

本轮要改成 problem-first：先看用户问题，再选 skill。

## 3. 范围

本轮只处理 `config/pack-manifest.json` 中的 `data-ml` pack。

直接纳入治理的当前 skill：

```text
aeon
creating-data-visualizations
data-exploration-visualization
engineering-features-for-machine-learning
evaluating-machine-learning-models
exploratory-data-analysis
LQF_Machine_Learning_Expert_Guide
ml-data-leakage-guard
ml-pipeline-workflow
preprocessing-data-with-automated-pipelines
running-clustering-algorithms
scikit-learn
shap
statistical-analysis
statsmodels
training-machine-learning-models
umap-learn
```

本轮可以观察相邻 ML 工具 pack 的冲突，例如 `ml-torch-geometric` 里的命名重复，但不在本轮修改它们。

## 4. 不做什么

本轮不做这些事：

- 不治理全仓所有 skills。
- 不把所有统计、可视化、深度学习、强化学习工具都塞进 `data-ml`。
- 不因为某个 skill 有资料价值就保留它在 `data-ml` 主路由里。
- 不直接删除带有 scripts、references、assets 的 skill。
- 不新增第二套路由系统。
- 不让同一问题类型下多个 skill 平等竞争主路由。

## 5. Problem-First 判断规则

每个 skill 必须回答三个问题：

1. 它解决的用户问题是什么？
2. 这个问题是否属于 `data-ml` 的核心职责？
3. 是否已有更合适的 skill 能解决同一个问题？

处理规则：

- 能独立负责一个核心问题：保留在 `data-ml`。
- 只能负责一个步骤：降级为 stage assistant。
- 只是某个工具或方法：保留为窄工具，触发词必须窄。
- 问题不属于 `data-ml` 核心职责：从 `data-ml` 移出，但不必删除目录。
- 和保留 skill 高度重复：迁移资产后删除或合并。

## 6. `data-ml` 应覆盖的问题类型

强收敛后的 `data-ml` 只覆盖下面 8 类问题。

| problem_id | 用户问题 | 主 skill | 辅助 skill |
|---|---|---|---|
| `ml_workflow_orchestration` | 我要从数据到模型产物做完整机器学习流程 | `ml-pipeline-workflow` | `ml-data-leakage-guard` |
| `ml_tabular_modeling` | 我要训练分类、回归、普通聚类或传统 ML baseline | `scikit-learn` | `evaluating-machine-learning-models` |
| `ml_data_understanding` | 我要先看数据质量、分布、缺失、异常、字段结构 | `exploratory-data-analysis` | `creating-data-visualizations` 迁出后由可视化 pack 接管 |
| `ml_preprocessing_features` | 我要清洗、编码、缩放、转换、构造特征 | `preprocessing-data-with-automated-pipelines` | 迁入 `engineering-features-for-machine-learning` 的可复用内容 |
| `ml_model_evaluation` | 我要判断模型是否可靠、指标是否合适、阈值怎么选 | `evaluating-machine-learning-models` | `ml-data-leakage-guard` |
| `ml_leakage_audit` | 我要检查数据泄漏、训练测试污染、预测时不可用特征 | `ml-data-leakage-guard` | 无 |
| `ml_explainability` | 我要解释模型预测、特征贡献或 SHAP 图 | `shap` | `evaluating-machine-learning-models` |
| `ml_time_series` | 我要做时间序列机器学习、时序分类、时序聚类、时序异常 | `aeon` | `statsmodels` 从 `data-ml` 移出后只在显式统计建模场景使用 |

## 7. 目标保留形态

目标 `data-ml.skill_candidates` 收敛为：

```text
aeon
evaluating-machine-learning-models
exploratory-data-analysis
ml-data-leakage-guard
ml-pipeline-workflow
preprocessing-data-with-automated-pipelines
scikit-learn
shap
```

目标 `route_authority_candidates` 收敛为：

```text
aeon
evaluating-machine-learning-models
exploratory-data-analysis
ml-data-leakage-guard
ml-pipeline-workflow
scikit-learn
shap
```

目标 `stage_assistant_candidates` 收敛为：

```text
preprocessing-data-with-automated-pipelines
```

目标 `defaults_by_task`：

```json
{
  "planning": "ml-pipeline-workflow",
  "research": "scikit-learn",
  "coding": "scikit-learn",
  "review": "evaluating-machine-learning-models"
}
```

说明：

- `shap` 可以作为 route authority，但只允许在模型解释、特征归因、SHAP 明确相关问题中触发。
- `aeon` 可以作为 route authority，但只允许在时间序列 ML 明确相关问题中触发。
- `ml-data-leakage-guard` 是质量门控型主专家，优先用于 review、评估复核和训练流程可信度检查。

## 8. 逐个 Skill 处理建议

| skill | 当前问题 | 处理动作 | 依据 |
|---|---|---|---|
| `ml-pipeline-workflow` | 端到端流程主入口 | 保留 | 对应完整 ML 生命周期，不和具体算法实现抢 coding 默认 |
| `scikit-learn` | 传统 ML 实现主入口 | 保留 | 覆盖分类、回归、聚类、预处理、调参、baseline |
| `exploratory-data-analysis` | 数据理解主入口 | 保留 | 对应数据质量、结构、分布、初步分析 |
| `ml-data-leakage-guard` | 可信度检查主入口 | 保留 | 解决数据泄漏这一独立高风险问题 |
| `evaluating-machine-learning-models` | 评估主入口 | 保留 | 对应指标、阈值、校准、模型比较 |
| `aeon` | 时序 ML 主入口 | 保留 | 时间序列是独立问题类型，普通 `scikit-learn` 不够精确 |
| `shap` | 模型解释工具 | 保留 | 对应可解释性问题，但触发词必须窄 |
| `preprocessing-data-with-automated-pipelines` | 预处理和特征处理阶段助手 | 保留为唯一阶段助手 | 作为清洗、编码、缩放、转换、验证的集中入口 |
| `engineering-features-for-machine-learning` | 和预处理阶段重叠 | 合并后移出或删除 | 迁移可复用脚本、assets、references 到预处理 owner 后再处理目录 |
| `data-exploration-visualization` | 和 EDA、可视化重叠 | 合并后移出或删除 | EDA 归 `exploratory-data-analysis`，普通图表归可视化 pack |
| `training-machine-learning-models` | 和 `scikit-learn`、`ml-pipeline-workflow` 重叠 | 合并后移出或删除 | 训练不是独立 pack 问题，应由传统 ML 或流程 owner 接管 |
| `running-clustering-algorithms` | 和 `scikit-learn` 聚类能力重叠 | 合并后移出或删除 | 聚类是传统 ML 的子问题，除非脚本证明不可替代 |
| `creating-data-visualizations` | 有价值但不是 ML pack 核心 | 从 `data-ml` 移出 | 普通图表应由可视化 pack 接管 |
| `LQF_Machine_Learning_Expert_Guide` | 容易覆盖普通 ML 路由 | 从 `data-ml` 移出，保留显式/评审型使用 | 价值在批判式方案评审，不应做普通 ML 主入口 |
| `statistical-analysis` | 统计分析价值高，但不是 ML pack 核心 | 从 `data-ml` 移出 | 归统计/科研设计场景，不抢 ML 主路由 |
| `statsmodels` | 统计建模价值高，但和 ML pack 边界混 | 从 `data-ml` 移出 | 保留显式统计建模/ARIMA/计量场景，不做普通 ML 候选 |
| `umap-learn` | 专用降维工具 | 从 `data-ml` 移出，保留显式工具调用 | 只有用户明确要 UMAP、流形学习或 UMAP 可视化时触发 |

## 9. 资产迁移规则

带有 `scripts/`、`references/`、`assets/` 的 skill 不能直接删除。

删除或合并前必须做三步：

1. 列出可复用资产。
2. 判断资产是否比目标 owner 现有内容更强。
3. 迁移或记录不迁移理由。

重点资产迁移方向：

| 来源 skill | 迁移方向 |
|---|---|
| `engineering-features-for-machine-learning` | `preprocessing-data-with-automated-pipelines` |
| `data-exploration-visualization` | `exploratory-data-analysis` 或可视化 pack |
| `training-machine-learning-models` | `scikit-learn` 或 `ml-pipeline-workflow` |
| `running-clustering-algorithms` | `scikit-learn` |

如果迁移后来源 skill 没有独立问题场景，也没有独立资产，就可以进入删除候选。

## 10. 路由设计

路由应先判断 problem_id，再选择 skill。

逻辑顺序：

1. 根据用户请求识别问题类型。
2. 每个问题类型只给一个主 skill。
3. 如果请求明确点名工具，例如 `SHAP`、`UMAP`、`aeon`，允许窄工具直接命中。
4. 如果请求是宽泛“做机器学习模型”，默认给 `scikit-learn` 或 `ml-pipeline-workflow`，不让训练、评估、聚类、可视化 helper 抢主路由。
5. 如果请求是“帮我检查这个模型是否靠谱”，优先给 `evaluating-machine-learning-models` 和 `ml-data-leakage-guard`。

## 11. 审计产物

实施前需要生成一份新的问题场景审计表。

建议输出：

```text
outputs/skills-audit/data-ml-problem-map.json
outputs/skills-audit/data-ml-problem-map.csv
outputs/skills-audit/data-ml-problem-consolidation.md
docs/governance/data-ml-problem-first-consolidation-2026-04-27.md
```

建议字段：

| 字段 | 含义 |
|---|---|
| `skill_id` | skill 名称 |
| `problem_ids` | 它能解决的问题类型 |
| `primary_problem_id` | 它最适合主导的问题 |
| `overlap_with` | 重叠 skill |
| `unique_assets` | 独有脚本、references、assets |
| `target_role` | keep、stage-assistant、move-out、merge-delete |
| `target_owner` | 合并或接管对象 |
| `routing_change` | pack-manifest 和 routing rules 需要怎么改 |
| `delete_allowed_after_migration` | 资产迁移后是否允许删除 |
| `risk_level` | low、medium、high |

## 12. 验证要求

实施后至少运行：

```powershell
python -m pytest tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
.\scripts\verify\vibe-ml-skills-pruning-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs/skills-audit
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
```

如果 `skill-metadata-gate` 仍因既有无关问题失败，必须在结果里明确区分，不把它伪装成本轮失败。

## 13. 成功标准

本轮完成后应满足：

- `data-ml.skill_candidates` 收敛到 8 个左右。
- `data-ml.route_authority_candidates` 不再超过 7 个。
- 每个保留 skill 都能映射到一个明确 problem_id。
- `data-ml` 中没有两个 skill 同时主导同一问题类型。
- 被移出 `data-ml` 的 skill 目录不自动删除，除非资产迁移和证据表都支持删除。
- 审计报告能用普通中文解释“为什么这个 skill 留下/移出/合并/删除”。

## 14. 实施顺序

1. 扩展审计工具，增加 problem-first 字段和问题矩阵输出。
2. 生成 `data-ml` 问题场景审计报告。
3. 人工复核带资产的重叠 skill。
4. 迁移可复用脚本、references、assets。
5. 修改 `config/pack-manifest.json`，收敛 `data-ml` membership 和 roles。
6. 同步 `skill-keyword-index.json` 和 `skill-routing-rules.json` 的关键词边界。
7. 删除已经完成迁移且没有独立问题场景的 skill 目录。
8. 刷新 `config/skills-lock.json`。
9. 运行验证 gate，并更新治理文档。
