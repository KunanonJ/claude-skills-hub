# 2026-04-05 Rules And Scripts Strong Slimming Execution Plan

## Execution Summary

按“冻结文档 -> 收缩 rules -> 删除低风险脚本垃圾 -> 验证硬引用 -> phase cleanup”的顺序执行第一波 `rules/ + scripts/` 强精简。

## Frozen Inputs

- `docs/requirements/2026-04-05-rules-scripts-strong-slimming.md`
- current repo state on branch `chore/non-bundled-surface-slimming`

## Anti-Proxy-Goal-Drift Controls

### Primary Objective

提升 `rules/` 的集中度并清除明显脚本垃圾，同时不误伤 runtime / router / verify 主干。

### Non-Objective Proxy Signals

- 不把 `scripts/` 主干大删冒充“强精简”
- 不把规则内容改成更多分散文档
- 不通过破坏宿主锚点换取文件数量下降

### Validation Material Role

验证只用于证明规则收口后没有硬引用残留、格式无误、cleanup 完成。

### Declared Tier

Tight

### Intended Scope

`rules/**` 第一波合并、`scripts/release/__pycache__` 清理、docs current-entry 更新。

### Abstraction Layer Target

Governance rule surface and low-risk script hygiene.

### Completion State Target

`rules/` 从 14 个文件收缩到少数稳定文件，脚本派生垃圾消失，current-entry 指向本波文档，验证通过。

### Generalization Evidence Plan

- exact-path deleted-path scans
- `git diff --check`
- repo cleanliness checks

## Internal Grade Decision

L

## Wave Plan

1. 冻结本波 requirement / plan，并把 docs current entry 切到本波。
2. 合并 `rules/common/**` 为少数稳定规则页，保留 `agents.md`。
3. 合并 `rules/typescript/**` 为一个索引页，保留 `coding-style.md` 作为宿主锚点。
4. 删除零消费者规则叶子与 `scripts/release/__pycache__/` 派生物。
5. 验证已删路径不存在 repo 内硬引用，运行格式校验。
6. 清理 `.pytest_cache/`、`.tmp/`，执行 repo-owned node audit。

## Delivery Acceptance Plan

- `rules/` 文件数下降且保留宿主锚点
- 已删除规则叶子不再有 repo 内硬引用
- 脚本垃圾路径消失

## Completion Language Rules

- 只能宣称完成本波 `rules/` 收缩和低风险 `scripts/` 清理
- 不得宣称整个 `scripts/` 强精简已完成

## Ownership Boundaries

- root lane: requirement/plan freeze、rules 合并、脚本垃圾清理、验证与 cleanup
- deferred future waves: `scripts/overlay`、`scripts/research/learn`、`scripts/setup`、`scripts/verify/router/runtime`

## Verification Commands

```bash
git diff --check
rg -n "rules/common/coding-style.md|rules/common/engineering-instincts.md|rules/common/git-workflow.md|rules/common/hooks.md|rules/common/patterns.md|rules/common/performance.md|rules/common/security.md|rules/common/testing.md|rules/typescript/hooks.md|rules/typescript/patterns.md|rules/typescript/security.md|rules/typescript/testing.md" . -g '!outputs/**' -g '!node_modules/**'
find scripts/release -type f | sort
```

## Rollback Plan

- 若发现宿主检查或文档仍依赖被删规则叶子，优先恢复或改正引用
- 若 `rules/typescript/coding-style.md` 锚点被意外破坏，立即回退到保守保留结构

## Phase Cleanup Contract

- 清理 `.pytest_cache/`
- 清理 `.tmp/` 下本轮临时产物
- 审计 repo-owned node 进程
- 保持工作树只含预期改动
