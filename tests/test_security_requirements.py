from __future__ import annotations

from pathlib import Path

from packaging.requirements import Requirement
from packaging.version import Version


ROOT = Path(__file__).resolve().parents[1]


def test_markdown_to_epub_requirements_pins_pygments_to_patched_version() -> None:
    requirements_path = ROOT / "skills" / "markdown-to-epub" / "requirements.txt"
    requirements = [
        Requirement(line)
        for line in requirements_path.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]

    pygments = next(
        requirement for requirement in requirements if requirement.name == "Pygments"
    )

    assert Version("2.20.0") in pygments.specifier
