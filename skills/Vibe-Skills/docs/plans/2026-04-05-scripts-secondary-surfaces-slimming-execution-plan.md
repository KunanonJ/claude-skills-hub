# 2026-04-05 Scripts Secondary Surfaces Slimming Execution Plan

## Execution Summary

按“冻结文档 -> overlay 单入口化 -> learn 并回 research -> 修 active docs/gates -> 验证与 cleanup”的顺序执行 `scripts/` 次级表面收口。

## Frozen Inputs

- `docs/requirements/2026-04-05-scripts-secondary-surfaces-slimming.md`
- current repo state on branch `chore/non-bundled-surface-slimming`

## Anti-Proxy-Goal-Drift Controls

### Primary Objective

减少脚本入口碎片，不误伤 `scripts/` 主干契约。

### Non-Objective Proxy Signals

- 不引入新的 wrapper 森林
- 不把 advice-first 变成执行控制面
- 不为了删目录而留下旧路径死引用

### Validation Material Role

验证用于证明 active docs/gates 已迁移到新入口，旧入口只留在历史材料中。

### Declared Tier

Tight

### Intended Scope

`scripts/overlay/**`、`scripts/research/**`、`scripts/learn/**`、少量 active docs/gates。

### Abstraction Layer Target

Advice-first helper surface consolidation.

### Completion State Target

overlay 家族脚本被一个入口替代，learn 并回 research，active docs/gates 已改向新路径。

### Generalization Evidence Plan

- exact-path deleted-path scans
- `git diff --check`
- smoke run for new overlay entry

## Internal Grade Decision

L

## Wave Plan

1. 冻结本波 requirement / plan，并把 docs current-entry 切到本波。
2. 新增 `scripts/overlay/suggest-overlays.ps1`，吸收 agency / gitnexus / turix-cua / ruc-nlpir / vco 的建议逻辑。
3. 删除四个旧 overlay 家族脚本，仅保留 BrowserOps provider 建议脚本。
4. 将 `scripts/learn/vibe-adaptive-train.ps1` 迁入 `scripts/research/`，并更新 docs / gate 引用。
5. 修补 `scripts/README.md`、`scripts/overlay/README.md`、`scripts/research/README.md` 与相关设计文档。
6. 运行 deleted-path 扫描、格式校验、overlay smoke run，之后执行 cleanup。

## Delivery Acceptance Plan

- 新 overlay 单入口可支持原有家族场景
- BrowserOps provider 脚本保持独立
- `scripts/learn/` 不再保留活动文件

## Completion Language Rules

- 只能宣称完成次级脚本面收口
- 不得宣称 `scripts/verify/router/runtime` 已被精简

## Ownership Boundaries

- root lane: new entrypoint、path migration、active docs/gates 修补、验证与 cleanup
- deferred future waves: `scripts/setup/**`、`scripts/verify/**`、`scripts/router/**`、`scripts/runtime/**`

## Verification Commands

```bash
git diff --check
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/overlay/suggest-overlays.ps1 -Catalog agency -Task "test api bug" -Stage do -AsJson
rg -n "suggest-agency-overlays.ps1|suggest-gitnexus-overlays.ps1|suggest-turix-cua-overlays.ps1|suggest-vco-overlays.ps1|scripts/learn/vibe-adaptive-train.ps1" scripts config tests references -g '!outputs/**' -g '!node_modules/**'
```

## Rollback Plan

- 若新单入口 smoke run 失败，恢复旧 overlay 家族脚本并重新切回旧路径
- 若 learn -> research 迁移导致 gate 断裂，先恢复旧路径或双保留再做下一次收口

## Phase Cleanup Contract

- 清理 `.pytest_cache/`
- 清理 `.tmp/` 下本轮临时产物
- 审计 repo-owned node 进程
- 保持工作树只含预期改动
