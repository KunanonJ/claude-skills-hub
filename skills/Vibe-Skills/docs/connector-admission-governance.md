# Connector Admission Governance

## Scope

Wave36 first moved `awesome-mcp-servers`, `composio`, and `activepieces` into a single **connector admission** governance plane.
Wave A on 2026-03-17 re-audits those same sources and keeps the core conclusion intact: connector sources may inform VCO, but none of them may become a second connector control plane.

This layer answers:

- which source is catalog-only,
- which source is a shadow-governed provider candidate,
- which capability/risk classes may enter the allowlist,
- which actions must remain confirm-gated or denied,
- which decision class the current packet reached.

## Source Roles

| Source | Position | Meaning | 2026-03-17 Decision Class |
|---|---|---|---|
| `awesome-mcp-servers` | `catalog_reference_only` | connector scouting / catalog snapshot only; never auto-install or execution owner | `metadata-only` |
| `composio` | `provider_candidate` | connector template / action surface candidate behind shadow governance | `admit` |
| `activepieces` | `provider_candidate` | workflow/action/piece taxonomy source behind shadow governance | `admit` |

## Dual Asset Surface

Connector governance intentionally uses two asset layers:

- gate-facing runtime contract:
  - `references/connector-admission-matrix.md`
  - `config/connector-provider-policy.json`
- operator-facing planning and catalog surface:
  - `references/connector-capability-matrix.md`
  - `config/connector-admission-policy.json`

The gate-facing pair remains authoritative for pass/fail verification.
The operator-facing pair exists to expose a richer planning view without creating a second owner.
Both pairs must resolve to the same governance truth.

## Control Plane Invariants

All connector sources share these invariants:

- `control_plane_owner = vco`
- `allow_second_orchestrator = false`
- `allow_provider_takeover = false`
- `allow_auto_install_from_catalog = false`
- `require_allowlist_entry = true`
- `require_confirm_for_write = true`
- `require_shadow_first_for_new_connectors = true`
- no external connector may gain de facto owner status through convenience or operator habit

## Admission States

| Status | Meaning |
|---|---|
| `catalog_governed` | catalog source is governed, but cannot directly become execution surface |
| `shadow_governed` | provider candidate is allowed only in bounded shadow/advice-first posture |
| `allowlisted_provider` | future explicit promotion target only; not opened in this packet |
| `denied` | source or source-capability combination is refused |

## Allowlist / Denylist Rule

The allowlist records only governed `source + capability` pairs that VCO is willing to preserve inside its own connector plane.
The denylist records connector behaviors that must never be admitted:

- second orchestrator
- route override
- auto install from catalog
- unconfirmed production write
- credential exfiltration
- connector-defined memory truth source

## 2026-03-17 Re-Audit Outcome

### `activepieces`

Upstream drift materially increases the value of piece/action/trigger taxonomy and auth-pattern framing.
Admitted effect:

- tighten capability tags and operator guidance
- keep all write-capable or trigger-capable usage shadow-governed and confirm-gated

### `composio`

Upstream drift materially increases the value of connect-client, auth-boundary, and app-catalog contract clarity.
Admitted effect:

- tighten provider metadata and secret-profile framing
- keep `composio` in `provider_candidate` posture with no takeover path

### `awesome-mcp-servers`

Upstream drift continues to matter as catalog churn only.
Admitted effect:

- refresh catalog metadata and operator wording only
- no install or execution widening

## Matrix Usage

- `references/connector-admission-matrix.md` is the gate-facing admission matrix
- `config/connector-provider-policy.json` is the gate-facing executable contract
- `references/connector-capability-matrix.md` is the operator-facing capability mapping
- `config/connector-admission-policy.json` is the operator-facing catalog and risk summary
- `scripts/verify/vibe-connector-admission-gate.ps1` is the binding gate for invariants

## Follow-up

This packet does not modify install, release, or runtime execution flow.
Any future attempt to widen a connector source beyond current posture must first satisfy:

- explicit decision class beyond `metadata-only` or bounded `admit`
- replay and rollback evidence
- scorecard evidence
- a fresh governed packet
