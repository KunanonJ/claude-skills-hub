# Memory Runtime v3 Governance (VCO / Wave64)

## 1. 文档目的

Wave64 的目标不是把 `mem0` 或 `Letta` 引入为新的 runtime owner，而是把已经存在的 `memory-runtime-v2`、`mem0`、`Letta` 价值压缩成 **单一控制面下可运行、可检查、可晋升** 的治理骨架。

这份文档定义的重点是：

- 如何保持 `VCO` 仍是唯一控制面、唯一路由入口、唯一默认执行 owner。
- 如何把 `mem0` 收口为 **external preference backend lane**，而不是第二 memory truth-source。
- 如何把 `Letta` 收口为 **policy / contract vocabulary lane**，而不是第二 orchestrator。
- 如何把 Wave64-66 组织成 `advice-first / shadow-first / rollback-first` 的 Memory Runtime v3 spine。

## 2. 定位结论（必须保持不变）

### 2.1 唯一控制面

- `VCO` 仍是 memory plane 的唯一控制面。
- `selected.pack_id`、`selected.skill`、`grade`、`route` 的决定权不得转移给任何 memory extension。
- Memory Runtime v3 只能在 **post-route governance** 层输出建议、合同、检查结果。

### 2.2 Canonical owners 不变

以下 canonical owners 在 v3 中必须保持不变：

| Memory Need | Canonical Owner | 不得被谁接管 |
|---|---|---|
| session state | `state_store` | `mem0` / `Letta` |
| explicit project decisions | `Serena` | `mem0` / `Letta` |
| short-term semantic cache | `ruflo` | `mem0` / `Letta` |
| long-term graph memory | `Cognee` | `mem0` / `Letta` |

### 2.3 Extension lanes 的固定角色

| Extension | 固定角色 | 明确禁止 |
|---|---|---|
| `mem0` | optional external preference backend | primary execution state、route assignment、canonical project decision |
| `Letta` | policy / contract source only | runtime takeover、second orchestrator、route mutation |

## 3. Wave64-66 rollout spine

### 3.1 Wave64 — Memory Runtime v3 baseline

Wave64 先建立统一治理骨架：

- `docs/memory-runtime-v3-governance.md`
- `config/memory-runtime-v3-policy.json`
- `references/memory-runtime-v3-contract.md`
- `scripts/verify/vibe-memory-runtime-v3-gate.ps1`

这一层只做合同化与 gate 化，不做 authority transfer。

### 3.2 Wave65 — mem0 soft rollout pilot

Wave65 只允许把 `mem0` 从 `shadow` 推进到 **可审计的 soft pilot**：

- 写入必须经过 `references/mem0-write-admission-contract.md`
- soft rollout 仍然是 `opt-in`
- 发生歧义、泄密风险、truth-source overlap 时，必须立即 deny write 并回退到 advisory-only

### 3.3 Wave66 — Letta conformance evaluator

Wave66 的重点不是扩大 Letta 权限，而是把它的 vocabulary 收束成可校验合同：

- memory block mapping
- archival search contract
- tool-rule contract
- token-pressure / compaction discipline

promotion 的含义只会是 **更严格的 conformance checking**，不会是更高 authority。

## 4. 运行不变量

Memory Runtime v3 的不变量如下：

1. **single control plane only**：不得出现第二 orchestrator。
2. **preserve routing assignment**：不得改写 `selected.pack_id`、`selected.skill`、`route`。
3. **preserve canonical truth-sources**：`state_store / Serena / ruflo / Cognee` 仍是默认 memory owners。
4. **advice-first / shadow-first**：Wave64 基线必须停留在 `shadow`，由 gate 驱动后续晋升。
5. **rollback-first**：任何外部扩展冲突都优先回退到 `shadow`，不得先扩权后补救。
6. **promotion requires evidence**：`shadow -> soft_candidate -> strict_candidate` 都必须有 gate、pilot、rollback 证据。

## 5. Operator guardrails

### 5.1 Kill switch

- `mem0` kill switch：`config/mem0-backend-policy.json`
- `Letta` kill switch：`config/letta-governance-contract.json`
- plane baseline：`config/memory-runtime-v3-policy.json`

### 5.2 回退规则

若出现以下任一情况，必须把 plane 退回 `shadow`：

- `mem0` 出现 truth-source overlap
- `Letta` 合同暗示 runtime takeover
- 任一 gate 失败
- cross-plane conflict unresolved

回退时必须保持：

- `state_store` 继续负责 session truth
- `Serena` 继续负责 explicit project decisions
- `mem0` 停止写入或保持 advisory-only
- `Letta` 只保留 contract vocabulary

## 6. 关键资产

- Governance doc：`docs/memory-runtime-v3-governance.md`
- Runtime policy：`config/memory-runtime-v3-policy.json`
- Backend adapters：`config/memory-backend-adapters.json`
- Unified contract：`references/memory-runtime-v3-contract.md`
- mem0 admission：`references/mem0-write-admission-contract.md`
- Letta conformance：`docs/letta-policy-conformance.md`
- Runtime adapter helpers：
  - `scripts/runtime/VibeMemoryBackends.Common.ps1`
  - `scripts/runtime/memory_backend_driver.py`
- Gates：
  - `scripts/verify/vibe-memory-runtime-v3-gate.ps1`
  - `scripts/verify/vibe-mem0-softrollout-gate.ps1`
  - `scripts/verify/vibe-letta-policy-conformance-gate.ps1`

## 7. Runtime Activation Boundary

Memory Runtime v3 now has a governed runtime adapter layer.
This layer does not create a second control plane.
It only decides whether a bounded lane action can be executed, then falls back to `state_store` or local artifacts if the lane is unavailable.

Stage-bound live actions:

- `deep_interview`: `Serena` decision recall when a project key exists
- `skeleton_check` / `xl_plan`: bounded `Cognee` relation recall
- `plan_execute`: XL-only `ruflo` handoff recall + handoff card write
- `phase_cleanup`: bounded `Serena` decision write and `Cognee` relation ingest

Fallback contract:

- missing `Serena` project key -> `deferred_no_project_key`
- disabled or unavailable backend -> local governed fallback
- no relevant memory hit -> `backend_read_empty`
- no admissible write payload -> `guarded_no_write`

## 8. 验证方式

```powershell
pwsh -File .\scripts\verify\vibe-memory-runtime-v3-gate.ps1
pwsh -File .\scripts\verify\vibe-mem0-softrollout-gate.ps1
pwsh -File .\scripts\verify\vibe-letta-policy-conformance-gate.ps1
```

## 9. 完成定义（Definition of Done）

满足以下条件，才视为 Wave64 governance spine 落地完成：

- `memory-runtime-v3` policy 明确表达 single-control-plane 与 canonical owners
- `mem0` soft rollout 具有 admission contract、audit 语义、kill switch
- `Letta` conformance 明确覆盖 memory block、tool-rule、token-pressure / compaction
- 三个 gate 都能直接执行并验证关键不变量
- 任何失败路径都能明确落回 `shadow`，而不是隐式扩权
