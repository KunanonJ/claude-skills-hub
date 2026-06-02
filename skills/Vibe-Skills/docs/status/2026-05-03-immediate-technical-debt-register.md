# Immediate Technical Debt Register

Generated: 2026-05-03

Scope: `Vibe-Skills`

This register records the immediate-fixable debt items from the approved
technical debt audit design. It separates fixed blocking debt from retained
maintainability debt so release and implementation discussions do not mix
unrelated risk classes.

## Fixed In Current Branch

| ID | Severity | Title | Evidence Before Fix | Fix Boundary | Verification After Fix |
| --- | --- | --- | --- | --- | --- |
| TD-001 | P0 | Tracked generated outputs violated the strict output artifact boundary | `vibe-output-artifact-boundary-gate.ps1` reported `Tracked outputs : 9` and failed output allowlist/count assertions | Move the nine tracked `outputs/**` files into `references/fixtures/**`, add fixture roots, and keep `expected_tracked_output_count = 0` | `powershell -NoLogo -NoProfile -File scripts\verify\vibe-output-artifact-boundary-gate.ps1` |
| TD-002 | P1 | Test baseline layer execution used broad pytest directories instead of classified layer files | `test-baseline-audit.py --collect-only` classified fast/heavy layers, while `run_layer()` still built commands from shared `pytest_args` | Select classified files from collected nodes and pass those files to pytest for the requested layer | `python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q` and `python scripts\verify\test-baseline-audit.py --run-layer contract_unit` |
| TD-003 | P1 | Quality debt overlay gate could leave byte-level policy diffs after a successful run | Running `vibe-quality-debt-overlay-gate.ps1` rewrote `config/quality-debt-overlay.json` and could leave a trailing blank-line diff | Restore the original policy bytes in the `finally` block | `python -m pytest tests\runtime_neutral\test_quality_debt_overlay_gate.py -q` and `git diff -- config/quality-debt-overlay.json` |
| TD-009 | P1 | `runtime_neutral_fast` exceeded its 300 second policy budget | `python scripts\verify\test-baseline-audit.py --run-layer runtime_neutral_fast` timed out at 300 seconds before the follow-up stabilization pass | Reclassify measured slow governed-runtime and multi-host files into `runtime_neutral_heavy` and keep fast-layer bytecode isolation | `python scripts\verify\test-baseline-audit.py --run-layer runtime_neutral_fast` |
| TD-010 | P1 | Several fast-layer tests asserted older JSON/output contracts | Focused runs failed in historical routing doc compression, workflow acceptance, root-child hierarchy, and skill-promotion metadata tests | Align tests and fixtures with current `summary`-nested hard-scan JSON, project-delivery v5 truth layers, current skill execution terminology, and non-exact destructive-route selection | Focused pytest for the changed runtime-neutral tests |
| TD-011 | P1 | Windows Unicode path projection was unstable in runtime helper tests | Runtime helper tests decoded PowerShell UTF-8 output with the Windows ANSI code page and compared `C:\Users\羽裳\...` with mojibake paths | Force UTF-8 decoding for text-mode PowerShell subprocesses in test support and update the path-boundary helper contract to `Test-VgoPathWithin` | `python -m pytest tests\runtime_neutral\test_runtime_entrypoint_helper.py -q` |
| TD-012 | P1 | Memory runtime activation contract drifted from emitted receipts | Memory tests failed on missing hard-fail `returncode`, changed native-specialist status, and missing `workspace_memory_plane` in write actions | Preserve `workspace_memory_plane` in memory read/write action reports and align tests with current non-hard-fail backend-degradation and direct current-session routing semantics | `python -m pytest tests\runtime_neutral\test_memory_runtime_activation.py -q` |
| TD-013 | P1 | Multi-host specialist execution test was not fast-layer safe | `test_multi_host_specialist_execution.py` timed out in per-file fast diagnostics | Reclassify multi-host specialist execution into `runtime_neutral_heavy` and verify it passes under its own longer runtime budget | `python -m pytest tests\runtime_neutral\test_multi_host_specialist_execution.py -q` |

## Recorded But Not Scheduled

| ID | Severity | Title | Reason Not Scheduled |
| --- | --- | --- | --- |
| TD-004 | P2 | Large runtime and router scripts increase maintenance cost | No current gate failure was traced to these files during this pass; splitting them needs a dedicated design. |
| TD-005 | P2 | Large verification/runtime Python functions increase repair risk | The immediate pass only touches focused audit/gate behavior; function extraction should be planned around a concrete failing contract. |
| TD-006 | P2 | Short wave gate wrappers depend on shared manifest-driven behavior | The wrapper pattern may be valid; evidence discoverability should be audited separately from the current blocking fixes. |
| TD-007 | P3 | Local `main` is ahead of `origin/main` | This is release-sync debt, not a repository code-quality fix. It should be handled by push/release policy after verification. |
| TD-008 | P3 | Historical retired terminology remains in marked historical records | Current routing terminology gates report zero blocking and review debt; historical records are outside this immediate pass. |

## Final Verification Commands

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-output-artifact-boundary-gate.ps1
python -m pytest tests\runtime_neutral\test_test_baseline_audit.py tests\runtime_neutral\test_quality_debt_overlay_gate.py -q
python scripts\verify\test-baseline-audit.py --collect-only
python scripts\verify\test-baseline-audit.py --run-layer contract_unit
python scripts\verify\test-baseline-audit.py --run-layer runtime_neutral_fast
powershell -NoLogo -NoProfile -File scripts\verify\vibe-quality-debt-overlay-gate.ps1
git diff -- config/quality-debt-overlay.json
powershell -NoLogo -NoProfile -File scripts\verify\vibe-repo-cleanliness-gate.ps1
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
git status --short --branch
```
