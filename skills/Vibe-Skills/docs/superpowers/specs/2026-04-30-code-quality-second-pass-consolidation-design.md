# Code-Quality Second-Pass Consolidation Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

日期：2026-04-30

## 1. 目标

本轮只治理 `code-quality` pack 的第二轮收敛。

目标不是重做六阶段 Vibe 运行时，也不是恢复阶段助手、辅助专家、咨询态或主/次技能。当前总体架构保持简化模型：

```text
candidate skill -> selected skill -> used / unused
```

本轮目标是：

- 保持 `code-quality` 当前 10 个直接 route owner 的任务边界。
- 清理旧治理文档中已经过时的 `stage assistant` 描述。
- 清理 surviving skill 文本里对旧 code-quality skills 的交叉调用和辅助专家暗示。
- 审阅被移出 pack 但仍存在于 `bundled/skills` 的旧目录。
- 迁移可复用内容后，物理删除低质量或重复旧 skill。
- 对不能安全删除的资产重目录，明确保留原因和后续迁移边界。

完成后，`code-quality` 应该继续是一个直接、可解释的路由面：每个保留 skill 都能独立回答“这个用户问题由谁负责”。

## 2. 当前状态

当前 `config/pack-manifest.json` 中，`code-quality` 为：

| 项目 | 当前值 |
|---|---:|
| `skill_candidates` | 10 |
| `route_authority_candidates` | 10 |
| `stage_assistant_candidates` | 0 |
| `defaults_by_task` | 3 |

当前直接 route owner：

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

当前默认任务映射：

```json
{
  "debug": "systematic-debugging",
  "coding": "tdd-guide",
  "review": "code-reviewer"
}
```

这说明 `code-quality` 已经不再使用阶段助手。旧文档中关于 `requesting-code-review` 是 `stage assistant` 的描述已经过时。

## 3. 当前问题

### 3.1 旧文档与当前配置矛盾

`docs/governance/code-quality-problem-first-consolidation-2026-04-27.md` 仍把 `requesting-code-review` 写成阶段助手。当前真实配置已经把它作为直接 route owner，负责准备 review request。

这会让后续维护者误以为 `code-quality` 仍有阶段助手状态。

### 3.2 旧 skill 目录仍存在

这些旧目录已经不在当前 `code-quality.skill_candidates` 中，但仍存在于 `bundled/skills`：

```text
code-review
debugging-strategies
error-resolver
code-review-excellence
```

初步判断：

| skill | 当前判断 |
|---|---|
| `code-review` | 与 `code-reviewer` 重叠，但含 `references/style-guide.md` 和 `scripts/check_style.py`，需要先迁移再判断删除。 |
| `debugging-strategies` | 与 `systematic-debugging` 重叠，当前只有 `SKILL.md`，是优先删除候选。 |
| `error-resolver` | 与 `systematic-debugging` 重叠，但含大量 `analysis/`、`patterns/`、`replay/` 内容，资产重，不能第一刀删除。 |
| `code-review-excellence` | 更像 review 文化、培训或标准，不应作为代码质量直接路由专家，需判断是否删除或迁移到 `code-reviewer` 的参考材料。 |

### 3.3 surviving skill 里仍有旧交叉调用暗示

一些 surviving skill 仍提到旧 owner，例如：

```text
code-review
debugging-strategies
error-resolver
code-review-excellence
```

这类文本不会自动证明 live routing 有问题，但会破坏用户要求的简洁架构：看起来像还有辅助专家、交叉调用、旧专家调度。

### 3.4 全局审计仍可能把合理边界误判为 overlap

全局 pack 审计会把这些共享 `review` 词根的 skill 视为疑似 overlap：

```text
code-reviewer <-> receiving-code-review
code-reviewer <-> requesting-code-review
code-reviewer <-> security-reviewer
```

这不一定是真问题。当前边界是：

| skill | 独立问题 |
|---|---|
| `code-reviewer` | 新鲜代码审查、PR review、质量和可维护性检查。 |
| `receiving-code-review` | 已经收到 CodeRabbit/GitHub/人工评审意见，逐条判断是否接受和修改。 |
| `requesting-code-review` | 准备发起 review request，整理范围、diff、reviewer prompt。 |
| `security-reviewer` | 明确的安全审计、OWASP、secret、auth、injection 等风险。 |

因此本轮应谨慎处理全局审计：不要为了降低分数而合并已经清楚的直接 owner。

## 4. 范围

本轮可以处理：

```text
config/pack-manifest.json
config/skill-keyword-index.json
config/skill-routing-rules.json
config/skills-lock.json
bundled/skills/code-reviewer/**
bundled/skills/systematic-debugging/**
bundled/skills/requesting-code-review/**
bundled/skills/receiving-code-review/**
bundled/skills/security-reviewer/**
bundled/skills/deslop/**
bundled/skills/generating-test-reports/**
bundled/skills/verification-before-completion/**
bundled/skills/tdd-guide/**
bundled/skills/windows-hook-debugging/**
bundled/skills/code-review/**
bundled/skills/debugging-strategies/**
bundled/skills/error-resolver/**
bundled/skills/code-review-excellence/**
packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py
tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py
tests/runtime_neutral/test_final_stage_assistant_removal.py
scripts/verify/vibe-pack-regression-matrix.ps1
scripts/verify/vibe-skill-index-routing-audit.ps1
docs/governance/**
```

本轮不处理：

- `bio-science`
- `data-ml`
- `docs-media`
- `research-design`
- `science-chem-drug`
- 六阶段 Vibe runtime
- specialist execution 物质使用证明
- installed Codex host 部署

## 5. 不做什么

本轮明确不做这些事：

- 不恢复 `stage_assistant_candidates`。
- 不新增“辅助专家”“咨询专家”“主技能/次技能”状态。
- 不把 `requesting-code-review` 降回阶段助手。
- 不把 `receiving-code-review`、`requesting-code-review`、`security-reviewer` 粗暴并入 `code-reviewer`。
- 不为了降低审计分数删除有明确任务边界的高质量 skill。
- 不直接删除 `error-resolver` 这类资产重目录。
- 不声称这些 skills 已在真实 Vibe 任务中被物质使用。

## 6. 目标架构

目标仍是 10 个直接 owner，0 个阶段助手。

| problem_id | 用户问题 | 目标 owner |
|---|---|---|
| `code_review_general` | 新鲜代码审查、PR review、质量检查、可维护性和回归风险 | `code-reviewer` |
| `review_request_preparation` | 准备发起代码审查，整理范围、diff、reviewer prompt | `requesting-code-review` |
| `review_feedback_handling` | 收到 CodeRabbit/GitHub/人工评审意见后逐条判断和处理 | `receiving-code-review` |
| `security_review` | OWASP、安全审计、secret、auth、injection、权限风险 | `security-reviewer` |
| `debug_root_cause` | bug、失败测试、构建失败、异常行为、根因定位 | `systematic-debugging` |
| `windows_hook_debug` | Windows hook、Git Bash、WSL、cannot execute binary file | `windows-hook-debugging` |
| `tdd_flow` | TDD、先写失败测试、红绿重构 | `tdd-guide` |
| `test_report_packaging` | 生成测试报告、coverage summary、JUnit/test summary | `generating-test-reports` |
| `completion_verification` | 收尾前确认测试、验收证据、完成声明前验证 | `verification-before-completion` |
| `ai_code_cleanup` | 清理 AI 生成代码废话注释、冗余防御式检查、模板噪声 | `deslop` |

目标 `code-quality` 仍保持：

```text
skill_candidates = 10
route_authority_candidates = 10
stage_assistant_candidates = 0
```

## 7. 旧目录处理设计

| skill | 目标处理 | 理由 |
|---|---|---|
| `debugging-strategies` | 优先物理删除，或迁移少量有价值文字后删除 | 只剩 `SKILL.md`，与 `systematic-debugging` 重叠，独立路由价值低。 |
| `code-review-excellence` | 审阅后删除或迁移到 `code-reviewer` references | 偏 review 文化/培训，不应作为独立专家。 |
| `code-review` | 先迁移 `style-guide.md` 和 `check_style.py`，再删除目录 | 与 `code-reviewer` 重叠，但有可复用资产，不能直接删。 |
| `error-resolver` | 暂不删除，先记录迁移计划 | 资产重，包含多语言/多场景错误模式，可后续并入 `systematic-debugging` references。 |

删除必须满足：

- 不在当前 `pack-manifest` 的 active candidates 中。
- 不在 active routing rules 中作为可选 route owner。
- 可复用 assets 已迁移或明确放弃。
- `skills-lock.json` 已刷新。
- offline skill gate 通过。
- 相关旧 ID 不再出现在 live `config`、`scripts`、`bundled` 活跃语义里，治理记录和测试删除清单除外。

## 8. 文本清理设计

需要清理两类文本。

第一类是过时阶段助手措辞：

```text
stage assistant
阶段助手
辅助专家
consultation
advisory
primary/secondary skill
```

如果这些词用于描述已经废弃的旧设计，应删除或改成当前直接路由模型。

第二类是旧 skill 交叉调用暗示：

```text
code-review
debugging-strategies
error-resolver
code-review-excellence
```

如果出现在 active skill 的“推荐调用 / 调度 / scheduling / invoke”语境中，应改成当前 owner：

| 旧引用 | 新 owner |
|---|---|
| `code-review` | `code-reviewer` |
| `code-review-excellence` | `code-reviewer` 或删除培训型暗示 |
| `debugging-strategies` | `systematic-debugging` |
| `error-resolver` | `systematic-debugging` |

治理记录和旧计划可以保留历史说明，但新治理文档必须明确这是历史状态，不是当前架构。

## 9. 路由和审计设计

本轮不应削弱当前已经通过的边界 probes：

| prompt | 应命中 |
|---|---|
| `run code review and quality checks` | `code-quality / code-reviewer` |
| `收到CodeRabbit评审意见，帮我逐条判断是否要改` | `code-quality / receiving-code-review` |
| `请帮我准备发起一次代码审查，整理 review 请求材料` | `code-quality / requesting-code-review` |
| `code review and security audit` | `code-quality / security-reviewer` |
| `构建失败，TypeScript compile error，帮我定位` | `code-quality / systematic-debugging` |
| `write failing tests first for this feature` | `code-quality / tdd-guide` |
| `准备收尾，确认测试通过并给出验收证据` | `code-quality / verification-before-completion` |
| `清理AI生成代码里的废话注释和多余防御式检查` | `code-quality / deslop` |

如果调整全局审计，应只修正误判逻辑，不放宽真实风险：

- `review_request_preparation`、`review_feedback_handling`、`security_review` 不应因为共享 `review` 词根被视作必须合并。
- 真正重复的旧目录仍应被 deletion/migration map 追踪。
- `stage_assistant_count` 必须保持 0。

## 10. 验证设计

实现后至少运行：

```powershell
python -m pytest tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_final_stage_assistant_removal.py -q
.\scripts\verify\vibe-code-quality-pack-consolidation-audit-gate.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
git diff --check
```

如果删除旧目录，还需要搜索旧 ID：

```powershell
rg -n -P "\b(code-review|debugging-strategies|error-resolver|code-review-excellence)\b" config scripts bundled
```

允许保留的旧 ID 引用范围：

- 新治理文档中的迁移/删除记录。
- 审计测试里的历史删除清单。
- 明确标注为 legacy compatibility 的白名单。

不允许保留的旧 ID 引用范围：

- active `pack-manifest` candidates。
- active `skill-routing-rules` route owner。
- active skill 的“invoke/schedule/route to old skill”说明。

## 11. 风险和缓解

| 风险 | 缓解 |
|---|---|
| 误删 `error-resolver` 资产 | 本轮不物理删除 `error-resolver`，只做迁移评估和旧引用清理。 |
| 为了压缩数量破坏 review/request/feedback/security 边界 | 保留当前 10 个直接 owner，靠 probes 保护窄任务。 |
| 旧文档继续误导后续维护 | 更新治理文档，明确 2026-04-30 后 `stage_assistant_candidates=0`。 |
| 全局审计继续把共享 `review` 词根判成 P0 | 调整审计口径或在治理 note 中解释误判边界。 |
| 删除目录后 lock/config 不一致 | 删除后刷新 `skills-lock.json` 并运行 offline gate。 |

## 12. 成功标准

本轮完成后应满足：

- `code-quality.stage_assistant_candidates = []`。
- `requesting-code-review` 仍是直接 route owner。
- `code-quality` 的 10 个保留 owner 均有清楚问题边界。
- 旧文档不再把当前架构描述为阶段助手模型。
- 可安全删除的旧低质量目录已物理删除。
- 资产重目录的保留原因和迁移边界已记录。
- active config/scripts/bundled 文本不再暗示旧 code-quality skills 仍是可调度辅助专家。
- 路由回归和 offline gate 通过。
- 最终报告区分“routing/config/bundled cleanup”与“真实任务中的 material skill use”。
