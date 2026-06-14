---
name: roadmap-communication
description: >
  Same roadmap, three audiences. Produce executive, customer, and internal
  variants of a single roadmap with appropriate framing, detail level, and
  risk language for each.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-execution
  updated: 2026-05-21
  tech-stack: roadmap, communication, now-next-later, outcome-roadmap, marty-cagan
---
# Roadmap Communication Expert

## Overview

A single roadmap cannot serve every audience. Executives need confidence and strategic framing. Customers need plausible promises with credible timelines. Internal teams need detail, dependency awareness, and honest risk. When PMs publish one roadmap to all three, one audience is always wrong -- either the executives are bored, customers feel misled, or engineers feel managed.

This skill produces three variants of the same underlying roadmap, each tailored to its audience. The underlying source of truth -- the roadmap data -- stays single. The framing, the level of detail, the risk language, and the visualization all change. The variants share names and identifiers so a customer reference can be traced back through the internal variant to the actual ticket.

The structural backbone is **Now / Next / Later** (popularized by Janna Bastow at ProdPad and now used widely), which Marty Cagan calls "right-sizing the roadmap" -- forecast confidence decreases with time horizon, so commit explicitly to "Now" items, name "Next" items by theme, and keep "Later" deliberately fuzzy. Each variant exposes a different slice of that backbone.

### When to Use

- **Quarterly roadmap publication** -- the regular cadence where you communicate to multiple audiences.
- **Pre-board meeting** -- the executive variant feeds the board packet.
- **Annual customer conference** -- the customer variant becomes the conference roadmap session.
- **Engineering kickoff** -- the internal variant grounds sprint planning across multiple teams.
- **Sales enablement** -- the customer variant feeds sales reps' "what's coming" pitch.

### When NOT to Use

- For a single-team backlog with one stakeholder (one roadmap suffices).
- For tactical sprint planning (use `../scrum-master/` outputs).
- For incident communication or in-flight project status (use `status-update-generator/`).

## The three variants

| Variant | Audience | Time horizon detail | Risk framing | Format |
|---------|----------|---------------------|--------------|--------|
| **Executive** | Board, exec team, investors | Outcome-led; quarterly | Confidence levels (high/med/low) | 1-page narrative + simple visual |
| **Customer** | Customers, partners, sales prospects | Theme-led; "this year / later this year / next year" | No risk language; "exploring", "in development", "shipping soon" | Themes + benefit statements, no dates beyond current quarter |
| **Internal** | Engineering, design, support, account teams | Feature-led with dependencies | Explicit risks with mitigations | Detailed table with owners, dependencies, links to PRDs |

### What changes across variants

| Element | Executive | Customer | Internal |
|---------|-----------|----------|----------|
| **Granularity** | Outcomes (3-7 items) | Themes (5-10 items) | Features (15-50 items) |
| **Time horizon** | This quarter / next quarter / H2 | Now / Next / Later (themes only) | Sprint-by-sprint for "Now"; quarter for "Next" |
| **Dates** | Quarter only | Quarter only for "Now"; "later this year" for "Next" | Specific sprint and release dates for "Now" |
| **Risk** | Confidence per outcome | None (use language like "exploring" / "shipping soon") | Explicit: tigers, mitigations, dependencies |
| **Owner** | Exec sponsor per outcome | None | PM, EM, design lead per feature |
| **Metric** | Outcome metric + target | Benefit statement | KR + leading indicator |
| **What's NOT here** | Implementation detail, risk discussion | Risk, dependencies, internal team names | Marketing language, exec framing |
| **Visual** | Now/Next/Later 3-column or Gantt-summary | Themed cards or simple Now/Next/Later | Detailed table or Gantt |

## The "right-size the roadmap" principle

Marty Cagan's observation: **forecast confidence drops sharply with time horizon**. A 2-week commitment can be 90% confident. A 1-quarter commitment is maybe 70%. A 1-year commitment is 30% at best. Pretending otherwise (by promising features 9 months out) trains customers to disbelieve every roadmap you publish.

The Now / Next / Later structure encodes this honesty:

- **Now (this quarter):** Specific features with committed dates. Build is in flight or starting imminently. High confidence.
- **Next (next 1-2 quarters):** Themes with named outcomes, but specific features are not committed. Medium confidence.
- **Later (beyond):** Directions, hypotheses, big bets. Deliberately fuzzy. Low confidence by design.

Each audience needs this honesty calibrated:

- **Executives** want confidence ratings on each item (so they can plan).
- **Customers** want forward visibility without firm dates (so they can buy with confidence in the direction).
- **Internal teams** want explicit dependencies and risks (so they can execute).

## Outcome-based vs feature-based roadmaps

A second axis: **outcomes vs features**. Cagan and Torres both argue for outcome-based roadmaps -- the roadmap promises a customer outcome ("reduce onboarding from 14 days to 3 days"), not a feature ("ship guided onboarding wizard"). Outcomes survive scope changes; features become commitments that bind you to wrong solutions.

| Variant | Default orientation |
|---------|---------------------|
| Executive | Outcome-based always |
| Customer | Mix: themes (outcomes) for Next/Later; specific features for Now (when they are committed) |
| Internal | Feature-based for execution, but each feature must trace to an outcome |

The translation from feature to outcome is the highest-leverage move a PM can make in roadmap communication. "We are shipping X" is a feature. "Customers can now achieve Y" is an outcome.

## Variant 1: Executive Roadmap

**Purpose:** Build confidence that the team is solving the right problems and is on track.

**Length:** 1 page (slide or memo).

**Structure:**

1. **Header:** Quarter, sponsor, the one-sentence strategy this roadmap serves.
2. **Now (this quarter) -- 3-5 outcomes:** Each outcome named, with metric target, confidence rating (High/Med/Low), and lead PM.
3. **Next (next quarter) -- 3-5 outcomes:** Theme-level. No specific features. Confidence is implicit (Medium).
4. **Later (H2 directions) -- 2-3 big bets:** One line each. Deliberately fuzzy.
5. **What we are explicitly NOT doing this period:** 2-3 items. Builds credibility by showing tradeoffs.

**Voice:** Direct, plain, confident-but-honest. No marketing adjectives. No "leveraging" or "synergizing." Bezos memo style.

**Visualization:** Now/Next/Later 3-column or a slim Gantt of the 3-5 Now-quarter outcomes. Avoid swim-lane explosions.

## Variant 2: Customer Roadmap

**Purpose:** Help customers and prospects make confident purchase or expansion decisions; help sales sell direction without overcommitting.

**Length:** 2-5 themed cards (web page or 1-2 slides).

**Structure:**

1. **Header:** "What's coming in [year]" -- positions roadmap as a window, not a contract.
2. **Now (this quarter) -- 3-5 themes with named features:** "Workflow automation: Connect tasks to your CRM with built-in triggers. Available this quarter."
3. **Next -- 3-5 themes, features unnamed:** "Reporting: deeper drill-down across teams and saved-view collaboration. Coming later this year."
4. **Exploring (Later) -- 2-3 directions:** "Exploring: AI-assisted task creation from meeting notes. Early experiments underway."

**Voice:** Benefits-led, customer-perspective. No internal team names. No release versions. No risk language. Use directional language ("exploring", "in development", "shipping soon") instead of dates beyond the current quarter.

**Visualization:** Themed cards (Notion / Productboard / Cards format). Avoid Gantt -- it reads as a commitment.

**Important caveats to repeat on the page:**

- "This roadmap is directional and may change as we learn from customers."
- "Items in 'Exploring' are not commitments."
- "Dates are based on current planning and may shift."

## Variant 3: Internal Roadmap

**Purpose:** Coordinate execution across teams; surface risks, dependencies, and capacity issues; enable detailed sprint planning.

**Length:** Detailed table or multi-tab spreadsheet/wiki. No length limit.

**Structure:**

1. **Header:** Quarter, sponsor, strategy reference, link to NSM and OKRs.
2. **Now (this quarter) -- features by team:**
   - Feature name, PM, EM, design lead, status, target sprint/release, KR mapped, dependencies, risks
3. **Next (next 1-2 quarters) -- themes with candidate features:**
   - Theme, PM, EM, target quarter, dependencies expected, open questions
4. **Later (H2) -- directions and hypotheses:**
   - Direction, sponsor, what we'd need to be true to commit
5. **Cross-cutting dependencies:** Platform changes, infra work, external vendor work
6. **Capacity view:** Team commitment vs available capacity per quarter

**Voice:** Direct, candid, complete. Risks named explicitly. Mitigations specified. Dependencies traced. This document trains trust internally and is the source of truth for the other two variants.

**Visualization:** Detailed table (sortable by team, quarter, status). Cross-link to PRDs (`create-prd/`), OKRs (`brainstorm-okrs/`), NSM (`north-star-metric/`), and PR/FAQs (`prfaq/`).

## Workflow

1. **Author the internal variant first.** This is the source of truth. All fields, all risks, all dependencies. Use the template in `assets/internal_roadmap_template.md`.
2. **Derive the executive variant.** Strip implementation; promote each Now item to its parent outcome; assign confidence ratings; remove dependencies; cap at 1 page.
3. **Derive the customer variant.** Translate features into customer benefits; strip dates beyond current quarter; remove risk language; use "exploring / in development / shipping soon."
4. **Run a triangulation check.** Pick one item in the Now bucket. Trace it from the internal feature to the executive outcome to the customer benefit. The three should be consistent -- different framings of the same thing.
5. **Distribute with named recipients.** Each variant has a distribution list. The internal variant is wiki-published; executive is in the board packet; customer goes on the public site or in sales decks.
6. **Re-publish on a fixed cadence.** Quarterly is standard; monthly for fast-moving startups.
7. **Update the customer variant LAST.** Customer-facing language outlives the items; surprise changes erode trust more than slow updates would.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Sales reps quote internal roadmap dates to prospects | One roadmap is being used by all audiences | Publish three variants; restrict internal-variant access; train sales on the customer variant |
| Executives say "I do not understand what's changing" between roadmap updates | Executive variant is feature-level instead of outcome-level | Rewrite Now items as outcomes; cap at 5 items per quarter |
| Customers feel misled when a "Later" item never ships | Customer variant uses commitment language for Later items | Use exploratory language ("exploring", "early experiments"); add the standard caveats line |
| Engineers feel managed by the customer variant | Customer variant lacks risk and the team feels accountable for the marketing version | Make the internal variant the operational source of truth; route engineering planning off internal only |
| The three variants drift apart over the quarter | No re-publication cadence; only updated when there's "news" | Publish on a fixed quarterly cadence; force the triangulation check at each update |
| Customer variant has 30 items | Mistaking comprehensiveness for transparency | Cap at 5-10 themes. More items dilute the signal and increase the surface area for "we never shipped X" |
| Internal variant lacks owners/dates | Created as a marketing asset, not as an execution tool | Make ownership and dates mandatory fields; reject roadmap entries without them |

## Success Criteria

- Every Now-quarter item exists in all three variants with consistent identity (same ID, different framing)
- The executive variant fits on one page and has 3-5 outcome items per Now-quarter
- The customer variant uses no internal team names, no dates beyond current quarter, and includes the directional caveats
- The internal variant has owner, dependencies, risks, and KR mapping for every Now item
- The triangulation check passes for every published roadmap (each item traces consistently across variants)
- Roadmaps are republished on a predictable cadence (quarterly minimum)
- A customer reading the customer variant 6 months later does not feel misled

## Scope & Limitations

**In Scope:**
- Three roadmap variants (executive, customer, internal) from a shared underlying spec
- Now / Next / Later horizon structure with audience-appropriate detail
- Outcome-based framing for executive and customer variants
- Detailed feature/dependency/risk framing for internal variant
- Triangulation check ensuring consistency across variants
- Templates for each variant

**Out of Scope:**
- Backlog prioritization (use `prioritization-frameworks/`)
- OKR drafting (use `brainstorm-okrs/`)
- NSM definition (use `north-star-metric/`)
- Outcome-roadmap transformation (use `outcome-roadmap/`)
- Sprint planning (use `../scrum-master/`)
- Marketing launch copy (handoff to marketing skills)
- Detailed dependency graphs (use `dependency-map/`)

**Important Caveats:**
- Three variants triple the maintenance load. Teams without the discipline to keep them aligned will be better off publishing only the internal variant and disclaiming everything else. The three-variant pattern is for teams that can sustain quarterly re-publication.
- The customer variant is a public commitment. Treat updates as carefully as you treat a launch. Surprise changes erode trust.
- The internal variant must remain non-public. Sales reps must be trained to quote the customer variant only.
- Outcome-based roadmaps require an NSM and OKRs to function. Without those, "outcomes" are unmeasurable aspirations.

## Integration Points

| Integration | Direction | Description |
|-------------|-----------|-------------|
| `execution/outcome-roadmap/` | Receives from | Outcome decomposition feeds the executive variant |
| `execution/north-star-metric/` | Receives from | NSM and inputs are the executive variant's metrics |
| `execution/brainstorm-okrs/` | Receives from | KRs map to internal roadmap items |
| `execution/create-prd/` | Receives from | Each Now-quarter feature in the internal variant links to its PRD |
| `execution/prfaq/` | Receives from | PR/FAQ summaries become the seed of customer variant theme descriptions |
| `execution/prioritization-frameworks/` | Receives from | Prioritization scores determine which items make Now / Next / Later |
| `execution/dependency-map/` | Pairs with | Internal-variant dependencies are sourced from the dependency map |
| `execution/status-update-generator/` | Feeds into | Weekly status updates reference roadmap variant deltas |
| `../senior-pm/` | Feeds into | Portfolio roll-ups aggregate executive variants across teams |
| `marketing/` (skills domain) | Hands off to | Customer variant feeds product marketing content calendars and launch comms |

## References

- `references/roadmap-communication-guide.md` -- Now/Next/Later origin, "right-size the roadmap" (Cagan), outcome vs feature roadmaps, and worked examples of all three variants for the same project
- `assets/executive_roadmap_template.md` -- Fill-in template for the executive variant
- `assets/customer_roadmap_template.md` -- Fill-in template for the customer variant
- `assets/internal_roadmap_template.md` -- Fill-in template for the internal variant
