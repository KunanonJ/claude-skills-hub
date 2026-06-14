# PR/FAQ: [Product Name]

**Date drafted:** [YYYY-MM-DD]
**Future launch date:** [YYYY-MM-DD]
**Author(s):** [PM name, exec sponsor]
**Status:** [Draft / In review / Approved / Archived]
**Version:** [0.1]

---

## Part 1: Press Release

**Headline:** [Single declarative sentence a journalist would write. No internal codenames. No "next-generation."]

**Sub-headline:** [One sentence naming the specific customer and the specific benefit.]

---

**[City], [Future Date]** -- [Company] today announced [product/feature], a [brief description] for [specific customer segment]. [What it does in one sentence.] [Why it matters in one sentence.]

[**Problem paragraph.** Describe the customer pain in the customer's own words. Include a specific example or a quantified pain point. Avoid "customers struggle with..." Name the struggle concretely.]

[**Solution paragraph.** Plain language only. Walk through what the customer experiences. No architecture words.]

"[Leader quote -- one or two sentences from an internal exec. Why this matters for the company. Measured language.]" said [Name], [Title] at [Company].

[**How it works paragraph.** 3-4 sentences walking through the experience. Show the path, not the architecture. No screenshots, no API names.]

"[Customer quote -- made-up but credible. Must describe a measurable outcome, not a feature. Use language an actual customer would use. Avoid superlatives.]" said [Customer name], [Customer title] at [Customer company].

[**Availability paragraph.** Pricing model (free, freemium, tier), launch geography, and how to get started. 1-2 sentences.]

For more information, visit [URL].

---

## Part 2: Internal FAQ

> Audience: exec sponsor, finance, legal, eng leadership. Answer 10-20 questions across all 9 categories below.

### Customer & demand

**Q: What is the customer problem in one sentence, and how many customers experience it?**

A: [1-3 paragraphs. Cite research interview count or data source. Quantify the addressable population.]

**Q: What is our evidence that customers will pay for this, not just use it?**

A: [Cite willingness-to-pay research, comparable pricing, or pre-sales evidence. If unknown, name the experiment that will tell us.]

### Business model

**Q: What is the v1 budget and the 3-year P&L projection?**

A: [Engineering FTEs, design FTEs, infra cost, expected revenue ramp. Cite the finance model.]

**Q: What is the CAC payback assumption and how was it derived?**

A: [Plain-language unit economics. State the assumption set explicitly.]

### Strategic fit

**Q: Why us? Why now? Why not in 2 years?**

A: [What unique capability, asset, or moment makes this the right initiative for our company at this time.]

**Q: How does this compound with the rest of the portfolio?**

A: [Does it enable existing products? Defend a flank? Open a new segment? Be specific.]

### Competition

**Q: Who else is solving this? Why will we win?**

A: [Name 2-4 specific competitors. Describe their approach honestly. Name our differentiator concretely.]

### Technical feasibility

**Q: What is the single biggest technical risk, and what is our plan to retire it?**

A: [Name the riskiest assumption. Describe the spike, prototype, or proof of concept that will resolve it before scale-up.]

### Operational

**Q: Who supports this product 24/7 after launch?**

A: [Name the team. Describe the runbook. State whether new on-call coverage is required.]

### Legal, privacy, compliance

**Q: What data do we collect? In what jurisdictions? Under what consent?**

A: [Inventory the data flows. Name applicable regulations (GDPR, CCPA, HIPAA, sector-specific). Note any new contracts (DPA, BAA) required.]

### Risk & failure modes

**Q: What is the worst-case scenario, and what is our exit criterion?**

A: [Name the failure mode. State the metric and threshold that would trigger a kill decision.]

**Q: What would we have to believe for this to be true?**

A: [List the 3-5 critical assumptions. Cross-reference to the validation plan.]

### Scope & alternative

**Q: What are we explicitly NOT doing in v1?**

A: [Enumerated list of deferred scope. Each item briefly justified.]

**Q: What is the cheapest alternative we considered, and why was it rejected?**

A: [Build-vs-buy. Build-vs-partner. Smaller version. Cite the cost and the rejection rationale.]

---

## Part 3: External FAQ

> Audience: customers, partners, support reps. Each answer 1-3 sentences. Longer answers belong in the help center.

**Q: What is it?**

A: [One-sentence positioning.]

**Q: Who is it for?**

A: [Named persona and use case.]

**Q: How is it different from [obvious alternative]?**

A: [Honest comparison. One or two sharp differentiators.]

**Q: How much does it cost?**

A: [Pricing tier or model. If TBD, state "available at launch."]

**Q: How do I get started?**

A: [Concrete first 60 seconds. URL or in-product entry point.]

**Q: Does it integrate with [top 2-3 likely integrations]?**

A: [Yes/No/Roadmapped. Be specific.]

**Q: Is my data private? Where is it stored?**

A: [Plain-language privacy stance. Region of storage. Encryption posture.]

**Q: What languages and regions are supported at launch?**

A: [List.]

**Q: What if I do not have [common prerequisite]?**

A: [Onboarding fallback or honest limitation.]

**Q: Can I cancel? What is the refund policy?**

A: [Plain-language terms.]

---

## Review log

| Date | Reviewer | Lens | Top concern | Resolution |
|------|----------|------|-------------|------------|
| [YYYY-MM-DD] | [Name] | Exec sponsor | [Concern] | [How addressed] |
| [YYYY-MM-DD] | [Name] | Engineer (external to team) | [Concern] | [How addressed] |
| [YYYY-MM-DD] | [Name] | Designer | [Concern] | [How addressed] |
| [YYYY-MM-DD] | [Name] | Customer-facing rep | [Concern] | [How addressed] |
| [YYYY-MM-DD] | [Name] | External advisor | [Concern] | [How addressed] |

---

## Approval

- [ ] Press Release Test passed with 3+ independent readers
- [ ] All 9 internal-FAQ categories answered
- [ ] Every quantitative claim cites a source
- [ ] Customer quote describes an outcome (not a feature)
- [ ] "What we are NOT doing in v1" answered explicitly
- [ ] Exec sponsor sign-off recorded below

**Exec sponsor:** [Name]
**Sign-off date:** [YYYY-MM-DD]
**Next milestone:** [PRD draft / kickoff / next review]
