# Heartbeat Observability & SLO

This document describes heartbeat audit fields, trace queries, and SLO summary metrics.

## Command Path Baseline

Define one CLI alias first (same baseline as README/SKILL/runbook docs):

```bash
CLI="python3 .agent/skills/agent-manager/scripts/main.py"
# CLI="python3 .claude/skills/agent-manager/scripts/main.py"
# CLI="python3 agent-manager/scripts/main.py"  # cloned repo mode
```

## Audit Log Location

Heartbeat runs append JSONL events to:

- `.claude/state/agent-manager/heartbeat-audit/{agent_id}.jsonl`

## Standard Event Fields

Each JSONL row includes:

- `timestamp` (UTC ISO-8601)
- `agent_id`
- `hb_id`
- `stage` (default: `heartbeat_attempt`)
- `result` (`success` / `failure` / `pending`)
- `duration` (milliseconds)
- `duration_ms` (milliseconds, same as `duration`)
- `send_status`
- `ack_status`
- `failure_type`
- `context_left`
- `session_mode`
- `attempt`
- `recovery_action`

## Trace Query

Use `heartbeat trace` to query audit logs by heartbeat id, agent, and time range.

```bash
$CLI heartbeat trace --agent EMP_0001 \
  --since 2026-02-09T00:00:00Z \
  --until 2026-02-10T00:00:00Z
```

## SLO Summary

Use `heartbeat slo` for daily/weekly summaries.

```bash
$CLI heartbeat slo --window daily
$CLI heartbeat slo --window weekly --agent EMP_0001
$CLI heartbeat slo --json
```

Standalone script:

```bash
python3 agent-manager/scripts/heartbeat_slo.py --window daily
```

## Built-in SLO Thresholds

- Success rate: `>= 99%`
- Timeout rate: `<= 2%`
- Recovery p95: `<= 120000ms`

When a metric breaches threshold, output status is `ALERT`.

## Failure Buckets

`failure_type` is bucketed as:

- `send_fail`
- `no_ack`
- `timeout`
- `blocked`

If `failure_type` is missing, bucket is inferred from `send_status`/`ack_status`.

## 30-Minute Triage Checklist

When heartbeat reliability appears degraded, use this sequence to produce reproducible evidence quickly.

1. Inspect recent trace events (last 20 rows by default):

```bash
$CLI heartbeat trace --agent EMP_0001
```

2. Narrow to a concrete incident window:

```bash
$CLI heartbeat trace --agent EMP_0001 \
  --since 2026-02-10T00:00:00Z --until 2026-02-10T01:00:00Z --json
```

3. Generate SLO summary to detect threshold breach:

```bash
$CLI heartbeat slo --window daily --agent EMP_0001
```

4. If status is `ALERT`, include below fields in issue/PR update:

- affected `agent_id`
- representative `hb_id`
- failed bucket (`send_fail` / `timeout` / `blocked` / `no_ack`)
- latest success rate / timeout rate / recovery p95

## QA Gate Evidence Template

For PR gate closure, QA should provide:

- CI status (`Quality Checks` and any integration jobs)
- local command evidence (trace/slo commands and relevant unit tests)
- PASS/FAIL verdict on the latest head commit
- blocker summary with owner + ETA if verdict is FAIL
