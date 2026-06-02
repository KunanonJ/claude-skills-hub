# Eval Slicing Taxonomy

## Purpose

本 taxonomy 用来把 `awesome-ai-tools`、`Prompt-Engineering-Guide`、`awesome-ai-agents-e2b` 的剩余价值转成 **可追踪、可比较、可审查** 的评测切片，而不是直接把这些项目的能力并入 live router。

核心原则：

- 切片用于 **解释差异**、**比较证据**、**组织 review**；
- 切片不用于直接决定默认路由；
- 没有 gate 和 rollback 语义的切片，不得进入 promotion 讨论。

## Slice Axes

| Axis | Values | Meaning |
| --- | --- | --- |
| `plane` | `prompt`, `tool`, `team`, `portfolio` | 切片究竟增强 VCO 的哪一层 |
| `evidence_mode` | `static-structure`, `shadow-replay`, `operator-review`, `rollback-drill` | 证据来源 |
| `decision_horizon` | `hold`, `review-ready`, `rollback-ready` | 离 board 行动有多近 |

## Recommended Slice Families

| Slice | Upstream value | Allowed use | Explicitly not allowed |
| --- | --- | --- | --- |
| `prompt-pattern-drift` | Prompt pattern cards | 解释 prompt drift warning | 自动改写 live prompt routing |
| `prompt-risk-checklist-alignment` | Prompt risk heuristics | release packet / operator reasoning | 代替 regression gate |
| `tool-risk-tier-alignment` | Tool taxonomy | 将外部工具映射到 VCO 风险分层 | 直接批准 tool enablement |
| `execution-isolation-readiness` | Agent sandbox ideas | 记录是否存在执行隔离缺口 | 引入第二执行平面 |
| `degraded-mode-recovery` | rollback / failure thinking | board-ready rollback evidence | 用“有 fallback”掩盖高风险扩张 |
| `candidate-overlap-pressure` | Cross-project overlap lens | 决定 remaining value 是否继续开采 | 以 taxonomic richness 替代 gap evidence |

## Operational Rule

任何 eval slice 要进入正式治理资产，至少满足：

1. 有清晰的 `landing zone`；
2. 有对应的 artifact family；
3. 明确写出 `default_surface_change = false`；
4. 能被 operator 解释，而不是只能被脚本看见。
