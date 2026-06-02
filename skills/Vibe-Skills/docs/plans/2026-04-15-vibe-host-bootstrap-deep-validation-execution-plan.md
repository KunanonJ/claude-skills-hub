# Vibe Host Bootstrap Deep Validation Execution Plan

**Goal:** Validate, in isolated temp roots only, that host global bootstrap injection is safe, idempotent, uninstall-clean, and materially useful for routing explicit `$vibe` and `/vibe` back to canonical `vibe`.

**Internal grade:** `L`

**Execution strategy:** Native serial validation. No subagents needed because the critical path is short and tightly coupled to local verification output.

## Step 1: Inspect Coverage and Freeze Evidence Targets

- review current host bootstrap templates, merge service, install integration, uninstall integration, and bootstrap doctor surfaces
- identify what is already covered by unit and runtime-neutral tests
- identify any missing end-to-end proof around:
  - preserved user-authored instruction text
  - exact managed-block content
  - reinstall idempotency
  - uninstall-only-owned-block semantics

## Step 2: Fill the Highest-Value Coverage Gap

- if an important guarantee is currently implicit rather than tested, add one focused test
- prefer one integration-style shell test that covers:
  - pre-existing user instruction content
  - install
  - check
  - reinvoke install
  - uninstall
  - post-uninstall preservation
- avoid broad refactors unless the test reveals a real defect

## Step 3: Run Focused Automated Verification

- run the existing focused bootstrap suites
- run the new or adjusted deep-validation test slice
- keep the commands bounded to bootstrap/install/check/uninstall surfaces

Planned commands:

`python3 -m pytest tests/unit/test_global_instruction_merge.py tests/runtime_neutral/test_global_instruction_bootstrap_runtime.py tests/runtime_neutral/test_bootstrap_doctor.py tests/runtime_neutral/test_installed_runtime_uninstall.py tests/runtime_neutral/test_claude_preview_scaffold.py tests/runtime_neutral/test_opencode_managed_preview.py tests/runtime_neutral/test_discoverable_wrapper_host_visibility.py -q`

plus any new focused integration test added in this run.

## Step 4: Perform Manual Temp-Root Spot Checks

- run manual temp-root install and uninstall flows for:
  - `codex`
  - `claude-code`
  - `opencode`
- inspect:
  - target file name
  - managed block markers
  - preserved user text
  - receipt presence
  - idempotent second install behavior
  - uninstall residue

## Step 5: Final Verification and Truthful Reporting

- run `git diff --check` on touched files
- report:
  - what is definitely proven safe
  - what is definitely proven injected
  - what is definitely proven useful at repo/bootstrap level
  - what is not fully proven because real host consumption is outside this environment

## Verification Rules

- no success claim without fresh command output
- any discovered defect must be fixed before final completion wording
- if no defect is found, say the result is validated within the tested boundary rather than universally guaranteed

## Rollback Rules

- if a new test demonstrates destructive behavior, stop and fix implementation before any more expansion
- do not touch real host roots under any circumstance

## Phase Cleanup Expectations

- leave behind only the new requirement doc, execution plan, and any necessary focused test additions
- do not keep ad hoc temp artifacts in the repo
