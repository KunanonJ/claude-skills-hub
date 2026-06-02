# Docker Fresh-Machine Proof Run

- Lane: linux-pwsh-run-02-docker
- Timestamp: 2026-03-13T10:00:41+00:00
- Repo source: /src
- Run root: /tmp/vco-linux-proof-run2
- Target root: /tmp/vco-linux-proof-run2/target-root
- Commands:
  - apt-get update && apt-get install git python3 nodejs npm powershell
  - bash ./scripts/bootstrap/one-shot-setup.sh --profile full --target-root /tmp/vco-linux-proof-run2/target-root
  - bash ./check.sh --profile full --target-root /tmp/vco-linux-proof-run2/target-root --deep
  - pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/verify/vibe-bootstrap-doctor-gate.ps1 -TargetRoot /tmp/vco-linux-proof-run2/target-root -WriteArtifacts
  - python3 ./scripts/verify/runtime_neutral/coherence_gate.py --target-root /tmp/vco-linux-proof-run2/target-root --write-artifacts
