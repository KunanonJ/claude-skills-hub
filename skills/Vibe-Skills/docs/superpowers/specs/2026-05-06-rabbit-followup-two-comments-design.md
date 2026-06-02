# Rabbit Follow-Up Two Comments Design

## Context

PR 228 has two unresolved CodeRabbit inline threads after the previous review
cleanup. The branch is `review/pr226-pr227-combined`.

The fix is intentionally narrow: address only the two still-unresolved,
actionable comments and avoid unrelated installer refactoring or optional
nitpick cleanup.

## Findings

### Plan Checklist Wording

`docs/superpowers/plans/2026-05-06-rabbit-review-followup.md` uses the phrase
`host approved additions` in a checklist sentence. CodeRabbit's grammar finding
is valid because the phrase acts as a compound modifier. The correction is
`host-approved additions`.

### Installer Helper Finding No Longer Applies

`scripts/install/Install-VgoAdapter.ps1` does not currently define
`Test-VgoSkillEntryPoint`. Repository search finds that symbol only in prior
spec and plan documents, not in installer code. The original remove-helper
finding no longer matches the current repository state.

## Design

Use the minimal-fix path:

1. Replace `host approved additions` with `host-approved additions` in the
   follow-up plan checklist.
2. Record that the `Test-VgoSkillEntryPoint` removal is no longer applicable
   because current installer code does not contain that function.

No installer behavior should change because this item requires only a design
document correction against current repository state.

## Validation

After implementation, validate with:

1. `rg -n "Test-VgoSkillEntryPoint" scripts tests packages -S` to confirm no
   stale code or test references remain. The design and implementation plan may
   still mention the removed helper by name.
2. The targeted generated nested bundled installer test:
   `pytest tests/runtime_neutral/test_generated_nested_bundled.py::InstallTimeGeneratedNestedBundledTests::test_powershell_fallback_in_place_internal_corpus_prunes_and_sanitizes -q`
3. `git diff --check`.
4. GitHub review-thread and PR-check queries after the branch update.

## Non-Goals

- Do not hoist or restructure unrelated PowerShell helpers.
- Do not handle optional low-value nitpicks unless they become unresolved
  actionable threads.
- Do not change installer public API documentation for a helper that has no
  current consumer.
