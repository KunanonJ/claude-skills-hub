# Historical Routing Doc Compression Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Compress and quarantine historical routing terminology so the active Vibe-Skills model remains `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage` without changing runtime behavior.

**Architecture:** Add failing runtime-neutral guards first, then widen the historical scan from a small file list to root-based Markdown inventory, mark historical files with one standard retired note, and compress duplicated legacy governance docs into short redirects. The six-stage runtime, pack route selection, skill execution, and current route fields remain unchanged.

**Tech Stack:** Markdown governance docs, JSON scan configuration, PowerShell verification scripts, Python `unittest` / `pytest` runtime-neutral tests, existing Vibe-Skills gate scripts.

---

> Historical / Retired Note: This implementation plan discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not new runtime states.

## Fixed Boundaries

- Keep the six governed stages unchanged: `skeleton_check`, `deep_interview`, `requirement_doc`, `xl_plan`, `plan_execute`, `phase_cleanup`.
- Keep the current route model unchanged: `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`.
- Keep selected-versus-used truth unchanged: a selected skill becomes used only when `skill_usage.used` has evidence.
- Do not rename deep runtime JSON containers such as `specialist_accounting` or `specialist_decision`.
- Do not restore old-format compatibility reads.
- Do not delete skills, packs, pack manifests, route thresholds, or runtime scripts.
- Do not deploy to the live Codex host in this plan.
- Do not make `historical_reference_count` zero a success criterion; marked historical references may remain.

---

## File Structure

- Create: `tests/runtime_neutral/test_historical_routing_doc_compression.py`
  - Runtime-neutral guard for root-based historical scan config, historical summary doc, compressed legacy governance docs, and unmarked historical references.
- Create: `docs/governance/historical-routing-terminology.md`
  - One concise historical index that explains retired terms and redirects readers to the current routing contract.
- Modify: `config/routing-terminology-hard-cleanup.json`
  - Add root-based historical Markdown scan inputs and current-document exemptions.
- Modify: `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1`
  - Scan historical roots, count marked and unmarked retired-term files, and fail only on unmarked historical files.
- Modify: `scripts/verify/vibe-current-routing-contract-scan.ps1`
  - Relay the widened hard-cleanup historical inventory counts in JSON and plain output.
- Modify: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
  - Assert the hard cleanup scan exposes and passes the widened historical inventory.
- Modify: `tests/runtime_neutral/test_current_routing_contract_scan.py`
  - Assert the current routing scan relays the widened historical inventory.
- Modify and compress:
  - `docs/governance/binary-skill-usage-routing-2026-04-28.md`
  - `docs/governance/simplified-skill-routing-2026-04-29.md`
  - `docs/governance/specialist-dispatch-governance.md`
  - `docs/governance/terminology-governance.md`
- Modify with a standard retired note only:
  - all unmarked Markdown files listed in Task 4.

---

### Task 1: Add Failing Historical Compression Guards

**Files:**
- Create: `tests/runtime_neutral/test_historical_routing_doc_compression.py`

- [ ] **Step 1: Write the failing guard test**

Create `tests/runtime_neutral/test_historical_routing_doc_compression.py`:

```python
from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config" / "routing-terminology-hard-cleanup.json"
HARD_SCAN = REPO_ROOT / "scripts" / "verify" / "vibe-routing-terminology-hard-cleanup-scan.ps1"
SUMMARY_DOC = REPO_ROOT / "docs" / "governance" / "historical-routing-terminology.md"
CURRENT_CONTRACT = "docs/governance/current-routing-contract.md"
CURRENT_FIELD_CONTRACT = "docs/governance/current-runtime-field-contract.md"
CURRENT_MODEL = "skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage"
COMPRESSED_DOCS = [
    REPO_ROOT / "docs" / "governance" / "binary-skill-usage-routing-2026-04-28.md",
    REPO_ROOT / "docs" / "governance" / "simplified-skill-routing-2026-04-29.md",
    REPO_ROOT / "docs" / "governance" / "specialist-dispatch-governance.md",
    REPO_ROOT / "docs" / "governance" / "terminology-governance.md",
]


def resolve_powershell() -> str | None:
    candidates = [
        shutil.which("pwsh"),
        shutil.which("pwsh.exe"),
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        shutil.which("powershell"),
        shutil.which("powershell.exe"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate))
    return None


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class HistoricalRoutingDocCompressionTests(unittest.TestCase):
    def test_config_declares_root_based_historical_inventory(self) -> None:
        config = json.loads(read(CONFIG_PATH))
        self.assertEqual(
            [
                "docs/governance",
                "docs/requirements",
                "docs/superpowers/plans",
                "docs/superpowers/specs",
            ],
            config["historical_doc_roots"],
        )
        self.assertIn("historical_doc_exemptions", config)
        self.assertIn(CURRENT_CONTRACT, config["historical_doc_exemptions"])
        self.assertIn(CURRENT_FIELD_CONTRACT, config["historical_doc_exemptions"])

    def test_hard_scan_reports_root_based_historical_inventory(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available")

        completed = subprocess.run(
            [shell, "-NoLogo", "-NoProfile", "-File", str(HARD_SCAN), "-Json"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        payload = json.loads(completed.stdout)

        self.assertIn("historical_doc_retired_term_file_count", payload)
        self.assertIn("historical_doc_marked_retired_term_count", payload)
        self.assertIn("historical_doc_unmarked_retired_term_count", payload)
        self.assertGreater(int(payload["historical_doc_retired_term_file_count"]), 50)
        self.assertGreater(int(payload["historical_doc_marked_retired_term_count"]), 50)
        self.assertEqual(0, int(payload["historical_doc_unmarked_retired_term_count"]))
        self.assertEqual([], payload["findings"])

    def test_historical_summary_redirects_to_current_contract(self) -> None:
        self.assertTrue(SUMMARY_DOC.exists(), "historical routing terminology summary must exist")
        text = read(SUMMARY_DOC)
        self.assertIn("Historical / Retired Note", text)
        self.assertIn(CURRENT_MODEL, text)
        self.assertIn(CURRENT_CONTRACT, text)
        self.assertIn(CURRENT_FIELD_CONTRACT, text)
        for retired_term in [
            "primary skill",
            "secondary skill",
            "route owner",
            "stage assistant",
            "consultation",
            "specialist dispatch",
        ]:
            self.assertIn(retired_term, text.lower())

    def test_compressed_legacy_governance_docs_are_short_redirects(self) -> None:
        for path in COMPRESSED_DOCS:
            with self.subTest(path=path):
                text = read(path)
                lines = [line for line in text.splitlines() if line.strip()]
                self.assertLessEqual(len(lines), 70)
                self.assertIn("Historical / Retired Note", text)
                self.assertIn(CURRENT_MODEL, text)
                self.assertIn(CURRENT_CONTRACT, text)
                self.assertIn("docs/governance/historical-routing-terminology.md", text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new guard and confirm it fails**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_historical_routing_doc_compression.py -q
```

Expected: `FAIL`. The failures should name the missing `historical_doc_roots` config, the missing `docs/governance/historical-routing-terminology.md`, unmarked historical files, or legacy governance docs with more than 70 nonblank lines.

- [ ] **Step 3: Commit the failing guard**

Run:

```powershell
git add tests/runtime_neutral/test_historical_routing_doc_compression.py
git commit -m "test: guard historical routing doc compression"
```

---

### Task 2: Widen Historical Scan From Explicit List To Roots

**Files:**
- Modify: `config/routing-terminology-hard-cleanup.json`
- Modify: `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1`
- Modify: `scripts/verify/vibe-current-routing-contract-scan.ps1`
- Modify: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
- Modify: `tests/runtime_neutral/test_current_routing_contract_scan.py`

- [ ] **Step 1: Add root inventory settings**

In `config/routing-terminology-hard-cleanup.json`, keep existing keys and add these two root-level keys after `historical_docs`:

```json
  "historical_doc_roots": [
    "docs/governance",
    "docs/requirements",
    "docs/superpowers/plans",
    "docs/superpowers/specs"
  ],
  "historical_doc_exemptions": [
    "docs/governance/current-routing-contract.md",
    "docs/governance/current-runtime-field-contract.md"
  ],
```

- [ ] **Step 2: Replace the historical-doc scan block**

In `scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1`, replace the existing block that starts with:

```powershell
foreach ($relative in @($config.historical_docs)) {
```

and ends before:

```powershell
$executionInternalCount = 0
```

with:

```powershell
$historicalDocFiles = [ordered]@{}
foreach ($relative in @($config.historical_docs)) {
    if (-not [string]::IsNullOrWhiteSpace([string]$relative)) {
        $historicalDocFiles[[string]$relative] = $true
    }
}

if ($config.PSObject.Properties.Name -contains 'historical_doc_roots') {
    foreach ($rootRelative in @($config.historical_doc_roots)) {
        if ([string]::IsNullOrWhiteSpace([string]$rootRelative)) {
            continue
        }
        $rootPath = Join-Path $RepoRoot ([string]$rootRelative)
        if (-not (Test-Path -LiteralPath $rootPath)) {
            continue
        }
        foreach ($file in @(Get-ChildItem -LiteralPath $rootPath -Recurse -File -Filter '*.md')) {
            $relativePath = [System.IO.Path]::GetRelativePath($RepoRoot, $file.FullName).Replace('\', '/')
            $historicalDocFiles[$relativePath] = $true
        }
    }
}

$historicalDocExemptions = @{}
foreach ($relative in @($config.current_docs)) {
    if (-not [string]::IsNullOrWhiteSpace([string]$relative)) {
        $historicalDocExemptions[[string]$relative] = $true
    }
}
if ($config.PSObject.Properties.Name -contains 'historical_doc_exemptions') {
    foreach ($relative in @($config.historical_doc_exemptions)) {
        if (-not [string]::IsNullOrWhiteSpace([string]$relative)) {
            $historicalDocExemptions[[string]$relative] = $true
        }
    }
}

$historicalMarkedCount = 0
$historicalRetiredTermFileCount = 0
foreach ($relative in @($historicalDocFiles.Keys | Sort-Object)) {
    if ($historicalDocExemptions.Contains([string]$relative)) {
        continue
    }

    $fullPath = Join-Path $RepoRoot ([string]$relative)
    $lines = @(Get-TextFileLines -Path $fullPath)
    if ($lines.Count -eq 0) {
        continue
    }

    $hasRetiredTerm = $false
    foreach ($lineText in @($lines)) {
        foreach ($pattern in @($config.retired_terms)) {
            if ([string]$lineText -and [string]$lineText.IndexOf([string]$pattern, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
                $hasRetiredTerm = $true
                break
            }
        }
        if ($hasRetiredTerm) { break }
    }
    if (-not $hasRetiredTerm) {
        continue
    }

    $historicalRetiredTermFileCount += 1
    $header = (@($lines | Select-Object -First 20) -join "`n")
    $hasMarker = $false
    foreach ($marker in @($config.historical_markers)) {
        if ($header.IndexOf([string]$marker, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
            $hasMarker = $true
            break
        }
    }
    if ($hasMarker) {
        $historicalMarkedCount += 1
    } else {
        $findings.Add((New-Finding -Category 'historical_doc_unmarked_retired_term' -Path ([string]$relative) -Line 1 -Pattern 'historical_marker' -Text 'Historical document contains retired terms but lacks a retired/historical marker in the first 20 lines.')) | Out-Null
    }
}
```

- [ ] **Step 3: Add scan summary fields**

In the `$summary = [pscustomobject]@{ ... }` object in `vibe-routing-terminology-hard-cleanup-scan.ps1`, replace:

```powershell
historical_doc_unmarked_retired_term_count = @($findings | Where-Object { $_.category -eq 'historical_doc_unmarked_retired_term' }).Count
```

with:

```powershell
historical_doc_retired_term_file_count = [int]$historicalRetiredTermFileCount
historical_doc_marked_retired_term_count = [int]$historicalMarkedCount
historical_doc_unmarked_retired_term_count = @($findings | Where-Object { $_.category -eq 'historical_doc_unmarked_retired_term' }).Count
```

In the plain-output block, replace:

```powershell
('Historical docs without retired marker: {0}' -f [int]$summary.historical_doc_unmarked_retired_term_count)
```

with:

```powershell
('Historical docs with retired terms: {0}' -f [int]$summary.historical_doc_retired_term_file_count)
('Historical docs with retired marker: {0}' -f [int]$summary.historical_doc_marked_retired_term_count)
('Historical docs without retired marker: {0}' -f [int]$summary.historical_doc_unmarked_retired_term_count)
```

- [ ] **Step 4: Relay the widened inventory in the current routing scan**

In `scripts/verify/vibe-current-routing-contract-scan.ps1`, add these summary fields next to the existing hard-cleanup fields:

```powershell
hard_cleanup_historical_doc_retired_term_file_count = if ($hardCleanup) { [int]$hardCleanup.historical_doc_retired_term_file_count } else { 0 }
hard_cleanup_historical_doc_marked_retired_term_count = if ($hardCleanup) { [int]$hardCleanup.historical_doc_marked_retired_term_count } else { 0 }
```

In the plain-output block, add:

```powershell
('Hard cleanup historical docs with retired terms: {0}' -f [int]$summary.hard_cleanup_historical_doc_retired_term_file_count)
('Hard cleanup historical docs with retired marker: {0}' -f [int]$summary.hard_cleanup_historical_doc_marked_retired_term_count)
```

Keep the existing fail condition based on `hard_cleanup_historical_doc_unmarked_retired_term_count`, not on total historical references.

- [ ] **Step 5: Update hard-cleanup test assertions**

In `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`, after the existing JSON key assertions, add:

```python
self.assertIn("historical_doc_retired_term_file_count", payload)
self.assertIn("historical_doc_marked_retired_term_count", payload)
self.assertGreater(int(payload["historical_doc_retired_term_file_count"]), 50)
self.assertGreater(int(payload["historical_doc_marked_retired_term_count"]), 50)
self.assertEqual(0, int(payload["historical_doc_unmarked_retired_term_count"]))
```

- [ ] **Step 6: Update current routing scan test assertions**

In `tests/runtime_neutral/test_current_routing_contract_scan.py`, add these JSON assertions:

```python
self.assertIn("hard_cleanup_historical_doc_retired_term_file_count", payload)
self.assertIn("hard_cleanup_historical_doc_marked_retired_term_count", payload)
self.assertGreater(int(payload["hard_cleanup_historical_doc_retired_term_file_count"]), 50)
self.assertGreater(int(payload["hard_cleanup_historical_doc_marked_retired_term_count"]), 50)
```

Add these plain-output assertions:

```python
self.assertIn("Hard cleanup historical docs with retired terms:", completed.stdout)
self.assertIn("Hard cleanup historical docs with retired marker:", completed.stdout)
```

- [ ] **Step 7: Run the widened scan tests and confirm they fail before markers**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_historical_routing_doc_compression.py tests/runtime_neutral/test_routing_terminology_hard_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py -q
```

Expected: `FAIL` because historical files with retired terms are not yet all marked.

- [ ] **Step 8: Commit the failing widened scan**

Run:

```powershell
git add config/routing-terminology-hard-cleanup.json scripts/verify/vibe-routing-terminology-hard-cleanup-scan.ps1 scripts/verify/vibe-current-routing-contract-scan.ps1 tests/runtime_neutral/test_historical_routing_doc_compression.py tests/runtime_neutral/test_routing_terminology_hard_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py
git commit -m "test: inventory historical routing terminology docs"
```

---

### Task 3: Add Historical Summary And Compress Duplicate Governance Docs

**Files:**
- Create: `docs/governance/historical-routing-terminology.md`
- Modify: `docs/governance/binary-skill-usage-routing-2026-04-28.md`
- Modify: `docs/governance/simplified-skill-routing-2026-04-29.md`
- Modify: `docs/governance/specialist-dispatch-governance.md`
- Modify: `docs/governance/terminology-governance.md`

- [ ] **Step 1: Create the historical terminology summary**

Create `docs/governance/historical-routing-terminology.md`:

```markdown
# Historical Routing Terminology

> Historical / Retired Note: This document is an index for retired routing language. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`.

This page exists so old routing vocabulary has one small place to live. It is not
a runtime contract, and it does not add another routing layer.

## Current Contract

Current readers should start here:

- `docs/governance/current-routing-contract.md`
- `docs/governance/current-runtime-field-contract.md`

Current state names:

- `skill_candidates`
- `skill_routing.selected`
- `selected_skill_execution`
- `skill_usage.used`
- `skill_usage.unused`
- `skill_usage.evidence`

The runtime distinction is simple: a skill can be a candidate, selected for a
task slice, executed, and then counted as used only when usage evidence is
written.

## Retired Terms

These terms appear in older requirements, specs, plans, and pack-cleanup notes.
They should not be used to describe current runtime state:

| Retired wording | Current reading rule |
| --- | --- |
| `primary skill` | Read as a historical way to say one selected skill. |
| `secondary skill` | Read as a historical way to say another candidate or selected skill. |
| `route owner` | Read as historical pack-cleanup language, not a runtime status. |
| `stage assistant` | Read as historical helper-role language, not a current role. |
| `consultation` | Read as historical planning/discussion input, not current skill usage. |
| `specialist dispatch` | Read as historical execution wording, not current routing truth. |
| `specialist_recommendations` | Read as retired old-format routing data, not current input. |
| `legacy_skill_routing` | Read as retired old-format routing data, not current input. |
| `stage_assistant_hints` | Read as retired old-format helper data, not current input. |

## Preserved Rationale

The older documents remain useful for audit history because they show why the
project removed advisory/helper/primary-secondary routing states and kept a
smaller selected-versus-used model.

When editing current docs, prefer the current contract links instead of copying
old terminology back into new prose.
```

- [ ] **Step 2: Compress `binary-skill-usage-routing-2026-04-28.md`**

Replace the file with:

```markdown
# Binary Skill Usage Routing

> Historical / Retired Note: This document records the older cleanup step that separated routing from usage proof. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`.

Current readers should use:

- `docs/governance/current-routing-contract.md`
- `docs/governance/current-runtime-field-contract.md`
- `docs/governance/historical-routing-terminology.md`

## Preserved Decision

The durable decision from this document is that route selection, old
recommendation fields, consultation records, and old dispatch records do not
prove skill use.

Current usage proof must come from `skill_usage.used` with evidence. A selected
skill is not counted as used unless the runtime writes usage evidence.

## Retired Context

Older wording in this area included `specialist_recommendations`,
`stage_assistant_hints`, consultation receipts, and dispatch records. Those names
remain historical audit vocabulary only.
```

- [ ] **Step 3: Compress `simplified-skill-routing-2026-04-29.md`**

Replace the file with:

```markdown
# Simplified Skill Routing

> Historical / Retired Note: This document records the older simplification pass. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`.

Current readers should use:

- `docs/governance/current-routing-contract.md`
- `docs/governance/current-runtime-field-contract.md`
- `docs/governance/historical-routing-terminology.md`

## Preserved Decision

The durable decision from this document is that Vibe-Skills should not expose a
multi-state helper architecture to users. The current model keeps only candidate,
selected, executed, used, and unused states.

## Retired Context

Older drafts used names such as `primary skill`, `secondary skill`,
`consultation_bucket`, and helper-style routing labels. These are historical
notes, not current route states.
```

- [ ] **Step 4: Compress `specialist-dispatch-governance.md`**

Replace the file with:

```markdown
# Specialist Dispatch Governance

> Historical / Retired Note: This document records a retired execution-wording design. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`.

Current readers should use:

- `docs/governance/current-routing-contract.md`
- `docs/governance/current-runtime-field-contract.md`
- `docs/governance/historical-routing-terminology.md`

## Preserved Decision

The durable decision from this document is that execution must be tied to the
skill selected for the task slice and must not be treated as hidden advisory
activity.

Current execution language is `selected_skill_execution`, `skill_execution_units`,
and `execution_skill_outcomes`.

## Retired Context

Older wording used `specialist dispatch`, `approved_dispatch`, and related
phrases. Those names remain historical audit vocabulary only and must not be
used as current routing truth.
```

- [ ] **Step 5: Compress `terminology-governance.md`**

Replace the file with:

```markdown
# Terminology Governance

> Historical / Retired Note: This document records prior terminology cleanup. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`.

Current readers should use:

- `docs/governance/current-routing-contract.md`
- `docs/governance/current-runtime-field-contract.md`
- `docs/governance/historical-routing-terminology.md`

## Current Rule

Use current names in active docs, runtime output, tests, and user-visible
messages:

- `skill_candidates`
- `skill_routing.selected`
- `selected_skill_execution`
- `skill_usage.used`
- `skill_usage.unused`
- `skill_usage.evidence`

## Retired Context

Older wording such as `route owner`, `primary skill`, `secondary skill`,
`stage assistant`, `consultation`, `specialist_recommendations`, and
`legacy_skill_routing` is historical only. Do not copy it into current surfaces
as active design language.
```

- [ ] **Step 6: Run the focused compression guards**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_historical_routing_doc_compression.py::HistoricalRoutingDocCompressionTests::test_historical_summary_redirects_to_current_contract tests/runtime_neutral/test_historical_routing_doc_compression.py::HistoricalRoutingDocCompressionTests::test_compressed_legacy_governance_docs_are_short_redirects -q
```

Expected: `PASS`.

- [ ] **Step 7: Commit summary and compressed docs**

Run:

```powershell
git add docs/governance/historical-routing-terminology.md docs/governance/binary-skill-usage-routing-2026-04-28.md docs/governance/simplified-skill-routing-2026-04-29.md docs/governance/specialist-dispatch-governance.md docs/governance/terminology-governance.md tests/runtime_neutral/test_historical_routing_doc_compression.py
git commit -m "docs: compress retired routing terminology governance"
```

---

### Task 4: Mark Historical Files That Still Contain Retired Terms

**Files:**
- Modify every file in the list below.

- [ ] **Step 1: Insert the standard marker**

Insert this exact marker after the top H1 title in each file listed in Step 2:

```markdown
> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.
```

If a file has YAML front matter, place the marker after the first Markdown H1 heading. If a file begins without an H1, add the marker as the first nonblank line.

- [ ] **Step 2: Apply the marker to these exact files**

```text
docs/governance/absorption-admission-matrix.md
docs/governance/ai-llm-pack-consolidation-2026-04-29.md
docs/governance/aios-core-hard-removal-2026-04-29.md
docs/governance/bio-science-high-prune-2026-04-30.md
docs/governance/bio-science-problem-first-consolidation-2026-04-28.md
docs/governance/code-quality-second-pass-consolidation-2026-04-30.md
docs/governance/cold-platform-quantum-pack-deletion-2026-04-30.md
docs/governance/connector-scorecard-governance.md
docs/governance/data-ml-problem-first-consolidation-2026-04-27.md
docs/governance/design-implementation-figma-consolidation-2026-04-30.md
docs/governance/figures-reporting-stage-assistant-removal-2026-04-29.md
docs/governance/final-stage-assistant-removal-2026-04-29.md
docs/governance/finance-edgar-macro-pack-consolidation-2026-04-30.md
docs/governance/global-pack-consolidation-audit-2026-04-27.md
docs/governance/integration-devops-pack-consolidation-2026-04-29.md
docs/governance/longtail-science-ml-pack-cleanup-2026-04-30.md
docs/governance/ml-skills-pruning-candidates-2026-04-27.md
docs/governance/research-design-high-prune-2026-04-30.md
docs/governance/ruc-nlpir-augmentation-tool-pack-cleanup-2026-04-29.md
docs/governance/science-chem-drug-high-prune-2026-04-30.md
docs/governance/science-clinical-regulatory-pack-consolidation-2026-04-29.md
docs/governance/science-lab-automation-pack-consolidation-2026-04-29.md
docs/governance/science-lab-automation-pack-deletion-2026-04-30.md
docs/governance/science-literature-peer-review-consolidation-2026-04-29.md
docs/governance/science-medical-imaging-pack-consolidation-2026-04-30.md
docs/governance/vibe-governed-project-delivery-acceptance-governance.md
docs/governance/zero-route-authority-pack-consolidation-2026-04-29.md
docs/governance/zero-route-authority-second-pass-2026-04-29.md
docs/governance/zero-route-authority-third-pass-2026-04-30.md
docs/requirements/2026-03-28-root-child-vibe-hierarchy-governance.md
docs/requirements/2026-04-06-pr-127-review-fixes.md
docs/requirements/2026-04-12-vibe-discussion-time-specialist-consultation.md
docs/requirements/2026-04-13-release-v3.0.2-from-latest-main.md
docs/requirements/2026-04-15-vibe-specialist-decision-fallback.md
docs/superpowers/plans/2026-04-06-governed-entry-lineage-hardening.md
docs/superpowers/plans/2026-04-09-authoritative-governed-specialist-injection.md
docs/superpowers/plans/2026-04-10-vibe-aggressive-specialist-routing.md
docs/superpowers/plans/2026-04-12-vibe-host-stage-disclosure-protocol.md
docs/superpowers/plans/2026-04-16-canonical-vibe-runtime-entry-hardening.md
docs/superpowers/plans/2026-04-27-code-quality-pack-consolidation.md
docs/superpowers/plans/2026-04-27-data-ml-problem-first-consolidation.md
docs/superpowers/plans/2026-04-27-global-pack-consolidation-audit.md
docs/superpowers/plans/2026-04-27-ml-skills-pruning.md
docs/superpowers/plans/2026-04-27-orchestration-core-minimal-routing-cleanup.md
docs/superpowers/plans/2026-04-28-binary-skill-usage-routing.md
docs/superpowers/plans/2026-04-28-bio-science-pack-consolidation.md
docs/superpowers/plans/2026-04-28-orchestration-core-pack-consolidation.md
docs/superpowers/plans/2026-04-29-aios-core-hard-removal.md
docs/superpowers/plans/2026-04-29-figures-reporting-stage-assistant-removal.md
docs/superpowers/plans/2026-04-29-final-stage-assistant-removal.md
docs/superpowers/plans/2026-04-29-research-design-pack-consolidation.md
docs/superpowers/plans/2026-04-29-ruc-nlpir-augmentation-tool-pack-cleanup.md
docs/superpowers/plans/2026-04-29-science-communication-slides-pack-consolidation.md
docs/superpowers/plans/2026-04-29-science-lab-automation-pack-consolidation.md
docs/superpowers/plans/2026-04-29-simplified-skill-routing.md
docs/superpowers/plans/2026-04-29-zero-route-authority-pack-consolidation.md
docs/superpowers/plans/2026-04-29-zero-route-authority-second-pass.md
docs/superpowers/plans/2026-04-30-bio-science-boundary-hardening.md
docs/superpowers/plans/2026-04-30-bio-science-second-pass-consolidation.md
docs/superpowers/plans/2026-04-30-code-quality-second-pass-consolidation.md
docs/superpowers/plans/2026-04-30-cold-platform-quantum-pack-deletion.md
docs/superpowers/plans/2026-04-30-finance-edgar-macro-pack-consolidation.md
docs/superpowers/plans/2026-04-30-longtail-science-ml-pack-cleanup.md
docs/superpowers/plans/2026-04-30-research-design-boundary-hardening.md
docs/superpowers/plans/2026-04-30-science-lab-automation-pack-deletion.md
docs/superpowers/plans/2026-04-30-science-medical-imaging-pack-consolidation.md
docs/superpowers/plans/2026-04-30-terminology-field-simplification.md
docs/superpowers/plans/2026-04-30-zero-route-authority-third-pass.md
docs/superpowers/plans/2026-05-01-active-consultation-simplification.md
docs/superpowers/plans/2026-05-01-current-routing-contract-cleanup.md
docs/superpowers/plans/2026-05-01-current-routing-vocabulary-final-cleanup.md
docs/superpowers/plans/2026-05-01-execution-internal-vocabulary-cleanup.md
docs/superpowers/plans/2026-05-01-retire-old-routing-compat.md
docs/superpowers/plans/2026-05-01-routing-terminology-hard-cleanup.md
docs/superpowers/plans/2026-05-01-runtime-output-compat-naming-cleanup.md
docs/superpowers/specs/2026-04-06-governed-entry-lineage-and-child-envelope-design.md
docs/superpowers/specs/2026-04-08-vibe-discoverable-intent-entry-design.md
docs/superpowers/specs/2026-04-09-authoritative-governed-specialist-injection-design.md
docs/superpowers/specs/2026-04-16-canonical-vibe-runtime-entry-hardening-design.md
docs/superpowers/specs/2026-04-27-code-quality-pack-consolidation-design.md
docs/superpowers/specs/2026-04-27-data-ml-problem-first-consolidation-design.md
docs/superpowers/specs/2026-04-28-binary-skill-usage-routing-design.md
docs/superpowers/specs/2026-04-28-bio-science-pack-consolidation-design.md
docs/superpowers/specs/2026-04-28-orchestration-core-pack-consolidation-design.md
docs/superpowers/specs/2026-04-29-aios-core-hard-removal-design.md
docs/superpowers/specs/2026-04-29-figures-reporting-stage-assistant-removal-design.md
docs/superpowers/specs/2026-04-29-final-stage-assistant-removal-design.md
docs/superpowers/specs/2026-04-29-routing-pack-boundary-cleanup-design.md
docs/superpowers/specs/2026-04-29-ruc-nlpir-augmentation-tool-pack-cleanup-design.md
docs/superpowers/specs/2026-04-29-scholarly-publishing-pack-consolidation-design.md
docs/superpowers/specs/2026-04-29-science-chem-drug-pack-consolidation-design.md
docs/superpowers/specs/2026-04-29-science-communication-slides-pack-consolidation-design.md
docs/superpowers/specs/2026-04-29-simplified-skill-routing-design.md
docs/superpowers/specs/2026-04-29-zero-route-authority-pack-consolidation-design.md
docs/superpowers/specs/2026-04-29-zero-route-authority-second-pass-design.md
docs/superpowers/specs/2026-04-30-bio-science-boundary-hardening-design.md
docs/superpowers/specs/2026-04-30-bio-science-second-pass-consolidation-design.md
docs/superpowers/specs/2026-04-30-code-quality-second-pass-consolidation-design.md
docs/superpowers/specs/2026-04-30-cold-platform-quantum-pack-deletion-design.md
docs/superpowers/specs/2026-04-30-finance-edgar-macro-pack-consolidation-design.md
docs/superpowers/specs/2026-04-30-longtail-science-ml-pack-cleanup-design.md
docs/superpowers/specs/2026-04-30-research-design-boundary-hardening-design.md
docs/superpowers/specs/2026-04-30-science-lab-automation-pack-deletion-design.md
docs/superpowers/specs/2026-04-30-science-medical-imaging-pack-consolidation-design.md
docs/superpowers/specs/2026-04-30-terminology-field-simplification-design.md
docs/superpowers/specs/2026-04-30-zero-route-authority-third-pass-design.md
docs/superpowers/specs/2026-05-01-active-consultation-simplification-design.md
docs/superpowers/specs/2026-05-01-current-routing-contract-cleanup-design.md
docs/superpowers/specs/2026-05-01-current-routing-vocabulary-final-cleanup-design.md
docs/superpowers/specs/2026-05-01-execution-internal-vocabulary-cleanup-design.md
docs/superpowers/specs/2026-05-01-historical-routing-doc-compression-design.md
docs/superpowers/specs/2026-05-01-retire-old-routing-compat-design.md
docs/superpowers/specs/2026-05-01-routing-terminology-hard-cleanup-design.md
docs/superpowers/specs/2026-05-01-runtime-output-compat-naming-cleanup-design.md
```

- [ ] **Step 3: Run the historical scan and confirm the marker pass works**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1
```

Expected: `Gate Result: PASS`, and plain output includes:

```text
Historical docs without retired marker: 0
```

- [ ] **Step 4: Commit the marker pass**

Run:

```powershell
git add docs/governance docs/requirements docs/superpowers/plans docs/superpowers/specs
git commit -m "docs: mark historical routing terminology references"
```

---

### Task 5: Full Verification And Regression Protection

**Files:**
- No planned edits beyond narrow fixes that preserve the fixed boundaries.

- [ ] **Step 1: Run focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_historical_routing_doc_compression.py tests/runtime_neutral/test_routing_terminology_hard_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py -q
```

Expected: `PASS`.

- [ ] **Step 2: Run routing terminology gates**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-current-routing-contract-scan.ps1
```

Expected: both scripts print `Gate Result: PASS`. The current routing scan may still report a nonzero `historical_reference_count`; that count is informational.

- [ ] **Step 3: Run behavior gates that prove no route/runtime regression**

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-governed-runtime-contract-gate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-runtime-execution-proof-gate.ps1
```

Expected:

```text
Gate Result: PASS
```

for each gate that prints a gate result. `vibe-pack-routing-smoke.ps1` should report all routing smoke cases passing.

- [ ] **Step 4: Clean generated untracked runtime artifacts**

Run:

```powershell
git status --short
```

If `.vibeskills/` appears as an untracked generated artifact under the repository root, remove only that generated folder:

```powershell
Remove-Item -LiteralPath .\.vibeskills -Recurse -Force
```

Run:

```powershell
git status --short
```

Expected: no untracked `.vibeskills/` remains.

- [ ] **Step 5: Run whitespace check**

Run:

```powershell
git diff --check
```

Expected: no output and exit code `0`.

- [ ] **Step 6: Commit final narrow fixes**

If verification required narrow doc/test/scan fixes, run:

```powershell
git add config scripts/verify tests/runtime_neutral docs/governance docs/requirements docs/superpowers/plans docs/superpowers/specs
git commit -m "fix: stabilize historical routing doc compression"
```

If Step 1 through Step 5 pass with no file changes, skip this commit and record the clean verification in the execution summary.

---

## Acceptance Checklist

- [ ] Current routing remains `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`.
- [ ] No runtime script adds back old-format routing compatibility.
- [ ] No six-stage runtime behavior changes.
- [ ] `docs/governance/historical-routing-terminology.md` exists and redirects to the current contracts.
- [ ] The four high-duplication legacy governance docs are short redirects with preserved decisions.
- [ ] Root-based historical scan covers `docs/governance`, `docs/requirements`, `docs/superpowers/plans`, and `docs/superpowers/specs`.
- [ ] Historical files with retired terms have `Historical / Retired Note` in the first 20 lines.
- [ ] `historical_doc_unmarked_retired_term_count = 0`.
- [ ] `current_surface_violation_count = 0`.
- [ ] `current_runtime_old_format_fallback_count = 0`.
- [ ] `hard_cleanup_current_doc_retired_term_violation_count = 0`.
- [ ] `hard_cleanup_current_behavior_test_retired_field_read_count = 0`.
- [ ] `hard_cleanup_current_policy_helper_dispatch_vocabulary_reference_count = 0`.
- [ ] Pack routing smoke still passes.
- [ ] Governed runtime contract gate still passes.
- [ ] Runtime execution proof gate still passes.
- [ ] `git diff --check` passes.

---

## Rollback Plan

Use commits as rollback units. Do not use `git reset --hard`.

If root-based scanning is too broad:

```powershell
git revert <scan-commit>
```

If marker insertion makes docs noisy:

```powershell
git revert <marker-commit>
```

If compressed governance docs lose needed rationale:

```powershell
git revert <compression-commit>
```

After any revert, run:

```powershell
python -m pytest tests/runtime_neutral/test_current_routing_vocabulary_final_cleanup.py tests/runtime_neutral/test_current_routing_contract_scan.py -q
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-current-routing-contract-scan.ps1
git diff --check
```
