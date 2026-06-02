from __future__ import annotations

import json
import pytest
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]


def _powershell_executable() -> str:
    for name in ("pwsh", "powershell"):
        resolved = shutil.which(name)
        if resolved:
            return resolved
    pytest.skip("PowerShell executable was not found on PATH.")


def _powershell_single_quoted_path(path: Path) -> str:
    return str(path).replace("'", "''")


def test_powershell_single_quoted_path_escapes_apostrophes():
    assert _powershell_single_quoted_path(Path(r"C:\Users\O'Brien\repo\file.ps1")) == r"C:\Users\O''Brien\repo\file.ps1"


def _run_projection(script_body: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp_dir:
        script_path = Path(tmp_dir) / "run-lock-projection.ps1"
        skill_routing_common = REPO_ROOT / "scripts" / "runtime" / "VibeSkillRouting.Common.ps1"
        runtime_common = REPO_ROOT / "scripts" / "runtime" / "VibeRuntime.Common.ps1"
        skill_routing_common_ps = _powershell_single_quoted_path(skill_routing_common)
        runtime_common_ps = _powershell_single_quoted_path(runtime_common)
        script_path.write_text(
            textwrap.dedent(
                f"""
                $ErrorActionPreference = 'Stop'
                Set-StrictMode -Version Latest
                . '{skill_routing_common_ps}'
                . '{runtime_common_ps}'
                {script_body}
                """
            ),
            encoding="utf-8",
        )
        completed = subprocess.run(
            [_powershell_executable(), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)],
            cwd=str(REPO_ROOT),
            text=True,
            capture_output=True,
            timeout=30,
        )
        assert completed.returncode == 0, completed.stderr + completed.stdout
        return json.loads(completed.stdout)


def test_previous_active_lock_unions_current_selected_skill():
    result = _run_projection(
        r"""
        $previous = [pscustomobject]@{
            skill_execution_lock = [pscustomobject]@{
                schema_version = 'v1'
                state = 'active'
                locked_skill_ids = @('latex-submission-pipeline', 'scientific-writing', 'scholarly-publishing')
                locked_dispatch = @(
                    [pscustomobject]@{ skill_id = 'latex-submission-pipeline'; task_slice = 'paper build' },
                    [pscustomobject]@{ skill_id = 'scientific-writing'; task_slice = 'scientific writing' },
                    [pscustomobject]@{ skill_id = 'scholarly-publishing'; task_slice = 'publishing package' }
                )
                resolution_required = $true
            }
        }
        $current = [pscustomobject]@{
            selected = @(
                [pscustomobject]@{ skill_id = 'latex-submission-pipeline'; task_slice = 'paper build current' },
                [pscustomobject]@{ skill_id = 'literature-review'; task_slice = 'literature verification' },
                [pscustomobject]@{ skill_id = 'scientific-writing'; task_slice = 'scientific writing current' },
                [pscustomobject]@{ skill_id = 'scholarly-publishing'; task_slice = 'publishing package current' }
            )
            candidates = @(
                [pscustomobject]@{ skill_id = 'candidate-only'; task_slice = 'candidate only' }
            )
            rejected = @(
                [pscustomobject]@{ skill_id = 'rejected-only'; task_slice = 'rejected only' }
            )
        }
        $lock = New-VibeSkillExecutionLockProjection `
            -PreviousRuntimeInputPacket $previous `
            -CurrentSkillRouting $current `
            -SourceRunId 'previous-run' `
            -Source 'approved_plan_reentry'
        $lock | ConvertTo-Json -Depth 20
        """
    )

    assert result["state"] == "active"
    assert result["locked_skill_ids"] == [
        "latex-submission-pipeline",
        "literature-review",
        "scientific-writing",
        "scholarly-publishing",
    ]
    assert "candidate-only" not in result["locked_skill_ids"]
    assert "rejected-only" not in result["locked_skill_ids"]


def test_host_approved_skills_do_not_replace_previous_or_current_obligations():
    result = _run_projection(
        r"""
        $previous = [pscustomobject]@{
            skill_execution_lock = [pscustomobject]@{
                schema_version = 'v1'
                state = 'active'
                locked_skill_ids = @('latex-submission-pipeline')
                locked_dispatch = @(
                    [pscustomobject]@{ skill_id = 'latex-submission-pipeline'; task_slice = 'previous paper build' }
                )
                resolution_required = $true
            }
        }
        $current = [pscustomobject]@{
            selected = @(
                [pscustomobject]@{ skill_id = 'literature-review'; task_slice = 'current literature review' }
            )
            candidates = @()
            rejected = @()
        }
        $hostDecision = [pscustomobject]@{
            approved_skill_ids = @('scientific-writing')
        }
        $lock = New-VibeSkillExecutionLockProjection `
            -PreviousRuntimeInputPacket $previous `
            -CurrentSkillRouting $current `
            -HostSpecialistDispatchDecision $hostDecision `
            -SourceRunId 'previous-run' `
            -Source 'approved_plan_reentry'
        $lock | ConvertTo-Json -Depth 20
        """
    )

    assert result["locked_skill_ids"] == [
        "literature-review",
        "scientific-writing",
        "latex-submission-pipeline",
    ]


def test_host_deferred_and_rejected_skills_are_excluded_from_execution_lock():
    result = _run_projection(
        r"""
        $previous = [pscustomobject]@{
            skill_execution_lock = [pscustomobject]@{
                schema_version = 'v1'
                state = 'active'
                locked_skill_ids = @('prior-reporting', 'rejected-prior')
                locked_dispatch = @(
                    [pscustomobject]@{ skill_id = 'prior-reporting'; task_slice = 'prior report' },
                    [pscustomobject]@{ skill_id = 'rejected-prior'; task_slice = 'rejected prior' }
                )
                resolution_required = $true
            }
        }
        $current = [pscustomobject]@{
            selected = @(
                [pscustomobject]@{ skill_id = 'keep-current'; task_slice = 'current selected' },
                [pscustomobject]@{ skill_id = 'deferred-current'; task_slice = 'deferred selected' }
            )
            candidates = @()
            rejected = @()
        }
        $hostDecision = [pscustomobject]@{
            approved_skill_ids = @('keep-approved', 'rejected-approved')
            deferred_skill_ids = @('deferred-current')
            rejected_skill_ids = @('rejected-prior', 'rejected-approved')
        }
        $lock = New-VibeSkillExecutionLockProjection `
            -PreviousRuntimeInputPacket $previous `
            -CurrentSkillRouting $current `
            -HostSpecialistDispatchDecision $hostDecision `
            -SourceRunId 'previous-run' `
            -Source 'approved_plan_reentry'
        $lock | ConvertTo-Json -Depth 20
        """
    )

    assert result["locked_skill_ids"] == [
        "keep-current",
        "keep-approved",
        "prior-reporting",
    ]


def test_explicit_zero_host_approval_does_not_rehydrate_previous_lock_without_current_selection():
    result = _run_projection(
        r"""
        $previous = [pscustomobject]@{
            skill_execution_lock = [pscustomobject]@{
                schema_version = 'v1'
                state = 'active'
                locked_skill_ids = @('literature-review')
                locked_dispatch = @(
                    [pscustomobject]@{ skill_id = 'literature-review'; task_slice = 'previous literature review' }
                )
                resolution_required = $true
            }
        }
        $current = [pscustomobject]@{
            selected = @()
            candidates = @()
            rejected = @()
        }
        $hostDecision = [pscustomobject]@{
            approved_skill_ids = @()
        }
        $lock = New-VibeSkillExecutionLockProjection `
            -PreviousRuntimeInputPacket $previous `
            -CurrentSkillRouting $current `
            -HostSpecialistDispatchDecision $hostDecision `
            -SourceRunId 'previous-run' `
            -Source 'approved_plan_reentry'
        $lock | ConvertTo-Json -Depth 20
        """
    )

    assert result["state"] == "inactive"
    assert result["locked_skill_ids"] == []
    assert result["locked_dispatch"] == []


def test_single_selected_skill_stays_single_locked_skill():
    result = _run_projection(
        r"""
        $current = [pscustomobject]@{
            selected = @(
                [pscustomobject]@{ skill_id = 'latex-submission-pipeline'; task_slice = 'single selected skill' }
            )
            candidates = @(
                [pscustomobject]@{ skill_id = 'candidate-only'; task_slice = 'candidate only' }
            )
            rejected = @()
        }
        $lock = New-VibeSkillExecutionLockProjection -CurrentSkillRouting $current
        $lock | ConvertTo-Json -Depth 20
        """
    )

    assert result["locked_skill_ids"] == ["latex-submission-pipeline"]


def test_previous_locked_skill_ids_without_dispatch_are_preserved():
    result = _run_projection(
        r"""
        $previous = [pscustomobject]@{
            skill_execution_lock = [pscustomobject]@{
                schema_version = 'v1'
                state = 'active'
                locked_skill_ids = @('literature-review')
                resolution_required = $true
            }
        }
        $current = [pscustomobject]@{
            selected = @()
            candidates = @()
            rejected = @()
        }
        $lock = New-VibeSkillExecutionLockProjection `
            -PreviousRuntimeInputPacket $previous `
            -CurrentSkillRouting $current `
            -SourceRunId 'previous-run' `
            -Source 'approved_plan_reentry'
        $lock | ConvertTo-Json -Depth 20
        """
    )

    assert result["locked_skill_ids"] == ["literature-review"]
    dispatch = result["locked_dispatch"][0]
    assert dispatch["skill_id"] == "literature-review"
    assert dispatch["lock_source"] == "previous_skill_execution_lock"
    assert dispatch["reconciliation_state"] == "inherited_not_currently_surfaced"


def test_lock_summary_derives_ids_from_locked_dispatch_when_id_list_missing():
    result = _run_projection(
        r"""
        $lock = [pscustomobject]@{
            schema_version = 'v1'
            state = 'active'
            locked_dispatch = @(
                [pscustomobject]@{ skill_id = 'scientific-writing' }
            )
            resolution_required = $true
        }
        $summary = New-VibeSkillExecutionLockSummaryProjection -SkillExecutionLock $lock
        $summary | ConvertTo-Json -Depth 20
        """
    )

    assert result["active"] is True
    assert result["locked_skill_count"] == 1
    assert result["locked_skill_ids"] == ["scientific-writing"]
