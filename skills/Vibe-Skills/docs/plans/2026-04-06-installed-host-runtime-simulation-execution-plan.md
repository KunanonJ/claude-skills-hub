# Installed Host Runtime Simulation Execution Plan

## Internal Grade

L

这轮工作以测试扩展和证据收集为主，适合串行落地并在每一步后运行验证。

## Workstreams

### 1. Installed Runtime Probe Harness

- 复用现有 shell install 流程在临时目录安装四个主机
- 从安装产物 `skills/vibe/scripts/runtime/invoke-vibe-runtime.ps1` 发起任务
- 必要时为非 codex 主机构造假的 specialist bridge 命令以获得稳定可重复结果

### 2. Scenario Matrix

- planning task
- debug task
- governed execution task
- memory continuity pair

### 3. Assertions

- route/runtime authority
- requirement_doc / execution_plan / runtime_summary / cleanup_receipt
- specialist recommendation or dispatch accounting
- execution manifest status
- memory activation report read/write continuity

### 4. Verification

```bash
pytest -q tests/runtime_neutral/test_installed_host_runtime_simulation.py
pytest -q tests/runtime_neutral/test_installed_runtime_scripts.py tests/runtime_neutral/test_openclaw_runtime_core.py tests/runtime_neutral/test_opencode_managed_preview.py tests/runtime_neutral/test_claude_preview_scaffold.py
```

### 5. Cleanup

- 删除 pytest 缓存
- 审计本仓库是否留下 zombie `node`
- 保持工作树仅包含预期改动

## Completion Rules

- 只有在新测试通过且不破坏既有 host/runtime 矩阵时，才允许宣称该轮高仿真测试完成。
