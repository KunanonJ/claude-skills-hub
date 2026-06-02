# 2026-04-05 Rules And Scripts Strong Slimming

## Summary

对 `rules/` 与 `scripts/` 执行高内聚、低耦合导向的强精简：先冻结当前治理边界，再优先收缩零消费者规则叶子、删除派生垃圾文件，并为后续 `scripts/` 子家族收口建立明确波次。

## Goal

把 `rules/` 从分散叶子收缩成少数稳定治理文档，把 `scripts/` 从“直接删风险高”的大平面拆成可分波治理的子家族。

## Deliverable

- 精简后的 `rules/` 文档结构
- 删除后的明显派生垃圾与低价值脚本残留
- 新的 `rules/ + scripts/` governed requirement / plan
- 保留主干 runtime / router / verify contract 的第一波收缩结果

## Constraints

- 不直接破坏 `scripts/verify/**`、`scripts/router/**`、`scripts/runtime/**`、`scripts/bootstrap/**` 的 live contract
- 保留仍被显式宿主检查消费的 `rules/common/agents.md` 与 `rules/typescript/coding-style.md`
- 不删除仍被配置、测试、文档或安装检查直接消费的脚本路径，除非同步修复消费者
- 不回滚用户未要求撤销的已有改动

## Acceptance Criteria

- `rules/` 文件数显著下降，但保留宿主锚点与最小治理可读性
- `scripts/release/__pycache__/` 这类派生垃圾被清除
- 所有已删除规则叶子在 repo 内不存在残余硬引用
- `docs/requirements/README.md` 与 `docs/plans/README.md` 切换到本波 current entry
- `git diff --check` 通过

## Product Acceptance Criteria

- 用户看到的是“规则文档更少、更集中”，而不是简单把内容打散到更多新文件
- `scripts/` 第一波只动低风险部分，不引入 runtime / verify 回归

## Manual Spot Checks

- `rules/common/agents.md` 仍在
- `rules/typescript/coding-style.md` 仍在
- `rules/` 目录树明显更短
- `scripts/release/__pycache__/` 不再存在

## Completion Language Policy

只有在规则叶子已收缩、硬引用已修复、验证命令通过、阶段清理完成后，才允许宣称本波完成。

## Delivery Truth Contract

本波只宣称完成 `rules/` 第一阶段收缩与 `scripts/` 第一波低风险清理；不宣称已完成整个 `scripts/` 强精简计划。

## Primary Objective

减少真实碎片面，而不是为了删除数量破坏宿主、安装或运行契约。

## Non-Objective Proxy Signals

- 不是简单把所有 `rules/` 文件改名后继续平铺
- 不是为了强精简而粗暴删除 `scripts/verify` 或 `scripts/runtime` 主干
- 不是以“目录更空”代替“结构更高内聚”

## Validation Material Role

验证材料用于证明保留锚点仍存在、已删路径没有残余硬引用、工作树无格式错误。

## Anti-Proxy-Goal-Drift Tier

Tight

## Intended Scope

`rules/**`、`scripts/release/**` 的明显派生物、`docs/requirements/README.md`、`docs/plans/README.md`，以及本波 requirement / plan 文档。

## Abstraction Layer Target

Repository governance rules surface and low-risk script hygiene surface.

## Completion State

当 `rules/` 已从多叶分散结构收束成少数稳定文档、第一波低风险脚本垃圾已清理、验证通过且 cleanup 完成时，本波视为完成。

## Generalization Evidence Bundle

- deleted-path hard-reference scan
- `git diff --check`
- repo status after cleanup

## Non-Goals

- 不在本波重构 `scripts/verify/**` gate 家族
- 不在本波重构 `scripts/router/**` 或 `scripts/runtime/**`
- 不在本波完成整个 `scripts/` 子家族合并

## Autonomy Mode

interactive_governed

## Assumptions

- 用户认可先做 `rules/` 高收益收缩，再逐波处理 `scripts/`
- `rules/common/agents.md` 与 `rules/typescript/coding-style.md` 需要继续作为宿主/检查锚点保留
- `scripts/release/__pycache__/` 属于纯派生垃圾，可以直接删除

## Evidence Inputs

- `rules/common/*.md`
- `rules/typescript/*.md`
- `scripts/release/build_release_bundle.py`
- `check.sh`
- `check.ps1`
- `scripts.check.upstream.sh`
- `adapters/codex/closure.json`
