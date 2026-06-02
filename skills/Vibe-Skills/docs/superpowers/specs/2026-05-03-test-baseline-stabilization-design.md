# Test Baseline Stabilization Design

## Summary

This design targets the next layer of technical debt in `<repo-root>`:
the repository has many tests, but no explicit, repeatable, risk-aware baseline
surface for running them as a full validation set.

Recent focused debt cleanup made the immediate merge blockers green:

- `check.sh` no longer depends on Bash `mapfile`.
- Windows Bash path normalization preserves trailing directory separators.
- `.vibeskills/` is classified as local operator noise.

The current routing and terminology gates are also green:

- `vibe-current-routing-debt-gate.ps1 -Json` reports `P0 = 0`, `P1 = 0`,
  `P2 = 0`, and `P3 = 0`.
- `vibe-routing-terminology-hard-cleanup-scan.ps1 -Json` reports
  `fail_count = 0` and `review_count = 0`.

The remaining debt is not a single known failing test. It is that full-test
validation is not yet safely observable. `tests/runtime_neutral` collects 923
tests and `tests/integration` collects 190 tests. Some local install/profile
tests are already known to be slow, and previous broad sweeps in this repository
family have been more reliable when run as targeted evidence rather than as one
unbounded command.

The recommended direction is a risk-aware baseline layer: classify tests by
execution layer and risk, produce repeatable evidence, and only then decide
which failures are code regressions, missing host dependencies, slow-test debt,
or unsafe external/network paths.

## Current Evidence

Fresh local repository state:

```text
## main...origin/main [ahead 42]
```

Recent local commits:

```text
8c244225 chore: classify vibeskills local state as noise
b998790f test: stabilize Windows bash setup helpers
ab79cbb0 fix: remove bash mapfile from check entrypoint
d7d609ff docs: plan test merge blocker debt cleanup
6f603df7 docs: design test merge blocker debt cleanup
```

Focused gates and tests already checked during exploration:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
```

Observed summary:

```text
status = pass
P0 = 0
P1 = 0
P2 = 0
P3 = 0
```

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
```

Observed summary:

```text
status = pass
fail_count = 0
review_count = 0
```

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\integration\test_runtime_core_packaging_roles.py -q
```

Observed result:

```text
8 passed
```

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\unit\test_runtime_packaging_resolver.py tests\runtime_neutral\test_install_profile_differentiation.py -q
```

Observed result:

```text
7 passed
```

This command took roughly one minute, which shows that install/profile tests can
be materially slower than fast contract/unit checks even when they pass.

Test collection evidence:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral --collect-only -q
```

Observed result:

```text
923 tests collected
```

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\integration --collect-only -q
```

Observed result:

```text
190 tests collected
```

The current test infrastructure already includes Python bytecode isolation in
`tests/conftest.py`:

```text
PYTHONDONTWRITEBYTECODE = 1
PYTHONPYCACHEPREFIX = .tmp/pycache
```

No unified baseline policy or full-test risk manifest exists yet.

## Goals

1. Make the full test surface observable before treating it as a single
   pass/fail command.
2. Split test execution into explicit layers with different expected cost,
   dependencies, and failure interpretation.
3. Detect slow and high-risk tests before running them in unbounded full
   sweeps.
4. Prevent accidental network/download paths from entering the default local
   baseline.
5. Produce structured JSON and Markdown evidence that can explain what was
   collected, classified, run, skipped, and why.
6. Keep the first implementation small: policy plus audit runner plus focused
   runner tests, not a full custom pytest replacement.

## Non-Goals

- Do not immediately force all `runtime_neutral` and `integration` tests to run
  as one unbounded command.
- Do not fix every possible current or future test failure in this pass.
- Do not introduce real network tests into the local baseline.
- Do not install or deploy to Codex or any host root.
- Do not write to the local Codex root.
- Do not change routing, runtime, installer, or host behavior.
- Do not commit generated `outputs/verify` artifacts.
- Do not remove existing tests or hide failures with broad skips.

## Design

### 1. Baseline Layers

The baseline should classify tests into at least four layers.

#### `contract_unit`

Purpose: fastest deterministic core checks.

Default command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\contract tests\unit -q
```

Expected interpretation:

- Failure usually indicates code regression or broken local Python setup.
- This layer should remain part of every implementation regression.

#### `runtime_neutral_fast`

Purpose: runtime-neutral tests that should not install hosts, call external
network paths, trigger large downloads, or run long materialization flows.

Default behavior:

- Use collect-only and policy classification first.
- Run only files not tagged as heavy, host-boundary, external, or unsafe.
- Report excluded files and reasons.

Expected interpretation:

- Failure usually indicates repo behavior regression.
- Missing PowerShell/Bash should not normally affect this layer unless a test is
  misclassified.

#### `runtime_neutral_heavy`

Purpose: runtime-neutral but expensive tests, especially install/profile,
installed runtime, canonical-entry simulation, shell bridge, and materialization
paths.

Default behavior:

- Run separately from fast tests.
- Use longer command timeout than fast baseline.
- Always emit durations with `--durations`.
- Keep per-file and per-test timing in the audit artifact.

Expected interpretation:

- Failure may indicate code regression, host shell drift, missing local tools, or
  slow-test timeout. The report must preserve this classification rather than
  collapsing it into one generic failure.

#### `integration_host_boundary`

Purpose: integration tests around PowerShell, host wrapper behavior, canonical
entry truth, host capability matrices, and command argument boundaries.

Default behavior:

- Collect and classify by default.
- Run only when required host dependencies are available or when the caller
  explicitly asks to run the layer.
- Preserve skip reasons such as missing `pwsh`.

Expected interpretation:

- Failure may be a real integration regression or an environment prerequisite
  problem. The baseline artifact should state which.

### 2. Baseline Policy

Add a policy file:

```text
config/test-baseline-policy.json
```

The policy should define:

- layer names and descriptions;
- default pytest path arguments for each layer;
- default timeout guidance for each layer;
- whether external network is allowed;
- dependency hints such as `powershell`, `pwsh`, `bash`, or `git`;
- file-pattern or test-name rules for heavy/runtime/install groups;
- risk keyword patterns for static scanning.

The policy should start conservative. For example:

- `contract_unit` points to `tests/contract` and `tests/unit`;
- known heavy patterns include `installed_runtime`, `install_profile`,
  `install_generated_nested`, `generated_nested_bundled`,
  `l_xl_native_execution_topology`, `runtime_delivery_acceptance`, and
  `workspace_shared_memory_plane`;
- network/download risk patterns include `curl`, `Invoke-WebRequest`,
  `requests.`, `download`, `ISO`, `eval-iso`, and raw `http://` or `https://`
  references in executable test code.

The policy should not be used to skip failures silently. It is a classification
contract and runner input.

### 3. Baseline Audit Runner

Add a small runner:

```text
scripts/verify/test-baseline-audit.py
```

Responsibilities:

1. Load `config/test-baseline-policy.json`.
2. Run pytest collect-only for configured test roots.
3. Parse collected test node ids.
4. Scan test files for configured risk keywords.
5. Classify files and node ids into baseline layers.
6. Optionally run one requested layer with pytest.
7. Emit structured JSON and Markdown reports under `outputs/verify/` when
   `--write-artifacts` is provided.

The first version should avoid becoming a custom test framework:

- no custom parallel scheduler;
- no automatic mutation of pytest configuration;
- no dependency installation;
- no broad rerun logic;
- no generated artifact committed to git.

Suggested command shapes:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python scripts\verify\test-baseline-audit.py --collect-only --write-artifacts
```

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python scripts\verify\test-baseline-audit.py --run-layer contract_unit --write-artifacts
```

The JSON report should include at least:

- generated timestamp;
- repo root;
- policy path;
- collection commands;
- total collected node count per test root;
- layer summaries;
- risk summaries;
- skipped or excluded reason summaries;
- run command and exit code for any executed layer.

The Markdown report should summarize the same information for human review.

### 4. Safety Rules For Network And Long Tasks

The default baseline must be deny-by-default for external network and long
download paths.

Rules:

- The runner should set a local environment flag for executed layers, such as
  `VIBESKILLS_TEST_DISABLE_NETWORK=1`, so tests can opt into respecting the
  baseline boundary.
- Tests with network/download risk tags should not enter `runtime_neutral_fast`.
- Any test that needs real external network must be explicitly classified as
  external and excluded from the default local baseline.
- Tests that assert "reject before network" behavior can remain in local
  baseline only if their focused regression proves the rejection occurs before
  network work.

This design intentionally avoids running full `tests/runtime_neutral` before
those classifications exist.

### 5. Runner Tests

Add focused tests:

```text
tests/runtime_neutral/test_test_baseline_audit.py
```

The tests should cover:

- the policy file can be loaded;
- collect-only output parsing extracts pytest node ids;
- static risk scanning tags files with configured keywords;
- policy file-pattern matching assigns known heavy files to
  `runtime_neutral_heavy`;
- default collection mode does not execute tests;
- `--run-layer contract_unit` builds the expected pytest command;
- JSON and Markdown artifact rendering includes totals, layer summary, risk
  summary, and command evidence.

The tests should mock subprocess execution for runner unit behavior where
possible. They should not execute the entire repository test suite.

## Validation Strategy

Focused runner tests:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Collect-only audit:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python scripts\verify\test-baseline-audit.py --collect-only --write-artifacts
```

Contract/unit layer through the runner:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python scripts\verify\test-baseline-audit.py --run-layer contract_unit --write-artifacts
```

Existing stable regression:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\contract tests\unit -q
```

Routing and terminology guardrails should remain green:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
```

Do not claim the full `tests/runtime_neutral tests/integration` suite is
passing unless it is explicitly run after the baseline runner exists and
finishes successfully.

## Risks And Mitigations

Risk: the baseline policy becomes a way to hide failures.

Mitigation: the report must show every collected test, its layer, and exclusion
reason. Policy classification is visible evidence, not a silent skip.

Risk: the runner becomes a complex pytest wrapper.

Mitigation: keep the first version small. Use pytest commands directly, classify
outputs, and write artifacts. Do not add parallel scheduling or automatic
reruns.

Risk: static keyword scanning produces false positives.

Mitigation: false positives are acceptable in the first pass because they only
move tests out of the fast layer. Later work can narrow policy rules using
evidence.

Risk: network-deny behavior is only partially enforced.

Mitigation: the first version sets the environment boundary and excludes risky
tests from the default baseline. It does not claim to sandbox all possible
network access.

Risk: full baseline remains slow.

Mitigation: the first deliverable makes slow tests measurable with durations and
layer summaries. Performance tuning can be a later spec after evidence exists.

## Completion Criteria

- A committed design, plan, and implementation define the baseline layers.
- `config/test-baseline-policy.json` exists and is covered by tests.
- `scripts/verify/test-baseline-audit.py` can collect and classify the current
  `runtime_neutral` and `integration` surfaces.
- Runner tests pass.
- `--run-layer contract_unit` successfully executes and records the existing
  contract/unit baseline.
- Generated reports are written under `outputs/verify/` only when requested and
  are not committed.
- No install, deploy, push, host-root mutation, routing change, or runtime
  behavior change is made in this pass.
