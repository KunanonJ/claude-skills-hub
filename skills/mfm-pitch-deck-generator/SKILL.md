---
name: mfm-pitch-deck-generator
description: "The My First Million Pitch Deck Generator — create an investor-ready .pptx using Shaan Puri's 15-slide framework from the MFM podcast. Trigger when a user mentions pitch deck, investor deck, fundraising deck, startup pitch, raising money, Series A/B/seed deck, preparing to pitch investors, or says 'help me with my deck.' Walks founders through each slide conversationally — coaching and pushing back — then generates a professionally designed .pptx with icons, brand colors, and card layouts."
---

# My First Million Pitch Deck Generator

Turn founders into fundraisers. Brought to you by the My First Million podcast — this skill walks a founder through Shaan Puri's 15-slide pitch deck framework one slide at a time, coaching their narrative at each step, then generates a professionally designed `.pptx` file with branded colors, icons, card layouts, and visual polish.

The philosophy: "A bad pitch deck is like having bad breath. It's not a total deal breaker, but man does it hurt your chances." Story first, design second — and this skill handles both.

## Before You Start

Read these reference files before starting any session:
- `references/framework.md` — complete 15-slide coaching structure with pro tips
- `references/mfm-design-spec.md` — visual design spec (read before Phase 3)
- `references/pptxgenjs.md` — pptxgenjs API reference (read before Phase 3)

Internalize the framework before talking to the founder. Read the design spec and API
reference before generating the deck. You'll reference it constantly during the walkthrough.

### Install Dependencies

The deck generation script requires pptxgenjs. Install before generating:

```bash
cd /tmp && npm install pptxgenjs 2>/dev/null || (npm init -y > /dev/null 2>&1 && npm install pptxgenjs)
```

## Phase 1: Identify the Founder's Starting Point

Open with energy. Something like: "Welcome to the My First Million Pitch Deck Generator! I'm going to walk you through the same 15-slide framework Shaan Puri used to raise $20M+ from VCs — straight from the MFM playbook. By the end, you'll have a professionally designed .pptx ready to send to investors."

Then ask a brief question to figure out where the founder is:

**Path A — Starting from scratch:** They have a company but no deck. Walk through every slide sequentially (the primary path, detailed below).

**Path B — Refining an existing deck:** They already have a deck. Ask them to share the content slide by slide, then evaluate it against the framework — identify missing slides, weak sections, narrative gaps, and slides out of order. Coach improvements on the weakest areas first.

**Path C — Pre-revenue / early stage:** They have an idea or very early product with limited traction. Adjust coaching: suggest moving the credibility slide to the end (if credentials are light), coach on framing leading indicators for traction (waitlist, LOIs, pilot results), and lean harder on vision, why now, and founder-market fit.

**Path D — Quick generation:** The founder already has all their content organized and just wants a deck built fast. Collect all inputs, validate them against the framework, flag any weak spots, and generate the .pptx.

## Phase 2: The Guided Walkthrough

Walk through the 15 slides in this exact narrative order. For each slide:

1. **Explain the purpose** — Tell the founder what this slide accomplishes in the story and why investors care.
2. **Ask a focused question** — Give them a clear prompt with an example to make it concrete.
3. **Evaluate their answer** — Check for clarity, specificity, and persuasiveness.
4. **Push back when needed** — Be direct. Founders don't have time for sugarcoating, and investors won't sugarcoat either. Show them what a stronger version looks like.
5. **Confirm and capture** — Once the content is strong, summarize what you've captured and move on.

Take slides one or two at a time. Let the founder respond, iterate, and feel good about each one before moving on. You're a coach, not a form.

### The 15 Slides

The framework reference (`references/framework.md`) has the full coaching details for each slide. Here's the sequence and what to focus on:

**Act 1 — Set the Stage**
1. **Title** — Company name + one-line subtitle. Must pass the "could my mom understand this?" test. Kill jargon.
2. **Credibility** — 3-5 accomplishments. This is the humblebrag slide. If credentials are light, move it to the end.

**⚠️ Credibility vs Traction — do not duplicate.** The credibility slide is for founder/team background: past roles, relevant exits, domain expertise, personal connection to the problem. Financial metrics (revenue, growth rate, customers) belong exclusively on the Traction slide (Slide 8). If the same numbers appear on both slides, investors notice and it makes the deck feel thin. Coach the founder: "Let's keep your financials for the Traction slide where they'll hit harder — what can we put here about your background and why you're the right person to build this?"

**Act 2 — The Problem**
3. **Problem** — Make the investor feel the pain. Needs data OR a vivid personal story. "People have trouble with X" is too vague.
4. **Current Solutions** — Show existing options are bad. The status quo needs to feel broken.
5. **The "What If"** — Paint the aspirational picture. NOT the product yet — the ideal experience. "What if instead, you could..."

**Act 3 — The Solution**
6. **Product** — The reveal. Product screenshot + 1-2 key value props. Not a feature list.
7. **Vision** — How this becomes a massive company. Use the "We are [big thing] for [big industry]" formula + market size.
8. **Traction** — The most important slide. Revenue > users > waitlist. This separates talkers from walkers.

**Act 4 — Why We Win**
9. **Differentiation** — "Others do X, we do Y." Strategic insight, not a feature comparison.
10. **Tailwinds** — The macro wave you're riding. The investor bets on the wave, not just the founder.
11. **Why Now** — Specific catalyst. A law changed, a technology emerged, a behavior shifted. "The market is growing" is not a why-now.

**⚠️ Why Now pushback — catch vague conclusions.** If the founder's why-now sounds like a landing line rather than a catalyst — phrases like "the demand was always there," "people are ready now," "timing is right," or "the world has changed" — push back immediately: "That's a conclusion, not a catalyst. What's the specific, dateable thing that happened that makes this possible or necessary now? A platform launched, a cost dropped below a threshold, a regulation changed, a behavior inflected — what's the one thing?" Do not move on until they give you a specific event with a year attached.
12. **Founder-Market Fit** — Why YOU were put on earth to build this. Narrative, not resume.

**Act 5 — The Close**
13. **Milestones** — What happens with the money. Specific outcomes, not a "use of funds" pie chart.
14. **Sweeten the Pot** — Save good news for dessert. An unannounced partnership, a strong closing summary.
15. **Call to Action** — Contact info and a clear ask.

### When to Push Back

Push back when you see:
- **Jargon soup** on the title slide. Rewrite it in plain English.
- **Generic problems.** Push for data or a personal story.
- **Too many features** on the product slide. Force them to pick 1-2.
- **Vision too small** for VC ("We'll be a $50M company") or too vague ("We'll change the world").
- **Missing traction.** Even pre-revenue founders should have something — waitlist, LOIs, engagement.
- **Vague "why now."** Demand a specific, dateable catalyst.
- **Forced founder-market fit.** The connection should feel like destiny, not a stretch.

### Pro Tricks

These are what separate this framework from generic templates:
- **Credibility placement is strategic.** Strong credentials → front. Light credentials → end.
- **"What if instead..." is a bridge, not a pitch.** Build desire before the reveal.
- **Milestones beat "use of funds."** Show exciting outcomes, not budget line items.
- **Save good news for dessert.** The "sweeten the pot" slide leaves the reader on a high note.
- **The investor bets on a wave.** Tailwinds and why-now make it feel inevitable, not just plausible.

## Phase 2.5: Narrative Arc — Write It Before You Build

After all 15 slides are coached and confirmed, but **before styling or building**, write the pitch narrative arc and show it to the founder. This is the story the deck is going to tell — locking it here prevents building slides that look polished but don't land as a pitch.

**Narrative structure (pitch context):**
1. **The hook** — What's the one thing an investor must walk away knowing? Usually the traction story or the insight that makes this inevitable.
2. **The problem** — What's broken, why current fixes fail.
3. **The solution** — The product reveal and vision.
4. **Why we win** — Differentiation, tailwinds, timing, team.
5. **The close** — The ask and the sweetener.

Write it as 5–8 sentences in the founder's voice. Show it before building.

**Example:**
> "MarginMax is the first profit operating system for e-commerce — and we have 27 paying brands and zero churn in 10 weeks to prove founders will pay for it. The problem is structural: Shopify shows revenue, ad platforms show ROAS, nobody shows profit per order. We do — in real time, with one-click fixes. The wave is real: cheap capital is gone, iOS killed ROAS, and the APIs finally exist to do this. We're raising $3M to get to $1M ARR and become the default profit tool for Shopify brands."

Get the founder's confirmation before moving to styling. If they say "that's not quite right," revise the arc — then build slides that match the revised story, not the original coaching notes.

---

## Phase 2.6: Styling & Branding

After the narrative arc is confirmed, ask the founder about their deck's visual identity. Ask these questions:

### Brand Colors
"Do you have brand colors? If so, give me the hex codes (e.g., #1B3A5C). If not, I'll pick a professional palette that fits your industry."

If they provide colors, map them to the theme:
- **Primary** — their main brand color (used for headers, footer bars, dark slide backgrounds)
- **Secondary** — their secondary color (used for icons, accent elements, card tops)
- **Accent** — a pop color (used for highlights, decorative lines, callout elements)

If they don't have brand colors, pick a palette from this list based on their industry:

| Industry | Primary | Secondary | Accent | Vibe |
|----------|---------|-----------|--------|------|
| **Fintech / Finance** | `1B2A4A` (navy) | `3B82F6` (blue) | `F59E0B` (amber) | Trust + energy |
| **Health / Biotech** | `065A82` (deep teal) | `00A896` (seafoam) | `02C39A` (mint) | Clean + innovative |
| **Construction / Trades** | `1B3A5C` (slate blue) | `E87722` (orange) | `F5A623` (gold) | Rugged + professional |
| **Consumer / E-commerce** | `6D2E46` (berry) | `A26769` (dusty rose) | `ECE2D0` (cream) | Warm + approachable |
| **Enterprise SaaS** | `1E2761` (midnight) | `CADCFC` (ice blue) | `FFFFFF` (white) | Premium + clean |
| **Climate / Energy** | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) | Growth + sustainability |
| **AI / Deep Tech** | `0F172A` (near-black) | `818CF8` (indigo) | `F472B6` (pink) | Cutting-edge + bold |
| **Education / Social** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) | Warm + trustworthy |

### Font Pairing
Default to Georgia (headers) + Calibri (body) — a classic professional pairing. If the founder has a brand font preference, use it if it's available in PowerPoint (Georgia, Arial, Calibri, Trebuchet MS, Palatino, Impact, Arial Black, Cambria, Consolas, Garamond).

### Theme Object
Compile the styling choices into a theme object for the JSON:

```json
"theme": {
    "primary": "1B3A5C",
    "secondary": "E87722",
    "accent": "F5A623",
    "bg_dark": "0D1B2A",
    "bg_light": "F7F5F2",
    "text_light": "FFFFFF",
    "text_dark": "1E293B",
    "text_muted": "64748B",
    "font_header": "Georgia",
    "font_body": "Calibri"
}
```

For `bg_dark`, derive it from the primary color by making it 2-3 shades darker. For `bg_light`, use a warm off-white (F7F5F2 or F8FAFC). For `text_muted`, use a mid-gray that works on both dark and light backgrounds.

## Phase 3: Generate the Deck

After walking through all 15 slides AND collecting styling preferences, generate the deck
using the pptxgenjs API. This phase has four steps: build the content JSON, write a
custom generation script, run it, and visually QA the output before delivering.

**Before starting Phase 3, read these two reference files:**
- `references/pptxgenjs.md` — pptxgenjs API reference (correct syntax, pitfalls to avoid)
- `references/mfm-design-spec.md` — MFM 15-slide design specification (layouts, colors,
  typography, dynamic height calculations, anti-patterns)

Do not rely on memory for API syntax. Read the reference files.

---

### Slide Headlines — Run This Check Before Writing Any JSON

Every slide headline must tell the story, not label the topic. Topic-label headlines are the most common reason a polished deck fails to land with investors.

| Bad (topic label) | Good (narrative-driven) |
|-------------------|------------------------|
| "The Problem" | "Record revenue. Somehow lost money." |
| "Our Product" | "Real-time profit per order — and a one-click fix." |
| "Traction" | "$32K MRR. 10 weeks. Zero churn." |
| "Why We Win" | "Others give you dashboards. We give you decisions." |
| "The Ask" | "$3M to get from early traction to category ownership." |

**Headline quality checklist — apply to every slide before writing the JSON:**
- Does this headline deliver the insight, not just label the slide?
- Would an investor understand the point before reading the body?
- Is it specific to this founder's story — not a generic template line?
- Does it use the founder's actual voice and numbers?

If any answer is no, rewrite it first. Then write the JSON.

---

### Step 1: Build the Content JSON

Compile all confirmed content into a JSON file at `/tmp/<company_name>_content.json`:

```json
{
    "company_name": "Company Name",
    "theme": {
        "primary": "HEX",
        "secondary": "HEX",
        "accent": "HEX",
        "bg_dark": "HEX",
        "bg_light": "HEX",
        "text_light": "FFFFFF",
        "text_dark": "HEX",
        "text_muted": "HEX",
        "font_header": "Georgia",
        "font_body": "Calibri"
    },
    "slides": {
        "title": {
            "headline": "[ACTUAL COMPANY NAME — renders as the large bold title. Not a placeholder.]",
            "subtitle": "One-line tagline"
        },
        "credibility": {
            "headline": "Headline for credibility slide",
            "accomplishments": ["Accomplishment 1", "Accomplishment 2", "Accomplishment 3"]
        },
        "problem": {
            "headline": "Problem headline with data",
            "body": "2-3 punchy lines explaining the pain"
        },
        "current_solutions": {
            "headline": "Why existing options fail",
            "body": "Option 1 — why it fails\nOption 2 — why it fails\nOption 3 — why it fails"
        },
        "what_if": {
            "headline": "What if instead...",
            "body": "1-2 sentences painting the dream — not describing the product"
        },
        "product": {
            "headline": "Product name — short value prop",
            "body": "Feature 1\nFeature 2\nFeature 3"
        },
        "vision": {
            "headline": "Vision headline",
            "vision_statement": "We are [big thing] for [big industry]",
            "market_detail": "Market size and supporting data"
        },
        "traction": {
            "headline": "So far, so good...",
            "body": "Metric 1\nMetric 2\nMetric 3\nMetric 4"
        },
        "differentiation": {
            "approach": "Headline: our core strategic difference",
            "comparison": "Others do X. We do Y.",
            "detail": "Why our approach wins — 2-3 sentences"
        },
        "tailwinds": {
            "body": "Macro trend 1\nMacro trend 2\nMacro trend 3"
        },
        "why_now": {
            "headline": "Why NOW?",
            "body": "The specific dateable catalyst — one paragraph"
        },
        "founder_market_fit": {
            "body": "Founder 1 — role, background, the moment\nFounder 2 — role, background\nClosing line"
        },
        "milestones": {
            "headline": "With $[amount], here's where we'll be in [timeframe]:",
            "body": "Milestone 1 — outcome + metric\nMilestone 2 — outcome + metric\nMilestone 3 — outcome + metric\nMilestone 4 — outcome + metric"
        },
        "sweeten_the_pot": {
            "headline": "One more thing...",
            "body": "One piece of good news in 2-3 sentences"
        },
        "call_to_action": {
            "cta_text": "We're raising $[X] to [goal]. Let's talk.",
            "contact": "email@company.com"
        }
    }
}
```

**Content rules before writing the JSON:**
- `title.headline` = actual company name. Never "Company Name".
- `credibility.accomplishments` = founder background and proof points. Financial metrics go on traction, not here.
- `tailwinds.body` = maximum 3 items. If founder gave 4+, pick the strongest 3.
- `what_if.body` = 1-2 sentences only. Paint the vision, do not describe the product.
- `sweeten_the_pot.body` = one piece of news, 2-3 sentences. If two announcements, pick the stronger one.
- Each milestone line = one specific outcome + one metric. Nothing longer.

---

### Step 2: Write the Generation Script

Write a fresh script at `/tmp/<company_name>_generate.js`. **Do not reuse or mirror a template — write content-aware code for this specific founder's content.**

The key architectural rule: **every layout decision must be driven by the actual content, not by a fixed template.** Text heights, font sizes, card counts, and y-positions must all be calculated from what the founder actually gave you. A vision slide with a short headline and three crisp horizon cards is a different layout than one with a long headline and paragraph market detail. Code them differently.

**Before writing a single slide, ask:**
- How many items does this slide's body have? (cards, metrics, bullets)
- How long is the headline — will it wrap? Scale the font down if needed.
- How much vertical space do the body elements need? Calculate it, don't guess.
- After placing all elements, is anything below y:5.3? If so, compress upward.

**Required boilerplate — always include these helpers:**

```javascript
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const content = JSON.parse(fs.readFileSync(process.argv[2], "utf-8"));
const outputPath = process.argv[3];
const { theme, slides } = content;

// ALWAYS use factory function — never reuse shadow objects (causes corruption)
const makeShadow = () => ({
  type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.12
});

// Dynamic height calculation — use for every text element
function estimateLines(text, fontSize, boxWidthInches) {
  const charsPerLine = Math.floor(boxWidthInches * (96 / fontSize) * 1.4);
  return text.split("\n").reduce((total, line) =>
    total + Math.max(1, Math.ceil(line.length / Math.max(1, charsPerLine))), 0);
}

function lineHeightIn(fontSize) {
  if (fontSize <= 9)  return 0.18;
  if (fontSize <= 14) return 0.26;
  if (fontSize <= 16) return 0.28;
  if (fontSize <= 18) return 0.32;
  if (fontSize <= 20) return 0.35;
  if (fontSize <= 28) return 0.45;
  if (fontSize <= 30) return 0.48;
  if (fontSize <= 36) return 0.56;
  if (fontSize <= 40) return 0.62;
  return 0.82;
}

function textHeight(text, fontSize, boxWidth) {
  return estimateLines(text, fontSize, boxWidth) * lineHeightIn(fontSize);
}

// Dynamic headline — scales font down for long headlines, returns bottom edge
function addHeadline(slide, text, maxFontSize, color, yStart) {
  const y = yStart || 0.75;
  // Scale font to prevent multi-line overflow eating card space
  const fontSize = text.length > 80 ? Math.min(maxFontSize, 20)
                 : text.length > 60 ? Math.min(maxFontSize, 24)
                 : text.length > 40 ? Math.min(maxFontSize, 28)
                 : maxFontSize;
  const h = Math.max(0.55, textHeight(text, fontSize, 8.6) + 0.12);
  slide.addText(text, {
    x: 0.7, y, w: 8.6, h,
    fontSize, fontFace: theme.font_header,
    color: color || theme.text_dark, bold: true, margin: 0
  });
  return y + h; // always chain from returned bottom edge
}

function addSectionLabel(slide, label) {
  slide.addText(label, {
    x: 0.7, y: 0.3, w: 5, h: 0.25,
    fontSize: 9, color: theme.text_muted,
    fontFace: theme.font_body, charSpacing: 3, bold: true, margin: 0
  });
}

function addFooter(slide, slideNum) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.45, w: 10, h: 0.175, fill: { color: theme.primary }
  });
  slide.addText(String(slideNum), {
    x: 9.3, y: 5.45, w: 0.5, h: 0.175,
    fontSize: 9, color: theme.text_muted,
    fontFace: theme.font_body, align: "center", valign: "middle", margin: 0
  });
}

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
```

**For each of the 15 slides, follow `references/mfm-design-spec.md` for the layout pattern. Key content-aware decisions to make per slide:**

| Slide | What to adapt based on content |
|-------|-------------------------------|
| Credibility (2) | Spacing between accomplishments = available height ÷ item count. Never fixed. |
| Problem (3) | Body card height = textHeight(body, 16, 8.2) + padding. Let it expand. |
| Current Solutions (4) | Card height = available space ÷ line count. 2 solutions vs 3 = different layout. |
| Vision (7) | If market_detail has Today/Tomorrow/Horizon pattern → 3 separate cards. Otherwise → single text block. Detect the structure, then code the layout for it. |
| Traction (8) | Card grid dimensions = f(metric count). 3 metrics = 1 row. 6 = 2 rows. Card height fills available space. |
| Differentiation (9) | Both card heights = textHeight of their content. No fixed heights. |
| Why Now (11) | Content card height = textHeight(body, 16, 8.0) + padding. Let it fill the slide. |
| Founder-Market Fit (12) | fontSize = 15 if body has 3+ founders (\n count ≥ 4). Body height = textHeight. |
| Milestones (13) | Card height = available space ÷ milestone count. 3 milestones vs 4 = different card height. |
| Sweeten the Pot (14) | If body has 2+ \n-separated items → render as stacked cards. Single paragraph → centered text block. |

**Critical rules (any violation will break the deck):**
- Never use `#` prefix on hex colors — file corruption
- Never reuse shadow objects — always `makeShadow()`
- Never hardcode a y position that assumes single-line headline — always chain from `addHeadline()` return value
- Never set a fixed card height floor — calculate from actual text content
- Nothing below y:5.3 — footer starts at 5.45

```javascript
// After building all 15 slides:
pres.writeFile({ fileName: outputPath })
  .then(() => console.log("✅ Deck saved: " + outputPath))
  .catch(err => { console.error(err); process.exit(1); });
```

---

### Step 3: Install Dependencies and Run

```bash
# Install if needed
cd /tmp && npm install pptxgenjs 2>/dev/null || (npm init -y > /dev/null 2>&1 && npm install pptxgenjs)

# Run the fresh script you just wrote
NODE_PATH=/tmp/node_modules node /tmp/<company_name>_generate.js /tmp/<company_name>_content.json /tmp/<company_name>_pitch_deck.pptx
```

---

### Step 4: Visual QA — Mandatory Per-Slide Inspection Loop

**You may not deliver the deck until every slide has been visually inspected and confirmed clean. Not "mostly clean." Every slide.**

#### Step 4a: Render

```bash
python3 <skill_path>/references/pptx_scripts/office/soffice.py --headless --convert-to pdf /tmp/<company_name>_pitch_deck.pptx
rm -f /tmp/slide-*.jpg
pdftoppm -jpeg -r 150 /tmp/<company_name>_pitch_deck.pdf /tmp/slide
ls -1 /tmp/slide-*.jpg
```

#### Step 4b: Inspect every slide — call view tool on each one individually

Do not skim. Call the `view` tool on every slide image path. For each slide, record ✓ (clean) or ✗ (issue found + what the issue is).

| Slide | What to specifically check |
|-------|---------------------------|
| 1 — Title | Company name shows (not "Company Name"). Subtitle visible. No overlap. |
| 2 — Credibility | All accomplishments visible. Last item not cut off. Checkmarks showing. |
| 3 — Problem | Headline not colliding with body card. Last line of body card not clipped. |
| 4 — Current Solutions | All 3 solution cards have text. Text not overflowing cards. |
| 5 — What If | Headline and body NOT overlapping. Icon not sitting on top of text. |
| 6 — Product | Body card text fully visible. Screenshot placeholder present. |
| 7 — Vision | If horizon structure: all 3 card bodies visible, not just headers. |
| 8 — Traction | Headline not overlapping card grid. All metric cards have content. |
| 9 — Differentiation | Both cards (comparison + dark detail) fully visible, no text clipped. |
| 10 — Tailwinds | 3 cards equal height. No card is sparse (empty space) or overflowing. |
| 11 — Why Now | Headline not colliding with content card. All body text in card visible. |
| 12 — Founder-Market Fit | All founders named. Last paragraph fully visible — not cut off. |
| 13 — Milestones | All milestone rows visible. Number labels showing (not white-on-white). |
| 14 — Sweeten the Pot | All items visible. If 2+ items: card layout, none clipped at bottom. |
| 15 — CTA | CTA text not overflowing. Contact info visible. |

#### Step 4c: Fix every ✗ — then re-run the full pass

For each issue:
1. Fix the generation script (adjust heights, y positions, font sizes, padding)
2. Regenerate the pptx — run the full Step 3 script again
3. Re-render — run the full Step 4a render commands again (not cached images)
4. Re-inspect **all 15 slides** — not just the ones you fixed. Fixes often shift other elements.
5. Repeat until every slide is ✓

**Common fixes:**

**⚠️ lineSpacingMultiple is the #1 source of clipping.** `textHeight()` calculates raw line height but does NOT account for `lineSpacingMultiple`. A body at `lineSpacingMultiple: 1.5` renders ~50% taller than `textHeight()` predicts. Any slide using 1.5x or 1.6x spacing on multi-paragraph content will clip unless you compensate. Fix: reduce `lineSpacingMultiple` to `1.2` on content-heavy slides (3, 12) and verify it fits. If still clipping, also reduce `fontSize` by 2pt.

- **Text clipped at bottom:** The box height is too small. Either increase padding (`+ 0.6–1.0"` for multi-paragraph), reduce `lineSpacingMultiple` from 1.5→1.2, or reduce `fontSize` by 2pt. Do all three if needed.
- **Headline overlapping body/icon:** Chain body `y` from `addHeadline()` return value. Never hardcode a `y` below the headline that assumes single-line rendering.
- **Icon sitting on top of headline text:** Push headline `y` down so it starts below `icon_y + icon_h + 0.15"`.
- **Cards unequal height (sparse/cramped):** Use `cardH = available / n` — equal division of space. Do not size cards to content height.
- **Founder body cut off (slide 12):** Long narratives need `lineSpacingMultiple: 1.1` and `fontSize: 12`. `textHeight()` at 1.6x spacing underestimates by ~60%.

#### Step 4d: Delivery gate

Look at the actual rendered image of every slide. If you can see any of the following, you are not done — fix it:
- Any text cut off at the bottom of a box or slide
- Any headline or body text overlapping another element
- Any card with content missing or partially hidden
- Any slide where the last line of text is not fully visible

Only proceed to Step 5 when you can state:

> "I have called the view tool on slides 1 through 15. Every slide is visually confirmed clean — nothing clipped, nothing overlapping, all content fully visible."

If you have not called `view` on every slide individually, you have not done this step.

---

### Step 5: Deliver

**STOP. Before copying the file, state this out loud:**

> "I have called the view tool on slides 1 through 15. Every slide is visually confirmed clean — nothing clipped, nothing overlapping, all content fully visible."

If you cannot state this truthfully, go back to Step 4. Do not copy the file first and check later. Do not deliver and mention issues as a footnote.

Once you can state the above:

```bash
cp /tmp/<company_name>_pitch_deck.pptx /mnt/user-data/outputs/<company_name>_pitch_deck.pptx
```

Tell the founder:

"Your pitch deck is ready — 15 slides, [palette] palette, Shaan Puri's full MFM framework.

Next steps:
1. **Add your product screenshots** — Slide 6 has a placeholder area. A real photo transforms this slide.
2. **Add your logo** — Title and CTA slides are the natural homes for it.
3. **Practice the arc** — Each slide ≈ 1 minute. Total pitch should land at 15 minutes.

[Founder name]'s story on Slide 12 is your secret weapon — don't rush it."


## Edge Cases

### Credibility Slide Placement
If the founder has light credentials, advise them to move the credibility slide to the end in PowerPoint. In the JSON, still populate it in position 2 — manual reordering takes 5 seconds in PowerPoint.

### Pre-Revenue Traction
Coach them to present leading indicators: waitlist signups, LOIs, pilot results, engagement metrics, or user feedback. Frame the traction headline as "Early signals" rather than "So far, so good..." to set the right expectations.

### Founder Wants to Skip Slides
Flag what they're leaving out and why it matters. The 15-slide structure is deliberate — every slide serves a purpose in the narrative arc. If they insist on skipping, populate the JSON with the best content you can and note it to them.

### Multiple Founders
The credibility slide should highlight all co-founders. The founder-market fit slide should weave together how the founding team's combined backgrounds make them uniquely qualified.

### Very Long Content
If a founder's answer is too long for a slide, coach them to tighten it. Slides are visual — body text should rarely exceed 3-4 lines. If they insist on long content, split it across multiple `\n`-separated bullet points so the layout engine can card-ify it.

## What NOT to Do

- Don't accept "we'll fill this in later" for critical slides (problem, product, traction, vision). Push for at least a draft answer.
- Don't give generic feedback. Every piece of coaching should be specific to their company and their answer.
- Don't overwhelm the founder with all 15 slides at once. Take it step by step.
- Don't skip the pushback. Being polite about a weak slide does the founder a disservice — investors won't be polite.
- Don't skip the styling step. A themed deck with brand colors looks 10x more professional than default colors.
- Don't put excessively long text on slides. Coach the founder to be concise — if it doesn't fit on the slide cleanly, it's too long.
