# Vibe Aggressive Specialist Routing Design

> Historical / Retired Note: This document records a previous routing design or
> migration state. Current routing authority is defined by
> `docs/governance/current-routing-contract.md` and
> `docs/governance/current-runtime-field-contract.md`.

## Goal

Make `vibe` treat specialist routing as a default governed behavior instead of an optional side path. Every governed `vibe` run must surface bounded specialist recommendations, and every eligible recommendation should promote to executable `approved_dispatch` as aggressively as safety allows.

## Problem

The current runtime already has specialist recommendation, promotion, and native execution plumbing, but the policy remains conservative in three places:

1. `Freeze-RuntimeInputPacket.ps1` can produce zero specialist recommendations when canonical router output is sparse.
2. Child-lane same-round auto-absorb requires an existing root-approved dispatch before promoting local suggestions.
3. Native specialist execution is disabled by default, so approved specialist dispatch may still degrade instead of executing.

This creates a mismatch between the intended governed routing story and observed behavior. Users expect routing to visibly happen and to materially affect execution, not just appear as advisory metadata.

## Design Principles

1. `vibe` remains the only governed runtime authority.
2. Specialist routing becomes mandatory behavior inside `vibe`, not a replacement for `vibe`.
3. Promotion stays aggressive for safe work and conservative only for destructive or incomplete contracts.
4. The runtime should prefer executing known native specialists instead of carrying recommendations as passive artifacts.

## Proposed Behavior

### 1. Mandatory specialist recommendation floor

Every governed `vibe` run must emit at least one bounded specialist recommendation.

Recommendation sourcing order:

1. Canonical router ranked specialist candidates
2. Overlay-provided recommended specialists
3. Router-selected non-`vibe` specialist route truth, if present
4. A new runtime fallback map keyed by router task type

If the router does not surface a specialist, the runtime will synthesize one from a policy-backed fallback profile. This keeps route authority intact while ensuring that `vibe` never skips specialist routing.

### 2. Root scope defaults to auto-dispatch

In `root_governed` runs, every non-destructive recommendation with a complete native contract should promote directly to `approved_dispatch`.

This is already partially true through skill-promotion metadata. The design formalizes it as required behavior rather than incidental behavior and updates contract text to say that eligible recommendations are expected to auto-promote.

### 3. Child scope uses aggressive same-round auto-absorb

Child-governed lanes should no longer require a pre-existing root-approved dispatch before auto-absorbing local specialist suggestions.

If a child suggestion:

- matches a frozen recommendation,
- preserves native workflow,
- requires native usage,
- stays within bounded write-scope rules,
- and is not destructive,

then the same-round auto-absorb gate should promote it into effective `approved_dispatch` automatically.

Residual `local_suggestion` state should exist only for blocked, degraded, or explicitly forced-escalation cases.

### 4. Native specialist execution defaults on

`native-specialist-execution-policy.json` should enable native execution by default so auto-approved dispatch has a high-probability execution path instead of degrading by policy default.

Environment flags still remain available to disable execution or force escalation in specific scenarios.

## Policy Changes

### Runtime input packet policy

Add or revise policy semantics so that:

- specialist recommendation generation is required
- a minimum recommendation floor exists
- fallback specialists are declared by task type
- child auto-absorb no longer requires existing root dispatch
- recommendation and auto-absorb limits are high enough to support aggressive routing

### Skill promotion policy

Keep destructive and incomplete-contract protections intact, but frame the default promotion mode as aggressive auto-dispatch for safe work.

### Native specialist execution policy

Change the default from opt-in to opt-out.

## Contract Updates

The governed runtime contract should say, in effect:

- `vibe` must attempt specialist routing on every governed run
- specialist recommendations are mandatory runtime output, not optional metadata
- eligible recommendations must auto-promote to `approved_dispatch`
- child lanes may auto-absorb bounded specialist help in the same round without waiting for a separately frozen root dispatch entry

This wording should be reflected consistently in:

- `SKILL.md`
- `protocols/runtime.md`
- `protocols/team.md`
- human-readable plan/requirement generation surfaces

## Testing Strategy

Add or update tests to prove:

1. Governed runtime always emits at least one specialist recommendation.
2. A fallback recommendation appears when router ranking alone would otherwise leave no specialist surfaced.
3. Root runs auto-promote safe recommendations to `approved_dispatch`.
4. Child runs can auto-absorb same-round specialist dispatch without existing root-approved dispatch.
5. Destructive prompts still block promotion.
6. Native specialist execution is enabled by default for eligible dispatch.

## Risks

### Over-routing

The runtime may surface specialists on tasks that would previously have stayed single-lane. This is intentional, but the fallback recommendation set must stay bounded and generic enough not to distort the task.

### Excessive dispatch fan-out

Aggressive routing can create too many specialist units. The policy should keep a finite cap and rely on execution topology to serialize where needed.

### Governance confusion

If wording is sloppy, aggressive routing could look like a second runtime authority. All contract text must explicitly preserve `vibe` as the sole governor.

## Acceptance Criteria

1. `vibe` governed runs always emit at least one specialist recommendation.
2. Safe recommendations in root scope default to `approved_dispatch`.
3. Child same-round auto-absorb can promote safe local suggestions without requiring existing root dispatch.
4. Native specialist execution is enabled by default.
5. Destructive prompts still do not auto-promote.
6. Contract docs and verification surfaces describe routing as aggressive-by-default while preserving single runtime authority.
