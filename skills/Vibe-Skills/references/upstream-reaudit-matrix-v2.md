# Upstream Re-Audit Matrix v2

Wave99 converts the upstream ledger into a migration-and-ceiling matrix. Wave121 extends the matrix to 19 canonical sources and resolves display-name drift with an explicit alias registry.

| Slug | Lane | Current status | Absorbability | Recommended migration | Promotion ceiling | Remaining value class | Explicit no-go | Next productization asset | Re-audit priority |
|---|---|---|---|---|---|---|---|---|---|
| `docling` | `document_plane_contract` | `canonical_contract` | `canonicalizable` | `keep` | `canonical_contract` | `contract_slice`, `benchmark_slice` | do not build a second document plane | `document failure taxonomy` | `P0` |
| `mem0` | `memory_policy_source` | `shadow_governed` | `shadow_only` | `keep` | `shadow_governed` | `preference_eval_slice`, `operator_sop_slice` | do not let mem0 become primary session or project truth owner | `memory quality eval` | `P0` |
| `letta` | `memory_policy_source` | `partial_absorption` | `selective_harvest_only` | `keep` | `partial_absorption` | `policy_conformance_slice`, `retention_eval_slice` | do not let Letta own runtime memory or compaction authority | `memory quality eval` | `P0` |
| `browser-use` | `browserops_provider_source` | `shadow_governed` | `shadow_only` | `keep` | `shadow_governed` | `openworld_eval_slice`, `provider_preview_slice` | do not let browser-use take over browser execution ownership | `openworld runtime eval` | `P0` |
| `agent-s` | `desktopops_shadow_source` | `shadow_governed` | `shadow_only` | `keep` | `shadow_governed` | `replay_eval_slice`, `desktop_shadow_slice` | do not let Agent-S become the default desktop execution plane | `desktopops replay` | `P0` |
| `awesome-mcp-servers` | `connector_admission` | `catalog_governed` | `catalog_governable` | `keep` | `catalog_governed` | `catalog_slice`, `scorecard_slice` | do not auto-install from the catalog | `connector sandbox simulation` | `P1` |
| `activepieces` | `connector_admission` | `shadow_governed` | `shadow_only` | `keep` | `shadow_governed` | `connector_risk_slice`, `discovery_eval_slice` | do not make Activepieces the default automation control plane | `connector sandbox simulation` | `P1` |
| `composio` | `connector_admission` | `shadow_governed` | `shadow_only` | `keep` | `shadow_governed` | `connector_risk_slice`, `catalog_slice` | do not absorb execution ownership or background action authority | `connector sandbox simulation` | `P1` |
| `prompt-engineering-guide` | `prompt_contract_source` | `partial_absorption` | `selective_harvest_only` | `keep` | `partial_absorption` | `prompt_pattern_slice`, `scorecard_slice` | do not replace VCO prompt/router rules | `prompt intelligence eval` | `P0` |
| `claude-skills` | `skill_catalog_source` | `partial_absorption` | `selective_harvest_only` | `keep` | `partial_absorption` | `skill_harvest_slice`, `scorecard_slice` | do not mirror the whole corpus into canonical runtime | `skill harvest v2` | `P0` |
| `antigravity-awesome-skills` | `skill_catalog_source` | `partial_absorption` | `selective_harvest_only` | `keep` | `partial_absorption` | `skill_harvest_slice` | do not wholesale import all skills | `skill harvest v2` | `P0` |
| `awesome-claude-skills-composio` | `skill_catalog_source` | `partial_absorption` | `selective_harvest_only` | `keep` | `partial_absorption` | `skill_harvest_slice`, `connector_risk_slice` | do not productize Composio-style skills by default | `skill harvest v2` | `P1` |
| `agent-squad` | `role_pack_source` | `tracked_corpus` | `selective_harvest_only` | `advance_to_catalog_governed` | `catalog_governed` | `role_pack_slice`, `handoff_pattern_slice` | do not import a second squad orchestrator | `role pack v2` | `P0` |
| `awesome-claude-code-subagents` | `role_pack_source` | `tracked_corpus` | `selective_harvest_only` | `advance_to_catalog_governed` | `catalog_governed` | `role_pack_slice`, `handoff_pattern_slice` | do not form a second subagent runtime | `role pack v2` | `P0` |
| `awesome-agent-skills` | `skill_catalog_source` | `tracked_corpus` | `selective_harvest_only` | `advance_to_catalog_governed` | `catalog_governed` | `skill_harvest_slice` | do not raw-import the catalog | `skill harvest v2` | `P1` |
| `awesome-ai-agents-e2b` | `discovery_eval_corpus` | `tracked_corpus` | `discovery_reference_only` | `hold_reference` | `tracked_corpus` | `discovery_eval_slice` | do not adopt its agent runtime assumptions | `discovery intake scorecard` | `P2` |
| `awesome-ai-tools` | `discovery_eval_corpus` | `tracked_corpus` | `discovery_reference_only` | `hold_reference` | `tracked_corpus` | `discovery_eval_slice` | do not turn the list into a runtime marketplace | `discovery intake scorecard` | `P2` |
| `awesome-vibe-coding` | `discovery_eval_corpus` | `tracked_corpus` | `discovery_reference_only` | `hold_reference` | `tracked_corpus` | `discovery_eval_slice` | do not create a second vibe methodology control plane | `discovery intake scorecard` | `P2` |
| `vibe-coding-cn` | `discovery_eval_corpus` | `tracked_corpus` | `discovery_reference_only` | `hold_reference` | `tracked_corpus` | `discovery_eval_slice`, `multilingual_pattern_slice` | do not bypass canonical vocabulary governance | `discovery intake scorecard` | `P2` |

The matrix remains evidence for lifecycle and harvest decisions, never a hidden promotion engine.
