---
name: instagram-reel-automation-blueprint
description: Stage 3 of the Instagram Reel pipeline. Produces a blueprint for a fully automated content system that finds daily trending topics, generates retention scripts, creates AI images, converts to short-form video, and outputs captions/hashtags — structured for multi-post-per-day publishing. Use once during pipeline setup, not per Reel. Replace [niche] before sending.
risk: low
source: community
date_added: '2026-05-14'
author: roman-knox
source_url: https://www.threads.com/@roman.knox/post/DYRjSy8CF85
tags:
  - instagram
  - reels
  - automation
  - workflow
  - n8n
  - make
  - zapier
  - content-pipeline
tools:
  - claude-code
  - claude-api
related:
  - instagram-reel-pipeline
  - instagram-reel-niche-validator
  - instagram-reel-script-writer
  - instagram-reel-hook-engineer
  - n8n-workflow-patterns
  - make-automation
  - zapier-make-patterns
---

# Instagram Reel — Automation Blueprint

Stage 3 of the [Instagram Reel Pipeline](../instagram-reel-pipeline/SKILL.md). Designs the end-to-end production workflow for posting AI Reels multiple times per day.

## When to use

- One-time, at the start of operationalising the pipeline.
- Migrating from manual posting to an automated system.
- Documenting a workflow for a VA or contractor to run.

This is **not** a per-Reel skill — run it once, get the blueprint, then implement.

## Prompt

Replace `[niche]` with your vertical.

```
Create a fully automated content system that finds trending topics daily in [niche], generates high-retention scripts, creates consistent AI images, converts them into short-form videos, and generates captions and hashtags. Structure everything as a repeatable workflow optimized for posting multiple times per day on Instagram.
```

## Output

A blueprint covering:
- Daily trend discovery sources and tools
- Script generation step (prompt → LLM → script artifact)
- AI image generation step (consistent character/style references)
- Image-to-video conversion step (Sora, Veo, Higgsfield, Kling, Runway)
- Caption and hashtag generation step
- Posting schedule and cadence
- The orchestration layer (n8n / Make / Zapier / custom code)

## Implementation reality check

The output is a **design doc**, not running code. To actually run the pipeline you need to wire it up — typical stack:

- **Orchestrator:** n8n (self-hosted, cheap), Make, Zapier, or a custom Node/Python script
- **LLM:** Claude API or OpenAI for script + captions
- **Image gen:** Midjourney, Imagen, fal.ai, Recraft, Ideogram
- **Video gen:** Sora 2, Veo 3, Higgsfield, Kling, Runway Gen-3
- **Voice (optional):** ElevenLabs, LMNT
- **Posting:** Instagram Graph API, or third-party (Buffer, Later, Metricool)
- **Trend source:** Apify (TikTok/IG scrapers), Exa, Tavily, RSS

## Caveats

- Instagram's policy on AI-generated and faceless content keeps tightening. Check the current ToS for your region before scaling output beyond personal use.
- "Multiple times per day" can trigger spam detection on new accounts. Ramp gradually.
- Without an attached web tool, Claude's blueprint will reference plausible tools but can't pull live trend data — that's expected for blueprint output.

## Composition

- Run `instagram-reel-niche-validator` (Stage 1) inside the daily trend-discovery step of this blueprint.
- Run `instagram-reel-script-writer` (Stage 2) inside the script-generation step.
- Run `instagram-reel-hook-engineer` (Stage 4) when refreshing hook formulas weekly.
