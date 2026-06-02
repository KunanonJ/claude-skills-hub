# mem0 Write Admission Contract

## Purpose

这个合同定义 `mem0` 在 VCO Memory Runtime v3 中何时可以写、写什么、何时必须拒绝。

## Allowed payload classes

| `payload_type` | 示例 | Minimum requirement |
|---|---|---|
| `preference` | 用户偏好 | `stability_window` |
| `style_hint` | 长期输出风格偏好 | `user_confirmation` |
| `recurring_constraint` | 反复出现的稳定约束 | `user_confirmation` + `fallback_owner` |
| `output_preference` | 结构化输出格式偏好 | `evaluation_id` + audit |

## Rejection classes

| Rejection Class | Trigger | Required action |
|---|---|---|
| `route_assignment` | 任何 pack / skill / route 改写暗示 | hard reject |
| `canonical_project_decision` | 架构或项目真相写入 | hard reject |
| `primary_session_state` | 执行中的临时状态 | deny and keep `state_store` |
| `security_secret` | secret / token / credential | hard reject + redact |
| `build_truth` | build / test / failure truth | deny and keep canonical owners |

## Required admission fields

- `payload_type`
- `candidate_value`
- `origin_surface`
- `stability_window`
- `operator_mode`
- `user_confirmation`
- `evaluation_id`
- `policy_version`
- `fallback_owner`
- `decision`
- `rejection_reason`

## Decision rules

1. In `shadow`, the pipeline can classify and report, but cannot write.
2. In `soft`, operator opt-in is mandatory.
3. Missing `stability_window` or `user_confirmation` means deny write.
4. Mixed payloads that blur preference and project truth must be downgraded to advisory-only.
5. Any `security_secret` or `build_truth` signal is a hard reject.
6. JSON or other structured content inside code fences must be preserved verbatim as `candidate_value` for admission review; extraction failure is not a license to silently drop the payload.

## Audit envelope

Every admitted soft write must preserve:

- `evaluation_id`
- `timestamp`
- `policy_version`
- `fallback_owner`
- `rollback_hint`

## Rollback note

Rollback is always implemented by forcing `mem0` back to `shadow` or `off`.
Rollback never migrates canonical owners away from `state_store`, `Serena`, `ruflo`, or `Cognee`.
