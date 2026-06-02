# Rabbit Follow-Up Three Comments Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the three currently unresolved CodeRabbit inline comments on PR 228 with narrow tests, minimal behavior changes, and fresh PR verification.

**Architecture:** This patch changes one Markdown plan heading, two runtime delivery loader predicates, and the CLI boundary of the test baseline audit wrapper. Tests are added at the existing unittest surfaces that already cover runtime delivery acceptance and baseline audit CLI behavior.

**Tech Stack:** Markdown, Python 3.10, unittest, pytest, GitHub CLI, ripgrep.

---

## File Structure

- Modify: `docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md`
  - Adds the missing `## Tasks` heading above existing task headings.
- Modify: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`
  - Treats empty manifest/accounting lock payloads as absent before fallback.
- Modify: `tests/runtime_neutral/test_runtime_delivery_acceptance.py`
  - Adds focused regression tests for empty lock and resolution fallback.
- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
  - Normalizes expected CLI failures into concise stderr and deterministic exit codes.
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`
  - Adds focused CLI boundary tests for policy and runtime collection failures.

## Tasks

### Task 1: Add Regression Tests For Runtime Lock Fallback

**Files:**
- Modify: `tests/runtime_neutral/test_runtime_delivery_acceptance.py`

- [ ] **Step 1: Add the failing tests**

Add these tests near the existing locked-specialist tests, after
`test_runtime_delivery_acceptance_fails_when_locked_specialist_is_unresolved`:

```python
    def test_runtime_delivery_acceptance_uses_runtime_packet_lock_when_manifest_locks_are_empty(self) -> None:
        skill_path = "/tmp/scientific-reporting/SKILL.md"
        session_root = self._build_session(
            run_id="pytest-empty-manifest-lock-fallback",
            approved_dispatch=[
                {
                    "skill_id": "scientific-reporting",
                    "native_skill_entrypoint": skill_path,
                }
            ],
            phase_execute_specialist_user_disclosure={
                "scope": "selected_skill_execution_only",
                "timing": "before_execution",
                "path_source": "native_skill_entrypoint",
                "routed_skills": [
                    {
                        "skill_id": "scientific-reporting",
                        "native_skill_entrypoint": skill_path,
                        "entrypoint_requirement_satisfied": True,
                    }
                ],
            },
            specialist_accounting={
                "skill_execution_lock": {},
                "selected_skill_execution": [
                    {
                        "skill_id": "scientific-reporting",
                        "native_skill_entrypoint": skill_path,
                    }
                ],
                "selected_skill_execution_count": 1,
                "effective_execution_status": "direct_current_session_routed",
                "direct_routed_skill_execution_units": [
                    {
                        "unit_id": "unit-1",
                        "skill_id": "scientific-reporting",
                        "result_path": "specialist-results/scientific-reporting.json",
                    }
                ],
            },
            skill_execution_lock={
                "schema_version": "v1",
                "state": "active",
                "locked_skill_ids": ["scientific-reporting"],
                "locked_dispatch": [
                    {
                        "skill_id": "scientific-reporting",
                        "native_skill_entrypoint": skill_path,
                    }
                ],
                "resolution_required": True,
            },
            specialist_lock_resolution={},
            phase_execute_specialist_decision={
                "decision_state": "approved_dispatch",
                "resolution_mode": "approved_dispatch",
                "approved_dispatch_skill_ids": ["scientific-reporting"],
            },
        )
        manifest_path = session_root / "execution-manifest.json"
        manifest_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_payload["skill_execution_lock"] = {}
        write_json(manifest_path, manifest_payload)

        report = evaluate(REPO_ROOT, session_root)

        self.assertEqual("FAIL", report["summary"]["gate_result"])
        self.assertEqual("failing", report["truth_results"]["specialist_lock_resolution_truth"]["state"])
        self.assertIn("scientific-reporting", report["execution_context"]["specialist_lock_unresolved_skill_ids"])

    def test_runtime_delivery_acceptance_uses_accounting_lock_resolution_when_manifest_resolution_is_empty(self) -> None:
        skill_path = "/tmp/scientific-reporting/SKILL.md"
        session_root = self._build_session(
            run_id="pytest-empty-manifest-resolution-fallback",
            approved_dispatch=[
                {
                    "skill_id": "scientific-reporting",
                    "native_skill_entrypoint": skill_path,
                }
            ],
            phase_execute_specialist_user_disclosure={
                "scope": "selected_skill_execution_only",
                "timing": "before_execution",
                "path_source": "native_skill_entrypoint",
                "routed_skills": [
                    {
                        "skill_id": "scientific-reporting",
                        "native_skill_entrypoint": skill_path,
                        "entrypoint_requirement_satisfied": True,
                    }
                ],
            },
            specialist_accounting={
                "specialist_lock_resolution": {
                    "active": True,
                    "locked_skill_ids": ["scientific-reporting"],
                    "executed_skill_ids": ["scientific-reporting"],
                    "not_applicable_skill_ids": [],
                    "deferred_skill_ids": [],
                    "failed_skill_ids": [],
                    "unresolved_skill_ids": [],
                    "delivery_blocking": False,
                },
                "selected_skill_execution": [
                    {
                        "skill_id": "scientific-reporting",
                        "native_skill_entrypoint": skill_path,
                    }
                ],
                "selected_skill_execution_count": 1,
                "effective_execution_status": "direct_current_session_routed",
                "direct_routed_skill_execution_units": [
                    {
                        "unit_id": "unit-1",
                        "skill_id": "scientific-reporting",
                        "result_path": "specialist-results/scientific-reporting.json",
                    }
                ],
            },
            skill_execution_lock={
                "schema_version": "v1",
                "state": "active",
                "locked_skill_ids": ["scientific-reporting"],
                "locked_dispatch": [
                    {
                        "skill_id": "scientific-reporting",
                        "native_skill_entrypoint": skill_path,
                    }
                ],
                "resolution_required": True,
            },
            specialist_lock_resolution={},
            phase_execute_specialist_decision={
                "decision_state": "approved_dispatch",
                "resolution_mode": "approved_dispatch",
                "approved_dispatch_skill_ids": ["scientific-reporting"],
            },
            sidecar_specialist_execution={
                "protocol_version": "v1",
                "source_run_id": "pytest-empty-manifest-resolution-fallback",
                "resolution_mode": "current_session_host_execution",
                "evidence_paths": ["/tmp/pytest-specialist-lock-pass.md"],
                "units": [
                    {
                        "unit_id": "unit-1",
                        "skill_id": "scientific-reporting",
                        "resolution_state": "executed",
                        "native_skill_entrypoint": skill_path,
                        "evidence_paths": ["/tmp/pytest-scientific-reporting.txt"],
                    }
                ],
            },
        )

        report = evaluate(REPO_ROOT, session_root)

        self.assertEqual("PASS", report["summary"]["gate_result"])
        self.assertEqual("passing", report["truth_results"]["specialist_lock_resolution_truth"]["state"])
        self.assertEqual([], report["execution_context"]["specialist_lock_unresolved_skill_ids"])
```

- [ ] **Step 2: Run the new tests and verify they fail before implementation**

Run:

```powershell
pytest tests/runtime_neutral/test_runtime_delivery_acceptance.py::RuntimeDeliveryAcceptanceTests::test_runtime_delivery_acceptance_uses_runtime_packet_lock_when_manifest_locks_are_empty tests/runtime_neutral/test_runtime_delivery_acceptance.py::RuntimeDeliveryAcceptanceTests::test_runtime_delivery_acceptance_uses_accounting_lock_resolution_when_manifest_resolution_is_empty -q
```

Expected before implementation: at least one test fails because empty `{}` payloads short-circuit fallback.

### Task 2: Implement Runtime Lock Fallback

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py:188-215`
- Test: `tests/runtime_neutral/test_runtime_delivery_acceptance.py`

- [ ] **Step 1: Update loader predicates**

Change the loader return predicates to require non-empty dictionaries:

```python
def _load_skill_execution_lock(
    runtime_packet: dict[str, Any],
    execution_manifest: dict[str, Any],
) -> dict[str, Any]:
    manifest_lock = execution_manifest.get("skill_execution_lock")
    if isinstance(manifest_lock, dict) and manifest_lock:
        return manifest_lock
    accounting = execution_manifest.get("specialist_accounting")
    if isinstance(accounting, dict):
        accounting_lock = accounting.get("skill_execution_lock")
        if isinstance(accounting_lock, dict) and accounting_lock:
            return accounting_lock
    packet_lock = runtime_packet.get("skill_execution_lock")
    if isinstance(packet_lock, dict) and packet_lock:
        return packet_lock
    return {}


def _load_specialist_lock_resolution(execution_manifest: dict[str, Any]) -> dict[str, Any]:
    manifest_resolution = execution_manifest.get("specialist_lock_resolution")
    if isinstance(manifest_resolution, dict) and manifest_resolution:
        return manifest_resolution
    accounting = execution_manifest.get("specialist_accounting")
    if isinstance(accounting, dict):
        accounting_resolution = accounting.get("specialist_lock_resolution")
        if isinstance(accounting_resolution, dict) and accounting_resolution:
            return accounting_resolution
    return {}
```

- [ ] **Step 2: Run the focused runtime tests**

Run:

```powershell
pytest tests/runtime_neutral/test_runtime_delivery_acceptance.py::RuntimeDeliveryAcceptanceTests::test_runtime_delivery_acceptance_uses_runtime_packet_lock_when_manifest_locks_are_empty tests/runtime_neutral/test_runtime_delivery_acceptance.py::RuntimeDeliveryAcceptanceTests::test_runtime_delivery_acceptance_uses_accounting_lock_resolution_when_manifest_resolution_is_empty -q
```

Expected after implementation: both tests pass.

### Task 3: Add Regression Tests For Test Baseline Audit CLI Errors

**Files:**
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`

- [ ] **Step 1: Add the failing CLI tests**

Add these tests inside `TestBaselineAuditCliTests`, before
`test_script_entrypoint_runs_collect_only`:

```python
    def test_main_reports_missing_policy_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            missing_policy = Path(tempdir) / "missing-policy.json"
            stderr = tempfile.TemporaryFile(mode="w+", encoding="utf-8")
            try:
                original_stderr = sys.stderr
                sys.stderr = stderr
                exit_code = audit.main(["--policy", str(missing_policy), "--collect-only"], runner=FakeRunner())
            finally:
                sys.stderr = original_stderr
            stderr.seek(0)
            message = stderr.read()
            stderr.close()

        self.assertEqual(2, exit_code)
        self.assertIn("[ERROR]", message)
        self.assertIn("missing-policy.json", message)
        self.assertNotIn("Traceback", message)

    def test_main_reports_collection_failure_without_traceback(self) -> None:
        class FailingCollectRunner(FakeRunner):
            def __call__(self, command: list[str], **kwargs: object) -> FakeCompletedProcess:
                self.calls.append({"command": command, "kwargs": kwargs})
                return FakeCompletedProcess(command, returncode=2, stdout="", stderr="collection failed")

        stderr = tempfile.TemporaryFile(mode="w+", encoding="utf-8")
        try:
            original_stderr = sys.stderr
            sys.stderr = stderr
            exit_code = audit.main(["--collect-only"], runner=FailingCollectRunner())
        finally:
            sys.stderr = original_stderr
        stderr.seek(0)
        message = stderr.read()
        stderr.close()

        self.assertEqual(1, exit_code)
        self.assertIn("[ERROR]", message)
        self.assertIn("pytest collection failed", message)
        self.assertNotIn("Traceback", message)
```

- [ ] **Step 2: Run the new CLI tests and verify they fail before implementation**

Run:

```powershell
pytest tests/runtime_neutral/test_test_baseline_audit.py::TestBaselineAuditCliTests::test_main_reports_missing_policy_without_traceback tests/runtime_neutral/test_test_baseline_audit.py::TestBaselineAuditCliTests::test_main_reports_collection_failure_without_traceback -q
```

Expected before implementation: the tests fail because `main()` raises the underlying expected errors.

### Task 4: Implement Test Baseline Audit CLI Error Handling

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py:640-677`
- Test: `tests/runtime_neutral/test_test_baseline_audit.py`

- [ ] **Step 1: Add stable error-code constants and helper**

Add these constants near `PolicyError`:

```python
CONFIG_ERROR_EXIT_CODE = 2
RUNTIME_ERROR_EXIT_CODE = 1
```

Add this helper before `main()`:

```python
def _print_cli_error(message: str) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
```

- [ ] **Step 2: Wrap main operational logic**

Replace `main()` with:

```python
def main(argv: list[str] | None = None, runner=subprocess.run) -> int:
    try:
        args = parse_args(argv or sys.argv[1:])
        repo_root = resolve_repo_root(Path(__file__))
        policy_path = (repo_root / args.policy).resolve()
        policy = load_policy(policy_path)
        collected_nodes, collection_results = run_collect_commands(repo_root, policy, runner=runner)
        run_result = None
        if args.run_layer and not args.collect_only:
            def print_progress(message: str) -> None:
                print(message, flush=True)

            run_result = run_layer(
                repo_root,
                policy,
                args.run_layer,
                collected_nodes=collected_nodes,
                runner=runner,
                progress=print_progress,
            )
        artifact = build_artifact(
            repo_root=repo_root,
            policy_path=policy_path,
            policy=policy,
            collected_nodes=collected_nodes,
            collection_results=collection_results,
            run_result=run_result,
        )
        if args.write_artifacts:
            write_artifacts(repo_root, artifact, args.output_directory, policy=policy)
        print(
            f"[INFO] total_nodes={artifact['summary']['total_nodes']} "
            f"layers={artifact['summary']['layer_count']} "
            f"risks={artifact['summary']['risk_tag_count']}"
        )
        if run_result is not None:
            print(f"[INFO] run_layer={run_result['layer_id']} exit_code={run_result['exit_code']}")
            return int(run_result["exit_code"])
        return 0
    except (PolicyError, json.JSONDecodeError) as exc:
        _print_cli_error(str(exc))
        return CONFIG_ERROR_EXIT_CODE
    except (RuntimeError, OSError) as exc:
        _print_cli_error(str(exc))
        return RUNTIME_ERROR_EXIT_CODE
```

- [ ] **Step 3: Run the focused CLI tests**

Run:

```powershell
pytest tests/runtime_neutral/test_test_baseline_audit.py::TestBaselineAuditCliTests::test_main_reports_missing_policy_without_traceback tests/runtime_neutral/test_test_baseline_audit.py::TestBaselineAuditCliTests::test_main_reports_collection_failure_without_traceback -q
```

Expected after implementation: both tests pass.

### Task 5: Fix Markdown Heading Increment

**Files:**
- Modify: `docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md:13`

- [ ] **Step 1: Insert the missing second-level heading**

Change:

```markdown
---

### Task 1: Fix Follow-Up Plan Checklist Wording
```

to:

```markdown
---

## Tasks

### Task 1: Fix Follow-Up Plan Checklist Wording
```

- [ ] **Step 2: Verify heading order**

Run:

```powershell
Select-String -LiteralPath 'docs\superpowers\plans\2026-05-06-rabbit-followup-two-comments.md' -Pattern '^#+' | ForEach-Object { "$($_.LineNumber):$($_.Line)" }
```

Expected: headings begin with `# Rabbit Follow-Up Two Comments Implementation Plan`, then `## Tasks`, then `### Task 1`.

### Task 6: Run Full Targeted Validation And Commit

**Files:**
- Check: `docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md`
- Check: `packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py`
- Check: `tests/runtime_neutral/test_runtime_delivery_acceptance.py`
- Check: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
- Check: `tests/runtime_neutral/test_test_baseline_audit.py`
- Check: `docs/superpowers/specs/2026-05-06-rabbit-followup-three-comments-design.md`
- Check: `docs/superpowers/plans/2026-05-06-rabbit-followup-three-comments.md`

- [ ] **Step 1: Run runtime delivery acceptance tests**

Run:

```powershell
pytest tests/runtime_neutral/test_runtime_delivery_acceptance.py packages/verification-core/src/vgo_verify/test_runtime_delivery_acceptance_lock_reconciliation.py -q
```

Expected: all selected runtime delivery tests pass.

- [ ] **Step 2: Run test baseline audit tests**

Run:

```powershell
pytest tests/runtime_neutral/test_test_baseline_audit.py -q
```

Expected: all test baseline audit tests pass.

- [ ] **Step 3: Run whitespace validation**

Run:

```powershell
git diff --check
```

Expected: no output and exit code `0`.

- [ ] **Step 4: Commit the implementation**

Run:

```powershell
git status --short
git add -- docs/superpowers/plans/2026-05-06-rabbit-followup-two-comments.md packages/verification-core/src/vgo_verify/runtime_delivery_acceptance_runtime.py tests/runtime_neutral/test_runtime_delivery_acceptance.py packages/verification-core/src/vgo_verify/test_baseline_audit.py tests/runtime_neutral/test_test_baseline_audit.py docs/superpowers/plans/2026-05-06-rabbit-followup-three-comments.md
git commit -m "fix: resolve rabbit three-comment followup"
```

Expected: one implementation commit is created.

### Task 7: Update PR Branch And Verify GitHub State

**Files:**
- No direct file edits.

- [ ] **Step 1: Attempt normal push**

Run:

```powershell
git push origin HEAD:review/pr226-pr227-combined
```

Expected: branch updates successfully. If HTTPS push fails with the known GitHub connection reset, use the GitHub Git Database API update path and then compare remote and local tree hashes.

- [ ] **Step 2: Verify remote/local tree equality**

Run:

```powershell
$remoteCommit = gh api repos/foryourhealth111-pixel/Vibe-Skills/git/ref/heads/review/pr226-pr227-combined --jq .object.sha
$remoteTree = gh api repos/foryourhealth111-pixel/Vibe-Skills/git/commits/$remoteCommit --jq .tree.sha
$localTree = git show -s --format=%T HEAD
[pscustomobject]@{
  remote_commit = $remoteCommit
  remote_tree = $remoteTree
  local_head = (git rev-parse HEAD)
  local_tree = $localTree
  tree_matches = ($remoteTree -eq $localTree)
} | Format-List
```

Expected: `tree_matches` is `True`.

- [ ] **Step 3: Verify unresolved review threads**

Run:

```powershell
$json = gh api graphql -f query='query($owner:String!, $repo:String!, $number:Int!) { repository(owner:$owner, name:$repo) { pullRequest(number:$number) { headRefOid mergeStateStatus reviewThreads(first: 100) { nodes { isResolved isOutdated path line } } } } }' -f owner='foryourhealth111-pixel' -f repo='Vibe-Skills' -F number=228 | ConvertFrom-Json
$pr = $json.data.repository.pullRequest
$threads = @($pr.reviewThreads.nodes)
$unresolved = @($threads | Where-Object { -not $_.isResolved })
[pscustomobject]@{
  headRefOid = $pr.headRefOid
  mergeStateStatus = $pr.mergeStateStatus
  total_threads = $threads.Count
  unresolved_threads = $unresolved.Count
  unresolved_paths = (@($unresolved | ForEach-Object { $_.path }) -join ', ')
} | Format-List
```

Expected after CodeRabbit processes the update: unresolved thread count is `0`.

- [ ] **Step 4: Verify PR checks**

Run:

```powershell
gh pr checks 228 --repo foryourhealth111-pixel/Vibe-Skills
```

Expected: CodeRabbit, gates, and python-validation pass.
