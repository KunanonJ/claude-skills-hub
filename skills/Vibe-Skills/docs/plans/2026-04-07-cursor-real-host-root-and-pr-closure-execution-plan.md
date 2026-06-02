# Cursor Real Host Root And PR Closure Execution Plan

## Internal Grade

`XL` — wave-sequential execution across tests, config/runtime, docs, verification, and PR publication.

## Waves

### Wave 1

- add failing tests for Cursor real-host defaults
- run targeted tests and confirm failure

### Wave 2

- update registry/index/runtime fallback for Cursor
- update public docs/prompts for Cursor defaults

### Wave 3

- run targeted verification suite
- inspect diff for unintended drift

### Wave 4

- commit the converged host-root work
- push the branch
- open a PR

## Ownership Boundaries

- code/config:
  - `config/adapter-registry.json`
  - `adapters/index.json`
  - `packages/runtime-core/src/vgo_runtime/router_contract_support.py`
- tests:
  - unit and integration tests covering target-root semantics and docs
- docs:
  - install prompts/reference docs only

## Verification Commands

```bash
pytest -q tests/unit/test_adapter_sdk.py tests/unit/test_installer_adapter_registry_target_roots.py tests/unit/test_router_contract_support.py tests/unit/test_adapter_registry_support.py tests/runtime_neutral/test_cursor_managed_preview.py tests/integration/test_multi_host_real_host_root_docs.py
```

## Delivery Acceptance Plan

- accept only if Cursor defaults to `~/.cursor`
- accept only if the verification command passes
- accept only if a PR is created successfully

## Completion Language Rules

- do not say the work is shipped until the PR exists

## Rollback Rules

- if PR publication fails due to auth or remote mismatch, report that exact blocker with the verified local state

## Phase Cleanup Expectations

- leave behind requirement/plan docs, verified code/docs changes, and PR metadata
