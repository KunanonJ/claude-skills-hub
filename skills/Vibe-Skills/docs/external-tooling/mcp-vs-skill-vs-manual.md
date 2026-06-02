# MCP vs Skill vs Provider vs Contract vs Manual Reference

## Purpose

This document defines the admission lanes for external resources entering VCO.
The goal is to stop “interesting upstream project” from being translated into “new default runtime surface” by accident.

VCO keeps one control plane. Every external resource must enter through exactly one primary lane.
If a resource appears to fit multiple lanes, pick the most restrictive lane first.

## Lane 1: MCP

**Use when:**
- The upstream resource exposes a callable tool surface.
- The capability is useful as a tool, not as a router or orchestrator.
- Failures can degrade safely to an existing VCO path.

**Good examples:**
- GitNexus MCP
- Search / retrieval / data access services

**Admission rules:**
- Must declare fallback behavior.
- Must not override `selected.pack_id` or `selected.skill`.
- Must not become a second workflow surface.

## Lane 2: Skill

**Use when:**
- The upstream material can be translated into a reusable VCO-native execution workflow.
- The task has a clear input/output contract.
- The capability belongs inside the bundled skill ecosystem.

**Good examples:**
- Domain skills
- Quality / debugging / documentation skills

**Admission rules:**
- Must have clear trigger boundaries.
- Must not duplicate an existing skill without a de-dup decision.
- Must fit an existing grade/task-type path.

## Lane 3: Provider

**Use when:**
- The upstream resource is one execution option inside an existing VCO plane.
- The plane already exists, but provider choice needs refinement.

**Good examples:**
- `browser-use` inside BrowserOps
- optional memory backends inside Memory Runtime v2

**Admission rules:**
- Only one primary provider per task.
- Provider selection remains owned by VCO policy.
- Provider must start as `off` or `shadow`.

## Lane 4: Contract / Reference

**Use when:**
- The resource contributes methods, rules, checklists, DSLs, or templates.
- Runtime takeover would create control-plane conflict.

**Good examples:**
- Letta memory blocks / tool rules
- Prompt-Engineering-Guide pattern cards
- Agent-S ACI / DAG contracts

**Admission rules:**
- Advice-only by default.
- Cannot introduce a second orchestrator.
- Cannot own default execution authority.

## Lane 5: Manual Reference

**Use when:**
- The resource is valuable as research input only.
- The material is useful for human-guided adaptation, not runtime binding.

**Good examples:**
- Large awesome lists
- upstream repos kept for comparative research

**Admission rules:**
- No runtime coupling.
- No automatic promotion.
- Use derived signals, not raw cargo-cult copying.

## Decision Rule

Choose the narrowest safe lane:

1. `Contract / Reference`
2. `Provider`
3. `Skill`
4. `MCP`

Do **not** choose a more powerful lane unless the weaker lane is demonstrably insufficient.

## Required Questions Before Admission

1. Which VCO plane does this resource strengthen?
2. What is its exact non-goal?
3. What existing capability overlaps with it?
4. What is the starting rollout mode (`off` or `shadow`)?
5. What is the rollback path?

If these questions are unanswered, the resource is not admission-ready.
