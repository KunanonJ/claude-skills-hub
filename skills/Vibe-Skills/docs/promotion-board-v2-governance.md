# Promotion Board v2 Governance

## Purpose

Wave78 upgrades the promotion board from a simple stage ledger into **board v2**, where stage review, scorecard evidence, replay readiness, rollback readiness, and release readiness are evaluated together.

Board v2 is still advice-first.
It records promotion evidence; it does not auto-promote planes.

## Board v2 Responsibilities

Board v2 must answer the following:

1. Which governed planes or governance tracks are in scope?
2. What is their current stage and next stage?
3. Which gates are mandatory before the next stage can be considered?
4. What scorecard bucket did the plane achieve?
5. Are replay, rollback, and operator-readiness evidence present?
6. What is the board’s `next_intake_effect` on the wider program?

## Required Board v2 Fields

Every tracked item should expose, directly or through board evidence, the following concepts:

- `current_stage`
- `next_stage`
- `required_gates`
- `scorecard_bucket`
- `replay_ready`
- `rollback_ready`
- `operator_readiness`
- `release_train_readiness`
- `evidence_summary`
- `next_intake_effect`

## Stage Semantics

| Stage | Meaning in board v2 |
|---|---|
| `shadow` | governed but not yet relied on for rollout |
| `soft` | soft_candidate evidence exists and operator review can proceed |
| `strict` | strict_candidate review is justified by evidence, not by aspiration |
| `promote` | release-facing exposure is approved by the board, never by script alone |

## Evidence Inputs

Board v2 consumes evidence from:

- plane scorecards in `references/plane-scorecards.md`;
- task contract and replay ledger governance;
- rollback drill evidence;
- ops cockpit health views;
- release train v2 evidence bundling;
- `config/promotion-board.json` as the operator-facing board snapshot.

## Decision Rules

Board v2 must preserve these rules:

1. `scorecard_bucket` cannot override missing rollback or replay evidence.
2. `strict_candidate` is a review state, not a self-serve promotion state.
3. `operator_readiness` must be visible before release train readiness is claimed.
4. `next_intake_effect` must be explicit so that upstream expansion decisions remain evidence-based.

Validation is performed by `scripts/verify/vibe-promotion-scorecard-gate.ps1`.
