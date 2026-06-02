---
name: datasheets
description: Extract structured specifications from electronic component datasheet PDFs — pinouts, electrical characteristics, peripherals, topology, and features. Cache extractions per project for consumption by schematic and PCB analyzers. Primary consumer infrastructure for `kicad`, `emc`, `spice`, and `thermal` analyzers. Use this skill whenever the user asks to extract, verify, or read specs from a component datasheet; when analyzers need verified IC knowledge (EN pin thresholds, PG presence, USB peripheral speed); or when a review mentions datasheet coverage, extraction quality, or per-MPN specifications. Also triggers on "extract this datasheet", "what are the specs for MPN X", "verify datasheet extraction", or "check pin functions for part Y".
---

# Datasheets Skill

## Purpose

Extract structured, machine-readable specifications from component datasheet PDFs and make them available to analyzer skills. Works on whatever PDFs are downloaded under `<project>/datasheets/` (downloads are owned by distributor skills like `digikey`, `mouser`, `lcsc`, `element14`).

## Scope

This skill owns:
- **Extraction schema** — the canonical JSON structure for per-MPN specs. Versioned via `EXTRACTION_VERSION` in `scripts/datasheet_extract_cache.py`.
- **PDF page selection** — heuristics to pick pages most likely to contain pinouts, e-chars, applications, SPICE models.
- **Quality scoring** — weighted rubric (pin coverage, voltage ratings, application info, electrical chars, SPICE specs).
- **Consumer API** — helpers in `scripts/datasheet_features.py` for other skills to query specific fields (e.g., `get_regulator_features(mpn)`, `get_mcu_features(mpn)`).
- **Verification** — consistency checks between extracted data and schematic/PCB usage.

## Non-goals

- **No PDF downloading.** That is owned by distributor skills (`digikey`, `mouser`, `lcsc`, `element14`).
- **No global library.** Each project's extractions live in `<project>/datasheets/extracted/`. There is no shared cross-project cache.

## Cache location

```
<project>/
  design.kicad_sch
  datasheets/
    TPS61023DRLR.pdf        # downloaded by distributor skills
    extracted/
      manifest.json         # extraction manifest (legacy name: index.json)
      TPS61023DRLR.json     # structured extraction (this skill's output)
```

## Reference guides

- `references/extraction-schema.md` — canonical schema, every field defined
- `references/field-extraction-guide.md` — how to find each field in datasheets from common vendors (TI, ST, NXP, Espressif, Microchip)
- `references/quality-scoring.md` — rubric details, score thresholds
- `references/consumer-api.md` — how kicad/emc/spice/thermal consume extractions

## Entry-point scripts

- `scripts/datasheet_extract_cache.py` — cache manager, resolver, indexer
- `scripts/datasheet_page_selector.py` — page selection heuristics
- `scripts/datasheet_score.py` — extraction quality scoring
- `scripts/datasheet_verify.py` — cross-check extraction vs schematic usage
- `scripts/datasheet_features.py` — consumer helper API (new in v1.3)

## Extraction workflow

1. User runs an analyzer or requests extraction.
2. This skill checks the cache (`<project>/datasheets/extracted/<MPN>.json`).
3. On cache miss / stale / low score: Claude reads selected PDF pages and extracts structured data.
4. Extraction is scored; if score ≥ 6.0, cached.
5. Consumers query via `datasheet_features.py`.

## When to trigger this skill

- **Immediately after downloading datasheets** via `sync_datasheets_digikey.py`, `sync_datasheets_lcsc.py`, or equivalent. Without extraction, IC-aware checks (VM-001 rail voltage, PS-001 power-good, PR-004 USB, DP-002 USB speed classification) fall back to heuristics on unknown ICs.
- **Before running analyzers on a new project** where datasheets are present but `datasheets/extracted/` is empty — the analyzers won't produce the extractions themselves.
- **When a review flags low trust level** due to missing manufacturer evidence: extracting the ICs referenced by power regulators, MCUs, and high-speed peripherals typically flips `trust_level: low` → `mixed` or `high`.
- **When a user asks for pin verification** ("verify U1 pin names match datasheet") — this skill's cached extraction is the authoritative source.
