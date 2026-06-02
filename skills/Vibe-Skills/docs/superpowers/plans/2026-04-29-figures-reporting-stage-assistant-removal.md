# Figures And Reporting Stage Assistant Removal Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove legacy stage-assistant routing from `science-figures-visualization` and `science-reporting` while preserving direct figure, schematic, report, and writing routes.

**Architecture:** This is a routing-contract cleanup. The live behavior is driven by `config/pack-manifest.json`, `config/skill-keyword-index.json`, and `config/skill-routing-rules.json`; tests call both the Python router contract and the PowerShell runtime freeze path because legacy stage-assistant data still leaks into runtime packets.

**Tech Stack:** Python unittest/pytest, PowerShell route probes, JSON routing config, Vibe-Skills governance docs, `skills-lock.json` refresh.

---

## File Map

- Create `tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py`: focused RED/GREEN coverage for the two pack manifests and candidate metadata.
- Modify `config/pack-manifest.json`: remove library/helper candidates from the two pack candidate surfaces and set both `stage_assistant_candidates` lists to `[]`.
- Modify `tests/runtime_neutral/test_bundled_stage_assistant_freeze.py`: update legacy freeze assertions so matplotlib/seaborn/plotly are no longer expected as stage hints.
- Modify `tests/runtime_neutral/test_router_bridge.py`: replace legacy-role assertions for plotting helpers with binary candidate-surface assertions.
- Modify `scripts/verify/probe-scientific-packs.ps1`: add route probes for matplotlib/seaborn/plotly library-wording prompts and reporting/diagram boundaries.
- Modify `scripts/verify/vibe-skill-index-routing-audit.ps1`: add representative route cases for the cleaned figure/reporting boundaries.
- Modify `scripts/verify/vibe-pack-regression-matrix.ps1`: add broader matrix cases so the two pack contracts stay protected.
- Create `docs/governance/figures-reporting-stage-assistant-removal-2026-04-29.md`: governance note for the cleanup.
- Modify `config/skills-lock.json`: refresh generated lock metadata after config and docs are stable.

## Task 1: Focused RED Tests

**Files:**
- Create: `tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py`

- [ ] **Step 1: Write the focused tests**

Create `tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py`:

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


def load_pack(pack_id: str) -> dict[str, object]:
    manifest = json.loads((REPO_ROOT / "config" / "pack-manifest.json").read_text(encoding="utf-8-sig"))
    return next(pack for pack in manifest["packs"] if pack["id"] == pack_id)


def route(prompt: str, task_type: str = "research", grade: str = "L") -> dict[str, object]:
    return route_prompt(prompt=prompt, grade=grade, task_type=task_type, repo_root=REPO_ROOT)


def selected(result: dict[str, object]) -> tuple[str, str]:
    selected_row = result.get("selected")
    assert isinstance(selected_row, dict), result
    return str(selected_row.get("pack_id") or ""), str(selected_row.get("skill") or "")


def pack_row(result: dict[str, object], pack_id: str) -> dict[str, object]:
    ranked = result.get("ranked")
    assert isinstance(ranked, list), result
    row = next((item for item in ranked if isinstance(item, dict) and item.get("pack_id") == pack_id), None)
    assert isinstance(row, dict), result
    return row


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


class FiguresReportingStageAssistantRemovalTests(unittest.TestCase):
    def assert_selected(
        self,
        prompt: str,
        expected_pack: str,
        expected_skill: str,
        *,
        task_type: str = "research",
        grade: str = "L",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertEqual((expected_pack, expected_skill), selected(result), ranked_summary(result))

    def test_figures_pack_has_only_direct_problem_owners(self) -> None:
        pack = load_pack("science-figures-visualization")
        expected = ["scientific-visualization", "scientific-schematics"]
        self.assertEqual(expected, pack["skill_candidates"])
        self.assertEqual(expected, pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])

    def test_reporting_pack_has_only_direct_problem_owners(self) -> None:
        pack = load_pack("science-reporting")
        expected = ["scientific-reporting", "scientific-writing"]
        self.assertEqual(expected, pack["skill_candidates"])
        self.assertEqual(expected, pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])

    def test_plotting_library_words_still_route_to_scientific_visualization(self) -> None:
        prompts = [
            "用 matplotlib 绘制 publication-ready result figure，600dpi TIFF，带误差棒和显著性标注",
            "用 seaborn 画模型评估结果图和投稿图，要求色盲友好配色",
            "用 plotly 做 interactive result figure，并导出 HTML figure 给科研报告使用",
        ]
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                self.assert_selected(
                    prompt,
                    "science-figures-visualization",
                    "scientific-visualization",
                    task_type="coding",
                )

    def test_figures_candidate_metadata_has_no_plotting_stage_assistants(self) -> None:
        result = route(
            "帮我做科研绘图，产出期刊级 figure，多面板、颜色无障碍、矢量导出",
            task_type="research",
            grade="L",
        )
        row = pack_row(result, "science-figures-visualization")
        ranking = row.get("candidate_ranking")
        assert isinstance(ranking, list), row
        ranking_skills = {str(item.get("skill") or "") for item in ranking if isinstance(item, dict)}
        self.assertEqual({"scientific-visualization", "scientific-schematics"}, ranking_skills)
        self.assertEqual([], row.get("stage_assistant_candidates"))

    def test_schematics_route_to_scientific_schematics(self) -> None:
        self.assert_selected(
            "用 Mermaid 写一个实验流程图 flowchart，并给出可复制 markdown",
            "science-figures-visualization",
            "scientific-schematics",
            task_type="coding",
            grade="M",
        )

    def test_reporting_routes_remain_stable(self) -> None:
        self.assert_selected(
            "科研技术报告：包含方法结果讨论，输出 HTML 和 PDF，附录写清复现步骤",
            "science-reporting",
            "scientific-reporting",
            task_type="planning",
            grade="L",
        )

    def test_reporting_candidate_metadata_has_no_figure_or_mermaid_stage_assistants(self) -> None:
        result = route(
            "请把我们现有实验结果整理成 research report，带 executive summary、appendix、Quarto/PDF 导出",
            task_type="research",
            grade="L",
        )
        row = pack_row(result, "science-reporting")
        ranking = row.get("candidate_ranking")
        assert isinstance(ranking, list), row
        ranking_skills = {str(item.get("skill") or "") for item in ranking if isinstance(item, dict)}
        self.assertEqual({"scientific-reporting", "scientific-writing"}, ranking_skills)
        self.assertEqual([], row.get("stage_assistant_candidates"))

    def test_manuscript_prose_still_selects_scientific_writing(self) -> None:
        result = route("请按 IMRAD 结构写科研论文正文", task_type="research", grade="L")
        self.assertEqual("scientific-writing", selected(result)[1], ranked_summary(result))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py -q
```

Expected: FAIL. The expected failures are manifest assertions and candidate metadata assertions because `matplotlib`, `seaborn`, `plotly`, `scientific-visualization`, `scientific-schematics`, and `markdown-mermaid-writing` are still present as stage-assistant-era pack candidates.

## Task 2: Manifest Cleanup

**Files:**
- Modify: `config/pack-manifest.json`

- [ ] **Step 1: Edit `science-figures-visualization` candidate lists**

In `config/pack-manifest.json`, change the `science-figures-visualization` block so the relevant lists are exactly:

```json
"skill_candidates": [
  "scientific-visualization",
  "scientific-schematics"
],
"route_authority_candidates": [
  "scientific-visualization",
  "scientific-schematics"
],
"stage_assistant_candidates": [],
```

Do not remove trigger keywords such as `matplotlib`, `seaborn`, or `plotly`; those words should still help route library-worded figure prompts to `scientific-visualization`.

- [ ] **Step 2: Edit `science-reporting` candidate lists**

In `config/pack-manifest.json`, change the `science-reporting` block so the relevant lists are exactly:

```json
"skill_candidates": [
  "scientific-reporting",
  "scientific-writing"
],
"route_authority_candidates": [
  "scientific-reporting",
  "scientific-writing"
],
"stage_assistant_candidates": [],
```

Do not change `defaults_by_task`; it should remain:

```json
"defaults_by_task": {
  "planning": "scientific-reporting",
  "coding": "scientific-reporting",
  "research": "scientific-reporting"
}
```

- [ ] **Step 3: Run focused test and verify the manifest assertions pass**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py -q
```

Expected: PASS for the new focused test file. If it fails, inspect whether the failure is due to route scoring or because the manifest still has old candidate names.

## Task 3: Update Legacy Runtime And Router Tests

**Files:**
- Modify: `tests/runtime_neutral/test_bundled_stage_assistant_freeze.py`
- Modify: `tests/runtime_neutral/test_router_bridge.py`

- [ ] **Step 1: Update runtime freeze stage-assistant assertions**

In `tests/runtime_neutral/test_bundled_stage_assistant_freeze.py`, replace the final `hint_pairs` assertions with:

```python
            hint_pairs = [
                (item["skill_id"], item["source"])
                for item in legacy["stage_assistant_hints"]
            ]
            self.assertNotIn(("matplotlib", "route_stage_assistant"), hint_pairs)
            self.assertNotIn(("seaborn", "route_stage_assistant"), hint_pairs)
            self.assertNotIn(("plotly", "route_stage_assistant"), hint_pairs)

            selected_ids = [
                item["skill_id"]
                for item in packet["skill_routing"]["selected"]
            ]
            self.assertEqual(["scientific-visualization"], selected_ids)
```

Keep the earlier assertions that the runtime-selected skill is `vibe` and the route snapshot selected `science-figures-visualization / scientific-visualization`.

- [ ] **Step 2: Update router bridge candidate metadata assertions**

In `tests/runtime_neutral/test_router_bridge.py`, rename the test:

```python
    def test_scientific_figure_route_uses_only_direct_figure_candidates(self) -> None:
```

Replace the legacy-role assertions in that test with:

```python
        figure_row = next(row for row in result["ranked"] if row["pack_id"] == "science-figures-visualization")
        ranking_by_skill = {row["skill"]: row for row in figure_row["candidate_ranking"]}
        self.assertEqual(
            {"scientific-visualization", "scientific-schematics"},
            set(ranking_by_skill),
        )
        self.assertEqual("route_authority", ranking_by_skill["scientific-visualization"]["legacy_role"])
        self.assertEqual("route_authority", ranking_by_skill["scientific-schematics"]["legacy_role"])
        self.assertEqual([], figure_row["stage_assistant_candidates"])
```

Remove assertions that expect `matplotlib`, `seaborn`, or `plotly` in `candidate_ranking` or `stage_assistant_candidates`.

- [ ] **Step 3: Run updated tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bundled_stage_assistant_freeze.py tests/runtime_neutral/test_router_bridge.py -q
```

Expected: PASS. If `test_bundled_stage_assistant_freeze.py` fails because `skill_routing.selected` contains `vibe` instead of `scientific-visualization`, inspect the generated packet and assert only the stable simplified routing field that contains the selected specialist; keep the no-stage-assistant assertions.

## Task 4: Script Probe Coverage

**Files:**
- Modify: `scripts/verify/probe-scientific-packs.ps1`
- Modify: `scripts/verify/vibe-skill-index-routing-audit.ps1`
- Modify: `scripts/verify/vibe-pack-regression-matrix.ps1`

- [ ] **Step 1: Extend scientific pack probes**

In `scripts/verify/probe-scientific-packs.ps1`, add these cases near the existing `science-figures-visualization` / `science-reporting` route probes:

```powershell
    [pscustomobject]@{
        name = "figures_matplotlib_library_wording"
        group = "science-figures-visualization"
        prompt = "/vibe 用 matplotlib 绘制 publication-ready result figure，600dpi TIFF，带误差棒和显著性标注"
        grade = "L"
        task_type = "coding"
        expected_pack = "science-figures-visualization"
        expected_skill = "scientific-visualization"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "figures_seaborn_library_wording"
        group = "science-figures-visualization"
        prompt = "/vibe 用 seaborn 画模型评估结果图和投稿图，要求色盲友好配色"
        grade = "L"
        task_type = "coding"
        expected_pack = "science-figures-visualization"
        expected_skill = "scientific-visualization"
        requested_skill = $null
    },
    [pscustomobject]@{
        name = "figures_mermaid_schematic"
        group = "science-figures-visualization"
        prompt = "/vibe 用 Mermaid 写一个实验流程图 flowchart，并给出可复制 markdown"
        grade = "M"
        task_type = "coding"
        expected_pack = "science-figures-visualization"
        expected_skill = "scientific-schematics"
        requested_skill = $null
    },
```

- [ ] **Step 2: Extend skill-index audit**

In `scripts/verify/vibe-skill-index-routing-audit.ps1`, add:

```powershell
    [pscustomobject]@{ Name = "matplotlib library wording still visualizer"; Prompt = "用 matplotlib 绘制 publication-ready result figure，600dpi TIFF，带误差棒和显著性标注"; Grade = "L"; TaskType = "coding"; ExpectedPack = "science-figures-visualization"; ExpectedSkill = "scientific-visualization" },
    [pscustomobject]@{ Name = "seaborn library wording still visualizer"; Prompt = "用 seaborn 画模型评估结果图和投稿图，要求色盲友好配色"; Grade = "L"; TaskType = "coding"; ExpectedPack = "science-figures-visualization"; ExpectedSkill = "scientific-visualization" },
    [pscustomobject]@{ Name = "reporting html pdf direct owner"; Prompt = "科研技术报告：包含方法结果讨论，输出 HTML 和 PDF，附录写清复现步骤"; Grade = "L"; TaskType = "planning"; ExpectedPack = "science-reporting"; ExpectedSkill = "scientific-reporting" },
```

Place these near the existing scientific figures and scientific report cases.

- [ ] **Step 3: Extend pack regression matrix**

In `scripts/verify/vibe-pack-regression-matrix.ps1`, add:

```powershell
    [pscustomobject]@{ Name = "figures matplotlib wording direct owner"; Prompt = "用 matplotlib 绘制 publication-ready result figure，600dpi TIFF，带误差棒和显著性标注"; Grade = "L"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = "science-figures-visualization"; ExpectedSkill = "scientific-visualization"; AllowedModes = @("pack_overlay", "confirm_required") },
    [pscustomobject]@{ Name = "figures mermaid schematic direct owner"; Prompt = "用 Mermaid 写一个实验流程图 flowchart，并给出可复制 markdown"; Grade = "M"; TaskType = "coding"; RequestedSkill = $null; ExpectedPack = "science-figures-visualization"; ExpectedSkill = "scientific-schematics"; AllowedModes = @("pack_overlay", "confirm_required") },
    [pscustomobject]@{ Name = "science reporting html pdf direct owner"; Prompt = "科研技术报告：包含方法结果讨论，输出 HTML 和 PDF，附录写清复现步骤"; Grade = "L"; TaskType = "planning"; RequestedSkill = $null; ExpectedPack = "science-reporting"; ExpectedSkill = "scientific-reporting"; AllowedModes = @("pack_overlay", "confirm_required") },
```

- [ ] **Step 4: Run route scripts**

Run:

```powershell
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
```

Expected:

```text
probe-scientific-packs.ps1 exits 0 and outputs no route mismatches in outputs/verify/route-probe-scientific/summary.json
vibe-skill-index-routing-audit.ps1 exits 0 with 0 failed assertions
vibe-pack-regression-matrix.ps1 exits 0 with 0 failed assertions
```

## Task 5: Governance Note

**Files:**
- Create: `docs/governance/figures-reporting-stage-assistant-removal-2026-04-29.md`

- [ ] **Step 1: Write governance record**

Create `docs/governance/figures-reporting-stage-assistant-removal-2026-04-29.md`:

```markdown
# Figures And Reporting Stage Assistant Removal

Date: 2026-04-29

## Scope

This pass cleans only:

- `science-figures-visualization`
- `science-reporting`

It preserves the public six-stage Vibe runtime and follows the simplified routing contract:

```text
candidate -> selected -> used / unused
```

## Before And After

| Pack | Before | After |
| --- | --- | --- |
| `science-figures-visualization` | 5 candidates, 2 route owners, 3 stage assistants | 2 direct candidates, 2 route owners, 0 stage assistants |
| `science-reporting` | 5 candidates, 2 route owners, 3 stage assistants | 2 direct candidates, 2 route owners, 0 stage assistants |

## Direct Owners

| Pack | Skill | Direct ownership |
| --- | --- | --- |
| `science-figures-visualization` | `scientific-visualization` | Publication/result/model-evaluation figures and data visualization. |
| `science-figures-visualization` | `scientific-schematics` | Scientific diagrams, flowcharts, mechanism schematics, graphical abstracts. |
| `science-reporting` | `scientific-reporting` | Scientific and technical reports with HTML/PDF, appendices, and reproducibility sections. |
| `science-reporting` | `scientific-writing` | Scientific prose and manuscript-body writing. |

## Moved Out Of Pack Candidate Surfaces

| Skill | Previous pack surface | Decision |
| --- | --- | --- |
| `matplotlib` | `science-figures-visualization` stage assistant | Removed from routed candidate surface; used as implementation library under `scientific-visualization` when needed. |
| `seaborn` | `science-figures-visualization` stage assistant | Removed from routed candidate surface; used as implementation library under `scientific-visualization` when needed. |
| `plotly` | `science-figures-visualization` stage assistant | Removed from routed candidate surface; used as implementation library under `scientific-visualization` when needed. |
| `scientific-visualization` | `science-reporting` stage assistant | Owned by `science-figures-visualization`; report tasks should route figure work as a separate selected slice. |
| `scientific-schematics` | `science-reporting` stage assistant | Owned by `science-figures-visualization`; diagram work should route as a separate selected slice. |
| `markdown-mermaid-writing` | `science-reporting` stage assistant | Removed from reporting helper surface; Mermaid/flowchart requests route to `scientific-schematics`. |

## Deletion Position

No bundled skill directory is physically deleted in this pass.

## Verification

```powershell
python -m pytest tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py -q
python -m pytest tests/runtime_neutral/test_bundled_stage_assistant_freeze.py tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py -q
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```
```

- [ ] **Step 2: Run focused tests again**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py -q
```

Expected: PASS.

## Task 6: Full Verification And Commits

**Files:**
- Modify: `config/skills-lock.json`

- [ ] **Step 1: Run broad verification**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py -q
python -m pytest tests/runtime_neutral/test_bundled_stage_assistant_freeze.py tests/runtime_neutral/test_router_bridge.py tests/runtime_neutral/test_docs_research_publishing_boundary_routing.py -q
.\scripts\verify\probe-scientific-packs.ps1
.\scripts\verify\vibe-skill-index-routing-audit.ps1
.\scripts\verify\vibe-pack-regression-matrix.ps1
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-generate-skills-lock.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
git diff --check
```

Expected:

```text
All pytest commands exit 0.
All PowerShell gates exit 0.
vibe-pack-routing-smoke reports 0 failed assertions.
vibe-offline-skills-gate reports PASS.
vibe-config-parity-gate reports PASS.
git diff --check exits 0.
```

- [ ] **Step 2: Inspect diffs**

Run:

```powershell
git status --short --branch
git diff --stat
git diff -- config/skills-lock.json
```

Expected:

```text
Config/test/script/governance changes are present.
config/skills-lock.json changes only generated_at.
```

- [ ] **Step 3: Commit implementation without lock timestamp**

Run:

```powershell
git add config/pack-manifest.json `
  tests/runtime_neutral/test_figures_reporting_stage_assistant_removal.py `
  tests/runtime_neutral/test_bundled_stage_assistant_freeze.py `
  tests/runtime_neutral/test_router_bridge.py `
  scripts/verify/probe-scientific-packs.ps1 `
  scripts/verify/vibe-skill-index-routing-audit.ps1 `
  scripts/verify/vibe-pack-regression-matrix.ps1 `
  docs/governance/figures-reporting-stage-assistant-removal-2026-04-29.md
git commit -m "fix: remove figures reporting stage assistants"
```

- [ ] **Step 4: Commit lock refresh separately**

If `config/skills-lock.json` changed only by `generated_at`, run:

```powershell
git add config/skills-lock.json
git commit -m "chore: refresh skills lock after figures reporting cleanup"
```

- [ ] **Step 5: Final status check**

Run:

```powershell
git status --short --branch
git log -4 --oneline
```

Expected:

```text
Working tree is clean.
The two new implementation commits are visible above the plan/spec commits.
```

## Self-Review Notes

- Spec coverage: Tasks cover manifest cleanup, legacy test update, route probe coverage, governance note, lock refresh, and broad verification.
- Scope control: The plan does not modify `data-ml`, `code-quality`, `ruc-nlpir-augmentation`, or `aios-core`.
- Deletion boundary: The plan does not physically delete skill directories.
- Simplified routing: The plan removes `stage_assistant_candidates` from both target packs and replaces old helper expectations with direct candidate-surface assertions.
