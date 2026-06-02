# Vibe Discussion-Time Specialist Consultation Implementation Plan

> **For agentic workers:** REQUIRED: Use governed `vibe` discipline for this change. Keep the PR scoped to discussion-time and plan-time specialist consultation. Do not expand into router redesign or execution-dispatch redesign.

**Goal:** Add a separate governed specialist-consultation layer so routed planning specialists can truly participate in discussion and plan formation before execution, with progressive disclosure under `vibe`.

**Architecture:** Introduce a dedicated consultation module and policy surface, invoke it from two consultation windows inside the existing governed path, persist consultation receipts and disclosure artifacts, and keep consultation truth strictly separate from execution-time dispatch truth.

**Tech Stack:** PowerShell governed runtime scripts, JSON policy, Markdown contract docs, Python runtime-neutral tests

---

## Chunk 1: Freeze The Consultation Contract

### Task 1: Lock the consultation semantics in docs and policy

**Files:**
- Modify: `SKILL.md`
- Modify: `protocols/runtime.md`
- Modify: `protocols/think.md`
- Modify: `protocols/team.md`
- Add: `config/specialist-consultation-policy.json`
- Modify: `docs/requirements/2026-04-12-vibe-discussion-time-specialist-consultation.md`
- Modify: `docs/superpowers/specs/2026-04-12-vibe-discussion-time-specialist-consultation-design.md`

- [ ] **Step 1: Add contract wording for governed specialist consultation**

State that routed specialists may be consulted during discussion and plan formation under `vibe`, but do not become runtime authorities or peer front-end speakers.

- [ ] **Step 2: Freeze the separation rule**

State explicitly that consultation truth is separate from execution truth and must not reuse execution `approved_dispatch` semantics.

- [ ] **Step 3: Add consultation policy**

Create `config/specialist-consultation-policy.json` with:

- `enabled`
- `max_consults_per_window`
- `allowed_windows`
- `require_contract_complete`
- `require_native_workflow`
- `require_native_usage_required`
- `require_entrypoint_path`
- `progressive_disclosure_enabled`
- `defer_unapproved_to_execution`

- [ ] **Step 4: Confirm the public six-stage contract remains unchanged**

Make the docs explicit that consultation is an internal governed subflow, not a seventh public runtime stage.

## Chunk 2: Build The Consultation Runtime Core

### Task 2: Create an isolated consultation module

**Files:**
- Add: `scripts/runtime/VibeConsultation.Common.ps1`
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
- Optionally add or extract a small shared invocation helper only if execution helpers are too coupled to execution semantics

- [ ] **Step 1: Define consultation data structures**

Add builders for:

- consultation candidate approval
- consultation window receipts
- consultation disclosure projections
- consultation summary projections

- [ ] **Step 2: Define consultation-specific prompt and schema builders**

Do not reuse execution-dispatch prompt wording directly. Consultation must ask for reasoning, plan-shaping advice, adoption notes, and bounded recommendations rather than code-execution receipts.

- [ ] **Step 3: Reuse only low-level invocation primitives**

Reuse host adapter resolution and process execution only where they are truly transport-level concerns. Keep consultation modeling separate from execution-dispatch modeling.

- [ ] **Step 4: Add stable artifact paths**

Define receipt paths such as:

- `discussion-specialist-consultation.json`
- `planning-specialist-consultation.json`

## Chunk 3: Integrate Discussion-Time Consultation

### Task 3: Consult specialists after `deep_interview`

**Files:**
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`
- Modify: `scripts/runtime/Invoke-DeepInterview.ps1`
- Modify: `scripts/runtime/Write-RequirementDoc.ps1`

- [ ] **Step 1: Insert discussion consultation window**

After `deep_interview` and before `requirement_doc`, invoke the consultation module using frozen `specialist_recommendations`.

- [ ] **Step 2: Approve only suitable specialists**

Filter for discussion-appropriate specialists and cap the number consulted per window.

- [ ] **Step 3: Emit progressive disclosure**

Generate user-facing disclosure entries that state:

- which specialist is being consulted
- why now
- where the skill is loaded from

- [ ] **Step 4: Feed consultation output into requirement freeze**

`Write-RequirementDoc.ps1` should consume the discussion consultation receipt and record:

- consulted specialists
- adopted insights
- deferred or rejected insights

## Chunk 4: Integrate Plan-Time Consultation

### Task 4: Consult specialists before final plan freeze

**Files:**
- Modify: `scripts/runtime/invoke-vibe-runtime.ps1`
- Modify: `scripts/runtime/Write-XlPlan.ps1`

- [ ] **Step 1: Insert planning consultation window**

After `requirement_doc` exists and before `xl_plan` finalization, invoke the same consultation engine with planning-specific prompt framing.

- [ ] **Step 2: Keep the consultation window independent of execution dispatch**

Planning consultation may inform the plan, but it must not auto-claim execution participation.

- [ ] **Step 3: Feed consultation output into the plan**

`Write-XlPlan.ps1` should record:

- which specialists were truly consulted
- which plan decisions were influenced
- which specialist suggestions were recorded but not adopted

## Chunk 5: Preserve Execution Separation

### Task 5: Ensure execution-time dispatch semantics stay intact

**Files:**
- Modify: `scripts/runtime/Invoke-PlanExecute.ps1`
- Modify: `scripts/runtime/VibeExecution.Common.ps1` only if strictly necessary
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`

- [ ] **Step 1: Keep consultation truth out of execution disclosure**

Execution disclosure should continue to be built only from effective `approved_dispatch`.

- [ ] **Step 2: Add runtime summary support**

Include consultation summary projections in runtime summary and relevant receipts, but do not blur them into execution specialist accounting.

- [ ] **Step 3: Confirm no execution behavior regression**

Specialist execution ordering, blocking, degradation, and unified pre-dispatch disclosure must keep their current meaning.

## Chunk 6: TDD And Verification

### Task 6: Add isolated consultation tests and regression coverage

**Files:**
- Add: `tests/runtime_neutral/test_vibe_specialist_consultation.py`
- Modify: `tests/runtime_neutral/test_governed_runtime_bridge.py`
- Modify: `tests/runtime_neutral/test_skill_promotion_freeze_contract.py`

- [ ] **Step 1: Add failing-first consultation tests**

Prove that:

- specialists can be approved for consultation from frozen recommendations
- consultation receipts are emitted
- progressive disclosure contains `skill_id`, `why_now`, and absolute `native_skill_entrypoint`

- [ ] **Step 2: Add requirement/plan propagation assertions**

Verify that requirement and plan surfaces reflect actual consultation truth rather than recommendation-only metadata.

- [ ] **Step 3: Add separation regression assertions**

Verify that consultation truth is not stored as execution `approved_dispatch`, and that execution-time disclosure still only uses execution truth.

- [ ] **Step 4: Run the focused verification slice**

Run:

`python3 -m pytest tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_runtime_contract_goldens.py tests/runtime_neutral/test_runtime_contract_schema.py tests/integration/test_runtime_config_manifest_roles.py -q`

Expected: PASS

## Chunk 7: Final Verification And PR Hygiene

### Task 7: Verify the standalone PR boundary

**Files:**
- No new semantic areas beyond consultation/runtime/doc/test surfaces

- [ ] **Step 1: Run targeted consultation and runtime regression tests**

Run:

`python3 -m pytest tests/runtime_neutral/test_vibe_specialist_consultation.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_skill_promotion_freeze_contract.py tests/runtime_neutral/test_skill_promotion_metrics.py tests/runtime_neutral/test_runtime_contract_goldens.py tests/runtime_neutral/test_runtime_contract_schema.py tests/integration/test_runtime_config_manifest_roles.py -q`

Expected: PASS

- [ ] **Step 2: Inspect the touched diff only**

Confirm the diff is limited to:

- consultation policy
- consultation runtime module
- runtime integration points
- requirement/plan docs
- consultation-focused tests

- [ ] **Step 3: Summarize residual risks**

Capture:

- whether consultation prompt/schema reuse still leaks execution assumptions
- whether some planning specialists need explicit consultation profile overrides
- whether host transcript surfaces still need follow-up work to render disclosures live in every adapter

- [ ] **Step 4: Verify before claiming completion**

Re-run the exact verification commands immediately before any completion claim and report actual pass/fail status.
