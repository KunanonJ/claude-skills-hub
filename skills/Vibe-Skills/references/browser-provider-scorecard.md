# Browser Provider Scorecard

| Provider | Status | Determinism | Fallback Readiness | Telemetry Readiness | Confirm Bias | Takeover Safety |
|---|---|---|---|---|---|---|
| `api` | `baseline` | `high` | `playwright_available` | `structured_high` | `not_required` | `hard_forbid_takeover` |
| `playwright` | `baseline` | `high` | `chrome_devtools_available` | `structured_high` | `not_required` | `hard_forbid_takeover` |
| `chrome-devtools` | `diagnostic` | `medium` | `playwright_available` | `diagnostic_high` | `not_required` | `hard_forbid_takeover` |
| `turix-cua` | `candidate_soft_only` | `medium` | `playwright_required` | `shadow_evidence_required` | `required` | `hard_forbid_takeover` |
| `browser-use` | `candidate_soft_only` | `medium` | `playwright_required` | `shadow_evidence_required` | `required` | `hard_forbid_takeover` |

## Interpretation

- `api` 与 `playwright` 仍是 BrowserOps baseline；
- `chrome-devtools` 是诊断执行面，不抢默认业务执行；
- `turix-cua` 与 `browser-use` 只能以 `candidate_soft_only` 身份进入 scorecard；
- `browser-use` 的治理含义是 route evidence 补充，而不是第二 orchestrator；
- 任何 `candidate_soft_only` provider 都必须带 `fallback_provider` 与 `confirm_required`。
