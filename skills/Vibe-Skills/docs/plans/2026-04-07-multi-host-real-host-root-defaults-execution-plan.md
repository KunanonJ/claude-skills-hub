# Multi-Host Real Host Root Defaults Execution Plan

## Internal Grade

`M` — bounded multi-file config/doc update with targeted verification.

## Steps

1. Add failing tests for the requested hosts:
   - registry target-root semantics
   - SDK/installer default-root resolution
   - runtime fallback resolution
2. Run targeted tests and confirm failure before the code change.
3. Update:
   - `config/adapter-registry.json`
   - `adapters/index.json`
   - `packages/runtime-core/src/vgo_runtime/router_contract_support.py`
4. Update public docs that still describe isolated fallback roots as defaults for these hosts.
5. Re-run the targeted test suite and a small cross-host regression suite.

## Ownership Boundaries

- Runtime/config:
  - `config/adapter-registry.json`
  - `adapters/index.json`
  - `packages/runtime-core/src/vgo_runtime/router_contract_support.py`
- Tests:
  - `tests/unit/test_adapter_sdk.py`
  - `tests/unit/test_installer_adapter_registry_target_roots.py`
  - `tests/unit/test_router_contract_support.py`
  - small cross-host regression subset as needed
- Docs:
  - install prompts and install reference docs only

## Verification Commands

```bash
pytest -q tests/unit/test_adapter_sdk.py tests/unit/test_installer_adapter_registry_target_roots.py tests/unit/test_router_contract_support.py
pytest -q tests/unit/test_adapter_registry_support.py tests/runtime_neutral/test_claude_preview_scaffold.py tests/runtime_neutral/test_windsurf_runtime_core.py tests/runtime_neutral/test_openclaw_runtime_core.py tests/runtime_neutral/test_opencode_preview_parity.py tests/runtime_neutral/test_opencode_managed_preview.py tests/integration/test_codex_install_prompt_discoverability.py
```

## Delivery Acceptance Plan

- Accept only if the requested four hosts resolve to real host roots by default.
- Accept only if the regression subset still passes.
- Accept only if docs no longer describe isolated fallback roots as the default path for those hosts.

## Completion Language Rules

- No “fixed” wording without green verification output.
- Keep host-managed limitations explicit in final delivery.

## Rollback Rules

- If a host cannot safely default to the real host root, stop and report the specific blocking surface instead of partially claiming success.

## Phase Cleanup Expectations

- Leave behind only requirement/plan docs, code/docs changes, and verification evidence.
