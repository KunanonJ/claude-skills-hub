from __future__ import annotations

import json
import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CORE_SRC = REPO_ROOT / "packages" / "verification-core" / "src"
SCRIPT_ENTRYPOINT = REPO_ROOT / "scripts" / "verify" / "test-baseline-audit.py"
if str(CORE_SRC) not in sys.path:
    sys.path.insert(0, str(CORE_SRC))

from vgo_verify import test_baseline_audit as audit


class TestBaselineAuditPolicyTests(unittest.TestCase):
    def test_policy_file_has_expected_layers_and_network_default(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")

        self.assertEqual(1, policy["version"])
        self.assertFalse(policy["defaults"]["external_network_allowed"])
        self.assertEqual(
            [
                "contract_unit",
                "runtime_neutral_fast",
                "runtime_neutral_heavy",
                "runtime_neutral_heavy_install",
                "runtime_neutral_heavy_runtime",
                "runtime_neutral_heavy_router_contract",
                "integration_host_boundary",
            ],
            [layer["id"] for layer in policy["layers"]],
        )
        self.assertEqual(["tests/contract", "tests/unit"], policy["layers"][0]["pytest_args"])

    def test_runtime_neutral_heavy_timeout_has_windows_runtime_budget(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        layers = {layer["id"]: layer for layer in policy["layers"]}

        self.assertGreaterEqual(layers["runtime_neutral_heavy"]["timeout_seconds"], 1800)

    def test_runtime_neutral_heavy_uses_file_serial_diagnostics(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        layers = {layer["id"]: layer for layer in policy["layers"]}

        self.assertEqual("file_serial", layers["runtime_neutral_heavy"]["run_strategy"])
        self.assertGreaterEqual(layers["runtime_neutral_heavy"]["per_file_timeout_seconds"], 300)

    def test_heavy_sublayer_include_patterns_are_parent_heavy_classification_patterns(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        heavy_patterns = set(policy["classification"]["heavy_file_patterns"])

        for layer in policy["layers"]:
            if layer.get("source_layer_id") != "runtime_neutral_heavy":
                continue
            missing = [pattern for pattern in layer.get("include_file_patterns", []) if pattern not in heavy_patterns]
            self.assertEqual([], missing, f"{layer['id']} patterns must classify into runtime_neutral_heavy first")

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

    def test_parse_collect_output_extracts_node_ids(self) -> None:
        output = "\n".join(
            [
                "tests/unit/test_alpha.py::test_one",
                "tests/unit/test_alpha.py::test_param[value]",
                "tests/runtime_neutral/test_beta.py::BetaTests::test_two",
                "packages/runtime-core/src/vgo_runtime/test_lock.py::test_package_node",
                "3 tests collected",
            ]
        )

        self.assertEqual(
            [
                "tests/unit/test_alpha.py::test_one",
                "tests/unit/test_alpha.py::test_param[value]",
                "tests/runtime_neutral/test_beta.py::BetaTests::test_two",
                "packages/runtime-core/src/vgo_runtime/test_lock.py::test_package_node",
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
        self.assertEqual(
            [
                "runtime_neutral_fast",
                "runtime_neutral_heavy",
                "runtime_neutral_heavy_install",
                "runtime_neutral_heavy_runtime",
                "runtime_neutral_heavy_router_contract",
            ],
            commands[1]["source_layer_ids"],
        )

    def test_script_entrypoint_disables_bytecode_before_core_import(self) -> None:
        text = SCRIPT_ENTRYPOINT.read_text(encoding="utf-8")

        disable_index = text.index("sys.dont_write_bytecode = True")
        import_index = text.index("from vgo_verify.test_baseline_audit import")

        self.assertLess(disable_index, import_index)

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

    def test_classify_slow_runtime_invocation_file_as_heavy(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        node = "tests/runtime_neutral/test_multi_host_specialist_execution.py::test_runtime"

        item = audit.classify_node(node, REPO_ROOT, policy)

        self.assertEqual("runtime_neutral_heavy", item["layer_id"])
        self.assertIn("heavy", item["risk_tags"])
        self.assertIn("heavy_file_pattern:multi_host_specialist_execution", item["reasons"])

    def test_classify_regular_runtime_neutral_file_as_fast(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        node = "tests/runtime_neutral/test_runtime_contracts.py::test_contract_shape"

        item = audit.classify_node(node, REPO_ROOT, policy)

        self.assertEqual("runtime_neutral_fast", item["layer_id"])
        self.assertEqual("tests/runtime_neutral/test_runtime_contracts.py", item["file"])

    def test_classify_runtime_neutral_host_install_keyword_is_excluded_from_fast(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            path = root / "tests" / "runtime_neutral" / "test_host_state_keyword.py"
            path.parent.mkdir(parents=True)
            path.write_text("def test_host_state():\n    assert '.vibeskills'\n", encoding="utf-8")

            item = audit.classify_node("tests/runtime_neutral/test_host_state_keyword.py::test_host_state", root, policy)

        self.assertEqual("runtime_neutral_heavy", item["layer_id"])
        self.assertIn("host_install", item["risk_tags"])
        self.assertIn("fast_layer_excluded_risk:host_install", item["reasons"])

    def test_classify_runtime_neutral_host_boundary_path_is_excluded_from_fast(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            path = root / "tests" / "runtime_neutral" / "test_canonical_entry_contract.py"
            path.parent.mkdir(parents=True)
            path.write_text("def test_help():\n    assert True\n", encoding="utf-8")

            item = audit.classify_node("tests/runtime_neutral/test_canonical_entry_contract.py::test_help", root, policy)

        self.assertEqual("integration_host_boundary", item["layer_id"])
        self.assertIn("host_boundary", item["risk_tags"])
        self.assertIn("fast_layer_excluded_risk:host_boundary", item["reasons"])

    def test_select_layer_files_separates_fast_and_heavy_runtime_neutral_files(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        nodes = [
            "tests/runtime_neutral/test_runtime_contracts.py::test_contract_shape",
            "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile",
        ]

        fast_files = audit.select_layer_files(nodes, REPO_ROOT, policy, "runtime_neutral_fast")
        heavy_files = audit.select_layer_files(nodes, REPO_ROOT, policy, "runtime_neutral_heavy")

        self.assertEqual(["tests/runtime_neutral/test_runtime_contracts.py"], fast_files)
        self.assertEqual(["tests/runtime_neutral/test_install_profile_differentiation.py"], heavy_files)

    def test_select_layer_files_splits_heavy_into_targeted_sublayers(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        nodes = [
            "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile",
            "tests/runtime_neutral/test_l_xl_native_execution_topology.py::test_topology",
            "tests/runtime_neutral/test_current_routing_contract_scan.py::test_scan",
        ]

        install_files = audit.select_layer_files(nodes, REPO_ROOT, policy, "runtime_neutral_heavy_install")
        runtime_files = audit.select_layer_files(nodes, REPO_ROOT, policy, "runtime_neutral_heavy_runtime")
        router_files = audit.select_layer_files(nodes, REPO_ROOT, policy, "runtime_neutral_heavy_router_contract")

        self.assertEqual(["tests/runtime_neutral/test_install_profile_differentiation.py"], install_files)
        self.assertEqual(["tests/runtime_neutral/test_l_xl_native_execution_topology.py"], runtime_files)
        self.assertEqual(["tests/runtime_neutral/test_current_routing_contract_scan.py"], router_files)

    def test_heavy_sublayer_union_covers_current_heavy_files(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        nodes, _collection_results = audit.run_collect_commands(REPO_ROOT, policy)

        heavy_selected = set(audit.select_layer_files(nodes, REPO_ROOT, policy, "runtime_neutral_heavy"))
        sublayer_selected: set[str] = set()
        for layer_id in (
            "runtime_neutral_heavy_install",
            "runtime_neutral_heavy_runtime",
            "runtime_neutral_heavy_router_contract",
        ):
            sublayer_selected.update(audit.select_layer_files(nodes, REPO_ROOT, policy, layer_id))

        self.assertGreater(len(heavy_selected), 0)
        self.assertEqual(heavy_selected, sublayer_selected)

    def test_run_collect_commands_reports_layer_context_on_timeout(self) -> None:
        policy = {
            "defaults": {"pytest_quiet_arg": "-q", "collect_timeout_seconds": 7},
            "layers": [
                {
                    "id": "slow_layer",
                    "pytest_args": ["tests/runtime_neutral/test_runtime_contracts.py"],
                    "timeout_seconds": 7,
                }
            ],
        }

        def timeout_runner(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            raise subprocess.TimeoutExpired(
                command,
                kwargs["timeout"],
                output="partial stdout",
                stderr="partial stderr",
            )

        with self.assertRaises(RuntimeError) as raised:
            audit.run_collect_commands(REPO_ROOT, policy, runner=timeout_runner)

        message = str(raised.exception)
        self.assertIn("pytest collection timed out", message)
        self.assertIn("tests/runtime_neutral/test_runtime_contracts.py", message)
        self.assertIn("slow_layer", message)
        self.assertIn("7s", message)
        self.assertIn("partial stdout", message)
        self.assertIn("partial stderr", message)

    def test_build_run_layer_command_uses_classified_files_when_nodes_are_available(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        nodes = [
            "tests/runtime_neutral/test_runtime_contracts.py::test_contract_shape",
            "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile",
        ]

        command = audit.build_run_layer_command(
            policy,
            "runtime_neutral_fast",
            repo_root=REPO_ROOT,
            collected_nodes=nodes,
        )

        self.assertIn("tests/runtime_neutral/test_runtime_contracts.py", command)
        self.assertNotIn("tests/runtime_neutral/test_install_profile_differentiation.py", command)
        self.assertNotIn("tests/runtime_neutral", command)

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
        self.assertEqual(1, artifact["layers"]["runtime_neutral_heavy_install"]["node_count"])
        self.assertEqual(1, artifact["layers"]["integration_host_boundary"]["node_count"])
        self.assertIn("host_install", artifact["risks"])

    def test_write_artifacts_emits_json_and_markdown(self) -> None:
        policy = audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json")
        policy["artifact_names"] = {
            "json": "custom-test-baseline.json",
            "markdown": "custom-test-baseline.md",
        }
        artifact = audit.build_artifact(
            repo_root=REPO_ROOT,
            policy_path=REPO_ROOT / "config" / "test-baseline-policy.json",
            policy=policy,
            collected_nodes=["tests/unit/test_vgo_verify_repo.py::test_repo_root"],
            collection_results=[],
            run_result=None,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            written = audit.write_artifacts(REPO_ROOT, artifact, tempdir, policy=policy)
            json_path = Path(written["json"])
            md_path = Path(written["markdown"])

            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())
            self.assertEqual("custom-test-baseline.json", json_path.name)
            self.assertEqual("custom-test-baseline.md", md_path.name)
            self.assertEqual(1, json.loads(json_path.read_text(encoding="utf-8"))["summary"]["total_nodes"])
            self.assertIn("Test Baseline Audit", md_path.read_text(encoding="utf-8"))

    def test_resolve_repo_root_uses_vco_marker_not_generic_ancestor_config(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            outer = Path(tempdir) / "outer"
            inner = Path(tempdir) / "outer" / "tools" / "Vibe-Skills"
            script_path = inner / "packages" / "verification-core" / "src" / "vgo_verify" / "test_baseline_audit.py"
            (outer / ".git").mkdir(parents=True)
            (outer / "config").mkdir()
            (inner / "config").mkdir(parents=True)
            (inner / "config" / "version-governance.json").write_text("{}\n", encoding="utf-8")
            script_path.parent.mkdir(parents=True)
            script_path.write_text("# fixture\n", encoding="utf-8")

            resolved = audit.resolve_repo_root(script_path)

        self.assertEqual(inner.resolve(), resolved)


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
                "tests/runtime_neutral/test_runtime_contracts.py::test_contract_shape",
                "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile",
                "tests/runtime_neutral/test_l_xl_native_execution_topology.py::test_topology",
                "3 tests collected",
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
        for call in runner.calls:
            env = call["kwargs"]["env"]
            self.assertEqual("1", env["VIBESKILLS_TEST_DISABLE_NETWORK"])
            self.assertEqual("1", env["PYTHONDONTWRITEBYTECODE"])
            self.assertEqual(str(REPO_ROOT / ".tmp" / "pycache"), env["PYTHONPYCACHEPREFIX"])

    def test_collect_only_overrides_run_layer(self) -> None:
        runner = FakeRunner()
        exit_code = audit.main(["--collect-only", "--run-layer", "contract_unit"], runner=runner)

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
        self.assertEqual("1", env["PYTHONDONTWRITEBYTECODE"])
        self.assertEqual(str(REPO_ROOT / ".tmp" / "pycache"), env["PYTHONPYCACHEPREFIX"])
        self.assertEqual(
            [sys.executable, "-m", "pytest", "tests/unit/test_vgo_verify_repo.py", "-q"],
            run_calls[0]["command"],
        )

    def test_run_layer_uses_classified_files_for_requested_layer(self) -> None:
        runner = FakeRunner()
        exit_code = audit.main(["--run-layer", "runtime_neutral_fast"], runner=runner)

        self.assertEqual(0, exit_code)
        run_calls = [call for call in runner.calls if "--collect-only" not in call["command"]]
        self.assertEqual(1, len(run_calls))
        command = run_calls[0]["command"]
        self.assertIn("tests/runtime_neutral/test_runtime_contracts.py", command)
        self.assertNotIn("tests/runtime_neutral/test_install_profile_differentiation.py", command)
        self.assertNotIn("tests/runtime_neutral", command)

    def test_build_run_layer_command_preserves_pytest_options_when_narrowing_to_files(self) -> None:
        policy = copy.deepcopy(audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json"))
        layers = {layer["id"]: layer for layer in policy["layers"]}
        layers["runtime_neutral_fast"]["pytest_args"] = [
            "tests/runtime_neutral",
            "-k",
            "runtime_contracts",
            "--maxfail=1",
        ]
        nodes = [
            "tests/runtime_neutral/test_runtime_contracts.py::test_contract_shape",
            "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile",
        ]

        command = audit.build_run_layer_command(
            policy,
            "runtime_neutral_fast",
            repo_root=REPO_ROOT,
            collected_nodes=nodes,
        )

        self.assertIn("-k", command)
        self.assertEqual("runtime_contracts", command[command.index("-k") + 1])
        self.assertIn("--maxfail=1", command)
        self.assertIn("tests/runtime_neutral/test_runtime_contracts.py", command)
        self.assertNotIn("tests/runtime_neutral", command)

    def test_run_layer_accepts_policy_defined_heavy_sublayer(self) -> None:
        runner = FakeRunner()
        exit_code = audit.main(["--run-layer", "runtime_neutral_heavy_runtime"], runner=runner)

        self.assertEqual(0, exit_code)
        run_calls = [call for call in runner.calls if "--collect-only" not in call["command"]]
        self.assertEqual(1, len(run_calls))
        self.assertEqual(
            [sys.executable, "-m", "pytest", "tests/runtime_neutral/test_l_xl_native_execution_topology.py", "-q"],
            run_calls[0]["command"],
        )

    def test_run_layer_raises_policy_error_for_unknown_layer_without_collected_nodes(self) -> None:
        policy = copy.deepcopy(audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json"))

        with self.assertRaisesRegex(audit.PolicyError, "Unknown layer id: missing_layer"):
            audit.run_layer(
                REPO_ROOT,
                policy,
                "missing_layer",
                collected_nodes=None,
                runner=FakeRunner(),
            )

    def test_run_layer_file_serial_strategy_records_per_file_results(self) -> None:
        policy = copy.deepcopy(audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json"))
        layers = {layer["id"]: layer for layer in policy["layers"]}
        layers["runtime_neutral_heavy"]["run_strategy"] = "file_serial"
        layers["runtime_neutral_heavy"]["per_file_timeout_seconds"] = 123
        runner = FakeRunner()

        result = audit.run_layer(
            REPO_ROOT,
            policy,
            "runtime_neutral_heavy",
            collected_nodes=[
                "tests/runtime_neutral/test_install_profile_differentiation.py::test_profile",
                "tests/runtime_neutral/test_multi_host_specialist_execution.py::test_runtime",
            ],
            runner=runner,
        )

        self.assertEqual(0, result["exit_code"])
        self.assertEqual("file_serial", result["run_strategy"])
        self.assertEqual(2, len(result["file_results"]))
        run_calls = [call for call in runner.calls if "--collect-only" not in call["command"]]
        self.assertEqual(2, len(run_calls))
        self.assertEqual(
            [sys.executable, "-m", "pytest", "tests/runtime_neutral/test_install_profile_differentiation.py", "-q"],
            run_calls[0]["command"],
        )
        self.assertEqual(123, run_calls[0]["kwargs"]["timeout"])
        self.assertIn("tests/runtime_neutral/test_multi_host_specialist_execution.py", result["stdout"])

    def test_run_layer_file_serial_strategy_caps_file_timeout_by_layer_budget(self) -> None:
        policy = copy.deepcopy(audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json"))
        layers = {layer["id"]: layer for layer in policy["layers"]}
        layers["runtime_neutral_heavy"]["run_strategy"] = "file_serial"
        layers["runtime_neutral_heavy"]["timeout_seconds"] = 5
        layers["runtime_neutral_heavy"]["per_file_timeout_seconds"] = 123
        runner = FakeRunner()

        audit.run_layer(
            REPO_ROOT,
            policy,
            "runtime_neutral_heavy",
            collected_nodes=["tests/runtime_neutral/test_install_profile_differentiation.py::test_profile"],
            runner=runner,
        )

        run_calls = [call for call in runner.calls if "--collect-only" not in call["command"]]
        self.assertEqual(5, run_calls[0]["kwargs"]["timeout"])

    def test_run_layer_default_strategy_reports_timeout(self) -> None:
        policy = copy.deepcopy(audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json"))
        layers = {layer["id"]: layer for layer in policy["layers"]}
        layers["contract_unit"]["timeout_seconds"] = 7

        def timeout_runner(command: list[str], **kwargs: object) -> FakeCompletedProcess:
            raise subprocess.TimeoutExpired(command, kwargs["timeout"], output="partial stdout", stderr="partial stderr")

        result = audit.run_layer(
            REPO_ROOT,
            policy,
            "contract_unit",
            runner=timeout_runner,
        )

        self.assertEqual(124, result["exit_code"])
        self.assertEqual(7, result["timeout_seconds"])
        self.assertIn("partial stdout", result["stdout"])
        self.assertIn("partial stderr", result["stderr"])
        self.assertEqual([], result["selected_files"])
        self.assertEqual(0, result["selected_file_count"])

    def test_run_layer_file_serial_strategy_emits_progress_events(self) -> None:
        policy = copy.deepcopy(audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json"))
        layers = {layer["id"]: layer for layer in policy["layers"]}
        layers["runtime_neutral_heavy"]["run_strategy"] = "file_serial"
        runner = FakeRunner()
        events: list[str] = []

        audit.run_layer(
            REPO_ROOT,
            policy,
            "runtime_neutral_heavy",
            collected_nodes=["tests/runtime_neutral/test_install_profile_differentiation.py::test_profile"],
            runner=runner,
            progress=events.append,
        )

        self.assertEqual(
            ["[INFO] start_file tests/runtime_neutral/test_install_profile_differentiation.py"],
            events[:1],
        )
        self.assertIn(
            "[FILE] tests/runtime_neutral/test_install_profile_differentiation.py exit_code=0",
            events[-1],
        )

    def test_run_layer_file_serial_strategy_reports_timeout_file(self) -> None:
        policy = copy.deepcopy(audit.load_policy(REPO_ROOT / "config" / "test-baseline-policy.json"))
        layers = {layer["id"]: layer for layer in policy["layers"]}
        layers["runtime_neutral_heavy"]["run_strategy"] = "file_serial"
        layers["runtime_neutral_heavy"]["per_file_timeout_seconds"] = 7

        def timeout_runner(command: list[str], **kwargs: object) -> FakeCompletedProcess:
            raise subprocess.TimeoutExpired(command, kwargs["timeout"], output="partial stdout", stderr="partial stderr")

        result = audit.run_layer(
            REPO_ROOT,
            policy,
            "runtime_neutral_heavy",
            collected_nodes=["tests/runtime_neutral/test_install_profile_differentiation.py::test_profile"],
            runner=timeout_runner,
        )

        self.assertEqual(124, result["exit_code"])
        self.assertEqual("timeout", result["file_results"][0]["status"])
        self.assertEqual("tests/runtime_neutral/test_install_profile_differentiation.py", result["file_results"][0]["file"])
        self.assertIn("partial stdout", result["stdout"])
        self.assertIn("partial stderr", result["stderr"])

    def test_main_reports_missing_policy_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            missing_policy = Path(tempdir) / "missing-policy.json"
            stderr = tempfile.TemporaryFile(mode="w+", encoding="utf-8")
            try:
                original_stderr = sys.stderr
                sys.stderr = stderr
                exit_code = audit.main(["--policy", str(missing_policy), "--collect-only"], runner=FakeRunner())
            finally:
                sys.stderr = original_stderr
            stderr.seek(0)
            message = stderr.read()
            stderr.close()

        self.assertEqual(2, exit_code)
        self.assertIn("[ERROR]", message)
        self.assertIn("missing-policy.json", message)
        self.assertNotIn("Traceback", message)

    def test_main_reports_collection_failure_without_traceback(self) -> None:
        class FailingCollectRunner(FakeRunner):
            def __call__(self, command: list[str], **kwargs: object) -> FakeCompletedProcess:
                self.calls.append({"command": command, "kwargs": kwargs})
                return FakeCompletedProcess(command, returncode=2, stdout="", stderr="collection failed")

        stderr = tempfile.TemporaryFile(mode="w+", encoding="utf-8")
        try:
            original_stderr = sys.stderr
            sys.stderr = stderr
            exit_code = audit.main(["--collect-only"], runner=FailingCollectRunner())
        finally:
            sys.stderr = original_stderr
        stderr.seek(0)
        message = stderr.read()
        stderr.close()

        self.assertEqual(1, exit_code)
        self.assertIn("[ERROR]", message)
        self.assertIn("pytest collection failed", message)
        self.assertNotIn("Traceback", message)

    def test_script_entrypoint_runs_collect_only(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "packages" / "verification-core" / "src" / "vgo_verify" / "test_baseline_audit.py"),
                "--collect-only",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn("[INFO] total_nodes=", completed.stdout)


if __name__ == "__main__":
    unittest.main()
