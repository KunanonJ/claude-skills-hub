# Immediate Technical Debt Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the immediate, evidence-backed technical debt identified by the approved audit design without changing runtime routing behavior or deploying to any host.

**Architecture:** Treat each debt item as a small repository-local contract fix. The output artifact boundary is fixed by moving tracked runtime outputs into governed fixtures and keeping `outputs/**` untracked; the test baseline audit is fixed by executing classified layer file sets rather than broad directories; the quality-debt overlay gate is fixed by restoring the original policy bytes exactly after gate mutation.

**Tech Stack:** PowerShell 5.1-compatible verify gates, Python 3.10+ audit code, `unittest`/`pytest`, JSON policy files, git-tracked fixture migration.

---

## File Structure

### Output Artifact Boundary

- Modify: `config/outputs-boundary-policy.json`
  - Add fixture roots for migrated runtime-session and skills-audit evidence.
- Modify: `references/fixtures/migration-map.json`
  - Add source-to-fixture mappings for the nine currently tracked output files.
- Move:
  - `outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/cleanup-receipt.json`
  - `outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/governance-capsule.json`
  - `outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/intent-contract.json`
  - `outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/phase-plan-execute.json`
  - `outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/skeleton-receipt.json`
  - `outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/stage-lineage.json`
  - `outputs/skills-audit/bio-science-problem-consolidation.md`
  - `outputs/skills-audit/bio-science-problem-map.csv`
  - `outputs/skills-audit/bio-science-problem-map.json`
- To:
  - `references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/`
  - `references/fixtures/skills-audit/bio-science-problem/`

### Test Baseline Layer Execution

- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
  - Add classified layer file selection.
  - Make `run_layer()` execute the selected layer file set when collected nodes are available.
  - Include selected files in `run_result` evidence.
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`
  - Add tests proving fast and heavy runtime-neutral layers produce different run commands.
  - Update the existing run-layer test to match classified-file execution.

### Quality Debt Overlay Gate

- Modify: `scripts/verify/vibe-quality-debt-overlay-gate.ps1`
  - Restore `config/quality-debt-overlay.json` from original bytes, not from decoded text.
- Create: `tests/runtime_neutral/test_quality_debt_overlay_gate.py`
  - Run the gate and assert the policy file bytes and git diff are unchanged afterward.

### Debt Register

- Create: `docs/status/2026-05-03-immediate-technical-debt-register.md`
  - Record fixed P0/P1 items and retained P2/P3 items with evidence commands.

---

### Task 1: Fix Output Artifact Boundary

**Files:**
- Modify: `config/outputs-boundary-policy.json`
- Modify: `references/fixtures/migration-map.json`
- Move: `outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/*`
- Move: `outputs/skills-audit/bio-science-problem-*`
- Test: `scripts/verify/vibe-output-artifact-boundary-gate.ps1`

- [ ] **Step 1: Run the current failing gate**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-output-artifact-boundary-gate.ps1
```

Expected: FAIL with these messages:

```text
[FAIL] [outputs] all tracked outputs are explicitly allowlisted
[FAIL] [outputs] no tracked outputs exist under disallowed generated-output roots
[FAIL] [outputs] tracked output count matches policy registry
```

- [ ] **Step 2: Create fixture directories**

Run:

```powershell
New-Item -ItemType Directory -Force -Path references\fixtures\runtime\vibe-sessions\20260413T131910Z-pr153-rabbit-review-fix | Out-Null
New-Item -ItemType Directory -Force -Path references\fixtures\skills-audit\bio-science-problem | Out-Null
```

Expected: directories exist under `references\fixtures`.

- [ ] **Step 3: Move tracked runtime session outputs into fixtures**

Run:

```powershell
git mv outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/cleanup-receipt.json references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/cleanup-receipt.json
git mv outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/governance-capsule.json references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/governance-capsule.json
git mv outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/intent-contract.json references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/intent-contract.json
git mv outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/phase-plan-execute.json references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/phase-plan-execute.json
git mv outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/skeleton-receipt.json references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/skeleton-receipt.json
git mv outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/stage-lineage.json references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/stage-lineage.json
```

Expected: `git status --short` shows six rename entries from `outputs/runtime/...` to `references/fixtures/runtime/...`.

- [ ] **Step 4: Move tracked skills-audit outputs into fixtures**

Run:

```powershell
git mv outputs/skills-audit/bio-science-problem-consolidation.md references/fixtures/skills-audit/bio-science-problem/bio-science-problem-consolidation.md
git mv outputs/skills-audit/bio-science-problem-map.csv references/fixtures/skills-audit/bio-science-problem/bio-science-problem-map.csv
git mv outputs/skills-audit/bio-science-problem-map.json references/fixtures/skills-audit/bio-science-problem/bio-science-problem-map.json
```

Expected: `git status --short` shows three rename entries from `outputs/skills-audit/...` to `references/fixtures/skills-audit/...`.

- [ ] **Step 5: Update fixture roots policy**

Edit `config/outputs-boundary-policy.json` so `fixture_roots` is:

```json
  "fixture_roots": [
    "references/fixtures/external-corpus/",
    "references/fixtures/retro-compare/",
    "references/fixtures/verify/routing-stability/",
    "references/fixtures/runtime/",
    "references/fixtures/skills-audit/"
  ]
```

Do not change these strict settings:

```json
  "expected_tracked_output_count": 0,
  "strict_requires_zero_tracked_outputs": true
```

- [ ] **Step 6: Add migration map entries**

Append these mappings to the `mappings` array in `references/fixtures/migration-map.json`:

```json
    {
      "source": "outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/cleanup-receipt.json",
      "destination": "references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/cleanup-receipt.json",
      "stage2_mirrored": true,
      "classification": "runtime_session_fixture"
    },
    {
      "source": "outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/governance-capsule.json",
      "destination": "references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/governance-capsule.json",
      "stage2_mirrored": true,
      "classification": "runtime_session_fixture"
    },
    {
      "source": "outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/intent-contract.json",
      "destination": "references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/intent-contract.json",
      "stage2_mirrored": true,
      "classification": "runtime_session_fixture"
    },
    {
      "source": "outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/phase-plan-execute.json",
      "destination": "references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/phase-plan-execute.json",
      "stage2_mirrored": true,
      "classification": "runtime_session_fixture"
    },
    {
      "source": "outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/skeleton-receipt.json",
      "destination": "references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/skeleton-receipt.json",
      "stage2_mirrored": true,
      "classification": "runtime_session_fixture"
    },
    {
      "source": "outputs/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/stage-lineage.json",
      "destination": "references/fixtures/runtime/vibe-sessions/20260413T131910Z-pr153-rabbit-review-fix/stage-lineage.json",
      "stage2_mirrored": true,
      "classification": "runtime_session_fixture"
    },
    {
      "source": "outputs/skills-audit/bio-science-problem-consolidation.md",
      "destination": "references/fixtures/skills-audit/bio-science-problem/bio-science-problem-consolidation.md",
      "stage2_mirrored": true,
      "classification": "skills_audit_fixture"
    },
    {
      "source": "outputs/skills-audit/bio-science-problem-map.csv",
      "destination": "references/fixtures/skills-audit/bio-science-problem/bio-science-problem-map.csv",
      "stage2_mirrored": true,
      "classification": "skills_audit_fixture"
    },
    {
      "source": "outputs/skills-audit/bio-science-problem-map.json",
      "destination": "references/fixtures/skills-audit/bio-science-problem/bio-science-problem-map.json",
      "stage2_mirrored": true,
      "classification": "skills_audit_fixture"
    }
```

Expected: `python -m json.tool references\fixtures\migration-map.json` exits with code 0.

- [ ] **Step 7: Verify no outputs are tracked**

Run:

```powershell
git ls-files outputs
```

Expected: no output.

- [ ] **Step 8: Verify output artifact boundary passes**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-output-artifact-boundary-gate.ps1
```

Expected: PASS, including:

```text
Tracked outputs : 0
[PASS] [outputs] tracked output count matches policy registry
```

- [ ] **Step 9: Commit output boundary fix**

Run:

```powershell
git status --short
git add config/outputs-boundary-policy.json references/fixtures/migration-map.json references/fixtures/runtime references/fixtures/skills-audit outputs
git commit -m "fix: migrate tracked outputs into fixtures"
```

Expected: commit succeeds and includes the nine renames plus two policy/fixture-map edits.

---

### Task 2: Make Test Baseline Layer Execution Use Classified Files

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`
- Test: `tests/runtime_neutral/test_test_baseline_audit.py`

- [ ] **Step 1: Add failing tests for classified run commands**

In `tests/runtime_neutral/test_test_baseline_audit.py`, update `FakeRunner.__call__` so collect output includes one unit node, one fast runtime-neutral node, and one heavy runtime-neutral node:

```python
        stdout = "\n".join(
            [
                "tests/unit/test_vgo_verify_repo.py::test_repo_root",
                "tests/runtime_neutral/test_runtime_contracts.py::test_contract_shape",
                "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile",
                "3 tests collected",
            ]
        )
```

Add these tests to `TestBaselineAuditPolicyTests`:

```python
    def test_select_layer_files_separates_fast_and_heavy_runtime_neutral_files(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        nodes = [
            "tests/runtime_neutral/test_runtime_contracts.py::test_contract_shape",
            "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile",
        ]

        fast_files = audit.select_layer_files(nodes, REPO_ROOT, policy, "runtime_neutral_fast")
        heavy_files = audit.select_layer_files(nodes, REPO_ROOT, policy, "runtime_neutral_heavy")

        self.assertEqual(["tests/runtime_neutral/test_runtime_contracts.py"], fast_files)
        self.assertEqual(["tests/runtime_neutral/test_install_profile_differentiation.py"], heavy_files)

    def test_build_run_layer_command_uses_classified_files_when_nodes_are_available(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        nodes = [
            "tests/runtime_neutral/test_runtime_contracts.py::test_contract_shape",
            "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile",
        ]

        command = audit.build_run_layer_command(
            policy,
            "runtime_neutral_fast",
            repo_root=REPO_ROOT,
            collected_nodes=nodes,
        )

        self.assertIn("tests/runtime_neutral/test_runtime_contracts.py", command)
        self.assertNotIn("tests/runtime_neutral/test_install_profile_differentiation.py", command)
        self.assertNotIn("tests/runtime_neutral", command)
```

Add this test to `TestBaselineAuditCliTests`:

```python
    def test_run_layer_uses_classified_files_for_requested_layer(self) -> None:
        runner = FakeRunner()
        exit_code = audit.main(["--run-layer", "runtime_neutral_fast"], runner=runner)

        self.assertEqual(0, exit_code)
        run_calls = [call for call in runner.calls if "--collect-only" not in call["command"]]
        self.assertEqual(1, len(run_calls))
        command = run_calls[0]["command"]
        self.assertIn("tests/runtime_neutral/test_runtime_contracts.py", command)
        self.assertNotIn("tests/runtime_neutral/test_install_profile_differentiation.py", command)
        self.assertNotIn("tests/runtime_neutral", command)
```

Update `test_run_layer_sets_disable_network_env` expected command to classified-file execution:

```python
        self.assertEqual(
            [sys.executable, "-m", "pytest", "tests/unit/test_vgo_verify_repo.py", "-q"],
            run_calls[0]["command"],
        )
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected: FAIL because `select_layer_files` does not exist and `build_run_layer_command()` does not accept `repo_root` or `collected_nodes`.

- [ ] **Step 3: Add classified file selection**

In `packages/verification-core/src/vgo_verify/test_baseline_audit.py`, add this function after `classify_node()`:

```python
def select_layer_files(
    collected_nodes: list[str],
    repo_root: Path,
    policy: dict[str, Any],
    layer_id: str,
) -> list[str]:
    layers = layer_by_id(policy)
    if layer_id not in layers:
        raise PolicyError(f"Unknown layer id: {layer_id}")

    files: set[str] = set()
    for node in collected_nodes:
        item = classify_node(node, repo_root, policy)
        if str(item["layer_id"]) == layer_id:
            files.add(str(item["file"]))
    return sorted(files)
```

- [ ] **Step 4: Update `build_run_layer_command()`**

Replace the existing `build_run_layer_command()` with:

```python
def build_run_layer_command(
    policy: dict[str, Any],
    layer_id: str,
    *,
    repo_root: Path | None = None,
    collected_nodes: list[str] | None = None,
) -> list[str]:
    layers = layer_by_id(policy)
    if layer_id not in layers:
        raise PolicyError(f"Unknown layer id: {layer_id}")
    quiet = str((policy.get("defaults") or {}).get("pytest_quiet_arg") or "-q")

    pytest_args = list(layers[layer_id]["pytest_args"])
    if collected_nodes is not None:
        if repo_root is None:
            raise PolicyError("repo_root is required when collected_nodes are provided")
        selected_files = select_layer_files(collected_nodes, repo_root, policy, layer_id)
        if not selected_files:
            raise PolicyError(f"No collected tests matched layer id: {layer_id}")
        pytest_args = selected_files

    return build_pytest_command(pytest_args, quiet=quiet)
```

- [ ] **Step 5: Update `run_layer()` and `main()`**

Replace `run_layer()` with:

```python
def run_layer(
    repo_root: Path,
    policy: dict[str, Any],
    layer_id: str,
    *,
    collected_nodes: list[str] | None = None,
    runner=subprocess.run,
) -> dict[str, Any]:
    selected_files: list[str] = []
    if collected_nodes is not None:
        selected_files = select_layer_files(collected_nodes, repo_root, policy, layer_id)
    command = build_run_layer_command(policy, layer_id, repo_root=repo_root, collected_nodes=collected_nodes)
    env = dict(os.environ)
    disable_env = str((policy.get("defaults") or {}).get("disable_network_env") or "VIBESKILLS_TEST_DISABLE_NETWORK")
    env[disable_env] = "1"
    layer = layer_by_id(policy)[layer_id]
    completed = runner(
        command,
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=int(layer.get("timeout_seconds") or 300),
        env=env,
    )
    return {
        "layer_id": layer_id,
        "command": command,
        "exit_code": int(completed.returncode),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "disable_network_env": disable_env,
        "selected_files": selected_files,
        "selected_file_count": len(selected_files),
    }
```

In `main()`, change:

```python
        run_result = run_layer(repo_root, policy, args.run_layer, runner=runner)
```

to:

```python
        run_result = run_layer(repo_root, policy, args.run_layer, collected_nodes=collected_nodes, runner=runner)
```

- [ ] **Step 6: Export `select_layer_files` from the wrapper**

In `scripts/verify/test-baseline-audit.py`, add `select_layer_files` to the import list and `__all__`:

```python
    select_layer_files,
```

- [ ] **Step 7: Run focused baseline audit tests**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected: all tests in `test_test_baseline_audit.py` pass.

- [ ] **Step 8: Run baseline collect command**

Run:

```powershell
python scripts\verify\test-baseline-audit.py --collect-only
```

Expected:

```text
[INFO] total_nodes=1410 layers=4 risks=6
```

- [ ] **Step 9: Run a classified layer smoke command**

Run:

```powershell
python scripts\verify\test-baseline-audit.py --run-layer contract_unit
```

Expected: exit code 0 and output includes:

```text
[INFO] run_layer=contract_unit exit_code=0
```

- [ ] **Step 10: Commit baseline execution fix**

Run:

```powershell
git add packages/verification-core/src/vgo_verify/test_baseline_audit.py scripts/verify/test-baseline-audit.py tests/runtime_neutral/test_test_baseline_audit.py
git commit -m "fix: execute classified test baseline layers"
```

Expected: commit succeeds with one audit implementation change, one wrapper export change, and one test change.

---

### Task 3: Restore Quality Debt Overlay Policy Bytes Exactly

**Files:**
- Modify: `scripts/verify/vibe-quality-debt-overlay-gate.ps1`
- Create: `tests/runtime_neutral/test_quality_debt_overlay_gate.py`
- Test: `tests/runtime_neutral/test_quality_debt_overlay_gate.py`

- [ ] **Step 1: Add failing byte-restoration test**

Create `tests/runtime_neutral/test_quality_debt_overlay_gate.py`:

```python
from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class QualityDebtOverlayGateTests(unittest.TestCase):
    @unittest.skipIf(shutil.which("powershell") is None, "PowerShell executable not available in PATH")
    def test_quality_debt_overlay_gate_restores_policy_bytes(self) -> None:
        policy_path = REPO_ROOT / "config" / "quality-debt-overlay.json"
        script_path = REPO_ROOT / "scripts" / "verify" / "vibe-quality-debt-overlay-gate.ps1"
        original_bytes = policy_path.read_bytes()

        try:
            completed = subprocess.run(
                ["powershell", "-NoLogo", "-NoProfile", "-File", str(script_path)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
                check=False,
            )

            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            self.assertEqual(original_bytes, policy_path.read_bytes())

            diff = subprocess.run(
                ["git", "diff", "--quiet", "--", "config/quality-debt-overlay.json"],
                cwd=REPO_ROOT,
                check=False,
            )
            self.assertEqual(0, diff.returncode)
        finally:
            policy_path.write_bytes(original_bytes)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test and verify it fails**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_quality_debt_overlay_gate.py -q
```

Expected: FAIL with a byte mismatch or git diff return code caused by the gate restoring decoded text rather than original bytes.

- [ ] **Step 3: Store original bytes in the gate**

In `scripts/verify/vibe-quality-debt-overlay-gate.ps1`, replace:

```powershell
$originalRaw = Get-Content -LiteralPath $policyPath -Raw -Encoding UTF8
```

with:

```powershell
$originalBytes = [System.IO.File]::ReadAllBytes($policyPath)
```

- [ ] **Step 4: Restore original bytes in `finally`**

In the `finally` block, replace:

```powershell
    Set-Content -LiteralPath $policyPath -Value $originalRaw -Encoding UTF8
    Write-Host "Restored quality-debt-overlay policy to original content."
```

with:

```powershell
    [System.IO.File]::WriteAllBytes($policyPath, $originalBytes)
    Write-Host "Restored quality-debt-overlay policy to original bytes."
```

- [ ] **Step 5: Run focused quality-debt test**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_quality_debt_overlay_gate.py -q
```

Expected: 1 passed, or skipped only if PowerShell is unavailable.

- [ ] **Step 6: Run the gate and check worktree cleanliness**

Run:

```powershell
git status --short --branch
powershell -NoLogo -NoProfile -File scripts\verify\vibe-quality-debt-overlay-gate.ps1
git diff -- config/quality-debt-overlay.json
git status --short --branch
```

Expected:

```text
Quality debt overlay gate passed.
```

Expected after `git diff -- config/quality-debt-overlay.json`: no output.

- [ ] **Step 7: Commit quality-debt gate fix**

Run:

```powershell
git add scripts/verify/vibe-quality-debt-overlay-gate.ps1 tests/runtime_neutral/test_quality_debt_overlay_gate.py
git commit -m "fix: restore quality debt overlay policy bytes"
```

Expected: commit succeeds with one gate change and one regression test.

---

### Task 4: Add Immediate Technical Debt Register

**Files:**
- Create: `docs/status/2026-05-03-immediate-technical-debt-register.md`
- Test: Markdown placeholder scan

- [ ] **Step 1: Create debt register**

Create `docs/status/2026-05-03-immediate-technical-debt-register.md` with this content:

````markdown
# Immediate Technical Debt Register

Generated: 2026-05-03

Scope: `F:\vibe\Vibe-Skills`

This register records the immediate-fixable debt items from the approved
technical debt audit design. It separates fixed blocking debt from retained
maintainability debt so release and implementation discussions do not mix
unrelated risk classes.

## Fixed In Current Branch

| ID | Severity | Title | Evidence Before Fix | Fix Boundary | Verification After Fix |
| --- | --- | --- | --- | --- | --- |
| TD-001 | P0 | Tracked generated outputs violated the strict output artifact boundary | `vibe-output-artifact-boundary-gate.ps1` reported `Tracked outputs : 9` and failed output allowlist/count assertions | Move the nine tracked `outputs/**` files into `references/fixtures/**`, add fixture roots, and keep `expected_tracked_output_count = 0` | `powershell -NoLogo -NoProfile -File scripts\verify\vibe-output-artifact-boundary-gate.ps1` |
| TD-002 | P1 | Test baseline layer execution used broad pytest directories instead of classified layer files | `test-baseline-audit.py --collect-only` classified fast/heavy layers, while `run_layer()` still built commands from shared `pytest_args` | Select classified files from collected nodes and pass those files to pytest for the requested layer | `python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q` and `python scripts\verify\test-baseline-audit.py --run-layer contract_unit` |
| TD-003 | P1 | Quality debt overlay gate could leave byte-level policy diffs after a successful run | Running `vibe-quality-debt-overlay-gate.ps1` rewrote `config/quality-debt-overlay.json` and could leave a trailing blank-line diff | Restore the original policy bytes in the `finally` block | `python -m pytest tests\runtime_neutral\test_quality_debt_overlay_gate.py -q` and `git diff -- config/quality-debt-overlay.json` |

## Recorded But Not Scheduled

| ID | Severity | Title | Reason Not Scheduled |
| --- | --- | --- | --- |
| TD-004 | P2 | Large runtime and router scripts increase maintenance cost | No current gate failure was traced to these files during this pass; splitting them needs a dedicated design. |
| TD-005 | P2 | Large verification/runtime Python functions increase repair risk | The immediate pass only touches focused audit/gate behavior; function extraction should be planned around a concrete failing contract. |
| TD-006 | P2 | Short wave gate wrappers depend on shared manifest-driven behavior | The wrapper pattern may be valid; evidence discoverability should be audited separately from the current blocking fixes. |
| TD-007 | P3 | Local `main` is ahead of `origin/main` | This is release-sync debt, not a repository code-quality fix. It should be handled by push/release policy after verification. |
| TD-008 | P3 | Historical retired terminology remains in marked historical records | Current routing terminology gates report zero blocking and review debt; historical records are outside this immediate pass. |

## Final Verification Commands

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-output-artifact-boundary-gate.ps1
python -m pytest tests\runtime_neutral\test_test_baseline_audit.py tests\runtime_neutral\test_quality_debt_overlay_gate.py -q
python scripts\verify\test-baseline-audit.py --collect-only
python scripts\verify\test-baseline-audit.py --run-layer contract_unit
powershell -NoLogo -NoProfile -File scripts\verify\vibe-quality-debt-overlay-gate.ps1
git diff -- config/quality-debt-overlay.json
powershell -NoLogo -NoProfile -File scripts\verify\vibe-repo-cleanliness-gate.ps1
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
git status --short --branch
```
````

- [ ] **Step 2: Scan register for placeholders**

Run:

```powershell
rg -n "TB[D]|TO[D]O|FIXM[E]|PLACEHOLD[E]R|\\?\\?\\?" docs\status\2026-05-03-immediate-technical-debt-register.md
```

Expected: no output and exit code 1.

- [ ] **Step 3: Commit debt register**

Run:

```powershell
git add docs/status/2026-05-03-immediate-technical-debt-register.md
git commit -m "docs: record immediate technical debt register"
```

Expected: commit succeeds with the debt register only.

---

### Task 5: Final Verification

**Files:**
- Verify only; no planned file edits.
- Test: gates and focused pytest commands below.

- [ ] **Step 1: Verify output boundary**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-output-artifact-boundary-gate.ps1
```

Expected: exit code 0 and `Tracked outputs : 0`.

- [ ] **Step 2: Verify focused Python tests**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_test_baseline_audit.py tests\runtime_neutral\test_quality_debt_overlay_gate.py -q
```

Expected: all selected tests pass.

- [ ] **Step 3: Verify baseline audit collection**

Run:

```powershell
python scripts\verify\test-baseline-audit.py --collect-only
```

Expected:

```text
[INFO] total_nodes=1410 layers=4 risks=6
```

- [ ] **Step 4: Verify classified layer smoke run**

Run:

```powershell
python scripts\verify\test-baseline-audit.py --run-layer contract_unit
```

Expected: exit code 0 and:

```text
[INFO] run_layer=contract_unit exit_code=0
```

- [ ] **Step 5: Verify quality debt overlay gate leaves no diff**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-quality-debt-overlay-gate.ps1
git diff -- config/quality-debt-overlay.json
```

Expected:

```text
Quality debt overlay gate passed.
```

Expected from `git diff -- config/quality-debt-overlay.json`: no output.

- [ ] **Step 6: Verify cleanliness and routing guardrails**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-repo-cleanliness-gate.ps1
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
git status --short --branch
```

Expected:

```text
Repo zero-dirty          : True
```

Expected routing debt JSON summary:

```text
P0 = 0
P1 = 0
P2 = 0
P3 = 0
```

Expected terminology scan summary:

```text
fail_count = 0
review_count = 0
```

- [ ] **Step 7: Record verification summary for the user**

Do not commit generated `outputs/verify` artifacts. Summarize command results in the final response with:

```text
output boundary: pass
baseline audit tests: pass
baseline collect: pass
baseline contract_unit run: pass
quality debt overlay: pass and no diff
repo cleanliness: pass
routing debt gates: pass
worktree: clean
```
