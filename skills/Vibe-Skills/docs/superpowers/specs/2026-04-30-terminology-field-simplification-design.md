# Terminology And Field Simplification Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-30

## Goal

Reduce Vibe-Skills routing and skill-use concepts to a small, stable vocabulary and remove historical fields in stages without functional regression.

The active design target is:

```text
skill_candidates -> selected -> used / unused
```

This is a field-level simplification project, not another pack-pruning pass. It must make the project easier to understand while preserving current routing behavior, six-stage runtime behavior, and existing evidence interpretation.

## Current Findings

The current repository already has the simplified direction, but historical names still leak through the active configuration, runtime helpers, tests, and governance documents.

Observed state:

| Item | Current state |
| --- | ---: |
| Active packs in `config/pack-manifest.json` | 41 |
| Packs with `skill_candidates` | 41 |
| Packs with `route_authority_candidates` | 41 |
| Packs where `route_authority_candidates` differs from `skill_candidates` | 0 |
| Packs with `stage_assistant_candidates` field | 37 |
| Packs with non-empty `stage_assistant_candidates` | 0 |

This means `route_authority_candidates` has become a redundant mirror of `skill_candidates`, and `stage_assistant_candidates` has no active payload in the live pack manifest.

The risky terms and fields are still present in many files, especially historical governance notes and implementation plans. They cannot be removed by blind search-and-replace without damaging history or breaking old artifact readers.

## Non-Negotiable Principles

1. The six-stage Vibe runtime remains unchanged.
2. New active configuration must use the smallest field set that preserves behavior.
3. New runtime outputs must use current authority fields before any legacy field.
4. Old artifacts may remain readable through a compatibility layer until a later deletion stage.
5. Tests must prove both simplification and no routing regression.
6. Historical documents may mention old terms only as historical or deprecated context.
7. Pack pruning and physical skill deletion are separate workstreams.

## Canonical Active Vocabulary

| Term | Meaning |
| --- | --- |
| `skill` | A bounded capability with a `SKILL.md` entrypoint. |
| `skill_candidates` | The only active pack field listing skills that may be selected for that pack. |
| `selected skill` | A skill selected for the current task or stage. |
| `skill_routing.selected` | Runtime evidence that a skill was selected into the governed workflow. |
| `skill_usage.used` | Runtime evidence that a selected skill was loaded and materially shaped artifacts. |
| `skill_usage.unused` | Runtime evidence that a selected skill was not materially used, with a reason. |
| `legacy_skill_routing` | A compatibility container for interpreting older runtime artifacts only. |

## Deprecated Vocabulary

These names must not be used as new product or governance concepts:

| Deprecated name | Replacement |
| --- | --- |
| `route_authority` / `route owner` / `direct owner` | `skill_candidates` or `selected skill`, depending on context |
| `主路由` | `选中 skill` or `候选 skill`, depending on context |
| `stage_assistant` / `阶段助手` | Historical compatibility only |
| `辅助专家` / `咨询专家` | Do not use |
| `primary skill` / `secondary skill` / `主技能` / `次技能` | Do not use |
| `specialist recommendation` as authority | Use `skill_routing.selected` |
| `approved dispatch` as proof of use | Use `skill_usage.used` / `skill_usage.unused` |

Implementation identifiers may remain temporarily when they are needed to read older data, but they must be labeled as legacy compatibility and must not be introduced into new active design language.

## Target Field Model

### Pack Manifest

Target active shape:

```json
{
  "id": "code-quality",
  "skill_candidates": ["code-reviewer", "systematic-debugging"],
  "defaults_by_task": {
    "review": "code-reviewer",
    "debug": "systematic-debugging"
  }
}
```

Fields to remove from active `config/pack-manifest.json`:

```text
route_authority_candidates
stage_assistant_candidates
```

Fallback behavior may stay in router helper code until old config and old fixture support are retired.

### Runtime Packet

Target active authority:

```text
skill_routing.selected
skill_usage.used
skill_usage.unused
```

Legacy runtime surfaces such as `specialist_recommendations`, `stage_assistant_hints`, and `specialist_dispatch` may remain only under `legacy_skill_routing` while old artifact readers still need them.

## Phased Plan

### Phase 1: Terminology Governance And Guardrail

Purpose: stop the project from creating new terminology drift before changing live fields.

Changes:

- Add `docs/governance/terminology-governance.md`.
- Update the README and README.zh glossary to use the active vocabulary.
- Add a terminology audit for active docs and new governance notes.
- Treat historical mentions as allowed only when they appear in explicit legacy/deprecated/history context.

Verification:

- Active docs use `skill_candidates`, `selected skill`, and `used / unused`.
- New governance text does not introduce `route owner`, `direct owner`, `主路由`, `stage assistant`, `辅助专家`, or `咨询态` as active concepts.
- Historical documents remain readable and are not blindly rewritten.

Out of scope for terminology governance itself:

- No runtime code changes.
- No physical skill deletion.
- No blind rewrite of historical docs.

### Phase 2: Active Pack Manifest Field Simplification

Purpose: make the live pack configuration match the simplified model.

Changes:

- Remove `route_authority_candidates` from all active packs.
- Remove `stage_assistant_candidates` from all active packs.
- Keep `skill_candidates` as the only pack candidate list.
- Keep `defaults_by_task`, and verify every default points to a `skill_candidates` entry.

Compatibility:

- Router helper functions may continue to read old fields only if `skill_candidates` is missing.
- New active config must not write the old fields.

Verification:

- Every active pack has non-empty `skill_candidates`.
- No active pack has `route_authority_candidates` or `stage_assistant_candidates`.
- Routing smoke tests still select the same expected skills for existing probes.
- Offline skill closure still passes.

### Phase 3: New Runtime Output Cleanup

Purpose: prevent new sessions from producing old routing surfaces.

Changes:

- New runtime packets should expose selection through `skill_routing.selected`.
- New usage evidence should expose final state through `skill_usage.used` and `skill_usage.unused`.
- Old `specialist_*` surfaces must be absent from new root-level runtime output unless explicitly nested under `legacy_skill_routing`.

Compatibility:

- Keep readers for old runtime artifacts.
- Compatibility helpers must prefer `skill_routing.selected` and use old surfaces only when current fields are absent.

Verification:

- New smoke runtime packets contain current fields.
- Old fixture packets can still be interpreted.
- Completion claims cannot be made from selected-only or dispatch-only data.

### Phase 4: Documentation And Audit Rewrite

Purpose: make project understanding match actual behavior.

Changes:

- Update active governance notes and future pack-cleanup templates to use only active vocabulary.
- Rewrite global pack audit labels away from route-authority language.
- Keep historical docs intact unless they are linked as current guidance.

Verification:

- Active docs do not present legacy names as current concepts.
- Audit outputs describe candidate count, selected behavior, overlap risk, and usage evidence without route-owner language.

### Phase 5: Legacy Compatibility Deletion

Purpose: delete old compatibility code after the new shape is stable.

Prerequisites:

- Phase 1-4 tests pass.
- Current runtime no longer writes legacy fields in new artifacts.
- Old artifact reader coverage is either intentionally retained or intentionally retired.

Changes:

- Remove old field fallback paths.
- Remove old `stage_assistant` candidate generation.
- Remove obsolete confirm UI names such as `primary_skill` and `accept_primary` if no host contract requires them.
- Remove obsolete tests that only prove old field mirroring.

Verification:

- Full routing and runtime gates pass.
- Historical artifact interpretation either still passes through an explicit archive reader or is declared retired in governance docs.

## Testing Strategy

Each phase must include three kinds of tests:

| Test type | Required proof |
| --- | --- |
| Field-shape tests | New config or new runtime artifacts use only current fields. |
| Behavior tests | Existing route probes still choose the expected selected skill. |
| Compatibility tests | Old artifacts or old fixtures are either still readable or explicitly retired. |

Minimum recurring verification set:

```powershell
python -m pytest tests/unit/test_router_contract_selection_guards.py tests/runtime_neutral/test_simplified_skill_routing_contract.py tests/runtime_neutral/test_binary_skill_usage_contract.py -q
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-global-pack-consolidation-audit-gate.ps1
git diff --check
```

The exact command list may expand in later phases when the implementation touches runtime output or broader tests.

## Approved First Implementation Slice

The user approved option B for the first implementation slice: Phase 1 plus active `pack-manifest.json` field simplification from Phase 2. This slice should simplify the current active field model without touching runtime output cleanup or legacy reader deletion.

Planned files:

- `docs/governance/terminology-governance.md`
- `README.md`
- `README.zh.md`
- one terminology audit test or gate under the existing test/verify structure
- `config/pack-manifest.json`
- pack routing tests that still assert `route_authority_candidates` or `stage_assistant_candidates` as active fields
- router selection tests that prove old-field fixture compatibility remains available only when `skill_candidates` is absent

Success criteria:

- The project has one canonical terminology source.
- README glossary matches the canonical terminology.
- New active docs cannot introduce deprecated routing terms as current concepts.
- Active `config/pack-manifest.json` has no `route_authority_candidates` or `stage_assistant_candidates`.
- Every active pack still has non-empty `skill_candidates`.
- Every `defaults_by_task` entry points to an existing `skill_candidates` entry.
- Existing route probes still select the same expected skills.
- Runtime helper code may still read old fields for old fixtures, but new active config does not write them.
- No six-stage runtime behavior changes occur in this slice.

Explicit non-goals for this slice:

- Do not delete skill directories.
- Do not continue pack quality pruning.
- Do not remove old runtime artifact readers.
- Do not rename the governed runtime stages.
- Do not claim skill use from selected-only or dispatch-only data.

## Open Boundary

The user mentioned doing this in stages. If video artifacts are actually required later, that should be a separate documentation or demo task after the terminology and field model are stable. This design does not include video production.
