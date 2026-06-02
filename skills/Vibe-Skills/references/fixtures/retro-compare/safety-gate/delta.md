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
| fallback_rate | 0.26 | 0.15 | -0.11 |
| stability_score | 0.71 | 0.835 | 0.125 |
| context_pressure | 0.81 | 0.63 | -0.18 |
| top1_top2_gap | 0.02 | 0.08 | 0.06 |

## Interpretation
- Negative allback_rate delta is better.
- Positive stability_score delta is better.
- Negative context_pressure delta is better.
- Positive 	op1_top2_gap delta generally means better route separability.
