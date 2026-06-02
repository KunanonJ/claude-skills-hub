# Role Pack Governance

## Goal

把 `agent-squad`、`claude-skills`、`awesome-agent-skills`、`awesome-claude-code-subagents`、`antigravity-awesome-skills`、`awesome-claude-skills-composio` 的剩余价值，统一沉淀成 **VCO-native role pack governance**。

## Core Boundary

- 执行 owner 仍然只有 `Codex Native Team Runtime`；
- role pack 只规定：角色边界、输入输出、职责分工、技能质量规则；
- upstream catalog 不能变成新的 orchestration runtime。

## Absorbed Value

| Source | Absorbed Value | Landing |
|---|---|---|
| `agent-squad` | supervisor-as-tools decomposition | team-template reference |
| `claude-skills` | skill packaging heuristics | skill-authoring reference |
| `awesome-agent-skills` | role/capability taxonomy | role-card catalog |
| `awesome-claude-code-subagents` | subagent responsibility patterns | subagent pattern reference |
| `antigravity-awesome-skills` | skill quality exemplars | quality rules reference |
| `awesome-claude-skills-composio` | curated root-vs-automation split, connector-aware skill catalog quarantine | distillation rule + connector-boundary reference |

## Explicit Rejects

- 第二 orchestrator
- 第二 execution owner
- 直接从 upstream catalog 动态装载角色并执行
- 把 role pack 当作 routing authority

## Exit Criteria

- `config/role-pack-policy.json` 能解释吸收/拒绝边界；
- `references/role-pack-catalog.md` 能映射上游价值 -> VCO 落点；
- `vibe-role-pack-governance-gate.ps1` 能阻止越权扩张。

## 2026-03-17 Wave C Re-Audit Notes

- `agent-squad` 最新变动主要是依赖与示例面维护，没有出现可替换 VCO 执行 owner 的新主干，因此继续只吸收 scatter/gather 与 bounded handoff 模式。
- `awesome-agent-skills` 持续新增 skill 卡片，说明它仍适合作为 role/card coverage feed，但不适合 bulk 进入 canonical runtime。
- `awesome-claude-code-subagents` 新增科研检索类 subagent，证明 reviewer / specialist archetype 仍在扩展，适合补强现有 review / research 模板。
- `claude-skills` 持续更新 skill 质量与 schema 规则，适合作为 distillation rule 刷新来源。
- `antigravity-awesome-skills` 已进入更大规模 catalog + workflow 阶段，继续只作为 taxonomy / quality evidence，避免 marketplace 事实 owner 化。
- `awesome-claude-skills-composio` 已把海量 automation skills 隔离到 `composio-skills/`，因此它的主要 retained value 是“curated root 与 connector automation 需要分层治理”，而不是把 composio catalog 直接并入 VCO。
