# PR130 Rabbit Review Fixes Execution Plan

## Internal Grade

`XL` — wave-sequential execution with bounded parallel analysis, then local implementation, verification, and PR publication.

## Waves

### Wave 1

- freeze requirement and plan artifacts
- inspect the existing prompt and configuration-guide surfaces
- add failing regression tests for the two confirmed review gaps

### Wave 2

- update the English framework-only prompt so Codex is a first-class host branch
- restore concrete post-install follow-up guidance in the Chinese and English configuration guides for Windsurf, OpenClaw, and OpenCode

### Wave 3

- run the targeted tests added or tightened for this fix
- run adjacent existing doc tests to guard against regressions
- inspect the final diff for scope drift

### Wave 4

- commit the branch with the review-fix delta
- push to the existing PR branch
- leave a concise PR closure summary

## Ownership Boundaries

- docs:
  - `docs/install/prompts/framework-only-install.en.md`
  - `docs/install/configuration-guide.en.md`
  - `docs/install/configuration-guide.md`
- tests:
  - `tests/integration/test_codex_install_prompt_discoverability.py`
  - `tests/integration/test_multi_host_real_host_root_docs.py`
- governance artifacts:
  - this requirement doc
  - this execution plan

## Verification Commands

```bash
pytest -q tests/integration/test_codex_install_prompt_discoverability.py tests/integration/test_multi_host_real_host_root_docs.py
pytest -q tests/unit/test_adapter_sdk.py tests/unit/test_installer_adapter_registry_target_roots.py tests/unit/test_router_contract_support.py tests/unit/test_adapter_registry_support.py tests/runtime_neutral/test_windsurf_runtime_core.py tests/runtime_neutral/test_openclaw_runtime_core.py tests/runtime_neutral/test_opencode_preview_parity.py
```

## Delivery Acceptance Plan

- accept only if the first verification command proves the repaired docs contract
- accept only if the second verification command shows no target-root regression on adjacent host-root behavior
- accept only if the branch is pushed successfully to the existing PR

## Completion Language Rules

- do not say the PR is updated until the push succeeds

## Rollback Rules

- if verification fails, stop and fix the failing contract before any commit
- if push fails, report the exact remote/auth blocker and keep the verified local commit intact

## Phase Cleanup Expectations

- leave behind only the requirement/plan artifacts, minimal doc/test fixes, verification evidence, and the resulting commit metadata
