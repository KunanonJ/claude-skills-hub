# Document Failure Taxonomy

Each class must explain which contract field failed and what fallback still remains valid.

| Failure class | Typical trigger | Required remediation |
|---|---|---|
| `provider_contract_violation` | output envelope mismatches Docling contract | emit `failure_object`, preserve provenance, fallback to shadow |
| `ocr_degraded_mode` | OCR-only extraction due to layout loss | label degraded mode, keep artifact bundle, note quality downgrade |
| `artifact_bundle_gap` | missing pages or bundle files | fail closed, request rerun, keep failure evidence |
| `provenance_gap` | source hash or transform lineage missing | stop promotion, re-run with provenance capture |
| `page_alignment_loss` | page ordering or offsets drift | keep failure note and require operator review before release evidence |

Every row must preserve the document plane as the primary contract surface.
