# Kill-Switch Decision Tree

The pre-incident playbook for when to flip a feature flag to 0% under user-affecting conditions. The point of writing this down **before** an incident is that incident-time decisions are biased toward inaction; pre-agreed thresholds remove that bias.

**Owner:** [PM + Engineering lead]
**Last reviewed:** 2026-05-22
**Drill cadence:** quarterly in non-prod; semi-annual rehearsal in prod (controlled)

---

## Principles

1. **Pre-agreed thresholds.** Decide before the incident; do not negotiate during.
2. **On-call has authority.** No escalation required for thresholds explicitly listed below. Escalation is for the gray zone.
3. **A flip is reversible.** A flag-off is a config change, not a code revert. Treat it like a fire alarm; pull early and apologize later.
4. **Communicate while you flip, not after.** A flip + Slack message in parallel beats a flip and silence.
5. **Document the flip.** Every flip creates an incident-tag entry. Even "false alarm" flips get documented to inform threshold tuning.

## Decision tree

```
1. Is there customer impact?
   Yes -> continue.
   No  -> Do not flip. Monitor; document; raise an issue for follow-up.

2. Is the impact within the feature-flagged surface?
   Yes -> continue.
   No  -> Use standard incident response. The flag is not the right control.

3. Does the impact match a pre-agreed kill-switch threshold below?
   Yes -> FLIP. Notify in parallel.
   No  -> continue.

4. Is the impact escalating (i.e., would meet a threshold within 15-30 min if untreated)?
   Yes -> FLIP. Document the projection.
   No  -> continue.

5. Is a paid / top-tier customer reporting?
   Yes -> Throttle (lower the ramp) immediately; investigate; flip if not resolved within agreed SLA.
   No  -> continue.

6. Investigate normally. Document the false alarm.
```

## Pre-agreed thresholds

### Tier 1: Critical (checkout, auth, billing, payments, data integrity)

| Metric | Threshold | Action |
|---|---|---|
| Error rate | > 0.5% sustained for 5 min | FLIP |
| p95 latency | > 2x baseline for 5 min | FLIP |
| Customer reports | >= 2 independent reports from paid customers | FLIP |
| Data corruption / loss signal | Any confirmed instance | FLIP IMMEDIATELY |
| Unauthorized access | Any confirmed instance | FLIP IMMEDIATELY + security incident |

### Tier 2: Core (search, signup, dashboard, primary workflow)

| Metric | Threshold | Action |
|---|---|---|
| Error rate | > 2% sustained for 10 min | FLIP |
| p95 latency | > 2x baseline for 10 min | FLIP |
| Customer reports | >= 3 independent reports from paid customers | FLIP |
| Adoption drop | Adoption < 50% of baseline within 24h | Throttle, then flip if no improvement |

### Tier 3: Non-critical (engagement features, secondary surfaces)

| Metric | Threshold | Action |
|---|---|---|
| Error rate | > 5% sustained for 15 min | FLIP |
| p95 latency | > 3x baseline for 15 min | Throttle, then flip |
| Customer reports | >= 5 independent reports | Investigate; flip if pattern is clear |

### AI-feature-specific thresholds

| Metric | Threshold | Action |
|---|---|---|
| Acceptance rate (online sample) | -5% vs baseline over 24h | FLIP |
| Hallucination rate (online sample) | +3% over 24h | FLIP |
| Refusal-on-harmful rate | drops below 95% | FLIP IMMEDIATELY |
| Refusal-on-benign rate | jumps above 15% | FLIP (over-refusal is user-hostile) |
| Cost per interaction | > 150% of budget for 24h | Throttle to fallback model; flip if not resolved |
| Jailbreak success in prod | Any confirmed instance | Patch system prompt; flip to safer variant if patch is not immediate |

## Authority

| Action | Authority |
|---|---|
| Flip Tier 1/2/3 flag based on listed thresholds | On-call engineer (no further approval) |
| Flip during ambiguous incident | On-call + PM (two-person check) |
| Re-enable a flag that was killed | On-call + PM + sponsor (three-person check) |
| Modify a kill-switch threshold | PM + Engineering lead in writing |

## Flip steps (sample)

1. Open the flag service (LaunchDarkly / Statsig / Optimizely / Unleash / internal).
2. Navigate to flag `<flag-name>`.
3. Set rollout to 0%.
4. Confirm in the production dashboard that traffic on the new path is dropping.
5. Post in #channel-incident-name:
   - `KILL-SWITCH ENGAGED on <flag-name> at <time>. Reason: <observed signal>. Impact pre-flip: <metric>. Next: <triage step>.`
6. Open an incident-tag ticket.

## Post-flip protocol

- **First hour:** confirm traffic on the new path is gone. Confirm no continued customer impact.
- **First 24 hours:** root-cause investigation. The owner files a post-mortem.
- **First 72 hours:** decide on re-enable plan. The flag stays off until a fix lands.
- **Re-enable:** never go straight back to the pre-incident rollout %. Restart at stage 1 of the ramp.

## False alarms

A flip that turns out to be a false alarm (threshold met but cause was elsewhere) is still a successful flip. The cost of a false alarm is small; the cost of a missed alarm is large. False alarms are signals to refine thresholds, not to punish the on-call.

Quarterly review of all flips (true + false alarms) feeds into threshold tuning.

## What is NOT a kill-switch trigger

- Negative qualitative feedback (Twitter complaints, single ticket from a free user). Investigate, do not flip.
- Internal-team disagreement about the feature. Resolve through normal channels.
- Stakeholder pressure to flip "just in case." If thresholds are not met, do not flip. Escalate the disagreement, not the flag.
- Single-tenant issue that affects only one customer. Use a tenant-specific override or permission-flag adjustment, not a global flip.

## Practice

Drill this tree quarterly. The drill:
1. PM picks a simulated incident scenario.
2. On-call walks the tree out loud.
3. The team observes whether the on-call would have flipped.
4. Compare to what the team thinks should have happened.
5. Tune the thresholds if they diverge.

Drills surface bad thresholds before real incidents do.

---

## Sign-offs

| Role | Name | Date |
|---|---|---|
| PM | | |
| Engineering lead | | |
| On-call lead | | |
| Customer success / Support (for Tier 1/2) | | |
