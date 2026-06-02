from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
ROUTE_SCRIPT = REPO_ROOT / "scripts" / "router" / "resolve-pack-route.ps1"
HELPER_SCRIPT = REPO_ROOT / "scripts" / "common" / "vibe-governance-helpers.ps1"
POLICY_PATH = REPO_ROOT / "config" / "skill-promotion-policy.json"
ML_PROMPT = (
    "Please use scikit-learn to prototype a tabular classification baseline, "
    "run feature selection, and compare cross-validation metrics."
)
SAFE_EDIT_PROMPT = "Remove dead imports and replace a mock in tests."
DESTRUCTIVE_PROMPT = (
    "Delete the old generated artifacts, remove the obsolete branch, "
    "and overwrite the install settings to reset the environment."
)
WINDOWS_DESTRUCTIVE_PROMPT = r"delete C:\tmp\build"
POWERSHELL_SUBPROCESS_TIMEOUT_SECONDS = 120


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


def run_route(prompt: str, *, repo_root: Path = REPO_ROOT) -> dict[str, object]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available in PATH")

    route_script = repo_root / "scripts" / "router" / "resolve-pack-route.ps1"
    completed = subprocess.run(
        [
            shell,
            "-NoLogo",
            "-NoProfile",
            "-File",
            str(route_script),
            "-Prompt",
            prompt,
            "-Grade",
            "M",
            "-TaskType",
            "coding",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=POWERSHELL_SUBPROCESS_TIMEOUT_SECONDS,
        check=True,
    )
    return json.loads(completed.stdout)


def run_helper_json(script_body: str) -> dict[str, object]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available in PATH")

    completed = subprocess.run(
        [
            shell,
            "-NoLogo",
            "-NoProfile",
            "-Command",
            script_body,
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=POWERSHELL_SUBPROCESS_TIMEOUT_SECONDS,
        check=True,
    )
    return json.loads(completed.stdout)


def as_list(value: object) -> list[object]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def get_selected_option(route: dict[str, object]) -> dict[str, object]:
    confirm_ui = route["confirm_ui"]
    selected_skill = confirm_ui.get("selected_skill")
    if not selected_skill and confirm_ui.get("selected"):
        selected_skill = confirm_ui["selected"].get("skill")
    match = next((item for item in confirm_ui["options"] if item["skill"] == selected_skill), None)
    if match is None:
        available = [item.get("skill") for item in confirm_ui["options"]]
        raise AssertionError(f"No option with skill={selected_skill!r} found in confirm_ui options: {available!r}")
    return match


def test_get_selected_option_fails_clearly_when_selected_skill_is_missing() -> None:
    route = {
        "confirm_ui": {
            "selected_skill": "missing-skill",
            "options": [{"skill": "available-skill"}],
        }
    }

    with pytest.raises(AssertionError, match="No option with skill='missing-skill'"):
        get_selected_option(route)


def copy_repo_fixture(target_root: Path) -> Path:
    fixture_root = target_root / "repo-copy"
    shutil.copytree(
        REPO_ROOT,
        fixture_root,
        ignore=shutil.ignore_patterns(".git", ".worktrees", "outputs", "__pycache__", ".pytest_cache"),
    )
    return fixture_root


class SkillPromotionRouterMetadataTests(unittest.TestCase):
    def test_non_destructive_ml_prompt_exposes_auto_dispatch_promotion_metadata(self) -> None:
        route = run_route(ML_PROMPT)

        selected = route["selected"]
        self.assertEqual("data-ml", selected["pack_id"])
        self.assertEqual("scikit-learn", selected["skill"])
        self.assertTrue(selected["promotion_eligible"])
        self.assertFalse(selected["destructive"])
        self.assertEqual([], as_list(selected["destructive_reason_codes"]))
        self.assertFalse(selected["snapshot_required"])
        self.assertFalse(selected["rollback_possible"])
        self.assertTrue(selected["contract_complete"])
        self.assertEqual("auto_dispatch", selected["recommended_promotion_action"])

        option = get_selected_option(route)
        self.assertEqual("scikit-learn", option["skill"])
        self.assertTrue(option["promotion_eligible"])
        self.assertFalse(option["destructive"])
        self.assertTrue(option["contract_complete"])
        self.assertEqual("auto_dispatch", option["recommended_promotion_action"])

    def test_destructive_prompt_exposes_confirmation_gated_promotion_metadata(self) -> None:
        route = run_route(DESTRUCTIVE_PROMPT)

        selected = route["selected"]
        self.assertIsInstance(selected["skill"], str)
        self.assertTrue(selected["skill"].strip())
        self.assertFalse(selected["promotion_eligible"])
        self.assertTrue(selected["destructive"])
        self.assertTrue(selected["snapshot_required"])
        self.assertTrue(selected["rollback_possible"])
        self.assertTrue(selected["contract_complete"])
        self.assertEqual("require_confirmation", selected["recommended_promotion_action"])
        self.assertGreaterEqual(len(as_list(selected["destructive_reason_codes"])), 1)

        option = get_selected_option(route)
        self.assertEqual(selected["skill"], option["skill"])
        self.assertFalse(option["promotion_eligible"])
        self.assertTrue(option["destructive"])
        self.assertTrue(option["snapshot_required"])
        self.assertEqual("require_confirmation", option["recommended_promotion_action"])

    def test_routine_edit_prompt_is_not_classified_as_destructive(self) -> None:
        assessment = run_helper_json(
            (
                "& { "
                f". '{HELPER_SCRIPT}'; "
                f"$result = Get-VgoDestructiveIntentAssessment -Prompt '{SAFE_EDIT_PROMPT}'; "
                "$result | ConvertTo-Json -Depth 20 }"
            )
        )

        self.assertFalse(assessment["destructive"])
        self.assertEqual([], as_list(assessment["destructive_reason_codes"]))
        self.assertFalse(assessment["rollback_possible"])
        self.assertFalse(assessment["snapshot_required"])

    def test_windows_style_path_prompt_is_classified_as_destructive(self) -> None:
        assessment = run_helper_json(
            (
                "& { "
                f". '{HELPER_SCRIPT}'; "
                f"$policy = Get-Content -LiteralPath '{POLICY_PATH}' -Raw -Encoding UTF8 | ConvertFrom-Json; "
                f"$result = Get-VgoDestructiveIntentAssessment -Prompt '{WINDOWS_DESTRUCTIVE_PROMPT}' -PromotionPolicy $policy; "
                "$result | ConvertTo-Json -Depth 20 }"
            )
        )

        self.assertTrue(assessment["destructive"])
        self.assertGreaterEqual(len(as_list(assessment["destructive_reason_codes"])), 1)
        self.assertTrue(assessment["rollback_possible"])
        self.assertTrue(assessment["snapshot_required"])

    def test_blank_contract_entries_do_not_count_as_complete(self) -> None:
        completeness = run_helper_json(
            (
                "& { "
                f". '{HELPER_SCRIPT}'; "
                "$result = Get-VgoSkillContractCompleteness "
                "-SkillMdPath '/tmp/skill.md' "
                "-Description 'desc' "
                "-RequiredInputs @('   ') "
                "-ExpectedOutputs @('') "
                "-VerificationExpectation 'verify'; "
                "$result | ConvertTo-Json -Depth 20 }"
            )
        )

        self.assertFalse(completeness["complete"])
        self.assertIn("required_inputs", as_list(completeness["missing_fields"]))
        self.assertIn("expected_outputs", as_list(completeness["missing_fields"]))

    def test_route_fails_closed_when_skill_promotion_policy_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo_copy = copy_repo_fixture(Path(tempdir))
            (repo_copy / "config" / "skill-promotion-policy.json").write_text(
                "{ invalid json",
                encoding="utf-8",
            )
            with self.assertRaises(subprocess.CalledProcessError):
                run_route(ML_PROMPT, repo_root=repo_copy)
