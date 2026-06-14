# State Persistence — Write Protocol, Bootstrap, Examples, Edge Cases

Load this file when about to write to `.factory/` after a ritual completion, or when bootstrapping `.factory/` for the first time. The **read** protocol and state file schema live in `SKILL.md` and do not require this file.

## 1. Write protocol

Claude writes to state ONLY when one of these triggers fires during the conversation. Each trigger has a specific detection rule and write action.

### Trigger table

| # | Trigger | Detection rule | Write action |
|---|---|---|---|
| 1 | Weekly review complete | Founder ran the weekly review protocol to its end — all stage-specific questions answered AND the "one thing we will NOT do next week" question answered | Append `## YYYY-MM-DD — Weekly review (<stage>)` entry to `.factory/journal.md` with the sub-sections for the founder's current stage |
| 2 | Experiment committed | Founder explicitly accepts an assigned experiment with affirmative language: "ok I'll do that", "yes, let's run it", "sure, this week", "I'll try that", or similar | Append `## YYYY-MM-DD — Experiment committed` entry to `.factory/journal.md` AND update `## Current experiment` section in `.factory/context.md` |
| 3 | Diagnosis accepted | Claude named the constraint (in customer-factory vocabulary) AND the founder affirmed explicitly ("yes that's it", "agreed", "makes sense") OR the founder immediately accepted a proposed experiment attacking that constraint (in which case both Diagnosis and Experiment committed writes fire) | Append `## YYYY-MM-DD — Diagnosis` entry to `.factory/journal.md` AND update `## Current constraint` in `.factory/context.md`. Entry MUST include both the founder's initial framing and the actual diagnosis. When both Diagnosis and Experiment committed fire from the same exchange, write the Diagnosis entry first, then the Experiment committed entry — both dated today. |
| 4 | Experiment outcome reported | Founder reports back at or after the experiment's deadline on a prior experiment's results. If the founder's report is ambiguous about which experiment, ask before writing; default assumption is the most recent `## Current experiment` from `context.md`. | Append `## YYYY-MM-DD — Experiment outcome` entry to `.factory/journal.md` |
| 5 | Experiment killed early | Founder says they stopped an experiment before its deadline | Append `## YYYY-MM-DD — Kill decision` entry to `.factory/journal.md` AND clear `## Current experiment` in `.factory/context.md` (set to empty or "none active") |
| 6 | Stage transition confirmed | Customer/MRR/team numbers changed enough to shift stage (per thresholds in `SKILL.md` decision tree) AND founder confirms the stage change | Update `## Stage` in `.factory/context.md` AND append `## YYYY-MM-DD — Stage change` entry to `.factory/journal.md` |
| 7 | Numbers change mentioned | Founder presents a number as a status update (not a passing aside) — e.g., any integer change to customer count, or a >10% change in MRR/ARR, team size changes, runway changes. | Update `## Numbers` in `.factory/context.md`. **No journal entry** — Numbers churn freely and don't need historical logging. |

### Sub-section templates

**Weekly review (pre-revenue):**

```markdown
## YYYY-MM-DD — Weekly review (pre-revenue)
**Conversations:** <count + who>
**What we learned:** <one or two key learnings>
**Hypothesis check:** <still believed? evidence for/against?>
**Next week's one thing:** <single most important thing to learn or test>
**One thing we will NOT do:** <what's tempting but off-limits>
```

**Weekly review (growth):**

```markdown
## YYYY-MM-DD — Weekly review (growth)
**Constraint:** <factory step + movement this week>
**Numbers:** <found / activated / paid / churned>
**Work pile:** <what's in progress, what shipped, what's stuck >2 weeks>
**Next week's 3 priorities:** <three bullets, each serving the constraint>
**One thing we will NOT do:** <what's tempting but off-limits>
```

**Weekly review (scaling):**

```markdown
## YYYY-MM-DD — Weekly review (scaling)
**Funnel snapshot:** <step with biggest drop-off, vs last week>
**Buffer/flow:** <where work is piling up, where capacity is idle>
**Initiative traffic lights:** <🟢/🟡/🔴 per initiative>
**Policy constraint scan:** <rule/process/habit slowing things down, if any>
**Next week's focus:** <one thing the team is rallying around>
**One thing we will NOT do:** <what's tempting but off-limits>
```

**Diagnosis:**

```markdown
## YYYY-MM-DD — Diagnosis
**Founder's initial framing:** <what the founder thought the problem was — verbatim quote where possible>
**Symptom probed:** <what Claude asked to surface the real constraint>
**Diagnosis:** <customer-factory step + magnitude — e.g. "Activation — 7-day rate at 18%">
**Why not the others:** <brief rule-out of the other factory steps>
**Confidence:** <High / Medium / Low>
```

**Experiment committed:**

```markdown
## YYYY-MM-DD — Experiment committed
**Experiment:** <what's being run>
**Constraint it attacks:** <which factory step>
**Metric:** <what number to watch — with current baseline>
**Deadline:** <YYYY-MM-DD>
```

**Experiment outcome:**

```markdown
## YYYY-MM-DD — Experiment outcome
**Experiment:** <reference to what was run>
**Did the metric move?** <yes / no / partially, with numbers>
**What we learned:** <one or two key learnings>
**Next:** <keep going, kill it, try something new — decided here or deferred>
```

**Kill decision:**

```markdown
## YYYY-MM-DD — Kill decision
**What was killed:** <experiment or initiative>
**Why:** <signal that triggered the kill>
**What we learned:** <even killed experiments teach something>
**What we'll try instead:** <next experiment, or "nothing — refocus on X">
```

**Stage change:**

```markdown
## YYYY-MM-DD — Stage change
**From:** <old stage>
**To:** <new stage>
**Trigger:** <what changed — first paying customer, crossed $100K MRR, lost all customers, etc.>
**What changes about how we work:** <brief — the new stage file has the full guidance>
```

### Founder override rule

If the founder says any of these phrases, skip writes for that session and do not bring it up again unless the founder re-authorizes:

- "don't log this"
- "don't write to my factory"
- "keep this off the record"
- "don't save this"
- or any clearly equivalent opt-out

Acknowledge with exactly: **"OK, not logging this one."**

After an override, Claude continues coaching normally for the rest of the session but writes nothing — neither journal entries nor context.md updates — until the founder explicitly re-authorizes ("actually, log it" / "on second thought, go ahead and write it").

### Announcement after writing

After writing, Claude says **"Logged."** (one word, not a wall of text) so the founder knows state was updated. Do not list what was written — the file is right there if the founder wants to see it.

### Write failure handling

If a file write fails (disk full, permission denied, directory not writable, etc.), tell the founder exactly what would have been written (in a markdown code block) and continue coaching. Do not retry silently. Do not claim a write succeeded when it didn't.

## 2. Bootstrap protocol

Runs when `.factory/` does not exist in CWD AND the current intake conversation has surfaced enough information to populate `context.md`.

"Enough information" means the founder has answered at least: stage (via the paying-customers question), customer count, team size, AND the primary problem they're bringing. Don't offer bootstrap before this bar is reached.

### Offer text

Offer once per session, after intake has reached the funnel break scan OR the minimum-fields bar above:

> "Want me to set up `.factory/` for this company? I'll create a `context.md` from what we just discussed and start a `journal.md`. It lives in this directory. The journal stays local (gitignored)."

### If founder declines

Don't offer again this session. Don't nag. The founder can ask later if they change their mind.

### If founder consents

Execute these steps in order:

**Step 1 — Ask the bootstrap-only Identity question:**

> "Before I scaffold, in one sentence — what does this company do and who for?"

This populates `## Identity`. Intake starts with "do you have paying customers" and never captures identity explicitly, so this gap is filled at bootstrap time only.

**Step 2 — Create `.factory/` directory in CWD.**

**Step 3 — Write `.factory/context.md`** with content derived from intake answers:

```markdown
# <Company name if known, otherwise leave title empty>

## Identity
<Answer to the bootstrap-only question>

## Numbers
<From intake: customer count, MRR/ARR if mentioned, team size, runway if mentioned>

## Stage
<Stage decided from intake routing> — <one-line justification from intake>

## JTBD
<If JTBD came up in intake, write it here. Otherwise: "TBD — capture in a future session">

## Current constraint
<If the funnel break scan ran and found a constraint, write it using customer-factory vocabulary. Otherwise: "TBD — run the funnel break scan next session">

## Current experiment


## Notes

```

**Step 4 — Write `.factory/journal.md`** with only the title line:

```markdown
# Journal
```

**Step 5 — Append `.factory/journal.md` to project `.gitignore`:**

- If `.gitignore` exists in CWD: check if `.factory/journal.md` is already listed. If not, append it on a new line at the end of the file.
- If `.gitignore` does not exist: create it with just the line `.factory/journal.md`.
- Never modify, reorder, or delete existing lines in `.gitignore`.
- If CWD is not a git repository (no `.git/` directory), skip this step silently but warn the founder in Step 6.

**Step 6 — Confirm to founder:**

If `.gitignore` was updated successfully:
> "Done. `.factory/context.md` is committable (team can share the truth); `.factory/journal.md` is gitignored (personal coaching log). Edit them by hand any time."

If CWD is not a git repo:
> "Done. `.factory/context.md` and `.factory/journal.md` are in place. Heads-up: this directory isn't a git repository, so I couldn't gitignore the journal. If you initialize git later, add `.factory/journal.md` to `.gitignore` to keep the personal log out of the repo."

## 3. Examples

### Example `.factory/context.md`

```markdown
# Swiftner

## Identity
Sales-call analytics for inside sales teams at B2B SaaS companies of 10-50 reps.

## Numbers
14 paying customers · $4.2K MRR · team of 2 · runway 9 months

## Stage
growth — first paying customers, product-market fit signals, focus is on repeatable sales

## JTBD
When sales reps join a new company, they want to ramp up faster, so they can hit quota in Q1 instead of Q2.

## Current constraint
Activation — 7-day rate at 18%. Diagnosed 2026-03-24.

## Current experiment
Rewrite onboarding email sequence to pull users to first "aha" in <10 min. Metric: 7-day activation rate. Deadline: 2026-04-14.

## Notes
- ICP: inside-sales leaders at Norwegian B2B SaaS, 10-50 reps
- Do NOT chase enterprise — burned on that in 2025
- Brand codes: orange, conversational tone, "sales reality" not "sales theater"
```

### Example `.factory/journal.md`

```markdown
# Journal

## 2026-03-24 — Diagnosis
**Founder's initial framing:** "We need more features."
**Symptom probed:** Do customers who activate stay? → 92% retention at 90 days.
**Diagnosis:** Activation — 7-day activation rate at 18%. Not a product problem.
**Why not the others:** Acquisition is fine (signups growing 12% mo/mo). Retention is fine (92%). Revenue converts when activated users see value.
**Confidence:** High.

## 2026-04-04 — Experiment committed
**Experiment:** Rewrite onboarding email sequence to pull users to first "aha" in <10 min.
**Constraint it attacks:** Activation.
**Metric:** 7-day activation rate (currently 18%).
**Deadline:** 2026-04-14.

## 2026-04-07 — Weekly review (growth)
**Constraint:** Activation (still). 7-day rate moved 18% → 21% — meaningful but small.
**Numbers:** Found 142, activated 30, paid 4, churned 0.
**Work pile:** Email sequence rewrite shipped Tuesday. Nothing else in progress.
**Next week's 3 priorities:** (1) Ship signup form simplification, (2) Interview 3 users who activated last week, (3) Nothing else.
**One thing we will NOT do:** Write any new blog content. Acquisition is not the constraint.
```

## 4. Edge cases

Eight cases with precise behaviors. When in doubt, trust the founder and never auto-rewrite state.

### 4.1 `.factory/` partial

If only `context.md` exists (no `journal.md`): read context normally, skip the journal-tail read. The first write that needs `journal.md` creates it with just `# Journal`.

If only `journal.md` exists (no `context.md`): rare and weird. Read the journal tail. Offer to reconstruct `context.md` from the most recent state implied by the journal: *"I see a journal but no context file. Want me to recreate `context.md` from the last few entries?"*

### 4.2 Required header missing in `context.md`

If a header Claude expects (e.g., `## Current constraint`) is missing entirely, ask the founder for that field. After they answer, write the answer under a freshly added `## Current constraint` section. Never refuse to proceed because of a missing header.

### 4.3 Header renamed by founder

If the founder has renamed a header (e.g., `## Current bottleneck` instead of `## Current constraint`), Claude cannot find the expected name. Ask: *"I see `## Current bottleneck` — should I treat that as `## Current constraint`?"* On confirmation, use the renamed header for reads and writes in this session. Do not auto-rewrite the file.

### 4.4 State conflicts with founder's stated reality

If `context.md` says `## Stage` is "growth" but the founder says "we just lost all our customers," trust the founder. Ask: *"Sounds like the state is stale. Want me to log a Stage change to restart and update context.md?"* Only update on consent.

### 4.5 `## Numbers` older than 30 days

If the most recent journal entry is >30 days ago (or the founder has explicitly annotated `## Numbers` with a date marker showing it's stale), re-confirm before routing: *"Your Numbers section says 14 customers, $4.2K MRR — is that still right?"* Update `context.md` if anything changed. Do NOT create a journal entry for the Numbers update — Numbers churn freely.

### 4.6 Wrong-factory mismatch

If a founder runs Factory Floor in a directory that has someone else's (or an abandoned) `.factory/`, Claude will read the saved state and open with an opening-line pattern that names the old state. If the founder says "wait, that's not what we're working on" or similar, ask: *"This `.factory/` says [identity]. Is this the wrong directory?"* Never delete or overwrite without explicit consent.

### 4.7 Bootstrap can't gitignore

If CWD is not a git repo (no `.git/` directory), bootstrap still creates `.factory/context.md` and `.factory/journal.md`, but skips the `.gitignore` step and warns the founder per §2 Step 6.

### 4.8 Claude Desktop / no-CWD environments

Claude Desktop has no filesystem access for auto-read/auto-write. The founder uploads `.factory/context.md` as project knowledge manually. Auto-write is disabled — at a ritual completion trigger, Claude tells the founder exactly what entry it *would have written* in a markdown code block, and the founder copy/pastes into their local `journal.md` themselves.

This is a second-class experience deliberately. It is documented in the project README so the founder knows what to expect on Claude Desktop.