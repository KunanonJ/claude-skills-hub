# Zero Route Authority Second Pass Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean the second batch of zero-route-authority packs by fixing `cloud-modalcom`, consolidating `ml-torch-geometric`, and making `science-quantum` direct-owner routing explicit.

**Architecture:** This is a routing-contract cleanup. The live contract is expressed in `config/pack-manifest.json`, `config/skill-keyword-index.json`, `config/skill-routing-rules.json`, bundled skill directories, and `config/skills-lock.json`; tests call `vgo_runtime.router_contract_runtime.route_prompt()` to prove prompt-level behavior.

**Tech Stack:** Python `unittest`/`pytest`, JSON routing config, PowerShell verification scripts, Vibe-Skills bundled `SKILL.md` directories.

---

## File Map

- Create `tests/runtime_neutral/test_zero_route_authority_second_pass.py`: focused RED/GREEN regression tests for the three selected packs.
- Modify `config/pack-manifest.json`: add direct route owners, keep `stage_assistant_candidates` empty, and consolidate `ml-torch-geometric` to one route owner.
- Modify `config/skill-keyword-index.json`: add Modal Chinese cloud execution phrases, PyG canonical keywords, and quantum boundary keywords.
- Modify `config/skill-routing-rules.json`: add or narrow positive/negative route rules for Modal, Vercel, PyG, generic PyTorch, and quantum ecosystem boundaries.
- Modify `bundled/skills/torch-geometric/SKILL.md`: only if useful alias guidance from `torch_geometric` must be preserved after deletion.
- Delete `bundled/skills/torch_geometric/`: only after confirming it is a thin compatibility alias with no unique assets.
- Create `docs/governance/zero-route-authority-second-pass-2026-04-29.md`: governance record with before/after counts, retained owners, deletion rationale, probes, and remaining zero-authority packs.
- Modify `config/skills-lock.json`: regenerate after bundled skill/config changes are stable.

## Task 1: Focused RED Tests

**Files:**
- Create: `tests/runtime_neutral/test_zero_route_authority_second_pass.py`

- [ ] **Step 1: Write focused tests**

Create `tests/runtime_neutral/test_zero_route_authority_second_pass.py` with this complete content:

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "packages" / "runtime-core" / "src"))

from vgo_runtime.router_contract_runtime import route_prompt  # noqa: E402


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


def load_pack(pack_id: str) -> dict[str, object]:
    manifest = json.loads((REPO_ROOT / "config" / "pack-manifest.json").read_text(encoding="utf-8-sig"))
    return next(pack for pack in manifest["packs"] if pack["id"] == pack_id)


class ZeroRouteAuthoritySecondPassTests(unittest.TestCase):
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

    def test_cloud_modalcom_has_direct_owner(self) -> None:
        pack = load_pack("cloud-modalcom")
        self.assertEqual(["modal-labs"], pack["skill_candidates"])
        self.assertEqual(["modal-labs"], pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])

    def test_cloud_modalcom_routes_chinese_modal_deployment(self) -> None:
        self.assert_selected("用 Modal 部署 Python GPU 函数和云端作业", "cloud-modalcom", "modal-labs")
        self.assert_selected("把 FastAPI 部署到 Modal 而不是 Vercel", "cloud-modalcom", "modal-labs")
        self.assert_selected("用 modal.com 部署 Python GPU function", "cloud-modalcom", "modal-labs")
        self.assert_selected("使用 Modal Labs 运行 serverless GPU batch job", "cloud-modalcom", "modal-labs")

    def test_cloud_modalcom_does_not_capture_frontend_modal_dialogs(self) -> None:
        result = route("修复 React modal dialog 弹窗和 overlay 样式", task_type="coding")
        self.assertNotEqual(("cloud-modalcom", "modal-labs"), selected(result), ranked_summary(result))

    def test_ml_torch_geometric_has_one_canonical_owner(self) -> None:
        pack = load_pack("ml-torch-geometric")
        self.assertEqual(["torch-geometric"], pack["skill_candidates"])
        self.assertEqual(["torch-geometric"], pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])
        self.assertEqual("torch-geometric", pack["defaults_by_task"]["planning"])
        self.assertEqual("torch-geometric", pack["defaults_by_task"]["coding"])
        self.assertEqual("torch-geometric", pack["defaults_by_task"]["research"])

    def test_ml_torch_geometric_routes_alias_keywords_to_canonical_skill(self) -> None:
        self.assert_selected("用 PyTorch Geometric 构建 GCN 图神经网络", "ml-torch-geometric", "torch-geometric")
        self.assert_selected("用 torch_geometric 写 GAT 节点分类模型", "ml-torch-geometric", "torch-geometric")
        self.assert_selected("训练 PyG graph classification pipeline", "ml-torch-geometric", "torch-geometric")

    def test_ml_torch_geometric_does_not_capture_generic_pytorch(self) -> None:
        result = route("用 PyTorch 训练 CNN 图像分类模型，不涉及 graph neural network 或 PyG", task_type="coding")
        self.assertNotEqual(("ml-torch-geometric", "torch-geometric"), selected(result), ranked_summary(result))

    def test_science_quantum_has_direct_owners(self) -> None:
        pack = load_pack("science-quantum")
        expected = ["qiskit", "cirq", "pennylane", "qutip"]
        self.assertEqual(expected, pack["skill_candidates"])
        self.assertEqual(expected, pack["route_authority_candidates"])
        self.assertEqual([], pack["stage_assistant_candidates"])
        self.assertEqual("qiskit", pack["defaults_by_task"]["planning"])
        self.assertEqual("qiskit", pack["defaults_by_task"]["coding"])
        self.assertEqual("qiskit", pack["defaults_by_task"]["research"])

    def test_science_quantum_routes_to_ecosystem_owners(self) -> None:
        self.assert_selected("用 Qiskit 构建量子电路并在 simulator 上运行", "science-quantum", "qiskit")
        self.assert_selected("用 Cirq 写 quantum gate circuit 和 moments", "science-quantum", "cirq")
        self.assert_selected("用 PennyLane 做 quantum machine learning 变分量子线路", "science-quantum", "pennylane")
        self.assert_selected("用 QuTiP 模拟开放量子系统 master equation", "science-quantum", "qutip")

    def test_selected_packs_do_not_reintroduce_stage_assistants(self) -> None:
        for pack_id in ("cloud-modalcom", "ml-torch-geometric", "science-quantum"):
            with self.subTest(pack_id=pack_id):
                self.assertEqual([], load_pack(pack_id)["stage_assistant_candidates"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_second_pass.py -q
```

Expected: FAIL. The expected failures are:

```text
KeyError: 'route_authority_candidates'
or assertion failure for cloud-modalcom selected integration-devops/vercel-deploy
or assertion failure because ml-torch-geometric still includes torch_geometric
```

Do not commit after this step; the suite is intentionally failing.

## Task 2: Inspect The PyG Duplicate Before Deletion

**Files:**
- Read: `bundled/skills/torch-geometric/**`
- Read: `bundled/skills/torch_geometric/**`
- Modify if needed: `bundled/skills/torch-geometric/SKILL.md`
- Delete if confirmed alias: `bundled/skills/torch_geometric/`

- [ ] **Step 1: Inspect both directories**

Run:

```powershell
Get-ChildItem -LiteralPath 'bundled\skills\torch-geometric' -Recurse -File |
  Select-Object FullName,Length
Get-ChildItem -LiteralPath 'bundled\skills\torch_geometric' -Recurse -File |
  Select-Object FullName,Length
```

Expected current finding:

```text
bundled/skills/torch-geometric has SKILL.md, references, and scripts.
bundled/skills/torch_geometric has only SKILL.md.
```

- [ ] **Step 2: Read the alias payload**

Run:

```powershell
Get-Content -LiteralPath 'bundled\skills\torch_geometric\SKILL.md' -TotalCount 160
```

Expected current finding:

```text
The file describes torch_geometric as a compatibility alias that delegates to ../torch-geometric.
It has no unique scripts, references, examples, or assets.
```

- [ ] **Step 3: Preserve useful alias wording in the canonical skill**

If the canonical `bundled/skills/torch-geometric/SKILL.md` does not already mention the underscore API spelling, add this short note near the top after the overview:

```markdown
## Naming Compatibility

Use `torch-geometric` as the canonical skill ID. Treat `torch_geometric`,
`PyG`, and `pytorch geometric` as API or keyword spellings that route to this
same skill, not as separate expert roles.
```

Run:

```powershell
rg -n "Naming Compatibility|torch_geometric|canonical skill ID" bundled\skills\torch-geometric\SKILL.md
```

Expected: the canonical skill now contains the compatibility note.

- [ ] **Step 4: Physically remove the alias directory**

Delete only the confirmed alias directory:

```powershell
Remove-Item -LiteralPath 'bundled\skills\torch_geometric' -Recurse
```

Run:

```powershell
Test-Path -LiteralPath 'bundled\skills\torch_geometric'
```

Expected:

```text
False
```

Do not delete `bundled/skills/torch-geometric`.

## Task 3: Routing Config Implementation

**Files:**
- Modify: `config/pack-manifest.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/skill-routing-rules.json`

- [ ] **Step 1: Update selected pack manifest entries**

Modify `config/pack-manifest.json` so the three selected packs match these exact contracts:

```json
{
  "id": "cloud-modalcom",
  "skill_candidates": ["modal-labs"],
  "route_authority_candidates": ["modal-labs"],
  "stage_assistant_candidates": [],
  "defaults_by_task": {
    "planning": "modal-labs",
    "coding": "modal-labs",
    "research": "modal-labs"
  }
}
```

```json
{
  "id": "ml-torch-geometric",
  "trigger_keywords": [
    "torch-geometric",
    "torch_geometric",
    "pyg",
    "pytorch geometric",
    "graph neural network",
    "gnn",
    "图神经网络"
  ],
  "skill_candidates": ["torch-geometric"],
  "route_authority_candidates": ["torch-geometric"],
  "stage_assistant_candidates": [],
  "defaults_by_task": {
    "planning": "torch-geometric",
    "coding": "torch-geometric",
    "research": "torch-geometric"
  }
}
```

```json
{
  "id": "science-quantum",
  "skill_candidates": ["qiskit", "cirq", "pennylane", "qutip"],
  "route_authority_candidates": ["qiskit", "cirq", "pennylane", "qutip"],
  "stage_assistant_candidates": [],
  "defaults_by_task": {
    "planning": "qiskit",
    "coding": "qiskit",
    "research": "qiskit"
  }
}
```

Preserve each pack's existing `id`, `priority`, `grade_allow`, `task_allow`, and unrelated `trigger_keywords` unless the snippet above explicitly expands them.

- [ ] **Step 2: Update keyword index**

In `config/skill-keyword-index.json`, use these exact keyword lists for the selected skills:

```json
"modal-labs": {
  "keywords": [
    "modal.com",
    "modal labs",
    "modallabs",
    "modal run",
    "modal deploy",
    "modal serve",
    "modal 部署",
    "serverless gpu",
    "gpu function",
    "python gpu function",
    "batch job",
    "autoscaling containers",
    "云端运行",
    "云端作业",
    "云端 gpu",
    "gpu 容器",
    "gpu 函数"
  ]
}
```

```json
"torch-geometric": {
  "keywords": [
    "torch-geometric",
    "torch_geometric",
    "pyg",
    "pytorch geometric",
    "graph neural network",
    "gnn",
    "gcn",
    "gat",
    "graph classification",
    "node classification",
    "link prediction",
    "图神经网络",
    "图分类",
    "节点分类"
  ]
}
```

Remove the top-level `torch_geometric` keyword-index entry after the alias directory is removed.

For quantum owners, keep existing keywords and ensure these minimum terms are present:

```json
"qiskit": ["qiskit", "quantum circuit", "ibm quantum", "quantum gates", "transpilation", "量子电路", "量子计算"]
"cirq": ["cirq", "google quantum", "quantum gate", "quantum circuit", "moments", "量子电路"]
"pennylane": ["pennylane", "qml", "quantum machine learning", "variational quantum circuit", "differentiable quantum", "量子机器学习", "变分量子线路", "量子ML"]
"qutip": ["qutip", "quantum dynamics", "open quantum system", "master equation", "density matrix", "量子动力学", "开放量子系统", "主方程"]
```

- [ ] **Step 3: Update routing rules**

In `config/skill-routing-rules.json`, set or add these exact rules.

For `modal-labs`:

```json
"modal-labs": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": [
    "modal.com",
    "modal labs",
    "modallabs",
    "modal run",
    "modal deploy",
    "modal serve",
    "modal 部署",
    "serverless gpu",
    "gpu function",
    "python gpu function",
    "batch job",
    "autoscaling",
    "云端运行",
    "云端作业",
    "云端 gpu",
    "gpu 容器",
    "gpu 函数"
  ],
  "negative_keywords": [
    "react",
    "vue",
    "antd",
    "bootstrap",
    "dialog",
    "modal dialog",
    "弹窗",
    "对话框",
    "前端"
  ],
  "equivalent_group": "cloud-execution",
  "canonical_for_task": ["coding"]
}
```

For `vercel-deploy`, keep existing positives and add Modal negatives:

```json
"negative_keywords": [
  "mcp server",
  "modal.com",
  "modal labs",
  "modallabs",
  "modal deploy",
  "modal 部署",
  "不是 vercel",
  "not vercel"
]
```

For `torch-geometric`:

```json
"torch-geometric": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": [
    "torch-geometric",
    "torch_geometric",
    "pyg",
    "pytorch geometric",
    "graph neural network",
    "gnn",
    "gcn",
    "gat",
    "graph classification",
    "node classification",
    "link prediction",
    "图神经网络",
    "图分类",
    "节点分类"
  ],
  "negative_keywords": [
    "cnn",
    "resnet",
    "image classification",
    "图像分类",
    "computer vision",
    "vision transformer"
  ],
  "equivalent_group": "graph-ml",
  "canonical_for_task": ["coding", "research"]
}
```

Remove any top-level `torch_geometric` routing-rule entry if it exists.

For quantum owners, keep the existing `equivalent_group: "quantum"` and use these positives/negatives:

```json
"qiskit": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["qiskit", "ibm quantum", "quantum circuit", "quantum gates", "transpilation", "量子电路", "量子计算"],
  "negative_keywords": ["pubmed", "pmid", "cirq", "pennylane", "qutip", "quantum machine learning", "open quantum system", "master equation"],
  "equivalent_group": "quantum",
  "canonical_for_task": ["coding", "research"]
}
```

```json
"cirq": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["cirq", "google quantum", "quantum gate", "quantum circuit", "moments", "量子电路"],
  "negative_keywords": ["pubmed", "pmid", "qiskit", "pennylane", "qutip"],
  "equivalent_group": "quantum",
  "canonical_for_task": []
}
```

```json
"pennylane": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["pennylane", "qml", "quantum machine learning", "variational quantum circuit", "differentiable quantum", "量子机器学习", "变分量子线路", "量子ML"],
  "negative_keywords": ["pubmed", "pmid", "qiskit", "cirq", "qutip", "open quantum system", "master equation"],
  "equivalent_group": "quantum",
  "canonical_for_task": []
}
```

```json
"qutip": {
  "task_allow": ["planning", "coding", "research"],
  "positive_keywords": ["qutip", "quantum dynamics", "open quantum system", "master equation", "density matrix", "量子动力学", "开放量子系统", "主方程"],
  "negative_keywords": ["pubmed", "pmid", "qiskit", "cirq", "pennylane", "quantum machine learning"],
  "equivalent_group": "quantum",
  "canonical_for_task": ["research"]
}
```

- [ ] **Step 4: Run focused tests and verify GREEN**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_second_pass.py -q
```

Expected:

```text
9 passed
```

If the exact pass count changes because tests are split or combined, all tests in `test_zero_route_authority_second_pass.py` must pass.

- [ ] **Step 5: Commit routing config and focused tests**

Run:

```powershell
git status --short
git add tests/runtime_neutral/test_zero_route_authority_second_pass.py `
  config/pack-manifest.json `
  config/skill-keyword-index.json `
  config/skill-routing-rules.json `
  bundled/skills/torch-geometric/SKILL.md `
  bundled/skills/torch_geometric
git commit -m "fix: clean zero route authority second pass"
```

Expected: one commit containing the test, config changes, and PyG alias deletion or migration.

## Task 4: Governance Record

**Files:**
- Create: `docs/governance/zero-route-authority-second-pass-2026-04-29.md`

- [ ] **Step 1: Write governance note**

Create `docs/governance/zero-route-authority-second-pass-2026-04-29.md` with this complete content, updating only the final verification command outputs after running them:

```markdown
# Zero Route Authority Second Pass

Date: 2026-04-29

## Scope

This pass cleans three zero-route-authority packs:

| Pack | Before | After |
| --- | --- | --- |
| `cloud-modalcom` | 1 skill candidate, 0 route owners | 1 direct route owner, 0 stage assistants |
| `ml-torch-geometric` | 2 skill candidates, 0 route owners | 1 canonical direct route owner, 0 stage assistants |
| `science-quantum` | 4 skill candidates, 0 route owners | 4 direct route owners, 0 stage assistants |

Out of scope:

- six-stage Vibe runtime changes
- specialist consultation policy changes
- dense-pack audits
- route selection claims about actual material skill use

## Direct Owners

| Pack | Direct route owners | Boundary |
| --- | --- | --- |
| `cloud-modalcom` | `modal-labs` | Modal / modal.com / Modal Labs cloud execution, Python GPU functions, batch jobs, serverless GPU, autoscaling containers, and Modal deployment. |
| `ml-torch-geometric` | `torch-geometric` | PyTorch Geometric / PyG graph neural networks, including GCN, GAT, graph classification, node classification, and link prediction. |
| `science-quantum` | `qiskit`, `cirq`, `pennylane`, `qutip` | Qiskit default quantum circuits, Cirq ecosystem work, PennyLane quantum ML, and QuTiP open quantum systems. |

## Removed Or Consolidated

| Skill | Decision | Reason |
| --- | --- | --- |
| `torch_geometric` | Removed after alias review | It was a thin compatibility alias that delegated to `torch-geometric` and had no unique scripts, references, examples, or assets. The underscore spelling is retained as a keyword/API spelling for the canonical `torch-geometric` skill. |

## Route Protection

Focused tests protect:

- Chinese Modal deployment prompts routing to `cloud-modalcom/modal-labs`.
- Modal-not-Vercel prompts avoiding `integration-devops/vercel-deploy`.
- Frontend modal dialog prompts avoiding `cloud-modalcom/modal-labs`.
- `torch_geometric` API spelling routing to canonical `torch-geometric`.
- Generic PyTorch image/CNN prompts avoiding PyG.
- Qiskit, Cirq, PennyLane, and QuTiP ecosystem prompts selecting the intended quantum owner.

## Remaining Zero-Route-Authority Packs

The following packs remain intentionally deferred:

```text
docs-markitdown-conversion
ip-uspto-patents
science-astropy
science-pymatgen
science-simpy-simulation
science-fluidsim-cfd
science-matchms-spectra
science-matlab-octave
science-neuropixels
science-pymc-bayesian
science-pymoo-optimization
science-rowan-chemistry
ml-stable-baselines3
science-timesfm-forecasting
```

## Verification

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_second_pass.py -q
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
git add docs/governance/zero-route-authority-second-pass-2026-04-29.md
git commit -m "docs: record zero route authority second pass"
```

Expected: one docs commit.

## Task 5: Refresh Skills Lock And Verify Config Integrity

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

- [ ] **Step 2: Confirm deleted alias is gone from lock**

Run:

```powershell
rg -n "torch_geometric|torch-geometric|modal-labs" config\skills-lock.json
```

Expected:

```text
torch-geometric appears
modal-labs appears
torch_geometric does not appear
```

- [ ] **Step 3: Run focused tests again**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_second_pass.py -q
```

Expected:

```text
9 passed
```

- [ ] **Step 4: Commit lock refresh**

Run:

```powershell
git add config/skills-lock.json
git commit -m "chore: refresh skills lock after zero route second pass"
```

Expected: one lockfile commit.

## Task 6: Broader Verification

**Files:**
- Read-only verification of repository gates

- [ ] **Step 1: Run focused plus related regression tests**

Run:

```powershell
python -m pytest tests/runtime_neutral/test_zero_route_authority_second_pass.py tests/runtime_neutral/test_zero_route_authority_pack_consolidation.py -q
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

Expected:

```text
0 failed
```

- [ ] **Step 3: Run offline skills gate**

Run:

```powershell
.\scripts\verify\vibe-offline-skills-gate.ps1
```

Expected:

```text
PASS
```

- [ ] **Step 4: Run config parity gate**

Run:

```powershell
.\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
```

Expected:

```text
PASS
```

- [ ] **Step 5: Run version packaging gate**

Run:

```powershell
.\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
```

Expected:

```text
PASS
```

- [ ] **Step 6: Capture final status**

Run:

```powershell
git status --short --branch
git log --oneline -8
```

Expected:

```text
working tree clean
latest commits include routing fix, governance note, and skills-lock refresh
```

## Task 7: Completion Report

**Files:**
- No file changes

- [ ] **Step 1: Report completion with evidence**

The completion report must include:

```text
branch
commit hashes
before/after pack counts for cloud-modalcom, ml-torch-geometric, science-quantum
deleted directory: bundled/skills/torch_geometric, if deletion occurred
focused test result
broader gate results
remaining zero-route-authority packs
explicit caveat that runtime consultation/primary terminology was not changed in this pass
```

Do not claim all route cleanup is complete. This pass leaves these packs for later:

```text
docs-markitdown-conversion
ip-uspto-patents
science-astropy
science-pymatgen
science-simpy-simulation
science-fluidsim-cfd
science-matchms-spectra
science-matlab-octave
science-neuropixels
science-pymc-bayesian
science-pymoo-optimization
science-rowan-chemistry
ml-stable-baselines3
science-timesfm-forecasting
```
