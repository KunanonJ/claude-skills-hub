# Orchestration-Core Hard Removal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove `orchestration-core` as an active scheduling pack, keep `$vibe` as the only governed runtime entry, and preserve `resolve-pack-route.ps1` only as an internal specialist recommendation mechanism.

**Architecture:** This is a routing-governance migration, not a physical skill-directory deletion. The implementation first adds a failing hard-removal gate, then removes the active pack, narrows compatibility routing, updates runtime terminology, folds process-method recommendations into `vibe` stages, and rewrites tests/goldens that still expect `selected_pack = orchestration-core`.

**Tech Stack:** PowerShell router and runtime scripts, JSON routing configuration, Python pytest runtime-neutral tests, Markdown runtime/governance docs, Vibe-Skills verification gates.

---

## File Structure

- Create: `scripts/verify/vibe-orchestration-core-hard-removal-gate.ps1`
  - Focused gate proving `orchestration-core` is no longer an active pack and no route result exposes it.
- Replace: `scripts/verify/vibe-orchestration-core-consolidation-gate.ps1`
  - Convert the old consolidation gate into a thin compatibility wrapper that calls the hard-removal gate.
- Modify: `config/pack-manifest.json`
  - Remove the active `orchestration-core` pack.
  - Add a narrow `workflow-compatibility` pack only for explicit `spec-kit-vibe-compat` routing.
- Modify: `config/retrieval-intent-profiles.json`
  - Remove `orchestration-core` from all `recommended_packs`.
  - Remove process-method skills from `recommended_skills` where they would recreate the old routing surface.
- Modify: `config/capability-catalog.json`
  - Map `brainstorm_planning` and `multi_agent_orchestration` to `vibe` as the governed capability owner instead of recommending `brainstorming`, `writing-plans`, or `subagent-driven-development` as active specialists.
- Modify: `config/runtime-input-packet-policy.json`
  - Remove `writing-plans` and `brainstorming` from fallback specialist recommendations.
- Modify: `config/runtime-contract.json`
  - Add explicit `internal_specialist_recommender` metadata while keeping the existing `canonical_router` key as a backward-compatible packet field.
- Modify: `SKILL.md`
  - Rename human-facing "Canonical router" language to "Internal specialist recommendation router".
- Modify: `core/skills/vibe/instruction.md`
  - State that `vibe` is authoritative and the router is only an internal specialist recommender.
- Modify: `protocols/runtime.md`
  - Rewrite key terms, priority rules, router integration, and authority boundary language.
- Modify: `protocols/think.md`
  - Remove external `brainstorming` / `writing-plans` tool ownership from Vibe planning stages and describe the native stage methods.
- Modify: `protocols/team.md`
  - Clarify that subagent development is a `plan_execute` topology, not a route-owning skill.
- Modify: `scripts/router/README.md`
  - Describe `resolve-pack-route.ps1` as a specialist recommendation surface, not the public entry.
- Modify: `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
  - Change user-facing error/reason strings from "canonical router" to "internal specialist recommender".
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`
  - Add a `role = internal_specialist_recommender` field under the existing `canonical_router` packet object for compatibility.
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`
  - Replace orchestration-core positive cases with blocked-pack assertions and a `workflow-compatibility/spec-kit-vibe-compat` explicit case.
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
  - Add blocked-pack support and replace old `orchestration-core` expected cases.
- Modify: `scripts/verify/vibe-routing-stability-gate.ps1`
  - Rename the orchestration planning group to a no-core regression group.
- Modify: `scripts/verify/vibe-pack-routing-smoke.ps1`
  - Remove `orchestration-core` from expected active packs and add `workflow-compatibility`.
- Modify: `scripts/verify/vibe-keyword-precision-audit.ps1`
  - Remove `orchestration-core` from pack precision coverage and add explicit spec-kit compatibility coverage.
- Modify: `scripts/verify/vibe-external-corpus-gate.ps1`
  - Replace generic workflow orchestration expectations with no-core assertions or domain-specific expected packs.
- Modify: `scripts/verify/vibe-openspec-governance-gate.ps1`
  - Replace `orchestration-core` expected pack assertions with `workflow-compatibility` for explicit spec-kit routes and no-core assertions for governance advice.
- Modify: `tests/runtime_neutral/test_router_bridge.py`
  - Update tests that expect requested `vibe` or wrapper entries to select `orchestration-core`.
- Modify: `tests/runtime_neutral/test_structured_bounded_reentry_continuation.py`
  - Update stubs that force `selected_pack = orchestration-core`.
- Modify: `tests/unit/test_router_contract_selection_guards.py`
  - Rename the synthetic pack id from `orchestration-core` to `synthetic-process-pack`.
- Modify: route replay fixtures under `tests/replay/route/`
  - Replace `selected_pack: orchestration-core` with new expected no-core or compatibility values.
- Modify: reference fixtures under `references/fixtures/`
  - Update fixture outputs so docs and gates no longer advertise `orchestration-core`.
- Create: `docs/governance/orchestration-core-hard-removal-2026-04-28.md`
  - Records the hard-removal decision, migrated method ownership, verification commands, and non-deletion caveat.

---

### Task 1: Add A Failing Hard-Removal Gate

**Files:**
- Create: `scripts/verify/vibe-orchestration-core-hard-removal-gate.ps1`
- Verify: `config/pack-manifest.json`
- Verify: `config/retrieval-intent-profiles.json`
- Verify: `SKILL.md`
- Verify: `protocols/runtime.md`
- Verify: `config/runtime-contract.json`

- [ ] **Step 1: Create the hard-removal gate**

Create `scripts/verify/vibe-orchestration-core-hard-removal-gate.ps1` with this content:

```powershell
param()

$ErrorActionPreference = "Stop"

function Assert-True {
    param(
        [bool]$Condition,
        [string]$Message,
        [string]$Details = ""
    )

    if ($Condition) {
        Write-Host "[PASS] $Message"
        return $true
    }

    if ($Details) {
        Write-Host "[FAIL] $Message - $Details" -ForegroundColor Red
    } else {
        Write-Host "[FAIL] $Message" -ForegroundColor Red
    }
    return $false
}

function Read-Json {
    param([Parameter(Mandatory)] [string]$Path)
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Invoke-Route {
    param(
        [Parameter(Mandatory)] [string]$Prompt,
        [Parameter(Mandatory)] [string]$Grade,
        [Parameter(Mandatory)] [string]$TaskType,
        [AllowEmptyString()] [string]$RequestedSkill = ""
    )

    $repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
    $resolver = Join-Path $repoRoot "scripts\router\resolve-pack-route.ps1"
    $args = @{
        Prompt = $Prompt
        Grade = $Grade
        TaskType = $TaskType
    }
    if (-not [string]::IsNullOrWhiteSpace($RequestedSkill)) {
        $args.RequestedSkill = $RequestedSkill
    }
    return (& $resolver @args | ConvertFrom-Json)
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$manifest = Read-Json -Path (Join-Path $repoRoot "config\pack-manifest.json")
$retrievalProfiles = Read-Json -Path (Join-Path $repoRoot "config\retrieval-intent-profiles.json")
$runtimeContract = Read-Json -Path (Join-Path $repoRoot "config\runtime-contract.json")
$skillMd = Get-Content -LiteralPath (Join-Path $repoRoot "SKILL.md") -Raw -Encoding UTF8
$runtimeProtocol = Get-Content -LiteralPath (Join-Path $repoRoot "protocols\runtime.md") -Raw -Encoding UTF8

$results = @()

$activePackIds = @($manifest.packs | ForEach-Object { [string]$_.id })
$results += Assert-True -Condition (-not ($activePackIds -contains "orchestration-core")) -Message "active pack-manifest no longer contains orchestration-core" -Details ("packs={0}" -f ($activePackIds -join ", "))
$results += Assert-True -Condition ($activePackIds -contains "workflow-compatibility") -Message "explicit compatibility pack exists"

$recommendedPacks = @(
    $retrievalProfiles.profiles |
        ForEach-Object { @($_.recommended_packs | ForEach-Object { [string]$_ }) }
)
$results += Assert-True -Condition (-not ($recommendedPacks -contains "orchestration-core")) -Message "retrieval profiles do not recommend orchestration-core"

$results += Assert-True -Condition ($runtimeContract.authority.PSObject.Properties.Name -contains "internal_specialist_recommender") -Message "runtime contract names internal specialist recommender"
$results += Assert-True -Condition ([string]$runtimeContract.authority.internal_specialist_recommender -eq "scripts/router/resolve-pack-route.ps1") -Message "internal specialist recommender points at resolve-pack-route.ps1"
$results += Assert-True -Condition ($runtimeContract.authority.PSObject.Properties.Name -contains "canonical_router") -Message "runtime contract keeps canonical_router compatibility field"

$results += Assert-True -Condition ($skillMd -match "Internal specialist recommendation router") -Message "SKILL.md uses internal specialist recommendation router wording"
$results += Assert-True -Condition ($skillMd -notmatch "(?m)^\s*Canonical router:") -Message "SKILL.md no longer labels router as the canonical entry"
$results += Assert-True -Condition ($runtimeProtocol -match "Internal specialist recommender") -Message "runtime protocol defines internal specialist recommender"
$results += Assert-True -Condition ($runtimeProtocol -notmatch "Canonical router authority stays intact") -Message "runtime protocol no longer gives router authority priority over vibe"

$blockedRoutes = @(
    [pscustomobject]@{ Name = "generic planning ZH"; Prompt = "请输出实施计划和任务拆解"; Grade = "L"; TaskType = "planning" },
    [pscustomobject]@{ Name = "generic brainstorming ZH"; Prompt = "先做头脑风暴，发散方案"; Grade = "L"; TaskType = "planning" },
    [pscustomobject]@{ Name = "generic subagent ZH"; Prompt = "把任务拆成多个子代理并行执行"; Grade = "XL"; TaskType = "planning" }
)

foreach ($case in $blockedRoutes) {
    $route = Invoke-Route -Prompt $case.Prompt -Grade $case.Grade -TaskType $case.TaskType
    $selectedPack = if ($route.selected) { [string]$route.selected.pack_id } else { "" }
    $rankedPackIds = @($route.ranked | ForEach-Object { [string]$_.pack_id })
    $confirmPack = if ($route.confirm_ui) { [string]$route.confirm_ui.pack_id } else { "" }
    $results += Assert-True -Condition ($selectedPack -ne "orchestration-core") -Message "[$($case.Name)] selected pack is not orchestration-core" -Details ("selected={0}/{1}" -f $selectedPack, $(if ($route.selected) { [string]$route.selected.skill } else { "" }))
    $results += Assert-True -Condition (-not ($rankedPackIds -contains "orchestration-core")) -Message "[$($case.Name)] ranked packs exclude orchestration-core" -Details ("ranked={0}" -f ($rankedPackIds -join ", "))
    $results += Assert-True -Condition ($confirmPack -ne "orchestration-core") -Message "[$($case.Name)] confirm UI does not expose orchestration-core"
}

$specRoute = Invoke-Route -Prompt "/speckit.plan 生成技术计划" -Grade "L" -TaskType "planning"
$results += Assert-True -Condition ([string]$specRoute.selected.pack_id -eq "workflow-compatibility") -Message "explicit speckit route uses workflow-compatibility" -Details ("selected={0}/{1}" -f $specRoute.selected.pack_id, $specRoute.selected.skill)
$results += Assert-True -Condition ([string]$specRoute.selected.skill -eq "spec-kit-vibe-compat") -Message "explicit speckit route selects spec-kit-vibe-compat"

$passCount = @($results | Where-Object { $_ }).Count
$failCount = @($results | Where-Object { -not $_ }).Count
$total = @($results).Count

Write-Host ""
Write-Host "=== Orchestration-Core Hard Removal Summary ==="
Write-Host "Total assertions: $total"
Write-Host "Passed: $passCount"
Write-Host "Failed: $failCount"

if ($failCount -gt 0) {
    exit 1
}
```

- [ ] **Step 2: Run the hard-removal gate and confirm current failure**

Run:

```powershell
.\scripts\verify\vibe-orchestration-core-hard-removal-gate.ps1
```

Expected now: FAIL. At minimum, it should report that active `orchestration-core` still exists and generic planning routes still expose it.

- [ ] **Step 3: Commit the failing gate**

Run:

```powershell
git add -- scripts/verify/vibe-orchestration-core-hard-removal-gate.ps1
git commit -m "test: add orchestration core hard removal gate"
```

---

### Task 2: Rename Router Semantics Without Breaking Packet Fields

**Files:**
- Modify: `SKILL.md`
- Modify: `core/skills/vibe/instruction.md`
- Modify: `protocols/runtime.md`
- Modify: `scripts/router/README.md`
- Modify: `config/runtime-contract.json`
- Modify: `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- Modify: `scripts/runtime/VibeRuntime.Common.ps1`

- [ ] **Step 1: Update `SKILL.md` launch wording**

In `SKILL.md`, replace:

```markdown
Canonical router: `scripts/router/resolve-pack-route.ps1`
```

with:

```markdown
Internal specialist recommendation router: `scripts/router/resolve-pack-route.ps1`
```

Also replace this sentence:

```markdown
Canonical router: `scripts/router/resolve-pack-route.ps1`
```

in the Maintenance section with:

```markdown
Internal specialist recommendation router: `scripts/router/resolve-pack-route.ps1`
```

- [ ] **Step 2: Update `SKILL.md` router input heading**

Replace:

```markdown
Router input rules:
```

with:

```markdown
Specialist recommender input rules:
```

Then add this sentence immediately below the heading:

```markdown
This recommender runs inside canonical `vibe`; it may suggest specialist skills, but it does not decide whether `$vibe` is the public runtime entry.
```

- [ ] **Step 3: Update `core/skills/vibe/instruction.md`**

Replace this bullet:

```markdown
- the canonical router remains authoritative
```

with:

```markdown
- `vibe` remains the runtime authority; the internal specialist recommender only suggests bounded specialist help
```

Replace this bullet:

```markdown
- provider-assisted intelligence may advise but must not replace route authority
```

with:

```markdown
- provider-assisted intelligence may advise but must not replace `vibe` runtime authority
```

- [ ] **Step 4: Rewrite `protocols/runtime.md` key terms and priorities**

In `protocols/runtime.md`, replace the key term:

```markdown
> - **Canonical router**: The internal logic that picks which skill handles your task.
```

with:

```markdown
> - **Internal specialist recommender**: The internal logic that suggests bounded specialist help after `vibe` is already the runtime authority.
```

Replace:

```markdown
It does not replace the canonical router.
It defines what must happen after `vibe` is selected.
```

with:

```markdown
It does not create a second router or second runtime surface.
It defines what must happen after `$vibe` enters the governed runtime.
```

Replace priority item 1:

```markdown
1. Canonical router authority stays intact.
```

with:

```markdown
1. `vibe` runtime authority stays intact.
```

- [ ] **Step 5: Rewrite `protocols/runtime.md` router integration and authority boundary**

Replace the `## Router Integration Rules` bullet block with:

```markdown
## Specialist Recommender Integration Rules

- specialist recommendation logic remains in `scripts/router/resolve-pack-route.ps1`
- `confirm_required` stays on the existing white-box confirm surface when specialist choice needs host confirmation
- unattended routing is interpreted as a governed runtime mode choice, not as a second runtime
- provider-backed intelligence remains advice-only
- fallback or degraded paths must emit an explicit hazard alert rather than a silent warning
- fallback or degraded paths must downgrade runtime truth to `non_authoritative`
```

Replace this ownership list:

```markdown
- canonical router: route selection authority
- VCO governed runtime: stage order, requirement freeze, plan traceability, execution receipts, cleanup receipts
- host bridge: hidden governance context attachment and host-hook wiring only
- superpowers and similar process layers: workflow discipline only
```

with:

```markdown
- VCO governed runtime: public entry, stage order, requirement freeze, plan traceability, execution receipts, cleanup receipts
- internal specialist recommender: bounded specialist suggestions inside the governed runtime
- host bridge: hidden governance context attachment and host-hook wiring only
- process-method layers: workflow discipline only, never a second runtime surface
```

- [ ] **Step 6: Update `scripts/router/README.md`**

Replace:

```markdown
`scripts/router/` 保存 VCO 路由决策面：pack route 解析、legacy compatibility、以及为 router 提供的模块化 helper。
```

with:

```markdown
`scripts/router/` 保存 VCO 内部专家推荐面：pack / skill recommendation、legacy compatibility、以及为 specialist recommender 提供的模块化 helper。公开治理入口仍然是 `$vibe` / `/vibe`。
```

Replace the `resolve-pack-route.ps1` row with:

```markdown
| [`resolve-pack-route.ps1`](resolve-pack-route.ps1) | 内部专家推荐入口；产出 pack / skill recommendation、overlay advice 与 confirm-required 信息 |
```

Replace the first rule bullet with:

```markdown
- router 目录解释“如何生成专家推荐结果”；公开执行、阶段治理与验证仍分别落到 `SKILL.md`、`protocols/`、`scripts/governance/` 与 `scripts/verify/`。
```

- [ ] **Step 7: Extend `config/runtime-contract.json` with explicit recommender metadata**

In `config/runtime-contract.json`, replace the `authority` object:

```json
  "authority": {
    "canonical_router": "scripts/router/resolve-pack-route.ps1",
    "runtime_protocol": "protocols/runtime.md",
    "forbid_second_router": true
  },
```

with:

```json
  "authority": {
    "internal_specialist_recommender": "scripts/router/resolve-pack-route.ps1",
    "canonical_router": "scripts/router/resolve-pack-route.ps1",
    "canonical_router_compatibility": "legacy packet field name only; runtime authority remains vibe",
    "runtime_protocol": "protocols/runtime.md",
    "forbid_second_router": true
  },
```

Keep `canonical_router` because runtime packet validation still expects that field name.

- [ ] **Step 8: Update runtime script messages**

In `scripts/runtime/Freeze-RuntimeInputPacket.ps1`, replace:

```powershell
throw ("Failed to freeze runtime input packet because canonical router exited with code {0}." -f [int]$routeInvocation.exit_code)
```

with:

```powershell
throw ("Failed to freeze runtime input packet because internal specialist recommender exited with code {0}." -f [int]$routeInvocation.exit_code)
```

Replace:

```powershell
-Reason 'canonical router selected a specialist candidate for governed bounded execution' `
```

with:

```powershell
-Reason 'internal specialist recommender selected a bounded specialist candidate for governed execution' `
```

- [ ] **Step 9: Add recommender role metadata to runtime input packet**

In `scripts/runtime/VibeRuntime.Common.ps1`, inside the `canonical_router = [pscustomobject]@{` object, add this first property:

```powershell
            role = 'internal_specialist_recommender'
```

Then replace:

```powershell
source_of_truth = 'canonical_router_shadow_freeze'
```

with:

```powershell
source_of_truth = 'vibe_runtime_with_internal_specialist_recommender'
```

- [ ] **Step 10: Run focused terminology checks**

Run:

```powershell
rg -n "Canonical router:|Canonical router authority stays intact|canonical router selected|because canonical router exited" SKILL.md protocols scripts/runtime core/skills/vibe
```

Expected: no matches.

Run:

```powershell
rg -n "internal specialist" SKILL.md protocols scripts/runtime core/skills/vibe config/runtime-contract.json
```

Expected: matches in the files changed above.

- [ ] **Step 11: Commit terminology and runtime metadata**

Run:

```powershell
git add -- SKILL.md core/skills/vibe/instruction.md protocols/runtime.md scripts/router/README.md config/runtime-contract.json scripts/runtime/Freeze-RuntimeInputPacket.ps1 scripts/runtime/VibeRuntime.Common.ps1
git commit -m "refactor: rename router authority to specialist recommender"
```

---

### Task 3: Remove Active `orchestration-core` Routing And Add Narrow Compatibility

**Files:**
- Modify: `config/pack-manifest.json`
- Modify: `config/retrieval-intent-profiles.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`

- [ ] **Step 1: Remove the active `orchestration-core` object**

In `config/pack-manifest.json`, remove the entire first pack object whose id is:

```json
"id": "orchestration-core"
```

This is the object that currently has:

```json
"priority": 100
```

and candidates:

```json
[
  "brainstorming",
  "writing-plans",
  "subagent-driven-development",
  "context-hunter",
  "think-harder",
  "dialectic",
  "local-vco-roles",
  "spec-kit-vibe-compat"
]
```

- [ ] **Step 2: Add the narrow explicit compatibility pack**

In `config/pack-manifest.json`, insert this pack object immediately after `aios-core`:

```json
{
  "id": "workflow-compatibility",
  "priority": 89,
  "grade_allow": [
    "M",
    "L",
    "XL"
  ],
  "task_allow": [
    "planning",
    "coding",
    "review",
    "debug",
    "research"
  ],
  "trigger_keywords": [
    "/speckit",
    "speckit",
    "speckit.",
    "spec-kit",
    ".specify"
  ],
  "skill_candidates": [
    "spec-kit-vibe-compat"
  ],
  "route_authority_candidates": [
    "spec-kit-vibe-compat"
  ],
  "stage_assistant_candidates": [],
  "defaults_by_task": {}
}
```

Expected behavior: `/speckit.plan 生成技术计划` can still route to compatibility, but generic `计划` / `方案` / `规划` no longer routes through a core pack.

- [ ] **Step 3: Remove `orchestration-core` from retrieval profiles**

In `config/retrieval-intent-profiles.json`, update these arrays:

For `repo_code`, replace:

```json
"recommended_packs": [
  "integration-devops",
  "orchestration-core",
  "code-quality"
]
```

with:

```json
"recommended_packs": [
  "integration-devops",
  "code-quality"
]
```

For `doc_api`, replace:

```json
"recommended_packs": [
  "ai-llm",
  "integration-devops",
  "orchestration-core"
]
```

with:

```json
"recommended_packs": [
  "ai-llm",
  "integration-devops"
]
```

For `composite`, replace:

```json
"recommended_packs": [
  "orchestration-core",
  "research-design",
  "integration-devops"
]
```

with:

```json
"recommended_packs": [
  "research-design",
  "integration-devops",
  "code-quality"
]
```

Also replace:

```json
"recommended_skills": [
  "vibe",
  "brainstorming",
  "verification-before-completion"
]
```

with:

```json
"recommended_skills": [
  "vibe",
  "verification-before-completion"
]
```

- [ ] **Step 4: Remove inactive process-method keyword entries**

In `config/skill-keyword-index.json`, remove these `skills` entries:

```json
"brainstorming": {
  "keywords": ["brainstorm", "ideation", "头脑风暴", "方案发散", "创意讨论", "比较几个方案", "比较几个方向"]
},
"writing-plans": {
  "keywords": ["implementation plan", "task breakdown", "execution plan", "milestone roadmap", "migration plan", "governance rollout", "rollout plan", "runbook", "wave plan", "cross-module migration", "routing governance", "计划书", "实施计划", "执行计划", "任务拆解", "里程碑规划", "迁移计划"]
},
"subagent-driven-development": {
  "keywords": ["subagent", "parallel agents", "multi-agent", "independent tasks", "子代理", "多代理", "并行执行", "拆成多个代理", "多个 agent"]
},
```

Keep `spec-kit-vibe-compat` because it is used by `workflow-compatibility`.

- [ ] **Step 5: Remove inactive process-method routing rules**

In `config/skill-routing-rules.json`, remove these top-level `skills` entries:

```json
"brainstorming": { ... },
"writing-plans": { ... },
"subagent-driven-development": { ... },
```

Keep `spec-kit-vibe-compat` and its existing:

```json
"requires_positive_keyword_match": true
```

If the current `spec-kit-vibe-compat` entry lacks that field, add:

```json
"requires_positive_keyword_match": true
```

- [ ] **Step 6: Validate JSON parsing**

Run:

```powershell
@(
  'config/pack-manifest.json',
  'config/retrieval-intent-profiles.json',
  'config/skill-keyword-index.json',
  'config/skill-routing-rules.json'
) | ForEach-Object {
  Get-Content -LiteralPath $_ -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
  Write-Host "[PASS] JSON parses: $_"
}
```

Expected: four `[PASS]` lines.

- [ ] **Step 7: Run the hard-removal gate**

Run:

```powershell
.\scripts\verify\vibe-orchestration-core-hard-removal-gate.ps1
```

Expected after this task: the static pack and retrieval assertions pass. Route assertions may still fail until test/golden updates are complete if other route surfaces still expose stale `orchestration-core`.

- [ ] **Step 8: Commit routing config migration**

Run:

```powershell
git add -- config/pack-manifest.json config/retrieval-intent-profiles.json config/skill-keyword-index.json config/skill-routing-rules.json
git commit -m "feat: remove orchestration core active routing"
```

---

### Task 4: Fold Process Methods Into `vibe` Stage Semantics

**Files:**
- Modify: `config/capability-catalog.json`
- Modify: `config/runtime-input-packet-policy.json`
- Modify: `protocols/think.md`
- Modify: `protocols/team.md`

- [ ] **Step 1: Make `brainstorm_planning` Vibe-owned in the capability catalog**

In `config/capability-catalog.json`, find capability id:

```json
"id": "brainstorm_planning"
```

Replace its `skills` array:

```json
"skills": [
  "brainstorming",
  "writing-plans",
  "create-plan",
  "vibe"
]
```

with:

```json
"skills": [
  "vibe"
]
```

Replace its `materialization` object:

```json
"materialization": {
  "mode": "runtime_recommendation",
  "canonical_owner": "config/pack-manifest.json",
  "runtime_surface": "vco-native",
  "promotion_stage": "soft"
}
```

with:

```json
"materialization": {
  "mode": "vibe_stage_method",
  "canonical_owner": "protocols/think.md",
  "runtime_surface": "vibe.deep_interview.xl_plan",
  "promotion_stage": "absorbed"
}
```

- [ ] **Step 2: Make `multi_agent_orchestration` Vibe-owned in the capability catalog**

In the same file, find capability id:

```json
"id": "multi_agent_orchestration"
```

Replace its `skills` array:

```json
"skills": [
  "vibe",
  "subagent-driven-development",
  "hive-mind-advanced",
  "local-vco-roles"
]
```

with:

```json
"skills": [
  "vibe"
]
```

Replace its `materialization` object with:

```json
"materialization": {
  "mode": "vibe_stage_method",
  "canonical_owner": "protocols/team.md",
  "runtime_surface": "vibe.plan_execute",
  "promotion_stage": "absorbed"
}
```

- [ ] **Step 3: Remove process-method fallback specialists**

In `config/runtime-input-packet-policy.json`, replace:

```json
"fallback_specialists_by_task_type": {
  "planning": [
    "writing-plans"
  ],
  "debug": [
    "systematic-debugging"
  ],
  "research": [
    "brainstorming"
  ],
  "coding": [
    "test-driven-development"
  ],
  "review": [
    "requesting-code-review"
  ],
  "default": [
    "writing-plans"
  ]
}
```

with:

```json
"fallback_specialists_by_task_type": {
  "planning": [],
  "debug": [
    "systematic-debugging"
  ],
  "research": [],
  "coding": [
    "test-driven-development"
  ],
  "review": [
    "requesting-code-review"
  ],
  "default": []
}
```

- [ ] **Step 4: Update `protocols/think.md` Phase A tool table**

Replace this table:

```markdown
| Estimated Grade | Tool | Source |
|----------------|------|--------|
| M | claude-code-settings:think-harder | 4-phase analysis |
| L | claude-code-settings:think-ultra | 7-phase analysis |
| XL | superpowers:brainstorming | Socratic dialogue |
| Any | sc:analyze | Code-focused analysis |
```

with:

```markdown
| Estimated Grade | Native Vibe Method | Stage |
|----------------|--------------------|-------|
| M | concise risk and objective check | `deep_interview` |
| L | structured options, constraints, and acceptance criteria | `deep_interview` -> `requirement_doc` |
| XL | Socratic clarification plus explicit tradeoff comparison | `deep_interview` -> `xl_plan` |
| Any code-heavy case | repository evidence probe before plan text | `skeleton_check` -> `xl_plan` |
```

- [ ] **Step 5: Update `protocols/think.md` compound decomposition table**

Replace this table:

```markdown
| Grade | Tool | Source |
|-------|------|--------|
| M | everything-claude-code:planner agent | Everything-CC |
| L | superpowers:writing-plans | Superpowers |
| XL | ruflo workflow_create | Claude-flow |
```

with:

```markdown
| Grade | Native Vibe Method | Stage |
|-------|--------------------|-------|
| M | short serial checklist | `xl_plan` |
| L | phase plan with owners, verification, and rollback notes | `xl_plan` |
| XL | wave-sequential plan with bounded parallel windows | `xl_plan` -> `plan_execute` |
```

- [ ] **Step 6: Replace external tool lines in `protocols/think.md`**

Replace:

```markdown
Tool: superpowers:brainstorming
- Socratic dialogue pattern
- HARD-GATE: No implementation until design is approved
- Output: Clarified requirements, user stories, acceptance criteria
```

with:

```markdown
Native method: `vibe.deep_interview`
- ask one high-value clarification when ambiguity blocks requirement quality
- compare options before choosing an implementation direction
- output clarified requirements, assumptions, acceptance criteria, and user-visible tradeoffs
```

Replace:

```markdown
Tool: superpowers:writing-plans
```

with:

```markdown
Native method: `vibe.xl_plan`
```

Replace:

```markdown
- Do NOT invoke both brainstorming systems simultaneously
- think-harder/think-ultra = problem analysis, brainstorming = requirements discovery
```

with:

```markdown
- Do not create a second requirement or plan surface outside the active `vibe` session
- deep analysis, option comparison, and plan writing are native methods inside `deep_interview` and `xl_plan`
```

- [ ] **Step 7: Update `protocols/team.md` subagent boundary**

After:

```markdown
This protocol only activates after the requirement and plan are already frozen.
```

add:

```markdown
`subagent-driven-development` is treated as an absorbed method here, not as a route-owning specialist. The decision to use child lanes belongs to `vibe.plan_execute` and must follow the frozen M/L/XL plan.
```

Replace:

```markdown
- Specialist routing is expected on governed runs, and eligible bounded specialist recommendations should become executable dispatch by default.
```

with:

```markdown
- Specialist recommendations are expected on governed runs, but process methods such as brainstorming, planning, and child-lane decomposition are owned by `vibe` stages rather than external route authorities.
```

- [ ] **Step 8: Validate JSON and protocol text**

Run:

```powershell
Get-Content -LiteralPath config/capability-catalog.json -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
Get-Content -LiteralPath config/runtime-input-packet-policy.json -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
rg -n "superpowers:brainstorming|superpowers:writing-plans|subagent-driven-development is treated" protocols/think.md protocols/team.md
```

Expected:

- JSON parsing succeeds.
- `superpowers:brainstorming` and `superpowers:writing-plans` have no matches in `protocols/think.md`.
- `subagent-driven-development is treated` has one match in `protocols/team.md`.

- [ ] **Step 9: Commit Vibe stage absorption**

Run:

```powershell
git add -- config/capability-catalog.json config/runtime-input-packet-policy.json protocols/think.md protocols/team.md
git commit -m "refactor: absorb process methods into vibe stages"
```

---

### Task 5: Rewrite Pack Regression And Skill Index Gates

**Files:**
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
- Replace: `scripts/verify/vibe-orchestration-core-consolidation-gate.ps1`

- [ ] **Step 1: Replace old orchestration cases in pack regression matrix**

In `scripts/verify/vibe-pack-regression-matrix.ps1`, replace the first eight `orchestration ...` cases with:

```powershell
    [pscustomobject]@{ Name = "generic planning no orchestration core EN"; Prompt = "create implementation plan and task breakdown with milestones"; Grade = "L"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "orchestration-core"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "generic planning no orchestration core ZH"; Prompt = "请给我实施计划和任务拆解"; Grade = "L"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "orchestration-core"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "generic brainstorming no orchestration core ZH"; Prompt = "先做头脑风暴，比较几个方案"; Grade = "L"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "orchestration-core"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "generic subagent no orchestration core ZH"; Prompt = "把任务拆成多个子代理并行执行"; Grade = "XL"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = $null; BlockedPack = "orchestration-core"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "generic coding M not subagent"; Prompt = "实现这个功能并修改代码"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = $null; BlockedSkill = "subagent-driven-development"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "generic coding L not subagent"; Prompt = "实现这个功能并修改代码"; Grade = "L"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = $null; BlockedSkill = "subagent-driven-development"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "generic coding XL not silent subagent"; Prompt = "实现这个功能并修改代码"; Grade = "XL"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = $null; BlockedSkill = "subagent-driven-development"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
    [pscustomobject]@{ Name = "explicit speckit compatibility"; Prompt = "/speckit.plan 生成技术计划"; Grade = "L"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = "workflow-compatibility"; ExpectedSkill = "spec-kit-vibe-compat"; AllowedModes = @("pack_overlay", "confirm_required", "legacy_fallback") },
```

- [ ] **Step 2: Add `BlockedPack` support to skill index audit**

In `scripts/verify/vibe-skill-index-routing-audit.ps1`, after the `ExpectedSkill` assertions in the loop, add:

```powershell
    if ($case.PSObject.Properties.Name -contains "BlockedPack" -and $case.BlockedPack) {
        $results += Assert-True -Condition ($route.selected.pack_id -ne $case.BlockedPack) -Message "[$($case.Name)] blocked pack $($case.BlockedPack) not selected"
    }

    if ($case.PSObject.Properties.Name -contains "BlockedSkill" -and $case.BlockedSkill) {
        $results += Assert-True -Condition ($route.selected.skill -ne $case.BlockedSkill) -Message "[$($case.Name)] blocked skill $($case.BlockedSkill) not selected"
    }
```

Then wrap the existing expected pack/skill assertions so they only run when expected fields are present:

```powershell
    if ($case.PSObject.Properties.Name -contains "ExpectedPack" -and $case.ExpectedPack) {
        $results += Assert-True -Condition ($route.selected.pack_id -eq $case.ExpectedPack) -Message "[$($case.Name)] pack expected=$($case.ExpectedPack), actual=$($route.selected.pack_id)"
    }
    if ($case.PSObject.Properties.Name -contains "ExpectedSkill" -and $case.ExpectedSkill) {
        $results += Assert-True -Condition ($route.selected.skill -eq $case.ExpectedSkill) -Message "[$($case.Name)] skill expected=$($case.ExpectedSkill), actual=$($route.selected.skill)"
    }
```

- [ ] **Step 3: Replace old orchestration cases in skill index audit**

In `scripts/verify/vibe-skill-index-routing-audit.ps1`, replace:

```powershell
    [pscustomobject]@{ Name = "brainstorming route"; Prompt = "先做头脑风暴，发散方案"; Grade = "L"; TaskType = "planning"; ExpectedPack = "orchestration-core"; ExpectedSkill = "brainstorming" },
    [pscustomobject]@{ Name = "writing plans route"; Prompt = "请输出实施计划并做任务拆解"; Grade = "L"; TaskType = "planning"; ExpectedPack = "orchestration-core"; ExpectedSkill = "writing-plans" },
    [pscustomobject]@{ Name = "subagent route"; Prompt = "把任务拆成多个子代理并行执行"; Grade = "XL"; TaskType = "planning"; ExpectedPack = "orchestration-core"; ExpectedSkill = "subagent-driven-development" },
```

with:

```powershell
    [pscustomobject]@{ Name = "brainstorming no orchestration core"; Prompt = "先做头脑风暴，发散方案"; Grade = "L"; TaskType = "planning"; BlockedPack = "orchestration-core"; BlockedSkill = "brainstorming" },
    [pscustomobject]@{ Name = "writing plan no orchestration core"; Prompt = "请输出实施计划并做任务拆解"; Grade = "L"; TaskType = "planning"; BlockedPack = "orchestration-core"; BlockedSkill = "writing-plans" },
    [pscustomobject]@{ Name = "subagent no orchestration core"; Prompt = "把任务拆成多个子代理并行执行"; Grade = "XL"; TaskType = "planning"; BlockedPack = "orchestration-core"; BlockedSkill = "subagent-driven-development" },
    [pscustomobject]@{ Name = "speckit explicit compatibility"; Prompt = "/speckit.plan 生成技术计划"; Grade = "L"; TaskType = "planning"; ExpectedPack = "workflow-compatibility"; ExpectedSkill = "spec-kit-vibe-compat" },
```

- [ ] **Step 4: Replace old consolidation gate with a wrapper**

Replace all content of `scripts/verify/vibe-orchestration-core-consolidation-gate.ps1` with:

```powershell
param()

$ErrorActionPreference = "Stop"

$replacementGate = Join-Path $PSScriptRoot "vibe-orchestration-core-hard-removal-gate.ps1"
if (-not (Test-Path -LiteralPath $replacementGate)) {
    throw "Replacement hard-removal gate not found: $replacementGate"
}

Write-Host "orchestration-core consolidation gate is superseded by hard-removal gate."
& $replacementGate
exit $LASTEXITCODE
```

- [ ] **Step 5: Run focused gates**

Run:

```powershell
.\scripts\verify\vibe-orchestration-core-hard-removal-gate.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-orchestration-core-consolidation-gate.ps1
```

Expected: all four commands pass.

- [ ] **Step 6: Commit focused gate rewrites**

Run:

```powershell
git add -- scripts/verify/vibe-pack-regression-matrix.ps1 scripts/verify/vibe-skill-index-routing-audit.ps1 scripts/verify/vibe-orchestration-core-consolidation-gate.ps1
git commit -m "test: update routing gates for orchestration core removal"
```

---

### Task 6: Update Remaining Route Gates, Unit Tests, And Goldens

**Files:**
- Modify: `scripts/verify/vibe-routing-stability-gate.ps1`
- Modify: `scripts/verify/vibe-pack-routing-smoke.ps1`
- Modify: `scripts/verify/vibe-keyword-precision-audit.ps1`
- Modify: `scripts/verify/vibe-external-corpus-gate.ps1`
- Modify: `scripts/verify/vibe-openspec-governance-gate.ps1`
- Modify: `scripts/verify/fixtures/llm-acceleration.mock.json`
- Modify: `tests/runtime_neutral/test_router_bridge.py`
- Modify: `tests/runtime_neutral/test_structured_bounded_reentry_continuation.py`
- Modify: `tests/unit/test_router_contract_selection_guards.py`
- Modify: `tests/replay/route/router-contract-gate-golden.json`
- Modify: `tests/replay/route/recovery-wave-curated-prompts.json`
- Modify: `tests/replay/route/openclaw-runtime-core-preview.json`
- Modify: `references/fixtures/verify/routing-stability/vibe-routing-stability-gate.md`
- Modify: `references/fixtures/verify/routing-stability/vibe-routing-stability-gate.json`
- Modify: `references/fixtures/runtime-contract/governed-runtime-root-golden.json`
- Modify: `references/fixtures/external-corpus/vco-suggestions.md`
- Modify: `references/fixtures/external-corpus/vco-suggestions.json`
- Modify: `references/fixtures/external-corpus/external-corpus-gate.json`

- [ ] **Step 1: Locate all non-doc stale references**

Run:

```powershell
rg -n "\borchestration-core\b" config scripts tests references SKILL.md protocols core -g "!docs/**"
```

Expected before this task: matches remain in route gates, tests, replay fixtures, and references.

- [ ] **Step 2: Update `vibe-routing-stability-gate.ps1`**

Replace the three `orchestration-planning` test cases with:

```powershell
    (New-TestCase -Group "planning-no-orchestration-core" -Prompt "create implementation plan and task breakdown" -Grade "L" -TaskType "planning" -BlockedPack "orchestration-core"),
    (New-TestCase -Group "planning-no-orchestration-core" -Prompt "请输出实施计划和任务拆解" -Grade "L" -TaskType "planning" -BlockedPack "orchestration-core"),
    (New-TestCase -Group "planning-no-orchestration-core" -Prompt "need milestone roadmap and execution plan" -Grade "L" -TaskType "planning" -BlockedPack "orchestration-core"),
```

If `New-TestCase` does not accept `BlockedPack`, add a `BlockedPack` parameter and assert it in the result loop:

```powershell
if ($case.BlockedPack) {
    $results += Assert-True -Condition ($route.selected.pack_id -ne $case.BlockedPack) -Message "[$($case.Group)] blocked pack $($case.BlockedPack) not selected"
}
```

- [ ] **Step 3: Update `vibe-pack-routing-smoke.ps1` active pack list**

Replace:

```powershell
"orchestration-core",
```

with:

```powershell
"workflow-compatibility",
```

If the smoke gate also probes generic planning, change the expected pack to `$null` and add `BlockedPack = "orchestration-core"` in the same style as Task 5.

- [ ] **Step 4: Update keyword precision audit**

In `scripts/verify/vibe-keyword-precision-audit.ps1`, remove `orchestration-core` from the pack list and replace its case:

```powershell
[pscustomobject]@{ Pack = "orchestration-core"; Grade = "L"; Task = "planning"; En = "Need workflow orchestration and subagent planning for this system"; Zh = "请做工作流编排和子代理规划方案" },
```

with:

```powershell
[pscustomobject]@{ Pack = "workflow-compatibility"; Grade = "L"; Task = "planning"; En = "/speckit.plan create the technical plan"; Zh = "/speckit.plan 生成技术计划" },
```

Update any expected default map key from:

```powershell
"orchestration-core" = @{ Grade = "L"; Task = "planning" }
```

to:

```powershell
"workflow-compatibility" = @{ Grade = "L"; Task = "planning" }
```

- [ ] **Step 5: Update external corpus gate**

In `scripts/verify/vibe-external-corpus-gate.ps1`, replace expectations:

```powershell
[pscustomobject]@{ expected = "orchestration-core"; grade = "L"; task = "planning"; prompt = "Design a workflow orchestration strategy for multi-agent delivery" },
[pscustomobject]@{ expected = "orchestration-core"; grade = "M"; task = "planning"; prompt = "Route this task and classify the execution path" },
```

with:

```powershell
[pscustomobject]@{ blocked = "orchestration-core"; grade = "L"; task = "planning"; prompt = "Design a workflow orchestration strategy for multi-agent delivery" },
[pscustomobject]@{ blocked = "orchestration-core"; grade = "M"; task = "planning"; prompt = "Route this task and classify the execution path" },
```

Then update the assertion loop so cases with `blocked` assert:

```powershell
if ($case.blocked) {
    $results += Assert-True -Condition ($route.selected.pack_id -ne $case.blocked) -Message "[$($case.prompt)] blocked pack $($case.blocked) not selected"
} else {
    $results += Assert-True -Condition ($route.selected.pack_id -eq $case.expected) -Message "[$($case.prompt)] expected pack $($case.expected)"
}
```

- [ ] **Step 6: Update OpenSpec governance gate**

In `scripts/verify/vibe-openspec-governance-gate.ps1`, replace `ExpectedPack = "orchestration-core"` with:

```powershell
ExpectedPack = "workflow-compatibility"
```

only for explicit `/speckit.*` or `spec-kit` compatibility cases.

For cases that are only checking `openspec_advice`, remove the selected-pack assertion and keep:

```powershell
$results += Assert-True -Condition ($route.openspec_advice.enabled -eq $true) -Message "[$($case.Name)] openspec advice enabled"
```

Replace:

```powershell
$results += Assert-True -Condition ($governanceObj.selected_pack -eq "orchestration-core") -Message "[governance script] selected pack preserved"
```

with:

```powershell
$results += Assert-True -Condition ($governanceObj.selected_pack -ne "orchestration-core") -Message "[governance script] does not preserve orchestration-core"
```

- [ ] **Step 7: Update LLM acceleration mock**

In `scripts/verify/fixtures/llm-acceleration.mock.json`, replace:

```json
"suggested_pack_id": "orchestration-core"
```

with:

```json
"suggested_pack_id": "code-quality"
```

Replace the reason with:

```json
"reason": "Mock: general coding task likely fits code-quality after orchestration-core hard removal."
```

- [ ] **Step 8: Update `test_router_bridge.py` expectations**

For requested `vibe` tests, replace assertions that expect:

```python
self.assertEqual("orchestration-core", result["selected"]["pack_id"])
self.assertEqual("vibe", result["selected"]["skill"])
```

with assertions that check the alias/runtime intent, not the pack:

```python
self.assertEqual("vibe", result["alias"]["requested_canonical"])
self.assertNotEqual("orchestration-core", result["selected"]["pack_id"])
```

For wrapper entry tests that use `requested_skill="vibe-do-it"`, keep:

```python
self.assertEqual("vibe", result["alias"]["requested_canonical"])
```

and add:

```python
self.assertNotEqual("orchestration-core", result["selected"]["pack_id"])
```

Remove ranking assertions that search for `row["pack_id"] == "orchestration-core"`.

- [ ] **Step 9: Update bounded reentry continuation stubs**

In `tests/runtime_neutral/test_structured_bounded_reentry_continuation.py`, replace stub fragments:

```powershell
selected_pack = 'orchestration-core';
options = @([pscustomobject]@{ skill = 'vibe'; pack_id = 'orchestration-core'; score = 1.0 })
```

with:

```powershell
selected_pack = 'runtime-entry';
options = @([pscustomobject]@{ skill = 'vibe'; pack_id = 'runtime-entry'; score = 1.0 })
```

- [ ] **Step 10: Update synthetic unit-test pack name**

In `tests/unit/test_router_contract_selection_guards.py`, replace:

```python
"id": "orchestration-core",
```

with:

```python
"id": "synthetic-process-pack",
```

This keeps the selection-guard test about fallback behavior without implying a real active pack.

- [ ] **Step 11: Regenerate or edit route replay goldens**

Open each route replay file listed in this task. Replace every:

```json
"selected_pack": "orchestration-core"
```

with the expected new value:

- `workflow-compatibility` only when the prompt is explicitly `/speckit.*` or spec-kit compatibility.
- `code-quality`, `data-ml`, `research-design`, or another domain pack when the prompt has clear domain ownership.
- `null` when the prompt is generic planning / brainstorming / task splitting without `$vibe` and the test format permits `null`.

After editing, run:

```powershell
Get-ChildItem tests\replay\route -Filter *.json | ForEach-Object {
  Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
  Write-Host "[PASS] JSON parses: $($_.Name)"
}
```

Expected: all replay JSON files parse.

- [ ] **Step 12: Update reference fixtures**

For `references/fixtures/verify/routing-stability/vibe-routing-stability-gate.md`, replace:

```markdown
- `orchestration-planning`: stability=`1` dominant=`orchestration-core|writing-plans`
```

with:

```markdown
- `planning-no-orchestration-core`: stability=`1` dominant does not include `orchestration-core`
```

For JSON reference fixtures, replace `expected_pack` and `selected_pack` values using the same rule as Step 11.

- [ ] **Step 13: Confirm no stale non-doc references remain**

Run:

```powershell
rg -n "\borchestration-core\b" config scripts tests references SKILL.md protocols core -g "!docs/**"
```

Expected: no matches except archival references that are intentionally outside active config, active tests, and active gates. If matches remain in active files, update them before continuing.

- [ ] **Step 14: Run updated tests and gates**

Run:

```powershell
python -m pytest tests/unit/test_router_contract_selection_guards.py tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_structured_bounded_reentry_continuation.py -q
.\scripts\verify\vibe-routing-stability-gate.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-keyword-precision-audit.ps1
.\scripts\verify\vibe-external-corpus-gate.ps1
.\scripts\verify\vibe-openspec-governance-gate.ps1
```

Expected: all commands pass.

- [ ] **Step 15: Commit remaining test and fixture updates**

Run:

```powershell
git add -- scripts/verify tests references
git commit -m "test: remove orchestration core routing expectations"
```

---

### Task 7: Add Governance Note

**Files:**
- Create: `docs/governance/orchestration-core-hard-removal-2026-04-28.md`
- Modify: `docs/governance/orchestration-core-pack-consolidation-2026-04-28.md`
- Modify: `docs/governance/orchestration-core-minimal-routing-cleanup-2026-04-27.md`

- [ ] **Step 1: Create governance note**

Create `docs/governance/orchestration-core-hard-removal-2026-04-28.md` with this content:

```markdown
# Orchestration-Core Hard Removal

Date: 2026-04-28

## Summary

`orchestration-core` is no longer an active routing pack.

The governed entry model is now:

```text
$vibe / /vibe -> vibe six-stage runtime -> internal specialist recommendations -> vibe-owned execution and cleanup
```

`resolve-pack-route.ps1` remains available, but only as an internal specialist recommendation mechanism.

## Removed Active Surface

| old surface | new ownership |
| --- | --- |
| `orchestration-core/brainstorming` | `vibe.deep_interview` method |
| `orchestration-core/writing-plans` | `vibe.xl_plan` method |
| `orchestration-core/subagent-driven-development` | `vibe.plan_execute` and `protocols/team.md` |
| `orchestration-core/spec-kit-vibe-compat` | `workflow-compatibility/spec-kit-vibe-compat` explicit compatibility |

## What Did Not Change

- The physical skill directories were not deleted in this pass.
- `vibe` remains the canonical runtime skill.
- Runtime packet field `canonical_router` is retained as a compatibility field name.
- Specialist recommendations remain bounded under `vibe` authority.

## Protected Boundaries

| prompt | expected boundary |
| --- | --- |
| `请输出实施计划和任务拆解` | must not select `orchestration-core` |
| `先做头脑风暴，发散方案` | must not select `orchestration-core` |
| `把任务拆成多个子代理并行执行` | must not select `orchestration-core` |
| `/speckit.plan 生成技术计划` | selects `workflow-compatibility/spec-kit-vibe-compat` |
| `$vibe ...` | enters `vibe`; specialists are subordinate recommendations |

## Verification

```powershell
.\scripts\verify\vibe-orchestration-core-hard-removal-gate.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-routing-stability-gate.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-keyword-precision-audit.ps1
.\scripts\verify\vibe-external-corpus-gate.ps1
.\scripts\verify\vibe-openspec-governance-gate.ps1
```
```

- [ ] **Step 2: Mark previous governance docs as superseded**

At the top of `docs/governance/orchestration-core-pack-consolidation-2026-04-28.md`, after the title and date, add:

```markdown
> Superseded by `docs/governance/orchestration-core-hard-removal-2026-04-28.md`.
> This document records the intermediate 8-skill consolidation state, not the current hard-removal target.
```

At the top of `docs/governance/orchestration-core-minimal-routing-cleanup-2026-04-27.md`, after the title and date, add:

```markdown
> Superseded by `docs/governance/orchestration-core-hard-removal-2026-04-28.md`.
> This document records the earlier minimal cleanup state.
```

- [ ] **Step 3: Scan governance docs for incomplete markers**

Run:

```powershell
$scanPattern = 'TO' + 'DO|TB' + 'D|' + '待' + '定|' + '占' + '位|place' + 'holder|FIX' + 'ME'
Select-String -LiteralPath docs\governance\orchestration-core-hard-removal-2026-04-28.md -Pattern $scanPattern -CaseSensitive:$false
```

Expected: no output.

- [ ] **Step 4: Commit governance note**

Run:

```powershell
git add -- docs/governance/orchestration-core-hard-removal-2026-04-28.md docs/governance/orchestration-core-pack-consolidation-2026-04-28.md docs/governance/orchestration-core-minimal-routing-cleanup-2026-04-27.md
git commit -m "docs: record orchestration core hard removal"
```

---

### Task 8: Full Verification And Packaging Gates

**Files:**
- Verify only unless a gate reports a specific stale artifact.

- [ ] **Step 1: Run focused hard-removal verification**

Run:

```powershell
.\scripts\verify\vibe-orchestration-core-hard-removal-gate.ps1
.\scripts\verify\vibe-orchestration-core-consolidation-gate.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected: all pass.

- [ ] **Step 2: Run router and route stability verification**

Run:

```powershell
python -m pytest tests/unit/test_router_contract_selection_guards.py tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_structured_bounded_reentry_continuation.py -q
.\scripts\verify\vibe-routing-stability-gate.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-keyword-precision-audit.ps1
.\scripts\verify\vibe-external-corpus-gate.ps1
.\scripts\verify\vibe-openspec-governance-gate.ps1
```

Expected: all pass.

- [ ] **Step 3: Run runtime authority verification**

Run:

```powershell
.\scripts\verify\vibe-governed-runtime-contract-gate.ps1
.\scripts\verify\vibe-canonical-entry-truth-gate.ps1
.\scripts\verify\vibe-runtime-execution-proof-gate.ps1
```

Expected: all pass. If a gate still prints `canonical_router`, verify it is referring to the compatibility packet field and not to user-facing router authority.

- [ ] **Step 4: Run parity and packaging gates**

Run:

```powershell
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
```

Expected: all pass. If config parity reports a tracked mirror path, update the reported mirror file with the same JSON content and rerun this step.

- [ ] **Step 5: Run stale-reference scan**

Run:

```powershell
rg -n "\borchestration-core\b" config scripts tests references SKILL.md protocols core -g "!docs/**"
```

Expected: no matches in active config, active scripts, active tests, or active references.

Run:

```powershell
rg -n "Canonical router:|Canonical router authority stays intact|canonical router selected|because canonical router exited" SKILL.md protocols scripts/runtime core/skills/vibe
```

Expected: no matches.

- [ ] **Step 6: Commit verification artifact fixes if any**

If Step 4 or Step 5 required fixture or mirror updates, run:

```powershell
git add -- config references scripts tests
git commit -m "chore: refresh hard removal verification fixtures"
```

If no files changed, skip this commit.

- [ ] **Step 7: Final worktree check**

Run:

```powershell
git status --short --branch
git log --oneline -8
```

Expected: worktree is clean and the latest commits show the hard-removal gate, terminology rename, routing config migration, stage absorption, test migration, governance note, and any fixture refresh.

---

## Execution Notes

- Do not physically delete `bundled/skills/brainstorming`, `bundled/skills/writing-plans`, `bundled/skills/subagent-driven-development`, or related directories in this pass.
- Do not rename the runtime packet object `canonical_router` in this pass. It is a compatibility field consumed by runtime validation and older tests.
- Do not add a new public `brainstorming`, `writing-plans`, or `subagent-driven-development` entrypoint.
- Only `workflow-compatibility/spec-kit-vibe-compat` remains as an explicit compatibility route because `/speckit.*` is a command-family compatibility case, not generic planning.
- If a generic planning prompt selects some other domain pack because of old broad defaults, fix that only when the pack is clearly wrong. The hard-removal acceptance criterion for this pass is that it does not select `orchestration-core` or process-method skills.

## Final Verification Command Set

Run this command set before claiming completion:

```powershell
.\scripts\verify\vibe-orchestration-core-hard-removal-gate.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
python -m pytest tests/unit/test_router_contract_selection_guards.py tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_structured_bounded_reentry_continuation.py -q
.\scripts\verify\vibe-routing-stability-gate.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-keyword-precision-audit.ps1
.\scripts\verify\vibe-external-corpus-gate.ps1
.\scripts\verify\vibe-openspec-governance-gate.ps1
.\scripts\verify\vibe-governed-runtime-contract-gate.ps1
.\scripts\verify\vibe-canonical-entry-truth-gate.ps1
.\scripts\verify\vibe-runtime-execution-proof-gate.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
```

Expected: all commands pass. Any pre-existing unrelated failure must be named with the failing assertion and evidence that it is unrelated to `orchestration-core`.
