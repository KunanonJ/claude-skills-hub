#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def resolve_wrapper_invocation(bridge_executable: str, bridge_args: list[str]) -> list[str]:
    bridge_path = Path(bridge_executable)
    suffix = bridge_path.suffix.lower()

    if os.name == "nt" and suffix in {".cmd", ".bat"}:
        comspec = os.environ.get("COMSPEC") or shutil.which("cmd.exe") or "cmd.exe"
        return [comspec, "/d", "/s", "/c", str(bridge_path), *bridge_args]

    if suffix == ".ps1":
        powershell = (
            shutil.which("pwsh")
            or shutil.which("pwsh.exe")
            or shutil.which("powershell")
            or shutil.which("powershell.exe")
        )
        if powershell:
            return [powershell, "-NoLogo", "-NoProfile", "-File", str(bridge_path), *bridge_args]

    return [str(bridge_path), *bridge_args]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host-adapter", required=True)
    parser.add_argument("--bridge-executable", required=True)
    parser.add_argument("--bridge-contract", default="vco_specialist_wrapper_v1")
    parser.add_argument("-C", "--repo-root", required=True)
    parser.add_argument("--output-schema", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("prompt")
    args = parser.parse_args()

    bridge_args = [
        "--repo-root",
        args.repo_root,
        "--output-schema",
        args.output_schema,
        "--output",
        args.output,
        "--host-adapter",
        args.host_adapter,
        "--bridge-contract",
        args.bridge_contract,
        "--prompt",
        args.prompt,
    ]
    invocation = resolve_wrapper_invocation(args.bridge_executable, bridge_args)

    completed = subprocess.run(
        invocation,
        cwd=args.repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.stdout:
        sys.stdout.write(completed.stdout)
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
