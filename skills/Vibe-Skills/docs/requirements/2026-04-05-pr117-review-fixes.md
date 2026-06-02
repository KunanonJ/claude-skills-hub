# 2026-04-05 PR117 Review Fixes

## Summary

对 PR `#117` 的 review findings 做一次受治理修复波次：优先修正 `scripts/overlay/suggest-overlays.ps1` 的真实运行时问题与安全边界，再修正文档中的验证假阳性和失效证据输入。

## Goal

在不扩大 `rules/ + scripts/` 精简范围的前提下，消除本轮 PR 中已确认的问题，使分支重新达到“可审、可验、可合并”的状态。

## Deliverable

- 加固后的 `scripts/overlay/suggest-overlays.ps1`
- 修正后的 requirement / plan 文档内容
- 本波 governed requirement / plan
- 验证与 cleanup 收据

## Constraints

- 不重新打开上一波 `rules/` 和 `scripts/` 的范围，只修复 review 暴露的问题
- 不引入新的 overlay/provider 配置语义变化
- 不把统一 overlay 建议器升级成第二路由器
- 不回滚用户未要求撤销的现有精简改动

## Acceptance Criteria

- `overlay_path` 和 `config_path` 读取被限制在预期 repo 子树内
- family catalog 的无关键词请求会回退到 `stage_fallbacks`，而不是被 stage bonus 误判为有信号
- review plan 文档中的验证命令不再命中自身造成假阳性
- requirement 文档不再引用已不存在的 `__pycache__` 产物
- `git diff --check` 与针对性脚本验证通过

## Product Acceptance Criteria

- 用户看到的是“PR review 问题被闭环修复”，而不是新一轮结构性折腾
- 统一 overlay 入口的 advice-only 行为保持不变

## Manual Spot Checks

- `scripts/overlay/suggest-overlays.ps1 -Catalog agency -Task "zzqv nonmatch token" -Stage do -AsJson` 的推荐顺序符合 `stage_fallbacks.do`
- 越界路径配置会被脚本拒绝
- `docs/plans/2026-04-05-pr117-review-fixes-execution-plan.md` 中的 `rg` 示例不会命中自身

## Completion Language Policy

只有在运行时问题修复、文档一致性修复、验证通过、cleanup 完成后，才允许宣称本波完成。

## Delivery Truth Contract

本波只宣称完成 PR `#117` review findings 的修复，不宣称开启新的仓库精简波次。

## Primary Objective

修复真实缺陷与 review blocker，而不是通过表面上的“已回复 review”来制造完成假象。

## Non-Objective Proxy Signals

- 不是只回复 review comment 而不修代码
- 不是为了安全硬化而改变 overlay 选择语义
- 不是为了文档整洁而跳过运行时验证

## Validation Material Role

验证材料用于证明脚本行为恢复正确、安全边界存在、文档验证步骤自洽。

## Anti-Proxy-Goal-Drift Tier

Tight

## Intended Scope

`scripts/overlay/suggest-overlays.ps1`、本波 requirement / plan 文档、上一波受 review 影响的两份 docs 素材。

## Abstraction Layer Target

Review-driven bugfix and governance-doc correction.

## Completion State

当 review 中确认的 4 个 actionable finding 全部被修复或合理驳回、验证通过、cleanup 完成时，本波视为完成。

## Generalization Evidence Bundle

- targeted PowerShell smoke runs
- `git diff --check`
- targeted `rg` scans for self-match / stale evidence issues

## Non-Goals

- 不新增新的 `rules/` 精简范围
- 不改 `scripts/router/**`、`scripts/runtime/**`、`scripts/verify/**` 的非必要逻辑
- 不处理纯风格型 nit（除非顺手澄清且无副作用）

## Autonomy Mode

interactive_governed

## Assumptions

- PR review 中的 4 条 actionable comments 是本波主范围
- `rules/common/quality.md` 的评分制建议不构成 blocker，只需在本波结论中说明

## Evidence Inputs

- `scripts/overlay/suggest-overlays.ps1`
- `docs/plans/2026-04-05-scripts-secondary-surfaces-slimming-execution-plan.md`
- `docs/requirements/2026-04-05-rules-scripts-strong-slimming.md`
- `config/*overlays.json`
- PR `#117` review comments
