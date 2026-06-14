---
name: prfaq
description: >
  Amazon Working Backwards PR/FAQ generator that forces customer-outcome
  thinking before any code is written. Produces a press release, an internal
  FAQ, and an external FAQ as a single decision artifact.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-execution
  updated: 2026-05-21
  tech-stack: working-backwards, pr-faq, amazon-method, narrative-memo
---
# PR/FAQ (Working Backwards) Expert

## Overview

The PR/FAQ is Amazon's "working backwards" artifact: before any team is funded to build a product, the PM writes a future-dated press release and an FAQ that anticipates every hard question. The discipline forces clarity on customer, problem, and outcome before a single design decision is made. If the team cannot write a compelling, credible PR/FAQ, the idea is not ready.

This skill is the standalone, deeper treatment of the technique previously bundled inside `create-prd/`. Use it when you need a high-fidelity narrative artifact for funding review, executive sponsorship, or a "should we even do this?" decision. The output is a single Markdown document with three sections: the press release, an internal FAQ (the questions your CFO, lawyer, and head of engineering will ask), and an external FAQ (the questions customers and press will ask).

The PR/FAQ is not a PRD substitute -- it precedes the PRD. It also is not a marketing draft -- it is an internal alignment document that happens to take the shape of a press release. The "Press Release Test" is the bar: if the press release does not pass scrutiny as something a customer would actually find newsworthy, the idea needs more work.

### When to Use

- **Funding gate** -- A new initiative needs executive approval before spend.
- **Concept stress-test** -- An idea is exciting internally but you suspect the customer narrative is weak.
- **Cross-team alignment** -- Engineering, design, marketing, and exec sponsors need a single document they all agree on before kickoff.
- **Portfolio bake-off** -- Two or three competing ideas need apples-to-apples comparison; PR/FAQs reveal which has the strongest customer story.
- **Reframe a stalled project** -- A product in flight has lost the customer plot; rewriting the PR/FAQ surfaces what was lost.

### When NOT to Use

- For an incremental feature on an existing product (use `wwas/` or `job-stories/` instead).
- When the team already has a signed-off PRD and is mid-build.
- For pure technical infrastructure with no end-customer narrative.

## The Working Backwards Method

Amazon's rule: **start from the customer experience and work backwards to the technology**. The PR/FAQ enforces this by making you write what the customer will see and feel before you write what you will build.

### The three artifacts

| Artifact | Audience | Purpose | Length |
|----------|----------|---------|--------|
| **Press Release (PR)** | Imagined customer/press | State the customer-facing news in plain language | 1 page |
| **Internal FAQ** | Exec sponsor, finance, legal, eng leadership | Surface every hard internal question and answer it honestly | 2-4 pages |
| **External FAQ** | Customers, partners, support reps | Anticipate the questions a buyer or user would ask | 1-2 pages |

A complete PR/FAQ is typically 4-7 pages. If yours is longer, the idea has not been compressed enough. If shorter, you have probably skipped hard questions.

## Part 1: The Press Release

### Required structure (in order)

1. **Headline** -- A single declarative sentence a real journalist would write. No internal codenames. No "next-generation" or "revolutionary."
2. **Sub-headline** -- One sentence naming the specific customer and the specific benefit.
3. **Summary paragraph** -- Location, date (future-dated to launch), and a 3-4 sentence summary of what was announced.
4. **Problem paragraph** -- The customer pain in the customer's own words. Cite the magnitude.
5. **Solution paragraph** -- How the product solves the pain. Plain language only.
6. **Leader quote** -- One sentence from an internal exec. Why this matters for the company.
7. **How it works** -- 3-4 sentences walking through the experience. No screenshots, no API names.
8. **Customer quote** -- A made-up but credible quote from a representative customer. Must describe an outcome, not a feature.
9. **Availability** -- Pricing model (if known), launch geography, how to get started.

### The Press Release Test

After writing, hand the PR to someone outside the team. Ask three questions:

1. **Who is this for?** They should answer with a specific persona, not "everyone."
2. **What problem does it solve?** They should answer in plain language.
3. **Would you click "Learn More" if you saw this?** Honest answer required.

If any answer is weak, the product concept is weak. Iterate the PR before writing a line of code.

### Common failure modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| Feature-led headline | "X launches AI-powered widget" | Rewrite from the customer-benefit angle |
| Vague customer | "for businesses" | Name the segment and the use case |
| Buzzword stuffing | "next-generation, seamless, cutting-edge" | Strike every adjective that does not add information |
| Internal jargon | Product names, team names, project codes | Use only words a customer would use |
| Implausible quote | "This will transform our entire industry" | Use a measured, outcome-specific quote |
| Missing magnitude | "saves time" | Quantify: "from 4 hours to 12 minutes" |

## Part 2: The Internal FAQ

The internal FAQ is where most PR/FAQs fail. It is also where the strongest PR/FAQs prove themselves. Write 10-20 Q&A pairs covering the hardest questions an exec sponsor, CFO, head of legal, or head of engineering will ask in the review meeting.

### Required question categories

Every internal FAQ must answer at least one question from each category:

- **Customer & demand** -- How big is the addressable problem? What evidence do we have that customers want this?
- **Business model** -- How do we make money? What is the unit economics? What is the cost to build vs. expected return?
- **Strategic fit** -- Why us? Why now? How does this compound with the rest of the portfolio?
- **Competition** -- Who else is solving this? Why will we win?
- **Technical feasibility** -- Can we build this? What is the riskiest technical bet?
- **Operational** -- Who supports it? What happens when it breaks? Does it require new on-call coverage?
- **Legal, privacy, compliance** -- Are there regulatory implications? What data do we collect?
- **Risk & failure modes** -- What is the worst-case scenario? How would we know it failed? What do we do if it does?
- **Scope & alternative** -- What are we explicitly NOT doing in v1? What is the cheapest alternative considered, and why was it rejected?

### Answer style

- Each answer is 1-3 paragraphs. Concise is honest; verbose hides uncertainty.
- Quantify wherever possible. "Large market" is meaningless; "$4.2B SAM, $310M SOM" is auditable.
- When you do not know, say "We do not know yet, and here is how we will find out." This is more credible than fabrication.
- Cite the source for every claim (research interview count, third-party report, internal data pull).

### Sample internal Qs (use as starting prompts)

1. What is the customer problem in one sentence, and how many customers experience it?
2. What is our evidence that customers will pay for this, not just use it?
3. What is the v1 budget and what is the 3-year P&L projection?
4. What is the build-vs-buy analysis? Did we evaluate at least two third-party alternatives?
5. What is the single biggest technical risk, and what is our plan to retire it?
6. Which existing products will this cannibalize, and is that acceptable?
7. What does success look like in 6 months? In 18 months? What metric tells us to kill it?
8. What is the smallest version we could ship to start learning?
9. Who owns this product 12 months from launch? Is that team committed?
10. What is the regulatory or privacy posture, especially under GDPR/CCPA/sector-specific rules?

## Part 3: The External FAQ

The external FAQ anticipates what customers, partners, and press will ask after the launch. It serves two purposes: (1) it forces the PM to think about the buyer's journey, and (2) it produces the first draft of help center and sales enablement content.

### Required question categories

- **What is it?** -- 1-sentence positioning
- **Who is it for?** -- Named persona and use case
- **How is it different from \[obvious alternative\]?** -- Honest comparison
- **How much does it cost?** -- Pricing tier or model
- **How do I get started?** -- Concrete first 60 seconds
- **Does it integrate with \[common tool\]?** -- The two or three integrations that will be asked
- **Is my data private?** -- Plain-language privacy stance
- **What if I do not have \[prerequisite\]?** -- The onboarding cliff
- **Can I cancel? Get a refund?** -- The trust questions

Each Q&A pair should be 1-3 sentences. Answers that need a paragraph belong in the help center, not the FAQ.

## Workflow

1. **Identify the customer and the news.** Before writing, complete the one-line statement: "We are announcing \[product\] for \[customer\] that does \[outcome\]."
2. **Draft the press release first.** No FAQ writing until the PR passes the Press Release Test with one outside reader.
3. **Write the internal FAQ in pairs.** PM drafts the question; an exec sponsor, finance partner, or eng lead drafts the answer. This surfaces blind spots.
4. **Write the external FAQ last.** This is the easiest part. If you cannot do it quickly, the PR is still too vague.
5. **Review with the "5 readers" rule.** Show the full PR/FAQ to: an exec, an engineer not on the team, a designer, a customer-facing rep, and one external person. Collect 3-5 questions from each. Add the strongest to the FAQ; revise the PR for any that the PR should have answered.
6. **Date the artifact and save it.** Save as `PRFAQ-[product-name]-[YYYY-MM-DD].md`. Track versions; PR/FAQs evolve through funding review and pre-launch.
7. **Hand off to `create-prd/`.** Once funded, the PR/FAQ becomes the prologue to the PRD. The PRD answers "how"; the PR/FAQ has already answered "what" and "why."

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Reviewers say "I do not understand who this is for" | The headline and sub-headline are feature-led, not customer-led | Rewrite the headline around the customer outcome; name the segment explicitly in the sub-headline |
| The customer quote sounds fake | It describes a feature or uses superlatives ("life-changing", "revolutionary") | Replace with a measured outcome quote: "I used to do X in 4 hours; now it takes 12 minutes" |
| The internal FAQ has 6 questions and they all sound easy | The PM is avoiding the hard questions | Run the "5 readers" rule and require each reader to submit at least one uncomfortable question |
| Exec sponsor says "this could be a slide deck" | The PR/FAQ has bullets and headers but no narrative | Strip the bullets; rewrite as paragraphs. Amazon's discipline is prose, not slides |
| External FAQ is longer than internal FAQ | Confusion about audience -- buyer questions are being mixed with reviewer questions | Re-split: anything an exec sponsor asks goes to internal; anything a customer asks goes to external |
| Press release passes review but team builds the wrong thing | PR/FAQ was treated as marketing draft, not as design constraint | Reference the PR explicitly in PRD Section 1 (Summary) and Section 7 (Solution); any feature not implied by the PR requires justification |
| PR/FAQ gets stale after kickoff | No update cadence after funding | Re-read the PR/FAQ at each milestone review; revise the FAQ when answers change; archive the final version at launch |

## Success Criteria

- The press release passes the Press Release Test with three independent readers
- The internal FAQ contains 10-20 Q&A pairs spanning all 9 required categories
- Every quantitative claim in the PR/FAQ has a cited source
- The customer quote describes an outcome, not a feature
- The "What we are NOT doing in v1" question is answered explicitly
- An exec sponsor signs off on the PR/FAQ before any PRD work begins
- The PR/FAQ is re-read and revised at each major milestone, not abandoned after kickoff

## Scope & Limitations

**In Scope:**
- Press release drafting in the Amazon Working Backwards format
- Internal FAQ generation across the 9 required categories
- External FAQ generation for buyer and customer-facing questions
- The Press Release Test review protocol
- Handoff to PRD (`create-prd/`) and roadmap (`outcome-roadmap/`) skills

**Out of Scope:**
- Marketing copy, ad copy, or external launch press releases (handoff to marketing skills)
- Detailed PRD authoring (handoff to `create-prd/`)
- OKR definition (handoff to `brainstorm-okrs/`)
- Backlog item drafting (handoff to `wwas/` or `job-stories/`)
- Pricing strategy or financial modeling (handoff to `finance/` domain)

**Important Caveats:**
- The PR/FAQ is an internal alignment artifact. It is not for external publication, even when polished. The future-dated press release is a thought experiment, not a draft for the comms team.
- The format originated at Amazon and works best in cultures that tolerate written narrative memos. Teams that primarily decide via slide decks may need to introduce the format gradually.
- A weak PR/FAQ is a feature, not a bug -- it surfaces a weak idea. Do not "fix" a weak PR/FAQ by inflating the language. Fix the idea or kill it.

## Integration Points

| Integration | Direction | Description |
|-------------|-----------|-------------|
| `discovery/brainstorm-ideas/` | Receives from | Top-ranked opportunity solutions become PR/FAQ candidates |
| `discovery/identify-assumptions/` | Receives from | Assumptions populate internal FAQ "what we do not know yet" answers |
| `discovery/pre-mortem/` | Receives from | Tiger risks populate internal FAQ "failure modes" answers |
| `execution/create-prd/` | Feeds into | Approved PR/FAQ becomes the prologue and scope anchor for the PRD |
| `execution/brainstorm-okrs/` | Feeds into | Press release outcomes become OKR candidates |
| `execution/outcome-roadmap/` | Feeds into | PR/FAQ launch date and v1 scope inform roadmap horizon placement |
| `execution/roadmap-communication/` | Feeds into | PR/FAQ summary becomes the executive-variant roadmap narrative |
| `marketing/` (skills domain) | Hands off to | After launch approval, marketing teams adapt the PR into actual launch press materials |

## References

- `references/working-backwards-guide.md` -- Deep dive on the Amazon Working Backwards method, history, and review choreography
- `assets/prfaq_template.md` -- Complete PR/FAQ template ready to fill in, with PR + internal FAQ + external FAQ sections
