# Codex Default Target Root And Cross-Host Audit Execution Plan

## Internal Grade

`M` — single-agent, tightly scoped config/test fix with bounded audit.

## Steps

1. Add regression tests covering:
   - registry/SDK default root for `codex`
   - runtime fallback root for `codex`
   - non-codex target roots remain unchanged
2. Run the targeted tests and confirm failure before code changes.
3. Update:
   - `config/adapter-registry.json`
   - `adapters/index.json`
   - `packages/runtime-core/src/vgo_runtime/router_contract_support.py`
4. Re-run the targeted tests until green.
5. Inspect other hosts against their settings-map and install-mode contracts, then summarize whether the same contradiction exists.

## Ownership Boundaries

- Tests:
  - `tests/unit/test_adapter_sdk.py`
  - `tests/unit/test_installer_adapter_registry_target_roots.py`
  - `tests/unit/test_router_contract_support.py`
- Runtime/config:
  - `config/adapter-registry.json`
  - `adapters/index.json`
  - `packages/runtime-core/src/vgo_runtime/router_contract_support.py`

## Verification Commands

```bash
pytest -q tests/unit/test_adapter_sdk.py tests/unit/test_installer_adapter_registry_target_roots.py tests/unit/test_router_contract_support.py
```

## Delivery Acceptance Plan

- Accept only if the targeted test suite passes.
- Accept only if `codex` now resolves to `~/.codex` by default when `CODEX_HOME` is unset.
- Accept only if the other hosts audit is evidence-backed.

## Completion Language Rules

- No “fixed” or “done” wording without passing test output.
- Report remaining risk separately from verified changes.

## Rollback Rules

- If changing `codex` default root breaks unrelated host tests, stop and isolate the failing dependency before widening scope.

## Phase Cleanup Expectations

- Leave behind only the requirement doc, execution plan, code changes, and test evidence.
