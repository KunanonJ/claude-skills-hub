from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
INSTALL_SCRIPT = REPO_ROOT / "install.sh"
CHECK_SCRIPT = REPO_ROOT / "check.sh"
UNINSTALL_SCRIPT = REPO_ROOT / "uninstall.sh"
BEGIN_MARKER = "<!-- VIBESKILLS:BEGIN managed-block"


class HostGlobalBootstrapShellLifecycleTests(unittest.TestCase):
    def run_install(self, host: str, target_root: Path) -> None:
        subprocess.run(
            [
                "bash",
                str(INSTALL_SCRIPT),
                "--host",
                host,
                "--profile",
                "full",
                "--target-root",
                str(target_root),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

    def bootstrap_receipt_path(self, target_root: Path) -> Path:
        matches = sorted((target_root / ".vibeskills").glob("global-instruction-bootstrap*.json"))
        self.assertTrue(matches)
        return matches[0]

    def run_check(self, host: str, target_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "bash",
                str(CHECK_SCRIPT),
                "--host",
                host,
                "--profile",
                "full",
                "--target-root",
                str(target_root),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

    def run_uninstall(self, host: str, target_root: Path) -> dict[str, object]:
        result = subprocess.run(
            [
                "bash",
                str(UNINSTALL_SCRIPT),
                "--host",
                host,
                "--profile",
                "full",
                "--target-root",
                str(target_root),
                "--purge-empty-dirs",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_shell_lifecycle_keeps_user_instruction_files_safe_and_bootstrap_useful(self) -> None:
        cases = [
            {
                "host": "codex",
                "instruction_relpath": "AGENTS.md",
                "instruction_text": "# Personal Codex rules\n\n- keep this line\n",
                "check_signal": "[OK] codex command/vibe-how-do-we-do",
                "unexpected_check_signal": "[WARN] codex command/",
            },
            {
                "host": "claude-code",
                "instruction_relpath": "CLAUDE.md",
                "instruction_text": "# Personal Claude rules\n\n- keep this line\n",
                "check_signal": "managed settings.json surface",
                "settings_relpath": "settings.json",
                "settings_payload": {
                    "env": {"ANTHROPIC_API_KEY": "secret"},
                    "model": "claude-sonnet-4-6",
                },
            },
            {
                "host": "opencode",
                "instruction_relpath": "AGENTS.md",
                "instruction_text": "# Personal OpenCode rules\n\n- keep this line\n",
                "check_signal": "[OK] opencode preview config example",
                "settings_relpath": "opencode.json",
                "settings_payload": {
                    "$schema": "https://opencode.ai/config.json",
                    "provider": {"default": "openai"},
                },
            },
        ]

        for case in cases:
            with self.subTest(host=case["host"]):
                with tempfile.TemporaryDirectory() as tempdir:
                    target_root = Path(tempdir)
                    instruction_path = target_root / case["instruction_relpath"]
                    instruction_path.parent.mkdir(parents=True, exist_ok=True)
                    instruction_path.write_text(case["instruction_text"], encoding="utf-8")

                    settings_path = None
                    if "settings_relpath" in case:
                        settings_path = target_root / case["settings_relpath"]
                        settings_path.parent.mkdir(parents=True, exist_ok=True)
                        settings_path.write_text(
                            json.dumps(case["settings_payload"], ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8",
                        )

                    self.run_install(case["host"], target_root)

                    merged = instruction_path.read_text(encoding="utf-8")
                    self.assertIn(case["instruction_text"].strip(), merged)
                    self.assertEqual(1, merged.count(BEGIN_MARKER))
                    self.assertIn("$vibe", merged)
                    self.assertIn("/vibe", merged)
                    self.assertIn("canonical `vibe`", merged)

                    receipt_path = self.bootstrap_receipt_path(target_root)
                    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                    self.assertEqual(case["host"], receipt["host"])
                    self.assertEqual(case["instruction_relpath"], receipt["target_relpath"])
                    self.assertEqual("inserted", receipt["action"])
                    self.assertEqual("global-vibe-bootstrap", receipt["block_id"])

                    if case["host"] == "claude-code":
                        settings = json.loads(settings_path.read_text(encoding="utf-8"))
                        self.assertEqual(case["settings_payload"]["env"], settings["env"])
                        self.assertEqual(case["settings_payload"]["model"], settings["model"])
                        self.assertEqual("claude-code", settings["vibeskills"]["host_id"])
                    elif case["host"] == "opencode":
                        self.assertEqual(case["settings_payload"], json.loads(settings_path.read_text(encoding="utf-8")))

                    check_result = self.run_check(case["host"], target_root)
                    self.assertIn(case["check_signal"], check_result.stdout)
                    if "unexpected_check_signal" in case:
                        self.assertNotIn(case["unexpected_check_signal"], check_result.stdout)

                    self.run_install(case["host"], target_root)

                    merged_again = instruction_path.read_text(encoding="utf-8")
                    receipt_again = json.loads(self.bootstrap_receipt_path(target_root).read_text(encoding="utf-8"))
                    self.assertEqual(1, merged_again.count(BEGIN_MARKER))
                    self.assertEqual("unchanged", receipt_again["action"])

                    uninstall_payload = self.run_uninstall(case["host"], target_root)
                    self.assertIn("PASS", uninstall_payload["gate_result"])

                    self.assertTrue(instruction_path.exists())
                    self.assertEqual(case["instruction_text"], instruction_path.read_text(encoding="utf-8"))

                    if case["host"] == "claude-code":
                        self.assertTrue(settings_path.exists())
                        self.assertEqual(case["settings_payload"], json.loads(settings_path.read_text(encoding="utf-8")))
                    elif case["host"] == "opencode":
                        self.assertTrue(settings_path.exists())
                        self.assertEqual(case["settings_payload"], json.loads(settings_path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
