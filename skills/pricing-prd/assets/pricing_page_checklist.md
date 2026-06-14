# Pricing Page Review Checklist

Run this checklist before any pricing-page launch. Items are grouped by section of the page.

## Above the fold

- [ ] **Headline value proposition** above the tiers. One sentence; what the product does.
- [ ] **Sub-headline** addressing the primary objection ("no credit card required", "cancel anytime", etc.)
- [ ] **Monthly / annual toggle** visible (if both options exist), with annual discount called out.
- [ ] **Currency toggle** (if multi-region), with default based on geo-IP.
- [ ] **Tax inclusion** disclosure visible ("Prices exclude tax" or "Prices include VAT").

## Tier presentation

- [ ] **3-4 tiers maximum** on the primary view. Hide additional SKUs behind "More options" or "Contact sales".
- [ ] **Most-popular tier** visually highlighted (border, color, "Most popular" badge).
- [ ] **Tier names** are descriptive, not arbitrary (avoid "Plan A / B / C").
- [ ] **Headline price** per tier is large, secondary attributes (per month, billed annually) are subordinated.
- [ ] **Per-tier value carrier** stated in 1-2 lines below the price.
- [ ] **Per-tier CTA** with verb-led copy ("Start free trial", "Get started", "Contact sales"). Avoid "Sign up".
- [ ] **CTA color** consistent within tier-importance hierarchy (the "most popular" tier has the primary CTA color).

## Feature comparison

- [ ] **Comparison table** below the tier cards.
- [ ] **Top 8-12 differentiating features** listed; longer lists hidden behind "See all features".
- [ ] **Limits stated explicitly** (e.g. "10,000 events/month", not "Unlimited*").
- [ ] **Asterisks and footnotes minimized.** Each footnote is a trust cost.
- [ ] **Tooltips on hover/click** for features that need explanation.
- [ ] **No "starting at" pricing** unless the variable cost driver is clearly stated.

## Trust signals

- [ ] **Customer logos** (with permission) — 5-8 logos, balanced segment representation.
- [ ] **Testimonial or quote** with attribution (name, role, company).
- [ ] **Security / compliance badges** (SOC 2, ISO 27001, GDPR, HIPAA) if applicable.
- [ ] **Money-back guarantee** stated clearly if offered.
- [ ] **Uptime / reliability data** if relevant ("99.99% uptime SLA").

## FAQ

- [ ] **Top 5 objections** addressed (cancellation, refund, taxes, limits, security).
- [ ] **Plain language**, no marketing jargon.
- [ ] **Linked from each tier** at the most-confusing concept.
- [ ] **Pricing change history** mentioned if recent (acknowledge that pricing changed).

## Enterprise / custom path

- [ ] **"Contact sales" tier** or button is visually distinct from self-serve tiers.
- [ ] **What enterprise gets** is summarized (3-5 differentiators).
- [ ] **Contact form** is short (under 5 fields) — name, work email, company size, use case.
- [ ] **Response SLA** stated ("We'll get back to you within 1 business day").

## Compliance and legal

- [ ] **Terms of service link** in the page footer.
- [ ] **Auto-renewal disclosure** visible (required in EU, California).
- [ ] **CCPA "Do Not Sell"** link if applicable.
- [ ] **Subscription length** stated for each tier.
- [ ] **Cancellation policy** stated and accessible.
- [ ] **Refund policy** stated and accessible.

## Mobile

- [ ] **Tier cards stack** on mobile, not horizontal scroll.
- [ ] **CTA buttons** are tappable (>44pt height).
- [ ] **Comparison table** is mobile-friendly (collapsed by default, expandable).
- [ ] **Monthly/annual toggle** is reachable.

## Accessibility

- [ ] **Color is not the only signal** (use icons or labels for "Most popular", limits, etc.).
- [ ] **Color contrast** meets WCAG AA on price text and CTA buttons.
- [ ] **Heading hierarchy** (h1, h2, h3) is meaningful.
- [ ] **Form fields** have labels (not placeholder-only).
- [ ] **Tooltips** are keyboard-accessible.

## Performance

- [ ] **LCP under 2.5s** on mid-tier mobile.
- [ ] **No render-blocking marketing scripts** above the fold.
- [ ] **Images optimized** (WebP/AVIF, lazy-loaded).

## Analytics

- [ ] **CTA clicks tracked** per tier.
- [ ] **Comparison-table expansions tracked**.
- [ ] **FAQ section interactions tracked**.
- [ ] **Currency / monthly-annual toggles tracked**.
- [ ] **Scroll depth tracked** to identify where customers drop off.
- [ ] **Funnel from pricing page to trial-start tracked** with attribution.

## A/B test instrumentation

- [ ] **Variant assignment** flows to analytics.
- [ ] **Variant assignment** is consistent for the same visitor across sessions (cookie-based).
- [ ] **Sample ratio mismatch (SRM)** check is automated.

## Pre-launch QA

- [ ] **All CTAs tested** end-to-end (click → sign-up → first-paid step).
- [ ] **Currency conversion verified** for each region.
- [ ] **Tax calculation verified** for each region.
- [ ] **Payment methods verified** by geo (card, ACH, SEPA, etc.).
- [ ] **Edge cases checked** (annual tier with monthly toggle, enterprise contact-sales flow).
- [ ] **Sales team has reviewed** the page and signed off.
- [ ] **Support team has reviewed** the FAQ and signed off.
- [ ] **Finance has approved** the prices and tax handling.
- [ ] **Legal has approved** the disclosures, terms, and pricing experiment design.

## Post-launch monitoring (first 14 days)

- [ ] **Conversion-rate dashboard** monitored daily.
- [ ] **Support ticket volume** monitored daily.
- [ ] **Social mentions** monitored daily.
- [ ] **Sales call notes** monitored for objections.
- [ ] **Bug reports** routed to engineering.
