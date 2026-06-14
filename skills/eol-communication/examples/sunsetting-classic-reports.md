# Example: Sunsetting "Classic Reports" at Acme Analytics

> Real-world scenario showing how to apply the EOL communication framework end-to-end.

## Context

Acme Analytics shipped "Classic Reports" in 2019. It was the original reporting surface, with a fixed grid layout and CSV export. In 2023 the team launched "Reports v2" with drag-and-drop layouts, scheduled emails, and shared dashboards. Reports v2 has been the default for new workspaces since 2024.

Today, 200 active workspaces still rely on Classic Reports. Continuing to maintain Classic costs ~0.5 engineer-FTE in patches, security updates, and customer-support burden. The team has decided to sunset Classic over 6 months and migrate the 200 holdouts to Reports v2.

The PM (Devi Rao) needs an EOL communication plan that preserves trust with the 200 affected customers (which include 12 enterprise accounts totaling $4.1M ARR).

## Inputs

- 200 active workspaces on Classic Reports (12 enterprise, 88 Pro, 100 free)
- $4.1M ARR exposure
- Reports v2 covers 95% of Classic functionality natively; 5% via a documented workaround
- Migration tool exists: auto-converts Classic report definitions into v2 equivalents
- 6-month timeline before final shutdown
- Legal has flagged 3 enterprise contracts that mention "Classic Reports" by name

## Applying the skill

1. **Pre-announcement planning** filled with the 7 mandatory questions. Honest framing: Classic is being discontinued because we cannot ship the security and accessibility improvements customers need on the legacy code path.
2. **Drafted the EOL message** using the template -- led with empathy ("we know this is a disruption"), focused on continuity (v2 covers your reports), gave concrete dates.
3. **Segmented the message** for enterprise (personal outreach), Pro (email + in-app), and free (email + blog).
4. **Reviewed contract clauses** with Legal. Three enterprise contracts named "Classic Reports" explicitly. Solution: parallel-run Classic until each contract's next renewal date.
5. **Built internal FAQ** for Support team -- 12 likely objections with recommended responses.
6. **Set monitoring checklist**: weekly migration rate, support ticket volume, social sentiment, portfolio churn.

Key decision quoted: *"We use the word 'discontinuing', not 'sunsetting' or 'streamlining'. Customers can read corporate euphemisms in 3 seconds."*

## The artifact

````markdown
# Acme Analytics -- Classic Reports End-of-Life Plan

**Affected product:** Classic Reports
**Replacement:** Reports v2 (already GA, default since 2024)
**Affected customers:** 200 workspaces ($4.1M ARR)
**Announce date:** 2026-05-26
**Final shutdown:** 2026-11-24 (6 months)
**Plan owner:** Devi Rao (PM, Reporting)

## Customer-facing announcement (email + blog)

```markdown
Subject: Important update: Classic Reports will be discontinued November 24, 2026

Hi {first_name},

We're writing to let you know that Classic Reports will be discontinued on
November 24, 2026 -- 6 months from today.

We know this is a disruption. You've built your reporting on Classic, and
the change asks something of you.

**Why we're making this change**

Classic Reports was built in 2019 on a layout engine that we cannot extend
to meet customers' current security, accessibility, and integration
requirements. Continuing to maintain Classic means we ship slower on
everything else. Reports v2 -- which has been our default since 2024 --
solves the same job better.

**What you keep**

- Every report you have in Classic can be migrated to Reports v2.
- Your CSV exports, scheduled emails, and shared links all carry over.
- Your existing dashboards continue to work; only the report layout
  changes.

**What's better in v2**

- Drag-and-drop layouts (instead of fixed grids)
- Native shared dashboards (no more PDF exports)
- Scheduled email digests with custom recipients
- Direct Slack and Teams integrations

**How we're helping**

- A one-click migration tool that converts every Classic report into a
  Reports v2 equivalent. We've tested it on 2,400 sample reports; 95%
  convert cleanly with no manual work.
- A dedicated migration support team available from now through
  shutdown.
- A side-by-side comparison guide for the 5% of cases that need manual
  adjustment.
- Free, hands-on migration consultation for any account that wants one.

**Timeline**

| Date | What happens |
|---|---|
| May 26, 2026 | Today: announcement; migration tool available |
| June 26, 2026 | Reports v2 set as the default for any new report; Classic remains available |
| September 24, 2026 | Classic enters read-only mode (existing reports view, no edits) |
| October 24, 2026 | Final data-export deadline for any unmigrated content |
| November 24, 2026 | Classic Reports is fully discontinued |

For enterprise customers under contract: if your contract names Classic
Reports specifically, we'll extend access through the end of your current
contract term.

**Your next step**

Visit `app.acme.com/reports/migrate` to start the migration. The first
report takes about 4 minutes. We'll be here every step.

If anything in this is unclear, reply to this email -- I read every
response.

Devi Rao
Product Manager, Reporting
Acme Analytics
```

## Enterprise outreach script (high-value accounts, $4.1M ARR exposure)

Each of the 12 enterprise accounts gets:

1. A personal email from their named CSM (2 days before the public announcement).
2. A scheduled 30-minute call with their CSM and Devi to walk through the migration plan.
3. A custom migration plan if their workflow has any of the 5% non-auto-convertible patterns.

**Personal email template:**

```
Subject: Important Acme update -- previewing for you before the public announcement

Hi {first_name},

I wanted to give you a heads-up directly before the public announcement
on Thursday. We're discontinuing Classic Reports on November 24, 2026,
and migrating customers to Reports v2.

I know this matters to you because {specific_workflow_reference}. Here's
what it means for {company_name}:

- Your contract mentions Classic Reports specifically. We'll honor that
  through {contract_end_date}.
- Reports v2 covers everything you do in Classic, with these
  improvements: {top_3_relevant_to_their_workflow}.
- We'd like to do a 30-min walkthrough with you and {csm_name} this
  week. {calendar_link}

If you have questions you'd rather raise privately first, reply to me
directly.

Devi Rao
PM, Reporting
```

## In-app notification

```
Banner (appears on every Classic Reports page from 2026-05-26 onward):

  ! Classic Reports will be discontinued November 24, 2026.
    Migrate your reports to v2 -> [Start migration] [Learn more]
```

The banner cannot be permanently dismissed; it reminders every 7 days.

## Internal FAQ for Customer Support

| Customer says | Recommended response |
|---|---|
| "I don't want to switch -- can I keep Classic?" | Acknowledge: this is a disruption. Reports v2 covers everything you do today, and we have a 1-click migration tool. Walk them through it. If they're enterprise with a Classic-named contract, escalate to CSM. |
| "I need more time" | The timeline is firm at November 24. Their CSM (if enterprise) can negotiate parallel-run through contract end. For Pro accounts, escalate to PM if there's a specific workflow blocker. |
| "Reports v2 doesn't do {feature}" | Document the gap in `gap-tracker.md`. We may be able to address it before shutdown; if not, we offer a documented workaround. Common cases: scheduled-export-to-FTP (workaround: scheduled email + webhook), custom-report-formula (workaround: v2 has expressions, share the cookbook). |
| "I want a refund" | If they're Pro and within 30 days of renewal, follow the standard refund policy. If outside that window, escalate to CSM. We're not refunding broadly; the replacement product is included in their existing subscription. |
| "Why wasn't I consulted?" | This was a product-roadmap decision based on customer feedback over the last 18 months. We'd love to hear how Reports v2 can be improved -- offer the v2 feedback channel. |
| "Will the migration tool break my reports?" | Tested on 2,400 sample reports, 95% convert cleanly. The other 5% we know about: list with workarounds is at `acme.com/docs/classic-to-v2-edge-cases`. If yours falls in that 5%, we'll do hands-on migration with you. |
| "What about my saved CSV exports / Excel macros downstream of Classic?" | The CSV output format is identical. Macros and downstream automations continue to work without change. We tested this explicitly. |
| "Can I roll back to Classic if v2 breaks something?" | Yes, until September 24, 2026. After that, Classic enters read-only and rollback is no longer available. We recommend migrating early so you have time to flag anything that doesn't behave right. |
| "Your contract says you'd support Classic for X years" | Refer to Legal. For the 3 enterprise contracts that name Classic specifically, we honor the contract through its current term. |
| "I'm worried about the data" | All your data stays. The migration tool moves report definitions, not the underlying analytics data. |
| "Is this because you're being acquired / shut down?" | No. We're investing more in Reports, not less -- v2 is where the investment goes. |
| "What if I do nothing?" | On October 24, 2026, you'll have a final-export-deadline reminder. On November 24, Classic stops working and the migration tool migrates anything you haven't migrated yourself. We'll send 3 more reminders before then. |

## Timeline summary

| Date | Milestone | Audience | Channel |
|---|---|---|---|
| 2026-05-22 | Internal alignment + Legal review | All Acme | Slack + Notion |
| 2026-05-23 | Support team briefing | Support | Training |
| 2026-05-24 | Enterprise CSM outreach starts | 12 enterprise accts | Direct email + call |
| 2026-05-26 | Public announcement | All Classic users | Email + blog + in-app banner |
| 2026-06-09 | Migration kickoff webinar | Pro users | Zoom (recorded) |
| 2026-06-26 | Reports v2 set as default for new reports | All | In-app |
| 2026-09-24 | Classic enters read-only mode | All Classic users | Email + in-app |
| 2026-10-24 | Final data-export deadline | All Classic users | Email |
| 2026-11-24 | Classic Reports discontinued | All | Email + status page |
| 2026-12-15 | Post-EOL retrospective | Internal | Notion + senior leadership |

## Monitoring checklist (weekly)

- [ ] Migration rate: % of Classic reports migrated (target: 80% by 2026-11-01)
- [ ] Support ticket volume on Classic EOL topics
- [ ] NPS / CSAT for accounts that completed migration (target: NPS >= pre-EOL Reports NPS)
- [ ] Churn rate across non-EOL products (target: no portfolio-wide bleed)
- [ ] Sentiment in `#acme` community Slack and on Twitter/X
- [ ] Number of accounts still on Classic but not started migration
- [ ] Enterprise account-by-account status (12 accounts)

## Success criteria

- [ ] EOL message reviewed by Legal, Support, CS, and PMM before publication
- [ ] 80%+ of affected workspaces migrated by 2026-11-01
- [ ] Support ticket volume on EOL declines weekly after week 4
- [ ] No churn increase on non-Classic products
- [ ] Zero contractual violations (3 named-Classic enterprise contracts honored)
- [ ] Post-EOL retrospective conducted within 30 days of shutdown

## What we are NOT going to do

- Refer to this as "sunsetting" or "streamlining" in customer-facing copy. Use "discontinuing".
- Allow Sales to commit to extending Classic for new prospects (not negotiable -- the product is on a known end date).
- Pretend Reports v2 has 100% feature parity. The 5% gap is documented; we own it.
- Push the deadline. The deadline is firm; what is negotiable is the per-account migration support.
````

## Why this works

- Leads with empathy and a real reason (legacy code path can't carry security + accessibility improvements), not corporate euphemism.
- Names dates specifically: announce, default, read-only, final export, shutdown. Five concrete dates beat "in the coming months".
- Honors the three enterprise contracts that name Classic by extending through contract end -- prevents legal exposure without compromising the broader EOL date.
- The internal FAQ covers 12 likely objections so Support doesn't improvise responses under pressure.
- The "what we are NOT going to do" list explicitly forbids corporate euphemisms ("sunsetting") in customer copy.

## What's next

- Use [../release-notes/](../release-notes/) to communicate the final Classic patches alongside the EOL timeline.
- Pair with [../create-prd/](../create-prd/) -- any v2 gap that becomes a v2.1 priority gets its own PRD.
- Use [../../senior-pm/](../../senior-pm/) for the stakeholder map of the 12 enterprise accounts.
- Use [../daci-framework/](../daci-framework/) to clarify who decides on per-account exception requests.
- Run a [../post-mortem/](../post-mortem/) at T+30 days after shutdown to capture lessons for the next EOL.
