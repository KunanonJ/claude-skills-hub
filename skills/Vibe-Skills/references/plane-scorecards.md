# Plane Scorecards

## Scorecard Catalog

| Plane / track | Primary score dimensions | Gate anchor |
|---|---|---|
| `memory-runtime-v2` | backend boundary, rollback, cross-plane clarity | `vibe-memory-tier-gate` |
| `prompt-intelligence` | advisory boundary, pattern cards, risk checklist | `vibe-prompt-intelligence-assets-gate` |
| `browserops-provider` | provider fit, replay, confirm discipline | `vibe-browserops-gate` |
| `desktopops-shadow` | supervised execution, replay, rollback | `vibe-desktopops-shadow-gate` |
| `docling-document-plane` | extraction contract, evidence quality, replayability | `vibe-docling-contract-gate` |
| `connector-scorecard` | provider freshness, capability fit, confirm discipline, replay coverage, rollback ready | `vibe-connector-scorecard-gate` |
| `prompt-intelligence-productization` | pattern cards, risk checklist, route hints, confirm hints, advisory-first boundary | `vibe-prompt-intelligence-productization-gate` |
| `cross-plane-task-contract` | canonical task envelope, confirm mode, rollback plan, replay handle | `vibe-cross-plane-task-contract-gate` |
| `cross-plane-replay-ledger` | checkpoint completeness, artifact hash, rollback token, evidence refs | `vibe-cross-plane-replay-gate` |
| `promotion-board-v2` | scorecard bucket visibility, operator readiness, release train readiness, next intake effect | `vibe-promotion-scorecard-gate` |
| `ops-cockpit` | freshness, drift, replay panel health, rollback panel health, SLO visibility | `vibe-ops-cockpit-gate` |
| `rollback-drill` | kill switch quality, fallback stage, drill cadence, operator SOP completeness | `vibe-rollback-drill-gate` |
| `release-train-v2` | stop-ship bundle, board snapshot, rollback evidence, release note readiness | `vibe-release-train-v2-gate` |

## Stage Guidance

| Scorecard bucket | Meaning |
|---|---|
| `shadow_only` | asset exists but does not yet justify rollout discussion |
| `soft_candidate` | governance evidence is good enough for operator review |
| `strict_candidate_review` | evidence is strong enough to justify strict review, not auto-promotion |

## Board v2 Usage

Promotion board v2 should consume these scorecards as advisory evidence.
No scorecard may bypass replay, rollback, or release readiness checks.
