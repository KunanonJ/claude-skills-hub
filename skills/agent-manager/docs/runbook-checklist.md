# Agent Manager Runbook Checklist (Slice 1)

This runbook is an actionable SOP for day-to-day operation and common failures.

## 0) 30-Minute Newcomer Path

Use this exact sequence from repo root (choose one CLI path first):

```bash
# Installed skill path (pick one that exists in your environment)
CLI="python3 .agent/skills/agent-manager/scripts/main.py"
# CLI="python3 .claude/skills/agent-manager/scripts/main.py"

# If running directly from a cloned repo (not installed skill):
# CLI="python3 agent-manager/scripts/main.py"

$CLI doctor
$CLI list
$CLI start EMP_0001
$CLI status EMP_0001
$CLI monitor EMP_0001 -n 80
$CLI stop EMP_0001
```

Checklist:
- [ ] `doctor` shows tmux available (or prints a clear install hint)
- [ ] `list` returns configured agents without parse errors
- [ ] `start/status/monitor/stop` flow works for at least one enabled agent
- [ ] no unknown command/flag errors in the basic path

## 1) Preflight Before Heartbeat / Schedule Operations

```bash
# Reuse CLI defined in section 0
$CLI doctor
$CLI heartbeat list
$CLI schedule list
```

Checklist:
- [ ] environment healthy (`doctor`)
- [ ] expected heartbeat and schedule jobs are visible
- [ ] target agent is enabled and not misconfigured

## 2) Incident SOP: Heartbeat No ACK

Symptoms:
- `heartbeat run` prints timeout/failure
- no ACK in recent audit events

Commands:

```bash
# Reuse CLI defined in section 0
$CLI heartbeat run EMP_0001 --timeout 30
$CLI heartbeat trace --agent EMP_0001 --limit 20
$CLI status EMP_0001
$CLI monitor EMP_0001 -n 120
```

Checklist:
- [ ] capture latest `HB_ID`
- [ ] verify `send_status` / `ack_status` / `failure_type`
- [ ] verify retry/backoff/fallback behavior matches policy
- [ ] if unresolved, escalate with `HB_ID` + trace output + next owner

## 3) Incident SOP: Session Stuck / Blocked

Symptoms:
- runtime state remains `busy`/`blocked` for too long
- no forward progress in monitor output

Commands:

```bash
# Reuse CLI defined in section 0
$CLI status EMP_0001
$CLI monitor EMP_0001 -n 160
$CLI heartbeat run EMP_0001 --timeout 20
# last resort
$CLI stop EMP_0001
$CLI start EMP_0001 --restore
```

Checklist:
- [ ] record runtime state + reason + elapsed seconds
- [ ] capture last meaningful output lines before restart
- [ ] after restart, confirm status returns to healthy state
- [ ] post incident note with owner and ETA for follow-up prevention

## 4) Periodic Rescue Sweep

Use the built-in rescue printer to generate a lightweight periodic sweep for residual main inbound work:

```bash
# Reuse CLI defined in section 0
$CLI inbound rescue main
```

The printed shell/cron/systemd snippets all converge on the same one-shot rescue command:

```bash
python3 agent-manager/scripts/main.py inbound drain main --once
```

Checklist:
- [ ] rescue path is periodic (cron/systemd timer), not heartbeat-owned
- [ ] restore/start auto-drain stays enabled separately
- [ ] rescue invocation remains one-pass / idempotent
- [ ] residual queued work can be recovered without manual operator typing

### Reading Rescue Outcomes

When `inbound drain main --once` reports `failed`, it means the drain attempted dispatch but could not confirm delivery. Treat this as still-open work: do not count it as handled or replied, and leave it in replay/retry flow unless repeated failures force deeper diagnosis.

When the summary reports `dead_lettered`, it means the item exhausted the normal replay budget and was moved out of the optimistic retry lane. Treat this as manual-triage work, not something a later automatic drain should be assumed to close.

A `handled` event means the consumer-side message path completed after a confirmed delivery attempt. That is useful processing evidence, but by itself it is still not the transport-facing closure signal.

A `replied` event is the operator-facing closure signal: the reply/audit closure was written with reply evidence such as `reply_evidence=transport_ack` and `transport_ack_status=ack`. In other words, `handled` says the message path ran; `replied` says the closure evidence was actually recorded.

## 5) Incident SOP: CI Gate Failure (PR Not Merge-Ready)

Commands:

```bash
# from repo root
python3 -m compileall -q agent-manager
python3 -m unittest discover -s agent-manager/scripts/tests -p 'test_*.py' -v

gh pr checks <PR_NUMBER>
gh pr view <PR_NUMBER> --json mergeable,mergeStateStatus,statusCheckRollup,reviews,comments
```

Checklist:
- [ ] required checks are green on latest head
- [ ] QA posts explicit `PASS` / `FAIL` with commands and evidence
- [ ] PR is mergeable (CLEAN/no conflicts)
- [ ] no unresolved CHANGES_REQUESTED reviews
- [ ] no blocking comments/reviews remain
- [ ] only then mark merge-ready

## 6) Merge Gate (Hard Rule)

A PR is merge-ready only if all are true:
- [ ] CI PASS
- [ ] QA PASS (explicit, evidence-backed)
- [ ] PR is mergeable (CLEAN/no conflicts)
- [ ] no unresolved CHANGES_REQUESTED reviews
- [ ] no blocking comments/reviews

If any item is missing, post a gate-status comment with:
1) missing item
2) owner
3) ETA

## 7) Evidence Comment Template

Use this template on issue/PR threads:

```text
Progress update:
- Scope: <what was executed>
- Commands: <exact commands>
- Result: PASS/FAIL + key evidence
- Gate: CI=<...>, QA=<...>, mergeable=<...>, changes_requested=<...>, blocking comments=<...>
- Owner/ETA: <who does next step by when>
```


## 8) Expected Output Anchors (Quick QA)

Use these as lightweight checks when validating docs/command behavior:

- `doctor` should end with either `✅ Doctor checks passed` or a clear problem count line.
- `schedule sync --dry-run` should print `🔍 Dry run - would sync` and show generated content/no-config message.
- `heartbeat run` failure path should print one of:
  - `❌ Heartbeat failed after recovery policy`
  - `⚠️  Heartbeat unresolved ... applying fallback: fresh`
- `status <agent>` should print `Runtime state:` and `Recent heartbeat:` lines.

## 8) QA Review Checklist for Docs PRs

Before posting `QA Verdict`, verify:

- [ ] all command paths in docs are repo-relative and executable in current tree
- [ ] examples align with current CLI flags/subcommands
- [ ] merge-gate policy text matches team rule (CI PASS + QA PASS + mergeable/no conflicts + no unresolved CHANGES_REQUESTED + no blocking comments)
- [ ] at least one copy-paste command sequence was executed end-to-end

Suggested QA evidence snippet:

```text
QA Verdict: PASS
Commands:
- python3 -m compileall -q agent-manager
- python3 -m unittest discover -s agent-manager/scripts/tests -p 'test_*.py' -v
- gh pr checks <PR>
Evidence:
- docs command paths/flags matched runtime behavior
- gate checklist wording verified
```

## 9) Stale-Issue 30-Minute Recovery Protocol

Use this when heartbeat/dispatch reports an issue stalled for >45 minutes.

Action rules:
- post one repo-visible increment within 30 minutes (commit or PR update)
- include owner + ETA + current blocker in the issue thread
- include evidence link (`commit` / `PR comment` / `CI run`)

Minimum execution sequence:

```bash
# 1) capture current branch / pending changes
 git status -sb
 git branch --show-current

# 2) produce one minimal, reviewable delta
 # (code/docs/test change)

# 3) publish issue update with evidence link
 gh issue comment <ISSUE_NUMBER> --body-file /tmp/update.md
```

Stale-recovery comment template:

```text
Stale recovery update:
- Visible increment: <commit-or-pr-link>
- Scope: <what changed>
- Validation: <commands + result>
- Owner/ETA: <owner>, <time>
- Blocker: <none or explicit blocker>
```
