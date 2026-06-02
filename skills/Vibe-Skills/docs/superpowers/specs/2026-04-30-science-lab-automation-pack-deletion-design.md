# Science Lab Automation Pack Deletion Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-30

## 1. Decision

Remove `science-lab-automation` from the live Vibe-Skills routing surface.

This is a hard removal pass, not another boundary-narrowing pass. The pack is too cold, too product/API-specific, and too costly to keep as a maintained direct routing surface for the current simplified Vibe-Skills package.

The public Vibe runtime remains unchanged:

```text
skeleton_check -> deep_interview -> requirement_doc -> xl_plan -> plan_execute -> phase_cleanup
```

The simplified usage model remains unchanged:

```text
candidate skill -> selected skill -> used / unused
```

No advisory experts, consultation state, helper experts, primary/secondary skill hierarchy, explicit replacement pack, or stage assistants will be added.

## 2. Current State

`config/pack-manifest.json` currently defines `science-lab-automation` as a six-owner pack:

| Surface | Current value |
| --- | --- |
| Pack | `science-lab-automation` |
| `skill_candidates` | `opentrons-integration`, `pylabrobot`, `protocolsio-integration`, `benchling-integration`, `labarchive-integration`, `ginkgo-cloud-lab` |
| `route_authority_candidates` | same six skills |
| `stage_assistant_candidates` | empty |
| Defaults | planning/research -> `protocolsio-integration`; coding -> `opentrons-integration` |

Bundled skill directories in scope:

```text
bundled/skills/opentrons-integration
bundled/skills/pylabrobot
bundled/skills/protocolsio-integration
bundled/skills/benchling-integration
bundled/skills/labarchive-integration
bundled/skills/ginkgo-cloud-lab
```

All six directories contain non-empty `SKILL.md` content and at least scripts or references. They are being removed because the pack is not worth preserving in the active package, not because every file is empty or individually low effort.

`latchbio-integration` is not in this pack and is out of scope for this deletion pass.

## 3. Problems

### 3.1 The Pack Is A Cold Specialist Surface

The retained skills focus on wet-lab robots, lab SaaS products, electronic lab notebooks, protocol hosting, and cloud-lab ordering. These are real but low-frequency tasks for the current Vibe-Skills package.

Keeping this pack means maintaining route boundaries for product-specific prompts that most users will not hit:

```text
opentrons
ot-2
opentrons flex
pylabrobot
hamilton
tecan
protocols.io
benchling
labarchives
ginkgo cloud lab
cloud.ginkgo.bio
```

The current package direction favors fewer, clearer expert roles over long-tail vendor and platform integrations.

### 3.2 The Pack Mixes Several Different Product Families

The current pack combines at least four different problem classes:

| Problem class | Current skills |
| --- | --- |
| Robot and liquid-handling code | `opentrons-integration`, `pylabrobot` |
| Protocol platform API | `protocolsio-integration` |
| Life-science R&D/ELN platforms | `benchling-integration`, `labarchive-integration` |
| Cloud-lab ordering service | `ginkgo-cloud-lab` |

These are not one clean expert role. A user asking for Opentrons code is not asking for Benchling or Ginkgo Cloud Lab. A user asking for an ELN backup is not asking for a lab robot protocol. Keeping them under one pack creates a tool-bag surface rather than a clear specialist boundary.

### 3.3 Narrowing Would Preserve Too Much Maintenance Burden

A prior pass already moved `latchbio-integration` out and made the six remaining skills direct route owners with no stage assistants. That fixed structural ambiguity, but it did not solve the main value question.

The remaining pack still requires ongoing maintenance for:

- Opentrons versus PyLabRobot boundaries.
- protocols.io versus generic protocol writing.
- Benchling versus generic ELN and inventory work.
- LabArchives versus generic attachment/document organization.
- Ginkgo Cloud Lab service and pricing references.
- False positives against literature search, bioinformatics, general documentation, and ordinary lab-method writing.

For the current cleanup direction, deleting the whole pack is simpler and more honest than preserving explicit-only variants.

## 4. Goals

- Remove `science-lab-automation` from live routing.
- Physically delete:

```text
bundled/skills/opentrons-integration
bundled/skills/pylabrobot
bundled/skills/protocolsio-integration
bundled/skills/benchling-integration
bundled/skills/labarchive-integration
bundled/skills/ginkgo-cloud-lab
```

- Remove the deleted pack and skills from:

```text
config/pack-manifest.json
config/skill-keyword-index.json
config/skill-routing-rules.json
config/skills-lock.json
```

- Rewrite existing positive route probes into absence or blocked-pack probes.
- Add governance evidence explaining that the deletion is a cold-pack hard removal.
- Keep `zero_route_authority = 0`.
- Keep every pack's `stage_assistant_candidates` empty.

## 5. Non-Goals

This pass will not:

- Create a replacement wet-lab automation pack.
- Move Opentrons or PyLabRobot into another ordinary route owner.
- Move protocols.io, Benchling, LabArchives, or Ginkgo Cloud Lab into another pack.
- Keep deleted skills as explicit-only, helper, advisory, or consultation routes.
- Delete `latchbio-integration`.
- Change Vibe's six-stage runtime.
- Change dispatch mechanics or material-use reporting.
- Claim that any skill was materially used in a real task.

## 6. Routing Migration

### 6.1 Deleted Prompt Classes

| Prompt class | Old behavior | Target behavior |
| --- | --- | --- |
| Opentrons OT-2/Flex protocol code | `science-lab-automation / opentrons-integration` | no `science-lab-automation` route |
| Hamilton/Tecan or PyLabRobot automation | `science-lab-automation / pylabrobot` | no `science-lab-automation` route |
| protocols.io API create/search/publish | `science-lab-automation / protocolsio-integration` | no `science-lab-automation` route |
| Benchling registry/inventory/ELN/API | `science-lab-automation / benchling-integration` | no `science-lab-automation` route |
| LabArchives notebook/entry/attachment backup | `science-lab-automation / labarchive-integration` | no `science-lab-automation` route |
| Ginkgo Cloud Lab ordering/pricing | `science-lab-automation / ginkgo-cloud-lab` | no `science-lab-automation` route |

The deletion does not require a replacement owner. If a future task needs these products, the agent can handle it as ordinary context-driven work with user-provided docs, installed tools, or web verification when appropriate.

### 6.2 Negative Boundary Classes To Preserve

These prompts already should not route to `science-lab-automation`; they must continue not to route there after deletion:

```text
Use LatchBio / Latch SDK to deploy a Nextflow RNA-seq workflow.
Write a generic wet-lab protocol in Markdown without protocols.io or robots.
Use PubMed to find wet-lab methods papers.
Organize an ELN template without Benchling or LabArchives.
```

## 7. Files To Change

Expected implementation files:

```text
config/pack-manifest.json
config/skill-keyword-index.json
config/skill-routing-rules.json
config/skills-lock.json
tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py
tests/runtime_neutral/test_zero_route_authority_third_pass.py
scripts/verify/probe-scientific-packs.ps1
scripts/verify/vibe-skill-index-routing-audit.ps1
scripts/verify/vibe-pack-regression-matrix.ps1
scripts/verify/vibe-pack-routing-smoke.ps1
docs/governance/science-lab-automation-pack-deletion-2026-04-30.md
```

Expected physical deletions:

```text
bundled/skills/opentrons-integration
bundled/skills/pylabrobot
bundled/skills/protocolsio-integration
bundled/skills/benchling-integration
bundled/skills/labarchive-integration
bundled/skills/ginkgo-cloud-lab
```

Other files may need focused updates if tests, docs, generated lock data, or verification scripts still reference the deleted pack or skills.

## 8. Verification Plan

Run focused checks first:

```powershell
python -m pytest tests/runtime_neutral/test_science_lab_automation_pack_consolidation.py -q
python -m pytest tests/runtime_neutral/test_zero_route_authority_third_pass.py tests/runtime_neutral/test_final_stage_assistant_removal.py -q
```

Then run routing and packaging gates:

```powershell
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

If a broad gate fails because a stale positive probe still expects `science-lab-automation`, update that probe to assert absence of the deleted pack instead of silently weakening the check.

## 9. Acceptance Criteria

- `science-lab-automation` is absent from `config/pack-manifest.json`.
- The six deleted skill ids are absent from `skill-keyword-index`, `skill-routing-rules`, and `skills-lock`.
- The six bundled skill directories no longer exist.
- No active route test expects `science-lab-automation` to be selected.
- Opentrons, PyLabRobot, protocols.io, Benchling, LabArchives, and Ginkgo Cloud Lab prompts do not select `science-lab-automation`.
- `zero_route_authority = 0`.
- `stage_assistant_candidates = 0` for all remaining packs.
- The governance note states this is a cold-pack hard removal and does not introduce helper/advisory/consultation routing.

## 10. Risks

### 10.1 Loss Of Narrow Product Help

Users who explicitly ask for Opentrons, PyLabRobot, protocols.io, Benchling, LabArchives, or Ginkgo Cloud Lab will no longer get a bundled specialist. This is acceptable because the pack is intentionally being removed as too cold for the current distribution.

### 10.2 Stale References

The deleted skills are referenced in tests, verification scripts, lock data, and historical governance docs. Implementation must clean active routing and test references while leaving historical documents intact unless they are current guidance.

### 10.3 Overclaiming

Passing route/config tests will prove the deletion is represented in repository routing surfaces. It will not prove anything about real task execution or material skill use.

## 11. Implementation Notes

- Use native PowerShell path checks before deleting directories.
- Do not delete outside `bundled/skills`.
- Refresh `skills-lock.json` only after all config and directory changes are stable.
- Keep the diff scoped to the deleted pack, deleted skills, route probes, verification scripts, lock data, and governance evidence.
