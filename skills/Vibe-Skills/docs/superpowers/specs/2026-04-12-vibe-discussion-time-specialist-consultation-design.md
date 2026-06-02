# Vibe Discussion-Time Specialist Consultation Design

> Historical / Retired Note: This document records a previous routing design or
> migration state. Current routing authority is defined by
> `docs/governance/current-routing-contract.md` and
> `docs/governance/current-runtime-field-contract.md`.

## Goal

Allow governed `vibe` runs to consult suitable routed specialist Skills during discussion and plan formation, while keeping `vibe` as the only runtime authority and the only outward-facing speaker.

The user should be able to see, progressively and truthfully, which specialist Skills are being consulted, why they are being consulted now, and where each Skill is loaded from.

## Problem

The current governed runtime already freezes high-quality specialist routing truth:

- router-selected specialist candidates are preserved
- fallback and overlay specialist recommendations are materialized
- specialist promotion and degradation are evaluated
- execution-time dispatch truth is preserved separately

However, that truth is used mostly in two ways:

- as metadata written into requirement and plan artifacts
- as execution-time dispatch input later in `plan_execute`

This means the current discussion and planning chain has a gap:

- relevant planning specialists are identified, but usually not truly consulted before requirement or plan freeze
- `vibe` owns the whole front-of-house conversation, but does not yet run a governed backstage consultation loop during requirement and plan formation
- users can see that routing happened, but they cannot see that specialist reasoning truly influenced the discussion before execution

The practical effect is that specialists are often deferred to execution-time help instead of improving the earlier conversation and planning process.

## Approved Scope

This design freezes one standalone PR with one coherent goal:

- introduce governed specialist consultation during discussion and plan formation
- keep the public six-stage runtime contract unchanged
- keep router authority unchanged
- keep execution-time `approved_dispatch` disclosure semantics unchanged
- add progressive user-facing consultation disclosure under `vibe`

The new consultation behavior should support two consultation windows:

1. discussion-time consultation after `deep_interview` and before `requirement_doc`
2. plan-time consultation after `requirement_doc` and before final `xl_plan`

Both windows use the same consultation engine, policy, and receipt shape.

## Non-Goals

- do not make specialist Skills become parallel runtime authorities
- do not let specialist Skills speak directly to the user as peer front-end agents
- do not replace the canonical router
- do not merge consultation truth into execution-time `approved_dispatch`
- do not redesign execution topology or specialist execution proof in this PR
- do not introduce host-specific transcript streaming behavior as the primary implementation surface

## Design Principles

### 1. Single Front Door

The user continues to talk only to `vibe`.

Specialists participate as backstage consultation units. Their output is absorbed, summarized, and presented by `vibe`.

### 2. Separate Truth Layers

This PR must keep three truths distinct:

- routing truth: what the router thought was relevant
- consultation truth: which specialists were truly consulted during discussion or planning
- execution truth: which specialists truly executed later in `plan_execute`

These truths must not be merged into one overloaded field.

### 3. Progressive Disclosure

The user should not receive a giant specialist dump at startup.

Instead, `vibe` should disclose specialist consultation incrementally:

- when consultation starts
- only for specialists actually approved for consultation
- with a brief explanation of why the specialist is being consulted now

### 4. High Cohesion

Discussion-time and plan-time specialist consultation should live in one isolated runtime module with one policy surface and one receipt model.

### 5. Low Coupling

Consultation should depend on frozen routing outputs and shared specialist invocation primitives, but should not mutate router selection logic or execution dispatch semantics.

## Recommended Architecture

### Public Runtime Contract

Keep the public six-stage state machine unchanged:

1. `skeleton_check`
2. `deep_interview`
3. `requirement_doc`
4. `xl_plan`
5. `plan_execute`
6. `phase_cleanup`

Do not add a seventh public stage.

Instead, add one internal runtime subflow:

- `specialist_consultation`

This subflow is invoked at controlled points inside the existing governed path.

### Consultation Windows

#### Window A: Discussion-Time Consultation

Run after `deep_interview` has produced the first intent contract and after `runtime_input_packet` has frozen specialist routing truth.

Purpose:

- sharpen ambiguity handling
- improve question selection
- refine requirement framing
- surface specialist risks before requirement freeze

#### Window B: Plan-Time Consultation

Run after `requirement_doc` exists and before final `xl_plan` freeze is written.

Purpose:

- improve plan structure
- refine step sequencing and ownership boundaries
- strengthen verification coverage and rollback strategy

The same consultation engine serves both windows; only the consultation stage label and prompt framing differ.

## Data Model

Add a new independent runtime surface named:

- `specialist_consultation`

Recommended shape:

- `enabled`
- `policy_version`
- `windows`

Each window entry should contain:

- `window_id`
- `stage`
- `candidate_skill_ids`
- `approved_consultation`
- `deferred_to_execution`
- `blocked`
- `degraded`
- `consulted_units`
- `user_disclosures`
- `summary`

Each approved consultation entry should contain:

- `skill_id`
- `native_skill_entrypoint`
- `native_skill_description`
- `consultation_reason`
- `consultation_scope`
- `consultation_role`
- `consultation_stage`
- `write_scope`
- `review_mode`

Each consulted unit should contain:

- `skill_id`
- `status`
- `response_json_path`
- `summary`
- `consultation_notes`
- `verification_notes`
- `prompt_path`
- `schema_path`
- `live_native_execution`

### Important Separation Rule

Do not store discussion-time consultation in:

- `approved_dispatch`
- `local_specialist_suggestions`
- execution topology specialist buckets

Those are execution-truth surfaces and must remain execution-truth surfaces.

## Policy Surface

Add a dedicated policy file:

- `config/specialist-consultation-policy.json`

Recommended fields:

- `enabled`
- `max_consults_per_window`
- `allowed_windows`
- `consultation_selection_mode`
- `require_contract_complete`
- `require_native_workflow`
- `require_native_usage_required`
- `require_entrypoint_path`
- `progressive_disclosure_enabled`
- `defer_unapproved_to_execution`
- `window_prompts`

This keeps consultation policy cohesive and prevents `runtime-input-packet-policy.json` from becoming a mixed routing and discussion engine.

## Runtime Surface

Create one consultation-focused runtime module:

- `scripts/runtime/VibeConsultation.Common.ps1`

This module should own:

- candidate approval for consultation windows
- consultation prompt construction
- consultation result schema
- consultation unit invocation
- consultation receipt building
- progressive disclosure rendering

Primary integration points:

- `scripts/runtime/invoke-vibe-runtime.ps1`
- `scripts/runtime/Write-RequirementDoc.ps1`
- `scripts/runtime/Write-XlPlan.ps1`
- `scripts/runtime/VibeRuntime.Common.ps1`

### Shared Invocation Primitive

Consultation should reuse existing low-level host invocation helpers where sensible:

- host adapter resolution
- captured process execution
- schema-backed JSON response validation

But it should not reuse execution-dispatch data structures directly.

If shared invocation logic is too entangled with execution semantics, extract the truly shared process-layer helpers and keep consultation-specific modeling separate.

## Consultation Approval Rules

`vibe` should approve consultation from frozen `specialist_recommendations`, not from raw router ranking.

Recommended approval gate:

- candidate must come from frozen `specialist_recommendations`
- candidate must have complete contract metadata
- candidate must not be destructive
- candidate must preserve native workflow
- candidate must expose real `native_skill_entrypoint`
- candidate must fit the current consultation window
- candidate count must respect `max_consults_per_window`

Candidates not approved for consultation should be placed into:

- `deferred_to_execution` if still viable later
- `blocked` if policy says no
- `degraded` if contract truth is insufficient

## User Disclosure Contract

Progressive disclosure should be user-facing but compact.

Recommended rendered pattern:

```text
Planning specialist consultation:
- consulting `writing-plans`
  why now: task breakdown before requirement freeze
  location: /abs/path/to/SKILL.md
```

Rules:

- disclose only actually approved consultation units
- disclose when the consultation begins, not all at once at startup
- keep `vibe` as the speaker
- include absolute path from `native_skill_entrypoint`
- explain why the specialist is being consulted now
- do not imply that the specialist has become runtime authority

## Requirement And Plan Consumption

### Requirement Doc

Add a section such as:

- `## Consulted Specialists`

This section should state:

- which specialists were truly consulted before requirement freeze
- what questions or risk areas they informed
- which ideas were absorbed into the frozen requirement

### Execution Plan

Add a section such as:

- `## Planning Consultation Inputs`

This section should state:

- which specialists were consulted before plan freeze
- which plan decisions were influenced by those consultations
- which specialist inputs were recorded but not adopted

This keeps consultation truth visible without pretending it was execution truth.

## Artifacts

Recommended new artifact paths:

- `outputs/runtime/vibe-sessions/<run-id>/discussion-specialist-consultation.json`
- `outputs/runtime/vibe-sessions/<run-id>/planning-specialist-consultation.json`
- `outputs/runtime/vibe-sessions/<run-id>/host-stage-disclosure.json`

Recommended runtime summary projection:

- `specialist_consultation`
- `host_user_briefing`

This gives hosts and tests one stable place to inspect consultation behavior without scraping prose documents.

## Error Handling

If a specialist is recommended but cannot be safely consulted:

- keep it in consultation accounting
- classify it as `blocked` or `degraded`
- do not emit a fake consultation disclosure
- do not silently promote it into execution dispatch

If consultation execution fails:

- keep the receipt
- mark the consulted unit as failed or degraded
- allow `vibe` to continue only with truthful fallback wording
- preserve traceability in requirement or plan surfaces

## Testing Strategy

Create a focused isolated test surface for consultation behavior rather than overloading execution-disclosure tests.

Recommended tests:

- `tests/runtime_neutral/test_vibe_specialist_consultation.py`

Existing tests to extend carefully:

- `tests/runtime_neutral/test_governed_runtime_bridge.py`
- `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`

The tests should prove:

1. discussion-time consultation can be approved from frozen specialist recommendations
2. consultation truth is stored separately from execution dispatch truth
3. approved consultation units generate disclosure entries with absolute `native_skill_entrypoint`
4. requirement docs can consume discussion consultation truth
5. plans can consume planning consultation truth
6. execution-time `approved_dispatch` behavior remains unchanged when consultation is added

## Acceptance Criteria

1. Governed `vibe` can truly consult suitable specialist Skills during discussion and plan formation.
2. Consultation occurs under `vibe` authority and does not create a second runtime authority.
3. Users receive progressive disclosure about consulted specialist Skills, including why-now reasoning and actual Skill location.
4. Consultation truth is modeled separately from execution dispatch truth.
5. Requirement and plan artifacts reflect real consultation inputs rather than only recommendation metadata.
6. Execution-time `approved_dispatch` disclosure behavior remains intact and semantically separate.
