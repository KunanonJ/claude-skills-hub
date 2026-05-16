---
name: litreview-so-what-test
description: "Compress everything known about a research field into a 5-minute briefing for an educated non-expert — three sentences: what's proven, what's unknown, what's the real-world impact. Plain language, no jargon, no hedging. Trigger when the user mentions so what test, explain to non-expert, 5-minute brief, อธิบายให้คนทั่วไป, plain-language summary, executive summary of research. Phase 6 of the litreview-* series."
---

# Literature Review — The "So What" Test

The final test of whether you actually understand a body of research: can you explain it to a smart person who isn't in the field, in three sentences, without falling back on jargon? This skill enforces that compression.

## When to Use

- After the rest of the `litreview-*` series — you now have everything synthesized
- The user needs to brief a manager, investor, or family member on the field
- They're writing an abstract, executive summary, or talk intro
- They want a stress-test of their own understanding ("can I really say this simply?")

**Don't use** before you've done deeper synthesis. This skill compresses; it doesn't summarize-from-scratch. Running it cold on a fresh corpus produces hedged platitudes.

## The Prompt (use exactly as written)

```
สมมติว่าฉันต้องอธิบายองค์ความรู้ทั้งหมดนี้ให้คนทั่วไปที่มีพื้นฐานดีแต่ไม่ใช่ผู้เชี่ยวชาญฟังภายใน 5 นาที
โปรดสรุปดังนี้:
1. หนึ่งประโยคที่อธิบายว่าสาขานี้พิสูจน์อะไรได้แล้ว
2. หนึ่งประโยคที่อธิบายว่าสิ่งใดที่วงการยังไม่รู้แน่ชัด
3. หนึ่งประโยคที่อธิบายผลกระทบต่อโลกจริงที่สำคัญที่สุด
ใช้ภาษาที่เข้าใจง่าย
ไม่ใช้ศัพท์เทคนิค
ไม่ใช้ถ้อยคำกำกวม
```

## Output Format

Exactly three sentences. Numbered. No preamble, no postscript.

```
1. [What the field has proven — one sentence, declarative]
2. [What the field doesn't yet know — one sentence, declarative]
3. [Why this matters in the real world — one sentence, concrete]
```

That's it. The discipline IS the format.

## The Three Sentences — How to Write Each

### 1. "What the field has proven"

- Start with the verb (active voice). "Sleep consolidates memories." NOT "It has been shown by researchers that…"
- State the **strongest, most-replicated claim**, not the most exciting one.
- If the field's most-proven thing is also boring, say it anyway — that's the truth.
- No qualifiers like "may," "could," "is associated with." Use "does," "is," "causes" (when justified).

❌ "Multiple studies suggest that exposure to nature may have potential benefits for stress reduction in some populations."
✅ "Spending time in green spaces lowers stress."

### 2. "What the field doesn't yet know"

- Pick the **most-acknowledged unknown** — the thing everyone in the field agrees is open.
- Phrase as a missing piece, not a vague gap. "Why X works" beats "More research needed on X."
- Don't list 5 unknowns. Pick one.

❌ "There are many remaining questions about mechanisms, populations, and long-term effects."
✅ "Why nature reduces stress — neurobiologically — is still unsettled."

### 3. "Why it matters"

- A **concrete consequence**, not an aspiration.
- Connect to a decision someone could make, a policy that could change, a thing that could be built.
- If the impact is "advances scientific knowledge," the skill failed — that's not real-world impact.

❌ "Understanding these effects will inform future health policies."
✅ "Urban planners have started designing 'nature breaks' into hospitals and schools."

## The Banned Words List

The prompt says "no jargon, no ambiguity." Specifically banned:

- "Significantly" (statistical jargon)
- "Robust" / "robustly"
- "Modulates," "mediates," "moderates"
- "Implicated in"
- "Hypothesized to"
- "Has been shown to"
- "Suggests that"
- "Empirical evidence indicates"
- "Effect size"
- "P < .05" or any p-values
- Acronyms not unpacked the first time used
- Anything you'd find on a methods page that wouldn't make sense at dinner

When in doubt, ask: "Would a smart 15-year-old understand this sentence?" If no, rewrite.

## Discipline

- **Three sentences total. No more.** If you can't compress to three, you haven't synthesized — go back to `litreview-knowledge-map`.
- **No "however," "but," "while it depends on context."** Each sentence stands.
- **No hedging in sentence 1.** Save uncertainty for sentence 2.
- **No false certainty.** If the field is genuinely contested, the proven sentence should be narrow ("Sleep helps memory" not "Sleep is essential for all cognitive function").
- **Anchor sentence 3 in something concrete** — a product, a policy, a behavior change, a number.

## After This Step

This is usually the last move in the workflow. Pair with:
- The full `litreview-knowledge-map` for someone who wants more depth after the 5-minute pitch
- A single recommended paper from the starter list for someone who wants to dig in

## Anti-Patterns

- ❌ Four sentences. The format is three. Cut.
- ❌ Sentence 1 with "may," "could," "is associated with" — that's sentence 2 territory.
- ❌ Sentence 3 about "advancing the field" — not real-world impact, that's career impact.
- ❌ Jargon snuck in as a "term of art" — if the audience needs a glossary, you've failed.
- ❌ Hedge stack ("In general, in most cases, when controlling for…") — pick the headline.
- ❌ Skipping the format and writing a paragraph. The constraint is the value.

## Example (Hypothetical Field: Gut Microbiome and Mood)

```
1. The bacteria in your gut influence your mood — gut and brain talk to each other constantly.
2. Why specific bacteria affect specific moods, and in which directions, is still being worked out.
3. The first probiotic-based treatments for depression are in clinical trials, and your diet today may shape your mental health tomorrow more than psychiatry currently accounts for.
```

That's the bar. Concrete, declarative, no jargon, three sentences.

## References

- Source prompt: user-authored Thai literature-review workflow
- Companion: run `litreview-intake-protocol`, `litreview-contradiction-finder`, `litreview-citation-chain`, `litreview-gap-scanner`, `litreview-knowledge-map` first. This is the final compression.
