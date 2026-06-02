# Windows Test Baseline Boundary Refactor Design

## Summary

The current Windows test baseline has nine stable failures in:

- `tests/unit/test_adapter_sdk.py`
- `tests/unit/test_vgo_cli_infra_split.py`
- `tests/unit/test_vgo_cli_installer_bridge.py`

These failures are not independent feature bugs. They point to three boundary
drifts:

1. Adapter target-root resolution mixes descriptor-contract strings with local
   filesystem path normalization.
2. CLI PowerShell execution tests still mock the pre-diagnostics
   `choose_powershell()` contract.
3. CLI install-ledger bridge tests still expect the core ledger payload only,
   while the bridge now attaches host runtime diagnostics when verification
   runtime support is importable.

This design fixes the test baseline by making those boundaries explicit. It is
a small boundary refactor, not a broad installer rewrite.

## Current Evidence

Fresh local evidence on Windows:

```powershell
python -m pytest tests/contract tests/unit -q
```

Current result:

```text
9 failed, 267 passed
```

The failing groups are:

- Six adapter-sdk target-root tests that expect POSIX-style test inputs such as
  `/home/tester` to stay POSIX-style, but the implementation returns
  Windows-shaped strings such as `\home\tester\.codex`.
- One CLI host target-root test where `/tmp/windsurf-home` is projected through
  Windows `Path` semantics and receives the current drive prefix.
- One CLI PowerShell process test that monkeypatches `choose_powershell` with
  the old zero-argument string-return contract while the implementation calls
  `choose_powershell(return_diagnostics=True)`.
- One installer bridge test that expects only `{"ok": true}` while
  `refresh_install_ledger_payload()` now appends `host_runtime` diagnostics when
  `vgo_verify.bootstrap_doctor_runtime` is available.

The current routing terminology gates are already green and must stay green:

```powershell
powershell -NoLogo -NoProfile -File scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
powershell -NoLogo -NoProfile -File scripts/verify/vibe-current-routing-debt-gate.ps1 -Json
```

Observed summary before this design:

- hard-cleanup `fail_count = 0`
- current-routing debt `P0 = 0`, `P1 = 0`, `P2 = 0`

## Goals

1. Make `python -m pytest tests/contract tests/unit -q` pass on the current
   Windows environment without using skip or xfail.
2. Separate descriptor-contract target-root strings from local filesystem
   `Path` projection.
3. Update CLI PowerShell tests to mock the current diagnostics contract.
4. Clarify that CLI install-ledger bridge output is the core ledger payload plus
   optional host runtime diagnostics.
5. Keep installation behavior, host defaults, runtime routing, and current
   terminology gates unchanged.

## Non-Goals

- Do not deploy or install this branch into Codex or any other host.
- Do not push to a remote.
- Do not rewrite adapter registry policy, host defaults, or install modes.
- Do not refactor the full installer, upgrade service, runtime readiness, or
  router stack.
- Do not clean historical terminology records or large runtime files in this
  change.
- Do not hide failures with skip, xfail, or looser assertions.

## Design

### 1. Adapter Target-Root Resolver Boundary

Affected implementation:

- `packages/adapter-sdk/src/vgo_adapters/target_root_resolver.py`

Affected tests:

- `tests/unit/test_adapter_sdk.py`

The adapter SDK resolver owns descriptor-contract semantics, not local
filesystem execution. It should return a stable target-root string from:

```text
descriptor + env + home
```

Rules:

- If the configured environment variable exists and is non-empty, return its
  value exactly as supplied.
- If `descriptor.default_target_root` is missing, keep raising `ValueError`.
- If `descriptor.default_target_root` is absolute, return it exactly as supplied.
- If `descriptor.default_target_root` is relative, join it to `home` using a
  small stable string join helper.
- If `home` uses POSIX separators, preserve POSIX separators.
- If `home` uses Windows separators or a Windows drive prefix, preserve Windows
  separators.

The resolver should avoid direct `Path(home) / rel` for contract output because
that converts synthetic POSIX test inputs into host-platform paths on Windows.

### 2. CLI Host Target-Root Projection Boundary

Affected implementation:

- `apps/vgo-cli/src/vgo_cli/hosts.py`

Affected tests:

- `tests/unit/test_vgo_cli_infra_split.py`

The CLI host layer can still return `Path` because downstream install and check
commands operate on the local filesystem. The debt is that registry-contract
inputs are currently projected through Windows `Path` semantics too early.

Design rule:

- Registry or installer-core target-root resolution should produce a stable
  target-root value first.
- CLI should convert that value to `Path` only at the CLI projection boundary.
- Unit tests that inject POSIX-shaped environment values must not be polluted by
  the current Windows drive.

Implementation can satisfy this either by reusing the adapter resolver helper or
by applying an equivalent boundary-preserving projection in the installer-core
path used by `vgo_cli.hosts.resolve_default_target_root()`. The selected
implementation should prefer the existing codebase ownership boundary and avoid
duplicating target-root policy.

### 3. PowerShell Diagnostics Contract Boundary

Affected implementation:

- `apps/vgo-cli/src/vgo_cli/process.py`

Affected tests:

- `tests/unit/test_vgo_cli_infra_split.py`

`choose_powershell()` now has two public call shapes:

- `choose_powershell()` returns a string path or `None`.
- `choose_powershell(return_diagnostics=True)` returns a diagnostics dictionary.

`run_powershell_file()` intentionally consumes the diagnostics form so it can
build better errors when no host is available.

Tests should mock the current diagnostics contract:

```python
{
    "host_path": "/usr/bin/pwsh",
    "host_kind": "pwsh",
    "fallback_used": False,
    "candidates_checked": [],
    "policy": {},
}
```

Expected command construction remains:

```text
pwsh -NoProfile -File <script> <args...>
```

For Windows PowerShell host kind, the command should still include:

```text
-ExecutionPolicy Bypass
```

Error behavior:

- If diagnostics are missing or `host_path` is empty, raise `CliError`.
- The error should include the script path and, when available, candidate paths
  or policy error text.

### 4. Install Ledger Diagnostics Boundary

Affected implementation:

- `apps/vgo-cli/src/vgo_cli/installer_bridge.py`

Affected tests:

- `tests/unit/test_vgo_cli_installer_bridge.py`

The bridge combines two responsibilities at the CLI boundary:

1. Delegate to installer core for ledger refresh.
2. Attach host runtime diagnostics when verification runtime support is
   available.

The core owner remains:

```text
vgo_installer.ledger_service.refresh_install_ledger()
```

The CLI owner remains:

```text
vgo_cli.installer_bridge.refresh_install_ledger_payload()
```

Rules:

- If ledger refresh raises `SystemExit`, wrap it in `CliError`.
- If `vgo_verify.bootstrap_doctor_runtime` is not importable because the
  `vgo_verify` root package is missing, return the core ledger payload
  unchanged.
- If another import error occurs, let it surface.
- If `collect_host_runtime()` is available, append `payload["host_runtime"]`.

Tests should stop asserting whole-payload equality for the diagnostics-enabled
path. They should assert:

- core ledger values remain present;
- `extend_workspace_package_path()` receives the repo root;
- `refresh_install_ledger()` receives the target root;
- diagnostics are attached when the doctor module is available;
- diagnostics are not attached when the `vgo_verify` package is unavailable.

## Testing Plan

Focused regression command:

```powershell
python -m pytest tests/unit/test_adapter_sdk.py tests/unit/test_vgo_cli_infra_split.py tests/unit/test_vgo_cli_installer_bridge.py -q
```

Acceptance command for the current baseline:

```powershell
python -m pytest tests/contract tests/unit -q
```

Terminology and routing-debt guardrails:

```powershell
powershell -NoLogo -NoProfile -File scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
powershell -NoLogo -NoProfile -File scripts/verify/vibe-current-routing-debt-gate.ps1 -Json
```

Optional smoke if implementation touches shared install or runtime helpers:

```powershell
powershell -NoLogo -NoProfile -File scripts/verify/vibe-pack-routing-smoke.ps1
```

Generated artifacts such as `.vibeskills/` or `docs/audits/` should be cleaned
before committing unless a specific test requires checking them in.

## Rollout and Risk

The primary risk is over-normalizing paths and accidentally changing real
Windows install behavior. The design mitigates this by:

- keeping adapter SDK output as a stable contract string;
- keeping CLI execution responsible for local `Path` projection;
- updating tests to assert the documented boundary instead of incidental host
  behavior.

The second risk is mutating installer bridge output expectations without
documenting ownership. The design treats `host_runtime` as CLI diagnostics, not
installer core state.

## Success Criteria

- `tests/contract tests/unit` pass on the current Windows machine.
- The three focused unit files pass without skip or xfail.
- The two current routing terminology gates still report zero blocking debt.
- No installation, deployment, push, or host-root mutation occurs.
- Final git diff is limited to the boundary implementation, tests, and any
  minimal supporting documentation required by the implementation plan.
