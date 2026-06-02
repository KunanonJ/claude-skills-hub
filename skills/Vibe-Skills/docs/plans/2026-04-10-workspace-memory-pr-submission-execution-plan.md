# Workspace Memory PR Submission Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the workspace-shared memory enhancement into a clean PR branch with reviewer-friendly documentation and fresh verification evidence.

**Architecture:** Start from a clean `origin/main` worktree, transplant only the validated workspace-memory files, then add plain-language README guidance and re-run the memory-focused regression suite before creating the commit and PR payload.

**Tech Stack:** Git worktrees, PowerShell runtime scripts, Python runtime helpers, pytest, Markdown documentation.

---

## Chunk 1: Isolate the PR branch

### Task 1: Create a clean review branch from `origin/main`

**Files:**
- Create: `.worktrees/workspace-memory-pr/*`

- [x] **Step 1: Create the isolated worktree branch**

Run: `git worktree add .worktrees/workspace-memory-pr -b feat/workspace-memory-plane origin/main`
Expected: new clean branch checked out from `origin/main`

- [x] **Step 2: Run a lightweight baseline check**

Run: `pytest tests/runtime_neutral/test_docs_readme_encoding.py -q`
Expected: PASS on the clean branch

## Chunk 2: Transplant the memory enhancement

### Task 2: Copy only the workspace-memory runtime/config/test surfaces

**Files:**
- Modify: `config/memory-backend-adapters.json`
- Modify: `config/memory-runtime-v3-policy.json`
- Modify: `config/memory-tier-router.json`
- Modify: `config/runtime-config-manifest.json`
- Modify: `config/runtime-script-manifest.json`
- Modify: `config/version-governance.json`
- Create: `config/memory-disclosure-policy.json`
- Create: `config/memory-ingest-policy.json`
- Create: `config/workspace-memory-plane.json`
- Modify: `packages/runtime-core/src/vgo_runtime/memory.py`
- Create: `packages/runtime-core/src/vgo_runtime/workspace_memory.py`
- Create: `packages/runtime-core/src/vgo_runtime/workspace_memory_schema.py`
- Modify: `scripts/runtime/VibeMemoryActivation.Common.ps1`
- Modify: `scripts/runtime/VibeMemoryBackends.Common.ps1`
- Create: `scripts/runtime/VibeWorkspaceMemory.Common.ps1`
- Modify: `scripts/runtime/memory_backend_driver.py`
- Create: `scripts/runtime/workspace_memory_driver.py`
- Create: `docs/design/workspace-memory-plane.md`
- Create: `references/workspace-memory-capsule-contract.md`
- Create: `references/workspace-memory-query-contract.md`
- Modify/Create: memory-focused tests under `tests/runtime_neutral/` and `tests/integration/`

- [x] **Step 1: Transplant the validated file set into the clean worktree**

Expected: `git status --short` in the worktree shows only memory-plane-related files

## Chunk 3: Make the PR readable

### Task 3: Update reviewer-facing docs

**Files:**
- Modify: `README.md`
- Modify: `README.zh.md`
- Create: `docs/requirements/2026-04-10-workspace-memory-pr-submission.md`
- Create: `docs/plans/2026-04-10-workspace-memory-pr-submission-execution-plan.md`

- [x] **Step 1: Add plain-language README guidance**

Expected: readers can understand sharing, isolation, relevance gating, and progressive disclosure without opening source files

- [x] **Step 2: Record the packaging scope and acceptance criteria**

Expected: requirement/plan docs explain why this PR exists and how it is verified

## Chunk 4: Verify and submit

### Task 4: Re-run the memory regression suite and create the PR commit

**Files:**
- Test: `tests/runtime_neutral/test_codex_memory_user_simulation.py`
- Test: `tests/runtime_neutral/test_memory_runtime_activation.py`
- Test: `tests/runtime_neutral/test_memory_progressive_disclosure.py`
- Test: `tests/runtime_neutral/test_runtime_contract_schema.py`
- Test: `tests/runtime_neutral/test_cross_host_memory_identity.py`
- Test: `tests/runtime_neutral/test_workspace_shared_memory_plane.py`
- Test: `tests/runtime_neutral/test_memory_ingest_noise_filters.py`
- Test: `tests/integration/test_runtime_config_manifest_roles.py`
- Test: `tests/integration/test_version_governance_runtime_roles.py`
- Test: `tests/runtime_neutral/test_docs_readme_encoding.py`
- Test: `tests/runtime_neutral/test_installed_host_runtime_simulation.py`

- [ ] **Step 1: Run the isolated branch regression suite**

Run: `pytest tests/runtime_neutral/test_codex_memory_user_simulation.py tests/runtime_neutral/test_memory_runtime_activation.py tests/runtime_neutral/test_memory_progressive_disclosure.py tests/runtime_neutral/test_runtime_contract_schema.py tests/runtime_neutral/test_cross_host_memory_identity.py tests/runtime_neutral/test_workspace_shared_memory_plane.py tests/runtime_neutral/test_memory_ingest_noise_filters.py tests/integration/test_runtime_config_manifest_roles.py tests/integration/test_version_governance_runtime_roles.py tests/runtime_neutral/test_docs_readme_encoding.py -q`
Expected: PASS

- [ ] **Step 2: Re-run the installed-host continuity probe**

Run: `pytest tests/runtime_neutral/test_installed_host_runtime_simulation.py -q -k high_fidelity_memory_continuity`
Expected: PASS

- [ ] **Step 3: Stage only the memory PR file set**

Run: `git add <isolated file set>`
Expected: staged diff contains only workspace-memory enhancement files

- [ ] **Step 4: Commit the PR branch**

Run: `git commit -m "feat: add workspace-shared memory plane"`
Expected: one reviewable commit for the enhancement

- [ ] **Step 5: Push and open the PR**

Run: `git push -u origin feat/workspace-memory-plane`
Expected: remote branch exists and can back a PR
