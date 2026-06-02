# Install Prompt MCP Auto-Provision Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a shared, non-blocking MCP auto-provision contract so install guidance, bootstrap wrappers, and doctor/reporting all attempt the same five MCP surfaces across all six public hosts and only summarize failures in the final install report.

**Architecture:** Introduce one registry-driven MCP auto-provision layer that defines required servers, host-specific attempt order, strategy preference, verification path, and final-report status vocabulary. Wire that layer into `vgo_cli` install postconditions first, persist a machine-readable receipt under the target root, then teach bootstrap doctor and prompt/docs surfaces to read and describe the same contract rather than each inventing their own wording.

**Tech Stack:** Python 3.10+ `vgo_cli`, runtime-neutral `pytest`/`unittest`, Bash and PowerShell bootstrap wrappers, Markdown install prompts and install-path docs, existing adapter registry and bootstrap doctor gates

---

## File Structure

### Prompt and install guidance contract
- Modify: `docs/install/prompts/full-version-install.md`
  Responsibility: require the assistant to attempt `github`, `context7`, `serena`, `scrapling`, and `claude-flow`, keep failures out of the mid-flow transcript, and require final-report-only disclosure.
- Modify: `docs/install/prompts/full-version-install.en.md`
  Responsibility: English parity for the same install-assistant contract.
- Modify: `docs/install/prompts/framework-only-install.md`
  Responsibility: carry the same MCP auto-provision rules for the `minimal` profile wording.
- Modify: `docs/install/prompts/framework-only-install.en.md`
  Responsibility: English parity for framework-only install wording.
- Modify: `docs/install/prompts/full-version-update.md`
  Responsibility: keep update guidance aligned with install guidance so reinstall/update does not regress the MCP attempt contract.
- Modify: `docs/install/prompts/full-version-update.en.md`
  Responsibility: English parity for full-version update wording.
- Modify: `docs/install/prompts/framework-only-update.md`
  Responsibility: keep framework-only update guidance aligned with the same MCP attempt contract.
- Modify: `docs/install/prompts/framework-only-update.en.md`
  Responsibility: English parity for framework-only update wording.
- Modify: `docs/install/recommended-full-path.md`
  Responsibility: explain that all hosts attempt the same five MCP surfaces, but local install success remains separate from MCP readiness and online-ready state.
- Modify: `docs/install/recommended-full-path.en.md`
  Responsibility: English parity for the recommended full-path explanation.
- Modify: `docs/one-shot-setup.md`
  Responsibility: document that one-shot now attempts the five MCP surfaces and reports readiness at the end without blocking base install.

### Shared MCP provision contract and install receipts
- Create: `config/mcp-auto-provision.registry.json`
  Responsibility: define the five required MCP surfaces, categories, host-specific attempt order, preferred strategy (`host_native` or `scripted_cli`), verification mode, and allowed status values.
- Create: `apps/vgo-cli/src/vgo_cli/mcp_provision.py`
  Responsibility: load the registry, execute host-specific attempt/verify steps, normalize results into the approved status vocabulary, and write a target-root receipt.
- Modify: `apps/vgo-cli/src/vgo_cli/external.py`
  Responsibility: shrink existing Codex-only external install helpers into command-level utilities that the new orchestrator can reuse for `scrapling` and `claude-flow`.
- Modify: `apps/vgo-cli/src/vgo_cli/install_support.py`
  Responsibility: run MCP auto-provision after core install, persist the final receipt, and keep strict-offline / postcondition behavior coherent.
- Modify: `apps/vgo-cli/src/vgo_cli/commands.py`
  Responsibility: pass host, profile, and target-root context into the new orchestrator and keep `install_external` semantics aligned for all hosts.
- Modify: `apps/vgo-cli/src/vgo_cli/output.py`
  Responsibility: print one concise final install report that separates `installed_locally`, `mcp_auto_provision_attempted`, per-MCP readiness, and online-ready follow-up.

### Bootstrap and doctor/reporting parity
- Modify: `scripts/bootstrap/one-shot-setup.sh`
  Responsibility: keep wrapper stage text compatible with the new MCP auto-provision flow and point final users to the unified end-of-install report instead of ad hoc warnings.
- Modify: `scripts/bootstrap/one-shot-setup.ps1`
  Responsibility: PowerShell parity for the same wrapper/reporting expectations.
- Modify: `packages/verification-core/src/vgo_verify/bootstrap_doctor.py`
  Responsibility: load the new target-root MCP receipt and include it in the generated artifact.
- Modify: `packages/verification-core/src/vgo_verify/bootstrap_doctor_runtime.py`
  Responsibility: evaluate the new MCP result vocabulary and preserve separation between local install completeness, MCP readiness, and online-governance readiness.
- Modify: `scripts/verify/vibe-bootstrap-doctor-gate.ps1`
  Responsibility: PowerShell gate parity for the new MCP receipt and state model.
- Modify: `mcp/servers.template.json`
  Responsibility: keep server metadata aligned with the new registry where the two surfaces overlap on server names, mode, and CLI expectations.

### Tests
- Create: `tests/runtime_neutral/test_mcp_auto_provision.py`
  Responsibility: cover registry shape, host-specific attempt order, non-blocking failure behavior, and final-report-only disclosure semantics.
- Create: `tests/runtime_neutral/test_install_prompt_mcp_contract.py`
  Responsibility: lock the install/update prompt docs to the approved host list, five required MCP surfaces, final-report-only disclosure rule, and key-name guidance.
- Modify: `tests/runtime_neutral/test_bootstrap_doctor.py`
  Responsibility: assert bootstrap doctor reads the MCP receipt and reports the new readiness separation correctly.
- Modify: `tests/runtime_neutral/test_shell_entrypoint_compatibility.py`
  Responsibility: keep wrapper syntax coverage after one-shot shell wording changes.

## Chunk 1: Shared MCP Contract And Receipt Model

### Task 1: Add the registry-backed MCP auto-provision contract

**Files:**
- Create: `config/mcp-auto-provision.registry.json`
- Create: `tests/runtime_neutral/test_mcp_auto_provision.py`

- [ ] **Step 1: Write the failing registry contract tests**

```python
class McpAutoProvisionContractTests(unittest.TestCase):
    def test_registry_declares_required_surfaces_for_all_public_hosts(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8-sig"))
        self.assertEqual(
            ["github", "context7", "serena", "scrapling", "claude-flow"],
            registry["required_servers"],
        )
        self.assertEqual(
            ["claude-code", "codex", "cursor", "openclaw", "opencode", "windsurf"],
            sorted(registry["hosts"].keys()),
        )

    def test_registry_declares_status_vocabulary_approved_in_spec(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8-sig"))
        self.assertEqual(
            [
                "ready",
                "attempt_failed",
                "host_native_unavailable",
                "missing_credentials",
                "verification_failed",
                "not_attempted_due_to_host_contract",
            ],
            registry["allowed_statuses"],
        )
```

- [ ] **Step 2: Run the targeted registry test and confirm failure**

Run: `python3 -m pytest tests/runtime_neutral/test_mcp_auto_provision.py -k "registry_declares" -v`

Expected: `FAIL` because `config/mcp-auto-provision.registry.json` does not exist yet.

- [ ] **Step 3: Add the minimal registry**

```json
{
  "schema_version": 1,
  "required_servers": ["github", "context7", "serena", "scrapling", "claude-flow"],
  "allowed_statuses": [
    "ready",
    "attempt_failed",
    "host_native_unavailable",
    "missing_credentials",
    "verification_failed",
    "not_attempted_due_to_host_contract"
  ],
  "hosts": {
    "codex": {
      "attempt_order": ["github", "context7", "serena", "scrapling", "claude-flow"]
    }
  }
}
```

- [ ] **Step 4: Re-run the targeted registry test**

Run: `python3 -m pytest tests/runtime_neutral/test_mcp_auto_provision.py -k "registry_declares" -v`

Expected: `PASS`

- [ ] **Step 5: Commit**

```bash
git add config/mcp-auto-provision.registry.json tests/runtime_neutral/test_mcp_auto_provision.py
git commit -m "feat: add mcp auto provision registry contract"
```

### Task 2: Implement the shared receipt model and orchestration surface

**Files:**
- Create: `apps/vgo-cli/src/vgo_cli/mcp_provision.py`
- Modify: `apps/vgo-cli/src/vgo_cli/external.py`
- Modify: `tests/runtime_neutral/test_mcp_auto_provision.py`

- [ ] **Step 1: Add the failing orchestration test**

```python
class McpAutoProvisionContractTests(unittest.TestCase):
    def test_attempt_failures_are_captured_without_blocking_install(self) -> None:
        report = provision_required_mcp(
            repo_root=REPO_ROOT,
            target_root=self.target_root,
            host_id="cursor",
            profile="full",
            allow_scripted_install=True,
            executor=FakeExecutor(
                results={
                    ("host_native", "github"): ProvisionResult(status="host_native_unavailable"),
                    ("scripted_cli", "scrapling"): ProvisionResult(status="attempt_failed", failure_reason="pip missing"),
                }
            ),
        )
        self.assertTrue(report["mcp_auto_provision_attempted"])
        self.assertEqual("installed_locally", report["install_state"])
        self.assertEqual("host_native_unavailable", lookup_server(report, "github")["status"])
        self.assertEqual("attempt_failed", lookup_server(report, "scrapling")["status"])
        self.assertEqual("final_report_only", lookup_server(report, "scrapling")["disclosure_mode"])
```

- [ ] **Step 2: Run the orchestration-focused tests and confirm failure**

Run: `python3 -m pytest tests/runtime_neutral/test_mcp_auto_provision.py -k "captured_without_blocking" -v`

Expected: `FAIL` because `provision_required_mcp` and the receipt model do not exist yet.

- [ ] **Step 3: Implement the orchestrator and reusable command helpers**

```python
def provision_required_mcp(
    *,
    repo_root: Path,
    target_root: Path,
    host_id: str,
    profile: str,
    allow_scripted_install: bool,
    executor: ProvisionExecutor | None = None,
) -> dict[str, object]:
    registry = load_registry(repo_root)
    host_contract = registry["hosts"][host_id]
    results = [
        attempt_server(
            repo_root=repo_root,
            target_root=target_root,
            host_id=host_id,
            server_name=server_name,
            contract=host_contract["servers"][server_name],
            allow_scripted_install=allow_scripted_install,
            executor=executor or ProvisionExecutor(),
        )
        for server_name in host_contract["attempt_order"]
    ]
    receipt = build_receipt(host_id=host_id, profile=profile, target_root=target_root, results=results)
    write_receipt(target_root, receipt)
    return receipt
```

- [ ] **Step 4: Run the focused orchestration tests**

Run: `python3 -m pytest tests/runtime_neutral/test_mcp_auto_provision.py -k "captured_without_blocking or registry_declares" -v`

Expected: `PASS`

- [ ] **Step 5: Commit**

```bash
git add apps/vgo-cli/src/vgo_cli/mcp_provision.py apps/vgo-cli/src/vgo_cli/external.py tests/runtime_neutral/test_mcp_auto_provision.py
git commit -m "feat: add shared mcp auto provision orchestrator"
```

## Chunk 2: Install CLI And Wrapper Integration

### Task 3: Wire MCP auto-provision into install postconditions and final reporting

**Files:**
- Modify: `apps/vgo-cli/src/vgo_cli/commands.py`
- Modify: `apps/vgo-cli/src/vgo_cli/install_support.py`
- Modify: `apps/vgo-cli/src/vgo_cli/output.py`
- Modify: `tests/runtime_neutral/test_mcp_auto_provision.py`

- [ ] **Step 1: Add the failing install-postcondition test**

```python
class McpAutoProvisionContractTests(unittest.TestCase):
    def test_reconcile_install_postconditions_emits_one_final_report(self) -> None:
        payload = run_install_postconditions_fixture(host_id="codex", profile="full")
        self.assertEqual("installed_locally", payload["install_state"])
        self.assertTrue(payload["mcp_auto_provision_attempted"])
        self.assertEqual(
            ["github", "context7", "serena", "scrapling", "claude-flow"],
            [item["name"] for item in payload["mcp_results"]],
        )
        self.assertNotIn("[WARN] github", payload["stdout"])
        self.assertIn("manual_follow_up", payload["stdout"])
```

- [ ] **Step 2: Run the focused install-postcondition test and confirm failure**

Run: `python3 -m pytest tests/runtime_neutral/test_mcp_auto_provision.py -k "one_final_report" -v`

Expected: `FAIL` because install postconditions do not yet invoke the orchestrator or render the final report.

- [ ] **Step 3: Implement install wiring and one final report renderer**

```python
receipt = provision_required_mcp(
    repo_root=repo_root,
    target_root=target_root,
    host_id=host_id,
    profile=profile,
    allow_scripted_install=install_external_enabled,
)
print_install_completion_report(
    host_id=host_id,
    profile=profile,
    target_root=target_root,
    install_receipt=refresh_install_ledger_payload(repo_root, target_root),
    mcp_receipt=receipt,
)
```

- [ ] **Step 4: Re-run the focused CLI/report tests**

Run: `python3 -m pytest tests/runtime_neutral/test_mcp_auto_provision.py -k "one_final_report or captured_without_blocking" -v`

Expected: `PASS`

- [ ] **Step 5: Commit**

```bash
git add apps/vgo-cli/src/vgo_cli/commands.py apps/vgo-cli/src/vgo_cli/install_support.py apps/vgo-cli/src/vgo_cli/output.py tests/runtime_neutral/test_mcp_auto_provision.py
git commit -m "feat: report mcp auto provision in install completion"
```

### Task 4: Keep one-shot wrappers aligned with the same report-only failure behavior

**Files:**
- Modify: `scripts/bootstrap/one-shot-setup.sh`
- Modify: `scripts/bootstrap/one-shot-setup.ps1`
- Modify: `tests/runtime_neutral/test_shell_entrypoint_compatibility.py`

- [ ] **Step 1: Add the failing wrapper-parity assertion**

```python
class ShellEntrypointCompatibilityTests(unittest.TestCase):
    def test_one_shot_wrappers_reference_final_mcp_report_instead_of_inline_failure_spam(self) -> None:
        for relpath in ("scripts/bootstrap/one-shot-setup.sh", "scripts/bootstrap/one-shot-setup.ps1"):
            content = (REPO_ROOT / relpath).read_text(encoding="utf-8")
            self.assertIn("MCP auto-provision summary", content)
            self.assertNotIn("continue on each MCP failure", content)
```

- [ ] **Step 2: Run the wrapper compatibility tests and confirm failure**

Run: `python3 -m pytest tests/runtime_neutral/test_shell_entrypoint_compatibility.py -k "one_shot_wrappers_reference_final_mcp_report" -v`

Expected: `FAIL` because wrapper text does not mention the new final-report contract yet.

- [ ] **Step 3: Update the shell and PowerShell one-shot wrapper messaging**

```powershell
Write-Host '[5/5] Running supported-path health check and preparing the MCP auto-provision summary...' -ForegroundColor Yellow
Write-Host '- MCP auto-provision summary is reported once at the end of install/check output.' -ForegroundColor DarkGray
```

```bash
echo '[5/5] Running supported-path health check and preparing the MCP auto-provision summary...'
echo '- MCP auto-provision summary is reported once at the end of install/check output.'
```

- [ ] **Step 4: Re-run shell compatibility coverage**

Run: `python3 -m pytest tests/runtime_neutral/test_shell_entrypoint_compatibility.py -k "install_entrypoints_are_bash_parseable or one_shot_wrappers_reference_final_mcp_report" -v`

Expected: `PASS`

- [ ] **Step 5: Commit**

```bash
git add scripts/bootstrap/one-shot-setup.sh scripts/bootstrap/one-shot-setup.ps1 tests/runtime_neutral/test_shell_entrypoint_compatibility.py
git commit -m "chore: align one-shot wrapper messaging with mcp report contract"
```

## Chunk 3: Bootstrap Doctor And Readiness Separation

### Task 5: Teach bootstrap doctor to read the MCP receipt and preserve truth separation

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/bootstrap_doctor.py`
- Modify: `packages/verification-core/src/vgo_verify/bootstrap_doctor_runtime.py`
- Modify: `scripts/verify/vibe-bootstrap-doctor-gate.ps1`
- Modify: `tests/runtime_neutral/test_bootstrap_doctor.py`
- Modify: `mcp/servers.template.json`

- [ ] **Step 1: Add the failing bootstrap doctor test**

```python
class BootstrapDoctorTests(unittest.TestCase):
    def test_mcp_receipt_keeps_install_and_mcp_readiness_separate(self) -> None:
        (self.target_root / ".vibeskills").mkdir(parents=True, exist_ok=True)
        (self.target_root / ".vibeskills" / "mcp-auto-provision.json").write_text(
            json.dumps(
                {
                    "install_state": "installed_locally",
                    "mcp_auto_provision_attempted": True,
                    "mcp_results": [
                        {"name": "github", "status": "host_native_unavailable", "next_step": "Register in host UI"},
                        {"name": "scrapling", "status": "ready", "next_step": "none"},
                    ],
                }
            )
            + "\n",
            encoding="utf-8",
        )

        artifact = self.module.evaluate(self.root, self.target_root)
        self.assertEqual("installed_locally", artifact["install_state"])
        self.assertTrue(artifact["mcp"]["auto_provision_attempted"])
        self.assertEqual("host_native_unavailable", artifact["mcp"]["servers"][0]["status"])
        self.assertEqual("manual_actions_pending", artifact["summary"]["readiness_state"])
```

- [ ] **Step 2: Run the bootstrap doctor tests and confirm failure**

Run: `python3 -m pytest tests/runtime_neutral/test_bootstrap_doctor.py -k "install_and_mcp_readiness_separate" -v`

Expected: `FAIL` because bootstrap doctor does not yet read the new receipt or expose `install_state`.

- [ ] **Step 3: Implement receipt loading and summary-state separation**

```python
def load_mcp_receipt(target_root: Path) -> dict[str, Any]:
    path = target_root / ".vibeskills" / "mcp-auto-provision.json"
    if not path.exists():
        return {"install_state": "unknown", "mcp_auto_provision_attempted": False, "mcp_results": []}
    return load_json(path)

summary = build_summary(
    settings_path=settings_path,
    active_mcp_path=active_mcp_path,
    settings=settings,
    install_state=mcp_receipt["install_state"],
    mcp_results=mcp_receipt["mcp_results"],
    ...
)
```

```powershell
$mcpReceiptPath = Join-Path $TargetRoot '.vibeskills\mcp-auto-provision.json'
$mcpReceipt = if (Test-Path -LiteralPath $mcpReceiptPath) {
    Get-Content -LiteralPath $mcpReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
} else {
    [pscustomobject]@{ install_state = 'unknown'; mcp_auto_provision_attempted = $false; mcp_results = @() }
}
```

- [ ] **Step 4: Re-run the bootstrap doctor coverage**

Run: `python3 -m pytest tests/runtime_neutral/test_bootstrap_doctor.py -v`

Expected: `PASS`

- [ ] **Step 5: Commit**

```bash
git add packages/verification-core/src/vgo_verify/bootstrap_doctor.py packages/verification-core/src/vgo_verify/bootstrap_doctor_runtime.py scripts/verify/vibe-bootstrap-doctor-gate.ps1 tests/runtime_neutral/test_bootstrap_doctor.py mcp/servers.template.json
git commit -m "feat: report mcp auto provision in bootstrap doctor"
```

## Chunk 4: Prompt Contract And User-Facing Docs

### Task 6: Lock the install prompt docs to the approved MCP auto-provision contract

**Files:**
- Create: `tests/runtime_neutral/test_install_prompt_mcp_contract.py`
- Modify: `docs/install/prompts/full-version-install.md`
- Modify: `docs/install/prompts/full-version-install.en.md`
- Modify: `docs/install/prompts/framework-only-install.md`
- Modify: `docs/install/prompts/framework-only-install.en.md`
- Modify: `docs/install/prompts/full-version-update.md`
- Modify: `docs/install/prompts/full-version-update.en.md`
- Modify: `docs/install/prompts/framework-only-update.md`
- Modify: `docs/install/prompts/framework-only-update.en.md`

- [ ] **Step 1: Write the failing prompt contract tests**

```python
class InstallPromptMcpContractTests(unittest.TestCase):
    def test_all_prompt_docs_require_the_same_five_mcp_surfaces(self) -> None:
        for path in PROMPT_FILES:
            text = path.read_text(encoding="utf-8-sig")
            for server_name in ("github", "context7", "serena", "scrapling", "claude-flow"):
                self.assertIn(server_name, text, path.name)
            self.assertIn("final install report", text.lower(), path.name)
            self.assertIn("installed locally", text.lower(), path.name)
            self.assertIn("online-ready", text.lower(), path.name)
```

- [ ] **Step 2: Run the prompt contract tests and confirm failure**

Run: `python3 -m pytest tests/runtime_neutral/test_install_prompt_mcp_contract.py -v`

Expected: `FAIL` because the prompt docs do not yet require MCP auto-provision or the final-report-only rule.

- [ ] **Step 3: Update all eight prompt docs**

```text
15. During installation guidance, you must attempt to provision these MCP surfaces for every supported host: `github`, `context7`, `serena`, `scrapling`, `claude-flow`.
16. Prefer host-native registration first for `github`, `context7`, and `serena`; prefer scripted CLI / stdio provisioning first for `scrapling` and `claude-flow`.
17. If any MCP attempt fails, do not interrupt the user repeatedly. Continue the install path and report the failure only in the final install report.
18. In the final report, separate `installed locally`, `mcp auto-provision attempted`, per-MCP readiness, and `online-ready`.
```

- [ ] **Step 4: Re-run the prompt contract tests**

Run: `python3 -m pytest tests/runtime_neutral/test_install_prompt_mcp_contract.py -v`

Expected: `PASS`

- [ ] **Step 5: Commit**

```bash
git add tests/runtime_neutral/test_install_prompt_mcp_contract.py docs/install/prompts/full-version-install.md docs/install/prompts/full-version-install.en.md docs/install/prompts/framework-only-install.md docs/install/prompts/framework-only-install.en.md docs/install/prompts/full-version-update.md docs/install/prompts/full-version-update.en.md docs/install/prompts/framework-only-update.md docs/install/prompts/framework-only-update.en.md
git commit -m "docs: require mcp auto provision in install prompts"
```

### Task 7: Align supporting install docs with the final-report contract

**Files:**
- Modify: `docs/install/recommended-full-path.md`
- Modify: `docs/install/recommended-full-path.en.md`
- Modify: `docs/one-shot-setup.md`
- Modify: `tests/runtime_neutral/test_install_prompt_mcp_contract.py`

- [ ] **Step 1: Extend the docs contract test**

```python
    def test_supporting_install_docs_describe_non_blocking_mcp_attempts(self) -> None:
        for path in SUPPORTING_DOCS:
            text = path.read_text(encoding="utf-8-sig")
            self.assertIn("scrapling", text, path.name)
            self.assertIn("claude-flow", text, path.name)
            self.assertIn("manual follow-up", text.lower(), path.name)
            self.assertIn("online-ready", text.lower(), path.name)
```

- [ ] **Step 2: Run the docs-focused contract tests and confirm failure**

Run: `python3 -m pytest tests/runtime_neutral/test_install_prompt_mcp_contract.py -k "supporting_install_docs" -v`

Expected: `FAIL` because the supporting docs do not yet describe the shared MCP attempt/report contract.

- [ ] **Step 3: Update the supporting install docs**

```markdown
- Local install success means the VibeSkills payload and sidecar state are present in the chosen host root.
- MCP auto-provision means VibeSkills attempted `github`, `context7`, `serena`, `scrapling`, and `claude-flow`; some hosts may still require manual host-native follow-up.
- Online-ready is a separate state controlled by `VCO_INTENT_ADVICE_*` and optional `VCO_VECTOR_DIFF_*` configuration.
```

- [ ] **Step 4: Re-run the docs contract tests**

Run: `python3 -m pytest tests/runtime_neutral/test_install_prompt_mcp_contract.py -v`

Expected: `PASS`

- [ ] **Step 5: Commit**

```bash
git add docs/install/recommended-full-path.md docs/install/recommended-full-path.en.md docs/one-shot-setup.md tests/runtime_neutral/test_install_prompt_mcp_contract.py
git commit -m "docs: align install guides with mcp auto provision reporting"
```

## Chunk 5: Final Verification And Delivery Closure

### Task 8: Run the focused verification set and capture delivery evidence

**Files:**
- Modify: `docs/superpowers/plans/2026-04-07-install-prompt-mcp-auto-provision.md`
  Responsibility: check off completed steps during execution and, if needed, record any scope adjustments before handoff.

- [ ] **Step 1: Run the focused Python test set**

Run: `python3 -m pytest tests/runtime_neutral/test_mcp_auto_provision.py tests/runtime_neutral/test_install_prompt_mcp_contract.py tests/runtime_neutral/test_bootstrap_doctor.py tests/runtime_neutral/test_shell_entrypoint_compatibility.py -v`

Expected: `PASS`

- [ ] **Step 2: Run wrapper syntax validation**

Run: `bash -n install.sh && bash -n check.sh && bash -n scripts/bootstrap/one-shot-setup.sh`

Expected: no output and exit code `0`

- [ ] **Step 3: Run one end-to-end install smoke in a temp target root**

Run: `tmpdir="$(mktemp -d)" && bash ./install.sh --host codex --profile full --target-root "$tmpdir/.codex" --skip-runtime-freshness-gate`

Expected: exit code `0`, a new `.vibeskills/mcp-auto-provision.json` under the temp target root, and one final install report that separates local install from MCP readiness.

- [ ] **Step 4: Inspect the doctor artifact from the same temp root**

Run: `python3 ./scripts/verify/runtime_neutral/bootstrap_doctor.py --target-root "$tmpdir/.codex" --write-artifacts`

Expected: exit code `0` or `1` based on readiness, plus `outputs/verify/vibe-bootstrap-doctor-gate.json` showing `install_state`, `mcp_auto_provision_attempted`, and per-MCP statuses.

- [ ] **Step 5: Commit and prepare execution handoff**

```bash
git add config/mcp-auto-provision.registry.json apps/vgo-cli/src/vgo_cli/mcp_provision.py apps/vgo-cli/src/vgo_cli/external.py apps/vgo-cli/src/vgo_cli/commands.py apps/vgo-cli/src/vgo_cli/install_support.py apps/vgo-cli/src/vgo_cli/output.py scripts/bootstrap/one-shot-setup.sh scripts/bootstrap/one-shot-setup.ps1 packages/verification-core/src/vgo_verify/bootstrap_doctor.py packages/verification-core/src/vgo_verify/bootstrap_doctor_runtime.py scripts/verify/vibe-bootstrap-doctor-gate.ps1 mcp/servers.template.json tests/runtime_neutral/test_mcp_auto_provision.py tests/runtime_neutral/test_install_prompt_mcp_contract.py tests/runtime_neutral/test_bootstrap_doctor.py tests/runtime_neutral/test_shell_entrypoint_compatibility.py docs/install/prompts/full-version-install.md docs/install/prompts/full-version-install.en.md docs/install/prompts/framework-only-install.md docs/install/prompts/framework-only-install.en.md docs/install/prompts/full-version-update.md docs/install/prompts/full-version-update.en.md docs/install/prompts/framework-only-update.md docs/install/prompts/framework-only-update.en.md docs/install/recommended-full-path.md docs/install/recommended-full-path.en.md docs/one-shot-setup.md
git commit -m "feat: add cross-host mcp auto provision install contract"
```

## Delivery Notes

- Keep the new receipt under the target root, not under repo-local `outputs/`, so install, check, one-shot, and doctor can all inspect the same machine-readable truth.
- Do not reintroduce Codex-only assumptions in shared helpers. Codex can still be the strongest governed path, but the orchestration contract must cover all six supported hosts.
- Do not make MCP failures fatal to base install success. The only fatal path here should be true local install failure, not MCP readiness gaps.
- Keep the final install report concise. The point is one summary at the end, not repeated warnings throughout the run.
