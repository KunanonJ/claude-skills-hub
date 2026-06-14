# Notion PRD Template

Copy this template into a new row of the PRDs database. The header rows are page properties; the body is the page content. Sections use Notion-native blocks (headings, callouts, toggles, to-dos, tables).

---

## Page properties (fill in the PRDs database row)

- **Title:** PRD: <Feature name>
- **Status:** Draft
- **Priority:** P1
- **Owner:** @PM
- **Author:** @PM
- **Reviewers:** @Eng-Lead, @Design-Lead, @Data-Lead
- **Target Date:** YYYY-MM-DD
- **Areas:** API, Web
- **Customer Segments:** SMB, Mid-Market
- **OKR:** (relation) → Increase activation rate to 45%
- **Roadmap Item:** (relation) → Self-Serve Onboarding
- **Confidence:** Medium
- **Last Reviewed:** YYYY-MM-DD

---

## Page body

### TL;DR

> [!NOTE]
> Two-sentence summary. What changes, and what business outcome it drives.

### Problem

What user/business problem does this solve? Include data:

- Today, X% of users do Y.
- This costs us Z in lost activation / revenue / time.

Link to supporting research:

- @Customer Research: Acme Inc CTO interview
- @Customer Research: Q1 2026 onboarding survey

### Goals

What does success look like?

- Primary goal: <single, measurable outcome>
- Secondary goals:
  - <secondary>
  - <secondary>

### Non-goals

What we are explicitly **not** doing in this PRD:

- Not solving X.
- Not addressing Y.
- Not changing Z.

### User stories

> As a <persona>, I want to <action>, so that <outcome>.

- As a new user, I want to sign up without talking to sales, so that I can start trialing in under 5 minutes.
- As a returning user, I want SSO, so that I do not have to remember another password.

### Solution

#### Overview

A diagram or 2-3 paragraph description.

#### User flow

1. User arrives at marketing page.
2. User clicks "Start free trial."
3. User enters email and creates password (or chooses SSO).
4. User lands in product with sample data loaded.

#### Edge cases

| Case | Behavior |
|---|---|
| User already has an account | Redirect to login with "We recognize this email" |
| Email domain matches an enterprise customer | Trigger SSO flow |
| Sign-up rate exceeds 10x normal | Trigger fraud-detection review |

### Requirements

#### Functional

- [ ] Sign-up form accepts email and password.
- [ ] Magic-link email is sent within 30 seconds.
- [ ] User lands in product with onboarding checklist visible.
- [ ] SSO flow detects enterprise domains via API call.

#### Non-functional

- [ ] Sign-up flow P95 latency < 2 seconds.
- [ ] Magic-link email delivery rate > 98%.
- [ ] WCAG 2.1 AA compliance.

### Success metrics

| Metric | Today | Target | Measure via |
|---|---|---|---|
| Activation rate | 30% | 45% | Mixpanel funnel |
| Time-to-first-value | 18 min | 5 min | Internal event |
| Trial-to-paid | 8% | 12% | Stripe + Mixpanel |

### Risks and dependencies

> [!WARNING]
> List risks that could derail the launch.

- Risk: Email deliverability through new IPs is unproven. Mitigation: warm up IPs 4 weeks early.
- Dependency: SSO requires the auth-svc rewrite (@Auth-Eng-Lead, target end of Q2).

### Open questions

<details>
<summary>Should we A/B test the new flow against the old one?</summary>

Pro: data-driven rollout. Con: 2 additional weeks. Decision needed by YYYY-MM-DD by @PM-VP.

</details>

<details>
<summary>What is the trial length: 7, 14, or 30 days?</summary>

Currently 14. Sales argues for 30; PMM argues 7 for urgency. Needs a Decision (see Decisions DB).

</details>

### Decision log

Link to relevant Decisions DB rows:

- @DEC-042: Adopt magic-link auth over password-first
- @DEC-051: Use 14-day trial as default

### Launch plan

- **Internal alpha:** YYYY-MM-DD (10 employees)
- **Closed beta:** YYYY-MM-DD (50 friendly customers)
- **General availability:** YYYY-MM-DD
- **Comms plan:** see Launch Playbook @Launch-Self-Serve

### Rollback plan

If activation rate drops by more than 10pp post-launch:

- [ ] Feature-flag off the new flow.
- [ ] Restore prior sign-up URL.
- [ ] Triage in incident channel.
- [ ] Post-mortem in Decisions DB within 5 business days.

### Links

- **Linear Project:** (property)
- **Figma:** (embed)
- **Tech design doc:** (link)
- **Data analysis:** (link)
- **Slack channel:** #proj-self-serve-signup

### Sign-off

- [ ] PM (@PM)
- [ ] Engineering lead (@Eng-Lead)
- [ ] Design lead (@Design-Lead)
- [ ] Data lead (@Data-Lead)
- [ ] Security review (@Sec-Reviewer)
- [ ] Legal/privacy review (@Legal-Reviewer)

> [!TIP]
> When all sign-offs are checked, set page Status to **Approved** and Approved On to today's date. This triggers the downstream Linear Project creation if the workspace has that sync configured.
