from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = REPO_ROOT / "config" / "current-routing-debt-erasure.json"
OLD_ROLE_TERMS = [
    "route_authority_candidates",
    "stage_assistant_candidates",
    "route_authority_eligible",
    "legacy_role",
    "_legacy_role",
    "_legacy_stage_assistant_candidates",
]


def load_policy() -> dict[str, object]:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def test_policy_defines_current_field_chain_and_retired_terms() -> None:
    policy = load_policy()

    assert policy["schema_version"] == 1
    assert policy["current_model"] == [
        "skill_candidates",
        "skill_routing.selected",
        "skill_execution_lock",
        "selected_skill_execution",
        "skill_usage.used",
        "skill_usage.unused",
        "skill_usage.evidence",
    ]

    active_fields = set(policy["active_fields"])
    for field in [
        "skill_candidates",
        "skill_routing",
        "skill_routing.candidates",
        "skill_routing.selected",
        "skill_routing.rejected",
        "skill_execution_lock",
        "selected_skill_execution",
        "skill_execution_units",
        "approved_skill_execution",
        "execution_skill_outcomes",
        "skill_usage",
        "skill_usage.loaded_skills",
        "skill_usage.used",
        "skill_usage.unused",
        "skill_usage.used_skills",
        "skill_usage.unused_skills",
        "skill_usage.evidence",
    ]:
        assert field in active_fields

    retired_terms = set(policy["retired_terms"])
    for term in [
        "legacy_skill_routing",
        "specialist_recommendations",
        "stage_assistant_hints",
        "specialist_dispatch",
        "approved_consultation",
        "consulted_units",
        "route authority",
        "stage assistant",
        "consultation expert",
        "primary skill",
        "secondary skill",
    ]:
        assert term in retired_terms

    for term in OLD_ROLE_TERMS:
        assert term in retired_terms

    high_risk_terms = set(policy["high_risk_retired_fields"])
    for term in OLD_ROLE_TERMS:
        assert term in high_risk_terms


def test_policy_separates_current_and_legacy_scopes() -> None:
    policy = load_policy()
    current_paths = set(policy["scan_scopes"]["current_paths"])
    allowed_paths = set(policy["scan_scopes"]["legacy_allowed_paths"])

    assert "scripts/runtime/VibeRuntime.Common.ps1" in current_paths
    assert "scripts/router/resolve-pack-route.ps1" in current_paths
    assert "packages/runtime-core/src/vgo_runtime" in current_paths
    assert "tests/runtime_neutral" in current_paths
    assert "tests/unit" in current_paths
    assert "tests/integration" in current_paths

    assert "tests/runtime_neutral/test_retired_old_routing_compat.py" in allowed_paths
    assert "docs/governance/historical-routing-terminology.md" in allowed_paths
    assert "docs/superpowers/specs" in allowed_paths

    excluded_roots = set(policy["scan_scopes"]["excluded_roots"])
    assert "bundled/skills" in excluded_roots
    assert "dist" in excluded_roots
    assert "vendor" in excluded_roots
    assert "third_party" in excluded_roots
    assert ".worktrees" in excluded_roots
