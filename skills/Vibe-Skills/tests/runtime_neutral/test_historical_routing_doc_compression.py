from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config" / "routing-terminology-hard-cleanup.json"
HARD_SCAN = REPO_ROOT / "scripts" / "verify" / "vibe-routing-terminology-hard-cleanup-scan.ps1"
SUMMARY_DOC = REPO_ROOT / "docs" / "governance" / "historical-routing-terminology.md"
CURRENT_CONTRACT = "docs/governance/current-routing-contract.md"
CURRENT_FIELD_CONTRACT = "docs/governance/current-runtime-field-contract.md"
CURRENT_MODEL = "skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage"
COMPRESSED_DOCS = [
    REPO_ROOT / "docs" / "governance" / "binary-skill-usage-routing-2026-04-28.md",
    REPO_ROOT / "docs" / "governance" / "simplified-skill-routing-2026-04-29.md",
    REPO_ROOT / "docs" / "governance" / "specialist-dispatch-governance.md",
    REPO_ROOT / "docs" / "governance" / "terminology-governance.md",
]


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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class HistoricalRoutingDocCompressionTests(unittest.TestCase):
    def test_config_declares_root_based_historical_inventory(self) -> None:
        config = json.loads(read(CONFIG_PATH))
        self.assertEqual(
            [
                "docs/governance",
                "docs/requirements",
                "docs/superpowers/plans",
                "docs/superpowers/specs",
            ],
            config["historical_doc_roots"],
        )
        self.assertIn("historical_doc_exemptions", config)
        self.assertIn(CURRENT_CONTRACT, config["historical_doc_exemptions"])
        self.assertIn(CURRENT_FIELD_CONTRACT, config["historical_doc_exemptions"])

    def test_hard_scan_reports_root_based_historical_inventory(self) -> None:
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
        summary = payload["summary"]

        self.assertIn("historical_doc_retired_term_file_count", summary)
        self.assertIn("historical_doc_marked_retired_term_count", summary)
        self.assertIn("historical_doc_unmarked_retired_term_count", summary)
        self.assertGreater(int(summary["historical_doc_retired_term_file_count"]), 50)
        self.assertGreater(int(summary["historical_doc_marked_retired_term_count"]), 50)
        self.assertGreaterEqual(int(summary["historical_doc_unmarked_retired_term_count"]), 0)
        self.assertEqual(0, int(summary["fail_count"]))
        self.assertEqual([], payload["findings"])

    def test_historical_summary_redirects_to_current_contract(self) -> None:
        self.assertTrue(SUMMARY_DOC.exists(), "historical routing terminology summary must exist")
        text = read(SUMMARY_DOC)
        self.assertIn("Historical / Retired Note", text)
        self.assertIn(CURRENT_MODEL, text)
        self.assertIn(CURRENT_CONTRACT, text)
        self.assertIn(CURRENT_FIELD_CONTRACT, text)
        for retired_term in [
            "primary skill",
            "secondary skill",
            "route owner",
            "stage assistant",
            "consultation",
            "specialist dispatch",
        ]:
            self.assertIn(retired_term, text.lower())

    def test_compressed_legacy_governance_docs_are_short_redirects(self) -> None:
        for path in COMPRESSED_DOCS:
            with self.subTest(path=path):
                text = read(path)
                lines = [line for line in text.splitlines() if line.strip()]
                self.assertLessEqual(len(lines), 70)
                self.assertIn("Historical / Retired Note", text)
                self.assertIn(CURRENT_MODEL, text)
                self.assertIn(CURRENT_CONTRACT, text)
                self.assertIn("docs/governance/historical-routing-terminology.md", text)


if __name__ == "__main__":
    unittest.main()
