# Router Provider Layer

> Scope: govern provider-assisted routing intelligence without turning any provider into router authority.

## Purpose

The repository already uses model-backed routing intelligence in the real system.
This layer documents how that intelligence remains replaceable, optional, and subordinate to the canonical router.

## Canonical Rule

The canonical router remains:

- `scripts/router/resolve-pack-route.ps1`

Provider layers may assist that router, but they must not own assignment.

## Contract Files

- `schemas/router-provider.schema.json`
- `config/router-provider-registry.json`
- `config/router-provider-defaults.json`
- `docs/universalization/router-model-neutrality.md`
- `scripts/verify/vibe-router-provider-neutrality-gate.ps1`
- `scripts/verify/vibe-router-offline-degrade-contract-gate.ps1`

## Allowed Provider Roles

- semantic extraction
- candidate rerank
- route advice
- shadow evaluation
- route explainability

## Forbidden Provider Roles

- canonical assignment owner
- second router
- live router takeover
- explicit command override
- release chain owner

## Runtime States

| State | Meaning |
| --- | --- |
| `provider-assisted` | live provider help is available and policy-allowed |
| `heuristic-only` | the canonical router continues without provider assistance |
| `offline-frozen` | provider assistance is intentionally disabled and replay stays deterministic |
| `unsupported` | no truthful degraded path exists for the requested provider-dependent feature |

## Offline Honesty Rule

When a provider is missing, blocked, or intentionally disabled:

- the router may continue
- the runtime must not pretend provider assistance still exists
- the system must label the resulting state as `heuristic-only` or `offline-frozen`

## Non-Replacement Rule

This layer is governance-only in the current phase.

Do not:

- rewrite router ownership
- add a second router
- claim provider-neutrality while hiding provider-specific required env surfaces
