# Current Router Runtime Old-Role Field Erasure Design

> Historical / Retired Note: This design intentionally names retired routing
> role fields as cleanup targets. The current routing model is
> `skill_candidates -> skill_routing.selected -> skill_execution_lock -> selected_skill_execution -> skill_usage`.
> Old role fields discussed here are debt targets, not current runtime states.

Date: 2026-05-02

## Goal

Remove old role-field semantics from the current router and runtime-core paths
without changing canonical `$vibe` behavior.

The current routing and usage chain must remain:

```text
skill_candidates
  -> skill_routing.selected
  -> skill_execution_lock
  -> selected_skill_execution
  -> skill_usage.used / skill_usage.unused / skill_usage.evidence
```

`docs/governance/current-runtime-field-contract.md` is the authoritative
current runtime field contract; this design records cleanup scope and defers to
that contract for the live field chain.

The cleanup target is the implementation residue that still reads, derives, or
filters by old role fields:

```text
route_authority_candidates
stage_assistant_candidates
route_authority_eligible
legacy_role
_legacy_role
_legacy_stage_assistant_candidates
```

The current manifest surface is already ready for this cut because
`config/pack-manifest.json` no longer needs `route_authority_candidates` or
`stage_assistant_candidates` as current pack fields. The remaining debt is in
the router/runtime implementation, custom admission metadata, runtime packet
assembly, and tests that still tolerate the old role model.

## Problem

Recent routing cleanup already blocks old packet fields such as
`legacy_skill_routing`, `specialist_recommendations`, and
`stage_assistant_hints` from current output paths. That is not enough.

The current code still contains a second class of retired terminology: old role
fields that describe whether a skill was a route authority, a stage assistant,
or an old fallback role. These fields are mostly hidden from public output, but
they still exist in current implementation paths.

That creates a mismatch:

- current docs teach one model based on candidates, selected skills, execution,
  and usage evidence;
- router/runtime-core still contains old role-specific readers and internal
  fields;
- public output cleanup currently strips old fields defensively, but the current
  selection path may still generate or consume them internally;
- future contributors can reintroduce old role semantics without tripping the
  existing debt gate unless those fields become explicit retired terms.

The desired end state is not a cosmetic rename. The current implementation must
stop depending on these fields.

## Non-Goals

This slice must not:

- change the six governed `$vibe` stages;
- change canonical entry launch behavior;
- rebuild the pack scoring algorithm;
- delete bundled skills;
- prune skill packs;
- redefine `selected` as `used`;
- do a broad historical documentation archive;
- deploy the branch to Codex;
- remove explicitly marked retired-behavior fixtures only to make grep output
  cleaner.

## Current Field Contract

Current candidate selection may use:

```text
skill_candidates
task_allow
routing rule positive/negative keywords
requires_positive_keyword_match
score
fallback threshold
explicit requested skill
custom admission _route_usable
```

Current candidate selection must not use:

```text
route_authority_candidates
stage_assistant_candidates
route_authority_eligible
legacy_role
_legacy_role
_legacy_stage_assistant_candidates
```

Current public route output may expose ranking facts:

```text
selected_candidate
candidate_ranking
candidate_selection_reason
candidate_selection_score
candidate_relevance_score
candidate_top1_top2_gap
candidate_filtered_out_by_task
```

It must not expose old role identity fields.

## Architecture

### PowerShell Router

Primary files:

```text
scripts/router/modules/41-candidate-selection.ps1
scripts/router/resolve-pack-route.ps1
```

`Get-PackSkillCandidates` should read only `skill_candidates`.

The current fallback from `route_authority_candidates` and
`stage_assistant_candidates` should be removed from the current module. If a
pack has no `skill_candidates`, it has no current candidates.

`Select-PackCandidate` should stop generating:

```text
_legacy_role
_legacy_stage_assistant_candidates
```

It should return only current selection fields:

```text
selected
score
reason
ranking
top1_top2_gap
filtered_out_by_task
_selection_usable
relevance_score
```

`resolve-pack-route.ps1` should stop reading `route_authority_eligible` as a
route usability fallback. Route usability should come from:

```text
_selection_usable
_route_usable
selected_candidate is present
```

Public output cleanup may continue to strip old fields as a defensive guard, but
that guard must not be the primary mechanism that makes the route output clean.

### Python Runtime-Core

Primary files:

```text
packages/runtime-core/src/vgo_runtime/router_contract_selection.py
packages/runtime-core/src/vgo_runtime/router_contract_runtime.py
packages/runtime-core/src/vgo_runtime/custom_admission.py
```

`get_pack_skill_candidates()` should read only `skill_candidates`.

`select_pack_candidate()` should remove:

```text
INTERNAL_LEGACY_ROLE
INTERNAL_LEGACY_STAGE_ASSISTANTS
candidate_legacy_role()
stage_assistant_ranked
route_authority allowlist
stage_assistant allowlist
```

Candidate row public-cleanup helpers may keep old-field stripping as a defensive
allowance, but normal current selection results should not generate old fields.

`custom_admission.py` should stop writing `route_authority_eligible`. It should
write a neutral internal field instead:

```text
_route_usable
```

The user-facing custom admission summary should explain the current metadata by
`trigger_mode`, `dispatch_phase`, `binding_profile`, and related current fields,
not by route-authority language.

### Runtime Packet Assembly

Primary file:

```text
scripts/runtime/Freeze-RuntimeInputPacket.ps1
```

Sibling recommendation logic should stop reading `route_authority_eligible`.

If XL sibling recommendations need a current eligibility check, they should use
neutral current ranking facts:

```text
candidate exists
candidate is not the selected runtime skill
candidate is not already recommended
candidate score >= threshold
candidate score is close enough to selected candidate score
```

No route-authority role field should be required to produce additional bounded
recommendations.

### Policy And Gate

Primary files:

```text
config/current-routing-debt-erasure.json
scripts/verify/vibe-current-routing-debt-gate.ps1
tests/runtime_neutral/test_current_routing_debt_erasure_policy.py
tests/runtime_neutral/test_current_routing_debt_gate.py
```

The current-routing debt policy should add these terms to the retired/high-risk
scan:

```text
route_authority_candidates
stage_assistant_candidates
route_authority_eligible
legacy_role
_legacy_role
_legacy_stage_assistant_candidates
```

Current paths should treat those terms as P1 findings unless the line is:

- in an explicit retired or legacy path;
- in a historical document or retired-context section;
- in a gate or test assertion that forbids the term;
- in this design or implementation-plan history under the approved
  `docs/superpowers/*` retired-context allowance.

## Data Flow

The target current flow is:

```text
config/pack-manifest.json
  pack.skill_candidates
    -> Get-PackSkillCandidates / get_pack_skill_candidates
    -> Select-PackCandidate / select_pack_candidate
    -> route result selected_candidate + candidate_ranking
    -> skill_routing.selected
    -> selected_skill_execution
    -> skill_usage.used / skill_usage.unused / skill_usage.evidence
```

The removed flow is:

```text
route_authority_candidates
stage_assistant_candidates
  -> fallback candidate source
  -> legacy_role / _legacy_role
  -> _legacy_stage_assistant_candidates
  -> route_authority_eligible
  -> sibling recommendation eligibility
```

After this cleanup, `candidate_ranking` expresses ranking and score facts only.
It does not express old role identity.

## Error Handling

### Pack Missing `skill_candidates`

Current router paths should return no candidates for that pack. They should not
recover from old role fields.

This makes manifest errors visible and prevents stale compatibility fields from
silently driving current routing.

### Old Manifest-Only Fixtures

Current behavior tests should prove that old manifest-only packs do not produce
current candidates.

Retired-behavior tests may still use old fields, but the assertion must be that
old fields are ignored, isolated, or kept out of current output.

### Custom Admission Without `_route_usable`

Generated custom admission metadata should always include `_route_usable`.

Defensive readers may fall back to "selected candidate is present" if custom
metadata is absent, but they must not fall back to `route_authority_eligible`.

### XL Sibling Recommendation

Sibling recommendation should rely on score and ranking facts, not on role
eligibility fields.

The safe neutral rule is:

```text
recommend sibling candidate only if it exists, is not already selected or seen,
has enough score, and is close enough to the selected candidate score
```

## Testing Strategy

The test strategy should prove both absence and preservation:

- absence: old role fields are no longer current inputs, outputs, or internal
  result fields;
- preservation: normal routing still selects the expected skills for focused
  route cases.

Focused tests should cover:

```text
tests/unit/test_router_contract_selection_guards.py
tests/runtime_neutral/test_runtime_route_output_shape.py
tests/runtime_neutral/test_router_bridge.py
tests/runtime_neutral/test_current_routing_debt_gate.py
tests/runtime_neutral/test_current_routing_debt_erasure_policy.py
```

Required assertions:

1. Python old manifest-only pack does not produce candidates.
2. PowerShell old manifest-only pack does not produce candidates.
3. Python current selection result does not generate old role fields.
4. PowerShell current selection result does not generate old role fields.
5. Custom admission writes `_route_usable` and does not write
   `route_authority_eligible`.
6. Runtime packet assembly does not read `route_authority_eligible`.
7. Public route output still contains no old role fields.
8. The current debt gate scans the new retired role terms.
9. Focused route probes still select expected packs and skills.

## Verification Commands

Minimum focused verification:

```powershell
python -m pytest tests/unit/test_router_contract_selection_guards.py -q
python -m pytest tests/runtime_neutral/test_runtime_route_output_shape.py -q
python -m pytest tests/runtime_neutral/test_current_routing_debt_gate.py -q
python -m pytest tests/runtime_neutral/test_current_routing_debt_erasure_policy.py -q
python -m pytest tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_simplified_skill_routing_contract.py -q
powershell.exe -NoLogo -NoProfile -File .\scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
```

Optional broader route smoke when time permits:

```powershell
powershell.exe -NoLogo -NoProfile -File .\scripts\verify\vibe-pack-routing-smoke.ps1
```

## Implementation Slices

### Slice 1: Policy And Gate

Update the current-routing debt policy and gate tests so the old role-field
terms are treated as retired fields before implementation begins.

Expected initial result: tests fail against current code because old role fields
still appear in current router/runtime-core paths.

### Slice 2: Python Runtime-Core

Remove old role fallback and old role field generation from runtime-core.

Expected result: Python router tests prove `skill_candidates` is the only
current candidate source and current selection rows have no old role fields.

### Slice 3: PowerShell Router

Mirror the Python runtime-core cleanup in PowerShell.

Expected result: PowerShell router tests match Python behavior for old
manifest-only packs and focused route probes.

### Slice 4: Runtime Packet Assembly

Remove `route_authority_eligible` from sibling recommendation logic and replace
it with neutral score/ranking checks.

Expected result: runtime packet tests and governed runtime bridge tests still
pass without old role-field dependency.

### Slice 5: Regression Closure

Run the focused verification matrix and the current-routing debt gate. If route
scoring or candidate selection drifts, fix the scoring logic directly rather
than reintroducing old role fields.

## Risks

### Hidden Test Dependency On Old Manifest Fallback

Some tests may still build old pack fixtures with only
`route_authority_candidates` or `stage_assistant_candidates`.

Resolution:

- current tests should migrate to `skill_candidates`;
- retired compatibility tests should be renamed or kept under explicit
  retired-behavior boundaries.

### Python / PowerShell Drift

The repo has two router implementations that must remain behaviorally aligned.

Resolution:

- use shared route cases that exercise both Python `route_prompt()` and
  PowerShell `resolve-pack-route.ps1`;
- keep old-role absence assertions in both paths.

### False Confidence From Public Output Scrubbing

Public output stripping can hide internal debt.

Resolution:

- keep public scrubbing as a defensive guard;
- add tests that inspect current selection internals or source text to prove the
  old fields are not generated in the first place.

## Success Criteria

This cleanup is complete only when all of these are true:

```text
1. config/pack-manifest.json still has no route_authority_candidates or stage_assistant_candidates.
2. Current router code no longer reads route_authority_candidates or stage_assistant_candidates as candidate fallback.
3. Current selection results no longer generate legacy_role or _legacy_role.
4. Current selection results no longer generate _legacy_stage_assistant_candidates.
5. Custom admission no longer writes route_authority_eligible.
6. Runtime packet assembly no longer reads route_authority_eligible.
7. Public route output remains free of old role fields.
8. The current debt gate treats the old role fields as retired terms.
9. Focused route probes still pass for both Python and PowerShell paths.
```

## Review Gate

After this design is committed, implementation must wait for explicit user
approval and then proceed through a separate implementation plan.
