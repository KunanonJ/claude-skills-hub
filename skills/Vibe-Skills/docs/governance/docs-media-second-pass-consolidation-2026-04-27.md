# Docs-Media Second-Pass Consolidation

日期：2026-04-27

## 结论先看

第二轮治理继续收窄 `docs-media`，目标是把它从“文档 + 表格 + 截图 + 旧助手混合包”收成更清楚的办公文件处理包。

这轮做三件事：

- `screenshot` 移出 `docs-media`，单独进入新的 `screen-capture` pack。
- `excel-analysis` 的浅层内容并入 `spreadsheet` 的职责，删除该 skill 目录入口。
- `doc` 不再作为 `docs-media` 候选；它有渲染脚本和素材，目录保留，后续如要物理删除要先迁移资产。

## 数量变化

| 项目 | 第一轮后 | 第二轮后 |
|---|---:|---:|
| `docs-media.skill_candidates` | 11 | 8 |
| `docs-media.route_authority_candidates` | 9 | 8 |
| `docs-media.stage_assistant_candidates` | 2 | 0 |
| `screen-capture.skill_candidates` | 0 | 1 |
| 物理删除 skill 目录入口 | 0 | 1 |

## 第二轮后的 docs-media

| skill | 角色 | 负责的问题 |
|---|---|---|
| `docs-write` | 主路由 | 写说明文档、Markdown 文档、用户文档。 |
| `docs-review` | 主路由 | 审阅文档表达、结构、风格。 |
| `docx` | 主路由 | Word / DOCX 创建、编辑、修订、格式处理，也接管排版和 layout fidelity 关键词。 |
| `docx-comment-reply` | 主路由 | 回复 Word 批注、处理 comments.xml/comment thread。 |
| `pdf` | 主路由 | 读取、生成、检查 PDF，尤其是版式相关任务。 |
| `spreadsheet` | 主路由 | CSV/TSV/普通表格处理、Excel 数据分析、数据透视。 |
| `xlsx` | 主路由 | 保留公式、工作簿格式、复杂 Excel 模板。 |
| `xan` | 主路由 | 百万行 CSV、低内存、流式表格处理。 |

## 新增 screen-capture

| skill | 角色 | 负责的问题 |
|---|---|---|
| `screenshot` | 主路由 | 桌面截图、窗口截图、屏幕快照。 |

这样做的原因很直接：截图是系统/屏幕捕获问题，不是文档处理问题。单独拆出来后，用户说“截图”时不会再把 `docs-media` 拉进来。

## 删除和保留

| skill | 处理 | 原因 |
|---|---|---|
| `excel-analysis` | 删除目录入口 | 只有一个浅层 `SKILL.md`，内容被 `spreadsheet` 覆盖；数据透视和 Excel 分析关键词已经由 `spreadsheet` 承接。 |
| `doc` | 移出 pack，保留目录 | 有 `scripts/render_docx.py`、assets、agent 文件；不能直接删。`docx` 已经有视觉转换说明，并补充了排版相关关键词。 |

## 配套路由调整

| 调整 | 新归属 |
|---|---|
| `数据透视` / `pivot table` workbook 分析推荐 | `spreadsheet` |
| `layout fidelity` / `文档排版` | `docx` |
| `截图` / `桌面截图` / `screen capture` | `screen-capture` / `screenshot` |

## 回归探针

本轮新增或更新的保护用例：

| 文件 | 覆盖边界 |
|---|---|
| `scripts/verify/vibe-pack-regression-matrix.ps1` | DOCX 排版归 `docx`，截图归 `screen-capture`。 |
| `scripts/verify/vibe-skill-index-routing-audit.ps1` | 截图不再归 `docs-media`。 |
| `scripts/verify/vibe-data-scale-overlay-gate.ps1` | 数据透视类 workbook 分析推荐 `spreadsheet`，不再推荐 `excel-analysis`。 |

## 剩余风险

- `doc` 目录仍存在，但已退出 `docs-media` 默认路由面；后续要删，需要先把 `render_docx.py` 等资产正式迁移或声明废弃。
- `docs-media` 仍有 8 个主路由，因为文档、PDF、Word、表格天然是较宽的办公文件面；但截图和两个旧助手已经不再混入。
- 本轮没有改 `docx-comment-reply`，因为它处理 Word 批注回复，是清楚的独立问题，不应并入普通 `docx`。
