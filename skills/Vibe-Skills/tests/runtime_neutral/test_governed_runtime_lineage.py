from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = REPO_ROOT / "config" / "runtime-input-packet-policy.json"
RUNTIME_ENTRY = REPO_ROOT / "scripts" / "runtime" / "invoke-vibe-runtime.ps1"


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


def run_governed_runtime(task: str, artifact_root: Path) -> dict[str, object]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available in PATH")

    run_id = "pytest-lineage-" + uuid.uuid4().hex[:10]
    completed = subprocess.run(
        [
            shell,
            "-NoLogo",
            "-NoProfile",
            "-Command",
            (
                "& { "
                f"$result = & '{RUNTIME_ENTRY}' "
                f"-Task '{task}' "
                "-Mode interactive_governed "
                f"-RunId '{run_id}' "
                f"-ArtifactRoot '{artifact_root}'; "
                "$result | ConvertTo-Json -Depth 20 }"
            ),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return json.loads(completed.stdout)


class GovernedRuntimeLineageTests(unittest.TestCase):
    def test_runtime_policy_declares_governance_artifact_contract(self) -> None:
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        artifact_contract = policy["hierarchy_contract"]["governance_artifacts"]

        self.assertEqual("governance-capsule.json", artifact_contract["capsule"])
        self.assertEqual("stage-lineage.json", artifact_contract["lineage"])
        self.assertEqual("delegation-envelope.json", artifact_contract["delegation_envelope"])
        self.assertEqual("delegation-validation-receipt.json", artifact_contract["delegation_validation"])

    def test_root_runtime_writes_capsule_and_stage_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            payload = run_governed_runtime(
                "Governed entry lineage runtime smoke.",
                artifact_root=Path(tempdir),
            )
            artifacts = payload["summary"]["artifacts"]

            capsule = json.loads(Path(artifacts["governance_capsule"]).read_text(encoding="utf-8"))
            lineage = json.loads(Path(artifacts["stage_lineage"]).read_text(encoding="utf-8"))

            self.assertEqual("vibe", capsule["runtime_selected_skill"])
            self.assertEqual("root", capsule["governance_scope"])
            self.assertEqual(
                [
                    "skeleton_check",
                    "deep_interview",
                    "requirement_doc",
                    "xl_plan",
                    "plan_execute",
                    "phase_cleanup",
                ],
                [entry["stage_name"] for entry in lineage["stages"]],
            )


if __name__ == "__main__":
    unittest.main()
