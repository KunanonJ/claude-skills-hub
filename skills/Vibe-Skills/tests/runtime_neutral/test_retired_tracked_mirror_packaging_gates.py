from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
HELPERS = REPO_ROOT / "scripts" / "common" / "vibe-governance-helpers.ps1"
VERSION_GATE = REPO_ROOT / "scripts" / "verify" / "vibe-version-packaging-gate.ps1"
NESTED_GATE = REPO_ROOT / "scripts" / "verify" / "vibe-nested-bundled-parity-gate.ps1"


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


class RetiredTrackedMirrorPackagingGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.powershell = resolve_powershell()
        if self.powershell is None:
            self.skipTest("PowerShell is required for retired tracked mirror gate tests.")
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self._write_fixture()
        subprocess.run(["git", "init"], cwd=self.root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.root, capture_output=True, text=True, check=True)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _write(self, relative_path: str, content: str) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    def _write_fixture(self) -> None:
        self._write("scripts/common/vibe-governance-helpers.ps1", HELPERS.read_text(encoding="utf-8"))
        self._write("scripts/verify/vibe-version-packaging-gate.ps1", VERSION_GATE.read_text(encoding="utf-8"))
        self._write("scripts/verify/vibe-nested-bundled-parity-gate.ps1", NESTED_GATE.read_text(encoding="utf-8"))
        self._write(
            "config/version-governance.json",
            json.dumps(
                {
                    "release": {"version": "9.9.9", "updated": "2026-04-01", "channel": "stable", "notes": "fixture"},
                    "source_of_truth": {"canonical_root": "."},
                    "mirror_topology": {
                        "canonical_target_id": "canonical",
                        "sync_source_target_id": "canonical",
                        "targets": [
                            {"id": "canonical", "path": ".", "role": "canonical", "required": True, "presence_policy": "required", "sync_enabled": False, "parity_policy": "authoritative"}
                        ],
                    },
                    "execution_context_policy": {
                        "require_outer_git_root": True,
                        "fail_if_script_path_is_under_mirror_root": True,
                    },
                    "version_markers": {
                        "maintenance_files": ["SKILL.md"],
                        "changelog_path": "references/changelog.md",
                    },
                    "logs": {
                        "release_ledger_jsonl": "references/release-ledger.jsonl",
                        "release_notes_dir": "docs/releases",
                    },
                    "packaging": {
                        "runtime_payload": {
                            "files": ["SKILL.md", "check.ps1", "check.sh", "install.ps1", "install.sh"],
                            "directories": ["templates", "mcp"],
                        },
                        "generated_compatibility": {
                            "nested_runtime_root": {
                                "relative_path": "bundled/skills/vibe",
                                "materialization_mode": "install_only",
                            }
                        },
                        "allow_installed_only": [],
                        "normalized_json_ignore_keys": ["updated", "generated_at"],
                    },
                    "runtime": {
                        "installed_runtime": {
                            "target_relpath": "skills/vibe",
                            "receipt_relpath": "skills/vibe/outputs/runtime-freshness-receipt.json",
                            "receipt_contract_version": 1,
                            "required_runtime_markers": [
                                "SKILL.md",
                                "config/version-governance.json",
                            ],
                            "require_nested_bundled_root": False,
                        }
                    },
                },
                indent=2,
            )
            + "\n",
        )
        self._write("SKILL.md", "---\nname: vibe\ndescription: fixture\n---\n")
        self._write("check.ps1", "Write-Host 'check'\n")
        self._write("check.sh", "echo check\n")
        self._write("install.ps1", "Write-Host 'install'\n")
        self._write("install.sh", "echo install\n")
        self._write("templates/ORIGIN.md.tmpl", "origin\n")
        self._write("mcp/profiles/full.json", "{}\n")
        self._write("references/changelog.md", "# changelog\n")
        self._write("references/release-ledger.jsonl", json.dumps({"version": "9.9.9", "updated": "2026-04-01"}) + "\n")

    def _run_gate(self, relative_script: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                self.powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(self.root / relative_script),
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=True,
        )

    def test_version_packaging_gate_passes_when_tracked_mirror_is_retired(self) -> None:
        result = self._run_gate("scripts/verify/vibe-version-packaging-gate.ps1")
        self.assertIn("Gate Result: PASS", result.stdout)
        self.assertIn("tracked bundled mirror root is absent from repo", result.stdout)

    def test_nested_bundled_parity_gate_passes_when_generated_compatibility_is_install_only(self) -> None:
        result = self._run_gate("scripts/verify/vibe-nested-bundled-parity-gate.ps1")
        self.assertIn("[PASS] [topology] tracked bundled target is not declared", result.stdout)
        self.assertIn("[PASS] [compat] generated nested runtime root stays install_only", result.stdout)


if __name__ == "__main__":
    unittest.main()
