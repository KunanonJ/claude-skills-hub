---
name: litreview-citation-chain
description: "Trace the intellectual lineage of the 3 most-mentioned concepts in a research corpus — who first proposed each idea, who challenged it, who refined it, and where consensus stands today. Output as a family-tree-style evolution. Trigger when the user mentions citation chain, intellectual genealogy, lineage of ideas, วิวัฒนาการของแนวคิด, who proposed first, how an idea evolved. Phase 3 of the litreview-* series."
---

# Literature Review — Citation Chain

A concept's journey from "novel proposal" to "field consensus" is itself the story of the science. This skill picks the 3 most-mentioned concepts in your corpus and reconstructs that journey for each — proposer, challenger, refiner, current state.

## When to Use

- After `litreview-intake-protocol` (you know which concepts repeat across papers)
- The user is writing a "background and theory" section
- They're trying to understand how a current framework was built
- They want to know whose work is foundational vs derivative
- Tracing whether a concept has been challenged or assumed

**Don't use** for a corpus with no recurring concepts (a topical grab bag rather than a coherent sub-field), or when fewer than ~5 papers — too small for evolution to be visible.

## The Prompt (use exactly as written)

```
เลือก 3 แนวคิดที่ถูกกล่าวถึงมากที่สุดในงานวิจัยทั้งหมด
สำหรับแต่ละแนวคิด ให้ระบุ:
• ใครเป็นผู้เสนอแนวคิดนี้เป็นคนแรก
• ใครเป็นผู้โต้แย้งหรือท้าทายแนวคิดนี้
• ใครเป็นผู้ปรับปรุงหรือต่อยอดแนวคิด
• ปัจจุบันวงการวิชาการมีข้อสรุปร่วมกันอย่างไร
แสดงลำดับวิวัฒนาการของแนวคิดเสมือนแผนผังเครือญาติ
```

## Output Format

For each of the 3 concepts, a family-tree-style block:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONCEPT 1: [Name of the concept]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌱 PROPOSED   [Author, Year]
              "The original claim, in one sentence."

🪨 CHALLENGED [Author, Year]   →   on [the specific point]
              "What they argued against."

🔧 REFINED    [Author, Year]   →   added [the specific refinement]
              [Author, Year]   →   added [the specific refinement]
              "How the concept evolved."

🎯 CURRENT CONSENSUS
              "Where the field stands today, in 1–2 sentences."
              Open questions: [list 1–2 if relevant]
```

Repeat for Concepts 2 and 3.

## How to Pick the 3 Concepts

Count concept frequency — but weight by **independent papers**, not raw mentions. A concept cited 3 times in one paper counts once. A concept appearing in 7 of 12 papers is more central than one appearing 15 times within 2 papers.

Choose concepts that are:
- ✅ Named entities (frameworks, models, hypotheses) — easier to trace
- ✅ Have a clear originator in the corpus
- ❌ Skip vague themes like "memory" or "learning" — not concepts, just topics

## Filling Gaps the Corpus Doesn't Cover

If the corpus shows refinement and consensus but not the original proposer, **say so**. Don't invent a citation:

```
🌱 PROPOSED   [Not represented in uploaded papers — pre-dates the corpus.
              Earliest mention here: Smith 2019, citing "the foundational work."]
```

You can recommend a search ("the original is likely [Author, Year] based on how papers cite it") but flag the inference.

## Discipline

- **Use names and years from uploaded papers only** — no invented citations.
- **One concept = one tree.** Don't merge related concepts; if they're separate in the literature, keep them separate.
- **Consensus statement must reflect the corpus**, not the model's general knowledge. If the corpus disagrees, the consensus is "still debated."
- **Challenges must be substantive.** "Did not cite the original" doesn't count.

## After This Step

- Some concept has no clear consensus? → likely flagged as a gap → `litreview-gap-scanner`
- Concepts conflict on a specific finding? → `litreview-contradiction-finder`
- Ready to put it all together? → `litreview-knowledge-map`

## Anti-Patterns

- ❌ Treating broad topics ("attention," "consciousness") as concepts — pick named theories/models instead.
- ❌ Listing every author who cited a concept — only those who proposed/challenged/refined.
- ❌ "Current consensus: It's complicated" — too vague. Either there's consensus or there's debate; say which.
- ❌ Inventing an "originator" the corpus doesn't actually attribute.
- ❌ Skipping the visual tree structure — the lineage view is the value.

## References

- Source prompt: user-authored Thai literature-review workflow
- Companion: `litreview-intake-protocol` (run first), `litreview-contradiction-finder`, `litreview-gap-scanner`, `litreview-knowledge-map`
