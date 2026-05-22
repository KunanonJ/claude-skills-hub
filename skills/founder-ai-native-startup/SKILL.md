---
name: founder-ai-native-startup
description: Use when helping founders or operators validate startup ideas, build AI-native MVPs, define product-market-fit evidence, plan launch or scale stages, control AI-generated technical debt, write founder operating systems, create agentic workflows, evaluate startup risk, or decide what Chat/Codex/automation should do at each startup stage.
---

# Founder AI-Native Startup

Use this skill to turn startup work into staged evidence gates before building. It adapts Anthropic's founder playbook for Codex: Idea, MVP, Launch, and Scale each need different outputs, exit criteria, failure-mode checks, and verification.

Source basis: https://claude.com/blog/the-founders-playbook

## Core Principles

- Keep sense-making ahead of building. AI makes execution cheap, so evidence gates matter more, not less.
- Classify the current stage before giving advice: Idea, MVP, Launch, or Scale.
- Treat Codex as an orchestrator and implementation partner, not a substitute for founder judgment.
- For product or code changes, preserve the user's TDD/project rules and write tests before production code when behavior changes.
- Keep persistent context legible from day one: specs, architecture decisions, scope, security assumptions, and operational playbooks.
- Separate evidence, assumptions, and guesses. Do not present market claims, customer intent, revenue potential, or security posture as verified unless evidence exists.

## Stage Workflow

### 1. Idea Stage

Goal: prove problem-solution fit before building.

Check for:

- A specific user segment and problem.
- Frequency, severity, and current workaround.
- Competitive alternatives and why they fail.
- Real customer discovery evidence, not only founder intuition.
- A solution hypothesis that matches the discovered problem, not the original fantasy.

Exit only when:

- The problem is real, specific, and frequent enough.
- The target user and market are named clearly.
- The solution addresses the actual problem revealed by validation.
- There is enough qualitative signal to justify an MVP.

Default outputs:

- Problem hypothesis.
- ICP and discovery questions.
- Competitive landscape.
- Disconfirming-evidence checklist.
- No-build recommendation if validation is too weak.

### 2. MVP Stage

Goal: ship the smallest focused product that creates real usage evidence without compounding AI-generated technical debt.

Before implementation, require:

- MVP scope document.
- Architecture constraints and non-goals.
- Critical user journey.
- Data/security assumptions.
- Test strategy and rollback path.

Exit only when there is genuine product-market-fit evidence, such as retention, revenue, referral, or repeated usage from a specific group. Early launch spikes, friends, press, investor intros, and novelty do not count by themselves.

Guardrails:

- Reject zero-friction scope creep. Add only what tests the core value proposition.
- Do a first-pass security review before real users or real data touch the system.
- Document technical debt intentionally with owner, risk, and payoff trigger.
- Prefer narrow vertical slices over broad feature inventory.

### 3. Launch Stage

Goal: turn early traction into a repeatable business and remove founder bottlenecks.

Check for:

- Repeatable acquisition channels with measurable CAC, LTV, and payback assumptions.
- Production readiness: reliability, observability, security, compliance, and support.
- Operational tasks the founder still personally remembers, formats, routes, or approves.
- Technical debt that starts to break under production workload.

Default outputs:

- Launch readiness audit.
- Technical debt and test-coverage plan.
- Founder bottleneck inventory.
- Agentic workflow candidates for support, triage, reporting, sprint planning, and customer feedback.

### 4. Scale Stage

Goal: make growth, operations, and technical systems auditable, transferable, and enterprise-ready.

Check for:

- Documented institutional knowledge that no longer lives only in the founder's head.
- Mature GTM motion beyond founder-led selling.
- Support playbooks, SLAs, incident response, monitoring, and customer-facing docs.
- Compliance, finance, legal, hiring, and procurement workflows.
- A defensible moat from product depth, integrations, data, and workflows.

Default outputs:

- Scale operating-system map.
- Enterprise-readiness checklist.
- GTM function plan.
- Delegation matrix: founder-only, human-owned, agent-assisted, fully automated.

## Planning Template

Use this for non-trivial founder work:

```text
STAGE: Idea | MVP | Launch | Scale
GOAL: one sentence
CURRENT EVIDENCE: verified signals only
ASSUMPTIONS: explicit unknowns
FAILURE MODES: premature build, false PMF, scope creep, debt, security, founder bottleneck
NEXT TEST: smallest evidence-producing action
OUTPUT: doc, prototype, report, workflow, code change, or dashboard
VERIFICATION: customer evidence, metric, test, review, smoke check, or security check
ROLLBACK: how to undo or stop the experiment
```

## Anti-Patterns

- Building before the problem is validated.
- Treating an attractive prototype as product-market fit.
- Adding features because Codex can build them quickly.
- Shipping AI-generated code without scope, architecture, tests, or security review.
- Letting founder-only context stay undocumented.
- Automating decisions that still require founder judgment or customer empathy.

## Handoff Shape

End with:

- Stage classification and confidence.
- What evidence exists and what is still assumed.
- The next smallest test or build slice.
- Risks and explicit stop conditions.
- Verification performed or still needed.
