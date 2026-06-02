# Subagent Role Taxonomy

本文件把 VCO 当前真正使用到的 subagent / role archetype 明确化，避免“角色越来越多，但语义越来越模糊”。

## 1. Design Goal

角色 taxonomy 只做三件事：

1. 定义 **角色 archetype**；
2. 绑定 **native agent type** 与 **permission bundle**；
3. 约束 **何时该用角色 prompt，何时不该额外造角色**。

它不是第二套 runtime，也不是社区 role prompt 的收藏夹。

## 2. Permission Bundles

| Bundle | Typical Native Agent Type | Allowed Behavior | Forbidden Behavior |
|---|---|---|---|
| `lead_synthesis` | `default` | 分解任务、整合结果、维护共享摘要、决定 follow-up | 直接在无 owner 的共享范围内大规模改写实现 |
| `read_only_analysis` | `explorer` / `default` | 阅读、检索、比对、提出风险与方案 | 未分配 owner 时直接写代码或改共享配置 |
| `scoped_implementation` | `worker` | 在明确文件/模块 owner 范围内实现、修复、补测试 | 越权回退他人改动、重写非 owner 范围 |
| `quality_gate` | `default` / `worker` | 审查 diff、验证契约、指出缺口与风险 | 将 review 角色降级成“直接帮忙改完” |
| `security_review` | `default` / `worker` | 从威胁、秘密、权限、输入处理角度做 focused review | 在没有证据的情况下扩大安全整改范围 |

## 3. Core Archetypes

### A. Lead / Planner

- Archetype: `lead_synthesis`
- Native type: `default`
- Typical use:
  - XL 任务主协调者
  - scatter-gather lead
  - final synthesis / merge planner
- Responsibilities:
  - 维护 task contract
  - 统一 shared rollup
  - 在阶段边界做 `wait` / `send_input` follow-up

### B. Researcher / Explorer

- Archetype: `read_only_analysis`
- Native type: `explorer`
- Typical use:
  - 代码库现状调研
  - 规则/文档/历史检查
  - 风险对照与 candidate pruning
- Responsibilities:
  - 只返回 evidence、差异、建议
  - 不直接做共享实现写入

### C. Implementer

- Archetype: `scoped_implementation`
- Native type: `worker`
- Typical use:
  - feature slice owner
  - gate / config / docs 某一块的独立落地
- Responsibilities:
  - 仅修改明确分配的写入范围
  - 不回退别人的改动
  - 必须说明改了哪些文件与验证命令

### D. Reviewer

- Archetype: `quality_gate`
- Native type: `default` / `worker`
- Typical use:
  - code review
  - contract review
  - pack/policy consistency review
- Responsibilities:
  - 先指出风险，再给建议
  - 输出应面向“是否能进入下一阶段”

### E. Security Reviewer

- Archetype: `security_review`
- Native type: `default` / `worker`
- Typical use:
  - secrets / egress / auth / input handling review
  - threat-focused delta review
- Responsibilities:
  - 不做泛化“安全感想”
  - 必须绑定到具体 trust boundary 或风险类型

## 4. Local VCO Dialectic Roles

Template 7 `local-vco-dialectic-review` 依赖以下本地角色 prompt：

| Role | Native Agent Type | Permission Bundle | Prompt Source |
|---|---|---|---|
| `team-lead` | `default` | `lead_synthesis` | `bundled/skills/local-vco-roles/references/role-prompts/team-lead.md` |
| `bug-analyst` | `explorer` | `read_only_analysis` | `bundled/skills/local-vco-roles/references/role-prompts/bug-analyst.md` |
| `arch-critic` | `default` | `quality_gate` | `bundled/skills/local-vco-roles/references/role-prompts/arch-critic.md` |
| `integration-analyst` | `worker` | `scoped_implementation` | `bundled/skills/local-vco-roles/references/role-prompts/integration-analyst.md` |
| `usability-analyst` | `default` | `quality_gate` | `bundled/skills/local-vco-roles/references/role-prompts/usability-analyst.md` |

这些角色的共同约束：

- 角色 prompt 只定义视角，不改变 native runtime 规则；
- lead 仍然是唯一共享摘要 owner；
- dialectic 组之间默认隔离，只在 synthesis 时合并。

## 5. Role Creation Rules

只有满足下列条件时，才应新增一个角色 archetype 或 role prompt：

- 该角色承担的职责不能被现有 archetype 清晰表达；
- 该角色需要独特的 evidence lens，而不是换个名字重复 review；
- 能明确绑定到某个 permission bundle；
- 在 `team-templates.md` 中有稳定使用场景。

否则，应优先复用：

- `Lead / Planner`
- `Researcher / Explorer`
- `Implementer`
- `Reviewer`
- `Security Reviewer`

## 6. Governance Rule

角色数增长不是目标，**角色边界清晰**才是目标。

VCO 在 P2 中吸收的不是“更多 subagents”，而是：

- archetype 明确化
- permission bundle 明确化
- local role prompt existence check
- template-to-role mapping 可验证化
