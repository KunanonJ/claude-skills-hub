---
name: instagram-reel-pipeline
description: Roman Knox's 4-stage Instagram Reels content pipeline — niche validation, short-form script architecture, automation-system design, and hook variation engineering. Use when planning, scripting, or scaling AI-generated short-form video content for Instagram or TikTok. Each stage is a self-contained prompt with a [niche] or [topic] placeholder.
risk: low
source: community
date_added: '2026-05-14'
author: roman-knox
source_url: https://www.threads.com/@roman.knox/post/DYRjSy8CF85
tags:
  - social-media
  - instagram
  - tiktok
  - reels
  - content-creation
  - viral-hooks
  - ai-content
  - prompts
tools:
  - claude-code
  - claude-api
---

# Instagram Reel Pipeline — "Claude Takeover"

A 4-stage prompt chain for finding viral content angles, scripting Reels, designing the production workflow, and engineering scroll-stopping hooks. Built around AI-generated visuals.

**Source:** [@Roman.Knox on Threads](https://www.threads.com/@roman.knox/post/DYRjSy8CF85)
**Reported result (creator's claim, not verified):** 1.5M views, $6,783 in 7 days.

---

## When to use

- Launching a new faceless / AI-visual Instagram Reels account in a chosen niche.
- Need to validate which content angles are working *right now* before producing.
- Writing a short-form script (20–30s) optimised for retention and shares.
- Designing a repeatable multi-post-per-day publishing pipeline.
- Out of hook ideas — need 5 fresh variations on what's already going viral.

Run stages in order for a cold start, or call any single stage independently.

## Atomic skills (invoke any stage standalone)

Each stage is also installed as its own skill, so you can call it via the Skill tool without loading the full pipeline:

- Stage 1 → [`instagram-reel-niche-validator`](../instagram-reel-niche-validator/SKILL.md)
- Stage 2 → [`instagram-reel-script-writer`](../instagram-reel-script-writer/SKILL.md)
- Stage 3 → [`instagram-reel-automation-blueprint`](../instagram-reel-automation-blueprint/SKILL.md)
- Stage 4 → [`instagram-reel-hook-engineer`](../instagram-reel-hook-engineer/SKILL.md)

For the interactive walkthrough, run the slash command `/instagram-reel-pipeline`.

---

## Stage 1 — Content & Niche Validation

Substitute `[niche]` with the target vertical (e.g., `personal finance for Gen Z`).

```
Search Instagram Reels, TikTok, and Reddit for the top-performing posts in [niche] over the last 30 days. Identify recurring visual styles, hooks, and topics that consistently go viral. Cross-reference what appears across all platforms and give me the 5 highest-demand content angles optimized for AI-generated visuals.
```

**Output:** 5 ranked content angles backed by cross-platform trend analysis.

---

## Stage 2 — Script Architecture (Short Form)

Feed one winning angle from Stage 1 into `[topic]`.

```
Write a high-retention Instagram Reel script for [topic] using a strong pattern interrupt in the first 2 seconds. Create emotional tension, curiosity, or controversy immediately, then deliver a quick payoff. Keep the script under 20–30 seconds. Optimize for watch time, replay value, and engagement (comments & shares). Include a soft CTA at the end.
```

**Output:** A 20–30s Reel script with hook, payoff, and soft CTA.

---

## Stage 3 — Hook + Retention Engineering (Automation System Design)

Substitute `[niche]` once to get the operational playbook for scaling output.

```
Create a fully automated content system that finds trending topics daily in [niche], generates high-retention scripts, creates consistent AI images, converts them into short-form videos, and generates captions and hashtags. Structure everything as a repeatable workflow optimized for posting multiple times per day on Instagram.
```

**Output:** A repeatable pipeline blueprint — tools, steps, cadence — for multi-post-per-day publishing.

---

## Stage 4 — Full Automation Via AI (Hook Variation Engine)

Use after Stage 1 or Stage 2 to multiply hook variants for a single angle.

```
Analyze the top 10 viral Reels in [niche]. Identify the hook patterns, pacing, and emotional triggers they use in the first 3 seconds. Then create 5 new hook variations that are more provocative, curiosity-driven, and optimized for stopping scroll behavior. Focus on psychological triggers like surprise, ego, fear, or desire.
```

**Output:** 5 fresh hook variations grounded in the niche's existing viral patterns.

---

## Recommended workflow

```
Stage 1 (validate niche)
    ↓ pick top angle
Stage 2 (script the Reel)
    ↓
Stage 4 (multiply hooks → A/B test 5 openers)
    ↓
Stage 3 (run once → wire up the daily production pipeline)
```

For ongoing operation: run Stage 1 weekly to refresh angles, Stage 2 + Stage 4 per Reel, Stage 3 once during setup.

---

## Caveats and honest framing

- **No live web access by default.** Stages 1, 3, and 4 ask Claude to "search" or "analyze" real posts. Without an attached web tool (Exa, Tavily, Apify, browser MCP), Claude will produce inference-based output, not real-time scraped data. Pair this skill with a web search/scrape tool for accurate trend data.
- **"Fully automated content system" is a design doc, not running code.** Stage 3 returns a workflow blueprint; you still have to implement it (n8n, Make, Zapier, custom code, etc.).
- **The revenue claim is marketing.** "$6,783 in 7 days" is the creator's own report — treat it as anecdote, not benchmark.
- **Saturation risk.** These prompts are circulating widely on Threads/IG; expect rising competition in any niche where you apply them verbatim. Differentiate via niche selection and personal voice, not just prompts.
- **Platform policy.** Instagram has been tightening rules on AI-generated and faceless content. Check current ToS in your region before scaling output.

---

## Related skills in this library

- `viral-hook-creator` — broader hook generation across platforms.
- `headline-psychologist` — psychological triggers behind viral copy.
- `cro-optimization` — landing-page conversion if you're funneling Reel traffic.
- `instagram-automation` — Instagram Graph API publishing/scheduling.
- `tiktok-automation` — cross-post the same pipeline to TikTok.
