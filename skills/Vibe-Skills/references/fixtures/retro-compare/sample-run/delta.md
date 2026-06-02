# CER Compare Report

Generated: $generatedAt

## Scope
- Baseline: $baselineId
- Current: $currentId
- Status: **improved**

## Pattern Delta
- Added: CF-2
- Removed: CF-5
- Common count: 1

## Metric Delta
| Metric | Baseline | Current | Delta |
|--------|----------|---------|-------|
| fallback_rate | 0.27 | 0.14 | -0.13 |
| stability_score | 0.71 | 0.835 | 0.125 |
| context_pressure | 0.79 | 0.62 | -0.17 |
| top1_top2_gap | 0.02 | 0.09 | 0.07 |

## Interpretation
- Negative allback_rate delta is better.
- Positive stability_score delta is better.
- Negative context_pressure delta is better.
- Positive 	op1_top2_gap delta generally means better route separability.
