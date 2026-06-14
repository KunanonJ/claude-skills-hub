---
name: ai-feature-prd
description: >
  AI/ML feature PRD scaffolding for the modern AI product manager. Extends the
  standard 8-section PRD with 3 AI-specific sections covering model selection,
  evals, guardrails, data flow, deployment, failure modes, human-in-the-loop,
  AI metrics, ethical review, and cost monitoring.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-execution
  updated: 2026-05-22
  tech-stack: ai-prd, ml-prd, llm-product, evals, guardrails, responsible-ai
---
# AI Feature PRD Expert

## Overview

AI and ML features break the assumptions a standard PRD takes for granted. Outputs are non-deterministic. Quality is statistical, not categorical. The "spec" is half product, half eval suite. A regular PRD that says "Search returns the top result" is replaced by "the assistant returns a helpful, harmless, on-policy answer with a refusal rate under 4% on the golden set, p95 latency under 1.8s, and cost-per-conversation under $0.05."

This skill produces an **AI Feature PRD** that extends the standard 8-section PRD (see `create-prd/`) with three additional sections built for the realities of shipping AI: **AI System Design** (Section 9), **Eval & Safety Plan** (Section 10), and **Operations & Cost** (Section 11). It draws on Andrej Karpathy's "Software 2.0" framing (the model *is* the spec), Anthropic's Responsible Scaling Policy patterns, OpenAI's GPT model-spec style for defining intended behavior, the Reforge AI PM curriculum, and the EU AI Act's risk-tier model that the team has to declare upfront.

This is a template-based skill -- no Python tool. The artifact is a markdown PRD. Pair this with `engineering/llm-cost-optimizer/` for the cost-model math and with `ra-qm-team/eu-ai-act-specialist/` for the regulatory classification.

### When to Use

- **Adding an AI/ML feature to an existing product** -- a search assistant, a recommendation, an auto-summarizer, a copilot, an agent.
- **Building an AI-first product** -- the entire surface area is model-mediated.
- **Migrating a deterministic feature to an LLM** -- replacing a rules-based system or scripted flow with a model.
- **Fine-tuning, prompt-tuning, or RAG decision** -- the PRD captures the architecture rationale so engineering does not relitigate it mid-build.
- **Regulated context** -- EU AI Act, HIPAA, FINRA, FDA SaMD -- the PRD must enumerate the risk tier, the eval bar, and the audit trail before kickoff.

### When NOT to Use

- For a non-AI feature (use `create-prd/` -- the standard 8-section PRD is sufficient).
- For pure model R&D with no product surface (use a research design doc).
- For a one-off internal prompt or batch script that does not ship to users (a Notion page is fine).
- When the AI feature has no production traffic plan -- this PRD assumes you will ship to real users.

## Why a separate AI PRD

A regular PRD assumes a deterministic function: input -> code -> output. AI flips this:

| Standard feature | AI feature |
|---|---|
| Output is the same for the same input | Output varies; same input may produce different responses |
| Quality is binary (correct / incorrect) | Quality is statistical (95% acceptance, 2% hallucination) |
| Tests verify behavior | Evals score quality on golden sets |
| Bugs are fixed in code | Bugs are reduced via prompts, fine-tunes, retrieval, or guardrails |
| Cost is roughly linear with traffic | Cost is per-token, per-call, per-context-window |
| Rollback is a code revert | Rollback may require a different model + prompt + retrieval combo |
| Failure modes are predictable | Failure modes include jailbreaks, hallucination, drift, prompt injection |

The standard PRD has no place to declare a hallucination budget, an eval golden set, a model-fallback strategy, or a refusal policy. This skill adds those sections.

## AI PRD Framework (11 Sections)

Sections 1-8 follow the standard PRD from `create-prd/` (Summary, Contacts, Background, Objective, Market Segments, Value Proposition, Solution, Release). The summary below is abbreviated; full guidance lives in `create-prd/SKILL.md`. Sections 9-11 are AI-specific and are the heart of this skill.

### Section 1: Summary
Two to three sentences. What the AI feature is, who it is for, why it matters now. State the model class plainly ("a Claude Sonnet-4.5 based assistant", "a fine-tuned BERT classifier") -- abstraction here hides cost and risk.

### Section 2: Contacts
PM, Eng Lead, Design Lead, ML/Applied Research Lead, Safety/Trust reviewer, Legal/Compliance reviewer. AI features need more cross-functional sign-off than standard features.

### Section 3: Background
Why now? What changed? Frontier models capable of this task, new internal data, regulatory clarity, customer demand, competitor shipping. Cite the model capability or research that unblocks this -- it dates the PRD honestly.

### Section 4: Objective
Business benefit + customer benefit + 2-4 SMART Key Results. AI KRs should include at least one quality metric (acceptance, win-rate, hallucination) **and** one cost metric.

### Section 5: Market Segments
Jobs-to-be-done, not demographics. Be explicit about which segments are excluded for safety reasons (e.g., minors, healthcare, legal advice contexts).

### Section 6: Value Proposition
What jobs, gains, pains for each segment? Be explicit about the "AI premium" -- what does an AI-mediated experience offer that the deterministic baseline cannot?

### Section 7: Solution
Standard UX, key features (P0/P1/P2), assumptions. Add a **prompt sketch** -- the rough system prompt + tool definitions you intend to use. The full prompt lives in source control, but the PRD shows the contract.

### Section 8: Release
T-shirt sizing, v1 scope, deferred items, success criteria. AI features almost always release on a **shadow -> internal -> canary -> percent-rollout -> GA** ramp; declare the gates between stages.

---

### Section 9: AI System Design

The architectural decisions for the AI subsystem.

**9.1 Model selection rationale**

| Field | Example |
|---|---|
| Primary model | `claude-sonnet-4.5` (Anthropic, via Bedrock) |
| Fallback model | `claude-haiku-4` for cost cap; `gpt-5-mini` for outage |
| Reason chosen | Best quality on our eval set; cheaper than `opus`; safety profile fits |
| Update policy | Re-evaluate primary every 90 days against new releases |
| Vendor risk | Single-vendor risk mitigated by `gpt-5-mini` fallback |

State a primary, a fallback, and a switch trigger. "Model lock-in" is the most expensive technical debt in AI products -- the PRD names the exit ramp.

**9.2 Architecture pattern (Prompt vs Fine-tune vs RAG vs Agent)**

| Pattern | When to choose | Cost profile | Engineering complexity |
|---|---|---|---|
| Prompt only | Behavior steerable via instructions; tasks broadly within base-model capability | Low (per-token) | Low |
| Few-shot / system prompt with examples | Stylistic consistency or format requirements | Low-medium | Low |
| RAG | Output must cite up-to-date private knowledge | Medium (vector store + LLM) | Medium |
| Fine-tune (SFT) | Domain-specific tone, format, or structured-output reliability | Medium-high (training + inference) | Medium-high |
| RLHF / preference fine-tune | Subjective quality the base model gets wrong | High | High |
| Agentic / tool use | Multi-step task requiring tool invocation | High (per-tool-call) | High |

Pick one (or a combination) and **state the rejected alternatives with reasons**. The Reforge AI PM curriculum is explicit: 80% of "we need a fine-tune" decisions are actually "we need better prompts and retrieval first."

**9.3 Data flow**

Diagram or describe: input -> preprocessing -> (retrieval?) -> model -> postprocessing -> output. Explicitly mark:

- What user data leaves the boundary (and to which vendor, under which DPA)
- PII handling (redaction, hashing, exclusion)
- Retention policy (user-input retention, model-output retention, training-opt-out)
- Logging strategy (what is logged, for how long, who can access)

**9.4 Prompt contract**

Sketch the system prompt structure. Production prompts live in source control with versioning, but the PRD captures the contract:

```
Role: <who the assistant is>
Goal: <task>
Inputs: <what context is passed>
Constraints: <refusals, scope, style>
Output format: <schema or example>
Tools: <list with one-line descriptions>
```

### Section 10: Eval & Safety Plan

This is the section that separates a real AI PRD from a thinly-rebadged one.

**10.1 Eval criteria**

| Metric | Target | Method | Cadence |
|---|---|---|---|
| Acceptance rate (golden set) | >= 90% | Human review, 200-item gold set | Weekly during build, monthly post-GA |
| Hallucination rate | <= 2% | Faithfulness check vs source (RAGAS or rubric) | Weekly |
| Refusal rate (on benign inputs) | <= 5% | Held-out benign set | Pre-launch + monthly |
| Refusal rate (on harmful inputs) | >= 98% | Red-team set (200 prompts) | Pre-launch + on prompt change |
| p95 latency | < 1800 ms | Production telemetry | Continuous |
| Cost per interaction | < $0.05 | Token accounting | Continuous |
| Win-rate vs baseline | > 60% on side-by-side | Human pairwise eval | Before each prompt/model change |

Tools commonly used in 2026: **Promptfoo** (offline eval), **Langfuse** or **Anthropic Console** (production trace + eval), **OpenAI Evals**, **Braintrust**, **Weights & Biases Weave**. The PRD names the stack so the team does not relitigate it.

**10.2 Golden set**

- Size: 100-500 examples for v1 (200 is a good default)
- Composition: 70% common cases, 20% edge cases, 10% adversarial
- Ownership: PM owns the set definition; ML owns the run; both review failures weekly
- Versioning: the golden set is in source control; bumps to the set require PR review

**10.3 Guardrails**

| Layer | What it does | Example tools |
|---|---|---|
| Input filter | Strip PII; refuse out-of-scope; classify intent | Regex + classifier; LlamaGuard 3 |
| Pre-prompt | System prompt constraints, refusal instructions | Prompt template |
| In-model | Use models with strong refusal training | Choice of `claude-sonnet-4.5` over base models |
| Output filter | Profanity, PII, jailbreak-success detection | Output classifier; Anthropic content filter |
| Post-response | Citation check (for RAG), schema validation | Programmatic check |
| Human-in-loop | Escalation queue for low-confidence outputs | Slack/Linear ticket on flag |

**10.4 Refusal policy**

Be explicit. The OpenAI Model Spec style is a useful template: state what the assistant should never do, what it should refuse, what it should redirect, and what it should answer plainly. Vague refusal policies produce inconsistent product behavior.

**10.5 Failure modes & graceful degradation**

| Failure | Detection | Response |
|---|---|---|
| Primary model outage | Health-check + error rate | Fail over to fallback model; degrade prompt features |
| Quality regression (acceptance drops) | Weekly eval CI | Roll back prompt/model; notify on-call |
| Hallucination spike | Faithfulness eval + user reports | Tighten retrieval; add citations to prompt |
| Jailbreak success in prod | Red-team monitor + output filter | Add to red-team set; patch system prompt |
| Cost spike | Per-tenant token meter | Throttle; switch tenant to cheaper model |
| Latency spike | p95 alert | Reduce context size; cache; pre-warm |
| Drift on real traffic | Online eval samples | Re-evaluate model; refresh golden set |

**10.6 Human-in-the-loop checkpoints**

Where does a human have to approve, review, or escalate?

- **Hard gate**: high-stakes actions never auto-execute (e.g., emails sent on behalf of a user, account changes).
- **Soft gate**: low-confidence outputs (model self-rated confidence below threshold) go to a review queue.
- **Sampling review**: random 1-5% of production traffic reviewed weekly by domain experts.
- **Escalation triggers**: explicit "I do not know" or repeated user dissatisfaction triggers handoff.

**10.7 Ethical review checklist**

- [ ] Have we identified who could be harmed by this feature?
- [ ] Have we tested with users from affected demographic groups?
- [ ] Have we considered the failure-mode cost (a wrong answer in this domain costs what?)?
- [ ] Is the EU AI Act risk tier declared (Minimal / Limited / High / Unacceptable)? See `ra-qm-team/eu-ai-act-specialist/`.
- [ ] Are we complying with applicable law (GDPR, HIPAA, COPPA, ADA) for the data flow?
- [ ] Have we documented training-data provenance (if fine-tuning)?
- [ ] Are users informed they are interacting with AI?
- [ ] Have we offered a non-AI alternative or escape hatch?

### Section 11: Operations & Cost

**11.1 Cost model**

| Cost line | Formula | Estimate at scale |
|---|---|---|
| Inference (primary) | requests/mo x avg_tokens x $/token | $X/mo at projected MAU |
| Inference (fallback) | <= 10% of primary | $Y/mo |
| Vector store | docs x dimension x $/GB-mo | $Z/mo |
| Eval runs | golden_set_size x model_calls x $/call | $E/mo |
| Human review | reviewer hourly x review hours | $H/mo |
| Logging/observability | events/mo x $/event | $L/mo |

Use `engineering/llm-cost-optimizer/` to model this with sensitivity. The PRD captures the headline number; the optimizer captures the math.

**11.2 Cost monitoring plan**

- Per-tenant token meter; alert at 80% and 100% of monthly budget.
- Daily cost dashboard; weekly variance review.
- Cost-per-successful-interaction (CSI) metric -- divides cost by acceptance rate so a "cheap but bad" model loses.
- Automatic throttle or model-downgrade trigger at 120% of budget.

**11.3 Deployment strategy**

| Stage | Audience | Gate to next |
|---|---|---|
| Shadow | Production traffic mirrored, no user-visible output | Logs reviewed; no crashes; eval bar met |
| Internal | Employees + invited testers | Acceptance >= 85%; no P0 safety incidents in 1 week |
| Canary | 1-5% of users; flagged by `feature-flag-strategy/` | Acceptance >= 90%; no regression vs baseline; cost in range |
| Percent rollout | 10% -> 25% -> 50% | Each step held >= 3 days; metrics within bounds |
| GA | 100% | Stable for 2 weeks; runbook in place |

This pairs directly with `feature-flag-strategy/` for the flag mechanics and `engineering/llm-cost-optimizer/` for the cost gate at each stage.

**11.4 Lifecycle**

- **Model refresh cadence**: re-evaluate primary model against alternatives every 90 days.
- **Prompt versioning**: every prompt change has a PR, an eval delta, and a rollback path.
- **Golden-set refresh**: review and refresh 10-20% of the set quarterly.
- **Deprecation**: when do we deprecate this feature, or migrate to a new model? State the sunset criteria.

## Workflow

1. Start from the standard 8-section PRD in `create-prd/`.
2. Declare the EU AI Act risk tier early; if "High", loop in `ra-qm-team/eu-ai-act-specialist/` before drafting.
3. Fill Sections 9-11 using `assets/ai_feature_prd_template.md`.
4. Define the golden set with the team before any model selection.
5. Define eval criteria and thresholds in Section 10.1 before writing prompts.
6. Use `assets/eval_spec_template.md` to lock the eval contract.
7. Use `assets/guardrail_checklist.md` to walk the safety layers.
8. Review with PM, Eng, ML, Safety/Trust, Legal/Compliance.
9. Lock the cost model with `engineering/llm-cost-optimizer/`.
10. Wire the deployment ramp through `feature-flag-strategy/`.

## Tools

This skill is template-based; no Python tool. The artifact is `PRD-AI-[feature-name].md`.

| Template | Purpose |
|---|---|
| `assets/ai_feature_prd_template.md` | Full 11-section AI PRD template |
| `assets/eval_spec_template.md` | Eval contract: golden set, metrics, cadence, owners |
| `assets/guardrail_checklist.md` | Input/output/HIL guardrail walkthrough |
| `assets/failure_mode_taxonomy.md` | AI-specific failure mode catalogue and mitigations |

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| "Eval bar" is hand-wavy; team can't agree on quality | Section 10.1 used vague thresholds ("good enough") | Force numeric targets: acceptance %, hallucination %, p95 latency ms, $/interaction. Use the golden set as the source of truth |
| PRD says "use the best model" with no vendor named | Section 9.1 dodged the cost/risk question | Name the primary model and version, the fallback, and the switch trigger. Single-vendor lock is named risk, not an unknown |
| Feature ships, then quality drops silently | No online eval; team relies on offline-only golden set | Add a sampling-review process in Section 10.6; instrument production-trace evals (Langfuse, Anthropic Console, etc.) |
| Cost overrun in production | Section 11 ignored token accounting and per-tenant meters | Pre-launch cost model + auto-throttle at 120% of budget; per-tenant token meter from day 1 |
| Legal/Compliance vetoes at the eleventh hour | EU AI Act risk tier was never declared | Declare tier in Section 5/10.7 on day 1; loop in `ra-qm-team/eu-ai-act-specialist/` before model selection |
| Prompt drift; nobody knows the live prompt | No prompt versioning in 11.4 | Move prompts to source control with PR review and eval-delta gate; tag each prompt with a semantic version |
| Engineering builds a fine-tune; PM wanted a prompt | Section 9.2 skipped the alternatives table | Force the team to fill the prompt-vs-RAG-vs-fine-tune table with cost+complexity estimates before committing |

## Success Criteria

- The PRD names a primary model and version, a fallback, and a switch trigger.
- Section 10.1 specifies numeric targets for acceptance, hallucination, refusal (benign and harmful), latency, and cost.
- The golden set exists in source control before the first prompt is written.
- The EU AI Act risk tier is declared and signed off.
- Section 11.1 cost model has a per-tenant alert at 80% and an auto-throttle at 120%.
- Section 11.3 deployment ramp names the gate metric between each stage.
- A reviewer who has never seen this PRD can identify (a) who can be harmed by this feature, (b) what the refusal policy is, (c) what happens when the primary model fails.

## Scope & Limitations

**In Scope:**
- 11-section AI Feature PRD template extending the standard 8-section structure
- Model selection rationale with primary/fallback/switch logic
- Eval criteria with golden set, hallucination, refusal, latency, cost metrics
- Guardrail layers (input, pre-prompt, in-model, output, post-response, HIL)
- Failure-mode taxonomy with detection + response per mode
- Deployment ramp (shadow -> internal -> canary -> percent -> GA) with gates
- Cost model and monitoring plan including per-tenant metering
- Ethical review checklist including EU AI Act tier declaration

**Out of Scope:**
- Building or running the evals (use Promptfoo, Langfuse, Anthropic Console, Braintrust)
- Cost-model arithmetic (use `engineering/llm-cost-optimizer/`)
- Regulatory classification deep dive (use `ra-qm-team/eu-ai-act-specialist/`, `ra-qm-team/iso42001-ai-management/`)
- Standard PRD structure for non-AI features (use `create-prd/`)
- Detailed system architecture (use engineering RFC; the PRD captures the contract, not the implementation)
- Production model training pipelines (MLOps tooling)

**Important Caveats:**
- Model versions move fast. Re-evaluate the primary model every 90 days. A PRD that names `claude-sonnet-4.5` today should expect to swap in `claude-sonnet-5` (or whatever ships) within a year -- the PRD's job is to make that swap a controlled change, not a rewrite.
- A "100% acceptance" target is a tell that the bar is wrong. Real AI features land at 85-95% on hard tasks. If your eval shows 100% on a non-trivial task, your golden set is too easy.
- Cost projections at low traffic underestimate real spend. Model with a 10x traffic scenario before launch.
- The OpenAI Model Spec and Anthropic Acceptable Use Policy evolve. Treat refusal policy as living guidance, not a one-time decision.
- AI features in regulated industries (health, finance, legal) require human-in-the-loop on every high-stakes action. Do not soft-pedal this in Section 10.6.

## Integration Points

| Integration | Direction | Description |
|---|---|---|
| `create-prd/` | Extends | Sections 1-8 follow the standard PRD; this skill adds 9-11 |
| `prfaq/` | Pairs with | Working Backwards PR for AI features should call out the AI premium plainly |
| `north-star-metric/` | Feeds into | NSM should include an AI-quality input (acceptance rate, win rate) |
| `brainstorm-okrs/` | Feeds into | KRs in Section 4 tie to eval targets in Section 10.1 |
| `feature-flag-strategy/` | Pairs with | Section 11.3 ramp executes via feature flags |
| `engineering/llm-cost-optimizer/` | Pairs with | Section 11.1 cost model uses the optimizer's math |
| `ra-qm-team/eu-ai-act-specialist/` | Receives from | Risk tier declaration in Section 10.7 |
| `ra-qm-team/iso42001-ai-management/` | Pairs with | AI management system documentation aligns with PRD lifecycle in 11.4 |
| `discovery/pre-mortem/` | Feeds into | AI-specific failure modes (hallucination, jailbreak, drift) populate the pre-mortem |
| `discovery/identify-assumptions/` | Pairs with | "The base model can do this" is the single biggest AI-PRD assumption; validate before commit |
| `status-update-generator/` | Feeds into | Weekly status surfaces eval drift, cost variance, safety incidents |

## References

- `references/ai-pm-frameworks-guide.md` -- Software 2.0 (Karpathy), OpenAI Model Spec, Anthropic RSP, Reforge AI PM, EU AI Act tiers, Aakash Gupta's AI PM playbook
- `references/eval-design-guide.md` -- Golden sets, pairwise eval, RAGAS, Promptfoo, Langfuse, online vs offline eval, drift detection
