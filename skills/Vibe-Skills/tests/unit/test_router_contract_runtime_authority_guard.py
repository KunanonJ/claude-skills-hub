from __future__ import annotations

from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SRC = ROOT / "packages" / "runtime-core" / "src"
if str(RUNTIME_SRC) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SRC))

from vgo_runtime import router_contract_runtime as runtime
from vgo_runtime.router_contract_selection import INTERNAL_SELECTION_USABLE


def test_unknown_authority_tier_uses_broad_owner_threshold(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        runtime,
        "load_router_config_bundle",
        lambda _config_root: {
            "pack_manifest": {
                "packs": [
                    {
                        "id": "shadow-pack",
                        "authority_tier": " Broad_Owner ",
                        "skill_candidates": ["shadow-skill"],
                    }
                ]
            },
            "alias_map": {"aliases": {}},
            "thresholds": {
                "thresholds": {
                    "min_top1_top2_gap": 0.08,
                    "min_candidate_signal_for_confirm_override": 0.2,
                    "min_candidate_signal_for_auto_route": 0.6,
                    "auto_route": 0.7,
                    "confirm_required": 0.45,
                    "fallback_to_legacy_below": 0.45,
                },
                "safety": {"enforce_confirm_on_legacy_fallback": False},
                "authority": {
                    "minimum_candidate_signal_by_tier": {
                        "broad_owner": 0.18,
                        "narrow_specialist": 0.32,
                    },
                    "global_safe_fallback_by_task": {},
                },
            },
            "skill_keyword_index": {},
            "fallback_policy": {},
            "routing_rules": {},
        },
    )
    monkeypatch.setattr(runtime, "resolve_requested_canonical", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        runtime,
        "load_custom_admission",
        lambda **kwargs: {
            "status": "not_configured",
            "target_root": None,
            "manifest_paths": [],
            "manifests_present": [],
            "invalid_entries": [],
            "dependency_failures": [],
            "admitted_candidates": [],
            "admitted_packs": [],
        },
    )
    monkeypatch.setattr(runtime, "get_pack_skill_candidates", lambda pack: ["shadow-skill"])
    monkeypatch.setattr(
        runtime,
        "select_pack_candidate",
        lambda **kwargs: {
            "selected": "shadow-skill",
            "reason": "keyword_ranked",
            "score": 0.2,
            "relevance_score": 0.2,
            "ranking": [{"skill": "shadow-skill", "score": 0.2}],
            "top1_top2_gap": 0.0,
            "filtered_out_by_task": [],
            INTERNAL_SELECTION_USABLE: True,
        },
    )
    monkeypatch.setattr(runtime, "_build_deep_discovery_advice", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        runtime,
        "_build_deep_discovery_intent_contract",
        lambda *args, **kwargs: {
            "goal": "",
            "deliverable": "unknown",
            "constraints": [],
            "capabilities": [],
            "execution_mode": "unspecified",
            "required_fields": [],
            "missing_fields": [],
            "completeness": 1.0,
            "field_presence": {},
        },
    )
    monkeypatch.setattr(runtime, "build_fallback_truth", lambda result, fallback_policy: {})
    monkeypatch.setattr(runtime, "build_confirm_ui", lambda repo, result, target_root, host_id=None: None)

    result = runtime.route_prompt(
        prompt="shadow skill keyword",
        grade="L",
        task_type="debug",
        repo_root=tmp_path,
    )

    assert result["route_mode"] == "legacy_fallback"
    assert result["route_reason"] == "no_eligible_pack"
    assert result["selected"] is None
    assert result["fallback_applied"] is False
    assert result["pre_fallback_top"] == {"pack_id": "shadow-pack", "skill": "shadow-skill"}
    assert result["rejected_specialist_reasons"] == ["candidate_signal_below_authority_threshold"]
