from __future__ import annotations

from typing import Any

from .router_contract_support import normalize_text


def _row_by_pack_id(ranked: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        normalize_text(row.get("pack_id") or ""): row
        for row in ranked
        if normalize_text(row.get("pack_id") or "")
    }


def _first_requested_route_usable_row(ranked: list[dict[str, Any]]) -> dict[str, Any] | None:
    for row in ranked:
        selected_skill = str(row.get("selected_candidate") or "").strip()
        route_usable = bool(row.get("_route_usable", bool(selected_skill)))
        if route_usable and selected_skill:
            return row
    return None


def choose_authoritative_route(
    ranked: list[dict[str, Any]],
    task_type: str,
    requested_canonical: str | None,
    authority_policy: dict[str, Any],
) -> dict[str, Any]:
    top = ranked[0] if ranked else None
    if not top:
        return {
            "selected_pack_id": None,
            "selected_skill": None,
            "selected_row": None,
            "fallback_applied": False,
            "fallback_target_pack_id": None,
            "fallback_target_skill": None,
            "pre_fallback_top_pack_id": None,
            "pre_fallback_top_skill": None,
            "rejected_specialist_reasons": [],
        }

    if requested_canonical:
        requested_row = _first_requested_route_usable_row(ranked) or top
        return {
            "selected_pack_id": str((requested_row or {}).get("pack_id") or ""),
            "selected_skill": str((requested_row or {}).get("selected_candidate") or ""),
            "selected_row": requested_row,
            "fallback_applied": False,
            "fallback_target_pack_id": None,
            "fallback_target_skill": None,
            "pre_fallback_top_pack_id": str(top.get("pack_id") or ""),
            "pre_fallback_top_skill": str(top.get("selected_candidate") or ""),
            "rejected_specialist_reasons": [],
        }

    if bool(top.get("authority_eligible", False)):
        return {
            "selected_pack_id": str(top.get("pack_id") or ""),
            "selected_skill": str(top.get("selected_candidate") or ""),
            "selected_row": top,
            "fallback_applied": False,
            "fallback_target_pack_id": None,
            "fallback_target_skill": None,
            "pre_fallback_top_pack_id": str(top.get("pack_id") or ""),
            "pre_fallback_top_skill": str(top.get("selected_candidate") or ""),
            "rejected_specialist_reasons": [],
        }

    rows_by_pack = _row_by_pack_id(ranked)
    fallback_by_task = authority_policy.get("global_safe_fallback_by_task") or {}
    task_fallback = fallback_by_task.get(task_type) or {}
    top_authority_tier = normalize_text(str(top.get("authority_tier") or ""))
    top_pack_fallback_pack_id = (
        normalize_text(top.get("fallback_owner_pack_id") or "")
        if top_authority_tier == "narrow_specialist"
        else ""
    )
    top_pack_fallback_skill = (
        str(top.get("fallback_owner_skill") or "").strip()
        if top_authority_tier == "narrow_specialist"
        else ""
    )
    fallback_pack_id = normalize_text(task_fallback.get("pack_id") or top_pack_fallback_pack_id or "")
    fallback_skill = str(task_fallback.get("skill") or top_pack_fallback_skill or "").strip()
    fallback_row = rows_by_pack.get(fallback_pack_id)

    if fallback_row:
        selected_pack_id = str(fallback_row.get("pack_id") or "")
        selected_skill = fallback_skill or str(fallback_row.get("selected_candidate") or "")
        selected_row = fallback_row
    else:
        broad_owner = next(
            (
                row
                for row in ranked
                if normalize_text(str(row.get("authority_tier") or "")) == "broad_owner"
                and bool(row.get("authority_eligible", False))
            ),
            None,
        )
        selected_row = broad_owner
        selected_pack_id = str((broad_owner or {}).get("pack_id") or "")
        selected_skill = str((broad_owner or {}).get("selected_candidate") or "")

    fallback_applied = bool(selected_row or selected_pack_id or selected_skill)
    return {
        "selected_pack_id": selected_pack_id or None,
        "selected_skill": selected_skill or None,
        "selected_row": selected_row,
        "fallback_applied": fallback_applied,
        "fallback_target_pack_id": selected_pack_id or None,
        "fallback_target_skill": selected_skill or None,
        "pre_fallback_top_pack_id": str(top.get("pack_id") or ""),
        "pre_fallback_top_skill": str(top.get("selected_candidate") or ""),
        "rejected_specialist_reasons": [str(item) for item in (top.get("authority_rejection_reasons") or [])],
    }
