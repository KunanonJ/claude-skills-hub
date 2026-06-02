# Open-World 任务合同（VCO 吸收版）

## 目标

这里定义的 open-world task contract，用来把 Agent-S 的开放环境任务理解能力，收口成 VCO 的 **任务合同层**，而不是外部执行层。

**所有 open-world 合同都必须满足：**
- `owner: vco_control_plane`
- `shadow_only: true`
- `requires_human_confirm: true`
- `promote: false`

## 任务分类

| `task_class` | 描述 | VCO 吸收方式 |
|---|---|---|
| `browser_only` | 纯浏览器可完成 | 回落到 BrowserOps provider plane |
| `desktop_only` | 纯桌面 GUI 任务 | 只允许 DesktopOps shadow 合同 |
| `browser_plus_desktop` | 浏览器 + 桌面跨边界 | BrowserOps 主导浏览器部分，DesktopOps 只补合同层 |
| `multi_app_openworld` | 多应用、环境开放、状态不确定 | 强制 shadow_only + 人工确认 |

## 必填字段

- `contract_id`
- `objective`
- `task_class`
- `uncertainty_level`
- `environment_surfaces`
- `observation_points`
- `side_effect_risk`
- `aci_contract_ref`
- `dag_summary`
- `handoff_boundary`
- `requires_human_confirm`
- `shadow_only`
- `owner`
- `promote`
- `fallback_path`

## 字段映射别名

为便于跨平面 replay / replay suite / unified task contract 对齐，可在 operator 视图中使用以下别名：
- `task_id` -> `contract_id`
- `risk_tier` -> `side_effect_risk`
- `confirm_required` -> `requires_human_confirm`

## 拆解规则

### 1. 先分类
- 若任务可退化为 `browser_only`，优先交给 `BrowserOps`
- 若必须跨浏览器与桌面，则保留 `browser_plus_desktop`
- 若任务依赖未知窗口、系统弹窗、本地应用状态，则进入 `multi_app_openworld`

### 2. 再合同化
- 用 `aci_contract_ref` 绑定动作级合同
- 用 `dag_summary` 表达关键节点与依赖
- 用 `handoff_boundary` 明确 BrowserOps / DesktopOps / manual SOP 分界

### 3. 最后治理
- 不允许把 open-world 任务直接 promote 成默认执行路径
- 不允许在合同层偷偷重写 owner
- 不允许在没有人工确认的情况下跨入桌面副作用操作

## 示例

```yaml
contract_id: openworld-export-and-attach-v1
objective: 导出网页报表并附加到本地邮件草稿
task_class: browser_plus_desktop
uncertainty_level: high
environment_surfaces:
  - browser
  - desktop_mail_client
observation_points:
  - export_button_visible
  - download_completed
  - attachment_visible_in_draft
side_effect_risk: high
aci_contract_ref: desktopops-report-screenshot-v1
dag_summary:
  nodes:
    - export_report
    - verify_download
    - attach_file_to_draft
  edges:
    - export_report -> verify_download
    - verify_download -> attach_file_to_draft
handoff_boundary:
  browser_part: browserops
  desktop_part: desktopops_shadow_advisory_only
requires_human_confirm: true
shadow_only: true
owner: vco_control_plane
promote: false
fallback_path:
  - degrade_to_browserops_when_possible
  - otherwise_stop_and_switch_to_manual_sop
```

## 高风险边界

以下情况一律不得隐式推进：
- 真实发送、发布、上传、同步、付款
- 使用本地保存凭证或自动填充凭证
- 修改系统设置、应用设置、权限、网络状态
- 批量文件移动、覆盖、删除

## 结论

Open-world 合同的本质是：**把“外部环境不确定性”变成 VCO 可治理的合同与确认边界。**

它不是第二执行 owner，更不是 Agent-S takeover 的合法入口。
