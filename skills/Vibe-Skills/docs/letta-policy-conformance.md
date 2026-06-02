# Letta Policy Conformance (VCO / Wave66)

## 1. 文档目的

Wave66 的目标不是把 `Letta` agent runtime 接入 VCO，而是把已经吸收的 policy vocabulary 变成 **可校验的 conformance surface**。

conformance evaluator 只回答一个问题：

> Letta-derived concepts 是否仍然保持 contract-source-only，而没有偷偷变成 runtime owner？

## 2. Conformance surface

| Letta concept | VCO landing surface | Conformance requirement |
|---|---|---|
| memory block mapping | `references/memory-block-contract.md` | canonical owners unchanged |
| archival search contract | `config/letta-governance-contract.json` | long-term retrieval expectations only |
| tool-rule contract | `references/tool-rule-contract.md` | may constrain tools, may not replace routing |
| token-pressure policy | `config/letta-governance-contract.json` | accepted as the only compaction signal surface |

## 3. Required checks

### 3.1 vocabulary completeness

以下 vocabulary 必须同时存在：

- `memory_block_mapping`
- `archival_search_contract`
- `tool_rule_contract`
- `token_pressure_policy`

### 3.2 owner preservation

Letta 只能解释 memory blocks，不能重写 owner：

- `state_store`
- `Serena`
- `ruflo`
- `Cognee`
- `mem0`

### 3.3 route immutability

若任何 tool-rule 暗示 route mutation、runtime takeover、second orchestrator，conformance 立即失败。

### 3.4 compaction discipline

在 VCO 中，`token-pressure policy` 是唯一被接受的 compaction policy surface。
它可以要求更轻量路径、更多确认、或更早 compaction，但不能借 compaction 名义转移 authority。

## 4. Explicit non-goals

- No Letta agent runtime inside the VCO control plane
- No second workflow surface
- No autonomous route reassignment
- No memory truth-source transfer

## 4.1 Current upstream re-audit note

The currently reviewed upstream delta can advance security or release hygiene without changing the absorbed policy vocabulary.
Such drift updates the observed upstream head, but does not justify expanding Letta beyond `contract-source-only`.

## 5. Failure semantics

若 conformance 失败，必须执行以下动作：

- keep `Letta` in contract-source-only mode
- freeze promotion to `shadow`
- keep routing and canonical owners unchanged
- require manual review before any further rollout

## 6. 必需资产

- `config/letta-governance-contract.json`
- `references/memory-block-contract.md`
- `references/tool-rule-contract.md`
- `config/memory-runtime-v3-policy.json`
- `scripts/verify/vibe-letta-policy-conformance-gate.ps1`

## 7. 验证方式

```powershell
pwsh -File .\scripts\verify\vibe-letta-policy-conformance-gate.ps1
```

## 8. 完成定义（Definition of Done）

满足以下条件，才视为 Wave66 conformance evaluator 落地完成：

- Letta governance contract 明确保留 contract-source-only
- memory block / tool-rule / token-pressure 三个 surface 都有可读合同
- compaction policy 被明确解释为 advice / constraint，而不是 authority transfer
- gate 能验证 vocabulary completeness、owner preservation、route immutability
- 任一 conformance failure 都能落回 `shadow`
