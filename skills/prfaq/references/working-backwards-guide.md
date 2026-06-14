# Working Backwards Guide

A reference guide to Amazon's Working Backwards method, the PR/FAQ artifact, and the review choreography that makes it effective.

---

## Origin and intent

The PR/FAQ originated at Amazon in the early 2000s. Jeff Bezos banned PowerPoint in S-Team meetings and required narrative six-page memos, with the PR/FAQ as the first such memo used at product conception. The rule was simple: **start from the customer and work backwards**. The PR/FAQ was a forcing function for clarity of thought before money was spent.

The discipline rests on three premises:

1. **Prose reveals thinking that bullets hide.** Slides let you skip the connectives. Sentences do not.
2. **Future-dating the press release commits you to a customer story.** If you cannot describe the launch convincingly, you do not understand the customer.
3. **The hardest questions deserve written answers, not deferred conversation.** The internal FAQ is where the team is honest with itself.

---

## The PR section: deep dive

### Headline craft

A good headline is **declarative**, **specific to a customer**, and **newsworthy on its merits**. The test: would a real reporter write this headline if they read your full release? If the answer requires hype, the headline is too generous.

| Bad | Why bad | Better |
|-----|---------|--------|
| "Acme launches the future of work" | Vague, hype-led | "Acme launches schedule-sync tool for remote engineering teams" |
| "Acme reimagines collaboration" | Buzzword soup | "Acme cuts cross-timezone standup time from 30 minutes to 4" |
| "Acme announces v3" | Internal version number, no customer | "Acme adds offline mode for field service technicians" |

### Sub-headline craft

The sub-headline names the specific customer and the specific outcome. It is the answer to "who is this for, and what changes for them?" Two sentences maximum.

### The summary paragraph

Future-dated dateline (e.g., "Seattle, March 15, 2027"). Then 3-4 sentences summarizing what was announced. This is the only paragraph a busy reader will read. It must stand alone.

### The problem paragraph

Describe the customer's situation in the customer's own words. Use a specific example or a quantified pain point. Avoid "customers struggle with..." -- name the struggle concretely.

**Example:**

> "For field service technicians working in basements, parking garages, and rural sites, network connectivity is unreliable. Today, a technician completing 14 service calls a day spends an average of 40 minutes re-entering data that failed to sync, and 1 in 20 calls is logged incorrectly because of partial sync state."

### The solution paragraph

Plain language only. Walk through what the customer experiences. No architecture words. No team names.

### The leader quote

A short quote from an internal exec (typically the GM or product owner). It should ladder up to the company strategy in one sentence. Keep it measured -- exec quotes that promise to "change the industry" read as marketing inflation.

### The how-it-works paragraph

3-4 sentences walking through the experience. Show the path, not the architecture. No screenshots, no API names, no internal jargon.

### The customer quote

A made-up but credible quote from a representative customer. It must:

- Name a measurable outcome
- Use language an actual customer would use
- Avoid superlatives ("life-changing", "revolutionary")

**Bad:** "This product has completely transformed how my team works. I cannot imagine going back."

**Good:** "I used to spend the first hour of every morning chasing standup updates across three time zones. Now I see them when I open my laptop. That hour is back."

### The availability line

Pricing model (free, freemium, tier), launch geography, and how to get started in 1-2 sentences. If pricing is not finalized, say "available at launch" rather than fabricating.

---

## The internal FAQ: deep dive

The internal FAQ is where the PR/FAQ proves itself. The 9 required categories exist because each one corresponds to a real reviewer who will ask the question:

| Category | Asked by | Example question |
|----------|----------|------------------|
| Customer & demand | Product, research | What evidence shows customers will pay, not just use? |
| Business model | Finance | What is the 3-year P&L? What is CAC payback? |
| Strategic fit | CEO, exec sponsor | Why us? Why now? Why not in 2 years? |
| Competition | GM, strategy | Who else solves this? Why do we win? |
| Technical feasibility | Eng leadership | What is the riskiest technical bet? How will we retire that risk? |
| Operational | Support, on-call leads | Who supports it 24/7? What is the runbook? |
| Legal, privacy, compliance | Legal, privacy office | What data? What jurisdictions? What new contracts are needed? |
| Risk & failure modes | Exec sponsor | What kills this? What is our exit criterion? |
| Scope & alternative | PM, finance | What did we choose NOT to build, and why? |

### Answer length and tone

- 1-3 paragraphs per answer
- Concise = honest. Verbosity hides uncertainty.
- "We do not know yet, and here is the experiment we will run" is a stronger answer than a confident guess.

### The Bezos question

A useful internal-FAQ habit is to add **"What would we have to believe for this to be true?"** as an explicit Q. The answers form the assumption set the team will validate during build.

---

## The external FAQ: deep dive

The external FAQ is the easiest section. If yours is difficult, the PR is still too abstract. Treat it as a first draft of help center content.

Questions to always include:

- "What is it?"
- "Who is it for?"
- "How is it different from \[obvious alternative\]?"
- "How much does it cost?"
- "How do I get started?"
- "Does it integrate with \[top 2-3 likely integrations\]?"
- "Is my data private and where is it stored?"
- "What languages and regions are supported?"
- "Can I cancel? Refund policy?"

Each answer is 1-3 sentences. Longer answers belong in the help center.

---

## Review choreography

### The "5 readers" rule

Show the full PR/FAQ to 5 readers, each with a different lens:

1. **An exec sponsor** -- challenges strategic fit and business case
2. **An engineer not on the team** -- challenges technical feasibility and operational load
3. **A designer** -- challenges customer experience clarity
4. **A customer-facing rep** (sales, success, support) -- challenges market and competitive framing
5. **One external person** (advisor, peer at another company) -- challenges the obvious-to-insiders blind spots

Each reader submits 3-5 questions. The strongest are added to the internal FAQ; the PR is revised to anticipate any the PR itself should have answered.

### The silent reading meeting

Amazon's S-Team practice: reviewers read the memo in silence at the start of the meeting (20-30 minutes), then discuss. The PM does not present. The memo speaks for itself.

If your culture cannot accommodate silent reading, at minimum: distribute the PR/FAQ 48 hours in advance and forbid in-meeting walkthroughs.

### The kill criterion

A PR/FAQ that survives 3 review rounds without substantive change is suspicious -- either the reviewers are not engaging, or the idea is too small to merit a PR/FAQ. A PR/FAQ that cannot survive 3 rounds is the system working correctly -- a weak idea was killed cheaply.

---

## Anti-patterns

| Anti-pattern | What it looks like | What to do instead |
|--------------|-------------------|--------------------|
| The reverse-engineered PR/FAQ | Team already decided what to build; PR/FAQ written to justify it | Write the PR/FAQ before the design sprint |
| The bullet-point smuggle | Markdown bullets in the press release | Strip all bullets from the PR. Prose only |
| The internal FAQ "softball" | Easy questions with confident answers | Force the 9 categories; require 1 uncomfortable question per reviewer |
| The 12-page PR/FAQ | Length used as a proxy for rigor | Cap at 6 pages. If longer, cut. Length hides weak thinking |
| The marketing-team PR draft | Treating the PR as comms copy | Remind the team this is internal; comms will write a different PR at launch |
| The PR/FAQ that never updates | Written once, filed, forgotten | Re-read at each milestone; revise when answers change |

---

## Handoff

After PR/FAQ approval, the artifact feeds:

- **PRD** -- The PR becomes the prologue; the internal FAQ becomes the risk and assumption sections.
- **Roadmap** -- The launch date in the PR informs horizon placement (Now / Next / Later).
- **OKRs** -- The customer outcome in the PR becomes the candidate Objective; quantified claims become Key Results.
- **Roadmap communication** -- The PR is the seed of the executive-variant roadmap narrative.

---

## Further reading

- Bezos shareholder letters (1997-2020) discuss the narrative memo discipline.
- "Working Backwards" by Colin Bryar and Bill Carr documents the practice in detail.
- The original 6-page memo format predates the PR/FAQ and is still used for non-product decisions.

---

**Last Updated:** 2026-05-21
