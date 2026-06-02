# Codex Default Target Root And Cross-Host Audit

## Goal

Make `codex` default installation and runtime target-root resolution land on the real host root so install results remain directly discoverable through `$vibe`, and verify whether other public hosts suffer from the same class of mismatch.

## Deliverable

- Registry and runtime fallback updated so `codex` defaults to real `~/.codex` when `CODEX_HOME` is unset.
- Regression tests proving the new default behavior.
- A bounded audit result for the other public hosts explaining whether they share the same mismatch.

## Constraints

- Do not revert existing user changes.
- Preserve current public semantics for `claude-code`, `cursor`, `windsurf`, `openclaw`, and `opencode` unless evidence shows the same contradiction.
- Keep edits minimal and evidence-backed.

## Acceptance Criteria

- `config/adapter-registry.json` and `adapters/index.json` no longer default `codex` to `.vibeskills/targets/codex`.
- runtime fallback in `packages/runtime-core/src/vgo_runtime/router_contract_support.py` no longer defaults `codex` to `.vibeskills/targets/codex`.
- targeted tests pass after the change.
- the final report explicitly states whether other hosts have the same issue.

## Product Acceptance Criteria

- For `codex`, “installed” should mean the current host can discover `$vibe` by default unless the operator explicitly chooses an isolated root.
- Other hosts should not be changed merely because they also have host-managed settings surfaces; the mismatch must be real, not inferred.

## Manual Spot Checks

- Read registry and runtime fallback code for `codex`.
- Compare each host's default target root against its declared host settings/discovery surface.
- Run targeted unit/integration tests for registry, SDK, and runtime fallback behavior.

## Completion Language Policy

- Do not claim the fix is complete without fresh test evidence.
- Distinguish “changed codex defaults” from “audited other hosts.”

## Delivery Truth Contract

- Report exact files changed.
- Report exact test commands run and whether they passed.
- If any residual mismatch remains elsewhere, state it directly.

## Non-Goals

- Re-architect all host target-root semantics.
- Change host-managed boundaries for non-codex adapters without evidence.

## Autonomy Mode

- Single-session governed execution with targeted verification.

## Inferred Assumptions

- The user wants the code-level default fixed, not just prompt documentation.
- `$vibe` discoverability is the codex-specific success criterion that was previously violated.
