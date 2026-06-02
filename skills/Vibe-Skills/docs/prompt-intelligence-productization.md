# Prompt Intelligence Productization

## Scope

Wave75 converts prompt intelligence from a loose asset bundle into a **productized advisory layer**.

The goal is not to create a second prompt router.
The goal is to make prompt intelligence observable, reviewable, and promotable inside the same VCO control plane.

## Productized Surfaces

Prompt intelligence may be productized through four bounded surfaces:

| Surface | Allowed output | Explicit boundary |
|---|---|---|
| `pattern_cards` | operator-readable pattern cards | cannot replace pack selection |
| `risk_checklist` | prompt risk checklist and quality metadata | cannot override route or skill |
| `route_hints` | advisory route hints for confirmation and review | cannot become a second router |
| `confirm_hints` | higher-risk prompt patterns may trigger stronger confirmation wording | cannot silently escalate privileges |

## Advisory-First Invariants

The following rules are non-negotiable:

1. `pattern cards` remain reference assets, not executable route owners.
2. `risk checklist` remains a quality signal, not a promotion command.
3. `route hints` can annotate VCO choices, but cannot rewrite `selected.pack_id` or `selected.skill`.
4. `confirm hints` can harden prompts, but cannot bypass normal control-plane safeguards.
5. Prompt intelligence must never become a searchable second router with independent authority.

## Productization Ladder

| Stage | What is true |
|---|---|
| `shadow` | pattern cards and risk checklist exist as reference-only assets |
| `soft_candidate` | route hints and confirm hints are operator-visible, advisory-first, and gate-bound |
| `strict_candidate_review` | quality metadata is consistently attached to governed prompt scenarios and board-reviewed |

Even in `strict_candidate_review`, prompt intelligence remains advice-first.

## Evidence Requirements

Prompt intelligence productization is credible only when the following evidence exists:

- `references/prompt-pattern-cards.md` is treated as canonical pattern evidence;
- `references/prompt-risk-checklist.md` captures reusable risk criteria;
- productization rules are recorded in this governance doc;
- the promotion board tracks prompt intelligence as a first-class governed surface;
- `scripts/verify/vibe-prompt-intelligence-productization-gate.ps1` validates the above.

## Operator View

Operators should be able to answer three questions quickly:

1. Which pattern cards were used?
2. Which risk checklist items were triggered?
3. Did prompt intelligence only emit route hints / confirm hints, or did it try to exceed its advisory boundary?

If the third question cannot be answered confidently, the productization stage must fall back to `shadow`.
