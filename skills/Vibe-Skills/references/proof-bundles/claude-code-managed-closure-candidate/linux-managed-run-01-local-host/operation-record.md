# Claude Linux Managed Proof Run

- Lane: `claude-code/linux`
- Run ID: `linux-managed-run-01-local-host`
- Timestamp: `2026-03-31T15:33:38+08:00`
- Host type: real local Linux host
- Repo source: `<repo-root>`
- Run root: `<proof-run-root>`
- Target root: `<proof-target-root>`
- Commands:
  - `bash ./install.sh --host claude-code --profile full --target-root <proof-target-root>`
  - `bash ./check.sh --host claude-code --profile full --target-root <proof-target-root> --deep`
  - `pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/verify/vibe-bootstrap-doctor-gate.ps1 -TargetRoot <proof-target-root> -WriteArtifacts`
  - `python3 ./scripts/verify/runtime_neutral/coherence_gate.py --target-root <proof-target-root> --write-artifacts`
  - `claude --version`
  - `CLAUDE_HOME=<proof-target-root> claude agents`

## Outcome

- `install.sh` passed with `Gate Result: PASS` from the installed runtime freshness gate
- `check.sh --deep` passed with `Result: 67 passed, 0 failed, 1 warnings`
- the single warning is the expected deep-doctor skip for adapter mode `preview-guidance`
- `vibe-bootstrap-doctor-gate.ps1` returned `manual_actions_pending`, which is truthful for a host-managed lane and does not invalidate the bounded Claude managed-closure proof
- `coherence_gate.py` passed
- the real local `claude` CLI binary returned `2.1.81 (Claude Code)`
- `CLAUDE_HOME=<target-root> claude agents` returned a successful agent listing, which is a command-level smoke result against the managed target root

## Boundary

This run proves the bounded Linux Claude managed-closure lane can install, check, and survive a real CLI command surface on a clean target root.

It does not prove:

- official-runtime ownership
- Windows or macOS support
- whole-host safety across every Claude startup path
