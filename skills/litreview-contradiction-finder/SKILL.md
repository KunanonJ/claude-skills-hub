---
name: litreview-contradiction-finder
description: "Surface every conflict in a research corpus — every point where 2+ author groups reach opposite conclusions, with positions, papers, and the methodological reasons for the disagreement (different methods, datasets, samples, time periods). Trigger when the user mentions contradictions, conflicting findings, disagreements between studies, ข้อขัดแย้ง, conflict finder, or wants a table of competing claims. Phase 2 of the litreview-* series."
---

# Literature Review — Contradiction Finder

Where the science fights itself is where the interesting questions live. This skill enumerates every direct contradiction across the uploaded corpus, in a single table, with the methodological roots of each disagreement made explicit.

## When to Use

- After running `litreview-intake-protocol` (you have a paper inventory)
- The user is preparing a "competing perspectives" section of a review
- They're trying to understand why a sub-field hasn't converged
- They want to design a study that resolves a known debate

**Don't use** for papers that merely disagree on emphasis or terminology. This skill is for direct, substantive contradictions on findings or interpretation.

## The Prompt (use exactly as written)

```
จากงานวิจัยทั้งหมดที่อัปโหลดมา
ให้ค้นหาทุกประเด็นที่มีนักวิจัยตั้งแต่ 2 กลุ่มขึ้นไปเสนอข้อสรุปที่ขัดแย้งกันโดยตรง
สำหรับแต่ละประเด็น ให้แสดง:
• จุดยืนของแต่ละฝ่าย
• ชื่องานวิจัยที่เกี่ยวข้อง
• เหตุผลที่ทำให้ผลลัพธ์แตกต่างกัน
  เช่น วิธีวิจัย ชุดข้อมูล กลุ่มตัวอย่าง หรือช่วงเวลาในการศึกษา
จัดผลลัพธ์ในรูปแบบตาราง
```

## Output Format

A single table. One row per contradiction:

| # | Point of contention | Position A (papers) | Position B (papers) | Likely reason for divergence |
|---|---|---|---|---|
| 1 | Does X cause Y? | "Yes, robustly" — Smith 2019, Lee 2021 | "Only in subset Z" — Park 2020 | Smith/Lee used college-aged samples; Park used 65+; effect may be age-moderated |
| 2 | Optimal dose | "10 mg/kg" — Chen 2018 | "20 mg/kg" — Garcia 2022 | Different administration routes (IV vs oral) → different effective concentrations |

If there are 3+ positions on the same point, add Position C, D columns. If there's only one paper on each side, still include it.

## The Key Discipline: Name the Methodological Root

The "Likely reason for divergence" column is what separates this skill from a list-of-disagreements. For each contradiction, point at the actual cause:

| Common roots | What to check for |
|---|---|
| **Sample differences** | Age, demographics, disease subtype, geography |
| **Methodology** | Experimental vs observational, lab vs field, in vivo vs in vitro |
| **Measurement** | Different scales, instruments, time windows |
| **Time period** | Pre/post a paradigm shift, technology change, or policy event |
| **Statistical approach** | Different control sets, covariates, threshold for significance |
| **Definitions** | Same word, different operationalization (e.g., "memory" measured by recall vs recognition) |
| **Sample size / power** | One study underpowered to detect effect the other found |
| **Publication context** | Different journal communities reward different findings |

If the actual cause isn't determinable from the papers, write "Cause unclear from uploaded papers" — don't invent a reason.

## Discipline

- **Direct contradictions only** — not "different emphasis" or "different framing."
- **Cite specific papers**, not "some studies."
- **The reason column is required.** A contradiction without a candidate cause is a half-finished entry.
- **No editorial verdict** on which side is right unless the corpus itself converges later — that's a finding, not your opinion.

## After This Step

- Want to trace how one of these contradictions evolved over time? → `litreview-citation-chain`
- Want to design a study to resolve one? → `litreview-gap-scanner` (especially the "methodology" column)
- Need to fold this into a full synthesis? → `litreview-knowledge-map`

## Anti-Patterns

- ❌ Including contradictions on terminology when both sides actually mean the same thing.
- ❌ "Smith says yes, Lee says maybe" — that's not a contradiction, that's hedging.
- ❌ Speculating on motives (publication pressure, funding bias) — stick to methodology.
- ❌ Burying the table inside prose. The deliverable IS the table.
- ❌ Putting two contradictions in one row to "save space."

## References

- Source prompt: user-authored Thai literature-review workflow
- Companion: `litreview-intake-protocol` (run first), `litreview-citation-chain`, `litreview-gap-scanner`, `litreview-knowledge-map`
