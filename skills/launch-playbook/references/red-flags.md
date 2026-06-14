# Red Flags: Launch Playbook

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan the run-of-show, RACI, comms plans, and rollback plan before T-7. Each red flag shows the *bad* version next to the *good* version, anchored to Marty Cagan's three-launches model (alpha/beta/GA) and the launch RACI.

---

## Red Flag 1: No rollback rehearsal

**Symptom.** Rollback plan is documented. Nobody has actually executed a rollback in staging. Launch day discovers the runbook has stale commands.

**Why it's bad.** A documented-but-untested rollback is a fiction. Production rollback drills surface stale credentials, missing access, runbook gaps, and decision-authority confusion — all of which become amplified in a real incident.

**Bad example:**
> "Rollback plan: 8-page doc, last updated 6 weeks ago. Drill: 'we'll do that in the future when we have time.' Launch day: rollback attempted; command in runbook fails because the service was renamed."

**Good example:**
> "Rollback rehearsal at T-14 and T-7:
> • Run in staging first; then in production with a no-op feature flag.
> • Time it; document the actual elapsed time.
> • Confirm: kill-switch flips < 60 sec; full rollback < 10 min.
> • Test each runbook step; every command works.
> • Test escalation paths; on-call rota current.
> Result documented in `assets/rollback-plan.md` with timestamps and the names of the people who ran it."

**How to catch it.** Ask: "show me the timestamps from the last rollback drill." If no answer, the drill didn't happen.

---

## Red Flag 2: Comms not aligned with engineering

**Symptom.** PMM publishes a launch post saying "shipping today, 100% available globally". Engineering's actual ramp is 5% → 25% → 100% over a week. Customers in Europe try the feature, hit "not available in your region", post on Twitter.

**Why it's bad.** Marketing message and engineering reality must match. When they don't, customers' expectations are set wrong, support is overwhelmed, and the launch narrative is hijacked by "broken promise" stories.

**Bad example:**
> "PMM blog: 'Available to all customers today.' Engineering rollout: 5% canary all week; 100% on Friday. Day 1: 95% of customers see a 'not available' message after clicking the blog post."

**Good example:**
> "T-7 alignment check: PMM and Eng Lead jointly review the rollout plan and the public messaging. Public message updated to match: 'Rolling out this week — most customers will see it by Friday. If you don't see it yet, click here to request access.' Engineering's ramp schedule documented in the in-app message users see. PMM, Eng, and Support agree on the language."

**How to catch it.** At T-7, read the PMM materials and the engineering rollout plan side by side. Any mismatch in scope or timing = misalignment.

---

## Red Flag 3: RACI cells unowned

**Symptom.** Launch RACI is published. Several cells are blank. Assumption: "someone will figure it out".

**Why it's bad.** Unowned launch workstreams *will not happen*. The single most common cause of failed launches is a missing RACI assignment, not a missing artifact. If you can name the artifact but not the owner, the artifact will not exist.

**Bad example:**
> "Launch RACI: 10 workstreams x 7 roles = 70 cells. 12 cells blank. Sales enablement row: A and R both blank. (Launch day: sales has no battle card; reps freelance their pitch; messaging fragments across the team.)"

**Good example:**
> "Launch RACI at T-21: every cell assigned to a named individual (not 'the team' or 'TBD'). Sales enablement row: R Jorge M (PMM); A Sarah K (Sales Director); C David T (PM), Eng Lead; I All sales reps. Battle card committed by T-14; mandatory training session T-7."

**How to catch it.** Read the RACI. Every R and A cell should have a person's name. Any "TBD", "the team", or blank = unowned.

---

## Red Flag 4: Beta gates not actually met

**Symptom.** Launch date is fixed for August 31 (committed to investors). Beta exit memo says outcome gate failed (38% achieved headline outcome vs 50% target). Team launches anyway.

**Why it's bad.** Beta gates exist precisely to prevent calendar-driven launches of products that aren't ready. Launching on the calendar instead of on the criteria means GA will be the first time customers experience the gaps. Trust erodes; support is overwhelmed; competitors notice.

**Bad example:**
> "Beta exit memo: 38% outcome (vs 50% target). PM: 'we have a hard launch date; we'll ship and iterate.'"

**Good example:**
> "Beta exit memo: 38% outcome (vs 50% target). DACI Driver convenes the gate review: launch postponed 4 weeks. Internal comms: 'we discovered a friction point in beta; pushing GA to Sep 28 so we ship the right thing.' Re-baseline the launch date with the exec sponsor; the calendar is not the gate, the criteria are."

**How to catch it.** Re-read the beta exit memo before launch decision. Any failed gate = address before T-0, not after.

---

## Red Flag 5: Support not trained before launch

**Symptom.** Launch day. Support inbox: 400 tickets in 4 hours. Agents respond "let me check on that" because the runbook is still draft.

**Why it's bad.** Support is the customer's only human touchpoint when something goes wrong. Untrained support means the customer's first experience of "something wrong" is also "the company can't help me" — a double failure.

**Bad example:**
> "Support runbook drafted at T-3. Training session: never scheduled. Launch day: agents see new feature tickets for first time. Macro responses absent. Escalation queue overflows."

**Good example:**
> "Support runbook completed at T-14; training T-7 (mandatory for all customer-facing agents). Top-10 anticipated questions: macro responses pre-written. Escalation rota: T-1 confirmation. Launch day: ticket volume spike of 3.2x baseline absorbed within SLA; macro responses cover 78% of tickets; escalations are real issues, not training gaps."

**How to catch it.** At T-3: ask 2 support agents "what's launching this week and how do I handle ticket X?" If they hesitate, training is missing.

---

## Red Flag 6: Sales has no idea the feature exists

**Symptom.** Launch day. Sales rep on a customer call: "We're launching what? Today?"

**Why it's bad.** Sales enablement is a workstream that requires deliberate effort, not osmosis. Without battle cards, training, and a defined SDR/AE handoff, sales freelances responses. Some reps oversell; others undersell; messaging fragments.

**Bad example:**
> "PMM published the launch blog on Wednesday at 9am. Sales-team Slack channel: '#products' was supposed to receive the heads-up. The heads-up never went. Reps learn from the customer."

**Good example:**
> "Sales enablement workstream owned by PMM:
> • T-21: battle card drafted (PMM + PM jointly).
> • T-14: battle card reviewed with VP Sales.
> • T-7: mandatory enablement session (all AEs, SDRs, CSMs). Recording in Highspot.
> • T-3: quiz to confirm rep readiness (90% pass before launch).
> • T-1: final talking points and FAQ in CRM playbook.
> Launch day: every rep can name the feature, target customer, and 3 differentiators."

**How to catch it.** At T-3: ask 3 random reps "what are we launching this week and to whom?" If 2 can't answer, sales enablement failed.

---

## Red Flag 7: Single incident commander missing

**Symptom.** Launch day. An issue surfaces. PMM tries one mitigation; Eng tries another; both miss each other's actions in the war-room thread.

**Why it's bad.** Multi-headed incident response produces conflicting actions, missed signals, and slower recovery. Cagan's framing and standard incident-management practice: one named incident commander with authority to make and reverse decisions.

**Bad example:**
> "War-room Slack: 12 active people; PMM posting 'I'm reaching out to TechCrunch'; Eng Manager posting 'I'm pausing the rollout'; PM trying to triage; nobody has the floor."

**Good example:**
> "Launch-day run-of-show: single incident commander named for the day (Eng Manager Tomas R). Authority: make any go/no-go decision for the next 4 hours without escalation. War room: he runs hourly check-in (top of every hour); everyone reports to him; he posts the consolidated update. Other roles post into a side thread, not into the main."

**How to catch it.** Read the run-of-show. Does it name a single incident commander with explicit authority? If not, the chain is unclear.

---

## Red Flag 8: Exec sponsor surprised by customer issue

**Symptom.** A customer escalates an issue on Twitter at 11am. VP Product first hears about it from a different customer on the 2pm board call.

**Why it's bad.** Exec sponsors are the company's senior face for the launch. Being surprised by a customer issue in a high-stakes meeting destroys credibility and gives the sponsor no time to prepare a response. Worse, it signals to the sponsor that the team doesn't have control.

**Bad example:**
> "Internal comms plan: 'we'll update the exec channel as needed'. (Reality: T+1 customer Twitter post; T+3 VP hears about it; T+4 VP messages PM 'why am I learning this from a customer?')"

**Good example:**
> "Exec briefing cadence:
> • T-1 17:00: pre-launch briefing memo to exec sponsor (current readiness, expected risks).
> • T+0 12:00: launch-day status (metrics + any issues).
> • T+0 17:00: end-of-day summary.
> • T+1 09:00: 24h retro.
> • Any P0/P1 incident: exec sponsor pinged within 15 min of declaration.
> No exec hears about a customer issue from outside the team before hearing about it from the team."

**How to catch it.** Look at the exec comms plan. Are scheduled briefings on the calendar? If no, surprise is likely.

---

## Red Flag 9: 30-day retro never happens

**Symptom.** Launch was September 1. It is now October 15. No retrospective scheduled. Team has moved to the next initiative.

**Why it's bad.** Without a 30-day retro, the team cannot learn what worked and what didn't. The next launch repeats the same mistakes. The 30-day window also captures the lagging metrics (cohort retention, customer-feedback themes) that day-1 metrics miss.

**Bad example:**
> "Launch: Sep 1. PM on next project Oct 5. No retro held. Director: 'we'll discuss at the next QBR.'"

**Good example:**
> "Calendar-blocked at kickoff:
> • T+7 retrospective: week-1 metrics, top issues, hotfix list.
> • T+30 retrospective: 30-day metrics vs forecast, cohort retention, customer-feedback themes, decision: invest-more / sustain / iterate / sunset.
> Owner: PM. Attendees: full launch team + exec sponsor. Output: 1-page memo to all-hands + actions for next launch."

**How to catch it.** Check the calendar at launch+30 days. Is the retro on the calendar? If not, it won't happen.

---

## Red Flag 10: Big bang when progressive would be safer

**Symptom.** First-of-its-kind feature; high blast radius (touches billing); team chooses big-bang launch because "marketing wants a moment".

**Why it's bad.** Big bang concentrates risk on one date. For high-blast features, progressive rollout reduces customer impact at the cost of marketing optics. Choosing big-bang because of optics is choosing optics over customers.

**Bad example:**
> "Launch plan: 'Big bang on Aug 31 to coincide with the conference keynote.' Touches billing. No prior testing at scale. Day 1: 12% transaction failure rate; revenue loss in 4 hours exceeds the conference's marketing budget."

**Good example:**
> "Launch plan: progressive rollout for the billing change (5% / 25% / 50% / 100% over 14 days). Conference keynote announces the launch with 'now rolling out — most customers will see it by mid-September'. Marketing optics preserved; risk distributed; the team can pause at any stage."

**How to catch it.** For each launch, ask: "what is the smallest blast radius we could start with?" If the answer is "all users on day 1" for a non-trivial feature, big-bang is over-confident.

---

## Red Flag 11: Press materials misrepresent the feature

**Symptom.** Press release says "AI-powered fully autonomous workflow assistant". Reality: scripted workflows with one AI-summary feature. Press writes stories matching the headline; customers expect autonomous AI; product underdelivers.

**Why it's bad.** Press exaggeration produces customer disappointment and erodes brand trust. The team handed the press the wrong headline; the press wrote what they were given. Recovery is hard because the framing is now public.

**Bad example:**
> "Press release headline: 'CompanyX launches fully autonomous AI workflow agent'. Reality: rule-based workflows with optional AI summarization."

**Good example:**
> "Single source of truth for messaging: PMM-owned positioning brief signed by PM, Eng Lead, Legal at T-21. Press release written from the brief. Press briefings only led by PMM; reps cite the brief verbatim. Anti-claims documented: 'we do not claim autonomous; we claim AI-assisted scripted workflows'. Legal reviews any 'AI' claim against substantiation."

**How to catch it.** Compare the press release to the PRD's customer-benefit statements. Any escalation in claims = misalignment.

---

## Red Flag 12: T-3 go/no-go check skipped

**Symptom.** T-3. Team is busy. The launch-readiness review never happens. Launch happens with several unaddressed risks.

**Why it's bad.** The T-3 check is the last formal gate. Skipping it means risks identified earlier (ambiguous owner, unresolved bug, missing translation) ride into launch unaddressed. The cost is paid by customers and by the team on launch day.

**Bad example:**
> "T-3: PM intended to run the readiness review; busy with stakeholder fires; skipped. T-0: rolling launch; 3 of the 8 risks flagged in week-2 review are unresolved; surprises ensue."

**Good example:**
> "T-3 go/no-go review (60 min, blocked on calendar at kickoff):
> Attendees: PM, Eng Lead, PMM, Sales Lead, Support Lead, Legal, Exec Sponsor.
> Agenda: walk the readiness checklist; each row is Green / Yellow / Red. Any Red blocks launch until resolution; any Yellow has a documented mitigation. Decision: Go / No-Go (or Postpone). Documented in `assets/external-comms-checklist.md`.
> Sample T-3 decisions: Green 18/20, Yellow 2 (mitigations documented), Red 0 → Go. If any Red, postpone to T+5; restart at T-3 from the new date."

**How to catch it.** Is the T-3 review on the calendar with the right attendees? If not, the gate is missing.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | No rollback rehearsal | Show me timestamps from the last drill |
| 2 | Comms not aligned with engineering | Side-by-side PMM message vs engineering ramp |
| 3 | RACI cells unowned | Every R/A cell has a person's name? |
| 4 | Beta gates not actually met | Re-read beta exit memo before launch decision |
| 5 | Support not trained before launch | Can support agents name top-10 questions at T-3? |
| 6 | Sales has no idea | Ask 3 reps at T-3 to name what's launching |
| 7 | Single incident commander missing | Run-of-show: does it name one person with authority? |
| 8 | Exec sponsor surprised | Are scheduled briefings on the calendar? |
| 9 | 30-day retro never happens | Is the retro on the calendar at T+30? |
| 10 | Big bang when progressive is safer | What is the smallest blast radius option? |
| 11 | Press materials misrepresent | Compare release to PRD's customer-benefit claims |
| 12 | T-3 go/no-go skipped | Is the T-3 review on the calendar with right attendees? |

## Related Reading

- SKILL.md Troubleshooting
- references/launch-coordination-guide.md
- `beta-program/` (beta exit feeds launch readiness)
- `feature-flag-strategy/` (progressive rollout mechanics)
- `prfaq/` (positioning brief is the single source of truth)
- `daci-framework/` (go/no-go decision authority)
- `post-mortem/` (if the launch becomes an incident)
- Marty Cagan, *Inspired* (2018) — three launches model
