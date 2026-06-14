# Estimation — How to Think About Time on a Project

## Contents
- [Why estimates fail](#why-estimates-fail)
- [Goldratt's Critical Chain Method](#goldratts-critical-chain-method)
- [Practical Estimation Techniques](#practical-estimation-techniques)
- [When to Estimate vs. When to Measure](#when-to-estimate-vs-when-to-measure)
- [Learning to Estimate at 50% Confidence](#learning-to-estimate-at-50-confidence)
- [Startup Quick Protocols](#startup-quick-protocols)

## Why estimates fail

Four forces compound against you:

1. **Student Syndrome** — Given generous time, people start late. A
   10-day estimate for 5-day work means starting on day 6 with zero buffer.
2. **Parkinson's Law** — Work expands to fill time available. Safety
   padding gets consumed by the task itself.
3. **Early/late asymmetry** — Early finishes evaporate (next task starts
   on schedule). Late finishes propagate. Over a chain, projects can only
   get later.
4. **Planning fallacy** — People systematically plan for the best case
   and treat it as expected case.

**Combined effect:** Individual task estimates with embedded safety produce
projects that are BOTH padded AND late. The safety exists on paper but
not in practice.

---

## Goldratt's Critical Chain Method

CCPM applies constraint thinking to project scheduling. The core insight: **stop protecting individual tasks
and start protecting the project.**

### The method in six steps

**Step 1: Get aggressive (focused) estimates.**

Ask for 50% confidence estimates — "how long if things go reasonably well,
with no major surprises?" This is NOT the best case. It's the median: half
the time you'd finish faster, half the time slower. Most people naturally
estimate at 80-90% confidence (the safe estimate). The gap between 50% and
80-90% is pure safety padding.

Practical tip: Ask "how long if you could just focus on this with no
interruptions?" That's close to the 50% estimate. Then ask "how long with
normal interruptions and surprises?" That's the 80% estimate. Use the
first number as the task duration.

**Step 2: Identify the critical chain.**

The critical chain is the longest sequence of dependent tasks, considering
both task dependencies AND resource dependencies. If the same person does
Task A and Task C, they can't happen in parallel even if they're not
logically dependent. The critical chain accounts for this.

In a small team, the critical chain is usually obvious: it's the sequence
of work flowing through the constraint (the bottleneck person or function).

**Step 3: Schedule tasks as late as possible.**

Unlike traditional scheduling (start everything as early as possible),
CCPM schedules tasks to start as late as possible. This reduces WIP,
prevents premature work, and concentrates effort.

**Step 4: Strip safety from tasks, pool it into a project buffer.**

This is the key innovation. Instead of each task carrying its own padding,
you aggregate safety into a buffer at the end of the project.

**The default rule: Buffer = critical chain × 0.4.**

A 20-day chain gets an 8-day buffer. Commit date = day 28. This works for
the vast majority of projects. Use it unless you have a specific reason not
to.

**Why pooling works:** If you have 10 tasks, each with 2 days of safety,
that's 20 days of safety scattered across the project. But you don't need
20 days — statistical aggregation means the overruns on some tasks cancel
with the underruns on others. A pooled buffer of 8 days protects the
project better than 20 days scattered across tasks, because the pooled
buffer actually gets used as a buffer instead of being consumed by Student
Syndrome and Parkinson's Law.

**Why 0.4?** Goldratt's original recommendation was 50% (0.5), which tends
to oversize buffers slightly. RSEM (see below) often produces 30-40% for
typical task distributions. 0.4 sits in the sweet spot: aggressive enough
to maintain urgency, safe enough to absorb real variance.

**Adjusting the multiplier by uncertainty:**

| Work type | Multiplier | When to use |
|---|---|---|
| Well-understood, repeatable | **0.3** | You've done this before — another integration, another landing page, another onboarding sequence. Low variance. |
| Normal startup work | **0.4** | The default. Most work lives here. |
| Novel or high-uncertainty | **0.5** | New technology, first time doing it, external dependencies you don't control, regulatory unknowns. |

The multiplier reflects how much you don't know. A team that's built 10
integrations has tight variance — 0.3 works. A team building their first
ML pipeline has wide variance — 0.5 is appropriate. When in doubt, use 0.4.

**Other buffer types (for larger projects):**

- **Feeding buffers:** Placed where non-critical paths feed INTO the
  critical chain. Sized at 40% of the feeding chain duration. These
  protect critical chain tasks from delays in non-critical work.

- **Resource buffers:** Not time — these are alerts. A heads-up to the
  next person on the critical chain: "Your task is coming up. Be ready."
  In a small team, this is as simple as a Slack message.

**Step 5: Run the project like a relay race.**

This is the behavioral shift. In a relay race, the runner doesn't wait for
their scheduled time slot — they start the moment the baton arrives.
Similarly, when a predecessor task finishes (early or on time), the next
person starts IMMEDIATELY, not on the scheduled date.

This is how early finishes propagate. In traditional scheduling they don't.
In CCPM, they do — because there are no fixed task start dates, only the
buffer end date (the commitment).

Tell the team: "I don't care when individual tasks finish. I care about
buffer consumption. Start when the predecessor hands off. Work with focus.
Hand off immediately when done."

**Step 6: Monitor buffer consumption, not task deadlines.**

Track exactly two numbers: % of critical chain completed, and % of project
buffer consumed. Plot them on a fever chart.

### Buffer sizing

**The default: critical chain × 0.4.** Use this for 90% of projects.
See Step 4 above for why it works.

**Alternative methods for edge cases:**

**RSEM (Root Square Error Method)** — when you need statistical precision,
e.g. regulated work or high-stakes external commitments where you need to
justify the buffer. RSEM requires both estimates per task: the focused
estimate (50%) and the safe estimate ("how long with normal life?", 80-90%).
For each task: safety = (safe - focused). Square each. Sum the squares.
Take the square root.

`Buffer = sqrt(sum((safe_i - focused_i)^2))`

RSEM accounts for the fact that independent task variances don't add
linearly — they add as square roots (central limit theorem). It typically
produces buffers in the 30-40% range for normal distributions, which is
why 0.4 works as a shortcut.

**Capacity shortcut** — when you don't have a project with a defined chain
of tasks (ongoing support, ops, mixed ad-hoc work). Plan only 80% of
available hours. In a 40-hour week, commit to 32 hours. The other 8 are
your buffer for interrupts, emergencies, and surprises. Track what consumes
the buffer weekly — patterns reveal systemic problems worth fixing.

---

## Practical Estimation Techniques

### PERT estimation

Program Evaluation and Review Technique (1950s). For each task, get three
estimates:
- O = Optimistic (everything goes perfectly)
- M = Most likely (normal conditions)
- P = Pessimistic (serious problems, but not catastrophic)

Expected duration = (O + 4M + P) / 6

The weighting toward M makes this more realistic than a simple average.
For CCPM, use M as your aggressive estimate and P as your safe estimate.
The difference feeds the buffer.

**Example:**
- Optimistic: 2 days
- Most likely: 4 days
- Pessimistic: 10 days
- PERT estimate: (2 + 16 + 10) / 6 = 4.7 days
- For CCPM: task duration = 4 days, safety = 6 days (contributes to buffer)

### Relative estimation (T-shirt sizes)

Instead of estimating in hours/days (absolute), estimate in relative
complexity. "Is this task bigger or smaller than that task?" Humans are
much better at relative comparison than absolute prediction.

**T-shirt sizing (fastest):**
S = a few hours, M = 1-2 days, L = 3-5 days, XL = more than a week.

Rule: If it's XL, break it down. Nothing should be XL. XL means you
don't understand the task well enough to estimate it, which means you
don't understand it well enough to build it.

### Cycle time measurement

Instead of estimating forward, measure backward. Track how long tasks
actually take from start to done. After 15-20 completed tasks, you have
a distribution. Use the distribution to predict future work.

- Median cycle time: 50% of tasks complete in this time or less.
- 85th percentile: 85% of tasks complete in this time or less.
  (This is your "safe" promise for external commitments.)

**This is the most accurate method for ongoing work.** It replaces
estimation with measurement. To start: track completion dates in your
tool. After 3-4 weeks of data, you have enough to use cycle time for
predictions.

### Monte Carlo forecasting

If you know your historical throughput (tasks completed per week) and the
number of remaining tasks, you can simulate thousands of possible futures.

Simple version:
1. Count remaining tasks (say 12).
2. Measure weekly throughput over the last 6 weeks (say: 3, 2, 4, 3, 2, 3).
3. Randomly sample from that throughput distribution, week by week, until
   all 12 tasks are done.
4. Repeat 1,000 times.
5. The distribution of completion dates gives you confidence levels:
   "50% chance of finishing by March 28, 85% chance by April 8."

Monte Carlo is overkill until you have 6+ weeks of throughput data. Start
with cycle time measurement first.

### The cone of uncertainty

Barry Boehm (1981), later formalized by Steve McConnell. At the start of
a project, estimates can be off by 4x in either direction. As the project
progresses and uncertainty resolves, the cone narrows:

| Project phase | Estimate range |
|---|---|
| Initial concept | 0.25x to 4x |
| Requirements defined | 0.5x to 2x |
| Detailed design | 0.67x to 1.5x |
| Code complete | 0.8x to 1.25x |

**Implication:** An estimate given before you've started building is almost
worthless as a point estimate. Always communicate ranges, not dates.
"2 to 8 weeks" is honest. "4 weeks" is a fiction.

---

## When to Estimate vs. When to Measure

### Estimate when:
- You need to decide whether a project is worth starting at all
  (Is this a 1-week or 6-month effort? That changes the priority decision.)
- You need to coordinate with external parties (customer launches, events,
  partner timelines)
- The work is genuinely novel — you've never done anything like it before,
  so you have no historical data

### Measure (don't estimate) when:
- You're doing ongoing product development (features, bugs, improvements)
- You have 3+ weeks of throughput data
- The work is similar in nature to previous work (another API integration,
  another onboarding improvement, another landing page)
- The cost of estimating exceeds the value of the estimate

### Time-box (don't estimate or measure) when:
- The work is experimental (will this approach even work?)
- You're exploring, not building (customer interviews, market research)
- The risk is in feasibility, not timeline

For experiments: use 2-week time-boxed cycles (GOLEAN sprints). Don't
estimate how long the experiment takes — time-box it. Either you learn
something in 2 weeks or the experiment wasn't focused enough.

---

## Learning to Estimate at 50% Confidence

The entire CCPM system depends on one skill: giving honest 50% confidence
estimates — the median duration where you'd finish faster half the time and
slower half the time. Most people can't do this naturally. They give 80-90%
estimates (padded, safe) and call them "aggressive." The good news: this is
a learnable skill. 80-90% of people achieve good calibration within a few
hours of practice.

### Why people are bad at this by default

When someone says "I think this will take 5 days," that number is almost
always their 80-90% confidence estimate — padded enough that they'd feel
comfortable committing to it publicly. Their actual 50% estimate might be
3 days, but they don't say that because it feels risky.

The problem isn't dishonesty. It's that people don't distinguish between
"how long will this take?" (which they hear as "what can you commit to?")
and "what's the median duration?" (which is what CCPM needs). The exercises
below train you to hear and answer the second question.

### Exercise 1: The two-question split (use every time you estimate)

For each task, always ask two questions:

1. **"How long if you could just focus — no interruptions, no surprises?"**
   This is close to the 50% estimate.
2. **"How long with normal life — interruptions, surprises, things being
   harder than expected?"** This is close to the 80-90% estimate.

The gap between the two numbers is the safety that CCPM strips from the
task and pools into the buffer. By always asking both, you train yourself
to see that "my estimate" is not one number — it's a range. The first
number goes into the schedule. The gap feeds the buffer.

### Exercise 2: Weekly estimation retrospective (the feedback loop)

This is the most important exercise. Without feedback, you don't improve.

Each week, review all tasks completed:

| Task | 50% estimate | Actual | Early or late? |
|---|---|---|---|
| Design onboarding flow | 3 days | 4 days | Late |
| Build signup page | 2 days | 1.5 days | Early |
| Write API docs | 1 day | 1 day | On time |

Keep a running tally: **what percentage of tasks finish at or before the
50% estimate?**

- **40-60% finish early:** You're well-calibrated. The buffer is working.
- **70%+ finish early:** Your "50% estimates" are actually 80% estimates.
  You're still hiding safety in the tasks. Push estimates down.
- **Under 30% finish early:** You're being unrealistically aggressive. Your
  buffer will be consumed every time. Push estimates up slightly.

Run this for 4-6 weeks and your calibration will tighten significantly.
The pattern of misses also reveals where your blind spots are — maybe
you consistently underestimate integration work but nail UI work.

### The key insight

Calibration is not about being right on any individual estimate. It's about
your estimates being right *in aggregate* — half early, half late, with the
buffer absorbing the variance. A team where every task finishes "on time"
is not well-calibrated. They're padding. A team where roughly half finish
early and half finish late, with the project buffer absorbing the net
variance, is perfectly calibrated.

---

## Startup Quick Protocols

The operational estimation protocol (quick protocol, two-question filter,
fever chart, and timeline communication templates) is in the stage files:

- **`stages/growth.md`** — The quick estimation protocol, two-question
  filter, fever chart summary, and when-to-estimate table for teams under 10.
- **`stages/scaling.md`** — Full CCPM method, buffer sizing, cycle time
  measurement, and communicating timelines to customers, board, and team.

This reference file covers the underlying theory and detailed methods.
