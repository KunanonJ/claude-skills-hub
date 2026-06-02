"""Consumer helper API for datasheet extractions.

Thin wrapper over datasheet_extract_cache. Provides field-level accessors for
IC-aware detectors in kicad, emc, spice, and thermal skills.

Contract:
  - Returns a dict of feature fields on cache hit with sufficient score.
  - Returns None on cache miss, stale entry, low score, or wrong schema version.
  - Individual fields within the dict may be None (datasheet didn't specify).
  - Consumers MUST distinguish None (unknown) from False (explicitly no).

Zero external dependencies — stdlib only.
"""
from __future__ import annotations

from typing import Optional

from datasheet_extract_cache import (
    resolve_extract_dir,
    get_cached_extraction,
    EXTRACTION_VERSION,
    MIN_SCORE,
)


_REGULATOR_TOPOLOGIES = ('boost', 'buck', 'ldo')
_MCU_TOPOLOGIES = ('mcu',)


def _load(mpn, extract_dir=None, analysis_json=None, project_dir=None):
    """Resolve extract dir and load the cached extraction for mpn.

    Returns the extraction dict only if:
      - The entry exists in cache
      - extraction_metadata.extraction_version >= EXTRACTION_VERSION
      - extraction_metadata.score >= MIN_SCORE

    Returns None otherwise.
    """
    if extract_dir is None:
        extract_dir = resolve_extract_dir(
            analysis_json=analysis_json, project_dir=project_dir
        )
    ext = get_cached_extraction(extract_dir, mpn)
    if not ext:
        return None
    meta = ext.get('extraction_metadata') or {}
    if (meta.get('extraction_version') or 0) < EXTRACTION_VERSION:
        return None
    if (meta.get('extraction_score') or 0) < MIN_SCORE:
        return None
    return ext


def _pin_with_function(pins, target_function):
    """Return the first pin whose function matches target_function, or None."""
    for pin in pins or []:
        if pin.get('function') == target_function:
            return pin
    return None


def get_regulator_features(mpn, *, extract_dir=None,
                            analysis_json=None, project_dir=None) -> Optional[dict]:
    """Return regulator-specific features for mpn, or None if not available.

    Returns None when:
      - No extraction is cached for the MPN
      - Extraction is stale (below EXTRACTION_VERSION)
      - Extraction score is below MIN_SCORE
      - Extraction topology is not one of: 'boost', 'buck', 'ldo'

    Returned dict fields (any may be None individually):
      topology:          'boost' | 'buck' | 'ldo'
      has_pg:            bool | None
      has_soft_start:    bool | None
      iss_time_us:       float | None
      en_v_ih_max:       float (V) | None  — from EN pin's threshold_high_v
      en_v_il_min:       float (V) | None  — from EN pin's threshold_low_v
      vin_pin:           str | None        — pin number of the VIN pin
      vout_pin:          str | None
      en_pin:            str | None
      pg_pin:            str | None
    """
    ext = _load(mpn, extract_dir=extract_dir,
                analysis_json=analysis_json, project_dir=project_dir)
    if not ext:
        return None
    topo = ext.get('topology')
    if topo not in _REGULATOR_TOPOLOGIES:
        return None
    pins = ext.get('pins') or []
    features = ext.get('features') or {}
    en_pin = _pin_with_function(pins, 'EN')
    vin_pin = _pin_with_function(pins, 'VIN')
    vout_pin = _pin_with_function(pins, 'VOUT')
    pg_pin = _pin_with_function(pins, 'PG')

    def _pin_number(p):
        if not p:
            return None
        n = p.get('number')
        return str(n) if n is not None else p.get('name')

    return {
        'topology': topo,
        'has_pg': features.get('has_pg'),
        'has_soft_start': features.get('has_soft_start'),
        'iss_time_us': features.get('iss_time_us'),
        'en_v_ih_max': (en_pin or {}).get('threshold_high_v'),
        'en_v_il_min': (en_pin or {}).get('threshold_low_v'),
        'vin_pin': _pin_number(vin_pin),
        'vout_pin': _pin_number(vout_pin),
        'en_pin': _pin_number(en_pin),
        'pg_pin': _pin_number(pg_pin),
    }


def get_mcu_features(mpn, *, extract_dir=None,
                     analysis_json=None, project_dir=None) -> Optional[dict]:
    """Return MCU-specific features for mpn, or None if not available.

    Returns None when:
      - No extraction is cached for the MPN
      - Extraction is stale or below MIN_SCORE
      - Extraction topology is not 'mcu'

    Returned dict fields (any may be None individually):
      usb_speed:              'FS' | 'HS' | 'SS' | None
      has_native_usb_phy:     bool | None
      usb_series_r_required:  bool | None
    """
    ext = _load(mpn, extract_dir=extract_dir,
                analysis_json=analysis_json, project_dir=project_dir)
    if not ext:
        return None
    if ext.get('topology') not in _MCU_TOPOLOGIES:
        return None
    peripherals = ext.get('peripherals') or {}
    usb = peripherals.get('usb') or {}
    return {
        'usb_speed': usb.get('speed'),
        'has_native_usb_phy': usb.get('native_phy'),
        'usb_series_r_required': usb.get('series_r_required'),
    }


def get_pin_function(mpn, pin_identifier, *, extract_dir=None,
                      analysis_json=None, project_dir=None) -> Optional[str]:
    """Return the functional category of a pin ('EN', 'VIN', etc.), or None.

    `pin_identifier` matches against pins[].number (exact) OR pins[].name
    (case-insensitive).
    """
    ext = _load(mpn, extract_dir=extract_dir,
                analysis_json=analysis_json, project_dir=project_dir)
    if not ext:
        return None
    target = str(pin_identifier).strip()
    target_lower = target.lower()
    for p in ext.get('pins') or []:
        if str(p.get('number', '')).strip() == target:
            return p.get('function')
        if str(p.get('name', '')).strip().lower() == target_lower:
            return p.get('function')
    return None


def is_extraction_available(mpn, *, extract_dir=None,
                             analysis_json=None, project_dir=None) -> bool:
    """True iff a v2+, sufficiently-scored extraction exists for mpn."""
    return _load(mpn, extract_dir=extract_dir,
                 analysis_json=analysis_json, project_dir=project_dir) is not None
