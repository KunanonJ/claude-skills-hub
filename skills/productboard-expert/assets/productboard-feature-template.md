# Productboard Feature Template

Recommended structure for the `description` field of a Productboard Feature. Productboard Features are decision artifacts (what we are considering or have decided to build), not implementation artifacts (engineering details live in Jira/Linear). The description should support the prioritization decision and the eventual handoff to engineering.

Paste this template into the Feature description editor and fill in.

---

## Hypothesis

> A single paragraph stating what we believe will happen if we build this Feature. Use the "If we ship X, then Y will improve by Z because W" format.

**Hypothesis:** ...

## Customer evidence

> Linked Insights count: (filled in automatically by Productboard)
>
> Top customer voices in the linked Insights:
> - {Customer / Company name} — {one-line summary of their ask}
> - {Customer / Company name} — {...}
> - {Customer / Company name} — {...}

## Underlying job-to-be-done

> What is the customer trying to accomplish? Phrased as a job, not a feature.

**Job:** When {situation}, I want to {motivation}, so I can {outcome}.

## Success criteria

> How we will know this Feature succeeded after launch. Each metric has a baseline and a target.

| Metric | Baseline | Target | Measurement window |
|---|---|---|---|
| Primary metric | | | |
| Guardrail metric 1 | | | |
| Guardrail metric 2 | | | |

## Scope

### In scope (v1)

- Bullet 1
- Bullet 2

### Out of scope (explicitly deferred)

- Bullet 1 — deferred because ...
- Bullet 2 — deferred because ...

## Dependencies

- **Other Productboard Features**: list with Feature IDs
- **External systems**: (e.g. "Requires the new auth service")
- **Cross-team**: (e.g. "Requires Design Systems team to add new icon")

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| | low/med/high | low/med/high | |
| | | | |

## Open questions

> Unresolved questions that need an answer before this moves to "Planned".

- Question 1
- Question 2

## Decision rationale

> If this Feature is selected for a Release, document why it was prioritized above alternatives. If it is parked or rejected, document why.

(Filled in at the prioritization decision)

## Related Insights (top 5)

> Productboard auto-renders linked Insights below. The PM can call out the most-representative 5 here to make the customer voice obvious in any view.

- ...
- ...

## Linked Jira / Linear ticket

> Once the Feature moves to "Planned", paste the Jira Epic key or Linear Project URL here.

- Jira: PROJ-1234
- Linear: ENG-567

## Owner

- PM: {name}
- Engineering Owner: {name}
- Design Owner: {name}

---

## Lifecycle status

The Feature moves through these statuses (or workspace-customized equivalents):

| Status | Meaning | Exit criteria to next |
|---|---|---|
| **Idea** | Captured; not yet scored | Description filled; Insights linked; Drivers scored |
| **Discovery** | Exploring; user research, prototypes | Hypothesis validated or invalidated |
| **Planned** | Committed to a Release | Engineering ticket created |
| **In Progress** | Being built | Code merged |
| **Done** | Shipped to customers | Success criteria measured |
| **Won't do** | Decided against | Rationale documented |

The status maps to engineering-tracker statuses via the integration. A Feature does not move to "Planned" without a Jira/Linear ticket created.

---

## Quality bar before "Planned"

A Feature should not move to "Planned" status until:

- [ ] Hypothesis statement is written
- [ ] At least 3 customer Insights are linked (or "no evidence" is explicitly documented and accepted)
- [ ] Driver scores are filled in
- [ ] Success criteria with baseline and target are defined
- [ ] At least one P0 risk has a mitigation
- [ ] Dependencies are identified
- [ ] PM, Engineering, and Design owners are named
- [ ] Decision rationale is written

A Feature that hits "Planned" without these is a placeholder, not a commitment.
