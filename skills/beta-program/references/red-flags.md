# Red Flags: Beta Program

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan the beta plan, recruitment script, weekly cadence, and exit memo for these patterns before opening recruitment. Each red flag shows the *bad* version next to the *good* version, anchored to the Friends/Family/Fanatics cohort model and Kano scope decisions.

---

## Red Flag 1: Vanity recruit (friends only)

**Symptom.** The recruitment list is 25 internal employees and 5 personal contacts. No Fanatics cohort cold-recruited from the ICP.

**Why it's bad.** Friends-cohort feedback is biased toward "this is great". Without Fanatics — cold-recruited prospects with the actual problem — the beta validates how the team uses the product, not whether the market wants it. The exit memo reads positive; GA flops.

**Bad example:**
> "Beta cohort: 30 employees from the engineering org + 5 advisor friends. Recruitment complete in 2 days."

**Good example:**
> "Beta cohort across 3 rings: 8 Friends (employees + 2 advisors); 15 Family (existing customers who opted in via product update email, screened for active use of the legacy feature); 12 Fanatics (cold-recruited via 2 industry Slack groups + LinkedIn outreach, ICP-screened for active pain in this area). 35 total; sequenced Friends -> Family -> Fanatics with 1-week overlap."

**How to catch it.** Count Fanatics. If under 30% of the cohort, the beta will not test acquisition risk.

---

## Red Flag 2: No exit criteria set before recruitment

**Symptom.** The team opens recruitment with placeholder metrics ("we'll figure out success when we see it"). Exit memo gets backfilled with whatever the data showed.

**Why it's bad.** Without pre-agreed gates, the exit decision becomes a vibe check. The exec sponsor will rationalize ship-it or kill-it based on the loudest signal. The exit memo loses defensibility.

**Bad example:**
> "Beta success: 'users like it'. Exit gate: 'team decides at end of week 6'."

**Good example:**
> "Exit gates, signed by PM + Eng Lead + Exec Sponsor on 2026-04-30, locked in `assets/beta-program-plan.md`: (1) Activation: >= 70% reach first key action in 7 days. (2) Engagement: median >= 3 sessions/week. (3) Outcome: >= 50% achieve the 'reduces close time by 30%' headline. (4) Crash-free: >= 99.5%. (5) P0 bugs: 0 open at exit. (6) Quotable testimonials: >= 3 named participants. Failure on any 2 of the first 4 = Extend or Pivot decision."

**How to catch it.** Look at the exit memo template. If thresholds are blank or vague, recruitment must wait.

---

## Red Flag 3: Beta-as-launch

**Symptom.** The "beta" is announced via a launch press release. 5,000 sign-ups expected. Marketing is treating it as soft GA.

**Why it's bad.** This is not a beta — it is an under-resourced launch with the word "beta" attached. 5,000 users at unknown stability is a support crisis. Feedback signal at that volume becomes noise. The actual purpose of beta (controlled learning before GA) is lost.

**Bad example:**
> "Beta launch: announced on TechCrunch + blog + 50k-subscriber newsletter. 'Sign up for the beta — limited spots' (no actual cap configured). Day 1: 3,200 signups."

**Good example:**
> "Closed beta: 30 invited participants across 3 cohorts. Recruitment via 1:1 outreach, not public announcement. Beta is not press-worthy at this stage. If we want a soft launch with broader audience, that is a separate decision after the closed beta exit; see `launch-playbook/`."

**How to catch it.** Count target participants. > 50 is no longer "closed beta" in most contexts.

---

## Red Flag 4: No Delight features in beta scope

**Symptom.** Beta ships with only Must-be features (Kano basic). Feedback at exit is neutral; no quotable testimonials.

**Why it's bad.** Must-be features generate no positive surprise — users notice their absence but not their presence. Without 1-2 Delight features, beta produces neutral feedback and no quotes for the launch press release.

**Bad example:**
> "Beta scope (v1): login, dashboard, basic CRUD on the main object, settings page. 'Keep it minimal so we don't have to fix bugs.'"

**Good example:**
> "Beta scope: all Must-be features stable (login, dashboard, CRUD). Plus 2 Delight features: (1) auto-summary of the user's last 7 days of activity on first dashboard load, (2) one-click export to the user's preferred BI tool. Delights are where we will get quotable testimonials; we accept the bug-fix cost."

**How to catch it.** Review the scope. Tag each feature Must-be / Performance / Delight. If 0 Delight features, the beta will produce no quotes.

---

## Red Flag 5: Silent cadence

**Symptom.** The team sends 1 welcome email on day 1, then nothing until week 4. Engagement crashes after week 2.

**Why it's bad.** A beta dies of silence. Participants who do not hear from the team within a week assume the program stalled. They disengage; the team gets no signal. The cadence is not optional — it is the program.

**Bad example:**
> "Comms plan: welcome email day 1; 'we'll check in periodically with updates and questions'."

**Good example:**
> "Weekly cadence (locked in `assets/weekly-cadence-template.md`):
> Mon — digest: what shipped, known issues, one specific thing to try this week.
> Tue — 30-min open office hours (Zoom).
> Wed — internal beta health review (PM).
> Thu — 2-3 1:1s with rotating participants.
> Fri — metrics snapshot to the participant Slack.
> Owner: PM. SLA on participant question: 1 business day."

**How to catch it.** Open the participant Slack at week 2. If the team has not posted in 5+ business days, the program is silent.

---

## Red Flag 6: Recruitment leads with features instead of problems

**Symptom.** The outreach email opens "We're launching an exciting new AI assistant — want to try it?" Conversion rate is 4%.

**Why it's bad.** Feature-led recruitment attracts curiosity, not pain. Curious users don't activate; the cohort fills with people who never had the problem the product solves. Outcome metrics fail at exit because the wrong people were in the cohort.

**Bad example:**
> "Subject: Try our new AI assistant before anyone else! Body: 'We're launching a powerful new AI assistant. We'd love your feedback. Sign up here.'"

**Good example:**
> "Subject: Beta — close deals 30% faster with auto-research. Body: 'You mentioned in our last call that pre-meeting research takes 90+ minutes per opportunity. We are testing a tool that compresses that to 10 minutes. We're inviting 15 sales leaders to a closed 6-week beta starting May 28. The ask: 2 hours/week using the product + a 30-min weekly chat. The payoff: you get the tool 4 months before GA and shape v1. Reply if interested.' Targeting: prospects who explicitly named this pain in discovery."

**How to catch it.** Read the recruitment email. If the first paragraph names the product before naming the problem, rewrite.

---

## Red Flag 7: Exit-gate metrics from a 5-person cohort

**Symptom.** Exit memo shows "80% activation" — but n = 5. Sponsor wants to ship.

**Why it's bad.** A 5-person beta is not statistically representative. Eight users out of 10 reaching activation tells you very little about the broader population. Treating that as a green light to GA ignores the variance.

**Bad example:**
> "Exit memo: 8/10 activated (80%). Outcome achieved by 6/10 (60%). Greenlight GA."

**Good example:**
> "Exit memo: cohort size n=30 (Friends 8, Family 14, Fanatics 8). Weighted scoring per the Caveats section: Fanatics weighted 2x. Activation: Friends 7/8 (88%), Family 10/14 (71%), Fanatics 5/8 (63%). Weighted: 71% — above 70% gate. Outcome: 4/8 Fanatics (50%) — meets gate but with low margin and small n. Decision: Extend beta 2 weeks to add 10 more Fanatics before greenlighting."

**How to catch it.** Compute n. If under 20, your gate numbers should be advisory at best.

---

## Red Flag 8: Friends-cohort feedback weighted equally

**Symptom.** Exit memo treats all participant feedback equally. Friends-cohort enthusiasm carries the average.

**Why it's bad.** Friends are biased toward saying "this is great" — they want the project to succeed. Family is moderately biased. Fanatics — cold-recruited with the actual pain — give the cleanest signal. Treating them equally inflates the apparent quality.

**Bad example:**
> "NPS: Friends 65, Family 40, Fanatics 25. Average: 43. Above the 30 gate."

**Good example:**
> "NPS by cohort: Friends 65, Family 40, Fanatics 25. Per the SKILL.md guidance, Fanatics weighted 2x in the exit decision (they represent the acquisition risk). Weighted score: (65 + 40 + 25*2) / 4 = 38.75. Discussion at exit-gate review: Fanatics NPS of 25 is concerning. What did they say about the gap? Do we extend beta to investigate, or is this a fundamental fit problem?"

**How to catch it.** Look for separate Fanatics-cohort metrics in the exit memo. If they're aggregated with Friends, weighting is being skipped.

---

## Red Flag 9: No explicit NDA or beta agreement

**Symptom.** The team assumes participants understand confidentiality. A Fanatics-cohort participant posts a feature screenshot to LinkedIn in week 3.

**Why it's bad.** Implied NDAs are unenforceable and create surprise. The leak forces an awkward correction; the leaker feels accused. Competitors see the feature early.

**Bad example:**
> "Participant onboarding email: 'We'd appreciate you keeping this confidential while we're in beta. Thanks!'"

**Good example:**
> "Activation packet includes: (1) one-page beta agreement signed via DocuSign (confidentiality for 90 days, ownership of feedback, no-warranty disclaimer). (2) Explicit list of what they can/cannot share — internally with their team yes, externally no until launch. (3) An early-public-praise window in the final week to channel enthusiasm legitimately. Reviewed with Legal."

**How to catch it.** Ask: "Show me the signed beta agreement for participant X." If none exists, the NDA is implied.

---

## Red Flag 10: Exit drags past planned window

**Symptom.** Beta planned for 6 weeks. Now in week 11, no exit decision. Team keeps adding features.

**Why it's bad.** Open-ended betas consume budget and morale. The team uses "still in beta" as an excuse to keep iterating instead of committing to GA or kill. Participants disengage; their feedback fatigues.

**Bad example:**
> "Week 11 update: 'still in beta — making good progress. Will revisit timeline next week.'"

**Good example:**
> "Beta was 6 weeks. At week 6 the exit memo went to the DACI driver. Outcome: Extend by 2 weeks to close the Fanatics-cohort activation gap with named action items. At week 8: definitive Greenlight / Extend / Pivot / Kill decision; no further extensions. If extension #2 is needed, the program is restructured as a new closed-beta cohort, not a continuation."

**How to catch it.** Look at the start date and the exit-memo date. If exit is > 8 weeks from start with no decision, the program has slipped from beta to "limbo".

---

## Red Flag 11: One-off enterprise customizations during beta

**Symptom.** The largest beta customer says "we'd buy this if it did X". Engineering builds X for that one customer. Other participants don't get it.

**Why it's bad.** Customization during beta produces a product that ships for one customer and ships poorly for everyone else. It also conflates the beta (learning) with sales (closing). The team optimizes for the loudest paying voice.

**Bad example:**
> "Acme Corp asked for a custom export format; eng built it in week 3 to keep them happy. Week 5: another participant asks for a different custom format."

**Good example:**
> "Acme Corp request logged in the customer-feedback-triage queue. PM responds: 'we hear you; this is going through our triage with the other beta input. We will commit to it in v1.1 if the broader signal supports it.' No mid-beta one-offs. Sales-promised customizations are tracked separately and reported monthly per `customer-feedback-triage/` discipline."

**How to catch it.** Ask the build team: "Have you built anything for one beta participant that the others don't have?" If yes, the program is drifting to bespoke.

---

## Red Flag 12: Decision deferred past the 5-day SLA

**Symptom.** Beta ends. Exit memo not published until 3 weeks later. Decision deferred to the next exec offsite.

**Why it's bad.** Delay erodes momentum. Participants lose context; engineering loses focus. The "GA timeline" becomes mythical. The DACI driver loses authority; the decision becomes consensus mush.

**Bad example:**
> "Beta ended May 12. Exit memo due 'soon'. GA decision: 'we will discuss at the quarterly review on June 28.'"

**Good example:**
> "Beta ended May 12. Per DACI: PM (Sarah K) is the Driver. Exit memo committed for May 17 (5 business days). Review meeting May 18. Documented decision (Greenlight / Extend / Pivot / Kill) by May 19, communicated to participants and exec sponsor. If the decision is Greenlight, kickoff with `launch-playbook/` happens within 7 days."

**How to catch it.** Look at the beta-end date and the exit-memo-publication date. Gap should be <= 5 business days.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Vanity recruit (friends only) | Is the Fanatics cohort >= 30% of total? |
| 2 | No exit criteria pre-recruitment | Are all gate thresholds locked before opening recruitment? |
| 3 | Beta-as-launch | Is target participant count > 50? |
| 4 | No Delight features in scope | Tag each feature Kano-class; is any classed Delight? |
| 5 | Silent cadence | Has the team posted in participant channel in last 5 business days? |
| 6 | Recruitment leads with features | Does the email's first paragraph name the product or the problem? |
| 7 | Exit-gate from < 20 participants | What is n? |
| 8 | Friends-feedback weighted equally | Are Fanatics-cohort metrics reported separately? |
| 9 | No explicit NDA | Show me the signed beta agreement. |
| 10 | Exit drags past window | Has the program run > 8 weeks without a decision? |
| 11 | One-off enterprise customizations | Has the team built anything for only one participant? |
| 12 | Decision deferred past 5-day SLA | Gap between beta-end and exit-memo publication? |

## Related Reading

- SKILL.md Troubleshooting
- references/beta-program-guide.md
- `daci-framework/` (for the exit-decision driver)
- `launch-playbook/` (for GA handoff)
- `customer-feedback-triage/` (for handling participant requests)
