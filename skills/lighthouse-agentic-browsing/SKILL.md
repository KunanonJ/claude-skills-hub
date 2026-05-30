---
name: lighthouse-agentic-browsing
description: Audit and optimize websites for AI agent interaction using Lighthouse Agentic Browsing. Covers WebMCP integration, agent-centric accessibility, llms.txt, and layout stability. Use when building agent-ready sites, auditing agentic readiness, implementing WebMCP tools, or improving how AI agents navigate and interact with a page.
---

# Lighthouse Agentic Browsing

> **Experimental** — Agentic Browsing audits and WebMCP are based on proposed Chrome standards (as of 2026-05-05).
> Reference: https://developer.chrome.com/docs/lighthouse/agentic-browsing/scoring

Evaluate and optimize how well a site is constructed for **machine interaction by AI agents**. Lighthouse's Agentic Browsing category runs deterministic audits across four pillars and reports a pass ratio instead of a 0–100 score.

---

## When to Use This Skill

- Building a site or app that AI agents should be able to navigate and use
- Running an agentic readiness audit before launch
- Implementing WebMCP to expose site logic or forms to AI agents
- Diagnosing why an AI agent is failing to interact with a page reliably
- Setting up CI/CD checks for agentic readiness
- Adding `llms.txt` to a domain root for agent discoverability

---

## Scoring Model

Unlike Performance / SEO / Accessibility (0–100 weighted average), Agentic Browsing reports:

| Output | Meaning |
|---|---|
| **Fractional score** | `passed / total` agentic readiness checks (e.g. 7/10) |
| **Pass / Fail per audit** | Errors or warnings when requirements aren't met |
| **Informational counts** | Pass ratio in category header for CI tracking |

**Why scores fluctuate:** Three causes:
1. **Dynamic tool registration timing** — imperative (JS) WebMCP tools may not be captured during Lighthouse snapshot
2. **A11y tree construction changes** — DOM size or complexity changes alter the accessibility tree
3. **Cumulative Layout Shift** — ads, unsized images, or injected content shift elements between agent detection and interaction

---

## The Four Audit Pillars

### 1. WebMCP Integration

Lighthouse calls the CDP `WebMCP` domain to verify tools are registered. Two modes:

#### Declarative (HTML) — preferred for forms and stable UI

```html
<!-- Register a search form as a WebMCP tool -->
<form method="POST" action="/search"
      mcp-tool="search"
      mcp-description="Search the product catalog by keyword">
  <input name="q" type="search"
         mcp-param="query"
         mcp-description="Search keywords">
  <button type="submit">Search</button>
</form>
```

#### Imperative (JavaScript) — for dynamic or programmatic tools

```js
// Register tools via the WebMCP Imperative API
if ('webmcp' in navigator) {
  navigator.webmcp.registerTool({
    name: 'add-to-cart',
    description: 'Add a product to the shopping cart',
    parameters: {
      productId: { type: 'string', description: 'SKU or product ID' },
      quantity:  { type: 'number', description: 'Number of units', default: 1 },
    },
    handler: async ({ productId, quantity }) => {
      await cart.add(productId, quantity);
      return { success: true, cartCount: cart.size };
    },
  });
}
```

> **Timing warning**: Imperative tools registered after page load may be missed by Lighthouse. Register early — ideally before `DOMContentLoaded`.

**Audits in this pillar:**
- `registered-webmcp-tools` — counts tools successfully captured
- `forms-missing-declarative-webmcp` — forms not yet annotated
- `webmcp-schema-validity` — schema is well-formed JSON

---

### 2. Agent-Centric Accessibility

Agents use the **accessibility tree** as their primary data model — not the visual DOM. Lighthouse checks a specific subset of a11y audits critical for machine interaction:

| Audit | Requirement | Fix |
|---|---|---|
| **Names and labels** | Every interactive element has a programmatic name | Add `aria-label`, `aria-labelledby`, or visible `<label>` |
| **Tree integrity** | Roles and parent-child relationships are valid | Fix invalid ARIA role nesting |
| **Visibility** | Nothing hidden from a11y tree while being interactive | Don't use `aria-hidden="true"` on focusable elements |

#### Practical checklist

```html
<!-- BAD: agent can't identify this button -->
<button><img src="cart.svg"></button>

<!-- GOOD: programmatic name present -->
<button aria-label="Add to cart">
  <img src="cart.svg" alt="">
</button>

<!-- BAD: invalid role nesting -->
<ul role="menu">
  <div role="menuitem">Item</div>  <!-- div not allowed as direct child of ul[menu] -->
</ul>

<!-- GOOD: valid tree -->
<ul role="menu">
  <li role="none">
    <a href="/item" role="menuitem">Item</a>
  </li>
</ul>

<!-- BAD: interactive but hidden from tree -->
<button aria-hidden="true" tabindex="0">Click me</button>

<!-- GOOD: visible to both agents and keyboard users -->
<button>Click me</button>
```

**Test the a11y tree directly:**
```bash
# Chrome DevTools → Accessibility tab → Full page tree
# Or via CLI:
npx axe-cli https://your-site.com --tags wcag2a,wcag2aa
```

Full audit: https://developer.chrome.com/docs/lighthouse/agentic-browsing/accessibility-for-agents

---

### 3. Discoverability — llms.txt

Lighthouse checks for a **machine-readable summary** at `https://yourdomain.com/llms.txt`.

#### Minimal llms.txt

```
# My Site

> One-sentence description of what this site does.

## Key pages

- [Home](https://example.com/): Main landing page
- [API docs](https://example.com/docs/api): REST API reference
- [Pricing](https://example.com/pricing): Plans and pricing

## Tools available

- Search products via WebMCP tool `search` on /search
- Add to cart via WebMCP tool `add-to-cart` on all product pages
```

#### Full llms.txt structure (recommended)

```
# {Site Name}

> {One-line description}

{Optional extended description, 1-3 sentences}

## Sections

- [{Section Title}]({URL}): {What an agent finds here}

## Optional: llms-full.txt

If this file is too large, point to a fuller version:
- [Full context](https://example.com/llms-full.txt)
```

Place at exactly `https://yourdomain.com/llms.txt` (root, not a subdirectory).

Full audit: https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt

---

### 4. Layout Stability (CLS)

Lighthouse measures **Cumulative Layout Shift** — critical because agents identify element positions at one moment and interact at another. Shifts cause misclicks or missed interactions.

#### Target: CLS < 0.1

Common causes and fixes:

```html
<!-- BAD: image shifts layout on load -->
<img src="hero.jpg" alt="Hero">

<!-- GOOD: dimensions reserved upfront -->
<img src="hero.jpg" alt="Hero" width="1200" height="600">

<!-- BAD: ad injected without reserved space -->
<div class="ad-container"></div>

<!-- GOOD: space reserved before ad loads -->
<div class="ad-container" style="min-height: 250px;"></div>
```

```css
/* BAD: font swap causes layout shift */
@font-face {
  font-family: 'MyFont';
  font-display: auto;
}

/* GOOD: swap with size-adjust to minimize shift */
@font-face {
  font-family: 'MyFont';
  font-display: swap;
  size-adjust: 105%;
}
```

Full audit: https://developer.chrome.com/docs/lighthouse/agentic-browsing/layout-stability

---

## Running the Audit

```bash
# Via Chrome DevTools
# DevTools → Lighthouse tab → check "Agentic browsing" → Analyze page load

# Via CLI (requires Chrome 127+)
npx lighthouse https://your-site.com \
  --only-categories=agentic-browsing \
  --output=html \
  --output-path=./agentic-report.html \
  --chrome-flags="--headless"

# CI/CD integration
npx lighthouse https://your-site.com \
  --only-categories=agentic-browsing \
  --output=json \
  --quiet | jq '.categories["agentic-browsing"].score'
```

---

## Agentic Readiness Checklist

### WebMCP
- [ ] All major forms have `mcp-tool` and `mcp-description` attributes
- [ ] All form inputs have `mcp-param` and `mcp-description` attributes
- [ ] Imperative tools registered before `DOMContentLoaded`
- [ ] WebMCP schemas are valid JSON (no syntax errors)
- [ ] Tools are tested with `navigator.webmcp.getTools()` in DevTools console

### Accessibility tree
- [ ] Every `<button>`, `<a>`, `<input>`, `<select>` has a programmatic name
- [ ] No `aria-hidden="true"` on focusable/interactive elements
- [ ] ARIA role parent-child relationships are valid
- [ ] Page passes `axe-core` at `wcag2a` level minimum

### Discoverability
- [ ] `https://yourdomain.com/llms.txt` returns 200 (not 404)
- [ ] `llms.txt` describes key pages and available WebMCP tools
- [ ] `Content-Type: text/plain` header on `llms.txt`

### Layout stability
- [ ] All images and video have explicit `width` and `height`
- [ ] Ad slots have `min-height` reserved before content loads
- [ ] Fonts use `font-display: swap` with `size-adjust`
- [ ] No content injected above existing content after initial load
- [ ] CLS < 0.1 measured in Chrome DevTools Performance panel

---

## Audit Map

```
Agentic Browsing Score = passed_audits / total_audits

├── WebMCP Integration
│   ├── registered-webmcp-tools        (informational count)
│   ├── forms-missing-declarative-webmcp  (warning if forms untagged)
│   └── webmcp-schema-validity         (error if schema malformed)
│
├── Discoverability
│   └── llms-txt                       (fail if missing at root)
│
├── Accessibility for agents
│   ├── names-and-labels subset        (error if missing)
│   ├── tree-integrity subset          (error if invalid roles)
│   └── visibility subset              (error if hidden+interactive)
│
└── Layout stability
    └── cumulative-layout-shift        (fail if CLS ≥ 0.1)
```

---

## Key Concepts

**WebMCP** — Chrome API for exposing site capabilities to AI agents. Two forms:
- *Declarative*: HTML attributes on existing elements (`mcp-tool`, `mcp-param`)
- *Imperative*: JavaScript `navigator.webmcp.registerTool()` calls

**llms.txt** — plain-text file at domain root summarising site structure for LLMs. Convention from [llmstxt.org](https://llmstxt.org).

**A11y tree as agent data model** — agents don't see the visual page; they navigate an in-memory accessibility tree built from ARIA roles, labels, and DOM structure.

**Fractional score** — `n/m` format (e.g. `8/10`) rather than 0–100 because agentic web standards are still being defined. Treat it as a progress tracker, not a ranking.

---

## Resources

- [Scoring overview](https://developer.chrome.com/docs/lighthouse/agentic-browsing/scoring)
- [Registered WebMCP tools audit](https://developer.chrome.com/docs/lighthouse/agentic-browsing/registered-webmcp-tools)
- [Forms missing declarative WebMCP](https://developer.chrome.com/docs/lighthouse/agentic-browsing/forms-missing-declarative-webmcp)
- [WebMCP schema validity](https://developer.chrome.com/docs/lighthouse/agentic-browsing/webmcp-schema-validity)
- [llms.txt audit](https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt)
- [Accessibility for agents](https://developer.chrome.com/docs/lighthouse/agentic-browsing/accessibility-for-agents)
- [Layout stability audit](https://developer.chrome.com/docs/lighthouse/agentic-browsing/layout-stability)
- [WebMCP Imperative API](https://developer.chrome.com/docs/ai/webmcp/imperative-api)
- [File a Lighthouse issue](https://github.com/GoogleChrome/lighthouse/issues)
