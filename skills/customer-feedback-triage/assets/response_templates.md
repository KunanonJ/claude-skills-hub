# Customer Response Templates

Three response templates (Will-build, Exploring, Won't-build), each with three variants for tone and context. Pick the template based on the triage outcome and the variant based on the originating channel.

The response is sent by the channel originator (support agent, AE, CSM), not by the PM directly. The PM provides the message and the rationale.

---

## Will-build

Use when the cluster is funded, scoped, and on the next 1-2 quarters of roadmap. Be specific about the underlying need, conservative about dates, and concrete about how the customer will hear about it.

### Variant A — Support response (concise)

> Hi {customer_first_name},
>
> Thanks for the feedback on {topic}. The good news: we've heard the same need from several customers and it's planned for an upcoming release. I'll add you to the notification list so you'll hear from us when it ships.
>
> Best,
> {agent_name}

### Variant B — Sales follow-up (deal context)

> Hi {customer_first_name},
>
> Thanks for raising {topic} in our conversation last week. I checked with product — it's on the roadmap for {when, e.g. "this quarter" or "the next couple of months"}, and I'll keep you posted on timing. Happy to set up a brief preview when we have something concrete to show.
>
> Best,
> {ae_name}

### Variant C — CSM proactive (account-tier)

> Hi {customer_first_name},
>
> Following up on the request you raised in our last QBR — the team has prioritized {topic} and we're targeting an upcoming release. I'll make sure your team gets early access when it's ready, and I'll loop you in for any input as we shape the experience.
>
> Best,
> {csm_name}

**Do NOT include in Will-build responses:**
- A specific shipping date unless it is locked and the team will hit it
- Implementation details that may change
- Promises about features adjacent to the one requested

---

## Exploring

Use when the cluster has signal but is not yet scoped. Acknowledge interest, do not commit. If the customer is engaged, invite them into discovery.

### Variant A — Support response (neutral)

> Hi {customer_first_name},
>
> Thanks for the suggestion about {topic}. We're hearing this from a handful of customers and looking into the underlying need more carefully. No commitment yet, but it's on our radar. If you'd like to share more context about how you'd use it, just reply to this thread.
>
> Best,
> {agent_name}

### Variant B — Sales response (deal still open)

> Hi {customer_first_name},
>
> On {topic} — it's something we're exploring but don't have a date for. I don't want to over-commit, so let me share where we are: the product team is interested in the use case, and they'd love to chat with your team to understand it better. Want me to set up a 30-minute call with them?
>
> Best,
> {ae_name}

### Variant C — Customer interview invite (high-signal customer)

> Hi {customer_first_name},
>
> Your feedback on {topic} caught my attention — you're not the first to raise it, and we're starting to look into it more seriously. We're not committing to building anything yet, but I'd value your input: would you be open to a 30-minute conversation with the product team? Your context would help us understand whether and how to move forward.
>
> Best,
> {pm_name}

**Do NOT include in Exploring responses:**
- "We'll definitely build this" — that is a commitment, not exploration
- "We'll never build this" — that's a Won't-build response and should be sent honestly
- A vague timeline that the customer may interpret as a promise

---

## Won't-build

Use when the cluster is out of scope, low-signal, or strategically off-direction. Be respectful, explain the rationale, and where possible offer the closest workaround.

A graceful won't-build is the single biggest trust-building response in the product manager's toolkit. Customers do not need a yes; they need an honest answer.

### Variant A — Support response (general)

> Hi {customer_first_name},
>
> Thank you for the suggestion about {topic}. We've thought about it carefully and have decided not to add it to the roadmap right now. A couple of reasons:
>
> 1. It doesn't fit the direction of the product for the next 2-3 quarters.
> 2. We've heard the request from a small number of customers, and we want to focus our limited capacity on changes that benefit a wider base.
>
> If there's a closely related workaround that would help, let us know and I'll see what we can do.
>
> Best,
> {agent_name}

### Variant B — Sales response (deal context, customer may push back)

> Hi {customer_first_name},
>
> Thanks for raising {topic} in our conversation. I want to be straight with you: it isn't on our roadmap, and I don't want to commit to something I'm not confident the team will build. Here's where the product is heading: {1-2 sentences on direction}. If {topic} is a renewal-critical capability for your team, let's talk about whether {related capability we do offer} works as a workaround, or whether there are aspects of {topic} we should reconsider together.
>
> Best,
> {ae_name}

### Variant C — Strategic decline (high-touch customer)

> Hi {customer_first_name},
>
> I want to be transparent about {topic}: after looking at the underlying need across our customer base, we've decided not to build it in the foreseeable future. The strongest reason is strategic — our product is heading toward {strategic theme}, and {topic} would pull resources in a different direction.
>
> I know this isn't the answer you were hoping for. A few things we can do instead:
>
> - {Workaround 1, if applicable}
> - {Workaround 2, if applicable}
> - Stay in touch — if the underlying need shifts or our roadmap changes, you'll be the first to know.
>
> Thanks for engaging with us this directly. Honest feedback is more valuable than diplomatic feedback, and I appreciate yours.
>
> Best,
> {pm_name or csm_name}

**Do NOT include in Won't-build responses:**
- "Maybe in the future" — if you mean that, send an Exploring response instead
- A blame-shift to engineering capacity ("the engineers can't do it"); own the decision
- A bait-and-switch upsell to a higher tier

---

## Tone guidelines (all templates)

| Do | Don't |
|---|---|
| Use the customer's first name | Use "Dear Valued Customer" boilerplate |
| Acknowledge the underlying job, not just the literal ask | Restate their request word-for-word |
| Be specific about what happens next | Use vague hedges ("we'll see what we can do") |
| Sign with a real name | Sign with a generic team name |
| Reply in the channel the customer used | Force the customer into a new channel for the reply |

## Reply SLA

| Channel | Target response time |
|---|---|
| Support ticket | 1 business day (auto-acknowledge); triage response within 7 business days |
| Sales call note (AE follow-up) | 3 business days |
| NPS verbatim | 14 business days (in a monthly batch) |
| In-app widget | 14 business days |
| Exec ask | 1 business day (acknowledge to exec); 7 business days (response to customer) |
| Social | 24 hours if public-facing; otherwise 7 business days |

## Auditing the program

The PM should sample 20 customer responses per quarter to confirm:

- Tone matches the template guidelines
- Will-build responses do not contain commitments that have slipped
- Won't-build responses include a stated rationale
- The response was sent by the originating channel owner, not deflected to the PM
