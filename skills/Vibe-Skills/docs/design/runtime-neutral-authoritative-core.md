# Runtime-Neutral Authoritative Core

> Status: active migration design
> Baseline: 2026-03-13

## Problem

The previous official-runtime authority path was PowerShell-first.

That was acceptable while Windows remained the only proven authoritative lane, but it prevented Linux from being promoted truthfully. The issue was not shell entrypoints alone. The issue was that the authoritative semantics for freshness, coherence, and bootstrap doctor lived behind PowerShell-only execution.

## Design Goal

Extract authoritative decision logic into a runtime-neutral core while preserving:

- exit semantics
- receipt semantics
- operator-visible failure classes
- Windows baseline authority

This is not a shell rewrite project.
It is a semantic extraction project.

## Current Architecture

### Runtime-neutral core

The shared core now lives under:

- `scripts/verify/runtime_neutral/freshness_gate.py`
- `scripts/verify/runtime_neutral/coherence_gate.py`
- `scripts/verify/runtime_neutral/bootstrap_doctor.py`

These Python modules own the portable decision logic.

### Wrappers

Wrappers remain host-facing entrypoints:

- `install.sh`
- `check.sh`
- existing PowerShell gates and wrappers on Windows

Wrapper responsibilities are intentionally narrow:

1. parse arguments
2. resolve repo/target paths
3. invoke the runtime-neutral core first where supported
4. fall back to PowerShell where contract still requires it
5. preserve explicit warning behavior when neither path is available

### Governance boundary

Protected official-runtime surfaces remain frozen by default and are only thawed through:

- `config/official-runtime-main-chain-policy.json`

This keeps the migration file-scoped and reviewable.

## What Has Been Implemented

The current migration batch has already completed these steps:

1. added runtime-neutral freshness, coherence, and bootstrap-doctor cores
2. wired `install.sh` to prefer the runtime-neutral freshness gate before PowerShell fallback
3. wired `check.sh` to prefer runtime-neutral freshness, coherence, and bootstrap-doctor execution before PowerShell fallback
4. updated one-shot setup messaging so Linux without `pwsh` does not falsely imply that authoritative verification simply “did not run” when a runtime-neutral path was actually used

## What Has Not Been Claimed

This design does **not** yet prove:

- Linux is `full-authoritative`
- receipt parity is frozen across all hosts
- fresh-machine Linux closure is complete
- PowerShell can be removed from Windows authority

Those are proof outcomes, not design assumptions.

## Verification Model

The design is currently guarded by:

- `tests/runtime_neutral/test_freshness_gate.py`
- `tests/runtime_neutral/test_bootstrap_doctor.py`
- `tests/runtime_neutral/test_coherence_gate.py`
- `scripts/verify/vibe-cross-host-install-isolation-gate.ps1`
- `scripts/verify/vibe-universalization-no-regression-gate.ps1`

The combination matters:

- Python tests validate portable semantics.
- shell syntax checks validate wrapper integrity.
- governance gates prove the migration stayed inside an approved main-chain change window and did not weaken the broader universalization contract.

## Promotion Boundary

The runtime-neutral core is a necessary condition for Linux promotion, but not a sufficient one.

Promotion still requires:

1. Linux fresh-machine evidence
2. replay fixture updates
3. platform contract updates
4. public-truth synchronization
5. Windows baseline preservation in the same batch

Until then, the runtime-neutral core should be described as **promotion-enabling infrastructure**, not as proof of parity.
