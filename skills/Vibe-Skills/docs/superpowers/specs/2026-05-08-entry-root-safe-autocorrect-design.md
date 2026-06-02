# Entry Root Safe Autocorrect Design

日期：2026-05-08

## 1. 目标

本轮设计的目标不是重做 Vibe-Skills 的安装、runtime 布局或宿主集成，而是用最小修改的原则，修复两类高频入口问题：

- 公开入口把用户工作目录误当成 `repo_root`，随后在 adapter registry / canonical contract 解析处报错。
- Windows 上从 `bash` / WSL / Git Bash 进入 shell 入口时，外层命令链不稳定，用户只能看到 `127` 或原始 traceback。

本轮目标是让公开入口满足下面四条原则：

- 高置信度场景下自动纠偏继续执行。
- 低置信度场景下明确阻断，不再让用户看到底层 traceback。
- 自动纠偏必须是无副作用的解释层修正，不做危险操作。
- 第一阶段只改最相关入口，不把问题扩成全链路重构。

## 2. 当前证据

当前问题不是“某个项目目录没初始化”，而是公开入口对路径角色和 shell lane 的理解不一致。

### 2.1 Python canonical-entry 直接相信传入的 repo_root

当前 `packages/runtime-core/src/vgo_runtime/canonical_entry.py` 会在真正启动前调用：

```text
resolve_canonical_vibe_contract(repo_root_path, host_id)
```

而 `packages/contracts/src/vgo_contracts/canonical_vibe_contract.py` 会继续把这个 `repo_root` 交给 adapter registry 解析。

这意味着：

- 如果宿主把 `D:\allworks\bj-refinery` 之类的工作目录误传成 `repo_root`
- 且该目录不是 Vibe-Skills 根

那么系统会直接在 adapter registry / canonical contract 解析处失败，用户看到的是 registry 缺失或原始 traceback，而不是“你把工作目录当成了 runtime 根”。

### 2.2 PowerShell 入口已经有更稳的 repo root 解析思路

当前 `scripts/common/vibe-governance-helpers.ps1` 里的 `Resolve-VgoRepoRoot` 会从脚本自身位置向上解析 governed repo root，而不是完全相信外部传参。

这说明仓库内部已经承认：

- 公开入口不应无条件相信调用方给的路径
- 脚本自身位置是更可靠的证据源

问题在于这套稳健行为没有覆盖到 Python canonical-entry 的入口边界。

### 2.3 Installed runtime 场景已经有“不要依赖用户项目目录”的回归目标

现有回归测试已经要求 installed shell scripts 在没有 repo-level adapter registry 时也能工作。

这说明当前产品方向本来就是：

- 用户项目目录不是 runtime 根
- 入口应当优先从已安装 runtime 或脚本自身位置恢复正确上下文

### 2.4 Windows 的官方强路径本来就是 PowerShell-first

当前平台支持矩阵已明确：

- Windows：`install.ps1` / `check.ps1` / `one-shot-setup.ps1` 是最强参考路径
- Linux/macOS：shell lane 可用，但语义和权威性不同

因此 Windows 上 shell lane 的设计目标不应是“和 PowerShell 一样权威”，而应是：

- 能安全切回 PowerShell 就切回去
- 不能安全切回时给清楚的人话阻断

## 3. 约束

本轮设计必须同时满足下面约束：

### 3.1 设计范围与实施节奏

- 设计范围按 `C`：最终适用于所有公开入口
- 实施节奏按 `B` 优先：第一阶段只落到 `canonical-entry`、`one-shot-setup.*`、`check.*`

### 3.2 最小修改原则

- 不新造大层级架构
- 不重做 runtime 布局
- 不改 packaging / manifest 结构
- 尽量复用已有 repo root 解析与 installed runtime 判断逻辑

### 3.3 自动纠偏策略

- 自动纠偏可以激进，但只能做高置信度、无副作用纠偏
- 自动纠偏只允许改“路径角色解释”和“调用链选择”
- 不允许把自动纠偏升级成自动修机器

### 3.4 禁止的危险操作

下面这些都禁止自动执行：

- 自动覆盖宿主根里的现有配置文件
- 自动删除或移动任何已有文件或目录
- 自动重装或自动升级 runtime
- 自动改用户项目目录内容

## 4. 备选方案

### Option A: 各入口分别补丁

做法：

- 在 `canonical-entry`、`one-shot-setup.*`、`check.*` 分别补 repo root 猜测和报错翻译

优点：

- 修改最少
- 短期见效快

缺点：

- 逻辑容易再次分叉
- wrapper、upgrade、其他入口后续仍可能重复同样错误
- 难以形成一致的错误语义和纠偏规则

### Option B: 薄共享入口守卫

做法：

- 保持现有 runtime、packaging、宿主布局不变
- 新增一个很薄的共享判定 helper
- 让公开入口在进入深层逻辑前统一做：
  - 路径角色识别
  - 高置信度自动纠偏
  - 低置信度阻断
  - shell lane 安全切换
  - 人话错误收敛

优点：

- 修改面可控
- 能同时解决 `repo_root` 误传和 Windows shell lane 失败
- 后续其他公开入口可以渐进接入，不要求一次重构完

缺点：

- 需要先明确统一的路径角色与错误语义合同

### Option C: 全面改成自发现入口

做法：

- 公开入口尽量不再依赖外部传入 `repo_root`
- 一律从已安装 runtime、自身脚本位置和宿主根自动发现

优点：

- 从根上减少调用方传错路径的机会

缺点：

- 超出本轮“最小修改”边界
- 会波及 wrapper、upgrade、安装器和兼容路径
- 回归面太大

## 5. 推荐方案

使用 Option B。

本轮推荐方案不是引入新的大架构层，而是在现有入口边界上补一个**薄共享入口守卫**。

它的职责只有四件事：

1. 识别路径角色
2. 在高置信度时自动纠偏
3. 在低置信度时明确阻断
4. 把底层错误翻译成稳定的人话错误类别

### 5.1 路径角色模型

第一阶段统一承认四种路径角色：

| 角色 | 含义 |
| --- | --- |
| `repo_root` | 真实 Vibe-Skills runtime / checkout 根 |
| `artifact_root` | 用户希望产生产物或 session 输出的位置 |
| `target_root` | 宿主根目录，如 `~/.codex` / `~/.claude` |
| `working_dir` | 当前任务工作目录或用户项目目录 |

关键原则：

- `working_dir` 不应被自动等同为 `repo_root`
- `artifact_root` 可以等于用户项目目录
- `repo_root` 必须来自受信证据，而不是只来自外部字符串参数

### 5.2 证据优先级

入口守卫应按三层证据判定 `repo_root`。

#### Strong evidence

下面任一命中即可高置信度认定真实 `repo_root`：

- 当前执行脚本位于已安装 runtime 目录下，例如 `.../skills/vibe/...`
- 当前执行脚本位于 Vibe-Skills checkout 下，并且关键 runtime 标记齐全
- 候选目录同时具备关键标记，例如：
  - `SKILL.md`
  - `config/version-governance.json`
  - `config/adapter-registry.json`
  - `apps/vgo-cli/src/vgo_cli/main.py`

#### Medium evidence

下面情况说明“像 repo root”，但不足以自动修：

- 只有部分配置文件
- 有 governed config，但 runtime 标记不齐
- 看起来像半安装、半升级或测试残留目录

#### Weak evidence

下面情况更像用户工作目录，不应被当成 `repo_root`：

- 普通业务仓库
- 有源码和 `.git`，但无 Vibe runtime 标记
- 只有项目文件，没有 runtime 关键目录

### 5.3 自动纠偏规则

自动纠偏分为三档。

#### A. 直接纠偏并继续

满足下面条件时直接继续执行：

- 传入 `repo_root` 只表现出 weak evidence
- 入口守卫能从脚本自身位置或已安装 runtime 唯一恢复 strong-evidence repo root
- 本次修正只涉及路径解释，不涉及写文件或改配置

行为：

- 把强证据候选作为实际 `repo_root`
- 保留原始路径作为 `working_dir` 或 `artifact_root` 候选
- 输出信息级提示，说明发生了自动纠偏

#### B. 切换到更安全的 shell lane 后继续

适用于 Windows shell 入口：

- 当前在 Windows
- 用户从 `bash` / WSL / Git Bash 进入 `one-shot-setup.sh` 或 `check.sh`
- PowerShell lane 可用

行为：

- 自动切换到对应 `.ps1` 路径
- 输出信息级提示，说明当前已切换到 PowerShell-first 受支持路径

#### C. 阻断并解释

出现下面任一情况时必须阻断：

- 找到多个 strong/medium 候选，无法唯一确定
- 当前目录看起来像半安装、损坏安装或混合 runtime
- 想继续执行必须重装、升级、覆盖、移动文件
- shell lane 无法安全切换

行为：

- 停止执行
- 不透出原始 traceback 作为主消息
- 输出稳定的人话阻断信息和修复命令

## 6. 用户可见错误类别

第一阶段统一把入口错误收敛为四类：

### 6.1 `ROOT_ROLE_MISMATCH`

含义：

- 传入 `repo_root` 更像工作目录或用户项目目录

用户主消息：

- `当前传入的 repo_root 更像用户工作目录，不是真实的 Vibe runtime 根。`

后续行为：

- 能安全纠偏则继续
- 否则阻断

### 6.2 `RUNTIME_INCOMPLETE`

含义：

- 已安装 runtime 或候选 runtime 缺少关键标记

用户主消息：

- `检测到 Vibe runtime 安装不完整，缺少关键运行时文件。`

后续行为：

- 只给修复命令
- 不自动重装

### 6.3 `UNSUPPORTED_SHELL_LANE`

含义：

- 当前 shell 路径对当前平台不稳或不受支持

用户主消息：

- `检测到当前 shell 调用链不适合当前平台。`

后续行为：

- 能自动切 PowerShell 就继续
- 否则给替代命令并阻断

### 6.4 `AMBIGUOUS_RUNTIME_ROOT`

含义：

- 检测到多个候选 runtime 根，系统拒绝猜测

用户主消息：

- `检测到多个候选 Vibe runtime 根，系统已停止执行以避免误操作。`

## 7. 诊断与证据策略

本轮不新增复杂诊断系统，只做两级输出：

### 7.1 终端摘要

每次纠偏或阻断都打印简短结构化摘要：

- 原始 `repo_root`
- 实际采用的 `repo_root`
- 原始路径被判定成什么角色
- 是否发生自动纠偏
- 为什么这么判断
- 推荐下一步

### 7.2 受控诊断文件

只有在当前入口已经处于受管 Vibe 目录时，才允许把纠偏摘要写入既有受控输出位置。

约束：

- 只写 Vibe 自己的输出目录
- 不写入用户项目源码树
- 不覆盖宿主现有配置
- 不创建与修复无关的新目录结构

## 8. Windows shell lane 规则

第一阶段统一以下规则：

1. Windows 主机优先 PowerShell lane。
2. shell 入口只要能安全切到 `.ps1`，就优先切换。
3. 只做无歧义路径转换，不做模糊猜测。
4. `127` 必须被翻译成“缺少哪个命令 / 哪条路径不受支持”的人话错误。
5. 文档与真实策略保持一致：Windows 官方强路径仍然是 PowerShell-first。

## 9. 第一阶段范围

第一阶段只接入这些公开入口：

- `packages/runtime-core/src/vgo_runtime/canonical_entry.py`
- `scripts/bootstrap/one-shot-setup.ps1`
- `scripts/bootstrap/one-shot-setup.sh`
- `check.ps1`
- `check.sh`

### 9.1 允许修改的面

第一阶段允许修改这些文件或相邻薄 helper：

```text
packages/contracts/src/vgo_contracts/**
packages/runtime-core/src/vgo_runtime/canonical_entry.py
apps/vgo-cli/src/vgo_cli/repo.py
scripts/common/vibe-governance-helpers.ps1
scripts/bootstrap/one-shot-setup.ps1
scripts/bootstrap/one-shot-setup.sh
check.ps1
check.sh
tests/unit/**
tests/integration/**
tests/runtime_neutral/**
docs/**
```

### 9.2 明确不处理的面

第一阶段明确不处理：

- runtime 布局重构
- packaging / manifest 结构改写
- install ledger 语义重写
- 自动重装或自动升级
- 宿主配置自动迁移
- 用户项目目录内容修复
- 六阶段 governed runtime 状态机重写

## 10. 最小修改落地策略

本轮实现应优先遵守下面策略：

### 10.1 不新造大层

不要把本轮扩成新的入口编排框架。

更合适的做法是：

- 复用已有 `Resolve-VgoRepoRoot`
- 复用已有 installed runtime / governed root 判定逻辑
- 新增一个很薄的 Python-side path-role / repo-root guard helper
- 让公开入口只做薄接入

### 10.2 错误在边界处收敛

优先在进入深层 runtime / contract 解析之前完成：

- 路径纠偏
- shell lane 切换
- 人话错误翻译

不要把问题留到 adapter registry 深处再报错。

### 10.3 自动纠偏只做解释层修正

允许：

- 改本次执行实际采用的 `repo_root`
- 重新解释原始路径角色
- 在 Windows 上切换到更安全的公开入口

禁止：

- 重写磁盘布局
- 覆盖配置
- 删除、移动已有内容
- 触发自动安装动作

## 11. 测试策略

第一阶段测试应覆盖四类场景。

### 11.1 单元测试

覆盖：

- strong / medium / weak evidence 分类
- 工作目录误传为 `repo_root`
- 已安装 runtime 根识别
- 多候选根阻断
- Windows / WSL / POSIX 路径形态

### 11.2 集成测试

覆盖：

- `canonical-entry` 误传 `repo_root` 时自动纠偏
- 无法唯一纠偏时输出 `ROOT_ROLE_MISMATCH` 或 `AMBIGUOUS_RUNTIME_ROOT`
- registry 缺失不再以原始 traceback 作为主错误

### 11.3 平台测试

覆盖：

- Windows + PowerShell 正常路径
- Windows + bash 且可切 PowerShell
- Windows + bash 且无法切换时的人话阻断
- `127` 显示为明确命令缺失或 lane 不受支持

### 11.4 回归测试

覆盖：

- 已有 installed-runtime 成功路径不退化
- 已有 shell / PowerShell 基线测试继续通过
- 已有 canonical-entry 真值工件和 proof gate 不被破坏

## 12. 验收标准

第一阶段完成后，至少满足下面标准：

1. 把用户项目目录误传为 `repo_root` 时，不再把原始 traceback 直接暴露给用户。
2. 高置信度场景下，入口能自动纠偏并继续执行。
3. 低置信度场景下，入口会明确阻断并给出修复命令。
4. Windows 上从 shell 入口进入时，能优先切换到 PowerShell-first 权威路径。
5. 整个纠偏流程不执行任何危险操作。

## 13. 后续阶段

第二阶段再把同一套入口守卫渐进接入：

- host wrapper
- `install.*`
- `upgrade`
- 其他公开 CLI 子命令

第三阶段才考虑进一步弱化外部对显式 `repo_root` 的依赖，向更强的自发现模式演进。

在进入第二、第三阶段前，第一阶段必须先证明：

- 它确实压住了这次两类核心报错
- 它没有扩大回归面
- 它没有引入危险自动操作
