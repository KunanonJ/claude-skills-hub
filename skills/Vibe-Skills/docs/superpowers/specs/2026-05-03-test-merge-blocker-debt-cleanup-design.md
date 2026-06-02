# Test Merge-Blocker Debt Cleanup Design

## Summary

This design targets the current merge-blocking technical debt on `main` after
the verification-core retired-field hard-erasure branch was fast-forward merged.
The cleanup is intentionally narrow: make the focused tests and cleanliness gate
safe and stable before continuing any broader terminology or runtime cleanup.

The debt falls into three buckets:

1. `check.sh` still uses Bash `mapfile`, which is incompatible with the shell
   entrypoint compatibility contract.
2. Windows Bash test command normalization strips a user-supplied trailing slash
   from Windows absolute path arguments. That can turn a directory-shaped output
   path into a file-shaped path and bypass pre-network guard tests.
3. `.vibeskills/` is local runtime/operator state, but the repository
   cleanliness gate currently treats it as uncategorized dirty state.

The recommended approach is test stability hardening, not a minimal string-only
patch. The change should remove the immediate blockers while preserving existing
runtime/router semantics.

## Current Evidence

Fresh local evidence on Windows:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_shell_entrypoint_compatibility.py -q
```

Current result:

```text
1 failed, 4 passed
```

The failing test is:

```text
tests/runtime_neutral/test_shell_entrypoint_compatibility.py::ShellEntrypointCompatibilityTests::test_install_entrypoints_avoid_mapfile
```

The failure is caused by `mapfile` in `check.sh`:

```text
check.sh:604: mapfile -t allowlist <<<"${allowlist_output}"
check.sh:635: mapfile -t PROJECTED_SKILL_NAMES <<<"${output}"
```

Windows Bash path normalization evidence:

```powershell
@'
from tests.bash_test_support import normalize_bash_command_args
cmd = ["bash", r"F:\vibe\Vibe-Skills\scripts\setup\fetch-windows11-eval-iso.sh", "--output", r"C:\Users\tester\AppData\Local\Temp\case\downloads/"]
print(normalize_bash_command_args(cmd))
'@ | python -
```

Current output:

```python
['D:\\tool\\Git\\usr\\bin\\bash.exe', '/f/vibe/Vibe-Skills/scripts/setup/fetch-windows11-eval-iso.sh', '--output', '/c/Users/tester/AppData/Local/Temp/case/downloads']
```

The original `downloads/` argument is directory-shaped. After normalization the
trailing slash is gone, so `scripts/setup/fetch-windows11-eval-iso.sh` may not
hit its directory-output rejection before attempting network work.

The relevant guard test is:

```text
tests/runtime_neutral/test_windows_setup_helpers.py::test_fetch_windows11_eval_iso_rejects_directory_output_path_before_network
```

The script guard is:

```bash
if [[ -d "${OUTPUT_PATH}" || "${OUTPUT_PATH}" == */ ]]; then
  echo "[ERROR] --output must be a file path, not a directory: ${OUTPUT_PATH}" >&2
  exit 1
fi
```

Repository cleanliness evidence:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-repo-cleanliness-gate.ps1
```

Current result:

```text
Dirty paths: 1
[PASS] [cleanliness] no local scratch / operator noise is visible in git status
[PASS] [cleanliness] no runtime-generated artifacts are visible in git status
[FAIL] [cleanliness] no uncategorized dirty paths remain visible
```

`git status --short --branch` currently reports:

```text
## main...origin/main [ahead 37]
?? .vibeskills/
```

`config/repo-cleanliness-policy.json` already recognizes local noise such as
`.serena/`, `.tmp/`, and scratch planning files, but not `.vibeskills/`.

## Goals

1. Make shell entrypoint compatibility pass without relying on Bash 4-only
   builtins.
2. Preserve trailing directory separators when Windows absolute path arguments
   are normalized for Git Bash command execution.
3. Ensure `.vibeskills/` is treated as local runtime/operator noise rather than
   uncategorized repository debt.
4. Add focused regression coverage for the path-normalization behavior so the
   Windows ISO helper test cannot accidentally trigger a long download path.
5. Keep validation bounded and evidence-based: first prove the affected tests
   and gate are fixed, then run broader regression checks only after the
   network-risk guard is stable.

## Non-Goals

- Do not change runtime/router routing semantics.
- Do not continue old terminology cleanup in this pass.
- Do not deploy, install, or push anything.
- Do not write to `C:\Users\羽裳\.codex`.
- Do not refactor Windows VM or ISO download tooling beyond the test-safety
  boundary needed here.
- Do not split large files or perform unrelated code cleanup.
- Do not claim the full runtime-neutral suite is green unless it is actually
  run to completion after this guard is fixed.

## Design

### 1. Bash Entry Point Compatibility

Affected implementation:

- `check.sh`

Affected test:

- `tests/runtime_neutral/test_shell_entrypoint_compatibility.py`

Replace the two `mapfile` usages with a Bash 3-compatible array-loading helper
or local loop pattern. The behavior must stay the same:

- Preserve each non-empty output line as one array element.
- Produce an empty array when the source output is empty.
- Preserve the existing error handling around JSON parsing and projection
  lookup.
- Avoid `eval`.

The implementation should prefer a small reusable helper inside `check.sh` if
both call sites can use the same behavior clearly. The helper should read from
standard input or accept a string in a way that does not collapse line
boundaries.

### 2. Windows Bash Path Separator Preservation

Affected implementation:

- `tests/bash_test_support.py`

Affected tests:

- `tests/runtime_neutral/test_bash_test_support.py`
- `tests/runtime_neutral/test_windows_setup_helpers.py`

`normalize_bash_command_args()` currently converts Windows absolute path text
through `Path(arg).resolve()` via `to_bash_path()`. That is fine for most file
paths, but it loses whether the original argument ended with `\` or `/`.

The design is to preserve explicit trailing separator intent for Windows
absolute path arguments:

- Detect whether the original argument string ends with `\` or `/`.
- Convert the path using the existing Bash path conversion behavior.
- If the original had a trailing separator and the converted path does not end
  in `/`, append `/`.
- Do not add a trailing slash to root-only conversions that already end with
  `/`.
- Do not change non-Bash commands.
- Do not change non-Windows path arguments.

Add a regression test that proves:

```python
r"C:\Users\tester\AppData\Local\Temp\case\downloads/"
```

normalizes to a Bash path ending in:

```text
/downloads/
```

This keeps `fetch-windows11-eval-iso.sh` on the pre-network rejection path when
the user supplied a directory-shaped `--output` value.

### 3. Local Runtime Noise Classification

Affected files:

- `.gitignore`
- `config/repo-cleanliness-policy.json`
- any focused cleanliness-policy tests that already cover local noise lists

`.vibeskills/` is local runtime/operator state. It should not be tracked, and it
should not fail the cleanliness gate as uncategorized dirty state.

The design is:

- Add `.vibeskills/` to `.gitignore` alongside existing local operator noise.
- Add `.vibeskills/` to `local_noise_paths` in
  `config/repo-cleanliness-policy.json` if the gate reads policy directly for
  visible dirty classification.
- Add or update a focused policy/gate test only if the existing test structure
  has a natural place for local-noise expectations.

The implementation should not delete `.vibeskills/`; it should make the repo
policy classify it correctly.

## Validation Strategy

Run focused checks first:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_shell_entrypoint_compatibility.py -q
```

Expected result: all tests pass.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_bash_test_support.py tests\runtime_neutral\test_windows_setup_helpers.py -q
```

Expected result: all tests pass without starting a Windows ISO download.

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-repo-cleanliness-gate.ps1
```

Expected result: no uncategorized `.vibeskills/` dirty path remains visible.

Then run bounded regression checks:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\contract tests\unit -q
```

Expected result: pass.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_routing_terminology_hard_cleanup.py tests\runtime_neutral\test_global_pack_consolidation_audit.py tests\runtime_neutral\test_code_quality_pack_consolidation_audit.py tests\runtime_neutral\test_bio_science_pack_consolidation_audit.py tests\runtime_neutral\test_ml_skills_pruning_audit.py -q
```

Expected result: pass, preserving the verification-core cleanup regression
surface.

Only after the path guard is fixed should a broader runtime-neutral sweep be
considered. If it is run and times out or hits unrelated long-running setup
work, report that result explicitly instead of claiming a full green baseline.

## Risks And Mitigations

Risk: the Bash replacement changes empty-output array behavior.

Mitigation: keep focused assertions around `check.sh` compatibility and preserve
the existing explicit empty-array handling.

Risk: trailing slash preservation changes ordinary file path arguments.

Mitigation: only preserve separators that the caller explicitly supplied on
Windows absolute path text passed to Bash command normalization. Leave non-Bash
commands and non-Windows paths unchanged.

Risk: classifying `.vibeskills/` as noise could hide meaningful repository
state.

Mitigation: classify only the local runtime state directory, matching existing
operator-noise handling. Do not broaden ignore rules beyond `.vibeskills/`.

Risk: broader runtime-neutral tests may still be slow or touch network setup
paths.

Mitigation: validate the exact guard first, then expand regression coverage in a
bounded order and report any remaining timeout as a separate debt item.
