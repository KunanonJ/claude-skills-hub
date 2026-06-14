# Feature Flag Naming Convention

A team-level naming sheet. Adopt this verbatim or fork it; the only requirement is that the team picks one convention and enforces it.

**Team:** ____________________
**Adopted:** 2026-05-22
**Enforcement:** PR review / flag-service lint hook / both

---

## The convention

```
<scope>__<feature>__<purpose>[__<version>]
```

All lowercase. Double-underscores between fields. Single-underscores within a field.

### Examples

| Flag name | Decoded |
|---|---|
| `web__checkout__new_flow__v2` | Web release toggle, new checkout flow, version 2 |
| `mobile_ios__paywall__experiment__q3_2026` | iOS A/B test, paywall variant, Q3 2026 |
| `api__search__relevance__rollout` | API release toggle, search relevance change |
| `infra__database__circuit_breaker` | Infrastructure ops toggle, database circuit breaker (permanent) |
| `product__enterprise_admin__permission` | Permission gate, enterprise admin panel (permanent) |
| `web__signup__email_verification__sunset` | Web sunset (reverse-ramp) for email verification |
| `mobile_android__camera__permission__beta_program` | Android camera permission gated to beta program |

## Field reference

### `<scope>` (required)

Where the flag is checked. One of:

| Value | Meaning |
|---|---|
| `web` | Web application |
| `mobile_ios` | iOS application |
| `mobile_android` | Android application |
| `mobile` | Both mobile platforms (only if behavior is identical) |
| `api` | Backend API |
| `infra` | Infrastructure / SRE / platform |
| `product` | Cross-surface product feature |
| `email` | Email-system toggles |
| `growth` | Growth experiments spanning surfaces |

### `<feature>` (required)

The system surface the flag controls. Use the engineering name, not the marketing name. Engineering names are stable; marketing names change. Examples: `checkout`, `search`, `signup`, `paywall`, `dashboard`, `notification`.

### `<purpose>` (required)

The flag's purpose. One of:

| Value | Meaning | Lifespan |
|---|---|---|
| `rollout` | Release toggle for general rollout | Short-lived |
| `new_flow`, `v2`, etc. | Release toggle for a specific UX change | Short-lived |
| `experiment` | A/B test toggle | Short-lived |
| `permission` | Permanent gating by user / plan / role | Permanent |
| `beta_program` | Permanent gating for beta participants | Permanent |
| `circuit_breaker` | Ops toggle for system protection | Permanent |
| `throttle` | Ops toggle for rate limiting | Permanent |
| `degrade_mode` | Ops toggle for degraded operation under load | Permanent |
| `sunset` | Reverse-ramp for retiring a feature | Short-lived |
| `dark_launch` | Shadow / dark-launch toggle | Short-lived |

### `<version>` (optional)

Use when multiple versions of the same purpose exist or when experiments need a time-window suffix. Examples: `v2`, `v3`, `q1_2026`, `q3_2026`, `aug_2026`.

## Rules

1. **All lowercase.** Avoid camelCase and PascalCase. Aligns with most flag-service search behavior.
2. **Underscores, not dashes.** Some flag services normalize dashes inconsistently.
3. **Double-underscore between fields, single within a field.** This keeps the field boundaries parseable by lint tools.
4. **No team names.** Teams reorg; flags outlive teams.
5. **No customer names.** Exception: per-tenant permission flags can include the tenant id (`api__feature__permission__tenant_acme_inc`).
6. **No vague words.** Avoid `new`, `improved`, `better`, `final`. Use a version number instead (`v2`, `v3`).
7. **No date stamps in release toggles.** Release toggles are short-lived and will be retired. Use dates only for experiments.
8. **Max 60 characters.** Long names degrade in dashboards.
9. **Description field is required.** The flag service should reject creation if the description is empty.

## What NOT to do

| Bad name | Why |
|---|---|
| `newCheckout` | camelCase; missing scope and purpose |
| `enable_feature` | Too vague; unclear what feature |
| `temp_fix_for_acme_bug` | Customer name; "temp" without retirement date |
| `checkout_v2` | Missing scope and purpose; not searchable |
| `EXPERIMENT-001` | uppercase; opaque |
| `bobs_test_flag` | Team-member name; will orphan |
| `final_release_flag` | "final" never is |
| `do_not_remove` | Documentation in name; should be in description |
| `the_one_true_flag` | Cute names age badly |
| `feature_x_y_z` | Multiple features in one flag |

## Lint hook (sample regex)

If your flag service supports validation on creation:

```regex
^(web|mobile|mobile_ios|mobile_android|api|infra|product|email|growth)__[a-z][a-z0-9_]+__(rollout|new_flow|v\d+|experiment|permission|beta_program|circuit_breaker|throttle|degrade_mode|sunset|dark_launch)(__[a-z0-9_]+)?$
```

Adjust the purpose enumeration to match your team's allowed values.

## Required metadata at flag creation

Beyond the name, every flag should have these fields populated:

| Field | Required for |
|---|---|
| Description (>= 1 sentence) | All flags |
| Owner team | All flags |
| Owner individual (PM + Eng) | Release / experiment flags |
| Type | All flags (auto-derivable from purpose) |
| Retirement date | Release / experiment flags |
| Tier (1/2/3 critical / core / non-critical) | All customer-visible flags |
| Linked PRD / ticket | All flags |

## Renaming

If a flag is mis-named, rename it. The flag service should support renaming. The risk of leaving a bad name is greater than the small migration cost.

When renaming:
1. Create the new flag with the correct name and same rollout state.
2. Update code references in a single PR.
3. Deploy.
4. Verify production is using the new flag.
5. Retire the old flag.

---

## Review

Re-review this sheet annually with the team. The convention is owned by the team; if the team finds it cumbersome, update it -- but only with full team agreement, not flag-by-flag drift.
