# ML Skills 激进瘦身设计

日期：2026-04-27

## 1. 目标

本轮目标是整治 Vibe-Skills 内置 ML 相关 skills。

当前问题不是“缺少更多 skills”，而是：

- ML 相关 skills 太多。
- 有些 skills 内容很薄，像模板换名。
- 多个 skills 解决同一类问题，边界不清。
- 路由时少数 skills 经常占主导，其他相近 skills 很少被触发。
- pack 里候选太多，导致路由判断变复杂，质量也不稳定。

本轮要做的是激进瘦身：

- 删除明显重复、低质量、没有独立价值的通用 ML skills。
- 保留真正有独立价值的主专家和专用工具 skills。
- 删除前必须先做深读比较，产出证据清单和迁移映射。
- 用户确认删除清单后，正式删除目录并同步清理配置。

一句话原则：

> 先审计，再删除；留下来的每个 skill 都要有明确职责。

## 2. 范围

本轮范围是所有 ML 相关 skills，不只限于 `data-ml` pack。

包括但不限于：

- 通用机器学习流程
- 数据分析与 EDA
- 训练、评估、特征工程
- 数据泄漏检查
- 可解释性与降维
- 统计建模
- 时间序列建模
- MLOps 与实验追踪
- 深度学习、图学习、强化学习
- 科学、生物、化学场景里的 ML 工具

但是第一刀只删除通用模板型 ML skills。

专用工具或专业框架型 skills 第一轮不直接删除，只进入第二轮专项评估。例如：

- `shap`
- `umap-learn`
- `statsmodels`
- `tensorboard`
- `weights-and-biases`
- `transformers`
- `torch-geometric`
- `stable-baselines3`
- `timesfm-forecasting`
- `scikit-survival`
- `deepchem`
- `torchdrug`

这些 skills 可以在第一轮被标记为“保留但需要路由调整”，但不作为第一刀删除对象。

## 3. 不做什么

本轮不做这些事：

- 不凭名字相似直接删除。
- 不只看关键词重复就删除。
- 不删除专用工具型 skill，除非进入后续专项评估。
- 不把低质量 skill 只标记 retired 但继续留在安装包里。
- 不新建第二套路由系统。
- 不让所有同类 skills 平等竞争主路由。

## 4. 核心判断标准

一个 skill 进入删除候选，必须同时满足下面条件：

1. 它是通用模板型 ML skill。
2. 内容质量低，通常表现为说明很短、泛泛而谈、缺少实际流程。
3. 和一个或多个更强 skill 高度重复。
4. 没有不可替代的脚本、references、数据处理流程或专家方法论。
5. 不是专用工具或专业框架绑定 skill。
6. 删除后有明确接管对象。
7. 删除不会破坏当前 runtime、安装或路由基本闭环。

如果不能满足这些条件，就不能直接删除。

## 5. Skill 分层

审计时把每个 ML skill 分成五类。

### 5.1 主专家

可以主导一类任务。

例子：

- `scikit-learn`：通用传统 ML 实现。
- `ml-pipeline-workflow`：端到端 ML 流程规划。
- `exploratory-data-analysis`：数据探索主流程。
- `ml-data-leakage-guard`：泄漏检查主专家。
- `LQF_Machine_Learning_Expert_Guide`：批判式 ML 方案评估。

主专家数量应该少。

一个 pack 通常只应有 1 到 3 个主专家。

### 5.2 阶段助手

只负责某个步骤，不抢主导权。

例子：

- 混淆矩阵分析
- 单独做特征重要性解释
- 单独做数据归一化检查
- 单独做聚类结果辅助分析

阶段助手可以保留，但必须有清楚边界。

如果一个阶段助手内容很薄，又完全能被主专家覆盖，就进入删除候选。

### 5.3 工具型 skill

绑定具体工具、库或框架。

例子：

- `shap`
- `umap-learn`
- `tensorboard`
- `weights-and-biases`
- `transformers`
- `torch-geometric`

工具型 skill 第一轮不直接删除。

但如果它在路由里不应该当主专家，就要降级为工具型或阶段助手。

### 5.4 参考型 skill

有一些资料价值，但不适合参与自动路由。

这类 skill 第一轮可以从路由候选中移除。

如果它同时质量低、重复高、无独立资料价值，就进入删除候选。

### 5.5 删除候选

这类 skill 应该从 `bundled/skills` 中删除。

删除前必须记录：

- 删除理由
- 重复对象
- 接管 skill
- 需要清理的配置
- 风险等级

## 6. 审计产物

正式删除前必须先生成审计表。

建议文件：

- `outputs/skills-audit/ml-skills-pruning-candidates.csv`
- `outputs/skills-audit/ml-skills-pruning-candidates.md`

字段：

| 字段 | 含义 |
|---|---|
| `skill_id` | skill 名称 |
| `category` | 主专家、阶段助手、工具型、参考型、删除候选 |
| `current_pack` | 当前所在 pack |
| `current_role` | 当前路由角色 |
| `lines` | `SKILL.md` 行数 |
| `has_scripts` | 是否有脚本 |
| `has_references` | 是否有 references |
| `quality_score` | 质量评分 |
| `duplication_score` | 重复度评分 |
| `recommended_action` | keep、delete、merge-into、defer-specialist-review |
| `replacement_skill` | 删除后由谁接管 |
| `deletion_reason` | 删除原因 |
| `config_cleanup_required` | 需要清理哪些配置 |
| `risk_level` | low、medium、high |

这张表是删除前的审核依据。

没有进入这张表的 skill，不允许在第一轮删除。

## 7. 评分方法

### 7.1 质量评分

质量评分看这些证据：

- `SKILL.md` 是否有清楚的适用场景。
- 是否写清楚不适用场景。
- 是否有 scripts。
- 是否有 references。
- 是否有真实流程，而不是泛泛说明。
- 是否能独立指导一次任务。
- 是否和相邻 skill 有清楚边界。

建议 0 到 5 分：

- 5 分：强 owner，边界清楚，有脚本或参考资料。
- 4 分：质量较好，有明确用途。
- 3 分：可用，但和其他 skill 有重叠。
- 2 分：内容偏薄，价值有限。
- 1 分：模板化明显，几乎没有独立价值。
- 0 分：坏链接、空壳、无法使用。

### 7.2 重复度评分

重复度看这些证据：

- 是否和另一个 skill 解决同一主问题。
- 是否只是把主流程的一小步拆成独立 skill。
- 是否没有独立关键词边界。
- 是否没有独立输出产物。
- 是否已有更强 skill 覆盖它。

建议 0 到 5 分：

- 5 分：高度重复，应删除或合并。
- 4 分：明显重复，除非有特殊证据，否则删除。
- 3 分：部分重叠，需要降级或收紧边界。
- 2 分：轻度重叠，可通过路由修正。
- 1 分：基本独立。
- 0 分：完全独立。

### 7.3 删除判定

第一轮建议删除条件：

```text
quality_score <= 2
duplication_score >= 4
has_scripts = false
has_references = false
replacement_skill 非空
risk_level != high
```

满足条件也不是自动删除。

它只进入删除清单，仍需用户确认。

## 8. 默认接管关系

删除通用模板型 skill 后，需要明确由谁接管。

建议默认接管方向：

| 被删除类型 | 接管方向 |
|---|---|
| 通用训练模板 | `scikit-learn` 或 `ml-pipeline-workflow` |
| 通用评估模板 | `scikit-learn` 或 `LQF_Machine_Learning_Expert_Guide` |
| 数据泄漏相关 | `ml-data-leakage-guard` |
| EDA 和数据探索 | `exploratory-data-analysis` |
| 特征工程 | `preprocessing-data-with-automated-pipelines` 或 `scikit-learn` |
| 可解释性 | `shap` 或 `LQF_Machine_Learning_Expert_Guide` |
| 统计建模 | `statsmodels` 或 `statistical-analysis` |
| 时间序列 | `aeon`、`timesfm-forecasting` 或 `statsmodels` |

接管关系必须写入审计表。

## 9. 删除执行设计

用户确认删除清单后，正式执行直接删除。

每个删除对象需要同步清理：

- `bundled/skills/<skill_id>/`
- `config/pack-manifest.json`
- `config/skill-keyword-index.json`
- `config/skill-routing-rules.json`
- `config/skills-lock.json`
- 测试 fixtures 或 replay 里对该 skill 的引用
- 文档中对该 skill 的推荐引用

如果某个 skill 被删除，但历史用户可能还会搜索它，可以在迁移说明里写：

```text
<deleted-skill> -> use <replacement-skill>
```

但不保留 retired 目录。

## 10. 路由收敛规则

瘦身后，ML pack 不应继续保持“大池子平等竞争”。

每个 pack 应该收敛成：

- 1 到 3 个 `route_authority_candidates`
- 若干 `stage_assistant_candidates`
- 少量工具型或显式调用候选
- 清楚的 `defaults_by_task`

如果一个 pack 没有显式 `route_authority_candidates`，当前路由可能把所有候选都当成可主导对象。

这类 pack 应该补齐主专家和助手分层。

## 11. 验证设计

删除 PR 至少要跑这些检查：

```powershell
.\scripts\verify\skill-metadata-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-built-in-skill-governance-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
```

还要补一组 ML 路由 replay 用例。

最少覆盖：

- “训练一个 scikit-learn 分类模型”
- “检查训练集和测试集是否数据泄漏”
- “做 EDA 并输出图表”
- “解释模型特征重要性”
- “评估分类模型混淆矩阵”
- “做时间序列预测”
- “比较两个 ML 方案哪个更可信”

这些 replay 用例用来确认：

- 主专家命中合理。
- 阶段助手不会抢主路由。
- 删除后的 replacement skill 能接住原来的任务。
- 低质量薄模板 skill 不再污染路由。

## 12. 风险和处理

### 风险 1：误删边缘有用 skill

处理：

- 只删除有证据的通用模板型 skill。
- 专用工具 skill 第一轮不删。
- 每个删除项都要有接管对象。

### 风险 2：配置引用残留

处理：

- 删除后跑 offline skills gate。
- 搜索全仓引用。
- 更新 `skills-lock.json`。

### 风险 3：路由变差

处理：

- 增加 ML replay 用例。
- 对高风险删除项先标记 medium 或 high，不进入第一轮删除。
- 删除后比较关键任务的路由结果。

### 风险 4：包瘦了但问题没解决

处理：

- 删除之外必须同步收敛 pack。
- 每个 ML pack 明确主专家和助手。
- 不允许继续让大量相似 skill 平等竞争。

## 13. 第一轮完成标准

第一轮完成时应该达到：

- 有一份完整 ML skill 审计表。
- 有一份用户确认过的删除清单。
- 删除所有确认删除的通用模板型 ML skills。
- 所有删除项都有 replacement skill。
- `pack-manifest` 不再引用已删除 skill。
- `skill-keyword-index` 和 `skill-routing-rules` 不再引用已删除 skill。
- `skills-lock.json` 已更新。
- 核心验证命令通过。
- ML replay 用例显示主专家和助手分层更清楚。

## 14. 后续阶段

第一轮之后，再进入第二轮：

- 专用工具 skill 质量评估。
- 专业框架 skill 路由分层。
- 生物、化学、科研数据相关 ML skill 的交叉治理。
- 其他类别的瘦身复制，例如 Research/Writing、Docs/Media、Code Quality。

第一轮的目标不是一次性解决全部问题。

第一轮的目标是建立一套可复制的瘦身方法，并先把 ML 相关的通用模板重复项清掉。
