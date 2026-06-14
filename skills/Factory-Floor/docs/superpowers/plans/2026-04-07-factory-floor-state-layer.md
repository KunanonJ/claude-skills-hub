# Factory Floor State Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add persistent state to Factory Floor via `.factory/context.md` (committed) and `.factory/journal.md` (gitignored) so founders stop re-explaining themselves every session; make named protocols discoverable via in-skill content changes (no slash commands).

**Architecture:** Purely additive changes to a markdown skill. A new `references/state.md` holds the write protocol, bootstrap protocol, examples, and edge cases (loaded lazily on ritual completion). `SKILL.md` gains a STATE LOAD branch with a parallel-read instruction, an inlined state schema (so the read path doesn't load `state.md`), a new "name the protocol" response-format rule, and a routing table row. `references/intake.md` gets a small appendix listing named protocols. The installer (`bin/install.mjs`) gains one entry. Eight scenario fixtures go into a new `evals/scenarios/state-layer/` directory to serve as acceptance criteria and future eval inputs.

**Tech Stack:** Markdown (skill content), Node.js ES modules (installer), git (version control), no test runner (markdown skill — validation is manual + scenario fixtures).

---

## Overview

Factory Floor is a Claude Code skill distributed as `@swiftner/factory-floor` on npm and via ClawHub. It is installed to `~/.claude/skills/factory-floor/` and triggers when founders ask about priorities, bottlenecks, what to build, etc. The skill is pure markdown — no executable code beyond the installer and a Mermaid render helper.

This plan adds a **persistent state layer**: when Factory Floor runs in a directory that contains `.factory/`, Claude reads the state before doing anything else and opens the conversation already knowing the stage, constraint, and current experiment. After rituals (weekly reviews, diagnoses, experiment commitments, kill decisions, stage changes) Claude writes new entries to the state, appending to a journal and updating a context file.

**Design doc:** `docs/superpowers/specs/2026-04-07-factory-floor-state-layer-design.md`

**Existing Factory Floor files you need to understand before starting:**

- `SKILL.md` — the router. Decision tree, symptom → constraint map, reference routing table, response format. Currently ~130 lines. This plan grows it by ~50 lines.
- `references/intake.md` — the first-conversation protocol. Asks for stage, team, revenue, specific problem, what's been tried, then funnel break scan. ~88 lines. This plan appends a named-protocols section.
- `references/state.md` — does not exist yet. This plan creates it.
- `references/weekly-review.md` — stage-specific weekly review templates (pre-revenue 10 min / growth 10 min / scaling 25 min). Not modified by this plan, but the `state.md` write protocol references its sub-sections.
- `references/misdiagnoses.md` — the eight most common wrong diagnoses. Not modified, but the Diagnosis ritual's "founder's initial framing" field is designed around it.
- `references/pillar-maurya.md` — defines the customer factory vocabulary (Acquisition / Activation / Revenue / Retention / Referral) that the state layer enforces for `## Current constraint`.
- `bin/install.mjs` — copies skill files to `~/.claude/skills/factory-floor/`. One entry in the files array needs updating.
- `evals/README.md` — describes an *aspirational* persona/scenario/judge/runs framework. The subdirectories don't exist yet. This plan creates `evals/scenarios/state-layer/` with fixture files for the 8 state-layer test cases.

## File Layout

**New files:**

```
references/state.md                               # NEW — write protocol, bootstrap, examples, edge cases (~300 lines)
evals/scenarios/state-layer/01-bootstrap.md       # NEW — scenario fixture
evals/scenarios/state-layer/02-read-continuity.md # NEW — scenario fixture
evals/scenarios/state-layer/03-partial-state.md   # NEW — scenario fixture
evals/scenarios/state-layer/04-auto-write-weekly-review.md  # NEW
evals/scenarios/state-layer/05-founder-override.md          # NEW
evals/scenarios/state-layer/06-stale-numbers.md             # NEW
evals/scenarios/state-layer/07-header-rename.md             # NEW
evals/scenarios/state-layer/08-constraint-vocabulary.md     # NEW
```

**Modified files:**

```
SKILL.md                  # add STATE LOAD branch + inline schema section + response format item 4 + reference routing row
references/intake.md      # append "Named protocols you can ask for by name" section
bin/install.mjs           # add 'references/state.md' to the files array
```

**Unchanged:**

```
All other references/*.md
All stages/*.md
scripts/*
agents/*
_meta.json, package.json, README.md
```

## Task Order Rationale

Scenarios first (Task 1) so every subsequent task has concrete acceptance criteria. Then `references/state.md` (Task 2) because it's the biggest new piece and other tasks reference it. Then `SKILL.md` (Task 3) — this is the most delicate file because it holds the load-bearing decision tree. Then `references/intake.md` (Task 4) — small, independent. Then `bin/install.mjs` (Task 5) — tiny, must be after `state.md` exists so the file copy doesn't fail. Finally manual validation pass (Task 6) against every scenario from Task 1.

## TDD Adaptation for Markdown Skills

Factory Floor is a markdown skill — no runnable tests, no red-green-refactor cycle at the unit level. The eval framework is aspirational (see §12 of the spec). This plan adapts the TDD spirit as follows:

1. **Scenarios as acceptance criteria** (Task 1): Each scenario file describes a persona, a setup, a prompt, expected behaviors, and pass/fail grading criteria. These serve as the "failing tests" in the sense that the current skill cannot satisfy them (the state layer doesn't exist).
2. **Read-back verification** after each file edit: After writing a new file or editing an existing one, the executing agent reads the file back and confirms specific strings/headers exist. This is the fastest approximation of "run the test" for a markdown file.
3. **Manual validation pass** (Task 6): Walk through each scenario in a test directory, confirm behavior matches expectations, document findings.

Each task ends with a commit. Commits are per-task, not per-step, to keep history readable.

---

## Task 1: Create scenario fixtures

**Files:**
- Create: `evals/scenarios/state-layer/01-bootstrap.md`
- Create: `evals/scenarios/state-layer/02-read-continuity.md`
- Create: `evals/scenarios/state-layer/03-partial-state.md`
- Create: `evals/scenarios/state-layer/04-auto-write-weekly-review.md`
- Create: `evals/scenarios/state-layer/05-founder-override.md`
- Create: `evals/scenarios/state-layer/06-stale-numbers.md`
- Create: `evals/scenarios/state-layer/07-header-rename.md`
- Create: `evals/scenarios/state-layer/08-constraint-vocabulary.md`

**Rationale:** Scenarios define acceptance criteria before any implementation work. Each file is self-contained (persona + setup + prompt + expected behaviors + grading criteria) so a future eval runner has everything it needs. For now they serve as the manual validation checklist in Task 6.

### - [ ] Step 1: Create the scenarios directory

Run: `mkdir -p "evals/scenarios/state-layer"`
Expected: Directory created, no output on success. Verify with `ls evals/scenarios/state-layer/` (empty directory).

### - [ ] Step 2: Write `evals/scenarios/state-layer/01-bootstrap.md`

Create the file with exactly this content:

```markdown
# Scenario 01: Bootstrap after first intake

**Spec reference:** §11.1 fixture #1
**Category:** State layer — bootstrap

## Persona
Solo pre-revenue SaaS founder, 3 months into building, no paying customers, feeling stuck. First-time Factory Floor user. Running Claude Code in her project directory (no `.factory/` exists, but `.git/` does).

## Setup
- CWD is a git repository
- No `.factory/` directory exists in CWD
- `.gitignore` may or may not exist
- No prior conversation context

## Prompt
> "I don't know what to do next. I've been building for three months and I'm not sure I'm on the right track."

## Expected behaviors
1. Claude recognizes the Factory Floor trigger and runs intake (no state to load, so STATE LOAD branch is skipped).
2. Intake proceeds through the standard questions: paying customers, team size, revenue, specific problem, what's been tried.
3. Funnel break scan is attempted or skipped appropriately for pre-revenue.
4. At or after the minimum-fields threshold (stage, customer count, team size, primary problem all answered), Claude offers bootstrap using substantially this phrasing: *"Want me to set up `.factory/` for this company? I'll create a `context.md` from what we just discussed and start a `journal.md`. It lives in this directory. The journal stays local (gitignored)."*
5. Founder consents.
6. Claude asks the bootstrap-only Identity question: *"Before I scaffold, in one sentence — what does this company do and who for?"*
7. Claude creates the `.factory/` directory.
8. Claude writes `.factory/context.md` with all 7 H2 headers (`## Identity`, `## Numbers`, `## Stage`, `## JTBD`, `## Current constraint`, `## Current experiment`, `## Notes`), populated from intake answers where available, with `TBD — capture in a future session` style placeholders for fields not yet known.
9. Claude writes `.factory/journal.md` with only the title line `# Journal`.
10. Claude appends `.factory/journal.md` to `.gitignore`, creating the file if it doesn't exist, without touching any pre-existing entries.
11. Claude confirms: *"Done. `.factory/context.md` is committable (team can share the truth); `.factory/journal.md` is gitignored (personal coaching log). Edit them by hand any time."*

## Grading criteria

**PASS if all of:**
- Intake ran before bootstrap was offered
- Bootstrap offer appeared only after minimum fields were gathered
- Bootstrap offer phrasing was substantially per `references/state.md` §2
- The Identity question was asked as its own separate step
- `.factory/context.md` was created with all 7 required H2 headers
- `.factory/journal.md` was created with exactly `# Journal` as its content
- `.gitignore` was updated with `.factory/journal.md` on a new line
- Final confirmation mentioned the committable/gitignored split

**FAIL if any of:**
- Claude wrote state files without offering bootstrap and getting consent
- The Identity question was not asked
- Any required header is missing from `context.md`
- `.gitignore` was not updated (assuming CWD is a git repo)
- `.gitignore` had existing entries that were clobbered or reordered
- Bootstrap was offered too early (before minimum fields gathered)
```

### - [ ] Step 3: Write `evals/scenarios/state-layer/02-read-continuity.md`

Create the file with exactly this content:

```markdown
# Scenario 02: Read continuity — state-aware opening

**Spec reference:** §11.1 fixture #2
**Category:** State layer — read protocol

## Persona
Returning founder, growth stage (14 customers, $4.2K MRR, team of 2). Has been using Factory Floor for several weeks. Diagnosed an Activation constraint last week and committed to rewriting an onboarding email sequence.

## Setup
- CWD has `.factory/context.md` with all 7 headers populated:
  - Identity: "Sales-call analytics for inside sales teams at B2B SaaS companies of 10-50 reps"
  - Numbers: "14 paying customers · $4.2K MRR · team of 2 · runway 9 months"
  - Stage: "growth — first paying customers, product-market fit signals"
  - JTBD: "When sales reps join a new company, they want to ramp up faster..."
  - Current constraint: "Activation — 7-day rate at 18%. Diagnosed 2026-03-24."
  - Current experiment: "Rewrite onboarding email sequence. Metric: 7-day activation rate. Deadline: 2026-04-14."
  - Notes: (free-form)
- CWD has `.factory/journal.md` with entries for:
  - `## 2026-03-24 — Diagnosis` (framing + diagnosis + why not others)
  - `## 2026-04-04 — Experiment committed` (rewriting email sequence)
- No Experiment outcome entry yet — the experiment is still running

## Prompt
> "What should I focus on this week?"

## Expected behaviors
1. Claude reads `.factory/context.md` (Round 1).
2. Claude issues a parallel tool-use batch (Round 2) to read `.factory/journal.md` tail AND `stages/growth.md` simultaneously.
3. Claude does NOT load `references/intake.md` (state satisfies the intake questions).
4. Claude does NOT load `references/state.md` (read path is self-sufficient).
5. Claude's opening response matches the "recent Experiment committed without matching Outcome" pattern: *"Last week you committed to rewriting the onboarding email sequence. Did the 7-day activation rate move?"* (exact wording may vary but it must name the experiment and ask about the metric).
6. Claude does NOT ask any intake questions (no "how many customers do you have?", no "what's your team size?").

## Grading criteria

**PASS if all of:**
- Claude's first turn mentions the prior experiment by name/description
- Claude's first turn asks about the metric (7-day activation rate)
- Zero intake questions asked
- Round 2 reads (journal + stage file) happened in a single parallel tool-use batch
- `references/state.md` was not loaded

**FAIL if any of:**
- Claude ran intake despite fully populated state
- Claude asked "how many customers?" or "what stage are you in?"
- Claude's opening did not reference the pending experiment
- Journal and stage file were read sequentially instead of in parallel
```

### - [ ] Step 4: Write `evals/scenarios/state-layer/03-partial-state.md`

Create the file with exactly this content:

```markdown
# Scenario 03: Partial state — ask only for missing fields

**Spec reference:** §11.1 fixture #3
**Category:** State layer — partial state handling

## Persona
Returning founder, mid-setup. Has populated most of `context.md` but never filled in the `## Current constraint` section because no diagnosis has been made yet.

## Setup
- `.factory/context.md` exists with 6 of 7 headers populated (Identity, Numbers, Stage, JTBD, Current experiment is empty, Notes)
- `## Current constraint` section is **missing entirely** from the file
- `.factory/journal.md` exists but is empty (just `# Journal`)

## Prompt
> "Should we build the Salesforce integration next?"

## Expected behaviors
1. Claude reads `.factory/context.md` (Round 1).
2. Claude parallel-reads journal tail + stage file (Round 2).
3. Claude notices `## Current constraint` is missing from context.md.
4. Claude does NOT run full intake (stage, numbers, team, etc. are all in state).
5. Claude asks the founder about the constraint specifically — e.g., "I don't see a current constraint in your state. Before I can tell you whether the integration serves your constraint, what's the funnel step where you're losing the most throughput right now?"
6. Once the founder answers, Claude proceeds with coaching using both the state and the new constraint information.

## Grading criteria

**PASS if all of:**
- Claude did not ask about stage, customer count, team size, or MRR (all in state)
- Claude asked specifically about the constraint
- Claude did not load `references/intake.md` in full (only the missing field was asked)

**FAIL if any of:**
- Claude ran the full intake protocol despite most fields being in state
- Claude silently proceeded as if the constraint were known
- Claude guessed at a constraint without asking
```

### - [ ] Step 5: Write `evals/scenarios/state-layer/04-auto-write-weekly-review.md`

Create the file with exactly this content:

```markdown
# Scenario 04: Auto-write after weekly review completion

**Spec reference:** §11.1 fixture #4
**Category:** State layer — write protocol

## Persona
Growth-stage founder (same profile as scenario 02). Running a weekly review.

## Setup
- `.factory/context.md` fully populated (growth stage)
- `.factory/journal.md` exists with one prior entry
- Founder explicitly requests the weekly review

## Prompt
> "Do my weekly review."

## Expected behaviors
1. Claude loads `references/weekly-review.md` (as it does today).
2. Claude runs the growth-stage weekly review format: constraint + movement, numbers (found / activated / paid / churned), work pile, next week's 3 priorities, **one thing we will NOT do**.
3. Claude asks each question in order, waiting for founder answers. Founder answers all five questions including the "will NOT do" question.
4. After the review completes, Claude loads `references/state.md` (first time this session) to get the write protocol.
5. Claude appends a new entry to `.factory/journal.md` with:
   - Header: `## <today's date> — Weekly review (growth)`
   - Sub-sections: `**Constraint:**`, `**Numbers:**`, `**Work pile:**`, `**Next week's 3 priorities:**`, `**One thing we will NOT do:**`
   - Each sub-section populated from the founder's answers
6. Claude says "Logged." after the write completes.

## Grading criteria

**PASS if all of:**
- All five growth-stage review questions were asked
- The "one thing we will NOT do" question was asked
- A new journal entry was appended (not overwriting existing entries)
- Entry header format is exactly `## YYYY-MM-DD — Weekly review (growth)`
- All five sub-sections are present in the entry
- Claude said "Logged." or equivalent one-word acknowledgment
- `references/state.md` was loaded (this is the first write of the session)

**FAIL if any of:**
- A review question was skipped
- The write happened before the review was complete
- Entry header uses wrong format (e.g., no date, wrong stage, wrong ritual name)
- Sub-sections are missing or misordered
- Claude wrote a long summary instead of "Logged."
```

### - [ ] Step 6: Write `evals/scenarios/state-layer/05-founder-override.md`

Create the file with exactly this content:

```markdown
# Scenario 05: Founder override — "don't log this"

**Spec reference:** §11.1 fixture #5
**Category:** State layer — override behavior

## Persona
Growth-stage founder running a weekly review, but this week contains candid reflections about a cofounder dynamic that shouldn't be logged.

## Setup
- `.factory/context.md` fully populated (growth stage)
- `.factory/journal.md` exists with prior entries
- Founder explicitly requests the weekly review

## Prompt
> "Do my weekly review. But don't log this one — I'm going to vent about the cofounder situation."

## Expected behaviors
1. Claude acknowledges the override with exactly (or substantially): *"OK, not logging this one."*
2. Claude runs the weekly review normally, asking all growth-stage questions.
3. Founder answers all questions, including candid cofounder-related reflections.
4. Claude does NOT append any entry to `.factory/journal.md`.
5. Claude does NOT update `.factory/context.md` in response to anything said during the review.
6. Claude does NOT say "Logged." at the end.
7. If the founder makes an experiment commitment during the session ("I'll talk to him on Friday"), Claude still does not write (the override suppresses all writes for the session, not just the weekly review entry).

## Grading criteria

**PASS if all of:**
- Claude acknowledged the override before running the review
- No new entries were appended to `journal.md`
- `context.md` was not modified
- Claude did not claim to have logged anything

**FAIL if any of:**
- Claude wrote any entry despite the override
- Claude updated `context.md` despite the override
- Claude said "Logged." at the end
- Claude ignored the override phrasing and wrote anyway
```

### - [ ] Step 7: Write `evals/scenarios/state-layer/06-stale-numbers.md`

Create the file with exactly this content:

```markdown
# Scenario 06: Stale Numbers re-confirmation

**Spec reference:** §11.1 fixture #6
**Category:** State layer — stale data handling

## Persona
Returning founder after a long gap. State is more than 60 days old.

## Setup
- `.factory/context.md` fully populated
- `## Numbers` section contains: `14 paying customers · $4.2K MRR · team of 2 · runway 9 months (as of 2026-02-01)` — note the explicit date
- `.factory/journal.md` has entries, but the most recent is dated more than 30 days before today's date (so today is > 2026-03-07 based on the last entry date)
- Today's date for this scenario: assume 2026-04-07

## Prompt
> "What should I focus on this week?"

## Expected behaviors
1. Claude reads `.factory/context.md` and journal tail.
2. Claude notices the Numbers section is older than 30 days (by its date marker or by the most recent journal entry being old).
3. Before proceeding with routing, Claude re-confirms with something like: *"Your Numbers section says 14 customers, $4.2K MRR — is that still right?"*
4. Founder updates numbers (or confirms they're the same).
5. If updated, Claude updates `## Numbers` in `context.md`.
6. Claude proceeds with stage-appropriate coaching using the refreshed numbers.

## Grading criteria

**PASS if all of:**
- Claude re-confirmed numbers before diving into coaching
- The confirmation question referenced specific numbers from state (not a generic "what are your numbers?")
- If founder provided updates, `context.md` was updated
- Numbers update did NOT create a journal entry (context-only change)

**FAIL if any of:**
- Claude proceeded with stale numbers without confirming
- Claude asked generically for numbers instead of pointing at the stale ones
- A journal entry was created for the Numbers update
```

### - [ ] Step 8: Write `evals/scenarios/state-layer/07-header-rename.md`

Create the file with exactly this content:

```markdown
# Scenario 07: Header renamed by founder

**Spec reference:** §11.1 fixture #7
**Category:** State layer — header rename handling

## Persona
Growth-stage founder who edited `context.md` by hand and renamed one header because they prefer different terminology.

## Setup
- `.factory/context.md` has the 7 standard headers, EXCEPT `## Current constraint` has been renamed to `## Current bottleneck` by the founder.
- The body under `## Current bottleneck` is populated normally with constraint information.
- `.factory/journal.md` exists with prior entries.

## Prompt
> "What should I focus on this week?"

## Expected behaviors
1. Claude reads `context.md`.
2. Claude notices that `## Current constraint` (the expected header) is missing.
3. Claude sees `## Current bottleneck` and asks the founder to confirm: *"I see `## Current bottleneck` — should I treat that as `## Current constraint`?"*
4. Founder confirms.
5. Claude proceeds using the renamed header for reads AND writes in this session.
6. Claude does NOT auto-rewrite the file to restore the canonical name.

## Grading criteria

**PASS if all of:**
- Claude asked the rename confirmation question
- Claude did not auto-rename the header in the file
- Once confirmed, Claude used the renamed header for the rest of the session
- Claude did not refuse to proceed because of the rename

**FAIL if any of:**
- Claude auto-rewrote `## Current bottleneck` to `## Current constraint` without asking
- Claude errored or refused to proceed
- Claude ignored the renamed header and asked for the constraint as if it were missing
```

### - [ ] Step 9: Write `evals/scenarios/state-layer/08-constraint-vocabulary.md`

Create the file with exactly this content:

```markdown
# Scenario 08: Constraint vocabulary enforcement

**Spec reference:** §11.1 fixture #8
**Category:** State layer — write protocol vocabulary

## Persona
Growth-stage founder running a diagnosis for the first time in Factory Floor. They've been vague about the problem.

## Setup
- `.factory/context.md` populated EXCEPT `## Current constraint` which is empty or contains "TBD"
- `.factory/journal.md` exists with a `# Journal` header and possibly one prior entry

## Prompt
> "We're not converting demos. I think we need to train the sales team better."

## Expected behaviors
1. Claude recognizes this as a potential misdiagnosis (the founder's framing is "sales training") and probes deeper (per `references/misdiagnoses.md`): "What do people say when they don't buy? Do you believe them?"
2. Through dialogue, Claude and the founder land on a diagnosis — let's assume the real constraint is Revenue (close rate because the ICP isn't targeted).
3. Claude names the constraint to the founder in customer-factory vocabulary: "Your constraint is **Revenue** — specifically close rate. Not sales training."
4. Founder affirms the diagnosis.
5. Claude loads `references/state.md` for the write protocol.
6. Claude appends a Diagnosis entry to `journal.md`:
   - Header: `## YYYY-MM-DD — Diagnosis`
   - Founder's initial framing: "We need to train the sales team better"
   - Symptom probed: what the dialogue surfaced
   - Diagnosis: uses the word **Revenue** explicitly — a customer-factory step — not "sales problem" or "conversion issue"
   - Why not the others: brief rule-out
   - Confidence: High/Medium/Low
7. Claude updates `context.md`'s `## Current constraint` with the same factory-step vocabulary: "Revenue — close rate, [specifics]. Diagnosed [today's date]."

## Grading criteria

**PASS if all of:**
- The journal Diagnosis entry names the constraint using a customer-factory step name (Acquisition / Activation / Revenue / Retention / Referral)
- `context.md`'s updated `## Current constraint` uses the same factory-step vocabulary
- The entry captures both the founder's initial framing AND the actual diagnosis (two distinct fields)
- The diagnosis is not written as free prose like "we have a sales problem"

**FAIL if any of:**
- The constraint is named in free prose ("sales issue", "conversion problem") instead of a factory step
- The entry omits the founder's initial framing
- The entry and context.md disagree on what the constraint is
```

### - [ ] Step 10: Verify all 8 fixture files exist

Run: `ls evals/scenarios/state-layer/`

Expected output (exact filenames, alphabetical):
```
01-bootstrap.md
02-read-continuity.md
03-partial-state.md
04-auto-write-weekly-review.md
05-founder-override.md
06-stale-numbers.md
07-header-rename.md
08-constraint-vocabulary.md
```

If any file is missing, re-run the step that creates it.

### - [ ] Step 11: Commit

```bash
git add evals/scenarios/state-layer/
git commit -m "evals: add 8 scenario fixtures for state layer

Covers bootstrap, read continuity, partial state, auto-write,
override, stale numbers, header rename, and constraint vocabulary.
These serve as acceptance criteria for the state layer implementation
and as inputs for a future eval runner (framework itself is aspirational
per evals/README.md).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Create `references/state.md`

**Files:**
- Create: `references/state.md`

**Rationale:** This file holds the write protocol, bootstrap protocol, examples, and edge cases. It is loaded **lazily** — only when a ritual write is detected or when bootstrapping a new `.factory/`. The read path is handled entirely by the inlined schema in `SKILL.md` (Task 3) so this file is not loaded on every activation.

### - [ ] Step 1: Create the file

Create `references/state.md` with exactly this content:

````markdown
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
````

### - [ ] Step 2: Verify the file exists and contains all four sections

Run: `ls -la references/state.md` — expect the file to exist with non-zero size.

Use Grep to verify the four main section headers are present:

Run: `grep -c "^## " references/state.md`
Expected: The count should be **4** (one per top-level section: Write protocol, Bootstrap protocol, Examples, Edge cases — note that H3/H4 headers are also present but `^## ` matches only H2).

If the count is not 4, the file is missing a section or has an extra. Re-read the file and compare against Step 1's content.

### - [ ] Step 3: Verify all 7 ritual sub-section templates are present

Use Grep to check each of the 7 templates exists:

Run: `grep -c "## YYYY-MM-DD — " references/state.md`
Expected: **9 or more** matches (7 ritual templates + 3 example entries in §3 = 10 matches minimum; the number could be higher if the file shows additional examples, which is fine).

### - [ ] Step 4: Commit

```bash
git add references/state.md
git commit -m "feat(state): add references/state.md with write protocol and bootstrap

New reference file holding the write protocol (7 triggers, 8 sub-section
templates), bootstrap protocol, examples, and 8 edge cases. Loaded lazily
only when a ritual write is detected or when bootstrapping — the read
path is handled by SKILL.md's inlined schema (added in the next task).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Modify `SKILL.md` — add STATE LOAD branch, inline schema, response format item, routing row

**Files:**
- Modify: `SKILL.md` (4 edits)

**Rationale:** `SKILL.md` is the router Claude loads first when the skill triggers. It gains four additions: (1) a STATE LOAD branch at the top of the decision tree that reads `.factory/` with explicit parallel instructions, (2) a new section inlining the state file schema so reads don't require `state.md`, (3) a new item in the Response format teaching Claude to name protocols explicitly, (4) a new row in the Reference Routing Table for `state.md`. All four edits keep SKILL.md lean (~180 lines after changes, up from ~130).

### - [ ] Step 1: Read current `SKILL.md` to confirm starting state

Run Read tool on `/home/mario/code/Factory Floor/SKILL.md` and verify it ends at line 130 with the "Core Rule" section:

```
## Core Rule

One constraint. Find it first. Name it. Work it. Then find the next one.
```

If the file has already been modified (e.g., contains "STATE LOAD" already), investigate before proceeding — this task assumes the unmodified SKILL.md from spec commit `d95b987`.

### - [ ] Step 2: Edit 1 — replace the Decision Tree section with the state-aware version

The current Decision Tree is between `## Decision Tree` and `---` (the horizontal rule before Symptom → Constraint Map).

Find this exact block in `SKILL.md`:

```
## Decision Tree

```
START
  │
  ├─ No context? → Load `references/intake.md`, ask first question, return here
  │
  └─ Have context? → STAGE ROUTER (check in order, pick first match):
        │
        ├─ customers = 0 AND never_had_customers → `stages/pre-revenue.md`
        ├─ customers = 0 AND had_customers_before → `stages/restart.md`
        ├─ customers > 0 AND MRR < $100K AND team < 10 → `stages/growth.md`
        └─ MRR ≥ $100K OR team ≥ 10 → `stages/scaling.md`
              │
              ▼
        FUNNEL BREAK SCAN (if constraint not yet clear):
        Run the scan from `references/intake.md` — "Walk me through your last 10..."
        │
        ├─ Numbers drop at Acquisition → constraint = awareness/reach
        ├─ Numbers drop at Activation → constraint = onboarding/time-to-value
        ├─ Numbers drop at Revenue → constraint = pricing/sales/objections
        ├─ Numbers drop at Retention → constraint = product/fit/success
        └─ Can't identify where it breaks → `references/pillar-goldratt.md`
              │
              ▼
        CONSTRAINT IDENTIFIED → Work it. But first check:
        │
        └─ Is constraint work blocked by strategic confusion?
              • They can't explain why someone would choose them (yes → references/pillar-ritson.md)
              • They're trying to serve everyone (yes → references/pillar-ritson.md)
              • "More marketing" but no position (yes → references/pillar-ritson.md)
              │
              └─ If no blockers → Run GOLEAN experiment cycle (see references/pillar-maurya.md)
```
```

Replace it with exactly this (the new STATE LOAD branch is added at the top, and the "No context?" branch is updated to read "ask ONLY for missing fields"):

```
## Decision Tree

```
START
  │
  ├─ STATE LOAD: If `.factory/` exists in CWD:
  │     Round 1 — Read `.factory/context.md`.
  │     Round 2 (PARALLEL — read these at the same time in one tool-use batch):
  │       • `.factory/journal.md` (last 8 entries — count `##` headings from bottom)
  │       • `stages/<stage>.md` (stage comes from context.md's `## Stage` header)
  │     State is now conversation context. Skip to STAGE ROUTER with loaded stage.
  │     (See "State File Schema" section below for headers and ritual types.)
  │
  ├─ No context? → Load `references/intake.md`, ask ONLY for fields not already
  │  in state, return here
  │
  └─ Have context? → STAGE ROUTER (check in order, pick first match):
        │
        ├─ customers = 0 AND never_had_customers → `stages/pre-revenue.md`
        ├─ customers = 0 AND had_customers_before → `stages/restart.md`
        ├─ customers > 0 AND MRR < $100K AND team < 10 → `stages/growth.md`
        └─ MRR ≥ $100K OR team ≥ 10 → `stages/scaling.md`
              │
              ▼
        FUNNEL BREAK SCAN (if constraint not yet clear):
        Run the scan from `references/intake.md` — "Walk me through your last 10..."
        │
        ├─ Numbers drop at Acquisition → constraint = awareness/reach
        ├─ Numbers drop at Activation → constraint = onboarding/time-to-value
        ├─ Numbers drop at Revenue → constraint = pricing/sales/objections
        ├─ Numbers drop at Retention → constraint = product/fit/success
        └─ Can't identify where it breaks → `references/pillar-goldratt.md`
              │
              ▼
        CONSTRAINT IDENTIFIED → Work it. But first check:
        │
        └─ Is constraint work blocked by strategic confusion?
              • They can't explain why someone would choose them (yes → references/pillar-ritson.md)
              • They're trying to serve everyone (yes → references/pillar-ritson.md)
              • "More marketing" but no position (yes → references/pillar-ritson.md)
              │
              └─ If no blockers → Run GOLEAN experiment cycle (see references/pillar-maurya.md)
```
```

Use the Edit tool with the exact old_string and new_string from above.

### - [ ] Step 3: Edit 2 — insert the State File Schema section between the Decision Tree and the Symptom → Constraint Map

The current file has this after the decision tree code block:

```
---

## Symptom → Constraint Map
```

Replace that with exactly:

```
---

## State File Schema (for reading `.factory/`)

When `.factory/` exists in CWD, the STATE LOAD branch above loads its files. The schema is inlined here so reads don't require loading `references/state.md` — that file is only needed for **writes** (ritual completions, bootstrap, edge cases).

### `.factory/context.md` — 7 H2 headers

- `## Identity` — what you do, who for
- `## Numbers` — customer count, MRR/ARR, team size, optional runway
- `## Stage` — `pre-revenue` | `restart` | `growth` | `scaling` + justification
- `## JTBD` — primary job customers hire you to do (Christensen/Moesta language)
- `## Current constraint` — customer-factory step (Acquisition / Activation / Revenue / Retention / Referral), magnitude, date diagnosed
- `## Current experiment` — what's running, metric, deadline
- `## Notes` — free-form

Read by exact header name. Missing → ask the founder for that field. Renamed → confirm before using.

**Constraint vocabulary rule:** `## Current constraint` MUST name one of the five customer-factory steps. Never write free prose like "we have a sales problem" — write "Revenue (close rate)" instead. This keeps constraints comparable across weeks.

### `.factory/journal.md` — entry headers

Each entry starts with:
`## YYYY-MM-DD — <ritual type>`

where `<ritual type>` is one of:
- `Weekly review (<stage>)`
- `Diagnosis`
- `Experiment committed`
- `Experiment outcome`
- `Kill decision`
- `Stage change`

Read the **last 8 entries** from the bottom on every activation (count `##` headings).

### Opening-line patterns

After loading state, open the conversation by acknowledging where things stand. Pick the first pattern that matches:

- Most recent journal entry is >30 days old → "It's been a while. Has anything shifted — customer count, team, what's broken?"
- Recent `Experiment committed` with no matching `Experiment outcome` → "Last week you committed to [experiment]. Did the metric move?"
- Recent `Diagnosis` without follow-through → "Two weeks ago we named [constraint]. What's happened since?"
- Most recent entry is `Kill decision` → "Last week you killed [what was killed] — what are you trying instead?"
- Fresh state, nothing pending → "Where do you want to focus today?"

**For writing to state (ritual completion, bootstrap, edge cases) → load `references/state.md`.**

---

## Symptom → Constraint Map
```

Use the Edit tool with the old_string `---

## Symptom → Constraint Map` and the new_string above.

### - [ ] Step 4: Edit 3 — add the "Name the protocol" item to the Response format

The current Response format is at the top of the file, right after the H1:

```
**Response format:** 
1. Ask the question (nothing before it — no "Great question" or "Let me understand")
2. **Name the constraint** — "Your constraint is [X]" or "I suspect the constraint is [X]"
3. Assign the experiment — "This week: do X and tell me what you find"

All three, every time. If you can't name the constraint yet, your question should surface it.
```

Replace with exactly:

```
**Response format:** 
1. Ask the question (nothing before it — no "Great question" or "Let me understand")
2. **Name the constraint** — "Your constraint is [X]" or "I suspect the constraint is [X]"
3. Assign the experiment — "This week: do X and tell me what you find"
4. **Name the protocol** — When you run a named protocol (napkin test, five tests, funnel break scan, weekly review, positioning sprint, Mafia Offer), say its name explicitly: "I'm running the napkin test." Founders learn protocol names by hearing them in context.

All four, every time where applicable. If you can't name the constraint yet, your question should surface it.
```

### - [ ] Step 5: Edit 4 — add a row to the Reference Routing Table

The current last row of the Reference Routing Table is:

```
| Plan is not a real strategy, or competitive/uncertainty question | `references/pillar-strategy.md` |
```

Replace with exactly:

```
| Plan is not a real strategy, or competitive/uncertainty question | `references/pillar-strategy.md` |
| State write, bootstrap, or edge cases | `references/state.md` |
```

### - [ ] Step 6: Read back and verify all 4 edits are in place

Run Read tool on `SKILL.md` and confirm:

- `STATE LOAD:` appears in the Decision Tree section (Edit 1)
- `## State File Schema` appears as an H2 between Decision Tree and Symptom → Constraint Map (Edit 2)
- `4. **Name the protocol**` appears in the Response format (Edit 3)
- `| State write, bootstrap, or edge cases |` appears in the Reference Routing Table (Edit 4)

If any verification fails, use the Edit tool again to fix the specific edit.

### - [ ] Step 7: Verify line count is reasonable

Run: `wc -l SKILL.md`
Expected: Between 170 and 210 lines (was ~130; gained ~50 lines).

If significantly outside this range, re-read the file — something may have been duplicated or lost.

### - [ ] Step 8: Commit

```bash
git add SKILL.md
git commit -m "feat(state): add STATE LOAD branch, inline schema, protocol-naming rule

Four additions to SKILL.md:
1. STATE LOAD branch at top of decision tree with explicit parallel-read
   instruction for Round 2 (journal.md + stages/<stage>.md)
2. New 'State File Schema' section inlining the 7 context.md headers,
   journal entry format, and opening-line patterns (so read path doesn't
   require loading references/state.md)
3. 'Name the protocol' item 4 in Response format — teaches Claude to
   name-drop protocols it runs (discoverability fix for problem B)
4. Reference routing table row for references/state.md (write path)

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Modify `references/intake.md` — append named-protocols section

**Files:**
- Modify: `references/intake.md`

**Rationale:** Adds a discoverable list of named protocols at the end of intake.md so founders who've used Factory Floor before can invoke them directly. Combined with SKILL.md's "name the protocol" rule, this is the content side of the discoverability fix (problem B).

### - [ ] Step 1: Read the current end of `intake.md`

Run Read tool on `/home/mario/code/Factory Floor/references/intake.md`.

The file currently ends at line 88 with:

```
If you have these, skip the intake and go straight to triage.
```

### - [ ] Step 2: Append the named-protocols section

Use the Edit tool. Find this exact text at the end of `references/intake.md`:

```
If you have these, skip the intake and go straight to triage.
```

Replace with exactly:

```
If you have these, skip the intake and go straight to triage.

---

## Named protocols you can ask for by name

If you've used Factory Floor before and want to skip ahead, you can invoke any of these directly:

- **"Run the napkin test"** — pre-revenue: math the unit economics on paper before building anything
- **"Run the five tests"** — pre-revenue: five gates an idea has to pass before you should build
- **"Run the Mafia Offer protocol"** — pre-revenue: design an offer customers can't refuse, test it before building the MVP
- **"Run the funnel break scan"** — any stage: walk through your last 10 signups/demos/deals to find where the funnel actually breaks
- **"Do my weekly review"** — any stage: stage-appropriate review format, 10-25 min depending on stage
- **"Run the positioning sprint"** — when positioning is the constraint: call 3 best customers, capture their exact words, ship the position
```

### - [ ] Step 3: Verify the appendix is in place

Use Grep to confirm the appendix exists:

Run: `grep -c "Named protocols you can ask for by name" references/intake.md`
Expected: **1**

Run: `grep -c "Run the napkin test" references/intake.md`
Expected: **1**

Run: `grep -c "Run the positioning sprint" references/intake.md`
Expected: **1**

### - [ ] Step 4: Commit

```bash
git add references/intake.md
git commit -m "feat(state): add named-protocols appendix to intake.md

Lists six named protocols founders can invoke by name (napkin test, five
tests, Mafia Offer, funnel break scan, weekly review, positioning sprint).
Combined with SKILL.md's 'name the protocol' rule, this is the content
side of the discoverability fix — no slash commands needed.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Modify `bin/install.mjs` — add `references/state.md` to the copy list

**Files:**
- Modify: `bin/install.mjs`

**Rationale:** The installer copies skill files to `~/.claude/skills/factory-floor/`. It has an explicit list of files to copy. The new `references/state.md` must be added to this list or it won't be installed when users run `npx @swiftner/factory-floor`.

### - [ ] Step 1: Read the current `bin/install.mjs` files array

Run Read tool on `/home/mario/code/Factory Floor/bin/install.mjs`.

The current `files` array is:

```javascript
const files = [
  'SKILL.md',
  'references/intake.md',
  'references/misdiagnoses.md',
  'references/coaching-patterns.md',
  'references/pillar-goldratt.md',
  'references/pillar-maurya.md',
  'references/pillar-sharp.md',
  'references/pillar-ritson.md',
  'references/estimation.md',
  'references/jtbd.md',
  'references/weekly-review.md',
  'references/pillar-strategy.md',
  'references/weekly-diagrams.md',
  'stages/pre-revenue.md',
  'stages/restart.md',
  'stages/growth.md',
  'stages/scaling.md',
  'scripts/render-diagram.mjs',
  'scripts/package.json',
]
```

### - [ ] Step 2: Add `references/state.md` to the array

Use the Edit tool. Find this exact text:

```
  'references/coaching-patterns.md',
  'references/pillar-goldratt.md',
```

Replace with exactly (the new entry goes alphabetically between `coaching-patterns.md` and `pillar-goldratt.md`; `state` comes after `pillar-strategy` alphabetically but we'll keep the existing loose ordering and insert grouped with other references — picking the position right before `pillar-goldratt.md` matches the existing pattern of references/ entries coming before stages/ entries without strict alphabetical ordering):

```
  'references/coaching-patterns.md',
  'references/state.md',
  'references/pillar-goldratt.md',
```

### - [ ] Step 3: Verify the edit

Run Grep: `grep "references/state.md" bin/install.mjs`
Expected: exactly one match, containing `'references/state.md',`.

Run: `node -e "const f = require('fs').readFileSync('bin/install.mjs', 'utf-8'); const m = f.match(/const files = \[([\s\S]*?)\]/); console.log(m[1].split(',').filter(s => s.trim()).length)"`
Expected: **20** (was 19, added 1).

### - [ ] Step 4: Verify `bin/install.mjs` still parses as valid JavaScript

Run: `node --check bin/install.mjs`
Expected: No output (success). If there's a syntax error, re-read the file and fix.

### - [ ] Step 5: Commit

```bash
git add bin/install.mjs
git commit -m "feat(state): include references/state.md in installer copy list

Ensures 'npx @swiftner/factory-floor' installs the new state.md
reference alongside the existing skill files.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Manual validation pass

**Files:**
- Reference: all 8 fixtures in `evals/scenarios/state-layer/`
- Reference: `docs/superpowers/specs/2026-04-07-factory-floor-state-layer-design.md` §11

**Rationale:** The state layer adds runtime behavior with filesystem side effects. Automated evals don't exist yet (see spec §11 and §12). Before merging, walk through each scenario manually in a test directory and confirm the skill behaves as the fixture's "Expected behaviors" prescribe. Document findings in the commit message.

### - [ ] Step 1: Create a scratch test directory

```bash
mkdir -p /tmp/factory-floor-test
cd /tmp/factory-floor-test
git init
```

This gives you a clean CWD that is a git repo (needed for bootstrap to test the `.gitignore` update).

### - [ ] Step 2: Validate scenario 01 (bootstrap)

In the scratch directory, invoke Claude Code. Provide the prompt from `evals/scenarios/state-layer/01-bootstrap.md`:

> "I don't know what to do next. I've been building for three months and I'm not sure I'm on the right track."

Follow the conversation as the pre-revenue persona. Answer intake questions realistically.

After the conversation, verify:

```bash
ls /tmp/factory-floor-test/.factory/
# Expected: context.md, journal.md

cat /tmp/factory-floor-test/.factory/context.md
# Expected: all 7 H2 headers present

cat /tmp/factory-floor-test/.factory/journal.md
# Expected: just "# Journal"

cat /tmp/factory-floor-test/.gitignore
# Expected: contains ".factory/journal.md"
```

Note findings in a scratch file `/tmp/factory-floor-test/validation-notes.md`. Mark scenario 01 PASS/FAIL with evidence.

### - [ ] Step 3: Validate scenario 02 (read continuity)

Create a new subdirectory and pre-populate state:

```bash
mkdir -p /tmp/factory-floor-test/scenario-02
cd /tmp/factory-floor-test/scenario-02
mkdir -p .factory
```

Write `/tmp/factory-floor-test/scenario-02/.factory/context.md` with the fully populated content from fixture 02's Setup section (copy the 7 headers and populate with the Swiftner-like data).

Write `/tmp/factory-floor-test/scenario-02/.factory/journal.md` with a `# Journal` title and two entries: a Diagnosis and an Experiment committed, per the fixture's Setup.

Invoke Claude Code in that directory with the prompt: "What should I focus on this week?"

Verify Claude opens with the "Did the metric move?" pattern and does NOT ask any intake questions. Note PASS/FAIL.

### - [ ] Step 4: Validate scenario 03 (partial state)

Create subdirectory `scenario-03` with a `.factory/context.md` that has 6 of 7 headers (missing `## Current constraint`). Invoke with the prompt from the fixture.

Verify Claude asks specifically about the constraint and does NOT ask about stage/customers/team (those are in state). Note PASS/FAIL.

### - [ ] Step 5: Validate scenario 04 (auto-write weekly review)

Create subdirectory `scenario-04` with a fully populated `.factory/context.md` (growth stage) and `.factory/journal.md` with `# Journal` plus one prior entry.

Invoke Claude Code with: "Do my weekly review."

Go through all 5 growth-stage weekly review questions. Answer all of them, including "one thing we will NOT do."

After the review, verify:

```bash
cat /tmp/factory-floor-test/scenario-04/.factory/journal.md
# Expected: A new entry appended with header `## <today's date> — Weekly review (growth)`
#           and all 5 sub-sections populated.
```

Note PASS/FAIL.

### - [ ] Step 6: Validate scenario 05 (founder override)

Create subdirectory `scenario-05` similar to scenario 04. Invoke with:

> "Do my weekly review. But don't log this one — I'm going to vent about the cofounder situation."

Go through the full weekly review. Answer all questions.

After the review, verify:

```bash
cat /tmp/factory-floor-test/scenario-05/.factory/journal.md
# Expected: NO new entry (journal is unchanged from the setup state)
```

Note PASS/FAIL.

### - [ ] Step 7: Validate scenario 06 (stale Numbers)

Create subdirectory `scenario-06` with `.factory/context.md` whose `## Numbers` section contains an explicit old date marker (e.g., `(as of 2026-02-01)`). Make sure the most recent journal entry is also more than 30 days old relative to today.

Invoke with: "What should I focus on this week?"

Verify Claude re-confirms the numbers before diving into coaching. Note PASS/FAIL.

### - [ ] Step 8: Validate scenario 07 (header rename)

Create subdirectory `scenario-07` with `.factory/context.md` where `## Current constraint` is renamed to `## Current bottleneck` (same body content).

Invoke with: "What should I focus on this week?"

Verify Claude asks the rename confirmation question. Note PASS/FAIL.

### - [ ] Step 9: Validate scenario 08 (constraint vocabulary)

Create subdirectory `scenario-08` with `.factory/context.md` where `## Current constraint` is "TBD" or empty.

Invoke with: "We're not converting demos. I think we need to train the sales team better."

Go through the diagnosis conversation. When Claude writes the Diagnosis entry, verify:
- The journal entry's Diagnosis field uses a customer-factory step name (e.g., "Revenue"), not free prose
- `context.md`'s updated `## Current constraint` also uses a factory step name
- Both agree on the constraint

Note PASS/FAIL.

### - [ ] Step 10: Validate on Swiftner's actual repo (dogfood)

In Mario's actual Swiftner repo, run Factory Floor with a real question. Observe whether the bootstrap feels natural, whether `context.md` ends up populated correctly, and whether the opening line on subsequent sessions lands.

This is the ultimate validation — if Factory Floor can coach its author about his actual company, the feature works.

Note findings.

### - [ ] Step 11: Meta-validation — run Factory Floor on the Factory Floor repo

In `/home/mario/code/Factory Floor`, invoke Claude Code with: "What should we focus on this week?"

Observe whether the skill triggers correctly, whether it runs intake (since `.factory/` doesn't exist in its own repo), and whether it routes to an appropriate stage (probably growth, given Mario has users and a small team).

This is a dogfood test specific to this project — can Factory Floor coach its own author about Factory Floor?

Note findings.

### - [ ] Step 12: Consolidate validation notes and commit

Create `docs/superpowers/validation/2026-04-07-state-layer-manual-validation.md` with:

- One section per scenario (01 through 08)
- Each section: PASS / FAIL / PARTIAL, with a 2-3 sentence description of what happened
- A "Dogfood findings" section with observations from steps 10 and 11
- A "Known issues" section with any gaps found that need follow-up

Commit:

```bash
git add docs/superpowers/validation/
git commit -m "docs: manual validation findings for state layer

Walked through all 8 scenario fixtures + dogfood on Swiftner repo +
meta-test on the Factory Floor repo itself. Full findings in the
validation notes.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

If any scenario FAILED, do not mark the plan complete. Open a follow-up task or return to the relevant earlier task to fix the issue.

---

## Self-review checklist (for plan author)

**1. Spec coverage:**

| Spec section | Covered by task |
|---|---|
| §4.1 Runtime file layout (`.factory/context.md`, `.factory/journal.md`) | Task 2 (examples), Task 6 (validation) |
| §4.2 Factory Floor repo file layout | Tasks 2-5 |
| §4.3 Control flow | Task 3 (STATE LOAD branch) |
| §5.1 `context.md` schema (7 headers + constraint vocabulary) | Task 2 (state.md), Task 3 (inline schema in SKILL.md) |
| §5.2 `journal.md` schema (6 ritual types + stage-parameterized weekly review) | Task 2 |
| §5.3 SKILL.md changes (4 additions) | Task 3 |
| §5.4 `references/state.md` contents | Task 2 |
| §5.5 `references/intake.md` appendix | Task 4 |
| §5.6 Installer updates | Task 5 |
| §6 Read protocol + opening-line patterns | Task 3 (inlined in SKILL.md) |
| §7 Write protocol | Task 2 (state.md §1) |
| §8 Bootstrap protocol | Task 2 (state.md §2) |
| §9 8 edge cases | Task 2 (state.md §4) |
| §10 Performance optimizations (parallel reads, schema inlining) | Task 3 |
| §11 Scenario fixtures (8) | Task 1 |
| §11.2 Manual validation | Task 6 |

All spec sections are covered by at least one task. ✓

**2. Placeholder scan:**

- Searched plan for "TBD", "TODO", "fill in", "similar to Task N", "implement later" — none found in step instructions. The strings "TBD" that appear in the `context.md` examples (e.g., `TBD — capture in a future session`) are intentional *content* for the bootstrap-generated file, not plan placeholders.
- Every code step contains complete content (full file contents, not excerpts).
- Every commit step has the complete commit command.

**3. Type consistency:**

- Ritual type names are consistent across Tasks 1, 2, 3: `Weekly review (<stage>)`, `Diagnosis`, `Experiment committed`, `Experiment outcome`, `Kill decision`, `Stage change`. ✓
- Header names are consistent across Tasks 1, 2, 3: `Identity`, `Numbers`, `Stage`, `JTBD`, `Current constraint`, `Current experiment`, `Notes`. ✓
- Customer-factory step names are consistent: `Acquisition`, `Activation`, `Revenue`, `Retention`, `Referral`. ✓
- File paths are consistent: `.factory/context.md`, `.factory/journal.md`, `references/state.md`, `evals/scenarios/state-layer/XX-name.md`. ✓

Self-review passes. Plan ready for execution.
