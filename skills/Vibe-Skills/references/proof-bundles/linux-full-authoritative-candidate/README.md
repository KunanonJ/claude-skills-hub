# Linux Full-Authoritative Candidate Proof Bundle

This proof bundle contains the frozen fresh-machine Linux evidence for the `codex/linux` promotion candidate lane.

It is the canonical proof anchor for future no-regression checks and for any later promotion decision.

## Included Artifacts

- `manifest.json`
- `docs/universalization/linux-full-authoritative-contract.md`
- `docs/universalization/platform-promotion-criteria.md`
- `docs/status/platform-promotion-baseline-2026-03-13.md`
- `docs/status/linux-pwsh-fresh-machine-evidence-ledger-2026-03-13.md`
- `linux-pwsh-run-01-wsl/`
- `linux-pwsh-run-02-docker/`

## Purpose

The bundle prevents Linux promotion work from drifting into documentation-first claims.

It keeps three things coupled:

1. current status
2. required fresh-machine evidence
3. replay/no-overclaim synchronization

## Verification

Use:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-linux-pwsh-proof-gate.ps1 -WriteArtifacts
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-platform-promotion-bundle.ps1 -WriteArtifacts
```

Run these gates from the canonical git checkout root. They are governance proof gates, not installed-runtime self-checks.

The gates are expected to pass in pre-promotion mode, which means the proof artifacts must remain complete while replay/docs/release truth stays synchronized to `supported-with-constraints`.

## Distribution Rule

The frozen proof artifacts in this bundle, including the `*.log` evidence files referenced by `manifest.json`, are intentionally tracked in git.

That rule is part of the release-truth contract:

- a clean clone must contain the same proof files as the author machine
- proof-gate green must not depend on ignored local residue
- promotion truth must be reproducible from versioned repository contents alone
