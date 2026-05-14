---
name: instagram-reel-script-writer
description: Stage 2 of the Instagram Reel pipeline. Writes a 20–30 second short-form Reel script with a pattern interrupt in the first 2 seconds, emotional payoff, and soft CTA — optimised for watch time, replays, and shares. Use when scripting a single Reel from a validated topic. Replace [topic] before sending.
risk: low
source: community
date_added: '2026-05-14'
author: roman-knox
source_url: https://www.threads.com/@roman.knox/post/DYRjSy8CF85
tags:
  - instagram
  - reels
  - short-form-video
  - scriptwriting
  - retention
  - viral-hooks
tools:
  - claude-code
  - claude-api
related:
  - instagram-reel-pipeline
  - instagram-reel-niche-validator
  - instagram-reel-hook-engineer
  - viral-hook-creator
  - copywriting-psychologist
---

# Instagram Reel — Script Writer (Short Form)

Stage 2 of the [Instagram Reel Pipeline](../instagram-reel-pipeline/SKILL.md). Produces a retention-engineered Reel script that earns watch time, replays, and shares.

## When to use

- You've validated a content angle (via Stage 1 or your own research) and need the script.
- You want a tight 20–30s format optimised for the IG/Reels algorithm, not long-form.
- You need a pattern-interrupt opener and a soft CTA without selling hard.

## Prompt

Replace `[topic]` with a concrete topic (e.g., `why your 401k is silently bleeding fees`, `the one Notion template that replaced 6 of mine`).

```
Write a high-retention Instagram Reel script for [topic] using a strong pattern interrupt in the first 2 seconds. Create emotional tension, curiosity, or controversy immediately, then deliver a quick payoff. Keep the script under 20–30 seconds. Optimize for watch time, replay value, and engagement (comments & shares). Include a soft CTA at the end.
```

## Output

- A scene-by-scene script under 30 seconds total
- First 2 seconds: pattern interrupt / hook
- Mid: tension or curiosity loop, then payoff
- End: soft CTA (no aggressive selling)

## Tips

- Run the prompt 3–5 times for variation — small wording changes produce surprisingly different hooks.
- Pair the output with `instagram-reel-hook-engineer` to A/B-test 5 alternative opening hooks against the script's default.
- For visuals, hand the script to an image/video model (Sora, Veo, Higgsfield, Kling) along with consistent character/style references.

## Next stage

Run `instagram-reel-hook-engineer` (Stage 4) on the same `[topic]` to generate 5 hook variants for A/B testing.
