# Rollout Shape Comparison Guide

A side-by-side reference for the seven common rollout shapes, with use cases, risk profiles, and worked examples. Each shape implies a different gate-criteria pattern between stages.

## Quick comparison table

| Shape | Pattern | Risk profile | Time to GA (typical) | Best for |
|---|---|---|---|---|
| A. Linear ramp | 0 -> 1% -> 5% -> 25% -> 50% -> 100% | Low risk per step | 2-3 weeks | Most new features |
| B. Segmented | Internal -> Beta -> Free -> Paid | Risk varies by audience | 4-8 weeks | Features with explicit risk gradients |
| C. Geographic / regulatory | Region 1 -> Region cluster -> Global | Risk varies by region | 4-12 weeks | Features with regulatory / regional differences |
| D. A/B split with holdout | A 50% / B 45% / Holdout 5% | Risk per arm | 2-4 weeks (experiment) | A/B tests with long-term measurement |
| E. Dark launch (shadow) | 100% code, 0% UX | Performance / load risk only | 1 week | High-traffic system changes; AI features |
| F. Reverse ramp (sunset) | 100% -> 75% -> 25% -> 0% | Risk of customer churn | 4-26 weeks | Feature deprecation |
| G. Mobile forced-upgrade | Server enforces minimum client version | Risk of locking out users | 4-12 weeks | Mobile features requiring new client |

## Shape A: Linear ramp

### When to use

The default. Use for any new feature where you do not have strong segment-specific hypotheses and the surface is well-understood.

### Standard cadence

| Stage | % | Hold | Gate criteria |
|---|---|---|---|
| 1 | 1% | 24-48h | No error spike; p95 latency in band; no top-customer reports |
| 2 | 5% | 24-48h | Same |
| 3 | 10% | 24-48h | Same + adoption metric in band |
| 4 | 25% | 48-72h | Same + business KPI not regressed |
| 5 | 50% | 48-72h | Same |
| 6 | 100% | -- | Stable for 1-2 weeks; retire flag |

### Risk profile

- Smooth ramp; easy to roll back at any step.
- Gate criteria are mostly the same across steps; later steps add business-KPI checks.
- A 1% ramp catches outright bugs but rarely catches subtle behavioral issues -- those surface at 10-25%.

### Pitfalls

- Skipping steps under deadline pressure. Each step exists for a reason.
- Not waiting long enough for metrics to settle. New traffic can take 24+ hours to fully reflect in dashboards.
- Treating "no error spike" as the only gate. Behavioral metrics matter too.

## Shape B: Segmented (audience-first)

### When to use

Audiences have explicit risk gradients. Enterprise tenants run on stricter SLAs; consumer beta users tolerate more breakage.

### Example cadence

| Stage | Audience | Gate criteria |
|---|---|---|
| 1 | Internal employees | Used by 50+ employees for 1 week; no P0 |
| 2 | Friends-and-family invites | 200+ external users for 1 week; satisfaction >= 70% |
| 3 | Public beta opt-in | 1000+ users for 1-2 weeks; metric in band |
| 4 | Free tier | Full free-tier rollout; week of stable metrics |
| 5 | Pro tier | 1-2 weeks at 100% on free; no enterprise-impacting regression |
| 6 | Enterprise tier | All segments stable; account-level sign-off in place |

### Risk profile

- Higher tier customers have higher SLAs but you also reach them later -- this is intentional risk-shedding.
- Each segment is a different "blast radius" if something goes wrong.

### Pitfalls

- Going faster on segments that complain less. Free-tier users complain less but are still real users.
- Treating internal as "real testing." Employees are not customers; their workflow is not the customer's workflow.

## Shape C: Geographic / regulatory-aware

### When to use

Features have regulatory variance (EU AI Act tier-specific UX, GDPR consent flows, age-verification rules, region-specific payment methods).

### Example cadence

| Stage | Region | Gate criteria |
|---|---|---|
| 1 | One low-risk region (e.g., AU + NZ) | 1-2 weeks; no regulator inquiries |
| 2 | English-speaking cluster (US, UK, CA, AU, NZ) | 2-3 weeks; no escalations |
| 3 | EU (with GDPR + AI Act variants) | 2-4 weeks; legal review of consent flows |
| 4 | Asia (with regional adjustments) | Region-specific gates |
| 5 | Global, regulated regions | Last; explicit regulatory sign-off |

### Risk profile

- Earliest regions absorb the risk of new compliance flows.
- Legal/Compliance is on every gate.
- Region-specific UX variants live alongside the rollout flag; this can become complex quickly.

### Pitfalls

- Ignoring data-residency constraints (region 1 may not be allowed to process region 2 data).
- Underestimating regulatory review time -- often weeks, not days.

## Shape D: A/B split with holdout

### When to use

A/B experiments where the team wants to measure short-term lift (during the experiment) and long-term impact (weeks/months after launch).

### Example structure

| Arm | Allocation | Purpose |
|---|---|---|
| Control (A) | 47.5% | Existing behavior |
| Variant (B) | 47.5% | New behavior |
| Short-term holdout | 5% | Never exposed during experiment; baseline for long-term lift |
| (Optional) Long-term global holdout | 1-5% (separate) | Across all experiments; quarterly baseline |

### Gate criteria

- Pre-registered hypothesis and primary metric.
- Sample size calculated from minimum detectable effect.
- Experiment run window determined by sample size + traffic.
- Stat-sig threshold (often p < 0.05 with multi-testing correction).
- Counter-metrics monitored alongside primary.

### Risk profile

- Risk is bounded to the variant arm.
- Holdout protects against treatment-effect interactions during launch.
- Long-term holdout lets leadership attribute aggregate lift to the team's experiment portfolio.

### Pitfalls

- Peeking (looking at the experiment before completion) inflates false-positive rate.
- Killing the holdout to "ship faster." Reduces statistical confidence on long-term impact.
- Running too many experiments on the same surface simultaneously without orthogonal design.

## Shape E: Dark launch (shadow)

### When to use

- High-traffic system changes where you need to validate performance and error rate without user impact.
- AI features (per `ai-feature-prd/` Section 11.3) where the model output is mirrored, logged, and compared offline.
- Migrations where the new path must produce the same output as the old path.

### Example flow

```
Request hits the system.
|
+-- Old path runs; result returned to user.
|
+-- New path runs in parallel; result discarded (or logged for comparison).
|
+-- Compare logs offline; flag any divergence.
```

### Gate criteria

- New path's error rate within tolerance.
- New path's latency within tolerance.
- New path's output matches old path (where determinism is expected) or is acceptable (where it is not).
- No resource contention on the production path.

### Risk profile

- Lowest risk shape. User-visible behavior is unchanged.
- Cost is doubled for the duration of the shadow.

### Pitfalls

- Shadow runs forever. Set an exit criterion; do not let shadow become a permanent cost.
- Shadow load affects production. Throttle if necessary.
- Logging volume is enormous; sample if needed.

## Shape F: Reverse ramp (sunset)

### When to use

Retiring a feature. Customers need time to migrate; the team needs to validate they have.

### Example cadence

| Stage | Audience still exposed | Gate to next |
|---|---|---|
| 1 | 100% | Communication out; migration path live |
| 2 | 75% | Migration adoption > 30%; support team prepared |
| 3 | 50% | Migration adoption > 60%; no major-customer blockers |
| 4 | 25% | Migration adoption > 85%; escalations resolved |
| 5 | 10% | Migration adoption > 95%; remaining users identified |
| 6 | 0% | Feature removed; final EOL communication |

### Gate criteria

- Customer-facing communication ahead of each step (see `eol-communication/`).
- Migration adoption metric -- did the affected customer move to the new path?
- Major-customer-impact check -- nobody is locked out without preparation.

### Risk profile

- Each step risks customer churn.
- Communication is the primary control surface, not the toggle.

### Pitfalls

- Skipping communication; angry tickets follow.
- Treating "we announced it" as "we communicated it" -- watch the open / acknowledgment rates.
- Removing 100% of users in one step. Always taper.

## Shape G: Mobile forced-upgrade

### When to use

Mobile feature requires a new client version (new API, new permission, new SDK).

### Example flow

```
1. New client version released to app stores.
2. Adoption climbs over 2-4 weeks (most users update within 30 days).
3. Server-side flag: minimum supported client version.
4. Old clients see a "please update" screen on launch.
5. After full migration, old client paths can be removed.
```

### Gate criteria

- New client adoption > 80% before any forced flow.
- Two-week notice in the app and via email/push.
- Migration support for non-updatable devices (rare but real).

### Risk profile

- High user impact. A forced upgrade is friction.
- Mistakes cannot be rolled back from the client side -- must be fixed server-side.

### Pitfalls

- Forcing too early; users on slow networks or older devices get locked out.
- No alternative path for users who cannot update (corporate-managed devices, end-of-life OS).
- Forced upgrade message that does not explain why.

## Decision flow: which shape?

```
Is this a sunset / EOL?
  Yes -> Shape F (reverse ramp).
  No -> continue

Is this an A/B test with measurement requirements?
  Yes -> Shape D (split with holdout).
  No -> continue

Is the feature server-only and high-traffic?
  Yes -> Start with Shape E (dark launch) before any user exposure, then Shape A.
  No -> continue

Does the audience have explicit risk gradients?
  Yes -> Shape B (segmented).
  No -> continue

Are there regional / regulatory variants?
  Yes -> Shape C (geographic).
  No -> continue

Is this a mobile feature requiring a client version bump?
  Yes -> Shape G (forced upgrade) combined with Shape A on the server.
  No -> continue

Default: Shape A (linear ramp).
```

## Combining shapes

Most real launches combine shapes. Examples:

- **AI feature launch** = Shape E (dark) -> Shape B (internal -> beta -> all) -> Shape A (percent ramp).
- **EU regulatory launch** = Shape C (region) -> Shape D (with holdout for impact measurement).
- **Mobile + server** = Shape G (client adoption) -> Shape A (server percent ramp).

The rollout plan template (`assets/rollout_plan_template.md`) supports combined shapes; specify the sequence in the stages table.

---
**Last Updated:** 2026-05-22
