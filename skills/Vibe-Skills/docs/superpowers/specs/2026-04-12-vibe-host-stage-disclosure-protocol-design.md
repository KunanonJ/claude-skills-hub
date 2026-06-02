# Vibe Host Stage Disclosure Protocol Design

> Historical / Retired Note: This document records a previous routing design or
> migration state. Current routing authority is defined by
> `docs/governance/current-routing-contract.md` and
> `docs/governance/current-runtime-field-contract.md`.

## Goal

Give hosts a stage-by-stage specialist disclosure surface that can be consumed while governed `vibe` is still running.

The protocol must let the host surface confirmed discussion, planning, and execution specialist activity incrementally without turning specialists into a second outward-facing runtime authority.

## Problem

The current runtime already has strong specialist truth surfaces:

- routing truth in the frozen runtime input packet
- consultation truth in discussion and planning consultation receipts
- execution truth in the approved-dispatch disclosure and execution manifest
- final human-readable aggregation in `host_user_briefing`

However, the host-facing aggregation only becomes available after the governed runtime returns. That means the host cannot progressively inform the user which Skills were routed, truly consulted, or approved for execution while the run is still in progress.

## Approved Scope

This design adds one new runtime artifact:

- `host-stage-disclosure.json`

It is an append-only host-consumption event stream backed by confirmed runtime facts.

The protocol covers four specialist milestones:

1. `discussion_routing_frozen`
2. `discussion_consultation_completed`
3. `planning_consultation_completed`
4. `execution_dispatch_confirmed`

## Non-Goals

- do not change the six public runtime stages
- do not merge host disclosure into `stage-lineage.json`
- do not let specialists speak directly to the user
- do not treat router candidates as if they were already consulted
- do not treat consultation truth as if it were execution approval

## Design Rules

### 1. Single outward speaker

`vibe` stays the only outward-facing speaker.

The host-stage protocol is a host-consumption surface, not a specialist transcript surface.

### 2. Confirmed facts only

An event is written only when the backing runtime fact already exists:

- routing event after runtime input freeze
- discussion consultation event after the discussion consultation receipt exists
- planning consultation event after the planning consultation receipt exists
- execution dispatch event after the effective approved-dispatch disclosure is known

### 3. Separate truth layers stay separate

Each event preserves the source truth layer:

- `routing`
- `consultation`
- `execution`

Hosts must not flatten those into one undifferentiated "used skill" concept.

### 4. High cohesion, low coupling

The protocol reuses existing lifecycle projections instead of inventing a second specialist model.

`stage-lineage.json` remains governance lineage.
`host-stage-disclosure.json` becomes host-consumption disclosure.

## Data Model

Top-level shape:

- `enabled`
- `protocol_version`
- `mode`
- `append_only`
- `event_count`
- `last_sequence`
- `freeze_gate_passed`
- `events`
- `rendered_text`

Each event contains:

- `sequence`
- `emitted_at`
- `event_id`
- `segment_id`
- `stage`
- `category`
- `truth_layer`
- `status`
- `gate_status`
- `skill_count`
- `skills`
- `rendered_text`

## Runtime Integration

### Runtime common helpers

Add shared helpers in `scripts/runtime/VibeRuntime.Common.ps1` for:

- host-stage artifact path resolution
- host briefing segment projection
- host-stage event projection
- append-only event persistence

### Root runtime integration

In `scripts/runtime/invoke-vibe-runtime.ps1`:

- append routing event after runtime input freeze
- append discussion consultation event after discussion consultation receipt
- append planning consultation event after planning consultation receipt
- load the final disclosure artifact into runtime summary and top-level payload

### Execution-stage integration

In `scripts/runtime/Invoke-PlanExecute.ps1`:

- append execution-dispatch event immediately after effective `approved_dispatch` disclosure is known
- do this before execution units run so the host can surface the approved execution Skills during the execution stage itself

## Acceptance Criteria

1. Governed runtime writes `host-stage-disclosure.json` when stage-confirmed specialist activity exists.
2. Events appear in deterministic order and use stable ids for routing, discussion consultation, planning consultation, and execution dispatch.
3. Each event includes the involved Skills and their real `native_skill_entrypoint` paths when available.
4. `runtime-summary.json` and the top-level runtime payload expose the disclosure artifact path and parsed object.
5. Governance lineage remains separate from host-consumption disclosure.
