# Code-Quality Problem-First Strong Consolidation Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

日期：2026-04-27

## 1. 目标

本轮只治理 `code-quality` pack。

目标是把它从“代码评审、调试、测试、验收、安全、兼容别名全混在一起”的大包，收成按用户问题分工的质量治理入口。

强收敛后的 `code-quality` 应该做到：

- 每个保留 skill 都能对应一个清楚的代码质量问题。
- 普通代码评审只由一个默认主入口负责。
- 调试、TDD、安全审计、测试报告、Windows hook、AI 代码清理分别有窄入口。
- 阶段动作和兼容别名不再和主 skill 平起平坐。
- 能安全删除的闲置薄包装先删除；资产重或内容可能有迁移价值的目录先退出路由，不直接删。

## 2. 当前问题

当前全局 pack 体检中，`code-quality` 是 P0：

| 指标 | 当前值 |
|---|---:|
| risk score | 65.20 |
| skill candidates | 16 |
| route authority candidates | 0 |
| stage assistant candidates | 0 |
| suspected overlap pairs | 16 |

当前候选为：

```text
build-error-resolver
code-review
code-reviewer
code-review-excellence
debugging-strategies
deslop
error-resolver
generating-test-reports
receiving-code-review
requesting-code-review
reviewing-code
security-reviewer
systematic-debugging
tdd-guide
verification-before-completion
windows-hook-debugging
```

实际探针已经暴露三个路由偏差：

| 用户提示 | 当前问题 |
|---|---|
| `收到CodeRabbit评审意见，帮我逐条判断是否要改` | 跑到 `aios-core / aios-qa` |
| `准备收尾，确认测试通过并给出验收证据` | 跑到 `ruc-nlpir-augmentation / flashrag-evidence` |
| `清理AI生成代码里的废话注释和多余防御式检查` | 跑到 `orchestration-core / autonomous-builder` |

这说明 `code-quality` 的问题不是单纯数量多，而是没有把“用户具体想解决什么问题”变成路由边界。

## 3. 范围

本轮直接处理：

```text
config/pack-manifest.json
config/skill-keyword-index.json
config/skill-routing-rules.json
config/skills-lock.json
bundled/skills/<code-quality-related-skill>/SKILL.md
scripts/verify/*
docs/governance/*
outputs/skills-audit/*
```

本轮可以新增 `code-quality` 专项治理脚本和治理说明。

本轮不治理：

- `bio-science`
- `research-design`
- `orchestration-core`
- `aios-core`
- 现有全局 metadata gate 旧失败
- `data-ml` 遗留的 `umap-learn` 路由旧失败

如果全局检查仍因这些旧债失败，最终报告要明确区分“本轮新增问题”和“既有问题”。

## 4. 不做什么

本轮不做这些事：

- 不重写整个 router。
- 不把所有代码相关 skill 都塞进 `code-quality`。
- 不因为某个 skill 名字像代码质量就保留它在主路由。
- 不直接删除带有脚本、references、assets 或明显迁移价值的目录。
- 不把 `code-reviewer`、`systematic-debugging` 这类核心 skill 互相合并。
- 不把阶段动作做成普通默认入口。

## 5. Router 约束

当前 router 的候选选择逻辑有一个重要约束：

- `route_authority_candidates` 才能成为主选中 skill。
- `stage_assistant_candidates` 只作为旁路建议返回，不会被普通提示直接选中。

因此，本轮不能简单把 `receiving-code-review` 和 `verification-before-completion` 放进 stage assistant 后还期待它们被直接选中。

设计选择：

- 真正只服务流程内部的 skill，放进 `stage_assistant_candidates`。
- 用户会直接问的阶段类问题，保留为“窄 route authority”，但不做默认入口。
- 窄 route authority 必须有具体关键词和负向边界，避免抢普通 code review。

## 6. Problem-First 判断规则

每个 skill 必须回答三个问题：

1. 它解决的用户问题是什么？
2. 这个问题是否属于 `code-quality` 的核心职责？
3. 是否已有更强或更清楚的 owner 能解决同一个问题？

处理规则：

- 能独立负责一个用户问题：保留为 route authority。
- 只服务某个流程节点，且用户通常不会直接问：降为 stage assistant。
- 只是兼容别名、薄包装、无独立资产：删除候选。
- 有内容价值但不该抢路由：移出 `code-quality`，目录保留，后续再迁移或显式调用。
- 资产重目录不能第一刀删，除非先完成迁移和验证。

## 7. `code-quality` 应覆盖的问题类型

| problem_id | 用户问题 | 目标 owner |
|---|---|---|
| `code_review_general` | 普通代码评审、PR review、质量检查、bug/maintainability 风险 | `code-reviewer` |
| `debug_root_cause` | 失败测试、bug、异常行为、根因定位 | `systematic-debugging` |
| `security_review` | OWASP、secret、auth、权限、输入校验、安全风险 | `security-reviewer` |
| `tdd_flow` | 明确要求 TDD、先写失败测试、红绿重构 | `tdd-guide` |
| `test_report_packaging` | 把 pytest/JUnit/coverage 结果整理成报告 | `generating-test-reports` |
| `windows_hook_debug` | Windows hook、Git Bash、WSL、`.sh` 误匹配、cannot execute binary file | `windows-hook-debugging` |
| `ai_code_cleanup` | 清理 AI 生成代码废话、冗余注释、多余防御式检查 | `deslop` |
| `review_feedback_handling` | 收到 review/CodeRabbit 意见后逐条判断是否要改 | `receiving-code-review` |
| `completion_verification` | 收尾前确认测试、验收证据、完成声明前验证 | `verification-before-completion` |

## 8. 目标保留形态

目标 `code-quality.skill_candidates` 收敛为：

```text
code-reviewer
deslop
generating-test-reports
receiving-code-review
requesting-code-review
security-reviewer
systematic-debugging
tdd-guide
verification-before-completion
windows-hook-debugging
```

目标 `route_authority_candidates` 收敛为：

```text
code-reviewer
deslop
generating-test-reports
receiving-code-review
security-reviewer
systematic-debugging
tdd-guide
verification-before-completion
windows-hook-debugging
```

目标 `stage_assistant_candidates` 收敛为：

```text
requesting-code-review
```

目标 `defaults_by_task` 保持清楚：

```json
{
  "debug": "systematic-debugging",
  "coding": "tdd-guide",
  "review": "code-reviewer"
}
```

说明：

- `receiving-code-review` 是窄主路由，因为用户会直接说“收到评审意见，帮我判断要不要改”。
- `verification-before-completion` 是窄主路由，因为用户会直接说“收尾前确认测试和证据”。
- `requesting-code-review` 更像流程动作，保留为 stage assistant，不作为普通 route authority。

## 9. 逐个 Skill 处理建议

| skill | 处理动作 | 原因 |
|---|---|---|
| `code-reviewer` | 保留主路由 | 普通代码审查、PR review、质量检查的默认入口。 |
| `systematic-debugging` | 保留主路由 | 调试和根因定位的默认入口，接管大部分构建失败和 stack trace 问题。 |
| `security-reviewer` | 保留主路由 | 安全审计是独立问题，不应被普通 review 吞掉。 |
| `tdd-guide` | 保留主路由 | TDD 是明确开发流程，边界清楚。 |
| `generating-test-reports` | 保留主路由 | 用户要交付测试报告时触发，不负责修 bug。 |
| `windows-hook-debugging` | 保留主路由 | Windows hook / Git Bash / WSL 问题足够窄，误触发风险低。 |
| `deslop` | 保留主路由 | AI 代码清理是明确问题，应修复当前跑到 `autonomous-builder` 的偏差。 |
| `receiving-code-review` | 保留为窄主路由 | 处理 review feedback，不抢普通 code review。 |
| `verification-before-completion` | 保留为窄主路由 | 处理完成声明前验证，不抢普通 test/report/debug。 |
| `requesting-code-review` | 降为 stage assistant | 更像提交前流程提醒，不作为默认评审 owner。 |
| `reviewing-code` | 删除候选，优先物理删除 | `SKILL.md` 明说是 legacy compatibility alias，且无独立资产。 |
| `build-error-resolver` | 删除候选，优先物理删除 | 薄兼容壳；构建失败由 `systematic-debugging` 接管。 |
| `code-review` | 移出 `code-quality`，暂不删 | 和 `code-reviewer` 重叠，但有脚本和 reference，先迁移再决定删除。 |
| `debugging-strategies` | 移出 `code-quality`，暂不删 | 和 `systematic-debugging` 重叠，内容较长，先做显式/迁移候选。 |
| `error-resolver` | 移出 `code-quality`，暂不删 | 资产很重，不能第一刀删除；debug 主路由先交给 `systematic-debugging`。 |
| `code-review-excellence` | 移出 `code-quality`，暂不删 | 更像 review 文化、标准、教学，不应抢实际代码审查主入口。 |

## 10. 删除和迁移边界

优先物理删除只允许满足全部条件：

- 目录只有薄 `SKILL.md` 或兼容 alias。
- 没有脚本、references、assets。
- 不在 `always required`、安装 profile 或测试固定引用中承担闭包责任。
- 路由已经由更清楚的 owner 接管。
- `vibe-offline-skills-gate.ps1` 通过。

本轮优先删除候选：

```text
reviewing-code
build-error-resolver
```

本轮只移出路由、不直接删除：

```text
code-review
debugging-strategies
error-resolver
code-review-excellence
```

这些目录后续可进入迁移批次。

## 11. 路由规则设计

需要调整三类信号。

### 11.1 强化目标 owner 的正向关键词

| owner | 关键词方向 |
|---|---|
| `code-reviewer` | `code review`, `PR review`, `quality checks`, `maintainability`, `bugs`, `代码审查`, `代码评审` |
| `systematic-debugging` | `root cause`, `failing test`, `stack trace`, `unexpected behavior`, `根因定位`, `系统化调试` |
| `security-reviewer` | `OWASP`, `security audit`, `secret leak`, `auth`, `input validation`, `安全审计` |
| `tdd-guide` | `TDD`, `red green refactor`, `先写失败测试`, `测试驱动` |
| `generating-test-reports` | `test report`, `coverage report`, `pytest report`, `测试报告`, `覆盖率报告` |
| `windows-hook-debugging` | `Windows hook`, `cannot execute binary file`, `Git Bash`, `WSL`, `.sh regex` |
| `deslop` | `AI-generated code slop`, `remove slop`, `多余注释`, `冗余防御式检查`, `清理AI生成代码` |
| `receiving-code-review` | `review feedback`, `CodeRabbit`, `评审意见`, `逐条判断`, `是否要改` |
| `verification-before-completion` | `completion gate`, `验收证据`, `完成前验证`, `收尾前确认`, `测试通过证据` |

### 11.2 给易误触发 skill 加负向边界

示例：

- `code-reviewer` 不应该抢 `CodeRabbit 评审意见逐条处理`。
- `systematic-debugging` 不应该抢 `测试报告整理`。
- `generating-test-reports` 不应该抢 `修复失败测试`。
- `verification-before-completion` 不应该抢普通 `测试报告` 或 `debug`。

### 11.3 从 pack 里移出重复 owner

从 `code-quality.skill_candidates` 移出：

```text
code-review
code-review-excellence
debugging-strategies
error-resolver
```

物理删除后也要从 `skills-lock.json` 移出：

```text
reviewing-code
build-error-resolver
```

## 12. 回归测试设计

新增或更新这些路由探针：

| 用户提示 | 期望 |
|---|---|
| `run code review and quality checks` | `code-quality / code-reviewer` |
| `做一次OWASP安全审计并给出修复建议` | `code-quality / security-reviewer` |
| `请做系统化调试和根因定位` | `code-quality / systematic-debugging` |
| `构建失败，TypeScript compile error，帮我定位` | `code-quality / systematic-debugging` |
| `按TDD方式开发，先写失败测试再重构` | `code-quality / tdd-guide` |
| `收到CodeRabbit评审意见，帮我逐条判断是否要改` | `code-quality / receiving-code-review` |
| `准备收尾，确认测试通过并给出验收证据` | `code-quality / verification-before-completion` |
| `把pytest和coverage结果整理成测试报告` | `code-quality / generating-test-reports` |
| `Windows hook error cannot execute binary file` | `code-quality / windows-hook-debugging` |
| `清理AI生成代码里的废话注释和多余防御式检查` | `code-quality / deslop` |

需要继续跑现有保护：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
```

`vibe-skill-index-routing-audit.ps1` 当前有全局旧失败。本轮应把新增 code-quality 相关用例全部跑通，并在报告里单独说明非本轮旧失败。

## 13. 审计产物

实施时建议新增：

```text
docs/governance/code-quality-problem-first-consolidation-2026-04-27.md
outputs/skills-audit/code-quality-problem-map.json
outputs/skills-audit/code-quality-problem-map.csv
outputs/skills-audit/code-quality-problem-consolidation.md
```

治理说明必须写清：

- before/after 数量。
- 保留主路由及问题归属。
- stage assistant 为什么不是主入口。
- 删除了哪些目录。
- 只是移出路由但未删除的目录。
- 哪些失败是旧债，哪些验证是本轮通过。

## 14. 成功标准

本轮完成后应满足：

- `code-quality.skill_candidates` 从 16 收敛到 10 左右。
- `route_authority_candidates` 明确列出，不再是隐式全员抢路由。
- `stage_assistant_candidates` 至少包含 `requesting-code-review`。
- `reviewing-code` 和 `build-error-resolver` 若经依赖检查安全，应物理删除。
- 三个已知误路由被修正：
  - CodeRabbit feedback 回到 `receiving-code-review`
  - completion evidence 回到 `verification-before-completion`
  - AI code cleanup 回到 `deslop`
- pack routing smoke、offline skills gate、code-quality focused probes 通过。

## 15. 风险和缓解

| 风险 | 缓解 |
|---|---|
| 删除 alias 后有安装 profile 或测试引用失败 | 删除前 `rg` 检查引用，删除后跑 offline gate 和 smoke。 |
| stage assistant 无法直接选中 | 对直接用户问题使用窄 route authority，而不是只放 stage assistant。 |
| `systematic-debugging` 过度吞掉 debug 子场景 | 用 `windows-hook-debugging`、`generating-test-reports` 的正负关键词做边界。 |
| `code-reviewer` 继续压住 `receiving-code-review` | 给 `receiving-code-review` 加 `CodeRabbit`、`评审意见`、`逐条判断` 等强关键词，并给 `code-reviewer` 加负向边界。 |
| `error-resolver` 资产被误删 | 本轮只移出路由，不物理删除。 |

## 16. 实施顺序

1. 生成 `code-quality` 问题地图和资产清单。
2. 检查 `reviewing-code`、`build-error-resolver` 是否有外部引用。
3. 修改 `pack-manifest.json` 的 candidates、route authority、stage assistant。
4. 调整 keyword index 和 routing rules。
5. 删除确认安全的闲置薄包装目录。
6. 刷新 `skills-lock.json`。
7. 添加 code-quality 回归探针。
8. 生成治理文档和审计 artifacts。
9. 跑 focused probes、pack regression、smoke、offline gate。
10. 提交实现。
