# PR 127 Review Fixes Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the remaining verified PR `#127` review defects and land regression coverage before pushing a new commit to the PR branch.

**Architecture:** Keep the current governed promotion model intact and patch only the verified defects. Drive the work with focused regression tests first, then apply the smallest PowerShell and test-harness changes needed to satisfy them.

**Tech Stack:** PowerShell, Python `unittest`, GitHub PR workflow

---

### Task 1: Freeze Regression Expectations

**Files:**
- Create: `docs/requirements/2026-04-06-pr-127-review-fixes.md`
- Create: `docs/plans/2026-04-06-pr-127-review-fixes-execution-plan.md`

- [ ] Step 1: Record the verified defects and acceptance criteria in the requirement doc.
- [ ] Step 2: Record the implementation and verification sequence in the plan doc.

### Task 2: Add Failing Tests First

**Files:**
- Modify: `tests/runtime_neutral/test_skill_promotion_router_metadata.py`
- Modify: `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`

- [ ] Step 1: Add a router/helper regression test proving Windows-style paths must classify as destructive.
- [ ] Step 2: Add a helper regression test proving whitespace-only contract entries are incomplete.
- [ ] Step 3: Add a freeze-contract regression test proving `surface_only` recommendations are not auto-approved.
- [ ] Step 4: Move the invalid-policy regression to an isolated temporary repo copy.
- [ ] Step 5: Run the targeted tests and confirm they fail for the expected reasons.

### Task 3: Apply Minimal Production Fixes

**Files:**
- Modify: `scripts/common/vibe-governance-helpers.ps1`
- Modify: `config/skill-promotion-policy.json`
- Modify: `scripts/runtime/Freeze-RuntimeInputPacket.ps1`

- [ ] Step 1: Extend destructive path patterns to Windows and backslash-relative forms in helper defaults and config.
- [ ] Step 2: Filter blank/whitespace contract entries before completeness counting.
- [ ] Step 3: Gate `approved_dispatch` on `recommended_promotion_action == 'auto_dispatch'`.
- [ ] Step 4: Keep all other promotion-state behaviors unchanged unless required by the new tests.

### Task 4: Verify End To End

**Files:**
- Test: `tests/runtime_neutral/test_skill_promotion_router_metadata.py`
- Test: `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`
- Test: `tests/runtime_neutral/test_skill_promotion_destructive_gate.py`

- [ ] Step 1: Re-run the targeted regression tests and confirm they pass.
- [ ] Step 2: Run the broader touched runtime-neutral subset and confirm it stays green.
- [ ] Step 3: Review `git diff` to ensure only the intended files changed.

### Task 5: Deliver To PR 127

**Files:**
- Modify: git history on PR branch only

- [ ] Step 1: Commit the verified fix set with a focused message.
- [ ] Step 2: Push `HEAD` to `origin/skill-promotion-governed-execution-clean`.
