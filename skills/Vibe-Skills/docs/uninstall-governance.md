# Unified Uninstall Governance

**Status**: frozen 2026-03-30  
**Scope**: cover `codex`, `claude-code`, `cursor`, `windsurf`, `openclaw`, `opencode`, and the official install surface

This document defines the **owned-only uninstall** contract that balances default direct cleanup with proof-based safety. It is the canonical reference for gate automation, release notes, and operator guidance.

## Ownership Model

- **Ledger-first** – the installer writes `<target-root>/.vibeskills/install-ledger.json` (schema v1) enumerating created directories, files, JSON stanzas, runtime roots, and shared templates. The uninstaller consults this ledger before touching any path.
- **Host closure fallback** – when a ledger is missing (legacy installs or preview lanes), `.vibeskills/host-closure.json` provides the secondary evidence of what Vibe wrote and what can be tidied safely.
- **Workspace sidecar boundary** – `<workspace-root>/.vibeskills/project.json` and the governed runtime artifact tree under `.vibeskills/docs/**` / `.vibeskills/outputs/**` are workspace-owned, not host-install-owned. Host uninstall must leave them intact.
- **Legacy compatibility** – without ledger or closure proof, deletions are limited to clearly Vibe-owned host surfaces such as `.vibeskills/host-settings.json`, `.vibeskills/host-closure.json`, `.vibeskills/install-ledger.json`, payload copies documented in `adapters/*/closure.json`, and the `vibeskills` stanzas inside shared JSON owned targets.
- **Shared JSON sanitization** – `settings.json` and `opencode.json` are never wiped entirely unless the ledger proves Vibe created them from canonical templates and the file collapses to `{}` once the `vibeskills` segment is removed.
- **Owned-only receipts** – each uninstall run dumps `outputs/runtime/uninstall/<run-id>/uninstall-receipt.json` enumerating deleted, mutated, and skipped paths plus the ownership source that authorized each change (ledger, closure, legacy fallback).

## Host-specific rules (reference `adapters/*/closure.json`)

- `codex`: runtime assets (`skills/**`, `commands/**`, `rules/**`, `mcp/**`, `config/plugins-manifest.codex.json`, config locks) plus the canonical `skills/vibe/**`. `settings.json` is mutated only through the `vibeskills` stanza declared in the ledger.
- `claude-code` / `cursor`: runtime core payload, specialist wrappers, host closure, and `commands/**`. The ledger drives safe removal of the `settings.json` `vibeskills` stanza while preserving unrelated host settings.
- `windsurf` / `openclaw`: runtime core, workflow, and MCP payloads recorded in the ledger plus `.vibeskills/**`. `global_workflows/**` and `mcp_config.json` are deleted only when the ledger proves Vibe created them.
- `opencode`: runtime core, command/agent wrappers, example config, and `.vibeskills/**`. `opencode.json` only loses Vibe-managed nodes (never entire file unless ledger proves `vibeskills` created it).

When a target root contains both host-managed `.vibeskills/*` files and a workspace `project.json`, the uninstaller must degrade to targeted host-sidecar cleanup instead of removing the whole `.vibeskills/` directory.

## Verification & gate coverage

- Gate: `scripts/verify/vibe-uninstall-coherence-gate.ps1` ensures the repository exposes the new `uninstall.ps1`/`uninstall.sh` entrypoints, the governance doc above, the ledger contract in each adapter closure, and that no gate/README claims host-managed rollback.
- Docs & README updates must mention the authoritative uninstall path and reiterate the owned-only boundary so operators do not expect full host cleanup.

## Non-goals

- Do not reverse host-managed credentials, plugin provisioning, or login state.
- Do not extend the uninstaller into a “system recovery” tool or a general-purpose `rm -rf`.

Any future host or lane additions must update this document and the adapter closure metadata before gate scripts allow the new host to appear in the uninstall path.
