# Windows Test Baseline Boundary Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the current Windows `tests/contract tests/unit` baseline pass by separating target-root string contracts, CLI filesystem projection, PowerShell diagnostics mocks, and installer-ledger diagnostics assertions.

**Architecture:** Move host target-root string semantics into a shared contracts helper and keep local `Path` resolution at installer/CLI boundaries. Update tests to assert current diagnostics-enabled behavior instead of old incidental shapes, while preserving installer behavior and current routing terminology gates.

**Tech Stack:** Python 3, pytest, pathlib, shared `vgo_contracts`, adapter SDK, installer-core, VGO CLI, PowerShell verification gates.

---

## File Structure

- Create: `packages/contracts/src/vgo_contracts/target_root_contract.py`
  - Owns platform-stable descriptor/registry target-root string resolution from `default_target_root`, environment, and home text.
- Modify: `packages/contracts/src/vgo_contracts/__init__.py`
  - Exports the shared target-root string helper for package-owned callers.
- Modify: `packages/adapter-sdk/src/vgo_adapters/target_root_resolver.py`
  - Delegates adapter descriptor target-root string output to the shared contract helper.
- Modify: `packages/installer-core/src/vgo_installer/adapter_registry.py`
  - Adds a target-root text resolver for registry semantics while preserving existing resolved-`Path` installer behavior.
- Modify: `apps/vgo-cli/src/vgo_cli/hosts.py`
  - Uses the registry text resolver before converting to `Path`, avoiding Windows drive-prefix pollution in synthetic POSIX env values.
- Modify: `tests/unit/test_adapter_sdk.py`
  - Verifies POSIX and Windows home separators are preserved by adapter SDK target-root resolution.
- Modify: `tests/unit/test_installer_adapter_registry_target_roots.py`
  - Verifies installer-core exposes stable target-root text while keeping existing resolved `Path` behavior.
- Modify: `tests/unit/test_vgo_cli_infra_split.py`
  - Verifies CLI default target-root projection and current PowerShell diagnostics command construction.
- Modify: `tests/unit/test_vgo_cli_installer_bridge.py`
  - Verifies installer bridge returns the core ledger payload plus optional host runtime diagnostics.

Do not modify:

- `config/adapter-registry.json`
- install scripts, runtime materialization scripts, or host roots under `C:\Users\羽裳\.codex`
- routing manifests or current routing terminology policy files, except if final guardrails expose an unrelated regression that must be reported separately

---

## Current Failing Baseline

Fresh focused command on Windows:

```powershell
python -m pytest tests\unit\test_adapter_sdk.py tests\unit\test_vgo_cli_infra_split.py tests\unit\test_vgo_cli_installer_bridge.py -q
```

Observed result before this plan:

```text
9 failed, 9 passed
```

The failures are:

- six adapter SDK assertions converting `/home/tester/...` into `\home\tester\...`;
- one CLI Windsurf env projection converting `/tmp/windsurf-home` into `F:\tmp\windsurf-home`;
- one PowerShell process test mocking `choose_powershell()` with the old zero-argument contract;
- one installer bridge test asserting only `{"ok": true}` while `host_runtime` diagnostics are now attached when `vgo_verify.bootstrap_doctor_runtime` is importable.

---

### Task 1: Add Shared Target-Root Text Contract

**Files:**

- Create: `packages/contracts/src/vgo_contracts/target_root_contract.py`
- Modify: `packages/contracts/src/vgo_contracts/__init__.py`
- Modify: `tests/unit/test_adapter_sdk.py`

- [ ] **Step 1: Add adapter SDK regression tests for stable target-root strings**

In `tests/unit/test_adapter_sdk.py`, add this import near the existing imports:

```python
from types import SimpleNamespace
```

Add these tests after `test_target_root_resolver_uses_env_when_available`:

```python
def test_target_root_resolver_preserves_windows_home_separators() -> None:
    descriptor = load_descriptor('codex')
    resolved = resolve_default_target_root(descriptor, env={}, home=r'C:\Users\tester')
    assert resolved == r'C:\Users\tester\.codex'


def test_target_root_resolver_returns_absolute_default_exactly() -> None:
    descriptor = SimpleNamespace(
        id='demo',
        default_target_root='/opt/vgo-demo',
        default_target_root_env='',
        default_target_root_kind='fixed',
    )

    resolved = resolve_default_target_root(descriptor, env={}, home=r'C:\Users\tester')

    assert resolved == '/opt/vgo-demo'
```

- [ ] **Step 2: Run adapter SDK tests and verify the current failure**

Run:

```powershell
python -m pytest tests\unit\test_adapter_sdk.py -q
```

Expected: FAIL. Existing POSIX-home tests should still show Windows backslash output such as `\home\tester\.codex`.

- [ ] **Step 3: Create the shared target-root text contract**

Create `packages/contracts/src/vgo_contracts/target_root_contract.py` with this exact content:

```python
from __future__ import annotations

from pathlib import Path
from typing import Mapping


def _clean_text(value: object) -> str:
    return str(value or "").strip()


def _is_absolute_target_root(value: str) -> bool:
    if value.startswith("/") or value.startswith("\\"):
        return True
    return len(value) >= 3 and value[1] == ":" and value[2] in {"/", "\\"}


def _looks_windows_path(value: str) -> bool:
    if "\\" in value:
        return True
    return len(value) >= 2 and value[1] == ":"


def _join_target_root_text(home: str, relative: str) -> str:
    home_text = _clean_text(home)
    rel_text = _clean_text(relative)
    if not home_text:
        raise ValueError("home is required for relative target root")
    separator = "\\" if _looks_windows_path(home_text) else "/"
    cleaned_home = home_text.rstrip("/\\")
    cleaned_rel = rel_text.replace("\\", "/").strip("/")
    return cleaned_home + separator + cleaned_rel.replace("/", separator)


def resolve_target_root_text(
    *,
    default_target_root: object,
    default_target_root_env: object = "",
    env: Mapping[str, str] | None = None,
    home: object | None = None,
    descriptor_id: object = "adapter",
) -> str:
    env_map = env or {}
    env_name = _clean_text(default_target_root_env)
    if env_name:
        env_value = _clean_text(env_map.get(env_name, ""))
        if env_value:
            return env_value

    rel = _clean_text(default_target_root)
    if not rel:
        raise ValueError(f"missing default target root for {_clean_text(descriptor_id) or 'adapter'}")
    if _is_absolute_target_root(rel):
        return rel

    home_text = _clean_text(home) if home is not None else str(Path.home())
    return _join_target_root_text(home_text, rel)
```

- [ ] **Step 4: Export the helper from contracts**

In `packages/contracts/src/vgo_contracts/__init__.py`, add this import after the `adapter_registry_support` imports:

```python
from .target_root_contract import resolve_target_root_text
```

Add this string to `__all__` after `'resolve_adapter_registry_path'`:

```python
    'resolve_target_root_text',
```

- [ ] **Step 5: Run a syntax check for the new contracts module**

Run:

```powershell
python -m py_compile packages\contracts\src\vgo_contracts\target_root_contract.py
```

Expected: exit code `0` and no output.

- [ ] **Step 6: Commit the shared contract test and helper**

Commit:

```powershell
git add packages\contracts\src\vgo_contracts\target_root_contract.py packages\contracts\src\vgo_contracts\__init__.py tests\unit\test_adapter_sdk.py
git commit -m "test: define stable target root text contract"
```

Expected: commit succeeds. Adapter SDK tests still fail until Task 2 delegates to the helper.

---

### Task 2: Apply Target-Root Contract To Adapter SDK And CLI Boundary

**Files:**

- Modify: `packages/adapter-sdk/src/vgo_adapters/target_root_resolver.py`
- Modify: `packages/installer-core/src/vgo_installer/adapter_registry.py`
- Modify: `apps/vgo-cli/src/vgo_cli/hosts.py`
- Modify: `tests/unit/test_installer_adapter_registry_target_roots.py`
- Modify: `tests/unit/test_vgo_cli_infra_split.py`

- [ ] **Step 1: Add installer-core text projection tests**

In `tests/unit/test_installer_adapter_registry_target_roots.py`, update the import block from `vgo_installer.adapter_registry` to include `resolve_default_target_root_text`:

```python
from vgo_installer.adapter_registry import (
    resolve_canonical_vibe_contract,
    resolve_default_target_root,
    resolve_default_target_root_text,
    resolve_matching_target_root_hosts,
    resolve_target_root_owner,
    resolve_target_root_spec,
)
```

Add these tests immediately before `test_resolve_default_target_root_uses_env_projection`:

```python
def test_resolve_default_target_root_text_preserves_env_projection() -> None:
    resolved = resolve_default_target_root_text(
        REPO_ROOT,
        'windsurf',
        env={'WINDSURF_HOME': '/tmp/windsurf-home'},
        home='/home/tester',
    )

    assert resolved == '/tmp/windsurf-home'


def test_resolve_default_target_root_text_preserves_posix_home_projection() -> None:
    resolved = resolve_default_target_root_text(
        REPO_ROOT,
        'opencode',
        env={},
        home='/home/tester',
    )

    assert resolved == '/home/tester/.config/opencode'
```

- [ ] **Step 2: Run target-root tests and verify failures**

Run:

```powershell
python -m pytest tests\unit\test_adapter_sdk.py tests\unit\test_installer_adapter_registry_target_roots.py tests\unit\test_vgo_cli_infra_split.py::test_resolve_default_target_root_uses_registry_env_projection -q
```

Expected: FAIL. The new installer-core tests should fail because `resolve_default_target_root_text` does not exist yet, and existing adapter/CLI tests should still show Windows path projection drift.

- [ ] **Step 3: Delegate adapter SDK resolution to the shared contract**

Replace all content in `packages/adapter-sdk/src/vgo_adapters/target_root_resolver.py` with:

```python
from vgo_contracts.target_root_contract import resolve_target_root_text


def resolve_default_target_root(descriptor, *, env: dict[str, str] | None = None, home: str | None = None) -> str:
    return resolve_target_root_text(
        default_target_root=getattr(descriptor, "default_target_root", ""),
        default_target_root_env=getattr(descriptor, "default_target_root_env", ""),
        env=env,
        home=home,
        descriptor_id=getattr(descriptor, "id", "adapter"),
    )
```

- [ ] **Step 4: Add installer-core text resolver while preserving resolved Path behavior**

In `packages/installer-core/src/vgo_installer/adapter_registry.py`, add this import after the existing `vgo_contracts.adapter_registry_support` import block:

```python
from vgo_contracts.target_root_contract import resolve_target_root_text
```

Replace `resolve_default_target_root` with these two functions:

```python
def resolve_default_target_root_text(
    repo_root: Path,
    host_id: str,
    *,
    env: dict[str, str] | None = None,
    home: str | Path | None = None,
) -> str:
    normalized, spec = resolve_target_root_spec(repo_root, host_id)
    return resolve_target_root_text(
        default_target_root=spec["rel"],
        default_target_root_env=spec["env"],
        env=env or dict(os.environ),
        home=home if home is not None else Path.home(),
        descriptor_id=normalized,
    )


def resolve_default_target_root(
    repo_root: Path,
    host_id: str,
    *,
    env: dict[str, str] | None = None,
    home: str | Path | None = None,
) -> Path:
    target_root = resolve_default_target_root_text(repo_root, host_id, env=env, home=home)
    return Path(target_root).expanduser().resolve()
```

This keeps existing installer-core callers on the resolved local filesystem `Path` contract.

- [ ] **Step 5: Move CLI default target-root projection to the text boundary**

In `apps/vgo-cli/src/vgo_cli/hosts.py`, replace `resolve_default_target_root` with:

```python
def resolve_default_target_root(host_id: str) -> Path:
    repo_root, module = _installer_registry_module()
    requested_host = str(host_id or os.environ.get('VCO_HOST_ID') or '').strip()
    try:
        target_root_text = module.resolve_default_target_root_text(
            repo_root,
            requested_host,
            env=dict(os.environ),
            home=str(Path.home()),
        )
        return Path(str(target_root_text)).expanduser()
    except SystemExit as exc:
        _raise_host_error(host_id, exc)
```

Keep `resolve_target_root(host_id, target_root)` unchanged so explicit user-provided roots still use `Path(...).expanduser().resolve()`.

- [ ] **Step 6: Run focused target-root tests and verify they pass**

Run:

```powershell
python -m pytest tests\unit\test_adapter_sdk.py tests\unit\test_installer_adapter_registry_target_roots.py tests\unit\test_vgo_cli_infra_split.py::test_resolve_default_target_root_uses_registry_env_projection -q
```

Expected: PASS.

- [ ] **Step 7: Run CLI install-support tests that consume host target roots**

Run:

```powershell
python -m pytest tests\unit\test_vgo_cli_commands.py tests\unit\test_vgo_cli_install_support.py tests\unit\test_vgo_cli_install_gates.py -q
```

Expected: PASS.

- [ ] **Step 8: Commit target-root boundary refactor**

Commit:

```powershell
git add packages\adapter-sdk\src\vgo_adapters\target_root_resolver.py packages\installer-core\src\vgo_installer\adapter_registry.py apps\vgo-cli\src\vgo_cli\hosts.py tests\unit\test_installer_adapter_registry_target_roots.py tests\unit\test_vgo_cli_infra_split.py
git commit -m "refactor: separate target root text and path projection"
```

Expected: commit succeeds.

---

### Task 3: Update PowerShell Diagnostics Contract Tests

**Files:**

- Modify: `tests/unit/test_vgo_cli_infra_split.py`

- [ ] **Step 1: Update the current PowerShell command test to mock diagnostics**

In `tests/unit/test_vgo_cli_infra_split.py`, replace the monkeypatch line in `test_run_powershell_file_composes_no_profile_command`:

```python
    monkeypatch.setattr(cli_process, 'choose_powershell', lambda: '/usr/bin/pwsh')
```

with this diagnostics-aware fake:

```python
    def fake_choose_powershell(*, return_diagnostics: bool = False) -> dict[str, object] | str:
        assert return_diagnostics is True
        return {
            'host_path': '/usr/bin/pwsh',
            'host_kind': 'pwsh',
            'fallback_used': False,
            'candidates_checked': [],
            'policy': {},
        }

    monkeypatch.setattr(cli_process, 'choose_powershell', fake_choose_powershell)
```

- [ ] **Step 2: Add Windows PowerShell execution-policy coverage**

Add this test after `test_run_powershell_file_composes_no_profile_command`:

```python
def test_run_powershell_file_adds_execution_policy_for_windows_powershell(monkeypatch: pytest.MonkeyPatch) -> None:
    recorded: dict[str, object] = {}

    def fake_run_subprocess(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        recorded['command'] = list(command)
        recorded['cwd'] = cwd
        return subprocess.CompletedProcess(args=list(command), returncode=0, stdout='', stderr='')

    def fake_choose_powershell(*, return_diagnostics: bool = False) -> dict[str, object]:
        assert return_diagnostics is True
        return {
            'host_path': 'powershell.exe',
            'host_kind': 'windows-powershell',
            'fallback_used': True,
            'candidates_checked': [],
            'policy': {},
        }

    monkeypatch.setattr(cli_process, 'choose_powershell', fake_choose_powershell)
    monkeypatch.setattr(cli_process, 'run_subprocess', fake_run_subprocess)

    result = run_powershell_file(Path('/tmp/test.ps1'), '-TargetRoot', '/tmp/out')

    assert result.returncode == 0
    assert recorded['command'] == [
        'powershell.exe',
        '-NoProfile',
        '-ExecutionPolicy',
        'Bypass',
        '-File',
        '/tmp/test.ps1',
        '-TargetRoot',
        '/tmp/out',
    ]
```

- [ ] **Step 3: Add missing-host error coverage**

Add this test after the Windows PowerShell test:

```python
def test_run_powershell_file_error_includes_script_and_resolution_details(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_choose_powershell(*, return_diagnostics: bool = False) -> dict[str, object]:
        assert return_diagnostics is True
        return {
            'host_path': None,
            'host_kind': None,
            'fallback_used': False,
            'candidates_checked': [
                {'candidate_name': 'path-pwsh', 'candidate_path': None},
                {'candidate_name': 'default-pwsh', 'candidate_path': r'C:\Program Files\PowerShell\7\pwsh.exe'},
            ],
            'policy': {},
            'error': 'pwsh is required on non-Windows hosts',
        }

    monkeypatch.setattr(cli_process, 'choose_powershell', fake_choose_powershell)

    with pytest.raises(CliError) as excinfo:
        run_powershell_file(Path('/tmp/test.ps1'), '-TargetRoot', '/tmp/out')

    message = str(excinfo.value)
    assert '/tmp/test.ps1' in message
    assert 'pwsh is required on non-Windows hosts' in message
    assert 'path-pwsh' in message
    assert r'C:\Program Files\PowerShell\7\pwsh.exe' in message
```

- [ ] **Step 4: Run the PowerShell process tests**

Run:

```powershell
python -m pytest tests\unit\test_vgo_cli_infra_split.py::test_run_powershell_file_composes_no_profile_command tests\unit\test_vgo_cli_infra_split.py::test_run_powershell_file_adds_execution_policy_for_windows_powershell tests\unit\test_vgo_cli_infra_split.py::test_run_powershell_file_error_includes_script_and_resolution_details -q
```

Expected: PASS. No implementation change should be needed because `apps/vgo-cli/src/vgo_cli/process.py` already consumes `choose_powershell(return_diagnostics=True)`.

- [ ] **Step 5: Commit diagnostics-contract tests**

Commit:

```powershell
git add tests\unit\test_vgo_cli_infra_split.py
git commit -m "test: update powershell diagnostics contract"
```

Expected: commit succeeds.

---

### Task 4: Make Installer Bridge Diagnostics Boundary Explicit

**Files:**

- Modify: `tests/unit/test_vgo_cli_installer_bridge.py`

- [ ] **Step 1: Add builtins import**

In `tests/unit/test_vgo_cli_installer_bridge.py`, add this import at the top:

```python
import builtins
```

- [ ] **Step 2: Replace the core delegation test with diagnostics-enabled assertions**

Replace `test_refresh_install_ledger_payload_delegates_to_installer_core` with:

```python
def test_refresh_install_ledger_payload_delegates_to_installer_core(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    recorded: dict[str, object] = {}

    def fake_extend(repo_root: Path) -> None:
        recorded['repo_root'] = repo_root

    def fake_refresh(target_root: Path) -> dict[str, object]:
        recorded['target_root'] = target_root
        return {'ok': True}

    def fake_collect_host_runtime(repo_root: Path, target_root: Path) -> dict[str, object]:
        recorded['runtime_repo_root'] = repo_root
        recorded['runtime_target_root'] = target_root
        return {'vibe_host_ready': True, 'source': 'test'}

    pkg = types.ModuleType('vgo_installer')
    pkg.__path__ = []
    ledger = types.ModuleType('vgo_installer.ledger_service')
    ledger.refresh_install_ledger = fake_refresh
    verify_pkg = types.ModuleType('vgo_verify')
    verify_pkg.__path__ = []
    doctor = types.ModuleType('vgo_verify.bootstrap_doctor_runtime')
    doctor.collect_host_runtime = fake_collect_host_runtime

    monkeypatch.setattr(installer_bridge, 'extend_workspace_package_path', fake_extend)
    monkeypatch.setitem(sys.modules, 'vgo_installer', pkg)
    monkeypatch.setitem(sys.modules, 'vgo_installer.ledger_service', ledger)
    monkeypatch.setitem(sys.modules, 'vgo_verify', verify_pkg)
    monkeypatch.setitem(sys.modules, 'vgo_verify.bootstrap_doctor_runtime', doctor)

    payload = refresh_install_ledger_payload(tmp_path / 'repo', tmp_path / 'target')

    assert payload['ok'] is True
    assert payload['host_runtime'] == {'vibe_host_ready': True, 'source': 'test'}
    assert recorded['repo_root'] == tmp_path / 'repo'
    assert recorded['target_root'] == tmp_path / 'target'
    assert recorded['runtime_repo_root'] == tmp_path / 'repo'
    assert recorded['runtime_target_root'] == tmp_path / 'target'
```

- [ ] **Step 3: Add missing verification-root fallback test**

Add this test after the delegation test:

```python
def test_refresh_install_ledger_payload_returns_core_payload_when_vgo_verify_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def fake_refresh(target_root: Path) -> dict[str, object]:
        return {'ok': True, 'target': str(target_root)}

    real_import = builtins.__import__

    def fake_import(name: str, *args: object, **kwargs: object) -> object:
        if name == 'vgo_verify.bootstrap_doctor_runtime':
            raise ModuleNotFoundError("No module named 'vgo_verify'", name='vgo_verify')
        return real_import(name, *args, **kwargs)

    pkg = types.ModuleType('vgo_installer')
    pkg.__path__ = []
    ledger = types.ModuleType('vgo_installer.ledger_service')
    ledger.refresh_install_ledger = fake_refresh

    monkeypatch.setattr(installer_bridge, 'extend_workspace_package_path', lambda _: None)
    monkeypatch.setattr(builtins, '__import__', fake_import)
    monkeypatch.setitem(sys.modules, 'vgo_installer', pkg)
    monkeypatch.setitem(sys.modules, 'vgo_installer.ledger_service', ledger)

    payload = refresh_install_ledger_payload(tmp_path / 'repo', tmp_path / 'target')

    assert payload == {'ok': True, 'target': str(tmp_path / 'target')}
```

- [ ] **Step 4: Add non-root import error surfacing test**

Add this test after the missing-root test:

```python
def test_refresh_install_ledger_payload_surfaces_nested_doctor_import_errors(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def fake_refresh(_: Path) -> dict[str, object]:
        return {'ok': True}

    real_import = builtins.__import__

    def fake_import(name: str, *args: object, **kwargs: object) -> object:
        if name == 'vgo_verify.bootstrap_doctor_runtime':
            raise ModuleNotFoundError(
                "No module named 'vgo_verify.bootstrap_doctor_runtime'",
                name='vgo_verify.bootstrap_doctor_runtime',
            )
        return real_import(name, *args, **kwargs)

    pkg = types.ModuleType('vgo_installer')
    pkg.__path__ = []
    ledger = types.ModuleType('vgo_installer.ledger_service')
    ledger.refresh_install_ledger = fake_refresh

    monkeypatch.setattr(installer_bridge, 'extend_workspace_package_path', lambda _: None)
    monkeypatch.setattr(builtins, '__import__', fake_import)
    monkeypatch.setitem(sys.modules, 'vgo_installer', pkg)
    monkeypatch.setitem(sys.modules, 'vgo_installer.ledger_service', ledger)

    with pytest.raises(ModuleNotFoundError, match='bootstrap_doctor_runtime'):
        refresh_install_ledger_payload(tmp_path / 'repo', tmp_path / 'target')
```

- [ ] **Step 5: Run installer bridge tests**

Run:

```powershell
python -m pytest tests\unit\test_vgo_cli_installer_bridge.py -q
```

Expected: PASS. No implementation change should be needed because `apps/vgo-cli/src/vgo_cli/installer_bridge.py` already appends `host_runtime` only when the doctor runtime module is available.

- [ ] **Step 6: Commit installer bridge diagnostics tests**

Commit:

```powershell
git add tests\unit\test_vgo_cli_installer_bridge.py
git commit -m "test: document installer bridge runtime diagnostics"
```

Expected: commit succeeds.

---

### Task 5: Close Windows Unit And Contract Baseline

**Files:**

- Verify only unless a test failure points to a missed boundary in files already listed above.

- [ ] **Step 1: Run the original focused failing group**

Run:

```powershell
python -m pytest tests\unit\test_adapter_sdk.py tests\unit\test_vgo_cli_infra_split.py tests\unit\test_vgo_cli_installer_bridge.py -q
```

Expected: PASS.

- [ ] **Step 2: Run related installer and CLI unit tests**

Run:

```powershell
python -m pytest tests\unit\test_installer_adapter_registry_target_roots.py tests\unit\test_vgo_cli_commands.py tests\unit\test_vgo_cli_install_support.py tests\unit\test_vgo_cli_install_gates.py tests\unit\test_vgo_cli_process.py -q
```

Expected: PASS.

- [ ] **Step 3: Run the current Windows unit/contract acceptance command**

Run:

```powershell
python -m pytest tests\contract tests\unit -q
```

Expected: PASS. The previous local baseline was `9 failed, 267 passed`; this task is complete only when those nine failures are gone without skip or xfail.

- [ ] **Step 4: Run current terminology and routing debt guardrails**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
```

Expected:

```text
vibe-routing-terminology-hard-cleanup-scan.ps1: status pass, summary.fail_count 0
vibe-current-routing-debt-gate.ps1: status pass, summary.P0 0, summary.P1 0, summary.P2 0
```

- [ ] **Step 5: Run whitespace check**

Run:

```powershell
git diff --check
```

Expected: exit code `0` and no output.

- [ ] **Step 6: Inspect changed files**

Run:

```powershell
git status --short
```

Expected: only files from this plan are changed. There should be no generated `.vibeskills/`, `docs/audits/`, host-root, or install-output artifacts staged.

- [ ] **Step 7: Commit final verification fixes only if needed**

If Step 3 or Step 4 required a small fix in a planned file, commit it:

```powershell
git add packages\contracts\src\vgo_contracts\target_root_contract.py packages\contracts\src\vgo_contracts\__init__.py packages\adapter-sdk\src\vgo_adapters\target_root_resolver.py packages\installer-core\src\vgo_installer\adapter_registry.py apps\vgo-cli\src\vgo_cli\hosts.py tests\unit\test_adapter_sdk.py tests\unit\test_installer_adapter_registry_target_roots.py tests\unit\test_vgo_cli_infra_split.py tests\unit\test_vgo_cli_installer_bridge.py
git commit -m "test: close windows unit baseline boundary drift"
```

If no tracked files changed after earlier commits, do not create an empty commit.

---

## Completion Criteria

The implementation is complete when:

- the focused failing group passes;
- `python -m pytest tests\contract tests\unit -q` passes on Windows;
- no skip or xfail is introduced for the nine baseline failures;
- adapter SDK returns descriptor target-root strings without host-platform separator rewriting;
- installer-core keeps its resolved local `Path` target-root behavior and also exposes stable target-root text;
- VGO CLI converts stable target-root text to `Path` without adding a drive prefix to synthetic POSIX env values;
- PowerShell tests mock `choose_powershell(return_diagnostics=True)`;
- installer bridge tests assert optional `host_runtime` diagnostics as CLI boundary output;
- current routing terminology gates still pass with zero blocking debt;
- the working tree is clean after commits.
