# Vibe Approved Dispatch User Disclosure Design

> Historical / Retired Note: This document records a previous routing design or
> migration state. Current routing authority is defined by
> `docs/governance/current-routing-contract.md` and
> `docs/governance/current-runtime-field-contract.md`.

## Goal

Make governed `vibe` runs tell the user, before specialist execution begins, which routed Skills will actually run and where each Skill is being executed from.

The disclosure must only cover real execution candidates, not router-only candidates or advisory recommendations.

## Problem

The current governed runtime already computes accurate specialist routing state:

- router truth is frozen into the runtime input packet
- specialist recommendations are materialized
- `approved_dispatch` identifies which specialist Skills are actually eligible to run
- each recommendation or dispatch already carries `native_skill_entrypoint`

However, that truth remains mostly inside artifacts such as the runtime input packet, generated requirement docs, execution plans, and execution manifests. Users can observe that routing happened internally, but they do not receive a concise pre-execution explanation in the interactive flow.

This creates a trust gap:

- users cannot easily tell which routed Skills will truly execute
- users cannot verify which physical Skill entrypoint is being used
- advisory or blocked specialist states are easy to confuse with real execution

## Approved Scope

This design freezes the disclosure contract to the following behavior:

- disclose only real specialist execution units derived from effective `approved_dispatch`
- disclose once per run as one unified summary
- disclose before specialist execution starts
- show the actual runtime entrypoint path used for execution
- do not disclose router-only candidates, `surfaced_skill_ids`, or residual `local_suggestion` entries in the user-facing summary

## Non-Goals

- do not expose all ranked router candidates to the user
- do not expose blocked or degraded specialists as if they were executing
- do not create a second router, second runtime authority, or second confirmation surface
- do not require hosts to materialize internal bundled Skills into top-level visible skill directories

## Recommended Architecture

Use runtime-backed disclosure generated from effective dispatch state inside `plan_execute`.

Why this layer:

- router output is too early and can still contain non-executing candidates
- freeze output is closer, but child/root same-round dispatch resolution can still change the final executable set
- `Invoke-PlanExecute.ps1` has the most accurate "what will really run now" view after effective dispatch resolution

The disclosure should therefore be built after:

1. frozen specialist dispatch is loaded
2. child auto-absorb or same-round promotion is resolved
3. effective `approved_dispatch` is known

and before:

1. specialist execution units are invoked

## Data Model

Add a runtime disclosure projection with these semantics:

- `enabled`: whether pre-dispatch disclosure is active
- `mode`: `approved_dispatch_pre_execution_unified_once`
- `timing`: `before_execution`
- `scope`: `approved_dispatch_only`
- `path_source`: `native_skill_entrypoint`
- `routed_skill_count`: count of unique executable specialist Skills
- `routed_skills`: array of bounded entries
- `rendered_text`: one user-facing pre-dispatch summary

Each routed skill entry should include:

- `skill_id`
- `native_skill_entrypoint`
- `native_skill_description`
- `dispatch_phase`
- `write_scope`
- `review_mode`

The disclosure must de-duplicate repeated skill ids while preserving first execution order.

## Rendered Output Contract

The user-facing text should be concise and deterministic.

Recommended format:

```text
Pre-dispatch specialist disclosure:
- systematic-debugging -> /abs/path/to/SKILL.md
- test-driven-development -> /abs/path/to/SKILL.md
```

Rules:

- one unified block per governed run
- only include executable specialist Skills
- absolute paths only
- no path aliases or repo-relative substitutions in the user-facing line
- if no approved specialist dispatch exists, no disclosure block is emitted

## Runtime Contract Changes

The governed runtime contract should explicitly require:

- governed `vibe` must emit a user-facing pre-dispatch disclosure when executable routed specialist Skills exist
- the disclosure must enumerate only effective `approved_dispatch` Skills
- the disclosure must identify the actual native entrypoint path used for each routed Skill
- this disclosure is an execution transparency surface, not a second route authority

This wording should be reflected in:

- `SKILL.md`
- `protocols/runtime.md`
- `protocols/team.md`

## Implementation Surface

Primary runtime files:

- `scripts/runtime/Invoke-PlanExecute.ps1`
- `scripts/runtime/VibeRuntime.Common.ps1`

Policy surface:

- `config/runtime-input-packet-policy.json`

Supporting narrative surfaces:

- `scripts/runtime/Write-XlPlan.ps1`
- `scripts/runtime/Write-RequirementDoc.ps1`

Test surfaces:

- `tests/runtime_neutral/test_governed_runtime_bridge.py`
- `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`
- optionally a focused runtime-neutral disclosure test if extraction becomes large enough to deserve isolated coverage

## Error Handling

If a dispatch entry lacks `native_skill_entrypoint`, the disclosure layer must not invent or normalize a different path.

Instead:

- keep the skill in execution accounting
- omit it from the user-facing disclosure if strict path presence is required by policy
- record the gap in execution proof or integrity surfaces

This avoids lying about the runtime location.

## Testing Strategy

Lock the behavior with tests that prove:

1. governed specialist runs produce a pre-dispatch disclosure object when `approved_dispatch` is non-empty
2. disclosure entries use `native_skill_entrypoint`
3. disclosure does not include non-executing recommendation-only skills
4. rendered text is unified once rather than repeated per skill
5. runtime summary or execution manifest carries the disclosure in a stable artifact surface

## Acceptance Criteria

1. Before specialist execution begins, governed `vibe` can surface one unified summary of actually executing routed Skills.
2. The summary uses effective `approved_dispatch`, not router-only candidates.
3. Each disclosed line points to the actual runtime entrypoint path.
4. Contract docs describe the behavior as mandatory execution transparency.
5. Tests prove the summary exists only for real execution candidates and stays aligned with execution truth.
