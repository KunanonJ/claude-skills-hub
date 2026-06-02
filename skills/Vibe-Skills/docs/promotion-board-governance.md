# Promotion Board Governance

## 目标

Wave27 建立了四平面 promotion board；Wave39 则把它扩展成 **release closure 证据板**：除了 memory / prompt / browser / desktop 四平面，还必须登记 Wave31-38 新增的治理条目（mirror topology、upstream corpus、docling、connector admission、role-pack distillation、capability catalog）。

promotion board 只负责记录证据、给出升级建议、保留 rollback 信息；它不能替代 `VCO` 主路由，也不能制造第二控制面。

## Board 范围

当前 board 统一存放在 `config/promotion-board.json` 的 `planes[]` 中，但语义上分成两类：

1. **execution planes**：`memory-runtime-v2`、`prompt-intelligence`、`browserops-provider`、`desktopops-shadow`
2. **governance tracks**：`mirror-topology-governance`、`upstream-corpus-governance`、`docling-document-plane`、`connector-admission-layer`、`role-pack-distillation`、`capability-catalog-corpus`

保留单一 `planes[]` 的原因是：
- 复用现有 board schema 与 rollout history；
- 让 Wave39 的 deep-extraction gate 能从单一列表取证；
- 避免再引入第二块并行 board 数据结构。

## 阶段梯度

| 阶段 | 含义 | 最低证据门槛 | 是否允许自动写板 |
|---|---|---|---|
| `shadow` | 只建档、只观察、只建议 | governance doc + policy + gate + rollback | 否 |
| `soft` | 可进入受控 advice-first 放量 | pilot fixture 已定义、gate 可执行、rollback 已就绪 | 仅允许显式 `shadow -> soft` |
| `strict` | 更强治理但仍不突破单一控制面 | `soft` 证据齐备 + 重复评估 + 人工复核 | 否 |
| `promote` | 正式吸收为稳定治理资产 | `strict` 证据齐备 + rollback drill + board signoff | 否 |

## Board 必填字段

每个 board item 至少要有：

- `plane_id`
- `current_stage`
- `next_stage`
- `required_gates`
- `pilot_fixture`
- `pilot_status`
- `evidence`
- `rollback`
- `evidence_summary`
- `owner`
- `last_reviewed_at`

## Evidence 约束

### execution planes

execution planes（四平面）进入 `soft` 时，仍沿用 Wave27/28 规则：

- `required_gates` 必须包含 `vibe-cross-plane-conflict-gate`
- `required_gates` 必须包含 `vibe-pilot-scenarios`
- 对应 `pilot-*.json` fixture 必须存在
- `rollback.max_safe_auto_write_stage` 只能是 `soft`

### governance tracks

governance tracks（Wave31-38）进入 `soft` 时，证据口径变为：

- 至少一个 domain gate（如 `vibe-docling-contract-gate`、`vibe-connector-admission-gate`）
- `pilot_fixture` 统一可复用 `scripts/verify/fixtures/pilot-deep-extraction.json`
- `required_gates` 必须包含能证明该治理面进入 canonical 的 gate
- rollback 必须描述“如何退回 reference/shadow，而不是如何接管 runtime”

## Rollout 原则

- `publish-absorption-soft-rollout.ps1` 默认只输出建议
- 脚本最多只允许在显式参数下写入 `shadow -> soft`
- `strict` 与 `promote` 只做 board 记录，不做脚本自动升级
- Wave39 新增的 board items 主要用于 **证明收口**，而不是宣布新的默认 runtime owner

## 与 Wave31-39 的关系

Wave31-39 之后，promotion / release closure 至少要求：

1. 有 mirror topology / runtime freshness 证据
2. 有 upstream corpus manifest / freshness 基线
3. 有 docling / connector / role-pack / capability catalog 的 canonical landing
4. 有 pilot fixture / eval 入口
5. 有 rollback
6. 有 changelog / release note 指向这些证据

因此，promotion board 不再只是四平面 rollout 板，而是 **深度榨取 + 漂移收口 + release note** 的统一证据入口。
