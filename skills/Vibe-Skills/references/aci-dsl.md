# ACI / DAG 合同 DSL（DesktopOps Shadow）

## 目标

这里定义的 ACI DSL 不是新的执行脚本语言，也不是第二桌面代理协议。

它的用途只有一个：**把 Agent-S 风格的 open-world / GUI 任务翻译成 VCO 可吸收、可审查、可验证的 shadow contract。**

## ACI 的最小合同字段

| 字段 | 含义 | VCO 约束 |
|---|---|---|
| `contract_id` | 合同 ID | 可追踪、可引用 |
| `objective` | 任务目标 | 必须面向用户结果 |
| `owner` | 执行 owner | 必须保持 `vco_control_plane` |
| `execution_mode` | 执行模式 | 必须为 `shadow_only` |
| `environment_scope` | 环境范围 | `browser` / `desktop` / `multi_app` |
| `preconditions` | 前置条件 | 登录、窗口、文件、权限 |
| `nodes` | DAG 节点列表 | 每个节点都要有动作与观察点 |
| `depends_on` | 依赖关系 | 显式表达 DAG 边 |
| `checkpoints` | 观察点 | 必须可验证 |
| `invariants` | 不可违反约束 | 安全/治理/副作用约束 |
| `fallback` | 失败回退 | BrowserOps / manual SOP / stop |
| `handoff_boundary` | 交接边界 | 标出 BrowserOps 与 DesktopOps 分工 |
| `confirm_required` | 是否确认 | DesktopOps 默认 `true` |

## ACI 节点语义

每个 `node` 至少要表达：
- `node_id`
- `action`
- `checkpoint`
- `risk_level`
- `fallback`

若节点存在依赖，则必须显式写出 `depends_on`；
若节点跨浏览器与桌面边界，则必须加 `handoff_boundary`；
若节点会带来真实副作用，则必须标记 `manual_confirm = true`。

## Agent-S DAG -> VCO 合同映射

| Agent-S/open-world 语义 | VCO 吸收后的字段 |
|---|---|
| task node | `nodes[]` |
| dependency edge | `depends_on[]` |
| observation step | `checkpoint` |
| unsafe action | `risk_level=high` + `manual_confirm=true` |
| recovery path | `fallback` |
| browser/desktop crossing | `handoff_boundary` |

## 示例

```yaml
contract_id: desktopops-report-screenshot-v1
objective: 将网页仪表盘截图插入本地报告文档
owner: vco_control_plane
execution_mode: shadow_only
environment_scope: multi_app
preconditions:
  - dashboard 已可访问
  - 本地报告文档已打开
nodes:
  - node_id: browser_capture
    action: capture_dashboard_region
    checkpoint: screenshot_file_created
    risk_level: medium
    fallback: switch_to_manual_capture_sop
  - node_id: desktop_insert
    action: insert_screenshot_into_report
    depends_on:
      - browser_capture
    checkpoint: image_visible_in_report
    risk_level: high
    manual_confirm: true
    fallback: stop_and_request_user_action
checkpoints:
  - screenshot_file_created
  - image_visible_in_report
invariants:
  - 不改变未确认的系统设置
  - 不使用未授权凭证
fallback:
  - prefer_browserops_when_browser_only
  - otherwise_stop_and_require_manual_confirmation
handoff_boundary:
  browser_part: browserops
  desktop_part: desktopops_shadow_advisory_only
confirm_required: true
```

## 治理约束

以下写法在 VCO 中一律视为非法：
- `owner: agent_s`
- `execution_mode: live_takeover`
- `confirm_required: false`
- 省略 `depends_on` 却隐含 DAG 顺序
- 把 ACI 直接当成可自动执行的桌面脚本
