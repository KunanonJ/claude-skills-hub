# Test Merge-Blocker Debt Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the current test and cleanliness blockers by hardening Bash entrypoint compatibility, Windows Bash path normalization, and local `.vibeskills/` noise policy.

**Architecture:** Keep the fix at the existing test-support and policy boundaries. `check.sh` drops Bash 4-only `mapfile` usage without changing runtime checks, `tests/bash_test_support.py` preserves explicit caller path intent before invoking Bash, and repo-cleanliness policy plus `.gitignore` classify `.vibeskills/` as local operator state.

**Tech Stack:** Bash 3-compatible shell, Python 3, pytest runtime-neutral tests, PowerShell cleanliness gate, JSON policy, Git.

---

## File Structure

**Shell entrypoint compatibility**

- Modify: `check.sh`
  - Replace the two Bash 4-only `mapfile` reads with Bash 3-compatible `while IFS= read -r ...` loops.
- Existing test: `tests/runtime_neutral/test_shell_entrypoint_compatibility.py`
  - Already owns the no-`mapfile` contract for `install.sh`, `check.sh`, and `scripts/bootstrap/one-shot-setup.sh`.

**Windows Bash path normalization**

- Modify: `tests/runtime_neutral/test_bash_test_support.py`
  - Add a regression proving explicit trailing `/` and `\` are preserved when Windows absolute path arguments are normalized for Bash.
- Modify: `tests/bash_test_support.py`
  - Add a small helper that records the original argument text, delegates to the current `to_bash_path(Path(...))`, then restores a trailing `/` if the caller supplied a trailing separator.
- Existing test: `tests/runtime_neutral/test_windows_setup_helpers.py`
  - Verifies `fetch-windows11-eval-iso.sh --output downloads/` rejects before network work.

**Local runtime noise policy**

- Create: `tests/runtime_neutral/test_repo_cleanliness_policy.py`
  - Verifies `.vibeskills/` is both ignored by Git and listed in repo-cleanliness local-noise policy.
- Modify: `.gitignore`
  - Ignore `.vibeskills/` under local operator noise.
- Modify: `config/repo-cleanliness-policy.json`
  - Add `.vibeskills/` to shared ignore metadata and local-noise classification.

**Do not modify**

- Runtime/router routing semantics.
- Host roots such as `C:\Users\羽裳\.codex`.
- Windows VM or ISO download scripts, except through existing tests proving pre-network behavior.
- Old terminology cleanup files or routing terminology policy in this pass.
- Broad file structure, packaging manifests, or install/deploy scripts outside the listed files.

---

## Current Baseline

Fresh focused command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_shell_entrypoint_compatibility.py -q
```

Observed result before this plan:

```text
1 failed, 4 passed
```

The failure is:

```text
ShellEntrypointCompatibilityTests.test_install_entrypoints_avoid_mapfile
```

Known offending lines:

```text
check.sh:604: mapfile -t allowlist <<<"${allowlist_output}"
check.sh:635: mapfile -t PROJECTED_SKILL_NAMES <<<"${output}"
```

Current path-normalization probe:

```powershell
@'
from tests.bash_test_support import normalize_bash_command_args
cmd = ["bash", r"F:\vibe\Vibe-Skills\scripts\setup\fetch-windows11-eval-iso.sh", "--output", r"C:\Users\tester\AppData\Local\Temp\case\downloads/"]
print(normalize_bash_command_args(cmd))
'@ | python -
```

Observed output before this plan:

```python
['D:\\tool\\Git\\usr\\bin\\bash.exe', '/f/vibe/Vibe-Skills/scripts/setup/fetch-windows11-eval-iso.sh', '--output', '/c/Users/tester/AppData/Local/Temp/case/downloads']
```

The final `downloads/` separator is lost.

Current cleanliness gate:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-repo-cleanliness-gate.ps1
```

Observed result before this plan:

```text
Dirty paths: 1
[FAIL] [cleanliness] no uncategorized dirty paths remain visible
```

Current `git status --short --branch` before implementation:

```text
## main...origin/main [ahead 38]
?? .vibeskills/
```

---

### Task 1: Remove Bash `mapfile` From `check.sh`

**Files:**

- Modify: `check.sh`
- Existing test: `tests/runtime_neutral/test_shell_entrypoint_compatibility.py`

- [ ] **Step 1: Run the existing red compatibility guard**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_shell_entrypoint_compatibility.py -q
```

Expected: FAIL with `AssertionError: 'mapfile' unexpectedly found ... : check.sh`.

- [ ] **Step 2: Replace the allowlist `mapfile` read**

In `check.sh`, inside `projected_skill_names_for_check()`, replace:

```bash
    if [[ -n "${allowlist_output}" ]]; then
      mapfile -t allowlist <<<"${allowlist_output}"
    fi
```

with:

```bash
    if [[ -n "${allowlist_output}" ]]; then
      local allowlist_entry=""
      while IFS= read -r allowlist_entry; do
        allowlist+=("${allowlist_entry}")
      done <<<"${allowlist_output}"
    fi
```

- [ ] **Step 3: Replace the projected skill names `mapfile` read**

In `check.sh`, inside `load_projected_skill_names_for_check()`, replace:

```bash
  mapfile -t PROJECTED_SKILL_NAMES <<<"${output}"
  if [[ ${#PROJECTED_SKILL_NAMES[@]} -eq 1 && -z "${PROJECTED_SKILL_NAMES[0]}" ]]; then
    PROJECTED_SKILL_NAMES=()
  fi
```

with:

```bash
  PROJECTED_SKILL_NAMES=()
  if [[ -n "${output}" ]]; then
    local projected_skill_name=""
    while IFS= read -r projected_skill_name; do
      PROJECTED_SKILL_NAMES+=("${projected_skill_name}")
    done <<<"${output}"
  fi
```

- [ ] **Step 4: Check shell syntax**

Run:

```powershell
bash -n check.sh
```

Expected: exits with code `0` and prints no output.

- [ ] **Step 5: Verify `mapfile` no longer appears in shell entrypoints**

Run:

```powershell
rg -n "mapfile" install.sh check.sh scripts\bootstrap\one-shot-setup.sh
```

Expected: exits with code `1` and prints no matches.

- [ ] **Step 6: Run the focused compatibility test**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_shell_entrypoint_compatibility.py -q
```

Expected:

```text
5 passed
```

- [ ] **Step 7: Commit the shell compatibility fix**

Run:

```powershell
git add check.sh
git commit -m "fix: remove bash mapfile from check entrypoint"
```

---

### Task 2: Preserve Windows Trailing Separators For Bash Tests

**Files:**

- Modify: `tests/runtime_neutral/test_bash_test_support.py`
- Modify: `tests/bash_test_support.py`
- Existing test: `tests/runtime_neutral/test_windows_setup_helpers.py`

- [ ] **Step 1: Add the trailing-separator regression test**

In `tests/runtime_neutral/test_bash_test_support.py`, add this test after `test_normalize_bash_command_args_converts_windows_paths`:

```python
def test_normalize_bash_command_args_preserves_windows_trailing_separators(monkeypatch) -> None:
    monkeypatch.setattr(bash_test_support, "resolve_bash_for_tests", lambda: "bash")
    monkeypatch.setattr(
        bash_test_support,
        "to_bash_path",
        lambda path: "/converted/" + str(path).replace("\\", "/").replace(":", ""),
    )

    normalized = bash_test_support.normalize_bash_command_args(
        [
            "bash",
            r"C:\Users\tester\AppData\Local\Temp\case\downloads/",
            "D:\\work\\output\\",
        ]
    )

    assert normalized == [
        "bash",
        "/converted/C/Users/tester/AppData/Local/Temp/case/downloads/",
        "/converted/D/work/output/",
    ]
```

- [ ] **Step 2: Run the Bash test-support tests and verify the new regression fails**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_bash_test_support.py -q
```

Expected: FAIL in `test_normalize_bash_command_args_preserves_windows_trailing_separators` because normalized paths do not end with `/`.

- [ ] **Step 3: Add a helper that preserves explicit trailing separator intent**

In `tests/bash_test_support.py`, add this function after `_is_windows_absolute_path_text()`:

```python
def _normalize_windows_bash_path_arg(value: Any) -> str:
    text = str(value)
    converted = to_bash_path(Path(text))
    if text.endswith(("\\", "/")) and not converted.endswith("/"):
        return converted + "/"
    return converted
```

- [ ] **Step 4: Route Windows path argument conversion through the helper**

In `tests/bash_test_support.py`, replace:

```python
        normalized = [command] + [
            to_bash_path(Path(arg)) if _is_windows_absolute_path_text(arg) else arg
            for arg in args[1:]
        ]
```

with:

```python
        normalized = [command] + [
            _normalize_windows_bash_path_arg(arg) if _is_windows_absolute_path_text(arg) else arg
            for arg in args[1:]
        ]
```

- [ ] **Step 5: Run the focused Bash test-support suite**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_bash_test_support.py -q
```

Expected:

```text
7 passed
```

- [ ] **Step 6: Run the Windows setup helper guard after the path fix**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_windows_setup_helpers.py::WindowsSetupHelpersTests::test_fetch_windows11_eval_iso_rejects_directory_output_path_before_network -q
```

Expected:

```text
1 passed
```

This command must return quickly. If it starts long network work, stop execution and report the path guard as still broken.

- [ ] **Step 7: Run the combined affected path tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_bash_test_support.py tests\runtime_neutral\test_windows_setup_helpers.py -q
```

Expected:

```text
12 passed
```

- [ ] **Step 8: Commit the Windows Bash path fix**

Run:

```powershell
git add tests\runtime_neutral\test_bash_test_support.py tests\bash_test_support.py
git commit -m "test: preserve trailing bash path separators"
```

---

### Task 3: Classify `.vibeskills/` As Local Runtime Noise

**Files:**

- Create: `tests/runtime_neutral/test_repo_cleanliness_policy.py`
- Modify: `.gitignore`
- Modify: `config/repo-cleanliness-policy.json`

- [ ] **Step 1: Add a policy regression test for `.vibeskills/`**

Create `tests/runtime_neutral/test_repo_cleanliness_policy.py` with this content:

```python
from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _gitignore_patterns() -> set[str]:
    lines = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    return {
        line.strip()
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    }


def test_vibeskills_local_state_is_ignored_and_classified() -> None:
    policy = json.loads(
        (REPO_ROOT / "config" / "repo-cleanliness-policy.json").read_text(encoding="utf-8")
    )

    assert ".vibeskills/" in _gitignore_patterns()
    assert ".vibeskills/" in policy["shared_repo_ignores"]
    assert ".vibeskills/" in policy["local_noise_paths"]
```

- [ ] **Step 2: Run the new policy test and verify the current failure**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_repo_cleanliness_policy.py -q
```

Expected: FAIL because `.vibeskills/` is not yet in `.gitignore` or `config/repo-cleanliness-policy.json`.

- [ ] **Step 3: Ignore `.vibeskills/` in Git**

In `.gitignore`, under `# Local operator noise`, replace:

```gitignore
.serena/
.tmp/
.worktrees/
```

with:

```gitignore
.serena/
.tmp/
.vibeskills/
.worktrees/
```

- [ ] **Step 4: Add `.vibeskills/` to repo-cleanliness policy**

In `config/repo-cleanliness-policy.json`, replace the `shared_repo_ignores` block with:

```json
    "shared_repo_ignores":  [
                                ".serena/",
                                ".tmp/",
                                ".vibeskills/"
                            ],
```

In the same file, replace the start of the `local_noise_paths` block with:

```json
    "local_noise_paths":  [
                              ".serena/",
                              ".tmp/",
                              ".vibeskills/",
                              "task_plan.md",
                              "findings.md",
                              "progress.md"
                          ],
```

- [ ] **Step 5: Run the policy regression test**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_repo_cleanliness_policy.py -q
```

Expected:

```text
1 passed
```

- [ ] **Step 6: Commit the local-noise policy fix before running the cleanliness gate**

Run:

```powershell
git add .gitignore config\repo-cleanliness-policy.json tests\runtime_neutral\test_repo_cleanliness_policy.py
git commit -m "chore: classify vibeskills local state as noise"
```

- [ ] **Step 7: Run the repo cleanliness gate**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-repo-cleanliness-gate.ps1
```

Expected:

```text
[PASS] [cleanliness] no local scratch / operator noise is visible in git status
[PASS] [cleanliness] no runtime-generated artifacts are visible in git status
[PASS] [cleanliness] no uncategorized dirty paths remain visible
```

The gate should pass because `.vibeskills/` is no longer visible in `git status`.

---

### Task 4: Final Focused Regression Sweep

**Files:**

- No new implementation files.
- Validation covers `check.sh`, `tests/bash_test_support.py`, `.gitignore`, `config/repo-cleanliness-policy.json`, and the new policy test.

- [ ] **Step 1: Run all focused tests from this cleanup**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_shell_entrypoint_compatibility.py tests\runtime_neutral\test_bash_test_support.py tests\runtime_neutral\test_windows_setup_helpers.py tests\runtime_neutral\test_repo_cleanliness_policy.py -q
```

Expected:

```text
18 passed
```

- [ ] **Step 2: Run the repo cleanliness gate again from a committed tree**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-repo-cleanliness-gate.ps1
```

Expected: exits with code `0` and prints the three cleanliness `[PASS]` assertions.

- [ ] **Step 3: Run contract and unit regression tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\contract tests\unit -q
```

Expected:

```text
284 passed
```

- [ ] **Step 4: Run the verification-core regression surface**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_routing_terminology_hard_cleanup.py tests\runtime_neutral\test_global_pack_consolidation_audit.py tests\runtime_neutral\test_code_quality_pack_consolidation_audit.py tests\runtime_neutral\test_bio_science_pack_consolidation_audit.py tests\runtime_neutral\test_ml_skills_pruning_audit.py -q
```

Expected:

```text
36 passed
```

- [ ] **Step 5: Confirm the current worktree has no uncommitted tracked changes**

Run:

```powershell
git status --short --branch
```

Expected: the first line starts with `## main...origin/main [ahead `, and there are no additional dirty-path lines. There should be no `?? .vibeskills/` line and no tracked modified files.

- [ ] **Step 6: Do not claim full runtime-neutral coverage unless it is actually run**

Record the final verification summary with exact commands and results. If the full `tests\runtime_neutral` suite is not run, state that it was intentionally not claimed because the previous full sweep triggered long Windows ISO setup behavior before this cleanup.

---

## Completion Criteria

- `rg -n "mapfile" install.sh check.sh scripts\bootstrap\one-shot-setup.sh` finds no matches.
- `tests\runtime_neutral\test_shell_entrypoint_compatibility.py` passes.
- `tests\runtime_neutral\test_bash_test_support.py` proves Windows trailing separators are preserved.
- `tests\runtime_neutral\test_windows_setup_helpers.py` passes without long network work.
- `.vibeskills/` is ignored by Git and listed in repo-cleanliness policy.
- `scripts\verify\vibe-repo-cleanliness-gate.ps1` passes from the committed tree.
- Contract/unit and verification-core focused regression tests remain green.
- No deployment, install, push, or host-root mutation occurs.
