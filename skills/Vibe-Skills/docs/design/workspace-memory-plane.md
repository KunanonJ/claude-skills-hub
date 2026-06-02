# Workspace Memory Plane

## Goal

Wave C introduces a single workspace-scoped broker for memory lanes so continuity survives run/session/host boundaries without introducing a second runtime control plane.

## Topology

1. Workspace identity is anchored by `.vibeskills/project.json`.
2. The broker resolves one shared plane file under `.vibeskills/memory/workspace-memory-plane.jsonl`.
3. Lane-specific adapters (`serena`, `ruflo`, `cognee`) map to logical kinds inside that plane instead of separate physical stores.

## Driver Roles

- `workspace_memory_driver.py`: canonical broker implementation.
  - owns workspace descriptor reconciliation
  - owns read ranking and write admission/noise filtering
  - emits capsule metadata + compatibility response fields
- `memory_backend_driver.py`: compatibility shell.
  - preserves legacy CLI contract
  - routes to workspace broker only
  - hard-fails when the workspace broker is unavailable
  - rejects all legacy compatibility modes, including explicit CLI/env overrides
- `VibeWorkspaceMemory.Common.ps1`: thin PowerShell bridge to broker contract.

## Ingest Noise Suppression

The broker applies write admission before persistence:

- reject structurally empty records
- suppress telemetry/tmp-heavy, temp-path-only low-signal writes
- preserve explicit decision/handoff/relation signals

This keeps continuity useful while avoiding low-value memory spam.

## Compatibility Notes

Runtime callers can continue consuming:

- `status`
- `item_count`
- `items`

New callers can consume:

- `capsules`
- `suppressed_count`
- `workspace_memory_plane`

No host adapter should depend on lane-local physical storage paths.

## Migration And Deprecation

- Legacy lane-local JSONL files are no longer an active read/write path once the workspace broker is enabled.
- `memory_backend_driver.py` remains only as a compatibility shell for the existing CLI contract; it routes to the workspace broker and hard-fails if that broker is unavailable.
- There is no silent downgrade back to legacy storage and no automatic import of old lane-local rows into the shared plane.
- If a maintainer needs to preserve historical legacy rows, migration must be an explicit one-off operation with workspace identity review instead of an implicit runtime side effect.
