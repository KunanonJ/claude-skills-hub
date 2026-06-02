# Router Authority And Safe Fallback Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a route-authority contract that prevents weak narrow specialists from owning ambiguous tasks, and safely falls back to a broader owner before confirmation or plan freeze.

**Architecture:** Extend pack metadata and routing rules with explicit authority tiers and fallback owners, then enforce that contract in both the Python contract mirror and the live PowerShell router. Use first-wave pack cleanup plus a regression matrix to prove that ambiguous debug, logs, runtime, API failure, PDF, CI, and publishing prompts are routed to the correct owner for the right reason.

**Tech Stack:** Python runtime-core modules, PowerShell router modules, JSON router config, `pytest`, existing Vibe-Skills regression gates, Markdown governance docs.

---

## File Map

- `config/pack-manifest.json`
  - Add `authority_tier`, `fallback_owner_pack_id`, and `fallback_owner_skill` to first-wave packs.
- `config/router-thresholds.json`
  - Add authority-policy thresholds and task-level safe fallback defaults.
- `config/skill-routing-rules.json`
  - Add `authority_keywords`, `supporting_keywords`, and explicit narrow-specialist guards for high-risk skills.
- `config/skill-keyword-index.json`
  - Trim first-wave narrow specialist keyword lists so generic terms stop inflating cross-domain relevance.
- `packages/runtime-core/src/vgo_runtime/router_contract_selection.py`
  - Enforce narrow-specialist admission at candidate-selection time and expose authority scoring in ranking rows.
- `packages/runtime-core/src/vgo_runtime/router_contract_authority.py`
  - New authority arbitration helper for pack eligibility and safe fallback choice.
- `packages/runtime-core/src/vgo_runtime/router_contract_runtime.py`
  - Use authority arbitration to rewrite `selected` after ranking and publish fallback audit fields.
- `scripts/router/modules/41-candidate-selection.ps1`
  - Mirror the Python candidate-selection authority guard in the live router.
- `scripts/router/resolve-pack-route.ps1`
  - Mirror Python authority arbitration and expose the same fallback audit fields in live route output.
- `tests/unit/test_router_contract_authority_selection.py`
  - Synthetic selection tests for authority keywords, supporting keywords, and narrow-specialist guards.
- `tests/unit/test_router_contract_authority.py`
  - Synthetic arbitration tests for ineligible top packs and safe fallback rewrites.
- `tests/runtime_neutral/test_router_authority_safe_fallback_contract.py`
  - Config contract tests for first-wave authority tiers and threshold defaults.
- `tests/runtime_neutral/test_router_authority_safe_fallback.py`
  - Real routing regressions for ambiguous debug, publishing, PDF, CI, and sentry prompts.
- `tests/runtime_neutral/test_runtime_route_output_shape.py`
  - Assert the new fallback audit fields are present in runtime-neutral route output.
- `tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py`
  - Keep existing PDF / LaTeX / docs boundaries aligned with the new authority contract.
- `tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py`
  - Lock the scholarly pack into narrow-specialist behavior instead of broad keyword absorption.
- `scripts/verify/vibe-pack-regression-matrix.ps1`
  - Add `should_fallback` and `should_rank_but_not_select` cases plus fallback assertions.
- `scripts/verify/vibe-skill-index-routing-audit.ps1`
  - Add cross-domain prompts that must keep narrow specialists out of `selected`.
- `docs/governance/router-authority-safe-fallback-governance.md`
  - Explain the authority tiers, fallback contract, and first-wave pack decisions.

## Task 1: Add The Authority Contract Metadata

**Files:**
- Create: `tests/runtime_neutral/test_router_authority_safe_fallback_contract.py`
- Modify: `config/pack-manifest.json`
- Modify: `config/router-thresholds.json`

- [ ] **Step 1: Write the failing contract tests**

Create `tests/runtime_neutral/test_router_authority_safe_fallback_contract.py`:

```python
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
```

- [ ] **Step 2: Run the contract tests and verify they fail**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_router_authority_safe_fallback_contract.py -q
```

Expected: FAIL with `KeyError: 'authority_tier'` or `KeyError: 'authority'` because the contract metadata does not exist yet.

- [ ] **Step 3: Add the first-wave authority metadata**

Update `config/router-thresholds.json` so it contains:

```json
{
  "authority": {
    "default_requires_positive_keyword_match_for_narrow": true,
    "supporting_keyword_weight": 0.35,
    "minimum_candidate_signal_by_tier": {
      "broad_owner": 0.18,
      "narrow_specialist": 0.32
    },
    "global_safe_fallback_by_task": {
      "debug": {
        "pack_id": "code-quality",
        "skill": "systematic-debugging"
      },
      "review": {
        "pack_id": "code-quality",
        "skill": "code-reviewer"
      }
    }
  }
}
```

Update the relevant `config/pack-manifest.json` pack objects so they contain:

```json
{
  "id": "code-quality",
  "authority_tier": "broad_owner",
  "fallback_owner_pack_id": "code-quality",
  "fallback_owner_skill": "systematic-debugging"
}
```

```json
{
  "id": "integration-devops",
  "authority_tier": "broad_owner",
  "fallback_owner_pack_id": "integration-devops",
  "fallback_owner_skill": "gh-fix-ci"
}
```

```json
{
  "id": "docs-media",
  "authority_tier": "broad_owner",
  "fallback_owner_pack_id": "docs-media",
  "fallback_owner_skill": "pdf"
}
```

```json
{
  "id": "scholarly-publishing-workflow",
  "authority_tier": "narrow_specialist",
  "fallback_owner_pack_id": "code-quality",
  "fallback_owner_skill": "systematic-debugging"
}
```

- [ ] **Step 4: Run the contract tests and verify they pass**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_router_authority_safe_fallback_contract.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add config/pack-manifest.json config/router-thresholds.json tests/runtime_neutral/test_router_authority_safe_fallback_contract.py
git commit -m "test: define router authority safe fallback contract"
```

## Task 2: Add Narrow-Specialist Admission Guards

**Files:**
- Create: `tests/unit/test_router_contract_authority_selection.py`
- Modify: `packages/runtime-core/src/vgo_runtime/router_contract_selection.py`
- Modify: `scripts/router/modules/41-candidate-selection.ps1`

- [ ] **Step 1: Write the failing selection-guard tests**

Create `tests/unit/test_router_contract_authority_selection.py`:

```python
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
```

- [ ] **Step 2: Run the selection tests and verify they fail**

Run:

```powershell
python -m pytest tests/unit/test_router_contract_authority_selection.py -q
```

Expected: FAIL because `authority_keyword_score` is missing and the narrow specialist still wins with only supporting keywords.

- [ ] **Step 3: Implement the narrow-specialist guard in Python and PowerShell**

Update `packages/runtime-core/src/vgo_runtime/router_contract_selection.py` inside `select_pack_candidate` with this authority-aware logic:

```python
def _pack_authority_tier(pack: dict[str, Any]) -> str:
    return normalize_text(pack.get("authority_tier") or "broad_owner") or "broad_owner"


def _rule_keyword_list(rule: dict[str, Any], key: str) -> list[str]:
    return [str(item).strip() for item in (rule.get(key) or []) if str(item).strip()]


authority_cfg = candidate_selection_config.get("authority") or {}
default_requires_positive_for_narrow = bool(
    authority_cfg.get("default_requires_positive_keyword_match_for_narrow", False)
)
supporting_keyword_weight = float(authority_cfg.get("supporting_keyword_weight", 0.35))
pack_authority_tier = _pack_authority_tier(pack)

for ordinal, candidate in enumerate(filtered_candidates):
    candidate_key = normalize_text(candidate)
    skill_entry = keywords_by_skill_normalized.get(candidate_key) or {}
    keyword_score = keyword_ratio(prompt_lower, skill_entry.get("keywords") or [])
    name_score = candidate_name_score(prompt_lower, candidate)
    rule = rules_by_skill.get(candidate_key) or {}
    authority_keywords = _rule_keyword_list(rule, "authority_keywords") or _rule_keyword_list(rule, "positive_keywords")
    supporting_keywords = _rule_keyword_list(rule, "supporting_keywords")
    authority_keyword_score = keyword_ratio(prompt_lower, authority_keywords)
    supporting_keyword_score = keyword_ratio(prompt_lower, supporting_keywords)
    positive_score = min(1.0, authority_keyword_score + (supporting_keyword_weight * supporting_keyword_score))
    negative_score = keyword_ratio(prompt_lower, rule.get("negative_keywords") or [])
    canonical_for_task = [normalize_text(item) for item in (rule.get("canonical_for_task") or [])]
    canonical_hit = 1.0 if task_type in canonical_for_task else 0.0

    requires_positive_keyword_match = bool(rule.get("requires_positive_keyword_match"))
    if pack_authority_tier == "narrow_specialist" and default_requires_positive_for_narrow:
        requires_positive_keyword_match = True if rule.get("requires_positive_keyword_match") is not False else False

    authority_guard_reason = ""
    use_eligible = True
    if requires_positive_keyword_match and authority_keyword_score <= 0:
        use_eligible = False
        authority_guard_reason = "missing_authority_keyword"

    score = (
        (weight_keyword * keyword_score)
        + (weight_name * name_score)
        + (positive_bonus * positive_score)
        - (negative_penalty * negative_score)
        + (canonical_bonus * canonical_hit)
    )
    score = round(max(0.0, min(1.0, score)), 4)

    scored.append(
        {
            "skill": candidate,
            "score": score,
            "keyword_score": round(keyword_score, 4),
            "name_score": round(name_score, 4),
            "positive_score": round(positive_score, 4),
            "negative_score": round(negative_score, 4),
            "authority_keyword_score": round(authority_keyword_score, 4),
            "supporting_keyword_score": round(supporting_keyword_score, 4),
            "authority_guard_reason": authority_guard_reason,
            "pack_authority_tier": pack_authority_tier,
            INTERNAL_CANDIDATE_USABLE: use_eligible,
            "requires_positive_keyword_match": requires_positive_keyword_match,
            "ordinal": ordinal,
        }
    )
```

Mirror the same behavior in `scripts/router/modules/41-candidate-selection.ps1`:

```powershell
$authorityConfig = if ($CandidateSelectionConfig -and $CandidateSelectionConfig.authority) { $CandidateSelectionConfig.authority } else { $null }
$defaultRequiresPositiveForNarrow = if ($authorityConfig -and $authorityConfig.default_requires_positive_keyword_match_for_narrow -ne $null) { [bool]$authorityConfig.default_requires_positive_keyword_match_for_narrow } else { $false }
$supportingKeywordWeight = if ($authorityConfig -and $authorityConfig.supporting_keyword_weight -ne $null) { [double]$authorityConfig.supporting_keyword_weight } else { 0.35 }
$packAuthorityTier = if ($Pack -and ($Pack.PSObject.Properties.Name -contains 'authority_tier') -and -not [string]::IsNullOrWhiteSpace([string]$Pack.authority_tier)) { [string]$Pack.authority_tier } else { 'broad_owner' }

$authorityKeywords = if ($rule -and $rule.authority_keywords) { @($rule.authority_keywords) } elseif ($rule -and $rule.positive_keywords) { @($rule.positive_keywords) } else { @() }
$supportingKeywords = if ($rule -and $rule.supporting_keywords) { @($rule.supporting_keywords) } else { @() }
$authorityKeywordScore = Get-KeywordRatio -PromptLower $PromptLower -Keywords $authorityKeywords
$supportingKeywordScore = Get-KeywordRatio -PromptLower $PromptLower -Keywords $supportingKeywords
$positiveScore = [Math]::Min(1.0, [double]$authorityKeywordScore + ($supportingKeywordWeight * [double]$supportingKeywordScore))

if ($packAuthorityTier -eq 'narrow_specialist' -and $defaultRequiresPositiveForNarrow) {
    $requiresPositiveKeywordMatch = $true
    if ($rule -and ($rule.PSObject.Properties.Name -contains 'requires_positive_keyword_match') -and ($rule.requires_positive_keyword_match -eq $false)) {
        $requiresPositiveKeywordMatch = $false
    }
}

$authorityGuardReason = $null
if ($requiresPositiveKeywordMatch -and ([double]$authorityKeywordScore -le 0.0)) {
    $useEligible = $false
    $authorityGuardReason = 'missing_authority_keyword'
}
```

- [ ] **Step 4: Run the selection tests and verify they pass**

Run:

```powershell
python -m pytest tests/unit/test_router_contract_authority_selection.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add packages/runtime-core/src/vgo_runtime/router_contract_selection.py scripts/router/modules/41-candidate-selection.ps1 tests/unit/test_router_contract_authority_selection.py
git commit -m "feat: guard narrow specialists with authority keywords"
```

## Task 3: Add Runtime Authority Arbitration And Safe Fallback

**Files:**
- Create: `packages/runtime-core/src/vgo_runtime/router_contract_authority.py`
- Create: `tests/unit/test_router_contract_authority.py`
- Modify: `packages/runtime-core/src/vgo_runtime/router_contract_runtime.py`
- Modify: `scripts/router/resolve-pack-route.ps1`
- Modify: `tests/runtime_neutral/test_runtime_route_output_shape.py`

- [ ] **Step 1: Write the failing arbitration tests**

Create `tests/unit/test_router_contract_authority.py`:

```python
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
            "candidate_ranking": [
                {"skill": "systematic-debugging", "score": 0.43}
            ],
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
            "candidate_ranking": [
                {"skill": "latex-submission-pipeline", "authority_keyword_score": 0.66, "score": 0.62}
            ],
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
```

Add this output-shape assertion to `tests/runtime_neutral/test_runtime_route_output_shape.py`:

```python
def test_runtime_route_output_exposes_fallback_audit_fields() -> None:
    result = route_prompt(
        prompt="根据错误日志排查翻译接口失败并给出解决方案",
        grade="XL",
        task_type="debug",
        repo_root=REPO_ROOT,
    )

    assert "fallback_applied" in result
    assert "rejected_specialist_reasons" in result
    assert "pre_fallback_top" in result
    assert "authority" in result["selected"]
```

- [ ] **Step 2: Run the arbitration tests and verify they fail**

Run:

```powershell
python -m pytest tests/unit/test_router_contract_authority.py tests/runtime_neutral/test_runtime_route_output_shape.py -q
```

Expected: FAIL because `router_contract_authority.py` does not exist and the route output does not expose fallback audit fields.

- [ ] **Step 3: Implement the authority arbiter in Python and PowerShell**

Create `packages/runtime-core/src/vgo_runtime/router_contract_authority.py`:

```python
from __future__ import annotations

from typing import Any

from .router_contract_support import normalize_text


def _row_by_pack_id(ranked: list[dict[str, Any]]) -> dict[str, Any]:
    return {normalize_text(row.get("pack_id") or ""): row for row in ranked if normalize_text(row.get("pack_id") or "")}


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

    if bool(top.get("authority_eligible", True)):
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
    fallback_pack_id = normalize_text(task_fallback.get("pack_id") or top.get("fallback_owner_pack_id") or "")
    fallback_skill = str(task_fallback.get("skill") or top.get("fallback_owner_skill") or "").strip()
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
                if str(row.get("authority_tier") or "") == "broad_owner"
                and bool(row.get("authority_eligible", True))
            ),
            None,
        )
        selected_row = broad_owner
        selected_pack_id = str((broad_owner or {}).get("pack_id") or "")
        selected_skill = str((broad_owner or {}).get("selected_candidate") or "")

    return {
        "selected_pack_id": selected_pack_id,
        "selected_skill": selected_skill,
        "selected_row": selected_row,
        "fallback_applied": True,
        "fallback_target_pack_id": selected_pack_id or None,
        "fallback_target_skill": selected_skill or None,
        "pre_fallback_top_pack_id": str(top.get("pack_id") or ""),
        "pre_fallback_top_skill": str(top.get("selected_candidate") or ""),
        "rejected_specialist_reasons": [str(item) for item in (top.get("authority_rejection_reasons") or [])],
    }
```

Update `packages/runtime-core/src/vgo_runtime/router_contract_runtime.py` so each pack row stores authority metadata and the final `selected` block is derived from `choose_authoritative_route`:

```python
from .router_contract_authority import choose_authoritative_route

authority_policy = thresholds_cfg.get("authority") or {}
minimum_candidate_signal_by_tier = authority_policy.get("minimum_candidate_signal_by_tier") or {}
pack_authority_tier = normalize_text(pack.get("authority_tier") or "broad_owner") or "broad_owner"
minimum_signal = float(minimum_candidate_signal_by_tier.get(pack_authority_tier, 0.0))
authority_eligible = bool(route_usable and candidate_signal >= minimum_signal)
authority_rejection_reasons: list[str] = []
if not bool(selection.get(INTERNAL_SELECTION_USABLE, selection.get("selected") is not None)):
    authority_eligible = False
    authority_rejection_reasons.append("no_usable_candidate")
if weak_fallback:
    authority_eligible = False
    authority_rejection_reasons.append("weak_fallback")
if candidate_signal < minimum_signal:
    authority_eligible = False
    authority_rejection_reasons.append("candidate_signal_below_authority_threshold")
top_candidate = next((row for row in selection["ranking"] if str(row.get("skill") or "") == str(selection["selected"] or "")), None)
if top_candidate and str(top_candidate.get("authority_guard_reason") or "").strip():
    authority_eligible = False
    authority_rejection_reasons.append(str(top_candidate["authority_guard_reason"]))

pack_results.append(
    {
        "pack_id": normalize_text(pack.get("id")),
        "score": score,
        "intent": round(intent_score, 4),
        "workspace": round(workspace_score, 4),
        "selected_candidate": selection["selected"],
        "candidate_selection_reason": selection["reason"],
        "candidate_selection_score": round(float(selection["score"]), 4),
        "candidate_relevance_score": round(relevance_score, 4),
        "candidate_ranking": selection["ranking"],
        "candidate_top1_top2_gap": round(float(selection["top1_top2_gap"]), 4),
        "candidate_signal": candidate_signal,
        "candidate_filtered_out_by_task": selection["filtered_out_by_task"],
        "authority_tier": pack_authority_tier,
        "authority_eligible": authority_eligible,
        "authority_rejection_reasons": authority_rejection_reasons,
        "fallback_owner_pack_id": _optional_text(pack.get("fallback_owner_pack_id")),
        "fallback_owner_skill": _optional_text(pack.get("fallback_owner_skill")),
    }
)

authority_decision = choose_authoritative_route(
    ranked=ranked,
    task_type=task_type,
    requested_canonical=requested_canonical,
    authority_policy=authority_policy,
)
effective_top = authority_decision["selected_row"]
selected_skill = authority_decision["selected_skill"]
selection_reason = (
    str(effective_top["candidate_selection_reason"])
    if effective_top
    else None
)
selection_score = (
    round(float(effective_top["candidate_selection_score"]), 4)
    if effective_top
    else None
)
result["fallback_applied"] = bool(authority_decision["fallback_applied"])
result["fallback_target"] = {
    "pack_id": authority_decision["fallback_target_pack_id"],
    "skill": authority_decision["fallback_target_skill"],
}
result["pre_fallback_top"] = {
    "pack_id": authority_decision["pre_fallback_top_pack_id"],
    "skill": authority_decision["pre_fallback_top_skill"],
}
result["rejected_specialist_reasons"] = authority_decision["rejected_specialist_reasons"]
result["selected"] = (
    {
        "pack_id": str((effective_top or {}).get("pack_id") or authority_decision["selected_pack_id"] or ""),
        "skill": selected_skill,
        "selection_reason": selection_reason,
        "selection_score": selection_score,
        "top1_top2_gap": float((effective_top or {}).get("candidate_top1_top2_gap") or 0.0),
        "candidate_signal": float((effective_top or {}).get("candidate_signal") or 0.0),
        "filtered_out_by_task": list((effective_top or {}).get("candidate_filtered_out_by_task") or []),
        "authority": {
            "tier": str((effective_top or {}).get("authority_tier") or ""),
            "eligible": bool((effective_top or {}).get("authority_eligible", True)),
        },
    }
    if effective_top
    else None
)
```

Mirror the same authority rewrite in `scripts/router/resolve-pack-route.ps1`:

```powershell
$authorityPolicy = if ($thresholds.authority) { $thresholds.authority } else { $null }
$minimumCandidateSignalByTier = if ($authorityPolicy -and $authorityPolicy.minimum_candidate_signal_by_tier) { $authorityPolicy.minimum_candidate_signal_by_tier } else { $null }
$packAuthorityTier = if ($pack.PSObject.Properties.Name -contains 'authority_tier') { [string]$pack.authority_tier } else { 'broad_owner' }
$minimumSignal = if ($minimumCandidateSignalByTier -and $minimumCandidateSignalByTier.PSObject.Properties.Name -contains $packAuthorityTier) { [double]$minimumCandidateSignalByTier.$packAuthorityTier } else { 0.0 }
$authorityEligible = [bool]$routeUsable -and ([double]$candidateSignal -ge $minimumSignal)
$authorityRejectionReasons = New-Object System.Collections.Generic.List[string]
if (-not [bool]$selection._selection_usable) { [void]$authorityRejectionReasons.Add('no_usable_candidate') }
if ($weakFallback) { [void]$authorityRejectionReasons.Add('weak_fallback') }
if ([double]$candidateSignal -lt $minimumSignal) { [void]$authorityRejectionReasons.Add('candidate_signal_below_authority_threshold') }
$selectedCandidateRow = @($selection.ranking | Where-Object { [string]$_.skill -eq [string]$selection.selected } | Select-Object -First 1)
if ($selectedCandidateRow -and -not [string]::IsNullOrWhiteSpace([string]$selectedCandidateRow.authority_guard_reason)) {
    $authorityEligible = $false
    [void]$authorityRejectionReasons.Add([string]$selectedCandidateRow.authority_guard_reason)
}

$packResults += [pscustomobject]@{
    pack_id = Normalize-RouteToken $pack.id
    score = [Math]::Round([double]$score, 4)
    intent = [Math]::Round([double]$intentScore, 4)
    workspace = [Math]::Round([double]$workspaceScore, 4)
    selected_candidate = $selection.selected
    candidate_selection_reason = $selection.reason
    candidate_selection_score = [Math]::Round([double]$selection.score, 4)
    candidate_relevance_score = [Math]::Round([double]$relevanceScore, 4)
    candidate_ranking = @($selection.ranking)
    candidate_top1_top2_gap = [Math]::Round([double]$selection.top1_top2_gap, 4)
    candidate_signal = [Math]::Round([double]$candidateSignal, 4)
    candidate_filtered_out_by_task = @($selection.filtered_out_by_task)
    authority_tier = $packAuthorityTier
    authority_eligible = [bool]$authorityEligible
    authority_rejection_reasons = @($authorityRejectionReasons.ToArray())
    fallback_owner_pack_id = if ($pack.PSObject.Properties.Name -contains 'fallback_owner_pack_id') { [string]$pack.fallback_owner_pack_id } else { $null }
    fallback_owner_skill = if ($pack.PSObject.Properties.Name -contains 'fallback_owner_skill') { [string]$pack.fallback_owner_skill } else { $null }
}

$authorityDecision = Get-AuthorityRouteDecision `
    -Ranked @($ranked) `
    -TaskType $taskType `
    -RequestedCanonical $requestedCanonical `
    -AuthorityPolicy $authorityPolicy

$effectiveTop = $authorityDecision.selected_row
$effectiveSelectedSkill = [string]$authorityDecision.selected_skill
$result.fallback_applied = [bool]$authorityDecision.fallback_applied
$result.fallback_target = [pscustomobject]@{
    pack_id = $authorityDecision.fallback_target_pack_id
    skill = $authorityDecision.fallback_target_skill
}
$result.pre_fallback_top = [pscustomobject]@{
    pack_id = $authorityDecision.pre_fallback_top_pack_id
    skill = $authorityDecision.pre_fallback_top_skill
}
$result.rejected_specialist_reasons = @($authorityDecision.rejected_specialist_reasons)
$result.selected = if ($effectiveTop) {
    [pscustomobject]@{
        pack_id = [string]$effectiveTop.pack_id
        skill = $effectiveSelectedSkill
        selection_reason = [string]$effectiveTop.candidate_selection_reason
        selection_score = [double]$effectiveTop.candidate_selection_score
        top1_top2_gap = [double]$effectiveTop.candidate_top1_top2_gap
        candidate_signal = [double]$effectiveTop.candidate_signal
        filtered_out_by_task = @($effectiveTop.candidate_filtered_out_by_task)
        authority = [pscustomobject]@{
            tier = [string]$effectiveTop.authority_tier
            eligible = [bool]$effectiveTop.authority_eligible
        }
    }
} else {
    $null
}
```

- [ ] **Step 4: Run the arbitration tests and verify they pass**

Run:

```powershell
python -m pytest tests/unit/test_router_contract_authority.py tests/runtime_neutral/test_runtime_route_output_shape.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add packages/runtime-core/src/vgo_runtime/router_contract_authority.py packages/runtime-core/src/vgo_runtime/router_contract_runtime.py scripts/router/resolve-pack-route.ps1 tests/unit/test_router_contract_authority.py tests/runtime_neutral/test_runtime_route_output_shape.py
git commit -m "feat: apply authority fallback before route freeze"
```

## Task 4: Harden First-Wave Packs And Add Real Routing Regressions

**Files:**
- Create: `tests/runtime_neutral/test_router_authority_safe_fallback.py`
- Modify: `config/skill-routing-rules.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py`
- Modify: `tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py`
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`

- [ ] **Step 1: Write the failing real-routing regressions**

Create `tests/runtime_neutral/test_router_authority_safe_fallback.py`:

```python
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
    assert result["fallback_applied"] is True
    assert "missing_authority_keyword" in result["rejected_specialist_reasons"]


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
```

- [ ] **Step 2: Run the real-routing regressions and verify they fail**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_router_authority_safe_fallback.py -q
```

Expected: FAIL because the current config still lets generic publishing / PDF / pipeline language over-inflate the wrong candidates.

- [ ] **Step 3: Tighten first-wave routing rules and replay scripts**

Update `config/skill-routing-rules.json` so `latex-submission-pipeline` uses:

```json
{
  "latex-submission-pipeline": {
    "task_allow": ["planning", "coding", "debug", "research"],
    "authority_keywords": [
      "latexmk",
      "latexindent",
      "chktex",
      "submission zip",
      "latex manuscript",
      "anonymous submission",
      "论文编译",
      "LaTeX manuscript"
    ],
    "supporting_keywords": [
      "build pdf",
      "paper pdf build",
      "github actions",
      "pipeline"
    ],
    "negative_keywords": [
      "runtime logs",
      "translation api failure",
      "sentry alert",
      "check ci logs",
      "线上告警"
    ],
    "requires_positive_keyword_match": true
  }
}
```

Update `config/skill-routing-rules.json` so `systematic-debugging`, `gh-fix-ci`, and `sentry` have explicit authority keywords:

```json
{
  "systematic-debugging": {
    "authority_keywords": [
      "root cause",
      "stack trace",
      "traceback",
      "runtime logs",
      "api failure",
      "报错",
      "异常",
      "故障定位",
      "错误日志"
    ]
  },
  "gh-fix-ci": {
    "authority_keywords": [
      "github actions",
      "workflow logs",
      "ci failed",
      "pipeline failed",
      "检查ci日志"
    ]
  },
  "sentry": {
    "authority_keywords": [
      "sentry alert",
      "sentry issue",
      "production error",
      "线上告警",
      "错误追踪"
    ]
  }
}
```

Trim `config/skill-keyword-index.json` for `latex-submission-pipeline` so its generic keywords stop at true publishing / LaTeX signals:

```json
{
  "latex-submission-pipeline": {
    "keywords": [
      "latex",
      "latexmk",
      "chktex",
      "latexindent",
      "submission zip",
      "latex manuscript",
      "latex paper",
      "LaTeX 论文",
      "论文编译",
      "可投稿 PDF"
    ]
  }
}
```

Append these prompts to `scripts/verify/vibe-pack-regression-matrix.ps1` and `scripts/verify/vibe-skill-index-routing-audit.ps1` with explicit expectations:

```powershell
[pscustomobject]@{
    Name = "debug logs translation api fallback"
    Prompt = "根据错误日志排查翻译接口失败并给出解决方案，检查 runtime pipeline 和 API 请求"
    Grade = "XL"
    TaskType = "debug"
    ExpectedPack = "code-quality"
    ExpectedSkill = "systematic-debugging"
}

[pscustomobject]@{
    Name = "latex submission authority"
    Prompt = "配置 latexmk chktex latexindent 编译 LaTeX manuscript PDF 并打包 submission zip"
    Grade = "XL"
    TaskType = "coding"
    ExpectedPack = "scholarly-publishing-workflow"
    ExpectedSkill = "latex-submission-pipeline"
}
```

- [ ] **Step 4: Run the real-routing regressions and gates**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_router_authority_safe_fallback.py tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py -q
pwsh -NoLogo -NoProfile -File scripts/verify/vibe-pack-regression-matrix.ps1
pwsh -NoLogo -NoProfile -File scripts/verify/vibe-skill-index-routing-audit.ps1
```

Expected: PASS, with the ambiguous debug/logs prompt selecting `code-quality / systematic-debugging` and explicit LaTeX build prompts staying in `scholarly-publishing-workflow / latex-submission-pipeline`.

- [ ] **Step 5: Commit**

```powershell
git add config/skill-routing-rules.json config/skill-keyword-index.json tests/runtime_neutral/test_router_authority_safe_fallback.py tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py scripts/verify/vibe-pack-regression-matrix.ps1 scripts/verify/vibe-skill-index-routing-audit.ps1
git commit -m "test: lock router authority safe fallback regressions"
```

## Task 5: Publish The Governance Note And Run Full Verification

**Files:**
- Create: `docs/governance/router-authority-safe-fallback-governance.md`

- [ ] **Step 1: Write the governance note**

Create `docs/governance/router-authority-safe-fallback-governance.md`:

```markdown
# Router Authority Safe Fallback Governance

日期：2026-05-07

## Purpose

This note documents the first-wave router authority policy that keeps weak narrow specialists out of `selected` and rewrites low-confidence selections to a safer broad owner before confirmation or plan freeze.

## Authority Tiers

| Pack | Authority Tier | Safe Fallback |
| --- | --- | --- |
| `code-quality` | `broad_owner` | `code-quality / systematic-debugging` |
| `integration-devops` | `broad_owner` | `integration-devops / gh-fix-ci` |
| `docs-media` | `broad_owner` | `docs-media / pdf` |
| `scholarly-publishing-workflow` | `narrow_specialist` | `code-quality / systematic-debugging` |

## Rules

- `narrow_specialist` packs must match `authority_keywords` before they can own a route.
- `supporting_keywords` may improve in-pack ranking but cannot replace authority evidence.
- Low-confidence or ineligible top packs stay in `ranked` for audit, but are removed from `selected`.
- `selected` must reflect the post-fallback owner that downstream confirmation and planning will actually use.

## Verification

- `python -m pytest tests/unit/test_router_contract_authority_selection.py -q`
- `python -m pytest tests/unit/test_router_contract_authority.py -q`
- `python -m pytest tests/runtime_neutral/test_router_authority_safe_fallback_contract.py -q`
- `python -m pytest tests/runtime_neutral/test_router_authority_safe_fallback.py -q`
- `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-pack-regression-matrix.ps1`
- `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-skill-index-routing-audit.ps1`
```

- [ ] **Step 2: Run the full verification suite**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_router_authority_safe_fallback_contract.py tests/unit/test_router_contract_authority_selection.py tests/unit/test_router_contract_authority.py tests/runtime_neutral/test_router_authority_safe_fallback.py tests/runtime_neutral/test_runtime_route_output_shape.py tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py tests/runtime_neutral/test_scholarly_publishing_pack_consolidation.py -q
pwsh -NoLogo -NoProfile -File scripts/verify/vibe-pack-regression-matrix.ps1
pwsh -NoLogo -NoProfile -File scripts/verify/vibe-skill-index-routing-audit.ps1
```

Expected: PASS with no ambiguous debug/logs prompt selecting `scholarly-publishing-workflow`.

- [ ] **Step 3: Review the route output for the original failure shape**

Run:

```powershell
python - <<'PY'
from pathlib import Path
import sys

root = Path.cwd()
sys.path.insert(0, str(root / "packages" / "runtime-core" / "src"))
from vgo_runtime.router_contract_runtime import route_prompt

result = route_prompt(
    prompt="根据错误日志排查翻译接口失败并给出解决方案，检查 runtime pipeline 和 API 请求",
    grade="XL",
    task_type="debug",
    repo_root=root,
)

print(result["selected"])
print(result["fallback_applied"])
print(result["pre_fallback_top"])
print(result["rejected_specialist_reasons"])
PY
```

Expected:

```text
{'pack_id': 'code-quality', 'skill': 'systematic-debugging'}
True
{'pack_id': 'scholarly-publishing-workflow', 'skill': 'latex-submission-pipeline'}
['missing_authority_keyword']
```

- [ ] **Step 4: Commit**

```powershell
git add docs/governance/router-authority-safe-fallback-governance.md
git commit -m "docs: explain router authority safe fallback policy"
```

- [ ] **Step 5: Record the finished branch state**

```powershell
git status --short --branch
git log --oneline --decorate -5
```

Expected: clean working tree and a recent sequence containing:

```text
test: define router authority safe fallback contract
feat: guard narrow specialists with authority keywords
feat: apply authority fallback before route freeze
test: lock router authority safe fallback regressions
docs: explain router authority safe fallback policy
```
