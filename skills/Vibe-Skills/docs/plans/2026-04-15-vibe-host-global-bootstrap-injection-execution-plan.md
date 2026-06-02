# Vibe Host Global Bootstrap Injection Execution Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an install-time, non-destructive, idempotent bootstrap injection path for `codex`, `claude-code`, and `opencode` so explicit `$vibe` and `/vibe` invocations are pulled into canonical `vibe` through the host's official global instruction file.

**Architecture:** Extend host profiles with a `global_instruction_surface` contract, add short host-specific bootstrap templates, and implement a dedicated managed-block service that can insert, update, verify, and remove one uniquely identified bootstrap block without overwriting the target file. Install, upgrade, uninstall, and check flows consume this service and emit receipts proving the block state.

**Tech Stack:** Python installer core, JSON host metadata, Markdown bootstrap templates, runtime-neutral pytest suite, install ledger and host closure receipts

---

## Chunk 1: Freeze Contract, Metadata, and Red Tests

### Task 1: Lock the bootstrap contract before implementation

**Files:**
- Modify: `adapters/codex/host-profile.json`
- Modify: `adapters/claude-code/host-profile.json`
- Modify: `adapters/opencode/host-profile.json`
- Add: `docs/requirements/2026-04-15-vibe-host-global-bootstrap-injection.md`
- Add: `docs/plans/2026-04-15-vibe-host-global-bootstrap-injection-execution-plan.md`
- Add: `tests/unit/test_global_instruction_merge.py`
- Add: `tests/runtime_neutral/test_global_instruction_bootstrap_runtime.py`
- Modify: `tests/runtime_neutral/test_bootstrap_doctor.py`

- [ ] **Step 1: Add a host metadata contract**

Define a `global_instruction_surface` object for each supported host. Minimum fields:

- target path
- format
- managed block id
- merge policy
- overwrite policy
- trigger tokens
- bootstrap-only authority note

- [ ] **Step 2: Write red unit tests for managed-block semantics**

Write failing tests that prove:

- missing file -> inserted
- existing file + no block -> inserted without content loss
- existing file + same block -> unchanged
- existing file + older block -> updated
- duplicate block -> failure
- corrupted delimiters -> failure

- [ ] **Step 3: Write red runtime-neutral tests for user-visible install behavior**

Write failing tests that prove:

- Codex install targets `AGENTS.md`
- Claude install targets `CLAUDE.md`
- OpenCode install targets `AGENTS.md`
- the managed block is visible to check surfaces and receipts

- [ ] **Step 4: Freeze duplicate and corruption policy**

Make the tests explicit that duplicate and corrupted blocks do not get auto-overwritten.

- [ ] **Step 5: Run the new focused red test slice**

Run:

`python3 -m pytest tests/unit/test_global_instruction_merge.py tests/runtime_neutral/test_global_instruction_bootstrap_runtime.py tests/runtime_neutral/test_bootstrap_doctor.py -q`

Expected: FAIL until the merge service and integration are implemented.

## Chunk 2: Add Host Templates and Managed-Block Core

### Task 2: Build a single merge service with clear boundaries

**Files:**
- Add: `config/global-bootstrap/codex-vibe-bootstrap.md`
- Add: `config/global-bootstrap/claude-code-vibe-bootstrap.md`
- Add: `config/global-bootstrap/opencode-vibe-bootstrap.md`
- Add: `packages/installer-core/src/vgo_installer/global_instruction_contract.py`
- Add: `packages/installer-core/src/vgo_installer/global_instruction_merge.py`
- Add: `packages/installer-core/src/vgo_installer/global_instruction_service.py`

- [ ] **Step 1: Create short host bootstrap templates**

Each template should:

- mention explicit `$vibe` and `/vibe`
- require entry into canonical `vibe`
- forbid silent normal-mode fallback
- state that the file is bootstrap only and does not own runtime authority

- [ ] **Step 2: Implement stable managed-block markers**

Render each template inside a machine-detectable block with:

- host id
- block id
- template version
- content hash or equivalent signature

- [ ] **Step 3: Implement pure merge operations**

The merge core should support:

- `insert_block`
- `update_block`
- `remove_block`
- `detect_duplicate_blocks`
- `detect_corruption`

Keep it pure and text-focused so installer entrypoints do not contain markdown surgery logic.

- [ ] **Step 4: Implement typed result semantics**

Return structured actions instead of ad hoc booleans:

- `inserted`
- `updated`
- `unchanged`
- `removed`
- `error_duplicate_managed_blocks`
- `error_corrupt_managed_block`
- `error_unsafe_merge`

- [ ] **Step 5: Re-run the unit tests**

Run:

`python3 -m pytest tests/unit/test_global_instruction_merge.py -q`

Expected: PASS

## Chunk 3: Integrate Install, Upgrade, Ledger, and Receipts

### Task 3: Wire the managed-block service into the installer lifecycle

**Files:**
- Modify: `packages/installer-core/src/vgo_installer/install_runtime.py`
- Modify: `packages/installer-core/src/vgo_installer/ledger_service.py`
- Modify: `packages/installer-core/src/vgo_installer/materializer.py`
- Modify: `apps/vgo-cli/src/vgo_cli/upgrade_service.py`
- Modify: `apps/vgo-cli/src/vgo_cli/install_support.py`

- [ ] **Step 1: Invoke bootstrap injection during install**

After adapter resolution and host payload materialization, call the global-instruction service for hosts that declare the new surface.

- [ ] **Step 2: Persist receipt evidence**

Emit a receipt under the host target root, for example:

- `.vibeskills/global-instruction-bootstrap.json`

Receipt should record:

- host
- target file
- block id
- action
- template version
- content hash
- timestamp

- [ ] **Step 3: Extend install ledger state**

Track enough information to support uninstall and drift reasoning without treating the whole file as installer-owned.

Minimum tracked data:

- target file path
- block id
- created-if-absent
- template version

- [ ] **Step 4: Keep upgrade idempotent**

Ensure reinstall and upgrade call the same service so host bootstrap evolves by in-place block update, not append.

- [ ] **Step 5: Re-run lifecycle-focused tests**

Run:

`python3 -m pytest tests/runtime_neutral/test_global_instruction_bootstrap_runtime.py tests/runtime_neutral/test_claude_preview_scaffold.py -q`

Expected: PASS

## Chunk 4: Integrate Uninstall and Drift-Safe Check Logic

### Task 4: Remove only owned blocks and surface health truth

**Files:**
- Modify: `packages/installer-core/src/vgo_installer/uninstall_service.py`
- Modify: `packages/verification-core/src/vgo_verify/bootstrap_doctor_support.py`
- Modify: `packages/verification-core/src/vgo_verify/bootstrap_doctor_runtime.py`
- Modify: `packages/verification-core/src/vgo_verify/opencode_preview_smoke_runtime.py`
- Modify: `tests/runtime_neutral/test_bootstrap_doctor.py`
- Modify: `tests/runtime_neutral/test_opencode_managed_preview.py`

- [ ] **Step 1: Add uninstall block-removal semantics**

Uninstall should:

- remove only the managed block
- preserve non-managed file content
- delete the file only if it was installer-created and empty after removal

- [ ] **Step 2: Add check visibility for bootstrap health**

Bootstrap doctor and related check surfaces should report:

- target file exists
- block present
- duplicate count
- corruption state
- template version
- last receipt action

- [ ] **Step 3: Keep duplicate and corruption states non-green**

Checks must fail when:

- duplicate managed blocks exist
- delimiters are corrupted
- the receipt points at a missing block

- [ ] **Step 4: Keep truthful wording**

Do not report bootstrap healthy merely because the host root exists or `skills/vibe` exists. The managed block itself must be proven.

- [ ] **Step 5: Re-run check-oriented tests**

Run:

`python3 -m pytest tests/runtime_neutral/test_bootstrap_doctor.py tests/runtime_neutral/test_opencode_managed_preview.py -q`

Expected: PASS

## Chunk 5: User-Facing Docs, Diff Audit, and Final Verification

### Task 5: Explain exactly what the installer changes and verify only touched surfaces

**Files:**
- Modify: `docs/install/one-click-install-release-copy.en.md`
- Modify: `docs/install/one-click-install-release-copy.md`
- Optionally add: `docs/install/host-global-bootstrap.md`

- [ ] **Step 1: Document user-visible behavior**

Explain in plain language:

- which file each host uses
- that only a managed `vibeskills` block is inserted
- that repeated install is safe
- that uninstall removes only the managed block

- [ ] **Step 2: Document limitations honestly**

State clearly that Phase 1 is host bootstrap guidance, not host-kernel hard enforcement.

- [ ] **Step 3: Run the focused verification slice**

Run:

`python3 -m pytest tests/unit/test_global_instruction_merge.py tests/runtime_neutral/test_global_instruction_bootstrap_runtime.py tests/runtime_neutral/test_bootstrap_doctor.py tests/runtime_neutral/test_claude_preview_scaffold.py tests/runtime_neutral/test_opencode_managed_preview.py -q`

Expected: PASS

- [ ] **Step 4: Inspect only the touched diff**

Run:

`git diff -- adapters/codex/host-profile.json adapters/claude-code/host-profile.json adapters/opencode/host-profile.json config/global-bootstrap/codex-vibe-bootstrap.md config/global-bootstrap/claude-code-vibe-bootstrap.md config/global-bootstrap/opencode-vibe-bootstrap.md packages/installer-core/src/vgo_installer/global_instruction_contract.py packages/installer-core/src/vgo_installer/global_instruction_merge.py packages/installer-core/src/vgo_installer/global_instruction_service.py packages/installer-core/src/vgo_installer/install_runtime.py packages/installer-core/src/vgo_installer/ledger_service.py packages/installer-core/src/vgo_installer/materializer.py packages/installer-core/src/vgo_installer/uninstall_service.py packages/verification-core/src/vgo_verify/bootstrap_doctor_support.py packages/verification-core/src/vgo_verify/bootstrap_doctor_runtime.py packages/verification-core/src/vgo_verify/opencode_preview_smoke_runtime.py apps/vgo-cli/src/vgo_cli/upgrade_service.py apps/vgo-cli/src/vgo_cli/install_support.py tests/unit/test_global_instruction_merge.py tests/runtime_neutral/test_global_instruction_bootstrap_runtime.py tests/runtime_neutral/test_bootstrap_doctor.py tests/runtime_neutral/test_claude_preview_scaffold.py tests/runtime_neutral/test_opencode_managed_preview.py docs/requirements/2026-04-15-vibe-host-global-bootstrap-injection.md docs/plans/2026-04-15-vibe-host-global-bootstrap-injection-execution-plan.md docs/install/one-click-install-release-copy.en.md docs/install/one-click-install-release-copy.md`

Expected: only host bootstrap metadata, merge service, lifecycle integration, tests, and docs.

- [ ] **Step 5: Record residual risks**

Call out the still-open Phase 2 area:

- host bootstrap increases entry stability but does not replace a future hard structured handoff if near-guaranteed invocation is required under extreme context pressure

- [ ] **Step 6: Verify before any completion claim**

Re-run the exact focused verification command immediately before claiming this enhancement complete and report the actual result.

## Plain-Language Outcome

After this plan is implemented:

- install will add one small `vibe` bootstrap block to the right host-wide instruction file
- it will never overwrite the rest of that file
- reinstall and upgrade will touch the same block instead of adding more copies
- uninstall will remove only that one block
- users will keep invoking `vibe` the same way they already do:
  - `$vibe`
  - `/vibe`
- `check` will be able to tell users whether the bootstrap block is healthy, duplicated, corrupted, or missing
