# 2026-04-05 Scripts Secondary Surfaces Slimming

## Summary

在不触碰 `scripts/verify/**`、`scripts/router/**`、`scripts/runtime/**` 主干契约的前提下，继续收缩 `scripts/` 的次级表面：把 overlay 家族脚本合并为单入口，并把 `scripts/learn/` 并回 `scripts/research/`。

## Goal

减少 `scripts/` 的入口碎片，提升相关脚本的高内聚与可导航性，同时保持现有 advice-first 行为与治理边界。

## Deliverable

- 一个统一的 `scripts/overlay/` 建议入口
- 被合并后的 `scripts/research/` 与移除的 `scripts/learn/`
- 修正后的当前文档与 gate 引用
- 本波 governed requirement / plan

## Constraints

- 不改变 BrowserOps provider 建议逻辑的治理边界
- 不改变 overlay suggestion 的 advice-only 语义
- 不破坏 `scripts/verify/vibe-adaptive-routing-readiness-gate.ps1` 对学习脚本存在性的检查
- 不破坏现有 `config/*overlays.json` 与 `config/vco-overlays.json` 的契约

## Acceptance Criteria

- `scripts/overlay/` 只保留单一 overlay 建议入口与 `suggest-browserops-provider.ps1`
- 旧的 `suggest-agency-overlays.ps1`、`suggest-gitnexus-overlays.ps1`、`suggest-turix-cua-overlays.ps1`、`suggest-vco-overlays.ps1` 被删除
- `scripts/learn/` 目录被拔除，`vibe-adaptive-train.ps1` 迁入 `scripts/research/`
- active docs / gate 引用已同步到新路径
- `git diff --check` 通过

## Product Acceptance Criteria

- 用户看到的是更少的脚本入口，而不是更多 wrapper
- overlay 与 research/learn 的功能仍可被当前文档和 gate 正确发现

## Manual Spot Checks

- `scripts/overlay/suggest-overlays.ps1` 可存在并作为统一入口
- `scripts/overlay/` 不再存在旧的四个家族脚本
- `scripts/research/vibe-adaptive-train.ps1` 存在
- `scripts/learn/` 不再有文件

## Completion Language Policy

只有在旧路径引用修正、工作树格式校验通过、并完成阶段清理后，才允许宣称这一波完成。

## Delivery Truth Contract

本波只宣称完成 `overlay + research/learn` 次级脚本面收口；不宣称整个 `scripts/` 精简完成。

## Primary Objective

在不改主干 runtime 契约的前提下减少脚本入口碎片。

## Non-Objective Proxy Signals

- 不是通过增加 wrapper 或 helper 数量伪装成“收口”
- 不是为了删文件而改坏 docs / gate 引用
- 不是把 overlay 建议器升级成第二路由器

## Validation Material Role

验证材料用于证明旧路径已退出 active docs/gates，新的入口已接住当前消费者。

## Anti-Proxy-Goal-Drift Tier

Tight

## Intended Scope

`scripts/overlay/**`、`scripts/research/**`、`scripts/learn/**`、少量 `docs/**` 与 `scripts/verify/**` 引用修补。

## Abstraction Layer Target

Secondary script surfaces and advice-first helper entrypoints.

## Completion State

当 overlay 入口收成单点、learn 已并回 research、active docs/gates 改为新路径、且验证清理完成时，本波视为完成。

## Generalization Evidence Bundle

- deleted-path exact reference scan
- `git diff --check`
- targeted script smoke run

## Non-Goals

- 不重构 `scripts/setup/**`
- 不重构 `scripts/verify/**` gate family
- 不改变 `config/*overlays.json` 的语义结构

## Autonomy Mode

interactive_governed

## Assumptions

- 用户认可继续推进 `scripts/` 次级表面的强精简
- 旧 overlay 家族脚本之间的逻辑足够同构，可以统一到单入口
- `scripts/learn/` 只剩一个脚本，合并入 `scripts/research/` 不会引起职责混乱

## Evidence Inputs

- `scripts/overlay/*.ps1`
- `scripts/research/*.ps1`
- `scripts/learn/vibe-adaptive-train.ps1`
- `docs/design/*overlay*.md`
- `docs/external-tooling/gitnexus-execution-checklist.md`
- `docs/governance/observability-consistency-governance.md`
- `scripts/verify/vibe-adaptive-routing-readiness-gate.ps1`
