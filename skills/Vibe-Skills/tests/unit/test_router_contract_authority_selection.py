from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SRC = ROOT / "packages" / "runtime-core" / "src"
if str(RUNTIME_SRC) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SRC))

from vgo_runtime.router_contract_selection import select_pack_candidate


def narrow_selection(prompt: str) -> dict[str, object]:
    return select_pack_candidate(
        prompt_lower=prompt.casefold(),
        candidates=["latex-submission-pipeline"],
        task_type="debug",
        requested_canonical=None,
        skill_keyword_index={
            "selection": {
                "weights": {"keyword_match": 0.8, "name_match": 0.2},
                "fallback_to_first_when_score_below": 0.2,
            },
            "skills": {
                "latex-submission-pipeline": {
                    "keywords": ["latex", "paper pdf", "build pdf", "pipeline", "github actions"]
                }
            },
        },
        routing_rules={
            "skills": {
                "latex-submission-pipeline": {
                    "task_allow": ["planning", "coding", "debug"],
                    "authority_keywords": [
                        "latexmk",
                        "submission zip",
                        "latex manuscript",
                        "论文编译",
                    ],
                    "supporting_keywords": [
                        "build pdf",
                        "pipeline",
                        "github actions",
                    ],
                    "negative_keywords": [],
                    "canonical_for_task": [],
                }
            }
        },
        pack={
            "id": "scholarly-publishing-workflow",
            "authority_tier": "narrow_specialist",
            "skill_candidates": ["latex-submission-pipeline"],
            "defaults_by_task": {},
        },
        candidate_selection_config={
            "rule_positive_keyword_bonus": 0.2,
            "rule_negative_keyword_penalty": 0.25,
            "canonical_for_task_bonus": 0.12,
            "authority": {
                "default_requires_positive_keyword_match_for_narrow": True,
                "supporting_keyword_weight": 0.35,
            },
        },
    )


def test_narrow_specialist_is_not_usable_with_only_supporting_keywords() -> None:
    result = narrow_selection("check runtime logs and translation api failure in pipeline")

    assert result["selected"] is None
    assert result["reason"] == "no_usable_candidate"
    assert result["_selection_usable"] is False


def test_narrow_specialist_can_win_with_authority_keywords() -> None:
    result = narrow_selection("configure latexmk and build a submission zip for the latex manuscript")

    assert result["selected"] == "latex-submission-pipeline"
    assert result["reason"] == "keyword_ranked"
    assert result["_selection_usable"] is True
    assert result["ranking"][0]["authority_keyword_score"] > 0


def test_requested_skill_still_bypasses_the_guard() -> None:
    result = select_pack_candidate(
        prompt_lower="check runtime logs and translation api failure in pipeline",
        candidates=["latex-submission-pipeline"],
        task_type="debug",
        requested_canonical="latex-submission-pipeline",
        skill_keyword_index={
            "selection": {
                "weights": {"keyword_match": 0.8, "name_match": 0.2},
                "fallback_to_first_when_score_below": 0.2,
            },
            "skills": {
                "latex-submission-pipeline": {"keywords": ["latex", "paper pdf", "build pdf"]}
            },
        },
        routing_rules={"skills": {}},
        pack={
            "id": "scholarly-publishing-workflow",
            "authority_tier": "narrow_specialist",
            "skill_candidates": ["latex-submission-pipeline"],
            "defaults_by_task": {},
        },
        candidate_selection_config={
            "rule_positive_keyword_bonus": 0.2,
            "rule_negative_keyword_penalty": 0.25,
            "canonical_for_task_bonus": 0.12,
            "authority": {
                "default_requires_positive_keyword_match_for_narrow": True,
                "supporting_keyword_weight": 0.35,
            },
        },
    )

    assert result["selected"] == "latex-submission-pipeline"
    assert result["reason"] == "requested_skill"
