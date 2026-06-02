# Global Pack Consolidation Audit Design

日期：2026-04-27

## 1. 目标

本轮只做全局体检，不做具体 pack 收敛。

目标是给 Vibe-Skills 的所有 pack 做一次只读审计，找出哪些 pack 最值得下一轮治理，并说明原因。审计结果用于回答：

> 下一刀应该先治理哪个 pack，为什么？

本轮输出治理排序和证据，不修改 live routing。

## 2. 非目标

本轮不做以下事情：

- 不修改 `config/pack-manifest.json`。
- 不修改 `config/skill-routing-rules.json`。
- 不修改 `config/skill-keyword-index.json`。
- 不删除任何 `bundled/skills/*` 目录。
- 不迁移 scripts、references、examples 或 assets。
- 不调整 `route_authority_candidates` 或 `stage_assistant_candidates`。
- 不声称某个 pack 已经完成收敛。

## 3. 审计输入

审计读取这些仓库文件：

```text
config/pack-manifest.json
config/skill-keyword-index.json
config/skill-routing-rules.json
bundled/skills/*/SKILL.md
```

如果某些配置不存在，审计应降级输出 `manual_review`，不能静默跳过。

## 4. 审计对象

每个 pack 生成一行审计记录。字段包括：

```text
pack_id
skill_candidate_count
route_authority_count
stage_assistant_count
has_explicit_role_split
default_task_count
missing_default_skill_count
suspected_overlap_count
broad_keyword_count
tool_primary_risk_count
asset_heavy_candidate_count
risk_score
priority
recommended_next_action
rationale
```

审计记录应同时支持人读报告和机器读 JSON/CSV。

## 5. 风险评分

风险评分用于排序，不是最终判决。建议维度如下：

| 维度 | 信号 | 解释 |
|---|---|---|
| pack 规模 | `skill_candidates` 很多 | 候选越多，边界越容易模糊 |
| 主路由压力 | `route_authority_candidates` 很多 | 主路由越多，越容易互相抢任务 |
| 角色缺失 | 没有显式 role split | pack 内所有 candidate 都可能变成默认竞争者 |
| 默认路由风险 | default skill 缺失或与角色不匹配 | 默认入口可能和治理意图冲突 |
| 重复嫌疑 | 名称、描述、关键词高度相似 | 说明 pack 可能不是问题导向 |
| 宽泛关键词 | 多个 skill 共享宽泛词 | 容易让某些 skill 长期压住其他 skill |
| 工具抢主路由 | 窄工具像主入口一样参与 | 工具型 skill 应更多作为显式或阶段辅助 |
| 资产治理难度 | 大量 scripts/references/assets | 后续删除或合并需要迁移证据 |

建议优先级：

```text
P0: 下一轮最应该治理
P1: 需要治理但不急
P2: 暂时观察
```

## 6. 重复与边界判断

本轮只做轻量判断，不做深度内容裁决。

重复嫌疑可以来自：

- skill id 词根相近，例如 `code-review`、`code-reviewer`、`reviewing-code`。
- 描述里反复出现同一问题域。
- 多个 skill 使用同一组宽泛关键词。
- 一个 pack 中同时存在主专家、工具、阶段助手，但没有 role split。

审计报告必须用“疑似”表达，不应直接要求删除。

## 7. 预期高风险候选

基于当前 pack 分布，审计预计会重点标出这些候选，但最终排序以实际脚本输出为准：

| pack | 已观察到的风险 |
|---|---|
| `research-design` | skill 多，route authority 多，研究设计、假设、因果、回归、报告边界混杂 |
| `science-literature-citations` | 文献检索、引用管理、同行评审、批判阅读多个 route authority 并存 |
| `bio-science` | skill 很多，工具和数据库密集，但当前缺少显式 role split |
| `docs-media` | 文档、PDF、表格、转写、内容写作混在同一 pack，当前缺少显式 role split |
| `code-quality` | review/debug/test/security 相关 skill 名称和职责相近，当前缺少显式 role split |
| `ai-llm` | docs、prompt、embedding、eval、transformers 边界可能混杂 |

这些不是治理结论，只是审计应覆盖的 sanity check。

## 8. 输出产物

建议输出：

```text
outputs/skills-audit/global-pack-consolidation-audit.json
outputs/skills-audit/global-pack-consolidation-audit.csv
docs/governance/global-pack-consolidation-audit-2026-04-27.md
```

Markdown 报告应包含：

- 全局风险排行榜。
- P0/P1/P2 分组。
- 每个 P0 pack 的风险解释。
- 只读审计边界说明。
- 下一轮建议治理顺序。
- 明确说明没有修改 live routing。

## 9. 测试方法

需要新增或扩展 runtime-neutral 测试，验证审计逻辑稳定：

- 能读取 `pack-manifest.json`。
- 能覆盖所有 pack。
- 能输出 JSON、CSV、Markdown。
- 能识别 role split 是否存在。
- 能给高风险 pack 生成非零风险分。
- 能把 `research-design`、`science-literature-citations`、`bio-science`、`docs-media`、`code-quality` 放进候选清单。
- 不修改 live config 文件。

建议验证命令：

```powershell
python -m pytest tests/runtime_neutral/test_global_pack_consolidation_audit.py -q
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
```

如果实现新增 verify gate，再补：

```powershell
.\scripts\verify\vibe-global-pack-consolidation-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs\skills-audit
```

## 10. 成功标准

本轮完成后应满足：

- 有一份已提交的全局 pack 审计设计文档。
- 有一份可复现的全局 pack 审计报告。
- 报告给出 P0/P1/P2 排序和理由。
- 没有修改任何 live routing config。
- 没有删除任何 skill 目录。
- 后续可以基于 P0 排名选择下一个具体 pack 做问题地图治理。

## 11. 后续实施边界

实施计划应分成两步：

1. 先实现只读审计和报告输出。
2. 等用户选择 P0 pack 后，再为该 pack 单独写 problem-first consolidation spec。

这样可以避免“全局审计”直接滑向“全局重构”。
