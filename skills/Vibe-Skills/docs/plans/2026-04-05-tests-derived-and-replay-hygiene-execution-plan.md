# 2026-04-05 Tests Derived And Replay Hygiene Execution Plan

## Execution Summary

按“冻结文档 -> 扫描 replay 消费 -> 删除派生缓存 -> 验证 -> cleanup”的顺序执行 `tests/` 保守精简波次。

## Frozen Inputs

- `docs/requirements/2026-04-05-tests-derived-and-replay-hygiene.md`
- current repo state on branch `chore/non-bundled-surface-slimming`

## Anti-Proxy-Goal-Drift Controls

### Primary Objective

清理 `tests/` 派生物，并仅在零消费者证据成立时删除 replay fixture。

### Non-Objective Proxy Signals

- 不把 docs/proof/test loader 仍引用的 fixture 当成可删
- 不扩大到测试结构重构
- 不用“扫描过”代替“证据充分”

### Validation Material Role

验证用于证明 replay fixture 的保留/删除结论和派生物清理结果。

### Declared Tier

Tight

### Intended Scope

`tests/**/__pycache__`、`tests/**/*.pyc`、`tests/**/*.pyo`、`tests/replay/**` fixtures。

### Abstraction Layer Target

Test hygiene and replay consumer proof.

### Completion State Target

派生缓存清空，零消费者 replay fixture 若存在则删除，若不存在则给出空集结论并保留。

## Internal Grade Decision

L

## Wave Plan

1. 冻结 requirement / plan，并把 docs current-entry 切到本波。
2. 对 `tests/replay/**` 执行 exact-path 引用扫描。
3. 对低引用候选补做 loader / test 级复核，确认是否存在间接消费者。
4. 删除 `tests/**` 下所有派生缓存文件。
5. 若零消费者 replay fixture 集合非空，则删除并修正引用；若为空，则仅记录结论。
6. 运行格式校验、派生物复查、关键 replay 消费验证。
7. 执行 phase cleanup。

## Delivery Acceptance Plan

- `tests/` 派生缓存归零
- replay fixture 删除只发生在证据充分场景
- 若零消费者为空集，结论明确写出

## Completion Language Rules

- 只能宣称完成 `tests/` 派生物与 replay hygiene 波次
- 不得宣称 `tests/` 目录整体精简完成

## Ownership Boundaries

- root lane: freeze、scan、cleanup、verify
- deferred future work: replay family重构、测试组织层面的进一步收口

## Verification Commands

```bash
git diff --check
find tests -type d -name '__pycache__'
find tests -type f \( -name '*.pyc' -o -name '*.pyo' \)
python3 -m pytest tests/runtime_neutral/test_router_bridge.py -q
```

## Rollback Plan

- 若误删 replay fixture 导致 loader/test/proof bundle 断裂，立即恢复该 fixture
- 若缓存清理误伤 tracked source file，则回退该删除并重新限定派生物模式

## Phase Cleanup Contract

- 清理 `.pytest_cache/`
- 清理 `.tmp/` 下本轮临时产物
- 审计 repo-owned node 进程
- 保持工作树只含预期 `tests/` hygiene 改动
