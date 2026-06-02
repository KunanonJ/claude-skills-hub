# Rabbit Review Follow-up Design

Date: 2026-05-06

## Context

PR 228 still has six unresolved CodeRabbit inline review threads after commit
`4049728a`. Each thread was checked against the current branch before this
design was written. The remaining comments are still valid and can be fixed
with narrow changes.

## Scope

This change addresses only the still-valid Rabbit findings:

- Keep the specialist execution lock plan snippet aligned with the current
  runtime semantics.
- Let Python delivery acceptance derive active lock IDs from `locked_dispatch`
  when `locked_skill_ids` is absent.
- Convert pytest collection timeouts into structured, layer-aware
  `RuntimeError` messages.
- Make the PowerShell installer fallback handle in-place internal skill corpus
  materialization the same way as the Python materializer.
- Make retired consultation fallback shims non-throwing when the legacy helper
  is absent.
- Exclude host-deferred and host-rejected skills from execution locks.

## Design

The verifier fix introduces a single helper in
`runtime_delivery_acceptance_runtime.py` that normalizes lock IDs from
`locked_skill_ids` first and falls back to `locked_dispatch[*].skill_id`. Both
lock evaluators use that helper so lock resolution and selected-lock
reconciliation share the same active lock view.

The test baseline audit fix wraps the collect-only runner call in a
`subprocess.TimeoutExpired` handler. The raised `RuntimeError` includes the
pytest arguments, source layer IDs, timeout, and any captured stdout or stderr
from the exception.

The installer fix removes the in-place early return from
`Sync-VgoInternalSkillCorpus`. It computes the selected skill set first,
prunes unselected child directories only in in-place mode, skips self-copy, and
still sanitizes every selected skill entrypoint to `SKILL.runtime-mirror.md`.

The runtime shim fix changes the missing-retired-helper fallbacks to no-op
functions that return `$null`. This prevents old receipts from breaking active
rendering paths when the legacy helper file is absent.

The execution lock fix derives a normalized host exclusion set from
`deferred_skill_ids` and `rejected_skill_ids`. Every lock source path checks the
set before adding records: current selected records, host approvals, previous
lock dispatch, previous lock ID-only fallback, and previous routing fallback.

## Testing

Targeted tests should cover each behavior:

- `packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py`
- `tests/runtime_neutral/test_test_baseline_audit.py`
- `tests/runtime_neutral/test_current_routing_contract_cleanup.py`
- `tests/runtime_neutral/test_skill_execution_lock_contract.py`
- `packages/runtime-core/src/vgo_runtime/test_skill_execution_lock_reconciliation.py`
- A focused PowerShell installer regression for in-place internal corpus
  materialization.

Final verification should also run the repository's Python validation gate if
the targeted tests pass.
