# Orchestration-Core Pack Consolidation Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-28

## 一句话结论

`orchestration-core` 不应该是万能代理包。它只应该回答三类问题：

1. 这个事情要不要先发散想方案。
2. 这个事情怎么写成可执行计划。
3. 这个计划是否适合用子代理拆开执行。

普通写代码、调试、代码审查、文档处理、机器学习、科研写作等问题，应该交给对应领域 pack。`orchestration-core` 不能靠高优先级和宽泛默认值抢走这些任务。

## 当前问题

当前 `orchestration-core` 的真实状态是：

| 字段 | 当前值 |
| --- | --- |
| `skill_candidates` | 27 |
| `route_authority_candidates` | `brainstorming`, `writing-plans`, `subagent-driven-development` |
| `stage_assistant_candidates` | 23 |
| `defaults_by_task.coding` | `subagent-driven-development` |
| `defaults_by_task.debug` | `subagent-driven-development` |

这个状态比之前“所有问题都落到 `vibe`”好，但又引入了新问题：普通 coding/debug 会默认落到 `subagent-driven-development`。这和项目原本的 M/L/XL 分级设计冲突。

人话说就是：现在一个普通“帮我改代码”的任务，可能被理解成“默认开子代理开发”。这不对。

## 设计目标

本轮治理目标：

1. 去掉严重重复的普通规划 skill 竞争。
2. 去掉低质量、旧框架、兼容命令对主路由面的污染。
3. 明确 `vibe`、`orchestration-core`、`subagent-driven-development` 的角色边界。
4. 恢复 M/L/XL 分级含义：子代理是受控执行模式，不是普通 coding 默认值。
5. 保留有价值目录内容，先做路由面收敛，再决定是否物理删除目录。

## 不做什么

本设计不建议第一步直接删除所有目录。

原因很简单：部分 skill 目录里有 scripts、assets、references 或兼容映射，直接删可能误伤安装、离线打包、旧命令兼容和测试夹具。

本轮先做三件事：

1. 从 `orchestration-core` 的候选面移除不该参与路由的 skill。
2. 把重复 skill 降级、合并或标记为迁移后删除。
3. 用路由探针证明普通任务不会再被错误地导向子代理。

物理删除目录放在下一轮，必须先确认目录没有资产价值或资产已经迁移。

## 分层模型

### 1. `vibe`: 总入口和运行时权威

`vibe` 是 canonical runtime skill，负责：

- 需求冻结。
- M/L/XL 分级。
- 阶段推进。
- 用户确认边界。
- specialist 调度。
- 验证与 cleanup。

`vibe` 不应该作为普通专家和 `brainstorming`、`writing-plans`、`subagent-driven-development` 抢同一条路由。

简单说：`vibe` 是总控台，不是某一个专家工位。

### 2. `orchestration-core`: 编排问题分流包

`orchestration-core` 只处理“怎么组织工作”的问题，不处理具体领域工作。

它应该回答：

- 要不要先想多个方案？
- 要不要先写计划？
- 是否适合拆成子代理？
- 有没有显式 spec-kit / SuperClaude / Ralph 兼容命令？

它不应该默认回答：

- 帮我写代码。
- 帮我修 bug。
- 帮我做代码审查。
- 帮我处理 Excel/PDF/图片。
- 帮我训练模型。
- 帮我写论文。

这些任务应该由其他 pack 处理。

### 3. `subagent-driven-development`: 受控执行模式

`subagent-driven-development` 不是“普通 coding 专家”。

它只应该在这些情况下进入：

- 用户明确说“子代理”“多代理”“并行执行”“拆成多个 agent”。
- 已有实施计划，而且任务之间相对独立。
- XL 级别任务在 `vibe` 确认后进入子代理执行。

它不应该因为 `TaskType = coding` 就自动触发。

## M/L/XL 分级设计

| 等级 | 子代理策略 | 说明 |
| --- | --- | --- |
| M | 默认不开子代理 | 小任务、单文件、普通修改，直接做或交给领域/code-quality pack。 |
| L | 可建议，但需要确认 | 先设计/计划，只有任务确实可拆时才建议子代理。 |
| XL | 推荐进入受控子代理流程 | 仍然必须经过 `vibe` 的需求冻结、计划确认、执行边界和验证。 |

这里的关键点是：XL 可以更主动建议子代理，但不等于任何 coding/debug 都直接默认进子代理。

## 目标角色表

| skill | 目标角色 | 处理的问题 | 处理方式 |
| --- | --- | --- | --- |
| `brainstorming` | route authority | 头脑风暴、方案发散、创意讨论 | 保留主路由 |
| `writing-plans` | route authority | 实施计划、任务拆解、迁移计划、runbook、波次计划 | 保留主路由 |
| `subagent-driven-development` | guarded route authority | 明确子代理、并行、多代理执行 | 保留，但去掉普通 coding/debug 默认权 |
| `vibe` | runtime authority only | canonical `$vibe` / `/vibe` 总治理 | 不作为普通专家候选 |
| `context-hunter` | stage assistant | 改代码前找上下文、找相似实现 | 只做阶段助手 |
| `think-harder` | stage assistant | 高风险决策前做深度分析 | 只做阶段助手 |
| `dialectic` | stage assistant / explicit-only | 多视角辩证分析 | 显式或 `vibe` 内部使用 |
| `local-vco-roles` | stage assistant / explicit-only | 本地 VCO 多角色审查角色包 | 显式或 `vibe` 内部使用 |
| `context-fundamentals` | explicit-only | 上下文工程概念解释 | 不进普通路由 |
| `create-plan` | merge-delete-after-migration | 简短计划，和 `writing-plans` 重叠 | 内容迁入 `writing-plans` 后移出 |
| `planning-with-files` | merge-delete-after-migration | 文件式计划，和 `writing-plans` 重叠 | 有价值模板迁移后移出 |
| `speckit-*` | explicit-only / separate spec-kit surface | spec-kit 工作流 | 只在 `/speckit.*` 或 `.specify/` 场景触发 |
| `spec-kit-vibe-compat` | explicit-only compat | spec-kit 到 vibe 的兼容桥 | 不参与普通规划路由 |
| `superclaude-framework-compat` | explicit-only compat | SuperClaude `/sc:*` 兼容 | 不参与普通路由 |
| `ralph-loop` | explicit-only compat | Ralph loop 兼容命令 | 不参与普通路由 |
| `cancel-ralph` | explicit-only compat | 取消 Ralph loop | 不参与普通路由 |
| `claude-skills` | move-out-of-pack | 创建/重构 Claude skill 的元技能 | 更适合 skill-creator/skill-governance 面 |
| `autonomous-builder` | move-out-of-pack | 端到端自动构建 | 不应在 orchestration-core 抢 coding |
| `hive-mind-advanced` | move-out-of-pack / explicit-only | 外部 swarm/queen-worker 框架 | 不参与普通路由 |

## 候选收敛设计

### 保留在 `orchestration-core.skill_candidates`

建议保留：

- `brainstorming`
- `writing-plans`
- `subagent-driven-development`
- `context-hunter`
- `think-harder`
- `dialectic`
- `local-vco-roles`
- `spec-kit-vibe-compat`

这些 skill 都和“如何组织任务”有关。

### 从 `orchestration-core.skill_candidates` 移出

建议移出：

- `autonomous-builder`
- `cancel-ralph`
- `claude-skills`
- `context-fundamentals`
- `create-plan`
- `hive-mind-advanced`
- `planning-with-files`
- `ralph-loop`
- `superclaude-framework-compat`
- 所有 `speckit-*` 子命令

说明：

- `create-plan` 和 `planning-with-files` 是规划重复项，先迁移内容，再从路由面移出。
- `speckit-*` 是一套独立命令语义，应该走显式 spec-kit 面。
- `ralph-loop`、`cancel-ralph`、`superclaude-framework-compat` 是兼容命令，不应该污染普通路由。
- `autonomous-builder` 太宽，放在这里会和所有 coding 任务抢路由。
- `claude-skills` 是 skill 制作/治理元技能，不属于编排核心。
- `context-fundamentals` 是解释型知识 skill，不应该做任务主路由。

## defaults 设计

目标不是给每个 task type 都硬塞一个默认 skill，而是避免低信息任务误触发。

建议：

| task type | 默认值 | 说明 |
| --- | --- | --- |
| `planning` | `writing-plans` | 计划类问题可以默认到计划作者。 |
| `research` | `brainstorming` | 方案探索类 research 可以默认到 brainstorming。 |
| `coding` | 不设置默认到 `subagent-driven-development` | 普通 coding 应该走领域 pack 或 `code-quality/tdd-guide`。 |
| `debug` | 不设置默认到 `subagent-driven-development` | 普通 debug 应该走 `code-quality/systematic-debugging`。 |
| `review` | 不设置默认到 `subagent-driven-development` | 普通 review 应该走 `code-quality/code-reviewer`。 |

如果现有 gate 要求 `defaults_by_task` 必须存在，只保留 `planning` 和必要的 `research` 默认即可；不要为了填满字段把 coding/debug 塞给子代理。

## routing rules 设计

### `subagent-driven-development`

调整方向：

- 移除 `canonical_for_task = coding`。
- 只用明确子代理关键词触发。
- 中文关键词要包括真实用户表达：`子代理`、`多代理`、`并行执行`、`拆成多个代理`、`多个 agent`。
- 英文关键词包括：`subagent`、`parallel agents`、`multi-agent`、`independent tasks`。

普通 `实现这个功能并修改代码` 不能命中它。

### `writing-plans`

保留计划类主路由：

- `实施计划`
- `任务拆解`
- `迁移计划`
- `runbook`
- `wave plan`
- `milestone`
- `执行计划`

它不应该处理普通代码审查、普通调试、普通安全审计。

### `brainstorming`

保留方案发散类主路由：

- `头脑风暴`
- `方案发散`
- `比较几个方向`
- `brainstorm`
- `ideation`

它不应该处理直接实现、直接修 bug、直接部署。

### spec-kit

`speckit-*` 不走普通规划关键词。

只在这些情况下触发：

- 用户显式输入 `/speckit.specify`、`/speckit.plan`、`/speckit.tasks` 等。
- 用户明确说 `.specify/`、`spec.md`、`plan.md`、`tasks.md`、`constitution.md` 并且语义就是 spec-kit 工作流。

## 物理删除策略

第一轮不建议物理删除以下目录：

- 有 `scripts/` 的目录。
- 有 `assets/` 的目录。
- 有 `references/` 的目录。
- 有兼容命令映射的目录。

第一轮只从 pack 路由面移除。

第二轮再按这个顺序处理：

1. 检查有没有安装、打包、测试引用。
2. 迁移有价值内容到保留 skill。
3. 更新 docs/governance 说明。
4. 跑离线技能门禁和打包门禁。
5. 再物理删除目录。

## 验证设计

必须新增或更新这些路由探针。

| prompt | grade | task type | 期望 |
| --- | --- | --- | --- |
| `实现这个功能并修改代码` | M | coding | 不能命中 `orchestration-core/subagent-driven-development` |
| `实现这个功能并修改代码` | L | coding | 不能命中 `orchestration-core/subagent-driven-development` |
| `实现这个功能并修改代码` | XL | coding | 不能仅因 XL 自动命中 `subagent-driven-development` |
| `把任务拆成多个子代理并行执行` | XL | planning | 命中 `orchestration-core/subagent-driven-development` |
| `请输出实施计划和任务拆解` | L | planning | 命中 `orchestration-core/writing-plans` |
| `先做头脑风暴，比较几个方案` | L | planning | 命中 `orchestration-core/brainstorming` |
| `/speckit.plan 生成技术计划` | L | planning | 命中 spec-kit 显式流程，不污染普通 `writing-plans` |
| `do root cause debugging for failing tests` | M | debug | 命中 `code-quality/systematic-debugging` |
| `write failing tests first for this feature` | M | coding | 命中 `code-quality/tdd-guide` |

建议运行：

```powershell
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
```

如果第一条普通 coding 探针仍然落到 `subagent-driven-development`，说明只改配置还不够，需要在路由器里阻止“没有正向子代理信号时 fallback 到子代理”。

## 风险和控制

| 风险 | 控制 |
| --- | --- |
| 移出太多 candidate 导致旧命令不可见 | 先从 pack 路由面移出，不物理删除目录；显式命令仍可由兼容入口处理。 |
| `vibe` 总治理被削弱 | 不改 `config/vibe-entry-surfaces.json`，不改 canonical runtime skill。 |
| XL 任务不再自动子代理 | XL 只是不静默自动；仍可由 `vibe` 在计划确认后推荐/启用子代理。 |
| spec-kit 普通 planning 互相抢路由 | spec-kit 改成显式工作流面，普通计划交给 `writing-plans`。 |
| 兼容框架失效 | 保留目录和脚本，先只改 pack 候选关系。 |

## 完成标准

本轮实现完成后，必须满足：

1. `orchestration-core` 不再把普通 coding/debug 默认交给 `subagent-driven-development`。
2. `subagent-driven-development` 只在明确子代理/并行/多代理场景触发。
3. `brainstorming`、`writing-plans`、`subagent-driven-development` 的边界清楚。
4. `create-plan`、`planning-with-files` 不再和 `writing-plans` 抢主路由。
5. spec-kit、SuperClaude、Ralph 兼容类 skill 不参与普通主路由。
6. `vibe` 仍然是 canonical runtime authority。
7. 有定向路由探针证明普通 coding 不会误进子代理。
8. 本轮报告明确区分“路由面移除”和“物理目录删除”。

## 推荐实施顺序

1. 新增 focused route regression，先复现普通 coding 误进子代理。
2. 收敛 `orchestration-core.skill_candidates`。
3. 收敛 `route_authority_candidates` 和 `stage_assistant_candidates`。
4. 移除 coding/debug 到 `subagent-driven-development` 的默认绑定。
5. 收窄 `subagent-driven-development` 的 routing rule。
6. 必要时加 fallback guard，禁止无子代理正向信号时选择子代理。
7. 更新 governance note，记录 before/after 数量和移出原因。
8. 跑定向探针和 pack 回归。
9. 提交路由治理修改。

