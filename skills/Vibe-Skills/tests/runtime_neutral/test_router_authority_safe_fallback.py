from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt


def selected(result: dict[str, object]) -> tuple[str, str]:
    selected_row = result.get("selected")
    assert isinstance(selected_row, dict), result
    return str(selected_row.get("pack_id") or ""), str(selected_row.get("skill") or "")


def test_debug_logs_api_failure_falls_back_to_systematic_debugging() -> None:
    result = route_prompt(
        prompt="根据错误日志排查翻译接口失败并给出解决方案，检查 runtime pipeline 和 API 请求",
        grade="XL",
        task_type="debug",
        repo_root=REPO_ROOT,
    )

    assert selected(result) == ("code-quality", "systematic-debugging")
    assert result["fallback_applied"] is False
    assert result["rejected_specialist_reasons"] == []
    assert result["pre_fallback_top"] == {"pack_id": "code-quality", "skill": "systematic-debugging"}


def test_explicit_latex_submission_build_stays_in_scholarly_publishing() -> None:
    result = route_prompt(
        prompt="配置 latexmk chktex latexindent 编译 LaTeX manuscript PDF 并打包 submission zip",
        grade="XL",
        task_type="coding",
        repo_root=REPO_ROOT,
    )

    assert selected(result) == ("scholarly-publishing-workflow", "latex-submission-pipeline")
    assert result["fallback_applied"] is False


def test_existing_pdf_extraction_stays_in_docs_media() -> None:
    result = route_prompt(
        prompt="读取 PDF 并提取正文",
        grade="XL",
        task_type="coding",
        repo_root=REPO_ROOT,
    )

    assert selected(result) == ("docs-media", "pdf")


def test_github_actions_logs_route_to_integration_devops() -> None:
    result = route_prompt(
        prompt="查看 github actions 日志并修复 CI pipeline failed",
        grade="L",
        task_type="debug",
        repo_root=REPO_ROOT,
    )

    assert selected(result) == ("integration-devops", "gh-fix-ci")


def test_sentry_alert_routes_to_integration_devops() -> None:
    result = route_prompt(
        prompt="排查 sentry production error 和线上告警",
        grade="L",
        task_type="debug",
        repo_root=REPO_ROOT,
    )

    assert selected(result) == ("integration-devops", "sentry")
