---
name: security-agentic-triage
description: Use for defensive security workflows that design, assess, or run AI-assisted alert triage, incident investigation, log enrichment, SIEM/EDR query orchestration, security data-governance review, detection-platform planning, investigation transcripts, false-positive reduction, or bounded security-agent tool use.
---

# Security Agentic Triage

Use this skill for defensive security operations where Codex helps collect evidence, enrich alerts, run bounded investigations, and produce auditable conclusions. It adapts Anthropic's CLUE detection-platform patterns for Codex while keeping safety, authorization, and traceability central.

Source basis: https://claude.com/blog/how-anthropic-uses-claude-cybersecurity

## Safety Boundary

This skill is for authorized defensive work only: alert triage, investigation, detection engineering, data-governance review, security tooling, and incident-response support.

Do not provide instructions for unauthorized access, exploitation, credential theft, persistence, evasion, or destructive activity. If a request is ambiguous, narrow it to defensive analysis and ask for authorization context before touching real systems.

## Core Principles

- Enrich isolated alerts with internal context: logs, identity, asset ownership, code, docs, Slack or ticket history, baselines, and recent changes.
- Give Codex bounded tools and data access, but avoid over-prescribing every investigation path. The goal is evidence, not a rigid playbook theater.
- Keep human analysts in control of disposition, escalation, containment, and customer or regulator communications.
- Preserve transcripts, queries, tool calls, source links, and assumptions so every conclusion is auditable.
- Prefer parallel evidence gathering for independent sources, then synthesize with confidence and gaps.
- Treat accuracy as harder to measure than speed. Track disagreements, false positives, missed findings, and analyst overrides.

## Triage Workflow

### 1. Frame the Alert

Capture:

- Alert name, source, severity, time window, affected user/service/asset.
- Detection rule or signal that fired.
- Expected behavior or known maintenance windows.
- Required response SLA.
- Authorized data sources and tools.

If authorization, scope, or data sensitivity is unclear, pause before querying live systems.

### 2. Gather Evidence

Use source-specific queries or connector calls where available. Common evidence:

- Identity and access logs.
- Authentication failures and successful logins.
- Endpoint, network, cloud, and application logs.
- Recent deploys, config changes, and code ownership.
- Tickets, Slack threads, change-management records, and internal docs.
- Historical baseline for the user, service, endpoint, account, or data object.

Record every query and source. Do not summarize away the path taken.

### 3. Enrich and Correlate

Ask:

- Is the behavior expected for this user, service, or team?
- Did the event coincide with a deploy, migration, support action, or incident?
- Are there related events before or after the alert?
- Does the activity match baseline volume, geography, device, account, or timing?
- Are multiple weak signals suspicious in aggregate?

Use parallel subagents only for read-only, independent evidence streams. Give each a narrow scope and ask for file/query/source references.

### 4. Decide a Disposition

Use one of:

- False positive.
- Expected behavior.
- Suspicious needs review.
- True positive.
- Malicious.
- Inconclusive.

Always include:

- Confidence.
- Evidence supporting the disposition.
- Evidence against it.
- Missing data.
- Recommended next action.
- Escalation owner or queue.

### 5. Produce an Audit-Ready Report

Use this shape:

```text
SUMMARY:
DISPOSITION:
CONFIDENCE:
TIME WINDOW:
AFFECTED ENTITIES:
EVIDENCE REVIEWED:
QUERIES OR TOOL CALLS:
KEY FINDINGS:
GAPS:
RECOMMENDED ACTIONS:
HUMAN APPROVAL NEEDED:
```

## Investigation Design

When designing a platform or recurring workflow:

- Start with the analyst pain: repeated context switching, manual correlation, query-language overhead, or alert fatigue.
- Define allowed tools and data boundaries before autonomy.
- Store investigation transcripts as organizational memory.
- Add batch processing for low-confidence signals that humans cannot review manually.
- Run multiple investigation strategies in parallel when the cost is low and the signal is important.
- Review analyst disagreements to tune prompts, tools, detections, and scoring.

## Metrics

Track:

- False-positive rate.
- Alerts enriched per day.
- Tool calls and queries per investigation.
- Time to disposition.
- Analyst override rate.
- Missed-signal reviews.
- Query or tool failure rate.
- Coverage of low-confidence signals previously ignored.

## Anti-Patterns

- Treating speed as proof of correctness.
- Letting Codex run unbounded queries or actions on sensitive systems.
- Returning a confident disposition without source references.
- Collapsing every investigation into a fixed SOAR-style checklist when exploratory context is needed.
- Skipping transcript storage and analyst feedback loops.
- Automating containment, notification, or access changes without explicit human approval.
