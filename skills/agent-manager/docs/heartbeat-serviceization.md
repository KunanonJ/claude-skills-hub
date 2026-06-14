# Heartbeat Serviceization (Issue #47 Slice-1)

This slice extracts heartbeat state/recovery logic into dedicated service modules.

## Modules

- `agent-manager/scripts/services/heartbeat_state_machine.py`
  - ack/failure classification
  - retry eligibility rules
  - standardized reason-code mapping

- `agent-manager/scripts/services/heartbeat_service.py`
  - recovery policy parsing
  - heartbeat attempt execution
  - fallback restart helper
  - failure notification helper

## Main CLI Role

`cmd_heartbeat_run` remains orchestration-only:

- resolve config and runtime context
- call heartbeat service helpers
- append audit events
- route success/failure exit codes

## Observability Hook

Heartbeat audit JSONL now includes:

- `failure_type`
- `reason_code`

`reason_code` provides a stable classifier for dashboards/alerts.

## Rollback Path

Serviceization is adapter-based:

- public helper names in `main.py` stay unchanged (`_run_heartbeat_attempt`, `_parse_heartbeat_recovery_policy`, etc.)
- wrappers delegate to service modules
- rollback can revert wrappers to inline logic without changing CLI surface
