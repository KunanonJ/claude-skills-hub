# Red Flags: Productboard Expert

> Common ways this skill's output goes wrong -- concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan every Productboard configuration, Insight triage, Driver scoring, or roadmap published from Productboard before relying on it for prioritization. Each red flag has bad and good quoted examples.

---

## Red Flag 1: Insights Without Sources

**Symptom.** Insights inbox is full of items typed in by sales reps with no link to the source (call recording, email, Slack thread, customer interview).
**Why it's bad.** Insights without sources cannot be verified. The original signal (a customer saying X in context Y) is lost; you have a paraphrase. Downstream prioritization scores get gamed because the same paraphrased insight is recorded multiple times by different team members.
**Bad example:**
> "Insight: 'Customer wants bulk-edit.' Source: 'Discussed in a sales call.'"
**Good example:**
> "Insight: 'Customer wants bulk-edit for candidate records (specifically: bulk-tag, bulk-status-change).' Source: Gong call recording link + 02:14-04:30 timestamp. Customer: AcmeCorp. ARR: $87k. Champion: <name>. Note links to interview-synthesis output."
**How to catch it.** Insight with no link to recording / transcript / email = reject from inbox.

---

## Red Flag 2: Driver Score Gaming

**Symptom.** Sales reps inflate the 'Customer Score' on insights tied to deals they want closed.
**Why it's bad.** Driver scoring in Productboard derives feature value from aggregated insights. Inflation by interested parties corrupts the rank -- features get prioritized because someone wants commission, not because they move the metric.
**Bad example:**
> "Insight 'SAML' attached to 14 deals. Sales rep set the Customer Score to 10/10 on all 14 -- including 8 deals where the customer mentioned SAML only as a nice-to-have."
**Good example:**
> "Customer Score requires evidence: a quoted line from the source + (for scores 8-10) a written confirmation from the customer that this is a deal-breaker, not a nice-to-have. Sales-ops audits the top-scored insights quarterly. Repeat inflation triggers a calibration session."
**How to catch it.** Same insight tagged 'deal-breaker' across 10+ deals by the same rep = audit.

---

## Red Flag 3: Features Listed Without an Owner

**Symptom.** Features in Productboard have no Owner, no Status, no last update.
**Why it's bad.** Productboard is supposed to be the master of feature-state. Without owners, no PM is accountable for moving a feature through Discovery -> Planned -> In Progress. Sales sees stale "Considering" features and over-promises.
**Bad example:**
> "Feature 'Bulk Edit Candidates' in Productboard: Owner = empty. Status = empty. Last update = empty."
**Good example:**
> "Every feature has: Owner (a PM), Status (Considering / Planning / In Progress / Launched / Won't Do), Target Release (quarter), Last Update (auto, weekly script). A daily report lists features without Owner or with stale Last Update; PMs reconcile."
**How to catch it.** Any feature in Considering / Planning / In Progress with no Owner = assign.

---

## Red Flag 4: Roadmap Published From Productboard With Dates

**Symptom.** Public roadmap from Productboard shows "Bulk-edit: Q2 2026 (May)" -- treated by sales / customers as a commitment.
**Why it's bad.** Productboard's roadmap views can be exposed externally, but Now / Next / Later is the right granularity for customer-facing artifacts. Specific months read as commitments and trigger the "dates promised as commitments" anti-pattern (see `roadmap-communication/references/red-flags.md` Red Flag 2).
**Bad example:**
> "Public roadmap from Productboard: 'Bulk-edit -- May 2026. SCIM -- June 2026. SAML -- August 2026.'"
**Good example:**
> "Public roadmap from Productboard uses Now / Next / Later buckets only. Specific dates are visible only in internal views (Productboard supports both)."
**How to catch it.** Any customer-facing Productboard view with calendar dates = switch view to Now/Next/Later.

---

## Red Flag 5: Component Hierarchy Used as a Free-Form Taxonomy

**Symptom.** Productboard has 280 components, half of them duplicates ('Bulk Edit', 'Bulk Editing', 'Mass Edit'). Hierarchy is 6 levels deep.
**Why it's bad.** Component hierarchy is a navigation aid. Bloat makes it useless -- features get filed under the wrong component, search returns inconsistent results, and the org loses sight of the product's actual structure.
**Bad example:**
> "Components: Candidates / Recruiters / Admin / Reporting / Reporting v2 / Old Reporting / Bulk Edit / Bulk Editing / Mass Edit ..."
**Good example:**
> "Component hierarchy is 2-3 levels deep, mirrored against the product's information architecture. Components are reviewed quarterly; merges happen via a designated component-owner. New components require a documented use case."
**How to catch it.** Component count > 60 or hierarchy > 4 levels deep = consolidate.

---

## Red Flag 6: Productboard Out of Sync with Jira / Linear

**Symptom.** Feature in Productboard marked 'In Progress'; the linked Jira epic was closed 6 weeks ago.
**Why it's bad.** Productboard is a customer-facing artifact for some users. Sync drift means the org publishes false status -- sales sees "In Progress" and promises a quarter, customer-success sees "Launched" and tells customers, and neither matches the engineering reality.
**Bad example:**
> "Feature 'Bulk Edit' in Productboard: In Progress. Jira epic PROJ-4400: Closed (status: Done) on 2026-04-10."
**Good example:**
> "Daily sync script reconciles Productboard feature status with linked Jira / Linear epic status. Mismatches surface to the PM-of-record within 1 business day. Documented in `references/sync-patterns.md`."
**How to catch it.** Any Productboard feature with linked Jira epic in a different state = run sync script.

---

## Red Flag 7: Customer Score Without Segmentation

**Symptom.** Insights from a free-tier user and from an enterprise customer count equally toward feature priority.
**Why it's bad.** Different customer segments have different economics. Treating them as equal in scoring means low-ARR voices dominate (because there are more of them), and the product drifts away from the strategic segment.
**Bad example:**
> "Driver: 'Add free-tier voice export' has 240 supporting insights; 'Add SCIM' has 18 supporting insights. Free-tier wins -- but the strategy is enterprise."
**Good example:**
> "Customer Score is weighted by ARR-band or strategic-segment. 240 free-tier insights at weight 0.2 = 48 weighted points. 18 enterprise insights at weight 5 = 90 weighted points. Segment + weighting documented in `prioritization-charter.md`."
**How to catch it.** Driver rankings flip when you re-score weighted by ARR = current scoring is segment-blind.

---

## Red Flag 8: 'Won't Do' as a Forgotten Bucket

**Symptom.** Features filed under "Won't Do" 18 months ago are never communicated back to the customers who asked.
**Why it's bad.** Customers who submitted feedback expect a closed loop. Silently dropping requests damages trust. Worse, the same request keeps coming back because nobody knows it was already declined.
**Bad example:**
> "'Won't Do' bucket: 340 features. None of the requesting customers were ever notified."
**Good example:**
> "When a feature moves to 'Won't Do', a Productboard automation triggers: (1) requesting customers receive a personalized note with reasoning + alternatives; (2) the feature stays visible in a 'Considered and not building' filter for transparency; (3) reasoning logged for next-time-it-comes-up."
**How to catch it.** Items in 'Won't Do' for > 6 months with no requester-notification log = run the close-the-loop process.

---

## Red Flag 9: Insights Aged Beyond Reality

**Symptom.** A feature has 80 supporting insights, but 60 of them are > 2 years old.
**Why it's bad.** Customer needs evolve. Treating 2-year-old insights as equivalent to current ones means the product is prioritizing for problems that may no longer exist. Worse, the team has confidence that "customers really want this" when really, customers really wanted this in 2024.
**Bad example:**
> "Feature 'Live activity feed' has 80 insights; 62 are 2020-2023. Scoring treats them equally."
**Good example:**
> "Insight scoring decays with age (e.g. half-weight after 12 months, quarter-weight after 24). Stale insights either get re-validated (mark current) or expire. Decay curve configurable per product."
**How to catch it.** Top features by insight count, segmented by age: if > 60% of supporting insights are > 18 months old, validate before prioritizing.

---

## Red Flag 10: PM as Sole Triager

**Symptom.** Every insight in the inbox must be triaged by one PM, who has 600 pending.
**Why it's bad.** A bottlenecked inbox is a useless inbox. Sales / Success / Support stop submitting because nothing happens. The signal dies.
**Bad example:**
> "Inbox: 612 untriaged insights. Single PM owner. Average time to triage: 47 days."
**Good example:**
> "Triage is shared: each PM owns the inbox for their product area. Sales / Success / Support get auto-acknowledged within 24h, with the assigned PM and target triage date. Weekly triage ritual: each PM clears their area; org-wide health metric (inbox age) tracked."
**How to catch it.** Insight inbox age (oldest untriaged) > 14 days = staff differently.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Insights without sources | Every insight has a link to recording / transcript |
| 2 | Customer Score gaming | Top-scored insights audited for inflation |
| 3 | Features without owners | All In Progress features have Owner + Last Update |
| 4 | Roadmap with dates | Public view uses Now / Next / Later |
| 5 | Component sprawl | < 60 components, hierarchy <= 3 levels |
| 6 | Out of sync with Jira | Daily reconciliation script |
| 7 | Customer Score unsegmented | ARR-band weighting in scoring |
| 8 | 'Won't Do' as forgotten bucket | Close-the-loop notifications |
| 9 | Insights aged out | Age-decay in scoring |
| 10 | PM as sole triager | Inbox age oldest < 14 days |

## Related Reading

- `SKILL.md` -- Productboard administration + REST API patterns
- `references/insight-triage-playbook.md` -- the triage workflow
- `references/driver-scoring.md` -- the scoring model
- `references/sync-patterns.md` -- Jira / Linear bidirectional sync
- Sibling skill: `execution/customer-feedback-triage/` -- the inbox triage workflow
- Sibling skill: `execution/prioritization-frameworks/` -- the scoring methods
- Sibling skill: `execution/roadmap-communication/` -- audience patterns for Productboard roadmap views
