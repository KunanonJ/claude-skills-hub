#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_MAIN="${SCRIPT_DIR}/apps/vgo-cli/src/vgo_cli/main.py"
PYTHON_HELPERS_SH="${SCRIPT_DIR}/scripts/common/python_helpers.sh"
PYTHON_MIN_MAJOR=3
PYTHON_MIN_MINOR=10

# run_runtime_freshness_gate semantics are delegated to vgo_cli.main.

source "${PYTHON_HELPERS_SH}"

PYTHON_BIN="$(pick_supported_python || true)"
if [[ -z "${PYTHON_BIN}" ]]; then
  print_python_requirement_error "vgo-cli shell install launcher"
  exit 1
fi

if [[ -f "${CLI_MAIN}" ]]; then
  export PYTHONPATH="${SCRIPT_DIR}/apps/vgo-cli/src${PYTHONPATH:+:${PYTHONPATH}}"
  exec "${PYTHON_BIN}" -m vgo_cli.main install --repo-root "${SCRIPT_DIR}" --frontend shell "$@"
fi

echo "[FAIL] Missing required vgo-cli entrypoint at ${CLI_MAIN}." >&2
echo "[FAIL] The shell install wrapper no longer falls back to legacy installer scripts." >&2
exit 1
