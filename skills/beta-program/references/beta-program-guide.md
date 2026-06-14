# Closed Beta Program Reference Guide

A practical reference for running closed betas that produce real learning and clean GA decisions. This guide expands on the patterns in `SKILL.md` and includes worked examples, anti-patterns, and decision rules drawn from common SaaS and B2B beta programs.

---

## 1. Why Most Betas Fail

Across post-mortems of failed betas, the same five causes recur:

1. **No pre-agreed exit gates.** The team starts the beta with a vague "let's see how it goes." When the launch date approaches, success criteria are reverse-engineered to match whatever the data shows.
2. **Recruitment is opportunistic.** PMs sign up whoever raises a hand. The resulting cohort is heavily skewed toward super-fans who would have loved anything.
3. **Communication collapses after week 2.** Engineering is heads-down on bug fixes; PM is fielding 1:1 requests; nobody owns the weekly digest. Participants drift.
4. **No delight features.** The beta is all Must-be features. Engagement is fine, but no participant says anything memorable. Launch lacks quotes.
5. **The decision is never made.** The beta drags 12+ weeks. Engineering moves on. The feature ships by default without a real GA decision.

Every section below maps to one of these failure modes.

---

## 2. Cohort Sequencing: Friends, Family, Fanatics

### Sequencing Logic

| Phase | Cohort | Duration | Primary Question |
|-------|--------|----------|------------------|
| **Phase 1** | Friends | Week 1-2 | Does it run at all? What is most embarrassing? |
| **Phase 2** | Family | Week 2-5 | Does it fit a real workflow and produce value? |
| **Phase 3** | Fanatics | Week 4-8 | Would a stranger pay for this? |

Phases overlap deliberately. By week 4, all three cohorts are active and the comparison across them is the most valuable signal in the beta.

### Cohort Recruitment Targets

| Cohort | Recruitment Channel | Conversion to Active | Recommended Outreach Volume |
|--------|--------------------|--------------------:|----------------------------:|
| Friends | Internal Slack, advisor network | 80-90% | 1.2x cohort size |
| Family | CS warm intros, existing-customer email | 30-50% | 3x cohort size |
| Fanatics | Cold outreach, LinkedIn, community | 5-15% | 10x cohort size |

If Fanatics conversion is below 5%, the problem is your value proposition, not your outreach. Pause Fanatics recruitment and rerun positioning before scaling.

### Cohort Bias Adjustment

Weight feedback by cohort distance from your team:

- Friends-cohort positive feedback: weight **0.5x** (assume bias toward niceness)
- Family-cohort feedback: weight **1.0x** (closest to baseline)
- Fanatics-cohort feedback: weight **2.0x** (this is your acquisition signal)

For example, a 4.8/5 satisfaction from Friends and 3.2/5 from Fanatics is a real warning sign even though the blended average looks fine.

---

## 3. Kano Model for Beta Scope

The Kano model distinguishes five categories of features by how user satisfaction responds to investment.

```
Satisfaction
   ^
   |                           Delight (curve: starts low, accelerates up)
   |                          /
   |                         /
   |               Performance (linear: more = better)
   |              /
   |  ----------+----------> Investment
   |          /
   |         /
   | Must-be (curve: starts very low, plateaus at "neutral")
```

### Beta Scoping Decisions

| Category | Beta Scoping Rule |
|----------|-------------------|
| **Must-be** | All Must-be features ship before beta day 1. Cutting one of these is a non-starter -- the beta will produce "this is broken" feedback that drowns everything else. |
| **Performance** | Ship enough Performance features to demonstrate the value curve. You do not need to be best-in-class on every Performance axis. |
| **Delight** | Pick 1-2 Delight features. These are where you generate quotable testimonials. If you ship zero Delight features, your beta produces neutral feedback and no launch story. |
| **Indifferent** | Cut from beta. Revisit post-GA if usage data supports it. |
| **Reverse** | Make opt-in. Track who turns them off; that data will help with GA positioning. |

### Worked Example: Beta Scope Decision

A team building a new dashboard feature could ship:
- Filters (Must-be)
- Saved views (Must-be)
- CSV export (Performance)
- Schedule daily email digest (Performance)
- AI-generated narrative summary (Delight)
- White-label theming (Indifferent for the beta cohort)
- Forced password rotation (Reverse)

**Good beta scope:** All Must-bes + 1 Performance (CSV) + 1 Delight (AI summary). Drop the rest.

**Bad beta scope:** All Must-bes + every Performance feature + zero Delights. The beta will run, but no participant will be excited.

---

## 4. Exit-Gate Design

### Gate Categories (Set Before Recruitment)

Every gate is one of four categories:

| Category | Question Answered | Example Gate |
|----------|-------------------|--------------|
| **Activation** | Are participants reaching first value? | >= 70% reach the first key action in 7 days |
| **Engagement** | Are participants using it repeatedly? | Median >= 3 sessions/week in week 2-4 |
| **Outcome** | Are participants getting the promised result? | >= 50% achieve the headline outcome |
| **Quality** | Is the product stable enough to ship? | 0 open P0 bugs, >= 99.5% crash-free sessions |

### The "Quotable Testimonials" Gate

The most-skipped gate, and the one that hurts launches most. Set an explicit target (typically 3-5 named customers willing to be quoted). Ask in the week-3 1:1 with a specific draft quote ("If we wrote: '<draft>' -- could we attribute that to you?"). Get written permission before the exit-gate review.

### Anti-Pattern: Vanity Gates

Avoid:

- "Positive feedback overall" -- not measurable.
- "Beta participants are happy" -- happy with what?
- "No critical issues" -- define critical.

Replace with quantified targets, baselines, and review owners.

---

## 5. The Four Exit-Gate Outcomes

Every beta ends in exactly one of these four outcomes. The DACI driver picks one within 5 business days of beta end.

### 5.1 Greenlight GA

**Conditions:** All gates met or all gaps explicitly accepted with mitigation.

**Next steps:** Hand off to `launch-playbook/` with the testimonial bundle, known-issues list, and pricing recommendation.

### 5.2 Extend Beta

**Conditions:** Most gates met, 1-2 specific gaps with a clear plan to close in 2-4 more weeks.

**Required artifacts:**
- Written extension plan with exact gaps, target dates, and gate owners.
- Communication to participants explaining the extension and any new commitments.
- New exit-gate review date on the calendar.

**Anti-pattern:** Extending "to keep learning" without a specific gap or close plan. This is how betas drag 12+ weeks.

### 5.3 Pivot

**Conditions:** Engagement or outcome gates failed, but usage pattern reveals a different job-to-be-done that the team wants to pursue.

**Required artifacts:**
- Rewritten PRD (see `create-prd/`) reflecting the new hypothesis.
- Honest postmortem on why the original hypothesis failed.
- Communication to participants -- some will follow you to the new direction, most will not.

### 5.4 Kill

**Conditions:** Both engagement and outcome gates failed, with no compelling alternative pattern in the usage data.

**Required artifacts:**
- Postmortem covering: original hypothesis, what we learned, why we are killing it, what we will not try again.
- Sunset communication to participants (see `eol-communication/`).
- Engineering effort estimate to remove the code or leave it dormant behind a flag.

Killing a beta is a successful outcome when the data supports it. The cost of killing now is far lower than shipping a feature nobody uses for the next 3 years.

---

## 6. Communication Cadence: What to Send and When

### Monday Digest (PM owns)

- What shipped last week (commits/tickets, plain language)
- Known issues (with workarounds)
- What we want you to try this week (specific task tied to a gate)
- Office hours reminder

### Tuesday Office Hours (PM + Eng Lead)

- 30 minutes, optional, async-friendly thread alternative
- Open agenda; PM posts seed questions if quiet

### Wednesday Internal Review (PM owns)

- Gate metrics snapshot
- Top 3 bugs by occurrence
- Top 3 feature requests by frequency
- Risk register update

### Thursday 1:1s (PM rotates participants)

- 2-3 participants per week
- 30 minutes each
- Standing questions: What is working? What is broken? What is missing? Would you renew/recommend? Can we quote you on X?

### Friday Snapshot (PM owns)

- One screenshot of the gate dashboard
- One sentence on the week's biggest learning
- One thank-you naming individual contributors from the beta cohort

---

## 7. NDA, Pricing, and Commitments

### NDA

A one-page mutual NDA is standard for closed betas. Send it at activation, not at recruitment, so it does not slow the funnel.

### Pricing

Three common patterns:

1. **Free during beta, full price at GA.** Simple. Use when beta is short (<6 weeks).
2. **Free during beta, discounted price for the first 6-12 months post-GA.** Good for design partners; rewards early commitment.
3. **Paid beta at a discounted rate.** Only when participants are getting clear value from day 1; signals seriousness.

Avoid: "We'll figure out pricing later." Participants will assume the lowest possible price.

### Commitments to Honor

If you promise:

- Early access -- give it.
- Pricing lock -- honor it for the stated period.
- Credits for feedback -- track and pay them.
- Reference customer status -- ask before quoting publicly, every time.

Beta participants who feel jerked around become the loudest detractors at GA.

---

## 8. Common Beta Failure Patterns (and Fixes)

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Recruitment over-reliance on Friends** | 90% of beta is internal or advisors; engagement metrics look great; no Fanatics | Hard-cap Friends at 25% of cohort; require equal Family and Fanatics sizing |
| **Silent participant** | One participant activates and never returns | Personal outreach in week 1 with one specific ask; if no response in 5 days, replace from waitlist |
| **The "beta forever" trap** | Beta runs 6+ months; team forgets why; feature ships by default | Enforce hard 8-week max; any extension is a new beta with new gates |
| **Bug-only beta** | All feedback is bug reports; no outcome signal | Add 1 outcome-focused question to every weekly digest; remove low-priority bugs from the participant Slack to reduce noise |
| **Pricing surprise** | Beta participants churn at GA when invoice arrives | Tell participants the exact GA price in the week-1 digest; offer a written commitment for the first renewal |
| **The "PM-vendor" trap** | Beta participants treat PM as their personal account manager; PM loses 50% of time on ad-hoc requests | Establish a single async channel for asks; batch responses 2x/week; route operational issues to CS |
| **Exit decision made in private** | Decision happens in a hallway conversation; no documented memo | Require a written exit memo using `assets/exit-memo.md`; circulate before any GA commitment |

---

## 9. Beta-to-GA Handoff Checklist

Before handing off to `launch-playbook/`:

- [ ] Exit memo signed by PM, Engineering, and exec sponsor
- [ ] At least 3 quotable testimonials with written permission
- [ ] Known-issues list with status and GA-day plan
- [ ] Pricing decision finalized
- [ ] Beta participant communication scheduled for launch day
- [ ] Sales enablement bundle (case studies, FAQ, objection handling)
- [ ] Support team trained on the feature
- [ ] Marketing has access to all assets at least 2 weeks before launch

---

## 10. References

- Kano, Noriaki. "Attractive Quality and Must-Be Quality." Journal of the Japanese Society for Quality Control, 14(2), 1984.
- Cagan, Marty. *Inspired: How to Create Tech Products Customers Love*. Wiley, 2018. (Chapter on customer discovery programs.)
- Olsen, Dan. *The Lean Product Playbook*. Wiley, 2015. (MVP definition, value proposition testing.)
- Reichheld, Fred. "The One Number You Need to Grow." Harvard Business Review, 2003. (NPS methodology.)
