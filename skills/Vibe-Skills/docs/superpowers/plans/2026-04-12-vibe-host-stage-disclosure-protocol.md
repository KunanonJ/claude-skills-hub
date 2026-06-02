# Vibe Host Stage Disclosure Protocol Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an append-only host stage disclosure artifact so governed `vibe` can surface discussion, planning, and execution specialist activity incrementally.

**Architecture:** Reuse the existing specialist lifecycle truth model, project each confirmed lifecycle segment into a host-facing event, and persist those events to a dedicated artifact that stays separate from governance lineage. Wire the artifact into runtime summary and top-level payloads so hosts can poll it during execution and still read it after closure.

**Tech Stack:** PowerShell runtime scripts, JSON runtime artifacts, Python runtime-neutral tests

---

## Chunk 1: Runtime Contract

### Task 1: Add the failing contract tests

**Files:**
- Modify: `tests/runtime_neutral/test_vibe_specialist_consultation.py`
- Modify: `tests/runtime_neutral/test_governed_runtime_bridge.py`

- [ ] **Step 1: Add assertions for `host_stage_disclosure`**

Check for:

- artifact presence
- summary presence
- stable event ids
- stable event order
- real `native_skill_entrypoint` paths

- [ ] **Step 2: Run the focused tests and verify they fail**

Run:

```bash
python3 -m pytest tests/runtime_neutral/test_vibe_specialist_consultation.py -q
python3 -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py -q
```

Expected: FAIL because `host_stage_disclosure` does not exist yet.

## Chunk 2: Runtime Helpers

### Task 2: Add the host-stage disclosure helper surface

**Files:**
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`

- [ ] **Step 1: Add path and event helpers**

Create helpers for:

- `Get-VibeHostStageDisclosurePath`
- `New-VibeHostUserBriefingSegmentProjection`
- `New-VibeHostStageDisclosureEventProjection`
- `Add-VibeHostStageDisclosureEvent`

- [ ] **Step 2: Extend runtime summary projections**

Add:

- `artifacts.host_stage_disclosure`
- `summary.host_stage_disclosure`

## Chunk 3: Stage Integration

### Task 3: Emit events from root runtime and execution runtime

**Files:**
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`

- [ ] **Step 1: Append routing and consultation events in root runtime**

Emit events for:

- discussion routing freeze
- discussion consultation completion
- planning consultation completion

- [ ] **Step 2: Append execution dispatch event inside `Invoke-PlanExecute.ps1`**

Emit the execution event immediately after effective approved-dispatch disclosure is known.

- [ ] **Step 3: Load the final disclosure artifact into runtime summary**

Expose:

- artifact path
- parsed object
- top-level payload fields

## Chunk 4: Contract Docs And Verification

### Task 4: Freeze the contract in docs and rerun tests

**Files:**
- Modify: `protocols/runtime.md`
- Modify: `references/runtime-contract-field-contract.md`

- [ ] **Step 1: Document the new artifact and behavior**

Freeze:

- append-only host-consumption purpose
- separation from `stage-lineage.json`
- optional public compatibility field in runtime summary

- [ ] **Step 2: Run the focused verification**

Run:

```bash
python3 -m pytest tests/runtime_neutral/test_vibe_specialist_consultation.py -q
python3 -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py -q
```

Expected: PASS

- [ ] **Step 3: Run broader regression checks**

Run:

```bash
python3 -m pytest tests/runtime_neutral/test_runtime_contract_goldens.py -q
python3 -m pytest tests/runtime_neutral/test_runtime_contract_schema.py -q
```

Expected: PASS
