# Vibe Host Global Bootstrap Injection Requirement

## Summary

Add a non-destructive, idempotent install-time bootstrap layer for supported hosts so explicit `$vibe` and `/vibe` invocations are pulled into canonical `vibe` through each host's official global instruction surface without turning that surface into a second runtime authority.

## Goal

Make `vibe` entry materially more stable on Codex CLI, Claude Code, and OpenCode by injecting a short managed bootstrap block into the correct host-level instruction file during install and upgrade while preserving user-authored content.

## Deliverable

A host-bootstrap capability that:

- declares each supported host's official global instruction surface in adapter metadata
- writes a uniquely identified `vibeskills` managed block into that file at install time
- updates the same managed block on upgrade instead of appending duplicates
- removes only the managed block on uninstall
- exposes check and receipt evidence for block presence, drift, corruption, and duplicate insertion

## Constraints

- `vibe` remains the only governed runtime authority
- host global instruction files are bootstrap entry surfaces only, not canonical governance truth
- do not overwrite user-authored global instruction files under any circumstance
- do not replace an existing file with a repo template
- only manage a uniquely identified `vibeskills` block inside the target file
- repeated install, repair, and upgrade must be idempotent
- if safe merge cannot be proven, fail closed instead of writing
- if duplicate managed blocks are found, fail and surface drift instead of guessing which block to keep
- Phase 1 is limited to official host instruction files:
  - Codex CLI: `~/.codex/AGENTS.md`
  - Claude Code: `~/.claude/CLAUDE.md`
  - OpenCode: `~/.config/opencode/AGENTS.md`
- `~/.claude/settings.json`, `~/.codex/settings.json`, and `~/.config/opencode/opencode.json` do not become the main prompt-governance surface in this change
- OpenCode real `opencode.json` remains host-managed in this phase
- this phase strengthens bootstrap entry, not host-kernel hard enforcement

## Acceptance Criteria

- each of `codex`, `claude-code`, and `opencode` declares a `global_instruction_surface` contract in host metadata
- the repo contains short host-specific bootstrap templates for:
  - `codex`
  - `claude-code`
  - `opencode`
- installation into a missing global instruction file creates a new file containing exactly one managed bootstrap block
- installation into an existing global instruction file preserves all user-authored content outside the managed block
- repeated install on an unchanged target yields `unchanged` and does not append a second block
- upgrade updates the existing managed block in place and does not duplicate it
- uninstall removes only the managed block and preserves user-authored content
- if the file was created solely by the installer and becomes empty after block removal, uninstall may delete the empty file
- duplicate managed blocks produce a failed check state instead of auto-repair by overwrite
- corrupted block delimiters produce a failed check state instead of silent rewrite
- receipts record one of:
  - `inserted`
  - `updated`
  - `unchanged`
  - `removed`
- check surfaces can prove:
  - target file path
  - block id
  - template version
  - content hash
  - duplicate or corruption status

## Product Acceptance Criteria

- a user can run install multiple times without their global instruction file growing duplicate `vibe` bootstrap text
- a user can already have personal guidance in `AGENTS.md` or `CLAUDE.md` and keep it intact after install or upgrade
- a user can remove Vibe-Skills without losing unrelated host-wide instructions
- explicit `$vibe` or `/vibe` usage has a clearer and more durable host-side entry pull toward canonical `vibe`
- product messaging remains truthful that this is bootstrap guidance backed by checks and receipts, not hidden second-runtime authority

## User-Visible Behavior

- Codex install updates `~/.codex/AGENTS.md` by inserting a small managed `vibe` bootstrap block if needed
- Claude Code install updates `~/.claude/CLAUDE.md` by inserting the same kind of managed block adapted to Claude's instruction file
- OpenCode install updates `~/.config/opencode/AGENTS.md` by inserting the managed block without taking over `opencode.json`
- users continue invoking `vibe` the same way as before:
  - `$vibe`
  - `/vibe`
- users do not need to hand-edit the bootstrap block during normal install or upgrade flows
- if the managed block drifts or duplicates, `check` should report that clearly instead of silently repairing by overwrite

## Manual Spot Checks

- Install into a clean temporary Codex root with no `AGENTS.md`; confirm a single managed block is created.
- Install into a temporary Claude root that already has handwritten `CLAUDE.md` content; confirm that content is preserved and only one managed block is inserted.
- Run the same install command twice; confirm the second run reports `unchanged` and the file still contains a single managed block.
- Simulate an upgrade with a newer template version; confirm the managed block changes in place and unrelated file content is unchanged.
- Uninstall from a file that contains both user text and the managed block; confirm only the managed block is removed.
- Corrupt one block delimiter manually; confirm `check` fails instead of rewriting the file silently.
- Insert a second managed block manually; confirm `check` fails with duplicate-block drift.

## Completion Language Policy

Do not claim this enhancement is complete until install, upgrade, uninstall, and check flows all prove non-destructive managed-block behavior for the three supported hosts.

## Delivery Truth Contract

This enhancement is successful only when the system can prove all of the following at the same time:

- explicit `$vibe` and `/vibe` invocations have an official host bootstrap path
- bootstrap content is traceable to a single managed block identity
- user-authored host instruction content is never overwritten
- repeated install and upgrade do not multiply the bootstrap block
- canonical governed runtime authority still belongs to `vibe`, not the host rule file

## Artifact Review Requirements

- review the managed block wording for each host and confirm it does not imply second-runtime authority
- review uninstall semantics and confirm no whole-file delete happens unless the file is installer-created and empty after block removal
- review check output language and confirm duplicate and corruption states are explicit and actionable

## Code Task TDD Evidence Requirements

- add red tests proving a missing target file can be created with a single managed block
- add red tests proving existing user-authored content survives insertion
- add red tests proving repeated install produces `unchanged` and no duplicate block
- add red tests proving upgrade performs in-place block update
- add red tests proving uninstall removes only the managed block
- add red tests proving duplicate or corrupted blocks fail check instead of being overwritten

## Code Task TDD Exceptions

No code-task TDD exceptions were frozen for this run.

## Task-Specific Acceptance Extensions

- the managed block must have a stable block id such as `global-vibe-bootstrap`
- the managed block must carry enough identity for drift detection:
  - host
  - block id
  - template version
  - content hash or equivalent verifiable signature
- block markers must be explicit and machine-detectable
- the bootstrap template must stay short and must not inline the full `vibe` runtime contract
- the bootstrap text must instruct blocked reporting instead of silent fallback when canonical `vibe` cannot be loaded

## Research Augmentation Sources

- OpenAI Codex AGENTS.md guide: `https://developers.openai.com/codex/guides/agents-md`
- Claude Code memory and `CLAUDE.md` guide: `https://code.claude.com/docs/en/memory`
- OpenCode rules guide: `https://opencode.ai/docs/rules`
- `adapters/codex/host-profile.json`
- `adapters/claude-code/host-profile.json`
- `adapters/opencode/host-profile.json`
- `packages/installer-core/src/vgo_installer/install_runtime.py`
- `packages/installer-core/src/vgo_installer/materializer.py`
- `packages/installer-core/src/vgo_installer/host_closure.py`
- `packages/installer-core/src/vgo_installer/uninstall_service.py`
- `tests/runtime_neutral/test_bootstrap_doctor.py`
- `tests/runtime_neutral/test_claude_preview_scaffold.py`

## Primary Objective

Turn host-side `vibe` bootstrap into an officially declared, non-destructive, testable install capability instead of an implicit text convention.

## Non-Objective Proxy Signals

- appending more forceful prompt text without idempotent merge semantics
- treating host instruction files as the canonical runtime authority
- passing install even when duplicate or corrupted blocks are present
- preserving bootstrap convenience by overwriting user content

## Validation Material Role

Installer-core tests, runtime-neutral host checks, and generated bootstrap receipts are the source of truth for this enhancement.

## Anti-Proxy-Goal-Drift Tier

Tier 1 host-bootstrap integrity and governance-boundary preservation.

## Intended Scope

Global host instruction bootstrap for explicit `vibe` entry on Codex CLI, Claude Code, and OpenCode.

## Abstraction Layer Target

Adapter metadata, installer-core merge services, install and uninstall integration, and runtime-neutral host verification.

## Completion State

Complete only when the managed-block contract is encoded in metadata, templates, installer logic, uninstall logic, verification, and tests.

## Generalization Evidence Bundle

- host-profile metadata updates for three hosts
- bootstrap template files for three hosts
- merge-service unit tests
- runtime-neutral install and check tests
- uninstall and drift-detection tests

## Non-Goals

- do not make host global instruction files the canonical route authority
- do not implement a hidden second runtime behind `AGENTS.md` or `CLAUDE.md`
- do not promise host-kernel hard enforcement in this phase
- do not expand this turn to every preview host beyond `codex`, `claude-code`, and `opencode`
- do not take ownership of unrelated user-level instruction content
- do not redesign `vibe`'s six-stage runtime contract in this change

## Autonomy Mode

Interactive governed planning with implementation deferred until the requirement and execution plan are approved.

## Assumptions

- each target host will continue to load its documented global instruction surface
- explicit `$vibe` and `/vibe` remain the primary user-visible invocation tokens
- the current installer architecture can absorb a new managed-markdown-block service without changing canonical runtime authority
- existing host closure and bootstrap doctor surfaces are the right downstream places to expose proof that the bootstrap block is present and healthy

## Evidence Inputs

- Source task: design a detailed landing plan for install-time host global bootstrap injection under `$vibe`
- Relevant host surfaces:
  - `~/.codex/AGENTS.md`
  - `~/.claude/CLAUDE.md`
  - `~/.config/opencode/AGENTS.md`
- Relevant repo surfaces:
  - `packages/installer-core/src/vgo_installer/*`
  - `apps/vgo-cli/src/vgo_cli/*`
  - `tests/unit/*installer*`
  - `tests/runtime_neutral/test_bootstrap_doctor.py`
