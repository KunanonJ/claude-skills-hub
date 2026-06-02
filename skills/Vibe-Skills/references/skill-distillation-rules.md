# Skill Distillation Rules

## 1. 适用范围

本规则用于把外部 skill / subagent / role 内容收口为 canonical VCO 资产，服务于：

- `config/role-pack-policy.json`
- 现有 canonical skills
- `references/team-templates.md`
- verify gates / quality rules / reference cards

它不用于批准新的 runtime surface。

## 2. Artifact 分类

| Artifact type | 定义 | 优先 landing | 不应该直接变成 |
|---|---|---|---|
| `team_pattern` | 多角色协作模式、调度结构、handoff 方式 | `team_template_seed` | 第二 orchestrator |
| `role_card` | 单角色职责、视角、review posture | `role_card_overlay` | 独立执行 owner |
| `skill_template` | skill 结构模板、质量规范、脚手架规则 | `skill_distillation_rule` | 第二 skill runtime |
| `reference_case` | taxonomy、示例、命名启发、覆盖面材料 | `reference_only` | 默认推荐链 |

## 3. 每条 distillation record 必须具备的字段

1. `artifact_id`
2. `upstream_source`
3. `artifact_type`
4. `retained_value`
5. `landing_decision`
6. `canonical_owner`
7. `dedup_with`
8. `evidence_required`
9. `rejection_reason_if_any`

如果任何字段无法填写，默认不进入 canonical runtime 邻接面。

## 4. Landing 决策表

| 条件 | Landing decision |
|---|---|
| 能映射到现有 team template，且不新增 runtime loop | `team_template_seed` |
| 主要是角色职责/视角卡片，不需要执行 owner | `merge_into_role_pack` |
| 主要是 skill schema / validation / quality checklist | `merge_into_existing_skill` |
| 主要是案例、taxonomy、命名启发 | `reference_only` |
| 与现有 canonical surface 冲突，或重复率过高 | `reject` |

## 5. 质量门禁

每条记录至少通过以下 5 项检查：

1. **problem_shape_reusable**：不是一次性的 repo-specific prompt。
2. **boundary_explicit**：明确写出不能吸收什么。
3. **runtime_conflict_cleared**：不会形成第二 orchestrator / owner / surface。
4. **evidence_path_defined**：能指向 docs / reference / gate / pilot artifact。
5. **maintenance_owner_named**：知道后续由谁维护 canonical 资产。

## 6. 去冗余规则

### 6.1 优先 merge into existing

如果现有 skill、pack、template 已经覆盖 70% 以上职责：

- 优先补充 retained value 到现有资产；
- 不创建新的 skill id；
- 不引入新的并排角色树。

### 6.2 仅 role 价值、无 runtime 价值

如果上游主要贡献是 prompt posture / persona / checklist：

- 保留为 `role_card_overlay`；
- 不新增命令、不新增执行控制器；
- 必须说明它服务哪个 canonical team template / pack。

### 6.3 taxonomy 价值大于运行价值

像 `antigravity-awesome-skills` 这类大市场型上游：

- 优先作为 taxonomy coverage / gap detection 输入；
- 允许进入 governance / reference；
- 默认不直接进入 runtime 推荐链。

像 `awesome-claude-skills-composio` 这类“curated root + massive automation subtree”型上游：

- 优先抽取根目录下可复用的 skill schema / checklist / packaging 约束；
- 明确把 connector automation 子树视为隔离区；
- 没有 canonical admission 之前，不得让外部 surface 借 catalog 体量获得事实 owner 地位。

## 7. 明确拒绝条件

出现以下任一情况，直接 `reject`：

- 需要额外 supervisor / agent loop 才能成立；
- 需要保留原始 upstream 命令语义；
- 只是重命名现有 canonical 能力；
- 不能解释 canonical owner；
- 不能提供去冗余理由；
- 会把 VCO 拉回“多入口、多真源、多责任边界”的双轨状态。

## 8. Evidence package

被吸收的 retained value 至少要有 1 条证据路径：

- governance doc
- reference card / rule
- policy JSON
- verify gate
- pilot scenario

没有证据路径的“吸收完成”表述一律无效。

## 9. 推荐口径

推荐使用以下一句话描述任何 distillation 结果：

> 这不是把上游原样纳入 runtime，而是把其中可复用、可验证、可去冗余的剩余价值映射到现有 canonical owner。

## 10. 2026-03-17 Re-Audit Addendum

- `claude-skills`：继续作为 skill quality / schema / validation 刷新源。
- `antigravity-awesome-skills`：继续作为 taxonomy coverage 证据，不进入默认推荐链。
- `awesome-claude-skills-composio`：只吸收 curated root 的规则价值；对 connector automation subtree 保持 quarantine posture。
