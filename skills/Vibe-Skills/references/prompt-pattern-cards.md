# Prompt Pattern Cards

This file translates high-value prompt engineering guidance into VCO-native pattern cards.
Each card is compact, reusable, and designed to support `prompt-overlay` and `prompt-asset-boost` without creating a second prompt surface.

| ID | Pattern | Use When | Core Structure | Avoid |
|---|---|---|---|---|
| P01 | Role-Goal-Constraints | need fast task framing | role + outcome + constraints + deliverable | vague role-only prompts |
| P02 | Explicit Output Schema | structured output required | schema + fields + validation hints | free-form output when parser needed |
| P03 | Few-Shot Anchor | repeated style or shape needed | 1-3 examples + invariants | too many examples causing context bloat |
| P04 | Plan-Then-Execute | multi-step work | planning phase + execution phase | mixing planning and execution blindly |
| P05 | Decompose-and-Assign | XL / multi-agent work | tasks + owners + interfaces | overlapping ownership |
| P06 | Ask-or-Assume Guard | ambiguity present | clarify critical unknowns / list assumptions | silent guessing on high-risk ambiguity |
| P07 | Retrieval First | source-grounded task | retrieve -> summarize -> answer | answering from memory when current docs needed |
| P08 | Tool Contract Prompt | tool use needs guardrails | tool purpose + inputs + stop conditions | unconstrained tool loops |
| P09 | Critique Pass | quality-sensitive output | draft -> critique -> revise | one-pass finalization |
| P10 | Self-Check Checklist | reliability before completion | answer + checklist + gaps | unverifiable “done” claims |
| P11 | Compare-and-Recommend | trade-off analysis | options + criteria + recommendation | false binary framing |
| P12 | Risk-Flag Prompt | safety/security review | scope + risk categories + evidence | broad fearmongering without evidence |
| P13 | Boundary Prompt | conflict-prone integration | what it does / does not do | unchecked scope creep |
| P14 | Contract Extraction | convert prose to policy | terms + required keys + non-goals | loose narrative without structure |
| P15 | Prompt Refine | improve existing prompt | preserve intent + reduce ambiguity + tighten output | rewriting intent away |
| P16 | Chain-of-Thought Suppression | user wants concise reasoning output | hidden reasoning + short answer + explicit checks | exposing verbose latent reasoning |
| P17 | ReAct-Lite | tool-interactive research | observe -> act -> summarize | uncontrolled agent loops |
| P18 | PAL | code-assisted reasoning | specify subproblem -> run math/code -> interpret | hand-wavy numeric reasoning |
| P19 | Safety Rewrite | user prompt contains risky phrasing | retain task intent + remove unsafe instruction patterns | overblocking harmless requests |
| P20 | Evaluation Prompt | score candidate outputs | rubric + score + evidence | ungrounded preferences |
| P21 | Counterexample Hunt | need robustness | claim + failure cases + edge inputs | only checking happy paths |
| P22 | Compression Prompt | context pressure present | compress into facts / decisions / open issues | lossy summarization without labels |
| P23 | Escalation Prompt | confirmation is required | show decision options + consequences | forcing silent default choice |
| P24 | Evidence Table | source-backed recommendation | claim + source + confidence + gap | claims without provenance |

## Usage Notes

- Cards are advisory assets, not routing triggers by themselves.
- Prefer card composition over inventing new prompt surfaces.
- Any new card must declare: use case, failure mode, and non-goal.
