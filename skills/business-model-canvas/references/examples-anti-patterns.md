# BMC — Examples & Anti-Patterns

## Example 1 — SaaS HR analytics tool (good canvas)

| Block | Content |
|-------|---------|
| Segments | Mid-market HR teams (200-2000 employees) — initial. Enterprise HR (later) |
| Value Props | "Cut HR reporting time 60%; reduce error rate 80%; one-click compliance reports" |
| Channels | Web direct + inbound + outbound SDR + partner referrals from HRIS vendors |
| Relationships | Self-service onboarding + dedicated CSM at $20K ARR+ |
| Revenue | Per-employee subscription ($X/EE/mo, tiered: starter/pro/enterprise) |
| Key Resources | Engineering team + customer dataset + integrations (Workday/BambooHR/etc) |
| Key Activities | Product development + integration maintenance + customer success |
| Key Partnerships | HRIS vendors (data integration + co-marketing) + payroll providers |
| Cost Structure | People-heavy (eng/sales/CS) + cloud infra + integration maintenance |

**Why it's strong:**
- Specific segment (size band)
- VP with measurable claims
- Channel diversity matches segment
- Pricing dimension (per-EE) matches value (HR insights = function of headcount)
- Partnerships specified by role

## Example 2 — Same idea, weak canvas

| Block | Content |
|-------|---------|
| Segments | "Businesses that want better HR" |
| Value Props | "AI-powered, easy to use, best-in-class HR analytics" |
| Channels | "Online" |
| Relationships | "Great customer service" |
| Revenue | "Subscription" |
| Key Resources | "Our team and AI" |
| Key Activities | "Build the product, sell to customers" |
| Key Partnerships | "TBD" |
| Cost Structure | "Salaries, marketing, infrastructure" |

**Why it's weak:** every block could describe any HR tech company.

## Example 3 — Multi-sided platform (consumer marketplace)

| Block | Content |
|-------|---------|
| Segments | Buyers: urban millennials seeking pre-owned designer goods. Sellers: fashion-conscious individuals with $50K+ wardrobes to monetize |
| Value Props | Buyers: authentic luxury at 40-70% off + return guarantee. Sellers: trusted resale platform with 70% take rate, white-glove pickup |
| Channels | Buyers: Instagram + paid social + influencer + SEO. Sellers: PR + buyer-to-seller conversion + influencer |
| Relationships | Buyers: self-service + concierge for $5K+ orders. Sellers: white-glove for top 1% of consigners |
| Revenue | Commission on sale (30% of GMV); express listing fee + premium placement |
| Key Resources | Authentication ops + photography studio + buyer database + brand |
| Key Activities | Authentication + photography + matching + dispute resolution + trust&safety |
| Key Partnerships | Brand authenticators + luxury logistics + payment processors |
| Cost Structure | Authentication labor + logistics + tech + marketing + chargebacks |

**Why it works:** 2 segments with distinct value props; channels tailored per side; relationships scaled by value; revenue model matches platform mechanic.

## 12 common anti-patterns

### A1 — The "everyone" segment
> Segments: "all businesses needing better project management"

Treats every prospect identically; can't tailor channels, pricing, or VP.

**Fix:** Pick one beachhead segment. Add segments after success.

### A2 — Feature list disguised as value prop
> Value Props: "AI summarization, real-time collaboration, mobile app, API access"

Lists what you built; not why anyone cares.

**Fix:** State the outcome. "Cuts meeting prep time 70% for product managers."

### A3 — Channel = "online"
> Channels: "Online, social media, content marketing"

Generic. Doesn't say which phase or which segment.

**Fix:** Map channels to (segment × awareness/evaluation/purchase/delivery/after-sales).

### A4 — Relationship = "great service"
> Customer Relationships: "We provide excellent customer service"

Aspirational. Says nothing about model.

**Fix:** Specify per segment: self-service, named CSM, community, etc.

### A5 — Revenue = "we'll figure it out"
> Revenue Streams: "Subscription, maybe usage-based"

Ambiguous. Suggests pricing not decided.

**Fix:** Pick a primary stream + mechanism. Iterate later, don't punt.

### A6 — Resources = "our amazing team"
> Key Resources: "Talented team, cutting-edge tech"

Generic and unverifiable.

**Fix:** Name the truly differentiating resources. "Proprietary dataset of X. Senior engineers with 5+ years in Y."

### A7 — Activities = everything
> Key Activities: "Product development, sales, marketing, customer service, operations, finance"

Lists everything = lists nothing.

**Fix:** Pick the 3-5 most-important.

### A8 — Partnerships = "TBD"
> Key Partnerships: "Strategic partnerships TBD"

Either you have partners (and they matter) or you don't. Don't punt.

**Fix:** If model truly doesn't depend on partners, write "None at this stage."

### A9 — Cost structure as wishful thinking
> Cost Structure: "Lean, mostly cloud + people"

Doesn't match scale; doesn't reflect what costs really are at the model's intended size.

**Fix:** Break out top 5 cost lines at target scale. Verify revenue covers.

### A10 — Unbundled-looking canvas hiding 3 businesses
A single canvas describing what's actually 3 different segments with different products.

**Fix:** Draw 3 separate canvases. If they share resources but have different VPs, that's an unbundled model.

### A11 — VP doesn't match cost structure
> VP: "white-glove premium service"
> Cost: "we'll keep costs lean"

Premium VP + lean cost = mediocre delivery.

**Fix:** Match orientation (cost-driven vs value-driven). Pick one consciously.

### A12 — No coherent customer journey
The blocks individually look fine, but you can't trace a customer from Segment through Channel through Relationship through Revenue.

**Fix:** Walk one customer. If you can't trace them, the model has a gap.

## Validation checklist

Before considering a BMC done:

- [ ] Each segment is specific enough to recognize
- [ ] Each segment has a distinct VP
- [ ] Each VP states outcomes, not features
- [ ] Each channel maps to a segment + phase
- [ ] Each relationship pattern matches the segment economics
- [ ] Revenue streams + pricing mechanism are explicit
- [ ] Key resources include something differentiating
- [ ] Key activities are the top 3-5 (not all things)
- [ ] Partnerships specify give + get for each
- [ ] Costs sum approximately to revenue at target scale
- [ ] The whole model can be summarized in 1 sentence per block
- [ ] Riskiest 3 assumptions are identified for testing
