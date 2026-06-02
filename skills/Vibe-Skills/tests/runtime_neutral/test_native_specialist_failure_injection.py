from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def resolve_powershell() -> str | None:
    candidates = [
        shutil.which("pwsh"),
        shutil.which("pwsh.exe"),
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        r"C:\Program Files\PowerShell\7-preview\pwsh.exe",
        shutil.which("powershell"),
        shutil.which("powershell.exe"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate))
    return None


def run_runtime(
    task: str,
    artifact_root: Path,
    *,
    governance_scope: str = "root",
    extra_env: dict[str, str] | None = None,
) -> dict[str, object]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available in PATH")

    script_path = REPO_ROOT / "scripts/runtime/invoke-vibe-runtime.ps1"
    run_id = "pytest-native-failure-" + uuid.uuid4().hex[:10]
    command = [
        shell,
        "-NoLogo",
        "-NoProfile",
        "-Command",
        (
            "& { "
            f"$result = & '{script_path}' "
            f"-Task '{task}' "
            "-Mode interactive_governed "
            f"-GovernanceScope {governance_scope} "
            f"-RunId '{run_id}' "
            f"-ArtifactRoot '{artifact_root}'; "
            "$result | ConvertTo-Json -Depth 20 }"
        ),
    ]
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        env={**os.environ, **(extra_env or {})},
    )
    stdout = completed.stdout.strip()
    if stdout in ("", "null"):
        raise AssertionError(
            "invoke-vibe-runtime returned null payload. "
            f"stderr={completed.stderr.strip()}"
        )
    return json.loads(stdout)


def load_json(path: str | Path) -> dict[str, object]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def create_fake_codex_command(directory: Path, *, mode: str) -> Path:
    suffix = ".cmd" if os.name == "nt" else ""
    command_path = directory / f"codex{suffix}"
    if os.name == "nt":
        behaviors = {
            "malformed_json": (
                "> \"%OUT%\" echo {bad-json\r\n"
                "echo fake codex malformed\r\n"
                "exit /b 0\r\n"
            ),
            "missing_required_fields": (
                "> \"%OUT%\" echo {\"status\":\"completed\",\"summary\":\"missing arrays\"}\r\n"
                "echo fake codex schema gap\r\n"
                "exit /b 0\r\n"
            ),
            "missing_response": (
                "echo fake codex no response\r\n"
                "exit /b 0\r\n"
            ),
            "nonzero_with_response": (
                "> \"%OUT%\" echo {\"status\":\"completed\",\"summary\":\"fake codex wrote payload before failing\",\"verification_notes\":[\"nonzero exit injected\"],\"changed_files\":[],\"bounded_output_notes\":[\"failure injection\"]}\r\n"
                "echo fake codex nonzero with response\r\n"
                "exit /b 17\r\n"
            ),
        }
        behavior = behaviors[mode]
        command_path.write_text(
            "@echo off\r\n"
            "setlocal EnableDelayedExpansion\r\n"
            "set OUT=\r\n"
            ":loop\r\n"
            "if \"%~1\"==\"\" goto done\r\n"
            "if \"%~1\"==\"-o\" (\r\n"
            "  set OUT=%~2\r\n"
            "  shift\r\n"
            "  shift\r\n"
            "  goto loop\r\n"
            ")\r\n"
            "shift\r\n"
            "goto loop\r\n"
            ":done\r\n"
            "if \"%OUT%\"==\"\" exit /b 2\r\n"
            + behavior,
            encoding="utf-8",
        )
    else:
        behaviors = {
            "malformed_json": (
                "printf '%s' '{bad-json' > \"$OUT\"\n"
                "printf 'fake codex malformed\\n'\n"
                "exit 0\n"
            ),
            "missing_required_fields": (
                "printf '%s' '{\"status\":\"completed\",\"summary\":\"missing arrays\"}' > \"$OUT\"\n"
                "printf 'fake codex schema gap\\n'\n"
                "exit 0\n"
            ),
            "missing_response": (
                "printf 'fake codex no response\\n'\n"
                "exit 0\n"
            ),
            "nonzero_with_response": (
                "printf '%s' '{\"status\":\"completed\",\"summary\":\"fake codex wrote payload before failing\",\"verification_notes\":[\"nonzero exit injected\"],\"changed_files\":[],\"bounded_output_notes\":[\"failure injection\"]}' > \"$OUT\"\n"
                "printf 'fake codex nonzero with response\\n'\n"
                "exit 17\n"
            ),
        }
        behavior = behaviors[mode]
        command_path.write_text(
            "#!/usr/bin/env sh\n"
            "OUT=''\n"
            "while [ \"$#\" -gt 0 ]; do\n"
            "  case \"$1\" in\n"
            "    -o)\n"
            "      OUT=\"$2\"\n"
            "      shift 2\n"
            "      ;;\n"
            "    *)\n"
            "      shift\n"
            "      ;;\n"
            "  esac\n"
            "done\n"
            "if [ -z \"$OUT\" ]; then\n"
            "  exit 2\n"
            "fi\n"
            + behavior,
            encoding="utf-8",
        )
        command_path.chmod(command_path.stat().st_mode | stat.S_IXUSR)
    return command_path


class NativeSpecialistFailureInjectionTests(unittest.TestCase):
    TASK = "I have a failing test and stack trace. Debug systematically and execute specialist workflow."

    def run_legacy_subprocess_case(
        self, mode: str
    ) -> tuple[dict[str, object], dict[str, object], list[tuple[dict[str, object], dict[str, object]]]]:
        with tempfile.TemporaryDirectory() as tempdir:
            temp_path = Path(tempdir)
            fake_codex = create_fake_codex_command(temp_path, mode=mode)
            payload = run_runtime(
                task=self.TASK,
                artifact_root=temp_path,
                governance_scope="root",
                extra_env={
                    "VGO_ENABLE_NATIVE_SPECIALIST_EXECUTION": "1",
                    "VGO_DISABLE_NATIVE_SPECIALIST_EXECUTION": "0",
                    "VGO_NATIVE_SPECIALIST_EXECUTION_MODE": "host_subprocess",
                    "VGO_SPECIALIST_CONSULTATION_MODE": "host_subprocess",
                    "VGO_CODEX_EXECUTABLE": str(fake_codex),
                },
            )
            summary = payload["summary"]
            execution_manifest = load_json(summary["artifacts"]["execution_manifest"])
            specialist_accounting = execution_manifest["specialist_accounting"]
            direct_routes = [
                (unit, load_json(unit["result_path"]))
                for unit in list(specialist_accounting["direct_routed_skill_execution_units"])
            ]
            self.assertGreaterEqual(len(direct_routes), 1)
            self.assertEqual("direct_current_session_routed", specialist_accounting["effective_execution_status"])
            self.assertEqual(0, int(specialist_accounting["attempted_specialist_unit_count"]))
            self.assertEqual(0, len(list(specialist_accounting["executed_skill_execution_units"])))
            self.assertEqual(0, len(list(specialist_accounting["failed_skill_execution_units"])))
            self.assertGreaterEqual(int(specialist_accounting["direct_routed_skill_execution_unit_count"]), 1)
            self.assertEqual("completed", execution_manifest["status"])

            execution_proof = load_json(summary["artifacts"]["execution_proof_manifest"])
            self.assertEqual("direct_current_session_routed", execution_proof["specialist_execution_status"])
            self.assertEqual(
                int(specialist_accounting["direct_routed_skill_execution_unit_count"]),
                int(execution_proof["direct_routed_skill_execution_unit_count"]),
            )
            return payload, execution_manifest, direct_routes

    def assert_legacy_subprocess_payload_is_direct_routed(self, mode: str) -> None:
        _, _, direct_routes = self.run_legacy_subprocess_case(mode)
        for unit, result in direct_routes:
            with self.subTest(unit_id=unit.get("unit_id", "")):
                self.assertEqual("completed", result["status"])
                self.assertEqual(0, int(result["exit_code"]))
                self.assertTrue(bool(result["verification_passed"]))
                self.assertFalse(bool(result["live_native_execution"]))
                self.assertFalse(bool(result["degraded"]))
                self.assertTrue(bool(result["direct_route"]))
                self.assertEqual("direct_current_session_route", result["execution_driver"])
                self.assertIn("hidden_host_subprocess:false", list(result["verification_notes"]))

    def test_legacy_malformed_json_subprocess_payload_is_not_executed(self) -> None:
        self.assert_legacy_subprocess_payload_is_direct_routed("malformed_json")

    def test_legacy_missing_response_subprocess_payload_is_not_executed(self) -> None:
        self.assert_legacy_subprocess_payload_is_direct_routed("missing_response")

    def test_legacy_missing_required_fields_subprocess_payload_is_not_executed(self) -> None:
        self.assert_legacy_subprocess_payload_is_direct_routed("missing_required_fields")

    def test_legacy_nonzero_subprocess_payload_is_not_executed(self) -> None:
        self.assert_legacy_subprocess_payload_is_direct_routed("nonzero_with_response")


if __name__ == "__main__":
    unittest.main()
