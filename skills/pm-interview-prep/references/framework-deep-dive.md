# Framework Deep Dive: CIRCLES, AARM, STAR, Estimation

Worked examples for the four most-used PM interview frameworks.

---

## CIRCLES Worked Example

**Question:** "Design a feature for Spotify that drives daily engagement."

### C -- Comprehend

> "Quick clarification: when you say drive daily engagement, are we optimizing for daily active users, sessions per user, or time spent? And is this a feature for the existing app, or am I free to imagine cross-product? Finally -- are we constrained to free, premium, or both tiers?"

Interviewer says: DAU is the goal, existing mobile app, both tiers.

### I -- Identify the customer

> "I want to focus on the segment most likely to give us DAU lift -- specifically, the working professional who already listens to Spotify 3-4 times a week during commute or focused work, but does not open the app on weekends. They have the highest absolute headroom because they are already habituated, just not daily."

### R -- Report customer needs

> "For this segment I see three needs:
> 1. Discover music for moods that are currently underserved -- e.g., post-work decompression, Sunday cooking, late-night reading.
> 2. Lower the friction of starting a session -- right now they have to pick a playlist, which is a decision tax.
> 3. Social context -- knowing what their network is listening to without performing publicly themselves."

### C -- Cut through prioritization

> "I want to prioritize need 2, lower the friction. It is the most direct lever on DAU because it removes the choice cost that is currently the barrier between intention and open-the-app. Discovery is a session-quality problem; social is a longer build. Friction is the highest-leverage single move."

### L -- List solutions

> "Three solutions, ordered roughly from least to most ambitious:
>
> a. **Smart Daily Start** -- a single tap on app open that resumes the most likely session given time of day, day of week, last-listened context. Like 'Resume listening' but predicted.
>
> b. **Always-on lock-screen card** -- a persistent lock-screen widget with a 'play your usual' button. Removes the open-app step entirely.
>
> c. **Daily Mix as a habit** -- repackage Daily Mix as a notification at the user's predicted listening time, asking 'Ready for your morning mix?' with one-tap play. Frames the daily habit as the product."

### E -- Evaluate trade-offs

> "Smart Daily Start is lowest effort, highest predicted lift for the existing user. Lock-screen has the strongest DAU effect but the highest engineering and OS-permission cost. Daily Mix notification could cannibalize organic open if poorly tuned -- notification fatigue risk. I would build Smart Daily Start first as it has the cleanest A/B test, then learn into the others."

### S -- Summarize

> "My recommendation is Smart Daily Start -- a predicted one-tap session resume that lowers the choice-cost between user intent and listening. It targets the working-professional segment with daily-habit headroom, addresses the highest-leverage need, and is the cleanest first test. Success metric: DAU among that segment, with guardrails on session length and notification-driven open rate."

**Why this works:** Specific segment, prioritization with stated criterion, distinct solutions with one creative-but-credible idea, clear trade-off discussion, crisp summary with success metric.

---

## AARM Worked Example

**Question:** "Instagram Stories views are down 5% month over month. What do you do?"

### A -- Align on the goal

> "Before I diagnose: when you say 'down 5%', do you mean total Stories views or views per user? And is this global or a specific market? Finally, what's the time horizon -- is this a trend or a single month?"

Interviewer says: views per user, global, sustained 3-month decline.

> "Got it. So we're looking at a per-user engagement decline that is structural, not a blip. The implicit goal is to restore per-user Stories views to baseline. I'll assume the underlying business goal is total time spent on Instagram, of which Stories is a major component."

### A -- Analyze the current state

> "I want to map this across three dimensions before guessing causes:
>
> 1. **Funnel decomposition** -- Stories views = (users who open Stories tray) x (stories viewed per session) x (sessions per user). Which factor is moving? My guess based on the symptom is that 'opens the tray' is declining, since views-per-session is usually stable.
>
> 2. **Segment cuts** -- Is this concentrated in new users, returning users, or veterans? Is it concentrated in certain countries (e.g., markets where Reels is more dominant)? Concentrated in iOS vs Android?
>
> 3. **Competitive substitution** -- TikTok and Snapchat Stories are obvious substitutes. Has Reels (Instagram's own product) cannibalized Stories?"

### R -- Recommend interventions

> "Assuming the diagnosis points to tray-open decline driven by Reels cannibalization, three interventions:
>
> a. **Tray placement experiment** -- Test moving the Stories tray more prominently above the feed for users showing Reels-heavy usage.
>
> b. **Content discovery** -- Surface friend-of-friend Stories in the tray for users whose own friend graph has lower posting rates.
>
> c. **Creator incentive** -- If the root cause is supply-side (friends posting less), an in-app prompt to creators showing 'X friends would love to see your Story' could lift supply."

### M -- Measure success

> "Primary metric: Stories views per user, recovered toward baseline. Guardrails: Reels views per user (do not cannibalize), Daily Active Users (do not push people away with prompts), creator posting volume (intervention C). I'd A/B test each intervention with 1-2 week holdouts on a randomized 5% slice, measuring 7-day retention as a secondary guardrail."

**Why this works:** Clarifies before diagnosing, decomposes the metric mathematically, considers segment and substitution effects, proposes interventions tied to root cause (not vibe), and names guardrails.

---

## STAR Worked Example

**Question:** "Tell me about a time you disagreed with your manager."

### S -- Situation (30 seconds)

> "Six months into my role at [company], we were planning the Q3 roadmap. My manager wanted to commit to launching a paid tier by end of Q3."

### T -- Task (30 seconds)

> "I was the PM for the product area, and I disagreed -- I felt the data showed we had not yet validated willingness to pay at the price point engineering was building toward."

### A -- Action (2-3 minutes)

> "I asked my manager for 30 minutes to walk through my concern. I had pulled three pieces of evidence: (1) our paid-tier survey had a 12% intent rate, but our usual conversion of stated intent to actual purchase was about 1/4 of that, projecting 3% conversion -- below the threshold the business case needed; (2) we had not yet run a pricing test, so the price point was sourced from a competitor analysis, not customer data; (3) the engineering cost of the paid tier was 8 person-weeks, which traded against a retention experiment we knew had higher confidence.
>
> I did not just push back -- I proposed a counter-plan: spend 2 weeks running a Wizard-of-Oz pricing test on the existing free tier, then make the Q3 call based on the test result. If the price held, we commit to launch in Q4 with stronger evidence. If it did not, we save the 8 person-weeks and redirect to the retention experiment.
>
> My manager initially pushed back -- they had committed the launch to the leadership team. I asked if we could go to leadership together and frame it as 'we found evidence that suggests we should pre-validate -- here is the 2-week plan.' My manager agreed. We presented together, and leadership approved the pre-validation step."

### R -- Result (1 minute)

> "The pricing test ran for 12 days. We found the willingness to pay was 40% below our planned price point. We restructured the tier and launched in Q4 instead of Q3. The launch converted at 5.2% -- above the 3% business case threshold. If we had launched in Q3 at the original price, our model would have predicted a 1.8% conversion, which would have triggered a re-do."

### Reflection (Senior+, 30 seconds)

> "What I learned: pushing back on a manager works best when you bring a counter-plan, not just a counter-argument. The 'here is an alternative path' framing made the disagreement productive rather than confrontational. I have used this pattern several times since."

**Why this works:** Quantified evidence, "I" not "we" on the disagreement, counter-plan not just objection, measurable result, and a reflection that shows transferable learning.

---

## Estimation Worked Example

**Question:** "How many cups of coffee are sold in San Francisco per day?"

### Step 1: Clarify scope

> "Quick clarifications: SF city only (not the broader Bay Area)? And we are counting all cups -- cafe, home brewing, vending machine, office -- or just cafe purchases?"

Interviewer says: SF city, cafe purchases only.

### Step 2: Pick an approach

> "I'll go bottom-up: estimate the number of cafes in SF, average cups sold per cafe per day. That seems more tractable than top-down from population x cafe-coffee-drinkers, because I'm less confident in the 'how often do you go to a cafe' rate than in the per-cafe throughput."

### Step 3: Decompose

> "Cups per day = (number of cafes) x (average cups per cafe per day)."

### Step 4: Estimate each factor

> "Number of cafes -- SF population is ~850K, plus daily commuters of maybe 200K, so call it 1M people in the city on a weekday. I'd guess one cafe per 1,000 people in a coffee-heavy city = 1,000 cafes. Sanity check: Google says SF has about 1,500 cafes, so I'm within an order of magnitude.
>
> Cups per cafe per day -- A small independent cafe with one barista probably serves 200 cups in 8 hours of mid-busy operation. A Starbucks might serve 600+. Let me weight: maybe 70% small (200), 30% chain (600). Weighted average: 0.7 x 200 + 0.3 x 600 = 320. Call it 300 for round numbers."

### Step 5: Sanity check

> "Total: 1,500 x 300 = 450K cups per day in SF cafes. Let me sanity check: that's 450K cups divided by 1M people = 0.45 cups per person per day, which means roughly half the city visits a cafe daily. That feels slightly high. The downtown population skews coffee-buyer, but tourists, kids, and people who only buy occasionally pull the average down.
>
> I'd revise my estimate down to ~300K-400K cups per day."

**Why this works:** Explicit scope, stated approach choice with reasoning, decomposed into 2 factors only (simple is good), order-of-magnitude sanity check on each input, final sanity check against a derived benchmark, and explicit revision of the answer based on the sanity check.

---

## Common cross-framework principles

1. **Always restate the question** before answering. It gives you thinking time and shows the interviewer you understood.
2. **State your reasoning out loud.** The interviewer is grading your thought process, not your final answer.
3. **Make trade-offs explicit.** Every recommendation has a cost. Naming the cost signals seniority.
4. **Quantify when possible.** Numbers beat adjectives. "30% lift" beats "significant lift".
5. **Summarize at the end.** Restate your recommendation and the why. Interviewers grade memory; the closing line is what they write down.
