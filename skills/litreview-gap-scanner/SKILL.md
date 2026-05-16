---
name: litreview-gap-scanner
description: "Identify 5 research questions the corpus does NOT fully answer — and for each: why the gap persists, which paper comes closest, what methodology would fill it. Trigger when the user mentions research gaps, unanswered questions, what's missing, ช่องว่างวิจัย, gap analysis, frontier of the field, or planning a new study. Phase 4 of the litreview-* series."
---

# Literature Review — Gap Scanner

The most valuable parts of a corpus are often what's missing from it. This skill enumerates 5 well-defined gaps in the body of work, names why each has persisted, points to the closest existing attempt, and proposes the methodology that would close it.

## When to Use

- After running `litreview-intake-protocol` and `litreview-contradiction-finder`
- The user is scoping a thesis topic, new study, or grant proposal
- They're trying to find an underexplored angle worth pursuing
- They want to know where the field's frontier actually sits

**Don't use** for narrowly-curated corpora where the user has only collected papers on one specific finding — gap analysis needs a representative slice of the field.

## The Prompt (use exactly as written)

```
จากงานวิจัยทั้งหมด
ให้ระบุคำถามวิจัย 5 ประเด็นที่ยังไม่มีใครตอบได้อย่างสมบูรณ์
สำหรับแต่ละประเด็น ให้ระบุ:
• เหตุใดช่องว่างนี้จึงยังคงอยู่
  (เช่น ศึกษายาก เฉพาะทางเกินไป หรือถูกมองข้าม)
• งานวิจัยใดที่เข้าใกล้คำตอบมากที่สุด
• ควรใช้ระเบียบวิธีวิจัยแบบใดเพื่อเติมเต็มช่องว่างนี้
```

## Output Format

For each of the 5 gaps:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GAP 1: [The research question, phrased as a question]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Why the gap persists:
  [Pick one or combine: methodologically hard / requires rare data /
   ethically tricky / too niche to fund / paradigmatically out of fashion /
   recently emerged / overlooked because of measurement limits]
  [1–3 sentences explaining specifically for THIS gap]

Closest existing attempt:
  [Author, Year] — [what they did, what they almost answered, where they stopped]

Methodology to fill it:
  [Concrete proposal: study design, sample requirements, instruments,
   data sources, analysis approach. 2–4 sentences. Should be implementable,
   not aspirational.]
```

Repeat for Gaps 2–5.

## What Makes a "Real" Gap

| ✅ Real gap | ❌ Fake gap |
|---|---|
| "Effect of X on Y in populations under 18" (corpus only has adults) | "More research is needed" (vague) |
| "Does X work in field conditions vs lab?" (corpus all-lab) | "Better understanding of X" (no question) |
| "Causal mechanism behind the X→Y association" (corpus is correlational) | "Extend Smith 2019 to bigger N" (incremental) |
| "Long-term outcomes beyond 6 months" (corpus has short follow-ups) | "Study X in different context" (no theoretical reason) |

The gap must be:
1. **Phrased as a specific answerable question**, not a topic
2. **Genuinely absent from the corpus**, not just under-emphasized
3. **Worth answering** — has theoretical or practical stakes
4. **Plausibly answerable** with available methods or near-future ones

## Discipline

- **Verify the gap is real.** Re-check that no uploaded paper has actually answered it. False negatives ("I didn't see it") are common.
- **The methodology must be concrete.** "Conduct a longitudinal RCT" isn't enough — specify duration, sample, primary outcome, key covariates.
- **The closest existing attempt is mandatory.** A "totally novel question with no precedent" is suspicious — usually means it's been ruled out as uninteresting.
- **Don't pad to 5.** If only 3 real gaps exist in the corpus, list 3 and say so.

## After This Step

- Want to bake these gaps into a research agenda? → `litreview-knowledge-map` (the "frontier questions" section)
- Going to brief a non-expert on what's known/unknown? → `litreview-so-what-test`
- Designing a study? Use the methodology suggestions as a starting brief.

## Anti-Patterns

- ❌ Gaps phrased as topics ("more on X") instead of questions.
- ❌ "More replication is needed" — true of everything, useless as a gap.
- ❌ Methodology that's a single buzzword ("use AI", "longitudinal study") — not a plan.
- ❌ Claiming a gap exists when the user can find a paper in their own uploads that addresses it.
- ❌ Inflating to 5 gaps when 3 are real and 2 are filler.

## References

- Source prompt: user-authored Thai literature-review workflow
- Companion: `litreview-intake-protocol`, `litreview-contradiction-finder`, `litreview-citation-chain`, `litreview-knowledge-map`, `litreview-so-what-test`
