---
name: litreview-knowledge-map
description: "Build a structured knowledge map of a research field — central thesis, 3–5 supporting findings, 2–3 active debates, 1–2 frontier questions, 3 starter papers with reasons. Output as a clean outline, not prose. Trigger when the user mentions knowledge map, literature structure, field synthesis, แผนที่องค์ความรู้, structured outline of literature, or 'what does this field look like?'. Phase 5 of the litreview-* series."
---

# Literature Review — Knowledge Map Builder

After paper inventory, contradictions, lineage, and gaps — synthesize everything into one structured outline that a reader can absorb in under a minute. This is the deliverable that turns a corpus into a navigable map.

## When to Use

- After running prior `litreview-*` skills (the inputs are already in your head)
- The user is writing the structure section of a review article
- They're onboarding a teammate to the sub-field
- They want a single document to revisit later as a recap

**Don't use** as the *first* step on a fresh corpus — it conceals reasoning. Run intake → contradictions → citation chain → gaps first, then synthesize.

## The Prompt (use exactly as written)

```
สร้างแผนที่องค์ความรู้ของวรรณกรรมทั้งหมดในรูปแบบโครงสร้าง
ประกอบด้วย:
• ข้อเสนอหลักที่เป็นศูนย์กลางของสาขานี้
• ประเด็นสนับสนุนหลัก 3–5 ประเด็น
• ประเด็นที่ยังมีข้อถกเถียง 2–3 ประเด็น
• คำถามแนวหน้าที่วงการยังตอบไม่ได้ 1–2 ประเด็น
• งานวิจัย 3 ฉบับที่ผู้เริ่มต้นควรอ่านก่อน พร้อมเหตุผล
แสดงผลในรูปแบบ Outline ที่ชัดเจน ไม่ต้องเขียนเป็นความเรียง
```

## Output Format — Outline Only

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KNOWLEDGE MAP: [Field / topic]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. CENTRAL THESIS
   • [One sentence stating the field's main organizing claim]

2. SUPPORTING FINDINGS (3–5)
   ├─ [Finding A] — supported by [Paper X, Paper Y]
   ├─ [Finding B] — supported by [Paper X, Paper Z]
   ├─ [Finding C] — supported by [Paper W]
   └─ ...

3. ACTIVE DEBATES (2–3)
   ├─ [Question being debated] — [side 1: Paper A] vs [side 2: Paper B]
   └─ [Question being debated] — [side 1: Paper C, Paper D] vs [side 2: Paper E]

4. FRONTIER QUESTIONS (1–2)
   ├─ [Open question that nobody has fully answered]
   └─ [Open question that nobody has fully answered]

5. STARTER READING (3 papers)
   ├─ [Paper 1] — read first because [reason]
   ├─ [Paper 2] — read second because [reason]
   └─ [Paper 3] — read third because [reason]
```

## Rules

- **Outline only.** No introductory paragraph, no concluding paragraph. The structure IS the deliverable.
- **Central thesis is ONE sentence.** If it needs two, the field isn't coherent enough for a thesis — say so.
- **Supporting findings are 3–5, not "as many as you can find."** Pick the ones with the most independent support across the corpus.
- **Debates must have a concrete question, not just "different schools."**
- **Frontier questions must point forward**, not backward. "We don't know X" is past; "Will doing Y reveal Z?" is forward.
- **Starter papers ranked by reading order**, not by importance. The reason for each should explain why it's first/second/third in the sequence (e.g., #1 builds intuition, #2 introduces the methods, #3 shows the current state).

## How to Pick the 3 Starter Papers

Not necessarily the most cited or most recent. Pick by **what they do for a new reader**:

| Slot | Best candidate |
|---|---|
| **#1** | The clearest exposition of the field's central problem. Often a review article or seminal proposal. |
| **#2** | A definitive empirical paper using the field's signature methodology. The reader learns "how this field works." |
| **#3** | The most recent paper that shows the current frontier. The reader sees where things stand today. |

If the corpus doesn't have a clean #1 or #3 candidate, say so — don't force-fit.

## Discipline

- **Every line must trace back to uploaded papers** — central thesis, supporting findings, debates, all sourced.
- **Frontier questions can be inferred** from gaps (use `litreview-gap-scanner` output) but should be phrased as forward-looking questions, not as gaps.
- **Outline format is non-negotiable.** Prose synthesis is `litreview-so-what-test`'s job. This skill's deliverable is a navigable structure.
- **Use the user's terms** for findings/debates, not the model's.

## After This Step

- Need a non-expert version of this map? → `litreview-so-what-test`
- Want to extend with the original Thai prompt's full output? → re-run with the prompt verbatim against your full corpus.

## Anti-Patterns

- ❌ Writing prose instead of an outline ("The field has converged on…").
- ❌ Listing 8 supporting findings to be thorough — 3–5, picked intentionally.
- ❌ Frontier questions phrased as gaps ("Need more research on X") — phrase as questions.
- ❌ Picking starter papers by citation count without considering reading flow.
- ❌ Inventing a "central thesis" when the field genuinely has multiple non-overlapping schools.
- ❌ Including findings, debates, or papers not actually in the uploaded corpus.

## References

- Source prompt: user-authored Thai literature-review workflow
- Companion: run `litreview-intake-protocol`, `litreview-contradiction-finder`, `litreview-citation-chain`, `litreview-gap-scanner` first. Pair with `litreview-so-what-test` for non-expert audiences.
