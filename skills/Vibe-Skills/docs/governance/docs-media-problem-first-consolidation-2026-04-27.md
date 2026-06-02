# Docs-Media Problem-First Consolidation

日期：2026-04-27

## 结论先看

本轮治理的是 `docs-media` pack。

核心原则很简单：

> 只有能独立处理一个清楚的文档、表格、PDF 或截图问题，才继续留在 `docs-media` 主路由里。

更新说明：本文件记录第一轮治理。第二轮继续把截图拆到 `screen-capture`，并把 `excel-analysis` 收并到 `spreadsheet`，见 `docs/governance/docs-media-second-pass-consolidation-2026-04-27.md`。

没有删除任何 skill 目录。带脚本、references、assets 的 skill 仍保留在仓库中，后续如要物理删除，需要单独迁移资产。

## 数量变化

| 项目 | 调整前 | 调整后 |
|---|---:|---:|
| `docs-media.skill_candidates` | 17 | 11 |
| `docs-media.route_authority_candidates` | 0 | 9 |
| `docs-media.stage_assistant_candidates` | 0 | 2 |
| `media-video.skill_candidates` | 1 | 3 |
| `media-video.route_authority_candidates` | 0 | 3 |

## 调整后的 docs-media

| skill | 角色 | 负责的问题 |
|---|---|---|
| `docs-write` | 主路由 | 写说明文档、Markdown 文档、用户文档。 |
| `docs-review` | 主路由 | 审阅文档表达、结构、风格。 |
| `docx` | 主路由 | Word / DOCX 创建、编辑、修订、格式处理。 |
| `docx-comment-reply` | 主路由 | 回复 Word 批注、处理 comments.xml/comment thread。 |
| `pdf` | 主路由 | 读取、生成、检查 PDF，尤其是版式相关任务。 |
| `spreadsheet` | 主路由 | CSV/TSV/普通表格处理，以及 Excel 数据分析、数据透视。 |
| `xlsx` | 主路由 | 保留公式、工作簿格式、复杂 Excel 模板。 |
| `xan` | 主路由 | 百万行 CSV、低内存、流式表格处理。 |
| `screenshot` | 主路由 | 截图、屏幕快照、桌面捕获。 |
| `doc` | 阶段助手 | DOCX 视觉检查、排版辅助，不单独抢主路由。 |
| `excel-analysis` | 阶段助手 | Excel 分析示例和数据透视辅助，由 `spreadsheet` 作为主入口。 |

## 移到 media-video

| skill | 新归属 | 原因 |
|---|---|---|
| `transcribe` | `media-video` 主路由 | 语音转文字、会议录音转写、说话人区分，本质是音频/媒体任务，不是文档 pack 的主职责。 |
| `speech` | `media-video` 主路由 | 文本转语音、配音、voiceover，本质是音频/媒体生成任务。 |

## 移出 docs-media 但保留目录

这些 skill 不是没价值，而是不应该继续在 `docs-media` 里抢主路由。

| skill | 处理 | 原因 |
|---|---|---|
| `content-research-writer` | 移出 `docs-media` | 文章/内容研究写作太宽，容易抢 Excel/PDF/文档处理的 fallback。 |
| `imagegen` | 移出 `docs-media` | 图片生成属于独立视觉资产生成能力，不是文档处理主路由。 |
| `jupyter-notebook` | 移出 `docs-media` | Notebook 是实验/教程执行载体，不应被文档媒体 pack 默认接管。 |
| `writing-docs` | 移出 `docs-media` | Remotion 专用文档写作规则过窄，不应作为通用文档 pack 候选。 |

## 本轮修掉的具体问题

| 问题 | 调整前 | 调整后 |
|---|---|---|
| Excel 数据透视/分析 | 可能 fallback 到 `content-research-writer` | 由 `spreadsheet` 接管 |
| Jupyter notebook 教程 | 被 `docs-media` 接管 | 不再由 `docs-media` 接管 |
| 会议录音转文字 | `docs-media` 接管 | `media-video` 的 `transcribe` 接管 |
| 文本转语音 | `docs-media` 接管 | `media-video` 的 `speech` 接管 |
| `docs-media` 无角色分层 | 所有候选一视同仁 | 9 个主路由 + 2 个阶段助手 |

## 回归探针

本轮新增或更新的保护用例在：

```text
scripts/verify/vibe-pack-regression-matrix.ps1
```

覆盖的边界：

| prompt | 期望 |
|---|---|
| `process xlsx workbook and preserve formulas` | `docs-media` / `xlsx` |
| `请把会议录音转文字并区分说话人` | `media-video` / `transcribe` |
| `分析这个Excel表格并生成数据透视表` | `docs-media` / `spreadsheet` |
| `创建一个Jupyter notebook教程` | 不由 `docs-media` 接管 |

## 审计口径修正

全局 pack 审计器也做了一处修正：`negative_keywords` 不再计入 shared broad keyword 风险。

原因是负向关键词是用来防误触的，不应该反过来被算成 pack 内部重叠。

## 剩余风险

- `docs-media` 仍然是 P1，不是完全无风险；它仍然有 9 个主路由，因为文档、表格、PDF、截图本来就是一个较宽的办公文件面。
- `doc` 和 `docx` 仍有资产重叠，本轮只把 `doc` 降为阶段助手，没有迁移或删除脚本。
- `excel-analysis` 仍保留为阶段助手，后续可以比较其内容是否需要迁入 `spreadsheet` 后再删除目录。
- `jupyter-notebook` 被移出 `docs-media` 后没有新 pack 归属；当前更合理的状态是显式调用或后续单独设计 notebook/education/experiment pack。

第二轮已处理前三项中的两项半：截图已迁出 `docs-media`，`excel-analysis` 已删除目录入口，`doc` 已移出 pack 但因仍有脚本和素材未物理删除。
