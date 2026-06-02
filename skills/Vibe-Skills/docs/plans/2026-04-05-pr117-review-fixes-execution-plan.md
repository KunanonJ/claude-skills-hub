# 2026-04-05 PR117 Review Fixes Execution Plan

## Execution Summary

按“冻结文档 -> 修运行时问题 -> 修文档问题 -> 验证 -> phase cleanup -> commit/push”顺序执行 PR `#117` review-fix 波次。

## Frozen Inputs

- `docs/requirements/2026-04-05-pr117-review-fixes.md`
- PR `#117` 当前 review findings
- branch `chore/non-bundled-surface-slimming`

## Anti-Proxy-Goal-Drift Controls

### Primary Objective

关闭 review blocker，恢复 PR 的可合并状态。

### Non-Objective Proxy Signals

- 不把“回复评论”当成修复完成
- 不借 review 修复扩大脚本重构范围
- 不跳过脚本验证直接推送

### Validation Material Role

验证用于证明行为修正而不是只证明文件被编辑过。

### Declared Tier

Tight

### Intended Scope

`scripts/overlay/suggest-overlays.ps1`、两份受影响 docs、current-entry README。

### Abstraction Layer Target

Bugfix and review-closure wave.

### Completion State Target

PR review 中的 4 条 actionable finding 被修复，验证通过，cleanup 完成，分支已推送。

## Internal Grade Decision

L

## Wave Plan

1. 冻结 requirement / plan，并把 docs current-entry 切到本波。
2. 在 `scripts/overlay/suggest-overlays.ps1` 中加入 repo 子树路径约束。
3. 修正 family catalog 的信号判定，确保 stage-only bonus 不压掉 `stage_fallbacks`。
4. 修正文档中的验证命令自命中问题与失效 evidence input。
5. 运行 targeted smoke tests、格式校验与 review 回归检查。
6. 清理临时产物与 repo-owned node audit。
7. 提交并推送到现有 PR 分支。

## Delivery Acceptance Plan

- 路径越界输入被拒绝
- family catalog 无关键词输入按 fallback 排序
- docs verification example 自洽
- PR 分支更新成功

## Completion Language Rules

- 只能宣称修复 review findings，不得宣称开启新一轮目录精简
- 若有建议型 nit 未处理，必须明确说明其不构成 blocker

## Ownership Boundaries

- root lane: freeze、code fix、docs fix、verify、cleanup、push
- out of scope: unrelated PR comments, broader repo slimming

## Verification Commands

```bash
git diff --check
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/overlay/suggest-overlays.ps1 -Catalog agency -Task "zzqv nonmatch token" -Stage do -AsJson
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/overlay/suggest-overlays.ps1 -Catalog gitnexus -Task "zzqv nonmatch token" -Stage review -AsJson
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/verify/vibe-adaptive-routing-readiness-gate.ps1
rg -n "suggest-agency-overlays.ps1|suggest-gitnexus-overlays.ps1|suggest-turix-cua-overlays.ps1|suggest-vco-overlays.ps1|scripts/learn/vibe-adaptive-train.ps1" scripts config tests references -g '!outputs/**' -g '!node_modules/**'
```

## Rollback Plan

- 若路径约束导致合法 overlay/config 无法读取，则回退到上一提交并缩小约束实现
- 若 family fallback 修复改变既有推荐行为超出预期，则恢复原逻辑并补针对性测试证据

## Phase Cleanup Contract

- 清理 `.pytest_cache/`
- 清理 `.tmp/` 与本轮 `/tmp` 临时产物
- 审计 repo-owned node 进程
- 保持工作树只含预期修复改动
