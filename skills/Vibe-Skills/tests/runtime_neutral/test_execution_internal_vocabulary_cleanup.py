from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
INVOKE_PLAN_EXECUTE = REPO_ROOT / "scripts" / "runtime" / "Invoke-PlanExecute.ps1"
VIBE_EXECUTION_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeExecution.Common.ps1"
DELEGATED_LANE_UNIT = REPO_ROOT / "scripts" / "runtime" / "Invoke-DelegatedLaneUnit.ps1"
DELIVERY_ACCEPTANCE = (
    REPO_ROOT
    / "packages"
    / "verification-core"
    / "src"
    / "vgo_verify"
    / "runtime_delivery_acceptance_runtime.py"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class ExecutionInternalVocabularyCleanupTests(unittest.TestCase):
    def test_plan_execute_declares_current_execution_accounting_fields(self) -> None:
        text = read(INVOKE_PLAN_EXECUTE)
        for field in [
            "skill_execution_unit_count",
            "selected_skill_execution_count",
            "selected_skill_execution",
            "frozen_selected_skill_execution_count",
            "frozen_selected_skill_execution",
            "auto_selected_skill_execution_count",
            "auto_selected_skill_execution",
            "blocked_skill_execution_unit_count",
            "blocked_skill_execution_units",
            "degraded_skill_execution_unit_count",
            "degraded_skill_execution_units",
            "execution_skill_outcome_count",
            "execution_skill_outcomes",
            "skill_execution_resolution_path",
        ]:
            self.assertIn(field, text)

    def test_current_runtime_files_do_not_emit_specialist_dispatch_lane_kind(self) -> None:
        for path in [INVOKE_PLAN_EXECUTE, VIBE_EXECUTION_COMMON, DELEGATED_LANE_UNIT]:
            text = read(path)
            self.assertNotIn("lane_kind = 'specialist_dispatch'", text, path)
            self.assertNotIn("'specialist_dispatch' {", text, path)
            self.assertNotIn("-eq 'specialist_dispatch'", text, path)
            self.assertNotIn("kind = 'specialist_dispatch'", text, path)

    def test_current_plan_execute_outputs_do_not_write_old_execution_field_names(self) -> None:
        text = read(INVOKE_PLAN_EXECUTE)
        forbidden_assignment_patterns = [
            r"^\s*specialist_dispatch_unit_count\s*=",
            r"^\s*specialist_dispatch_outcome_count\s*=",
            r"^\s*specialist_dispatch_outcomes\s*=",
            r"^\s*specialist_dispatch_resolution_path\s*=",
            r"^\s*approved_dispatch_count\s*=",
            r"^\s*approved_dispatch\s*=",
            r"^\s*frozen_approved_dispatch_count\s*=",
            r"^\s*frozen_approved_dispatch\s*=",
            r"^\s*auto_approved_dispatch_count\s*=",
            r"^\s*auto_approved_dispatch\s*=",
            r"^\s*blocked_specialist_unit_count\s*=",
            r"^\s*blocked_specialist_units\s*=",
            r"^\s*degraded_specialist_unit_count\s*=",
            r"^\s*degraded_specialist_units\s*=",
        ]
        for pattern in forbidden_assignment_patterns:
            self.assertIsNone(re.search(pattern, text, flags=re.MULTILINE), pattern)

    def test_delivery_acceptance_reads_current_execution_accounting_first(self) -> None:
        text = read(DELIVERY_ACCEPTANCE)
        self.assertIn('specialist_accounting.get("selected_skill_execution")', text)
        self.assertIn('specialist_accounting.get("selected_skill_execution_count")', text)
        self.assertIn('specialist_accounting.get("direct_routed_skill_execution_units")', text)
        self.assertIn('specialist_accounting.get("blocked_skill_execution_units")', text)
        self.assertIn('specialist_accounting.get("degraded_skill_execution_units")', text)
        self.assertNotIn('runtime_input_packet.get("specialist_dispatch")', text)
        self.assertNotIn('legacy_skill_routing.get("specialist_dispatch")', text)


if __name__ == "__main__":
    unittest.main()
