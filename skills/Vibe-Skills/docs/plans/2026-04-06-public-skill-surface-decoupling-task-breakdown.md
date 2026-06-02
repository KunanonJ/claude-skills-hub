# Public Skill Surface Decoupling Task Breakdown

## Purpose

This document turns the execution plan into an implementation-ready checklist.
It is ordered to minimize coupling risk:

1. freeze contracts
2. teach runtime to read the new truth
3. change installer topology
4. switch uninstall ownership model
5. cut over docs and release gates

## Delivery Strategy

Use branch-safe incremental delivery.
Each phase should land in a reviewable slice with its own tests.
Do not combine contract changes, runtime resolver changes, and uninstall rewrites in one patch.

## Implementation Standards

### Subjective Standards

- Keep each PR centered on one semantic boundary change.
- Avoid "clever" fallback logic when a contract field can make the dependency explicit.
- Preserve user trust in the visible workspace layout; treat top-level skill directories as a UX surface, not just a filesystem detail.
- Prefer migration paths that make rollback cheap and local.

### Objective Standards

- Every phase must identify:
  - changed files
  - acceptance criteria
  - verification commands
- No phase is considered complete without at least one automated check passing.
- Any change that expands or preserves legacy compatibility must also define the condition for later removal.
- Any change touching uninstall must include a residue-focused verification case.
- Any topology cutover phase must include at least one host-realistic task probe for `codex`, `claude-code`, `openclaw`, and `opencode`.
- Any claim borrowed from README must map to a test or probe, or be marked as a remaining gap.
- Any phase that changes runtime or installer behavior must identify which of `codex`, `claude-code`, `openclaw`, and `opencode` are re-verified in that phase.
- Any phase that changes router or governed runtime behavior must include at least one realistic task probe, not just a schema assertion.
- Any topology-affecting phase must identify host coverage for `codex`, `claude-code`, `openclaw`, and `opencode`.
- Any phase that claims runtime safety must identify at least one routing probe, one governance probe, and one memory/runtime probe when relevant.

## Phase A

### Goal

Add new topology vocabulary and ledger schema support without changing default install behavior.

### A1. Packaging Contract Split

Files likely to change:

- `config/runtime-core-packaging.json`
- `config/runtime-core-packaging.minimal.json`
- `config/runtime-core-packaging.full.json`
- `packages/installer-core/src/vgo_installer/runtime_packaging.py`

Tasks:

- add explicit fields for:
  - `public_skill_surface`
  - `internal_skill_corpus`
  - `compatibility_skill_projections`
- keep current compatibility projection values so default behavior does not change yet
- make `resolve_runtime_core_packaging()` return normalized values for the new fields
- preserve older fields until later phases stop reading them

Acceptance:

- current install behavior remains unchanged
- packaging projections still round-trip from base manifest to generated profile manifests

Verification:

```bash
pytest -q tests/integration/test_runtime_core_packaging_roles.py
```

### A2. Internal Corpus Descriptor Contract

Files likely to change:

- `packages/contracts/src/vgo_contracts/catalog_descriptor.py`
- `packages/contracts/src/vgo_contracts/runtime_surface_contract.py`
- new contract/helper file under `packages/contracts/src/vgo_contracts/`
- possibly a new config file such as `config/internal-skill-corpus.json`

Tasks:

- define a contract that tells runtime-core where to resolve internal official skill descriptors
- keep detached `skill-catalog` metadata separate from runtime authority
- define how canonical repo runtime and installed runtime each locate the internal corpus

Acceptance:

- runtime can consume a single descriptor source of truth without assuming top-level installed skill directories
- catalog remains metadata-only

Verification:

```bash
pytest -q tests/integration/test_catalog_contract_consumption.py
```

### A3. Ledger v2 Schema Introduction

Files likely to change:

- `packages/contracts/src/vgo_contracts/install_ledger.py`
- `packages/installer-core/src/vgo_installer/ledger_service.py`
- unit tests for ledger parsing and summary logic

Tasks:

- add v2 schema support for:
  - `runtime_roots`
  - `compatibility_roots`
  - `sidecar_roots`
  - `config_rollbacks`
  - `legacy_cleanup_candidates`
- keep read compatibility for v1 ledgers
- do not switch uninstall to v2-only behavior yet

Acceptance:

- v1 ledgers still parse
- new installs can emit v2-compatible ownership structures

Verification:

```bash
pytest -q tests/unit/test_installer_ledger_service.py
```

### A4. Compatibility Toggle Contract

Files likely to change:

- `config/runtime-core-packaging.json`
- `config/version-governance.json`
- `packages/contracts/src/vgo_contracts/installed_runtime_contract.py`

Tasks:

- add a contract-level toggle or host-scoped compatibility projection declaration
- avoid environment-variable-only rollout switches
- document that rollback re-enables legacy public projection without reverting internal corpus support

Acceptance:

- contract exposes a stable toggle path for later rollout phases
- toggle semantics are documented well enough that rollback does not require source-code archaeology

Host/probe note:

- before leaving Phase A, map the future host verification matrix and ensure no later phase can claim success while skipping one of the four target hosts

## Phase B

### Goal

Make runtime descriptor resolution independent from legacy top-level installed official skill directories.

### B1. Descriptor-Driven Resolver

Files likely to change:

- `packages/runtime-core/src/vgo_runtime/router_contract_support.py`
- `packages/runtime-core/src/vgo_runtime/router_contract_runtime.py`
- possibly a new helper module in `packages/runtime-core/src/vgo_runtime/`

Tasks:

- refactor `resolve_skill_md_path()` into a descriptor-driven resolver
- preserve `select_pack_candidate()` and ranking logic unless evidence forces change
- resolve in this order:
  - internal corpus entry
  - explicit public companion projection
  - custom installed skill
  - temporary legacy top-level official skill fallback

Acceptance:

- runtime can resolve official skill descriptions even when they are no longer top-level installed directories
- candidate routing behavior remains stable

Verification:

```bash
pytest -q tests/integration/test_catalog_contract_consumption.py
pytest -q tests/runtime_neutral/test_install_generated_nested_bundled.py
```

### B2. Fallback Telemetry and Guardrails

Files likely to change:

- `packages/runtime-core/src/vgo_runtime/router_contract_support.py`
- targeted tests under `tests/runtime_neutral/` or `tests/unit/`

Tasks:

- make legacy fallback usage visible in tests or receipts
- add assertions proving fallback remains temporary compatibility, not hidden primary behavior

Acceptance:

- fallback paths are observable
- later removal can be gated on proof rather than assumption
- runtime no longer treats top-level official installed skills as its only installed-runtime truth source

Required probes:

- route a planning task through `$vibe`
- route a debug task through `$vibe`
- confirm runtime authority remains `vibe` when a specialist is selected

Required realistic probes:

- debug task routed through `/vibe`
- planning task that produces confirm-required or governed-plan behavior
- at least one governed runtime invocation that still emits stage receipts after resolver refactor

## Phase C

### Goal

Move `full` from broad public projection to full internal corpus plus narrow public surface.

### C1. Internal Corpus Materialization

Files likely to change:

- `packages/installer-core/src/vgo_installer/install_runtime.py`
- `packages/installer-core/src/vgo_installer/materializer.py`
- `packages/installer-core/src/vgo_installer/profile_inventory.py`

Tasks:

- materialize full official corpus under `skills/vibe/...`
- stop using `bundled/skills -> skills` as the meaning of full capability breadth
- keep `skills/vibe` as the canonical public root
- keep only explicitly required public companions

Acceptance:

- fresh full install no longer creates hundreds of top-level official skill directories
- full still has broader internal capability coverage than minimal

Verification:

```bash
pytest -q tests/runtime_neutral/test_install_profile_differentiation.py
pytest -q tests/runtime_neutral/test_installed_runtime_scripts.py
```

### C2. Payload Summary Semantics

Files likely to change:

- `packages/installer-core/src/vgo_installer/ledger_service.py`
- tests around profile differentiation and payload summary

Tasks:

- redefine payload summary so it reflects owned capability surfaces accurately
- stop implicitly treating top-level official skill count as the main product metric

Acceptance:

- payload summaries remain useful after the topology change
- tests assert meaningful distinctions between minimal and full
- summary semantics no longer equate product value with top-level official skill count

Required probes:

- inspect top-level `skills/` count on fresh installs
- inspect internal corpus placement under `skills/vibe/...`
- verify host-visible `vibe` remains stable across the mandatory hosts

Required host checks:

- `codex`: narrow public `skills/` surface after full install
- `claude-code`: bounded managed settings still preserved
- `openclaw`: runtime-core preview lane boundaries still hold
- `opencode`: preview-guidance wrappers and config example still materialize correctly

## Phase D

### Goal

Switch uninstall from heuristic cleanup to authoritative ownership deletion.

### D1. Root-Class Deletion

Files likely to change:

- `packages/installer-core/src/vgo_installer/uninstall_service.py`
- `packages/installer-core/src/vgo_installer/uninstall_plan.py`
- `packages/installer-core/src/vgo_installer/ledger_service.py`

Tasks:

- uninstall prefers ledger v2
- delete `runtime_roots`, `compatibility_roots`, and `sidecar_roots` by class
- use static host inventory only as compatibility cleanup

Acceptance:

- nested/runtime-mirror residue is gone after uninstall
- uninstall preview and actual uninstall agree

Verification:

```bash
pytest -q tests/runtime_neutral/test_installed_runtime_uninstall.py
```

### D2. Config Rollback and BOM Safety

Files likely to change:

- `packages/installer-core/src/vgo_installer/uninstall_service.py`
- `packages/installer-core/src/vgo_installer/host_closure.py`
- shared JSON helpers if needed

Tasks:

- replay `config_rollbacks`
- unify JSON reading/writing to BOM-safe behavior
- cover delete-empty-file vs preserve-user-file behavior explicitly

Acceptance:

- managed JSON nodes are removed cleanly
- BOM-encoded files do not break uninstall

Required probes:

- Claude Code existing `settings.json`
- OpenCode existing `opencode.json`
- at least one BOM-encoded managed JSON fixture

Verification:

```bash
pytest -q tests/runtime_neutral/test_installed_runtime_uninstall.py
```

### D3. Upgrade/Reinstall Legacy Cleanup

Files likely to change:

- `packages/installer-core/src/vgo_installer/install_runtime.py`
- `packages/installer-core/src/vgo_installer/ledger_service.py`
- reinstall/profile-switch tests

Tasks:

- prune legacy broad public skill directories during reinstall/profile changes
- only prune previously managed paths, not user-owned custom skills

Acceptance:

- legacy broad installs converge into narrow-surface installs without orphaned official skill dirs
- cleanup touches only previously managed official projections, not user-owned custom content

Required probes:

- reinstall after prior broad install
- uninstall after profile switch
- verify no managed residue under nested compatibility/runtime-mirror paths

## Phase E

### Goal

Align docs, release truth, and rollback policy with the new topology.

### E1. Install and Governance Docs

Files likely to change:

- `docs/install/opencode-path.en.md`
- `docs/install/custom-skill-governance-rules.en.md`
- related install path docs in `docs/install/`

Tasks:

- rewrite default install explanation around `vibe` plus internal capability packs
- document compatibility projections as explicit exceptions, not default truth
- document rollback/toggle behavior

Acceptance:

- docs no longer imply that broad public top-level official skill projection is the intended steady state

### E2. Release Gates

Files likely to change:

- tests and possibly verification docs or SOPs

Tasks:

- require three gate classes before final cutover:
  - contract/config gate
  - installed runtime gate
  - docs/truth gate

Acceptance:

- release criteria are explicit and auditable
- objective release failure conditions are written down before the final topology cutover

Required evidence bundle:

- host matrix results for `codex`, `claude-code`, `openclaw`, `opencode`
- task matrix results for planning/debug/governed execution/memory continuity
- README claim-to-proof matrix
- current baseline test results and post-change comparison

Required release gate classes:

- router/guided-runtime gate
- host install/check/runtime gate
- memory activation gate
- uninstall residue gate
- README claim alignment gate

### E3. README Claim-to-Proof Mapping

Files likely to change:

- `README.md`
- planning docs or release checklist docs

Tasks:

- map major README claims to proof assets:
  - intelligent routing
  - governed workflow
  - root/child governance
  - memory system
  - host install/uninstall behavior
- identify claims that need stronger runtime probes rather than only contract tests

Acceptance:

- every major README claim relevant to this refactor has a named test or probe path

## Cross-Phase Guardrails

### Do Not Change Together

Avoid combining these in one patch:

- contract split and uninstall rewrite
- runtime resolver refactor and host smoke expectation updates
- full-profile topology switch and docs/truth cutover

### Compatibility Policy

- keep legacy public projection available through a contract-level toggle until host matrix is proven stable
- remove fallback only after tests and smoke runs prove it is no longer needed

### Deep-Test Policy

- do not rely only on unit and integration tests
- keep at least one runtime-neutral probe and one installed-runtime probe in every serious acceptance run
- prefer task prompts that resemble README-advertised usage:
  - debug with failing test/stack trace
  - planning/specification request
  - multi-step governed execution
  - long-context or continuity-sensitive task for memory activation

### Multi-Host Validation Policy

- do not declare completion based on Codex-only evidence
- require representative coverage for:
  - `codex`
  - `claude-code`
  - `openclaw`
  - `opencode`
- if a host cannot run a full governed lane, require explicit install/check/probe evidence for the mode it does support

### Layer Validation Policy

- routing must be validated independently from install
- governance must be validated independently from routing
- memory must be validated independently from governance artifacts
- uninstall cleanliness must be validated independently from install success

### Rollback Policy

Rollback means:

- restore legacy public projection for affected hosts

Rollback does not mean:

- remove the internal corpus reader
- revert ledger v2 support
- restore heuristic uninstall as the preferred path

## Recommended PR Slices

1. `contracts: add public/internal/compatibility topology vocabulary + ledger v2`
2. `runtime-core: add descriptor-driven internal corpus resolver with legacy fallback`
3. `installer-core: materialize full corpus under skills/vibe and classify ownership`
4. `installer-core: authoritative uninstall + BOM-safe config rollback`
5. `docs/tests: cut over product truth, deep validation matrix, and release gates`

## Final Acceptance Checklist

- `full` default install shows a narrow public `skills/` surface centered on `vibe`
- internal specialist corpus is present and readable by runtime-core
- supported hosts still discover `vibe` and required agents/config surfaces
- reinstall and profile changes clean up legacy broad public projections
- uninstall leaves no managed residue
- docs, tests, and rollout controls all describe the same topology
- subjective goal check: the resulting architecture reads as one governed runtime with explicit sidecars and explicit compatibility projections, not as a bundle of loosely related install tricks
- `codex`, `claude-code`, `openclaw`, and `opencode` each pass at least one realistic `$vibe` task probe after the cutover
- routing, governance, and memory probes still match README-described behavior after the cutover
- deep validation check: `codex`, `claude-code`, `openclaw`, and `opencode` each pass at least one install/check/runtime or uninstall probe relevant to their lane
- README alignment check: routing, governance, memory, and install-management claims remain supported by runnable evidence
- `codex`, `claude-code`, `openclaw`, and `opencode` each have explicit passing proof appropriate to their supported install mode
- routed planning/debug tasks, governance stage checks, and memory activation/folding checks all have passing proof after the topology change
- README-level claims relevant to routing, governance, memory, and install management have named proof assets
