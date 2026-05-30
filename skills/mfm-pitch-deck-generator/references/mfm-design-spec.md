# MFM Pitch Deck — Design Specification

This file defines the visual and structural design for the MFM Pitch Deck Generator.
Read this alongside `pptxgenjs.md` (API reference) when writing the generation script.

---

## Slide Layout

- **Dimensions**: LAYOUT_16x9 — 10" wide × 5.625" tall
- **Margins**: 0.7" left/right minimum. Never place content closer than 0.5" to any edge.
- **Footer bar**: Every slide gets a dark accent bar at the bottom — x:0, y:5.45, w:10, h:0.175

---

## The 15 Slides

| # | Key | Background | Style |
|---|-----|-----------|-------|
| 1 | title | bg_dark | Dark hero — large company name, subtitle |
| 2 | credibility | bg_light | Light — checkmark bullet list |
| 3 | problem | bg_dark | Dark — large headline, body paragraph |
| 4 | current_solutions | bg_light | Light — 3 red-X cards |
| 5 | what_if | primary | Dark — centered icon, headline, italic body |
| 6 | product | bg_light | Light — content card with left accent border |
| 7 | vision | bg_dark | Dark — target icon, headline, market detail |
| 8 | traction | bg_light | Light — metric cards in 2-row grid |
| 9 | differentiation | bg_light | Light — comparison card + dark detail card |
| 10 | tailwinds | bg_dark | Dark — 3 accent-bordered cards |
| 11 | why_now | bg_light | Light — content card with left accent border |
| 12 | founder_market_fit | primary | Dark — person icon, italic narrative |
| 13 | milestones | bg_light | Light — numbered step cards |
| 14 | sweeten_the_pot | bg_dark | Dark — gem icon, centered headline + body |
| 15 | call_to_action | bg_dark | Dark — large bold CTA text, email icon |

---

## Color System

All colors come from the theme object. Never hardcode colors except for structural
elements. The theme object always contains:

```
primary    — main brand color (dark slides, headers)
secondary  — accent color (icons, card tops, checkmarks)
accent     — pop color (decorative lines, highlights)
bg_dark    — near-black derived from primary (dark slide backgrounds)
bg_light   — warm off-white (light slide backgrounds)
text_light — FFFFFF (text on dark slides)
text_dark  — 1E293B (text on light slides)
text_muted — 64748B (section labels, captions)
font_header — header font (Georgia default)
font_body   — body font (Calibri default)
```

---

## Typography Scale

| Element | Size | Weight | Font |
|---------|------|--------|------|
| Slide hero headline | 48–54pt | bold | font_header |
| Section headline | 30–36pt | bold | font_header |
| What If headline | 36pt | bold | font_header, centered |
| Vision headline | 36–40pt | bold | font_header |
| Card body text | 14–16pt | normal | font_body |
| Section label | 9pt | bold | font_body, charSpacing:3, UPPERCASE |
| Founder narrative | 16–18pt | italic | font_body |
| Metric card text | 14–16pt | normal | font_body, centered |
| CTA headline | 36–44pt | bold | font_header, centered |

---

## Section Labels

Every light slide gets a small UPPERCASE section label top-left.

```javascript
slide.addText("SECTION NAME", {
  x: 0.7, y: 0.3, w: 4, h: 0.25,
  fontSize: 9, color: theme.text_muted,
  fontFace: theme.font_body,
  charSpacing: 3, bold: true, margin: 0
});
```

Dark slides do NOT get section labels — the design contrast is sufficient.
Exception: Founder-Market Fit (dark) gets a small "FOUNDER-MARKET FIT" label.

---

## Content Positioning Rule — CRITICAL

Section labels sit at y=0.3 with h=0.25, bottom edge at y=0.55.
Headlines must start at y=0.75 minimum to avoid collision.
The accent underline (if used) must sit BELOW the headline bottom edge.

**Calculate headline height based on content:**
- Single-line headline at 36pt: h=0.7
- Two-line headline at 36pt: h=1.1
- Two-line headline at 30pt: h=0.9
- Estimate lines: `Math.ceil(headline.length / 35)` for 36pt at 8.6" wide

**All downstream elements must respect the actual headline bottom:**
```javascript
const headlineLines = Math.ceil(headline.length / 35);
const headlineH = headlineLines === 1 ? 0.7 : headlineLines * 0.55;
const headlineBottom = 0.75 + headlineH;
// Place accent bar and content BELOW headlineBottom
const accentBarY = headlineBottom + 0.1;
const contentStartY = accentBarY + 0.2;
```

---

## Card Layouts

### Standard content card (light slides)
```javascript
// Card background
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.7, y: contentStartY, w: 8.6, h: cardH,
  fill: { color: "FFFFFF" },
  shadow: makeShadow()
});
// Left accent border
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.7, y: contentStartY, w: 0.08, h: cardH,
  fill: { color: theme.secondary }
});
```

### Dark detail card (differentiation slide)
```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.7, y: detailY, w: 8.6, h: detailH,
  fill: { color: theme.primary }
});
```

### Shadow — ALWAYS use a factory function, never reuse the object
```javascript
const makeShadow = () => ({
  type: "outer", color: "000000", blur: 6,
  offset: 2, angle: 135, opacity: 0.12
});
```

---

## Slide-by-Slide Layout Guide

### Slide 1 — Title (dark)
- Accent top bar: x:0, y:0, w:10, h:0.08, fill:accent
- Company name: x:0.8, y:1.4, w:8.4, h:1.4, fontSize:54, bold, centered, text_light
- Subtitle: x:1.5, y:3.0, w:7, h:0.8, fontSize:20, color:accent, centered
- Decorative line under subtitle: x:4.2, y:3.9, w:1.6, h:0.04, fill:accent

### Slide 2 — Credibility (light)
- Section label: "ABOUT US"
- Headline: dynamic height, y:0.75
- Accent bar below headline
- Accomplishments: checkmark icon + text, spaced 0.65" apart starting below accent bar
- Max 5 accomplishments. If more than 4, reduce spacing to 0.55"

### Slide 3 — Problem (dark)
- Warning triangle icon: x:0.7, y:0.5, w:0.7, h:0.7
- Headline starts x:1.5 (beside icon), y:0.4, large and bold
- Accent bar below headline
- Body text in a card: light semi-transparent background

### Slide 4 — Current Solutions (light)
- Section label: "CURRENT SOLUTIONS"
- Headline: dynamic height, y:0.75
- 3 cards with red X icon, spaced evenly below headline
- Card height: 0.9". Total cards span must fit above footer (max y+h = 5.3)
- Calculate card y: `contentStartY + (i * (cardH + 0.15))`

### Slide 5 — What If (dark, primary color)
- Lightbulb icon: centered, x:4.5, y:0.6, w:1, h:1
- Headline: centered, y:1.8, fontSize:36
- Body: centered, italic, y:2.8, h calculated from content length

### Slide 6 — Product (light)
- Section label: "OUR PRODUCT"
- Headline: dynamic height, y:0.75
- Content card with left secondary border
- Body as \n-separated lines, fontSize:16
- Screenshot placeholder: dashed border box below content card
- Body card height: calculate from line count. 3 lines ≈ 1.8", 4 lines ≈ 2.2"

### Slide 7 — Vision (dark)
- Target/circle icon: x:0.7, y:0.5, w:0.7, h:0.7
- Headline: large, y:1.2
- Accent bar below
- Vision statement in bold, larger text
- Market detail in smaller muted text below

### Slide 8 — Traction (light)
- Section label: "TRACTION"
- Headline "So far, so good..." y:0.75
- Metric cards in grid: up to 6 metrics, 2 rows of 3
- Each card: w:2.9, h:1.4, with icon and centered text
- Row 1 y:1.6, Row 2 y:3.15

### Slide 9 — Differentiation (light)
- Section label: "WHY WE WIN"
- Headline (approach field): dynamic height, y:0.75
- Comparison card below: h calculated from comparison text length
- Dark detail card below comparison: h calculated from detail text length
- Shield icon in detail card left margin

### Slide 10 — Tailwinds (dark)
- "TAILWINDS" label: y:0.3
- "The waves we're riding" headline: y:0.6, fontSize:32
- 3 accent-bordered cards below, stacked vertically
- Each card: h:0.9, spacing:0.15, starting y:1.5
- Left accent border on each card (secondary color)
- Trend icon per card (FaArrowUp, FaGlobeAmericas, FaBolt)
- Maximum 3 tailwinds — coach founder to pick strongest 3

### Slide 11 — Why Now (light)
- Section label: "TIMING"
- "Why NOW?" headline: y:0.75, fontSize:40
- Clock icon: x:8.6, y:0.65, w:0.65, h:0.65
- Content card: h calculated from body length, min h:1.8
- Accent left border on content card

### Slide 12 — Founder-Market Fit (dark, primary)
- "FOUNDER-MARKET FIT" label in text_muted
- "Why I was built for this" headline: y:0.7, fontSize:32
- Accent bar below headline
- Person icon: x:0.7, y:1.75, w:0.5, h:0.5
- Body text: starts y:2.4, h calculated from content
  - Calculate: `Math.ceil(body.length / 80) * 0.35 + 0.5` for height estimate
  - Min h:2.0, but expand as needed. Slide height limit: 5.3"
  - fontSize:16, italic, color:E2E8F0
- If body has 3+ founders (contains multiple \n), reduce fontSize to 15pt

### Slide 13 — Milestones (light)
- Section label: "THE ASK"
- Headline: dynamic height, y:0.75, fontSize:30
- 4 numbered step cards, stacked vertically
- Each card: h:0.75, spacing:0.12, starting at contentStartY
- Number label: colored filled rectangle (NOT oval — more reliable), w:0.45, h:0.45
  - fill: theme.primary (NOT secondary — secondary may be too light)
  - text: white, centered, bold, fontSize:14
- Milestone text: starts x:1.55

### Slide 14 — Sweeten the Pot (dark)
- Gem icon: centered, x:4.5, y:0.5, w:0.8, h:0.8
- Headline "One more thing...": centered, y:1.5, fontSize:36
- Accent line below headline: x:4.2, y:2.45, w:1.6, h:0.04
- Body: centered, y:2.65, h calculated from content
  - One piece of news, 2-3 sentences max
  - fontSize:18, color:E2E8F0

### Slide 15 — CTA (dark)
- Top accent bar: x:0, y:0, w:10, h:0.08
- CTA text: centered, y:1.2, w:9, h:2.2, fontSize:36–44 (scale down for long text), bold
- Email icon: centered, x:4.6, y:3.6, w:0.7, h:0.7
- Contact line: centered, y:4.45, fontSize:18, text_muted

---

## Anti-Patterns — Never Do These

From the pptx SKILL.md:
- **NEVER use accent lines under titles** — use whitespace instead. Exception: our thin
  accent bars (h:0.05, w:1.2) are decorative and used sparingly, not as full-width
  underlines. Keep them narrow.
- **Never hardcode `#` prefix on hex colors** — causes file corruption
- **Never reuse shadow objects** — use `makeShadow()` factory function every time
- **Never use ROUNDED_RECTANGLE with accent overlay bars** — use RECTANGLE instead
- **Never encode opacity in 8-char hex** — use `opacity` property on shadow object
- Do not repeat content from credibility slide on traction slide
- Do not put section labels on dark slides (except Founder-Market Fit)
- **Do not set a fixed minimum card height** — cards must size to actual content. A comparison card with one sentence should be ~0.85" tall, not 1.6". Calculate from text height, not from a floor value. Sparse cards with lots of empty space look broken.

---

## Dynamic Height Calculation Helpers

Use these patterns when sizing text boxes to actual content:

```javascript
// Estimate lines for a given text at a given font size and box width
function estimateLines(text, fontSize, boxWidthInches) {
  // Approximate chars per line based on font size and box width
  const charsPerLine = Math.floor(boxWidthInches * (96 / fontSize) * 1.4);
  const lines = text.split('\n');
  let totalLines = 0;
  for (const line of lines) {
    totalLines += Math.max(1, Math.ceil(line.length / charsPerLine));
  }
  return totalLines;
}

// Get height for a text block
function textHeight(text, fontSize, boxWidth, lineHeightInches) {
  return estimateLines(text, fontSize, boxWidth) * lineHeightInches;
}

// Line height reference (inches):
// 9pt  → 0.18"
// 14pt → 0.26"
// 16pt → 0.28"
// 18pt → 0.32"
// 20pt → 0.35"
// 28pt → 0.45"
// 30pt → 0.48"
// 36pt → 0.56"
// 40pt → 0.62"
// 54pt → 0.82"
```

---

## QA Checklist

After generating, run thumbnail.py and inspect every slide for:
- Section label visible and not overlapping headline
- Headline fully visible, not cut off or overlapping accent bar
- All card text visible, not cut off at bottom
- No element extends below y=5.3 (footer starts at 5.45)
- Founder-Market Fit: all founders named, last line visible
- Milestones: numbered labels visible (not white-on-white)
- Title slide: actual company name, not "Company Name"
- Current Solutions: all 3 cards have text
- Traction: all metric cards have content
