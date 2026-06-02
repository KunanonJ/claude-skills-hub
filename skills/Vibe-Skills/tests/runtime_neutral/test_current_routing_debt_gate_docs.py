from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_verify_docs_include_current_routing_debt_gate() -> None:
    readme = (REPO_ROOT / "scripts" / "verify" / "README.md").read_text(encoding="utf-8")
    index = (REPO_ROOT / "scripts" / "verify" / "gate-family-index.md").read_text(encoding="utf-8")

    for text in [readme, index]:
        assert "vibe-current-routing-debt-gate.ps1" in text
        assert "current routing debt" in text.lower()


def test_common_verify_sequence_keeps_router_contract_before_debt_gate() -> None:
    readme = (REPO_ROOT / "scripts" / "verify" / "README.md").read_text(encoding="utf-8")
    router_index = readme.index("vibe-router-contract-gate.ps1")
    debt_index = readme.index("vibe-current-routing-debt-gate.ps1")
    assert router_index < debt_index
