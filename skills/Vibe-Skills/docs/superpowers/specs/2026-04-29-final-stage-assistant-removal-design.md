# Final Stage Assistant Removal Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-29
Status: Approved for implementation planning

## Context

The current routing simplification goal is to keep the public six-stage Vibe runtime unchanged while simplifying skill usage inside routed work. The desired skill model is:

```text
candidate skill -> selected skill -> used / unused
```

The pack manifest scan found no internal manifest reference inconsistency: defaults, route authority candidates, and stage assistant candidates all point to existing skill IDs. The remaining mismatch is semantic: two packs still keep non-empty `stage_assistant_candidates`.

Current residual stage assistant entries:

| pack | residual stage assistant |
| --- | --- |
| `code-quality` | `requesting-code-review` |
| `data-ml` | `preprocessing-data-with-automated-pipelines` |

These entries preserve the older "helper / stage assistant" layer that the cleanup is trying to remove.

## Goals

1. Remove the last active `stage_assistant_candidates` usage from `code-quality` and `data-ml`.
2. Preserve the six-stage Vibe runtime and existing router architecture.
3. Convert any retained skill into an explicit direct owner of a clear user task.
4. Avoid treating `route_authority_candidates` as a second execution model. It remains a compatibility/config allowlist for direct skill selection.
5. Avoid physical deletion of asset-bearing skill directories until their useful content has been reviewed or migrated.

## Non-Goals

- Do not redesign canonical Vibe stages.
- Do not introduce primary/secondary/helper/stage-assistant replacement terminology.
- Do not batch-fix zero-route-authority long-tail packs in this change.
- Do not prune large packs such as `bio-science`, `research-design`, or `docs-media` in this change.
- Do not physically delete `preprocessing-data-with-automated-pipelines` in the first implementation pass, because it contains `assets`, `references`, and `scripts`.

## Design

### Pack Manifest Semantics

After this cleanup, both target packs must have:

```text
stage_assistant_candidates: []
```

A skill that remains in a pack must be in the normal candidate surface and, if it can own a user request, in `route_authority_candidates`. Selection then means the skill is directly eligible for use; non-selection means unused.

### `code-quality`

`requesting-code-review` should be retained and converted from stage assistant to direct route authority.

Its direct task boundary is:

```text
Prepare and request a code review after implementation or before integration.
```

It must not own actual code-review findings. That stays with `code-reviewer`.

It must not own review-feedback repair. That stays with `receiving-code-review`.

Required boundary examples:

| user task | expected owner |
| --- | --- |
| "请帮我审查这次代码改动有没有问题" | `code-reviewer` |
| "请帮我准备发起一次代码审查，整理 review 请求材料" | `requesting-code-review` |
| "我收到了 code review 意见，请帮我处理" | `receiving-code-review` |

The `requesting-code-review` skill text should remove historical "stage assistant" wording and describe itself as a direct workflow skill for preparing review requests.

### `data-ml`

`preprocessing-data-with-automated-pipelines` must stop being a stage assistant. Its directory is asset-bearing and should not be physically deleted in this pass.

Implementation must apply this decision rule:

1. If the skill has a distinct direct user task after content review, keep it as a route authority.
2. If the skill is only a thin overlap with `ml-pipeline-workflow`, `scikit-learn`, or `ml-data-leakage-guard`, remove it from `data-ml` routing and document later migration/deletion work.
3. In both cases, it must not remain in `stage_assistant_candidates`.

The intended direct task boundary, if retained, is:

```text
Build a repeatable ML data preprocessing pipeline for cleaning, encoding, transforming, and validating input data.
```

It must not own full ML workflow planning. That stays with `ml-pipeline-workflow`.

It must not own general scikit-learn modeling. That stays with `scikit-learn`.

It must not own leakage auditing. That stays with `ml-data-leakage-guard`.

Required boundary examples:

| user task | expected owner |
| --- | --- |
| "我需要一个完整机器学习建模流程，包括训练和评估" | `ml-pipeline-workflow` or `scikit-learn` |
| "请帮我做自动化数据清洗、编码、转换、验证流水线" | `preprocessing-data-with-automated-pipelines` if retained |
| "请检查训练集和测试集是否发生数据泄漏" | `ml-data-leakage-guard` |

## Files Expected To Change During Implementation

The implementation plan should inspect and update only the required subset of:

- `config/pack-manifest.json`
- `config/skill-keyword-index.json`
- `config/skill-routing-rules.json`
- `config/skills-lock.json`
- `bundled/skills/requesting-code-review/SKILL.md`
- `bundled/skills/preprocessing-data-with-automated-pipelines/SKILL.md`
- focused runtime-neutral tests for the two pack boundaries
- a concise governance note under `docs/governance/`

No implementation file should be edited until an implementation plan is written and approved.

## Verification Design

Focused verification should prove:

1. `config/pack-manifest.json` has no non-empty `stage_assistant_candidates`.
2. `code-quality` routes review-request preparation to `requesting-code-review`.
3. `code-quality` still routes actual review to `code-reviewer`.
4. `code-quality` still routes received review feedback to `receiving-code-review`.
5. `data-ml` no longer exposes preprocessing as a stage assistant.
6. If preprocessing is retained, preprocessing-heavy prompts select it directly without stealing broad ML modeling prompts.
7. If preprocessing is removed from routing, broad ML prompts still route to `ml-pipeline-workflow` or `scikit-learn` and leakage prompts still route to `ml-data-leakage-guard`.

Expected command families:

```powershell
python -m pytest <focused runtime-neutral tests> -q
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
```

The exact focused test names should be selected in the implementation plan after inspecting existing tests.

## Acceptance Criteria

- `stage_assistant_candidates` is empty for every pack in `config/pack-manifest.json`.
- No retained target skill describes itself as a stage assistant, helper, secondary expert, or auxiliary expert.
- `requesting-code-review` has a clear direct task boundary.
- `preprocessing-data-with-automated-pipelines` is either retained as a direct owner with a clear boundary or removed from active `data-ml` routing with deletion deferred.
- The governance note reports before/after counts, retained direct owners, removed stage-assistant semantics, and route probes.
- Focused tests and routing/config gates pass before implementation is called complete.
