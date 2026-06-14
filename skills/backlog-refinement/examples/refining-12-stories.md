# Example: Refining 12 Stories for Wayfinder's Q3 Backlog

> Real-world scenario showing how to apply INVEST grading and vertical splitting end-to-end.

## Context

Wayfinder is a 30-person Series-B B2B project-management SaaS (~$11M ARR, ~280 paying teams). The Onboarding & Activation squad runs 2-week sprints with three engineers, a designer, and a PM (Sam). Sprint completion has been erratic: 4 of the last 5 sprints carried over at least 3 stories. The retro pinpointed refinement quality as the cause.

Sam has 12 candidate stories on the Q3 backlog from a recent activation push. The team has agreed to do a Monday refinement session before sprint planning Wednesday. Goal: every story entering the next sprint must score 5/6 or 6/6 on INVEST, with a working Definition of Ready and Definition of Done.

## Inputs

- 12 candidate stories drafted by Sam + two CSMs, mostly from customer feedback
- The team's existing DoR (in Notion)
- 90 minutes scheduled with the squad
- Sprint planning capacity: 22 story points (median velocity over last 6 sprints)
- The `refinement_scorer.py` tool to grade each story before the session

## Applying the skill

1. **Pre-grade with the scorer.** Sam ran `refinement_scorer.py` against `backlog.json` Monday morning. 3 stories scored 5-6 (ready), 6 scored 3-4 (need refinement), 3 scored below 3 (split or send back).
2. **Triage in the session.** First 30 min: confirm the 3 ready stories. Next 45 min: refine the 6 mid-tier. Last 15 min: agree to split the 3 low-tier.
3. **Split the oversized stories** using Richard Lawrence's 9 recipes. The two biggest splits: "Onboarding wizard rewrite" (workflow-steps split) and "SSO support" (input-options + business-rule-variations).
4. **Update the DoR for one missed criterion** the team kept tripping on: "acceptance criteria reference a measurable outcome, not an output."
5. **Lock the sprint candidate set** at 11 INVEST-passing stories (the 12th was returned to discovery).

Key decision quoted: *"If we cannot estimate within 2x, it is too big. Split it now, or send it back."*

## The artifact

````markdown
# Backlog Refinement Session -- Wayfinder Onboarding Squad

**Date:** 2026-05-22
**Facilitator:** Sam (PM)
**Participants:** N. Gupta (EM), 3 engineers, 1 designer, 1 CSM observer
**Duration:** 90 min
**Output:** 11 INVEST-passing stories ready for sprint planning Wednesday

## Pre-session INVEST scores (refinement_scorer.py)

| ID | Title | Score | Verdict |
|---|---|:-:|---|
| WAY-201 | Show "Get Started" checklist on first login | 6 | Sprint-ready |
| WAY-202 | Send welcome email 5 minutes after signup | 6 | Sprint-ready |
| WAY-203 | Track activation events in Amplitude | 5 | Sprint-ready (T soft) |
| WAY-204 | Improve onboarding | 1 | Send back |
| WAY-205 | Onboarding wizard rewrite | 2 | Split |
| WAY-206 | SSO support | 2 | Split |
| WAY-207 | Show team-invite step in wizard | 4 | Refine |
| WAY-208 | Make sample project optional | 3 | Refine |
| WAY-209 | Migrate users from old onboarding | 4 | Refine |
| WAY-210 | Add tooltip to first dashboard widget | 4 | Refine |
| WAY-211 | Detect inactive workspaces after 7 days | 3 | Refine |
| WAY-212 | Re-engagement email after 14-day inactivity | 4 | Refine |

## Before / After (per story)

### WAY-201 -- Sprint-ready (6/6) -- no change

**Title:** Show "Get Started" checklist on first login
**Why:** Increase D1 activation from 28% to 38% (Q3 KR-1).
**Description:** New workspace owners see a 5-item checklist on first login containing the highest-leverage onboarding tasks.
**Acceptance:**
- Checklist appears within 800 ms of first dashboard render
- Items can be checked manually OR auto-complete on event
- Dismissing the checklist sets a flag, never re-appears
- 5 items load from a config table (no hardcoded copy)
**Estimate:** 3
**Verdict:** Ready

### WAY-202 -- Sprint-ready (6/6) -- no change

**Title:** Send welcome email 5 minutes after signup
**Acceptance:**
- Email queued within 5 min of `user.signed_up` event
- Subject A/B variants drawn from `welcome_email_variant` flag
- Unsubscribe link present and functional
- Delivery rate >= 98% in staging load test
**Estimate:** 2
**Verdict:** Ready

### WAY-203 -- Sprint-ready (5/6) -- T soft

**Title:** Track activation events in Amplitude
**Soft fail:** Testable (T) -- acceptance does not enumerate every event.
**Fix in session:** added explicit event list (5 events: signup_completed, first_project_created, first_member_invited, first_task_completed, checklist_dismissed).
**New score:** 6
**Verdict:** Ready

### WAY-204 -- Send back

**Title (was):** "Improve onboarding"
**Failure:** Fails N (negotiable -- prescribes nothing), V (no value statement), E (cannot estimate), S (unbounded).
**Action:** Returned to discovery (`discovery/brainstorm-ideas/`). Sam to bring 2-3 candidate solutions to next refinement.

### WAY-205 -- Split (workflow steps)

**Title (was):** "Onboarding wizard rewrite"
**Problem:** 3-week effort; touches signup, workspace creation, invite, sample-project, first-task.
**Split (Lawrence #1 -- workflow steps):**

| Slice | Story | Estimate |
|---|---|---|
| 5a | "Wizard step: workspace details" | 3 |
| 5b | "Wizard step: invite teammates (optional)" | 3 |
| 5c | "Wizard step: connect data source (optional)" | 5 |
| 5d | "Wizard step: create first project from template" | 3 |
| 5e | "Wizard exit + dashboard handoff" | 2 |

Each slice ships behind flag `wizard_v2_step_<n>`; first slice gates rest.
**Verdict:** 5a, 5b ready; 5c, 5d, 5e deferred to next sprint.

### WAY-206 -- Split (input options + rules)

**Title (was):** "SSO support"
**Problem:** Touches three IDPs (Okta, Google, Azure AD), org-level + workspace-level config, just-in-time provisioning, deprovisioning.
**Split:**

| Slice | Story | Recipe | Estimate |
|---|---|---|---|
| 6a | "Google Workspace SSO (read-only)" | Lawrence #4 (input options) | 5 |
| 6b | "Okta SSO (read-only)" | #4 | 5 |
| 6c | "Azure AD SSO (read-only)" | #4 | 5 |
| 6d | "JIT user provisioning" | #2 (rules) | 3 |
| 6e | "Deprovisioning on IDP delete" | #2 | 3 |

**Verdict:** 6a (Google) admitted to candidate set; 6b-6e deferred until 6a validates the abstraction.

### WAY-207 -- Refined (4 -> 6)

**Before acceptance:**
- "Team invite step works"

**After acceptance:**
- Step appears as wizard step 2/4 with skip option
- User can add up to 10 emails (validated for format)
- Each email triggers an invite send within 30s
- Skipping records `wizard_invite_skipped` event
- Re-entering the wizard pre-fills previously-added emails

**New score:** 6. **Verdict:** Ready.

### WAY-208 -- Refined (3 -> 5)

**Before:** "Make sample project optional"
**Problem:** No why; ambiguous scope.
**Refined Why:** 22% of users who saw the sample project skipped it and never returned; making it optional reduces drop-off.
**Refined acceptance:**
- "Create sample project" replaced with "Start with sample" + "Start blank" choice
- Default selection randomized 50/50 for A/B test via flag `sample_project_default`
- Choice recorded in `wizard_sample_choice` event
- Pre-existing workspaces unaffected

**New score:** 5 (T soft -- no explicit success metric per variant). Soft-admit with team agreement to define after first 200 signups.

### WAY-209 -- Refined (4 -> 6)

**Title:** Migrate existing users from v1 onboarding to v2
**Refined:** Background job; idempotent; runs in batches of 500; emits per-user telemetry; admin dashboard shows progress.
**New score:** 6. **Verdict:** Ready.

### WAY-210 -- Refined (4 -> 6)

**Title:** Tooltip on first dashboard widget
**Refined Why:** 38% of new users hover the widget without clicking; tooltip should drive 60% click-through.
**Refined acceptance:** appears on first 3 dashboard loads only; A/B copy from flag; dismisses on click; event tracked.
**New score:** 6. **Verdict:** Ready.

### WAY-211 -- Refined (3 -> 5)

**Title:** Detect inactive workspaces after 7 days
**Refined:** Daily job; "inactive" = no `user_active` event in 7 rolling days; writes `workspace_inactive` event; feeds WAY-212.
**New score:** 5. **Verdict:** Ready (T soft -- defined as enabler for 212).

### WAY-212 -- Refined (4 -> 6)

**Title:** Re-engagement email after 14-day inactivity
**Refined acceptance:**
- Triggered by `workspace_inactive` event sustained 14 days
- Subject + body A/B from flag
- Suppressed if user already opened any email in last 7 days
- Click-through tracked; unsubscribe honored

**New score:** 6. **Verdict:** Ready.

## Updated Definition of Ready (delta)

Added: "Acceptance criteria reference a measurable outcome (count, rate, time) where applicable, not just an output. Pure config or telemetry stories are exempt."

## Sprint candidate set (post-refinement)

| ID | Title | Est | Status |
|---|---|:-:|---|
| WAY-201 | Get Started checklist | 3 | Ready |
| WAY-202 | Welcome email | 2 | Ready |
| WAY-203 | Activation events in Amplitude | 3 | Ready |
| WAY-205a | Wizard step: workspace details | 3 | Ready |
| WAY-205b | Wizard step: invite teammates | 3 | Ready |
| WAY-206a | Google Workspace SSO (read-only) | 5 | Ready |
| WAY-207 | Team-invite wizard step | 2 | Ready |
| WAY-208 | Sample project optional + A/B | 3 | Ready (soft) |
| WAY-209 | Migrate users to v2 onboarding | 3 | Ready |
| WAY-210 | Dashboard widget tooltip | 2 | Ready |
| WAY-211 | Inactive workspace detector | 2 | Ready |
| **Total** | | **31** | |

Capacity = 22; team selects top 7-8 by RICE at planning.
````

## Why this works

- INVEST scoring was done before the session, freeing the meeting to fix stories rather than grade them.
- Two oversized stories (205, 206) were split using Lawrence recipes by name -- workflow steps for the wizard, input options for SSO -- so the splits stayed vertical (each slice shippable end-to-end).
- The "send back" verdict on WAY-204 saved the team a planning round on a story that had no value statement.
- "Soft admit" with a known T-gap on WAY-203 and WAY-208 documents the trade-off rather than hiding it.
- DoR was updated in-session based on a recurring miss, which is how DoRs stay alive instead of becoming wall art.

## What's next

- Feed the refined candidates into [../prioritization-frameworks/](../prioritization-frameworks/) (RICE) at sprint planning Wednesday.
- Use [../story-splitting/](../story-splitting/) when the team needs deeper splitting practice on WAY-205 sub-slices.
- Use [../wwas/](../wwas/) if any of these stories grow strategic context (e.g., WAY-206a SSO for an enterprise deal).
- Use [../cycle-time-analyzer/](../cycle-time-analyzer/) at the next retro to verify the predictability lift.
