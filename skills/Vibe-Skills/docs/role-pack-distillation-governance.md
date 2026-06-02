# Wave37 Role Pack / Skill Distillation Governance

## 1. 目标

Wave37 的目标不是把 `agent-squad`、`claude-skills`、`awesome-agent-skills`、`awesome-claude-code-subagents`、`antigravity-awesome-skills`、`awesome-claude-skills-composio` 原样搬进仓库，而是把它们的剩余价值沉淀为 **VCO-native role-pack / team-template / skill-distillation governance**。

这意味着：

1. VCO 仍然是唯一控制面与执行编排入口。
2. `references/team-templates.md` 仍然是 canonical team execution contract。
3. 新吸收的上游内容只能成为 role-pack seed、role-card overlay、skill distillation rule，或 reference case。
4. 任何上游项目都不能形成第二 orchestrator、第二 team execution owner、第二 runtime surface。

## 2. Canonical 边界

### 2.1 控制权边界

- **唯一 orchestrator**：`SKILL.md`、`protocols/*`、pack router 与现有 team template 仍是唯一运行时决策链。
- **唯一 team execution owner**：实际执行所有权只属于 VCO-native team template / role contract；role pack 只能解释与补充，不得直接接管执行。
- **唯一技能落点**：skill distillation 只能进入现有 canonical 技能、reference、policy、gate；不得把上游目录变成新的默认技能面。

### 2.2 产物边界

本 wave 新增的 canonical 产物只有：

- `docs/role-pack-distillation-governance.md`
- `references/skill-distillation-rules.md`
- `config/role-pack-policy.json`
- `scripts/verify/vibe-role-pack-governance-gate.ps1`

任何未来整合若需要改动 `references/team-templates.md`、`references/index.md`、`config/promotion-board.json`，都必须以这些 canonical 产物为上游依据，而不是直接复写原始上游内容。

## 3. Upstream → Landing 映射

| Upstream | 保留价值 | Canonical landing | 明确不吸收 |
|---|---|---|---|
| `agent-squad` | supervisor scatter/gather、fan-out/fan-in、milestone handoff | team-template seed / role-pack policy | 新 supervisor runtime、新命令面 |
| `claude-skills` | 技能规范、模板、验证逻辑、质量门禁 | skill distillation rule | 第二 skill runtime、第二安装器语义 |
| `awesome-agent-skills` | 角色卡片、问题域覆盖、角色分层案例 | role-card overlay / domain specialist pack | 海量 raw skill 直接进 runtime |
| `awesome-claude-code-subagents` | reviewer / analyst / implementer prompt archetype | review-board / delivery role pack seed | 新 subagent owner、新会话框架 |
| `antigravity-awesome-skills` | 大规模 skill taxonomy、命名启发、角色覆盖缺口 | role-card overlay / reference case | 把 marketplace 当作默认技能面 |
| `awesome-claude-skills-composio` | curated root / automation subtree 分层、connector-aware skill packaging | skill distillation rule / connector-boundary reference | composio automation 树直接变成默认 skill surface |

## 4. Landing taxonomy

### 4.1 `team_template_seed`

用于解释“哪些上游团队模式值得映射进现有 team template”。

适用条件：

- 模式能被现有 `default` / `explorer` / `worker` agent type 表达；
- 不需要额外 runtime loop；
- 可以映射到 `references/team-templates.md` 现有模板或未来增量模板。

### 4.2 `role_card_overlay`

用于沉淀角色职责与 prompt archetype，但不直接升级为 team template。

适用条件：

- 上游提供的是角色画像、评审视角、领域专家职责；
- 这些内容适合服务已有 pack、review flow、research flow；
- 不要求单独的执行 owner。

### 4.3 `skill_distillation_rule`

用于把上游技能模板、规范、检查清单转成 canonical skill quality rules。

适用条件：

- 上游价值主要是模板、规范、验证方法，而不是运行时能力；
- 能归并到已有 skill / gate / reference；
- 能用统一字段记录 retained value、dedup relation、拒绝原因。

### 4.4 `reference_case_only`

仅保留为案例与 taxonomy 参考，不进入运行时推荐链。

适用条件：

- 内容重复率高；
- 价值主要在覆盖面与命名启发；
- 若直接吸收会明显扩大维护面或引入第二语义面。

## 5. Distillation workflow

1. **Intake**：登记 upstream 来源、目标问题域、候选 retained value。
2. **Classify**：先判断它是 team pattern、role card、skill template 还是 reference case。
3. **Dedup**：与现有 `team-templates`、`pack-manifest`、canonical skills 对照，确认是否已被覆盖。
4. **Land**：只能落到 `team_template_seed`、`role_card_overlay`、`skill_distillation_rule`、`reference_case_only` 四类之一。
5. **Gate**：必须通过 `vibe-role-pack-governance-gate.ps1`，并提供 retained value、canonical owner、禁止事项、证据路径。
6. **Promote later**：如需进入 index/tool-registry/promotion board，只能在后续 wave 基于本治理资产追加，不得跳过 governance 直接写入运行面。

## 6. 去冗余规则

### 6.1 永久禁止事项

- 引入第二 orchestrator。
- 引入第二 team execution owner。
- 以 upstream 名称暴露新的默认 runtime surface。
- 复制整套 raw prompt / raw role trees 到 canonical runtime。
- 因为 taxonomy 很大就绕过现有 VCO 角色边界。

### 6.2 允许的“剩余价值”形态

- 角色职责矩阵。
- handoff / milestone / dispatch envelope 模式。
- reviewer / specialist 的 prompt archetype。
- skill template 的 schema、quality gate、anti-pattern。
- taxonomy 级别的命名启发、覆盖缺口与吸收优先级。

### 6.3 与 team template 的关系

role pack 不是 team template 的平行替身，而是 team template 的治理输入层。

- role pack 负责解释“为什么值得吸收、吸收到哪一层、哪些部分不能吸收”；
- team template 负责定义“真正运行时的角色组合与 agent type”；
- 二者必须保持 **policy → template** 的单向关系，不能反向把上游 role tree 直接当成执行合同。

## 7. 与 skill distillation 的关系

`claude-skills` 与 `antigravity-awesome-skills` 的主要价值是：

- 给出技能模板与结构规范；
- 帮助定义 retained value / dedup / reject 的统一判断口径；
- 让 skill 质量门禁变成可验证资产，而不是主观口头判断。

因此，Wave37 将 skill distillation 明确收口到 `references/skill-distillation-rules.md` 与 `config/role-pack-policy.json` 的 `skill_distillation_contract`，而不是新增一套 skill creation runtime。

`awesome-claude-skills-composio` 在 2026-03 的结构变化进一步强化了这一点：

- curated root 可以继续作为质量与模板参考；
- `composio-skills/` 这类 connector automation 大目录必须被视为隔离区，而不是默认 skill runtime；
- connector / prompt / browser / memory 这些外部 surface 只有在 canonical 审核明确批准后，才允许进入事实 owner 位。

## 8. 操作命令

```powershell
pwsh -File .\scripts\verify\vibe-role-pack-governance-gate.ps1 -WriteArtifacts
```

可选联动验证：

```powershell
pwsh -File .\scripts\verify\vibe-promotion-board-gate.ps1
pwsh -File .\scripts\verify\vibe-pack-routing-smoke.ps1
```

## 9. 结论

Wave37 的 canonical 结论只有一句话：

> 上游角色/技能生态只作为 **VCO-native role-pack / team-template / skill-distillation governance** 的输入层存在；任何会形成第二 orchestrator、第二 team execution owner、第二 runtime surface 的吸收方式，一律视为越界。
