from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SRC = ROOT / "packages" / "runtime-core" / "src"
if str(RUNTIME_SRC) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SRC))

from vgo_runtime.router_contract_authority import choose_authoritative_route


def test_ineligible_narrow_top_pack_falls_back_to_broad_owner() -> None:
    ranked = [
        {
            "pack_id": "scholarly-publishing-workflow",
            "score": 0.58,
            "selected_candidate": "latex-submission-pipeline",
            "candidate_selection_reason": "keyword_ranked",
            "candidate_selection_score": 0.27,
            "candidate_signal": 0.22,
            "candidate_top1_top2_gap": 0.05,
            "authority_tier": "narrow_specialist",
            "authority_eligible": False,
            "authority_rejection_reasons": ["missing_authority_keyword"],
            "candidate_ranking": [
                {
                    "skill": "latex-submission-pipeline",
                    "authority_keyword_score": 0.0,
                    "supporting_keyword_score": 0.8,
                    "authority_guard_reason": "missing_authority_keyword",
                    "score": 0.27,
                }
            ],
        },
        {
            "pack_id": "code-quality",
            "score": 0.54,
            "selected_candidate": "systematic-debugging",
            "candidate_selection_reason": "keyword_ranked",
            "candidate_selection_score": 0.43,
            "candidate_signal": 0.39,
            "candidate_top1_top2_gap": 0.13,
            "authority_tier": "broad_owner",
            "authority_eligible": True,
            "authority_rejection_reasons": [],
            "candidate_ranking": [{"skill": "systematic-debugging", "score": 0.43}],
        },
    ]

    decision = choose_authoritative_route(
        ranked=ranked,
        task_type="debug",
        requested_canonical=None,
        authority_policy={
            "global_safe_fallback_by_task": {
                "debug": {"pack_id": "code-quality", "skill": "systematic-debugging"}
            }
        },
    )

    assert decision["selected_pack_id"] == "code-quality"
    assert decision["selected_skill"] == "systematic-debugging"
    assert decision["fallback_applied"] is True
    assert decision["pre_fallback_top_pack_id"] == "scholarly-publishing-workflow"
    assert decision["rejected_specialist_reasons"] == ["missing_authority_keyword"]


def test_eligible_top_pack_stays_selected() -> None:
    ranked = [
        {
            "pack_id": "scholarly-publishing-workflow",
            "score": 0.77,
            "selected_candidate": "latex-submission-pipeline",
            "candidate_selection_reason": "keyword_ranked",
            "candidate_selection_score": 0.62,
            "candidate_signal": 0.61,
            "candidate_top1_top2_gap": 0.21,
            "authority_tier": "narrow_specialist",
            "authority_eligible": True,
            "authority_rejection_reasons": [],
            "candidate_ranking": [{"skill": "latex-submission-pipeline", "authority_keyword_score": 0.66, "score": 0.62}],
        }
    ]

    decision = choose_authoritative_route(
        ranked=ranked,
        task_type="coding",
        requested_canonical=None,
        authority_policy={"global_safe_fallback_by_task": {}},
    )

    assert decision["selected_pack_id"] == "scholarly-publishing-workflow"
    assert decision["selected_skill"] == "latex-submission-pipeline"
    assert decision["fallback_applied"] is False
    assert decision["rejected_specialist_reasons"] == []


def test_requested_canonical_skips_blank_top_row_and_uses_first_route_usable_candidate() -> None:
    ranked = [
        {
            "pack_id": "design-implementation",
            "score": 0.178,
            "selected_candidate": None,
            "candidate_selection_reason": "no_usable_candidate",
            "candidate_selection_score": 0.0,
            "candidate_signal": 0.0,
            "candidate_top1_top2_gap": 0.0,
            "authority_tier": "broad_owner",
            "authority_eligible": False,
            "authority_rejection_reasons": ["no_usable_candidate", "candidate_signal_below_authority_threshold"],
            "candidate_ranking": [],
            "_route_usable": False,
        },
        {
            "pack_id": "scholarly-publishing-workflow",
            "score": 0.177,
            "selected_candidate": "scholarly-publishing",
            "candidate_selection_reason": "fallback_task_default",
            "candidate_selection_score": 0.12,
            "candidate_signal": 0.09,
            "candidate_top1_top2_gap": 0.0,
            "authority_tier": "narrow_specialist",
            "authority_eligible": False,
            "authority_rejection_reasons": ["candidate_signal_below_authority_threshold"],
            "candidate_ranking": [{"skill": "scholarly-publishing", "score": 0.12}],
            "_route_usable": True,
        },
    ]

    decision = choose_authoritative_route(
        ranked=ranked,
        task_type="planning",
        requested_canonical="writing-plans",
        authority_policy={"global_safe_fallback_by_task": {}},
    )

    assert decision["selected_pack_id"] == "scholarly-publishing-workflow"
    assert decision["selected_skill"] == "scholarly-publishing"
    assert decision["fallback_applied"] is False
    assert decision["pre_fallback_top_pack_id"] == "design-implementation"
    assert decision["pre_fallback_top_skill"] == ""
    assert decision["rejected_specialist_reasons"] == []


def test_ineligible_top_with_no_fallback_destination_does_not_claim_fallback_applied() -> None:
    ranked = [
        {
            "pack_id": "scholarly-publishing-workflow",
            "score": 0.58,
            "selected_candidate": "latex-submission-pipeline",
            "candidate_selection_reason": "keyword_ranked",
            "candidate_selection_score": 0.27,
            "candidate_signal": 0.22,
            "candidate_top1_top2_gap": 0.05,
            "authority_tier": "narrow_specialist",
            "authority_eligible": False,
            "authority_rejection_reasons": ["missing_authority_keyword"],
            "candidate_ranking": [{"skill": "latex-submission-pipeline", "score": 0.27}],
        }
    ]

    decision = choose_authoritative_route(
        ranked=ranked,
        task_type="debug",
        requested_canonical=None,
        authority_policy={"global_safe_fallback_by_task": {}},
    )

    assert decision["selected_pack_id"] is None
    assert decision["selected_skill"] is None
    assert decision["selected_row"] is None
    assert decision["fallback_applied"] is False
    assert decision["pre_fallback_top_pack_id"] == "scholarly-publishing-workflow"
    assert decision["rejected_specialist_reasons"] == ["missing_authority_keyword"]


def test_missing_authority_eligible_field_does_not_fail_open() -> None:
    ranked = [
        {
            "pack_id": "latent-broad-owner",
            "score": 0.61,
            "selected_candidate": "systematic-debugging",
            "candidate_selection_reason": "keyword_ranked",
            "candidate_selection_score": 0.43,
            "candidate_signal": 0.39,
            "candidate_top1_top2_gap": 0.13,
            "authority_tier": "broad_owner",
            "authority_rejection_reasons": [],
            "candidate_ranking": [{"skill": "systematic-debugging", "score": 0.43}],
        }
    ]

    decision = choose_authoritative_route(
        ranked=ranked,
        task_type="debug",
        requested_canonical=None,
        authority_policy={"global_safe_fallback_by_task": {}},
    )

    assert decision["selected_pack_id"] is None
    assert decision["selected_skill"] is None
    assert decision["selected_row"] is None
    assert decision["fallback_applied"] is False
    assert decision["pre_fallback_top_pack_id"] == "latent-broad-owner"
