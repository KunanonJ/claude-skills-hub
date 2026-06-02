from __future__ import annotations

import json
from pathlib import Path

from vgo_verify.runtime_delivery_acceptance_runtime import (
    _evaluate_selected_lock_reconciliation,
    _evaluate_specialist_lock_resolution,
    evaluate_delivery_acceptance,
)


def test_selected_lock_reconciliation_passes_when_selected_and_approved_are_locked():
    runtime_packet = {
        "skill_routing": {
            "selected": [
                {"skill_id": "latex-submission-pipeline"},
                {"skill_id": "literature-review"},
            ],
            "candidates": [
                {"skill_id": "candidate-only"},
            ],
        },
        "specialist_decision": {
            "approved_dispatch_skill_ids": [
                "latex-submission-pipeline",
                "literature-review",
            ]
        },
    }
    lock = {
        "state": "active",
        "locked_skill_ids": [
            "latex-submission-pipeline",
            "literature-review",
        ],
    }

    state, notes, lists = _evaluate_selected_lock_reconciliation(runtime_packet, lock)

    assert state == "passing"
    assert notes == ["Selected/approved specialist execution obligations are locked."]
    assert lists["missing"] == []
    assert lists["required"] == ["latex-submission-pipeline", "literature-review"]
    assert "candidate-only" not in lists["required"]


def test_selected_lock_reconciliation_requires_manual_review_when_selected_skill_missing_from_lock():
    runtime_packet = {
        "skill_routing": {
            "selected": [
                {"skill_id": "latex-submission-pipeline"},
                {"skill_id": "literature-review"},
                {"skill_id": "scientific-writing"},
            ],
        },
        "specialist_decision": {
            "approved_dispatch_skill_ids": [
                "latex-submission-pipeline",
                "literature-review",
                "scientific-writing",
            ]
        },
    }
    lock = {
        "state": "active",
        "locked_skill_ids": [
            "latex-submission-pipeline",
            "scientific-writing",
        ],
    }

    state, notes, lists = _evaluate_selected_lock_reconciliation(runtime_packet, lock)

    assert state == "manual_review_required"
    assert lists["missing"] == ["literature-review"]
    assert "literature-review" in notes[0]


def test_selected_lock_reconciliation_does_not_require_candidates_or_advice():
    runtime_packet = {
        "skill_routing": {
            "selected": [
                {"skill_id": "latex-submission-pipeline"},
            ],
            "candidates": [
                {"skill_id": "ml-pipeline-workflow"},
                {"skill_id": "literature-review"},
            ],
            "rejected": [
                {"skill_id": "rejected-only"},
            ],
        },
        "ml_lifecycle_advice": {
            "task_applicable": True,
            "scope_applicable": False,
            "enforcement": "none",
            "reason": "outside_scope",
        },
        "specialist_decision": {
            "approved_dispatch_skill_ids": [
                "latex-submission-pipeline",
            ]
        },
    }
    lock = {
        "state": "active",
        "locked_skill_ids": [
            "latex-submission-pipeline",
        ],
    }

    state, _notes, lists = _evaluate_selected_lock_reconciliation(runtime_packet, lock)

    assert state == "passing"
    assert lists["required"] == ["latex-submission-pipeline"]
    assert "ml-pipeline-workflow" not in lists["required"]
    assert "literature-review" not in lists["required"]
    assert "rejected-only" not in lists["required"]


def test_selected_lock_reconciliation_passes_when_no_active_lock_is_present():
    runtime_packet = {
        "specialist_decision": {
            "approved_dispatch_skill_ids": [
                "systematic-debugging",
            ]
        },
    }
    lock: dict[str, object] = {}

    state, notes, lists = _evaluate_selected_lock_reconciliation(runtime_packet, lock)

    assert state == "passing"
    assert notes == ["No active specialist execution lock was present."]
    assert lists["required"] == ["systematic-debugging"]
    assert lists["locked"] == []
    assert lists["missing"] == []


def test_specialist_lock_resolution_ignores_stale_resolution_buckets():
    skill_execution_lock = {
        "state": "active",
        "locked_skill_ids": ["literature-review"],
    }
    specialist_lock_resolution = {
        "executed_skill_ids": ["literature-review"],
        "not_applicable_skill_ids": [],
        "deferred_skill_ids": ["old-deferred-skill"],
        "failed_skill_ids": ["old-failed-skill"],
        "unresolved_skill_ids": ["old-unresolved-skill"],
    }

    state, notes, lists = _evaluate_specialist_lock_resolution(
        skill_execution_lock,
        specialist_lock_resolution,
    )

    assert state == "passing"
    assert notes == ["All locked specialist execution obligations were resolved."]
    assert lists["executed"] == ["literature-review"]
    assert lists["deferred"] == []
    assert lists["failed"] == []
    assert lists["unresolved"] == []


def test_specialist_lock_resolution_does_not_readd_deferred_or_phantom_unresolved_skills():
    skill_execution_lock = {
        "state": "active",
        "locked_skill_ids": ["literature-review", "scientific-writing"],
    }
    specialist_lock_resolution = {
        "executed_skill_ids": ["scientific-writing"],
        "not_applicable_skill_ids": [],
        "deferred_skill_ids": ["literature-review"],
        "failed_skill_ids": [],
        "unresolved_skill_ids": ["literature-review", "phantom-skill"],
    }

    state, notes, lists = _evaluate_specialist_lock_resolution(
        skill_execution_lock,
        specialist_lock_resolution,
    )

    assert state == "manual_review_required"
    assert notes == ["Locked specialist execution was deferred for: literature-review."]
    assert lists["deferred"] == ["literature-review"]
    assert lists["unresolved"] == []


def test_specialist_lock_resolution_uses_locked_dispatch_when_id_list_missing():
    skill_execution_lock = {
        "state": "active",
        "locked_dispatch": [
            {"skill_id": "literature-review"},
        ],
    }
    specialist_lock_resolution = {
        "executed_skill_ids": [],
        "not_applicable_skill_ids": [],
        "deferred_skill_ids": [],
        "failed_skill_ids": [],
        "unresolved_skill_ids": [],
    }

    state, notes, lists = _evaluate_specialist_lock_resolution(
        skill_execution_lock,
        specialist_lock_resolution,
    )

    assert state == "failing"
    assert lists["locked"] == ["literature-review"]
    assert lists["unresolved"] == ["literature-review"]
    assert "literature-review" in notes[0]


def test_selected_lock_reconciliation_uses_locked_dispatch_when_id_list_missing():
    runtime_packet = {
        "skill_routing": {
            "selected": [
                {"skill_id": "latex-submission-pipeline"},
            ],
        },
        "specialist_decision": {
            "approved_dispatch_skill_ids": [
                "latex-submission-pipeline",
            ]
        },
    }
    lock = {
        "state": "active",
        "locked_dispatch": [
            {"skill_id": "latex-submission-pipeline"},
        ],
    }

    state, notes, lists = _evaluate_selected_lock_reconciliation(runtime_packet, lock)

    assert state == "passing"
    assert notes == ["Selected/approved specialist execution obligations are locked."]
    assert lists["locked"] == ["latex-submission-pipeline"]
    assert lists["missing"] == []


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_delivery_acceptance_manual_review_when_selected_skill_missing_from_lock(tmp_path):
    repo_root = tmp_path / "repo"
    session_root = tmp_path / "session"
    session_root.mkdir(parents=True)
    (repo_root / "config").mkdir(parents=True)
    _write_json(
        repo_root / "config" / "project-delivery-acceptance-contract.json",
        {
            "version": 1,
            "truth_states": {
                "passing": {"counts_as_success": True, "completion_language_allowed": True},
                "manual_review_required": {"counts_as_success": False, "completion_language_allowed": False},
                "failing": {"counts_as_success": False, "completion_language_allowed": False},
                "partial": {"counts_as_success": False, "completion_language_allowed": False},
                "not_run": {"counts_as_success": False, "completion_language_allowed": False},
                "degraded": {"counts_as_success": True, "completion_language_allowed": True},
            },
        },
    )

    requirement_doc = tmp_path / "requirement.md"
    requirement_doc.write_text(
        "\n".join(
            [
                "# Requirement",
                "## Product Acceptance Criteria",
                "- Delivery acceptance can be evaluated.",
                "## Completion Language Policy",
                "- Full completion wording is allowed only after downstream delivery truth is passing.",
                "## Delivery Truth Contract",
                "- Selected specialists must be reconciled before delivery.",
            ]
        ),
        encoding="utf-8",
    )
    execution_plan = tmp_path / "plan.md"
    execution_plan.write_text(
        "# Plan\n\n## Delivery Acceptance Plan\n- Run delivery acceptance.\n",
        encoding="utf-8",
    )
    runtime_packet = session_root / "runtime-input-packet.json"
    execution_manifest = session_root / "execution-manifest.json"
    _write_json(
        runtime_packet,
        {
            "skill_routing": {
                "selected": [
                    {"skill_id": "latex-submission-pipeline"},
                    {"skill_id": "literature-review"},
                ]
            },
            "specialist_decision": {
                "decision_state": "approved_dispatch",
                "resolution_mode": "approved_dispatch",
                "approved_dispatch_skill_ids": [
                    "latex-submission-pipeline",
                    "literature-review",
                ],
            },
            "skill_execution_lock": {
                "state": "active",
                "locked_skill_ids": ["latex-submission-pipeline"],
            },
        },
    )
    loaded_skills = [
        {
            "skill_id": "latex-submission-pipeline",
            "load_status": "loaded_full_skill_md",
            "skill_md_path": "skills/latex-submission-pipeline/SKILL.md",
            "skill_md_sha256": "a" * 64,
        },
        {
            "skill_id": "literature-review",
            "load_status": "loaded_full_skill_md",
            "skill_md_path": "skills/literature-review/SKILL.md",
            "skill_md_sha256": "b" * 64,
        },
    ]
    _write_json(
        execution_manifest,
        {
            "stage": "plan_execute",
            "status": "completed",
            "executed_unit_count": 1,
            "failed_unit_count": 0,
            "timed_out_unit_count": 0,
            "specialist_accounting": {
                "effective_execution_status": "direct_current_session_routed",
                "selected_skill_execution": [
                    {
                        "skill_id": "latex-submission-pipeline",
                        "native_skill_entrypoint": "skills/latex-submission-pipeline/SKILL.md",
                    },
                ],
                "selected_skill_execution_count": 1,
                "direct_routed_skill_execution_units": [
                    {
                        "unit_id": "unit-latex",
                        "skill_id": "latex-submission-pipeline",
                        "result_path": "execution-manifest.json",
                    },
                ],
            },
            "skill_execution_lock": {
                "state": "active",
                "locked_skill_ids": ["latex-submission-pipeline"],
            },
            "specialist_lock_resolution": {
                "executed_skill_ids": ["latex-submission-pipeline"],
                "not_applicable_skill_ids": [],
                "deferred_skill_ids": [],
                "failed_skill_ids": [],
                "unresolved_skill_ids": [],
            },
            "skill_usage": {
                "schema_version": 2,
                "state_model": "binary_used_unused",
                "used": [],
                "unused": [],
                "loaded_skills": loaded_skills,
                "evidence": [],
            },
        },
    )
    _write_json(
        session_root / "phase-execute.json",
        {
            "status": "completed",
            "completion_claim_allowed": True,
            "requirement_doc_path": str(requirement_doc),
            "execution_plan_path": str(execution_plan),
            "execution_manifest_path": str(execution_manifest),
            "runtime_input_packet_path": str(runtime_packet),
            "specialist_user_disclosure": {
                "scope": "selected_skill_execution_only",
                "timing": "before_execution",
                "path_source": "native_skill_entrypoint",
                "routed_skills": [
                    {
                        "skill_id": "latex-submission-pipeline",
                        "native_skill_entrypoint": "skills/latex-submission-pipeline/SKILL.md",
                        "entrypoint_requirement_satisfied": True,
                    },
                ],
            },
            "specialist_decision": {
                "decision_state": "approved_dispatch",
                "resolution_mode": "approved_dispatch",
                "approved_dispatch_skill_ids": ["latex-submission-pipeline"],
            },
            "specialist_execution": {
                "resolution_mode": "current_session_host_execution",
                "units": [
                    {
                        "unit_id": "unit-latex",
                        "skill_id": "latex-submission-pipeline",
                        "resolution_state": "executed",
                        "evidence_paths": ["execution-manifest.json"],
                    },
                ],
                "evidence_paths": ["execution-manifest.json"],
            },
        },
    )
    _write_json(
        session_root / "cleanup-receipt.json",
        {
            "cleanup_mode": "completed",
            "status": "completed",
        },
    )
    _write_json(
        session_root / "skill-usage.json",
        {
            "schema_version": 2,
            "state_model": "binary_used_unused",
            "used": [],
            "unused": [],
            "loaded_skills": loaded_skills,
            "evidence": [],
        },
    )

    report = evaluate_delivery_acceptance(repo_root, session_root)

    assert report["summary"]["gate_result"] == "MANUAL_REVIEW_REQUIRED"
    assert report["summary"]["completion_language_allowed"] is False
    assert report["truth_results"]["selected_lock_reconciliation_truth"]["state"] == "manual_review_required"
    assert report["selected_lock_reconciliation"]["missing"] == ["literature-review"]
    assert (
        "Selected/approved specialist execution was not locked for: literature-review."
        in report["residual_risks"]
    )
