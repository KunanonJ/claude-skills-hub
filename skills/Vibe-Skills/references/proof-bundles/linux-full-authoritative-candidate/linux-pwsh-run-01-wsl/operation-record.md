# WSL Fresh-Machine Proof Run

- Lane: linux-pwsh-run-01-wsl
- Timestamp: 2026-03-13T16:48:39+08:00
- Linux host: Linux DESKTOP-DR94I6D 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
- Repo source: /mnt/d/table/new_ai_table/_ext/vco-skills-codex
- Run root: /tmp/vco-linux-proof-run1
- Target root: /tmp/vco-linux-proof-run1/target-root
- Commands:
  - bash ./scripts/bootstrap/one-shot-setup.sh --profile full --target-root /tmp/vco-linux-proof-run1/target-root
  - bash ./check.sh --profile full --target-root /tmp/vco-linux-proof-run1/target-root --deep
  - pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/verify/vibe-bootstrap-doctor-gate.ps1 -TargetRoot /tmp/vco-linux-proof-run1/target-root -WriteArtifacts
  - python3 ./scripts/verify/runtime_neutral/coherence_gate.py --target-root /tmp/vco-linux-proof-run1/target-root --write-artifacts
