---
name: instagram-reel-niche-validator
description: Stage 1 of the Instagram Reel pipeline. Cross-references Instagram Reels, TikTok, and Reddit to surface the 5 highest-demand content angles in a given niche, optimised for AI-generated visuals. Use when starting a new faceless/AI-visual account or refreshing a content calendar. Replace [niche] before sending.
risk: low
source: community
date_added: '2026-05-14'
author: roman-knox
source_url: https://www.threads.com/@roman.knox/post/DYRjSy8CF85
tags:
  - instagram
  - tiktok
  - reddit
  - niche-research
  - content-strategy
  - viral-content
tools:
  - claude-code
  - claude-api
related:
  - instagram-reel-pipeline
  - instagram-reel-script-writer
  - instagram-reel-hook-engineer
  - instagram-reel-automation-blueprint
---

# Instagram Reel — Niche Validator

Stage 1 of the [Instagram Reel Pipeline](../instagram-reel-pipeline/SKILL.md). Surfaces the highest-demand content angles in a niche by triangulating across three platforms.

## When to use

- Spinning up a new AI-visual Instagram account and need to pick winning angles before producing.
- Existing account is plateauing and you want fresh angles validated by current cross-platform demand.
- Auditing a competitor's niche before entering it.

## Prompt

Replace `[niche]` with the target vertical (e.g., `personal finance for Gen Z`, `luxury travel`, `productivity for ADHD`).

```
Search Instagram Reels, TikTok, and Reddit for the top-performing posts in [niche] over the last 30 days. Identify recurring visual styles, hooks, and topics that consistently go viral. Cross-reference what appears across all platforms and give me the 5 highest-demand content angles optimized for AI-generated visuals.
```

## Output

5 ranked content angles, each with:
- Cross-platform trend evidence
- Recurring visual style notes
- Hook patterns observed
- Suitability for AI-generated visuals

## Caveats

Claude cannot actually browse Instagram, TikTok, or Reddit without an attached web tool. Pair this skill with one of: `exa-search`, `tavily-automation`, `apify-trend-analysis`, `firecrawl-scraper`, `reddit-automation`, or the `browse` skill. Without web access, output is inference-based, not real-time data.

## Next stage

Feed the chosen angle into `instagram-reel-script-writer` (Stage 2) or `instagram-reel-hook-engineer` (Stage 4 — for hook A/B testing).
