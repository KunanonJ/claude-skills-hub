---
name: zero-downtime-migration
description: Plan a production migration with feature flags, canary, dual-writes, validation gates, rollback triggers, comms plan, and worst-case scenarios. Use when the user is migrating between databases, frameworks, services, schemas, or any production system — "migrate from X to Y", "switch from A to B", "move our database/queue/service".
---

# Zero-Downtime Migration Plan

The user is migrating a production system. Treat this as if real revenue is at stake.

Produce a plan with these sections:

## 1. Pre-migration
- What to verify: data integrity baseline, schema diffs, traffic patterns, dependency map
- What to back up: full backup, point-in-time recovery enabled, snapshot of metrics/dashboards
- What to communicate before starting: stakeholders, on-call, customer-facing notice (or not)

## 2. Rollout strategy
Pick the right pattern for the system:
- **Feature flag**: toggle new vs old path per request/user/percentage
- **Canary deployment**: route 1% → 5% → 25% → 100% with health checks at each step
- **Dual writes**: write to both old and new for a period, compare results
- **Shadow traffic**: send copies of real traffic to new system, don't use response
- **Backfill + cutover**: copy historical data, then atomic switch
- Specify the *gates* between phases (what metric must be green to proceed)

## 3. Validation
- Data integrity: row counts, checksums, sampling-based equality checks
- Behavioral correctness: response comparison (old vs new) for the same input
- Performance: latency p50/p95/p99, error rate, throughput
- What automated checks run continuously during migration
- What gets human eyes before each gate

## 4. Rollback plan
- **Trigger conditions**: explicit thresholds (error rate > X%, latency > Y, data divergence > Z) — *not* "if it feels wrong"
- **Rollback steps**: exact commands/toggles to revert, in order
- **Rollback testing**: when did you last verify the rollback path works?
- **Point of no return**: at what step does rollback stop being possible? Why? Can you push that point later?

## 5. Communication plan
- Pre-migration: who to notify, how far in advance, what to say
- During: status updates cadence, escalation path, war-room channel
- Post: success criteria announcement, postmortem schedule, lessons-learned doc

## 6. Worst-case scenarios
Brainstorm 3-5 ways this goes catastrophically wrong:
- Data loss / corruption
- Long outage outside business hours
- Customer-facing degradation discovered days later
- Cascade failure into other services
For each: detection, blast radius, recovery time, prevention

## Rules
- **No optimism.** Plan for the migration to go wrong somewhere; identify which "somewhere" you can survive.
- **Observable at every step.** If a phase can't be measured, it can't be safely run.
- **Reversible at every step**, until you explicitly accept the point of no return.
- If the user gave you only "migrate from X to Y", ask the constraint questions before planning: traffic volume, data size, downtime tolerance, dual-write feasibility, schema compatibility.
