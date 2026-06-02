# 2026-04-05 Tests Derived And Replay Hygiene

## Summary

对 `tests/` 执行保守精简：不删除测试主结构，只清理派生缓存文件，并对 `tests/replay/**` 做 exact-path 与 loader 双重消费扫描，仅在零消费者证据充分时删除 replay fixture。

## Goal

在不破坏测试、gate、proof bundle、治理文档契约的前提下，让 `tests/` 更干净、更少派生垃圾，并给出 replay fixture 是否可删的证据结论。

## Deliverable

- 删除后的 `tests/**/__pycache__` 与 `*.pyc` / `*.pyo`
- 本波 governed requirement / plan
- replay fixture 消费分析结论
- phase cleanup 收据

## Constraints

- 不删除 `tests/` 主目录或测试代码
- 不删除任何仍被脚本、测试、proof bundle、活跃 docs 直接引用的 replay fixture
- 不把“仅减少文件数量”当成完成目标
- 不回滚用户未要求撤销的既有改动

## Acceptance Criteria

- `tests/**` 下派生缓存文件被清理
- `tests/replay/**` 每个候选 fixture 都经过 exact-path / loader 双重复核
- 若无零消费者 fixture，则明确保留并给出证据
- `git diff --check` 通过

## Product Acceptance Criteria

- 用户看到的是“测试面更干净，但证明链没被砍断”
- replay fixture 的保留或删除都有证据支撑

## Manual Spot Checks

- `find tests -type d -name '__pycache__'` 无输出
- `find tests -type f \\( -name '*.pyc' -o -name '*.pyo' \\)` 无输出
- `tests/replay/platform/linux-without-pwsh.json` 若保留，应能指出其 loader

## Completion Language Policy

只有在派生物清理完成、replay fixture 结论明确、验证通过、cleanup 完成后，才允许宣称本波完成。

## Delivery Truth Contract

本波只宣称完成 `tests/` 派生物清理与 replay fixture 消费核查；若零消费者集合为空，必须如实说明为空。

## Primary Objective

清理真正的派生垃圾，并用证据判断 replay fixture 是否能删。

## Non-Objective Proxy Signals

- 不是为了“目录变短”而删除活跃 fixture
- 不是把 docs-only / proof-only 消费误判成零消费者
- 不是把测试缓存清理包装成大规模测试精简

## Validation Material Role

验证材料用于证明 replay fixture 仍有消费者或确实无消费者，以及测试派生物已移除。

## Anti-Proxy-Goal-Drift Tier

Tight

## Intended Scope

`tests/**` 的派生缓存、`tests/replay/**` 的 fixture 消费分析、对应 governed docs entry。

## Abstraction Layer Target

Test-surface hygiene and replay-fixture retention proof.

## Completion State

当派生缓存被清理、replay fixture 候选已完成消费核查、验证通过且 cleanup 完成时，本波视为完成。

## Generalization Evidence Bundle

- `find` 派生物扫描结果
- replay fixture exact-path 引用扫描
- loader / test 级复核结果

## Non-Goals

- 不重构测试组织结构
- 不新增或删改测试逻辑
- 不处理 `third_party/`、`vendor/` 本波之外的主题

## Autonomy Mode

interactive_governed

## Assumptions

- 用户接受“零消费者 fixture 为空集”也是一个有效结论
- `__pycache__` 和 `.pyc/.pyo` 属于可直接清理的派生物

## Evidence Inputs

- `tests/replay/**`
- `tests/runtime_neutral/test_router_bridge.py`
- `packages/verification-core/src/vgo_verify/router_bridge_gate_runtime.py`
- `references/proof-bundles/**/manifest.json`
- `scripts/verify/*replay*`
