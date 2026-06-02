# Router Authority And Safe Fallback Design

日期：2026-05-07

## 1. 目标

本轮设计的目标不是修补一两个误路由样例，而是修复 Vibe-Skills 当前 `pack / skill` 路由面的核心治理缺口。

本轮只处理 `pack / skill` 选择逻辑与关键词边界，不重做 `task_type`、`grade`、`xl_plan` 或六阶段 Vibe 运行时。

目标是让路由满足下面三条原则：

- 窄专家只有在领域证据足够强时才允许主导。
- 低置信度时优先回退到更通用、更安全的大类专家，而不是继续冻结到错误的窄专家。
- 回归验证必须证明修的是路由系统，不是只把几个测试样例按下去。

当前总体运行时模型保持不变：

```text
skill_candidates -> selected candidate -> selected skill execution
```

本轮新增的是主导资格和安全回退合同，而不是恢复旧的 `route_authority_candidates`、`stage_assistant_candidates` 或第二套路由面。

## 2. 当前证据

当前问题不是单个 pack 偶然失误，而是现有路由合同存在三个结构性缺口。

### 2.1 低置信度只改变 route_mode，不改变错误主选

当前 `packages/runtime-core/src/vgo_runtime/router_contract_runtime.py` 的主流程会：

1. 先为每个 pack 计算 `score`
2. 选出顶部 pack
3. 在低置信度时把 `route_mode` 切成 `pack_overlay` 或 `confirm_required`

但它不会在低置信度时重新选择更安全的主选。结果是：

```text
confidence low -> confirm_required
selected.pack_id still points at the wrong top pack
later confirmation or xl_plan still starts from the wrong specialist context
```

这正是“计划冻结点看起来守规矩，但冻结出来的还是错专家计划”的根因。

### 2.2 窄专家的强正向证据门槛不是系统默认

当前 `packages/runtime-core/src/vgo_runtime/router_contract_selection.py` 已支持：

```text
requires_positive_keyword_match
```

但是这只是单个 skill 可以自愿声明的守门规则，不是窄专家的系统默认行为。

因此一个窄专家 skill 只要：

- 词表较宽
- pack priority 较高
- pack trigger keywords 与 prompt 有模糊重叠

就可能在没有真正领域锚点的情况下进入主选。

### 2.3 pack 分数会让高优先级窄领域 pack 带着弱证据上位

当前 pack 分数混合了：

```text
trigger keyword ratio
candidate relevance
priority signal
```

这意味着像 `scholarly-publishing-workflow` 这样的高优先级窄领域 pack，只要 prompt 同时出现：

```text
pipeline
build
pdf
logs
runtime
github actions
```

这一类高歧义词，就可能在缺少真正学术投稿语义的情况下进入顶部竞争。

### 2.4 当前调试 owner 和领域窄专家之间缺少显式权威边界

当前配置里，`code-quality` 已经具备较合理的通用调试 owner：

```text
debug -> systematic-debugging
```

并且 `systematic-debugging` 的正向词已经覆盖：

```text
root cause
stack trace
build error
compile error
报错
异常
根因分析
故障定位
```

但系统并没有规定：

```text
当窄领域 pack 证据不足时，优先退回 broad debug owner
```

因此“有更安全的通用专家存在”和“真的会退回到它”之间仍然断了一层。

## 3. 范围

本轮设计允许修改这些面：

```text
config/pack-manifest.json
config/skill-keyword-index.json
config/skill-routing-rules.json
config/skills-lock.json
packages/runtime-core/src/vgo_runtime/router_contract_selection.py
packages/runtime-core/src/vgo_runtime/router_contract_runtime.py
tests/unit/**
tests/runtime_neutral/**
tests/replay/route/**
scripts/verify/vibe-pack-regression-matrix.ps1
scripts/verify/vibe-skill-index-routing-audit.ps1
docs/governance/**
```

本轮明确不处理：

- `task_type` 推断逻辑
- `grade` 选择逻辑
- `xl_plan` 冻结与继续执行治理
- 六阶段 Vibe 运行时
- deep discovery、AI rerank、retrieval overlay 的产品目标重写
- installed host 部署验证

如果实现时发现某个 overlay 读取了旧字段，只允许做兼容性修正，不允许把本轮范围扩成全链路重构。

## 4. 备选方案

### Option A: 只补关键词和负关键词

做法：

- 给误路由 pack 增加 `negative_keywords`
- 给目标 owner 增加更多 `positive_keywords`
- 给个别窄 skill 手动打开 `requires_positive_keyword_match`

优点：

- 改动最小
- 短期见效快

缺点：

- 本质是 case-by-case 补丁
- 不能阻止下一个高优先级窄 pack 复制同样的问题
- 难以证明修的是合同而不是词库碰运气

### Option B: 引入 authority model 和 safe fallback contract

做法：

- 明确区分 `broad owner`、`narrow specialist`、`safe fallback`
- 先判“顶部 pack 是否有主导资格”，再决定是否沿用它
- 低置信度时把默认主选切回更安全的 owner，而不是只切 `confirm_required`

优点：

- 直接对准当前根因
- 符合“宁可回退到通用专家，也不要强推错窄专家”的产品原则
- 可以在不重写 task_type / grade 的前提下系统性提升稳定性

缺点：

- 需要同时改 manifest、selection、runtime output 和测试矩阵

### Option C: 重写为两段式路由

做法：

1. 先选任务大类
2. 再在大类内部选 skill

优点：

- 架构最干净
- 天然抑制跨域窄专家误夺权

缺点：

- 已经越过本轮边界
- 实际上会把 `task_type / domain` 这层一起重做
- 难以在一轮内控制回归风险

## 5. 推荐方案

使用 Option B。

本轮应视为一次 `problem-first` 路由治理：修复谁有资格主导、何时必须回退、以及如何证明回退是正确的。

### 5.1 Authority Model

设计上应把当前路由面视为三类角色：

| 角色 | 含义 | 默认行为 |
| --- | --- | --- |
| `broad_owner` | 负责一类宽问题面的主 owner | 可接住模糊任务与回退任务 |
| `narrow_specialist` | 只在明确领域语义出现时才允许主导 | 不得靠模糊词、priority 或弱回退夺权 |
| `safe_fallback` | 低置信度时的保守落点 | 优先保证大类正确，再决定是否确认 |

实现上可以用两层字段表达，而不必引入第二套路由系统：

```text
pack.authority_tier
pack.fallback_owner_pack_id
pack.fallback_owner_skill
```

其中：

- `authority_tier` 至少支持 `broad_owner` 和 `narrow_specialist`
- `safe_fallback` 既可以是专门 pack，也可以是某个 `broad_owner` pack 内的默认 skill

这层治理的关键不是“谁分数更高”，而是“谁有资格在当前语义下主导”。

### 5.2 Authority Eligibility Contract

pack 在进入最终主选前，必须通过主导资格判定。

建议为每个 pack row 显式生成：

```text
authority_eligible: true | false
authority_rejection_reasons: [...]
```

基础判定应至少包括：

1. `selected_candidate` 存在且可用
2. `candidate_selection_reason` 不是弱回退
3. `candidate_signal` 达到当前 tier 的最小阈值
4. 若 `authority_tier == narrow_specialist`，必须满足领域强正向证据

需要特别明确两条规则：

- `priority` 只能放大已有证据，不能替代领域证据
- pack 内部分数第一，不等于拥有跨 pack 主导资格

对 `narrow_specialist` 来说，下面这些信号默认不应足以构成主导资格：

```text
pipeline
build
logs
pdf
runtime
api
github actions
```

这些词最多只能作为辅助证据，不能单独完成夺权。

### 5.3 Low-Confidence Safe Fallback Contract

当前最大问题不是“低置信度没有被发现”，而是“低置信度没有改变错误主选”。

因此本轮必须把 fallback 合同改成：

1. 先选出原始顶部候选
2. 再做 `authority_eligible` 审查
3. 若未通过，则启动安全回退
4. `selected`、`confirm_ui` 和冻结计划都使用回退后的主选

建议固定回退顺序：

1. 用户显式指定 skill，若合法，则保留
2. 当前问题域的 `broad_owner`
3. 全局 `safe_fallback`

对调试类与日志排查类任务，优先保守回退到：

```text
code-quality -> systematic-debugging
```

而不是保留一个证据不足但分数暂时领先的窄领域 pack。

回退后，结果对象应新增审计字段：

```text
pre_fallback_top_pack_id
pre_fallback_top_skill
fallback_applied
fallback_target_pack_id
fallback_target_skill
rejected_specialist_reasons
```

这样后续任何确认界面、计划冻结点或调试证据都能回答：

```text
最初谁排第一
为什么它没有资格主导
最后为什么退回到了当前 owner
```

### 5.4 Specialist Admission Rules

本轮应把“窄专家默认需要强正向证据”升级成系统级治理，而不是继续依赖单个 skill 自愿声明。

建议新增以下准入规则：

1. 所有 `narrow_specialist` 默认开启 `requires_positive_keyword_match`
2. 窄专家应区分两层词：

```text
authority_keywords
supporting_keywords
```

含义如下：

- `authority_keywords`：决定它是否允许跨 pack 主导
- `supporting_keywords`：只用于 pack 内部排序或轻微加分

例如，对 `latex-submission-pipeline` 这类 skill：

- 可以保留 `latexmk`、`chktex`、`venue template`、`submission zip` 一类强锚点
- 但 `build pdf`、`github actions`、`pipeline` 这类高歧义词只能放在 `supporting_keywords`

这样可以避免：

```text
有 build / logs / pdf -> 被当成论文投稿流水线
```

同时建议支持 pack 级最小主导条件，例如：

```text
minimum_authority_keyword_hits
required_authority_keyword_groups
```

这样可以表达“至少命中 1 组真正领域锚点”之类规则，而不必继续把所有判断塞进一份长 `positive_keywords`。

### 5.5 Pack Cleanup Rules

本轮不是物理删除 skill 目录优先，而是先做权威面清理。

建议的第一轮治理方向：

- 保持 `code-quality` 这类通用调试 / 质量问题面为 `broad_owner`
- 保持 `docs-media` 这类明确文件操作问题面为 `broad_owner`
- 将 `scholarly-publishing-workflow` 这一类窄领域 pack 明确降为 `narrow_specialist`
- 将其他明显依赖强领域锚点的 scientific / publishing / literature 类 pack 按问题归属继续审查

对 `gh-fix-ci`、`sentry` 这类 skill，本轮不要求一定挪 pack，但要求它们不能依靠模糊日志词跨域夺权。它们应在自己的问题面内竞争，而不是把所有“日志/失败/排查”都吸到自身或其他窄领域 pack。

新的 pack 审查标准应是：

```text
它真正拥有什么用户问题
它是 broad owner 还是 narrow specialist
它低置信度时退回谁
```

说不清这三点的 pack，不应继续保留强路由权威。

## 6. 回归验证与审计证据

本轮的成功标准不能只是“几个固定 prompt 结果变了”，而必须证明跨域误吸附被系统性压住。

### 6.1 回归矩阵分类

建议把回归样本分为四类：

| 类别 | 含义 |
| --- | --- |
| `should_own` | 这个 pack / skill 本来就该赢 |
| `should_not_steal` | 不该跨域夺权 |
| `should_fallback` | 信号不足时应退回通用 owner |
| `should_rank_but_not_select` | 可进入候选榜，但不能成为主选 |

这样可以避免“最后主选看起来对了，但过程实际上仍是错路径撞对”的假阳性。

### 6.2 断言结果不只看 selected

每条关键回归除了断言：

```text
selected_pack
selected_skill
```

还应断言：

```text
authority_eligible
fallback_applied
fallback_target_pack_id
rejected_specialist_reasons
pre_fallback_top_pack_id
```

这能证明：

- 窄专家为什么被拒绝
- 安全回退是否真的发生
- 错候选是否只保留在 `ranked`，而没有成为主选

### 6.3 重点冲突矩阵

本轮必须新增覆盖这些高风险边界的真实回归：

```text
debug / logs / runtime / api failure
    vs scholarly-publishing-workflow

pdf / docx / xlsx file operations
    vs scientific writing / latex

ci / workflow logs
    vs production error / sentry

research / paper / literature
    vs code-quality / systematic-debugging

deploy / runtime
    vs broad coding or debug owners
```

每组都应至少包含：

- 强正例
- 模糊例
- 历史误吸附例
- 中英文变体

### 6.4 建议的验证层次

建议分两层验证：

1. Python 单元测试

覆盖：

- authority 资格判定
- narrow specialist 默认准入规则
- fallback 结果重写 `selected`
- rejected candidate 审计字段

2. PowerShell 路由 probe / gate

覆盖：

- 真实配置下的 pack 排名
- 回退前后主选变化
- 审计工件输出
- 回归矩阵统计

这样可以同时约束算法实现和配置漂移。

## 7. 成功标准

完成后，应能稳定满足下面这些外部可验证结果：

- 窄专家只有在出现明确领域锚点时才会主导。
- 模糊 prompt 不会继续冻结到错误窄专家，而是优先回退到更安全的大类 owner。
- `confirm_required` 不再只是提醒用户风险，而是建立在已经过安全回退的主选之上。
- `ranked` 仍保留原始竞争证据，但 `selected` 只反映通过资格审查后的主选。
- 回归矩阵能解释“为什么回退”，而不只是给出一个最终结果值。

## 8. 不做什么

本轮明确不做这些事：

- 不重写 `task_type` 推断
- 不重写 `grade` 选择
- 不修改 `xl_plan`、`requirement_doc` 或六阶段运行时的停顿治理
- 不把所有 pack 全部重构成新的多段式领域分类器
- 不为了降低误路由而恢复旧的 `route_authority_candidates` 或 `stage_assistant_candidates`
- 不声称这轮已经修好所有 overlay，只处理与 `pack / skill` 主导资格直接相关的路由合同

## 9. 推荐实施顺序

实施时建议按下面顺序推进：

1. 在 `pack-manifest` 中引入 authority / fallback 元数据
2. 在 `router_contract_selection.py` 中补齐窄专家默认准入逻辑
3. 在 `router_contract_runtime.py` 中实现 authority 审查与回退后重写 `selected`
4. 为高风险 pack 做第一轮 `broad_owner` / `narrow_specialist` 清理
5. 扩充 unit tests、runtime-neutral tests 和 PowerShell probe gates
6. 生成新的回归证据与治理说明

这个顺序的目的，是先把“谁有资格主导”和“低置信度时如何安全回退”固定下来，再做 pack 级清理，避免继续出现靠补词库驱动的修修补补。
