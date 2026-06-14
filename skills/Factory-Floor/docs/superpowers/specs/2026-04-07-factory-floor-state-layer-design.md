# Factory Floor — State Layer & Discoverability Design

**Date:** 2026-04-07
**Status:** Design approved, pending implementation plan
**Author:** Mario Michelli (with Claude Code)

---

## 1. Goal

Make Factory Floor remember founders across sessions so every conversation doesn't start from zero, and make its named protocols discoverable without adding slash commands.

## 2. Background & motivation

Two problems Factory Floor currently has, surfaced during the 2026-04-07 brainstorming:

**Problem A — "Every conversation starts from zero."** Factory Floor has no memory between sessions. A founder re-explains their stage, constraint, JTBD, team size, and current experiment every single time. The skill can't open with "last week your constraint was X — did the metric move?" because it doesn't know there *was* a last week.

**Problem B — "The good stuff is hidden."** Factory Floor contains sharp named protocols (napkin test, five tests, Mafia Offer, funnel break scan, weekly review, positioning sprint) buried inside stage files. Founders get them only when Claude happens to route there. They can't ask for them by name unless they already know the names.

Problem A is the architectural work. Problem B is solvable with a content change, no new infrastructure.

Ideas considered and deliberately **not** pursued in this spec:
- Slash commands (`/factory:napkin`, etc.) — dropped because they're Claude Code-specific and conflict with the skill's cross-platform distribution (npm, Codex, Claude Desktop, agentskills.io).
- Pillar-as-personas — interesting but orthogonal to the continuity problem.
- Temporal pattern detection (drift across multiple weeks) — partially absorbed by the Diagnosis ritual capturing the founder's framing; a separate analysis feature is deferred.
- Template cascade / user-domain overrides — deferred until there's real demand.

## 3. Scope

**In scope:**
- A persistent state layer stored in `.factory/` in the founder's CWD.
- Automatic read on every skill activation, automatic write after ritual completion.
- One bootstrap flow for first-use scaffolding.
- Changes to `SKILL.md` to integrate state into the decision tree.
- A new reference file `references/state.md` for write protocol, bootstrap, examples, edge cases.
- A small discoverability edit to `references/intake.md` and a response-format rule in `SKILL.md`.
- Installer updates (`bin/install.mjs`) to copy the new reference file.
- New evals for the state layer.

**Out of scope:**
- Refactoring the existing stage files (`stages/pre-revenue.md`, `stages/growth.md`, etc.).
- Reducing the size of stage files or pillar references.
- Multi-company-per-user support (one company per CWD).
- Claude Desktop auto-write (degraded to a documented manual workflow).
- Slash commands.

## 4. Architecture

### 4.1 File layout (runtime — in the founder's project)

```
<founder's CWD>/
└── .factory/
    ├── context.md      # stable, committed to repo
    └── journal.md      # append-only, gitignored
```

`.factory/` is created on first-use bootstrap. It is project-local; a founder running Factory Floor in a different directory gets different state (or no state). This matches how founders actually run Claude Code — from inside their company repo.

### 4.2 File layout (Factory Floor repo — what changes)

```
SKILL.md                           # modified: state load branch, inline schema, protocol naming
references/
├── intake.md                      # modified: named-protocols appendix
├── state.md                       # NEW: write protocol, bootstrap, examples, edge cases
└── (all other references unchanged)
stages/                            # unchanged
agents/, evals/                    # evals gets new tests (section 10)
scripts/                           # unchanged
bin/install.mjs                    # modified: copy references/state.md
```

No files are deleted. No existing files are restructured. The state layer is additive — existing routing and stage files continue to work when `.factory/` is absent.

### 4.3 Control flow

**Cold start with `.factory/` present:**

```
Claude triggers on founder message
  │
  ├─ Read SKILL.md (already in context when skill activates)
  │
  ├─ Decision tree: .factory/ exists in CWD → STATE LOAD
  │
  ├─ Round 1: Read .factory/context.md
  │
  ├─ Round 2 (parallel):
  │     • Read .factory/journal.md (tail: last 8 entries)
  │     • Read stages/<stage>.md (stage from context.md)
  │
  ├─ Open conversation with state-aware pattern (see §6.2)
  │
  └─ Proceed to diagnosis / coaching with full context
```

Two read rounds, one of them parallelized. `references/state.md` is **not** loaded on the read path — its content (write protocol, bootstrap, edge cases) is only needed when writing, which is rare.

**Cold start without `.factory/`:**

```
Claude triggers on founder message
  │
  ├─ Read SKILL.md
  │
  ├─ Decision tree: no .factory/ → run intake.md as today
  │
  ├─ After intake establishes enough state: offer bootstrap (see §8)
  │
  └─ If accepted → create .factory/ (load references/state.md at this moment)
```

**Ritual completion (write path):**

```
Ritual detected (weekly review complete, experiment accepted, etc.)
  │
  ├─ Load references/state.md (first time this session)
  │
  ├─ Follow write protocol for the detected ritual type
  │
  ├─ Append to .factory/journal.md and/or update .factory/context.md
  │
  └─ Acknowledge write to founder ("Logged.")
```

## 5. Detailed design

### 5.1 `.factory/context.md` schema

Stable company state. Committed to the repo so the team shares the truth. Prescribed H2 headers, free-form bodies. Edited by Claude on updates, can be edited by hand.

**Header set (7 headers):**

| Header | Purpose | Example body |
|---|---|---|
| `## Identity` | What you do, who for. Stable. | "Swiftner is sales-call analytics for inside sales teams at B2B SaaS companies of 10-50 reps." |
| `## Numbers` | Customer count, MRR/ARR, team size, optional runway. Updated freely between sessions. Drives stage re-evaluation. | "14 paying customers · $4.2K MRR · team of 2 · runway 9 months" |
| `## Stage` | `pre-revenue` \| `restart` \| `growth` \| `scaling`, with one-line justification. | "growth — first paying customers, product-market fit signals, focus on repeatable sales" |
| `## JTBD` | Primary job customers hire you to do, in Christensen/Moesta form. Optional dominant force. | "When sales reps join a new company, they want to ramp up faster, so they can hit quota in Q1 instead of Q2." |
| `## Current constraint` | Which customer-factory step (Acquisition / Activation / Revenue / Retention / Referral), magnitude, date diagnosed. **MUST use customer-factory vocabulary** — not free prose. | "Activation — 7-day rate at 18%. Diagnosed 2026-03-24." |
| `## Current experiment` | What's running, metric, deadline. Empty if no experiment is committed. | "Rewrite onboarding email sequence. Metric: 7-day activation rate. Deadline: 2026-04-14." |
| `## Notes` | Free-form escape hatch. Anything the founder wants Claude to remember that doesn't fit elsewhere — brand codes, ICP, in-flight initiatives. | (free text) |

**Header rules:**

- **Read by exact header name.** If a header is missing, ask the founder for that field and write the answer under a freshly added header.
- **Renames require confirmation.** If a founder renames `## Current constraint` to `## Current bottleneck`, Claude cannot find the expected name and asks: "I see `## Current bottleneck` — should I treat that as `## Current constraint`?" Never auto-rewrite.
- **Constraint vocabulary is enforced.** `## Current constraint` must name one of the five customer-factory steps (Acquisition, Activation, Revenue, Retention, Referral), plus specifics. Don't write "we have a sales problem" — write "Revenue (close rate) — only 12% of demos convert." This is load-bearing: it makes the constraint comparable across weeks and across founders.

**Example `context.md`:**

```markdown
# Swiftner

## Identity
Sales-call analytics for inside sales teams at B2B SaaS companies of 10-50 reps.

## Numbers
14 paying customers · $4.2K MRR · team of 2 · runway 9 months

## Stage
growth — first paying customers with product-market fit signals, team is small, focus is on repeatable sales

## JTBD
When sales reps join a new company, they want to ramp up faster, so they can hit quota in Q1 instead of Q2.

## Current constraint
Activation — only 18% of signups complete onboarding within 7 days. Diagnosed 2026-03-24.

## Current experiment
Rewrite onboarding email sequence to pull users to first "aha" in <10 min. Metric: 7-day activation rate. Deadline: 2026-04-14.

## Notes
- ICP: inside-sales leaders at Norwegian B2B SaaS, 10-50 reps
- Do NOT chase enterprise — burned on that in 2025
- Brand codes: orange, conversational tone, "sales reality" not "sales theater"
```

### 5.2 `.factory/journal.md` schema

Append-only history. Gitignored by default (personal coaching log — can contain candid reflections).

**Entry header format (enforced):**

```
## YYYY-MM-DD — <ritual type>
```

For Weekly review entries, the stage goes in parens:

```
## 2026-04-07 — Weekly review (growth)
```

**Six ritual types and their recommended sub-sections:**

| Ritual | Trigger | Recommended sub-sections |
|---|---|---|
| `Weekly review (<stage>)` | Founder ran the weekly review protocol to its end | Stage-specific (see below). Always ends with **"One thing we will NOT do"** |
| `Diagnosis` | Constraint identified or re-identified, founder accepts | **Founder's initial framing**, **Symptom probed**, **Diagnosis** (customer-factory language), **Why not the others**, **Confidence** |
| `Experiment committed` | Founder explicitly accepts an assigned experiment ("ok I'll do that") | **Experiment**, **Constraint it attacks**, **Metric**, **Deadline** |
| `Experiment outcome` | Founder reports back on a prior experiment at/after deadline | **Did the metric move?**, **What we learned**, **Next** |
| `Kill decision` | Experiment or initiative stopped early, before deadline | **What was killed**, **Why**, **What we learned**, **What we'll try instead** |
| `Stage change` | Stage transition confirmed (e.g., pre-revenue → growth) | **From**, **To**, **Trigger**, **What changes about how we work** |

**Weekly review sub-sections by stage** (from `references/weekly-review.md`):

- **Pre-revenue:** Conversations count, What we learned, Hypothesis check, Next week's one thing, **One thing we will NOT do**
- **Growth:** Constraint + movement, Numbers (found / activated / paid / churned), Work pile, Next week's 3 priorities, **One thing we will NOT do**
- **Scaling:** Funnel snapshot, Buffer/flow, Initiative traffic lights, Policy constraint scan, Next week's focus, **One thing we will NOT do**

The **"One thing we will NOT do"** capture is load-bearing — it appears in every weekly review in the existing protocol and must be preserved in journal entries.

**Diagnosis entries capture two things, not one:**

Per `references/misdiagnoses.md`, the founder's *initial framing* of the problem is itself diagnostic (recurring tells like "we need more features," "everyone is a customer"). Each Diagnosis entry records both what the founder *thought* the problem was AND what was actually diagnosed. This gives temporal data for spotting framing patterns without a dedicated pattern-detection subsystem.

**Sub-sections are recommended, not enforced.** The H2 entry header is the only load-bearing structure. Bold labels like `**Constraint:**` are conventional to help Claude pattern-match, but missing one is not an error.

**Read tail rule:** On every activation, Claude reads the **last 8 entries** from the bottom of `journal.md`. Count `##` headings from the bottom. This is ~2-3K tokens of context, enough for 6-8 weeks of coaching history. Older entries are archive.

**Example `journal.md`:**

```markdown
# Journal

## 2026-03-24 — Diagnosis
**Founder's initial framing:** "We need more features."
**Symptom probed:** Do customers who activate stay? → 92% retention at 90 days.
**Diagnosis:** Activation (customer-factory step). 7-day activation rate at 18%. Not a product problem.
**Why not the others:** Acquisition is fine (signups growing 12% mo/mo). Retention is fine (92%). Pricing closes when activated users see value.
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

### 5.3 SKILL.md changes

Four additions, no removals. SKILL.md grows from ~130 lines to ~150 lines.

**Addition 1 — New top branch in the decision tree** (before "No context?"):

```
START
  │
  ├─ STATE LOAD: If `.factory/` exists in CWD:
  │     Round 1 — Read `.factory/context.md`.
  │     Round 2 (PARALLEL) — Read these at the same time:
  │       • `.factory/journal.md` (last 8 entries — count ## headings from bottom)
  │       • `stages/<stage>.md` (stage comes from context.md's `## Stage` header)
  │     State is now conversation context. Proceed to stage-appropriate coaching.
  │
  ├─ Check context: From state + conversation, do you know stage, customer count,
  │  the symptom, what they've tried?
  │     ├─ Yes → STAGE ROUTER
  │     └─ No → Load `references/intake.md`, ask ONLY for missing fields, return here
  │
  └─ STAGE ROUTER ... (unchanged)
```

**Addition 2 — Inline state file schema** (new section after the decision tree):

```markdown
## State File Schema (for reading `.factory/`)

`.factory/context.md` has these H2 headers:

- `## Identity` — what you do, who for
- `## Numbers` — customer count, MRR/ARR, team size, optional runway
- `## Stage` — pre-revenue | restart | growth | scaling + justification
- `## JTBD` — primary job customers hire you to do (Christensen/Moesta language)
- `## Current constraint` — customer-factory step (Acquisition / Activation / Revenue / Retention / Referral), magnitude, date
- `## Current experiment` — what's running, metric, deadline
- `## Notes` — free-form

Read by exact header name. Missing → ask founder. Renamed → confirm before using.
**Constraint is always named as a customer-factory step, never free prose.**

`.factory/journal.md` has entries with header format:
`## YYYY-MM-DD — <ritual>` where ritual is one of:
`Weekly review (<stage>)`, `Diagnosis`, `Experiment committed`,
`Experiment outcome`, `Kill decision`, `Stage change`.

Read the last 8 entries from the bottom on every activation.

**For write protocol, bootstrap, and edge cases → load `references/state.md`.**
```

~20 lines. The read path is now self-sufficient inside SKILL.md — no second file load required for the cold path.

**Addition 3 — New item in "Response format":**

```
4. **Name the protocol** — When you run a named protocol (napkin test, five tests,
   funnel break scan, weekly review, positioning sprint, Mafia Offer), say its
   name explicitly. "I'm running the napkin test." Founders learn protocol
   names by hearing them in context.
```

**Addition 4 — New row in the Reference Routing Table:**

```
| State write, bootstrap, or edge cases | references/state.md |
```

### 5.4 New file: `references/state.md`

Loaded lazily — only when a ritual completion is detected or when bootstrapping. Not loaded on the read path (SKILL.md is self-sufficient for reads).

**Section 1 — Write protocol**

Claude writes to state ONLY when one of these triggers fires. Each trigger has a specific write action.

| Trigger | Detection rule | Write action |
|---|---|---|
| Weekly review complete | Founder ran the weekly-review protocol to its end (all stage-specific questions answered, including "one thing we will NOT do") | Append `## YYYY-MM-DD — Weekly review (<stage>)` entry to `journal.md` with stage-specific sub-sections |
| Experiment committed | Founder explicitly accepts an assigned experiment with affirmative language: "ok I'll do that", "yes, let's run it", "sure, this week", or similar | Append `## YYYY-MM-DD — Experiment committed` entry AND update `## Current experiment` in `context.md` |
| Diagnosis accepted | Claude named the constraint AND the founder affirmed explicitly ("yes that's it", "agreed", "makes sense") OR the founder immediately accepted a proposed experiment attacking that constraint (which also triggers Experiment committed — both writes fire) | Append `## YYYY-MM-DD — Diagnosis` entry AND update `## Current constraint` in `context.md`. Entry MUST include both founder's initial framing and actual diagnosis. |
| Experiment outcome reported | Founder reports back at/after deadline on a prior experiment | Append `## YYYY-MM-DD — Experiment outcome` entry |
| Experiment killed early | Founder says they stopped an experiment before deadline | Append `## YYYY-MM-DD — Kill decision` entry AND clear `## Current experiment` in `context.md` |
| Stage transition confirmed | Constraint shift large enough to change stage (e.g., first paying customer moves pre-revenue → growth) and founder confirms | Update `## Stage` in `context.md` AND append `## YYYY-MM-DD — Stage change` entry |
| Numbers change mentioned | Founder mentions a meaningful number change ("we're at 17 customers now", "MRR doubled") | Update `## Numbers` in `context.md`. **No journal entry** — Numbers churn freely. |

**Founder override rule:** If the founder says "don't log this" / "don't write to my factory" / "keep this off the record" or similar, skip the write for that session and acknowledge: "OK, not logging this one." No further writes in that session unless the founder re-authorizes.

**Section 2 — Bootstrap protocol**

Runs when `.factory/` does not exist in CWD AND the current intake conversation has surfaced enough information to populate `context.md`.

Offer once:

> "Want me to set up `.factory/` for this company? I'll create a `context.md` from what we just discussed and start a `journal.md`. It lives in this directory. The journal stays local (gitignored)."

If founder consents:

1. Ask one bootstrap-only question (not part of intake): *"In one sentence — what does this company do and who for?"* (Populates `## Identity`. Intake starts with "do you have paying customers" and never captures identity explicitly.)
2. Create `.factory/` directory in CWD.
3. Write `.factory/context.md`:
   - `## Identity` from the bootstrap question answer
   - `## Numbers` from intake answers (customers, MRR, team, runway if mentioned)
   - `## Stage` from intake routing decision + one-line justification
   - `## JTBD` if it came up in intake, otherwise write "TBD — capture in a future session"
   - `## Current constraint` if the funnel break scan ran, otherwise "TBD — run the funnel break scan next session"
   - `## Current experiment` empty
   - `## Notes` empty
4. Write `.factory/journal.md` with just `# Journal` as the title.
5. Append `.factory/journal.md` to the project's `.gitignore` — create the file if it doesn't exist, add only this one line, don't touch other entries.
6. Confirm: "Done. `.factory/context.md` is committable; `.factory/journal.md` is gitignored. Edit them by hand any time."

If founder declines bootstrap → don't offer again this session. They can ask later.

**Section 3 — Examples**

- Full example `context.md` (see §5.1)
- Full example `journal.md` with one entry per ritual type (see §5.2)

**Section 4 — Edge cases**

See §9.

### 5.5 `references/intake.md` appendix

New section appended to the bottom of the existing file. No changes to the existing intake flow.

```markdown
## Named protocols you can ask for by name

If you've used Factory Floor before and want to skip ahead, you can invoke
any of these directly:

- "Run the napkin test" — pre-revenue: math the unit economics on paper
  before building anything
- "Run the five tests" — pre-revenue: five gates an idea has to pass
- "Run the Mafia Offer protocol" — pre-revenue: design an offer customers
  can't refuse, test it before building
- "Run the funnel break scan" — any stage: walk through your last 10
  signups/demos/deals to find where the funnel breaks
- "Do my weekly review" — any stage: stage-appropriate review format,
  10-25 min depending on stage
- "Run the positioning sprint" — when positioning is the constraint:
  call 3 best customers, capture their exact words, ship the position
```

Combined with SKILL.md's new "name the protocol" response-format rule, this solves Problem B: founders learn the names by hearing Claude say them during runs, and have a written reference to fall back on.

### 5.6 Installer updates (`bin/install.mjs`)

Add one file to the copy list:

```javascript
const files = [
  'SKILL.md',
  'references/intake.md',
  'references/misdiagnoses.md',
  'references/coaching-patterns.md',
  'references/state.md',                // NEW
  'references/pillar-goldratt.md',
  // ... rest unchanged
]
```

The installer already creates `~/.claude/skills/factory-floor/references/`, so the new file lands in the right place automatically. No other installer changes.

## 6. Read protocol (detailed)

### 6.1 Cold-start flow with `.factory/` present

1. Skill triggers on a founder message.
2. Claude reads `SKILL.md` (already loads on activation).
3. Decision tree: `.factory/` exists → STATE LOAD.
4. **Round 1**: Read `.factory/context.md`. Parse the 7 H2 headers.
5. **Round 2 (parallel)**: In a single tool-use batch, read:
   - `.factory/journal.md` — last 8 entries from the bottom
   - `stages/<stage>.md` where `<stage>` is from `## Stage` in context.md
6. State and stage are now loaded. Claude opens the conversation with a state-aware pattern (see §6.2).

**Total read rounds:** 2 (one sequential, then one parallel). Current cold path is 3-5 sequential rounds with intake cascading. This is the primary latency improvement.

### 6.2 Opening-line patterns

Claude opens the conversation by acknowledging state. Five patterns, matched against the journal tail:

| Situation | Opening pattern |
|---|---|
| Recent `Experiment committed` without a matching `Experiment outcome` | "Last week you committed to [experiment]. Did the metric move?" |
| Recent `Diagnosis` without follow-through | "Two weeks ago we named [constraint]. What's happened since?" |
| Most recent entry is a `Kill decision` | "Last week you killed [what was killed] — what are you trying instead?" |
| State is older than 30 days (last entry > 30d ago) | "It's been a while. Has anything shifted — customer count, team, what's broken?" |
| State is fresh, no pending items | "Where do you want to focus today?" |

Opening-line patterns are critical — the continuity isn't real until Claude *says it back* to the founder. This is where the "every conversation starts from zero" pain actually dissolves.

### 6.3 Partial state handling

If `.factory/context.md` has some headers but not all, Claude reads what's there and asks intake questions ONLY for the missing fields. No double-asking.

If `.factory/journal.md` is missing entirely, Claude treats the journal as empty (no tail to read) and proceeds with context.md only.

If `.factory/context.md` is missing but `.factory/journal.md` exists (rare edge case), Claude reads the journal tail and offers to reconstruct context.md from it.

## 7. Write protocol (detailed)

See §5.4 Section 1 for the full trigger table. Key principles:

1. **Writes are rare and deliberate.** Only ritual completions trigger writes. Q&A, exploration, and coaching conversations do NOT write anything.
2. **Founder can override at any time.** "Don't log this" stops the write for the session.
3. **Writes are additive.** Journal entries are appended, never edited. Context.md fields are updated in place, but the previous value can be reconstructed from the journal (via the Stage change / Diagnosis entries that record transitions).
4. **Writes are announced.** After writing, Claude says "Logged." (one word, not a wall of text) so the founder knows state was updated.

## 8. Bootstrap protocol (detailed)

See §5.4 Section 2. One additional clarification not mentioned in the offer text:

**Bootstrap is offered only once per session.** If the founder declines, Claude doesn't re-offer until a new session or the founder explicitly asks. Repeated offers would be nagging.

**Bootstrap requires enough intake context.** Don't offer bootstrap after only the first 1-2 intake questions. Wait until intake has reached the funnel break scan OR the founder has answered at least: stage, customer count, team size, primary problem. Otherwise `context.md` would be mostly empty.

## 9. Edge cases

Eight cases with precise behaviors, enumerated in `references/state.md` Section 4:

| # | Case | Behavior |
|---|---|---|
| 1 | `.factory/` partial (only `context.md` or only `journal.md`) | Read whatever exists. Don't error. Create the missing file on first write that needs it. |
| 2 | Required header missing in `context.md` | Ask the founder for that field. Write under a freshly added header. Don't refuse to proceed. |
| 3 | Header renamed by founder (e.g., `## Current bottleneck`) | Claude can't find expected name. Asks: "I see `## Current bottleneck` — should I treat that as `## Current constraint`?" Don't auto-rewrite. |
| 4 | State conflicts with founder's stated reality | Trust the founder. Ask: "Sounds like the state is stale. Want me to log a Stage change to restart and update context.md?" |
| 5 | `## Numbers` older than 30 days | Before routing, re-confirm: "Your Numbers section says 14 customers, $4.2K MRR — is that still right?" Update if changed. |
| 6 | Wrong-factory mismatch (founder runs in a directory with someone else's `.factory/`) | Opens with saved state per §6.2. If founder says "wait, that's wrong" → Claude asks if this is the wrong directory. Never delete or overwrite without consent. |
| 7 | Bootstrap can't gitignore (CWD isn't a git repo) | Tell founder honestly: "Not a git repo here — `.factory/journal.md` won't be gitignored unless you initialize git or add a `.gitignore` manually. The journal still gets created, just not protected from accidental commits later." Don't refuse to bootstrap. |
| 8 | Claude Desktop / no-CWD environments | README documents the manual workflow: founder uploads `.factory/context.md` as project knowledge; auto-write is disabled; Claude tells the founder what entry it would have written and the founder copy/pastes into their local `journal.md` themselves. |

## 10. Performance considerations

Two optimizations included in the design specifically to attack startup latency:

### 10.1 Parallel reads in SKILL.md

Cold-start file reads today are implicitly sequential — routing decisions cascade. The new STATE LOAD branch explicitly instructs Claude to parallelize Round 2 reads (`.factory/journal.md` + `stages/<stage>.md`). This changes cold start from multiple sequential read rounds (each routing decision triggering the next read) to 2 rounds — one sequential read of `context.md`, then a single parallel batch for the rest.

Claude *can* parallelize tool calls when explicitly told to; the current SKILL.md doesn't tell it to. An explicit instruction in the STATE LOAD branch is ~5 lines and directly addresses the perceived "takes some time and reads and processes a while."

### 10.2 Schema inlined in SKILL.md (state.md not on the read path)

`references/state.md` as drafted would have contained a read protocol section. The design moves that content into SKILL.md as an inline schema (~20 lines). This means the read path loads SKILL.md + `context.md` + journal.md + stage file — no state.md load.

`references/state.md` is loaded only when a ritual completion is detected (rare), for the write protocol and bootstrap protocol. Writes are uncommon compared to reads, so the lazy-load trade-off favors the common case.

### 10.3 Known latency costs NOT addressed by this spec

- **First-use in a new directory** (no state) runs the full intake flow exactly as today. Intake is Q&A-driven, not file-read-driven, so this isn't a file-read latency problem — it's unavoidable without prior state.
- **Stage files are 12-20 KB each.** Reading `stages/growth.md` in full is a meaningful chunk of latency. Refactoring stage files into smaller chunks is a separate project and deliberately out of scope here.
- **Re-diagnosis sessions** that need to load pillar references (Sharp, Ritson, Maurya) on top of state and stage still have multiple reads. The state layer doesn't change that.

## 11. Validation strategy

Factory Floor has an `evals/` directory with an aspirational `README.md` describing a persona/scenario/judge/runs structure, plus `agents/grader.md` and `agents/analyzer.md` which are grading and analysis agent prompts. `agents/openai.yaml` is the agentskills.io skill manifest (name, icon, tags, color), not an evals config.

**Current reality:** the eval *framework* (personas/ scenarios/ judges/ runs/ subdirectories, a runner to execute persona↔skill dialogues, judge integration to score responses) does not exist yet. It's described in `evals/README.md` as the intended shape but not implemented.

**Implication for this spec:** we can't write runnable evals because there's nothing to run. Instead we:
1. **Create scenario fixtures** for the 8 test cases below as markdown files in `evals/scenarios/state-layer/` — one file per scenario with the persona description, opening prompt, expected Claude behaviors, and grading criteria. These become the inputs when someone builds the runner.
2. **Rely on manual validation** during implementation (run the skill in test directories, confirm behavior matches each scenario's expected behaviors).
3. **Defer the eval runner itself** to a separate plan. Building persona replay, judge integration, and a runs harness is a substantial project that would double the scope here.

The state layer adds runtime behavior with filesystem side effects, so manual validation of bootstrap, override, and write-trigger behaviors is non-negotiable before merging.

### 11.1 Scenario fixtures to create

1. **Bootstrap eval** — Empty CWD. Run intake. Verify Claude offers bootstrap at the right moment (after funnel break scan or enough fields gathered). On consent, verify `.factory/context.md` and `.factory/journal.md` exist with correct shape, `.gitignore` updated with `.factory/journal.md`.
2. **Read continuity eval** — Pre-populate `.factory/` with realistic growth-stage state, recent Experiment committed, no Outcome. Trigger skill. Verify Claude opens with "Did the metric move?" pattern, NOT with intake questions.
3. **Partial-state eval** — Pre-populate `context.md` with all headers except `## Current constraint`. Verify Claude reads what's there, asks ONLY about constraint, does not re-run intake.
4. **Auto-write trigger eval** — Run a growth-stage weekly review to completion (all questions answered, including "one thing we will NOT do"). Verify `Weekly review (growth)` entry appended with all stage-specific sub-sections.
5. **Override eval** — Say "don't log this" during a ritual. Verify no write happens. Verify Claude acknowledges with "OK, not logging this one."
6. **Stale Numbers eval** — Pre-populate state with `## Numbers` dated 60 days ago (include a date comment in the body). Verify Claude re-confirms before routing.
7. **Header rename eval** — Pre-populate `context.md` with `## Current bottleneck` instead of `## Current constraint`. Verify Claude asks the confirmation question rather than auto-rewriting.
8. **Constraint vocabulary eval** — Run a Diagnosis ritual. Verify the new constraint in the journal entry AND the updated `## Current constraint` in context.md use customer-factory vocabulary (Acquisition / Activation / Revenue / Retention / Referral), not free prose.

### 11.2 Manual validation

- **Run Factory Floor on Swiftner's repo** (the maintainer's actual company) — does bootstrap feel natural, does the opening line land, does the journal capture the right things.
- **Run on a fresh scratch directory** with no context — verify nothing breaks when there's no `.factory/` and no obvious company.
- **Meta test: run Factory Floor on the Factory Floor repo itself** — can Factory Floor coach its own author about itself? Dogfooding signal.

## 12. Open questions / future work

**Not blocking this spec, worth tracking:**

- **Stage file size.** `stages/growth.md` is ~20 KB. That's a real latency tax on every session. Splitting stage files into smaller chunks (e.g., `growth/constraint-work.md`, `growth/weekly-review.md`, `growth/worked-examples.md`) would let Claude load only what's needed. Separate project.
- **Claude Desktop degradation.** The manual workflow for Claude Desktop (founder uploads context.md as project knowledge, auto-write disabled) is honest but second-class. If Claude Desktop ever adds filesystem access, the state layer could work there natively.
- **Pattern detection across weeks.** Problem E from the brainstorming ("you've named the same constraint 4 weeks running and the metric hasn't moved") is partially absorbed by Diagnosis entries capturing founder framing — Claude can notice patterns when reading the tail. A dedicated "drift detector" is deferred.
- **Multi-company support.** One `.factory/` per CWD means a consultant with multiple clients uses separate directories. If a meaningful user asks for `~/.factory-floor/<company>/` global state with session-start switching, revisit.
- **Eval runner framework.** `evals/README.md` describes a persona/scenario/judge/runs framework that doesn't exist yet. This spec captures the 8 state-layer scenarios as fixture files, but there's no runner to execute them. Building the runner (persona replay, judge integration, results aggregation) is a separate project that would let the fixtures become automated regression tests instead of manual validation checklists.

## 13. Summary of file changes

| File | Change | Lines added |
|---|---|---|
| `SKILL.md` | Modified: state load branch, inline schema, protocol-naming rule, new reference routing row | ~20 |
| `references/intake.md` | Modified: named-protocols appendix | ~15 |
| `references/state.md` | **NEW:** write protocol, bootstrap protocol, examples, edge cases | ~200 |
| `bin/install.mjs` | Modified: add `references/state.md` to copy list | 1 |
| `evals/` | New eval files for state layer (8 scenarios) | ~400 across multiple files |

Nothing is deleted. Nothing is restructured. The design is purely additive.
