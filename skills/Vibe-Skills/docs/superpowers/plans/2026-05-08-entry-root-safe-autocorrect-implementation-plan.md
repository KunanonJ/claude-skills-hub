# Entry Root Safe Autocorrect Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent public entry surfaces from misreading user workspaces as `repo_root`, automatically recover when the true Vibe runtime root is obvious, and convert Windows bash/WSL shell failures into PowerShell-first handoffs or clear blocking messages without dangerous file operations.

**Architecture:** Add one thin Python-side runtime-root guard that classifies repo-root evidence and returns either a corrected `repo_root` or a user-facing guard error. Integrate that guard into canonical-entry before deep contract loading, then keep Windows shell frontends thin by handing `check.sh` and `one-shot-setup.sh` to their `.ps1` peers as early as possible instead of trying to make bash equal to the PowerShell lane.

**Tech Stack:** Python 3.10+, existing `vgo_contracts` / `vgo_runtime` packages, Bash and PowerShell wrappers, `pytest`, `unittest`, existing Windows shell compatibility tests.

---

## File Map

- Create: `packages/contracts/src/vgo_contracts/entry_root_guard.py`
  - Shared Python helper for runtime-root evidence, non-destructive auto-correction, and user-facing guard errors.
- Create: `tests/unit/test_entry_root_guard.py`
  - Unit coverage for strong/medium/weak evidence, auto-correction, and ambiguity blocking.
- Create: `tests/integration/test_shell_frontend_windows_handoff_contract.py`
  - Text-level contract coverage that the shell frontends now advertise Windows PowerShell handoff behavior.
- Modify: `packages/runtime-core/src/vgo_runtime/canonical_entry.py`
  - Run the new guard before `resolve_canonical_vibe_contract()`, preserve safe behavior, and surface guard failures without a raw traceback.
- Modify: `tests/unit/test_canonical_vibe_entry_launcher.py`
  - Coverage for canonical-entry auto-correction and human-readable `SystemExit` blocking.
- Modify: `scripts/bootstrap/one-shot-setup.sh`
  - Add early Windows shell detection, PowerShell handoff, and clear blocking when no PowerShell host exists.
- Modify: `check.sh`
  - Same Windows shell detection and handoff strategy as `one-shot-setup.sh`.
- Modify: `tests/runtime_neutral/test_installed_runtime_scripts.py`
  - Runtime-neutral Windows behavioral coverage for installed `check.sh` and `one-shot-setup.sh`.
- Modify: `docs/universalization/platform-support-matrix.md`
  - State that Windows shell frontends are convenience wrappers that should hand off to PowerShell-first when available.
- Modify: `docs/install/installation-rules.md`
  - Clarify that Windows bash frontends are not authoritative and will hand off or block.

## Task 1: Add The Shared Python Entry-Root Guard

**Files:**
- Create: `packages/contracts/src/vgo_contracts/entry_root_guard.py`
- Test: `tests/unit/test_entry_root_guard.py`

- [ ] **Step 1: Write the failing guard tests**

```python
from pathlib import Path

import pytest

from vgo_contracts.entry_root_guard import EntryRootGuardError, resolve_entry_repo_root


def _write_runtime_root(root: Path) -> None:
    (root / "config").mkdir(parents=True, exist_ok=True)
    (root / "apps" / "vgo-cli" / "src" / "vgo_cli").mkdir(parents=True, exist_ok=True)
    (root / "SKILL.md").write_text("---\nname: vibe\n---\n", encoding="utf-8")
    (root / "config" / "version-governance.json").write_text("{}", encoding="utf-8")
    (root / "config" / "adapter-registry.json").write_text('{"adapters": []}', encoding="utf-8")
    (root / "apps" / "vgo-cli" / "src" / "vgo_cli" / "main.py").write_text("def main():\n    return 0\n", encoding="utf-8")


def test_resolve_entry_repo_root_accepts_explicit_runtime_root(tmp_path: Path) -> None:
    runtime_root = tmp_path / "Vibe-Skills"
    _write_runtime_root(runtime_root)

    decision = resolve_entry_repo_root(runtime_root, script_anchor=runtime_root / "packages" / "runtime-core" / "src" / "vgo_runtime" / "canonical_entry.py")

    assert decision.repo_root == runtime_root.resolve()
    assert decision.auto_corrected is False
    assert decision.reason_code == "repo_root_ok"


def test_resolve_entry_repo_root_autocorrects_workspace_like_input(tmp_path: Path) -> None:
    runtime_root = tmp_path / "Vibe-Skills"
    workspace_root = tmp_path / "bj-refinery"
    _write_runtime_root(runtime_root)
    workspace_root.mkdir(parents=True, exist_ok=True)
    (workspace_root / ".git").mkdir()
    (workspace_root / "README.md").write_text("# workspace\n", encoding="utf-8")

    decision = resolve_entry_repo_root(
        workspace_root,
        script_anchor=runtime_root / "packages" / "runtime-core" / "src" / "vgo_runtime" / "canonical_entry.py",
    )

    assert decision.repo_root == runtime_root.resolve()
    assert decision.original_repo_root == workspace_root.resolve()
    assert decision.auto_corrected is True
    assert decision.reason_code == "root_role_mismatch_autocorrected"


def test_resolve_entry_repo_root_blocks_when_candidates_are_ambiguous(tmp_path: Path) -> None:
    first_runtime = tmp_path / "install-a"
    second_runtime = tmp_path / "install-b"
    workspace_root = tmp_path / "bj-refinery"
    _write_runtime_root(first_runtime)
    _write_runtime_root(second_runtime)
    workspace_root.mkdir(parents=True, exist_ok=True)

    with pytest.raises(EntryRootGuardError, match="multiple candidate Vibe runtime roots"):
        resolve_entry_repo_root(
            workspace_root,
            script_anchor=first_runtime / "packages" / "runtime-core" / "src" / "vgo_runtime" / "canonical_entry.py",
            installed_runtime_roots=(first_runtime, second_runtime),
        )
```

- [ ] **Step 2: Run the new tests to verify they fail**

Run: `pytest -q tests/unit/test_entry_root_guard.py`

Expected: FAIL with `ModuleNotFoundError: No module named 'vgo_contracts.entry_root_guard'`

- [ ] **Step 3: Implement the shared guard**

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

RUNTIME_ROOT_REQUIRED_MARKERS = (
    "SKILL.md",
    "config/version-governance.json",
    "config/adapter-registry.json",
    "apps/vgo-cli/src/vgo_cli/main.py",
)


@dataclass(frozen=True, slots=True)
class EntryRootDecision:
    repo_root: Path
    original_repo_root: Path
    working_dir_candidate: Path | None
    reason_code: str
    auto_corrected: bool


class EntryRootGuardError(RuntimeError):
    def __init__(self, code: str, message: str, *, original_repo_root: Path, candidates: tuple[Path, ...] = ()) -> None:
        super().__init__(message)
        self.code = code
        self.original_repo_root = original_repo_root
        self.candidates = candidates


def _normalize_path(value: str | Path | None) -> Path | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return Path(text).resolve()


def _looks_like_runtime_root(path: Path) -> bool:
    return all((path / marker).exists() for marker in RUNTIME_ROOT_REQUIRED_MARKERS)


def _looks_like_workspace_root(path: Path) -> bool:
    if _looks_like_runtime_root(path):
        return False
    if (path / ".git").exists():
        return True
    return any((path / name).exists() for name in ("README.md", "pyproject.toml", "package.json", "src"))


def _script_anchor_runtime_root(script_anchor: Path | None) -> Path | None:
    current = script_anchor.resolve() if script_anchor is not None else None
    while current is not None:
        if current.is_file():
            current = current.parent
            continue
        if _looks_like_runtime_root(current):
            return current
        if current.parent == current:
            return None
        current = current.parent
    return None


def resolve_entry_repo_root(
    repo_root: str | Path,
    *,
    script_anchor: str | Path | None = None,
    installed_runtime_roots: tuple[str | Path, ...] = (),
) -> EntryRootDecision:
    original_repo_root = _normalize_path(repo_root)
    if original_repo_root is None:
        raise EntryRootGuardError(
            "root_role_mismatch",
            "repo_root was empty; pass the real Vibe runtime root instead of a workspace path.",
            original_repo_root=Path.cwd(),
        )

    if _looks_like_runtime_root(original_repo_root):
        return EntryRootDecision(
            repo_root=original_repo_root,
            original_repo_root=original_repo_root,
            working_dir_candidate=None,
            reason_code="repo_root_ok",
            auto_corrected=False,
        )

    candidates: list[Path] = []
    anchor_candidate = _script_anchor_runtime_root(_normalize_path(script_anchor))
    if anchor_candidate is not None:
        candidates.append(anchor_candidate)
    for value in installed_runtime_roots:
        candidate = _normalize_path(value)
        if candidate is not None and _looks_like_runtime_root(candidate) and candidate not in candidates:
            candidates.append(candidate)

    if len(candidates) == 1 and _looks_like_workspace_root(original_repo_root):
        return EntryRootDecision(
            repo_root=candidates[0],
            original_repo_root=original_repo_root,
            working_dir_candidate=original_repo_root,
            reason_code="root_role_mismatch_autocorrected",
            auto_corrected=True,
        )

    if len(candidates) > 1:
        raise EntryRootGuardError(
            "ambiguous_runtime_root",
            "Detected multiple candidate Vibe runtime roots; refusing to guess.",
            original_repo_root=original_repo_root,
            candidates=tuple(candidates),
        )

    raise EntryRootGuardError(
        "runtime_incomplete",
        "The provided repo_root does not look like a Vibe runtime root, and no trusted runtime root could be recovered.",
        original_repo_root=original_repo_root,
    )
```

- [ ] **Step 4: Run the guard tests to verify they pass**

Run: `pytest -q tests/unit/test_entry_root_guard.py`

Expected: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add packages/contracts/src/vgo_contracts/entry_root_guard.py tests/unit/test_entry_root_guard.py
git commit -m "feat: add shared entry root guard"
```

### Task 2: Integrate The Guard Into Canonical Entry

**Files:**
- Modify: `packages/runtime-core/src/vgo_runtime/canonical_entry.py`
- Test: `tests/unit/test_canonical_vibe_entry_launcher.py`

- [ ] **Step 1: Write the failing canonical-entry integration tests**

```python
from pathlib import Path

import pytest

from vgo_contracts.entry_root_guard import EntryRootDecision, EntryRootGuardError
from vgo_runtime import canonical_entry


def test_launch_canonical_vibe_uses_corrected_repo_root(monkeypatch, tmp_path: Path) -> None:
    corrected_root = tmp_path / "Vibe-Skills"
    session_root = tmp_path / "artifacts" / "outputs" / "runtime" / "vibe-sessions" / "run-1"
    decision = EntryRootDecision(
        repo_root=corrected_root,
        original_repo_root=tmp_path / "bj-refinery",
        working_dir_candidate=tmp_path / "bj-refinery",
        reason_code="root_role_mismatch_autocorrected",
        auto_corrected=True,
    )

    monkeypatch.setattr(canonical_entry, "resolve_entry_repo_root", lambda *args, **kwargs: decision)
    monkeypatch.setattr(canonical_entry, "_resolve_effective_prompt", lambda **kwargs: "safe prompt")
    monkeypatch.setattr(canonical_entry, "_resolve_progressive_requested_stage_stop", lambda **kwargs: None)
    monkeypatch.setattr(canonical_entry, "_validate_bounded_reentry", lambda **kwargs: None)
    monkeypatch.setattr(canonical_entry, "_inherit_frozen_host_decision_fields_from_bounded_reentry", lambda **kwargs: None)
    monkeypatch.setattr(canonical_entry, "_attach_bounded_continuation_context_to_host_decision", lambda **kwargs: None)
    monkeypatch.setattr(canonical_entry, "resolve_canonical_vibe_contract", lambda repo_root, host_id: {"fallback_policy": "blocked", "allow_skill_doc_fallback": False} if repo_root == corrected_root else (_ for _ in ()).throw(AssertionError(repo_root)))
    monkeypatch.setattr(canonical_entry, "write_host_launch_receipt", lambda *args, **kwargs: session_root / "host-launch-receipt.json")
    monkeypatch.setattr(
        canonical_entry,
        "invoke_vibe_runtime_entrypoint",
        lambda **kwargs: {
            "run_id": "run-1",
            "session_root": str(session_root),
            "summary_path": str(session_root / "runtime-summary.json"),
            "summary": {},
        },
    )
    monkeypatch.setattr(canonical_entry, "assert_minimum_truth_artifacts", lambda session_root: {
        "runtime_input_packet": str(Path(session_root) / "runtime-input-packet.json"),
        "governance_capsule": str(Path(session_root) / "governance-capsule.json"),
        "stage_lineage": str(Path(session_root) / "stage-lineage.json"),
    })
    monkeypatch.setattr(canonical_entry, "assert_minimum_truth_consistency", lambda **kwargs: None)
    monkeypatch.setattr(canonical_entry, "_load_json_dict", lambda *args, **kwargs: {})

    result = canonical_entry.launch_canonical_vibe(
        repo_root=tmp_path / "bj-refinery",
        host_id="codex",
        entry_id="vibe",
        prompt="repair route",
        artifact_root=tmp_path / "artifacts",
    )

    assert result.run_id == "run-1"


def test_canonical_entry_main_surfaces_guard_error_without_traceback(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        canonical_entry,
        "launch_canonical_vibe",
        lambda **kwargs: (_ for _ in ()).throw(
            EntryRootGuardError(
                "runtime_incomplete",
                "The provided repo_root does not look like a Vibe runtime root, and no trusted runtime root could be recovered.",
                original_repo_root=tmp_path / "bj-refinery",
            )
        ),
    )

    with pytest.raises(SystemExit, match="does not look like a Vibe runtime root"):
        canonical_entry.main(
            [
                "--repo-root",
                str(tmp_path / "bj-refinery"),
                "--host-id",
                "codex",
                "--entry-id",
                "vibe",
                "--prompt",
                "repair route",
            ]
        )
```

- [ ] **Step 2: Run the canonical-entry tests to verify they fail**

Run: `pytest -q tests/unit/test_canonical_vibe_entry_launcher.py -k "uses_corrected_repo_root or surfaces_guard_error_without_traceback"`

Expected: FAIL because `canonical_entry.py` does not yet import `resolve_entry_repo_root` or catch `EntryRootGuardError`

- [ ] **Step 3: Integrate the guard and suppress raw tracebacks**

```python
from vgo_contracts.entry_root_guard import EntryRootDecision, EntryRootGuardError, resolve_entry_repo_root


@dataclass(slots=True)
class CanonicalLaunchResult:
    run_id: str
    session_root: Path
    summary_path: Path
    host_launch_receipt_path: Path
    launch_mode: str
    summary: dict[str, Any]
    artifacts: dict[str, str]
    notices: list[str]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["session_root"] = str(self.session_root)
        payload["summary_path"] = str(self.summary_path)
        payload["host_launch_receipt_path"] = str(self.host_launch_receipt_path)
        payload["artifacts"] = dict(self.artifacts)
        payload["notices"] = list(self.notices)
        return payload


def launch_canonical_vibe(
    *,
    repo_root: str | Path,
    host_id: str,
    entry_id: str,
    prompt: str,
    requested_stage_stop: str | None = None,
    requested_grade_floor: str | None = None,
    run_id: str | None = None,
    artifact_root: str | Path | None = None,
    continue_from_run_id: str | None = None,
    bounded_reentry_token: str | None = None,
    host_decision: dict[str, Any] | None = None,
    force_runtime_neutral: bool = False,
) -> CanonicalLaunchResult:
    decision = resolve_entry_repo_root(repo_root, script_anchor=Path(__file__))
    repo_root_path = decision.repo_root
    notices: list[str] = []
    if decision.auto_corrected:
        notices.append(
            "The provided repo_root looked like a workspace path. Canonical entry auto-corrected it to the trusted Vibe runtime root."
        )

    requested_entry_id = _normalize_requested_entry_id(entry_id)
    resolved_artifact_root = _resolve_artifact_root(repo_root_path, artifact_root)
    normalized_host_decision = _normalize_host_decision(host_decision)
    validated_reentry = _validate_bounded_reentry(
        artifact_root=resolved_artifact_root,
        entry_id=requested_entry_id,
        prompt=prompt,
        run_id=run_id,
        continue_from_run_id=continue_from_run_id,
        bounded_reentry_token=bounded_reentry_token,
        host_decision=normalized_host_decision,
    )
    effective_host_decision = _inherit_frozen_host_decision_fields_from_bounded_reentry(
        host_decision=normalized_host_decision,
        bounded_reentry=validated_reentry,
    )
    effective_host_decision = _attach_bounded_continuation_context_to_host_decision(
        host_decision=effective_host_decision,
        bounded_reentry=validated_reentry,
        prompt_text=prompt,
    )
    effective_requested_stage_stop = _resolve_progressive_requested_stage_stop(
        repo_root=repo_root_path,
        entry_id=requested_entry_id,
        requested_stage_stop=requested_stage_stop,
        bounded_reentry=validated_reentry,
    )
    effective_prompt = _resolve_effective_prompt(
        host_id=host_id,
        entry_id=requested_entry_id,
        prompt=prompt,
        host_decision=effective_host_decision,
        artifact_root=resolved_artifact_root,
        run_id=run_id,
        bounded_reentry=validated_reentry,
        continuation_source_run_id=(str(validated_reentry["source_run_id"]) if validated_reentry else None),
        allow_bounded_preferred_source=bool(validated_reentry),
    )
    contract = resolve_canonical_vibe_contract(repo_root_path, host_id)
    if str(contract.get("fallback_policy") or "").strip() != "blocked":
        raise RuntimeError("unsupported fallback policy for canonical entry launcher")
    if bool(contract.get("allow_skill_doc_fallback", False)):
        raise RuntimeError("unsupported fallback policy for canonical entry launcher")
    resolved_run_id = str(run_id or "").strip() or _new_run_id()
    session_root = _resolve_session_root(repo_root=repo_root_path, run_id=resolved_run_id, artifact_root=artifact_root)
    summary_path = (session_root / "runtime-summary.json").resolve()
    # existing receipt / runtime invocation logic stays unchanged
    return CanonicalLaunchResult(
        run_id=resolved_run_id,
        session_root=session_root,
        summary_path=summary_path,
        host_launch_receipt_path=receipt_path,
        launch_mode=verified_receipt.launch_mode,
        summary=summary,
        artifacts=artifacts,
        notices=notices,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Launch canonical vibe entry and emit receipt-backed JSON output.")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--host-id", default="codex")
    parser.add_argument("--entry-id", default="vibe")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--requested-stage-stop")
    parser.add_argument("--requested-grade-floor", choices=("L", "XL"))
    parser.add_argument("--run-id")
    parser.add_argument("--artifact-root")
    parser.add_argument("--continue-from-run-id")
    parser.add_argument("--bounded-reentry-token")
    parser.add_argument("--host-decision-json")
    parser.add_argument("--host-decision-json-file")
    parser.add_argument("--force-runtime-neutral", action="store_true")
    args = parser.parse_args(argv)
    host_decision = _parse_host_decision_json(args.host_decision_json, args.host_decision_json_file)

    try:
        result = launch_canonical_vibe(
            repo_root=args.repo_root,
            host_id=args.host_id,
            entry_id=args.entry_id,
            prompt=args.prompt,
            requested_stage_stop=args.requested_stage_stop,
            requested_grade_floor=args.requested_grade_floor,
            run_id=args.run_id,
            artifact_root=args.artifact_root,
            continue_from_run_id=args.continue_from_run_id,
            bounded_reentry_token=args.bounded_reentry_token,
            host_decision=host_decision,
            force_runtime_neutral=bool(args.force_runtime_neutral),
        )
    except EntryRootGuardError as exc:
        raise SystemExit(str(exc))

    for notice in result.notices:
        print(f"[INFO] {notice}", file=sys.stderr)
    json.dump(result.to_dict(), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0
```

- [ ] **Step 4: Run the canonical-entry tests to verify they pass**

Run: `pytest -q tests/unit/test_canonical_vibe_entry_launcher.py -k "uses_corrected_repo_root or surfaces_guard_error_without_traceback"`

Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add packages/runtime-core/src/vgo_runtime/canonical_entry.py tests/unit/test_canonical_vibe_entry_launcher.py
git commit -m "fix: guard canonical entry repo root resolution"
```

### Task 3: Hand Off Windows Shell Frontends To PowerShell Early

**Files:**
- Modify: `scripts/bootstrap/one-shot-setup.sh`
- Modify: `check.sh`
- Create: `tests/integration/test_shell_frontend_windows_handoff_contract.py`
- Test: `tests/runtime_neutral/test_installed_runtime_scripts.py`

- [ ] **Step 1: Write the failing shell-handoff tests**

```python
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_shell_frontends_advertise_windows_powershell_handoff() -> None:
    bootstrap_shell = (REPO_ROOT / "scripts" / "bootstrap" / "one-shot-setup.sh").read_text(encoding="utf-8")
    check_shell = (REPO_ROOT / "check.sh").read_text(encoding="utf-8")

    assert "Windows shell frontend detected; switching to PowerShell-first supported path." in bootstrap_shell
    assert "one-shot-setup.ps1" in bootstrap_shell
    assert "Windows shell frontend detected; switching to PowerShell-first supported path." in check_shell
    assert "check.ps1" in check_shell
```

```python
def test_installed_check_sh_hands_off_to_powershell_first_on_windows(self) -> None:
    if os.name != "nt":
        self.skipTest("Windows-only shell handoff behavior")
    powershell = resolve_powershell()
    if powershell is None:
        self.skipTest("requires PowerShell host")

    self.install_shell_runtime(profile="full")
    installed_root = self.target_root / "skills" / "vibe"
    result = subprocess.run(
        [
            "bash",
            str(installed_root / "check.sh"),
            "--host",
            "codex",
            "--profile",
            "full",
            "--target-root",
            str(self.target_root),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    combined = (result.stdout or "") + (result.stderr or "")
    self.assertIn("switching to PowerShell-first supported path", combined)
    self.assertNotIn("command not found", combined)
```

- [ ] **Step 2: Run the shell-handoff tests to verify they fail**

Run: `pytest -q tests/integration/test_shell_frontend_windows_handoff_contract.py tests/runtime_neutral/test_installed_runtime_scripts.py -k "powershell_handoff or shell_frontends_advertise_windows_powershell_handoff"`

Expected: FAIL because the shell frontends do not yet contain the handoff notice or early `.ps1` handoff path

- [ ] **Step 3: Add early Windows shell handoff and clear blocking**

```bash
is_windows_shell_host() {
  case "$(uname -s 2>/dev/null || printf '')" in
    CYGWIN*|MINGW*|MSYS*) return 0 ;;
  esac
  [[ -n "${WINDIR:-}" || -n "${SYSTEMROOT:-}" ]]
}

handoff_to_windows_powershell_frontend() {
  local script_path="$1"
  shift
  if ! is_windows_shell_host; then
    return 1
  fi
  local shell_path=""
  shell_path="$(pick_powershell || true)"
  if [[ -z "${shell_path}" ]]; then
    echo "[FAIL] Windows shell frontend detected, but no pwsh/powershell executable was found." >&2
    echo "[FAIL] Re-run the matching .ps1 entrypoint from PowerShell, or install PowerShell 7." >&2
    exit 1
  fi
  echo "[INFO] Windows shell frontend detected; switching to PowerShell-first supported path." >&2
  run_powershell_file "${script_path}" "$@"
  exit $?
}
```

```bash
# one-shot-setup.sh: after argument parsing, before repository metadata work
ps_args=(-Profile "${PROFILE}" -HostId "${HOST_ID}")
if [[ -n "${TARGET_ROOT}" ]]; then
  ps_args+=(-TargetRoot "${TARGET_ROOT}")
fi
if [[ "${SKIP_EXTERNAL_INSTALL}" == "true" ]]; then
  ps_args+=(-SkipExternalInstall)
fi
if [[ "${STRICT_OFFLINE}" == "true" ]]; then
  ps_args+=(-StrictOffline)
fi
handoff_to_windows_powershell_frontend "${REPO_ROOT}/scripts/bootstrap/one-shot-setup.ps1" "${ps_args[@]}"
```

```bash
# check.sh: after argument parsing, before adapter or doctor work
ps_args=(-Profile "${PROFILE}" -HostId "${HOST_ID}")
if [[ -n "${TARGET_ROOT}" ]]; then
  ps_args+=(-TargetRoot "${TARGET_ROOT}")
fi
if [[ "${SKIP_RUNTIME_FRESHNESS_GATE}" == "true" ]]; then
  ps_args+=(-SkipRuntimeFreshnessGate)
fi
if [[ "${DEEP}" == "true" ]]; then
  ps_args+=(-Deep)
fi
handoff_to_windows_powershell_frontend "${SCRIPT_DIR}/check.ps1" "${ps_args[@]}"
```

- [ ] **Step 4: Run the shell-handoff tests to verify they pass**

Run: `pytest -q tests/integration/test_shell_frontend_windows_handoff_contract.py tests/runtime_neutral/test_installed_runtime_scripts.py -k "powershell_handoff or shell_frontends_advertise_windows_powershell_handoff"`

Expected: text-contract tests PASS everywhere; Windows behavioral test PASS on Windows and SKIP elsewhere

- [ ] **Step 5: Commit**

```bash
git add scripts/bootstrap/one-shot-setup.sh check.sh tests/integration/test_shell_frontend_windows_handoff_contract.py tests/runtime_neutral/test_installed_runtime_scripts.py
git commit -m "fix: hand off Windows shell frontends to PowerShell"
```

### Task 4: Sync Public Docs And Run The Targeted Regression Matrix

**Files:**
- Modify: `docs/universalization/platform-support-matrix.md`
- Modify: `docs/install/installation-rules.md`

- [ ] **Step 1: Add the failing documentation expectations**

```python
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_windows_support_matrix_mentions_powershell_first_shell_handoff() -> None:
    content = (REPO_ROOT / "docs" / "universalization" / "platform-support-matrix.md").read_text(encoding="utf-8")
    assert "Windows shell frontends should hand off to PowerShell-first when a PowerShell host is available." in content


def test_installation_rules_explain_windows_shell_blocking_behavior() -> None:
    content = (REPO_ROOT / "docs" / "install" / "installation-rules.md").read_text(encoding="utf-8")
    assert "Windows bash frontends are convenience wrappers, not the authoritative lane." in content
```

- [ ] **Step 2: Run the documentation expectations to verify they fail**

Run: `pytest -q tests/integration/test_shell_frontend_windows_handoff_contract.py -k "support_matrix or installation_rules"`

Expected: FAIL because the new Windows handoff guidance is not in the docs yet

- [ ] **Step 3: Update the docs**

```markdown
| Windows | `install.ps1`, `one-shot-setup.ps1` | `check.ps1` | strongest current path for PowerShell-first gates | `full-authoritative` | this is the current reference closure lane; Windows shell frontends should hand off to PowerShell-first when a PowerShell host is available |
```

```markdown
- Windows bash frontends are convenience wrappers, not the authoritative lane.
- On Windows, `one-shot-setup.sh` and `check.sh` should hand off to the matching `.ps1` entrypoint when a PowerShell host is available.
- If neither `pwsh` nor `powershell.exe` is available, block with a clear re-run instruction instead of surfacing raw `127` or traceback output.
```

- [ ] **Step 4: Run the targeted regression matrix**

Run: `pytest -q tests/unit/test_entry_root_guard.py tests/unit/test_canonical_vibe_entry_launcher.py -k "entry_root or corrected_repo_root or guard_error" && pytest -q tests/integration/test_shell_frontend_windows_handoff_contract.py && pytest -q tests/runtime_neutral/test_installed_runtime_scripts.py -k "installed_shell_scripts_work_without_repo_level_adapter_registry or powershell_handoff" && git diff --check`

Expected:
- unit guard tests PASS
- canonical-entry launcher tests PASS
- shell handoff contract tests PASS
- installed runtime shell regression tests PASS or Windows-only tests SKIP when not applicable
- `git diff --check` returns clean

- [ ] **Step 5: Commit**

```bash
git add docs/universalization/platform-support-matrix.md docs/install/installation-rules.md
git commit -m "docs: document Windows PowerShell-first shell handoff"
```

## Self-Review

### Spec coverage

- Strong/medium/weak evidence and no-danger auto-correction are covered by Task 1.
- Canonical-entry pre-contract correction and no-traceback blocking are covered by Task 2.
- Windows bash/WSL shell handoff and human-readable failure behavior are covered by Task 3.
- Public PowerShell-first guidance and verification matrix are covered by Task 4.

### Placeholder scan

- No `TBD`, `TODO`, or “implement later” placeholders remain.
- Every code-changing step includes exact file content or exact code blocks.
- Every validation step has an exact command and expected result.

### Type consistency

- Shared guard types remain `EntryRootDecision` and `EntryRootGuardError` across all tasks.
- The canonical-entry integration consistently uses `resolve_entry_repo_root(...)`.
- The shell handoff message string is consistent across shell code, tests, and docs.
