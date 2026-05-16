---
name: litreview-intake-protocol
description: "Literature review intake — when the user uploads multiple research papers, produce a corpus-level inventory before any deep questions: paper-by-paper one-liner (author, year, key finding), concept-based groupings, and conflict flags. Trigger when the user uploads 2+ research papers, says they're starting a literature review, mentions วิจัย/intake protocol/research synthesis/literature review, or asks for an overview of a body of work. Phase 1 of the litreview-* skill series."
---

# Literature Review — Intake Protocol

The first move after uploading a stack of research papers. Build a corpus-level map before answering any specific question. Without this pass, every later question fights the model's tendency to over-index on the most recent or most charismatic paper.

## When to Use

- The user just uploaded 3+ research papers in one turn
- They say "I'm going to ask questions about these papers" or similar setup
- They start a research synthesis / literature review / dissertation prep
- They're trying to make sense of a sub-field they're new to

**Don't use** when there's a single paper (use direct summarization instead) or when the user has a specific question that doesn't need the full corpus mapped first.

## How to Run It

Send the user the prompt below verbatim (this is their phrasing, in Thai) — or paraphrase if they're working in another language. Then execute against the uploaded corpus.

### The Prompt (use exactly as written)

```
ฉันกำลังจะอัปโหลดงานวิจัยจำนวน [X] ฉบับ ในหัวข้อ [หัวข้อวิจัย]
ก่อนที่ฉันจะถามคำถามใด ๆ ให้คุณทำสิ่งต่อไปนี้:
1. แสดงรายชื่องานวิจัยทุกฉบับ พร้อมชื่อผู้แต่ง ปีที่ตีพิมพ์ และข้อค้นพบหลักใน 1 ประโยค
2. จัดกลุ่มงานวิจัยตามแนวคิด สมมติฐาน หรือมุมมองที่คล้ายกัน
3. ระบุว่างานวิจัยฉบับใดมีข้อค้นพบหรือข้อสรุปที่ขัดแย้งกัน
อย่าเพิ่งสรุปรายละเอียดเชิงลึก
ให้สร้างภาพรวมขององค์ความรู้ทั้งหมดก่อน
```

## What to Output

Three sections, in order:

### 1. Paper Inventory
| # | Author(s) | Year | Title (short) | Key finding (1 sentence) |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

One row per paper. The finding must be ≤1 sentence — if it needs two, the synthesis isn't done yet.

### 2. Concept Groups
Cluster papers by hypothesis, framework, or perspective — not by topic. Show:
- **Group A — [the shared claim]**: Paper 1, Paper 3, Paper 7
- **Group B — [the shared claim]**: Paper 2, Paper 5
- **Group C — [the shared claim]**: Paper 4, Paper 6

A paper can appear in multiple groups if it spans frameworks. Name each group by the **claim**, not the topic — "Memory consolidates during slow-wave sleep" beats "Sleep and memory."

### 3. Conflict Flags
List every place where 2+ papers reach opposing conclusions. Brief — full analysis is the next skill (`litreview-contradiction-finder`).
- Paper 1 vs Paper 4: disagree on [the specific claim]
- Paper 2 vs Paper 5, Paper 7: split on [the specific claim]

## Discipline

- **Do not deep-dive any single paper.** This is corpus mapping, not summarization.
- **Do not draw conclusions** about which paper is "right." That's user judgment.
- **Use the user's terms**, not your synthetic vocabulary, for concept group names.
- **If the user uploaded papers that don't fit any group**, label them "Outliers" — don't force-fit.

## After This Step

The user now has the lay of the land. Recommend next moves:
- Conflicts looked interesting? → `litreview-contradiction-finder`
- Curious how the ideas evolved? → `litreview-citation-chain`
- Looking for what's missing? → `litreview-gap-scanner`
- Need to brief someone? → `litreview-so-what-test`
- Want a full synthesis? → `litreview-knowledge-map`

## Anti-Patterns

- ❌ Summarizing each paper in 200 words — defeats the "overview first" rule.
- ❌ Grouping by topic (e.g., "memory papers") instead of by claim (e.g., "claim that memory consolidates during REM").
- ❌ Stating a conflict without naming the specific point of disagreement.
- ❌ Skipping the inventory and jumping to synthesis.
- ❌ Including papers the user didn't upload (no inventing references).

## References

- Source prompt: user-authored Thai literature-review workflow
- Companion skills: `litreview-contradiction-finder`, `litreview-citation-chain`, `litreview-gap-scanner`, `litreview-knowledge-map`, `litreview-so-what-test`
