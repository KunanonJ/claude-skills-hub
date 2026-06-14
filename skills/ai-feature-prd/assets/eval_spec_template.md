# Eval Spec: [Feature Name]

A self-contained contract for how this AI feature is evaluated. This is the **spec** in the Software 2.0 sense -- the document that tells engineering, ML, and safety what "shipped" means.

**Owner:** [PM name]
**ML co-owner:** [Name]
**Safety reviewer:** [Name]
**Last reviewed:** 2026-05-22
**Status:** Draft / Locked / Superseded

---

## 1. Feature scope

| Field | Value |
|---|---|
| Feature | |
| Primary model | |
| Fallback model | |
| Architecture | Prompt / RAG / Fine-tune / Agent |
| User-visible? | Yes / No (shadow only) |

## 2. Golden set

| Field | Value |
|---|---|
| Path | [Source-control location, e.g. `evals/<feature>/golden_v1.jsonl`] |
| Size | [N] examples |
| Composition | [70/20/10 or custom] |
| Labelers | [Names; minimum 2 per example] |
| Inter-rater agreement | [Cohen's kappa or % agreement] |
| Refresh cadence | Quarterly, replace 10-20% |
| Versioning | Bumps require PR review |

**Example row format:**

```json
{
  "id": "gold-001",
  "category": "common | edge | adversarial",
  "input": "...",
  "expected_behavior": "...",
  "must_contain": [],
  "must_not_contain": [],
  "rubric": "rubric_name_v1"
}
```

## 3. Red-team set

| Field | Value |
|---|---|
| Path | [Source control location] |
| Size | [N] prompts |
| Categories | Direct harm / role-play harm / prompt injection / jailbreak / privacy probe / PII extraction |
| Refresh cadence | On every primary-model change; quarterly otherwise |
| Pass criteria | Refusal rate >= 98% |

## 4. Metric targets

| Metric | Target | Method | Tool | Cadence |
|---|---|---|---|---|
| Acceptance rate (golden) | >= [%] | Rubric / pairwise | Promptfoo / Braintrust / human review | Weekly |
| Hallucination rate | <= [%] | Faithfulness rubric | RAGAS / custom | Weekly |
| Faithfulness (RAG) | >= [%] | RAGAS | RAGAS | Weekly |
| Refusal rate (benign) | <= [%] | Benign set | Promptfoo | Pre-launch + monthly |
| Refusal rate (harmful) | >= [%] | Red-team set | Promptfoo + manual | Pre-launch + on prompt change |
| Format compliance | >= [%] | Schema validator | Custom | Every release |
| p95 latency | < [ms] | Production telemetry | Langfuse / Datadog | Continuous |
| Cost per interaction | < $[X] | Token accounting | Per-tenant meter | Continuous |
| Win-rate vs baseline | > [%] | Pairwise | Braintrust / manual | Before each change |
| User thumbs-up rate | >= [%] | User feedback | In-product | Continuous |
| Escalation rate | <= [%] | Tag handoffs | CRM / in-product | Continuous |

## 5. Eval pipeline

### Offline (CI / pre-release)

```
PR opened -> CI runs golden eval -> Posts delta report on PR -> 
Reviewer reads acceptance/hallucination/cost delta -> Merge or block
```

| Step | Tool | Trigger |
|---|---|---|
| Run golden set | [Promptfoo] | Every PR touching prompts/ or models/ |
| Run red-team set | [Promptfoo] | Every PR + nightly |
| Generate delta vs main | [Custom or platform] | PR |
| Post comment to PR | [Custom or GitHub Action] | PR |

### Online (production)

| Step | Tool | Cadence |
|---|---|---|
| Sample N% of traces | [Langfuse / Anthropic Console] | Continuous (1-5%) |
| Score with LLM-as-judge | [Same platform] | Continuous |
| Human-review subset | [Internal queue] | Weekly |
| Dashboard | [Grafana / Looker / Hex] | Continuous |
| Alert on regression | [Alertmanager] | Threshold-based |

## 6. Alert thresholds

| Signal | Warning | Critical |
|---|---|---|
| Acceptance rate drop | -2% over 24h | -5% over 24h |
| Hallucination rate rise | +1% over 24h | +3% over 24h |
| Refusal-on-benign rise | +2% over 24h | +5% over 24h |
| Refusal-on-harmful drop | -1% over 24h | -3% over 24h |
| p95 latency | > 1500ms | > 1800ms |
| Cost per interaction | > $0.04 | > $0.05 |
| Thumbs-up rate drop | -3% over 7d | -5% over 7d |

## 7. Review cadence

| Cadence | Attendees | Output |
|---|---|---|
| Weekly | PM + ML + Eng | Golden-set deltas, drift, top failures |
| Bi-weekly | Add safety reviewer | Red-team status, refusal-policy edits |
| Monthly | Add Legal/Compliance | Compliance posture, incident review |
| Quarterly | All + sponsor | Model refresh decision, golden-set refresh |

## 8. Sign-off

Eval spec is **locked** when all of the following are signed:

| Role | Name | Date |
|---|---|---|
| PM | | |
| ML lead | | |
| Safety reviewer | | |

Changes to a locked spec require a versioned new spec (v2) and re-sign-off.
