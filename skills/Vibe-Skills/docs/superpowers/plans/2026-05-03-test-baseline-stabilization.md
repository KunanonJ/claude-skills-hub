# Test Baseline Stabilization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a conservative test-baseline audit surface that classifies the repository test suite into observable layers before anyone treats broad pytest sweeps as one pass/fail gate.

**Architecture:** Keep the behavior in the existing verification-core pattern: pure Python logic lives in `packages/verification-core/src/vgo_verify/test_baseline_audit.py`, and `scripts/verify/test-baseline-audit.py` is a thin repo-facing entrypoint. A JSON policy in `config/test-baseline-policy.json` owns layer names, pytest roots, risk keywords, and heavy-file patterns; focused runtime-neutral tests validate the runner without executing the full suite.

**Tech Stack:** Python 3 standard library, pytest, JSON policy files, existing `packages/verification-core` import bootstrap, PowerShell validation commands, generated evidence under `outputs/verify/`.

---

## File Structure

**Baseline policy**

- Create: `config/test-baseline-policy.json`
  - Owns layer definitions, pytest roots, timeout guidance, dependency hints, risk keywords, and conservative heavy/runtime/install classification patterns.
  - Keeps external network denied by default.

**Audit implementation**

- Create: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
  - Owns policy loading, pytest collect-output parsing, command construction, subprocess execution, risk scanning, layer classification, artifact rendering, and CLI behavior.
  - Exposes pure functions that tests can call with temp directories and fake subprocess runners.
- Create: `scripts/verify/test-baseline-audit.py`
  - Thin entrypoint matching the existing verify-wrapper pattern.
  - Adds `packages/verification-core/src` to `sys.path`, imports the core module, re-exports public functions, and calls `main()`.

**Runner tests**

- Create: `tests/runtime_neutral/test_test_baseline_audit.py`
  - Uses `importlib.util.spec_from_file_location()` to load the entrypoint or imports the core module after adding `packages/verification-core/src` to `sys.path`.
  - Uses temporary directories and fake subprocess runners for runner behavior.
  - Does not execute the whole repository suite.

**Generated evidence**

- Runtime output only: `outputs/verify/test-baseline-audit.json`
- Runtime output only: `outputs/verify/test-baseline-audit.md`
- These files are already covered by the repo-wide `outputs/` ignore rule and must not be committed.

**Do Not Modify**

- Do not change routing, runtime, installer, host adapter, or skill-selection behavior.
- Do not write to the local Codex root.
- Do not add network access to local tests.
- Do not change `pytest.ini`.
- Do not add broad skip markers to existing tests.
- Do not commit generated `outputs/verify` files.

---

## Current Baseline

Spec committed before this plan:

```text
c6c2d662 docs: design test baseline stabilization
```

Fresh worktree state before this plan:

```text
## main...origin/main [ahead 43]
```

Known collection evidence from the spec:

```text
tests/runtime_neutral --collect-only: 923 tests collected
tests/integration --collect-only: 190 tests collected
```

Existing focused guardrails that must remain available after implementation:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
```

Existing test infrastructure:

```text
pytest.ini testpaths = tests
tests/conftest.py sets PYTHONDONTWRITEBYTECODE=1 and PYTHONPYCACHEPREFIX=.tmp/pycache
```

---

### Task 1: Add Policy Contract And Loader

**Files:**

- Create: `config/test-baseline-policy.json`
- Create: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
- Create: `tests/runtime_neutral/test_test_baseline_audit.py`

- [ ] **Step 1: Write the failing policy tests**

Create `tests/runtime_neutral/test_test_baseline_audit.py` with this initial content:

```python
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CORE_SRC = REPO_ROOT / "packages" / "verification-core" / "src"
if str(CORE_SRC) not in sys.path:
    sys.path.insert(0, str(CORE_SRC))

from vgo_verify import test_baseline_audit as audit


class TestBaselineAuditPolicyTests(unittest.TestCase):
    def test_policy_file_has_expected_layers_and_network_default(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")

        self.assertEqual(1, policy["version"])
        self.assertFalse(policy["defaults"]["external_network_allowed"])
        self.assertEqual(
            ["contract_unit", "runtime_neutral_fast", "runtime_neutral_heavy", "integration_host_boundary"],
            [layer["id"] for layer in policy["layers"]],
        )
        self.assertEqual(["tests/contract", "tests/unit"], policy["layers"][0]["pytest_args"])

    def test_policy_load_rejects_duplicate_layer_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "policy.json"
            path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "defaults": {"external_network_allowed": False},
                        "layers": [
                            {"id": "contract_unit", "pytest_args": ["tests/unit"]},
                            {"id": "contract_unit", "pytest_args": ["tests/contract"]},
                        ],
                        "classification": {"heavy_file_patterns": [], "host_boundary_file_patterns": []},
                        "risk_keywords": [],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(audit.PolicyError, "Duplicate layer id"):
                audit.load_policy(path)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the red policy tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected: FAIL because `vgo_verify.test_baseline_audit` or `config/test-baseline-policy.json` does not exist yet.

- [ ] **Step 3: Create the baseline policy file**

Create `config/test-baseline-policy.json` with this content:

```json
{
  "version": 1,
  "updated_at": "2026-05-03",
  "defaults": {
    "external_network_allowed": false,
    "disable_network_env": "VIBESKILLS_TEST_DISABLE_NETWORK",
    "pytest_quiet_arg": "-q",
    "collect_timeout_seconds": 180
  },
  "layers": [
    {
      "id": "contract_unit",
      "description": "Fast deterministic contract and unit checks.",
      "pytest_args": ["tests/contract", "tests/unit"],
      "timeout_seconds": 180,
      "dependencies": ["python", "pytest"],
      "external_network_allowed": false
    },
    {
      "id": "runtime_neutral_fast",
      "description": "Runtime-neutral tests that are not classified as heavy, host-boundary, or external-risk.",
      "pytest_args": ["tests/runtime_neutral"],
      "timeout_seconds": 300,
      "dependencies": ["python", "pytest"],
      "external_network_allowed": false,
      "exclude_risk_tags": ["network", "download", "external_url", "host_install", "host_boundary", "heavy"]
    },
    {
      "id": "runtime_neutral_heavy",
      "description": "Runtime-neutral but expensive install/profile/materialization/canonical-entry checks.",
      "pytest_args": ["tests/runtime_neutral"],
      "timeout_seconds": 900,
      "dependencies": ["python", "pytest", "powershell", "bash", "git"],
      "external_network_allowed": false,
      "include_risk_tags": ["heavy", "host_install"]
    },
    {
      "id": "integration_host_boundary",
      "description": "Integration tests that cross shell, host wrapper, canonical-entry, or platform boundaries.",
      "pytest_args": ["tests/integration"],
      "timeout_seconds": 900,
      "dependencies": ["python", "pytest", "powershell", "bash", "git"],
      "external_network_allowed": false,
      "include_risk_tags": ["host_boundary", "host_install"]
    }
  ],
  "classification": {
    "heavy_file_patterns": [
      "installed_runtime",
      "install_profile",
      "install_generated_nested",
      "generated_nested_bundled",
      "l_xl_native_execution_topology",
      "runtime_delivery_acceptance",
      "workspace_shared_memory_plane"
    ],
    "host_boundary_file_patterns": [
      "canonical_entry",
      "host_runtime",
      "installed_host",
      "powershell",
      "shell_entrypoint",
      "windows_setup"
    ]
  },
  "risk_keywords": [
    {"tag": "network", "keywords": ["requests.", "urllib.", "socket.", "http.client"]},
    {"tag": "download", "keywords": ["download", "curl", "Invoke-WebRequest", "Start-BitsTransfer", "fetch-windows11-eval-iso"]},
    {"tag": "external_url", "keywords": ["http://", "https://"]},
    {"tag": "host_install", "keywords": ["install.ps1", "install.sh", "TargetRoot", ".codex", ".vibeskills"]},
    {"tag": "heavy", "keywords": ["--durations", "runtime_delivery_acceptance", "workspace_shared_memory_plane"]}
  ],
  "artifact_names": {
    "json": "test-baseline-audit.json",
    "markdown": "test-baseline-audit.md"
  }
}
```

- [ ] **Step 4: Create the minimal policy loader**

Create `packages/verification-core/src/vgo_verify/test_baseline_audit.py` with this initial content:

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class PolicyError(ValueError):
    """Raised when the test baseline policy is malformed."""


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_policy(path: Path) -> dict[str, Any]:
    policy = load_json(path)
    layers = policy.get("layers")
    if not isinstance(layers, list) or not layers:
        raise PolicyError("Policy must define at least one layer")

    seen: set[str] = set()
    for layer in layers:
        if not isinstance(layer, dict):
            raise PolicyError("Layer entries must be objects")
        layer_id = str(layer.get("id") or "")
        if not layer_id:
            raise PolicyError("Layer id is required")
        if layer_id in seen:
            raise PolicyError(f"Duplicate layer id: {layer_id}")
        seen.add(layer_id)
        pytest_args = layer.get("pytest_args")
        if not isinstance(pytest_args, list) or not all(isinstance(item, str) and item for item in pytest_args):
            raise PolicyError(f"Layer {layer_id} must define non-empty pytest_args")

    defaults = policy.get("defaults")
    if not isinstance(defaults, dict):
        raise PolicyError("Policy defaults must be an object")
    if bool(defaults.get("external_network_allowed")):
        raise PolicyError("Default external network must remain disabled")
    return policy
```

- [ ] **Step 5: Run the policy tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected:

```text
2 passed
```

- [ ] **Step 6: Commit the policy and loader**

Run:

```powershell
git add config/test-baseline-policy.json packages/verification-core/src/vgo_verify/test_baseline_audit.py tests/runtime_neutral/test_test_baseline_audit.py
git commit -m "test: add test baseline policy contract"
```

---

### Task 2: Add Pytest Collection Parsing And Command Planning

**Files:**

- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`

- [ ] **Step 1: Add failing parser and command tests**

Append these test methods to `TestBaselineAuditPolicyTests` in `tests/runtime_neutral/test_test_baseline_audit.py`:

```python
    def test_parse_collect_output_extracts_node_ids(self) -> None:
        output = "\n".join(
            [
                "tests/unit/test_alpha.py::test_one",
                "tests/unit/test_alpha.py::test_param[value]",
                "tests/runtime_neutral/test_beta.py::BetaTests::test_two",
                "3 tests collected",
            ]
        )

        self.assertEqual(
            [
                "tests/unit/test_alpha.py::test_one",
                "tests/unit/test_alpha.py::test_param[value]",
                "tests/runtime_neutral/test_beta.py::BetaTests::test_two",
            ],
            audit.parse_collect_output(output),
        )

    def test_build_collect_commands_deduplicates_shared_pytest_args(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        commands = audit.build_collect_commands(policy)

        self.assertEqual(3, len(commands))
        command_map = {tuple(item["pytest_args"]): item["command"] for item in commands}
        self.assertEqual(
            [sys.executable, "-m", "pytest", "tests/contract", "tests/unit", "--collect-only", "-q"],
            command_map[("tests/contract", "tests/unit")],
        )
        self.assertEqual(
            [sys.executable, "-m", "pytest", "tests/integration", "--collect-only", "-q"],
            command_map[("tests/integration",)],
        )
        self.assertEqual(["runtime_neutral_fast", "runtime_neutral_heavy"], commands[1]["source_layer_ids"])
```

- [ ] **Step 2: Run the red parser tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected: FAIL because `parse_collect_output` and `build_collect_commands` do not exist.

- [ ] **Step 3: Add collection parser and command builder**

Append these functions to `packages/verification-core/src/vgo_verify/test_baseline_audit.py`:

```python
def parse_collect_output(stdout: str) -> list[str]:
    nodes: list[str] = []
    for raw_line in stdout.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("<") or line.startswith("="):
            continue
        if "::" in line and (line.startswith("tests/") or line.startswith("tests\\")):
            nodes.append(line.replace("\\", "/"))
    return nodes


def layer_by_id(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(layer["id"]): layer for layer in policy["layers"]}


def build_pytest_command(pytest_args: list[str], *, collect_only: bool = False, quiet: str = "-q") -> list[str]:
    command = [__import__("sys").executable, "-m", "pytest", *pytest_args]
    if collect_only:
        command.append("--collect-only")
    if quiet:
        command.append(quiet)
    return command


def build_collect_commands(policy: dict[str, Any]) -> list[dict[str, Any]]:
    quiet = str((policy.get("defaults") or {}).get("pytest_quiet_arg") or "-q")
    by_args: dict[tuple[str, ...], dict[str, Any]] = {}
    commands: list[dict[str, Any]] = []
    for layer in policy["layers"]:
        pytest_args = tuple(str(item) for item in layer["pytest_args"])
        if pytest_args not in by_args:
            item = {
                "source_layer_ids": [],
                "pytest_args": list(pytest_args),
                "command": build_pytest_command(list(pytest_args), collect_only=True, quiet=quiet),
                "timeout_seconds": int(layer.get("timeout_seconds") or (policy.get("defaults") or {}).get("collect_timeout_seconds") or 180),
            }
            by_args[pytest_args] = item
            commands.append(item)
        by_args[pytest_args]["source_layer_ids"].append(str(layer["id"]))
        by_args[pytest_args]["timeout_seconds"] = max(
            int(by_args[pytest_args]["timeout_seconds"]),
            int(layer.get("timeout_seconds") or (policy.get("defaults") or {}).get("collect_timeout_seconds") or 180),
        )
    return commands
```

- [ ] **Step 4: Run the parser and policy tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected:

```text
4 passed
```

- [ ] **Step 5: Commit parser and command planning**

Run:

```powershell
git add packages/verification-core/src/vgo_verify/test_baseline_audit.py tests/runtime_neutral/test_test_baseline_audit.py
git commit -m "test: add baseline collection command planning"
```

---

### Task 3: Add Risk Scanning And Layer Classification

**Files:**

- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`

- [ ] **Step 1: Add failing risk and classification tests**

Append these test methods to `TestBaselineAuditPolicyTests`:

```python
    def test_scan_file_risks_tags_configured_keywords(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "tests" / "runtime_neutral" / "test_download.py"
            path.parent.mkdir(parents=True)
            path.write_text("def test_rejects_before_network():\n    assert 'https://' and 'download'\n", encoding="utf-8")

            risks = audit.scan_file_risks(path, policy)

        self.assertIn("download", risks)
        self.assertIn("external_url", risks)

    def test_classify_known_heavy_runtime_file(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        node = "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile"

        item = audit.classify_node(node, REPO_ROOT, policy)

        self.assertEqual("runtime_neutral_heavy", item["layer_id"])
        self.assertIn("host_install", item["risk_tags"])
        self.assertIn("heavy_file_pattern:install_profile", item["reasons"])

    def test_classify_regular_runtime_neutral_file_as_fast(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        node = "tests/runtime_neutral/test_runtime_contracts.py::test_contract_shape"

        item = audit.classify_node(node, REPO_ROOT, policy)

        self.assertEqual("runtime_neutral_fast", item["layer_id"])
        self.assertEqual("tests/runtime_neutral/test_runtime_contracts.py", item["file"])
```

- [ ] **Step 2: Run the red classification tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected: FAIL because `scan_file_risks` and `classify_node` do not exist.

- [ ] **Step 3: Add path and risk helpers**

Append these helpers to `packages/verification-core/src/vgo_verify/test_baseline_audit.py`:

```python
def node_file(node_id: str) -> str:
    return node_id.split("::", 1)[0].replace("\\", "/")


def path_contains_pattern(path_text: str, pattern: str) -> bool:
    return pattern.lower() in path_text.lower()


def scan_file_risks(path: Path, policy: dict[str, Any]) -> list[str]:
    if not path.exists() or not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    tags: list[str] = []
    for entry in policy.get("risk_keywords") or []:
        tag = str(entry.get("tag") or "")
        keywords = entry.get("keywords") or []
        if tag and any(str(keyword) in text for keyword in keywords):
            tags.append(tag)
    return sorted(set(tags))


def classify_by_path(file_rel: str, policy: dict[str, Any]) -> tuple[str, list[str], list[str]]:
    classification = policy.get("classification") or {}
    risk_tags: list[str] = []
    reasons: list[str] = []

    for pattern in classification.get("heavy_file_patterns") or []:
        pattern_text = str(pattern)
        if path_contains_pattern(file_rel, pattern_text):
            risk_tags.append("heavy")
            if "install" in pattern_text:
                risk_tags.append("host_install")
            reasons.append(f"heavy_file_pattern:{pattern_text}")

    for pattern in classification.get("host_boundary_file_patterns") or []:
        pattern_text = str(pattern)
        if path_contains_pattern(file_rel, pattern_text):
            risk_tags.append("host_boundary")
            reasons.append(f"host_boundary_file_pattern:{pattern_text}")

    if file_rel.startswith("tests/integration/"):
        risk_tags.append("host_boundary")
        reasons.append("integration_root")
        return "integration_host_boundary", sorted(set(risk_tags)), reasons

    if file_rel.startswith("tests/contract/") or file_rel.startswith("tests/unit/"):
        return "contract_unit", sorted(set(risk_tags)), reasons or ["contract_or_unit_root"]

    if "heavy" in risk_tags or "host_install" in risk_tags:
        return "runtime_neutral_heavy", sorted(set(risk_tags)), reasons

    return "runtime_neutral_fast", sorted(set(risk_tags)), reasons or ["runtime_neutral_default"]


def classify_node(node_id: str, repo_root: Path, policy: dict[str, Any]) -> dict[str, Any]:
    file_rel = node_file(node_id)
    layer_id, path_tags, reasons = classify_by_path(file_rel, policy)
    file_tags = scan_file_risks(repo_root / file_rel, policy)
    risk_tags = sorted(set(path_tags + file_tags))
    if any(tag in {"network", "download", "external_url"} for tag in file_tags) and layer_id == "runtime_neutral_fast":
        layer_id = "runtime_neutral_heavy"
        reasons.append("risk_keyword_excluded_from_fast")
    return {
        "node_id": node_id,
        "file": file_rel,
        "layer_id": layer_id,
        "risk_tags": risk_tags,
        "reasons": reasons,
    }
```

- [ ] **Step 4: Run the classification tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected:

```text
7 passed
```

- [ ] **Step 5: Commit classification logic**

Run:

```powershell
git add packages/verification-core/src/vgo_verify/test_baseline_audit.py tests/runtime_neutral/test_test_baseline_audit.py
git commit -m "test: classify baseline test risk layers"
```

---

### Task 4: Add Artifact Construction And Rendering

**Files:**

- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`

- [ ] **Step 1: Add failing artifact tests**

Append these test methods to `TestBaselineAuditPolicyTests`:

```python
    def test_build_artifact_summarizes_layers_and_risks(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        nodes = [
            "tests/unit/test_vgo_verify_repo.py::test_repo_root",
            "tests/runtime_neutral/test_runtime_contracts.py::test_contract_shape",
            "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile",
            "tests/integration/test_runtime_core_packaging_roles.py::test_roles",
        ]

        artifact = audit.build_artifact(
            repo_root=REPO_ROOT,
            policy_path=REPO_ROOT / "config" / "test-baseline-policy.json",
            policy=policy,
            collected_nodes=nodes,
            collection_results=[],
            run_result=None,
        )

        self.assertEqual(4, artifact["summary"]["total_nodes"])
        self.assertEqual(1, artifact["layers"]["contract_unit"]["node_count"])
        self.assertEqual(1, artifact["layers"]["runtime_neutral_fast"]["node_count"])
        self.assertEqual(1, artifact["layers"]["runtime_neutral_heavy"]["node_count"])
        self.assertEqual(1, artifact["layers"]["integration_host_boundary"]["node_count"])
        self.assertIn("host_install", artifact["risks"])

    def test_write_artifacts_emits_json_and_markdown(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        artifact = audit.build_artifact(
            repo_root=REPO_ROOT,
            policy_path=REPO_ROOT / "config" / "test-baseline-policy.json",
            policy=policy,
            collected_nodes=["tests/unit/test_vgo_verify_repo.py::test_repo_root"],
            collection_results=[],
            run_result=None,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            written = audit.write_artifacts(REPO_ROOT, artifact, tempdir)
            json_path = Path(written["json"])
            md_path = Path(written["markdown"])

            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())
            self.assertEqual(1, json.loads(json_path.read_text(encoding="utf-8"))["summary"]["total_nodes"])
            self.assertIn("Test Baseline Audit", md_path.read_text(encoding="utf-8"))
```

- [ ] **Step 2: Run the red artifact tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected: FAIL because `build_artifact` and `write_artifacts` do not exist.

- [ ] **Step 3: Add artifact construction helpers**

Append these imports and helpers to `packages/verification-core/src/vgo_verify/test_baseline_audit.py`:

```python
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def summarize_classified(classified: list[dict[str, Any]], policy: dict[str, Any]) -> tuple[dict[str, Any], dict[str, int]]:
    layers: dict[str, Any] = {
        str(layer["id"]): {
            "description": str(layer.get("description") or ""),
            "node_count": 0,
            "files": [],
            "risk_tags": [],
        }
        for layer in policy["layers"]
    }
    risks: dict[str, int] = {}
    files_by_layer: dict[str, set[str]] = {layer_id: set() for layer_id in layers}
    tags_by_layer: dict[str, set[str]] = {layer_id: set() for layer_id in layers}

    for item in classified:
        layer_id = str(item["layer_id"])
        layers[layer_id]["node_count"] += 1
        files_by_layer[layer_id].add(str(item["file"]))
        for tag in item["risk_tags"]:
            tag_text = str(tag)
            risks[tag_text] = risks.get(tag_text, 0) + 1
            tags_by_layer[layer_id].add(tag_text)

    for layer_id in layers:
        layers[layer_id]["files"] = sorted(files_by_layer[layer_id])
        layers[layer_id]["risk_tags"] = sorted(tags_by_layer[layer_id])
    return layers, dict(sorted(risks.items()))


def build_artifact(
    *,
    repo_root: Path,
    policy_path: Path,
    policy: dict[str, Any],
    collected_nodes: list[str],
    collection_results: list[dict[str, Any]],
    run_result: dict[str, Any] | None,
) -> dict[str, Any]:
    classified = [classify_node(node, repo_root, policy) for node in collected_nodes]
    layers, risks = summarize_classified(classified, policy)
    return {
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "policy_path": str(policy_path),
        "summary": {
            "total_nodes": len(collected_nodes),
            "layer_count": len(layers),
            "risk_tag_count": len(risks),
            "external_network_allowed": bool((policy.get("defaults") or {}).get("external_network_allowed")),
        },
        "collection_results": collection_results,
        "layers": layers,
        "risks": risks,
        "classified": classified,
        "run_result": run_result,
    }
```

- [ ] **Step 4: Add Markdown and write helpers**

Append these helpers to `packages/verification-core/src/vgo_verify/test_baseline_audit.py`:

```python
def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def render_markdown(artifact: dict[str, Any]) -> str:
    lines = [
        "# Test Baseline Audit",
        "",
        f"- Generated At: `{artifact['generated_at']}`",
        f"- Total Nodes: `{artifact['summary']['total_nodes']}`",
        f"- External Network Allowed: `{artifact['summary']['external_network_allowed']}`",
        "",
        "## Layers",
        "",
    ]
    for layer_id, layer in artifact["layers"].items():
        lines.append(f"- `{layer_id}`: nodes=`{layer['node_count']}` files=`{len(layer['files'])}` risks=`{', '.join(layer['risk_tags']) or 'none'}`")
    lines += ["", "## Risks", ""]
    if artifact["risks"]:
        for tag, count in artifact["risks"].items():
            lines.append(f"- `{tag}`: `{count}`")
    else:
        lines.append("- `none`: `0`")
    if artifact.get("run_result"):
        run_result = artifact["run_result"]
        lines += [
            "",
            "## Executed Layer",
            "",
            f"- Layer: `{run_result['layer_id']}`",
            f"- Exit Code: `{run_result['exit_code']}`",
            f"- Command: `{' '.join(run_result['command'])}`",
        ]
    return "\n".join(lines) + "\n"


def write_artifacts(repo_root: Path, artifact: dict[str, Any], output_directory: str | None = None) -> dict[str, str]:
    output_root = Path(output_directory) if output_directory else repo_root / "outputs" / "verify"
    names = {
        "json": "test-baseline-audit.json",
        "markdown": "test-baseline-audit.md",
    }
    json_path = output_root / names["json"]
    md_path = output_root / names["markdown"]
    write_text(json_path, json.dumps(artifact, ensure_ascii=False, indent=2) + "\n")
    write_text(md_path, render_markdown(artifact))
    return {"json": str(json_path), "markdown": str(md_path)}
```

- [ ] **Step 5: Run the artifact tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected:

```text
9 passed
```

- [ ] **Step 6: Commit artifact rendering**

Run:

```powershell
git add packages/verification-core/src/vgo_verify/test_baseline_audit.py tests/runtime_neutral/test_test_baseline_audit.py
git commit -m "test: render test baseline audit artifacts"
```

---

### Task 5: Add CLI, Thin Entrypoint, And Safe Layer Execution

**Files:**

- Modify: `packages/verification-core/src/vgo_verify/test_baseline_audit.py`
- Create: `scripts/verify/test-baseline-audit.py`
- Modify: `tests/runtime_neutral/test_test_baseline_audit.py`

- [ ] **Step 1: Add failing CLI tests**

Append this helper class and tests to `tests/runtime_neutral/test_test_baseline_audit.py`:

```python
class FakeCompletedProcess:
    def __init__(self, args: list[str], returncode: int = 0, stdout: str = "", stderr: str = "") -> None:
        self.args = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class FakeRunner:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def __call__(self, command: list[str], **kwargs: object) -> FakeCompletedProcess:
        self.calls.append({"command": command, "kwargs": kwargs})
        stdout = "\n".join(
            [
                "tests/unit/test_vgo_verify_repo.py::test_repo_root",
                "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile",
                "2 tests collected",
            ]
        )
        if "--collect-only" not in command:
            stdout = "1 passed"
        return FakeCompletedProcess(command, stdout=stdout)


class TestBaselineAuditCliTests(unittest.TestCase):
    def test_collect_only_uses_subprocess_without_running_tests(self) -> None:
        runner = FakeRunner()
        exit_code = audit.main(["--collect-only"], runner=runner)

        self.assertEqual(0, exit_code)
        self.assertEqual(3, len(runner.calls))
        self.assertTrue(all("--collect-only" in call["command"] for call in runner.calls))

    def test_run_layer_sets_disable_network_env(self) -> None:
        runner = FakeRunner()
        exit_code = audit.main(["--run-layer", "contract_unit"], runner=runner)

        self.assertEqual(0, exit_code)
        run_calls = [call for call in runner.calls if "--collect-only" not in call["command"]]
        self.assertEqual(1, len(run_calls))
        env = run_calls[0]["kwargs"]["env"]
        self.assertEqual("1", env["VIBESKILLS_TEST_DISABLE_NETWORK"])
        self.assertEqual(
            [sys.executable, "-m", "pytest", "tests/contract", "tests/unit", "-q"],
            run_calls[0]["command"],
        )
```

- [ ] **Step 2: Run the red CLI tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected: FAIL because `main()` does not accept `runner`, and CLI execution functions do not exist.

- [ ] **Step 3: Add subprocess execution helpers**

Add these imports near the top of `packages/verification-core/src/vgo_verify/test_baseline_audit.py`:

```python
import argparse
import os
import subprocess
import sys

from ._repo import resolve_repo_root as resolve_vco_repo_root
```

Append these helpers:

```python
def resolve_repo_root(start: Path) -> Path:
    return resolve_vco_repo_root(start)


def run_collect_commands(repo_root: Path, policy: dict[str, Any], runner=subprocess.run) -> tuple[list[str], list[dict[str, Any]]]:
    nodes: list[str] = []
    results: list[dict[str, Any]] = []
    for item in build_collect_commands(policy):
        completed = runner(
            item["command"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=item["timeout_seconds"],
        )
        parsed_nodes = parse_collect_output(completed.stdout)
        nodes.extend(parsed_nodes)
        results.append(
            {
                "source_layer_ids": item["source_layer_ids"],
                "command": item["command"],
                "exit_code": int(completed.returncode),
                "node_count": len(parsed_nodes),
                "stderr": completed.stderr,
            }
        )
        if int(completed.returncode) != 0:
            raise RuntimeError(f"pytest collection failed for {item['pytest_args']} with exit code {completed.returncode}")
    return sorted(set(nodes)), results


def build_run_layer_command(policy: dict[str, Any], layer_id: str) -> list[str]:
    layers = layer_by_id(policy)
    if layer_id not in layers:
        raise PolicyError(f"Unknown layer id: {layer_id}")
    quiet = str((policy.get("defaults") or {}).get("pytest_quiet_arg") or "-q")
    return build_pytest_command(list(layers[layer_id]["pytest_args"]), quiet=quiet)


def run_layer(repo_root: Path, policy: dict[str, Any], layer_id: str, runner=subprocess.run) -> dict[str, Any]:
    command = build_run_layer_command(policy, layer_id)
    env = dict(os.environ)
    disable_env = str((policy.get("defaults") or {}).get("disable_network_env") or "VIBESKILLS_TEST_DISABLE_NETWORK")
    env[disable_env] = "1"
    layer = layer_by_id(policy)[layer_id]
    completed = runner(
        command,
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=int(layer.get("timeout_seconds") or 300),
        env=env,
    )
    return {
        "layer_id": layer_id,
        "command": command,
        "exit_code": int(completed.returncode),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "disable_network_env": disable_env,
    }
```

- [ ] **Step 4: Add CLI parser and main**

Append these functions to `packages/verification-core/src/vgo_verify/test_baseline_audit.py`:

```python
def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect, classify, and optionally run Vibe-Skills test baseline layers.")
    parser.add_argument("--policy", default="config/test-baseline-policy.json")
    parser.add_argument("--collect-only", action="store_true", help="Collect and classify tests without executing a layer.")
    parser.add_argument("--run-layer", choices=["contract_unit", "runtime_neutral_fast", "runtime_neutral_heavy", "integration_host_boundary"])
    parser.add_argument("--write-artifacts", action="store_true")
    parser.add_argument("--output-directory")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None, runner=subprocess.run) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = resolve_repo_root(Path(__file__))
    policy_path = (repo_root / args.policy).resolve()
    policy = load_policy(policy_path)
    collected_nodes, collection_results = run_collect_commands(repo_root, policy, runner=runner)
    run_result = None
    if args.run_layer:
        run_result = run_layer(repo_root, policy, args.run_layer, runner=runner)
    artifact = build_artifact(
        repo_root=repo_root,
        policy_path=policy_path,
        policy=policy,
        collected_nodes=collected_nodes,
        collection_results=collection_results,
        run_result=run_result,
    )
    if args.write_artifacts:
        write_artifacts(repo_root, artifact, args.output_directory)
    print(
        f"[INFO] total_nodes={artifact['summary']['total_nodes']} "
        f"layers={artifact['summary']['layer_count']} "
        f"risks={artifact['summary']['risk_tag_count']}"
    )
    if run_result is not None:
        print(f"[INFO] run_layer={run_result['layer_id']} exit_code={run_result['exit_code']}")
        return int(run_result["exit_code"])
    return 0
```

- [ ] **Step 5: Create the repo-facing entrypoint**

Create `scripts/verify/test-baseline-audit.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


CORE_SRC = Path(__file__).resolve().parents[2] / "packages" / "verification-core" / "src"
if str(CORE_SRC) not in sys.path:
    sys.path.insert(0, str(CORE_SRC))

from vgo_verify.test_baseline_audit import (  # noqa: E402
    PolicyError,
    build_artifact,
    build_collect_commands,
    build_run_layer_command,
    classify_node,
    load_policy,
    main,
    parse_collect_output,
    render_markdown,
    run_collect_commands,
    run_layer,
    scan_file_risks,
    write_artifacts,
)

__all__ = [
    "PolicyError",
    "build_artifact",
    "build_collect_commands",
    "build_run_layer_command",
    "classify_node",
    "load_policy",
    "main",
    "parse_collect_output",
    "render_markdown",
    "run_collect_commands",
    "run_layer",
    "scan_file_risks",
    "write_artifacts",
]


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 6: Run the CLI tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected:

```text
11 passed
```

- [ ] **Step 7: Commit CLI and entrypoint**

Run:

```powershell
git add packages/verification-core/src/vgo_verify/test_baseline_audit.py scripts/verify/test-baseline-audit.py tests/runtime_neutral/test_test_baseline_audit.py
git commit -m "test: add test baseline audit runner"
```

---

### Task 6: Validate Audit Runner On The Real Repository Surface

**Files:**

- No source file changes expected.
- Runtime output: `outputs/verify/test-baseline-audit.json`
- Runtime output: `outputs/verify/test-baseline-audit.md`

- [ ] **Step 1: Run focused runner tests**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\runtime_neutral\test_test_baseline_audit.py -q
```

Expected:

```text
11 passed
```

- [ ] **Step 2: Run collect-only audit with artifacts**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python scripts\verify\test-baseline-audit.py --collect-only --write-artifacts
```

Expected:

```text
[INFO] total_nodes=<positive integer> layers=4 risks=<integer>
```

Manual evidence check:

```powershell
Test-Path outputs\verify\test-baseline-audit.json
Test-Path outputs\verify\test-baseline-audit.md
```

Expected:

```text
True
True
```

- [ ] **Step 3: Run contract/unit layer through the runner**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python scripts\verify\test-baseline-audit.py --run-layer contract_unit --write-artifacts
```

Expected: exits with code `0` and prints:

```text
[INFO] run_layer=contract_unit exit_code=0
```

- [ ] **Step 4: Run the direct contract/unit baseline**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests\contract tests\unit -q
```

Expected: exits with code `0`.

- [ ] **Step 5: Re-run routing and terminology guardrails**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
```

Expected summaries:

```text
status=pass
fail_count=0
review_count=0
```

- [ ] **Step 6: Confirm generated evidence is not staged**

Run:

```powershell
git status --short --ignored outputs\verify
```

Expected: `outputs/verify/test-baseline-audit.json` and `outputs/verify/test-baseline-audit.md` may appear as ignored files; neither file may appear as staged or tracked.

- [ ] **Step 7: Commit any final source-only adjustment if validation exposed a narrow source issue**

If validation required a source adjustment, run:

```powershell
git add config/test-baseline-policy.json packages/verification-core/src/vgo_verify/test_baseline_audit.py scripts/verify/test-baseline-audit.py tests/runtime_neutral/test_test_baseline_audit.py
git commit -m "test: stabilize test baseline audit validation"
```

If validation required no source adjustment, do not create a commit in this step.

---

## Self-Review Checklist For Implementer

- Every goal in `docs/superpowers/specs/2026-05-03-test-baseline-stabilization-design.md` maps to a task here:
  - layers and policy: Task 1
  - collect-only parsing and command evidence: Task 2
  - risk scanning and heavy classification: Task 3
  - JSON and Markdown artifacts: Task 4
  - safe `--run-layer contract_unit`: Task 5
  - real repository validation and generated-output boundary: Task 6
- No implementation step installs, deploys, pushes, mutates host roots, changes routing, or writes to the local Codex root.
- Full `tests/runtime_neutral tests/integration` is not claimed green by this plan.
- Generated files under `outputs/verify/` are evidence, not committed source.
- Final completion wording must cite the exact commands that passed in the current execution session.

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-03-test-baseline-stabilization.md`. Two execution options:

**1. Subagent-Driven (recommended)** - Dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
