# CER Compare Report

Generated: $generatedAt

## Scope
- Baseline: $baselineId
- Current: $currentId
- Status: **improved**

## Pattern Delta
- Added: CF-2
- Removed: CF-3
- Common count: 0

## Metric Delta
| Metric | Baseline | Current | Delta |
|--------|----------|---------|-------|
| fallback_rate | 0.3 | 0.12 | -0.18 |
| stability_score | 0.675 | 0.85 | 0.175 |
| context_pressure | 0.85 | 0.6 | -0.25 |
| top1_top2_gap | 0.02 | 0.09 | 0.07 |

## Interpretation
- Negative allback_rate delta is better.
- Positive stability_score delta is better.
- Negative context_pressure delta is better.
- Positive 	op1_top2_gap delta generally means better route separability.
