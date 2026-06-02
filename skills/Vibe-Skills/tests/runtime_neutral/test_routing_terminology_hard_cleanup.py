from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_DOC = REPO_ROOT / "docs" / "governance" / "current-runtime-field-contract.md"
HARD_SCAN = REPO_ROOT / "scripts" / "verify" / "vibe-routing-terminology-hard-cleanup-scan.ps1"


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


class RoutingTerminologyHardCleanupTests(unittest.TestCase):
    def test_current_runtime_field_contract_defines_allowed_layers(self) -> None:
        self.assertTrue(CONTRACT_DOC.exists(), "current runtime field contract must exist")
        text = CONTRACT_DOC.read_text(encoding="utf-8")

        self.assertIn(
            "skill_candidates -> skill_routing.selected -> selected_skill_execution -> "
            "skill_usage.used / skill_usage.unused",
            text,
        )
        for required in [
            "## Routing Layer",
            "## Usage Layer",
            "## Execution Layer",
            "## Retired Layer",
            "`skill_routing.selected`",
            "`skill_usage.used`",
            "`skill_usage.unused`",
            "`skill_usage.evidence`",
            "`selected_skill_execution`",
            "`skill_execution_units`",
            "`execution_skill_outcomes`",
        ]:
            self.assertIn(required, text)

        current_section = text.split("## Retired Layer", 1)[0].lower()
        for forbidden in [
            "primary skill",
            "secondary skill",
            "route owner",
            "consultation expert",
            "auxiliary expert",
            "stage assistant",
        ]:
            self.assertNotIn(forbidden, current_section)

    def test_hard_cleanup_scan_reports_json(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available")

        completed = subprocess.run(
            [shell, "-NoLogo", "-NoProfile", "-File", str(HARD_SCAN), "-Json"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        payload = json.loads(completed.stdout)
        self.assertIn("summary", payload)
        self.assertIn("fail_count", payload["summary"])
        self.assertIn("allowed_negative_count", payload["summary"])
        self.assertIn("allowed_historical_count", payload["summary"])
        self.assertIn("review_count", payload["summary"])
        self.assertIn("findings", payload)
        self.assertIn("failures", payload)
        self.assertIn("allowed_negative", payload)
        self.assertIn("allowed_historical", payload)
        self.assertIn("review", payload)
        self.assertEqual("pass", payload["status"])
        self.assertEqual(0, int(payload["summary"]["fail_count"]))
        self.assertGreater(int(payload["summary"]["allowed_negative_count"]), 0)
        self.assertGreater(int(payload["summary"]["allowed_historical_count"]), 50)
        self.assertEqual(0, int(payload["summary"]["review_count"]))
        self.assertEqual([], payload["failures"])
        self.assertEqual([], payload["review"])

    def test_policy_defines_current_surface_budget_layers(self) -> None:
        policy_path = REPO_ROOT / "config" / "routing-terminology-hard-cleanup.json"
        payload = json.loads(policy_path.read_text(encoding="utf-8"))

        self.assertIn("current_surface_roots", payload)
        self.assertIn("historical_surface_roots", payload)
        self.assertIn("allowed_negative_files", payload)
        self.assertIn("compatibility_review_files", payload)
        self.assertIn("retired_positive_terms", payload)

        current_roots = set(payload["current_surface_roots"])
        self.assertIn("packages/verification-core/src/vgo_verify", current_roots)
        self.assertIn("scripts/verify", current_roots)
        self.assertIn("tests/runtime_neutral", current_roots)
        self.assertIn("docs/governance/current-routing-contract.md", current_roots)
        self.assertIn("docs/governance/current-runtime-field-contract.md", current_roots)
        self.assertIn("docs/governance/terminology-governance.md", current_roots)

        historical_roots = set(payload["historical_surface_roots"])
        self.assertIn("docs/superpowers/plans", historical_roots)
        self.assertIn("docs/superpowers/specs", historical_roots)

        retired_terms = set(payload["retired_positive_terms"])
        for term in [
            "route_authority_candidates",
            "stage_assistant_candidates",
            "route_authority_eligible",
            "legacy_role",
            "_legacy_role",
            "_legacy_stage_assistant_candidates",
            "route authority",
            "stage assistant",
            "route owner",
        ]:
            self.assertIn(term, retired_terms)


if __name__ == "__main__":
    unittest.main()
