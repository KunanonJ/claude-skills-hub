---
name: instagram-reel-hook-engineer
description: Stage 4 of the Instagram Reel pipeline. Analyses the first 3 seconds of the top 10 viral Reels in a niche, then generates 5 fresh hook variations using psychological triggers (surprise, ego, fear, desire). Use for A/B testing openers, refreshing tired hooks, or unblocking writer's block. Replace [niche] before sending.
risk: low
source: community
date_added: '2026-05-14'
author: roman-knox
source_url: https://www.threads.com/@roman.knox/post/DYRjSy8CF85
tags:
  - instagram
  - tiktok
  - reels
  - viral-hooks
  - psychology
  - scroll-stopping
  - ab-testing
tools:
  - claude-code
  - claude-api
related:
  - instagram-reel-pipeline
  - instagram-reel-niche-validator
  - instagram-reel-script-writer
  - viral-hook-creator
  - headline-psychologist
  - copywriting-psychologist
  - scarcity-urgency-psychologist
---

# Instagram Reel — Hook Engineer

Stage 4 of the [Instagram Reel Pipeline](../instagram-reel-pipeline/SKILL.md). Reverse-engineers what's already stopping the scroll in a niche, then produces 5 fresh, more provocative variations.

## When to use

- You have a script (Stage 2 output) and want 5 alternative openers to A/B test.
- Your hook formula is fatiguing — engagement is dropping despite same content quality.
- Entering a new niche and need a quick read on which psychological triggers dominate there.

## Prompt

Replace `[niche]` with the target vertical.

```
Analyze the top 10 viral Reels in [niche]. Identify the hook patterns, pacing, and emotional triggers they use in the first 3 seconds. Then create 5 new hook variations that are more provocative, curiosity-driven, and optimized for stopping scroll behavior. Focus on psychological triggers like surprise, ego, fear, or desire.
```

## Output

- Breakdown of recurring hook patterns in the niche (first 3 seconds)
- Pacing observations
- Emotional triggers dominant in the niche
- 5 new hook variations leveraging surprise / ego / fear / desire

## A/B testing protocol

1. Lock the rest of the script (Stage 2 output).
2. Cut 5 versions of the same Reel — only the first 3 seconds differ.
3. Post one variant every 24–48h.
4. Track 3-second view-through rate and shares.
5. Keep the winning hook formula and feed back into Stage 2 for future scripts.

## Caveats

Without an attached web tool (`exa-search`, `tavily-automation`, `apify-influencer-discovery`, `firecrawl-scraper`), Claude can't actually analyse real viral Reels — it will produce plausible-but-fabricated patterns. Pair this skill with one of those for real trend grounding.

## Composition

- Combine with `viral-hook-creator` for broader hook libraries across platforms.
- Combine with `headline-psychologist` if your Reel uses heavy on-screen text.
