# Rabbit Follow-Up Three Comments Design

## Context

PR 228 has three unresolved CodeRabbit inline threads after the previous
follow-up patch. The branch is `review/pr226-pr227-combined`.

This design covers only the three currently unresolved actionable threads:

1. Markdown heading-level lint in the previous implementation plan.
2. Empty skill execution lock and lock resolution payload fallback behavior.
3. Stable CLI failure handling in the test baseline audit wrapper.

Optional low-value nitpicks and unrelated refactors remain out of scope.

## Verified Findings

### Markdown Heading Increment

`docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md` has a
top-level `#` heading and then jumps directly to `### Task 1`. This violates
Markdown heading increment rules. The minimal fix is to insert a `## Tasks`
section before the task headings and leave existing `### Task N` headings in
place.

### Empty Lock Payload Fallback

`packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`
currently returns any dictionary found in `execution_manifest.skill_execution_lock`,
`execution_manifest.specialist_accounting.skill_execution_lock`,
`execution_manifest.specialist_lock_resolution`, or
`execution_manifest.specialist_accounting.specialist_lock_resolution`, even when
the dictionary is empty. An empty `{}` is not an actual lock or resolution
payload and should not suppress fallback to a populated lower-priority source.

For `_load_skill_execution_lock`, empty manifest/accounting payloads must fall
through to `runtime_packet.skill_execution_lock`. For
`_load_specialist_lock_resolution`, empty manifest/accounting payloads must fall
through to the next manifest source and then return `{}` only when no non-empty
resolution exists.

### Test Baseline Audit CLI Failures

`packages/verification-core/src/vgo_verify/test_baseline_audit.py` lets expected
gate-wrapper failures escape from `main()` as Python tracebacks. Missing policy
files, malformed policies, pytest collection failures, unknown layer IDs, and
artifact write failures are expected CLI failure modes. They should be reported
as concise stderr messages with deterministic non-zero exit codes.

The successful path must keep its current behavior: collect-only returns `0`,
successful run-layer returns the layer exit code, and a subprocess timeout that
is already represented as a run result keeps returning `124`.

## Design

### Documentation Fix

Add `## Tasks` after the front matter separator in
`docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md`. This keeps
the document structure `# -> ## -> ###` without rewriting the existing plan.

### Runtime Loader Fix

Update `_load_skill_execution_lock` to return only non-empty dictionaries from:

1. `execution_manifest["skill_execution_lock"]`
2. `execution_manifest["specialist_accounting"]["skill_execution_lock"]`
3. `runtime_packet["skill_execution_lock"]`

Update `_load_specialist_lock_resolution` to return only non-empty dictionaries
from:

1. `execution_manifest["specialist_lock_resolution"]`
2. `execution_manifest["specialist_accounting"]["specialist_lock_resolution"]`

The final fallback remains `{}`. This preserves source precedence while treating
empty containers as absent payloads.

### CLI Error Handling

Wrap the operational body of `test_baseline_audit.main()` in a narrow
`try/except` block that catches expected CLI failures:

- `PolicyError`
- `RuntimeError`
- `OSError`
- `json.JSONDecodeError`

On those failures, print a single-line `[ERROR] ...` message to `stderr` and
return a deterministic non-zero exit code. Policy/config errors should return
`2`; runtime, collection, layer, artifact, and I/O errors should return `1`.

Do not catch `KeyboardInterrupt`, `SystemExit`, or broad `Exception`. Unexpected
programming errors should still surface normally during development.

## Tests

Add or update focused tests before implementation:

1. A runtime delivery acceptance test where
   `execution_manifest.skill_execution_lock` and
   `specialist_accounting.skill_execution_lock` are `{}`, while the runtime
   packet contains an active lock. The report must treat the lock as active.
2. A runtime delivery acceptance test where empty manifest resolution falls
   through to non-empty accounting resolution.
3. Test baseline audit CLI tests showing missing or malformed policy input
   returns a stable error code and stderr without `Traceback`.
4. A test baseline audit CLI test showing collection failure returns a stable
   error code and stderr without `Traceback`.

## Validation

Run these checks after implementation:

1. `pytest tests/runtime_neutral/test_runtime_delivery_acceptance.py packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py -q`
2. `pytest tests/runtime_neutral/test_test_baseline_audit.py -q`
3. `git diff --check`
4. GitHub review-thread query for PR 228 to confirm unresolved thread count.
5. `gh pr checks 228 --repo foryourhealth111-pixel/Vibe-Skills`

If normal `git push` still fails with GitHub HTTPS connection resets, use the
existing GitHub Git Database API path and verify remote/local tree equality.

## Non-Goals

- Do not introduce a full CLI exit-code taxonomy or a new public API module.
- Do not restructure `runtime_delivery_acceptance_runtime.py`.
- Do not rewrite the existing two-comments plan beyond the heading fix.
- Do not resolve optional Rabbit comments that are not unresolved actionable
  threads.
