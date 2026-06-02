# Eval Replay Ledger Contract

## Required Fields

- `recorded_at`
- `task_id`
- `task_type`
- `baseline_route`
- `candidate_route`
- `decision_mode` (`observe_only` / `shadow_compare` / `manual_promote`)
- `evidence`
- `delta_summary`
- `rollback_hint`

## Rule

没有 replay ledger 记录的 adaptive routing 建议，不得进入 promotion 讨论。
