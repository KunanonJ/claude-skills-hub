# Docling Output Spec

本文件定义 VCO 在接入 `Docling MCP` 时依赖的 **document plane contract**。它不是对上游所有字段的完整镜像，而是 VCO 在解析、转换、审计、样例回放与降级流程中要求保留的最小稳定 subset。

## 1. 适用范围

- 仅用于 `config/tool-registry.json` 中 `docling-mcp` 的 `contract_reference`；
- 与 `references/document-plane-samples.md` 配套使用；
- 仅约束 VCO 读取的最小字段，不限制上游扩展更多字段；
- 若上游输出变更，只要本文件定义的 contract 仍可恢复，就视为兼容。

## 2. Template Posture（Wave12）

`docling-mcp` 在 Wave12 中被固定为 **document plane primary capability**，并同时承担两层语义：

| 层级 | 含义 | 默认运行暴露 |
|---|---|---|
| `approved-template` | contract、样例、degraded mode、artifact bundle 已固定，可被项目引用 | `not-enabled` |
| `project-enabled` | 某个项目/运行显式绑定文档输入并执行解析 | `scoped` |

两层共同约束：

- `advice-first`：先给 intake / parse 建议；
- `artifact-first`：结果优先写 artifact bundle；
- `read-only-first`：只处理用户显式提供的文档；
- `isolated-runtime`：大文件/OCR/资源密集场景必须隔离执行。

## 3. 输入契约

允许的输入来源：

- 用户显式提供的本地文件；
- 由上游 MCP 提供的受控二进制/文本附件；
- VCO 已批准的文档转换流水线中的中间产物。

允许的输入类型：

- `pdf`
- `docx`
- `pptx`
- `xlsx`
- `html`
- `image/*`（OCR 场景）
- 纯文本或 markdown
- 无扩展名但可通过本地 ZIP/容器检查正向识别的 Office Open XML 文档

约束：

- 默认只处理用户显式授权的文档；
- 大文件必须在隔离 runtime 中执行，避免进入默认会话上下文；
- 输入文件的原始二进制不得在日志中全文回显；
- 当来源只暴露为 `application/zip` 时，只有在本地容器检查能正向识别为 `docx` / `pptx` / `xlsx` 时才允许进入 contract；
- `source.mime_type` 应记录恢复后的有效 MIME，而不是保留模糊的 `application/zip`；
- 无扩展名 OOXML 的 MIME 恢复仅限本地 intake 正规化，不得被解释为远程 URL 探测或自动抓取能力；
- `project-enabled` 只允许绑定“本次运行或本项目显式提供”的文档来源，不得自动扩张为远程抓取器。

## 4. 最小输出结构

VCO 期望 Docling 结果可被归一化为如下逻辑结构：

```json
{
  "tool_id": "docling-mcp",
  "enablement_level": "approved-template|project-enabled",
  "document_plane_role": "primary",
  "document_id": "string",
  "source": {
    "path": "string|null",
    "mime_type": "string",
    "sha256": "string|null"
  },
  "content": {
    "markdown": "string|null",
    "plain_text": "string|null"
  },
  "pages": [
    {
      "page_number": 1,
      "text": "string|null",
      "blocks": []
    }
  ],
  "tables": [],
  "images": [],
  "artifact_bundle": {
    "manifest_path": "string|null",
    "markdown_path": "string|null",
    "json_path": "string|null",
    "text_path": "string|null"
  },
  "provenance": {
    "parser": "docling",
    "parser_version": "string|null",
    "warnings": []
  },
  "degraded_mode": "markdown_plus_pages|text_plus_provenance|page_ocr_only|failure_object",
  "failure_object": null
}
```

说明：

- `enablement_level`：明确当前是在模板验证还是项目执行；
- `document_plane_role`：固定为 `primary`；
- `artifact_bundle`：是 Wave12 的模板化新增要求，用于把多份输出绑定到一个可引用集合；
- `degraded_mode`：必须显式给出，而不是靠调用方猜测；
- `failure_object`：成功时可为 `null`，失败时必须是结构化对象。

## 5. Artifact Bundle Contract

`artifact_bundle` 最少要支持以下层次：

- `manifest_path`：记录 bundle 中各文件路径与摘要；
- `markdown_path`：主 Markdown artifact；
- `json_path`：结构化输出 / provenance / page map；
- `text_path`：必要时的纯文本降级产物。

兼容原则：

- 不要求固定文件名，但要求可通过 manifest 恢复 bundle；
- 大对象优先进入 bundle，再把精简摘要带回主会话；
- 若某一类产物不存在，manifest 中要么显式写 `null`，要么给出 warning。

## 6. Provenance / Confidence / Page Mapping

VCO 至少要求以下可追踪能力：

- **page mapping**：任一段落、块或表格若来自具体页，应能映射到 `page_number`；
- **parser provenance**：记录 `parser` 与 `parser_version`；
- **warning channel**：将 OCR 失败、版面异常、表格恢复失败等信息写入 `provenance.warnings[]`；
- **mime recovery trace（建议）**：若输入曾从泛化 ZIP MIME 恢复为具体 Office MIME，建议在 provenance 或 manifest 中保留该事实；
- **confidence（可选）**：若上游可提供 OCR 或结构恢复置信度，应保留到 block/table/image 级别；若没有，不强制。

## 7. 大文件与资源隔离

对大文件、复杂扫描件或富媒体文档：

- 必须在 `isolated_doc_runner` 或等价隔离 runtime 中执行；
- 优先输出结构化摘要与 markdown，而不是把整份文档直接灌入聊天上下文；
- 超过资源阈值时必须返回可解释的降级结果，而不是静默截断；
- 若必须中止执行，`failure_object` 中要记录原因、建议下一步与是否适合人工处理。

## 8. 失败与降级行为

当结构化解析失败时，VCO 接受以下降级顺序：

1. 正常结构化输出（`markdown_plus_pages`）
2. 仅 markdown/plain text + provenance（`text_plus_provenance`）
3. 仅 page-level OCR text + warnings（`page_ocr_only`）
4. 返回失败对象，并显式说明失败原因与建议下一步（`failure_object`）

禁止行为：

- 结构化字段缺失但不报告 warning；
- 返回空结果且不提供失败原因；
- 未经说明地把二进制内容直接写入日志或主上下文；
- 在 `approved-template` / `project-enabled` 之间切换时改变 `degraded_mode` 的含义。

## 9. Admission Filter Obligations

Docling 的 admission filter 与 Wave12 控制面配置必须保持一致：

- `admission_filter_profile = document_plane_primary`；
- `risk_tier = tier1_bounded_transform`；
- `egress_profile = none`；
- `secret profile = document_plane_primary`（即默认无外部 connector secret）；
- `write_surface_class = artifact_only`。

这意味着 Docling 可以写 artifact，但不能因此被误判成外部写面工具。

## 10. Document Plane 角色定义

在 Wave12 中，`docling-mcp` 被定义为 VCO 的 **document plane primary capability**。这意味着：

- 它负责“文档输入 -> 结构化中间表示/Markdown artifact bundle”的主路径；
- 它不是默认常驻 runtime，也不是默认联网抓取器；
- 它必须遵守 `advice-first`、`artifact-first`、`isolated-runtime` 三条约束；
- 它的 contract 以最小兼容字段为准，而不是追随上游所有可选字段。

## 11. Gate-facing 最小不变量

后续 `doc-tool-contract-gate.ps1` 以本节作为最小不变量来源。Docling 结果至少要能表达：

- `document_plane_role = primary`；
- `artifact_first = true`；
- `isolated_runtime_required = true`；
- `degraded_mode` 属于以下集合之一：
  - `markdown_plus_pages`
  - `text_plus_provenance`
  - `page_ocr_only`
  - `failure_object`
- `provenance.warnings[]` 可为空，但 warning channel 必须存在；
- `artifact_bundle` 与 `failure_object` 都能被 gate 和样例文件引用。

## 12. Samples Reference

Wave12 的样例集位于 `references/document-plane-samples.md`。样例文件负责证明：

- `approved-template` 与 `project-enabled` 两层输出长什么样；
- `markdown_plus_pages`、`page_ocr_only`、`failure_object` 如何被稳定表达；
- 文档解析失败时如何仍然保持 artifact-first 与人工降级路径。

## 13. 最小验收矩阵

建议至少持续用以下样本验证兼容性：

| 场景 | 期望主输出 | 最低可接受降级 |
|---|---|---|
| 原生文本 PDF | `markdown + pages + provenance + artifact_bundle` | `text_plus_provenance` |
| 扫描版 PDF | `markdown/text + warnings + artifact_bundle` | `page_ocr_only` |
| 含表格 Office 文档 | `markdown + tables + provenance + artifact_bundle` | `markdown + warnings` |
| 无扩展名 OOXML/ZIP 附件 | `source.mime_type + artifact_bundle + provenance + content/tables` | `text_plus_provenance` |
| 大文件/资源受限 | artifact-first + warning | `failure_object` |
| 损坏文件 | 失败对象 + 建议下一步 | `failure_object` |

Wave12 的目标不是“所有文档都完美恢复”，而是“所有成功都能落 bundle、所有失败都可解释、所有模板都可被 gate 复验”。
