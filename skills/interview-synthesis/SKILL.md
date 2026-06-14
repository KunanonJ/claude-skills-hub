---
name: interview-synthesis
description: >
  Customer interview synthesis expert that turns raw transcripts into themed
  insights, an opportunity solution tree, and a follow-up question list using
  Teresa Torres' continuous discovery methodology.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: project-management
  domain: pm-discovery
  updated: 2026-05-21
  python-tools: interview_synthesizer.py
  tech-stack: customer-interviews, opportunity-solution-tree, jobs-to-be-done
---
# Customer Interview Synthesis Expert

## Overview

Turn customer interview transcripts into actionable product opportunities. This skill takes raw question-and-answer transcripts and produces three artifacts: (1) themed insight clusters, (2) an opportunity solution tree mapping outcomes to opportunities and candidate solutions, and (3) a prioritized list of follow-up questions to close evidence gaps.

The synthesis approach is grounded in Teresa Torres' Continuous Discovery Habits (opportunity solution trees), Steve Portigal's interview methodology (looking for stories and contradictions), and the Jobs-To-Be-Done synthesis approach popularized by Alan Klement (situation-motivation-outcome decomposition).

### When to Use

- **Post-interview synthesis** -- You have 3-20 interview transcripts and need to extract themes before they become stale.
- **Opportunity space mapping** -- Building an opportunity solution tree before committing to solutions.
- **Discovery sprint readout** -- Sharing findings with the product trio (PM, Design, Engineering) and stakeholders.
- **Evidence gap analysis** -- Identifying which assumptions still lack interview evidence and need targeted follow-ups.

### When NOT to Use

- Quantitative survey synthesis -- use a data analysis skill instead.
- Usability test debriefs -- use a UX research-specific workflow.
- Sales call analysis for win/loss -- use `business-growth/` skills.

## Synthesis Framework

The framework moves from raw transcript -> coded snippets -> themes -> opportunities -> solutions, with explicit evidence trails at each step.

### Step 1: Snippet Extraction (Portigal)

For each interview, extract atomic snippets. A snippet is a single quote or paraphrase that captures one of:

- **A story** -- A specific past event with context, action, and outcome ("Last Tuesday I tried to..."). Stories are the highest-evidence data.
- **A contradiction** -- The participant says X but their behavior shows Y. Contradictions reveal latent needs.
- **A surprise** -- Something the interviewer did not expect. Surprises mark the edge of the team's mental model.
- **An emotion** -- Frustration, delight, fear, relief. Emotional markers signal motivation strength.

Avoid extracting opinions about hypothetical futures ("I would use X if...") -- they are low-evidence.

### Step 2: Coding into Categories

Each snippet is coded with:

- **Need code** -- What underlying need does this point to? (e.g., "trust-in-data", "time-to-insight", "control-over-process")
- **Job code** -- What job-to-be-done is the participant trying to accomplish? Use the Klement format: *When [situation], I want to [motivation], so I can [outcome].*
- **Pain code** -- What specific friction, risk, or workaround appears? (e.g., "manual-reconciliation", "fear-of-data-loss")
- **Gain code** -- What positive outcome would matter? (e.g., "faster-close", "audit-trail", "peer-recognition")
- **Strength** -- 1 (single mention), 2 (multiple participants), 3 (multiple participants + behavioral evidence)

### Step 3: Theme Clustering

Group coded snippets into themes. A theme requires:

- At least 3 snippets
- From at least 2 different participants
- Sharing a coherent need, job, pain, or gain code

For each theme, write a 1-sentence headline that a stakeholder can scan in 5 seconds. Example: *"Finance leads do not trust automated reconciliations because they cannot see the rule that produced each match."*

### Step 4: Opportunity Solution Tree (Torres)

Build a tree with four levels:

```
Outcome (top)
  |
  +-- Opportunity 1 (a customer need, pain, or desire)
  |     +-- Solution A
  |     +-- Solution B
  |     +-- Solution C
  |
  +-- Opportunity 2
        +-- Solution D
        +-- Solution E
```

**Rules:**

- The outcome at the top is a measurable business or user outcome -- not a feature.
- Opportunities are customer-side framings ("Finance leads cannot verify automation rules"), not solution-side ("Add a rules dashboard").
- Each opportunity must trace to >=1 themed insight.
- Solutions live under opportunities so the team can compare multiple solutions against the same opportunity.

### Step 5: Follow-Up Question Generation

For each weak-evidence theme (strength <= 2) or unmapped assumption, generate 2-3 targeted follow-up questions for the next round of interviews. Good follow-ups:

- Ask for stories, not opinions ("Tell me about the last time..." not "Would you...").
- Probe contradictions ("You mentioned X earlier but also Y -- can you walk me through that?").
- Test counterfactuals ("If [workaround] disappeared tomorrow, what would you do?").

## Workflow

1. **Prepare input.** Convert interview notes into JSON with one entry per interview containing participant id, role, and a list of question/answer pairs. See `assets/interview_input_template.json`.
2. **Run the synthesizer.** `python scripts/interview_synthesizer.py --input interviews.json --format markdown --output synthesis.md`. Use `--format mermaid` for the opportunity solution tree alone.
3. **Review themes.** Validate each theme against the source snippets. Drop themes that fail the 3-snippet / 2-participant threshold.
4. **Refine the tree.** Edit the generated tree in `assets/opportunity_tree_template.md`. Add or split opportunities based on stakeholder review.
5. **Plan follow-ups.** Use the generated follow-up list to script the next interview round.
6. **Hand off.** Feed validated opportunities into `discovery/brainstorm-experiments/` for hypothesis design, or directly into `execution/create-prd/` if evidence is strong enough.

## Tools

| Tool | Purpose | Command |
|------|---------|---------|
| `interview_synthesizer.py` | Cluster snippets into themes, build opportunity solution tree, generate follow-up questions | `python scripts/interview_synthesizer.py --input interviews.json --format markdown --output synthesis.md` |

The tool supports all six PM-standard output formats (`json`, `markdown`, `mermaid`, `confluence`, `notion`, `linear`) per `SHARED_OUTPUT_SCHEMA.md`. Use `--demo` to generate a sample output for any format.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| Themes feel generic or obvious | Snippet extraction captured opinions, not stories | Re-extract using the story/contradiction/surprise/emotion filter; drop hypothetical-future quotes |
| Opportunity tree has too many top-level opportunities (>7) | Outcome at the top is too broad | Narrow the outcome (e.g., "Increase activation" -> "Reduce time from signup to first successful import") |
| Solutions appear instead of opportunities | Team jumped to solution mode during synthesis | Rewrite each opportunity as a customer-side framing; move every "Add X feature" line into the Solutions row |
| Only 1-2 themes emerge from 10+ interviews | Coding categories too narrow OR participants too homogenous | Broaden need codes to capture latent jobs; check that participants span at least 2 segments |
| Follow-up questions are leading or close-ended | Questions phrased as solution validation | Convert each follow-up to a "Tell me about the last time you..." story-prompt |
| Mermaid tree renders flat in Confluence | Confluence requires the Mermaid macro to be enabled | Use `--format confluence` which converts the tree to a nested bullet list |
| `--input` JSON parse error | Interview file missing required fields (`participant`, `qa`) | Validate against `assets/interview_input_template.json`; run `python -m json.tool interviews.json` |

## Success Criteria

- Every theme references >=3 snippets from >=2 participants
- Opportunity tree has 1 measurable outcome at the top, 3-7 opportunities, and >=1 solution per opportunity
- Each opportunity traces back to >=1 themed insight (evidence trail intact)
- Follow-up questions are story-prompts, not opinion-prompts
- Synthesis produced within 5 working days of the last interview (before insights decay)
- Stakeholders can read the executive summary in under 3 minutes and name the top 3 opportunities

## Scope & Limitations

**In Scope:**
- Qualitative synthesis of 3-20 customer interview transcripts
- Theme clustering with evidence thresholds
- Opportunity solution tree generation (Mermaid + Markdown)
- Follow-up question generation for evidence gaps
- Multi-format output (Markdown, JSON, Mermaid, Confluence, Notion, Linear)

**Out of Scope:**
- Live interview facilitation -- this skill works on completed transcripts
- Quantitative analysis (survey statistics, click-stream data)
- Sentiment scoring via ML -- the tool uses deterministic keyword and code matching only
- Win/loss analysis -- use `business-growth/` skills
- Persona generation -- the output is opportunity-centric, not persona-centric

**Important Caveats:**
- Synthesis quality is bounded by interview quality. Garbage in, garbage out.
- The opportunity solution tree is a thinking aid, not a roadmap. Solutions still need experiment validation.
- Teresa Torres' methodology assumes continuous discovery (weekly touchpoints). One-off interview rounds produce shallower trees.

## Integration Points

| Integration | Direction | What Flows |
|-------------|-----------|------------|
| `discovery/brainstorm-experiments/` | Feeds into | Validated opportunities become hypotheses for lean experiments |
| `discovery/identify-assumptions/` | Bidirectional | Assumptions inform follow-up questions; interview evidence resolves assumptions |
| `discovery/brainstorm-ideas/` | Feeds into | Themed insights seed Product Trio ideation sessions |
| `discovery/pre-mortem/` | Feeds into | Pain themes surface candidate risks for pre-mortem analysis |
| `execution/create-prd/` | Feeds into | Top opportunities + supporting evidence populate PRD Background and Market Segments sections |
| `execution/job-stories/` | Feeds into | Klement-format job codes convert directly into When/Want/So job stories |

## Tool Reference

### interview_synthesizer.py

Ingests interview JSON and produces themed clusters, an opportunity solution tree, and a follow-up question list.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--input` | string | (required unless `--demo`) | Path to interview JSON file (see `assets/interview_input_template.json`) |
| `--format` | string | `markdown` | Output format: `json`, `markdown`, `mermaid`, `confluence`, `notion`, `linear` |
| `--output` | string | stdout | Output file path; if omitted, prints to stdout |
| `--outcome` | string | "Improve customer outcome" | Top-of-tree outcome label |
| `--min-strength` | int | 1 | Drop themes below this evidence strength (1-3) |
| `--demo` | flag | off | Generate sample synthesis using a built-in fixture |

**Mermaid diagram type:** `graph LR` (opportunity solution tree).

## References

- `references/synthesis-methodology-guide.md` -- Full methodology with worked examples (Torres, Portigal, Klement)
- `assets/interview_input_template.json` -- JSON schema for interview transcripts
- `assets/opportunity_tree_template.md` -- Editable opportunity solution tree template
