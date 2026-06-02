# No-Regression Proof Standard (Task 6 / Replay Harness)

> Status baseline: 2026-03-13  
> Scope: Task 6 of `docs/plans/2026-03-13-universal-vibeskills-execution-program.md`

This document defines the **minimum, conservative, replay-based proof standard** used by
the Task 6 harness to support a bounded claim:

- We can automatically detect regressions in **adapter/platform contract truth**, **offline provider-state degrade behavior**, **install isolation**, and **governed runtime contract smoke**.
- We do **not** overclaim full router-output replay parity or multi-OS execution parity beyond current evidence.

## Non-Negotiable Rule

The replay harness must remain **additive by default** and must not require changing the official runtime
main chain to pass unless the change is explicitly admitted by the file-scoped policy at
`config/official-runtime-main-chain-policy.json`.

Protected main-chain surfaces remain:

- `scripts/router/**`
- `scripts/bootstrap/**`
- `install.ps1` / `check.ps1`
- `install.sh` / `check.sh`
- `config/version-governance.json`

If the proof can only pass by changing those surfaces without an active, plan-backed, file-scoped
exception window, the proof is invalid.

If an exception window is used, it must:

- name the exact files allowed to change;
- point to the governing migration plan;
- keep the default mode frozen for every other protected path; and
- require fresh verification evidence for the exception batch.

## What This Harness Proves (Bounded)

### Adapter/platform contract baseline (offline contract-only)

Proves: the repo still carries a consistent, machine-readable adapter/platform contract surface
with explicit no-overclaim lanes and host-capability evidence.

Fixture:
- `tests/replay/fixtures/host-capability-matrix.json`

Gate:
- `scripts/verify/vibe-cross-host-route-parity-gate.ps1`

### Provider-state degrade contract (explicit abstention)

Proves: when provider state enters offline / missing-secret lanes, the relevant contract remains
explicit and machine-readable, with no silent behavior drift.

Fixture:
- `tests/replay/fixtures/provider-state-matrix.json`

Gate:
- `scripts/verify/vibe-cross-host-degrade-contract-gate.ps1`

### Install isolation (diff-based main-chain freeze)

Proves: the official-runtime protected paths stay frozen by default, and any approved exceptions
must be covered by the file-scoped main-chain policy window.

Evidence:
- `git status --porcelain`
- `config/official-runtime-main-chain-policy.json`

Gate:
- `scripts/verify/vibe-cross-host-install-isolation-gate.ps1`

### Governed runtime contract smoke

Proves: the governed runtime still emits the required stage artifacts, keeps `$vibe` as the
frozen runtime skill, and preserves the bounded specialist-dispatch contract in a fresh smoke run.

Evidence:
- fresh runtime smoke artifacts emitted under `.tmp/` or `outputs/verify/`

Gate:
- `scripts/verify/vibe-governed-runtime-contract-gate.ps1`

## How To Run (Task 6 Canonical)

From the repo root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-cross-host-route-parity-gate.ps1 -WriteArtifacts
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-cross-host-degrade-contract-gate.ps1 -WriteArtifacts
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-cross-host-install-isolation-gate.ps1 -WriteArtifacts
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-governed-runtime-contract-gate.ps1 -WriteArtifacts
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-universalization-no-regression-gate.ps1 -WriteArtifacts
```

The final aggregate gate transitively re-runs the governed runtime contract gate as part of the
canonical Batch C closure.

Artifacts are written under `outputs/verify/` when `-WriteArtifacts` is provided.
