# Vibe Approved Dispatch User Disclosure Requirement

## Summary

Add a governed execution-transparency surface so `vibe` can tell the user, before specialist execution begins, which routed Skills will actually run and where each Skill is being executed from.

## Goal

Eliminate silent routed-skill execution by requiring one unified pre-execution disclosure for effective `approved_dispatch`.

## Deliverable

A runtime-backed disclosure projection and aligned contract text that:

- only covers actually executing routed Skills
- is emitted once before execution
- uses the real `native_skill_entrypoint` path for each disclosed Skill

## Constraints

- `vibe` remains the only runtime authority
- no second router or second confirmation surface may be introduced
- user-facing disclosure must not include router-only candidates or residual advisory specialist suggestions
- disclosure must use actual runtime entrypoints, not guessed repo-relative fallbacks
- existing specialist promotion, blocking, and degradation safeguards remain intact

## Acceptance Criteria

- governed `vibe` runs with non-empty effective `approved_dispatch` produce a unified pre-execution disclosure surface
- the disclosure only enumerates effective `approved_dispatch` Skills
- each disclosed skill includes its real `native_skill_entrypoint`
- no blocked, degraded, or recommendation-only skills appear as executing in the user-facing disclosure
- execution artifacts and runtime contracts remain traceable to the disclosure behavior

## Product Acceptance Criteria

- a user can tell which routed Skills will really run without opening requirement or plan artifacts manually
- a user can inspect the exact entrypoint path for each disclosed Skill
- disclosure wording does not blur the boundary between recommendation and execution

## Manual Spot Checks

- Trigger a governed runtime task that routes at least one specialist and confirm the disclosure block appears before execution.
- Confirm each disclosed path matches the effective `native_skill_entrypoint` used for execution and resolves to the actual Skill entrypoint at runtime.
- Confirm a run with recommendation-only or blocked specialist state does not claim execution for those Skills.

## Completion Language Policy

Do not claim this behavior is complete unless fresh runtime verification proves the disclosure is emitted before execution and remains aligned with effective dispatch truth.

## Delivery Truth Contract

Success means execution transparency exists for actual routed specialist execution, not merely that specialist metadata appears in frozen artifacts.

## Artifact Review Requirements

No additional artifact review requirements were frozen for this run.

## Code Task TDD Evidence Requirements

- Record failing-first evidence for the disclosure behavior before implementation.
- Verify that the disclosure excludes recommendation-only, blocked, and degraded specialist states.
- Verify that disclosed paths come from `native_skill_entrypoint` rather than a separately synthesized display path.

## Code Task TDD Exceptions

No code-task TDD exceptions were frozen for this run.

## Baseline Document Quality Dimensions

No baseline document quality dimensions were frozen for this run.

## Baseline UI Quality Dimensions

No baseline UI quality dimensions were frozen for this run.

## Task-Specific Acceptance Extensions

- The disclosure must be unified once per run rather than emitted one line at a time for each specialist.
- The disclosure must preserve first execution order for routed Skills.

## Research Augmentation Sources

- `SKILL.md`
- `protocols/runtime.md`
- `protocols/team.md`
- `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- `scripts/runtime/Invoke-PlanExecute.ps1`
- `scripts/runtime/VibeRuntime.Common.ps1`
- `tests/runtime_neutral/test_governed_runtime_bridge.py`

## Primary Objective

Expose truthful pre-execution routed-skill disclosure for effective `approved_dispatch`.

## Non-Objective Proxy Signals

- merely increasing specialist recommendation counts
- documenting routed Skills in requirement or plan artifacts only
- exposing router candidate lists without execution truth

## Validation Material Role

Runtime-neutral tests and execution artifacts are the source of truth for this change.

## Anti-Proxy-Goal-Drift Tier

Tier 1 execution-truth preservation.

## Intended Scope

Governed runtime disclosure for routed specialist execution.

## Abstraction Layer Target

Runtime execution disclosure and contract surfaces.

## Completion State

Complete only when runtime artifacts and tests both prove pre-execution disclosure for real executable specialist Skills.

## Generalization Evidence Bundle

- governed runtime integration evidence
- focused specialist-dispatch disclosure assertions
- contract-text alignment across runtime documents

## Non-Goals

- do not redesign confirm UI for router candidate choice
- do not expose all surfaced recommendations to the user
- do not change host packaging topology for bundled specialist Skills

## Autonomy Mode

Interactive governed execution with XL planning discipline and bounded implementation changes.

## Assumptions

- `native_skill_entrypoint` is already the most accurate path source for actual specialist execution
- host-visible user messaging can consume a rendered disclosure surface from runtime artifacts or the governed prompt contract
- current runtime tests are sufficient to prove disclosure truth without introducing a new host adapter layer in this turn

## Evidence Inputs

- Source task: Add unified pre-dispatch disclosure for actually executing routed Skills
- Design spec: `docs/superpowers/specs/2026-04-12-vibe-approved-dispatch-user-disclosure-design.md`
- Relevant runtime surfaces: `scripts/runtime/Invoke-PlanExecute.ps1`, `scripts/runtime/VibeRuntime.Common.ps1`
