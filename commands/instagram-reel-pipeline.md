# Instagram Reel Pipeline

Run Roman Knox's 4-stage Instagram Reels content pipeline interactively.

Source: https://www.threads.com/@roman.knox/post/DYRjSy8CF85

## Steps

1. **Ask for the niche** (e.g., `personal finance for Gen Z`, `luxury travel`, `productivity for ADHD`). Wait for the user's answer.

2. **Ask which stage(s) to run**:
   - `all` — full pipeline in order
   - `1` — niche validation only (skill: `instagram-reel-niche-validator`)
   - `2` — script architecture only (skill: `instagram-reel-script-writer`, needs a [topic])
   - `3` — automation blueprint only (skill: `instagram-reel-automation-blueprint`)
   - `4` — hook engineering only (skill: `instagram-reel-hook-engineer`)

3. **For each requested stage**, invoke the corresponding skill via the Skill tool with the user's niche substituted into the prompt.

4. **For `all`** run in this order: 1 → 2 → 4 → 3.
   - After Stage 1, pause and ask the user which of the 5 angles to pass into Stage 2 as `[topic]`.
   - After Stage 4, summarise which hook variant to A/B test first.

5. **Surface caveats up front:**
   - If no web tool is attached (Exa, Tavily, Apify, Firecrawl, `browse`, etc.), warn that Stages 1, 3, and 4 will produce inference-based output rather than real trend data. Offer to use `exa-search` or `tavily-automation` to ground the results.
   - Flag that the "1.5M views / $6,783 in 7 days" claim is the creator's marketing, not benchmark.

6. **Output format**: render each stage's result as a clearly delimited markdown section, with the stage number, title, and the input parameters used. End with a "next action" line.
