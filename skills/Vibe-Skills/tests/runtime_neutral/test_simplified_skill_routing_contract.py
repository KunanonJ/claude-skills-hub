from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeRuntime.Common.ps1"
SKILL_USAGE_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeSkillUsage.Common.ps1"
SKILL_ROUTING_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeSkillRouting.Common.ps1"
FREEZE_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "Freeze-RuntimeInputPacket.ps1"


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


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def run_ps_json(script: str) -> dict[str, object]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available")
    completed = subprocess.run(
        [shell, "-NoLogo", "-NoProfile", "-Command", script],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return json.loads(completed.stdout)


def as_list(value: object) -> list[object]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


class SimplifiedSkillRoutingContractTests(unittest.TestCase):
    def test_helper_builds_candidate_selected_rejected_from_legacy_inputs(self) -> None:
        payload = run_ps_json(
            "& { "
            f". {ps_quote(str(RUNTIME_COMMON))}; "
            f". {ps_quote(str(SKILL_USAGE_COMMON))}; "
            f". {ps_quote(str(SKILL_ROUTING_COMMON))}; "
            "$recommendations = @( "
            "[pscustomobject]@{ skill_id = 'scikit-learn'; reason = 'model training'; native_skill_entrypoint = 'skills/scikit/SKILL.md'; dispatch_phase = 'in_execution'; parallelizable_in_root_xl = $true }, "
            "[pscustomobject]@{ skill_id = 'plotly'; reason = 'optional charting'; native_skill_entrypoint = 'skills/plotly/SKILL.md'; dispatch_phase = 'post_execution'; parallelizable_in_root_xl = $false } "
            "); "
            "$hints = @([pscustomobject]@{ skill_id = 'matplotlib'; reason = 'legacy stage helper' }); "
            "$dispatch = [pscustomobject]@{ "
            "approved_dispatch = @($recommendations[0]); "
            "local_specialist_suggestions = @($recommendations[1]); "
            "blocked = @(); degraded = @() "
            "}; "
            "$routing = New-VibeSkillRoutingFromLegacy "
            "-RouterSelectedSkill 'scikit-learn' "
            "-Recommendations @($recommendations) "
            "-StageAssistantHints @($hints) "
            "-SpecialistDispatch $dispatch; "
            "$routing | ConvertTo-Json -Depth 20 "
            "}"
        )

        self.assertEqual("simplified_skill_routing_v1", payload["schema_version"])
        candidate_ids = [item["skill_id"] for item in as_list(payload["candidates"])]
        selected_ids = [item["skill_id"] for item in as_list(payload["selected"])]
        rejected_ids = [item["skill_id"] for item in as_list(payload["rejected"])]
        self.assertEqual(["scikit-learn"], selected_ids)
        self.assertIn("scikit-learn", candidate_ids)
        self.assertIn("plotly", candidate_ids)
        self.assertIn("matplotlib", candidate_ids)
        self.assertIn("plotly", rejected_ids)
        self.assertIn("matplotlib", rejected_ids)
        selected = as_list(payload["selected"])[0]
        self.assertEqual("in_execution", selected["dispatch_phase"])
        self.assertEqual("model training", selected["reason"])

    def test_selected_skill_ids_prefer_skill_routing_over_legacy_dispatch(self) -> None:
        payload = run_ps_json(
            "& { "
            f". {ps_quote(str(RUNTIME_COMMON))}; "
            f". {ps_quote(str(SKILL_ROUTING_COMMON))}; "
            "$packet = [pscustomobject]@{ "
            "skill_routing = [pscustomobject]@{ selected = @([pscustomobject]@{ skill_id = 'new-authority' }) }; "
            "specialist_dispatch = [pscustomobject]@{ approved_dispatch = @([pscustomobject]@{ skill_id = 'legacy-only' }) } "
            "}; "
            "$ids = Get-VibeSkillRoutingSelectedSkillIds -RuntimeInputPacket $packet; "
            "[pscustomobject]@{ selected_skill_ids = $ids } | ConvertTo-Json -Depth 20 "
            "}"
        )

        self.assertEqual(["new-authority"], as_list(payload["selected_skill_ids"]))

    def test_selected_skill_ids_ignore_old_dispatch_when_skill_routing_is_absent(self) -> None:
        payload = run_ps_json(
            "& { "
            f". {ps_quote(str(RUNTIME_COMMON))}; "
            f". {ps_quote(str(SKILL_ROUTING_COMMON))}; "
            "$packet = [pscustomobject]@{ "
            "specialist_dispatch = [pscustomobject]@{ approved_dispatch = @([pscustomobject]@{ skill_id = 'legacy-skill' }) } "
            "}; "
            "$ids = Get-VibeSkillRoutingSelectedSkillIds -RuntimeInputPacket $packet; "
            "[pscustomobject]@{ selected_skill_ids = $ids } | ConvertTo-Json -Depth 20 "
            "}"
        )

        self.assertEqual([], as_list(payload["selected_skill_ids"]))

    def test_freeze_emits_skill_routing_with_selected_skills(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available")
        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir) / "artifacts"
            completed = subprocess.run(
                [
                    shell,
                    "-NoLogo",
                    "-NoProfile",
                    "-File",
                    str(FREEZE_SCRIPT),
                    "-Task",
                    "Build a scikit-learn tabular classification baseline and compare cross-validation metrics.",
                    "-Mode",
                    "interactive_governed",
                    "-RunId",
                    "pytest-simplified-skill-routing-freeze",
                    "-ArtifactRoot",
                    str(artifact_root),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            self.assertIn("packet_path", completed.stdout)
            packet_path = next(artifact_root.rglob("runtime-input-packet.json"))
            packet = json.loads(packet_path.read_text(encoding="utf-8"))

        routing = packet["skill_routing"]
        selected_ids = [item["skill_id"] for item in as_list(routing["selected"])]
        self.assertIn("scikit-learn", selected_ids)
        self.assertGreaterEqual(len(as_list(routing["candidates"])), len(selected_ids))
        for selected in as_list(routing["selected"]):
            self.assertIn("skill_id", selected)
            self.assertIn("task_slice", selected)
            self.assertIn("skill_md_path", selected)

    def test_new_freeze_packet_omits_old_routing_compatibility_fields(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available")
        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir) / "artifacts"
            subprocess.run(
                [
                    shell,
                    "-NoLogo",
                    "-NoProfile",
                    "-File",
                    str(FREEZE_SCRIPT),
                    "-Task",
                    "Use biopython to parse FASTA and summarize sequence lengths.",
                    "-Mode",
                    "interactive_governed",
                    "-RunId",
                    "pytest-skill-routing-legacy-isolation",
                    "-ArtifactRoot",
                    str(artifact_root),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            packet_path = next(artifact_root.rglob("runtime-input-packet.json"))
            packet = json.loads(packet_path.read_text(encoding="utf-8"))

        self.assertIn("skill_routing", packet)
        self.assertIn("skill_usage", packet)
        self.assertNotIn("legacy_skill_routing", packet)
        self.assertNotIn("stage_assistant_hints", packet)
        self.assertNotIn("specialist_recommendations", packet)
        self.assertNotIn("specialist_dispatch", packet)
