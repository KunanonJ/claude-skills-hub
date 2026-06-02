# RUC-NLPIR Augmentation Tool Pack Cleanup Design

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

Date: 2026-04-29

## Goal

Simplify `ruc-nlpir-augmentation` from a mixed augmentation pack into a narrow tool pack with only two direct, explicit capabilities:

- `flashrag-evidence`: local evidence retrieval from repo/config/docs/skills.
- `webthinker-deep-research`: auditable multi-hop web research.

The cleanup must preserve the public six-stage Vibe runtime and follow the simplified routing model:

```text
candidate -> selected -> used / unused
```

There should be no auxiliary expert, secondary skill, stage assistant, consultation, or implicit helper semantics in this pack.

## Current State

Current `config/pack-manifest.json` entry:

| Field | Current value |
| --- | --- |
| Pack | `ruc-nlpir-augmentation` |
| `skill_candidates` | `flashrag-evidence`, `webthinker-deep-research`, `deepagent-toolchain-plan`, `deepagent-memory-fold` |
| `route_authority_candidates` | `flashrag-evidence`, `webthinker-deep-research` |
| `stage_assistant_candidates` | `deepagent-toolchain-plan`, `deepagent-memory-fold` |
| Defaults | planning/review/debug -> `flashrag-evidence`; research -> `webthinker-deep-research` |

Asset check:

| Skill | Files | Useful assets | Initial decision |
| --- | ---: | --- | --- |
| `flashrag-evidence` | 2 | `scripts/flashrag_evidence.py` | keep |
| `webthinker-deep-research` | 2 | `scripts/init_webthinker_run.py` | keep |
| `deepagent-toolchain-plan` | 1 | only `SKILL.md` | delete |
| `deepagent-memory-fold` | 1 | only `SKILL.md` | delete |

The two DeepAgent skills are thin wrappers. They do not provide scripts, templates, examples, or local assets. They also preserve the old idea of an implicit planning/memory helper, which conflicts with the simplified routing contract.

## Observed Routing Problem

Representative route probes show that stage assistants are not purely passive in practice:

| Prompt | Observed route |
| --- | --- |
| `用 DeepAgent 规划工具链和技能链` | `ruc-nlpir-augmentation / deepagent-toolchain-plan` |
| `请整理长会话上下文，做 memory folding` | `ruc-nlpir-augmentation / deepagent-memory-fold` |
| `我要做 deep research，多跳浏览网页并保留 trace.jsonl 和 sources.json 证据链` | `ruc-nlpir-augmentation / webthinker-deep-research` |

This means the current pack still exposes DeepAgent as selectable work, even though it was intended as stage assistance. That is the exact pattern this cleanup should remove.

## Target Boundary

After cleanup:

```text
ruc-nlpir-augmentation
├─ flashrag-evidence
└─ webthinker-deep-research
```

There will be:

- 2 `skill_candidates`
- 2 `route_authority_candidates`
- 0 `stage_assistant_candidates`
- `defaults_by_task` narrowed to `research -> webthinker-deep-research` only
- no DeepAgent bundled skill directories
- no DeepAgent keyword or routing-rule entries
- no DeepAgent capability-catalog entry
- no DeepAgent upstream alias or upstream lock entry

There should be no broad `planning`, `review`, or `debug` default pointing at `flashrag-evidence`. Those defaults would keep the pack acting like a generic phase helper. `flashrag-evidence` should be selected by explicit local-evidence keywords and route rules, not by generic task type.

## Trigger Definitions

### `flashrag-evidence`

This skill is a local evidence retrieval tool.

It should trigger only when the task explicitly needs local, citeable evidence from repo-local sources such as configs, governance docs, route rules, or `SKILL.md` files.

Positive trigger concepts:

- local evidence
- repo/config/governance evidence
- route rule evidence
- file path and line number
- `SKILL.md` source of truth
- `where is this defined`
- `配置依据`
- `路由规则在哪里`
- `给出文件和行号`

Negative trigger concepts:

- web research
- deep research report
- literature review
- competitor research
- paper writing
- PDF/document processing
- ordinary claim support from internet sources

### `webthinker-deep-research`

This skill is an auditable web research tool.

It should trigger only when the task explicitly asks for multi-hop web research or an auditable research bundle.

Positive trigger concepts:

- deep research
- multi-hop browse/search
- traceable web research
- `trace.jsonl`
- `sources.json`
- web source chain
- competitor/technology/company/policy research report
- `深度调研`
- `多跳浏览`
- `网页证据链`
- `保留 trace`

Negative trigger concepts:

- local config lookup
- codebase call graph
- simple search
- asking for a few sources
- PDF extraction
- ordinary scientific writing
- model training
- visualization

## DeepAgent Removal

Delete these bundled skill directories:

```text
bundled/skills/deepagent-toolchain-plan
bundled/skills/deepagent-memory-fold
```

Remove these skills from:

- `config/pack-manifest.json`
- `config/skill-keyword-index.json`
- `config/skill-routing-rules.json`
- `config/capability-catalog.json`
- `config/skills-lock.json`

Remove DeepAgent reimport handles from:

- `config/upstream-source-aliases.json`
- `config/upstream-lock.json`

This is a hard deletion because both skill directories are thin wrappers and there is no asset migration target.

## Kept Skills

Keep `flashrag-evidence` because it has a concrete local script and a clear evidence artifact contract: query -> citeable snippets with path and line anchors.

Keep `webthinker-deep-research` because it has a concrete scaffold script and a clear auditable output contract:

```text
report.md
sources.json
trace.jsonl
notes.md
```

These two skills solve distinct problems and should remain direct route owners.

## Non-Goals

- Do not change Vibe's six-stage runtime.
- Do not introduce a new helper/assistant mechanism.
- Do not replace DeepAgent with another toolchain-planning expert.
- Do not remove FlashRAG or WebThinker upstream references.
- Do not broaden this pass to `data-ml`, `code-quality`, zero-route-authority packs, or other science packs.
- Do not modify runtime router algorithms unless tests prove config-only cleanup cannot enforce the boundary.

## Future Verification Design

Implementation should add a focused runtime-neutral test that proves:

- `ruc-nlpir-augmentation.skill_candidates` contains only `flashrag-evidence` and `webthinker-deep-research`.
- `stage_assistant_candidates` is empty.
- no `bundled/skills/deepagent-*` directory remains.
- config files and `skills-lock.json` contain no `deepagent-*` skill.
- upstream source aliases and upstream lock no longer expose `RUC-NLPIR/DeepAgent`.
- DeepAgent prompts do not select `ruc-nlpir-augmentation / deepagent-*`.
- local route-evidence prompts still select `flashrag-evidence`.
- deep web research prompts still select `webthinker-deep-research`.

Existing gates to run after implementation:

```powershell
python -m pytest tests/runtime_neutral/test_ruc_nlpir_augmentation_cleanup.py tests/runtime_neutral/test_router_bridge.py -q
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-routing-stability-gate.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

## Acceptance Criteria

The cleanup is complete when:

- DeepAgent is absent from live routing config, bundled skills, lock file, capability catalog, and upstream reimport handles.
- `ruc-nlpir-augmentation` has exactly two direct route owners and zero stage assistants.
- route probes show no `deepagent-toolchain-plan` or `deepagent-memory-fold` selection.
- route probes still show `flashrag-evidence` for local evidence lookup and `webthinker-deep-research` for auditable deep web research.
- all focused and broad routing gates pass.

## Expected User-Facing Result

Users should not see `ruc-nlpir-augmentation` as an expert team or DeepAgent as an implicit helper.

They should only experience two explicit tool choices:

```text
Need local repo/config evidence -> use flashrag-evidence
Need auditable deep web research -> use webthinker-deep-research
Anything else -> do not use this pack
```
