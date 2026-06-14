# Customer Interview Methodology Guide

Deep reference for the live-interview craft. Synthesizes Portigal, Torres, Fitzpatrick, and Lin into a single applied playbook.

---

## 1. Why interview technique matters more than question content

A common mistake is to spend three days writing questions and zero minutes practicing how to ask them. The opposite ratio produces better data.

The same question -- "Tell me about the last time you tried to reconcile a payment" -- produces wildly different answers depending on:

- The 30 seconds of rapport that preceded it
- Whether the interviewer paused after the participant's first sentence
- Whether the follow-up probe pulled for a story or accepted an opinion
- Whether the interviewer flinched, agreed, or stayed neutral when the participant criticized the product

Method is the multiplier on every question.

---

## 2. Portigal: Interviewing Users in detail

Steve Portigal's *Interviewing Users* (2013, second edition 2023) is the canonical text on qualitative customer research craft. Key principles applied here:

### 2.1 The researcher's stance

Portigal frames the interviewer as a *learner*, not an *expert*. This is more than humility -- it is a structural choice that changes the participant's behavior. An expert posture causes the participant to perform for the interviewer; a learner posture causes them to teach.

**Practical signals of a learner stance:**

- Ask the participant to explain things you "already know" -- jargon, processes, tools
- Take notes visibly so they can see you are learning
- Say "I don't understand -- can you explain that?" when something is unclear (even if you do understand)
- Avoid completing the participant's sentences

### 2.2 The orientation phase

Portigal emphasizes that the first 5-10 minutes set the trajectory for the rest of the interview. He recommends:

1. **Introduce the research, not the product.** "We're studying how people manage payments" -- not "We're building a payments product."
2. **Disclaim wrong answers.** "Whatever you say is helpful -- there is no right or wrong."
3. **Frame the time.** "We have 60 minutes. If you need a break, just say so."
4. **Start with the participant's expertise.** Open with a question only they can answer (their role, their week, their tools).

### 2.3 Listening for the unexpected

Portigal argues the most valuable interview moments are surprises -- statements that violate the team's mental model. The interviewer's job is to notice them in real time and probe.

**Surprise markers to listen for:**

- "Actually, the way I do it is..." (deviation from expected workflow)
- "Most people don't know this, but..." (insider information)
- "It depends on..." (conditional behavior that hides a system)
- Long pauses before answering simple questions (something complicated underneath)
- Emotional language ("frustrating", "scary", "love") -- emotions mark importance

### 2.4 Reading the room (and the screen)

For remote interviews:

- Watch the participant's eyes -- when they look away to think, that is the most honest answer coming
- Notice tool switches if they are screen-sharing
- Use video; audio-only loses 30-40% of behavioral signal

For in-person:

- Note the workspace -- artifacts on the wall, monitor arrangement, paper notes
- Ask about anything you see ("What's that diagram?")

---

## 3. Torres: Continuous Discovery Habits in detail

Teresa Torres' *Continuous Discovery Habits* (2021) introduced the now-standard weekly-touchpoint cadence and the opportunity solution tree. For interview craft, the key contributions are:

### 3.1 The story-based interview

Torres argues that asking for *stories* (specific past events) rather than *opinions* (general statements about future behavior) is the single highest-leverage shift a PM can make.

**The diagnostic test:**

After every participant answer, ask yourself: *Could a different participant give the exact same answer?* If yes, you collected an opinion. If no, you collected a story.

Opinion: "Onboarding is too hard." (Anyone could say this.)
Story: "On my third day I tried to upload the CSV but it kept rejecting the date format, so I called Mike and we spent 40 minutes fixing it together." (Only this participant could say this.)

### 3.2 The Continuous Discovery cadence

Torres recommends a *weekly* touchpoint with customers, not quarterly research sprints. The implications for interview craft:

- **Shorter, more frequent.** 30-60 minute interviews, not 2-hour deep-dives.
- **Lower stakes per interview.** Miss something? You'll be in another interview next week.
- **Compounding learning.** Each interview's findings inform next week's questions.
- **Team-based.** The full Product Trio (PM, Designer, Engineer) participates -- not just the researcher.

### 3.3 The opportunity solution tree as an interview goal

Torres frames the *output* of an interview as: new branches on the opportunity solution tree (`discovery/interview-synthesis/`). This goal changes how you interview:

- You are listening for **opportunities** (customer needs, pains, desires)
- You are *not* primarily listening for solutions
- When a participant pitches a solution, redirect to the underlying opportunity: "What is that solving for you?"

---

## 4. Fitzpatrick: The Mom Test in detail

Rob Fitzpatrick's *The Mom Test* (2013) is the shortest book in the PM canon and arguably the most useful. The core premise: even your mother, who loves you, will tell you your idea is great. Most interview answers are polite signal, not real signal.

### 4.1 The three rules (full version)

**Rule 1: Talk about their life instead of your idea.**

Bad: "We're building a tool that does X. What do you think?"
Good: "Walk me through how you handle X today."

If they never mention your product category unprompted, that is itself signal -- it is not a problem they think about.

**Rule 2: Ask about specifics in the past, not generics or opinions about the future.**

Bad: "Would you ever pay for a tool that did X?"
Good: "What tools do you currently pay for that touch this workflow? How much?"

The participant's wallet is a better source of truth than their stated preferences.

**Rule 3: Talk less, listen more.**

Aim for a 30/70 split -- interviewer 30%, participant 70%. Use silence (see Section 6) and short prompts ("Tell me more", "What happened next?") rather than long questions.

### 4.2 Compliments are red flags

When a participant says "That's a great idea!" or "I would definitely use that!", you have learned almost nothing -- you have only confirmed that they are polite. Probe past behavior:

> Participant: "I would totally use that!"
> Interviewer: "That's encouraging. Tell me what you do today for that job. What tools? How often?"

If they cannot describe current behavior, the "I would use it" is fluff.

### 4.3 The price of a customer's time

Fitzpatrick observes that the strongest signal a customer cares about a problem is what they have already done about it:

- **Built a workaround** -- They care a lot
- **Pay another tool** -- They care a lot
- **Complained to their boss** -- They care
- **Googled it** -- Mild care
- **Mentioned it in an interview** -- Almost nothing

Probe for evidence at the top of the ladder: "What have you tried? What did you spend on it? What workaround did you build?"

---

## 5. Lewis Lin: Behavioral Interviewing

Lewis Lin (author of *Decode and Conquer* and *Cracking the PM Interview*) popularized the *concrete-recent-relevant* framework for behavioral interviewing in PM hiring. The framework transfers cleanly to customer interviews:

### 5.1 Concrete

A concrete story has named people, named tools, dates, durations, and outcomes. A vague story has none of these.

Vague: "We often run into issues with the data."
Concrete: "Last Wednesday I was pulling the QBR deck and the dashboard was showing $4.2M ARR but Salesforce showed $4.07M. I spent 90 minutes with the data eng on Slack figuring out which one was right."

**Probe for concreteness:**

- "When exactly was this?"
- "Who else was there?"
- "What tool were you in?"
- "How long did it take?"
- "What happened in the end?"

### 5.2 Recent

Stories more than 90 days old are reconstructions, not memories. They are still useful, but treat them as lower-evidence.

**Probe for recency:**

- "Has anything like this happened more recently?"
- "When was the most recent time?"

### 5.3 Relevant

A relevant story is about the job-to-be-done you are studying, not a tangentially related anecdote.

**Probe for relevance:**

- "How did that connect to [the job]?"
- "Is that representative of how this usually goes?"

If a story is missing one of the three Rs, redirect: "Has anything like that happened more recently?" or "Tell me about a time when [job] specifically."

---

## 6. Silence as a tool

The most underused interview technique is the pause. After the participant finishes a sentence:

- Count to 3 before speaking
- If the pause is still active, do not fill it
- 80% of the time the participant adds the most important detail in the gap

Why this works: most participants front-load the socially acceptable answer and bury the honest answer behind it. The first answer is rehearsed; the second is real. Silence creates the space for the second answer to emerge.

**Practical tactics:**

- Mute your microphone briefly to resist filler speech
- Take a sip of water -- it gives you something to do during the pause
- Pre-rehearse short prompts ("Mm-hmm", "What were you about to say?") so silence does not panic you

---

## 7. Handling difficult moments

### 7.1 The participant pitches you a feature

> Participant: "You guys should add a dark mode."

Redirect to the underlying problem:

> Interviewer: "Tell me about the moment that made you think of that. What were you doing? What happened?"

The dark mode request might be a symptom of "I'm using this at night and it's hurting my eyes" or "My team has a dark-mode design system and your product looks broken in our environment" -- two very different problems.

### 7.2 The participant criticizes the product harshly

Stay neutral. Do not defend. Do not apologize. Probe:

> Participant: "Your onboarding is terrible. I almost quit on day one."
> Interviewer: "That's helpful to hear. Walk me through what happened. When did you sign up? What were you trying to do first?"

Defending the product breaks rapport and stops the criticism flow.

### 7.3 The participant goes off-topic

Let it run for 60-90 seconds -- off-topic monologue often reveals adjacent problems. Then redirect:

> Interviewer: "That's a great example of [adjacent topic]. I want to make sure we have time for [original topic] too -- can we go back to [original prompt]?"

### 7.4 The participant is too quiet

Lower the cognitive load. Switch from open-ended questions to specific-recent prompts:

> Interviewer: "Let me ask something more specific. Yesterday morning -- what was the first work thing you did?"

Once they are talking about a concrete moment, you can probe outward.

---

## 8. Pair-interviewing patterns

### 8.1 Lead + note-taker

The most common pattern. Lead drives conversation; note-taker captures verbatim quotes and timestamps.

**Pre-interview agreement:**

- Hand signal for "we have enough on this thread"
- Hand signal for "I have a question to ask"
- Note-taker introduces themselves at the start but does not speak after

### 8.2 Lead + silent observer

Used when bringing stakeholders into discovery (Engineer, Designer, Exec). The observer learns the method and the customer's world without participating.

**Pre-interview brief for observer:**

- Camera on, microphone muted
- Do not speak, do not ask follow-ups
- Take your own notes -- they will inform your post-interview debrief

### 8.3 Trio: lead + note + observer

For complex B2B workflows or high-stakes discovery. Engineer or Designer joins as silent observer; PM leads; researcher note-takes.

---

## 9. Recording consent: full script

```text
"Before we start, I want to share how this will be recorded and stored:

- We'll record audio and video.
- The recording stays internal to the [Company] product team.
- I'll generate a written transcript. Identifying details (your name,
  your company, anything sensitive you mention) get redacted.
- Raw recordings are deleted after 90 days. Redacted transcripts are
  kept indefinitely for research.
- You can ask me to stop recording at any time and we can continue
  off the record.

Is that okay with you?"
```

For B2B/enterprise: include this language in the recruiting NDA or research agreement so consent is documented in writing before the interview starts.

---

## 10. Post-interview debrief checklist

Within 30 minutes of the interview, write down:

1. **Three biggest surprises** -- moments where the participant said something you did not expect
2. **Two strongest stories** -- with timestamps, so you can find them in the recording
3. **One contradiction** -- where the participant said X earlier and Y later (probe this in the next interview)
4. **Unanswered must-answer questions** -- did you actually get evidence for the top assumptions?
5. **Recruiting feedback** -- did this participant fit the segment? Adjust criteria if not.

Hand off the transcript + debrief notes to `discovery/interview-synthesis/` for theme clustering.

---

## 11. References

- Portigal, Steve. *Interviewing Users: How to Uncover Compelling Insights*. Rosenfeld Media, 2nd ed. 2023.
- Torres, Teresa. *Continuous Discovery Habits*. Product Talk, 2021.
- Fitzpatrick, Rob. *The Mom Test*. Self-published, 2013.
- Lin, Lewis C. *Decode and Conquer*. Impact Interview, 2013-2023 (multiple editions).
- Klein, Laura. *UX for Lean Startups* (interview chapters). O'Reilly, 2013.
- Beyer, Hugh & Holtzblatt, Karen. *Contextual Design* (foundational ethnographic technique). Morgan Kaufmann, 1998.
