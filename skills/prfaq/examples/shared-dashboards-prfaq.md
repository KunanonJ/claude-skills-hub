# Example: PR/FAQ for Acme Analytics Shared Dashboards

> Real-world scenario showing how to write a Working Backwards PR/FAQ end-to-end.

## Context

Acme Analytics is preparing to fund the build of "Shared Dashboards" -- a feature letting customers share read-only dashboards with their own clients during QBRs. The investment is significant (1 squad, 6 weeks, marketing investment for conference launch). The CPO (Hana Aoki) wants a PR/FAQ before approving the spend, to stress-test whether the customer story is real and whether the team has thought through the hard internal questions.

The PM (Devi Rao) writes a draft and circulates to the exec sponsor, the head of engineering, the CFO, and Legal. The PR/FAQ will then either fund the work or kill the idea.

## Inputs

- Customer interviews (n=11) and sales-call notes (4 mentions)
- Concierge MVP results (8/10 generated >= 3 share links)
- Pre-mortem from `discovery/pre-mortem/`
- Estimated v1 build cost: $220k loaded
- Projected ARR contribution by Q4 2026: $1.2M (CSM-attributed expansion)

## Applying the skill

1. **Wrote the press release first** -- 1 page max, customer-language only, no buzzwords. Future-dated 2026-07-14.
2. **Ran the Press Release Test** by handing the draft to a CSM (not on the team). She answered "head of analytics at a mid-market company"; "share live dashboards with their clients without buying them seats"; and "yes" to clicking Learn More.
3. **Drafted the Internal FAQ** with 14 Q&A pairs, covering every category (customer, business model, strategic fit, competition, feasibility, operations, legal/privacy, risk, scope).
4. **Drafted the External FAQ** with 8 Q&A pairs in customer voice.
5. **Stress-tested the leader quote** -- rewrote twice. Final version is a measured CEO statement, not a hype quote.
6. **Locked the document** for the CPO funding review.

Key decision quoted: *"We do not write 'next-generation' or 'revolutionary'. Every word a customer would not actually use comes out."*

## The artifact

````markdown
# PR/FAQ: Acme Shared Dashboards

**Status:** Final for funding review
**Author:** Devi Rao (PM Growth)
**Reviewers:** C. Bell (VP Product, sponsor), N. Okafor (EM), J. Tran (CFO), M. Hughes (Legal)
**Date:** 2026-05-22 (future-dated press release: 2026-07-14)

---

## Part 1: Press Release

**FOR IMMEDIATE RELEASE -- July 14, 2026**

### Acme Analytics now lets customers share live dashboards with their clients in 30 seconds

San Francisco, CA -- July 14, 2026 -- Acme Analytics today launched **Shared Dashboards**, a new capability that lets customers share read-only versions of any dashboard with stakeholders outside their workspace -- in under 30 seconds, without buying additional seats and without exporting to PDF.

Before Shared Dashboards, Acme customers who wanted to show analytics to their own clients had three bad options: screenshot the dashboard (which goes stale within hours), export a PDF (which loses interactivity), or grant a guest seat (which requires procurement approval and adds cost). Heads of analytics at mid-market companies reported spending an average of 45 minutes per quarterly business review rebuilding slide decks the night before.

With Shared Dashboards, customers click Share, set an expiry date and optional password, and send a single link. Recipients see the live, interactive dashboard branded with the customer's company name. The customer sees who has viewed and when, and can revoke access at any time. The dashboard stays current automatically.

"Our customers told us they didn't want to lose interactivity to share data with their clients, and they didn't want to make their clients log into another tool," said Catherine Bell, VP Product at Acme Analytics. "Shared Dashboards solves both at once: a link, no seat, live data."

To create a Shared Dashboard, a customer opens any dashboard, clicks Share, picks an expiry (30, 60, or 90 days), optionally adds a password, and copies the link. Sharing is included with Pro and Enterprise tiers; the limit is 50 active share links per workspace.

"Before this, we spent half a day per QBR rebuilding slides. Now we send a link and our client sees the numbers as they update. It changed how we run reviews," said Maya Chen, Head of Analytics at Northwind SaaS.

Shared Dashboards is available today at acme.com/shared-dashboards for all Pro and Enterprise customers. Free-tier customers can preview the feature with a 14-day trial.

---

## Part 2: Internal FAQ

### Customer & demand

**Q1: What is the customer problem in one sentence, and how many customers experience it?**

A: Customers who use Acme for internal reporting cannot share live dashboards with stakeholders outside their workspace without paying for additional seats or exporting to lossy formats. From CSM logs and interview research, this affects 1,180 mid-market workspaces (35% of paying base). 9 of 11 interviewed customers described it as their #1 friction with Acme.

**Q2: What is our evidence that customers will use this, not just say they want it?**

A: We ran a concierge MVP in March 2026: manually generated share links for 10 mid-market customers and tracked usage over 4 weeks. 8 of 10 generated >= 3 share links each (target was 6 of 10). 6 of those 8 reported share recipients viewing >= 3 times. Independent evidence: 4 deals stalled in Q1 over "no native share" feedback, totaling $480k ARR; competitor (Looker, Mode, Tableau) all ship share-link features.

### Business model

**Q3: How does this make money?**

A: Two ways. (1) Conversion -- this is currently a deal-loss reason in 4-of-quarter mid-market deals; closing those is worth ~$2M ARR/year. (2) Expansion -- Pro tier expansion from Starter is constrained today by no compelling Pro-only feature; Shared Dashboards is Pro-and-above. CSM forecast: 35% of Pro expansions in next two quarters will be attributable. v1 budget: $220k loaded; payback estimate: 2 quarters.

**Q4: What is the 3-year P&L projection?**

A: Year 1 ARR contribution: ~$1.2M (deal-closure + expansion). Year 2: ~$2.8M (compounding + reduced churn). Year 3: ~$3.5M (plateau, but feature is now a moat against competitive losses). Infrastructure cost of running Shared Dashboards at projected volume: ~$70k/year (CDN + read-replica + audit log storage). Net: positive in Year 1.

**Q5: Is there a build-vs-buy alternative? Did we evaluate at least two third-party options?**

A: Two options evaluated. (1) Reembed via iframe in customer-built portals -- already supported, but requires the customer to build a portal, which our segment will not do. (2) Acquire Looker-style embedded analytics -- considered, but cost + integration overhead is 5-10x building this natively. We chose build.

### Strategic fit

**Q6: Why us and why now?**

A: Why us: we own the data; sharing is a natural extension of our existing analytics product. Why now: every direct competitor (Looker, Mode, Tableau) shipped a share feature in Q1 2026. We are 1-2 quarters behind. The strategic cost of waiting another quarter is more deal losses we can attribute to this gap.

**Q7: How does this connect to our North Star Metric?**

A: Direct contributor. Our NSM is Weekly Active Workspaces with External Stakeholder Engagement (WAWSE). Shared Dashboards moves Input #2 (workspaces sharing externally) directly. The whole NSM was redefined around the stakeholder-facing strategy that this feature embodies.

### Competition

**Q8: Who else is solving this and why will we win?**

A: Looker Studio (Google) -- ships share links but lacks brand customization. Tableau Cloud -- ships share but is enterprise-heavy and not aimed at our segment. Mode -- shipped a share-link feature in Q1 2026 but with a 7-day expiry maximum that customers complain about. Our differentiation: 90-day expiry, brand customization, audit log, native to our existing dashboards (no separate "share product").

### Technical feasibility

**Q9: Can we build this in 6 weeks? What's the riskiest technical bet?**

A: Yes. Engineering Lead has signed off on scope. Riskiest bet: the auth-less recipient view (we are exposing dashboard renders without an Acme login). Mitigation: signed short-lived tokens + per-link revocation + audit log + IP-based rate limiting + EU regional domain for EU tenants.

### Operational

**Q10: Who supports this and what happens when it breaks?**

A: Support owns customer-facing tickets; existing on-call rotation absorbs operational pages. Adds ~5 tickets/week at projected volume. Status page and runbook are in scope.

### Legal & privacy

**Q11: Is there a GDPR concern? What about HIPAA, COPPA, FINRA?**

A: GDPR: yes -- a share link allows EU customer data to be viewed by EU stakeholders. Mitigated by region-aware share-link domain (`share.eu.acme.com` for EU tenants); no cross-region data movement. HIPAA: out of scope (Acme is not a HIPAA-covered product). COPPA: no (B2B product, no minors). FINRA: out of scope.

**Q12: What is the ToS update we need?**

A: A new clause covering external-recipient view of customer data. Legal has drafted; ready for July 7 review.

### Risk & failure modes

**Q13: What is the worst-case scenario?**

A: A share link is leaked publicly and exposes a customer's sensitive data (e.g., financial KPIs, customer PII embedded in the dashboard). Mitigations: (1) Audit log -- customer can see who viewed and revoke; (2) Default 30-day expiry; (3) Password option; (4) Field-level deny list for sensitive columns; (5) Banner warning at share creation if sensitive fields detected. Pre-mortem (`discovery/pre-mortem/`) classified this as Tiger; full mitigation list in PRD section 8.

**Q14: How would we know it failed?**

A: Three signals: (1) Adoption: <30% of Pro workspaces generate >=1 share link by end of Q3. (2) Outcome: recipient NPS < 15. (3) Quality: Sev1/2 security incident in first 90 days. Any one triggers a "what do we do" exec review.

### Scope & alternatives

**Q15: What are we explicitly NOT building in v1?**

A: PDF export (deferred to v1.1), white-label branding (deferred), custom share-link domain (deferred), live cursor presence on shared views (deferred to v1.1 after beta), editing rights on shared views (out of scope -- changes the security model), embedded share in third-party apps (use existing iframe embed, not this feature).

---

## Part 3: External FAQ

**What is Shared Dashboards?**

A feature that lets you share read-only versions of any Acme dashboard with people outside your workspace, via a secure link. No additional seats required, and the data stays live.

**Who needs an Acme account to view a Shared Dashboard?**

Nobody beyond your existing Acme workspace members. Recipients open the link and see the dashboard, optionally entering a password.

**How long does a share link work?**

By default, 30 days. You can set it to 60 or 90 days, or revoke it at any time. You can also see who has viewed the link and when.

**Can I password-protect a share link?**

Yes. Adding a password is optional at link creation.

**What can recipients do with a shared dashboard?**

View it interactively (drill into chart filters, scroll through table data). They cannot edit, comment, or export. The dashboard stays read-only at all times.

**What tier is this available on?**

Pro and Enterprise tiers. Each workspace can have up to 50 active share links; if you need more, your account manager can raise the ceiling.

**What happens to share links if I cancel my Acme subscription?**

Active share links are revoked at cancellation. Recipients will see a "this share is no longer available" message.

**Is Shared Dashboards available in the EU?**

Yes. EU customers' share links use a regional domain (`share.eu.acme.com`) and the data does not leave EU infrastructure. GDPR compliance is maintained.

**Will this be available in the mobile app?**

Recipients can view a shared dashboard on a mobile browser. We are evaluating share-link creation in the mobile app for a future release.
````

## Why this works

- The press release names the customer (head of analytics at a mid-market company), the problem (45 minutes per QBR rebuilding slides), and the solution (a link, no seat, live data) without buzzwords.
- The customer quote ("changed how we run reviews") is outcome-specific and measured -- not "this revolutionizes the industry".
- The Internal FAQ tackles the hardest questions explicitly (worst-case data leak, GDPR data flow, build-vs-buy alternatives, signal of failure). The CFO sees the unit economics; Legal sees the data-residency answer; engineering sees the riskiest technical bet.
- "What we are NOT building in v1" (Q15) is named explicitly -- the PR/FAQ doubles as the scope-creep defense at funding time.
- The Press Release Test was applied -- a non-team member identified the customer, the problem, and would click Learn More. The bar passed before the document was final.

## What's next

- Use [../create-prd/](../create-prd/) for the 8-section build artifact once funding is approved.
- Use [../beta-program/](../beta-program/) for the closed beta plan referenced in External FAQ Q9.
- Use [../launch-playbook/](../launch-playbook/) for the 2026-07-14 conference launch.
- Pair with [../../discovery/pre-mortem/](../../discovery/pre-mortem/) -- the Internal FAQ Q13 worst-case feeds the pre-mortem risk register.
- Use [../north-star-metric/](../north-star-metric/) -- Internal FAQ Q7 references the NSM directly.
