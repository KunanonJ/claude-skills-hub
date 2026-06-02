# Ops Cockpit Gap Matrix

| plane_id | panel | blocker | evidence_ref | next_action |
| --- | --- | --- | --- | --- |
| `memory-runtime-v2` | `promotion` | ops cockpit summary not yet marked ready on the promotion board | `config/promotion-board.json` | mark cockpit evidence after Wave124 dashboard generation and review |
| `prompt-intelligence` | `release` | release_train_ready is still false | `config/promotion-board.json` | finish release evidence bundle and board review before widening |
| `browserops-provider` | `freshness` | provider evidence needs continuous runtime freshness review | `outputs/verify/vibe-installed-runtime-freshness-gate.json` | re-run freshness and provider soft-rollout gates together |
| `desktopops-shadow` | `replay` | replay evidence exists but still needs operator-visible cockpit surfacing | `outputs/verify/vibe-desktopops-replay-gate.json` | keep replay evidence linked in the cockpit until strict review |
| `docling-document-plane` | `rollback` | rollback evidence must stay visible next to document benchmarks | `outputs/verify/vibe-rollback-drill-gate.json` | keep rollback references present in the release cockpit panel |
