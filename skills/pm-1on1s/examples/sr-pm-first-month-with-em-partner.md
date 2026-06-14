# Example: Priya's First Month of Weekly 1:1s with her EM Partner

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Priya Rao is a newly promoted Sr PM at Northwind SaaS (Series-B logistics platform, ~150 engineers). She just took over the Payments team after the previous PM left abruptly. Her engineering partner, Marcus Lee, has been the Payments EM for 18 months. They have never worked together. Marcus was Priya's biggest internal advocate during her promo cycle, but they have no shared operating model yet.

This is exactly the scenario the pm-1on1s skill's "Type B: With your engineering manager partner" template is designed for. The first month sets the partnership tone for the next year. Priya is using the skill to keep the 1:1s structured without making them feel scripted.

## Inputs

- Priya: 4 years PM experience, first time as Sr PM, first time on Payments
- Marcus: 18 months as EM, 9 engineers reporting to him, on-call rotation owner
- Cadence agreed: weekly, Tuesdays 11:00-11:30, in person when possible
- Open partnership questions:
  - Who owns roadmap commitments to leadership?
  - Who runs sprint planning?
  - How are escalations handled at 11pm on a Friday?
- Recent context: a Black Friday payment outage 3 weeks ago that the previous PM mishandled

## Applying the skill

1. **Used the Type B template, not the Type A.** Priya is partnering with Marcus, not reporting to him. The "manager" template would have inverted the agenda and made the conversation feel hierarchical.
2. **Set expectations in week 1.** Used the kickoff variation: shared the agenda template up front, agreed on default questions, agreed that cancelled 1:1s get rescheduled rather than skipped.
3. **Care personally, challenge directly.** Priya consciously asked at least one Radical Candor "challenging" question every week — even when the partnership felt smooth. The instinct of a new Sr PM is to be agreeable.
4. **Rotated topics weekly.** Instead of repeating the same agenda, Priya rotated through the suggested topic categories (roadmap, team dynamics, shared partner feedback, operational risk).
5. **Documented agreements, not transcripts.** Each 1:1 ended with 1-3 agreements written to a shared Confluence page. The notes are 6 lines per week, not 600.

## The artifact

```
================================================================
  Priya Rao <> Marcus Lee — Weekly 1:1 Log
  Cadence: Tuesdays 11:00-11:30
  Shared space: Confluence > Payments > Operations > 1:1 Log
================================================================


--- KICKOFF 1:1 — 2026-05-05 (Week 0) ---

PURPOSE
Set our operating model for the partnership.

AGENDA (40 min, one-time extended)
  5  min  Personal check-in
  10 min  What kind of PM/EM partnership do we each want?
  10 min  Default 1:1 agenda + cadence
  10 min  How we handle the hard stuff (escalations, conflict)
  5  min  Closing agreements

AGREEMENTS
  1. Default 1:1 agenda = Type B template from pm-1on1s skill.
  2. Cancelled 1:1s get rescheduled within 5 business days.
     If neither can find a slot, we call it on Slack.
  3. Roadmap commitments to leadership: Priya owns the framing,
     Marcus owns the estimate. Neither commits without the other.
  4. Sprint planning: Marcus facilitates, Priya owns the goal
     statement and pre-reads.
  5. Escalations: 11pm-Friday rule -> page Marcus first if it is
     a system issue; ping Priya first if it is a customer issue;
     either of us can pull the other in any time.
  6. Direct feedback is expected. We will each ask for one piece
     of feedback per month explicitly.

PERSONAL NOTES (only what they shared, not interpretations)
  Marcus is taking 2 weeks of paternity leave in late July.
  Priya is studying for an executive program in fall, exec
  sponsorship needed.


--- WEEK 1 — 2026-05-12 ---

TOP OF MIND
  Priya: I have not met half the team. What is the right way to
         do the meet-and-greets without it feeling performative?
  Marcus: Black Friday post-mortem is in 3 days. Three engineers
          on the team are still raw about the outage.

DISCUSSION
  Agreed Priya will join Marcus' next team standup as an observer
  on Wednesday — no agenda, no introductions, just sit in the back.
  Marcus will send a Slack message Tuesday afternoon framing it as
  "Priya is here to listen, not to interrogate."

  On the post-mortem: Marcus shared he is worried the engineers
  will blame the previous PM in the room. Priya offered to open
  the meeting with a blameless framing.

PRIYA'S CHALLENGE QUESTION
  "Is there anything I have done in the first week that has made
   your job harder?"
  Marcus: One thing — Priya scheduled a roadmap review for
  Thursday that conflicts with on-call sync. He had not flagged
  it because she is new.

AGREEMENTS
  1. Priya joins team standup Wed as silent observer.
  2. Priya re-schedules Thursday roadmap review off on-call sync.
  3. Priya opens post-mortem Friday with blameless framing.


--- WEEK 2 — 2026-05-19 ---

TOP OF MIND
  Priya: The post-mortem went well, but two engineers came to me
         after with separate "off the record" concerns about the
         on-call rotation. I do not want to triangulate.
  Marcus: I am behind on hiring the senior engineer slot we
          opened in March.

DISCUSSION
  Priya described what she heard without naming engineers. The
  pattern: on-call burden is uneven; one engineer is taking 40%
  of pages. Marcus already knew but had not realized engineers
  were going around him.

  Marcus asked Priya to send those engineers back to him with
  a script: "Have you raised this directly with Marcus?" Priya
  agreed.

  On hiring: Marcus is screening but the pipeline is thin.
  Priya offered to help by writing a clearer JD focused on
  payments-specific work. Marcus accepted.

PRIYA'S CHALLENGE QUESTION
  "If I were doing one thing differently to be a better partner
   for you, what would it be?"
  Marcus: Slow down on Slack DMs. Priya sent 14 DMs Monday;
  Marcus prefers a single threaded update.

AGREEMENTS
  1. Priya redirects future "off the record" concerns back to
     Marcus directly using the agreed script.
  2. Priya drafts a new payments-specific JD by Friday.
  3. Priya consolidates Slack DMs into a single thread by topic.


--- WEEK 3 — 2026-05-26 ---

TOP OF MIND
  Priya: I want to take a position on the next quarter's
         roadmap before our planning offsite. Want to pressure-
         test with you.
  Marcus: One of our senior engineers is interviewing externally.
          I cannot name them, but it affects what we commit to.

DISCUSSION
  On the roadmap: Priya walked through three bets she is
  considering, ranked by RICE. Marcus pushed back on bet #2
  (chargebacks rebuild) — said the architecture risk is bigger
  than Priya is modeling. Agreed to redo the estimate with
  the senior engineer who knows the chargebacks code.

  On the at-risk engineer: Marcus did not name them, which
  Priya respected. They agreed to model the roadmap with two
  capacity scenarios (full vs minus-1 senior). This is the
  partnership signal: Marcus trusted Priya enough to share
  the risk; Priya did not push to know who.

PRIYA'S CHALLENGE QUESTION
  "What is an opinion you have about the roadmap you have not
   shared with me yet?"
  Marcus: He thinks the chargebacks rebuild is being driven by
  one loud customer, not by the data. Priya promised to pull
  the actual support volume and churn data before the offsite.

AGREEMENTS
  1. Priya pulls chargebacks support + churn data by Friday.
  2. Marcus + senior engineer re-estimate chargebacks rebuild.
  3. Roadmap modelled at two capacity scenarios.


--- WEEK 4 — 2026-06-02 ---

TOP OF MIND
  Priya: The roadmap offsite is next week. I am nervous about
         the leadership conversation if we don't commit to the
         chargebacks rebuild.
  Marcus: We are not nervous about the same thing. I am
          worried about burnout on the team if we commit to
          three big bets at once.

DISCUSSION
  This was the first 1:1 where the conversation got genuinely
  hard. Priya wanted to commit to three bets. Marcus pushed
  back: two bets max. They disagreed for 12 minutes.

  Resolution: not a compromise. Priya agreed Marcus' team
  health concern is the binding constraint and that two bets
  is the right commit. Priya will own the leadership
  conversation about why bet #3 is deferred. Marcus owns
  team morale conversation post-offsite.

  This is the partnership signal: they disagreed openly, named
  it, and one of them moved.

PRIYA'S CHALLENGE QUESTION (asked by Marcus this time)
  "Is there anything I am doing that is making YOUR job harder?"
  Priya: Marcus' Friday afternoon Slack messages tend to be
  high-context with no TL;DR; she has spent 20 minutes
  reconstructing them twice this month. Asked for a one-line
  summary at the top.

AGREEMENTS
  1. Roadmap commit: 2 bets. Priya owns the leadership comms.
  2. Marcus owns team morale comms post-offsite.
  3. Marcus adds TL;DR to long Friday Slack messages.
  4. Schedule month-2 retro for 2026-06-09.


================================================================
  MONTH 1 RETRO — 2026-06-09
================================================================

WHAT WORKED
  - Kickoff template set the operating model on day one. No
    ambiguity about roadmap ownership or escalation paths.
  - "What is making your job harder" question normalized direct
    feedback by week 1. By week 4, Marcus volunteered the
    same question back unprompted.
  - Documented agreements, not transcripts. The shared
    Confluence log is 30 lines per week, not 300. Both can
    skim it before next week.

WHAT TO ADJUST
  - 30 minutes is tight. Considered moving to 45, decided to
    keep 30 + an overflow 30 only when needed.
  - Topic rotation: 4 weeks of "what is on your mind" defaulted
    to operational. Need to deliberately schedule a roadmap-
    only and a people-only 1:1 each month.

WHAT TO KEEP
  - Tuesday 11:00 slot — never skip, reschedule if needed.
  - Each of us asks one Radical Candor "challenging" question
    per 1:1.
  - Closing 2 minutes always for agreements + next-week prep.

NEXT MONTH'S FOCUS
  - Hiring: stay tight on the senior engineer JD pipeline.
  - The interviewing engineer situation (no names, just two
    capacity scenarios held in mind).
  - Marcus' paternity leave coverage plan (he is out late July).
```

## Why this works

- **Used the Type B template, not the manager template.** PM-EM partnerships are peer relationships. New Sr PMs default to a manager-style agenda and inadvertently create hierarchy where none exists.
- **The kickoff 1:1 set the rules.** Roadmap ownership, escalation rules, and feedback expectations were named on day zero. Without that, week 4's hard conversation would have been a power struggle, not a partnership decision.
- **One challenge question per week.** Priya forced herself to ask one Radical Candor "challenging" question every single 1:1 — even when the relationship felt smooth. By week 4, Marcus reciprocated. That is the relationship moving from ruinous empathy to actual partnership.
- **Agreements, not transcripts.** Each entry is 20-30 lines. The instinct to capture everything kills psychological safety. The shared Confluence log is reviewable, not surveillance.
- **Held the line on team health.** In week 4 Priya wanted to commit to three bets. Marcus pushed back on team health. Priya moved — not because she "lost," but because the binding constraint was real. A weaker partnership would have compromised to "two and a half bets."
- **Refused to triangulate.** When team members went around Marcus to Priya, she sent them back. This is the single biggest trust accelerator in a new PM-EM partnership.

## What's next

- For Priya's own 1:1s with her manager, switch to the Type A template from this same skill.
- The roadmap offsite is the handoff to [`../../execution/outcome-roadmap/`](../../execution/outcome-roadmap/) and [`../../execution/quarterly-planning/`](../../execution/quarterly-planning/).
- The Black Friday post-mortem learnings should feed [`../../execution/post-mortem/`](../../execution/post-mortem/) and any preventive work tracked through [`../../delivery-manager/`](../../delivery-manager/).
- Marcus' paternity coverage planning maps to [`../../program-manager/`](../../program-manager/) for cross-team capacity modeling.
- As Priya grows, she can use [`../pm-career-ladder/`](../pm-career-ladder/) to map what behaviors at this 1:1 level look like at the next ladder rung (Group PM).
