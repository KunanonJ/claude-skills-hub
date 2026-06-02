from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
HELPERS = REPO_ROOT / "scripts" / "common" / "vibe-governance-helpers.ps1"
GATE = REPO_ROOT / "scripts" / "verify" / "vibe-mirror-edit-hygiene-gate.ps1"


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


class MirrorEditHygieneGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.powershell = resolve_powershell()
        if self.powershell is None:
            self.skipTest("PowerShell is required for hygiene-gate tests.")
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self._write_fixture()
        subprocess.run(["git", "init"], cwd=self.root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "commit", "-m", "fixture"], cwd=self.root, capture_output=True, text=True, check=True)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _write(self, relative_path: str, content: str) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    def _write_fixture(self) -> None:
        self._write("scripts/common/vibe-governance-helpers.ps1", HELPERS.read_text(encoding="utf-8"))
        self._write("scripts/verify/vibe-mirror-edit-hygiene-gate.ps1", GATE.read_text(encoding="utf-8"))
        self._write(
            "config/version-governance.json",
            json.dumps(
                {
                    "release": {"version": "9.9.9", "updated": "2026-03-31", "channel": "stable", "notes": "fixture"},
                    "source_of_truth": {
                        "canonical_root": ".",
                        "bundled_root": "bundled/skills/vibe",
                        "nested_bundled_root": "bundled/skills/vibe/bundled/skills/vibe",
                    },
                    "mirror_topology": {
                        "canonical_target_id": "canonical",
                        "sync_source_target_id": "canonical",
                        "targets": [
                            {"id": "canonical", "path": ".", "role": "canonical", "required": True, "presence_policy": "required", "sync_enabled": False, "parity_policy": "authoritative"},
                            {"id": "bundled", "path": "bundled/skills/vibe", "role": "mirror", "required": True, "presence_policy": "required", "sync_enabled": True, "parity_policy": "full"},
                            {"id": "nested_bundled", "path": "bundled/skills/vibe/bundled/skills/vibe", "role": "mirror", "required": False, "presence_policy": "if_present_must_match", "sync_enabled": False, "parity_policy": "full", "materialization_mode": "release_install_only"},
                        ],
                    },
                    "execution_context_policy": {
                        "require_outer_git_root": True,
                        "fail_if_script_path_is_under_mirror_root": True,
                    },
                    "packaging": {
                        "mirror": {
                            "files": ["SKILL.md"],
                            "directories": ["config", "scripts"],
                        },
                        "target_overrides": {
                            "bundled": {
                                "files": ["README.md"],
                                "directories": ["agents"],
                            }
                        },
                        "allow_bundled_only": [],
                    },
                },
                indent=2,
            )
            + "\n",
        )

        self._write("SKILL.md", "---\nname: vibe\ndescription: fixture\n---\n")
        self._write("README.md", "# canonical readme\n")
        self._write("config/sample.json", json.dumps({"version": 1}, indent=2) + "\n")
        self._write("scripts/sample.ps1", "Write-Host 'sample'\n")
        self._write("docs/readme.md", "# canonical docs\n")

        self._write("bundled/skills/vibe/SKILL.md", "---\nname: vibe\ndescription: bundled fixture\n---\n")
        self._write("bundled/skills/vibe/README.md", "# bundled readme\n")
        self._write("bundled/skills/vibe/config/sample.json", json.dumps({"version": 1}, indent=2) + "\n")
        self._write("bundled/skills/vibe/scripts/sample.ps1", "Write-Host 'sample'\n")
        self._write("bundled/skills/vibe/docs/readme.md", "# bundled docs\n")

    def _run_gate(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                self.powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(self.root / "scripts" / "verify" / "vibe-mirror-edit-hygiene-gate.ps1"),
                "-WriteArtifacts",
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=True,
        )

    def test_gate_allows_pruned_legacy_directories_removed_from_mirror_contract(self) -> None:
        shutil.rmtree(self.root / "bundled" / "skills" / "vibe" / "docs")

        result = self._run_gate()
        self.assertIn("[PASS] [hygiene] no mirror-only edits detected", result.stdout)

        artifact = json.loads(
            (self.root / "outputs" / "verify" / "vibe-mirror-edit-hygiene-gate.json").read_text(encoding="utf-8")
        )
        self.assertEqual("PASS", artifact["gate_result"])
        reconciled_paths = {item["path"] for item in artifact["reconciled_mirror_edits"]}
        self.assertIn("bundled/skills/vibe/docs/readme.md", reconciled_paths)
        mirror_only_paths = {item["path"] for item in artifact["mirror_only_edits"]}
        self.assertNotIn("bundled/skills/vibe/docs/readme.md", mirror_only_paths)

    def test_gate_allows_bundled_target_specific_release_surface_when_paired_with_canonical(self) -> None:
        (self.root / "README.md").write_text("# canonical readme updated\n", encoding="utf-8")
        (self.root / "bundled" / "skills" / "vibe" / "README.md").write_text("# canonical readme updated\n", encoding="utf-8")

        result = self._run_gate()
        self.assertIn("[PASS] [hygiene] no mirror-only edits detected", result.stdout)

        artifact = json.loads(
            (self.root / "outputs" / "verify" / "vibe-mirror-edit-hygiene-gate.json").read_text(encoding="utf-8")
        )
        self.assertEqual("PASS", artifact["gate_result"])
        paired_paths = {item["path"] for item in artifact["paired_mirror_edits"]}
        self.assertIn("bundled/skills/vibe/README.md", paired_paths)

    def test_gate_allows_retiring_tracked_mirror_in_canonical_only_mode(self) -> None:
        governance_path = self.root / "config" / "version-governance.json"
        governance = json.loads(governance_path.read_text(encoding="utf-8"))
        governance["source_of_truth"] = {"canonical_root": "."}
        governance["mirror_topology"] = {
            "canonical_target_id": "canonical",
            "sync_source_target_id": "canonical",
            "targets": [
                {"id": "canonical", "path": ".", "role": "canonical", "required": True, "presence_policy": "required", "sync_enabled": False, "parity_policy": "authoritative"}
            ],
        }
        governance["packaging"] = {
            "runtime_payload": {"files": ["SKILL.md"], "directories": ["config", "scripts"]},
            "generated_compatibility": {
                "nested_runtime_root": {
                    "relative_path": "bundled/skills/vibe",
                    "materialization_mode": "install_only",
                }
            },
            "allow_installed_only": [],
        }
        governance_path.write_text(json.dumps(governance, indent=2) + "\n", encoding="utf-8")

        shutil.rmtree(self.root / "bundled" / "skills" / "vibe")

        result = self._run_gate()
        self.assertIn("[PASS] [hygiene] no mirror-only edits detected", result.stdout)

        artifact = json.loads(
            (self.root / "outputs" / "verify" / "vibe-mirror-edit-hygiene-gate.json").read_text(encoding="utf-8")
        )
        self.assertEqual("PASS", artifact["gate_result"])
        self.assertEqual("canonical_only_retired_tracked_mirror", artifact["mode"])
        reconciled_paths = {item["path"] for item in artifact["reconciled_mirror_edits"]}
        self.assertIn("bundled/skills/vibe/SKILL.md", reconciled_paths)


if __name__ == "__main__":
    unittest.main()
