# CLI Modularization Plan (Issue #46)

This document tracks incremental modularization of `agent-manager/scripts/main.py`.

## Goals

- keep CLI behavior stable while reducing entrypoint complexity
- make command wiring explicit and testable
- move command implementations into dedicated modules in small merge-safe slices

## Delivery Status

### Completed slices

- **Slice 1**: parser/registry extraction
  - `agent-manager/scripts/cli_parser.py`
  - `agent-manager/scripts/command_registry.py`
- **Slice 2**: lifecycle command extraction
  - `agent-manager/scripts/commands/lifecycle.py`
  - `main.py` wrappers delegate to lifecycle handlers
- **Slice 3-A**: status/schedule handler extraction
  - `agent-manager/scripts/commands/status.py`
  - `agent-manager/scripts/commands/schedule.py`
  - wrapper delegation tests updated
- **Slice 4**: list handler extraction
  - `agent-manager/scripts/commands/listing.py`
  - `main.py` `cmd_list` converted to wrapper delegation
  - list output/filter regression tests added
- **Slice 5**: doctor handler extraction
  - `agent-manager/scripts/commands/doctor.py`
  - `main.py` `cmd_doctor` converted to wrapper delegation
  - doctor command behavior + wrapper delegation tests added

### Completed slice (latest)

- **Slice 8**: schedule run flow decomposition
  - extracted runtime/restart decision and task-message building into helper functions
  - kept `cmd_schedule_run` CLI output and exit-code behavior stable
  - added deeper tests for busy/stuck/error restart boundaries and codex task-file fallback

### Next slice (current target)

- **Slice 9**: schedule run waiting/monitoring maintainability pass
  - isolate wait-loop and tail-capture section into focused helper(s)
  - keep current completion-detection behavior unchanged
  - add regression tests for idle/non-idle terminal state handling

## Migration Notes

- User-facing CLI remains unchanged: command names, arguments, defaults, and outputs are preserved.
- No config/schema migration is required for existing `agents/*.md` files.
- Any future command extension should update:
  - argument definitions in `cli_parser.py`
  - command routing in `command_registry.py`
  - command implementation in `scripts/commands/`

## Validation Baseline

- `python3 -m compileall -q agent-manager`
- `python3 -m unittest discover -s agent-manager/scripts/tests -p 'test_*.py' -q`
- plus targeted wrapper tests for each extracted slice

## Rollback Strategy

- revert only the latest slice commit(s) if behavior drift is detected
- keep wrappers in `main.py` stable so rollback does not change CLI surface
