---
name: awesome-claude-design
description: Pick and apply a DESIGN.md from 68 curated brand design systems to scaffold a full UI. Use when asked to "set up a design system", "use a DESIGN.md", "scaffold UI tokens", "pick a design style", or "use Claude Design".
license: MIT
metadata:
  author: KunanonJ
  version: "1.0"
  source: https://github.com/VoltAgent/awesome-claude-design
---

# awesome-claude-design

68 ready-to-use `DESIGN.md` files that scaffold a full design system (color tokens, type scale, components, UI kit) in one drop into Claude Design.

## What is DESIGN.md?

`DESIGN.md` is a plain-text markdown file describing a brand's visual language in a format AI agents can act on — tokens, rules, and rationale in one file. Drop it into a project and tell Claude to reference it before writing any UI.

| File | Who reads it | What it defines |
|------|-------------|-----------------|
| `AGENTS.md` | Coding agents | How to build the project |
| `DESIGN.md` | Design agents | How the project should look and feel |

## Install the CLI

```bash
npm install -g getdesign
```

## Usage

```bash
# In your project root, download a design system:
getdesign add claude         # Warm terracotta, parchment canvas, editorial serif
getdesign add linear         # Ultra-minimal, precise, purple accent
getdesign add stripe         # Signature purple gradients, weight-300 elegance
getdesign add vercel         # Black/white precision, Geist font
getdesign add apple          # Premium white space, SF Pro, cinematic
getdesign add supabase       # Dark emerald, code-first
getdesign add spotify        # Vibrant green on dark, bold type
getdesign add notion         # Warm minimalism, serif headings, soft surfaces
getdesign add figma          # Vibrant multi-color, playful yet professional
getdesign add tesla          # Radical subtraction, cinematic photography
```

This writes a `DESIGN.md` to your project root. Then reference it in Claude:

> "Use DESIGN.md as your style reference before writing any UI components."

## Available Design Systems (68 total)

### AI & LLM Platforms
`claude` · `cohere` · `elevenlabs` · `minimax` · `mistral.ai` · `ollama` · `opencode.ai` · `replicate` · `runwayml` · `together.ai` · `voltagent` · `x.ai`

### Developer Tools & IDEs
`cursor` · `expo` · `lovable` · `raycast` · `superhuman` · `vercel` · `warp`

### Backend, Database & DevOps
`clickhouse` · `composio` · `hashicorp` · `mongodb` · `posthog` · `sanity` · `sentry` · `supabase`

### Productivity & SaaS
`cal` · `intercom` · `linear.app` · `mintlify` · `notion` · `resend` · `zapier`

### Design & Creative Tools
`airtable` · `clay` · `figma` · `framer` · `miro` · `webflow`

### Fintech & Crypto
`binance` · `coinbase` · `kraken` · `mastercard` · `revolut` · `stripe` · `wise`

### E-commerce & Retail
`airbnb` · `meta` · `nike` · `shopify`

### Media & Consumer Tech
`apple` · `ibm` · `nvidia` · `pinterest` · `playstation` · `spacex` · `spotify` · `theverge` · `uber` · `vodafone` · `wired`

### Automotive
`bmw` · `bugatti` · `ferrari` · `lamborghini` · `renault` · `tesla`

## With Claude Design (claude.ai/design)

**Option A — Start from a design system:**
1. Go to `claude.ai/design/#org` → Create new design system
2. On setup screen, upload your `DESIGN.md` under "Add assets"

**Option B — Start from a prototype:**
1. Create a new prototype, attach `DESIGN.md` in chat
2. Prompt: `"Create a design system from this DESIGN.md"`

Claude produces:
- `colors_and_type.css` — CSS variables and type scale
- `preview/` — color, type, spacing, component cards
- `index.html` — working UI kit applying the full system
- `SKILL.md` — portable skill for future projects

## What each DESIGN.md contains

| Section | Purpose |
|---------|---------|
| Visual Theme & Atmosphere | Tone, density, mood |
| Color Palette & Roles | CSS variables with semantic names |
| Typography Rules | Type scale, Google Fonts fallbacks |
| Component Stylings | Buttons, inputs, cards, nav with states |
| Layout Principles | Spacing scale, grid, whitespace rhythm |
| Depth & Elevation | Shadow tokens and surface hierarchy |
| Do's and Don'ts | Guardrails for generating new screens |
| Responsive Behavior | Breakpoints, touch targets |
| Agent Prompt Guide | Reusable prompts for the generated SKILL.md |

## Tips

- **Start in a fresh project** — Claude Design anchors the system to the project it was scaffolded in.
- **Ask for variants** — request light/dark, compact/comfortable, or marketing/app variants.
- **Export the `SKILL.md`** — save it to your skills folder to re-summon the same aesthetic in any future Claude project.
- **Use as coding reference** — even without Claude Design, reference `DESIGN.md` directly in Claude Code: *"refer to DESIGN.md for all color and typography decisions."*

## References

- [awesome-claude-design repo](https://github.com/VoltAgent/awesome-claude-design)
- [getdesign.md collection](https://getdesign.md/)
- [Claude Design](https://claude.ai/design)
- [What is DESIGN.md?](https://getdesign.md/what-is-design-md)
