# Memory Runtime v3 Contract

## Contract Objective

Memory Runtime v3 把 `memory-runtime-v2` 的 owner boundary、`mem0` 的 preference lane、`Letta` 的 contract vocabulary 收束成一个 **可运行但不扩权** 的统一合同层。

它的核心目标不是增加新的 memory owner，而是把晋升条件写清楚。

## Canonical owner matrix

| Memory Need | Canonical Owner | Non-transfer Rule |
|---|---|---|
| session truth | `state_store` | external lanes cannot replace it |
| explicit project decision | `Serena` | `mem0` cannot persist project truth |
| short-term semantic recall | `ruflo` | `Letta` only describes policy, not cache ownership |
| long-term relationship memory | `Cognee` | `mem0` remains preference-only |

## Extension lanes

| Lane | Allowed output | Required contract | Forbidden authority |
|---|---|---|---|
| `mem0` | preference write suggestion / audited soft write | `references/mem0-write-admission-contract.md` | route assignment、primary session state、canonical project decision |
| `Letta` | memory block mapping / archival search vocabulary / tool-rule guidance / token-pressure policy | `references/memory-block-contract.md` + `references/tool-rule-contract.md` | runtime takeover、second orchestrator、route mutation |

## Runtime invariants

1. `VCO` remains the single control plane.
2. All memory guidance is post-route and advisory-first.
3. `mem0` can be promoted only as a soft_candidate lane, never as primary owner.
4. `Letta` conformance can tighten policy checks, but cannot create a new runtime surface.
5. Any unresolved conflict forces the plane back to `shadow`.

## Promotion contract

| Stage | Meaning | Required evidence |
|---|---|---|
| `shadow` | governance baseline only | `vibe-memory-runtime-v3-gate` |
| `soft_candidate` | `mem0` write lane becomes auditable and opt-in | `vibe-mem0-softrollout-gate` + rollback path |
| `strict_candidate` | `Letta` vocabulary checks become release-blocking | `vibe-letta-policy-conformance-gate` + board review |

## Minimum evidence bundle

- `config/memory-runtime-v3-policy.json`
- `docs/memory-runtime-v3-governance.md`
- `references/mem0-write-admission-contract.md`
- `docs/letta-policy-conformance.md`
- Gate outputs for all three Wave64-66 checks
- Explicit rollback command that preserves canonical owners

## Execution note

`memory-runtime-v3` is a governance plane, not a new store.
If a proposal implies another truth-source, another orchestrator, or silent route mutation, the contract is invalid.
