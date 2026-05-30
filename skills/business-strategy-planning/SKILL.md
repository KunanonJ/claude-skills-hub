---
name: Business Strategy and Planning
description: Comprehensive business planning using the Miyabi 8-phase framework — self-analysis, product concept, persona development, market sizing (TAM/SAM/SOM), revenue modeling, GTM strategy, 3-year financial forecast, and execution roadmap. Use when creating business plans, product strategies, or Go-To-Market plans.
allowed-tools: Read, Write, WebFetch, Bash
---

# 💼 Business Strategy and Planning

**Version**: 2.0.0 | **Priority**: ⭐⭐⭐ (P2 - Business) | **Source**: [mcpmarket.com](https://mcpmarket.com/tools/skills/business-strategy-planning-1) | **Author**: ShunsukeHayashi

Generates comprehensive business plans and product strategies using a structured 8-phase framework (Miyabi) with market analysis tools. Designed for founders and product managers moving from an initial idea to a structured GTM strategy and 3-year financial forecast.

---

## Triggers

| Trigger | Example |
|---|---|
| Business plan | "create a business plan" |
| Product strategy | "define our product strategy" |
| Customer identification | "identify target customers" |
| New venture | "starting new business/product" |

---

## 8-Phase Business Planning Framework

Each phase has a dedicated agent and produces a specific artifact:

| Phase | Task | Agent | Deliverable |
|---|---|---|---|
| **1** | Self-analysis | じぶんるん | Strengths/weaknesses analysis |
| **2** | Product concept | つくるそん | USP, Business Model Canvas |
| **3** | Persona design | ぺるそん | 3–5 customer personas |
| **4** | Market analysis | しらべるん | TAM / SAM / SOM |
| **5** | Revenue model | あきんどさん | Pricing strategy |
| **6** | GTM strategy | ひろめるん | Channel plan |
| **7** | Financial plan | すうじるん | 3-year forecast |
| **8** | Execution plan | あきんどさん | Roadmap |

---

## Analysis Templates

### Business Model Canvas (BMC)

```
┌─────────────┬─────────────────┬─────────────────┬─────────────┐
│ Key Partners│ Key Activities  │                 │ Value       │
│             │                 │ Value           │ Proposition │
├─────────────┤                 │ Proposition     ├─────────────┤
│             ├─────────────────┤                 │ Customer    │
│ Key         │ Key Resources   ├─────────────────┤ Segments    │
│ Resources   │                 │ Channels        │             │
├─────────────┴─────────────────┼─────────────────┴─────────────┤
│ Cost Structure                │ Revenue Streams               │
│                               │                               │
└───────────────────────────────┴───────────────────────────────┘
```

Fill all 9 elements: Key Partners, Key Activities, Key Resources, Value Propositions, Customer Relationships, Channels, Customer Segments, Cost Structure, Revenue Streams.

### TAM / SAM / SOM

| Market | Definition | How to Calculate |
|---|---|---|
| **TAM** | Total Addressable Market | Industry reports |
| **SAM** | Serviceable Addressable Market | TAM × region/segment filter |
| **SOM** | Serviceable Obtainable Market | SAM × realistic market share |

```
TAM → SAM → SOM
$10B  →  $2B  →  $200M (10% of SAM in year 3)
```

### Persona Template

```yaml
Persona:
  name: "Jane Smith"
  age: 35
  role: "IT Manager at mid-size company"
  pain_points:
    - "Team productivity gaps"
    - "Tool sprawl and management overhead"
  goals:
    - "Reduce overtime through automation"
    - "Improve team morale"
  buying_criteria:
    - "Clear ROI within 6 months"
    - "Easy onboarding, no heavy IT lift"
```

Create 3–5 distinct personas covering primary and secondary user types.

---

## Revenue Models

| Model | Characteristic | Best Fit |
|---|---|---|
| **Freemium** | Free → paid conversion | SaaS, B2C |
| **Subscription** | Monthly / annual | SaaS, B2B |
| **Usage-based** | Pay per use | API, Infrastructure |
| **Tiered** | Stepped pricing | Diverse customer segments |

### LTV Calculation

```
LTV = ARPU × Gross Margin × (1 / Churn Rate)

Example: ¥10,000 × 70% × (1 / 5%) = ¥140,000
         $100   × 70% × (1 / 5%) = $1,400
```

**Key SaaS metrics to track:**
- CAC (Customer Acquisition Cost)
- LTV/CAC ratio (target ≥ 3)
- Payback period (target < 12 months)
- NRR (Net Revenue Retention)

---

## Financial Plan Structure (3-Year)

```
Year 1: Foundation
  Revenue: $X (target: cover 50% of burn)
  Focus: PMF validation, early customers

Year 2: Growth
  Revenue: $3–5X (MoM growth 15–20%)
  Focus: Channel optimization, team scaling

Year 3: Scale
  Revenue: $8–15X (path to profitability)
  Focus: Expansion, international / enterprise
```

---

## GTM Strategy Framework

1. **Ideal Customer Profile (ICP)** — firmographics, technographics, behavioral signals
2. **Positioning** — unique value vs. alternatives, category creation vs. entry
3. **Channels** — outbound, inbound, PLG, partnerships, community
4. **Launch sequence** — beta → launch → expansion
5. **Success metrics** — activation rate, time-to-value, NPS, retention

---

## Success Criteria

| Deliverable | Standard |
|---|---|
| BMC | All 9 elements completed |
| Personas | 3–5 distinct profiles with pain points + buying criteria |
| TAM/SAM/SOM | Sourced figures with methodology documented |
| Financial plan | 3-year forecast with assumptions logged |
| GTM plan | Channel mix + launch timeline |

---

## Workflow

```
[1] Self-analysis    → Strengths, weaknesses, founder-market fit
[2] Product concept  → Problem statement, USP, BMC draft
[3] Persona design   → 3–5 customer profiles
[4] Market sizing    → TAM/SAM/SOM with sources
[5] Revenue model    → Pricing strategy + LTV/CAC projection
[6] GTM strategy     → Channels, launch plan, positioning
[7] Financial plan   → 3-year P&L forecast
[8] Execution plan   → Roadmap with milestones and owners
```

---

## Related Skills

- **market-research** — Market data and competitive intelligence
- **saas-metrics-coach** — KPI design and SaaS health tracking
- **financial-analyst** — Detailed financial modeling (DCF, budgeting)
- **sales-engineer** — Sales strategy and enablement
- **competitive-intel** — Competitive teardown and positioning
