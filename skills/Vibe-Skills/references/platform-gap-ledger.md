# Platform Gap Ledger

## Active Gaps

### Gap 1: Linux without `pwsh` is still a degraded lane

- Current impact: authoritative closure is intentionally limited without `pwsh`.
- Required closure: keep the degraded contract explicit and prove it never drifts into fake full-support wording.

### Gap 2: macOS is not frozen as a proof lane

- Current impact: shell entry points exist, but no measured closure contract is recorded.
- Required closure: separate platform contract + replay evidence.

### Gap 3: Claude Code platform support is template-level, not closure-level

- Current impact: repository exposes intent, not proof.
- Required closure: adapter replay, install isolation, and host-managed boundary validation.

### Gap 4: OpenCode remains target-state only

- Current impact: it is a roadmap host, not a verified adapter.
- Required closure: real host contract before any support claim.

## Recently Closed

### Closed 1: Linux full-authoritative promotion sync is complete

- Result: `codex/linux` is now promoted truthfully when `pwsh` is available.
- Closure evidence: frozen proof bundle, synchronized replay allowlist, aligned adapter contract, and passing promotion bundle gate.
