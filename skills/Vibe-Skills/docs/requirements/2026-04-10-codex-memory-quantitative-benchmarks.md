# Codex Memory Quantitative Benchmarks

Date: 2026-04-10
Run ID: 20260410-codex-memory-quantitative-benchmarks
Mode: interactive_governed
Runtime lane: root_governed

## Goal

Quantify whether the current workspace-shared memory design remains effective for Codex-style user calls under repeated follow-up scenarios, not just single happy-path recalls.

## Deliverable

A benchmark-style regression surface that:

- measures related follow-up hit rate across multiple Codex simulation cases
- measures unrelated follow-up false-recall rate
- measures continuity retention after intervening unrelated turns
- measures cross-workspace leak rate when backend roots are intentionally shared
- keeps the benchmark reusable as a normal pytest regression entrypoint

## Constraints

- Work inside the target `Vibe-Skills` repository root (`<repo-root>`)
- Reuse the current Codex simulation harness instead of inventing a second host simulator
- Keep the benchmark focused on memory behavior, not unrelated host-specialist bridge failures
- Use governed runtime paths that match real Codex-style task submission as closely as practical
- Keep assertions stable and deterministic enough for CI-style reruns

## Acceptance Criteria

- The benchmark covers at least three quantitative dimensions with multiple simulated cases each
- Related follow-up cases produce a measurable hit-rate summary rather than a single binary pass/fail
- Unrelated follow-up cases prove a zero or near-zero false-recall rate at the benchmarked threshold
- Cross-workspace cases prove that shared backend-root configuration does not leak memories across workspace identities
- The suite can be run independently and alongside the existing memory regressions

## Product Acceptance Criteria

- A maintainer can answer "does memory still work under repeated Codex follow-ups?" using reproducible evidence
- The benchmark separates relevant recall, irrelevant suppression, and workspace isolation instead of collapsing them into one broad test
- The benchmark is narrow enough to fail on memory regressions without being polluted by unrelated host-runtime failures

## Manual Spot Checks

- Inspect the selected memory capsules for at least one relevant follow-up case
- Inspect the selected memory capsules for at least one unrelated follow-up case
- Confirm that requirement and plan artifacts only show memory context when a benchmarked hit actually occurs
- Confirm that two distinct Codex workspaces sharing the same backend root still return empty backend reads for cross-workspace follow-ups

## Completion Language Policy

- Do not describe the memory system as "effective" unless quantitative benchmark evidence is present
- Call out boundaries explicitly when the benchmark only proves lexical-family recall rather than deep semantic paraphrase recall
- Keep non-memory regressions separate from the benchmark conclusion

## Delivery Truth Contract

- Evidence must come from runnable benchmark tests and fresh outputs
- Benchmark conclusions must distinguish measured success from untested capability
- No claims about semantic-vector retrieval may be made from this benchmark

## Non-Goals

- Re-architecting the memory system in this run
- Fixing unrelated installed-host specialist bridge degradation
- Proving semantic paraphrase retrieval beyond the lexical-family cases we actually benchmark
- Replacing the existing functional memory tests

## Autonomy Mode

interactive_governed with inferred assumptions

## Inferred Assumptions

- The user wants reusable quantitative evidence, not only one-off exploratory runs
- The existing Codex simulation harness is the correct place to express benchmark scenarios
- The current design goal is to prove stable governed-memory behavior before attempting more ambitious semantic retrieval work
