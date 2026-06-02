# Current Surface Retired Terminology Erasure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove positive-use retired routing terminology from the current maintenance surface while preserving historical records and negative assertions.

**Architecture:** Extend the existing terminology scan into a current-surface budget gate, then migrate verification-core audit outputs and active docs to skill-routing language. Retired terms remain allowed only as historical evidence, negative assertions, or explicitly named compatibility input handling.

**Tech Stack:** PowerShell gate scripts, JSON policy files, Python verification modules, pytest/unittest test suites, Markdown governance docs.

---

## File Structure

**Gate and policy**

- Modify: `config/routing-terminology-hard-cleanup.json`
  - Owns current-surface terminology scan inputs for active docs, current code roots, historical roots, negative assertion files, and compatibility review files.
- Modify: `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1`
  - Owns classification of retired-term hits into `fail`, `allowed_negative`, `allowed_historical`, and `review`.
- Modify: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
  - Owns the JSON contract and regression tests for the terminology budget gate.

**Verification-core audit outputs**

- Modify: `packages/verification-core/src/vgo_verify/global_pack_consolidation_audit.py`
  - Renames current report columns away from route-authority and stage-assistant wording.
- Modify: `packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py`
  - Renames target routing role fields and markdown sections to current skill-routing terms.
- Modify: `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`
  - Renames target routing role fields and markdown sections to current skill-routing terms.
- Modify: `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`
  - Renames current-role compatibility handling and target summary terms.
- Modify: `tests/runtime_neutral/test_global_pack_consolidation_audit.py`
- Modify: `tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py`
- Modify: `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`
- Modify: `tests/runtime_neutral/test_ml_skills_pruning_audit.py`
  - These tests own audit output expectations and retired-term absence checks.

**Active docs**

- Modify: `docs/governance/current-routing-contract.md`
- Modify: `docs/governance/current-runtime-field-contract.md`
- Modify: `docs/governance/terminology-governance.md`
- Modify when the budget gate reports active-doc failures: `README.md`, `README.zh.md`, `SKILL.md`, `protocols/runtime.md`, `protocols/team.md`, `docs/install/**`, and `docs/status/**`.
  - These docs own the current user-visible and maintainer-visible vocabulary.

**Do not modify for cosmetic cleanup**

- Do not rewrite `docs/superpowers/plans/**` beyond this implementation plan.
- Do not rewrite old dated governance reports if the gate classifies them as historical.
- Do not install or deploy this branch into Codex.

---

### Task 1: Add The Current-Surface Budget Gate Contract

**Files:**

- Modify: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
- Modify: `config/routing-terminology-hard-cleanup.json`

- [ ] **Step 1: Add failing JSON-contract assertions to the terminology gate test**

In `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`, update `test_hard_cleanup_scan_reports_json` so it asserts the new budget categories. Keep the existing PowerShell resolution helper unchanged.

Replace the payload assertions in that test with this block:

```python
        payload = json.loads(completed.stdout)
        self.assertIn("summary", payload)
        self.assertIn("fail_count", payload["summary"])
        self.assertIn("allowed_negative_count", payload["summary"])
        self.assertIn("allowed_historical_count", payload["summary"])
        self.assertIn("review_count", payload["summary"])
        self.assertIn("findings", payload)
        self.assertIn("failures", payload)
        self.assertIn("allowed_negative", payload)
        self.assertIn("allowed_historical", payload)
        self.assertIn("review", payload)
        self.assertEqual("pass", payload["status"])
        self.assertEqual(0, int(payload["summary"]["fail_count"]))
        self.assertGreater(int(payload["summary"]["allowed_negative_count"]), 0)
        self.assertGreater(int(payload["summary"]["allowed_historical_count"]), 50)
        self.assertGreaterEqual(int(payload["summary"]["review_count"]), 0)
        self.assertEqual([], payload["failures"])
```

- [ ] **Step 2: Add policy-shape assertions to the same test file**

Add this test method to `RoutingTerminologyHardCleanupTests`:

```python
    def test_policy_defines_current_surface_budget_layers(self) -> None:
        policy_path = REPO_ROOT / "config" / "routing-terminology-hard-cleanup.json"
        payload = json.loads(policy_path.read_text(encoding="utf-8"))

        self.assertIn("current_surface_roots", payload)
        self.assertIn("historical_surface_roots", payload)
        self.assertIn("allowed_negative_files", payload)
        self.assertIn("compatibility_review_files", payload)
        self.assertIn("retired_positive_terms", payload)

        current_roots = set(payload["current_surface_roots"])
        self.assertIn("packages/verification-core/src/vgo_verify", current_roots)
        self.assertIn("scripts/verify", current_roots)
        self.assertIn("tests/runtime_neutral", current_roots)
        self.assertIn("docs/governance/current-routing-contract.md", current_roots)
        self.assertIn("docs/governance/current-runtime-field-contract.md", current_roots)
        self.assertIn("docs/governance/terminology-governance.md", current_roots)

        historical_roots = set(payload["historical_surface_roots"])
        self.assertIn("docs/superpowers/plans", historical_roots)
        self.assertIn("docs/superpowers/specs", historical_roots)

        retired_terms = set(payload["retired_positive_terms"])
        for term in [
            "route_authority_candidates",
            "stage_assistant_candidates",
            "route_authority_eligible",
            "legacy_role",
            "_legacy_role",
            "_legacy_stage_assistant_candidates",
            "route authority",
            "stage assistant",
            "route owner",
        ]:
            self.assertIn(term, retired_terms)
```

- [ ] **Step 3: Extend the policy file with the new budget keys**

In `config/routing-terminology-hard-cleanup.json`, add these top-level keys while keeping the existing keys in place until the script has been migrated:

```json
  "current_surface_roots": [
    "README.md",
    "README.zh.md",
    "SKILL.md",
    "protocols",
    "docs/governance/current-routing-contract.md",
    "docs/governance/current-runtime-field-contract.md",
    "docs/governance/terminology-governance.md",
    "docs/install",
    "docs/status",
    "packages/verification-core/src/vgo_verify",
    "packages/runtime-core/src/vgo_runtime",
    "scripts/router",
    "scripts/runtime",
    "scripts/verify",
    "tests/runtime_neutral",
    "tests/unit",
    "tests/integration"
  ],
  "historical_surface_roots": [
    "docs/superpowers/plans",
    "docs/superpowers/specs",
    "docs/governance"
  ],
  "historical_surface_exemptions": [
    "docs/governance/current-routing-contract.md",
    "docs/governance/current-runtime-field-contract.md",
    "docs/governance/terminology-governance.md"
  ],
  "allowed_negative_files": [
    "tests/runtime_neutral/test_current_routing_debt_gate.py",
    "tests/runtime_neutral/test_current_routing_debt_erasure_policy.py",
    "tests/runtime_neutral/test_current_routing_contract_cleanup.py",
    "tests/runtime_neutral/test_routing_terminology_hard_cleanup.py",
    "tests/runtime_neutral/test_retired_old_routing_compat.py",
    "tests/runtime_neutral/test_runtime_route_output_shape.py",
    "scripts/verify/vibe-current-routing-debt-gate.ps1",
    "scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1"
  ],
  "compatibility_review_files": [
    "scripts/runtime/VibeConsultation.Common.ps1",
    "scripts/runtime/legacy/VibeRetiredConsultation.Common.ps1",
    "packages/runtime-core/src/vgo_runtime/router_contract_runtime.py",
    "packages/runtime-core/src/vgo_runtime/router_contract_presentation.py",
    "scripts/router/resolve-pack-route.ps1"
  ],
  "retired_positive_terms": [
    "route_authority_candidates",
    "stage_assistant_candidates",
    "route_authority_eligible",
    "legacy_role",
    "_legacy_role",
    "_legacy_stage_assistant_candidates",
    "route authority",
    "stage assistant",
    "route owner",
    "primary skill",
    "secondary skill",
    "legacy admission role",
    "pack consolidation role"
  ]
```

If JSON commas need adjusting, keep the file valid JSON and preserve the existing `retired_terms` block for backward compatibility with the old scan assertions until Task 2 removes the old shape.

- [ ] **Step 4: Run the focused tests and verify they fail for missing JSON fields or current-surface findings**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_routing_terminology_hard_cleanup.py -q
```

Expected: FAIL. The failure should mention one of the new payload keys, policy keys, or a nonzero fail count. If it fails because the JSON file is invalid, fix the comma placement in `config/routing-terminology-hard-cleanup.json` before moving to Task 2.

---

### Task 2: Implement Budget Classification In The Existing Scan Script

**Files:**

- Modify: `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1`
- Modify: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
- Modify: `config/routing-terminology-hard-cleanup.json`

- [ ] **Step 1: Add reusable path helpers to the scan script**

In `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1`, keep `Read-JsonFile`, `Get-TextFileLines`, `New-Finding`, and `ConvertTo-RepoRelativePath`. Add these helpers after `ConvertTo-RepoRelativePath`:

```powershell
function Test-PathPrefix {
    param(
        [Parameter(Mandatory)] [string]$Path,
        [Parameter(Mandatory)] [string[]]$Prefixes
    )

    $normalized = $Path.Replace('\', '/').TrimStart('/')
    foreach ($prefix in $Prefixes) {
        $candidate = [string]$prefix
        if ([string]::IsNullOrWhiteSpace($candidate)) {
            continue
        }
        $candidate = $candidate.Replace('\', '/').TrimEnd('/')
        if ($normalized.Equals($candidate, [System.StringComparison]::OrdinalIgnoreCase)) {
            return $true
        }
        if ($normalized.StartsWith($candidate + '/', [System.StringComparison]::OrdinalIgnoreCase)) {
            return $true
        }
    }
    return $false
}

function Get-BudgetScanFiles {
    param(
        [Parameter(Mandatory)] [string]$Root,
        [Parameter(Mandatory)] [string[]]$Roots,
        [string[]]$HistoricalRoots = @(),
        [string[]]$HistoricalExemptions = @()
    )

    $extensions = @('.ps1', '.py', '.json', '.md', '.yaml', '.yml', '.toml')
    $files = New-Object System.Collections.Generic.List[object]
    $seen = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)

    foreach ($relative in $Roots) {
        $full = Join-Path $Root $relative
        if (Test-Path -LiteralPath $full -PathType Leaf) {
            $item = Get-Item -LiteralPath $full
            $repoRelative = ConvertTo-RepoRelativePath -Path $item.FullName -Root $Root
            $isHistorical = (Test-PathPrefix -Path $repoRelative -Prefixes $HistoricalRoots) -and -not (Test-PathPrefix -Path $repoRelative -Prefixes $HistoricalExemptions)
            if (($extensions -contains $item.Extension.ToLowerInvariant()) -and -not $isHistorical -and $seen.Add($item.FullName)) {
                $files.Add($item) | Out-Null
            }
            continue
        }
        if (-not (Test-Path -LiteralPath $full -PathType Container)) {
            continue
        }
        foreach ($file in Get-ChildItem -LiteralPath $full -Recurse -File) {
            $repoRelative = ConvertTo-RepoRelativePath -Path $file.FullName -Root $Root
            $isHistorical = (Test-PathPrefix -Path $repoRelative -Prefixes $HistoricalRoots) -and -not (Test-PathPrefix -Path $repoRelative -Prefixes $HistoricalExemptions)
            if ($isHistorical) {
                continue
            }
            if (($extensions -contains $file.Extension.ToLowerInvariant()) -and $seen.Add($file.FullName)) {
                $files.Add($file) | Out-Null
            }
        }
    }

    return @($files.ToArray() | Sort-Object FullName)
}
```

- [ ] **Step 2: Add line classification helpers**

Add these helpers after `Test-LineHasRetiredContext`:

```powershell
function Test-LineIsNegativeAssertion {
    param([Parameter(Mandatory)] [string]$Line)

    foreach ($needle in @('assertNotIn', 'assertNotRegex', 'not in', 'forbidden', 'must not', 'do not', 'absence', 'leaked', 'retired')) {
        if ($Line.IndexOf($needle, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
            return $true
        }
    }
    return $false
}

function Test-LineIsCompatibilityExplanation {
    param([Parameter(Mandatory)] [string]$Line)

    foreach ($needle in @('compatibility', 'retired input', 'migration input', 'old input', 'legacy fallback', 'retired old routing')) {
        if ($Line.IndexOf($needle, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
            return $true
        }
    }
    return $false
}
```

- [ ] **Step 3: Add the budget scan after the existing historical scan**

After the existing `$currentPolicyHelperCount` loop and before `$summary = [pscustomobject]@{`, add this block:

```powershell
$budgetFailures = New-Object System.Collections.Generic.List[object]
$allowedNegative = New-Object System.Collections.Generic.List[object]
$allowedHistorical = New-Object System.Collections.Generic.List[object]
$compatibilityReview = New-Object System.Collections.Generic.List[object]

$budgetTerms = @()
if ($config.PSObject.Properties.Name -contains 'retired_positive_terms') {
    $budgetTerms = @($config.retired_positive_terms | ForEach-Object { [string]$_ })
} else {
    $budgetTerms = @($config.retired_terms | ForEach-Object { [string]$_ })
}

$currentSurfaceRoots = @($config.current_surface_roots | ForEach-Object { [string]$_ })
$historicalSurfaceRoots = @($config.historical_surface_roots | ForEach-Object { [string]$_ })
$historicalSurfaceExemptions = @($config.historical_surface_exemptions | ForEach-Object { [string]$_ })
$allowedNegativeFiles = @($config.allowed_negative_files | ForEach-Object { [string]$_ })
$compatibilityReviewFiles = @($config.compatibility_review_files | ForEach-Object { [string]$_ })

$budgetFiles = @(Get-BudgetScanFiles -Root $RepoRoot -Roots $currentSurfaceRoots -HistoricalRoots $historicalSurfaceRoots -HistoricalExemptions $historicalSurfaceExemptions)
foreach ($file in $budgetFiles) {
    $relative = ConvertTo-RepoRelativePath -Path $file.FullName -Root $RepoRoot
    $lines = @(Get-TextFileLines -Path $file.FullName)
    for ($index = 0; $index -lt $lines.Count; $index++) {
        $lineText = [string]$lines[$index]
        foreach ($pattern in $budgetTerms) {
            if ([string]::IsNullOrWhiteSpace($pattern)) {
                continue
            }
            if ($lineText.IndexOf([string]$pattern, [System.StringComparison]::OrdinalIgnoreCase) -lt 0) {
                continue
            }
            $finding = New-Finding -Category 'current_surface_retired_term' -Path $relative -Line ($index + 1) -Pattern ([string]$pattern) -Text $lineText
            if (Test-PathPrefix -Path $relative -Prefixes $allowedNegativeFiles) {
                if (Test-LineIsNegativeAssertion -Line $lineText) {
                    $allowedNegative.Add($finding) | Out-Null
                } else {
                    $budgetFailures.Add($finding) | Out-Null
                }
                continue
            }
            if (Test-PathPrefix -Path $relative -Prefixes $compatibilityReviewFiles) {
                if ((Test-LineIsCompatibilityExplanation -Line $lineText) -or (Test-LineHasRetiredContext -Line $lineText)) {
                    $compatibilityReview.Add($finding) | Out-Null
                } else {
                    $budgetFailures.Add($finding) | Out-Null
                }
                continue
            }
            $budgetFailures.Add($finding) | Out-Null
        }
    }
}

foreach ($relative in @($historicalDocFiles.Keys | Sort-Object)) {
    if ($historicalDocExemptions.Contains([string]$relative)) {
        continue
    }
    if (-not (Test-PathPrefix -Path ([string]$relative) -Prefixes $historicalSurfaceRoots)) {
        continue
    }
    $fullPath = Join-Path $RepoRoot ([string]$relative)
    $lines = @(Get-TextFileLines -Path $fullPath)
    for ($index = 0; $index -lt $lines.Count; $index++) {
        $lineText = [string]$lines[$index]
        foreach ($pattern in $budgetTerms) {
            if ($lineText.IndexOf([string]$pattern, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
                $allowedHistorical.Add((New-Finding -Category 'allowed_historical' -Path ([string]$relative) -Line ($index + 1) -Pattern ([string]$pattern) -Text $lineText)) | Out-Null
                break
            }
        }
    }
}
```

- [ ] **Step 4: Replace the JSON summary shape while preserving old counters**

Replace the existing `$summary = [pscustomobject]@{ ... }` block with this block:

```powershell
$allFindings = New-Object System.Collections.Generic.List[object]
foreach ($finding in @($findings.ToArray())) { $allFindings.Add($finding) | Out-Null }
foreach ($finding in @($budgetFailures.ToArray())) { $allFindings.Add($finding) | Out-Null }

$summary = [pscustomobject]@{
    current_doc_retired_term_violation_count = @($findings | Where-Object { $_.category -eq 'current_doc_retired_term' }).Count
    current_behavior_test_retired_field_read_count = @($findings | Where-Object { $_.category -eq 'current_behavior_test_retired_field_read' }).Count
    historical_doc_retired_term_file_count = [int]$historicalRetiredTermFileCount
    historical_doc_marked_retired_term_count = [int]$historicalMarkedCount
    historical_doc_unmarked_retired_term_count = @($findings | Where-Object { $_.category -eq 'historical_doc_unmarked_retired_term' }).Count
    execution_internal_specialist_dispatch_reference_count = [int]$executionInternalCount
    current_policy_helper_dispatch_vocabulary_reference_count = [int]$currentPolicyHelperCount
    fail_count = @($budgetFailures).Count
    allowed_negative_count = @($allowedNegative).Count
    allowed_historical_count = @($allowedHistorical).Count
    review_count = @($compatibilityReview).Count
}

$status = if (@($allFindings).Count -eq 0) { 'pass' } else { 'fail' }
$payload = [pscustomobject]@{
    status = $status
    summary = $summary
    findings = [object[]]$allFindings.ToArray()
    failures = [object[]]$budgetFailures.ToArray()
    allowed_negative = [object[]]$allowedNegative.ToArray()
    allowed_historical = [object[]]$allowedHistorical.ToArray()
    review = [object[]]$compatibilityReview.ToArray()
}
```

Then update both output branches to write `$payload` instead of `$summary`.

- [ ] **Step 5: Preserve the existing text output and exit behavior**

In the non-JSON branch, print the new budget counters after the old counters:

```powershell
    ('Current surface failures: {0}' -f [int]$summary.fail_count)
    ('Allowed negative hits: {0}' -f [int]$summary.allowed_negative_count)
    ('Allowed historical hits: {0}' -f [int]$summary.allowed_historical_count)
    ('Compatibility review hits: {0}' -f [int]$summary.review_count)
```

Replace the final exit condition with:

```powershell
if ($status -ne 'pass') {
    exit 1
}
exit 0
```

- [ ] **Step 6: Run the focused gate tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_routing_terminology_hard_cleanup.py -q
```

Expected: FAIL if current-surface retired terms remain. PASS only after the next tasks clean or classify every current-surface hit.

- [ ] **Step 7: Commit the budget gate contract and implementation if the scan script behaves correctly**

If the test still fails because of real terminology debt, commit the gate only after confirming the JSON shape is correct by running:

```powershell
powershell -NoLogo -NoProfile -File scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
```

Expected: valid JSON with `status`, `summary`, `failures`, `allowed_negative`, `allowed_historical`, and `review`.

Commit:

```bash
git add config/routing-terminology-hard-cleanup.json scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 tests/runtime_neutral/test_routing_terminology_hard_cleanup.py
git commit -m "test: add current surface terminology budget gate"
```

---

### Task 3: Make Verification-Core Audit Tests Demand Current Terminology

**Files:**

- Modify: `tests/runtime_neutral/test_global_pack_consolidation_audit.py`
- Modify: `tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py`
- Modify: `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`
- Modify: `tests/runtime_neutral/test_ml_skills_pruning_audit.py`

- [ ] **Step 1: Add a shared local retired-term assertion pattern to each audit test file**

At the top of each of the four test files, after path constants, add:

```python
RETIRED_POSITIVE_OUTPUT_TERMS = [
    "route_authority_count",
    "stage_assistant_count",
    "target_route_authority_count",
    "target_stage_assistant_count",
    "target_route_authority_candidates",
    "target_stage_assistant_candidates",
    "keep-route-authority",
    "Route Authorities",
    "Stage Assistants",
    "Target Route Authorities",
    "Target Stage Assistants",
    "route authority",
    "stage assistant",
]


def assert_no_retired_positive_output_terms(text: str) -> None:
    lower = text.lower()
    for term in RETIRED_POSITIVE_OUTPUT_TERMS:
        assert term.lower() not in lower, term
```

If a fixture input still needs `route_authority_candidates` or `stage_assistant_candidates`, keep those fixture literals inside the fixture writer. Do not apply this helper to fixture input strings.

- [ ] **Step 2: Update global audit expectations**

In `tests/runtime_neutral/test_global_pack_consolidation_audit.py`, update assertions to the new output names:

```python
        self.assertEqual(0, rows["research-design"].compat_direct_candidate_count)
        self.assertFalse(rows["research-design"].has_compat_role_split)
```

In `test_artifact_writer_outputs_json_csv_and_markdown`, replace the CSV and Markdown assertions with:

```python
        self.assertIn("pack_id,skill_candidate_count,compat_direct_candidate_count", csv_text)
        self.assertIn("research-design", csv_text)
        assert_no_retired_positive_output_terms(csv_text)

        markdown_text = written["markdown"].read_text(encoding="utf-8")
        self.assertIn("# Global Pack Routing Audit", markdown_text)
        self.assertIn("## P0", markdown_text)
        self.assertIn("research-design", markdown_text)
        assert_no_retired_positive_output_terms(markdown_text)
```

- [ ] **Step 3: Update code-quality audit expectations**

In `tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py`, replace every expected `keep-route-authority` target role with `keep-routing-skill`.

In `test_artifact_writer_outputs_json_csv_and_markdown`, replace:

```python
        self.assertEqual(0, artifact.to_dict()["summary"]["target_stage_assistant_count"])
```

with:

```python
        self.assertEqual(0, artifact.to_dict()["summary"]["target_retired_stage_candidate_count"])
        self.assertEqual(10, artifact.to_dict()["summary"]["target_routing_skill_count"])
```

Then add after reading markdown:

```python
        assert_no_retired_positive_output_terms(json.dumps(artifact.to_dict(), ensure_ascii=False))
        assert_no_retired_positive_output_terms(csv_text)
        assert_no_retired_positive_output_terms(markdown_text)
```

In `test_problem_artifact_does_not_describe_live_stage_assistants`, replace the method name with `test_problem_artifact_uses_current_routing_skill_language` and replace the assertion body with:

```python
        markdown_text = written["markdown"].read_text(encoding="utf-8")
        self.assertIn("## 保留路由技能", markdown_text)
        self.assertIn("## 迁移后删除", markdown_text)
        self.assertIn("## 推迟迁移", markdown_text)
        assert_no_retired_positive_output_terms(markdown_text)
```

- [ ] **Step 4: Update bio-science audit expectations**

In `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`, rename imports and aliases in the test file:

```python
    BIO_SCIENCE_ROUTING_SKILLS,
    BIO_SCIENCE_RETIRED_STAGE_CANDIDATES,
```

Replace local alias names:

```python
BIO_SCIENCE_DIRECT_ROUTING_SKILLS = BIO_SCIENCE_DIRECT_OWNERS
```

Replace summary assertions:

```python
        self.assertEqual(4, artifact.to_dict()["summary"]["target_routing_skill_count"])
        self.assertEqual(0, artifact.to_dict()["summary"]["target_retired_stage_candidate_count"])
```

Replace markdown assertions:

```python
        self.assertIn("# Bio-Science Problem-First Consolidation", markdown_text)
        self.assertIn("## Routing Skills", markdown_text)
        self.assertIn("Retired stage candidates: 0", markdown_text)
        assert_no_retired_positive_output_terms(markdown_text)
```

- [ ] **Step 5: Update ML audit expectations**

In `tests/runtime_neutral/test_ml_skills_pruning_audit.py`, replace:

```python
        self.assertEqual(0, artifact.to_dict()["summary"]["target_stage_assistant_count"])
```

with:

```python
        self.assertEqual(0, artifact.to_dict()["summary"]["target_retired_stage_candidate_count"])
```

In `test_problem_artifact_writer_outputs_json_csv_and_markdown`, add:

```python
        assert_no_retired_positive_output_terms(json.dumps(artifact.to_dict(), ensure_ascii=False))
        assert_no_retired_positive_output_terms(csv_text)
        assert_no_retired_positive_output_terms(markdown_text)
```

- [ ] **Step 6: Run audit tests and verify they fail before implementation**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_global_pack_consolidation_audit.py tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
```

Expected: FAIL on missing renamed attributes, old summary keys, or retired output terms.

---

### Task 4: Migrate Verification-Core Audit Modules To Current Routing Language

**Files:**

- Modify: `packages/verification-core/src/vgo_verify/global_pack_consolidation_audit.py`
- Modify: `packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py`
- Modify: `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`
- Modify: `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`

- [ ] **Step 1: Migrate global audit field names**

In `global_pack_consolidation_audit.py`, replace the `CSV_FIELDS` role columns:

```python
    "compat_direct_candidate_count",
    "compat_stage_candidate_count",
    "has_compat_role_split",
```

Replace the `PackAuditRow` role fields with:

```python
    compat_direct_candidate_count: int
    compat_stage_candidate_count: int
    has_compat_role_split: bool
```

Rename helper functions:

```python
def _compat_candidates(pack: dict[str, Any], key: str) -> list[str]:
    return [str(item).strip() for item in _as_list(pack.get(key)) if str(item).strip()]


def _has_compat_role_split(pack: dict[str, Any]) -> bool:
    return "route_authority_candidates" in pack or "stage_assistant_candidates" in pack
```

Keep the old manifest keys inside these compatibility helpers only. Do not emit those key names to CSV or Markdown.

- [ ] **Step 2: Migrate global audit calculations and report text**

In `audit_repository`, use:

```python
        compat_direct = _compat_candidates(pack, "route_authority_candidates")
        compat_stage = _compat_candidates(pack, "stage_assistant_candidates")
        compat_roles = _has_compat_role_split(pack)
```

Pass these values into scoring and rows:

```python
            route_count=len(compat_direct),
            explicit_roles=compat_roles,
```

Create `PackAuditRow` with:

```python
            compat_direct_candidate_count=len(compat_direct),
            compat_stage_candidate_count=len(compat_stage),
            has_compat_role_split=compat_roles,
```

Replace `_recommended_next_action` text:

```python
        return "write a pack-specific problem map before changing skill routing"
```

and:

```python
        return "define explicit skill-routing boundaries after content review"
```

Replace `_markdown_table` header with:

```python
        "| priority | pack | score | skills | compat direct | compat stage | rationale |",
        "|---|---|---:|---:|---:|---:|---|",
```

Replace row formatting to read:

```python
                direct=row.compat_direct_candidate_count,
                stage=row.compat_stage_candidate_count,
```

Rename the report title to:

```python
        "# Global Pack Routing Audit",
```

- [ ] **Step 3: Migrate code-quality audit terms**

In `code_quality_pack_consolidation_audit.py`, rename constants:

```python
TARGET_ROUTING_SKILLS = [
```

and:

```python
TARGET_RETIRED_STAGE_CANDIDATES: list[str] = []
```

Replace every decision value:

```python
"target_role": "keep-routing-skill",
```

Replace `routing_change` phrases such as:

```python
"keep as default code review routing skill"
"keep as default debug/root-cause routing skill"
"keep as narrow security review routing skill"
"keep as TDD routing skill"
"keep as test report packaging routing skill"
"keep as narrow Windows hook routing skill"
"keep as AI-code-cleanup routing skill"
"keep as narrow review-feedback routing skill"
"keep as narrow completion-evidence routing skill"
"keep as direct routing skill for preparing review requests"
```

Replace summary output keys in `to_dict`:

```python
                "target_routing_skill_count": len(TARGET_ROUTING_SKILLS),
                "target_retired_stage_candidate_count": len(TARGET_RETIRED_STAGE_CANDIDATES),
```

Replace output collections:

```python
            "target_routing_skills": TARGET_ROUTING_SKILLS,
            "target_retired_stage_candidates": TARGET_RETIRED_STAGE_CANDIDATES,
```

Rename current-role compatibility sets inside `_current_role`:

```python
    compat_direct = {str(item) for item in _as_list(pack.get("route_authority_candidates"))}
    compat_stage = {str(item) for item in _as_list(pack.get("stage_assistant_candidates"))}
    if skill_id in compat_direct:
        return "compat_direct_candidate"
    if skill_id in compat_stage:
        return "compat_stage_candidate"
```

Replace markdown keep-row selection:

```python
    keep_rows = [row for row in artifact.rows if row.target_role == "keep-routing-skill"]
```

Replace heading:

```python
            "## 保留路由技能",
```

- [ ] **Step 4: Migrate bio-science audit terms**

In `bio_science_pack_consolidation_audit.py`, rename constants:

```python
BIO_SCIENCE_ROUTING_SKILLS = [
```

and:

```python
BIO_SCIENCE_RETIRED_STAGE_CANDIDATES: list[str] = []
```

Replace `routing_change` phrases with current language:

```python
"keep as routing skill for single-cell RNA-seq clustering, annotation, marker genes, and h5ad/10X workflows"
"keep as routing skill for bulk RNA-seq differential expression, DESeq2-style statistics, MA plots, and volcano plots"
"remove from default bundled routing skill set; explicit BAM/VCF processing should be handled as normal coding rather than a retained bio-science expert"
"keep as routing skill and planning/coding default for sequence IO, FASTA, GenBank, SeqIO, Entrez, and sequence conversion"
"keep as unified routing skill for biological database evidence, annotation, pathway, variant, target, structure, interaction, reference census, and cross-database lookup tasks"
```

Replace the rationale sentence:

```python
"A single evidence skill keeps useful database material without exposing every source wrapper as a separate routing skill."
```

Replace summary keys:

```python
                "target_routing_skill_count": sum(1 for row in self.rows if row.target_role == "keep"),
                "target_retired_stage_candidate_count": sum(1 for row in self.rows if row.target_role == "retired-stage-candidate"),
```

Replace output collections:

```python
            "target_routing_skills": BIO_SCIENCE_ROUTING_SKILLS,
            "target_retired_stage_candidates": BIO_SCIENCE_RETIRED_STAGE_CANDIDATES,
```

Inside `_pack_skill_index`, rename record keys:

```python
                    {"packs": set(), "compat_direct": set(), "compat_stage": set(), "defaults": set()},
```

and use:

```python
                if role_key == "route_authority_candidates":
                    record["compat_direct"].add(pack_id)
                if role_key == "stage_assistant_candidates":
                    record["compat_stage"].add(pack_id)
```

Replace `_current_role`:

```python
def _current_role(record: dict[str, set[str]]) -> str:
    if record["compat_direct"]:
        return "compat_direct_candidate"
    if record["compat_stage"]:
        return "compat_stage_candidate"
    if record["defaults"]:
        return "default"
    return "candidate"
```

Replace markdown labels:

```python
        f"- Target Routing Skills: {len(route_rows)}",
        f"- Retired stage candidates: {len(stage_rows)}",
        "## Routing Skills",
```

Only emit the stage section if `stage_rows` is nonempty, and name it:

```python
        lines.extend(["", "## Retired Stage Candidates", ""])
```

- [ ] **Step 5: Migrate ML audit terms**

In `ml_skills_pruning_audit.py`, replace `routing_change` phrases that say `route authority`:

```python
"keep in data-ml as narrow time-series ML routing skill"
"keep in data-ml as review/evaluation routing skill"
"keep in data-ml as data-understanding routing skill"
"keep in data-ml as leakage-audit routing skill"
"keep in data-ml as direct preprocessing-pipeline routing skill"
"keep in data-ml as narrow explainability routing skill"
```

Replace problem-map summary keys:

```python
                "target_routing_skill_count": sum(1 for row in self.rows if row.target_role == "keep"),
                "target_retired_stage_candidate_count": sum(1 for row in self.rows if row.target_role == "retired-stage-candidate"),
```

Inside `_pack_skill_index`, rename record keys to:

```python
{"packs": set(), "compat_direct": set(), "compat_stage": set(), "defaults": set()}
```

Replace `_current_role` and `_current_pack_role` returns:

```python
    if record["compat_direct"]:
        return "compat_direct_candidate"
    if record["compat_stage"]:
        return "compat_stage_candidate"
```

and:

```python
    if skill_id in compat_direct:
        return "compat_direct_candidate"
    if skill_id in compat_stage:
        return "compat_stage_candidate"
```

Replace checks that compare `current_role`:

```python
    if current_role == "compat_stage_candidate" and len(text) < 3500 and skill_id in DEFAULT_REPLACEMENTS:
```

```python
    if skill_id in OWNER_SKILLS or current_role == "compat_direct_candidate":
```

```python
    if current_role == "compat_stage_candidate":
```

Replace markdown labels:

```python
        f"- Target Routing Skills: {len(keep_rows)}",
        f"- Retired Stage Candidates: {len(stage_rows)}",
```

and:

```python
    lines.extend(["", "## Retired Stage Candidates", ""])
```

- [ ] **Step 6: Run audit tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_global_pack_consolidation_audit.py tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
```

Expected: PASS.

- [ ] **Step 7: Run audit gates**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts/verify/vibe-global-pack-consolidation-audit-gate.ps1
powershell -NoLogo -NoProfile -File scripts/verify/vibe-code-quality-pack-consolidation-audit-gate.ps1
powershell -NoLogo -NoProfile -File scripts/verify/vibe-bio-science-pack-consolidation-audit-gate.ps1
powershell -NoLogo -NoProfile -File scripts/verify/vibe-ml-skills-pruning-audit-gate.ps1
```

Expected: each command prints `[PASS] ... passed`.

- [ ] **Step 8: Commit verification-core terminology migration**

Commit:

```bash
git add packages/verification-core/src/vgo_verify/global_pack_consolidation_audit.py packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py tests/runtime_neutral/test_global_pack_consolidation_audit.py tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py tests/runtime_neutral/test_ml_skills_pruning_audit.py
git commit -m "refactor: rename audit outputs to current routing terms"
```

---

### Task 5: Clean Active Docs And Test Names Exposed By The Budget Gate

**Files:**

- Modify: `docs/governance/current-routing-contract.md`
- Modify: `docs/governance/current-runtime-field-contract.md`
- Modify: `docs/governance/terminology-governance.md`
- Modify as reported by the budget gate: `README.md`, `README.zh.md`, `SKILL.md`, `protocols/runtime.md`, `protocols/team.md`, `docs/install/**`, `docs/status/**`
- Modify as reported by the budget gate: current tests under `tests/runtime_neutral`, `tests/unit`, and `tests/integration`

- [ ] **Step 1: Run the budget gate to get the current active-doc failure list**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
```

Expected: JSON. If `status` is `fail`, use `failures[*].path`, `failures[*].line`, and `failures[*].pattern` as the worklist for this task.

- [ ] **Step 2: Rewrite current routing docs to the current model**

In `docs/governance/current-routing-contract.md`, ensure the current section uses this sentence:

```markdown
The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage.used / skill_usage.unused / skill_usage.evidence`.
```

Move any retired field names into a `## Retired Compatibility Terms` section with this wording:

```markdown
## Retired Compatibility Terms

The following names may appear only in retired-input handling, historical records, or negative assertions. They do not define the current routing model: `route_authority_candidates`, `stage_assistant_candidates`, `route_authority_eligible`, `legacy_role`, `_legacy_role`, and `_legacy_stage_assistant_candidates`.
```

- [ ] **Step 3: Rewrite current runtime field docs to the current model**

In `docs/governance/current-runtime-field-contract.md`, keep retired terms only under `## Retired Layer`. In all sections before `## Retired Layer`, use:

```markdown
Current field authority is split into three layers: `skill_routing` selects candidate skills, `selected_skill_execution` records execution intent, and `skill_usage` records used/unused evidence.
```

If the current section contains `route owner`, rewrite it as `routing skill`. If it contains `stage assistant`, rewrite it as `retired stage-candidate compatibility term`.

- [ ] **Step 4: Rewrite terminology governance as the active glossary**

In `docs/governance/terminology-governance.md`, make the first current glossary table use these rows:

```markdown
| Current term | Meaning |
| --- | --- |
| `skill_candidates` | Candidate skills available to a pack or route decision. |
| `skill_routing.selected` | The selected skill decisions produced by routing. |
| `selected_skill_execution` | The current execution-intent projection shown to users and hosts. |
| `skill_usage.used` | Skills materially used in the run. |
| `skill_usage.unused` | Candidate or selected skills that were not materially used. |
| `skill_usage.evidence` | Evidence tying usage claims to concrete artifacts, files, or receipts. |
```

Add a retired-vocabulary paragraph:

```markdown
Older terms are retired vocabulary. They can appear in historical records, compatibility readers, and negative tests, but active docs and reports must not use them as current architecture names.
```

- [ ] **Step 5: Rename current test methods that present retired terms as the subject**

For failures in current tests, rename method names and assertion messages to lead with current-surface leakage. Use this pattern:

```python
def test_current_surface_forbids_retired_routing_fields(self) -> None:
```

Use assertion messages like:

```python
self.assertNotIn("route_authority_candidates", payload, "retired field leaked into current routing output")
```

Keep negative fixture values only in files that are listed in `allowed_negative_files`.

- [ ] **Step 6: Run the budget gate until it passes**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
```

Expected JSON:

```json
{
  "status": "pass",
  "summary": {
    "fail_count": 0
  },
  "failures": []
}
```

The actual JSON can include additional keys. The required condition is `status == "pass"`, `summary.fail_count == 0`, and an empty `failures` array.

- [ ] **Step 7: Run current terminology and routing tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_routing_terminology_hard_cleanup.py tests/runtime_neutral/test_current_routing_debt_gate.py tests/runtime_neutral/test_current_routing_debt_erasure_policy.py tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py -q
```

Expected: PASS.

- [ ] **Step 8: Commit docs and exposed test cleanup**

Commit:

```bash
git add docs/governance/current-routing-contract.md docs/governance/current-runtime-field-contract.md docs/governance/terminology-governance.md README.md README.zh.md SKILL.md protocols/runtime.md protocols/team.md docs/install docs/status tests/runtime_neutral tests/unit tests/integration config/routing-terminology-hard-cleanup.json scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1
git commit -m "docs: erase retired terminology from current surface"
```

If some listed files were not changed, `git add` will ignore them or report pathspec problems for absent paths. If an absent pathspec fails, re-run `git add` with only the changed paths from `git status --short`.

---

### Task 6: Final Verification And Regression Sweep

**Files:**

- No planned source edits.
- May modify only if a verification failure identifies a concrete missed current-surface terminology leak.

- [ ] **Step 1: Run the terminology budget gate**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
```

Expected: `status` is `pass`, `summary.fail_count` is `0`, and `failures` is `[]`.

- [ ] **Step 2: Run the existing current routing debt gate**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts/verify/vibe-current-routing-debt-gate.ps1 -Json
```

Expected: `status` is `pass`, and `summary.P0`, `summary.P1`, and `summary.P2` are all `0`.

- [ ] **Step 3: Run runtime/router output shape and selection tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_runtime_route_output_shape.py tests/unit/test_router_contract_selection_guards.py tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_simplified_skill_routing_contract.py -q
```

Expected: PASS.

- [ ] **Step 4: Run verification-core audit tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_global_pack_consolidation_audit.py tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py tests/runtime_neutral/test_ml_skills_pruning_audit.py -q
```

Expected: PASS.

- [ ] **Step 5: Run the pack routing smoke gate**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts/verify/vibe-pack-routing-smoke.ps1
```

Expected: all smoke assertions pass. Previous local baseline was `1014 passed, 0 failed`; if the total changes, inspect the output and confirm there are no failures.

- [ ] **Step 6: Run final text scans for current paths**

Run:

```powershell
rg -n "route_authority|stage_assistant|legacy_role|route authority|stage assistant|route owner|keep-route-authority" packages/verification-core/src/vgo_verify scripts/verify docs/governance/current-routing-contract.md docs/governance/current-runtime-field-contract.md docs/governance/terminology-governance.md tests/runtime_neutral/test_global_pack_consolidation_audit.py tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py tests/runtime_neutral/test_ml_skills_pruning_audit.py
```

Expected: no positive-use hits. Remaining hits are acceptable only when they are fixture input, compatibility input, or explicit negative assertions already classified by the budget gate.

- [ ] **Step 7: Run whitespace check**

Run:

```powershell
git diff --check
```

Expected: no output.

- [ ] **Step 8: Commit any verification fixes**

If the final sweep required fixes, commit them:

```bash
git add -u
git commit -m "test: verify current surface terminology erasure"
```

---

## Completion Criteria

The implementation is complete when:

- `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 -Json` reports `status: pass`;
- `failures` is empty and `summary.fail_count` is `0`;
- verification-core audit JSON/CSV/Markdown outputs use current skill-routing language;
- active current docs use the current model and isolate retired vocabulary under retired/compatibility sections;
- existing runtime/router contract tests pass;
- historical plans/specs and old dated governance reports remain available as historical evidence;
- the working tree is clean after commits.
