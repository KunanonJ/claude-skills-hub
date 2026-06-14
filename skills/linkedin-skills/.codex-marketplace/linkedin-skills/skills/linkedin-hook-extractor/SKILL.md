---
name: linkedin-hook-extractor
description: Reverse-engineer the hook formula from a viral LinkedIn post URL. Returns which of the 10 canonical 2026 formulas it uses (anaphora, R.I.P., year-pivot, time-anchor, self-proving, odd-money, paid-vs-free, curiosity-gap, contrarian, comment-gate), why it worked, and a blank template. Use to learn from a competitor's post, not to write your own (use linkedin-post-writer).
---

# LinkedIn Hook Extractor

Paste a viral LinkedIn post URL. Get back: which hook formula it uses, the exact structure, why it worked, and a blank template mapped to your topic.

## When to use

- User finds a viral post they want to study
- User wants to replicate a specific creator's pattern
- Before `linkedin-post-writer` to seed a draft with a proven structure

## Input

A LinkedIn post URL (any type: activity, share, ugcPost).

## Output

- **Formula identified** (F1-F10 from `../../references/hook-formulas.md`) with confidence score
- **Structural breakdown:**
  - Hook lines (first 210 chars)
  - Body architecture (sections + what each does)
  - Close pattern
  - Reaction-triggering devices (numbers, named entities, vulnerabilities)
- **Why it worked** psychologically
- **Blank template** filled with slot markers matched to the original, ready for the user's voice
- **Cautions:** anything in the original post that would fail 2026 audit (em dashes, AI vocab, outdated tactics)

## Steps

1. **Parse URL.** `lib.url_parser.parse_linkedin_url` → `post_urn`.
2. **Fetch post body.** If `APIFY_TOKEN` is set, call `lib.ApifyClient.fetch_post(url)`. Otherwise ask the user to paste the text.
3. **Classify.** Match against the 10 formulas using features:
   - First 2 lines: anaphoric? question? confession? number-led?
   - Body: numbered list? dated receipts? ledger? teardown?
   - Close: mirror question? identity reframe? commitment?
4. **Score confidence.** If multiple formulas fit, return top 2 with fit scores.
5. **Extract structure.** Pull each logical section and label it by formula role.
6. **Generate blank template.** Replace specifics with `{slot}` markers that match the user's topic.
7. **Audit the source.** Flag any AI tells in the original so the user doesn't copy them.

## Example

See `references/examples.md` for worked examples.

## Formulas reference

See `../../references/hook-formulas.md` for the 10 canonical formulas with full skeletons.

## Files

- `SKILL.md` — this file
- `references/classification-rules.md` — feature extraction + scoring heuristics

## Related skills

- `linkedin-post-writer` — use the extracted template to draft your own
- `linkedin-humanizer --mode audit` — audit your draft before shipping
