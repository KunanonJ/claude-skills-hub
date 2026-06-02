# Openworld Evaluation Scenarios

The harness scenarios are intentionally small and auditable.

| Scenario | Candidate | Required evidence |
|---|---|---|
| `browser_form_fill_confirmed` | `browser-use` | confirm_required, replay_handle, rollback_plan, preview_prompt_baseline |
| `browser_navigation_fallback` | `browser-use` | fallback provider, operator owner, evidence_refs, bounded_extraction_plan |
| `desktop_operator_visible_edit` | `Agent-S` | replay_handle, checkpoint corpus, rollback_plan |
| `cross_plane_openworld_bundle` | both | unified task contract, confirm_required, no takeover, provider_preview_note |

All scenarios must remain candidate-only and replayable.

Browser-use scenario notes:

- Use `search_page` for text lookup evidence.
- Use `find_elements` for structure or attribute evidence.
- Do not depend on `read_long_content`; record bounded extraction or fallback.
- Treat gateway/auth/model drift as preview evidence only.
