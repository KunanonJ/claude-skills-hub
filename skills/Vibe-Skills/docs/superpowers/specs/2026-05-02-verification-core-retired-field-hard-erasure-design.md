# Verification-Core Retired Field Hard Erasure Design

## Summary

The current terminology hard-cleanup gate passes, but it still reports 15
`review` hits in verification-core audit modules. All 15 hits come from current
audit code reading retired routing fields:

- `route_authority_candidates`
- `stage_assistant_candidates`

This design hard-clears those fields from the current verification-core audit
surface. The audit modules will no longer read, branch on, count, or output
values from those retired fields. The terminology gate policy will also stop
classifying these modules as compatibility-review exceptions, so the same
retired-field usage becomes a failure if it returns.

## Current Evidence

Current branch state before this design:

```text
main...origin/main [ahead 28]
```

The Windows test baseline was recently closed:

```text
python -m pytest tests\contract tests\unit -q
284 passed
```

The terminology cleanup gate currently passes but still has review debt:

```text
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
status: pass
summary.fail_count: 0
summary.review_count: 15
```

The 15 review hits are concentrated in:

- `packages/verification-core/src/vgo_verify/global_pack_consolidation_audit.py`
- `packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py`
- `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`
- `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`

Those four files are currently listed in
`config/routing-terminology-hard-cleanup.json` under
`compatibility_review_files`, which means retired-field reads are classified as
review debt rather than blocking debt.

## Goals

1. Remove all current verification-core reads of `route_authority_candidates`
   and `stage_assistant_candidates`.
2. Ensure verification-core audit behavior is based only on current inputs such
   as `skill_candidates`, `defaults_by_task`, skill files, replacement policy,
   and current output fields.
3. Remove the four verification-core audit modules from the terminology gate's
   compatibility-review exception list.
4. Tighten the terminology hard-cleanup test so `review_count == 0` and
   `review == []` are required.
5. Add behavior tests proving retired-field fixture values cannot influence
   audit rows, risk signals, current-role decisions, JSON, CSV, or Markdown
   output.

## Non-Goals

- Do not modify `config/pack-manifest.json` business content unless a test
  exposes a real current-manifest retired-field leak.
- Do not clean historical plans, historical specs, or old dated governance
  documents.
- Do not change runtime/router/install behavior.
- Do not introduce a shared verification-core helper for this pass.
- Do not split large audit or runtime files as part of this change.
- Do not install, deploy, push, or mutate host roots.

## Design

### 1. Terminology Gate Escalation

The implementation should first remove these files from
`compatibility_review_files`:

- `packages/verification-core/src/vgo_verify/global_pack_consolidation_audit.py`
- `packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py`
- `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`
- `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`

`tests/runtime_neutral/test_routing_terminology_hard_cleanup.py` should then
require:

```text
summary.review_count == 0
review == []
```

The first focused gate run is expected to fail before the audit modules are
cleaned. That failure is intentional; it proves the gate catches the current
retired-field residue.

### 2. Global Pack Consolidation Audit

`global_pack_consolidation_audit.py` currently models retired role split
compatibility through:

- `compat_direct_candidate_count`
- `compat_stage_candidate_count`
- `has_compat_role_split`
- `_compat_candidates(...)`
- `_has_compat_role_split(...)`

The current-only design removes retired role splitting from the audit logic.
Risk scoring and output should be based on current fields:

- `skill_candidates`
- `defaults_by_task`
- skill metadata and content signals
- overlap and breadth signals
- current recommendations

Retired direct/stage split fields must not influence:

- priority calculation;
- risk score;
- CSV columns;
- Markdown tables;
- JSON summary fields;
- next-action wording.

If existing tests assert compat split counters, they should be rewritten to
assert current-only candidate counts and absence of retired positive terms.

### 3. Code-Quality Pack Audit

`code_quality_pack_consolidation_audit.py` currently has `_current_role()` read
the retired fields and return:

- `compat_direct_candidate`
- `compat_stage_candidate`

After hard erasure, `_current_role()` should use only:

- whether a skill is in `skill_candidates`;
- whether a skill is selected in `defaults_by_task`;
- whether a skill has been removed from the pack;
- fixed current target policies for keep/delete/defer decisions.

It must no longer return compatibility direct/stage roles. Old fields in an
input fixture should be ignored rather than treated as current signal.

### 4. Bio-Science Pack Audit

`bio_science_pack_consolidation_audit.py` currently builds its pack index by
iterating over:

```text
skill_candidates
route_authority_candidates
stage_assistant_candidates
```

After hard erasure, the index should use only `skill_candidates` plus
`defaults_by_task`. `_current_role()` should return current states only, for
example:

- `skill_candidate`
- `default`
- `candidate`
- `removed_from_pack`

Exact names should follow existing current test language, but no returned value
may encode retired direct/stage role semantics.

### 5. ML Skills Pruning Audit

`ml_skills_pruning_audit.py` should drop retired-field reads from both
`_pack_skill_index()` and `_current_pack_role()`. Keep/delete/migration
decisions should use only current inputs:

- `skill_candidates`
- `defaults_by_task`
- `OWNER_SKILLS`
- skill file existence and content length
- replacement/default/current target policy

Existing decisions that depend on `compat_stage_candidate` or
`compat_direct_candidate` should be rewritten to use current candidate/default
state or explicit target policy. Retired fields should not grant keep status,
stage status, or direct-owner status.

## Testing

### Gate Tests

`tests/runtime_neutral/test_routing_terminology_hard_cleanup.py` should require
zero compatibility-review hits:

```text
summary.review_count == 0
review == []
```

The gate command should end with:

```text
status: pass
summary.fail_count: 0
summary.review_count: 0
review: []
```

### Audit Behavior Tests

Each affected audit test should include a fixture where old fields are present
but must be ignored:

```python
pack = {
    "id": "...",
    "skill_candidates": ["current-skill"],
    "route_authority_candidates": ["retired-only-direct"],
    "stage_assistant_candidates": ["retired-only-stage"],
}
```

The expected behavior is:

- `retired-only-direct` is absent from audit rows;
- `retired-only-stage` is absent from audit rows;
- risk scores and current roles are calculated from `skill_candidates`;
- output artifacts do not include the retired field names;
- JSON, CSV, and Markdown do not include retired-only candidate values.

### Output Term Tests

The existing `assert_no_retired_positive_output_terms(...)` pattern should
remain in place and cover:

- artifact dictionaries serialized to JSON;
- CSV output text;
- Markdown output text.

If a retired field name or retired routing phrase leaks into generated output,
the tests should fail.

### Acceptance Commands

Focused acceptance:

```powershell
python -m pytest tests\runtime_neutral\test_routing_terminology_hard_cleanup.py tests\runtime_neutral\test_global_pack_consolidation_audit.py tests\runtime_neutral\test_code_quality_pack_consolidation_audit.py tests\runtime_neutral\test_bio_science_pack_consolidation_audit.py tests\runtime_neutral\test_ml_skills_pruning_audit.py -q
```

Gate acceptance:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
```

Regression acceptance:

```powershell
python -m pytest tests\contract tests\unit tests\runtime_neutral -q
git diff --check
```

## Error Handling

- If a pack lacks `skill_candidates`, the audit should treat the current
  candidate list as empty or follow its existing empty-candidate behavior.
- If old fields appear in an input fixture, the audit should ignore them without
  raising. This keeps old fixture data readable while preventing compatibility
  reads from becoming current behavior.
- If old fields appear in the four current audit modules after policy
  escalation, the terminology gate should fail.
- If real `config/pack-manifest.json` still contains retired fields, existing
  runtime-neutral tests should catch that as manifest drift; this design does
  not add a separate manifest migration.

## Implementation Order

1. Tighten terminology hard-cleanup policy and tests so the 15 review hits become
   blocking current-surface failures.
2. Clean `global_pack_consolidation_audit.py` and
   `code_quality_pack_consolidation_audit.py`.
3. Clean `bio_science_pack_consolidation_audit.py` and
   `ml_skills_pruning_audit.py`.
4. Run focused audit tests, terminology gates, routing debt gate, full
   `tests/contract tests/unit tests/runtime_neutral`, and `git diff --check`.

## Rollback

The implementation should be committed in small stages so rollback stays
targeted:

- If the gate escalation is too strict, revert the policy/test commit.
- If global/code-quality audit cleanup fails, revert that audit cleanup commit.
- If bio-science/ml audit cleanup fails, revert that audit cleanup commit.
- No rollback path should require touching runtime, router, installer, or host
  deployment state.

## Success Criteria

The cleanup is complete when:

- `vibe-routing-terminology-hard-cleanup-scan.ps1 -Json` reports `status: pass`.
- `summary.fail_count == 0`.
- `summary.review_count == 0`.
- `review == []`.
- `rg "route_authority_candidates|stage_assistant_candidates" packages/verification-core/src/vgo_verify/*_audit.py` has no hits in the four targeted audit modules.
- Old fixture values from retired fields cannot influence audit rows or generated JSON/CSV/Markdown output.
- `vibe-current-routing-debt-gate.ps1 -Json` remains `P0/P1/P2 = 0/0/0`.
- `tests/contract tests/unit tests/runtime_neutral` pass.
- No install, deployment, push, or host-root mutation happens.
