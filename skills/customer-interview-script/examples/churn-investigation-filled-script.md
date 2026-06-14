# Example: Wayfinder Analytics — Filled-in Problem Discovery Interview Script for a Churn Investigation

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Wayfinder Analytics (Series-B B2B analytics platform, ~180 employees, ~3,200 paying accounts) saw mid-market churn jump from 8% to 13% over the last two quarters. Customer success has theories — pricing, competitor encroachment, missing AI features — but the PM, Anita Vasquez, does not believe stated reasons capture the truth. Many "I'm leaving because of pricing" calls actually have a behavioral root cause underneath.

Anita is conducting a 6-interview churn investigation across recently-churned and at-risk customers. The customer-interview-script skill is being applied to design a problem-discovery script (Portigal + Torres + Fitzpatrick frameworks) and to walk through one interview end-to-end with one of the churned customers, "Brian Chen" at PolySigma (mid-market data team lead).

## Inputs

- 6 interviewees scheduled (3 churned, 3 at-risk)
- 60 minutes per interview
- Recording permitted with consent
- Anita is conducting; a junior PM, Daniel, is note-taking
- Hypothesis going in: "Stated churn reason (pricing) is downstream of an unstated root cause"
- Brian Chen profile: Senior Data Lead at PolySigma (300-person company), customer for 14 months, churned 6 weeks ago, gave "too expensive" as exit reason

## Applying the skill

1. **Built the script structure before the call.** Five sections in order: rapport (10 min), context (10 min), story funnel for the job (20 min), churn-specific probe (10 min), closing (10 min).
2. **Used story-funnel structure for the meat of the interview.** Did NOT ask "why did you leave?" as an opener. The story-first approach surfaces behavior; the why-question surfaces narrative.
3. **Avoided all three Mom Test pitfalls.** No compliments. No hypotheticals. No solution-pitching. Anita scripted phrases to use AND phrases to avoid.
4. **Pre-wrote 4 specific probes for the suspected root cause.** Anita's prior was that PolySigma stopped using a key feature 30 days before churn — but did not ask that directly. Instead, she designed probes that would surface it without leading.
5. **Used silence deliberately.** Three places in the script say "[silence — count to 3]" so the interviewee fills the gap.
6. **Captured Brian's exact words.** Notes used direct quotes, not paraphrases.

## The artifact

```
================================================================
  CHURN DISCOVERY INTERVIEW — FILLED SCRIPT
  Interviewer:    Anita Vasquez, PM
  Note-taker:     Daniel Park, APM
  Interviewee:    Brian Chen, Sr Data Lead, PolySigma
  Duration:       58 minutes
  Date:           2026-05-22, 10:00-11:00 PT
  Recording:      Consented; Dovetail clip ID 24-CHURN-014
================================================================


==============================
PART 1 — RAPPORT (10 minutes)
==============================

Q: "Brian, thanks for jumping on. Before we start — this is a
   learning conversation, not a sales call. I'm not going to
   try to win you back today. I just want to understand how
   things actually went from your side, and there's nothing
   you can say that would be wrong. Sound good?"

  Brian: "Yeah, that's appreciated. The renewal call was a
         little intense so this feels different."

Q: "Mind if I record? Just for my note-taking. It'd stay
   internal to my team and would be deleted after 90 days."

  Brian: "Sure."

Q: "Great. To start really easy — walk me through your role
   at PolySigma. What do you actually do day to day?"

  Brian: "I lead a 4-person data team. We support marketing,
         finance, and operations. Most of my day is split
         between answering ad hoc questions from non-data
         people and trying to build dashboards that mean
         they stop asking me ad hoc questions."

  [silence — count to 3]

  Brian: "Honestly, the second part is what's interesting to
         me but the first part is what I get paid for."

  ANITA'S MENTAL NOTE: His real job is reducing ad-hoc
  questions. That's the JTBD lens for Wayfinder.

Q: "Got it. How long have you been doing that at PolySigma?"

  Brian: "Almost two years."


==============================
PART 2 — CONTEXT (10 minutes)
==============================

Q: "I want to understand the broader picture before we get
   into Wayfinder specifically. Walk me through the data
   tools your team uses today."

  Brian: "Snowflake for the warehouse. dbt for transforms.
         We were on Wayfinder for dashboards. Now we're
         building everything in Sigma. Hex for ad hoc
         exploration."

Q: "Pre-Wayfinder, what were you using?"

  Brian: "Nothing, really. We had Mode for a while but it
         got expensive and the team rebelled when we tried
         to make non-data people use it. Then we went to
         Wayfinder for like a year, and now Sigma."

Q: "How would you describe how those tools fit together?
   Like, who actually opens Sigma?"

  Brian: "The marketing team mostly. They self-serve from
         a set of templates my team built. Finance the
         same. Operations is more bespoke, they message me
         on Slack."

  ANITA'S MENTAL NOTE: Non-data people self-serve in Sigma
  with templates. This is the use case Wayfinder competes for.

Q: "How's that working overall?"

  Brian: "Way better than before. Way fewer Slack pings."

  [silence — count to 3]

  Brian: "I mean honestly that's the whole thing for me. If
         the tool lets marketing answer their own questions,
         my life is better. If it doesn't, my life is worse."

  ANITA'S MENTAL NOTE: Self-serve adoption by non-data
  users IS the success metric for Brian. Not feature
  richness, not price.


==============================
PART 3 — STORY FUNNEL (20 minutes)
==============================

Goal: Pull a concrete recent story about using Wayfinder
when it was still in place.

Q: "Take me back to the last time you actively built or
   modified something in Wayfinder. When was that?"

  Brian: "Probably... February? I built a churn dashboard
         for the customer success team. That was the last
         real project."

Q: "Walk me through what happened that day."

  Brian: "I had a meeting with the CS lead. He said he
         needed visibility into accounts that had stopped
         using the product. I told him I'd get him
         something by end of week. I started building in
         Wayfinder Monday morning."

Q: "What did you do first?"

  Brian: "Pulled up the existing customer-health dashboard
         in Wayfinder and tried to fork it as a starting
         point."

Q: "And what happened?"

  Brian: "The fork worked but then I couldn't change one
         of the filters. The filter was bound to a workspace
         variable that wasn't exposed in the fork. I spent
         maybe 45 minutes trying to figure that out."

Q: "How did you feel during those 45 minutes?"

  Brian: "Honestly? Stupid. Then frustrated. Then resentful,
         because that's the kind of thing I should have been
         able to do in 5 minutes."

  ANITA'S MENTAL NOTE: This is the moment. Friction in
  customization of forked dashboards. He used the word
  "resentful." Worth a follow-up question.

Q: "What did you do after the 45 minutes?"

  Brian: "I rebuilt the dashboard from scratch. Took two
         hours but I didn't have to fight the platform."

Q: "Who else was involved in that day?"

  Brian: "Just me and the CS lead at the end. I sent him
         the dashboard Friday."

Q: "Did the dashboard get used?"

  Brian: "For about three weeks. Then I switched everyone
         to Sigma in March and migrated the dashboard. CS
         lead never noticed the change."

  [silence — count to 3]

  Brian: "That tells you something, right? They didn't
         notice."

  ANITA'S MENTAL NOTE: Sigma vs Wayfinder is invisible
  to end-users. The tool change served Brian, not them.

Q: "Brian, you mentioned 'resentful' earlier. Was that
   a one-time thing with the filter, or was that a feeling
   you had at other moments?"

  Brian: "It was a lot of moments. I keep using that word
         because it's the right one. The product worked,
         like, 80% of the time. The other 20% was always
         these little things where I felt like I was
         working against the platform instead of with it.
         The forked-filter thing. Variables not scoping the
         way I expected. Two metrics with the same name in
         different workspaces. Each one was small. They
         added up."

  [silence — count to 3]

  Brian: "And the thing is — Sigma also has weird stuff. But
         when I hit a weird thing in Sigma, I can google it
         and there's a Stack Overflow answer or a Reddit
         thread. Wayfinder, it's me and the support docs
         and a 4-hour ticket response."


==============================
PART 4 — CHURN-SPECIFIC PROBE (10 minutes)
==============================

Goal: Without asking "why did you churn," surface the real
reasons through behavioral probes.

Q: "Walk me through how the decision to move off Wayfinder
   actually happened. What was the first conversation?"

  Brian: "Our CFO sent me a list of SaaS contracts to review
         in January. Wayfinder was on it. He asked: 'is this
         worth $48K a year?' I sat with it for a week."

Q: "What did you do during that week?"

  Brian: "I made a spreadsheet of what we'd built in
         Wayfinder. Then I looked at Sigma's pricing — it
         was actually almost the same as Wayfinder for our
         seat count. So price wasn't really the answer."

  ANITA'S MENTAL NOTE: HE JUST CONTRADICTED THE STATED
  CHURN REASON. He gave "too expensive" as the exit reason
  but is now saying Sigma costs the same.

Q: "Interesting — so what tipped it?"

  Brian: "Honestly? I sent both teams the same dashboard
         spec and timed how long they took to build it.
         Sigma in 40 minutes. Wayfinder still hadn't
         finished after an hour because of the variable
         thing again."

Q: "When you told the CFO the answer, what did you say?"

  Brian: "I told him we were going to switch to Sigma
         because it was cheaper."

  [silence — count to 3 — long]

  Brian: "Which... isn't true. I think I said that because
         CFOs hear 'cheaper' better than they hear 'my
         workflow is annoying.' I should have told him
         the real reason."

  ANITA'S MENTAL NOTE: STATED CHURN REASON IS WRONG. Real
  reason is workflow friction. He said "too expensive" to
  the CFO because that was the language of the SaaS review.

Q: "If you had told him the real reason, what would you
   have said?"

  Brian: "Something like — I spend 20% of my time on
         workflow friction with this tool, and the tools
         my non-data users touch are fine. So the savings
         is my time, not the license fee."

Q: "When you say 'workflow friction' — is it always the
   filters and variables thing? Or is there a category of
   thing?"

  Brian: "It's anything that requires me to mentally model
         what's happening under the hood. Like, the tool
         should hide that. When it leaks the abstraction,
         I lose flow."

Q: "Tell me about a time the tool didn't leak the
   abstraction. Was there a thing it was good at?"

  Brian: "Yeah — the data-cataloging stuff was actually
         really nice. I just wish the dashboard editor
         had the same care put into it."


==============================
PART 5 — CLOSING (10 minutes)
==============================

Q: "I have a couple of last questions and then I'll let
   you go. Is there anything you wish I had asked you?"

  Brian: "I think you got it. Maybe one thing — the support
         experience. Tickets took 4-24 hours. Sigma has a
         Slack channel where someone responds in 10 minutes.
         That sounds small but when you're in a flow state
         and stuck, 4 hours is a long time."

Q: "If a magic wand fixed everything about the dashboard
   editor friction tomorrow, would you have stayed?"

  Brian: "Honestly... maybe. The data cataloging stuff was
         genuinely better than Sigma. Workflow friction
         was the deal-breaker. I'm not sure it's solvable,
         to be fair — that's a deep product decision."

Q: "Anyone else on your team or in your network I should
   talk to who had a similar experience?"

  Brian: "There's a guy at Helios who churned a few months
         ago. I think for the same reason. I'll DM you his
         email."

Q: "Brian, this was tremendously helpful. Thank you. Last
   thing — can I check back in three months and see how
   Sigma is working out?"

  Brian: "Sure. And honestly — if you fix the workflow
         thing, I'd take another look. Just an honest look,
         no promises."

================================================================
POST-INTERVIEW DEBRIEF (Anita + Daniel, 10 min)
================================================================

Top 3 takeaways:
  1. STATED churn reason ("too expensive") IS NOT the real
     reason. Real reason is workflow friction in dashboard
     authoring. Brian himself acknowledged the
     misattribution during the interview.
  2. The friction is a recurring pattern around mental
     model leakage (filters, variables, scope). NOT a
     single missing feature.
  3. Support response time is the secondary factor. 4-24 hr
     ticket SLA vs. competitor's 10-min Slack response
     compounds the workflow friction.

One contradiction captured:
  - Brian said "too expensive" on exit; said in interview
    that Sigma costs about the same. Pricing is being used
    as the socially-acceptable language for workflow
    annoyance.

One surprise:
  - The data-cataloging product IS better than competitor's.
    Brian volunteered this. We are not communicating it
    well. Possible "save" lever for at-risk accounts.

Followups:
  - Ask Brian for the Helios contact (immediate)
  - Brian invited a 3-month follow-up — schedule it now
  - Anita should re-listen to the recording around minute
    23 ("each one was small. They added up.") and at the
    "resentful" moment — these are the high-signal quotes

Direct quotes worth preserving:
  - "Working against the platform instead of with it"
  - "Each one was small. They added up."
  - "I told him cheaper because that's the language of
    SaaS reviews"
  - "When it leaks the abstraction, I lose flow"


WHAT ANITA DID NOT DO
---------------------
  - Did not pitch the Wayfinder roadmap (no "we're building X")
  - Did not ask "what would make you come back" until the
    very end as a closing
  - Did not say "that's a great point" even once
  - Did not interrupt the silences
  - Did not reframe Brian's complaints sympathetically
    (the resistance to "yeah, the platform is hard" is
    intentional; it would have biased him toward more
    complaints)
  - Did not ask about features by name
```

## Why this works

- **Story-first, not "why" first.** Anita opened the main section with "Walk me through the last time you actively built something in Wayfinder" — not "Why did you churn?" The story produced the "resentful" moment and the filter-friction pattern. A direct "why" question would have produced "too expensive" again.
- **Caught the contradiction live.** When Brian said Sigma cost the same as Wayfinder, Anita followed up with "so what tipped it?" — which surfaced that the stated churn reason was wrong. That single moment is worth the entire interview.
- **Used silence three times.** After the role description, after "resentful," after the CFO conversation. Each gap produced the most important sentence in that section. Less-experienced interviewers fill the silence themselves and bury the signal.
- **Avoided all three Mom Test failure modes.** No compliments (would have biased toward agreement), no hypotheticals (the magic-wand question at the end is the one exception — used intentionally as closing, not as core data), no solution pitching.
- **Captured direct quotes, not paraphrases.** "Working against the platform instead of with it" and "Each one was small. They added up." are the quotes that will go into the synthesis. Paraphrases lose the texture.
- **Named what wasn't done.** The "what Anita did NOT do" section is the discipline. Each item is something a less-experienced PM would have done and degraded the interview signal.
- **Got a referral.** Asked at the end. Got one (Helios). One interview snowballed into two.

## What's next

- Synthesize this and the other 5 churn interviews using [`../interview-synthesis/`](../interview-synthesis/) into an opportunity solution tree with the friction patterns at the top.
- Convert the workflow-friction insight into testable assumptions via [`../identify-assumptions/`](../identify-assumptions/) before committing to any roadmap response.
- The misattribution insight (price vs friction) goes to [`../../execution/customer-feedback-triage/`](../../execution/customer-feedback-triage/) so the CS team stops categorizing similar exits as "pricing."
- For at-risk accounts, the data-cataloging strength (volunteered by Brian) becomes a "save" lever — frame this for CS leadership.
- Workflow-friction patterns feed a [`../brainstorm-ideas/`](../brainstorm-ideas/) trio session for the dashboard editor.
- Brian's 3-month follow-up is on Anita's calendar and uses the same skill.
