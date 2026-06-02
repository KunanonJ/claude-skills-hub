# Docling Document Plane Integration

## Scope

Wave35 把 `docling` 从 runtime-only 素材回收到 canonical repo，并把它固定为 **document plane primary contract source**。

这次收口只做三件事：

- 把 `references/docling-output-spec.md` 变成 canonical source of truth；
- 用 `config/docling-provider-policy.json` 固定 provider posture；
- 用 `scripts/verify/vibe-docling-contract-gate.ps1` 把 contract / degraded mode / policy 不变量变成可复验门禁。

## Positioning

`docling-mcp` 在 VCO 中是 provider 与 contract source，不是 second document orchestrator（第二 document orchestrator）。

固定约束：

- `advice-first`
- `artifact-first`
- `read-only-first`
- `isolated-runtime`
- `explicit project enablement only`
- `allow_second_orchestrator = false`

## Template Posture

Docling 的模板姿态分成两层：

| Level | Meaning | Default Exposure |
|---|---|---|
| `approved-template` | contract / sample / degraded mode / artifact bundle 已固定，可被项目引用 | `not-enabled` |
| `project-enabled` | 某个项目显式绑定本次运行中的文档输入并执行解析 | `scoped` |

这两层都必须保持同一套 degraded mode 语义，不能在不同运行上下文中改变 `artifact_bundle`、`failure_object` 或 `warning channel` 的含义。

## Canonical Contract

最小 contract 以 `references/docling-output-spec.md` 为准，关键字段包括：

- `document_plane_role = primary`
- `artifact_bundle`
- `provenance`
- `degraded_mode`
- `failure_object`
- page-level mapping / warnings channel

固定 degraded modes：

- `markdown_plus_pages`
- `text_plus_provenance`
- `page_ocr_only`
- `failure_object`

输入面补充约束：

- 对无扩展名的 Office/OpenXML 文档，只允许通过本地 ZIP 容器内容检查来恢复有效 MIME；
- `application/zip` 只有在能被正向识别为 `docx` / `pptx` / `xlsx` 时才进入 document plane；
- 这种 MIME 恢复属于本地 intake 正规化，不构成远程抓取、URL 扩张或新的 enablement 语义。

## Admission Filter

Docling 的 admission filter 固定为：

- `profile = document_plane_primary`
- `risk_tier = tier1_bounded_transform`
- `egress_profile = none`
- `secret_profile = document_plane_primary`
- `write_surface_class = artifact_only`

因此它可以写 artifact bundle，但不能被当成外部写面工具，也不能被升格成远程抓取器。

## Operational Rules

- 大文件、扫描件、OCR 密集场景必须走隔离 runtime；
- 结果优先写 artifact bundle，再把摘要带回主会话；
- 失败时必须返回结构化 `failure_object`；
- warning channel 必须存在，即使 warnings 为空；
- 不允许绕过 `artifact-first` 把整份文档原文直接灌回主上下文。

## Gate Coverage

`vibe-docling-contract-gate.ps1` 负责验证：

- spec / policy / integration doc 是否同时存在；
- canonical spec 是否与 runtime backup 中的 recovered spec 同源；
- provider policy 是否保留 `artifact-first` / `isolated-runtime` / `allow_second_orchestrator = false`；
- degraded modes 与 admission filter 是否与 contract 一致。

## Follow-up

本轮只回收 canonical contract，不在此文件内改动 bundled/runtime 镜像。后续 packaging / install / release 流程需要把这三份资产同步到 mirror roots。
