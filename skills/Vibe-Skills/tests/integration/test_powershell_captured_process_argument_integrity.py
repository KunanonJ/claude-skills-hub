from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]


def _require_powershell() -> str:
    powershell = shutil.which("pwsh") or shutil.which("powershell")
    if not powershell:
        pytest.skip("PowerShell executable not available in PATH")
    return powershell


def test_invoke_vibe_captured_process_preserves_multiline_prompt_as_single_argument(
    tmp_path: Path,
) -> None:
    powershell = _require_powershell()
    captured_args_path = tmp_path / "captured-args.json"
    script_path = tmp_path / "capture_args.py"
    stdout_path = tmp_path / "stdout.txt"
    stderr_path = tmp_path / "stderr.txt"
    prompt = "line1\nline two with spaces\nconsultation_role: discussion_consultant"
    script_path.write_text(
        "import json, pathlib, sys\n"
        "pathlib.Path(sys.argv[1]).write_text("
        "json.dumps(sys.argv[2:], ensure_ascii=False), encoding='utf-8')\n",
        encoding="utf-8",
    )

    command = f"""
. '{(REPO_ROOT / "scripts" / "runtime" / "VibeExecution.Common.ps1").as_posix()}'
$prompt = @'
{prompt}
'@
Invoke-VibeCapturedProcess `
    -Command '{shutil.which("python3") or sys.executable}' `
    -Arguments @(
        '{script_path.as_posix()}',
        '{captured_args_path.as_posix()}',
        '--flag',
        'value with spaces',
        $prompt
    ) `
    -WorkingDirectory '{REPO_ROOT.as_posix()}' `
    -TimeoutSeconds 10 `
    -StdOutPath '{stdout_path.as_posix()}' `
    -StdErrPath '{stderr_path.as_posix()}' | Out-Null
"""

    subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-Command", command],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    captured_args = json.loads(captured_args_path.read_text(encoding="utf-8"))
    assert captured_args == ["--flag", "value with spaces", prompt]


def test_invoke_vibe_captured_process_applies_environment_overrides(tmp_path: Path) -> None:
    powershell = _require_powershell()
    captured_env_path = tmp_path / "captured-env.json"
    script_path = tmp_path / "capture_env.py"
    stdout_path = tmp_path / "stdout.txt"
    stderr_path = tmp_path / "stderr.txt"
    script_path.write_text(
        "import json, os, pathlib, sys\n"
        "pathlib.Path(sys.argv[1]).write_text("
        "json.dumps({'SPECIAL_TEST_ENV': os.environ.get('SPECIAL_TEST_ENV')}, ensure_ascii=False), encoding='utf-8')\n",
        encoding="utf-8",
    )

    command = f"""
. '{(REPO_ROOT / "scripts" / "runtime" / "VibeExecution.Common.ps1").as_posix()}'
Invoke-VibeCapturedProcess `
    -Command '{shutil.which("python3") or sys.executable}' `
    -Arguments @(
        '{script_path.as_posix()}',
        '{captured_env_path.as_posix()}'
    ) `
    -WorkingDirectory '{REPO_ROOT.as_posix()}' `
    -TimeoutSeconds 10 `
    -StdOutPath '{stdout_path.as_posix()}' `
    -StdErrPath '{stderr_path.as_posix()}' `
    -EnvironmentOverrides @{{ SPECIAL_TEST_ENV = 'expected-value' }} | Out-Null
"""

    subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-Command", command],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    captured_env = json.loads(captured_env_path.read_text(encoding="utf-8"))
    assert captured_env == {"SPECIAL_TEST_ENV": "expected-value"}


def test_invoke_vibe_captured_process_closes_stdin_for_child_process(tmp_path: Path) -> None:
    powershell = _require_powershell()
    stdin_state_path = tmp_path / "stdin-state.json"
    script_path = tmp_path / "capture_stdin.py"
    stdout_path = tmp_path / "stdout.txt"
    stderr_path = tmp_path / "stderr.txt"
    script_path.write_text(
        "import json, pathlib, sys\n"
        "payload = sys.stdin.read()\n"
        "pathlib.Path(sys.argv[1]).write_text("
        "json.dumps({'stdin_closed': payload == ''}, ensure_ascii=False), encoding='utf-8')\n",
        encoding="utf-8",
    )

    command = f"""
. '{(REPO_ROOT / "scripts" / "runtime" / "VibeExecution.Common.ps1").as_posix()}'
Invoke-VibeCapturedProcess `
    -Command '{shutil.which("python3") or sys.executable}' `
    -Arguments @(
        '{script_path.as_posix()}',
        '{stdin_state_path.as_posix()}'
    ) `
    -WorkingDirectory '{REPO_ROOT.as_posix()}' `
    -TimeoutSeconds 10 `
    -StdOutPath '{stdout_path.as_posix()}' `
    -StdErrPath '{stderr_path.as_posix()}' | Out-Null
"""

    subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-Command", command],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    stdin_state = json.loads(stdin_state_path.read_text(encoding="utf-8"))
    assert stdin_state == {"stdin_closed": True}
