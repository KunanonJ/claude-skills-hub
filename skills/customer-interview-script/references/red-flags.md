# Red Flags: Customer Interview Script

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them. Pair with the SKILL.md and Troubleshooting table.

## How to use this document

When you have just drafted an interview script, conducted an interview, or reviewed a recording, scan the red flags below. Each red flag shows the *bad* version of a question or behavior next to the *good* version, anchored in Portigal, Torres, Fitzpatrick, and Lin's interviewing principles.

---

## Red Flag 1: Leading Questions (Telegraphing the Answer)

**Symptom.** "Would you say you wish there was a faster way to do this?" The question contains the desired answer.

**Why it's bad.** Leading questions get the answers you wanted, not the truth. Customers are socially primed to agree, especially with a friendly PM. Fitzpatrick's Mom Test specifically warns against this — interviewees give compliments and confirmation rather than facts.

**Bad example:**
> "Don't you think a calendar integration would help here?"

**Good example:**
> "Walk me through the last time you tried to schedule a meeting using this. What did you actually do, step by step?"

**How to catch it.** Read your question aloud. Could the interviewee guess your hypothesis from it? If yes, rewrite.

---

## Red Flag 2: Hypothetical / Future Questions ("Would You")

**Symptom.** "Would you use a feature that did X?" "If we built Y, would you pay for it?"

**Why it's bad.** Hypothetical answers are stated-preference fiction. Fitzpatrick: people are good at imagining their future selves, terrible at predicting their future behavior. Past behavior — what they actually did, last week — is the only reliable signal.

**Bad example:**
> "Would you use an AI assistant that summarized meetings?"

**Good example:**
> "Tell me about the last time you tried to remember what was decided in a meeting. What did you do? What did you search for? How long did it take?"

**How to catch it.** Search your script for "would you", "if we", "imagine", "in the future". Replace each with a question about past behavior.

---

## Red Flag 3: Demoing Instead of Listening

**Symptom.** Interview becomes a 40-minute product demo. PM does most of the talking. Interviewee nods politely.

**Why it's bad.** This is not an interview; it is a sales call. The PM learns nothing about the customer's actual workflow, pains, or alternatives. Portigal: rapport-building, then listening, are the entire job; product never appears in a discovery interview.

**Bad example:**
> "Let me show you what we're building. [40 min of product walkthrough.] What do you think?"

**Good example:**
> "I want to understand how you work today, before we discuss anything we are considering. Tell me about your most recent [job to be done]. What happened step by step?"

**How to catch it.** In a 60-min interview, what % was the PM talking? If above 25%, you demoed instead of listened.

---

## Red Flag 4: Soliciting Opinions Instead of Stories

**Symptom.** "What do you think about X?" "Do you like our pricing?" "How important is integration?"

**Why it's bad.** Opinions are cheap and free. Stories cost something to recount and reveal what actually mattered. Portigal and Torres both anchor interviews on stories: "tell me about the last time", "walk me through what you did" — never "what do you think."

**Bad example:**
> "How important is it to you that the tool integrates with Slack?"

**Good example:**
> "Tell me about the last time you needed information from this tool while in Slack. What did you do? Did you switch apps? What did that cost you?"

**How to catch it.** Count "story" questions vs "opinion" questions in your script. Stories should outnumber opinions 5-to-1.

---

## Red Flag 5: Compliments and Validation Hunting

**Symptom.** "Does this make sense?" "Sounds great, right?" The PM seeks validation; the interviewee provides it.

**Why it's bad.** Fitzpatrick's #1 Mom Test rule: "compliments are useless." A polite interviewee gives compliments to make the PM feel good. The PM mistakes the compliment for signal. The product fails because real concerns were never voiced.

**Bad example:**
> "And then we're thinking about adding X. That sounds useful, right?"

**Good example:**
> "And then we're thinking about adding X. What's the last time you ran into the problem this is meant to solve? How did you handle it?"

**How to catch it.** Did the interviewee say "that's great" or "sounds useful"? If yes, you got a compliment, not data.

---

## Red Flag 6: Not Probing on Surprises

**Symptom.** Interviewee says something unexpected. PM moves to the next scripted question without probing.

**Why it's bad.** Surprises are where the insight lives. Portigal: an interview that produced zero surprises was probably a confirmation-fishing expedition. Skipping the probe is leaving the insight on the table.

**Bad example:**
> Interviewee: "Actually, I export to Excel and edit there before re-uploading." PM (moving on): "Okay, next question..."

**Good example:**
> Interviewee: "Actually, I export to Excel and edit there before re-uploading." PM: "Wait — tell me more about that. Why Excel? What's the workflow look like? When did you start doing that? How long does it take?"

**How to catch it.** Mark surprises in your notes as you go. For each, did you probe at least 2 follow-up questions deep? If not, you missed insight.

---

## Red Flag 7: Asking About Future Willingness to Pay

**Symptom.** "Would you pay $X for this?" or "What would you pay?"

**Why it's bad.** Stated WTP is fiction; real WTP only emerges in actual purchase contexts. Interviewees consistently overstate willingness to pay during interviews and underspend when the moment comes. The signal you want is *what they pay for today* and *what they fired to make room for it*.

**Bad example:**
> "Would you pay $49/month for this product?"

**Good example:**
> "Walk me through your current spend on tools for this job. What did you try, what did you keep, what did you cancel? When you canceled X, what triggered that?"

**How to catch it.** Are you asking about *current spending behavior* or *hypothetical willingness*? Past behavior is the only reliable signal.

---

## Red Flag 8: Skipping Rapport-Building

**Symptom.** Interview opens with "let's get started — first question..." Five questions in, the interviewee is still giving short, guarded answers.

**Why it's bad.** Portigal: rapport quality bounds interview quality. The first 5-10 minutes are the foundation of every honest answer that follows. Skipping rapport produces guarded answers throughout the rest of the session.

**Bad example:**
> "Okay, thanks for joining. First question: tell me about your workflow." (No introduction, no context-setting.)

**Good example:**
> "Thanks for making time. Quick context: I'm not selling anything; I'm trying to learn how you do this work today. There are no right or wrong answers. I'll record so I don't miss anything; that okay? Before we dive in, what does your day-to-day look like at [company]?"

**How to catch it.** Are the first 5 minutes spent on warm-up and framing? If you went straight to a tactical question, you skipped rapport.

---

## Red Flag 9: Forgetting to Ask "Why" Multiple Times

**Symptom.** Interviewee gives a surface answer; PM accepts it and moves on. The underlying motivation is never surfaced.

**Why it's bad.** First-level answers are surface-level. The Toyota Five Whys principle applies to interviews: each layer of "why" surfaces deeper motivation, until you reach a job-to-be-done or root pain. Stopping at the first answer means stopping at the symptom.

**Bad example:**
> "I switched from tool A to tool B." "Why?" "B was better." [Move on.]

**Good example:**
> "I switched from tool A to tool B." "Why?" "B was better." "What made B better in your situation?" "It saved me an hour a week." "What were you doing with that hour before?" "Mostly waiting for A to load reports. The waiting was the killer."

**How to catch it.** For every behavior the interviewee mentions, did you ask "why" at least twice? If not, you stopped at the surface.

---

## Red Flag 10: Interview Sample Is the Wrong Population

**Symptom.** 8 interviews scheduled, all with current power users. The product's challenge is acquisition; these interviews say nothing about why prospects do not convert.

**Why it's bad.** Interview sample must match the question. To understand churn, interview churned users. To understand acquisition, interview prospects who chose competitors. Talking to happy customers about why other people don't sign up is theater.

**Bad example:**
> Goal: understand why activation rate is 12%. Interviews: 8 power users who reached activation. (Says nothing about the 88% who didn't.)

**Good example:**
> Goal: understand why activation is 12%. Interviews: 5 users who signed up and never activated, 3 who activated late (>7 days), 2 who activated quickly (as control). Sample matches question.

**How to catch it.** Write your research question. Does your sample include the population that can answer it? If not, the data is the wrong data.

---

## Red Flag 11: Confirmation-Bias Question Order

**Symptom.** Script frontloads questions about the PM's favored hypothesis. By the time other topics come up, the interviewee is primed to agree with whatever was foregrounded.

**Why it's bad.** Question order anchors the interview. Opening with "tell me about challenges with X" primes everything that follows. Mom Test recommends starting open and broad, narrowing only after the interviewee's own framing is established.

**Bad example:**
> Q1: "What's frustrating about the calendar integration?" (Anchors the interview around calendar; misses everything else.)

**Good example:**
> Q1: "Walk me through how you got work done yesterday — start of day to end. Where did you spend most of your time?" (Open; lets the interviewee surface their own priorities. Calendar comes up if it's actually a priority.)

**How to catch it.** Does the script start broad and narrow, or start narrow and anchor? Narrow-first is biased.

---

## Red Flag 12: Note-Taking That Loses the Voice

**Symptom.** Post-interview notes contain only the PM's interpretations ("user wants faster setup") with no direct quotes.

**Why it's bad.** Interpretation without quotes loses the texture and the unexpected language that drives insight. Synthesis (the `interview-synthesis/` skill) requires the original phrases. Quote-free notes are essentially fiction.

**Bad example:**
> Notes: "User wants faster setup. User likes integrations. User finds onboarding too long."

**Good example:**
> Notes: "Quote: 'I tried for 20 minutes to figure out where the dashboard was, then I gave up and asked my colleague.' Behavior: gave up after 20 min, asked human help. Quote: 'I would have paid to skip the setup, honestly.' Surprise: user mentions willingness to pay unprompted."

**How to catch it.** Are there direct quotes in your notes? Aim for 5-10 per interview. If zero, you have lost the data.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Leading Questions | Could the interviewee guess your hypothesis from the question? |
| 2 | Hypothetical "Would You" | Any "would you" / "if we" questions? Replace with past behavior. |
| 3 | Demoing Instead of Listening | PM talk time under 25%? |
| 4 | Opinions Not Stories | Stories outnumber opinions 5:1? |
| 5 | Compliment Hunting | Got "sounds great" responses? You hunted compliments. |
| 6 | Not Probing on Surprises | Each surprise probed at least 2 follow-ups deep? |
| 7 | Future Willingness to Pay | Asked about current spend, not hypothetical price? |
| 8 | Skipping Rapport | First 5 min spent on warm-up and framing? |
| 9 | Single "Why" | Asked "why" at least twice per behavior? |
| 10 | Wrong Population | Sample includes the population that can answer your question? |
| 11 | Anchoring Question Order | Script opens broad, narrows later? |
| 12 | Notes Without Quotes | 5-10 direct quotes per interview? |

## Related Reading

- SKILL.md Troubleshooting section (for symptom -> root cause -> resolution)
- references/mom-test.md (for Fitzpatrick's principles, if present)
- references/portigal-rapport.md (for rapport patterns, if present)
- interview-synthesis/references/red-flags.md (for post-interview analysis)
- identify-assumptions/references/red-flags.md (for question generation)
