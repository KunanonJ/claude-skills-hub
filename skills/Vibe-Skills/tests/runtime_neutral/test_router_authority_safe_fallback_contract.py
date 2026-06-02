from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PACK_MANIFEST = json.loads((REPO_ROOT / "config" / "pack-manifest.json").read_text(encoding="utf-8-sig"))
ROUTER_THRESHOLDS = json.loads((REPO_ROOT / "config" / "router-thresholds.json").read_text(encoding="utf-8-sig"))


def pack_by_id(pack_id: str) -> dict[str, object]:
    for pack in PACK_MANIFEST["packs"]:
        if pack["id"] == pack_id:
            return pack
    raise AssertionError(f"missing pack: {pack_id}")


def test_first_wave_packs_define_authority_tiers() -> None:
    code_quality = pack_by_id("code-quality")
    integration_devops = pack_by_id("integration-devops")
    docs_media = pack_by_id("docs-media")
    scholarly = pack_by_id("scholarly-publishing-workflow")

    assert code_quality["authority_tier"] == "broad_owner"
    assert code_quality["fallback_owner_pack_id"] == "code-quality"
    assert code_quality["fallback_owner_skill"] == "systematic-debugging"

    assert integration_devops["authority_tier"] == "broad_owner"
    assert integration_devops["fallback_owner_pack_id"] == "integration-devops"
    assert integration_devops["fallback_owner_skill"] == "gh-fix-ci"

    assert docs_media["authority_tier"] == "broad_owner"
    assert docs_media["fallback_owner_pack_id"] == "docs-media"
    assert docs_media["fallback_owner_skill"] == "pdf"

    assert scholarly["authority_tier"] == "narrow_specialist"
    assert scholarly["fallback_owner_pack_id"] == "code-quality"
    assert scholarly["fallback_owner_skill"] == "systematic-debugging"


def test_router_thresholds_define_safe_fallback_policy() -> None:
    authority = ROUTER_THRESHOLDS["authority"]

    assert authority["default_requires_positive_keyword_match_for_narrow"] is True
    assert authority["supporting_keyword_weight"] == 0.35
    assert authority["minimum_candidate_signal_by_tier"] == {
        "broad_owner": 0.18,
        "narrow_specialist": 0.32,
    }
    assert authority["global_safe_fallback_by_task"]["debug"] == {
        "pack_id": "code-quality",
        "skill": "systematic-debugging",
    }
    assert authority["global_safe_fallback_by_task"]["review"] == {
        "pack_id": "code-quality",
        "skill": "code-reviewer",
    }
