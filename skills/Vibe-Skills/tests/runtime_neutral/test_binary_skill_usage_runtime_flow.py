from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def resolve_powershell() -> str | None:
    candidates = [
        shutil.which("pwsh"),
        shutil.which("pwsh.exe"),
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        shutil.which("powershell"),
        shutil.which("powershell.exe"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate))
    return None


class BinarySkillUsageRuntimeFlowTests(unittest.TestCase):
    def test_requirement_and_plan_promote_loaded_skill_to_used(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available")

        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir) / "artifacts"
            run_id = "pytest-binary-skill-usage-flow"
            task = "Use biopython to parse FASTA and summarize sequence lengths."
            for script_name in (
                "Freeze-RuntimeInputPacket.ps1",
                "Invoke-SkeletonCheck.ps1",
                "Invoke-DeepInterview.ps1",
                "Write-RequirementDoc.ps1",
                "Write-XlPlan.ps1",
            ):
                command = [
                    shell,
                    "-NoLogo",
                    "-NoProfile",
                    "-File",
                    str(REPO_ROOT / "scripts" / "runtime" / script_name),
                    "-Task",
                    task,
                    "-Mode",
                    "interactive_governed",
                    "-RunId",
                    run_id,
                    "-ArtifactRoot",
                    str(artifact_root),
                ]
                subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", check=True)

            session_root = next(artifact_root.rglob(run_id))
            packet = json.loads((session_root / "runtime-input-packet.json").read_text(encoding="utf-8"))
            selected_skill = packet["route_snapshot"]["selected_skill"]
            usage_path = session_root / "skill-usage.json"
            usage = json.loads(usage_path.read_text(encoding="utf-8"))
            requirement_receipt = json.loads((session_root / "requirement-doc-receipt.json").read_text(encoding="utf-8"))
            plan_receipt = json.loads((session_root / "execution-plan-receipt.json").read_text(encoding="utf-8"))
            requirement_text = Path(requirement_receipt["requirement_doc_path"]).read_text(encoding="utf-8")
            plan_text = Path(plan_receipt["execution_plan_path"]).read_text(encoding="utf-8")

            self.assertIn(selected_skill, usage["used_skills"])
            self.assertNotIn(selected_skill, usage["unused_skills"])
            stages = {row["stage"] for row in usage["evidence"] if row["skill_id"] == selected_skill}
            self.assertIn("requirement_doc", stages)
            self.assertIn("xl_plan", stages)
            self.assertIn("## Skill Usage", requirement_text)
            self.assertIn("## Binary Skill Usage Plan", plan_text)

    def test_plan_execute_and_cleanup_preserve_skill_usage_truth(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available")

        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir) / "artifacts"
            run_id = "pytest-binary-skill-usage-execute"
            task = "Use biopython to parse FASTA and summarize sequence lengths."
            for script_name in (
                "Freeze-RuntimeInputPacket.ps1",
                "Invoke-SkeletonCheck.ps1",
                "Invoke-DeepInterview.ps1",
                "Write-RequirementDoc.ps1",
                "Write-XlPlan.ps1",
                "Invoke-PlanExecute.ps1",
                "Invoke-PhaseCleanup.ps1",
            ):
                command = [
                    shell,
                    "-NoLogo",
                    "-NoProfile",
                    "-File",
                    str(REPO_ROOT / "scripts" / "runtime" / script_name),
                    "-Task",
                    task,
                    "-Mode",
                    "interactive_governed",
                    "-RunId",
                    run_id,
                    "-ArtifactRoot",
                    str(artifact_root),
                ]
                subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", check=True)

            session_root = next(artifact_root.rglob(run_id))
            usage = json.loads((session_root / "skill-usage.json").read_text(encoding="utf-8"))
            execution_manifest = json.loads((session_root / "execution-manifest.json").read_text(encoding="utf-8"))
            phase_execute = json.loads((session_root / "phase-execute.json").read_text(encoding="utf-8"))
            cleanup = json.loads((session_root / "cleanup-receipt.json").read_text(encoding="utf-8"))
            selected_skill = json.loads((session_root / "runtime-input-packet.json").read_text(encoding="utf-8"))[
                "route_snapshot"
            ]["selected_skill"]

            self.assertIn(selected_skill, usage["used_skills"])
            self.assertEqual(usage["used_skills"], execution_manifest["skill_usage"]["used_skills"])
            self.assertEqual(usage["used_skills"], phase_execute["skill_usage"]["used_skills"])
            self.assertEqual(usage["used_skills"], cleanup["skill_usage"]["used_skills"])
            self.assertGreaterEqual(cleanup["skill_usage_summary"]["used_skill_count"], 1)


if __name__ == "__main__":
    unittest.main()
