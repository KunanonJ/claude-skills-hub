# Router Authority Safe Fallback Governance

Date: 2026-05-07

## Purpose

This note records the first-wave router authority policy that prevents weak narrow specialists from owning ambiguous prompts and rewrites ineligible tops to a safer broad owner before confirmation or plan freeze.

The immediate trigger was a debug/logs task that drifted into `scholarly-publishing-workflow / latex-submission-pipeline`. The fix is not a one-off keyword patch. It introduces an authority contract, safe fallback audit fields, and first-wave pack cleanup.

## Authority Tiers

| Pack | Authority Tier | Safe Fallback |
| --- | --- | --- |
| `code-quality` | `broad_owner` | `code-quality / systematic-debugging` |
| `integration-devops` | `broad_owner` | `integration-devops / gh-fix-ci` |
| `docs-media` | `broad_owner` | `docs-media / pdf` |
| `scholarly-publishing-workflow` | `narrow_specialist` | `code-quality / systematic-debugging` |

## Rules

- `narrow_specialist` packs must match `authority_keywords` before they can own a route.
- `supporting_keywords` can help in-pack scoring, but they do not replace authority evidence.
- `broad_owner` packs can absorb ambiguous prompts, but they still need usable candidates and sufficient signal to become `authority_eligible`.
- `selected` is derived after authority arbitration, not directly from raw top score.
- `fallback_applied`, `pre_fallback_top`, and `rejected_specialist_reasons` are required audit fields whenever a top route is rewritten.

## First-Wave Keyword Decisions

- `latex-submission-pipeline` now treats `latexmk`, `latexindent`, `chktex`, `submission zip`, `latex manuscript`, `LaTeX 写论文`, `LaTeX 论文 PDF`, and related publishing anchors as authority evidence.
- `build pdf`, `paper pdf build`, `github actions`, and `pipeline` remain only supporting evidence for the LaTeX pipeline.
- `runtime logs`, `translation api failure`, `sentry alert`, and similar operational phrases are explicitly negative for `latex-submission-pipeline`.
- `systematic-debugging` now has explicit authority evidence for `runtime logs`, `api failure`, `stack trace`, `traceback`, `错误日志`, and `故障定位`.
- `gh-fix-ci` and `sentry` now declare authority anchors instead of relying on generic pipeline/error language alone.

## Runtime Contract

Each ranked pack row now exposes:

- `authority_tier`
- `authority_eligible`
- `authority_rejection_reasons`
- `fallback_owner_pack_id`
- `fallback_owner_skill`

The final route result now exposes:

- `fallback_applied`
- `fallback_target`
- `pre_fallback_top`
- `rejected_specialist_reasons`
- `selected.authority`

## Operational Notes

- Safe fallback is a guardrail, not the desired steady state.
- After the keyword hardening in this change, the original debug/logs prompt now routes directly to `code-quality / systematic-debugging` instead of requiring a post-hoc fallback rewrite.
- Broad-owner self-fallback is intentionally not used when a broad owner has no usable candidate. In that case the router can stop at `confirm_required` or `legacy_fallback_guard` instead of inventing a misleading default skill.

## Verification

- `python -m pytest tests/runtime_neutral/test_router_authority_safe_fallback_contract.py -q`
- `python -m pytest tests/unit/test_router_contract_authority_selection.py -q`
- `python -m pytest tests/unit/test_router_contract_authority.py -q`
- `python -m pytest tests/runtime_neutral/test_router_authority_safe_fallback.py -q`
- `python -m pytest tests/runtime_neutral/test_runtime_route_output_shape.py -q`
- `python -m pytest tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py -q`
- `python -m pytest tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py -q`
- `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-pack-regression-matrix.ps1`
- `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-skill-index-routing-audit.ps1`
