# Zero Route Authority Third Pass Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish the remaining single-skill zero-route-authority pack cleanup by making all 14 retained packs explicit direct route owners with route rules and regression coverage.

**Architecture:** This is a routing-contract cleanup. The live behavior is driven by `config/pack-manifest.json`, `config/skill-keyword-index.json`, `config/skill-routing-rules.json`, bundled skill directories, and `config/skills-lock.json`; tests call `vgo_runtime.router_contract_runtime.route_prompt()` to prove prompt-level selection.

**Tech Stack:** Python `unittest`/`pytest`, JSON routing config, PowerShell verification scripts, Vibe-Skills bundled `SKILL.md` directories.

---

## File Map

- Create `tests/runtime_neutral/test_zero_route_authority_third_pass.py`: focused RED/GREEN tests for all 14 remaining zero-route-authority packs.
- Modify `config/pack-manifest.json`: add direct route ownership and empty `stage_assistant_candidates` for all 14 retained single-skill packs.
- Modify `config/skill-keyword-index.json`: add narrow natural-language trigger keywords for retained skills.
- Modify `config/skill-routing-rules.json`: add or narrow positive/negative route rules for retained skills and false-positive boundaries.
- Create `docs/governance/zero-route-authority-third-pass-2026-04-30.md`: governance record for retained owners, why no directories were deleted, and verification results.
- Modify `config/skills-lock.json`: regenerate after config/docs/test changes are stable.

## Current Decision From Pre-Plan Inspection

The design allowed `fluidsim` and `rowan` to be deleted, retained, or manual-reviewed after inspection. The pre-plan inspection found both are asset-bearing and have clear task ownership:

```text
fluidsim: SKILL.md plus 6 references; owns computational fluid dynamics simulation workflows.
rowan: SKILL.md plus 6 references; owns Rowan cloud quantum-chemistry workflows, not a generic quaternion helper.
```

Implementation target for this plan:

```text
Keep all 14 remaining single-skill packs as direct route owners.
Perform no physical skill directory deletion in this pass.
Reduce remaining zero-route-authority pack count to 0.
```

## Target Direct Owners

| Pack | Skill |
| --- | --- |
| `docs-markitdown-conversion` | `markitdown` |
| `ip-uspto-patents` | `uspto-database` |
| `science-astropy` | `astropy` |
| `science-pymatgen` | `pymatgen` |
| `science-simpy-simulation` | `simpy` |
| `science-fluidsim-cfd` | `fluidsim` |
| `science-matchms-spectra` | `matchms` |
| `science-matlab-octave` | `matlab` |
| `science-neuropixels` | `neuropixels-analysis` |
| `science-pymc-bayesian` | `pymc` |
| `science-pymoo-optimization` | `pymoo` |
| `science-rowan-chemistry` | `rowan` |
| `ml-stable-baselines3` | `stable-baselines3` |
| `science-timesfm-forecasting` | `timesfm-forecasting` |

## Task 1: Focused RED Tests

**Files:**
- Create: `tests/runtime_neutral/test_zero_route_authority_third_pass.py`

- [ ] **Step 1: Write focused tests**

Create `tests/runtime_neutral/test_zero_route_authority_third_pass.py` with this complete content:

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


TARGET_DIRECT_OWNERS = {
    "docs-markitdown-conversion": "markitdown",
    "ip-uspto-patents": "uspto-database",
    "science-astropy": "astropy",
    "science-pymatgen": "pymatgen",
    "science-simpy-simulation": "simpy",
    "science-fluidsim-cfd": "fluidsim",
    "science-matchms-spectra": "matchms",
    "science-matlab-octave": "matlab",
    "science-neuropixels": "neuropixels-analysis",
    "science-pymc-bayesian": "pymc",
    "science-pymoo-optimization": "pymoo",
    "science-rowan-chemistry": "rowan",
    "ml-stable-baselines3": "stable-baselines3",
    "science-timesfm-forecasting": "timesfm-forecasting",
}


PROMPT_CASES = [
    ("用 MarkItDown 将 PDF 和 DOCX 转换成 Markdown", "docs-markitdown-conversion", "markitdown", "coding"),
    ("查询 USPTO patent 专利全文和权利要求", "ip-uspto-patents", "uspto-database", "research"),
    ("用 Astropy 读取 FITS 天文数据并处理 WCS 坐标", "science-astropy", "astropy", "coding"),
    ("用 pymatgen 解析 CIF 晶体结构并计算材料特征", "science-pymatgen", "pymatgen", "coding"),
    ("用 SimPy 做离散事件仿真排队系统和 resource process", "science-simpy-simulation", "simpy", "coding"),
    ("用 FluidSim 做 Navier-Stokes CFD 流体仿真并分析 turbulence spectra", "science-fluidsim-cfd", "fluidsim", "coding"),
    ("用 matchms 处理 MS/MS mass spectra 并计算 spectral similarity", "science-matchms-spectra", "matchms", "coding"),
    ("写 MATLAB/Octave 脚本做矩阵计算和 Simulink 数据处理", "science-matlab-octave", "matlab", "coding"),
    ("分析 Neuropixels spike sorting 和 SpikeGLX 电生理数据", "science-neuropixels", "neuropixels-analysis", "research"),
    ("用 PyMC 建立 Bayesian hierarchical model 并运行 NUTS MCMC", "science-pymc-bayesian", "pymc", "coding"),
    ("用 pymoo 做 NSGA-II 多目标优化和 Pareto front 分析", "science-pymoo-optimization", "pymoo", "coding"),
    ("用 Rowan 云端量子化学平台做 pKa prediction 和 conformer search", "science-rowan-chemistry", "rowan", "research"),
    ("用 Stable-Baselines3 训练 PPO 强化学习智能体", "ml-stable-baselines3", "stable-baselines3", "coding"),
    ("用 TimesFM 做 zero-shot time series forecasting 并输出 prediction intervals", "science-timesfm-forecasting", "timesfm-forecasting", "coding"),
]


def route(prompt: str, task_type: str = "coding", grade: str = "M") -> dict[str, object]:
    return route_prompt(prompt=prompt, grade=grade, task_type=task_type, repo_root=REPO_ROOT)


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
                str(row.get("candidate_selection_reason") or row.get("legacy_role") or ""),
            )
        )
    return rows


def load_manifest() -> dict[str, object]:
    return json.loads((REPO_ROOT / "config" / "pack-manifest.json").read_text(encoding="utf-8-sig"))


def load_pack(pack_id: str) -> dict[str, object]:
    manifest = load_manifest()
    return next(pack for pack in manifest["packs"] if pack["id"] == pack_id)


class ZeroRouteAuthorityThirdPassTests(unittest.TestCase):
    def assert_selected(
        self,
        prompt: str,
        expected_pack: str,
        expected_skill: str,
        *,
        task_type: str = "coding",
        grade: str = "M",
    ) -> None:
        result = route(prompt, task_type=task_type, grade=grade)
        self.assertEqual((expected_pack, expected_skill), selected(result), ranked_summary(result))

    def test_manifest_makes_all_third_pass_packs_direct_owners(self) -> None:
        for pack_id, skill_id in TARGET_DIRECT_OWNERS.items():
            with self.subTest(pack_id=pack_id):
                pack = load_pack(pack_id)
                self.assertEqual([skill_id], pack["skill_candidates"])
                self.assertEqual([skill_id], pack["route_authority_candidates"])
                self.assertEqual([], pack["stage_assistant_candidates"])
                self.assertEqual(skill_id, pack["defaults_by_task"]["planning"])
                self.assertEqual(skill_id, pack["defaults_by_task"]["coding"])
                self.assertEqual(skill_id, pack["defaults_by_task"]["research"])

    def test_manifest_has_no_remaining_zero_route_authority_packs(self) -> None:
        manifest = load_manifest()
        zero_route = [
            pack["id"]
            for pack in manifest["packs"]
            if pack.get("skill_candidates") and not pack.get("route_authority_candidates")
        ]
        self.assertEqual([], zero_route)

    def test_third_pass_prompts_route_to_direct_owners(self) -> None:
        for prompt, expected_pack, expected_skill, task_type in PROMPT_CASES:
            with self.subTest(prompt=prompt):
                self.assert_selected(prompt, expected_pack, expected_skill, task_type=task_type)

    def test_third_pass_false_positive_boundaries(self) -> None:
        false_positive_cases = [
            ("用 NumPy 编写 Python matrix multiplication，不使用 MATLAB 或 Octave", ("science-matlab-octave", "matlab")),
            ("用 scikit-learn 训练随机森林分类模型，不是 reinforcement learning", ("ml-stable-baselines3", "stable-baselines3")),
            ("用 scikit-learn 做普通 tabular regression，不是 time series forecasting", ("science-timesfm-forecasting", "timesfm-forecasting")),
            ("检索 PubMed 文献并画论文 figures，不处理 mass spectra", ("science-matchms-spectra", "matchms")),
            ("用 scipy Rotation 做 quaternion transformation，不调用 Rowan 云端化学平台", ("science-rowan-chemistry", "rowan")),
        ]
        for prompt, forbidden in false_positive_cases:
            with self.subTest(prompt=prompt):
                result = route(prompt)
                self.assertNotEqual(forbidden, selected(result), ranked_summary(result))

    def test_no_third_pass_skill_directory_was_deleted(self) -> None:
        for skill_id in TARGET_DIRECT_OWNERS.values():
            with self.subTest(skill_id=skill_id):
                self.assertTrue((REPO_ROOT / "bundled" / "skills" / skill_id / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_third_pass.py -q
```

Expected: FAIL. Expected failure classes:

```text
KeyError: 'route_authority_candidates'
or assertion failure because zero_route contains the 14 remaining packs
```

Do not commit after this step; the test suite is intentionally failing.

## Task 2: Confirm No Third-Pass Skill Should Be Deleted

**Files:**
- Read: `bundled/skills/fluidsim/**`
- Read: `bundled/skills/rowan/**`

- [ ] **Step 1: Inspect the two previously uncertain directories**

Run:

```powershell
Get-ChildItem -LiteralPath 'bundled\skills\fluidsim' -Recurse -File |
  Select-Object FullName,Length
Get-ChildItem -LiteralPath 'bundled\skills\rowan' -Recurse -File |
  Select-Object FullName,Length
```

Expected findings:

```text
bundled/skills/fluidsim has SKILL.md and 6 reference files.
bundled/skills/rowan has SKILL.md and 6 reference files.
```

- [ ] **Step 2: Read both skill headers**

Run:

```powershell
Get-Content -LiteralPath 'bundled\skills\fluidsim\SKILL.md' -TotalCount 80
Get-Content -LiteralPath 'bundled\skills\rowan\SKILL.md' -TotalCount 80
```

Expected findings:

```text
fluidsim owns CFD simulation tasks: Navier-Stokes, shallow water, turbulence, pseudospectral/FFT workflows.
rowan owns Rowan cloud quantum-chemistry tasks: pKa, conformer search, geometry optimization, docking, AI cofolding.
```

- [ ] **Step 3: Record the implementation decision**

Use this decision in the config and governance tasks:

```text
Keep fluidsim as science-fluidsim-cfd direct route owner.
Keep rowan as science-rowan-chemistry direct route owner.
Do not delete third-pass skill directories.
```

No commit is needed for this read-only task.

## Task 3: Routing Config Implementation

**Files:**
- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`
- Test: `tests/runtime_neutral/test_zero_route_authority_third_pass.py`

- [ ] **Step 1: Update the pack manifest**

Modify `config/pack-manifest.json` for each target pack so:

```json
"route_authority_candidates": ["<skill_id>"],
"stage_assistant_candidates": [],
"defaults_by_task": {
  "planning": "<skill_id>",
  "coding": "<skill_id>",
  "research": "<skill_id>"
}
```

Use these exact pack-to-skill mappings:

```json
{
  "docs-markitdown-conversion": "markitdown",
  "ip-uspto-patents": "uspto-database",
  "science-astropy": "astropy",
  "science-pymatgen": "pymatgen",
  "science-simpy-simulation": "simpy",
  "science-fluidsim-cfd": "fluidsim",
  "science-matchms-spectra": "matchms",
  "science-matlab-octave": "matlab",
  "science-neuropixels": "neuropixels-analysis",
  "science-pymc-bayesian": "pymc",
  "science-pymoo-optimization": "pymoo",
  "science-rowan-chemistry": "rowan",
  "ml-stable-baselines3": "stable-baselines3",
  "science-timesfm-forecasting": "timesfm-forecasting"
}
```

Also ensure each target pack has natural-language trigger keywords for its owner. These minimum trigger phrases must be present in the pack's `trigger_keywords`:

```json
{
  "docs-markitdown-conversion": ["markitdown", "convert to markdown", "pdf to markdown", "docx to markdown", "转成 markdown"],
  "ip-uspto-patents": ["uspto", "patent", "claims", "patent metadata", "专利检索"],
  "science-astropy": ["astropy", "fits", "wcs", "astronomy", "天文数据"],
  "science-pymatgen": ["pymatgen", "cif", "crystal structure", "materials", "晶体结构"],
  "science-simpy-simulation": ["simpy", "discrete event simulation", "queue simulation", "resource process", "离散事件仿真"],
  "science-fluidsim-cfd": ["fluidsim", "cfd", "navier-stokes", "turbulence", "流体仿真"],
  "science-matchms-spectra": ["matchms", "mass spectra", "ms/ms", "spectral similarity", "质谱"],
  "science-matlab-octave": ["matlab", "octave", ".m script", "simulink", "矩阵计算"],
  "science-neuropixels": ["neuropixels", "spike sorting", "spikeglx", "electrophysiology", "神经电生理"],
  "science-pymc-bayesian": ["pymc", "bayesian", "mcmc", "nuts", "贝叶斯"],
  "science-pymoo-optimization": ["pymoo", "multi-objective", "nsga-ii", "pareto", "多目标优化"],
  "science-rowan-chemistry": ["rowan", "rowan chemistry", "pka prediction", "conformer search", "量子化学"],
  "ml-stable-baselines3": ["stable-baselines3", "sb3", "ppo", "sac", "dqn", "reinforcement learning", "强化学习"],
  "science-timesfm-forecasting": ["timesfm", "time series forecasting", "zero-shot forecasting", "prediction intervals", "时间序列预测"]
}
```

Preserve unrelated pack fields such as `id`, `priority`, `grade_allow`, and `task_allow`.

- [ ] **Step 2: Update the keyword index**

In `config/skill-keyword-index.json`, use or extend these exact keyword lists:

```json
{
  "markitdown": ["markitdown", "convert to markdown", "pdf to markdown", "docx to markdown", "pptx to markdown", "office to markdown", "document conversion", "转成 markdown", "转成markdown", "markdown转换"],
  "uspto-database": ["uspto", "patent", "patents", "patent claims", "patent metadata", "patent search", "专利", "专利检索", "权利要求", "发明专利"],
  "astropy": ["astropy", "fits", "fits file", "wcs", "astronomy", "celestial coordinates", "astropy units", "天文数据", "天文坐标"],
  "pymatgen": ["pymatgen", "cif", "crystal structure", "materials project", "composition", "structure analysis", "材料计算", "晶体结构", "材料结构"],
  "simpy": ["simpy", "discrete event simulation", "event simulation", "queue simulation", "resource process", "process simulation", "离散事件仿真", "排队仿真"],
  "fluidsim": ["fluidsim", "cfd", "navier-stokes", "fluid simulation", "turbulence", "shallow water", "stratified flow", "pseudospectral", "流体仿真", "湍流"],
  "matchms": ["matchms", "mass spectra", "mass spectrum", "ms/ms", "msms", "spectral similarity", "spectrum processing", "质谱", "谱图匹配"],
  "matlab": ["matlab", "octave", ".m script", "m-file", "simulink", "matrix calculation", "matlab script", "矩阵计算", "matlab脚本"],
  "neuropixels-analysis": ["neuropixels", "kilosort", "spike sorting", "spikeglx", "open ephys", "ibl", "electrophysiology", "神经电生理", "峰电位排序"],
  "pymc": ["pymc", "bayesian", "mcmc", "nuts", "posterior", "hierarchical model", "bayesian model", "贝叶斯", "后验"],
  "pymoo": ["pymoo", "multi-objective", "multi objective optimization", "nsga-ii", "nsga", "pareto", "constraint optimization", "多目标优化", "帕累托"],
  "rowan": ["rowan", "rowan chemistry", "rowan-python", "labs.rowansci.com", "pka prediction", "conformer search", "geometry optimization", "quantum chemistry", "docking", "boltz", "chai-1", "量子化学"],
  "stable-baselines3": ["stable-baselines3", "stable baselines3", "sb3", "ppo", "sac", "dqn", "reinforcement learning", "rl agent", "强化学习", "智能体训练"],
  "timesfm-forecasting": ["timesfm", "time series forecasting", "zero-shot forecasting", "prediction intervals", "foundation model forecasting", "forecast horizon", "时间序列预测", "零样本预测"]
}
```

Do not add new top-level skill IDs beyond these existing skills.

- [ ] **Step 3: Update routing rules**

In `config/skill-routing-rules.json`, ensure each retained skill has one rule object. Use these exact rule bodies.

```json
"markitdown": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["markitdown", "convert to markdown", "pdf to markdown", "docx to markdown", "pptx to markdown", "office to markdown", "document conversion", "转成 markdown", "转成markdown", "markdown转换"],
  "negative_keywords": ["write markdown article", "markdown README", "markdown table formatting", "not conversion"],
  "equivalent_group": "document-conversion",
  "canonical_for_task": ["coding", "research"]
}
```

```json
"uspto-database": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["uspto", "patent", "patents", "patent claims", "patent metadata", "patent search", "专利", "专利检索", "权利要求", "发明专利"],
  "negative_keywords": ["pubmed", "clinical trial", "trademark", "copyright", "论文检索"],
  "equivalent_group": "ip-patent-data",
  "canonical_for_task": ["research"]
}
```

```json
"astropy": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["astropy", "fits", "fits file", "wcs", "astronomy", "celestial coordinates", "astropy units", "天文数据", "天文坐标"],
  "negative_keywords": ["astrology", "horoscope", "pymatgen", "crystal structure", "materials project", "占星"],
  "equivalent_group": "astronomy-data",
  "canonical_for_task": ["coding", "research"]
}
```

```json
"pymatgen": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["pymatgen", "cif", "crystal structure", "materials project", "composition", "structure analysis", "材料计算", "晶体结构", "材料结构"],
  "negative_keywords": ["astropy", "fits", "wcs", "astronomy", "bioinformatics"],
  "equivalent_group": "materials-science",
  "canonical_for_task": ["coding", "research"]
}
```

```json
"simpy": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["simpy", "discrete event simulation", "event simulation", "queue simulation", "resource process", "process simulation", "离散事件仿真", "排队仿真"],
  "negative_keywords": ["sympy", "symbolic math", "matplotlib animation", "agent-based model"],
  "equivalent_group": "simulation",
  "canonical_for_task": ["coding"]
}
```

```json
"fluidsim": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["fluidsim", "cfd", "navier-stokes", "fluid simulation", "turbulence", "shallow water", "stratified flow", "pseudospectral", "流体仿真", "湍流"],
  "negative_keywords": ["css", "fluid layout", "responsive design", "fluid typography", "液态布局"],
  "equivalent_group": "cfd-simulation",
  "canonical_for_task": ["coding", "research"]
}
```

```json
"matchms": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["matchms", "mass spectra", "mass spectrum", "ms/ms", "msms", "spectral similarity", "spectrum processing", "质谱", "谱图匹配"],
  "negative_keywords": ["pubmed", "literature review", "plotting", "matplotlib", "not mass spectra", "不处理 mass spectra"],
  "equivalent_group": "mass-spectra",
  "canonical_for_task": ["coding", "research"]
}
```

```json
"matlab": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["matlab", "octave", ".m script", "m-file", "simulink", "matrix calculation", "matlab script", "矩阵计算", "matlab脚本"],
  "negative_keywords": ["not matlab", "not octave", "不使用 matlab", "不使用 MATLAB", "python matrix multiplication", "numpy matrix multiplication", "numpy array"],
  "equivalent_group": "matlab-octave",
  "canonical_for_task": ["coding"]
}
```

```json
"neuropixels-analysis": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["neuropixels", "kilosort", "spike sorting", "spikeglx", "open ephys", "ibl", "electrophysiology", "神经电生理", "峰电位排序"],
  "negative_keywords": ["single-cell rna", "flow cytometry", "clinical eeg", "fMRI"],
  "equivalent_group": "neuro-electrophysiology",
  "canonical_for_task": ["research", "coding"]
}
```

```json
"pymc": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["pymc", "bayesian", "mcmc", "nuts", "posterior", "hierarchical model", "bayesian model", "贝叶斯", "后验"],
  "negative_keywords": ["pymatgen", "crystal structure", "materials project", "pymoo", "nsga"],
  "equivalent_group": "bayesian-modeling",
  "canonical_for_task": ["coding", "research"]
}
```

```json
"pymoo": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["pymoo", "multi-objective", "multi objective optimization", "nsga-ii", "nsga", "pareto", "constraint optimization", "多目标优化", "帕累托"],
  "negative_keywords": ["pymc", "bayesian", "mcmc", "posterior"],
  "equivalent_group": "optimization",
  "canonical_for_task": ["coding", "research"]
}
```

```json
"rowan": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["rowan", "rowan chemistry", "rowan-python", "labs.rowansci.com", "pka prediction", "conformer search", "geometry optimization", "quantum chemistry", "docking", "boltz", "chai-1", "量子化学"],
  "negative_keywords": ["quaternion", "scipy rotation", "rotation matrix", "rowan tree", "not rowan", "不调用 rowan"],
  "equivalent_group": "cloud-quantum-chemistry",
  "canonical_for_task": ["research", "coding"]
}
```

```json
"stable-baselines3": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["stable-baselines3", "stable baselines3", "sb3", "ppo", "sac", "dqn", "reinforcement learning", "rl agent", "强化学习", "智能体训练"],
  "negative_keywords": ["scikit-learn", "sklearn", "random forest", "supervised learning", "ordinary supervised", "不是 reinforcement learning", "not reinforcement learning"],
  "equivalent_group": "reinforcement-learning",
  "canonical_for_task": ["coding", "research"]
}
```

```json
"timesfm-forecasting": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["timesfm", "time series forecasting", "zero-shot forecasting", "prediction intervals", "foundation model forecasting", "forecast horizon", "时间序列预测", "零样本预测"],
  "negative_keywords": ["scikit-learn", "ordinary regression", "tabular regression", "not time series", "不是 time series forecasting"],
  "equivalent_group": "time-series-forecasting",
  "canonical_for_task": ["coding", "research"]
}
```

- [ ] **Step 4: Run focused tests and verify GREEN**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_third_pass.py -q
```

Expected:

```text
5 passed
```

If route ranking exposes a narrow false positive, inspect the ranked output before changing rules. Change only the relevant positive/negative keyword boundary and rerun this command.

- [ ] **Step 5: Commit focused tests and routing config**

Run:

```powershell
git status --short
git add tests/runtime_neutral/test_zero_route_authority_third_pass.py `
  config/pack-manifest.json `
  config/skill-keyword-index.json `
  config/skill-routing-rules.json
git commit -m "fix: complete zero route authority single skill packs"
```

Expected: one commit containing the focused test and route/config changes.

## Task 4: Governance Record

**Files:**
- Create: `docs/governance/zero-route-authority-third-pass-2026-04-30.md`

- [ ] **Step 1: Write governance note**

Create `docs/governance/zero-route-authority-third-pass-2026-04-30.md` with this complete content:

```markdown
# Zero Route Authority Third Pass

Date: 2026-04-30

## Scope

This pass completes the remaining single-skill zero-route-authority cleanup.

| Metric | Before | After |
| --- | ---: | ---: |
| zero-route-authority packs | 14 | 0 |
| non-empty `stage_assistant_candidates` | 0 | 0 |
| physically deleted skill directories | 0 | 0 |

Out of scope:

- six-stage Vibe runtime changes
- specialist consultation policy changes
- dense-pack false-positive audits
- route selection claims about actual material skill use

## Direct Owners

| Pack | Direct route owner | Boundary |
| --- | --- | --- |
| `docs-markitdown-conversion` | `markitdown` | MarkItDown document-to-Markdown conversion. |
| `ip-uspto-patents` | `uspto-database` | USPTO patent search, claims, text, and metadata. |
| `science-astropy` | `astropy` | Astronomy data, FITS, WCS, units, and Astropy workflows. |
| `science-pymatgen` | `pymatgen` | Materials structures, CIF, crystal structures, and pymatgen workflows. |
| `science-simpy-simulation` | `simpy` | Discrete-event simulation, queues, resources, and SimPy process models. |
| `science-fluidsim-cfd` | `fluidsim` | Computational fluid dynamics, Navier-Stokes, turbulence, and FluidSim workflows. |
| `science-matchms-spectra` | `matchms` | Mass spectra processing and spectral similarity with matchms. |
| `science-matlab-octave` | `matlab` | MATLAB/Octave scripts, Simulink, and matrix workflows. |
| `science-neuropixels` | `neuropixels-analysis` | Neuropixels electrophysiology, spike sorting, SpikeGLX, and Open Ephys workflows. |
| `science-pymc-bayesian` | `pymc` | Bayesian models, MCMC/NUTS, posterior analysis, and PyMC workflows. |
| `science-pymoo-optimization` | `pymoo` | Multi-objective and constrained optimization with pymoo. |
| `science-rowan-chemistry` | `rowan` | Rowan cloud quantum-chemistry workflows: pKa, conformer search, geometry optimization, docking, and cofolding. |
| `ml-stable-baselines3` | `stable-baselines3` | Stable-Baselines3 reinforcement-learning agents and PPO/SAC/DQN workflows. |
| `science-timesfm-forecasting` | `timesfm-forecasting` | TimesFM and foundation-model time-series forecasting. |

## Deletion Decision

No skill directories were physically deleted in this pass.

`fluidsim` was retained because the directory contains a full CFD skill and references for simulation setup, solvers, parameters, output analysis, and advanced features.

`rowan` was retained because the directory contains a full Rowan cloud quantum-chemistry skill with references for API usage, molecule handling, workflow types, RDKit/native workflows, and result interpretation.

## Route Protection

Focused tests protect:

- all 14 retained packs having direct route owners
- all 14 retained packs having empty `stage_assistant_candidates`
- prompt-level routing for each retained owner
- false-positive boundaries for MATLAB, Stable-Baselines3, TimesFM, matchms, and Rowan
- no remaining zero-route-authority packs

## Remaining Work

No zero-route-authority packs remain after this pass.

Remaining route architecture work is outside this pass:

- runtime/presentation compatibility terms such as `primary_skill`, `accept_primary`, `stage_assistant_candidates`, and `consultation_bucket`
- dense-pack false-positive audits for packs such as `bio-science`, `docs-media`, `data-ml`, `science-chem-drug`, and `scholarly-publishing-workflow`

## Verification

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_third_pass.py -q
python -m pytest tests/runtime_neutral/test_zero_route_authority_second_pass.py tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py -q
.\scripts\verify\vibe-pack-routing-smoke.ps1
.\scripts\verify\vibe-offline-skills-gate.ps1
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
```

Record the final pass/fail results in the completion report.
```

- [ ] **Step 2: Commit governance note**

Run:

```powershell
git add docs/governance/zero-route-authority-third-pass-2026-04-30.md
git commit -m "docs: record zero route authority third pass"
```

Expected: one docs commit.

## Task 5: Refresh Skills Lock

**Files:**
- Modify: `config/skills-lock.json`

- [ ] **Step 1: Regenerate skills lock**

Run:

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected output contains:

```text
skills-lock generated:
```

- [ ] **Step 2: Confirm retained skills remain in lock**

Run:

```powershell
rg -n "fluidsim|rowan|timesfm-forecasting|stable-baselines3|markitdown" config\skills-lock.json
```

Expected:

```text
all five searched retained skills appear in config/skills-lock.json
```

- [ ] **Step 3: Run focused tests again**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_third_pass.py -q
```

Expected:

```text
5 passed
```

- [ ] **Step 4: Commit lock refresh**

Run:

```powershell
git status --short
git add config/skills-lock.json
git commit -m "chore: refresh skills lock after zero route third pass"
```

Expected: one lockfile commit. If `config/skills-lock.json` has no changes, report that the lockfile was already current and do not create an empty commit.

## Task 6: Broader Verification

**Files:**
- Read-only verification of repository gates

- [ ] **Step 1: Run focused and prior zero-route regression tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_third_pass.py tests/runtime_neutral/test_zero_route_authority_second_pass.py tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py -q
```

Expected:

```text
all tests pass
```

- [ ] **Step 2: Run routing smoke gate**

Run:

```powershell
.\scripts\verify\vibe-pack-routing-smoke.ps1
```

Expected summary:

```text
Failed: 0
Pack routing smoke checks passed.
```

- [ ] **Step 3: Run offline skills gate**

Run:

```powershell
.\scripts\verify\vibe-offline-skills-gate.ps1
```

Expected:

```text
[PASS] offline skill closure gate passed.
```

- [ ] **Step 4: Run config parity gate**

Run:

```powershell
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
```

Expected:

```text
Gate Result: PASS
```

- [ ] **Step 5: Run version packaging gate**

Run:

```powershell
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
```

Expected:

```text
Gate Result: PASS
```

- [ ] **Step 6: Confirm zero-route count is zero**

Run:

```powershell
@'
import json
from pathlib import Path
manifest = json.loads(Path("config/pack-manifest.json").read_text(encoding="utf-8-sig"))
zero = [
    pack["id"]
    for pack in manifest["packs"]
    if pack.get("skill_candidates") and not pack.get("route_authority_candidates")
]
print("ZERO_ROUTE_COUNT", len(zero))
for pack_id in zero:
    print(pack_id)
'@ | python -
```

Expected:

```text
ZERO_ROUTE_COUNT 0
```

- [ ] **Step 7: Capture final status**

Run:

```powershell
git status --short --branch
git log --oneline -8
```

Expected:

```text
working tree clean
latest commits include routing fix, governance note, and optional skills-lock refresh
```

## Task 7: Completion Report

**Files:**
- No file changes

- [ ] **Step 1: Report completion with evidence**

The completion report must include:

```text
branch
commit hashes
before/after zero-route-authority count: 14 -> 0
explicit statement that no third-pass skill directories were deleted
focused test result
broader gate results
remaining route work outside this pass
explicit caveat that runtime consultation/primary/stage-assistant compatibility terminology was not changed
```

Do not claim dense-pack cleanup is complete. The likely next route-cleanup categories are:

```text
runtime/presentation compatibility terminology cleanup
dense-pack false-positive audits
```
