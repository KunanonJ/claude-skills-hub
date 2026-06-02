# Binary Skill Usage Routing Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-28

## 1. Goal

This design freezes the minimal architecture cleanup for Vibe-Skills skill routing and skill usage accounting.

The public six-stage governed runtime remains unchanged:

1. `skeleton_check`
2. `deep_interview`
3. `requirement_doc`
4. `xl_plan`
5. `plan_execute`
6. `phase_cleanup`

The cleanup target is narrower: make routed skills enter the work in a simple, honest, and verifiable way.

The final user-facing skill state model has only two states:

```text
used
unused
```

No other user-facing skill usage state is authoritative.

## 2. Problem

The current routing and specialist surfaces contain too many adjacent concepts:

- `skill_candidates`
- `route_authority_candidates`
- `stage_assistant_candidates`
- `specialist_recommendations`
- `stage_assistant_hints`
- `specialist_dispatch.approved_dispatch`
- consultation receipts
- execution proof artifacts

These concepts are useful internally, but they create a practical governance problem: a skill can be routed, recommended, hinted, consulted, or dispatched without clearly proving that its `SKILL.md` workflow actually shaped the work.

The user-facing result is confusing:

- routed does not necessarily mean used
- recommended does not necessarily mean used
- hinted does not necessarily mean used
- consulted does not necessarily mean used
- dispatched does not necessarily mean used

The runtime needs one final truth layer for skill usage.

## 3. Approved Design Direction

Use the minimal binary usage model.

Chosen approach:

```text
route selection remains internal routing truth
skill_usage becomes the only skill usage truth
```

Rejected approaches:

| Alternative | Why not |
|---|---|
| Keep `stage_assistant_hints` and strengthen consultation | This keeps the same mental-model problem: many intermediate states still look like partial skill use. |
| Force one and only one skill per run | This is simple but too restrictive for future multi-skill work such as ML plus reporting or data plus publication workflows. |
| Treat `approved_dispatch` as used | Dispatch can prove a skill was assigned, but not that full `SKILL.md` guidance affected six-stage artifacts. |

The selected minimal approach is:

1. Keep the public six stages unchanged.
2. Keep existing router scoring and route selection initially.
3. Add a `Skill Use Gate` that fully loads selected skills before they can become `used`.
4. Add one `skill_usage` truth object.
5. Make final reports and governance gates trust only `skill_usage` for skill usage claims.

## 4. Binary State Definition

### `used`

A skill is `used` only when both conditions are true:

```text
full SKILL.md was loaded
+
the skill's requirements or workflow shaped at least one six-stage artifact
```

The evidence must be explicit and traceable.

Examples of acceptable artifact impact:

- `requirement_doc` adopts the skill's input/output boundaries, constraints, or acceptance criteria.
- `xl_plan` adopts the skill's native workflow, task sequence, or verification style.
- `plan_execute` follows the skill's execution steps, scripts, or checks.
- `phase_cleanup` or completion evidence reports concrete outputs shaped by the skill.

### `unused`

A skill is `unused` when it does not satisfy the `used` standard.

These cases are always `unused` unless later evidence proves otherwise:

- candidate only
- route-selected but not fully loaded
- frontmatter or description only
- hint only
- recommendation only
- consultation only
- dispatch only
- loaded but no artifact impact

## 5. Skill Use Gate

Add a small internal gate before any skill can be called `used`.

The gate has three responsibilities:

1. Resolve the selected skill's real `SKILL.md` path.
2. Load the complete `SKILL.md`, not only frontmatter or description.
3. Record immutable load evidence.

Required load evidence:

```json
{
  "skill_id": "scanpy",
  "skill_md_path": "bundled/skills/scanpy/SKILL.md",
  "skill_md_sha256": "...",
  "load_status": "loaded_full_skill_md",
  "loaded_at_stage": "skeleton_check"
}
```

Loading alone does not make a skill `used`. It only makes the skill eligible to become `used` after artifact impact is recorded.

## 6. `skill_usage` Data Model

Add one canonical usage object:

```json
{
  "skill_usage": {
    "schema_version": 1,
    "state_model": "binary_used_unused",
    "used_skills": [],
    "unused_skills": [],
    "loaded_skills": [],
    "evidence": []
  }
}
```

Field meanings:

| Field | Meaning |
|---|---|
| `loaded_skills` | Skills whose full `SKILL.md` was loaded. |
| `used_skills` | Skills that were fully loaded and have artifact impact evidence. |
| `unused_skills` | Skills that were routed, recommended, hinted, dispatched, or loaded but did not satisfy the `used` standard. |
| `evidence` | Traceable proof for each `used` skill. |

Recommended evidence row:

```json
{
  "skill_id": "scanpy",
  "skill_md_path": "bundled/skills/scanpy/SKILL.md",
  "skill_md_sha256": "...",
  "loaded_at_stage": "skeleton_check",
  "used_at_stages": ["requirement_doc", "xl_plan"],
  "impact_summary": "Requirement and plan adopt Scanpy-native AnnData loading, QC, neighbors, Leiden clustering, and marker-gene workflow.",
  "artifact_refs": [
    "requirement_doc.md",
    "xl_plan.md"
  ]
}
```

## 7. Relationship To Existing Fields

Existing fields may remain for compatibility during migration, but they are no longer authoritative for skill usage.

| Existing field | New interpretation |
|---|---|
| `specialist_recommendations` | Candidate or route recommendation only. Not usage proof. |
| `stage_assistant_hints` | Deprecated or internal hint only. Not usage proof. |
| `specialist_dispatch.approved_dispatch` | Dispatch assignment only. Not usage proof. |
| consultation receipts | Historical consultation artifact only. Not usage proof. |
| `native_skill_description` | Description metadata only. Not usage proof. |

Only `skill_usage.used_skills`, `skill_usage.unused_skills`, and `skill_usage.evidence` can support a final claim that a skill was or was not used.

## 8. Six-Stage Integration

The public six-stage model does not change.

The internal usage flow is:

```text
router selects candidate skill
  -> Skill Use Gate fully loads SKILL.md
  -> six-stage artifacts adopt relevant requirements or workflow
  -> skill_usage records impact evidence
  -> completion reports used / unused only from skill_usage
```

Stage responsibilities:

| Stage | Usage responsibility |
|---|---|
| `skeleton_check` | Freeze route selection and load the selected main skill through Skill Use Gate. |
| `deep_interview` | Use loaded skill requirements to sharpen questions when relevant. |
| `requirement_doc` | Record skill-shaped requirement boundaries, constraints, or acceptance criteria. |
| `xl_plan` | Record skill-shaped workflow steps and verification expectations. |
| `plan_execute` | Record concrete execution actions that follow the skill workflow. |
| `phase_cleanup` | Finalize `used` / `unused` from evidence, not from route metadata. |

The first migration should require the main routed skill to pass the Skill Use Gate. Additional skills may stay `unused` until a later multi-skill usage design makes them pass the same evidence standard.

## 9. User-Facing Reporting

User-facing reports should no longer expose weak participation categories such as:

- auxiliary hint
- reference skill
- consulted skill
- maybe used
- route assistant

The completion summary should use only binary language:

```text
Actually used skills:
- scanpy: full SKILL.md loaded and adopted in requirement_doc.md and xl_plan.md.

Unused routed skills:
- anndata: route_hint_only.
- scvi-tools: route_hint_only.
```

If there is no `skill_usage.evidence`, the completion summary must not claim the skill was used.

## 10. Governance Gates

Add or update gates around four rules.

### Gate 1: Old Fields Cannot Claim Usage

Fail if a completion claim treats any of these as usage proof:

- `specialist_recommendations`
- `stage_assistant_hints`
- `approved_dispatch`
- consultation receipts
- frontmatter or description metadata

### Gate 2: Used Skills Require Full Load Evidence

Every `used_skills` entry must have:

- `skill_md_path`
- `skill_md_sha256`
- `load_status = loaded_full_skill_md`

### Gate 3: Used Skills Require Artifact Impact

Every `used_skills` entry must have at least one evidence row with:

- `stage`
- `artifact_ref`
- `impact_summary`

### Gate 4: Touched But Unproven Skills Must Not Be Hidden

If a skill appears in routing, hints, recommendations, dispatch, or load evidence but does not satisfy the `used` standard, it must not be reported as used.

It must appear in `unused_skills` with a reason when the current runtime can enumerate that touched skill.

Final usage claims must not silently hide a touched but unproven skill.

Recommended unused reason codes:

```text
candidate_only
route_hint_only
recommendation_only
dispatch_without_verified_artifact_impact
not_loaded_full_skill_md
loaded_but_no_artifact_impact
```

## 11. Migration Plan

### Step 1: Establish `skill_usage` Truth Layer

Add `skill_usage` to runtime artifacts and make the selected main route skill pass the Skill Use Gate.

Initial target files likely include:

- `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- `scripts/runtime/VibeRuntime.Common.ps1`
- `scripts/runtime/Write-RequirementDoc.ps1`
- `scripts/runtime/Write-XlPlan.ps1`
- `scripts/runtime/Invoke-PlanExecute.ps1`
- runtime delivery acceptance gates

### Step 2: Switch User-Facing Truth To `skill_usage`

Completion summaries, host user briefings, and governance reports should trust only `skill_usage` for usage claims.

### Step 3: Reduce Old Concept Authority

Keep old fields during compatibility migration, but mark them as non-authoritative for usage.

The migration should not immediately delete old fields or rewrite router scoring.

## 12. Non-Goals

This design does not:

- change the public six stages
- add a seventh public stage
- rewrite router scoring
- physically delete skill directories
- automatically promote auxiliary skills to `used`
- keep `stage_assistant_hints` as a user-facing usage concept
- treat consultation or dispatch as usage proof

## 13. Acceptance Criteria

The cleanup is accepted when:

1. A routed main skill is fully loaded through the Skill Use Gate.
2. The runtime writes `skill_usage` with `used_skills`, `unused_skills`, `loaded_skills`, and `evidence`.
3. A skill can enter `used_skills` only with full `SKILL.md` load evidence and artifact impact evidence.
4. Final user-facing reports state only `used` and `unused`.
5. Gates fail if old routing, hint, consultation, or dispatch fields are used as proof of skill usage.
6. The public six-stage governed runtime contract remains unchanged.

## 14. Completion Language Policy

Agents must not say a skill was used unless `skill_usage.used_skills` contains it and `skill_usage.evidence` supports it.

Allowed:

```text
The run used scanpy; its full SKILL.md was loaded and its workflow shaped xl_plan.md.
```

Not allowed:

```text
The run used anndata because it appeared in stage_assistant_hints.
```

If evidence is absent, the correct language is:

```text
The skill was routed or mentioned, but it was not proven used.
```
