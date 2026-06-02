# Installed Host Runtime Simulation Requirement

## Goal

在已安装的主机场景下，对 `vibe` 运行时做高度仿真的多维任务调用测试，验证安装后的真实调用链而不是仅验证仓库内核桥接。

## Scope

In scope:

- 在临时目标根安装 `codex`、`claude-code`、`openclaw`、`opencode`
- 使用安装产物中的 `skills/vibe/scripts/runtime/invoke-vibe-runtime.ps1`
- 覆盖 planning、debug、governed execution、memory continuity 四类任务
- 验证 route/runtime authority、阶段产物、cleanup receipt、memory activation、host-specific closure 基础可用性

Out of scope:

- 真实外部应用 GUI 点击测试
- 依赖真实第三方桥接命令的联网执行
- 非受支持主机的额外兼容性证明

## Acceptance Criteria

1. 四个主机都能在临时目标根完成安装，并保留 `skills/vibe` 可调用运行时。
2. 已安装运行时能执行 planning、debug、governed execution 三类任务样本，并输出 requirement/plan/runtime summary/cleanup receipt。
3. 每类任务都能证明 `authority_flags.explicit_runtime_skill == "vibe"`。
4. debug 任务能证明 specialist recommendation 或 dispatch accounting 被记录，而不是丢失到安装拓扑之外。
5. memory continuity 至少能证明安装后运行时在两次执行间发生 backend read/write，并把 memory context 注入 requirement/plan。
6. 测试必须基于安装产物路径执行，而不是直接回落到仓库根脚本。

## Product Acceptance Checks

- `codex`：受治理入口存在，planning/debug/execution 样本可跑通。
- `claude-code`：preview-guidance 安装后仍可从 installed runtime 做受治理调用。
- `openclaw`：runtime-core 安装后可跑受治理调用且不发生 self-deleting source。
- `opencode`：preview-guidance 安装后命令/agent scaffold 不阻断 installed runtime 调用。

## Manual Spot Checks

- 无额外 GUI spot check；本轮以高仿真自动探针为主。

## Delivery Truth Contract

- 只有在新增探针通过并保留现有矩阵绿色时，才允许宣称“已安装主机场景的高仿真调用测试完成”。
