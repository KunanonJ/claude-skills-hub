from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SRC = REPO_ROOT / "packages" / "runtime-core" / "src"
if str(RUNTIME_SRC) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SRC))

from vgo_runtime.router_contract_runtime import _public_admitted_candidates, _public_pack_row, route_prompt  # noqa: E402


POLICY = REPO_ROOT / "config" / "current-routing-debt-erasure.json"


ROUTE_CASES = [
    (
        "帮我做科研绘图，产出期刊级 figure，多面板、颜色无障碍、矢量导出",
        "L",
        "research",
        "science-figures-visualization",
        "scientific-visualization",
    ),
    (
        "请用 LaTeX 构建论文 PDF，检查 bibtex 引用、模板和 submission checklist",
        "L",
        "coding",
        "scholarly-publishing-workflow",
        "latex-submission-pipeline",
    ),
    (
        "机器学习 data preprocessing pipeline：清洗数据、feature encoding、standardize data、validate input data",
        "L",
        "coding",
        "data-ml",
        "preprocessing-data-with-automated-pipelines",
    ),
    (
        "request code review before merge：请整理提交评审材料，准备 code review request",
        "L",
        "review",
        "code-quality",
        "requesting-code-review",
    ),
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


def assert_public_route_output_shape(testcase: unittest.TestCase, result: dict[str, Any]) -> None:
    retired_fields = set(json.loads(POLICY.read_text(encoding="utf-8"))["high_risk_retired_fields"])
    testcase.assertIn("ranked", result)
    testcase.assertIsInstance(result["ranked"], list)
    for pack_row in result["ranked"]:
        testcase.assertIsInstance(pack_row, dict)
        for field in retired_fields:
            testcase.assertNotIn(field, pack_row, pack_row.get("pack_id"))
        custom_admission = pack_row.get("custom_admission")
        if isinstance(custom_admission, dict):
            for field in retired_fields:
                testcase.assertNotIn(field, custom_admission, pack_row.get("pack_id"))
        ranking = pack_row.get("candidate_ranking") or []
        testcase.assertIsInstance(ranking, list)
        for candidate_row in ranking:
            testcase.assertIsInstance(candidate_row, dict)
            for field in retired_fields:
                testcase.assertNotIn(field, candidate_row, candidate_row.get("skill"))


def run_powershell_old_manifest_candidate_probe(testcase: unittest.TestCase) -> list[str]:
    shell = resolve_powershell()
    if shell is None:
        testcase.skipTest("PowerShell executable not available")

    module_path = REPO_ROOT / "scripts" / "router" / "modules" / "41-candidate-selection.ps1"
    retired_candidate_fields = [
        field
        for field in json.loads(POLICY.read_text(encoding="utf-8"))["high_risk_retired_fields"]
        if field.endswith("_candidates")
    ]
    retired_member_writes = " ".join(
        "$pack | Add-Member -NotePropertyName '{field}' -NotePropertyValue @('primary','shared'); ".format(
            field=field.replace("'", "''"),
        )
        for field in retired_candidate_fields
    )
    script = (
        f". '{module_path}'; "
        "$pack = [pscustomobject]@{}; "
        f"{retired_member_writes}"
        "$result = @(Get-PackSkillCandidates -Pack $pack); "
        "$result | ConvertTo-Json -Depth 5"
    )
    completed = subprocess.run(
        [shell, "-NoLogo", "-NoProfile", "-Command", script],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    output = completed.stdout.strip()
    if not output:
        return []
    payload = json.loads(output)
    return payload if isinstance(payload, list) else [payload]


class RuntimeRouteOutputShapeTests(unittest.TestCase):
    def test_runtime_route_output_exposes_fallback_audit_fields(self) -> None:
        result = route_prompt(
            prompt="根据错误日志排查翻译接口失败并给出解决方案",
            grade="XL",
            task_type="debug",
            repo_root=REPO_ROOT,
        )

        self.assertIn("fallback_applied", result)
        self.assertIn("rejected_specialist_reasons", result)
        self.assertIn("pre_fallback_top", result)
        self.assertIn("authority", result["selected"])

    def test_powershell_pack_skill_candidates_ignore_retired_role_fields(self) -> None:
        self.assertEqual([], run_powershell_old_manifest_candidate_probe(self))

    def test_python_public_route_helpers_scrub_retired_custom_metadata(self) -> None:
        retired_key = "route_authority" + "_eligible"
        public_pack = _public_pack_row(
            {
                "pack_id": "custom-pack",
                "_route_usable": True,
                "custom_admission": {
                    "_route_usable": True,
                    retired_key: True,
                    "trigger_mode": "auto",
                },
                "candidate_ranking": [],
            }
        )

        self.assertNotIn("_route_usable", public_pack)
        self.assertNotIn("_route_usable", public_pack["custom_admission"])
        self.assertNotIn(retired_key, public_pack["custom_admission"])

        admitted = _public_admitted_candidates(
            [
                {
                    "skill_id": "custom-skill",
                    "_route_usable": True,
                    retired_key: True,
                    "pack": {
                        "pack_id": "custom-pack",
                        "_route_usable": True,
                        retired_key: True,
                        "custom_admission": {
                            "_route_usable": True,
                            retired_key: True,
                        },
                    },
                }
            ]
        )[0]

        self.assertNotIn("_route_usable", admitted)
        self.assertNotIn(retired_key, admitted)
        self.assertNotIn("_route_usable", admitted["pack"])
        self.assertNotIn(retired_key, admitted["pack"])
        self.assertNotIn("_route_usable", admitted["pack"]["custom_admission"])
        self.assertNotIn(retired_key, admitted["pack"]["custom_admission"])

    def test_python_route_output_has_only_current_skill_ranking_fields(self) -> None:
        for prompt, grade, task_type, expected_pack, expected_skill in ROUTE_CASES:
            with self.subTest(expected_pack=expected_pack, expected_skill=expected_skill):
                result = route_prompt(prompt=prompt, grade=grade, task_type=task_type, repo_root=REPO_ROOT)

                self.assertEqual(expected_pack, result["selected"]["pack_id"])
                self.assertEqual(expected_skill, result["selected"]["skill"])
                assert_public_route_output_shape(self, result)

    def test_powershell_route_output_has_only_current_skill_ranking_fields(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available")

        script_path = REPO_ROOT / "scripts" / "router" / "resolve-pack-route.ps1"
        for prompt, grade, task_type, expected_pack, expected_skill in ROUTE_CASES:
            with self.subTest(expected_pack=expected_pack, expected_skill=expected_skill):
                completed = subprocess.run(
                    [
                        shell,
                        "-NoLogo",
                        "-NoProfile",
                        "-File",
                        str(script_path),
                        "-Prompt",
                        prompt,
                        "-Grade",
                        grade,
                        "-TaskType",
                        task_type,
                    ],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    check=True,
                    env={**os.environ, "VGO_DISABLE_NATIVE_SPECIALIST_EXECUTION": "1"},
                )
                result = json.loads(completed.stdout)

                self.assertEqual(expected_pack, result["selected"]["pack_id"])
                self.assertEqual(expected_skill, result["selected"]["skill"])
                assert_public_route_output_shape(self, result)


if __name__ == "__main__":
    unittest.main()
