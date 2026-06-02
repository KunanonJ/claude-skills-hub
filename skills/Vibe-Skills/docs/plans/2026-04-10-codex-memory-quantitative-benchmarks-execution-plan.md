# Codex Memory Quantitative Benchmarks Execution Plan

Date: 2026-04-10
Run ID: 20260410-codex-memory-quantitative-benchmarks
Internal grade: L
Runtime lane: root_governed

## Scope

Add a dedicated quantitative benchmark layer on top of the current Codex memory simulation harness by combining:

1. benchmark helper extraction from the existing Codex simulation tests
2. multi-case related follow-up hit-rate measurement
3. multi-case unrelated false-recall measurement
4. multi-case continuity-retention measurement after intervening unrelated turns
5. multi-case cross-workspace leak-rate measurement
6. regression verification against the existing memory core suites

## Serial Execution Units

1. Inspect the current Codex simulation harness and freeze benchmark dimensions
2. Add helper functions that extract repeatable memory-hit metrics from governed runtime outputs
3. Add a related follow-up hit-rate benchmark with multiple lexical-family cases
4. Add an unrelated follow-up false-recall benchmark with multiple unrelated cases
5. Add an intervening-turn continuity benchmark with multiple filler-depth cases
6. Add a cross-workspace leak-rate benchmark that intentionally shares a backend root
7. Run the benchmark suite by itself
8. Run the benchmark suite together with the existing memory regressions
9. Clean caches and temporary residue and audit `node` / `pwsh` zombie processes

## Ownership Boundaries

- Root lane owns the requirement doc, execution plan, benchmark tests, and final evidence summary
- Benchmark helpers stay colocated with the Codex simulation test surface
- No unrelated installed-host specialist bridge logic is modified in this run

## Verification Commands

- `pytest tests/runtime_neutral/test_codex_memory_user_simulation.py -q`
- `pytest tests/runtime_neutral/test_installed_host_runtime_simulation.py -q -k high_fidelity_memory_continuity`
- `pytest tests/runtime_neutral/test_codex_memory_user_simulation.py tests/runtime_neutral/test_memory_runtime_activation.py tests/runtime_neutral/test_memory_progressive_disclosure.py tests/runtime_neutral/test_runtime_contract_schema.py tests/runtime_neutral/test_cross_host_memory_identity.py tests/runtime_neutral/test_workspace_shared_memory_plane.py tests/runtime_neutral/test_memory_ingest_noise_filters.py tests/integration/test_runtime_config_manifest_roles.py tests/integration/test_runtime_script_manifest_roles.py tests/integration/test_version_governance_runtime_roles.py -q`

## Delivery Acceptance Plan

- Benchmark cases must be numerous enough to produce a rate, not just a single example
- Related-hit assertions must use the same governed runtime path that Codex-style tasks actually use
- False-recall and leak-rate assertions must ignore local state-store fallback digests and focus on backend memory injection
- Final reporting must separate measured benchmark outcomes from known non-memory failures

## Completion Language Rules

- Use quantitative wording such as hit rate, false-recall rate, retention rate, and leak rate where evidence exists
- Do not imply semantic-paraphrase coverage if the benchmark only proves lexical-family continuity
- Do not collapse unrelated host-runtime failures into memory-system conclusions

## Rollback Rules

- Remove only the benchmark docs and benchmark tests if the suite proves unstable
- Do not touch unrelated host-runtime simulation behavior unless a benchmark change directly requires it

## Phase Cleanup Expectations

- Remove `.pytest_cache`, `__pycache__`, and `.tmp` residue created by verification
- Preserve requirement, plan, and benchmark test files
- Audit `node` and `pwsh` zombie processes and report if any remain
