# RUC-NLPIR Augmentation Tool Pack Cleanup Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce `ruc-nlpir-augmentation` to two explicit tools, `flashrag-evidence` and `webthinker-deep-research`, and remove DeepAgent helper/stage-assistant surfaces from live routing.

**Architecture:** Make the test fail first against every live surface that can expose DeepAgent. Then delete the two thin DeepAgent skills, narrow the pack manifest and routing rules, remove DeepAgent upstream/runtime/overlay reimport handles, regenerate `skills-lock.json`, and document the new boundary.

**Tech Stack:** Python `unittest` route probes through `vgo_runtime.router_contract_runtime.route_prompt`, JSON config files, PowerShell verification gates, repository-local bundled skills.

---

## File Structure

Create:

- `tests/runtime_neutral/test_ruc_nlpir_augmentation_cleanup.py` - focused regression tests for the cleaned pack boundary.
- `docs/governance/ruc-nlpir-augmentation-tool-pack-cleanup-2026-04-29.md` - governance note with before/after counts and route probes.

Modify:

- `config/pack-manifest.json` - make `ruc-nlpir-augmentation` a two-skill explicit tool pack and clear stage assistants.
- `config/skill-keyword-index.json` - remove DeepAgent skills and narrow kept tool keywords.
- `config/skill-routing-rules.json` - remove DeepAgent routing rules, remove `flashrag-evidence` canonical review ownership, and keep only explicit tool triggers.
- `config/capability-catalog.json` - remove DeepAgent-style `toolchain_planning` and `memory_folding` capability entries and clean `dedup_with` references to them.
- `config/ruc-nlpir-runtime.json` - keep only FlashRAG and WebThinker runtime declarations.
- `config/ruc-nlpir-overlays.json` - keep only FlashRAG and WebThinker overlays, with no team/retro DeepAgent fallbacks.
- `config/vco-overlays.json` - rename the RUC-NLPIR provider from agents to tools and remove DeepAgent from the display name.
- `config/upstream-source-aliases.json` - remove DeepAgent aliases.
- `config/upstream-lock.json` - remove `RUC-NLPIR/DeepAgent`.
- `config/skills-lock.json` - regenerate after deleting bundled skill directories.
- `scripts/ruc-nlpir/preflight.ps1` - stop hardcoding `DeepAgent` in the preflight repo loop.
- `references/overlays/index.md` - update the RUC-NLPIR overlay description.
- `tests/runtime_neutral/test_router_bridge.py` - update the existing deep research assertion so the pack has no legacy stage assistants.

Delete:

- `bundled/skills/deepagent-toolchain-plan/SKILL.md`
- `bundled/skills/deepagent-memory-fold/SKILL.md`
- `references/overlays/ruc-nlpir/deepagent-toolchain-plan.md`
- `references/overlays/ruc-nlpir/deepagent-memory-fold.md`

Do not modify:

- Vibe's six-stage runtime.
- The `flashrag-evidence` and `webthinker-deep-research` skill bodies except if a test proves their own text still contains stale DeepAgent cross-call instructions.
- Other packs such as `data-ml`, `code-quality`, `science-literature-citations`, or zero-route-authority long-tail packs.

## Task 1: Add Failing Cleanup Regression Tests

**Files:**

- Create: `tests/runtime_neutral/test_ruc_nlpir_augmentation_cleanup.py`

- [ ] **Step 1: Write the failing test file**

Create `tests/runtime_neutral/test_ruc_nlpir_augmentation_cleanup.py` with this exact content:

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


KEEP_SKILLS = ["flashrag-evidence", "webthinker-deep-research"]
DEEPAGENT_SKILLS = ["deepagent-toolchain-plan", "deepagent-memory-fold"]


def load_json(relative_path: str) -> dict[str, object]:
    path = REPO_ROOT / relative_path
    return json.loads(path.read_text(encoding="utf-8-sig"))


def route(prompt: str, task_type: str = "research", grade: str = "L") -> dict[str, object]:
    return route_prompt(
        prompt=prompt,
        grade=grade,
        task_type=task_type,
        requested_skill=None,
        repo_root=REPO_ROOT,
    )


def selected(result: dict[str, object]) -> tuple[str, str]:
    selected_row = result.get("selected")
    assert isinstance(selected_row, dict), result
    return str(selected_row.get("pack_id") or ""), str(selected_row.get("skill") or "")


def ranked_summary(result: dict[str, object]) -> list[tuple[str, str, float, str]]:
    ranked = result.get("ranked")
    assert isinstance(ranked, list), result
    rows: list[tuple[str, str, float, str]] = []
    for row in ranked[:8]:
        assert isinstance(row, dict), row
        rows.append(
            (
                str(row.get("pack_id") or ""),
                str(row.get("selected_candidate") or ""),
                float(row.get("score") or 0.0),
                str(row.get("candidate_selection_reason") or ""),
            )
        )
    return rows


def ruc_pack() -> dict[str, object]:
    manifest = load_json("config/pack-manifest.json")
    packs = manifest.get("packs")
    assert isinstance(packs, list), manifest
    for pack in packs:
        assert isinstance(pack, dict), pack
        if pack.get("id") == "ruc-nlpir-augmentation":
            return pack
    raise AssertionError("ruc-nlpir-augmentation pack missing")


class RucNlpirAugmentationCleanupTests(unittest.TestCase):
    def test_manifest_keeps_only_explicit_tool_route_owners(self) -> None:
        pack = ruc_pack()
        self.assertEqual(KEEP_SKILLS, pack.get("skill_candidates"))
        self.assertEqual(KEEP_SKILLS, pack.get("route_authority_candidates"))
        self.assertEqual([], pack.get("stage_assistant_candidates"))
        self.assertEqual({"research": "webthinker-deep-research"}, pack.get("defaults_by_task"))

        trigger_keywords = {str(item).lower() for item in pack.get("trigger_keywords") or []}
        for forbidden in ["deepagent", "toolchain", "skill chain", "memory folding", "工具链", "技能链", "记忆折叠"]:
            self.assertNotIn(forbidden, trigger_keywords)

    def test_deepagent_skill_ids_are_absent_from_live_config_surfaces(self) -> None:
        keyword_index = load_json("config/skill-keyword-index.json")
        routing_rules = load_json("config/skill-routing-rules.json")
        capability_catalog = load_json("config/capability-catalog.json")
        upstream_aliases = load_json("config/upstream-source-aliases.json")
        upstream_lock = load_json("config/upstream-lock.json")
        runtime = load_json("config/ruc-nlpir-runtime.json")
        overlays = load_json("config/ruc-nlpir-overlays.json")
        vco_overlays = load_json("config/vco-overlays.json")

        routing_skills = routing_rules.get("skills")
        self.assertIsInstance(routing_skills, dict)

        for skill in DEEPAGENT_SKILLS:
            self.assertNotIn(skill, keyword_index)
            self.assertNotIn(skill, routing_skills)
            self.assertNotIn(skill, ruc_pack().get("skill_candidates") or [])
            self.assertNotIn(skill, ruc_pack().get("route_authority_candidates") or [])
            self.assertNotIn(skill, ruc_pack().get("stage_assistant_candidates") or [])

        serialized_catalog = json.dumps(capability_catalog, ensure_ascii=False).lower()
        self.assertNotIn("deepagent", serialized_catalog)
        self.assertNotIn("deepagent-toolchain-plan", serialized_catalog)
        self.assertNotIn("deepagent-memory-fold", serialized_catalog)
        capability_ids = {str(item.get("id")) for item in capability_catalog.get("capabilities") or [] if isinstance(item, dict)}
        self.assertNotIn("toolchain_planning", capability_ids)
        self.assertNotIn("memory_folding", capability_ids)

        aliases = upstream_aliases.get("aliases")
        self.assertIsInstance(aliases, dict)
        self.assertNotIn("DeepAgent", aliases)
        self.assertNotIn("RUC-NLPIR/DeepAgent", aliases)
        self.assertNotIn("deepagent", {str(value) for value in aliases.values()})

        upstream_entries = upstream_lock.get("sources")
        if upstream_entries is None:
            upstream_entries = upstream_lock.get("upstreams")
        self.assertIsInstance(upstream_entries, list)
        serialized_upstream = json.dumps(upstream_entries, ensure_ascii=False).lower()
        self.assertNotIn("deepagent", serialized_upstream)

        repos = runtime.get("repos")
        self.assertIsInstance(repos, dict)
        self.assertEqual({"FlashRAG", "WebThinker"}, set(repos))
        self.assertEqual(
            {
                "flashrag_evidence": "auto",
                "webthinker_deep_research": "lite",
            },
            runtime.get("engine_defaults"),
        )

        overlay_text = json.dumps(overlays, ensure_ascii=False).lower()
        self.assertNotIn("deepagent", overlay_text)
        provider_text = json.dumps(vco_overlays, ensure_ascii=False).lower()
        self.assertNotIn("deepagent", provider_text)

    def test_deepagent_skill_and_overlay_files_are_physically_deleted(self) -> None:
        for relative_path in [
            "bundled/skills/deepagent-toolchain-plan",
            "bundled/skills/deepagent-memory-fold",
            "references/overlays/ruc-nlpir/deepagent-toolchain-plan.md",
            "references/overlays/ruc-nlpir/deepagent-memory-fold.md",
        ]:
            self.assertFalse((REPO_ROOT / relative_path).exists(), relative_path)

    def test_preflight_no_longer_hardcodes_deepagent(self) -> None:
        preflight = (REPO_ROOT / "scripts" / "ruc-nlpir" / "preflight.ps1").read_text(encoding="utf-8")
        self.assertNotIn("DeepAgent", preflight)
        self.assertIn("FlashRAG", preflight)
        self.assertIn("WebThinker", preflight)

    def test_deleted_deepagent_prompts_do_not_select_deleted_skills_or_pack(self) -> None:
        prompts = [
            ("用 DeepAgent 规划工具链和技能链", "planning"),
            ("请整理长会话上下文，做 memory folding", "review"),
        ]
        for prompt, task_type in prompts:
            with self.subTest(prompt=prompt):
                result = route(prompt, task_type=task_type)
                pack_id, skill = selected(result)
                self.assertNotEqual("ruc-nlpir-augmentation", pack_id, ranked_summary(result))
                self.assertNotIn(skill, DEEPAGENT_SKILLS, ranked_summary(result))

    def test_kept_tools_still_route_on_explicit_tool_prompts(self) -> None:
        local_result = route(
            "请用 FlashRAG 做本地 repo/config 证据检索，给出 SKILL.md 文件和行号，说明路由规则在哪里定义",
            task_type="review",
        )
        self.assertEqual(("ruc-nlpir-augmentation", "flashrag-evidence"), selected(local_result), ranked_summary(local_result))

        web_result = route(
            "我要做 deep research，多跳浏览网页并保留 trace.jsonl 和 sources.json 证据链",
            task_type="research",
        )
        self.assertEqual(("ruc-nlpir-augmentation", "webthinker-deep-research"), selected(web_result), ranked_summary(web_result))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and confirm it fails for current DeepAgent exposure**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_ruc_nlpir_augmentation_cleanup.py -q
```

Expected: FAIL. The failures should mention the current DeepAgent candidates, stage assistants, existing bundled directories, upstream alias/lock entries, overlays, runtime config, or route selection.

- [ ] **Step 3: Do not commit yet**

Leave the failing test staged or unstaged until the implementation in later tasks makes it pass.

## Task 2: Remove DeepAgent From Routing and Tool Configs

**Files:**

- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`
- Modify: `config/capability-catalog.json`
- Modify: `config/ruc-nlpir-runtime.json`
- Modify: `config/ruc-nlpir-overlays.json`
- Modify: `config/vco-overlays.json`
- Modify: `config/upstream-source-aliases.json`
- Modify: `config/upstream-lock.json`
- Modify: `scripts/ruc-nlpir/preflight.ps1`
- Modify: `references/overlays/index.md`
- Delete: `references/overlays/ruc-nlpir/deepagent-toolchain-plan.md`
- Delete: `references/overlays/ruc-nlpir/deepagent-memory-fold.md`

- [ ] **Step 1: Update `config/pack-manifest.json`**

Change the `ruc-nlpir-augmentation` pack so its route contract matches this shape:

```json
{
  "id": "ruc-nlpir-augmentation",
  "priority": 91,
  "grade_allow": ["M", "L", "XL"],
  "task_allow": ["planning", "review", "debug", "research"],
  "trigger_keywords": [
    "flashrag",
    "webthinker",
    "evidence plane",
    "local evidence",
    "repo evidence",
    "repo config evidence",
    "route rule evidence",
    "where is this defined",
    "skill.md",
    "file and line",
    "path and line",
    "deep research",
    "multi-hop browse",
    "trace.jsonl",
    "sources.json",
    "web source chain",
    "证据平面",
    "本地证据",
    "仓库依据",
    "配置依据",
    "路由规则在哪里",
    "文件和行号",
    "深度调研",
    "多跳浏览",
    "网页证据链",
    "保留 trace",
    "可审计"
  ],
  "skill_candidates": [
    "flashrag-evidence",
    "webthinker-deep-research"
  ],
  "route_authority_candidates": [
    "flashrag-evidence",
    "webthinker-deep-research"
  ],
  "stage_assistant_candidates": [],
  "defaults_by_task": {
    "research": "webthinker-deep-research"
  }
}
```

Keep the surrounding manifest ordering unchanged.

- [ ] **Step 2: Update `config/skill-keyword-index.json`**

Remove the `deepagent-toolchain-plan` and `deepagent-memory-fold` top-level entries.

Use these narrowed entries for the kept tools:

```json
"flashrag-evidence": {
  "keywords": [
    "flashrag",
    "local evidence",
    "repo evidence",
    "repo config evidence",
    "route rule evidence",
    "where is this defined",
    "source of truth",
    "path and line",
    "file and line",
    "skill.md",
    "本地证据",
    "仓库依据",
    "配置依据",
    "路由规则在哪里",
    "文件和行号",
    "出处"
  ]
},
"webthinker-deep-research": {
  "keywords": [
    "webthinker",
    "deep research",
    "deep research report",
    "multi-hop",
    "multi-hop browse",
    "trace.jsonl",
    "sources.json",
    "web source chain",
    "auditable web research",
    "深度调研",
    "多跳浏览",
    "网页证据链",
    "保留 trace",
    "可审计调研"
  ]
}
```

- [ ] **Step 3: Update `config/skill-routing-rules.json`**

Remove the `deepagent-toolchain-plan` and `deepagent-memory-fold` entries under `skills`.

Replace the `flashrag-evidence` entry with:

```json
"flashrag-evidence": {
  "task_allow": ["planning", "review", "debug", "research"],
  "positive_keywords": [
    "flashrag",
    "local evidence",
    "repo evidence",
    "repo config evidence",
    "route rule evidence",
    "where is this defined",
    "source of truth",
    "path and line",
    "file and line",
    "skill.md",
    "本地证据",
    "仓库依据",
    "配置依据",
    "路由规则在哪里",
    "文件和行号",
    "出处"
  ],
  "negative_keywords": [
    "webthinker",
    "deep research",
    "multi-hop",
    "trace.jsonl",
    "sources.json",
    "web source chain",
    "literature review",
    "paper writing",
    "pdf extraction",
    "scientific visualization",
    "model training",
    "深度调研",
    "多跳浏览",
    "网页证据链",
    "论文撰写",
    "文献综述",
    "模型训练",
    "可视化"
  ],
  "equivalent_group": "evidence-retrieval",
  "canonical_for_task": []
}
```

Replace the `webthinker-deep-research` entry with:

```json
"webthinker-deep-research": {
  "task_allow": ["planning", "research"],
  "positive_keywords": [
    "webthinker",
    "deep research",
    "deep research report",
    "multi-hop",
    "multi-hop browse",
    "trace.jsonl",
    "sources.json",
    "web source chain",
    "auditable web research",
    "深度调研",
    "多跳浏览",
    "网页证据链",
    "保留 trace",
    "可审计调研"
  ],
  "negative_keywords": [
    "flashrag",
    "local evidence",
    "repo evidence",
    "repo config evidence",
    "where is this defined",
    "path and line",
    "skill.md",
    "pdf extraction",
    "latex build",
    "scientific visualization",
    "browser automation",
    "web scraping",
    "本地证据",
    "仓库依据",
    "文件和行号",
    "PDF提取",
    "LaTeX构建",
    "科研绘图",
    "浏览器自动化",
    "网页抓取"
  ],
  "equivalent_group": "deep-research",
  "canonical_for_task": ["research"]
}
```

- [ ] **Step 4: Update `config/capability-catalog.json`**

Delete the two capability objects whose ids are `toolchain_planning` and `memory_folding`.

Remove `toolchain_planning` from every remaining `dedup_with` list. Do not replace it with another planning helper id.

Keep `local_evidence_retrieval` and `deep_web_research`, but make sure their `skills` arrays do not mention DeepAgent:

```json
"skills": [
  "flashrag-evidence",
  "verification-quality-assurance",
  "context-hunter"
]
```

```json
"skills": [
  "webthinker-deep-research",
  "research-lookup",
  "playwright"
]
```

- [ ] **Step 5: Update `config/ruc-nlpir-runtime.json`**

Remove the `DeepAgent` repo entry and both DeepAgent engine defaults. The retained runtime shape must include:

```json
"repos": {
  "FlashRAG": {
    "upstream_repo": "https://github.com/RUC-NLPIR/FlashRAG",
    "path": "${VCO_EXTERNAL_ROOT}/ruc-nlpir/FlashRAG",
    "expected_commit": "6aca76d1325c0eed9e00fba6ec692bf8b8a52b39",
    "requirements_relpath": "requirements.txt",
    "license_relpath": "LICENSE"
  },
  "WebThinker": {
    "upstream_repo": "https://github.com/RUC-NLPIR/WebThinker",
    "path": "${VCO_EXTERNAL_ROOT}/ruc-nlpir/WebThinker",
    "expected_commit": "db387eb3261de9b5e2db7d2d7fb20af2aceb7882",
    "requirements_relpath": "requirements.txt",
    "license_relpath": "LICENSE"
  }
},
"engine_defaults": {
  "flashrag_evidence": "auto",
  "webthinker_deep_research": "lite"
}
```

- [ ] **Step 6: Update `scripts/ruc-nlpir/preflight.ps1`**

Replace the hardcoded repo loop:

```powershell
foreach ($name in @("FlashRAG", "WebThinker", "DeepAgent")) {
```

with a loop over the runtime config:

```powershell
$repoNames = @($runtime.repos.PSObject.Properties.Name | Sort-Object)
foreach ($name in $repoNames) {
```

This keeps the preflight aligned with the two retained runtime repos and removes the live DeepAgent preflight handle.

- [ ] **Step 7: Update overlay configs and references**

In `config/ruc-nlpir-overlays.json`, remove DeepAgent fallback ids and delete the two DeepAgent overlay objects. The final overlay ids must be exactly:

```json
["ruc-flashrag-evidence", "ruc-webthinker-deep-research"]
```

Use stage fallbacks that do not create hidden helper behavior:

```json
"stage_fallbacks": {
  "think": ["ruc-flashrag-evidence", "ruc-webthinker-deep-research"],
  "do": ["ruc-flashrag-evidence"],
  "review": ["ruc-flashrag-evidence"],
  "research": ["ruc-webthinker-deep-research"],
  "team": [],
  "retro": [],
  "any": []
}
```

In `config/vco-overlays.json`, change the provider name to:

```json
"name": "RUC-NLPIR Tools (FlashRAG / WebThinker)"
```

In `references/overlays/index.md`, change the RUC-NLPIR row to:

```markdown
| [`ruc-nlpir`](ruc-nlpir) | FlashRAG / WebThinker tool overlay references |
```

Delete:

```text
references/overlays/ruc-nlpir/deepagent-toolchain-plan.md
references/overlays/ruc-nlpir/deepagent-memory-fold.md
```

- [ ] **Step 8: Update upstream reimport handles**

In `config/upstream-source-aliases.json`, remove:

```json
"DeepAgent": "deepagent",
"RUC-NLPIR/DeepAgent": "deepagent"
```

In `config/upstream-lock.json`, delete the source object whose `id` is `RUC-NLPIR/DeepAgent`.

- [ ] **Step 9: Run JSON parse checks**

Run:

```powershell
python -m json.tool config/pack-manifest.json > $null
python -m json.tool config/skill-keyword-index.json > $null
python -m json.tool config/skill-routing-rules.json > $null
python -m json.tool config/capability-catalog.json > $null
python -m json.tool config/ruc-nlpir-runtime.json > $null
python -m json.tool config/ruc-nlpir-overlays.json > $null
python -m json.tool config/vco-overlays.json > $null
python -m json.tool config/upstream-source-aliases.json > $null
python -m json.tool config/upstream-lock.json > $null
```

Expected: all commands exit 0.

## Task 3: Physically Delete DeepAgent Bundled Skill Directories

**Files:**

- Delete: `bundled/skills/deepagent-toolchain-plan/SKILL.md`
- Delete: `bundled/skills/deepagent-memory-fold/SKILL.md`
- Modify: `config/skills-lock.json`

- [ ] **Step 1: Verify the deletion targets are inside the repo**

Run:

```powershell
$repo = (Resolve-Path .).Path
$targets = @(
  'bundled\skills\deepagent-toolchain-plan',
  'bundled\skills\deepagent-memory-fold'
)
foreach ($target in $targets) {
  $resolved = (Resolve-Path -LiteralPath $target).Path
  if (-not $resolved.StartsWith($repo, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Unsafe delete target outside repo: $resolved"
  }
  Get-ChildItem -LiteralPath $resolved -Force -Recurse | Select-Object FullName, Length
}
```

Expected: each directory contains only `SKILL.md`.

- [ ] **Step 2: Delete the two DeepAgent skill files and empty directories**

Use `apply_patch` to delete:

```text
bundled/skills/deepagent-toolchain-plan/SKILL.md
bundled/skills/deepagent-memory-fold/SKILL.md
```

Then remove the empty directories:

```powershell
Remove-Item -LiteralPath 'bundled\skills\deepagent-toolchain-plan' -Force
Remove-Item -LiteralPath 'bundled\skills\deepagent-memory-fold' -Force
```

Expected: both directories no longer exist.

- [ ] **Step 3: Regenerate `config/skills-lock.json`**

Run:

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected: command exits 0 and prints `skills-lock generated`.

- [ ] **Step 4: Confirm the lock no longer mentions DeepAgent skills**

Run:

```powershell
Select-String -LiteralPath 'config\skills-lock.json' -Pattern 'deepagent' -CaseSensitive:$false
```

Expected: no output.

## Task 4: Update Router Bridge Regression

**Files:**

- Modify: `tests/runtime_neutral/test_router_bridge.py`

- [ ] **Step 1: Replace the legacy stage-assistant test**

Replace `test_deep_research_pack_records_deepagent_helpers_as_legacy_stage_assistants` with:

```python
    def test_deep_research_pack_has_no_legacy_stage_assistants(self) -> None:
        result = run_bridge(
            "我要做 deep research，多跳浏览网页并保留 trace.jsonl 和 sources.json 证据链",
            "L",
            "research",
        )

        self.assertEqual("ruc-nlpir-augmentation", result["selected"]["pack_id"])
        self.assertEqual("webthinker-deep-research", result["selected"]["skill"])

        deep_research_row = next(row for row in result["ranked"] if row["pack_id"] == "ruc-nlpir-augmentation")
        ranking_by_skill = {row["skill"]: row for row in deep_research_row["candidate_ranking"]}
        self.assertEqual({"flashrag-evidence", "webthinker-deep-research"}, set(ranking_by_skill))
        self.assertEqual("route_authority", ranking_by_skill["webthinker-deep-research"]["legacy_role"])
        self.assertEqual("route_authority", ranking_by_skill["flashrag-evidence"]["legacy_role"])
        self.assertEqual([], deep_research_row["stage_assistant_candidates"])
```

- [ ] **Step 2: Run the focused bridge tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_ruc_nlpir_augmentation_cleanup.py tests/runtime_neutral/test_router_bridge.py -q
```

Expected: all selected tests pass. If the new route prompts reveal overly weak FlashRAG/WebThinker keywords, adjust only the kept tool keyword lists; do not re-add DeepAgent keywords.

## Task 5: Add Governance Note

**Files:**

- Create: `docs/governance/ruc-nlpir-augmentation-tool-pack-cleanup-2026-04-29.md`

- [ ] **Step 1: Write the governance note**

Create the governance note with this content:

```markdown
# RUC-NLPIR Augmentation Tool Pack Cleanup

Date: 2026-04-29

## Decision

`ruc-nlpir-augmentation` is now an explicit two-tool pack:

| Tool | Ownership |
| --- | --- |
| `flashrag-evidence` | Local repo/config/governance evidence lookup with file and line anchors |
| `webthinker-deep-research` | Auditable multi-hop web research with `report.md`, `sources.json`, and `trace.jsonl` |

The pack no longer exposes DeepAgent as a skill, helper, stage assistant, overlay, runtime repo, capability, or upstream reimport handle.

## Before / After

| Surface | Before | After |
| --- | --- | --- |
| `skill_candidates` | 4 | 2 |
| `route_authority_candidates` | 2 | 2 |
| `stage_assistant_candidates` | 2 | 0 |
| `defaults_by_task` | planning/review/debug -> `flashrag-evidence`; research -> `webthinker-deep-research` | research -> `webthinker-deep-research` |
| Bundled DeepAgent skills | `deepagent-toolchain-plan`, `deepagent-memory-fold` | none |
| RUC-NLPIR runtime repos | FlashRAG, WebThinker, DeepAgent | FlashRAG, WebThinker |

## Trigger Boundary

`flashrag-evidence` is selected only for explicit local evidence lookup, such as repo/config evidence, route rule evidence, `SKILL.md` source-of-truth lookup, or file-and-line citation requests.

`webthinker-deep-research` is selected only for explicit auditable web research, such as deep research, multi-hop browsing, `trace.jsonl`, `sources.json`, or web evidence-chain requests.

DeepAgent prompts such as toolchain planning, skill-chain planning, memory folding, and context compression do not route to this pack.

## Verification

Protected by:

- `tests/runtime_neutral/test_ruc_nlpir_augmentation_cleanup.py`
- `tests/runtime_neutral/test_router_bridge.py`
- `scripts/verify/vibe-pack-regression-matrix.ps1`
- `scripts/verify/vibe-pack-routing-smoke.ps1`
- `scripts/verify/vibe-routing-stability-gate.ps1`
- `scripts/verify/vibe-offline-skills-gate.ps1`
- `scripts/verify/vibe-config-parity-gate.ps1`
- `scripts/verify/vibe-capability-catalog-gate.ps1`

## Non-Changes

This cleanup does not change Vibe's six-stage runtime and does not introduce a replacement helper, assistant, or consultation role.
```

- [ ] **Step 2: Check governance note for stale helper wording**

Run:

```powershell
Select-String -LiteralPath 'docs\governance\ruc-nlpir-augmentation-tool-pack-cleanup-2026-04-29.md' -Pattern 'assistant|consultation|secondary|helper|stage assistant|辅助|咨询|次技能' -CaseSensitive:$false
```

Expected: either no output or only the sentence stating that these roles were removed.

## Task 6: Run Verification Gates and Commit

**Files:**

- All files changed in Tasks 1-5.

- [ ] **Step 1: Run focused tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_ruc_nlpir_augmentation_cleanup.py tests/runtime_neutral/test_router_bridge.py -q
```

Expected: pass.

- [ ] **Step 2: Run routing and config gates**

Run:

```powershell
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-routing-stability-gate.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-capability-catalog-gate.ps1
```

Expected: every gate exits 0. `vibe-config-parity-gate.ps1 -WriteArtifacts` may update governance output artifacts; include only expected source or generated governance artifacts in the commit.

- [ ] **Step 3: Run repository hygiene checks**

Run:

```powershell
git diff --check
git status --short
```

Expected: `git diff --check` exits 0. `git status --short` shows only the intended config, test, governance, skill deletion, overlay deletion, and lock changes.

- [ ] **Step 4: Commit the implementation**

Run:

```powershell
git add -- config/pack-manifest.json config/skill-keyword-index.json config/skill-routing-rules.json config/capability-catalog.json config/ruc-nlpir-runtime.json config/ruc-nlpir-overlays.json config/vco-overlays.json config/upstream-source-aliases.json config/upstream-lock.json config/skills-lock.json scripts/ruc-nlpir/preflight.ps1 references/overlays/index.md tests/runtime_neutral/test_ruc_nlpir_augmentation_cleanup.py tests/runtime_neutral/test_router_bridge.py docs/governance/ruc-nlpir-augmentation-tool-pack-cleanup-2026-04-29.md
git add -u -- bundled/skills/deepagent-toolchain-plan bundled/skills/deepagent-memory-fold references/overlays/ruc-nlpir/deepagent-toolchain-plan.md references/overlays/ruc-nlpir/deepagent-memory-fold.md
git commit -m "fix: simplify ruc nlpir augmentation routing"
```

Expected: commit succeeds with only the intended cleanup files.

- [ ] **Step 5: Report completion**

Report:

- branch and commit hash
- before/after counts: 4 -> 2 candidates, 2 -> 0 stage assistants
- deleted directories and overlay files
- kept route owners and their trigger boundaries
- verification commands and pass/fail status
- any gate that could not be run, with the exact reason

## Self-Review Checklist

- Spec coverage: every spec acceptance criterion maps to a test or gate in this plan.
- Completeness scan: every step has concrete files, commands, and expected outcomes.
- Scope control: this plan only touches `ruc-nlpir-augmentation` and directly related RUC-NLPIR config/reference surfaces.
- Runtime control: Vibe's six-stage runtime is unchanged.
- Routing model: the result remains `candidate -> selected -> used / unused`; there is no new primary/secondary/helper/stage-assistant mechanism.
